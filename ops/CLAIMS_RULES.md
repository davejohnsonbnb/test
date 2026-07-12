# Cirtupro Claims Tracking — Rules (source of truth for the daily report)

## Sheets
- **VP tracker**: Drive fileId `10_8AESc3uh7IZOUkPr6MB5giT_LmgcoTt9RDhVyj3RA` — 13 client tabs.
  The **SkyHomes tab inside this tracker is canonical** (the standalone
  "VirtuPro - SkyHomes Claims" sheet mirrors it; do not double-count).
- **Inter Property Phuket**: Drive fileId `1h1enX5eOiT1GXtSSeS4kgItizqcdtzr61xc7uTF-wG8`,
  tab **"Claims"** only. Other tabs are credentials — do not read or copy them.
  The standalone "InterClaims" sheet is a stale copy — ignore.

## Color semantics (cell fill)
- **Green** = won; Received Amount column has the money.
- **Yellow** = in progress (filed / emails ongoing).
- **Red** = rejected; reasoning is in the row.
- **Uncolored** = pending / not yet actioned → flag if older than 5 days.
- **Blue / magenta / cyan** = ignore (per Dave, 2026-07-12).

## Exceptions
- **EliteNest** and **Royal Vista** tabs are filed via Guesty (not Airbnb) and use
  no colors: **every data row = WON at the recorded amount**.
- Inter Claims tab has TWO columns headed "Recieved Amount" — the FIRST (col K)
  is money; the second is a TRUE/FALSE flag. Use K.

## Daily report format (deltas vs snapshot, not totals)
VirtuPro — per client with new wins: name, "Claim won N", "Amount: X aed".
Inter Property — counts (Ongoing / Pending / Lost / Won) + amount of each new won claim in THB.
Flag: new unfiled (uncolored) rows > 5 days old; money holes (green/closed rows with no received amount).

## Baseline snapshot: ops/claims_snapshot.json (updated by each daily run)
