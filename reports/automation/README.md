# Sky Homes — Weekly Report Automation

Generates the automatable sections of the weekly performance report straight
from the Hostfully PMS API — no manual input required for these:

| Section | Source | Auto? |
|---|---|---|
| §8 Guest Reviews | `leads` → `/reviews` (per `leadUid`) | ✅ full |
| §2 Response times (OTA) | `/messages` (Airbnb / Booking.com) | ✅ full |
| §4/7 Escalations (OTA) | keyword scan of OTA guest messages | ✅ detect (confirm + resolutions manual) |
| §1 KPIs, §5 holding replies, §6 turnovers, §9 claims, §2 WhatsApp | manual weekly export | ⛔ placeholder |

WhatsApp analysis needs the manual chat export; KPIs and the claims tracker
are manual dashboards. The generator renders those as "awaiting input".

## Run

```bash
export HF_BASE='https://api.hostfully.com/api/v3.3'
export HF_KEY='...'          # Hostfully API key
export HF_AGENCY='...'       # agency UID
python3 generate_weekly_report.py --week-end 2026-07-24 --out ./out
```

`--week-end` is the Friday the week ends on (defaults to today). Output is
`sky_report_YYYYMMDD.html` + `.pdf` (PDF needs headless Chromium on PATH or at
the pinned Playwright location).

## Schedule

Runs every Friday 22:00 Gulf Standard Time (18:00 UTC) via a Claude Code
Routine that spawns a fresh session, runs this script, and delivers the PDF.
Credentials come from the environment configuration (env vars above).
