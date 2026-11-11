#!/usr/bin/env python3
"""Layer after consolidate_huller: link registry <-> catalog, flag/repair stale act versions, add the bulk-source node and catalog gaps.
Runs after provenance.py (its sources are the dataset's own URLs, not search results)."""
import json, re, sys
from collections import Counter
from pathlib import Path
SP = Path(__file__).resolve().parent
sys.path.insert(0, str(SP / 'corpus'))
REPO = 'https://github.com/Ansvar-Systems/danish-law-mcp'
m = json.load(open(SP / 'data' / 'final.json'))
R = json.load(open(SP / 'corpus' / 'data' / 'resolved.json'))
docs = {d['id']: d for d in R['docs']}; link = R['link']
nodes = {n['id']: n for n in m['nodes']}
LAWT = {'lov', 'lovbekendtgørelse'}

def ntitle(t):
    t = t.lower(); t = re.sub(r'\(\*\s*\d*\)', ' ', t); return re.sub(r'[^a-zæøåé0-9 ]', ' ', re.sub(r'\s+', ' ', t)).split()

# successor for regulations: same normalised title, issued later, gældende
by_title = {}
for d in R['docs']:
    if d['type'] in ('bekendtgørelse',):
        by_title.setdefault(' '.join(ntitle(d['titel'])), []).append(d)

def successor(d):
    if d['type'] in LAWT:
        f = d.get('_family')
        return docs[f] if f and f != d['id'] and docs[f]['status_2026_06'] == 'gældende' else None
    c = [x for x in by_title.get(' '.join(ntitle(d['titel'])), []) if x['status_2026_06'] == 'gældende' and (x['udstedt'] or '') > (d['udstedt'] or '')]
    return max(c, key=lambda x: x['udstedt']) if c else None

stat = Counter(); stale = []; newer_in_registry = []
for rid, did in link.items():
    n = nodes[rid]; d = docs[did]
    n['katalog_id'] = did; stat['linked'] += 1
    if d['status_2026_06'] != 'historisk': continue
    s = successor(d)
    ids = n.setdefault('identifikatorer', {'kilder': [], 'sikkerhed': 'ukendt'})
    note = (f"Retsinformation-høsten (danish-law-mcp, {d['retrieved_at'][:10]}) markerer {d['lovtidende']} som historisk"
            + (f" (markeret {d['historisk_markeret']})" if d.get('historisk_markeret') else '') + '. ')
    if s:
        note += f"Gældende version i høsten: {s['lovtidende']} ({s['id']})."
        ids['gaeldende_i_katalog'] = s['id']; n['katalog_id'] = s['id']
        for u in (d['url_xml'], s['url_xml']):
            if u and u not in ids['kilder']: ids['kilder'].append(u)
        stat['stale_with_successor'] += 1
    else:
        note += 'Afløseren findes ikke i høsten (formentlig udstedt efter datasættets sidste udstedelsesdato 2026-02-12) – ikke fundet.'
        if d['url_xml'] and d['url_xml'] not in ids['kilder']: ids['kilder'].append(d['url_xml'])
        stat['stale_no_successor'] += 1
    ids['katalog_note'] = note
    stale.append(rid)

# unlinked registry acts that are newer than the corpus: link to the family's latest version as predecessor
keyidx = {}
for d in R['docs']:
    if d['type'] in LAWT:
        for k in d.get('_keys', []): keyidx.setdefault(k, []).append(d)
from resolve_keys import keys_for_name  # noqa: E402
for n in m['nodes']:
    if n['type'] not in ('lov', 'bekendtgørelse') or n['id'] in link: continue
    cands = set()
    for k in keys_for_name(n['navn']):
        for d in keyidx.get(k, []):
            cands.add(d.get('_family') or d['id'])
    if len(cands) == 1:
        c = docs[cands.pop()]
        n['katalog_id'] = c['id']
        ids = n.setdefault('identifikatorer', {'kilder': [], 'sikkerhed': 'ukendt'})
        ids['katalog_note'] = (f"Seneste version i Retsinformation-høsten (dækker udstedelser til 2026-02-12): {c['lovtidende']} ({c['id']}, "
                               f"status {c['status_2026_06']} pr. {c['retrieved_at'][:10]}); registry'ets nyere identifikator er ikke i høsten.")
        stat['linked_by_name'] += 1; newer_in_registry.append(n['id'])

# bulk-source node
dl = {
    'id': 'kilde-danish-law-mcp', 'navn': 'danish-law-mcp (Ansvar Systems): bulk-høst af Retsinformation, Lovtidende A', 'type': 'dokumentkilde',
    'ministerium': 'ingen', 'status': 'aktiv', 'domaener': ['byggeri', 'bolig', 'plan', 'energi', 'miljoe', 'arbejdsmiljoe', 'brand', 'el-gas-vvs', 'datakilder-standarder'],
    'tidligere_navne': [],
    'hjemmel': {'tekst': 'ikke relevant (privat open source-projekt, der høster Retsinformations ELI-XML)', 'kilder': [REPO], 'sikkerhed': 'verificeret'},
    'dokumenttyper': {'liste': [{'type': 'lov', 'bindende': 'bindende'}, {'type': 'lovbekendtgørelse', 'bindende': 'bindende'},
                                {'type': 'bekendtgørelse', 'bindende': 'bindende'}, {'type': 'anordning', 'bindende': 'bindende'},
                                {'type': 'ændringslov/ændringsbekendtgørelse', 'bindende': 'bindende'}],
                      'note': 'Kun Lovtidende A. Ingen cirkulærer, vejledninger, skrivelser, Lovtidende B/C eller afgørelser (kontrolleret i alle 62.762 seed-filer).',
                      'kilder': [REPO], 'sikkerhed': 'verificeret'},
    'url': {'vaerdi': REPO, 'kilder': [REPO], 'sikkerhed': 'verificeret'},
    'adgang': {'vaerdier': ['bulk'], 'note': 'Git-repo med én JSON-fil pr. dokument (data/seed/, 62.762 filer: titel, short_name/dokumenttype, status Valid/Historic, datoer, '
               'DocumentId, AccessionNumber, ELI-XML-URL, paragraffer, definitioner) og data/census.json. Paragraftekst uden præambel ("I medfør af …"), '
               'underskrift og EU-noter. Hentet her: commit da22657 (2026-07-22). Ca. 1,7 GB.', 'kilder': [REPO], 'sikkerhed': 'verificeret'},
    'identifikatorer': {'andet': 'Dokument-id = Lovtidende A år:nummer (fx 2019:1399); DocumentId-præfiks angiver udstedende ministeriums dokumentkonto.',
                        'kilder': [REPO], 'sikkerhed': 'verificeret'},
    'licens': {'tekst': 'Kode: Apache-2.0. Data: "DK-Statutory-PD" – ikke ophavsretligt beskyttet efter ophavsretslovens § 9 (sources.yml).',
               'kilder': [REPO], 'sikkerhed': 'verificeret'},
    'opdatering': {'frekvens': 'Status høstet 2026-06-10–12; nyeste udstedelse i datasættet 2026-02-12. sources.yml angiver daglig kontrol, men nye dokumenter efter 12/2/2026 mangler.',
                   'versionshistorik': 'Git-historik; provision_versions i seed-filerne', 'kilder': [REPO], 'sikkerhed': 'verificeret'},
    'krydsref_moenstre': ['ELI-XML-URL https://www.retsinformation.dk/eli/lta/ÅÅÅÅ/NNN/xml pr. dokument', '"lov nr. N af D. måned ÅÅÅÅ" i paragraftekst',
                          '"direktiv ÅÅÅÅ/NN/EU" og "forordning (EU) nr. N/ÅÅÅÅ" i paragraftekst'],
    'ingest': {'vaerdi': 5, 'besvaer': 1, 'begrundelse': 'Hele Lovtidende A som struktureret JSON i ét git-repo; ingen rate limits. Grundlaget for katalog-laget (katalog/).'},
    'note': 'Katalog-laget dk-regulering/katalog/ er bygget herfra uden netværkskald til Retsinformation.',
}
if 'kilde-danish-law-mcp' not in nodes:
    m['nodes'].append(dl)
    m['edges'].append({'from': 'kilde-danish-law-mcp', 'type': 'henviser_til', 'to': 'kilde-retsinformation',
                       'beskrivelse': 'Høster Lovtidende A fra Retsinformation (ELI-XML); hver seed-fil angiver Retsinformation-URL og DocumentId',
                       'kilder': [REPO], 'sikkerhed': 'verificeret'})

HE = R.get('hjemmel_eval', {})
_qf = SP / 'data' / 'ressort_quality.json'
RQ = json.load(open(_qf)) if _qf.exists() else {}
_g = [d for d in R['docs'] if d['status_2026_06'] == 'gældende']
NO_TEXT_ALL = sum(1 for d in R['docs'] if not d['n_prov']); NO_TEXT_G = sum(1 for d in _g if not d['n_prov']); NO_TEXT_PCT = round(100 * NO_TEXT_G / len(_g))
_bek = [d for d in _g if d['type'] == 'bekendtgørelse']
BEK_LINK_PCT = round(100 * sum(1 for d in _bek if d['_laws']) / len(_bek))
H = [
    {'emne': 'Retsinformation ud over Lovtidende A er ikke i katalog-laget', 'type': 'ingen-api',
     'beskrivelse': 'Bulk-kilden (danish-law-mcp) rummer kun Lovtidende A: love, lovbekendtgørelser, bekendtgørelser, anordninger. Cirkulærer, vejledninger, skrivelser, '
                    'Lovtidende B og C, Folketingets Ombudsmands udtalelser og andre afgørelser på Retsinformation mangler. Retsinformations høsteservice (REST, højst ét kald pr. 10 s) '
                    'kan levere dem, men api.retsinformation.dk var blokeret af sessionens netværkspolitik.',
     'noder': ['kilde-retsinformation', 'kilde-danish-law-mcp'], 'kilder': [REPO], 'domaener': ['datakilder-standarder']},
    {'emne': 'Dokumenter udstedt efter 2026-02-12 mangler i katalog-laget', 'type': 'ikke-fundet',
     'beskrivelse': 'Datasættets nyeste udstedelse er 2026-02-12, selv om status blev høstet 2026-06-10–12. Nye love og bekendtgørelser fra 13/2/2026 og frem (fx arbejdsmiljøreformens '
                    'bekendtgørelser af 29/6/2026, BEK 514/2026 og nye lovbekendtgørelser) står kun i registry\'et, hvor de er fundet ved søgning. '
                    f'{len(newer_in_registry)} registry-noder er koblet til forgængeren i høsten.',
     'noder': sorted(newer_in_registry) + ['kilde-danish-law-mcp'], 'kilder': [REPO], 'domaener': ['datakilder-standarder']},
    {'emne': 'Hjemmel (præambel) og EU-noter mangler i bulk-teksten – hjemmel_for kan ikke udledes for katalog-dokumenter', 'type': 'uklart',
     'beskrivelse': 'Seed-filerne har kun paragraftekst, ikke præamblen ("I medfør af § … i lov om …"), underskrift eller EU-noten ("Bekendtgørelsen indeholder bestemmelser, der gennemfører …"). '
                    'Katalog-kanterne er derfor henviser_til (loven eller retsakten nævnes i teksten) og implementerer_EU, når et direktiv nævnes i samme bestemmelse som "gennemfører"/"til gennemførelse af". '
                    f'Kun {BEK_LINK_PCT} % af de gældende bekendtgørelser nævner overhovedet en lov, der kan genfindes. '
                    f'Afprøvning mod registry\'ets {sum(HE.values())} kendte hjemmel_for-kanter: den mest nævnte lov var hjemmelsloven i {HE.get("top", 0)}, nævnt men ikke flest gange i {HE.get("blandt", 0)}, '
                    f'forkert i {HE.get("forkert", 0)}, og intet kandidatlov i {HE.get("ingen_kandidat", 0)}. Den mest nævnte lov er derfor IKKE brugt som hjemmel. Præamblen kan hentes fra Retsinformations ELI-XML.',
     'noder': ['kilde-danish-law-mcp'], 'kilder': [REPO], 'domaener': ['datakilder-standarder']},
    {'emne': f'{NO_TEXT_G} gældende katalog-dokumenter ({NO_TEXT_PCT} %) har ingen tekst i bulk-høsten', 'type': 'ikke-fundet',
     'beskrivelse': f'{NO_TEXT_ALL} af {len(R["docs"])} dokumenter i danish-law-mcp har ingen paragraffer, heraf {NO_TEXT_G} gældende. For dem findes kun metadata (titel, nummer, status, datoer, '
                    'DocumentId), så der kan hverken udtrækkes lovhenvisninger, EU-referencer eller ministertitler. Udsteder kendes stadig fra DocumentId-præfikset. Teksten kan hentes fra Retsinformations ELI-XML.',
     'noder': ['kilde-danish-law-mcp'], 'kilder': [REPO], 'domaener': ['datakilder-standarder']},
    {'emne': f'Nuværende ressort for de {len(_g)} gældende katalog-dokumenter er klassificeret, ikke slået op', 'type': 'uklart',
     'beskrivelse': 'Retsinformation angiver ressortministerium, men feltet er ikke i bulk-kilden. Udstedende ministerium er udledt af DocumentId-præfikset (sandsynlig). '
                    'Nuværende ressort pr. 2026-10-28 er klassificeret af Haiku-agenter ud fra titel, udsteder og en ressortguide for kgl. res. 3/6/2026 (BEK 514/2026), '
                    'hvis fulde tekst ikke kunne læses; de usikre er klassificeret igen af Opus, og registry-noder med ressortansvar-kant går forud. '
                    f'Målt kvalitet: {RQ.get("registry_match_pct", "?")} % af de "sandsynlige" stemmer med registry\'et ({RQ.get("registry_n", "?")} noder); '
                    f'en uafhængig Opus-kontrol af {RQ.get("sample_n", "?")} tilfældige "sandsynlige" fandt ministeriet korrekt i {RQ.get("sample_ok_pct", "?")} %. '
                    'Kendte usikre zoner: klagenævn betjent af Nævnenes Hus (Erhvervsministeriet eller fagministeriet), fødevarer (delt mellem Erhvervsministeriet og Ministeriet for Natur og Dyrevelfærd), '
                    'finansiel regulering (flyttet til Skatte- og Vækstministeriet), byggevarer og dagtilbud.',
     'noder': ['bek-ressortoverfoersel-bolig-2026'] if 'bek-ressortoverfoersel-bolig-2026' in nodes else [], 'kilder': ['https://www.retsinformation.dk/api/pdf/256544', 'https://stm.dk/media/nishv4wc/kgl-resolution-af-3-juni-2026.pdf'],
     'domaener': ['datakilder-standarder']},
    {'emne': 'Registry-noder hvis retsakt er markeret historisk i Retsinformation-høsten', 'type': 'uklart',
     'beskrivelse': 'Krydstjek af registry\'ets ELI/Lovtidende-numre mod høstens status. For noder med en gældende afløser i høsten er den tilføjet (identifikatorer.gaeldende_i_katalog). '
                    'For resten er afløseren udstedt efter datasættets dækning; noden bør efterprøves. Se identifikatorer.katalog_note på hver node.',
     'noder': sorted(stale), 'kilder': [REPO], 'domaener': ['datakilder-standarder']},
]

# --- two indexes the user pointed to (assessed via WebSearch only; both domains blocked in the session)
DL = ['https://danskelove.dk/vilkår', 'https://danskelove.dk/register/a', 'https://danskelove.dk/register/s', 'https://danskelove.dk/hvidvaskloven', 'https://danskelove.dk/hvidvaskloven/46d']
JB = ['https://djoefforlag.dk/products/jurabibliotek', 'https://djoefforlag.dk/products/lovgivning', 'https://jurabibliotek.dk/betingelser', 'https://jurabibliotek.ai/danske-lov',
      'https://jurabibliotek.ai/strafberegningsbekendtgoerelsen', 'https://jurabibliotek.ai/cirkulaere-om-vaaben-og-ammunition-mv/paragraf/8', 'https://jurabibliotek.dk/forarbejder/aendringslov-2025-06-20-722',
      'https://jurabibliotek.dk/forarbejder/lovforslag-som-fremsat-1991-01-30-19902-lsf-103', 'https://jurabibliotek.ai/hvidvaskloven/paragraf/6a']
ALL8 = ['byggeri', 'bolig', 'plan', 'energi', 'miljoe', 'arbejdsmiljoe', 'brand', 'el-gas-vvs', 'datakilder-standarder']
NEW = [
 {'id': 'kilde-danskelove', 'navn': 'Danske Love (danskelove.dk)', 'type': 'dokumentkilde', 'ministerium': 'ingen', 'status': 'aktiv', 'domaener': ALL8, 'tidligere_navne': [],
  'hjemmel': {'tekst': 'ikke relevant (privat, gratis opslagsværk; ifølge vilkårssiden ejet og drevet af en privatperson, CVR 21095575, i samarbejde med Legal Desk ApS om rådgivning)', 'kilder': DL[:1], 'sikkerhed': 'verificeret'},
  'dokumenttyper': {'liste': [{'type': 'lov', 'bindende': 'bindende'}], 'note': 'Kun love (også enkelte ophævede, fx persondataloven). Ingen bekendtgørelser, cirkulærer, vejledninger, afgørelser eller forarbejder set i søgeresultaterne. Uofficiel gengivelse uden synligt LBK-nummer eller versionsdato.', 'kilder': DL[1:], 'sikkerhed': 'sandsynlig'},
  'url': {'vaerdi': 'ikke fundet', 'kilder': [], 'sikkerhed': 'ukendt', 'kilde_note': 'Forsiden optrådte ikke selv i søgeresultaterne; undersider gjorde. Domænet er blokeret i sessionen.'},
  'adgang': {'vaerdier': ['HTML'], 'note': 'Lovside /<kortnavn>, paragrafside /<kortnavn>/<nr> (bogstavparagraffer uden mellemrum, fx /hvidvaskloven/46d) og alfabetisk register /register/<bogstav>, der lister alle kortnavne. Ingen API, sitemap eller bulk set. danskelove.dk var blokeret af sessionens netværkspolitik.', 'kilder': DL[1:], 'sikkerhed': 'verificeret'},
  'identifikatorer': {'andet': 'Kortnavn som slug (små bogstaver, URL-kodet æ/ø/å) og "<Kortnavn> § N" som sidetitel. Ingen Lovtidende-numre, ELI eller ministerium set.', 'kilder': DL[3:], 'sikkerhed': 'sandsynlig'},
  'licens': {'tekst': 'Vilkårene: "Danske Love er et gratis opslagsværk, som kan benyttes af alle uden begrænsninger. Indhold på hjemmesiden herunder tekniske indretninger, vil i nogle tilfælde være ophavsretligt beskyttet materiale og må kun benyttes i overensstemmelse med de rettigheder som lovgivningen tillader. Enhver anden benyttelse kræver forudgående tilladelse fra Danske Love." '
                       'Lovteksterne selv er ikke genstand for ophavsret (ophavsretslovens § 9, stk. 1) og må bruges frit. Sitets egen sammenstilling (register, opdeling i paragrafsider) kan være beskyttet som database efter § 71: kopiering af hele eller en væsentlig del, eller gentagne systematiske udtræk, kræver tilladelse. '
                       'Tekst- og datamining er tilladt efter § 11 b, stk. 2 (gælder også databaser, § 71, stk. 5), medmindre rettighedshaveren udtrykkeligt har forbeholdt sig det; det er uafklaret, om vilkårenes "enhver anden benyttelse" er et sådant forbehold, og robots.txt kunne ikke ses. '
                       'Praksis: opslag og kortnavne-registeret frit; lovteksten hentes fra Retsinformation; en fuld crawl af sitet aftales med Danske Love.',
             'kilder': DL[:1] + ['https://www.retsinformation.dk/eli/lta/2023/1093/xml'], 'sikkerhed': 'verificeret',
             'kilde_note': 'Vilkårsordlyden er givet af brugeren 2026-11-02 og stemmer med vilkårssiden i søgeresultaterne; §§ 9, 11 b og 71 er læst i ophavsretsloven (LBK nr. 1093 af 20/08/2023, gældende pr. 2026-06-12) i katalog-laget.'},
  'opdatering': {'frekvens': 'ukendt (ingen versionsdatoer eller LBK-numre vises)', 'versionshistorik': 'ingen set', 'kilder': [], 'sikkerhed': 'ukendt'},
  'krydsref_moenstre': ['danskelove.dk/<kortnavn>/<paragraf>', 'danskelove.dk/register/<bogstav>'],
  'ingest': {'vaerdi': 2, 'besvaer': 3, 'begrundelse': 'Gratis og frit til opslag. Nyttig som ordbog kortnavn ↔ lov (registeret) og som model for §-ankre. Teksten er uofficiel og uden version og dækker kun love; Retsinformation er den primære kilde til selve teksten. Kun HTML, og domænet skal tillades i miljøet.'},
  'note': 'Peget på af brugeren 2026-11-02 som indeks. Vurderet ud fra søgeresultater, da domænet var blokeret.'},
 {'id': 'kilde-jurabibliotek', 'navn': 'Jurabibliotek (Djøf Forlag; jurabibliotek.dk / jurabibliotek.ai)', 'type': 'dokumentkilde', 'ministerium': 'ingen', 'status': 'aktiv', 'domaener': ALL8, 'tidligere_navne': [],
  'hjemmel': {'tekst': 'ikke relevant (kommercielt juridisk onlinebibliotek fra Djøf Forlag)', 'kilder': JB[:2], 'sikkerhed': 'verificeret'},
  'dokumenttyper': {'liste': [{'type': 'lov/lovbekendtgørelse (konsolideret)', 'bindende': 'bindende'}, {'type': 'bekendtgørelse', 'bindende': 'bindende'}, {'type': 'cirkulære (enkelte)', 'bindende': 'blandet'},
                              {'type': 'forarbejder (lovforslag som fremsat, betænkninger, lovforslag som vedtaget, ændringslove)', 'bindende': 'vejledende'}, {'type': 'juridisk litteratur og tidsskrifter', 'bindende': 'vejledende'}],
                    'note': 'Djøf angiver over 2.000 konsoliderede love og bekendtgørelser (mod 13.819 gældende Lovtidende A-dokumenter i katalog-laget) og forarbejder på paragrafniveau. Ingen myndighedsvejledninger eller afgørelsesdatabase set. Siden /danske-lov er Christian V\'s Danske Lov (lov nr. 11000 af 15/4 1683), ikke et indeks over danske love.',
                    'kilder': JB[1:2] + JB[3:], 'sikkerhed': 'verificeret'},
  'url': {'vaerdi': 'https://jurabibliotek.dk', 'kilder': ['https://jurabibliotek.dk'], 'sikkerhed': 'verificeret'},
  'adgang': {'vaerdier': ['betalingsmur', 'HTML'], 'note': 'Fuld tekst kræver abonnement (Djøf: Jurabibliotek Lovgivning ca. 8.190 kr./år, samlet ca. 12.475 kr./år, 14 dages prøve); uden login vises titel, header med LBK-nr. og ændringslove samt disposition. Sider pr. lov/BEK/CIR (/<slug>), kapitel (/<slug>/kapitel/<n>) og paragraf (/<slug>/paragraf/<n>); forarbejder under /forarbejder/ med samling og LSF/LSV-nr. i stien. Djøf omtaler en API ("Jura til maskiner") og MCP-integration, som kræver aftale. jurabibliotek.dk var blokeret af sessionens netværkspolitik.',
             'kilder': JB[:2] + JB[4:], 'sikkerhed': 'sandsynlig'},
  'identifikatorer': {'andet': 'Slug med populærnavn eller titel (æ→ae, ø→oe, å→aa); Lovtidende-nr. og dato i headeren; lovforslag som <samling> LSF/LSV <nr> af <dato>.', 'kilder': JB[4:], 'sikkerhed': 'verificeret'},
  'licens': {'tekst': 'Lukket og kommerciel. De generelle betingelser forbyder brug af indhold til tekst- og datamining, træning af sprogmodeller, embeddings og anden AI-brug samt maskinel tilgang uden aftale.', 'kilder': JB[2:3], 'sikkerhed': 'verificeret'},
  'opdatering': {'frekvens': 'Dagligt ifølge Djøf; dokumenter fra september 2026 set (fx lovforslag som vedtaget 4/9 2026)', 'versionshistorik': '"som ændret ved"-liste og noter om ikke-ikraftsatte ændringer pr. paragraf', 'kilder': JB[1:2] + JB[6:8], 'sikkerhed': 'sandsynlig'},
  'krydsref_moenstre': ['jurabibliotek.dk/<slug>/paragraf/<nr>', 'jurabibliotek.dk/forarbejder/lovforslag-som-fremsat-<dato>-<samling>-lsf-<nr>'],
  'ingest': {'vaerdi': 3, 'besvaer': 5, 'begrundelse': 'Aktuel og med kobling lov ↔ forarbejder, men bag betalingsmur, og vilkårene forbyder maskinel brug og AI. Kan kun bruges til manuel kontrol eller via en licensaftale (Djøf-API). Åben vej til forarbejder: Folketingets Åbne Data.'},
  'note': 'Brugeren pegede på jurabibliotek.dk/danske-lov som indeks 2026-11-02; siden er Christian V\'s Danske Lov fra 1683. Vurderet ud fra søgeresultater, da domænet var blokeret.'},
]
for nd in NEW:
    if nd['id'] not in nodes: m['nodes'].append(nd); nodes[nd['id']] = nd
H += [
    {'emne': 'Love fra før 1852 (fx Christian V\'s Danske Lov 1683) er ikke i bulk-høsten', 'type': 'ikke-fundet',
     'beskrivelse': 'danish-law-mcp starter i 1852, men Retsinformation har ældre gældende retsakter, fx Danske Lov (lov nr. 11000 af 15/4 1683, ændret senest ved lov nr. 522 af 6/6 2007 ifølge Jurabiblioteks lovside). De mangler i katalog-laget og kan hentes fra Retsinformation.',
     'noder': ['kilde-danish-law-mcp', 'kilde-jurabibliotek'], 'kilder': ['https://jurabibliotek.ai/danske-lov'], 'domaener': ['datakilder-standarder']},
    {'emne': 'Kobling lov ↔ forarbejder findes kun bag betalingsmur (Jurabibliotek); den åbne vej er Folketingets data', 'type': 'betalingsmur',
     'beskrivelse': 'Jurabibliotek kobler love til lovforslag som fremsat, betænkninger og lovforslag som vedtaget, men bag abonnement og med forbud mod maskinel brug og AI. danskelove.dk har ingen forarbejder. Koblingen bør bygges fra Folketingstidende/Folketingets Åbne Data og Retsinformations henvisninger.',
     'noder': ['kilde-jurabibliotek', 'kilde-danskelove'], 'kilder': JB[:2] + JB[6:8], 'domaener': ['datakilder-standarder']},
]
have = {h['emne'] for h in m['huller']}
m['huller'] += [h for h in H if h['emne'] not in have]
json.dump(m, open(SP / 'data' / 'final.json', 'w'), ensure_ascii=False, indent=1)
print(dict(stat), 'stale', stale, 'newer', newer_in_registry)
