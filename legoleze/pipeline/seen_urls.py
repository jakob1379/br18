#!/usr/bin/env python3
"""Collect every URL that appeared in a WebSearch result anywhere in this session (main + all workflow agents)."""
import json, re, glob, sys
from urllib.parse import unquote
ROOT='/root/.claude/projects/-home-user-ai-job-search-fork/9c9ad245-1536-5d87-980d-1a4837c57ed1'
URL=re.compile(r'https?://[^\s"\'<>\)\]\}\\,]+')
def norm(u):
    u=unquote(u.strip()).rstrip('.;:/').replace(' ','%20')
    u=re.sub(r'^http://','https://',u); u=re.sub(r'^https://www\.','https://',u)
    return u.lower()
seen=set(); n=0
files=glob.glob(f'{ROOT}/**/*.jsonl',recursive=True)+glob.glob(f'/root/.claude/projects/-home-user-ai-job-search-fork/*.jsonl')
for p in files:
    for ln in open(p,errors='ignore'):
        if 'Web search results for query' not in ln: continue
        try: d=json.loads(ln)
        except Exception: continue
        c=(d.get('message') or {}).get('content')
        if not isinstance(c,list): continue
        for x in c:
            if x.get('type')!='tool_result': continue
            t=x.get('content'); t=json.dumps(t,ensure_ascii=False) if not isinstance(t,str) else t
            if 'Web search results for query' not in t or 'budget is used up' in t: continue
            n+=1
            for u in URL.findall(t.replace('\\"','"').replace('\\/','/')):
                seen.add(norm(u))
json.dump(sorted(seen),open('data/seen_urls.json','w'))
json.dump({'results':n,'urls':len(seen)},open('data/seen_meta.json','w'))
print('search results',n,'urls',len(seen))
