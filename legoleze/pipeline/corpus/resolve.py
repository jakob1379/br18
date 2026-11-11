#!/usr/bin/env python3
"""Pass 2: law families, reference resolution, hjemmel candidates, EU refs, registry links -> data/resolved.json"""
import json, re, os
from collections import Counter, defaultdict
HERE = os.path.dirname(os.path.abspath(__file__)); SP = os.path.dirname(HERE)
docs = [json.loads(l) for l in open(os.path.join(HERE, 'data', 'docs.jsonl'))]
byid = {d['id']: d for d in docs}
LAWT = {'lov', 'lovbekendtgørelse'}

def clean(t):
    t = t.lower().replace('\\n', ' ')
    t = re.sub(r'\(\*\s*\d*\)', ' ', t); t = re.sub(r'\s+', ' ', t).strip(' .')
    return t

def keys_for(title):
    """-> (keys, kortnavn). keys: normalised 'lov om'-names and short names."""
    t = clean(title); ks = set(); kort = None
    m = re.search(r'\(([a-zæøå\- ]*lov(?:en)?)\)\s*$', t)
    if m:
        kort = m.group(1).strip(); t = t[:m.start()].strip(' .,')
        if kort.endswith('lov'): kort += 'en'  # "(erhvervslejelov)" -> matches "erhvervslejeloven" in text
    t = re.sub(r'^bekendtgørelse af ', '', t)
    if re.fullmatch(r'[a-zæøå\-]+loven?', t): kort = kort or (t if t.endswith('en') else t + 'en')
    m = re.match(r'^lov(?:en)? om (.+)$', t)
    if m: ks.add(norm_name(m.group(1)))
    if kort: ks.add('#' + kort)
    return ks, kort

TAIL = {'m', 'v', 'mv', 'mm', 'fl', 'mfl'}
def norm_name(s):
    s = re.sub(r'\b(?:m\.\s?v|mv|m\.\s?m|m\.\s?fl)\b\.?', ' ', s)
    w = re.sub(r'[^a-zæøåé0-9\- ]', ' ', s).split()
    while w and w[-1] in TAIL: w.pop()  # "… m.v" cut at the full stop, or a dangling "m" from the text regex
    return ' '.join(w)

# --- law families
key2docs = defaultdict(list)
for d in docs:
    if d['type'] in LAWT:
        ks, kort = keys_for(d['titel']); d['_keys'] = sorted(ks); d['_kort'] = kort
        for k in ks: key2docs[k].append(d['id'])
keyset = set(key2docs)
maxwords = max(len(k.split()) for k in keyset if not k.startswith('#'))

def current_for_key(k):
    c = [byid[i] for i in key2docs.get(k, [])]
    if not c: return None
    g = [x for x in c if x['status_2026_06'] == 'gældende']
    pool = g or c
    return max(pool, key=lambda x: (x['udstedt'] or '', x['nr']))['id']

def match_lovom(phrase):
    p = phrase
    while True:
        m = re.match(r'^(?:ændring af |ophævelse af )+(?:lov(?:en)? om )?(.*)$', p)
        if not m or m.group(1) == p: break
        p = m.group(1)
    w = norm_name(p).split()
    for n in range(min(len(w), maxwords), 0, -1):
        k = ' '.join(w[:n])
        if k in keyset: return k
    return None

def law_of_doc(i):
    """historic/current law doc -> current law id of its family (or itself)."""
    d = byid.get(i)
    if not d or d['type'] not in LAWT: return i if d else None
    best = None
    for k in d.get('_keys', []):
        c = current_for_key(k)
        if c and (best is None or (byid[c]['udstedt'] or '') > (byid[best]['udstedt'] or '')): best = c
    return best or i

def version_at(keys, date):
    """Family member in force when a document dated `date` was issued: latest version issued on or before it (else the earliest)."""
    cands = {i for k in keys for i in key2docs.get(k, [])}
    if not cands: return None
    key = lambda i: (byid[i]['udstedt'] or '', byid[i]['nr'])
    before = [i for i in cands if date and (byid[i]['udstedt'] or '') <= date]
    return max(before, key=key) if before else min(cands, key=key)

stats = Counter()
for d in docs:
    f = d['f']; refs = Counter(); how = defaultdict(set)
    for k, n in f['nr'].items():
        yn, typ, dm = k.split('|'); y, nr = yn.split(':'); tid = f'lta-{y}-{nr}'
        t = byid.get(tid)
        if not t or tid == d['id']: continue
        ok = t['udstedt'] and f"{int(t['udstedt'][8:10])}.{int(t['udstedt'][5:7])}" == dm
        if not ok: stats['nr_date_mismatch'] += 1; continue
        refs[tid] += n; how[tid].add('nr')
    for ph, n in f['lovom'].items():
        k = match_lovom(ph)
        if k:
            c = version_at([k], d['udstedt'])
            if c and c != d['id']: refs[c] += n; how[c].add('lovom')
        else: stats['lovom_unmatched'] += 1
    for kn, n in f['kort'].items():
        c = version_at(['#' + kn], d['udstedt'])
        if c and c != d['id']: refs[c] += n; how[c].add('kort')
    # targets stay the cited (nr) or time-correct (name) version; the family's current version is kept beside it
    laws = Counter(); lhow = defaultdict(set); docrefs = Counter(); cur = {}
    for tid, n in refs.items():
        t = byid[tid]
        if tid == d['id']: continue
        if t['type'] in LAWT:
            laws[tid] += n; lhow[tid] |= how[tid]
            c = law_of_doc(tid)
            if c and c != tid: cur[tid] = c
        else: docrefs[tid] += n
    d['_laws'] = dict(laws.most_common(25)); d['_lhow'] = {k: sorted(v) for k, v in lhow.items() if k in d['_laws']}
    d['_cur'] = {k: v for k, v in cur.items() if k in d['_laws']}
    d['_docrefs'] = dict(docrefs.most_common(25))

def ntitle(t):
    t = re.sub(r'\(\*\s*\d*\)', ' ', t.lower()); return re.sub(r'[^a-zæøåé0-9 ]', ' ', t).split()
bek_by_title = defaultdict(list)
for d in docs:
    if d['type'] in ('bekendtgørelse', 'anordning'):
        bek_by_title[' '.join(ntitle(d['titel']))].append(d)

# --- hjemmel candidates for regulations (BEK etc.)
REGT = {'bekendtgørelse', 'ændringsbekendtgørelse', 'ikrafttrædelsesbekendtgørelse', 'anordning', 'ændringsanordning', 'ikrafttrædelsesanordning', 'bekendtgørelse-af-anordning'}
for d in docs:
    if d['type'] in LAWT:
        d['_family'] = law_of_doc(d['id'])
    if d['type'] in ('ændringsbekendtgørelse', 'ikrafttrædelsesbekendtgørelse', 'ikrafttrædelsesanordning', 'ændringsanordning'):
        t = clean(d['titel']); am = []
        m = re.match(r'^(?:bekendtgørelse|anordning) om ændring af (bekendtgørelse|anordning) (.+)$', t)
        if m:
            key = ' '.join(ntitle(m.group(1) + ' ' + m.group(2)))
            c = [x for x in bek_by_title.get(key, []) if (x['udstedt'] or '') <= (d['udstedt'] or '9')]
            if c:
                same = [x for x in c if x['prefix'] == d['prefix']] or c
                am.append(max(same, key=lambda x: (x['udstedt'] or '', x['nr']))['id'])
        for m in re.finditer(r'lov(?:en)? om ([^,()]+)', t):
            if d['type'] == 'ændringsbekendtgørelse': break
            k = match_lovom(m.group(1))
            if k:
                c = version_at([k], d['udstedt'])
                if c and c not in am: am.append(c)
        for m in re.finditer(r'\b([a-zæøå\-]{4,}loven)\b', t):
            if d['type'] == 'ændringsbekendtgørelse': break
            c = version_at(['#' + m.group(1)], d['udstedt'])
            if c and c not in am: am.append(c)
        d['_amends'] = am
        d['_amends_cur'] = {a: law_of_doc(a) for a in am if byid[a]['type'] in LAWT and law_of_doc(a) != a}
        d['_amends_rel'] = 'ændrer' if 'ændring' in d['type'] else 'sætter i kraft'
    if d['type'] == 'ændringslov':
        # amended law(s) from the title
        t = clean(d['titel']); am = []
        for m in re.finditer(r'lov(?:en)? om ([^,()]+)', t):
            k = match_lovom(m.group(1))
            if k:
                c = version_at([k], d['udstedt'])
                if c and c not in am: am.append(c)
        for m in re.finditer(r'\b([a-zæøå\-]{4,}loven)\b', t):
            c = version_at(['#' + m.group(1)], d['udstedt'])
            if c and c not in am: am.append(c)
        d['_amends'] = am
        d['_amends_cur'] = {a: law_of_doc(a) for a in am if law_of_doc(a) != a}
    if d['type'] in REGT:
        L = d['_laws']
        if not L: d['_hjemmel'] = None; continue
        top = list(L.items())
        best, n1 = top[0]; n2 = top[1][1] if len(top) > 1 else 0
        # title cue: 'bekendtgørelse om ikrafttræden af lov ...'
        d['_hjemmel'] = {'lov': best, 'n': n1, 'n2': n2, 'dominans': round(n1 / (n1 + n2), 2)}

# --- registry links
reg = json.load(open(os.path.join(SP, 'data', 'final.json')))
link = {}; reg_by_id = {n['id']: n for n in reg['nodes']}
AMEND_T = {'ændringslov', 'ændringsbekendtgørelse', 'ændringsanordning'}
for n in reg['nodes']:
    if n['type'] not in ('lov', 'bekendtgørelse', 'cirkulære', 'teknisk-forskrift', 'plan'): continue  # råd, tilsyn osv. kobles ikke til en retsakt
    ids = n.get('identifikatorer') or {}
    cands = []
    for m in re.finditer(r'\b(LBK|LOV|BEK)\s+nr\.?\s*(\d+)\s+af\s+\d{1,2}/\d{1,2}/(\d{4})', str(ids.get('lovtidende') or '')):
        cands.append(f'lta-{m.group(3)}-{m.group(2)}')
    for m in re.finditer(r'lta/(\d{4})/(\d+)', str(ids.get('eli') or '')):
        cands.append(f'lta-{m.group(1)}-{m.group(2)}')
    ok = [c for c in cands if c in byid and not (n['type'] in ('lov', 'bekendtgørelse') and byid[c]['type'] in AMEND_T)]
    if ok: link[n['id']] = ok[0]
    elif cands: stats['reg_link_missing'] += 1
# propagate registry link to family current version
fam_link = {}
for rid, did in link.items():
    d = byid[did]; fam = d.get('_family', did); fam_link.setdefault(fam, rid)

# --- evaluate hjemmel vs registry hjemmel_for edges (lov -> bek)
inv = dict(link)
ev = Counter(); bad = []
for e in reg['edges']:
    if e['type'] != 'hjemmel_for': continue
    a, b = e['from'], e['to']
    if a in inv and b in inv:
        da, db = byid[inv[a]], byid[inv[b]]
        if db['type'] not in REGT: continue
        h = db.get('_hjemmel')
        fa = da.get('_family', da['id'])
        if not h: ev['ingen_kandidat'] += 1; continue
        fams = {law_of_doc(t) for t in db['_laws']}
        if law_of_doc(h['lov']) == fa or fa in fams:
            ev['top' if law_of_doc(h['lov']) == fa else 'blandt'] += 1
        else: ev['forkert'] += 1; bad.append((b, a, h['lov'], byid[h['lov']]['titel'][:60]))
print('stats', dict(stats)); print('registry links', len(link), 'families linked', len(fam_link)); print('hjemmel eval', dict(ev)); print(bad[:12])
reg_t = Counter(d['type'] for d in docs if d['type'] in REGT and d['status_2026_06'] == 'gældende')
has = Counter(d['type'] for d in docs if d['type'] in REGT and d['status_2026_06'] == 'gældende' and d.get('_hjemmel'))
print('gældende regs with hjemmel cand', has, '/', reg_t)
cur_laws = [d for d in docs if d['type'] in LAWT and d['status_2026_06'] == 'gældende']
print('gældende love', len(cur_laws), 'heraf family==self', sum(1 for d in cur_laws if d['_family'] == d['id']))
json.dump({'docs': docs, 'link': link, 'fam_link': fam_link, 'hjemmel_eval': dict(ev), 'stats': dict(stats)}, open(os.path.join(HERE, 'data', 'resolved.json'), 'w'), ensure_ascii=False)
