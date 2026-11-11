#!/usr/bin/env python3
"""Keep only sources that were actually seen in a WebSearch result (or the br18 seed list); downgrade the rest."""
import json, re
from collections import Counter
from urllib.parse import unquote
SP='/tmp/claude-0/-home-user-ai-job-search-fork/9c9ad245-1536-5d87-980d-1a4837c57ed1/scratchpad'
def norm(u):
    u=unquote(u.strip()).rstrip('.;:/').replace(' ','%20')
    u=re.sub(r'^http://','https://',u); u=re.sub(r'^https://www\.','https://',u)
    return u.lower()
seen=set(json.load(open(f'{SP}/data/seen_urls.json')))
SEED={norm(u) for u in [
 'https://github.com/jakob1379/br18/blob/main/xref-laws.toml',
 *[f'https://www.retsinformation.dk/eli/lta/{x}' for x in ['2016/1178','2024/572','2024/53','2024/927','2020/181','2023/1693','2025/1741','2018/219','2026/442','1953/169','2014/433','2025/1017','2026/842','2025/681','2021/420','2017/541']]]}
OK=seen|SEED
RANK={'verificeret':2,'sandsynlig':1,'ukendt':0}
stat=Counter()
def ok(u):
    n=norm(u)
    if n in OK: return True
    # tolerate /pdf suffix and query/fragment variants of a seen URL
    base=re.sub(r'[#?].*$','',n); base2=re.sub(r'/pdf$','',base)
    return base in OK or base2 in OK or (base2+'/pdf') in OK
def fix(c, where):
    ks=c.get('kilder') or []
    keep=[k for k in ks if ok(k)]
    drop=len(ks)-len(keep)
    stat['kilder i alt']+=len(ks); stat['kilder fjernet']+=drop
    c['kilder']=keep
    if drop and not keep:
        if c['sikkerhed']=='verificeret': stat['verificeret→sandsynlig (ingen set kilde)']+=1
        c['sikkerhed']='sandsynlig' if c['sikkerhed']!='ukendt' else 'ukendt'
        c['kilde_note']='Angivne kilder er fjernet: de optrådte ikke i noget søgeresultat (påstanden bygger på modelviden).'
    elif c.get('sikkerhed')=='verificeret' and not keep:
        c['sikkerhed']='sandsynlig'; stat['verificeret uden kilde→sandsynlig']+=1
    return drop
m=json.load(open(f'{SP}/data/final.json'))
for n in m['nodes']:
    for f in ('hjemmel','dokumenttyper','url','adgang','identifikatorer','licens','opdatering'):
        fix(n[f], f'{n["id"]}.{f}')
    u=n['url'].get('vaerdi','')
    if isinstance(u,str) and u.startswith('http') and not ok(u):
        stat['url-værdi ikke set → ikke fundet']+=1
        n['url']={'vaerdi':'ikke fundet','kilder':[],'sikkerhed':'ukendt','kilde_note':f'Tidligere angivet URL ({u}) optrådte ikke i noget søgeresultat og er fjernet.'}
    elif isinstance(u,str) and u.startswith('http') and n['url']['sikkerhed']=='verificeret' and not n['url']['kilder']:
        n['url']['kilder']=[u]
    for p in n.get('tidligere_navne',[]): fix(p,'prev')
    if n.get('baseline'): n['baseline']['kilder']=[k for k in n['baseline']['kilder'] if ok(k)]
for e in m['edges']:
    fix(e,'edge')
for h in m['huller']:
    h['kilder']=[k for k in h['kilder'] if ok(k)]
for x in m['baseline'].get('ressortomlaegninger',[]): fix(x,'ressort')
fix(m['baseline']['regering'],'regering')
json.dump(m,open(f'{SP}/data/final.json','w'),ensure_ascii=False,indent=1)
meta=json.load(open(f'{SP}/data/seen_meta.json'))
json.dump({'results':meta['results'],'urls':meta['urls'],'kilder':stat['kilder i alt'],'fjernet':stat['kilder fjernet']},open(f'{SP}/data/provenance_stats.json','w'))
print(json.dumps(stat,ensure_ascii=False,indent=1))
