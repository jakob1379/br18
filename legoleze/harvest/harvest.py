#!/usr/bin/env python3
"""Resumable, polite harvester for Retsinformation (www.retsinformation.dk + api.retsinformation.dk).

Rules it keeps (Retsinformation høsteservice): at most one request per 10 s, only within the opening hours
03:00–23:45 Danish time, back off on HTTP 429/5xx. Everything is stored on disk so it can be stopped and resumed.

  python3 harvest.py probe                 # 1 request: is the host reachable?
  python3 harvest.py sitemap               # sitemap index + pages -> data/sitemap.jsonl
  python3 harvest.py plan --seed-dir DIR   # prioritised worklist -> data/plan.jsonl
  python3 harvest.py fetch [--limit N]     # fetch XML in plan order -> data/xml/*.xml.gz
  python3 harvest.py parse                 # XML -> data/parsed.jsonl (meta, preamble/hjemmel, ministry, EU note, text)
  python3 harvest.py run --seed-dir DIR    # all of the above, resumable
  python3 harvest.py status
"""
import argparse, gzip, json, os, re, ssl, sys, time, urllib.error, urllib.request
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

HERE = Path(__file__).resolve().parent
DATA = HERE / 'data'
WWW = 'https://www.retsinformation.dk'
API = 'https://api.retsinformation.dk/v1'
UA = 'dk-regulering-kortlaegning/1.0 (forskningsprojekt; RAG-korpus over dansk regulering)'
MIN_GAP = 10.5                      # seconds between request starts
CPH = ZoneInfo('Europe/Copenhagen')
OPEN, CLOSE = (3, 0), (23, 45)
_last = [0.0]

def ctx():
    ca = os.environ.get('SSL_CERT_FILE') or ('/root/.ccr/ca-bundle.crt' if os.path.exists('/root/.ccr/ca-bundle.crt') else None)
    return ssl.create_default_context(cafile=ca) if ca else ssl.create_default_context()
SSL = ctx()

def wait_open(now=None):
    """Sleep until inside the opening hours (03:00–23:45 Copenhagen time). Returns seconds slept."""
    now = now or datetime.now(CPH)
    t = (now.hour, now.minute)
    if OPEN <= t < CLOSE: return 0
    nxt = now.replace(hour=OPEN[0], minute=OPEN[1], second=30, microsecond=0)
    if t >= CLOSE: nxt += timedelta(days=1)
    secs = (nxt - now).total_seconds()
    log(f'uden for åbningstid ({now:%H:%M}); venter til {nxt:%Y-%m-%d %H:%M}')
    time.sleep(max(0, secs)); return secs

def log(msg):
    line = f'{datetime.now(CPH):%Y-%m-%d %H:%M:%S} {msg}'
    print(line, flush=True)
    with open(DATA / 'harvest.log', 'a', encoding='utf-8') as fh: fh.write(line + '\n')

def get(url, accept='application/xml,text/xml,application/json;q=0.9,*/*;q=0.5', tries=6):
    """Rate-limited GET with backoff. Returns (status, bytes, content_type)."""
    back = 60
    for attempt in range(tries):
        wait_open()
        gap = MIN_GAP - (time.time() - _last[0])
        if gap > 0: time.sleep(gap)
        _last[0] = time.time()
        req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': accept, 'Accept-Encoding': 'gzip'})
        try:
            with urllib.request.urlopen(req, timeout=90, context=SSL) as r:
                body = r.read()
                if r.headers.get('Content-Encoding') == 'gzip': body = gzip.decompress(body)
                return r.status, body, r.headers.get('Content-Type', '')
        except urllib.error.HTTPError as e:
            if e.code in (404, 410): return e.code, b'', ''
            if e.code == 429 or e.code >= 500:
                ra = e.headers.get('Retry-After')
                delay = int(ra) if ra and ra.isdigit() else back
                log(f'HTTP {e.code} for {url}; venter {delay}s'); time.sleep(delay); back = min(back * 2, 1800); continue
            return e.code, b'', ''
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            reason = str(getattr(e, 'reason', e))
            if '403' in reason or 'Tunnel' in reason or 'tunnel' in reason:
                raise SystemExit(f'Netværket afviser {url} ({reason}). Tillad domænet i miljøets netværksindstillinger.')
            log(f'netværksfejl for {url}: {reason}; venter {back}s'); time.sleep(back); back = min(back * 2, 1800)
    return 0, b'', ''

# ---------------------------------------------------------------- sitemap
LOC = re.compile(r'<loc>\s*([^<]+?)\s*</loc>'); URLE = re.compile(r'<url>(.*?)</url>', re.S); LASTMOD = re.compile(r'<lastmod>\s*([^<]+?)\s*</lastmod>')

def cmd_sitemap(a):
    st, body, _ = get(f'{WWW}/sitemap.xml')
    if st != 200: raise SystemExit(f'sitemap index: HTTP {st}')
    pages = [u for u in LOC.findall(body.decode('utf-8', 'replace')) if 'sitemap' in u]
    log(f'sitemap: {len(pages)} sider')
    d = DATA / 'sitemap_pages'; d.mkdir(exist_ok=True)
    for i, p in enumerate(pages):
        f = d / f'page_{i:04d}.xml.gz'
        if f.exists(): continue
        st, b, _ = get(p)
        if st == 200: f.write_bytes(gzip.compress(b))
        else: log(f'sitemapside {p}: HTTP {st}')
    n = 0
    with open(DATA / 'sitemap.jsonl', 'w', encoding='utf-8') as out:
        for f in sorted(d.glob('page_*.xml.gz')):
            x = gzip.decompress(f.read_bytes()).decode('utf-8', 'replace')
            for u in URLE.findall(x):
                loc = LOC.search(u); lm = LASTMOD.search(u)
                if loc and '/eli/' in loc.group(1):
                    out.write(json.dumps({'loc': loc.group(1), 'lastmod': lm.group(1) if lm else None}) + '\n'); n += 1
    log(f'sitemap: {n} dokument-URL\'er')

# ---------------------------------------------------------------- plan
ELI = re.compile(r'/eli/([a-z]+)/(\d{4})/(\d+)')

def cmd_plan(a):
    """Priority: 1 = Lovtidende A not in the bulk harvest (new since 2026-02-12 or before 1852),
    2 = gældende LTA without text in the bulk, 3 = other gældende LTA (preamble/hjemmel, ministry, EU note),
    4 = other Retsinformation series (retsinfo = vejledninger/cirkulærer/skrivelser, fob, …), 5 = historic LTA."""
    seeds = {}
    if a.seed_dir:
        for f in os.listdir(a.seed_dir):
            m = re.match(r'(\d{4})_(\d+)\.json$', f)
            if not m: continue
            try: d = json.load(open(os.path.join(a.seed_dir, f)))
            except Exception: continue
            seeds[(int(m.group(1)), int(m.group(2)))] = (d.get('status'), bool(d.get('provisions')))
    rows = []; seen = set()
    for l in open(DATA / 'sitemap.jsonl', encoding='utf-8'):
        e = json.loads(l); m = ELI.search(e['loc'])
        if not m: continue
        series, y, n = m.group(1), int(m.group(2)), int(m.group(3))
        key = (series, y, n)
        if key in seen: continue
        seen.add(key)
        if series == 'lta':
            s = seeds.get((y, n))
            pri = 1 if s is None else (2 if s[0] == 'in_force' and not s[1] else 3 if s[0] == 'in_force' else 5)
        else:
            pri = 4
        rows.append({'pri': pri, 'series': series, 'aar': y, 'nr': n, 'loc': e['loc'], 'lastmod': e['lastmod'],
                     'xml': f'{WWW}/eli/{series}/{y}/{n}/xml'})
    rows.sort(key=lambda r: (r['pri'], -r['aar'], -r['nr']))
    with open(DATA / 'plan.jsonl', 'w', encoding='utf-8') as fh:
        for r in rows: fh.write(json.dumps(r) + '\n')
    from collections import Counter
    c = Counter(r['pri'] for r in rows); log(f'plan: {len(rows)} dokumenter, pr. prioritet {dict(sorted(c.items()))}')
    hrs = {p: round(c[p] * MIN_GAP / 3600 * 24 / 20.75, 1) for p in c}
    log(f'skønnet tid (inkl. lukketid) pr. prioritet i timer: {hrs}')

# ---------------------------------------------------------------- fetch
def xml_path(r): return DATA / 'xml' / r['series'] / f"{r['aar']}_{r['nr']}.xml.gz"

def cmd_fetch(a):
    (DATA / 'xml').mkdir(exist_ok=True)
    done = 0; status_f = DATA / 'fetch_status.jsonl'
    skip = set()
    if status_f.exists():
        for l in open(status_f): e = json.loads(l); skip.add(e['key']) if e['status'] in (200, 404, 410) else None
    for l in open(DATA / 'plan.jsonl', encoding='utf-8'):
        r = json.loads(l)
        if a.max_pri and r['pri'] > a.max_pri: break
        key = f"{r['series']}/{r['aar']}/{r['nr']}"; p = xml_path(r)
        if key in skip or p.exists(): continue
        st, body, ct = get(r['xml'])
        if st == 200 and b'<Dokument' not in body[:4000]: st = 'ikke-xml'
        if st == 200:
            p.parent.mkdir(parents=True, exist_ok=True); p.write_bytes(gzip.compress(body))
        with open(status_f, 'a') as fh: fh.write(json.dumps({'key': key, 'status': st, 'pri': r['pri'], 'at': datetime.now(CPH).isoformat(timespec='seconds')}) + '\n')
        done += 1
        if done % 25 == 0: log(f'hentet {done} (seneste {key}, prioritet {r["pri"]})')
        if a.limit and done >= a.limit: break
    log(f'fetch færdig for denne kørsel: {done} forespørgsler')

# ---------------------------------------------------------------- parse
TAG = re.compile(r'<[^>]+>')
def text_of(xml):
    t = re.sub(r'<(?:/(?:Char|Linea|Exitus|Explicatus|Stk|Paragraf|Kapitel|Nr|Litra)|br\s*/?)>', '\n', xml)
    t = TAG.sub(' ', t)
    for a, b in (('&amp;', '&'), ('&lt;', '<'), ('&gt;', '>'), ('&quot;', '"'), ('&apos;', "'"), ('&#xA0;', ' '), ('&nbsp;', ' ')): t = t.replace(a, b)
    return re.sub(r'[ \t]+', ' ', re.sub(r'\n\s*\n+', '\n', t)).strip()

R_PRE = re.compile(r'((?:I medfør af|I henhold til|Efter bemyndigelse).{0,2500}?(?:fastsættes|bestemmes|bekendtgøres)[^:\n]{0,80}:?)', re.S)
R_BODY = re.compile(r'\n\s*(?:Kapitel 1\b|§ 1\.)')
R_EU = re.compile(r'([^.\n]{0,200}(?:indeholder bestemmelser,? der gennemfører|gennemfører dele af|til gennemførelse af)[^\n]{0,600}?(?:direktiv|forordning)[^\n]{0,400})', re.I)
R_SIG = re.compile(r'([A-ZÆØÅ][\w\-,. ]{3,120}?(?:ministeriet|Styrelsen|styrelsen|Direktoratet|direktoratet|Tilsynet|tilsynet|Nævnet|nævnet)[^\n]{0,40}?,? den \d{1,2}\. \w+ \d{4})')

def meta_of(xml):
    """All simple <Tag>value</Tag> children of <Meta>; repeated tags become lists."""
    m = re.search(r'<Meta[^>]*>(.*?)</Meta>', xml, re.S)
    out = {}
    if not m: return out
    for tag, val in re.findall(r'<([A-Za-z]\w*)\b[^>]*>([^<]*)</\1>', m.group(1)):
        v = val.strip()
        if not v: continue
        if tag not in out: out[tag] = v
        elif isinstance(out[tag], list): out[tag].append(v)
        else: out[tag] = [out[tag], v]
    return out

def cmd_parse(a):
    n = 0
    with open(DATA / 'parsed.jsonl', 'w', encoding='utf-8') as out:
        for f in sorted((DATA / 'xml').rglob('*.xml.gz')):
            xml = gzip.decompress(f.read_bytes()).decode('utf-8', 'replace')
            meta = meta_of(xml); txt = text_of(re.sub(r'<Meta[^>]*>.*?</Meta>', '', xml, flags=re.S))
            b = R_BODY.search(txt); head = txt[:b.start()] if b and b.start() < 8000 else txt[:4000]; tail = txt[-3000:]
            pre = R_PRE.search(head); sig = R_SIG.findall(tail)
            eu = list(dict.fromkeys(e.strip() for e in R_EU.findall(txt[:2000] + '\n' + (tail if len(txt) > 2000 else ''))))
            series = f.parent.name; y, nr = f.name[:-7].split('_')
            out.write(json.dumps({'id': f'{series}-{y}-{nr}', 'series': series, 'meta': meta,
                                  'praeambel': pre.group(1).strip() if pre else None, 'eu_note': eu[:5],
                                  'underskrift': sig[-1].strip() if sig else None, 'n_tegn': len(txt), 'tekst': txt}, ensure_ascii=False) + '\n')
            n += 1
    log(f'parse: {n} dokumenter -> data/parsed.jsonl')

def cmd_probe(a):
    st, body, ct = get(f'{API}/Documents?date={(datetime.now(CPH) - timedelta(days=1)):%Y-%m-%d}', accept='application/json')
    print('api.retsinformation.dk /v1/Documents:', st, ct, len(body))
    if st == 200:
        try: d = json.loads(body); print('første post:', json.dumps(d[0] if isinstance(d, list) and d else d, ensure_ascii=False)[:600])
        except Exception: print(body[:300])

def cmd_status(a):
    from collections import Counter
    pl = [json.loads(l) for l in open(DATA / 'plan.jsonl')] if (DATA / 'plan.jsonl').exists() else []
    st = [json.loads(l) for l in open(DATA / 'fetch_status.jsonl')] if (DATA / 'fetch_status.jsonl').exists() else []
    ok = Counter(e['pri'] for e in st if e['status'] == 200); tot = Counter(r['pri'] for r in pl)
    print('plan:', dict(sorted(tot.items())), '| hentet ok:', dict(sorted(ok.items())), '| fejl:', Counter(str(e['status']) for e in st if e['status'] != 200))

def cmd_run(a):
    if not (DATA / 'sitemap.jsonl').exists(): cmd_sitemap(a)
    if not (DATA / 'plan.jsonl').exists(): cmd_plan(a)
    cmd_fetch(a); cmd_parse(a)

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('cmd', choices=['probe', 'sitemap', 'plan', 'fetch', 'parse', 'run', 'status'])
    ap.add_argument('--seed-dir'); ap.add_argument('--limit', type=int); ap.add_argument('--max-pri', type=int)
    a = ap.parse_args(); DATA.mkdir(exist_ok=True)
    globals()['cmd_' + a.cmd](a)
