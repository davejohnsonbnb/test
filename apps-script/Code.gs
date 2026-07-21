/**
 * IPP × VirtuPro — Commission Finance engine (Google Apps Script)
 * ---------------------------------------------------------------
 * Container-bound to the MASTER workbook (owned by davejohnsonbnb@gmail.com).
 *
 * What it does:
 *   1. Reads Inter Property's Main Claims Tracker (a separate spreadsheet).
 *   2. Finds every WON claim (Status contains "WON" + a Received Amount) that
 *      has NOT already been billed in this workbook.
 *   3. Generates a weekly "CLAIM PAID IPP <MON DD>" tab in Ava's exact layout,
 *      with the TOTAL row and the vIRTUPRO commission line (30% in THB / USD).
 *   4. Keeps a live Dashboard tab with the headline stats.
 *
 * A reservation code counts as "already billed" once it appears in the hidden
 * _Ledger (or in any prior CLAIM PAID IPP tab of this workbook).
 *
 * Nothing is ever written back to the Tracker or Ava's old finance sheet —
 * this engine only reads them and writes inside THIS workbook.
 */

const CONFIG = {
  // ---- Source spreadsheets (read-only) --------------------------------
  TRACKER_ID:      '1h1enX5eOiT1GXtSSeS4kgItizqcdtzr61xc7uTF-wG8', // Main Claims Tracker
  OLD_FINANCE_ID:  '1IHIHQwgFCzWSbN7j0_CRbWV0_c0yxiurL7t40sgrXI8', // Ava's existing finance sheet (for one-time seeding)

  // ---- Business rules -------------------------------------------------
  COMMISSION_RATE: 0.30,          // VirtuPro's cut of the RECEIVED (won) amount
  BILLABLE_REQUIRES_WON_STATUS: true, // true => must say WON *and* have an amount. false => amount alone is enough.
  WON_KEYWORD: 'WON',

  // ---- Naming ---------------------------------------------------------
  WEEKLY_TAB_PREFIX: 'CLAIM PAID IPP', // final tab name = "CLAIM PAID IPP JUL 21"
  LEDGER_SHEET:    '_Ledger',          // hidden: everything already billed
  DASHBOARD_SHEET: 'Dashboard',

  // ---- Misc -----------------------------------------------------------
  RES_CODE_RE: /HM[A-Z0-9]{8}/g,       // Airbnb reservation code (HM + 8 chars)
  FALLBACK_THB_PER_USD: 32.9,          // used only if the live FX lookup fails
  BAHT_FMT:  '"฿"#,##0.00',
  NUM_FMT:   '#,##0.00',
  HEADER_BG: '#b6d7a8',                // green, like Ava's headers
  TOTAL_BG:  '#d9ead3',
};

/* ===================================================================== */
/*  MENU                                                                 */
/* ===================================================================== */

function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('⚙️ VirtuPro Finance')
    .addItem('▶ Generate this week\'s finance tab', 'generateWeeklyTab')
    .addItem('👁 Preview pending (no changes)', 'previewPending')
    .addSeparator()
    .addItem('📊 Refresh dashboard now', 'refreshDashboard')
    .addSeparator()
    .addItem('🌱 Seed "already billed" from Ava\'s sheet', 'seedLedgerFromOldFinance')
    .addItem('🔧 First-time setup', 'setupWorkbook')
    .addToUi();
}

/* ===================================================================== */
/*  SETUP                                                                 */
/* ===================================================================== */

function setupWorkbook() {
  const ss = SpreadsheetApp.getActive();
  ensureLedgerSheet_();
  ensureDashboardSheet_();

  // Daily dashboard refresh so the numbers are always current.
  const have = ScriptApp.getProjectTriggers().some(function (t) {
    return t.getHandlerFunction() === 'refreshDashboard';
  });
  if (!have) {
    ScriptApp.newTrigger('refreshDashboard').timeBased().everyDays(1).atHour(6).create();
  }

  refreshDashboard();
  SpreadsheetApp.getUi().alert(
    'Setup complete ✅',
    'Created the Dashboard + hidden _Ledger, and scheduled a daily dashboard refresh.\n\n' +
    'Next steps:\n' +
    '  1. Run "Seed already billed from Ava\'s sheet" once (marks history as done).\n' +
    '  2. Use "Preview pending" to check, then "Generate this week\'s finance tab".',
    SpreadsheetApp.getUi().ButtonSet.OK);
}

function ensureLedgerSheet_() {
  const ss = SpreadsheetApp.getActive();
  let sh = ss.getSheetByName(CONFIG.LEDGER_SHEET);
  if (!sh) {
    sh = ss.insertSheet(CONFIG.LEDGER_SHEET);
    sh.getRange(1, 1, 1, 4)
      .setValues([['Reservation Code', 'Received Amount', 'Billed In Tab', 'Date Billed']])
      .setFontWeight('bold');
    sh.setFrozenRows(1);
  }
  sh.hideSheet();
  return sh;
}

function ensureDashboardSheet_() {
  const ss = SpreadsheetApp.getActive();
  let sh = ss.getSheetByName(CONFIG.DASHBOARD_SHEET);
  if (!sh) sh = ss.insertSheet(CONFIG.DASHBOARD_SHEET, 0);
  return sh;
}

/* ===================================================================== */
/*  READ THE TRACKER                                                     */
/* ===================================================================== */

/**
 * Locate the Claims tab by content (a header row containing "Reservation
 * Code" and "Status"), then map columns by header text so the code keeps
 * working even if columns get reordered.
 */
function readTrackerClaims_() {
  const src = SpreadsheetApp.openById(CONFIG.TRACKER_ID);
  const sheets = src.getSheets();

  for (let s = 0; s < sheets.length; s++) {
    const sheet = sheets[s];
    const maxRows = Math.min(8, sheet.getLastRow());
    if (maxRows < 1) continue;
    const lastCol = sheet.getLastColumn();
    const probe = sheet.getRange(1, 1, maxRows, lastCol).getValues();

    for (let r = 0; r < probe.length; r++) {
      const header = probe[r].map(function (h) { return String(h).trim().toLowerCase(); });
      const hasCode = header.indexOf('reservation code') > -1;
      const hasStatus = header.indexOf('status') > -1;
      if (!hasCode || !hasStatus) continue;

      // Found the header row.
      const col = mapHeaders_(header);
      const firstDataRow = r + 2; // 1-indexed sheet row
      const n = sheet.getLastRow() - firstDataRow + 1;
      if (n <= 0) return { claims: [], sheetName: sheet.getName() };
      const rows = sheet.getRange(firstDataRow, 1, n, lastCol).getValues();

      const claims = [];
      for (let i = 0; i < rows.length; i++) {
        const row = rows[i];
        const code = String(row[col.code] || '').trim().toUpperCase().replace(/\s+/g, '');
        if (!/^HM[A-Z0-9]{8}$/.test(code)) continue; // skip blanks / junk rows
        claims.push({
          property: String(row[col.property] || '').trim(),
          guest:    String(row[col.guest] || '').trim(),
          code:     code,
          ci:       String(row[col.ci] || '').trim(),
          co:       String(row[col.co] || '').trim(),
          claim:    parseAmount_(row[col.claim]),
          status:   String(row[col.status] || '').trim(),
          received: parseAmount_(row[col.received]),
          rowNum:   firstDataRow + i,
        });
      }
      return { claims: claims, sheetName: sheet.getName() };
    }
  }
  throw new Error('Could not find a Claims tab (a header row with "Reservation Code" and "Status") in the Tracker.');
}

function mapHeaders_(header) {
  function find(names) {
    for (let k = 0; k < names.length; k++) {
      const idx = header.indexOf(names[k]);
      if (idx > -1) return idx;
    }
    return -1;
  }
  return {
    property: find(['property']),
    guest:    find(['guest name', 'guest']),
    code:     find(['reservation code']),
    ci:       find(['ci date', 'check-in', 'checkin']),
    co:       find(['co date', 'check-out', 'checkout']),
    claim:    find(['claim amount', 'claim amount (thb)']),
    status:   find(['status']),
    received: find(['recieved amount', 'received amount']), // NB: sheet spells it "Recieved"
  };
}

function parseAmount_(v) {
  if (v === null || v === undefined || v === '') return null;
  if (typeof v === 'number') return isNaN(v) ? null : v;
  const cleaned = String(v).replace(/[^0-9.\-]/g, '');
  if (cleaned === '' || cleaned === '-' || cleaned === '.') return null;
  const n = parseFloat(cleaned);
  return isNaN(n) ? null : n;
}

/* ===================================================================== */
/*  BILLED / PENDING LOGIC                                                */
/* ===================================================================== */

function statusIsWon_(status) {
  return String(status).toUpperCase().indexOf(CONFIG.WON_KEYWORD) > -1;
}

function isBillable_(c) {
  const hasAmount = c.received !== null && c.received > 0;
  if (!hasAmount) return false;
  if (CONFIG.BILLABLE_REQUIRES_WON_STATUS) return statusIsWon_(c.status);
  return true;
}

/** All reservation codes already billed: the _Ledger plus any prior weekly tab. */
function getBilledCodes_() {
  const ss = SpreadsheetApp.getActive();
  const billed = {};

  const ledger = ss.getSheetByName(CONFIG.LEDGER_SHEET);
  if (ledger && ledger.getLastRow() > 1) {
    ledger.getRange(2, 1, ledger.getLastRow() - 1, 1).getValues().forEach(function (r) {
      const code = String(r[0]).trim().toUpperCase();
      if (code) billed[code] = true;
    });
  }

  ss.getSheets().forEach(function (sh) {
    if (sh.getName().indexOf(CONFIG.WEEKLY_TAB_PREFIX) !== 0) return;
    const values = sh.getDataRange().getValues();
    values.forEach(function (row) {
      row.forEach(function (cell) {
        const m = String(cell).toUpperCase().match(CONFIG.RES_CODE_RE);
        if (m) m.forEach(function (code) { billed[code] = true; });
      });
    });
  });
  return billed;
}

/** Won-but-unbilled claims, plus data-quality warnings. */
function computePending_() {
  const data = readTrackerClaims_();
  const billed = getBilledCodes_();

  const pending = [];
  const seen = {};
  const warnings = { wonNoAmount: [], amountNotWon: [], duplicates: [] };

  data.claims.forEach(function (c) {
    const won = statusIsWon_(c.status);
    const hasAmount = c.received !== null && c.received > 0;

    if (won && !hasAmount) warnings.wonNoAmount.push(c);
    if (hasAmount && !won && CONFIG.BILLABLE_REQUIRES_WON_STATUS) warnings.amountNotWon.push(c);

    if (!isBillable_(c)) return;
    if (billed[c.code]) return;              // already billed in a prior tab
    if (seen[c.code]) { warnings.duplicates.push(c); return; }
    seen[c.code] = true;
    pending.push(c);
  });

  return { pending: pending, warnings: warnings, trackerSheet: data.sheetName, allClaims: data.claims };
}

/* ===================================================================== */
/*  PREVIEW (read-only)                                                   */
/* ===================================================================== */

function previewPending() {
  const res = computePending_();
  const totalReceived = res.pending.reduce(function (a, c) { return a + c.received; }, 0);
  const commission = totalReceived * CONFIG.COMMISSION_RATE;

  let html = '<div style="font-family:Arial;font-size:13px">';
  html += '<h3 style="margin:0 0 6px">Pending commission — ' + res.pending.length + ' claim(s)</h3>';
  html += '<p style="margin:0 0 10px">Tracker tab read: <b>' + res.trackerSheet + '</b><br>' +
          'Total received: <b>฿' + fmt_(totalReceived) + '</b> &nbsp;|&nbsp; ' +
          'VirtuPro 30%: <b>฿' + fmt_(commission) + '</b></p>';

  if (res.pending.length) {
    html += '<table style="border-collapse:collapse;font-size:12px">' +
            '<tr style="background:#b6d7a8"><th style="border:1px solid #ccc;padding:3px">Code</th>' +
            '<th style="border:1px solid #ccc;padding:3px">Guest</th>' +
            '<th style="border:1px solid #ccc;padding:3px">Property</th>' +
            '<th style="border:1px solid #ccc;padding:3px">Received</th></tr>';
    res.pending.forEach(function (c) {
      html += '<tr><td style="border:1px solid #ccc;padding:3px">' + c.code + '</td>' +
              '<td style="border:1px solid #ccc;padding:3px">' + esc_(c.guest) + '</td>' +
              '<td style="border:1px solid #ccc;padding:3px">' + esc_(c.property) + '</td>' +
              '<td style="border:1px solid #ccc;padding:3px;text-align:right">฿' + fmt_(c.received) + '</td></tr>';
    });
    html += '</table>';
  }

  const w = res.warnings;
  if (w.wonNoAmount.length || w.amountNotWon.length || w.duplicates.length) {
    html += '<h4 style="margin:12px 0 4px">⚠ Please check</h4><ul style="margin:0">';
    if (w.wonNoAmount.length)
      html += '<li>' + w.wonNoAmount.length + ' marked WON but no Received Amount (can\'t bill yet): ' +
              w.wonNoAmount.map(function (c) { return c.code; }).join(', ') + '</li>';
    if (w.amountNotWon.length)
      html += '<li>' + w.amountNotWon.length + ' have a Received Amount but Status isn\'t WON (mislabel?): ' +
              w.amountNotWon.map(function (c) { return c.code; }).join(', ') + '</li>';
    if (w.duplicates.length)
      html += '<li>' + w.duplicates.length + ' duplicate reservation code(s): ' +
              w.duplicates.map(function (c) { return c.code; }).join(', ') + '</li>';
    html += '</ul>';
  }
  html += '<p style="margin:12px 0 0;color:#666">Nothing has been changed. Use “Generate this week\'s finance tab” to write it.</p></div>';

  SpreadsheetApp.getUi().showModalDialog(
    HtmlService.createHtmlOutput(html).setWidth(640).setHeight(560),
    'Preview — pending commission');
}

/* ===================================================================== */
/*  GENERATE THE WEEKLY FINANCE TAB (Ava's exact layout)                 */
/* ===================================================================== */

function generateWeeklyTab() {
  const ui = SpreadsheetApp.getUi();
  const res = computePending_();
  if (!res.pending.length) {
    ui.alert('Nothing to bill', 'No won-but-unbilled claims were found in the Tracker.', ui.ButtonSet.OK);
    return;
  }

  const ss = SpreadsheetApp.getActive();
  ensureLedgerSheet_();

  const tz = ss.getSpreadsheetTimeZone();
  const label = Utilities.formatDate(new Date(), tz, 'MMM d').toUpperCase(); // e.g. "JUL 21"
  const tabName = uniqueSheetName_(CONFIG.WEEKLY_TAB_PREFIX + ' ' + label);
  const monthDue = Utilities.formatDate(new Date(), tz, 'MMMM');

  const sh = ss.insertSheet(tabName, ss.getNumSheets());

  // ---- Header (matches Ava: A..I) ------------------------------------
  const header = ['#', 'Reservation Code', 'Guest', 'Property',
                  'Claim Amount (THB)', 'Status', 'Payment due', 'Recieved Amount', 'Paid?'];
  sh.getRange(1, 1, 1, header.length).setValues([header])
    .setFontWeight('bold').setBackground(CONFIG.HEADER_BG)
    .setHorizontalAlignment('center');

  // ---- Rows -----------------------------------------------------------
  const rows = res.pending.map(function (c, i) {
    return [i + 1, c.code, c.guest, c.property, c.received, 'WON', monthDue, c.received, false];
  });
  sh.getRange(2, 1, rows.length, header.length).setValues(rows);

  const lastRow = 1 + rows.length;
  sh.getRange(2, 5, rows.length, 1).setNumberFormat(CONFIG.NUM_FMT); // E Claim Amount
  sh.getRange(2, 8, rows.length, 1).setNumberFormat(CONFIG.BAHT_FMT); // H Received
  sh.getRange(2, 9, rows.length, 1).insertCheckboxes();               // I Paid?

  const totalReceived = res.pending.reduce(function (a, c) { return a + c.received; }, 0);

  // ---- TOTAL row ------------------------------------------------------
  const totalRow = lastRow + 1;
  sh.getRange(totalRow, 4).setValue('TOTAL').setFontWeight('bold');
  sh.getRange(totalRow, 5).setValue(totalReceived).setNumberFormat(CONFIG.NUM_FMT).setFontWeight('bold');
  sh.getRange(totalRow, 8).setValue(totalReceived).setNumberFormat(CONFIG.BAHT_FMT).setFontWeight('bold');
  sh.getRange(totalRow, 1, 1, header.length).setBackground(CONFIG.TOTAL_BG);

  // ---- vIRTUPRO commission row (THB / USD) ----------------------------
  const commission = totalReceived * CONFIG.COMMISSION_RATE;
  const thbPerUsd = getThbPerUsd_();
  const usd = commission / thbPerUsd;
  const commRow = totalRow + 1;
  sh.getRange(commRow, 4).setValue('vIRTUPRO').setFontWeight('bold');
  sh.getRange(commRow, 5)
    .setValue('฿' + fmt_(commission) + ' / $' + fmt_(usd))
    .setFontWeight('bold').setBackground(CONFIG.TOTAL_BG);
  sh.getRange(commRow, 6).setValue('(30% of received · FX ' + thbPerUsd.toFixed(2) + ' THB/USD)')
    .setFontColor('#666').setFontStyle('italic');

  // ---- Cosmetics ------------------------------------------------------
  sh.setFrozenRows(1);
  sh.setColumnWidth(2, 120); sh.setColumnWidth(3, 150); sh.setColumnWidth(4, 260);
  try { sh.autoResizeColumns(5, 4); } catch (e) {}

  // ---- Record in ledger so these never bill twice --------------------
  appendToLedger_(res.pending, tabName);

  refreshDashboard();
  ss.setActiveSheet(sh);
  ss.toast(res.pending.length + ' claim(s) billed · ฿' + fmt_(commission) + ' commission', 'Tab created: ' + tabName, 8);
}

function appendToLedger_(pending, tabName) {
  const sh = ensureLedgerSheet_();
  const now = new Date();
  const rows = pending.map(function (c) { return [c.code, c.received, tabName, now]; });
  sh.getRange(sh.getLastRow() + 1, 1, rows.length, 4).setValues(rows);
}

function uniqueSheetName_(base) {
  const ss = SpreadsheetApp.getActive();
  let name = base, i = 2;
  while (ss.getSheetByName(name)) { name = base + ' (' + i + ')'; i++; }
  return name;
}

/* ===================================================================== */
/*  SEED "ALREADY BILLED" FROM AVA'S EXISTING FINANCE SHEET              */
/* ===================================================================== */

function seedLedgerFromOldFinance() {
  const ui = SpreadsheetApp.getUi();
  const resp = ui.alert(
    'Seed already-billed history',
    'This scans Ava\'s existing finance sheet and marks every reservation code found there as ' +
    '"already billed", so your first weekly run only shows the genuinely un-billed claims.\n\n' +
    'The "FROM CLAIM SUPPORT" tab is ignored. Continue?',
    ui.ButtonSet.OK_CANCEL);
  if (resp !== ui.Button.OK) return;

  const old = SpreadsheetApp.openById(CONFIG.OLD_FINANCE_ID);
  const codes = {};
  old.getSheets().forEach(function (sh) {
    if (/from claim support/i.test(sh.getName())) return; // ignore, per instruction
    if (sh.getLastRow() < 1) return;
    sh.getDataRange().getValues().forEach(function (row) {
      row.forEach(function (cell) {
        const m = String(cell).toUpperCase().match(CONFIG.RES_CODE_RE);
        if (m) m.forEach(function (code) { codes[code] = true; });
      });
    });
  });

  const ledger = ensureLedgerSheet_();
  const existing = {};
  if (ledger.getLastRow() > 1) {
    ledger.getRange(2, 1, ledger.getLastRow() - 1, 1).getValues()
      .forEach(function (r) { existing[String(r[0]).trim().toUpperCase()] = true; });
  }
  const toAdd = Object.keys(codes).filter(function (c) { return !existing[c]; });
  if (toAdd.length) {
    const now = new Date();
    ledger.getRange(ledger.getLastRow() + 1, 1, toAdd.length, 4)
      .setValues(toAdd.map(function (c) { return [c, '', 'SEED (Ava sheet)', now]; }));
  }
  refreshDashboard();
  ui.alert('Seeding done ✅', 'Marked ' + toAdd.length + ' reservation code(s) as already billed.', ui.ButtonSet.OK);
}

/* ===================================================================== */
/*  DASHBOARD                                                             */
/* ===================================================================== */

function refreshDashboard() {
  const ss = SpreadsheetApp.getActive();
  const sh = ensureDashboardSheet_();
  const data = readTrackerClaims_();
  const billed = getBilledCodes_();

  let won = 0, lost = 0, progress = 0, claimedTotal = 0, recoveredTotal = 0;
  let pendingCount = 0, pendingReceived = 0, billedReceived = 0;
  const byMonth = {}, byProperty = {};

  data.claims.forEach(function (c) {
    if (c.claim) claimedTotal += c.claim;
    const hasAmount = c.received !== null && c.received > 0;
    const isWon = hasAmount || statusIsWon_(c.status);
    const isLost = !hasAmount && /reject|lost|not eligible|wrong guest|ineligible/i.test(c.status);

    if (isWon && hasAmount) {
      won++;
      recoveredTotal += c.received;
      const m = monthKey_(c.co);
      byMonth[m] = (byMonth[m] || 0) + c.received;
      const p = propCode_(c.property);
      byProperty[p] = (byProperty[p] || 0) + c.received;
      if (billed[c.code]) billedReceived += c.received;
      else { pendingCount++; pendingReceived += c.received; }
    } else if (isLost) {
      lost++;
    } else {
      progress++;
    }
  });

  const total = data.claims.length;
  const winRate = (won + lost) ? won / (won + lost) : 0;
  const recRate = claimedTotal ? recoveredTotal / claimedTotal : 0;
  const commissionEarned = recoveredTotal * CONFIG.COMMISSION_RATE;
  const commissionBilled = billedReceived * CONFIG.COMMISSION_RATE;
  const commissionPending = pendingReceived * CONFIG.COMMISSION_RATE;
  const thbPerUsd = getThbPerUsd_();

  sh.clear();
  sh.getRange(1, 1).setValue('Inter Property × VirtuPro — Live Dashboard')
    .setFontSize(16).setFontWeight('bold');
  sh.getRange(2, 1).setValue('Last refreshed: ' +
    Utilities.formatDate(new Date(), ss.getSpreadsheetTimeZone(), 'yyyy-MM-dd HH:mm') +
    '  ·  FX ' + thbPerUsd.toFixed(2) + ' THB/USD')
    .setFontColor('#666');

  const tiles = [
    ['Total claims', total,                                   'Claims won', won],
    ['Claims lost', lost,                                     'In progress', progress],
    ['Win rate', pct_(winRate),                               'Recovery rate', pct_(recRate)],
    ['Total claimed', '฿' + fmt_(claimedTotal),              'Total recovered', '฿' + fmt_(recoveredTotal)],
    ['Commission earned (30%)', '฿' + fmt_(commissionEarned), 'Commission earned ($)', '$' + fmt_(commissionEarned / thbPerUsd)],
    ['Commission billed', '฿' + fmt_(commissionBilled),      'Commission PENDING', '฿' + fmt_(commissionPending)],
    ['⏳ Pending claims (unbilled)', pendingCount,            'Pending received', '฿' + fmt_(pendingReceived)],
  ];
  let row = 4;
  tiles.forEach(function (t) {
    sh.getRange(row, 1).setValue(t[0]).setFontColor('#666');
    sh.getRange(row, 2).setValue(t[1]).setFontWeight('bold').setFontSize(12);
    sh.getRange(row, 4).setValue(t[2]).setFontColor('#666');
    sh.getRange(row, 5).setValue(t[3]).setFontWeight('bold').setFontSize(12);
    row++;
  });
  // Highlight the pending row
  sh.getRange(row - 1, 1, 1, 5).setBackground('#fff2cc');

  // ---- Monthly recovered table + chart -------------------------------
  const monthRow = row + 2;
  sh.getRange(monthRow, 1).setValue('Recovered by month').setFontWeight('bold');
  const months = Object.keys(byMonth).sort(monthSort_);
  const monthData = [['Month', 'Recovered (฿)']].concat(months.map(function (m) { return [m, byMonth[m]]; }));
  if (monthData.length > 1) {
    const mRange = sh.getRange(monthRow + 1, 1, monthData.length, 2);
    mRange.setValues(monthData);
    sh.getRange(monthRow + 2, 2, monthData.length - 1, 1).setNumberFormat(CONFIG.BAHT_FMT);
    buildChart_(sh, mRange, Charts.ChartType.COLUMN, 'Recovered by month', monthRow, 7);
  }

  // ---- Top properties table + chart ----------------------------------
  const props = Object.keys(byProperty).sort(function (a, b) { return byProperty[b] - byProperty[a]; }).slice(0, 10);
  const propStart = monthRow + monthData.length + 3;
  sh.getRange(propStart, 1).setValue('Top properties by recovered').setFontWeight('bold');
  const propData = [['Property', 'Recovered (฿)']].concat(props.map(function (p) { return [p, byProperty[p]]; }));
  if (propData.length > 1) {
    const pRange = sh.getRange(propStart + 1, 1, propData.length, 2);
    pRange.setValues(propData);
    sh.getRange(propStart + 2, 2, propData.length - 1, 1).setNumberFormat(CONFIG.BAHT_FMT);
    buildChart_(sh, pRange, Charts.ChartType.BAR, 'Top properties', propStart, 7);
  }

  sh.setColumnWidth(1, 210); sh.setColumnWidth(2, 150);
  sh.setColumnWidth(4, 200); sh.setColumnWidth(5, 150);
}

function buildChart_(sh, range, type, title, anchorRow, anchorCol) {
  try {
    sh.getCharts().forEach(function (ch) {
      // remove an existing chart with the same title to avoid stacking on refresh
      if (ch.getOptions().get('title') === title) sh.removeChart(ch);
    });
    const chart = sh.newChart().addRange(range).setChartType(type)
      .setPosition(anchorRow, anchorCol, 0, 0)
      .setOption('title', title).setOption('legend', { position: 'none' })
      .setOption('width', 460).setOption('height', 240).build();
    sh.insertChart(chart);
  } catch (e) { /* charts are best-effort */ }
}

/* ===================================================================== */
/*  HELPERS                                                               */
/* ===================================================================== */

function getThbPerUsd_() {
  const cache = CacheService.getScriptCache();
  const key = 'thbPerUsd_' + Utilities.formatDate(new Date(), 'UTC', 'yyyy-MM-dd');
  const hit = cache.get(key);
  if (hit) return parseFloat(hit);
  try {
    const resp = UrlFetchApp.fetch('https://open.er-api.com/v6/latest/USD', { muteHttpExceptions: true });
    const json = JSON.parse(resp.getContentText());
    const rate = json && json.rates && json.rates.THB;
    if (rate && rate > 0) { cache.put(key, String(rate), 21600); return rate; }
  } catch (e) { /* fall through */ }
  return CONFIG.FALLBACK_THB_PER_USD;
}

var MONTHS_ = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec'];
function monthKey_(dateStr) {
  const m = String(dateStr).toLowerCase().match(/jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec/);
  if (!m) return 'Unknown';
  return m[0].charAt(0).toUpperCase() + m[0].slice(1);
}
function monthSort_(a, b) {
  const ia = MONTHS_.indexOf(String(a).toLowerCase().slice(0, 3));
  const ib = MONTHS_.indexOf(String(b).toLowerCase().slice(0, 3));
  return (ia < 0 ? 99 : ia) - (ib < 0 ? 99 : ib);
}
function propCode_(name) {
  const matches = String(name).toUpperCase().match(/[VC]\s?-?\s?\d{1,3}/g);
  if (matches && matches.length) return matches[matches.length - 1].replace(/[\s-]/g, '');
  const t = String(name).trim();
  return t ? t.slice(0, 24) : 'Unknown';
}
function fmt_(n) { return Utilities.formatString('%s', (Math.round(n * 100) / 100).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })); }
function pct_(x) { return (Math.round(x * 1000) / 10) + '%'; }
function esc_(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
