#!/usr/bin/env python3
"""Collect Haiku ressort results from workflow journals -> data/ressort.json; report missing ids per batch."""
import json, os, sys, glob
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__))
WF = '/root/.claude/projects/-home-user-ai-job-search-fork/9c9ad245-1536-5d87-980d-1a4837c57ed1/subagents/workflows'
runs = sys.argv[1:]  # later runs override earlier ones for the same id
OPUS_RUNS = {'wf_7152a576-cab'}
inp = {}
for f in sorted(glob.glob(os.path.join(HERE, 'jobs', 'ressort', 'batch_*.jsonl'))):
    b = os.path.basename(f)[6:9]
    for l in open(f): inp[json.loads(l)['id']] = b
out = {}; st = Counter()
for r in runs:
    for l in open(os.path.join(WF, r, 'journal.jsonl')):
        x = json.loads(l)
        if x.get('type') != 'result' or not x.get('result'): continue
        model = 'opus' if r in OPUS_RUNS else 'haiku'
        for it in x['result'].get('items', []):
            if 'm' not in it: continue  # verification rows (stikprøve) have another shape
            if it['id'] not in inp: st['ukendt_id'] += 1; continue
            st['opdateret' if it['id'] in out else 'ok'] += 1
            out[it['id']] = {'m': it['m'], 'o': it['o'], 's': it['s'], 'model': model}
# deterministic title rules for systematic errors found by the Opus sample check
import re
RULES = [(re.compile(r'ændring(?:er)? i (?:ministerierne?s forretningsområder|forretningernes fordeling)', re.I), 'STM', 'forretningsfordeling udstedes af Statsministeriet'),
         (re.compile(r'dobbeltbeskatning', re.I), 'SVM', 'dobbeltbeskatningsoverenskomster hører under skatteministeren')]
titles = {}
for f in glob.glob(os.path.join(HERE, 'jobs', 'ressort', 'batch_*.jsonl')):
    for l in open(f): x = json.loads(l); titles[x['id']] = x['titel']
for i, v in out.items():
    for rx, code, why in RULES:
        if rx.search(titles.get(i, '')):
            if v['m'] != code: st['regel_rettet'] += 1
            out[i] = {**v, 'm': code, 's': 's', 'model': 'regel', 'regel': why}
            break
miss = Counter(b for i, b in inp.items() if i not in out)
json.dump(out, open(os.path.join(HERE, 'data', 'ressort.json'), 'w'), ensure_ascii=False)
print(dict(st), 'dækket', len(out), '/', len(inp)); print('mangler pr. batch', dict(sorted(miss.items())))
print(Counter(v['m'] for v in out.values()).most_common()); print(Counter(v['s'] for v in out.values()))
