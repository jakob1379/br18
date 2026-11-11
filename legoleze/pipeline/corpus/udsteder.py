#!/usr/bin/env python3
"""udstedt_af (historical issuing ministry) per doc from DocumentId prefix + text evidence; writes data/udsteder.json and job batches."""
import json, os, re
from collections import Counter
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from prefixes import top_min
HERE = os.path.dirname(os.path.abspath(__file__))
MANUAL = {  # prefixes where minister mentions are absent/mixed; named from sample titles (see data/prefixes.json)
    'AB': 'Arbejdsministeriet', 'AQ': 'Sundhedsministeriet', 'AD': 'Erhvervsministeriet', 'AF': 'Forskningsministeriet',
    'AC': 'By- og Boligministeriet', 'BG': 'Familie- og Forbrugerministeriet', 'AR': 'Trafikministeriet / Transport- og Energiministeriet',
    'AP': 'Statsministeriet', 'AX': 'Folketinget', 'AM': 'Folketinget', 'AS': 'Udenrigsministeriet', 'CN': 'Sundheds- og Ældreministeriet / Sundhedsministeriet',
    'DH': 'Social- og Ældreministeriet / Social-, Bolig- og Ældreministeriet / Social- og Boligministeriet', 'DK': 'Digitaliseringsministeriet',
    'DN': 'Ældreministeriet', 'DM': 'Ministeriet for Grøn Trepart', 'CZ': 'Transport- og Boligministeriet', 'DJ': 'Økonomiministeriet',
    'AH': 'Fødevareministeriet / Ministeriet for Fødevarer, Landbrug og Fiskeri', 'DC': 'Ministeriet for Fødevarer, Landbrug og Fiskeri',
}
MIXED = {'CM'}
SMALL = {'og', 'for', 'i', 'af'}
def min2ministry(s):
    if not s: return None
    if s.startswith('ministeren for '):
        rest = s[len('ministeren for '):]
        return 'Ministeriet for ' + ' '.join(w if w in SMALL else w[:1].upper() + w[1:] for w in rest.split(' '))
    if s.endswith('ministeren'):
        n = s[:-len('ministeren')] + 'ministeriet'
        return ' '.join(w if w in SMALL else w[:1].upper() + w[1:] for w in n.split(' '))
    return None
P = {o['prefix']: o for o in json.load(open(os.path.join(HERE, 'data', 'prefixes.json')))}
out = {}; stat = Counter()
for l in open(os.path.join(HERE, 'data', 'docs.jsonl')):
    d = json.loads(l); p = d['prefix'] or '?'; o = P.get(p, {})
    c = top_min(d); own = c.most_common(1)[0][0] if c else None
    prefset = {m for m, _ in o.get('top_ministre', [])}
    if p in MANUAL:
        u, how = MANUAL[p], 'praefiks-manuel'
        if own and own in prefset and '/' in u: u, how = min2ministry(own), 'praefiks+tekst'
    elif p in MIXED or not o.get('dominerende_minister') or (o.get('renhed') or 0) < 0.6 or o.get('dok_med_ministernavn', 0) < 10:
        u, how = (min2ministry(own), 'tekst') if own else (None, 'ingen')
    else:
        u, how = (min2ministry(own), 'praefiks+tekst') if own and own in prefset else (min2ministry(o['dominerende_minister']), 'praefiks')
    out[d['id']] = {'udstedt_af': u, 'metode': how, 'prefix': p, 'minister_i_tekst': own}
    stat[how] += 1
names = {v['udstedt_af'] for v in out.values() if v['udstedt_af']}
for v in out.values():  # genitive forms ("…Landdistrikters") -> base name
    n = v['udstedt_af']
    if n and n.endswith('s') and n[:-1] in names: v['udstedt_af'] = n[:-1]
json.dump(out, open(os.path.join(HERE, 'data', 'udsteder.json'), 'w'), ensure_ascii=False)
print(stat)
