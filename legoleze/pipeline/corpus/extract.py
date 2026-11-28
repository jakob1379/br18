#!/usr/bin/env python3
"""Pass 1: Retsinformation LTA seeds (danish-law-mcp) -> data/docs.jsonl (meta + text features).

    python3 extract.py <seed-dir>
    python3 extract.py selftest
"""
import json, os, re, sys
from collections import Counter
from multiprocessing import Pool

SEED = sys.argv[1]
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'docs.jsonl')
MONTHS = {m: i + 1 for i, m in enumerate('januar februar marts april maj juni juli august september oktober november december'.split())}

def norm_type(sn, title):
    s = (sn or '').strip(); t = title.lower()
    if s.startswith('LOV Æ') or s == 'Ændringslov': return 'ændringslov'
    if s.startswith('LBK') or s == 'Lovbekendtgørelse': return 'lovbekendtgørelse'
    if s.startswith('LOV') or s == 'Lov' or s.startswith('LSV'):
        return 'ændringslov' if t.startswith('lov om ændring af') else 'lov'
    if s.startswith('BEK Æ') or s == 'Ændringsbekendtgørelse': return 'ændringsbekendtgørelse'
    if s.startswith('BEK I') or s.startswith('Ikrafttræd. bek'): return 'ikrafttrædelsesbekendtgørelse'
    if s.startswith('BKI') or s == 'Bekendtgørelse (international)': return 'bekendtgørelse-international'
    if s.startswith('BEK') or s == 'Bekendtgørelse':
        return 'ændringsbekendtgørelse' if t.startswith('bekendtgørelse om ændring af') else 'bekendtgørelse'
    if s.startswith('AND Æ') or s == 'Ændringsanordning': return 'ændringsanordning'
    if s.startswith('AND I') or s.startswith('ANG') or s.startswith('Ikrafttræd. anordning'): return 'ikrafttrædelsesanordning'
    if s.startswith('AND') or s == 'Anordning': return 'anordning'
    if s.startswith('ABK'): return 'bekendtgørelse-af-anordning'
    if s.startswith('ÅBR') or s.startswith('Åbent'): return 'åbent-brev'
    return 'ukendt'

ABBR = {'lov': 'LOV', 'ændringslov': 'LOV', 'lovbekendtgørelse': 'LBK', 'bekendtgørelse': 'BEK', 'ændringsbekendtgørelse': 'BEK',
        'ikrafttrædelsesbekendtgørelse': 'BEK', 'bekendtgørelse-international': 'BKI', 'anordning': 'AND', 'ændringsanordning': 'AND',
        'ikrafttrædelsesanordning': 'ANG', 'bekendtgørelse-af-anordning': 'ABK', 'åbent-brev': 'ÅBR', 'ukendt': '?'}

DATE = r'(\d{1,2})\.? ?(januar|februar|marts|april|maj|juni|juli|august|september|oktober|november|december) (\d{4})'
R_NR = re.compile(r'\b(lovbekendtgørelse|bekendtgørelse|lov|anordning)\s+nr\.?\s*(\d+)\s+af\s+' + DATE, re.I)
R_LOVOM = re.compile(r'\blov(?:en)? om ((?:[a-zæøåé0-9\-]+[ ,]{0,2}){1,18})', re.I)
R_KORT = re.compile(r'\b([a-zæøå][a-zæøå\-]{3,}loven)\b')
R_MIN = re.compile(r'\b((?:[a-zæøå]+-,? )*(?:[a-zæøå]+- og )?[a-zæøå]*ministeren)\b', re.I)
R_MINFOR = re.compile(r'\bministeren for ((?:[a-zæøå\-]+(?:,| og)? ){0,6}[a-zæøå\-]+)', re.I)
R_STY = re.compile(r'\b([A-ZÆØÅ][a-zæøå\-]+styrelsen|Styrelsen for (?:[A-ZÆØÅa-zæøå\-]+(?:,| og)? ){0,5}[A-ZÆØÅa-zæøå\-]+|[A-ZÆØÅ][a-zæøå\-]+tilsynet|[A-ZÆØÅ][a-zæøå\-]+direktoratet)\b')
R_DIR = re.compile(r'direktiv(?:et|er|erne)?(?:\s+|(?=\())(?:nr\.\s*)?(?:\((EU|EF|EØF|Euratom)\)\s*(?:nr\.\s*)?)?(\d{2,4})/(\d{1,4})(?:/(EØF|EF|EU|Euratom|EURATOM))?', re.I)
R_REG_OLD = re.compile(r'forordning(?:en|er|erne)?\s+\((EU|EF|EØF|Euratom)\)\s+nr\.\s*(\d{1,5})/(\d{2,4})', re.I)
R_REG_NEW = re.compile(r'forordning(?:en|er|erne)?\s+\((EU|Euratom)\)\s+(\d{4})/(\d{1,5})', re.I)
R_DEC = re.compile(r'(?:afgørelse|beslutning)\s+(?:\((EU|EF)\)\s+)?(\d{4})/(\d{1,4})(?:/(EU|EF|EØF))?', re.I)

R_GF = re.compile(r'\b(?:gennemfører|gennemføres|gennemført|gennemføre|til gennemførelse af|implementerer|implementeres|implementering af)\b', re.I)

def y4(y):
    y = int(y)
    return y + 1900 if y < 100 and y > 50 else (y + 2000 if y < 100 else y)

def eu_refs(text):
    out = Counter(); gf = set()
    for m in R_DIR.finditer(text):
        a, b = m.group(2), m.group(3)
        if m.group(1) and len(a) == 4: yr, nr = int(a), int(b)
        else: yr, nr = y4(a), int(b)
        if 1957 < yr <= 2026: k = f'dir:{yr}/{nr}'; out[k] += 1
    for m in R_REG_OLD.finditer(text):
        yr, nr = y4(m.group(3)), int(m.group(2))
        if 1957 < yr <= 2026: out[f'reg:{yr}/{nr}'] += 1
    for m in R_REG_NEW.finditer(text):
        yr, nr = int(m.group(2)), int(m.group(3))
        if 2014 < yr <= 2026: out[f'reg:{yr}/{nr}'] += 1
    for m in R_DEC.finditer(text):
        yr, nr = int(m.group(2)), int(m.group(3))
        if (m.group(1) or m.group(4)) and 1957 < yr <= 2026: out[f'dec:{yr}/{nr}'] += 1
    return out

def process(f):
    try:
        d = json.load(open(os.path.join(SEED, f)))
    except Exception as e:
        return {'_err': f, 'e': str(e)}
    if 'provisions' not in d: return None
    i = d.get('_ingest', {}) or {}
    if re.match(r'^\d{4}:\d+$', d['id']): yr, nr = d['id'].split(':')
    else: yr, nr = f[:-5].split('_', 1)
    typ = norm_type(d.get('short_name'), d['title'])
    iss = d.get('issued_date') or ''
    lt = f"{ABBR[typ]} nr. {nr} af {iss[8:10]}/{iss[5:7]}/{iss[:4]}" if iss else None
    did = i.get('document_id') or ''
    pre = re.match(r'[A-Z]+', did)
    provs = d.get('provisions') or []
    text = '\n'.join(p.get('content', '') for p in provs)
    nr_refs = Counter(); lovom = Counter(); kort = Counter(); mins = Counter(); stys = Counter(); eu = Counter(); gfe = set()
    for m in R_NR.finditer(text):
        nr_refs[f"{m.group(5)}:{m.group(2)}|{m.group(1).lower()}|{m.group(3)}.{MONTHS[m.group(4).lower()]}"] += 1
    for m in R_LOVOM.finditer(text): lovom[m.group(1).strip(' ,').lower()[:160]] += 1
    for m in R_KORT.finditer(text): kort[m.group(1)] += 1
    for m in R_MIN.finditer(text):
        w = m.group(1).lower()
        if w not in ('ministeren',): mins[w] += 1
    for m in R_MINFOR.finditer(text): mins['ministeren for ' + m.group(1).lower()] += 1
    for m in R_STY.finditer(text): stys[m.group(1)] += 1
    for p in provs:
        c = p.get('content', '')
        e = eu_refs(c)
        eu.update(e)
        # implementerer_EU only for directives, and only with a real verb phrase ("gennemfører", "til gennemførelse af direktiv");
        # compounds such as "gennemførelsesforordning" do not count, and regulations are directly applicable (henviser_til)
        if e and R_GF.search(c): gfe.update(k for k in e if k.startswith('dir:'))
    tmin = Counter(m.group(1).lower() for m in R_MIN.finditer(d['title']))
    return {
        'id': f'lta-{yr}-{nr}', 'aar': int(yr), 'nr': int(nr), 'titel': d['title'].replace('\\n', ' ').strip(), 'short_name': d.get('short_name'),
        'type': typ, 'lovtidende': lt, 'status_2026_06': {'Valid': 'gældende', 'Historic': 'historisk'}.get(i.get('upstream_status'), i.get('upstream_status')),
        'udstedt': iss or None, 'ikraft': d.get('in_force_date'), 'gyldig_fra': i.get('start_date'), 'gyldig_til': i.get('end_date'),
        'historisk_markeret': i.get('historic_marked'), 'url_xml': d.get('url'), 'document_id': did or None, 'prefix': pre.group(0) if pre else None,
        'accession': i.get('accession'), 'unique_document_id': i.get('unique_document_id'), 'retrieved_at': i.get('retrieved_at'),
        'n_prov': len(provs), 'n_chars': len(text), 'n_def': len(d.get('definitions') or []),
        'f': {'nr': dict(nr_refs.most_common(60)), 'lovom': dict(lovom.most_common(40)), 'kort': dict(kort.most_common(30)),
              'min': dict(mins.most_common(8)), 'tmin': dict(tmin), 'sty': dict(stys.most_common(8)),
              'eu': dict(eu.most_common(60)), 'eu_gf': sorted(gfe)},
        'seed_file': f, 'seed_id': d['id'],
    }

if __name__ == '__main__':
    if SEED == 'selftest':
        assert eu_refs('direktiv(EU) 2023/1791 af 13. september 2023 samt ophævelse af direktiv 2012/27/EU') == {'dir:2023/1791': 1, 'dir:2012/27': 1}
        assert eu_refs('direktiv (EU) 2023/1791, direktivet(EU) 2018/2001 og direktiv nr. 98/24/EF') == {'dir:2023/1791': 1, 'dir:2018/2001': 1, 'dir:1998/24': 1}
        assert not eu_refs('direktiv2012/27/EU, direktivforslag (EU) 2023/1791 og direktiv(er) 2012/27')
        print('selftest ok'); sys.exit()
    files = sorted(x for x in os.listdir(SEED) if x.endswith('.json'))
    n = 0; errs = []
    with Pool(4) as p, open(OUT, 'w', encoding='utf-8') as fh:
        for r in p.imap_unordered(process, files, chunksize=200):
            if r is None: continue
            if '_err' in r: errs.append(r); continue
            fh.write(json.dumps(r, ensure_ascii=False) + '\n'); n += 1
    print('docs', n, 'errors', len(errs), errs[:3])
