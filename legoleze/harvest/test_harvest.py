import gzip, io, json, sys, time, types, urllib.error, urllib.request
from datetime import datetime
from pathlib import Path
sys.path.insert(0, '/tmp/claude-0/-home-user-ai-job-search-fork/9c9ad245-1536-5d87-980d-1a4837c57ed1/scratchpad/harvest')
import harvest as H
TD = Path(__file__).resolve().parent / 'data'; TD.mkdir(exist_ok=True); H.DATA = TD
# 1) opening hours
assert H.wait_open(datetime(2026, 11, 2, 12, 0, tzinfo=H.CPH)) == 0
orig_sleep = time.sleep; slept = []
time.sleep = lambda s: slept.append(s)
H.wait_open(datetime(2026, 11, 2, 23, 50, tzinfo=H.CPH)); assert 3.1 * 3600 < slept[-1] < 3.3 * 3600, slept[-1]
H.wait_open(datetime(2026, 11, 3, 1, 0, tzinfo=H.CPH)); assert 1.9 * 3600 < slept[-1] < 2.1 * 3600, slept[-1]
# 2) rate limit + 429 backoff with a fake opener
H.wait_open = lambda now=None: 0
calls = []
class Resp:
    def __init__(s, body): s.body = body; s.status = 200; s.headers = {'Content-Type': 'application/xml'}
    def read(s): return s.body
    def __enter__(s): return s
    def __exit__(s, *a): pass
def fake(req, timeout=0, context=None):
    calls.append(time.time())
    if len(calls) == 1: raise urllib.error.HTTPError(req.full_url, 429, 'Too Many', {'Retry-After': '5'}, None)
    return Resp(b'<Dokument><Meta><DocumentType>BEK H#LOKDOK04</DocumentType></Meta></Dokument>')
urllib.request.urlopen = fake; slept.clear()
st, body, ct = H.get('https://www.retsinformation.dk/eli/lta/2019/1399/xml')
assert st == 200 and b'Dokument' in body and 5 in slept, (st, slept)
# 3) parsing on a realistic body
xml = '''<Dokument><Meta><DocumentType>BEK H#LOKDOK04</DocumentType><AccessionNumber>A20190139929</AccessionNumber><DocumentTitle>Bekendtgørelse om bygningsreglement 2018 (BR18)</DocumentTitle>
<Year>2019</Year><Number>1399</Number><DiesSigni>2019-12-12</DiesSigni><Ministry>Trafik-, Bygge- og Boligstyrelsen</Ministry><Ministry>Transport- og Boligministeriet</Ministry></Meta>
<IndledningGruppe><Indledning><Char>I medfør af § 5, stk. 2, § 6 og § 12 i lov om byggeri, jf. lovbekendtgørelse nr. 1178 af 23. september 2016, fastsættes efter bemyndigelse:</Char></Indledning></IndledningGruppe>
<Kapitel><Explicatus>Kapitel 1</Explicatus><Paragraf><Explicatus>§ 1.</Explicatus><Char>Bygningsreglementet gælder for opførelse af nye bygninger.</Char></Paragraf></Kapitel>
<Exitus><Char>Trafik-, Bygge- og Boligstyrelsen, den 12. december 2019</Char><Char>Thomas Kjær</Char></Exitus>
<Noter><Char>Bekendtgørelsen indeholder bestemmelser, der gennemfører dele af Europa-Parlamentets og Rådets direktiv 2010/31/EU af 19. maj 2010 om bygningers energimæssige ydeevne.</Char></Noter></Dokument>'''
d = TD / 'xml' / 'lta'; d.mkdir(parents=True, exist_ok=True); (d / '2019_1399.xml.gz').write_bytes(gzip.compress(xml.encode()))
H.cmd_parse(None)
r = json.loads(open(TD / 'parsed.jsonl').readline())
print(json.dumps({k: r[k] for k in ('id', 'meta', 'praeambel', 'eu_note', 'underskrift', 'n_tegn')}, ensure_ascii=False, indent=1))
assert r['meta']['Ministry'] == ['Trafik-, Bygge- og Boligstyrelsen', 'Transport- og Boligministeriet']
assert r['praeambel'].startswith('I medfør af § 5') and 'fastsættes' in r['praeambel']
assert r['eu_note'] and '2010/31/EU' in r['eu_note'][0]
assert r['underskrift'] and r['underskrift'].startswith('Trafik-, Bygge- og Boligstyrelsen, den 12. december 2019'), r['underskrift']
# 4) plan priorities
(TD / 'sitemap.jsonl').write_text('\n'.join(json.dumps({'loc': u, 'lastmod': None}) for u in [
    'https://www.retsinformation.dk/eli/lta/2026/600', 'https://www.retsinformation.dk/eli/lta/2019/1399', 'https://www.retsinformation.dk/eli/retsinfo/2019/10226',
    'https://www.retsinformation.dk/eli/lta/1975/38', 'https://www.retsinformation.dk/eli/lta/1922/252']) + '\n')
H.cmd_plan(types.SimpleNamespace(seed_dir='/home/user/ansvar-systems/danish-law-mcp/data/seed'))
print([ (r['pri'], r['series'], r['aar'], r['nr']) for r in map(json.loads, open(TD / 'plan.jsonl'))])
time.sleep = orig_sleep
print('ALLE TESTS OK')
