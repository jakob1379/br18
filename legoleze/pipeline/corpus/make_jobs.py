#!/usr/bin/env python3
"""Gældende docs -> jobs/ressort/batch_NNN.jsonl (280 per batch, sorted by issuer and year) for the Haiku ressort workflow."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
u = json.load(open(os.path.join(HERE, 'data', 'udsteder.json')))
AB = {'lov': 'LOV', 'ændringslov': 'LOV-Æ', 'lovbekendtgørelse': 'LBK', 'bekendtgørelse': 'BEK', 'ændringsbekendtgørelse': 'BEK-Æ', 'ikrafttrædelsesbekendtgørelse': 'BEK-IKR',
      'bekendtgørelse-international': 'BEK-INT', 'anordning': 'AND', 'ændringsanordning': 'AND-Æ', 'ikrafttrædelsesanordning': 'AND-IKR', 'bekendtgørelse-af-anordning': 'ABK', 'åbent-brev': 'ÅBR'}
items = []
for l in open(os.path.join(HERE, 'data', 'docs.jsonl')):
    d = json.loads(l)
    if d['status_2026_06'] != 'gældende': continue
    items.append({'id': d['id'], 't': AB.get(d['type'], d['type']), 'aar': d['aar'], 'titel': d['titel'][:230], 'udsteder': u[d['id']]['udstedt_af'] or 'ukendt'})
items.sort(key=lambda x: (x['udsteder'], x['aar'], x['id']))
os.makedirs(os.path.join(HERE, 'jobs', 'ressort'), exist_ok=True)
for k, i in enumerate(range(0, len(items), 280)):
    with open(os.path.join(HERE, 'jobs', 'ressort', f'batch_{k:03d}.jsonl'), 'w') as fh:
        for x in items[i:i + 280]: fh.write(json.dumps(x, ensure_ascii=False) + '\n')
print(len(items), 'items')
