#!/usr/bin/env python3
"""Quality of the ressort classification -> data/ressort_quality.json: agreement with curated registry nodes and the independent Opus sample check."""
import json, os
from collections import Counter
from pathlib import Path
HERE = Path(__file__).resolve().parent; SP = HERE.parent
WF = Path('/root/.claude/projects/-home-user-ai-job-search-fork/9c9ad245-1536-5d87-980d-1a4837c57ed1/subagents/workflows')
OPUS = 'wf_7152a576-cab'
CODES = {'STM': 'min-statsministeriet', 'OIM': 'min-oekonomi-og-indenrigs', 'UM': 'min-udenrigs', 'EM': 'min-erhverv', 'FM': 'min-finans', 'JM': 'min-justits',
         'FUD': 'min-forskning-uddannelse-og-digitalisering', 'KEFM': 'min-klima-energi-og-forsyning', 'BLT': 'min-by-land-og-transport', 'UIM': 'min-udlaendinge-og-integration',
         'UVM': 'min-undervisning', 'BLM': 'min-beskaeftigelse-og-ligestilling', 'FMN': 'min-forsvar', 'SVM': 'min-skat-og-vaekst', 'SKM': 'min-sundhed-og-kirke',
         'MND': 'min-natur-og-dyrevelfaerd', 'KUM': 'min-kultur', 'MSB': 'min-samfundssikkerhed-og-beredskab', 'BAB': 'min-boern-aeldre-og-bolig', 'SOM': 'min-social', 'MIM': 'min-miljoe', 'FT': 'ingen', 'UKENDT': 'ukendt'}
R = json.load(open(HERE / 'data' / 'ressort.json'))
link = json.load(open(HERE / 'data' / 'resolved.json'))['link']
nodes = {n['id']: n for n in json.load(open(SP / 'data' / 'final.json'))['nodes']}
c = Counter()
for rid, did in link.items():
    n = nodes[rid]; r = R.get(did)
    if not r or n['type'] not in ('lov', 'bekendtgørelse') or n.get('status') != 'aktiv': continue
    k = 'match' if CODES[r['m']] == n['ministerium'] else 'mismatch'
    c[k + '_' + r['s']] += 1
q = {'registry_n': c['match_s'] + c['mismatch_s'], 'registry_match_pct': round(100 * c['match_s'] / max(1, c['match_s'] + c['mismatch_s'])),
     'registry_n_u': c['match_u'] + c['mismatch_u'], 'registry_match_pct_u': round(100 * c['match_u'] / max(1, c['match_u'] + c['mismatch_u']))}
J = WF / OPUS / 'journal.jsonl'
if J.exists():
    lab = {}; ver = []; re_n = 0; re_s = 0
    for l in open(J):
        x = json.loads(l)
        if x.get('type') == 'started': lab[x['agentId']] = x['label']
        if x.get('type') == 'result' and x.get('result'):
            L = lab.get(x['agentId'], '')
            if L.startswith('opus-ver'): ver += x['result']['items']
            if L.startswith('opus-re'):
                re_n += len(x['result']['items']); re_s += sum(1 for i in x['result']['items'] if i['s'] == 's')
    if ver:
        mk = Counter(v['ministerium_korrekt'] for v in ver); ok = Counter(v['omraade_korrekt'] for v in ver)
        q.update({'sample_n': len(ver), 'sample_ok_pct': round(100 * mk['ja'] / len(ver)), 'sample_nej': mk['nej'], 'sample_tvivl': mk['tvivl'],
                  'sample_omr_ok_pct': round(100 * ok['ja'] / len(ver))})
        json.dump(ver, open(HERE / 'data' / 'opus_sample.json', 'w'), ensure_ascii=False, indent=1)
    if re_n: q.update({'opus_recheck_n': re_n, 'opus_recheck_s': re_s})
json.dump(q, open(SP / 'data' / 'ressort_quality.json', 'w'), ensure_ascii=False, indent=1)
print(q)
