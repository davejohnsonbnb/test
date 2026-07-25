#!/usr/bin/env python3
"""
Sky Homes — Weekly Performance Report generator (automatable sections).

Pulls everything the PMS API can provide with NO manual input:
  - Section 8  Guest Reviews         (leads -> /reviews)
  - Section 2  OTA response times     (/messages, Airbnb/Booking.com)
  - Section 4/7 OTA escalations       (keyword scan of guest messages)

Sections that require a manual weekly export (WhatsApp chat export, the
claims tracker, the KPI dashboard, cleaning-group notes) are rendered as
"awaiting input" placeholders for a human/assistant to complete.

Credentials are read from the environment:
  HF_BASE    e.g. https://api.hostfully.com/api/v3.3
  HF_KEY     Hostfully API key   (X-HOSTFULLY-APIKEY)
  HF_AGENCY  agency UID

Usage:
  python3 generate_weekly_report.py [--week-end YYYY-MM-DD] [--out DIR]
The report week is Saturday..Friday. --week-end defaults to today (the
Friday the job runs); the week is the 7 days ending that Friday.
"""
import os, sys, json, re, base64, time, argparse, urllib.request
from datetime import datetime, timedelta, timezone

DUBAI = timezone(timedelta(hours=4))
BASE = os.environ.get("HF_BASE", "").rstrip("/")
KEY  = os.environ.get("HF_KEY", "")
AG   = os.environ.get("HF_AGENCY", "")

def _need_creds():
    missing = [k for k in ("HF_BASE", "HF_KEY", "HF_AGENCY") if not os.environ.get(k)]
    if missing:
        sys.exit("Missing credentials in environment: " + ", ".join(missing) +
                 "\nAdd them to the environment configuration and re-run.")

def get(url, tries=4):
    req = urllib.request.Request(url, headers={"X-HOSTFULLY-APIKEY": KEY})
    last = None
    for a in range(tries):
        try:
            return json.load(urllib.request.urlopen(req, timeout=25))
        except Exception as e:
            last = e; time.sleep(min(1.6 ** a, 12))
    raise last

def cursor(offset):
    return base64.b64encode(('{"offset":%d}' % offset).encode()).decode()

def paginate(path, stop=None, cap=60):
    """Yield items from a cursor-paginated collection endpoint."""
    off = 0
    for _ in range(cap):
        sep = "&" if "?" in path else "?"
        d = get(f"{BASE}/{path}{sep}limit=100&_cursor={cursor(off)}")
        key = next((k for k in d if isinstance(d.get(k), list)), None)
        items = d.get(key, []) if key else []
        if not items:
            break
        for it in items:
            yield it
        off += len(items)
        if stop and stop(items):
            break
        if not d.get("_paging", {}).get("_nextCursor"):
            break

def parse_utc(ts):
    ts = re.sub(r'(\.\d{6})\d+', r'\1', ts.replace("Z", "+00:00"))
    return datetime.fromisoformat(ts).astimezone(DUBAI)

def strip_html(h):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', h or '')).strip()

def is_night(dt):
    return dt.hour >= 22 or dt.hour < 8

def overnight_excluded(g, r, gap_min):
    if gap_min <= 60:
        return False
    c = g
    while c < r:
        if is_night(c):
            return True
        c += timedelta(minutes=15)
    return is_night(r)

# ---------------------------------------------------------------- reviews
def pull_reviews(props_by_uid, wk0, wk1):
    reviews = []
    booked = ("BOOKED", "CHECKED_OUT", "CLOSED")
    for lead in paginate(f"leads?agencyUid={AG}", cap=40):
        co = lead.get("checkOutLocalDateTime", "")
        if not (wk0.strftime("%Y-%m-%d") <= co[:10] < wk1.strftime("%Y-%m-%d")):
            continue
        if lead.get("status") not in booked:
            continue
        try:
            d = get(f"{BASE}/reviews?leadUid={lead['uid']}&limit=10")
        except Exception:
            continue
        for rv in d.get("reviews", []):
            rv["_prop"] = props_by_uid.get(rv.get("propertyUid"), "?")
            rv["_channel"] = lead.get("channel")
            reviews.append(rv)
    return reviews

# ------------------------------------------------------- OTA messages
def pull_ota(wk0_utc, wk1_utc):
    start_iso = wk0_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
    msgs = []
    def stop(batch):
        return min(m["createdUtcDateTime"] for m in batch) < start_iso
    for m in paginate(f"messages?agencyUid={AG}", stop=stop, cap=80):
        msgs.append(m)
    lo = wk0_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
    hi = wk1_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
    return [m for m in msgs if lo <= m["createdUtcDateTime"] < hi]

def response_times(msgs, wk0, wk1):
    from collections import defaultdict
    th = defaultdict(list)
    for m in msgs:
        m["dt"] = parse_utc(m["createdUtcDateTime"])
        th[m["threadUid"]].append(m)
    gaps = []
    for _, ms in th.items():
        ms.sort(key=lambda x: x["dt"]); i = 0
        while i < len(ms):
            if ms[i]["senderType"] == "GUEST":
                j = i + 1
                while j < len(ms) and ms[j]["senderType"] != "AGENCY":
                    j += 1
                if j < len(ms):
                    g, r = ms[i], ms[j]
                    gap = (r["dt"] - g["dt"]).total_seconds() / 60
                    if wk0 <= g["dt"] < wk1 and not overnight_excluded(g["dt"], r["dt"], gap):
                        gaps.append(gap)
                    i = j + 1; continue
            i += 1
    import statistics as st
    if not gaps:
        return None
    return dict(n=len(gaps), avg=round(st.mean(gaps), 1), median=round(st.median(gaps), 1),
                within5=round(100 * sum(1 for x in gaps if x <= 5) / len(gaps)))

def scan_escalations(msgs):
    pat = re.compile(r'\b(leak|flood|no water|no power|no electricity|no gas|not working|'
                     r'broken|refund|cancel|dirty|filthy|not clean|stain|smell|cockroach|'
                     r'insect|bug|a/?c|air ?con|hot water|codes? (are )?not working|locked out|'
                     r'unsafe)\b', re.I)
    hits = []
    for m in msgs:
        if m.get("senderType") == "GUEST":
            t = strip_html(m.get("content", {}).get("text", ""))
            if pat.search(t):
                hits.append((parse_utc(m["createdUtcDateTime"]), m.get("type"), t[:140]))
    hits.sort()
    return hits

# ---------------------------------------------------------------- render
def esc(s):
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def render_html(ctx):
    css = """
    :root{--green:#1f7a4d;--green-d:#155c39;--green-l:#e8f3ec;--ink:#1f2937;--muted:#6b7280;
    --line:#e5e7eb;--amber:#b45309;--amber-l:#fef3e2;--red:#b91c1c;--red-l:#fdecec;}
    *{box-sizing:border-box}html{-webkit-print-color-adjust:exact;print-color-adjust:exact}
    body{font-family:-apple-system,'Segoe UI',Roboto,Arial,sans-serif;color:var(--ink);margin:0;font-size:12.5px;line-height:1.5}
    .page{max-width:820px;margin:0 auto;padding:28px 34px}
    header.cover{background:linear-gradient(135deg,var(--green),var(--green-d));color:#fff;border-radius:12px;padding:26px 30px;margin-bottom:22px}
    header.cover .brand{font-size:13px;letter-spacing:.16em;text-transform:uppercase;opacity:.85}
    header.cover h1{margin:6px 0 2px;font-size:26px;font-weight:700}
    header.cover .period{font-size:14px;opacity:.95}
    h2{color:var(--green-d);font-size:15px;margin:26px 0 10px;padding:7px 12px;background:var(--green-l);border-left:5px solid var(--green);border-radius:4px}
    h2 .n{opacity:.6;font-weight:600;margin-right:8px}
    table{width:100%;border-collapse:collapse;margin:8px 0;font-size:11.5px}
    th,td{text-align:left;padding:6px 9px;border-bottom:1px solid var(--line);vertical-align:top}
    th{background:#f7faf8;color:var(--green-d);font-weight:600;font-size:10.5px;text-transform:uppercase}
    .stat-row{display:flex;gap:10px;margin:8px 0;flex-wrap:wrap}
    .stat{flex:1;min-width:120px;border:1px solid var(--line);border-radius:9px;padding:10px 12px}
    .stat .v{font-size:20px;font-weight:700;color:var(--green-d)}
    .stat .k{font-size:10.5px;color:var(--muted);text-transform:uppercase}
    .pill{display:inline-block;padding:1px 8px;border-radius:20px;font-size:10px;font-weight:600}
    .pill.pend{background:var(--amber-l);color:var(--amber)}
    .muted{color:var(--muted)}
    .note{background:var(--amber-l);border-left:4px solid var(--amber);padding:8px 12px;border-radius:4px;font-size:11.5px;margin:8px 0;color:#7c3a06}
    @media print{.page{padding:10px 6px}h2{break-after:avoid}table,.stat-row{break-inside:avoid}}
    """
    rt = ctx["ota_rt"]
    rows_rev = "".join(
        f"<tr><td>{esc(r.get('date'))}</td><td>{esc(r['_prop'])}</td>"
        f"<td>{r.get('rating','?')}&#9733;</td><td>{esc(r.get('author'))}</td>"
        f"<td>{esc((r.get('content') or '').strip()[:160])}"
        + (f"<br><span class='muted'>Private: {esc(r['privateFeedback'][:80])}</span>" if r.get('privateFeedback') and r['privateFeedback'] not in ('لا يوجد',) else "")
        + "</td></tr>"
        for r in sorted(ctx["reviews"], key=lambda z: z.get("rating", 5))
    )
    rows_esc = "".join(
        f"<tr><td>{d.strftime('%d %b %H:%M')}</td><td>{esc(p)}</td><td>{esc(t)}</td></tr>"
        for d, p, t in ctx["escalations"][:20]
    )
    avg = round(sum(r.get("rating", 0) for r in ctx["reviews"]) / len(ctx["reviews"]), 1) if ctx["reviews"] else 0
    five = round(100 * sum(1 for r in ctx["reviews"] if r.get("rating") == 5) / len(ctx["reviews"])) if ctx["reviews"] else 0
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<title>Sky Homes — Weekly Performance Report</title><style>{css}</style></head><body><div class="page">
<header class="cover"><div class="brand">Sky Homes &middot; Abu Dhabi</div>
<h1>Weekly Performance Report</h1><div class="period">{ctx['period']}</div></header>

<h2><span class="n">01</span>Key Performance Indicators</h2>
<p><span class="pill pend">Awaiting input</span> KPIs come from the PMS dashboard export &mdash; paste this week's figures to populate.</p>

<h2><span class="n">02</span>Guest Response Times &mdash; OTA</h2>
{'<div class="stat-row"><div class="stat"><div class="v">'+str(rt['avg'])+' min</div><div class="k">Average reply</div></div><div class="stat"><div class="v">'+str(rt['median'])+' min</div><div class="k">Median reply</div></div><div class="stat"><div class="v">'+str(rt['within5'])+'%</div><div class="k">&le; 5 min</div></div><div class="stat"><div class="v">'+str(rt['n'])+'</div><div class="k">Guest&rarr;reply pairs</div></div></div><p class="muted">Airbnb / Booking.com via the PMS. Overnight gaps &gt;60 min excluded. WhatsApp channel requires the manual chat export to be added.</p>' if rt else '<p class="muted">No OTA messages found for the week.</p>'}

<h2><span class="n">04 &amp; 07</span>Escalations &mdash; OTA (auto-detected)</h2>
<p class="muted">Keyword-detected guest messages; confirm which are genuine and add resolutions (not assumed). WhatsApp escalations require the chat export.</p>
<table><tr><th>When</th><th>Channel</th><th>Guest message</th></tr>{rows_esc or '<tr><td colspan=3>None auto-detected.</td></tr>'}</table>

<h2><span class="n">08</span>Guest Reviews</h2>
<div class="stat-row"><div class="stat"><div class="v">{len(ctx['reviews'])}</div><div class="k">New reviews</div></div>
<div class="stat"><div class="v">{avg}&#9733;</div><div class="k">Average</div></div>
<div class="stat"><div class="v">{five}%</div><div class="k">5-star</div></div></div>
<table><tr><th>Date</th><th>Unit</th><th>Rating</th><th>Guest</th><th>Review</th></tr>{rows_rev or '<tr><td colspan=5>No reviews posted yet for this week.</td></tr>'}</table>

<div class="note"><strong>Manual sections still required:</strong> KPIs (§1), WhatsApp response times &amp; escalations (§2/§7),
holding replies (§5), turnovers (§6), damage claims (§9). Provide the WhatsApp export + trackers to complete the report.</div>
</div></body></html>"""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--week-end", help="Friday date YYYY-MM-DD (default: today)")
    ap.add_argument("--out", default=".")
    args = ap.parse_args()
    _need_creds()
    end = datetime.strptime(args.week_end, "%Y-%m-%d").date() if args.week_end else datetime.now(DUBAI).date()
    wk1 = datetime(end.year, end.month, end.day, tzinfo=DUBAI) + timedelta(days=1)  # Sat 00:00 after the Friday
    wk0 = wk1 - timedelta(days=7)                                                    # Sat 00:00
    period = f"{wk0.strftime('%A %-d %B')} – {(wk1 - timedelta(days=1)).strftime('%A %-d %B %Y')}"
    print(f"[report] week {wk0.date()} .. {(wk1-timedelta(days=1)).date()}")

    props = {p["uid"]: p["name"] for p in paginate(f"properties?agencyUid={AG}", cap=5)}
    print(f"[report] {len(props)} properties")
    reviews = pull_reviews(props, wk0, wk1)
    print(f"[report] {len(reviews)} reviews")
    ota = pull_ota(wk0.astimezone(timezone.utc), wk1.astimezone(timezone.utc))
    print(f"[report] {len(ota)} OTA in-week messages")
    ctx = dict(period=period, reviews=reviews,
               ota_rt=response_times(ota, wk0, wk1),
               escalations=scan_escalations(ota))
    html = render_html(ctx)
    os.makedirs(args.out, exist_ok=True)
    stub = wk0.strftime("%Y%m%d")
    hp = os.path.join(args.out, f"sky_report_{stub}.html")
    open(hp, "w").write(html)
    print("[report] wrote", hp)
    # PDF via chromium if available
    for cand in ("/opt/pw-browsers/chromium-1194/chrome-linux/chrome", "chromium", "google-chrome"):
        if os.path.exists(cand) or cand in ("chromium", "google-chrome"):
            pdf = os.path.join(args.out, f"sky_report_{stub}.pdf")
            rc = os.system(f'"{cand}" --headless --no-sandbox --disable-gpu '
                           f'--print-to-pdf="{pdf}" --no-pdf-header-footer "file://{os.path.abspath(hp)}" 2>/dev/null')
            if rc == 0 and os.path.exists(pdf):
                print("[report] wrote", pdf); break
    return 0

if __name__ == "__main__":
    sys.exit(main())
