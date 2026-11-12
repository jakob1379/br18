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
kedges = sum(1 for _ in open(KD / "kanter.jsonl", encoding="utf-8"))
keu = sum(1 for _ in open(KD / "eu_index.jsonl", encoding="utf-8"))
kg = [d for d in kdocs if d["status"]["vaerdi"] == "gældende"]
kres = Counter((d.get("ministerium") or {}).get("sikkerhed", "ingen") for d in kg)
kreg = sum(len(d.get("registry_ids") or []) for d in kdocs)
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

**Kortlagt i dybden (registry):** byggeri · bolig · plan · energi · miljø · arbejdsmiljø · brand · el/gas/VVS. **Instanslag tilføjet i fase 7:** {' · '.join(OMR[d].lower() for d in fase7)} ({n7} noder; senest opdateret {m.get('opdateret', 'ukendt')[:10]}). **Bredt (katalog):** hele Lovtidende A – {len(kdocs)} love, lovbekendtgørelser, bekendtgørelser og anordninger, heraf {len(kg)} gældende. **Status pr. 2026-10-28** (katalogets dokumentstatus pr. 2026-06-12).

Kortlægningen dækker myndigheder, retsakter, klage- og tilsynsveje, EU-retsakter og dokumentkilder. Den skal bruges til at bygge et krydsrefereret korpus (udvidelse af `jakob1379/br18`), hvor søgning kan følge hjemmelskæder fra lov til bekendtgørelse til vejledning til praksis. Der er **ikke** hentet dokumenter til korpusset; katalog-laget er metadata og krydsreferencer udledt af en offentlig bulk-høst.

To lag:

- **Registry** (`registry.yaml`): håndkurateret og verificeret graf over myndigheder, centrale retsakter, klage-/tilsynsveje, EU-retsakter og datakilder for de otte domæner.
- **Katalog** (`katalog/`): én post pr. dokument i Lovtidende A fra Retsinformation ({len(kdocs)}), bygget fra bulk-høsten `Ansvar-Systems/danish-law-mcp` uden websøgning. Hver post har Lovtidende-nr., DocumentId, status, datoer, udstedende ministerium og, for gældende dokumenter, nuværende ressortministerium og retsområde. {kedges} kanter (`henviser_til`, `implementerer_EU`, `ressortansvar`) og {keu} refererede EU-retsakter med CELEX. {kreg} registry-noder er koblet til deres katalogpost (`katalog_id` ↔ `registry_ids`).

| Fil | Indhold |
|-----|---------|
| [`registry.yaml`](registry.yaml) | **Sandheden.** Indeholder meta, regering, ressortomlægninger, uafklarede konflikter, {len(m['nodes'])} noder, {len(m['edges'])} kanter og {len(m['huller'])} huller. |
| [`diagrammer/oversigt.md`](diagrammer/oversigt.md) | Mermaid-overblik over ministerier og instanser, med ét diagram pr. ministerområde ({len(mins)} aktive ministerier plus nedlagte/omdøbte). |
| [`datakilder.md`](datakilder.md) | Datakilder sorteret efter ingest-prioritet (værdi ÷ besvær) i tre tabeller: portaler/databaser, udstedende instanser og retsakter/samlinger. |
| [`huller.md`](huller.md) | Betalingsmur, kun PDF, intet API, uklare forhold og ikke-fundne kilder. |
| [`katalog/retsinformation_lta.jsonl`](katalog/retsinformation_lta.jsonl) | Katalog-laget: én JSON-linje pr. Lovtidende A-dokument ({len(kdocs)}). |
| [`katalog/kanter.jsonl`](katalog/kanter.jsonl) | {kedges} kanter fra katalog-dokumenter (kun de tilladte kanttyper). |
| [`katalog/eu_index.jsonl`](katalog/eu_index.jsonl) | {keu} EU-retsakter nævnt i dansk lovtekst, med CELEX og antal danske dokumenter. |
| [`katalog/README.md`](katalog/README.md) | Genereret oversigt over katalog-laget (typer, ressort, retsområder, kanter, top EU-retsakter). |
| [`scripts/build.py`](scripts/build.py) | Validerer `registry.yaml` og katalog-laget og genererer views ovenfor. Kør `python3 scripts/build.py`, og brug `--check` i CI. |

## Scope

Scope-felterne i opgaven var ikke udfyldt. Første mulighed i hver parentes er valgt:

- **Domæner:** byggeri, bolig, plan, energi, miljø, arbejdsmiljø, brand og el/gas/VVS, ikke hele staten. Natur, vand og kyst er taget med som en del af miljø.
- **Niveauer:** stat, kommunalt og EU. Kommuner og regioner er aggregeret i `kommune-alle` og `region-alle`, og deres plantyper, regulativer og datakilder er egne noder.
- **Praksis:** klagenævn, Ankestyrelsen, Folketingets Ombudsmand og domstole.
- **Standarder og branchevejledninger** (DS/EN, Eurocodes, BUILD/SBi, Molio, DBI, TEKNIQ, BFA m.fl.) er **kun metadata**.
- **Al offentlig lovgivning (udvidelse):** hele Lovtidende A er med i katalog-laget, uanset domæne. Cirkulærer, vejledninger og afgørelser uden for de otte domæner er ikke med, fordi bulk-kilden ikke rummer dem (se huller).

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
   - **Nuværende ressort og retsområde** for de {len(kg)} gældende dokumenter: 50 Haiku-agenter (effort high, ingen websøgning) klassificerede alle ud fra titel, udsteder og en ressortguide for kgl. res. 3/6/2026. De {RQ.get('opus_recheck_n', '…')} usikre blev klassificeret igen af Opus (effort high) med en skærpet guide. Hvor et dokument er en registry-node med en ressortansvar-kant, bruges registry'ets ministerium ({kmet.get('registry', 0)} dokumenter). Kvalitet: mod registry'et stemmer {RQ.get('registry_match_pct', '…')} % af de "sandsynlige" klassifikationer ({RQ.get('registry_n', '…')} noder), og en uafhængig Opus-kontrol af {RQ.get('sample_n', '…')} tilfældige "sandsynlige" (højst 20 pr. ministerium) fandt ministeriet korrekt i {RQ.get('sample_ok_pct', '…')} % og retsområdet i {RQ.get('sample_omr_ok_pct', '…')} %. Resultat: {kres.get('verificeret', 0)} `verificeret`, {kres.get('sandsynlig', 0)} `sandsynlig`, {kres.get('ukendt', 0)} `ukendt`.
   - **Krydsreferencer:** "lov nr. N af …" og "bekendtgørelse nr. N af …" i paragrafteksten matches på nummer og dato og peger på den citerede version (`verificeret`). "lov om …" og kortnavne ("byggeloven") matches på titel mod lovfamilier og peger på den version, der gjaldt, da dokumentet blev udstedt (`sandsynlig`); den nuværende version står i kantens `gaeldende_version`. {nf(RSTAT.get('lovom_unmatched', 0))} "lov om …"-fraser kunne ikke matches. EU-retsakter genkendes med regex og får CELEX efter EUR-Lex' syntaks. `implementerer_EU` kræver et direktiv i samme bestemmelse som "gennemfører"/"til gennemførelse af"/"implementerer" (`sandsynlig`); forordninger er direkte anvendelige og får `henviser_til`.
   - Lovfamilier: historiske lovbekendtgørelser peger på den gældende version (`gaeldende_version`); hvis familiens nyeste version er markeret historisk efter datasættets sidste udstedelse, står den i `nyeste_version_afloeser_mangler`. Ændringslove peger på de love, titlen nævner (`aendrer`).
   - Krydstjek mod registry: 14 registry-noder pegede på versioner, Retsinformation har markeret historiske; de 7 med en gældende afløser i høsten har fået den (`identifikatorer.gaeldende_i_katalog`), resten er markeret med `katalog_note` og listet i huller.
6. **Proveniensfilter:** Alle kilde-URL'er er tjekket mod de {prov['urls']} URL'er, der faktisk optrådte i sessionens {prov['results']} søgeresultater. {prov['fjernet']} af {prov['kilder']} kilder optrådte ikke og er fjernet, og påstanden er nedgraderet.
7. **Instanslag uden for de otte domæner (fase 7, fra 2026-11-11):** Én research-agent pr. retsområde kortlægger myndigheder, klage- og tilsynsveje, hjemmelslove og dokumentkilder og leverer hver påstand med kilde-URL og et ordret citat. `pipeline/populate.py` henter derefter selv hver kilde og leder efter citatet, og læser nummer, dato, titel og status for love og bekendtgørelser direkte i Retsinformations metadata. En uafhængig kontrollant bedømmer til sidst, om belægget bærer påstanden. `verificeret` kræver et genfundet citat på en officiel side, som kontrollanten godkender, eller et opslag hos Retsinformation; ellers bliver påstanden `sandsynlig`. Fra 2026-11-12 ser kontrollanten også sidens egen tekst omkring citatet og den paragraf, citatet står i; en lov, hvis citerede version er historisk, flyttes til den gældende lovbekendtgørelse fra Retsinformations tidslinje; og en `ressortansvar`-kant til en lov eller bekendtgørelse er `verificeret`, når Retsinformations ministeriefelt er det samme ministerium og med sikkerhed er sat efter regeringsdannelsen 3/6/2026 (dokumentet er udstedt efter den, eller ministeriet fik sit navn ved den). Brief, rå fund, domme og kontroljournaler ligger i `pipeline/populate-brief.md` og `raw/populate/`.

## Begrænsninger

- **Fase 7 er kontrolleret mod selve siderne, fase 1–6 er ikke.** I første runde (skat, sundhed, finansiel, udlændinge) så kontrollanterne kun selve citatet og var ikke lige strenge: sundhed, finansiel og udlændinge er bedømt hårdere end skat, så `sandsynlig` betyder dér ofte kun, at en paragraf eller frist i påstanden ikke stod i citatet. Fra anden runde (social, arbejdsmarked, transport, fødevarer) får kontrollanten sidens tekst omkring citatet og paragraffen, så de to runders `sandsynlig` kan ikke sammenlignes direkte. Retsinformations ministeriefelt er ikke ført ajour for alle ældre dokumenter (fødevare- og sociallove står fx stadig under ministerienavne fra før 3/6/2026), så det bruges kun, når feltet med sikkerhed er sat efter regeringsdannelsen.
- **Gældende version er slået op for retsakterne, ikke for teksten.** Den 12/11/2026 blev de 239 aktive love, bekendtgørelser og vejledninger med en adresse på Retsinformation slået op (`populate.py ajour`): 227 er gældende, 3 love pegede på en historisk lovbekendtgørelse og er flyttet til den gældende (sundhedsloven, erhvervslejeloven og havstrategiloven), og 9 bekendtgørelser er historiske, uden at afløseren er fundet (tidslinjen dækker kun love). Ændringslove, der er kommet efter den gældende lovbekendtgørelse, er ikke registreret. Journal: `raw/populate/2026-11-12-ajour.kontrol.json`.
- **WebFetch var blokeret i fase 1–6** af sessionens netværkspolitik for alle eksterne domæner, herunder retsinformation.dk og eur-lex.europa.eu. Al evidens er derfor søgeresultater (titel, URL og uddrag). `verificeret` betyder, at påstanden fremgår af et søgeresultat fra en officiel eller primær kilde, men siden er ikke åbnet direkte. Tillad fx `retsinformation.dk`, `eur-lex.europa.eu`, `ft.dk`, `naevneneshus.dk` og `sbst.dk` i miljøets netværksindstillinger, så kan næste iteration verificere mod selve dokumenterne.
- **Katalog-lagets kilder er datasættets egne felter**, ikke søgeresultater: hver post citerer den ELI-XML-URL, seed-filen selv angiver, og repoet. Status er Retsinformations status ved høsten 2026-06-10–12 og kan være ændret siden. Dokumenter udstedt efter 2026-02-12 mangler.
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
- **Katalog-laget mangler præambel og EU-noter.** Hjemmel (`hjemmel_for`) kan derfor ikke udledes for de 62.762 katalog-dokumenter; den mest nævnte lov ramte kun hjemmelsloven i {HE.get('top', 0)} af {sum(HE.values())} kendte tilfælde og er ikke brugt. Cirkulærer, vejledninger, Lovtidende B/C og afgørelser er ikke i bulk-kilden, og dokumenter efter 2026-02-12 mangler. Retsinformations høsteservice (højst ét kald pr. 10 s) kan lukke hullerne, når netværkspolitikken tillader det.
- **Ressort og status er uafklaret flere steder.** Det gælder bl.a. miljøvurderingsloven (Miljøministeriet eller Natur og Dyrevelfærd) og affaldsbekendtgørelsen (KEFM eller Miljøstyrelsen). Det gælder også Social- og Boligstyrelsens opdeling, udfasningen af navnet Kystdirektoratet og den danske gennemførelse af EPBD-recast, IED 2.0 og gasdirektivet 2024/1788.
"""
(SP / "dk-regulering" / "README.md").write_text(doc, encoding="utf-8")
print("README", len(doc))
