# Sky Homes Weekly Report — Full Playbook (for a fresh session)

Goal: produce the "SKY HOMES — WEEKLY PERFORMANCE REPORT" PDF, same 11-section
layout every week. Report window = **Saturday..Friday** (e.g. Jul 12–18). The two
completed examples are the PDFs sent in chat; match that structure exactly.

## Credentials / sources
- Hostfully API (Sky Homes agency): key + agency UID are in Drive doc
  **"Cirtupro Ops - Hostfully API Credentials [SENSITIVE]"**
  (fileId 14_bjN878mzww9N_5IG-4Hnsom48McHVoJiBAIZ-MeUQ). Read it, don't hardcode.
  - Base: `https://api.hostfully.com/api/v3.3/`  Header: `X-HOSTFULLY-APIKEY`
  - Endpoints used: `/messages`, `/leads`, `/properties` (all take `agencyUid=` +
    `limit=100` + cursor paging via `_paging._nextCursor`, passed as `&_cursor=`).
  - API is flaky (503s / connection resets) — ALWAYS wrap calls in retry w/ backoff.
- Claims: VP tracker **SkyHomes tab** in fileId
  10_8AESc3uh7IZOUkPr6MB5giT_LmgcoTt9RDhVyj3RA (canonical). Colors:
  green=won, yellow=ongoing, red=rejected, uncolored=unfiled. Parser =
  ops/claims_engine.py.

## Section-by-section: where each number comes from
1. **KPIs (Revenue / Nights / Occupancy / ADR / RevPAR)** — from Dave's Hostfully
   dashboard SCREENSHOT (he sends it; set date range to the window, Compare=Preceding
   period). Compute WoW % vs last week's report. Report down weeks honestly with a
   one-line seasonality/baseline context. Verify occupancy against PMS pull (below);
   they should be within ~1-2pp.
2. **Response times (§01-02)** — pull `/messages` back to window start. Pair each
   guest msg → next agency reply (skip when next msg is also guest = burst). Report
   AVG excluding >60min overnight-gap outliers (state this), plus median and % within
   5min. First-response = first guest→agency reply per new thread. Always note the
   Hostfully sync-delay caveat. DO NOT invent numbers (Dave once asked for a made-up
   4.8 — refuse; the trimmed real avg is defensible and usually better).
3. **Query accuracy (§03)** — scan agency msgs for wrong-guest/wrong-unit sends.
4. **Escalations (§04/07)** — keyword-scan guest msgs (dirty/insect/broken/smell/
   refund/security/AC/leak/sewage etc.), rank by guest-side hit count, read the top
   threads. Get RESOLUTION OUTCOMES from Dave (often handled off-PMS on WhatsApp).
5. **Turnovers (§06)** — Dave gives a count from WhatsApp; cross-check against PMS
   checkouts in window (`/leads`, type=BOOKING, status in BOOKED/ARCHIVED/CHECKED_OUT/
   PAID_IN_FULL, checkOut in window). Also mine the 3 WhatsApp cleaning-group .txt
   exports he uploads for damage items + issues (Waters Edge & Noya, Reem & Vista,
   Masder). Dedupe: teams post "for tomorrow" (evening) + "for today" (morning) = ONE
   cleaning day.
6. **Reviews (§08)** — Hostfully review API returns ZERO (sync off). Dave pulls via
   the **Claude Chrome extension** on the co-host Airbnb account and pastes text.
   Prompt template is in chat history. Filter to Sky Homes unit names only.
7. **Damage claims (§09)** — from the SkyHomes claims tab + the WhatsApp damage items.
8. **Team (§10)** — Dave provides; has been Wardah/Sohaib/Shahmeer/Ali (unchanged).
9. **What we're working on (§11)** — recurring: check-in auto-deploy (open), PMS sync
   delay. Add themes that recurred this week (pest control, plumbing/drainage).

## Occupancy denominator
Active units = live count from `/properties` (isActive). Was 68. It fluctuates —
always pull live, never hardcode.

## Build the PDF
Write HTML (green #1e6b3a headers, KPI row, 11 tables) then:
`chromium --headless --print-to-pdf` using the binary under
/opt/pw-browsers/chromium-1194/chrome-linux/chrome. Send via SendUserFile.

## Inputs to request from Dave each week (he supplies these)
1. Dashboard screenshot (KPIs)  2. 3 WhatsApp cleaning exports  3. Review extension
paste  4. Team update  5. Escalation outcomes (incl. any carried-over unknowns).

## Standing coaching flags (surface, don't bury)
- SkyHomes claims tab barely moves — unfiled items pile up (Radiant 204, WE021B04,
  Noya 736, Noya 956 lamp, Radiant 915, Radiant 1901, Ajwan 923). Push Ahmad Shahi.
- Written guest damage admissions (e.g. Noya 956 "my baby broke the lamp") = free
  claims; make sure they get filed.
- Recurring unit: Noya 1130 (water/insects across multiple weeks).
