# IPP × VirtuPro — Commission Finance (Apps Script)

Automates VirtuPro's weekly commission reconciliation for Inter Property Phuket.
Runs entirely inside a single Google Sheet (the **master workbook**), owned by
`davejohnsonbnb@gmail.com`.

## What it does

- Reads the **Main Claims Tracker** (a separate spreadsheet — read only).
- Finds every **WON** claim (Status contains `WON` **and** a Received Amount is
  filled) that has **not already been billed** in the master workbook.
- Writes a weekly **`CLAIM PAID IPP <MON DD>`** tab in Ava's exact layout, with
  the `TOTAL` row and the **`vIRTUPRO` commission line (30% in THB / USD)** at the
  day's live FX rate.
- Maintains a live **Dashboard** tab (win rate, recovered, commission earned,
  billed vs. pending, monthly trend, top properties).
- Never writes to the Tracker or to Ava's old finance sheet.

A reservation code is considered **already billed** once it appears in the hidden
`_Ledger` sheet or in any prior `CLAIM PAID IPP` tab.

## One-time setup

1. Create a new Google Sheet in your Drive (this becomes the **master workbook**).
   Name it e.g. `IPP × VirtuPro — Commission Finance (Master)`.
2. In that sheet: **Extensions → Apps Script**.
3. Delete the sample `myFunction` code, paste the full contents of **`Code.gs`**.
4. Click the ⚙️ **Project Settings** gear → tick **“Show `appsscript.json`”**,
   then open the `appsscript.json` file in the editor and replace it with the one
   in this folder (sets the timezone + permissions).
5. **Save** (💾). Reload the spreadsheet tab.
6. A new menu **⚙️ VirtuPro Finance** appears. Run **🔧 First-time setup**
   → approve the Google permission prompt (it's your own script).
7. Run **🌱 Seed "already billed" from Ava's sheet** once, so history is marked
   done and only genuinely un-billed claims show up.

## Weekly use

- **👁 Preview pending** — shows what would be billed (no changes written).
- **▶ Generate this week's finance tab** — creates the `CLAIM PAID IPP …` tab and
  records the codes so they never bill twice.
- The **Dashboard** refreshes automatically every day, and after each generate;
  **📊 Refresh dashboard now** forces it.

## Configuration (top of `Code.gs`)

| Key | Meaning |
|-----|---------|
| `TRACKER_ID` | Main Claims Tracker spreadsheet ID |
| `OLD_FINANCE_ID` | Ava's existing finance sheet (seeding only) |
| `COMMISSION_RATE` | `0.30` |
| `BILLABLE_REQUIRES_WON_STATUS` | `true` = must say `WON` **and** have an amount |
| `WEEKLY_TAB_PREFIX` | `CLAIM PAID IPP` |

The FX rate is fetched live from `open.er-api.com` (no key); if that call ever
fails it falls back to `FALLBACK_THB_PER_USD`.
