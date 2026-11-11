import json, os, sys, re
from collections import Counter
D=sys.argv[1]
types=Counter(); status=Counter(); ret=Counter(); maxd=''; noprov=0; up=Counter(); hist=Counter(); yrs=Counter()
sample={}
for i,f in enumerate(os.listdir(D)):
    d=json.load(open(os.path.join(D,f)))
    t=(d.get('short_name') or '').split(' ')[0]
    types[t]+=1; status[d.get('status')]+=1; up[d.get('_ingest',{}).get('upstream_status')]+=1
    ret[(d.get('_ingest',{}).get('retrieved_at') or '')[:7]]+=1
    if (d.get('issued_date') or '')>maxd: maxd=d['issued_date']
    if not d.get('provisions'): noprov+=1
    sample.setdefault(t,d['id']+' '+d['title'][:80])
    if d.get('status')=='in_force': yrs[(d.get('issued_date') or '????')[:4]]+=1
print('types',types.most_common(40)); print('status',status); print('upstream',up); print('retrieved',sorted(ret.items())); print('max issued',maxd,'noprov',noprov)
print('samples',json.dumps(sample,ensure_ascii=False,indent=0)[:3000])
print('in_force by decade', sorted(Counter(y[:3]+'0s' for y in yrs.elements()).items()))
