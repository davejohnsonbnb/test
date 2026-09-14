# Daily Claims Report — OUTAGE STATUS

**Last updated: 2026-09-14**

## Summary
The automated routine **"Daily Claims Report — VP + Inter Property"**
(`trig_01NfyXQdDDBHkQTZWwFYtYSX`) has fired once per day since **~2026-08-21**
but has produced **no report on any of those days**.

**Root cause:** the Google Drive connector in this automated session is
persistently disconnected. The two source spreadsheets (VP Claims Tracker,
Inter Property Claims) cannot be downloaded, so there is no data to parse.

**No numbers have been fabricated.** No report was issued rather than a
guessed one. Gmail is also down in this session, so an email escalation
could not be sent either.

## What IS working
- The trigger/schedule itself is healthy — it fires ~09:05 UTC (2 PM Pakistan)
  daily, as designed. The problem is the data source, not the schedule.
- Parser (`claims_engine.py`), rules (`CLAIMS_RULES.md`), and the last good
  baseline (`claims_snapshot.json`) are all committed here — nothing is lost.

## Last good baseline (`ops/claims_snapshot.json`, dated 2026-07-20)
- Inter Property: won 95 / ongoing 12 / lost 13 / pending 24
- VirtuPro: 13 client tabs tracked

## Action needed (Dave)
1. **Reconnect Google Drive** for this session (Settings → Connectors), or
   reopen the session so Drive re-auth completes. The daily report then
   resumes automatically — no other change needed.
2. **If you want the daily fires to stop** until then, pause the routine
   "Daily Claims Report — VP + Inter Property" in your Routines on claude.ai.
   I did not do this from here: it needs your approval, you were not present,
   and disabling it was declined earlier in the session.
