#!/usr/bin/env python3
"""Assemble the catalog layer (dk-regulering/katalog/) from resolved corpus data + Haiku ressort results.

Outputs
  katalog/retsinformation_lta.jsonl   one record per Lovtidende A document (62,762)
  katalog/kanter.jsonl                edges (allowed types only) from catalog docs
  katalog/eu_index.jsonl              EU acts referenced in the corpus (CELEX derived by syntax)
"""
import json, os, re
from collections import Counter, defaultdict
HERE = os.path.dirname(os.path.abspath(__file__)); SP = os.path.dirname(HERE)
OUT = os.path.join(SP, 'dk-regulering', 'katalog')
REPO = 'https://github.com/Ansvar-Systems/danish-law-mcp'
COMMIT = 'da22657b7aa604e0a900d69b2b60a7b0c424b0cb'
CELEX_HELP = 'https://eur-lex.europa.eu/content/help/eurlex-content/celex-number.html'
CODES = {'STM': 'min-statsministeriet', 'OIM': 'min-oekonomi-og-indenrigs', 'UM': 'min-udenrigs', 'EM': 'min-erhverv', 'FM': 'min-finans',
         'JM': 'min-justits', 'FUD': 'min-forskning-uddannelse-og-digitalisering', 'KEFM': 'min-klima-energi-og-forsyning',
         'BLT': 'min-by-land-og-transport', 'UIM': 'min-udlaendinge-og-integration', 'UVM': 'min-undervisning', 'BLM': 'min-beskaeftigelse-og-ligestilling',
         'FMN': 'min-forsvar', 'SVM': 'min-skat-og-vaekst', 'SKM': 'min-sundhed-og-kirke', 'MND': 'min-natur-og-dyrevelfaerd', 'KUM': 'min-kultur',
         'MSB': 'min-samfundssikkerhed-og-beredskab', 'BAB': 'min-boern-aeldre-og-bolig', 'SOM': 'min-social', 'MIM': 'min-miljoe', 'FT': 'ingen', 'UKENDT': 'ukendt'}
SCOPE = {'byggeri': 'byggeri', 'bolig': 'bolig', 'plan-landdistrikter': 'plan', 'energi-forsyning': 'energi', 'klima': 'energi', 'miljoe': 'miljø',
         'affald': 'miljø', 'natur-vandmiljoe': 'miljø', 'arbejdsmiljoe': 'arbejdsmiljø', 'beredskab-brand': 'brand', 'el-gas-vvs': 'el/gas/VVS'}
LAWT = {'lov', 'lovbekendtgørelse'}

def territorium(title):
    t = title.lower(); gl = bool(re.search(r'grønland|grønlandsk', t)); fo = bool(re.search(r'færø', t))
    return 'GL+FO' if gl and fo else 'GL' if gl else 'FO' if fo else 'DK'

def rolle(d):
    t = d['type']; ti = d['titel'].lower()
    if t in ('ændringslov', 'ændringsbekendtgørelse', 'ændringsanordning'): return 'ændring'
    if t in ('ikrafttrædelsesbekendtgørelse', 'ikrafttrædelsesanordning'): return 'ikrafttræden'
    if re.match(r'^(bekendtgørelse|lov|anordning) om ophævelse af', ti): return 'ophævelse'
    return 'hoved'

def eu_id(k):
    t, yn = k.split(':'); y, n = yn.split('/')
    return f"eu-{t}-{y}-{int(n)}", f"3{y}{ {'dir': 'L', 'reg': 'R', 'dec': 'D'}[t] }{int(n):04d}".replace(' ', '')

def main():
    R = json.load(open(os.path.join(HERE, 'data', 'resolved.json')))
    docs = R['docs']; byid = {d['id']: d for d in docs}
    link = defaultdict(list)
    for rid, did in sorted(R['link'].items()): link[did].append(rid)
    U = json.load(open(os.path.join(HERE, 'data', 'udsteder.json')))
    rp = os.path.join(HERE, 'data', 'ressort.json')
    RS = json.load(open(rp)) if os.path.exists(rp) else {}
    reg = json.load(open(os.path.join(SP, 'data', 'final.json')))
    reg_ids = {n['id'] for n in reg['nodes']}
    reg_min = {n['id']: n for n in reg['nodes'] if n['type'] == 'ministerium'}
    reg_nodes = {n['id']: n for n in reg['nodes']}
    ress_edge = {(e['from'], e['to']): e for e in reg['edges'] if e['type'] == 'ressortansvar'}
    os.makedirs(OUT, exist_ok=True)
    eu = defaultdict(lambda: {'n_dok': 0, 'n_gaeldende': 0, 'implementeres_af': 0})
    st = Counter(); edges = []
    with open(os.path.join(OUT, 'retsinformation_lta.jsonl'), 'w', encoding='utf-8') as fh:
        for d in docs:
            did = d['id']; src = [d['url_xml']] if d.get('url_xml') else []
            u = U[did]; r = RS.get(did)
            rec = {
                'id': did, 'navn': d['titel'], 'type': d['type'], 'kilder': src,
                'status': {'vaerdi': d['status_2026_06'], 'pr': (d.get('retrieved_at') or '')[:10] or None, 'sikkerhed': 'verificeret' if src else 'sandsynlig'},
                'identifikatorer': {'lovtidende': d['lovtidende'], 'document_id': d.get('document_id'), 'accession': d.get('accession'),
                                    'unique_document_id': d.get('unique_document_id'), 'sikkerhed': 'verificeret' if src else 'sandsynlig'},
                'datoer': {k: v for k, v in (('udstedt', d['udstedt']), ('historisk_markeret', d['historisk_markeret']),
                           ('ri_registreret', d['gyldig_fra']), ('ri_aendret', d['gyldig_til'])) if v},
                'territorium': territorium(d['titel']), 'dokumentrolle': rolle(d),
                'udstedt_af': {'vaerdi': u['udstedt_af'] or 'ukendt', 'metode': u['metode'], 'praefiks': u['prefix'],
                               'sikkerhed': 'sandsynlig' if u['udstedt_af'] else 'ukendt'},
                'seed_fil': d['seed_file'], 'n_paragraffer': d['n_prov'], 'n_definitioner': d['n_def'],
            }
            if r:
                mid = CODES.get(r['m'], 'ukendt')
                rec['ministerium'] = {'vaerdi': mid, 'sikkerhed': 'sandsynlig' if (r['s'] == 's' and mid not in ('ukendt',)) else 'ukendt', 'metode': r.get('model', 'haiku')}
                # a curated registry node with a ressortansvar edge wins over the classification
                for rid in link.get(did, []):
                    rn = reg_nodes[rid]; rm = rn.get('ministerium')
                    e = ress_edge.get((rm, rid))
                    if rm in reg_min and rn.get('status') == 'aktiv' and e:
                        if rm != mid: st['ressort_fra_registry_rettet'] += 1
                        mid = rm
                        rec['ministerium'] = {'vaerdi': rm, 'sikkerhed': e['sikkerhed'], 'metode': 'registry', 'kilder': e.get('kilder', []), 'registry_kant': f'{rm}|ressortansvar|{rid}'}
                        break
                rec['retsomraade'] = r['o']
                if SCOPE.get(r['o']): rec['domaener'] = [SCOPE[r['o']]]
                if mid not in ('ukendt', 'ingen') and mid in reg_min:
                    reg_m = rec['ministerium']['metode'] == 'registry'
                    edges.append({'from': mid, 'type': 'ressortansvar', 'to': did,
                                  'beskrivelse': 'Nuværende ressort (fra registry-noden)' if reg_m else 'Nuværende ressort (klassifikation)',
                                  'kilder': rec['ministerium'].get('kilder', []) if reg_m else [], 'sikkerhed': rec['ministerium']['sikkerhed'],
                                  'metode': 'registry' if reg_m else rec['ministerium']['metode'] + '-klassifikation'})
                st['ressort_' + rec['ministerium']['sikkerhed']] += 1
            if d['type'] in LAWT and d.get('_family') and d['_family'] != did:
                rec['gaeldende_version' if byid[d['_family']]['status_2026_06'] == 'gældende' else 'nyeste_version_afloeser_mangler'] = d['_family']
            if d['type'] in LAWT and d['_family'] == did and d['status_2026_06'] == 'historisk' and not d.get('historisk_markeret', '') < '2026-02-13':
                rec['afloeser_mangler'] = True  # marked historic after the dataset's last issue date: successor not in the harvest
            if d.get('_amends'):
                rec['aendrer'] = d['_amends']
                for t in d['_amends']:
                    e = {'from': did, 'type': 'henviser_til', 'to': t, 'beskrivelse': f"{d.get('_amends_rel', 'ændrer')} (ifølge titlen; versionen der gjaldt på tidspunktet)", 'kilder': src,
                         'sikkerhed': 'sandsynlig', 'metode': 'titel-navnematch'}
                    c = d.get('_amends_cur', {}).get(t)
                    if c: e['gaeldende_version' if byid[c]['status_2026_06'] == 'gældende' else 'nyeste_version_afloeser_mangler'] = c
                    edges.append(e)
            if did in link: rec['registry_ids'] = link[did]
            # law references from text
            for t, n in list(d['_laws'].items())[:15]:
                how = d['_lhow'].get(t, [])
                if t in (d.get('_amends') or []): continue
                e = {'from': did, 'type': 'henviser_til', 'to': t,
                     'beskrivelse': f'nævner loven {n} gang(e) i teksten' + ('' if 'nr' in how else ' (navnematch; versionen der gjaldt ved udstedelsen)'),
                     'kilder': src, 'sikkerhed': 'verificeret' if 'nr' in how and src else 'sandsynlig', 'metode': '+'.join(how) or 'navnematch'}
                c = d.get('_cur', {}).get(t)
                if c: e['gaeldende_version' if byid[c]['status_2026_06'] == 'gældende' else 'nyeste_version_afloeser_mangler'] = c
                edges.append(e)
            for t, n in list(d['_docrefs'].items())[:10]:
                edges.append({'from': did, 'type': 'henviser_til', 'to': t, 'beskrivelse': f'nævner dokumentet (nr. og dato) {n} gang(e)',
                              'kilder': src, 'sikkerhed': 'verificeret' if src else 'sandsynlig', 'metode': 'nr+dato'})
            # EU
            gf = set(d['f']['eu_gf']); eus = []
            for k, n in list(d['f']['eu'].items())[:40]:
                eid, celex = eu_id(k); eus.append(eid)
                e = eu[eid]; e['celex'] = celex; e['n_dok'] += 1; e['n_gaeldende'] += d['status_2026_06'] == 'gældende'
                if k in gf:
                    e['implementeres_af'] += 1
                    edges.append({'from': did, 'type': 'implementerer_EU', 'to': eid, 'beskrivelse': 'direktivet nævnes i samme bestemmelse som "gennemfører"/"til gennemførelse af"/"implementerer"',
                                  'kilder': src, 'sikkerhed': 'sandsynlig', 'metode': 'tekst-samforekomst'})
                else:
                    edges.append({'from': did, 'type': 'henviser_til', 'to': eid, 'beskrivelse': f'nævner EU-retsakten {n} gang(e)',
                                  'kilder': src, 'sikkerhed': 'verificeret' if src else 'sandsynlig', 'metode': 'tekst-regex'})
            if eus: rec['eu_referencer'] = eus
            fh.write(json.dumps(rec, ensure_ascii=False) + '\n'); st['docs'] += 1
    # dedupe edges
    seen = set(); E = []
    for e in edges:
        k = (e['from'], e['type'], e['to'])
        if k in seen: continue
        seen.add(k); E.append(e)
    with open(os.path.join(OUT, 'kanter.jsonl'), 'w', encoding='utf-8') as fh:
        for e in E: fh.write(json.dumps(e, ensure_ascii=False) + '\n')
    with open(os.path.join(OUT, 'eu_index.jsonl'), 'w', encoding='utf-8') as fh:
        for eid, e in sorted(eu.items(), key=lambda x: -x[1]['n_dok']):
            t = eid.split('-')[1]
            fh.write(json.dumps({'id': eid, 'type': {'dir': 'eu-direktiv', 'reg': 'eu-forordning', 'dec': 'eu-afgørelse'}[t],
                                 'identifikatorer': {'celex': e['celex'], 'kilder': [CELEX_HELP], 'sikkerhed': 'verificeret',
                                                     'kilde_note': 'CELEX afledt af den citerede retsakts år og nummer efter EUR-Lex\' CELEX-syntaks (sektor 3).'},
                                 'registry_id': eid if eid in reg_ids else None, 'n_dok': e['n_dok'], 'n_gaeldende': e['n_gaeldende'],
                                 'n_implementerer': e['implementeres_af']}, ensure_ascii=False) + '\n')
    st['edges'] = len(E); st['eu'] = len(eu)
    st.update(Counter('kant_' + e['type'] + '_' + e['sikkerhed'] for e in E))
    print(dict(st))

if __name__ == '__main__':
    main()
