#!/usr/bin/env python3
"""Write dk-regulering/README.md from data/final.json (numbers + ressort table)."""
import json
from collections import Counter
from pathlib import Path

SP = Path(__file__).resolve().parent
m = json.load(open(SP / "data" / "final.json"))
prov = json.load(open(SP / "data" / "provenance_stats.json"))
N = {n["id"]: n for n in m["nodes"]}
bl = m["baseline"]
CF = ("hjemmel", "dokumenttyper", "url", "adgang", "identifikatorer", "licens", "opdatering")
cert = Counter(n[f]["sikkerhed"] for n in m["nodes"] for f in CF) + Counter(e["sikkerhed"] for e in m["edges"])
tot = sum(cert.values())
pct = {k: round(100 * v / tot) for k, v in cert.items()}
types = Counter(n["type"] for n in m["nodes"])
etypes = Counter(e["type"] for e in m["edges"])
gaps = Counter(h["type"] for h in m["huller"])
KD = SP / "dk-regulering" / "katalog"
kdocs = [json.loads(l) for l in open(KD / "retsinformation_lta.jsonl", encoding="utf-8")]
ktyper, kkoblet, kbest = Counter(), set(), Counter()
for l in open(KD / "kanter.jsonl", encoding="utf-8"):
    e = json.loads(l)
    ktyper[e["type"]] += 1
    if "from_bestemmelse" in e:
        kbest[e.get("metode")] += 1
    if e.get("metode") == "retsinformation-eksport" and e["type"] in ("hjemmel_for", "henviser_til"):
        kkoblet.add(e["from"] if e["type"] == "henviser_til" else e["to"])
kandre = [(d["id"], d["status"]["vaerdi"] == "gældende", (d.get("ministerium") or {}).get("metode"), len(d.get("registry_ids") or []), d.get("lovforslag"), d.get("lov"))
          for s in ("ltb", "ltc", "mt", "retsinfo", "fob", "ft") for d in map(json.loads, (KD / f"retsinformation_{s}.jsonl").open(encoding="utf-8"))]
kag = [x for x in kandre if x[1]]
ksager = {x[4] for x in kandre if x[5]}
kakob = sum(x[0] in kkoblet for x in kag)
klove = len({x[5] for x in kandre if x[5]})
kftdok = sum(x[4] in ksager for x in kandre)
kamet = Counter(x[2] for x in kag)
kedges = sum(ktyper.values())
keu = sum(1 for _ in open(KD / "eu_index.jsonl", encoding="utf-8"))
kg = [d for d in kdocs if d["status"]["vaerdi"] == "gældende"]
ksenest = max(d["status"]["pr"] for d in kdocs)
ktekst = list(map(json.loads, (KD / "tekst.jsonl").open(encoding="utf-8")))
kxml = {t["id"] for t in ktekst if t["n_tegn"]}
kuden = sum(not d.get("n_paragraffer") and d["id"] not in kxml for d in kg)
kres = Counter((d.get("ministerium") or {}).get("sikkerhed", "ingen") for d in kg)
kreg = sum(len(d.get("registry_ids") or []) for d in kdocs) + sum(x[3] for x in kandre)
RES = json.load(open(SP / "corpus" / "data" / "resolved.json"))
HE = RES.get("hjemmel_eval", {}); RSTAT = RES.get("stats", {})
qf = SP / "data" / "ressort_quality.json"
RQ = json.load(open(qf)) if qf.exists() else {}
kmet = Counter((d.get("ministerium") or {}).get("metode") for d in kg)
mins = sorted((n for n in m["nodes"] if n["type"] == "ministerium" and n["status"] == "aktiv"), key=lambda n: n["navn"])
OMR = {o["omraade"]: o["navn"] for o in json.load(open(SP / "dash" / "omraader.json"))}
BASIS = {"byggeri", "bolig", "plan", "kommunalt", "energi", "miljoe", "natur-vand-kyst", "arbejdsmiljoe", "brand", "el-gas-vvs", "klage-tilsyn-praksis", "eu", "datakilder-standarder", "baseline"}
fase7 = sorted({d for n in m["nodes"] for d in n.get("domaener", [])} & set(OMR) - BASIS)
n7 = sum(1 for n in m["nodes"] if set(n.get("domaener", [])) & set(fase7))
ajour = [n["identifikatorer"] for n in m["nodes"] if n["identifikatorer"].get("aendringer_kontrolleret")]
aend = [len(i["senere_aendringer"]) for i in ajour if i.get("senere_aendringer")]
ajour_dato = max((i["aendringer_kontrolleret"] for i in ajour), default="ukendt")


def nf(x):
    return f"{x:,}".replace(",", ".")


def name(i):
    return N[i]["navn"] if i in N else i


def cell(s):
    return str(s).replace("|", "\\|").replace("\n", " ")


rows = []
for o in bl["omraader"]:
    inst = ", ".join(name(i) for i in o["instans_ids"]) or "–"
    rows.append(f"| {cell(o['omraade'])} | {cell(name(o['ministerium_id']))} | {cell(inst)} | `{o['sikkerhed']}` |")

doc = f"""# Dansk regulering: kortlægning til RAG

**Kortlagt i dybden (registry):** byggeri · bolig · plan · energi · miljø · arbejdsmiljø · brand · el/gas/VVS. **Instanslag tilføjet i fase 7:** {' · '.join(OMR[d].lower() for d in fase7)} ({n7} noder; senest opdateret {m.get('opdateret', 'ukendt')[:10]}). **Bredt (katalog):** hele Lovtidende A – {len(kdocs)} love, lovbekendtgørelser, bekendtgørelser og anordninger, heraf {len(kg)} gældende, og Retsinformations øvrige samlinger – {len(kandre)} cirkulærer, vejledninger, afgørelser, lovforslag m.m., heraf {len(kag)} ikke markeret historiske. **Status pr. 2026-10-28** (katalogets dokumentstatus pr. {ksenest}).

Kortlægningen dækker myndigheder, retsakter, klage- og tilsynsveje, EU-retsakter og dokumentkilder. Den skal bruges til at bygge et krydsrefereret korpus (udvidelse af `jakob1379/br18`), hvor søgning kan følge hjemmelskæder fra lov til bekendtgørelse til vejledning til praksis. Der er **ikke** hentet dokumenter til korpusset; katalog-laget er metadata og krydsreferencer udledt af en offentlig bulk-høst.

To lag:

- **Registry** (`registry.yaml`): håndkurateret og verificeret graf over myndigheder, centrale retsakter, klage-/tilsynsveje, EU-retsakter og datakilder for de otte domæner.
- **Katalog** (`katalog/`): én post pr. dokument hos Retsinformation. Lovtidende A ({len(kdocs)}) er bygget fra bulk-høsten `Ansvar-Systems/danish-law-mcp` og ført ajour fra Retsinformations søgeeksport {ksenest}; hver post har Lovtidende-nr., DocumentId, status, datoer, udstedende ministerium og, for gældende dokumenter, nuværende ressortministerium og retsområde. De øvrige samlinger ({len(kandre)} dokumenter: administrative forskrifter og afgørelser, Ministerialtidende, Lovtidende B og C, Folketingets Ombudsmand og Folketingstidende) kommer direkte fra søgeeksporten og har kun metadata; {kakob} af de {len(kag)} ikke-historiske er koblet til den lovgivning, de vedrører, herunder {kftdok} dokumenter om lovforslag til de {klove} love, de blev til. {kedges} kanter (`henviser_til`, `hjemmel_for`, `implementerer_EU`, `ressortansvar` og `udsteder`: {ktyper['udsteder']} afgørelser og udtalelser er koblet til den myndighed, Retsinformation fører dem under, når den er en instans i registry'et) og {keu} refererede EU-retsakter med CELEX. {kreg} registry-noder er koblet til deres katalogpost (`katalog_id` ↔ `registry_ids`). **Tekst:** Retsinformations XML er hentet for {len(ktekst)} dokumenter (de dokumenter, registry'et peger på, gældende dokumenter i de otte domæner og afløserkandidaternes lovtekster, de fleste ophævede; `katalog/tekst.jsonl` og `intermediate/corpus/xml/`); {len(ktekst) - len(kxml)} af dem har ingen tekst i XML-filen, kun metadata. {sum(kbest.values())} `hjemmel_for`-kanter har derfra de bestemmelser i loven, forskriftens præambel nævner (`from_bestemmelse`).

| Fil | Indhold |
|-----|---------|
| [`registry.yaml`](registry.yaml) | **Sandheden.** Indeholder meta, regering, ressortomlægninger, uafklarede konflikter, {len(m['nodes'])} noder, {len(m['edges'])} kanter og {len(m['huller'])} huller. |
| [`diagrammer/oversigt.md`](diagrammer/oversigt.md) | Mermaid-overblik over ministerier og instanser, med ét diagram pr. ministerområde ({len(mins)} aktive ministerier plus nedlagte/omdøbte). |
| [`datakilder.md`](datakilder.md) | Datakilder sorteret efter ingest-prioritet (værdi ÷ besvær) i tre tabeller: portaler/databaser, udstedende instanser og retsakter/samlinger. |
| [`huller.md`](huller.md) | Betalingsmur, kun PDF, intet API, uklare forhold og ikke-fundne kilder. |
| [`katalog/retsinformation_lta.jsonl`](katalog/retsinformation_lta.jsonl) | Katalog-laget: én JSON-linje pr. Lovtidende A-dokument ({len(kdocs)}). |
| [`katalog/retsinformation_retsinfo.jsonl`](katalog/retsinformation_retsinfo.jsonl) m.fl. | De øvrige samlinger, én fil pr. samling (`retsinfo`, `mt`, `ltb`, `ltc`, `fob`, `ft`): {len(kandre)} cirkulærer, vejledninger, afgørelser, traktatbekendtgørelser, ombudsmandsudtalelser, lovforslag og betænkninger. |
| [`katalog/kanter.jsonl`](katalog/kanter.jsonl) | {kedges} kanter fra katalog-dokumenter (kun de tilladte kanttyper). |
| [`katalog/tekst.jsonl`](katalog/tekst.jsonl) | Tekstlagets indeks: én linje pr. dokument, hvis XML er hentet fra Retsinformation ({len(ktekst)}), med sti til XML-filen, hentedato, omfang, præambel, fodnoter, underskriftssted og EU-retsakter. |
| [`katalog/eu_index.jsonl`](katalog/eu_index.jsonl) | {keu} EU-retsakter nævnt i dansk lovtekst, med CELEX og antal danske dokumenter. |
| [`katalog/README.md`](katalog/README.md) | Genereret oversigt over katalog-laget (typer, ressort, retsområder, kanter, top EU-retsakter). |
| [`scripts/build.py`](scripts/build.py) | Validerer `registry.yaml` og katalog-laget og genererer views ovenfor. Kør `python3 scripts/build.py`, og brug `--check` i CI. |

## Scope

Scope-felterne i opgaven var ikke udfyldt. Første mulighed i hver parentes er valgt:

- **Domæner:** byggeri, bolig, plan, energi, miljø, arbejdsmiljø, brand og el/gas/VVS, ikke hele staten. Natur, vand og kyst er taget med som en del af miljø.
- **Niveauer:** stat, kommunalt og EU. Kommuner og regioner er aggregeret i `kommune-alle` og `region-alle`, og deres plantyper, regulativer og datakilder er egne noder.
- **Praksis:** klagenævn, Ankestyrelsen, Folketingets Ombudsmand og domstole.
- **Standarder og branchevejledninger** (DS/EN, Eurocodes, BUILD/SBi, Molio, DBI, TEKNIQ, BFA m.fl.) er **kun metadata**.
- **Al offentlig lovgivning (udvidelse):** hele Lovtidende A er med i katalog-laget, uanset domæne. De cirkulærer, vejledninger og afgørelser, Retsinformation har, er med som metadata og koblet til lovgivningen; det, myndighederne kun offentliggør på egne sider, er ikke med (se huller).

## Ressortfordeling pr. 2026-10-28 (hovedtræk)

Regeringen Mette Frederiksen III (S, SF, RV, M) blev dannet 3. juni 2026. Forretningsfordelingen følger BEK nr. 514 af 08/06/2026, og den 27/10/2026 blev Karina Lorentzen Dehnhardt by-, land- og transportminister. Ændringer, der er vigtige for korpusset:

- **3/6/2026:**
  - Byggeri og bolig (byggeloven, BR18, almene boliger, leje) flyttes til **Børne-, Ældre- og Boligministeriet**. Social- og Boligstyrelsen administrerer fortsat, men ligger organisatorisk under Socialministeriet (uafklaret opdeling).
  - Plan flyttes til **By-, Land- og Transportministeriet** (Plan- og Landdistriktsstyrelsen). By-, Land- og Kirkeministeriet er nedlagt.
  - Affald flyttes til **Klima-, Energi- og Forsyningsministeriet**.
  - Indenrigsområdet og kommunaltilsynet flyttes til **Økonomi- og Indenrigsministeriet**.
  - Ministeriet for Grøn Trepart omdøbes til **Ministeriet for Natur og Dyrevelfærd**, og Miljø- og Ligestillingsministeriet omdøbes til **Miljøministeriet**.
- **1/1/2026:** Sikkerhedsstyrelsen fusioneres ind i **Erhvervsstyrelsen** (afd. Markedsovervågning), som nu står for el- og gassikkerhed, autorisation og markedsovervågning af byggevarer.
- **29/8/2024:** Beredskab flyttes fra Forsvarsministeriet til **Ministeriet for Samfundssikkerhed og Beredskab**.

| Område | Ministerium | Instans(er) | Sikkerhed |
|--------|-------------|-------------|-----------|
""" + "\n".join(rows) + f"""

Den fulde liste over ressortomlægninger med datoer og kilder står i `registry.yaml` under `ressortomlaegninger`, og afstemningskonflikter står under `uafklarede_konflikter`.

## Metode

1. **Baseline:** To uafhængige agenter kortlagde regering og ressort, og en tredje afstemte dem til kanoniske id'er (200 søgninger).
2. **Domæneresearch:** 13 domæner, hver med én research-agent, to adversarielle verifikatorer (organisation/hjemmel og kilder/identifikatorer) og en konsolidator.
3. **Verifikation med reelt søgebudget:** WebSearch er begrænset til 200 kald pr. tur, delt af alle agenter. Fase 2 var derfor underforsynet: 5 domæner og alle verifikatorer fik 0 søgninger. Det blev rettet med fem runder i hver sin tur:
   - én adversariel verifikator og konsolidator pr. domæne (cirka 35 søgninger hver);
   - udfyldning af kanoniske URL'er, ELI, CELEX og adgang for 387 noder (cirka 20 søgninger pr. batch på 20 noder);
   - en completeness-kritiker pr. ministerområde (cirka 30 søgninger), som tilføjede manglende noder og kanter og bestred forkerte kanter. De 23 bestridte kanter er gennemgået manuelt og fjernet eller mærket `[HISTORISK …]` eller `[BESTRIDT …]` i kantens `beskrivelse`.
4. **Verifikation pr. node:** Alle påstande, der stadig var `sandsynlig` eller `ukendt`, blev efterprøvet node for node i 75 batches. Det gjaldt felter, tidligere navne og kanter, og hver agent havde cirka 25 søgninger. Påstande blev bekræftet, rettet med ny kilde eller markeret som ikke fundet.
   - Generelle forhold blev belagt én gang pr. nodeklasse med officielle kilder: ophavsretslovens § 9 for love, bekendtgørelser og cirkulærer, EU's genbrugsregler (afgørelse 2011/833/EU og EUR-Lex' juridiske meddelelse), og opdatering og adgang på Retsinformation og EUR-Lex. Feltet `regel` viser, hvilken regel der er brugt.
5. **Katalog-lag (fase 6):** Alle 62.762 seed-filer i `Ansvar-Systems/danish-law-mcp` (commit da22657, status høstet 2026-06-10–12) er læst lokalt:
   - Dokumenttype fra `short_name`, Lovtidende-nr. fra år/nummer og udstedelsesdato, status fra Retsinformations `Valid`/`Historic`.
   - **Udstedende ministerium** fra præfikset i Retsinformations DocumentId: hvert ministerium har haft sin egen dokumentkonto (fx `AA` Justitsministeriet, `DG` Transportministeriet 2021–). Præfikserne er navngivet ud fra de ministertitler, teksterne oftest nævner (renhed typisk 0,8–0,99); 20 blandede eller tavse præfikser er navngivet manuelt ud fra eksempeltitler. Sikkerhed: `sandsynlig`.
   - **Nuværende ressort og retsområde** for de 13.819 dokumenter, der var gældende ved høsten: 50 Haiku-agenter (effort high, ingen websøgning) klassificerede alle ud fra titel, udsteder og en ressortguide for kgl. res. 3/6/2026. De {RQ.get('opus_recheck_n', '…')} usikre blev klassificeret igen af Opus (effort high) med en skærpet guide. Hvor et dokument er en registry-node med en ressortansvar-kant, bruges registry'ets ministerium ({kmet.get('registry', 0)} dokumenter). Kvalitet: mod registry'et stemmer {RQ.get('registry_match_pct', '…')} % af de "sandsynlige" klassifikationer ({RQ.get('registry_n', '…')} noder), og en uafhængig Opus-kontrol af {RQ.get('sample_n', '…')} tilfældige "sandsynlige" (højst 20 pr. ministerium) fandt ministeriet korrekt i {RQ.get('sample_ok_pct', '…')} % og retsområdet i {RQ.get('sample_omr_ok_pct', '…')} %.
   - **Krydsreferencer:** "lov nr. N af …" og "bekendtgørelse nr. N af …" i paragrafteksten matches på nummer og dato og peger på den citerede version (`verificeret`). "lov om …" og kortnavne ("byggeloven") matches på titel mod lovfamilier og peger på den version, der gjaldt, da dokumentet blev udstedt (`sandsynlig`); den nuværende version står i kantens `gaeldende_version`. {nf(RSTAT.get('lovom_unmatched', 0))} "lov om …"-fraser kunne ikke matches. EU-retsakter genkendes med regex og får CELEX efter EUR-Lex' syntaks. `implementerer_EU` kræver et direktiv i samme bestemmelse som "gennemfører"/"til gennemførelse af"/"implementerer" (`sandsynlig`); forordninger er direkte anvendelige og får `henviser_til`.
   - Lovfamilier: historiske lovbekendtgørelser peger på den gældende version (`gaeldende_version`); hvis familiens nyeste version er markeret historisk efter datasættets sidste udstedelse, står den i `nyeste_version_afloeser_mangler`. Ændringslove peger på de love, titlen nævner (`aendrer`). Fra 2026-11-15 samles versionerne af love med en gældende version efter Retsinformations tidslinje for loven i stedet for efter titlen (`familie_metode: tidslinje`).
   - Krydstjek mod registry: 14 registry-noder pegede på versioner, Retsinformation har markeret historiske; de 7 med en gældende afløser i høsten har fået den (`identifikatorer.gaeldende_i_katalog`), resten er markeret med `katalog_note` og listet i huller.
   - **Ajourføring fra Retsinformations søgeeksport ({ksenest}, `pipeline/corpus/eksport.py`):** status for alle dokumenter, de dokumenter høsten manglede, og `hjemmel_for`-kanter fra eksportens hjemmelsfelt ({ktyper['hjemmel_for']} kanter), som er Retsinformations egen kobling mellem en forskrift og den lovgivning, den vedrører. Ministerium er sat fra Retsinformations ressortfelt for de {kmet.get('retsinformation', 0)} gældende dokumenter, hvor feltet med sikkerhed er aktuelt: dokumentet er udstedt efter regeringsdannelsen, eller ministeriet fik sit navn ved den. Mod feltet stemte klassifikationen i 91 % af 2.780 tilfælde, og de 248 afvigende er rettet. Nye dokumenter uden et sådant felt har arvet ministerium og retsområde fra den lov, de er udstedt efter eller ændrer ({kmet.get('arvet', 0)}), eller er klassificeret af Haiku. Resultat for de {len(kg)} gældende dokumenter: {kres.get('verificeret', 0)} `verificeret`, {kres.get('sandsynlig', 0)} `sandsynlig`, {kres.get('ukendt', 0)} `ukendt`. De øvrige samlinger er lagt i kataloget fra samme eksport. Hjemmelsfeltet giver `hjemmel_for` fra loven til forskrifter og vejledninger og `henviser_til` fra afgørelser, udtalelser og domme til loven. Af de {len(kag)} ikke-historiske dokumenter har {kamet.get('retsinformation', 0)} ministerium fra ressortfeltet efter samme regel, {kamet.get('arvet', 0)} har arvet det fra den lovgivning, de vedrører, og {kamet.get(None, 0)} har intet. Folketingstidendes dokumenter er grupperet pr. lovforslag (samling og nummer, feltet `lovforslag`), og den vedtagne tekst har feltet `lov`, når netop én lov har samme titel og er underskrevet fra 3 dage før til 60 dage efter vedtagelsen: {klove} love har fået deres lovforslag, betænkninger og ændringsforslag ad den vej.
6. **Proveniensfilter:** Alle kilde-URL'er er tjekket mod de {prov['urls']} URL'er, der faktisk optrådte i sessionens {prov['results']} søgeresultater. {prov['fjernet']} af {prov['kilder']} kilder optrådte ikke og er fjernet, og påstanden er nedgraderet.
7. **Instanslag uden for de otte domæner (fase 7, fra 2026-11-11):** Én research-agent pr. retsområde kortlægger myndigheder, klage- og tilsynsveje, hjemmelslove og dokumentkilder og leverer hver påstand med kilde-URL og et ordret citat. `pipeline/populate.py` henter derefter selv hver kilde og leder efter citatet, og læser nummer, dato, titel og status for love og bekendtgørelser direkte i Retsinformations metadata. En uafhængig kontrollant bedømmer til sidst, om belægget bærer påstanden. `verificeret` kræver et genfundet citat på en officiel side, som kontrollanten godkender, eller et opslag hos Retsinformation; ellers bliver påstanden `sandsynlig`. Fra 2026-11-12 ser kontrollanten også sidens egen tekst omkring citatet og den paragraf, citatet står i; en lov, hvis citerede version er historisk, flyttes til den gældende lovbekendtgørelse fra Retsinformations tidslinje; en historisk bekendtgørelse, vejledning eller et historisk cirkulære flyttes til det gældende dokument med samme titel blandt dem, Retsinformation fører som senere ændringer; og en `ressortansvar`-kant til en lov eller bekendtgørelse er `verificeret`, når Retsinformations ministeriefelt er det samme ministerium og med sikkerhed er sat efter regeringsdannelsen 3/6/2026 (dokumentet er udstedt efter den, eller ministeriet fik sit navn ved den). Brief, rå fund, domme og kontroljournaler ligger i `pipeline/populate-brief.md` og `raw/populate/`.

## Begrænsninger

- **Fase 7 er kontrolleret mod selve siderne, fase 1–6 er ikke.** I første runde (skat, sundhed, finansiel, udlændinge) så kontrollanterne kun selve citatet og var ikke lige strenge: sundhed, finansiel og udlændinge er bedømt hårdere end skat, så `sandsynlig` betyder dér ofte kun, at en paragraf eller frist i påstanden ikke stod i citatet. Fra anden runde (social, arbejdsmarked, transport, fødevarer) får kontrollanten sidens tekst omkring citatet og paragraffen, så de to runders `sandsynlig` kan ikke sammenlignes direkte. Retsinformations ministeriefelt er ikke ført ajour for alle ældre dokumenter (fødevare- og sociallove står fx stadig under ministerienavne fra før 3/6/2026), så det bruges kun, når feltet med sikkerhed er sat efter regeringsdannelsen.
- **Retsakterne er slået op hos Retsinformation, teksten er ikke.** `populate.py ajour` slår hver aktiv lov, bekendtgørelse og vejledning med en adresse på Retsinformation eller en katalogpost op ({len(ajour)} noder, senest {ajour_dato}). Historiske versioner flyttes til den gældende, og `identifikatorer.senere_aendringer` lister de ændringer, Retsinformation fører efter den gældende version: {len(aend)} retsakter har mindst én, {sum(aend)} i alt, så den konsoliderede tekst skal læses sammen med dem. Hjemmel- og EU-kanter, som Retsinformation selv fører mellem to noder i registry, er bekræftet eller tilføjet; kanter til retsakter uden for registry er ikke med. Hver kørsel skriver sin journal i `raw/populate/*-ajour.kontrol.json`.
- **WebFetch var blokeret i fase 1–6** af sessionens netværkspolitik for alle eksterne domæner, herunder retsinformation.dk og eur-lex.europa.eu. Al evidens er derfor søgeresultater (titel, URL og uddrag). `verificeret` betyder, at påstanden fremgår af et søgeresultat fra en officiel eller primær kilde, men siden er ikke åbnet direkte. Tillad fx `retsinformation.dk`, `eur-lex.europa.eu`, `ft.dk`, `naevneneshus.dk` og `sbst.dk` i miljøets netværksindstillinger, så kan næste iteration verificere mod selve dokumenterne.
- **Katalog-lagets kilder er datasættets egne felter**, ikke søgeresultater: hver post citerer dokumentets ELI-XML-URL (for høstens dokumenter den, seed-filen selv angiver) og repoet. Status er Retsinformations markering pr. {ksenest} (søgeeksporten) og kan være ændret siden; et dokument kan stå som historisk, før ophævelsen har virkning. Dokumenter udstedt efter 2026-02-12 og alle dokumenter uden for Lovtidende A er tilføjet fra eksporten og har kun metadata.
- **URL'er er aldrig konstrueret.** Er en side ikke set i et søgeresultat, står der `ikke fundet`, også når ELI-mønsteret gør adressen forudsigelig. ELI'er for 16 love og bekendtgørelser stammer fra `jakob1379/br18/xref-laws.toml`, som var tjekket mod Retsinformation 2026-10-26.
- **Sikkerhedsfordeling** over alle påstandsfelter og kanter: verificeret {pct.get('verificeret', 0)} %, sandsynlig {pct.get('sandsynlig', 0)} %, ukendt {pct.get('ukendt', 0)} %.
- Ressortforhold ændrer sig ofte. Kortlægningen afspejler 2026-10-28, og nedlagte eller omdøbte instanser har `status` samt `tidligere_navne` med perioder.

## Datamodel (`registry.yaml`)

**Noder** ({', '.join(f'{t} {c}' for t, c in types.most_common(12))} …) har disse felter:

- `id`, `navn`, `type`, `ministerium` (et ministerie-id eller `ingen`), `status` (aktiv/nedlagt/omdøbt/ophævet) og `domaener`.
- Påstandsfelter, hver med egne `kilder[]` og `sikkerhed`:
  - `tidligere_navne[]` (navn, periode, efterfølger);
  - `hjemmel` (oprettelsesgrundlag eller hjemmels-§);
  - `dokumenttyper` (type + bindende/vejledende);
  - `url` (kanonisk);
  - `adgang` (API/bulk/ELI/RSS/HTML/PDF/betalingsmur);
  - `identifikatorer` (ELI, Lovtidende-nr., CELEX, journalnr.);
  - `licens`;
  - `opdatering` (frekvens og versionshistorik).
- `krydsref_moenstre[]` med typiske henvisningsmønstre i teksten, nyttige som regex ved ingest.
- `ingest` (værdi og besvær 1-5), `note` og `baseline`.

**Kanter** ({', '.join(f'{t} {c}' for t, c in etypes.most_common())}) har `from`, `type`, `to`, `beskrivelse`, `kilder[]`, `sikkerhed` og `domaener`. `from` er altid den aktive part:

| Kanttype | Betydning |
|----------|-----------|
| `ressortansvar` | ministerium → instans/lov |
| `delegation` | ministerium/styrelse → styrelse/kommune |
| `hjemmel_for` | lov/bekendtgørelse → bekendtgørelse/vejledning/instans/plan |
| `udsteder` | instans → retsakt/vejledning/dokumentkilde |
| `klageinstans` | klageinstans → førsteinstans |
| `tilsyn` | tilsynsmyndighed → tilsynsobjekt |
| `implementerer_EU` | dansk retsakt → EU-retsakt |
| `henviser_til` | dokument → dokument |

**Id'er:**

| Type | Format |
|------|--------|
| Ministerier | `min-` |
| Styrelser | `sty-` |
| Nævn | `naevn-` |
| Tilsyn | `tilsyn-` |
| Råd | `raad-` |
| Fonde | `fond-` |
| Domstole | `dom-` |
| Ombudsmand | `ombud-` |
| Øvrige organisationer | `org-` |
| Love | `lov-<kortnavn>` (én node pr. lov; identifikatorer peger på gældende LBK) |
| Bekendtgørelser | `bek-` |
| Vejledninger | `vejl-` |
| Tekniske forskrifter | `tf-` |
| Planer | `plan-` |
| Regulativer | `reg-` |
| EU-retsakter | `eu-dir-ÅÅÅÅ-N`, `eu-reg-ÅÅÅÅ-N`, `eu-dec-ÅÅÅÅ-N` |
| Dokumentkilder | `kilde-` |
| Standarder | `std-` |
| Branchevejledninger | `bv-` |

Id'erne er stabile og kan bruges som nøgler i korpusset.

## Eksempel på hjemmelskæde

`min-boern-aeldre-og-bolig` —ressortansvar→ `lov-byggeloven` —hjemmel_for→ `bek-br18` ←henviser_til— `vejl-br18-vejledninger`; `bek-br18` —henviser_til→ `std-eurocodes` (kun metadata); `naevn-byggeklageenheden` —klageinstans→ `kommune-alle` og —udsteder→ `kilde-bke-afgoerelser`; `bek-br18` —implementerer_EU→ `eu-dir-2024-1275` (EPBD). Se [diagrammer/min-boern-aeldre-og-bolig.md](diagrammer/min-boern-aeldre-og-bolig.md).

## Huller (oversigt)

{', '.join(f'{t}: {c}' for t, c in gaps.most_common())}. De vigtigste er:

- **Standarder og domspraksis står bag betalingsmur.** Det gælder DS/EN og Eurocodes (dog er de danske nationale annekser gratis på bygningsreglementet.dk), UfR/Karnov, BUILD/SBi, Molio og DBI.
- **Afgørelsesportaler mangler API.** Nævnenes Hus' portaler (MFKN, PKN, EKN, Byggeklageenheden), Arbejdsmiljøklagenævnets afgørelser og Domsdatabasen (API kræver ansøgning) mangler API, bulk eller indeks. Mange afgørelser findes kun som PDF.
- **Katalog-laget har hjemmel på dokumentniveau; præambel og EU-noter er kun læst for tekstlagets udsnit.** `hjemmel_for` i kataloget er Retsinformations egen kobling fra søgeeksporten ({ktyper['hjemmel_for']} kanter). Feltet peger på den version af loven, Retsinformation fører forskriften under; for et flertal af kanterne er den udstedt senere end forskriften selv og er altså ikke den version, forskriften citerer. Paragrafhenvisningen i præamblen er læst for de {len(kxml)} dokumenter, hvis XML er hentet og har tekst: {kbest.get('retsinformation-eksport', 0)} af kanterne har lovens bestemmelser i `from_bestemmelse` (og den citerede version i `citeret_version`, når den er en anden), og {kbest.get('praeambel', 0)} kanter findes kun i præamblen. Den mest nævnte lov i teksten ramte kun hjemmelsloven i {HE.get('top', 0)} af {sum(HE.values())} kendte tilfælde og er ikke brugt. {kuden} af de {len(kg)} gældende dokumenter i Lovtidende A har ingen tekst, hverken i bulk-høsten eller i tekstlaget, og i de øvrige samlinger har kun de {sum(not i.startswith('lta-') for i in kxml)} hentede dokumenter tekst. Retsinformations XML har ingen tekst for {len(ktekst) - len(kxml)} af de hentede dokumenter, især fra før 2010; om de findes som PDF med tekst, er ikke undersøgt. For resten er koblingen til lovgivningen Retsinformations felt for hjemmel og vedrørt lovgivning: det siger ikke, hvilken paragraf dokumentet angår, og {len(kag) - kakob} af de {len(kag)} ikke-historiske har ingen kobling. Lovforslag er koblet til loven på titel og dato, ikke på en henvisning i loven: for love fra før 1998 har Retsinformation ikke den vedtagne tekst, så de er ikke koblet, og skriftlige fremsættelser og beslutningsforslag har ingen kobling. Teksten kan hentes fra Retsinformations ELI-XML med ét kald pr. dokument (værktøjerne holder 10,5 sekunder mellem kald).
- **Ressort og status er uafklaret flere steder.** Det gælder bl.a. miljøvurderingsloven (Miljøministeriet eller Natur og Dyrevelfærd) og affaldsbekendtgørelsen (KEFM eller Miljøstyrelsen). Det gælder også Social- og Boligstyrelsens opdeling, udfasningen af navnet Kystdirektoratet og den danske gennemførelse af EPBD-recast, IED 2.0 og gasdirektivet 2024/1788.
"""
(SP / "dk-regulering" / "README.md").write_text(doc, encoding="utf-8")
print("README", len(doc))
