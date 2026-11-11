#!/usr/bin/env python3
"""Hand-reviewed fixes applied after provenance: canonical root URLs that literally appeared in search results."""
import json
SP='/tmp/claude-0/-home-user-ai-job-search-fork/9c9ad245-1536-5d87-980d-1a4837c57ed1/scratchpad'
m=json.load(open(f'{SP}/data/final.json'))
seen=set(json.load(open(f'{SP}/data/seen_urls.json')))
fixes=json.load(open(f'{SP}/data/url_fixes.json'))
N={n['id']:n for n in m['nodes']}
done=0
for nid,u in fixes.items():
    n=N.get(nid)
    if not n or u.lower() not in seen: continue
    if n['url'].get('vaerdi') in ('ikke fundet',None) or n['url']['sikkerhed']!='verificeret':
        n['url']={'vaerdi':u,'kilder':[u],'sikkerhed':'verificeret','kilde_note':'Forsiden optrådte selv i søgeresultaterne (manuelt efterset).'}
        done+=1
contra=0
for n in m['nodes']:
    u=n['url']
    if not str(u.get('vaerdi','')).startswith('http') and u.get('sikkerhed')=='verificeret':
        u['sikkerhed']='ukendt'; u['kilde_note']='Ingen kanonisk URL fundet; de angivne kilder omtaler noden, men er ikke dens kanoniske side.'; contra+=1
import os
added=0
if os.path.exists(f'{SP}/data/replacement_edges.json'):
    keys={(e['from'],e['type'],e['to']) for e in m['edges']}
    for e in json.load(open(f'{SP}/data/replacement_edges.json')):
        if e['from'] in N and e['to'] in N and (e['from'],e['type'],e['to']) not in keys:
            m['edges'].append({**e,'domaener':[]}); added+=1
json.dump(m,open(f'{SP}/data/final.json','w'),ensure_ascii=False,indent=1)
print('url fixes',done,'modsigelser rettet',contra,'erstatningskanter',added)
