#!/usr/bin/env python3
"""Daily claims delta runner. Usage: python daily_delta.py VP.xlsx INTER.xlsx [YYYY-MM-DD]
Reads ops/claims_snapshot.json as baseline, prints deltas, writes new snapshot."""
import json, sys, re, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from claims_engine import analyze, row_color
GUESTY={'EliteNest','Royal Vista'}
def amt(s):
    s=(s or '').replace(',','').strip(); m=re.search(r'-?\d+\.?\d*',s); return float(m.group()) if m else None
def run(vpx, inx, date, snap_path):
    base=json.load(open(snap_path)); bvp={k:v['won'] for k,v in base['vp'].items()}; bi=base['inter']
    vp=analyze(vpx); newvp={}; changed=[]
    for tab,rows in vp.items():
        if not rows: continue
        c=tab.replace(' - Claim Tracker','').strip()
        if c in GUESTY: n=sum(1 for rn,v in rows[1:] if any(x[0].strip() for x in v.values()))
        else: n=sum(1 for rn,v in rows[1:] if row_color(v)=='green')
        newvp[c]=n; b=bvp.get(c)
        if b is None: changed.append(f"{c}: NEW tab {n} won")
        elif n!=b:
            hdr=rows[0][1]; pr=[(x[0].strip().lower(),k) for k,x in hdr.items()]
            rec=next((k for tt,k in pr if 'reciev' in tt or 'receiv' in tt),None); clm=next((k for tt,k in pr if 'amount' in tt),None)
            dr=[(rn,v) for rn,v in rows[1:] if any(x[0].strip() for x in v.values())] if c in GUESTY else [(rn,v) for rn,v in rows[1:] if row_color(v)=='green']
            nr=dr[b-n:]; tot=sum((amt(v.get(rec,('',''))[0]) if rec else None) or (amt(v.get(clm,('',''))[0]) if clm else 0) or 0 for _,v in nr)
            changed.append(f"{c}: +{n-b} won, {tot:,.0f} AED")
    inter=analyze(inx); rows=inter.get('Claims') or list(inter.values())[0]
    st={'green':0,'yellow':0,'red':0,'none':0}; tot=0
    for rn,v in rows[1:]:
        col=row_color(v) or 'none'; st[col]=st.get(col,0)+1
        if col=='green': tot+=amt(v.get('K',('',''))[0]) or 0
    dwon=st['green']-bi['won']
    print("VP vs %s: %s"%(base['date'], changed if changed else "NONE"))
    print("Inter: Won {}({:+d}) Ongoing {}({:+d}) Lost {}({:+d}) Pending {}({:+d}) recv{:+,.0f}".format(
        st['green'],dwon,st['yellow'],st['yellow']-bi['ongoing'],st['red'],st['red']-bi['lost'],
        st['none'],st['none']-bi['pending'],tot-bi['won_received_thb']))
    if dwon>0:
        for rn,v in [r for r in rows[1:] if row_color(r[1])=='green'][-dwon:]:
            print("  new won:",(v.get('C',('',''))[0] or '')[:22], amt(v.get('K',('',''))[0]),"THB")
    snap={'date':date,'vp':{k:{'won':v} for k,v in newvp.items()},
          'inter':{'won':st['green'],'ongoing':st['yellow'],'lost':st['red'],'pending':st['none'],'won_received_thb':int(tot)}}
    json.dump(snap, open(snap_path,'w'), indent=1)
if __name__=='__main__':
    run(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv)>4 else 'ops/claims_snapshot.json')
