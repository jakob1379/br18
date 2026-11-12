# Dansk regulering: kortlægning til RAG

**Kortlagt i dybden (registry):** byggeri · bolig · plan · energi · miljø · arbejdsmiljø · brand · el/gas/VVS. **Instanslag tilføjet i fase 7:** arbejdsmarked og ydelser · finansiel regulering · fiskeri · fødevarer · landbrug og dyr · skat og afgifter · social · sundhed · transport · udlændinge og integration (167 noder; senest opdateret 2026-11-12). **Bredt (katalog):** hele Lovtidende A – 62762 love, lovbekendtgørelser, bekendtgørelser og anordninger, heraf 13819 gældende. **Status pr. 2026-10-28** (katalogets dokumentstatus pr. 2026-06-12).

Kortlægningen dækker myndigheder, retsakter, klage- og tilsynsveje, EU-retsakter og dokumentkilder. Den skal bruges til at bygge et krydsrefereret korpus (udvidelse af `jakob1379/br18`), hvor søgning kan følge hjemmelskæder fra lov til bekendtgørelse til vejledning til praksis. Der er **ikke** hentet dokumenter til korpusset; katalog-laget er metadata og krydsreferencer udledt af en offentlig bulk-høst.

To lag:

- **Registry** (`registry.yaml`): håndkurateret og verificeret graf over myndigheder, centrale retsakter, klage-/tilsynsveje, EU-retsakter og datakilder for de otte domæner.
- **Katalog** (`katalog/`): én post pr. dokument i Lovtidende A fra Retsinformation (62762), bygget fra bulk-høsten `Ansvar-Systems/danish-law-mcp` uden websøgning. Hver post har Lovtidende-nr., DocumentId, status, datoer, udstedende ministerium og, for gældende dokumenter, nuværende ressortministerium og retsområde. 136557 kanter (`henviser_til`, `implementerer_EU`, `ressortansvar`) og 1778 refererede EU-retsakter med CELEX. 222 registry-noder er koblet til deres katalogpost (`katalog_id` ↔ `registry_ids`).

| Fil | Indhold |
|-----|---------|
| [`registry.yaml`](registry.yaml) | **Sandheden.** Indeholder meta, regering, ressortomlægninger, uafklarede konflikter, 782 noder, 1611 kanter og 273 huller. |
| [`diagrammer/oversigt.md`](diagrammer/oversigt.md) | Mermaid-overblik over ministerier og instanser, med ét diagram pr. ministerområde (21 aktive ministerier plus nedlagte/omdøbte). |
| [`datakilder.md`](datakilder.md) | Datakilder sorteret efter ingest-prioritet (værdi ÷ besvær) i tre tabeller: portaler/databaser, udstedende instanser og retsakter/samlinger. |
| [`huller.md`](huller.md) | Betalingsmur, kun PDF, intet API, uklare forhold og ikke-fundne kilder. |
| [`katalog/retsinformation_lta.jsonl`](katalog/retsinformation_lta.jsonl) | Katalog-laget: én JSON-linje pr. Lovtidende A-dokument (62762). |
| [`katalog/kanter.jsonl`](katalog/kanter.jsonl) | 136557 kanter fra katalog-dokumenter (kun de tilladte kanttyper). |
| [`katalog/eu_index.jsonl`](katalog/eu_index.jsonl) | 1778 EU-retsakter nævnt i dansk lovtekst, med CELEX og antal danske dokumenter. |
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
| Byggeri: byggeloven og bygningsreglementet (BR18) | Børne-, Ældre- og Boligministeriet | Social- og Boligstyrelsen, Byggeklageenheden, Nævnenes Hus | `verificeret` |
| Certificering af statikere og brandrådgivere | Børne-, Ældre- og Boligministeriet | Social- og Boligstyrelsen | `sandsynlig` |
| Byggeskadeforsikring (obligatorisk for nyt helårsbyggeri) | Børne-, Ældre- og Boligministeriet | Social- og Boligstyrelsen | `verificeret` |
| Byggevarer: regler om markedsføring og CE-mærkning (CPR 305/2011 og revideret CPR 2024/3110) | Børne-, Ældre- og Boligministeriet | Social- og Boligstyrelsen | `sandsynlig` |
| Byggevarer: markedsovervågning (CPR) | Erhvervsministeriet | Erhvervsstyrelsen | `verificeret` |
| Almene boliger (inkl. ældre-, studie-, ungdoms- og friplejeboliger) og Landsbyggefonden | Børne-, Ældre- og Boligministeriet | Social- og Boligstyrelsen, Landsbyggefonden, Byggeskadefonden, Beboerklagenævn (kommunale) | `verificeret` |
| Privat udlejning: lejeloven, lov om boligforhold, huslejenævn og Grundejernes Investeringsfond | Børne-, Ældre- og Boligministeriet | Social- og Boligstyrelsen, Huslejenævn (kommunale), Grundejernes Investeringsfond (GI), Boligretten (ved byretterne) | `verificeret` |
| Andelsboliger og ejerlejligheder | Børne-, Ældre- og Boligministeriet | Social- og Boligstyrelsen | `sandsynlig` |
| Byfornyelse | Børne-, Ældre- og Boligministeriet | Social- og Boligstyrelsen, Byggeskadefonden | `verificeret` |
| Boligstøtte (boligsikring og boligydelse) | Beskæftigelses- og Ligestillingsministeriet | Udbetaling Danmark | `verificeret` |
| Indsatsen mod parallelsamfund (udsatte almene boligområder, ghettorepræsentanter, parallelsamfundsredegørelse) | Udlændinge- og Integrationsministeriet | – | `verificeret` |
| Plan: planloven, landsplandirektiver, Fingerplan, kystnærhedszone og zoneregler (land, by og sommerhus) | By-, Land- og Transportministeriet | Plan- og Landdistriktsstyrelsen, Planklagenævnet | `verificeret` |
| Udstykning og matrikel | Klima-, Energi- og Forsyningsministeriet | Geodatastyrelsen, Klimadatastyrelsen | `verificeret` |
| Bygningsfredning og bevaring | Kulturministeriet | Slots- og Kulturstyrelsen, Det Særlige Bygningssyn | `verificeret` |
| Energimærkning af bygninger og energieffektivitet | Klima-, Energi- og Forsyningsministeriet | Energistyrelsen, Energiklagenævnet | `sandsynlig` |
| Varmeforsyning (fjernvarme) | Klima-, Energi- og Forsyningsministeriet | Energistyrelsen, Forsyningstilsynet, Energiklagenævnet | `sandsynlig` |
| El- og gasforsyning og vedvarende energi (VE) | Klima-, Energi- og Forsyningsministeriet | Energistyrelsen, Forsyningstilsynet, Energinet, Energiklagenævnet | `verificeret` |
| Ladestandere: offentligt tilgængelige ladepunkter (AFI-loven/AFIR) | By-, Land- og Transportministeriet | Færdselsstyrelsen | `sandsynlig` |
| Ladestandere i bygninger (ladestanderbekendtgørelsen) | Børne-, Ældre- og Boligministeriet | Social- og Boligstyrelsen | `sandsynlig` |
| Forsyningstilsyn (el, gas og varme samt vandsektorens økonomi) | Klima-, Energi- og Forsyningsministeriet | Forsyningstilsynet, Vandsektortilsynet | `verificeret` |
| Miljøbeskyttelse inkl. støj | Miljøministeriet | Miljøstyrelsen, Miljø- og Fødevareklagenævnet, Danmarks Miljøportal | `verificeret` |
| Jordforurening | Miljøministeriet | Miljøstyrelsen, Miljø- og Fødevareklagenævnet | `sandsynlig` |
| Kemikalier | Miljøministeriet | Miljøstyrelsen | `sandsynlig` |
| Miljøvurdering (VVM og plan-SMV) | Ministeriet for Natur og Dyrevelfærd | Miljøstyrelsen, Styrelsen for Grøn Arealomlægning og Vandmiljø (SGAV), Planklagenævnet, Miljø- og Fødevareklagenævnet | `verificeret` |
| Affald inkl. bygge- og anlægsaffald | Klima-, Energi- og Forsyningsministeriet | Energistyrelsen, Miljøstyrelsen | `verificeret` |
| Natur: naturbeskyttelse og habitat/Natura 2000 | Ministeriet for Natur og Dyrevelfærd | Styrelsen for Grøn Arealomlægning og Vandmiljø (SGAV), Naturstyrelsen, Miljø- og Fødevareklagenævnet | `verificeret` |
| Kystbeskyttelse | Miljøministeriet | Kystdirektoratet, Miljøstyrelsen, Miljø- og Fødevareklagenævnet | `verificeret` |
| Drikkevand og grundvandsbeskyttelse | Miljøministeriet | Miljøstyrelsen | `verificeret` |
| Spildevand | Miljøministeriet | Miljøstyrelsen | `verificeret` |
| Vandsektor: økonomisk regulering og organisering | Klima-, Energi- og Forsyningsministeriet | Energistyrelsen, Vandsektortilsynet, Konkurrence- og Forbrugerstyrelsen | `verificeret` |
| Vandmiljø og vandplanlægning | Ministeriet for Natur og Dyrevelfærd | Styrelsen for Grøn Arealomlægning og Vandmiljø (SGAV) | `sandsynlig` |
| Arbejdsmiljø inkl. byggepladser og asbest | Beskæftigelses- og Ligestillingsministeriet | Arbejdstilsynet, Arbejdsmiljøklagenævnet, Ankestyrelsen | `verificeret` |
| Beredskab og brand | Ministeriet for Samfundssikkerhed og Beredskab | Beredskabsstyrelsen, Styrelsen for Samfundssikkerhed | `verificeret` |
| Elsikkerhed og gassikkerhed | Erhvervsministeriet | Erhvervsstyrelsen | `sandsynlig` |
| Autorisation af el-, VVS- og kloakvirksomheder | Erhvervsministeriet | Erhvervsstyrelsen | `sandsynlig` |
| Klagenævn: Nævnenes Hus m.fl. | Erhvervsministeriet | Nævnenes Hus, Planklagenævnet, Miljø- og Fødevareklagenævnet, Energiklagenævnet, Erhvervsankenævnet, Byggeklageenheden | `sandsynlig` |
| Kommunaltilsyn | Økonomi- og Indenrigsministeriet | Ankestyrelsen | `verificeret` |
| Folketingets Ombudsmand | ingen | Folketingets Ombudsmand | `verificeret` |
| Retsinformation og Lovtidende (kundgørelse af love og forskrifter) | Justitsministeriet | Civilstyrelsen | `sandsynlig` |
| Domstole og Domsdatabasen | Justitsministeriet | Domstolsstyrelsen, Boligretten (ved byretterne) | `sandsynlig` |

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
   - **Nuværende ressort og retsområde** for de 13819 gældende dokumenter: 50 Haiku-agenter (effort high, ingen websøgning) klassificerede alle ud fra titel, udsteder og en ressortguide for kgl. res. 3/6/2026. De 1755 usikre blev klassificeret igen af Opus (effort high) med en skærpet guide. Hvor et dokument er en registry-node med en ressortansvar-kant, bruges registry'ets ministerium (110 dokumenter). Kvalitet: mod registry'et stemmer 88 % af de "sandsynlige" klassifikationer (189 noder), og en uafhængig Opus-kontrol af 437 tilfældige "sandsynlige" (højst 20 pr. ministerium) fandt ministeriet korrekt i 93 % og retsområdet i 92 %. Resultat: 58 `verificeret`, 13453 `sandsynlig`, 308 `ukendt`.
   - **Krydsreferencer:** "lov nr. N af …" og "bekendtgørelse nr. N af …" i paragrafteksten matches på nummer og dato og peger på den citerede version (`verificeret`). "lov om …" og kortnavne ("byggeloven") matches på titel mod lovfamilier og peger på den version, der gjaldt, da dokumentet blev udstedt (`sandsynlig`); den nuværende version står i kantens `gaeldende_version`. 5.252 "lov om …"-fraser kunne ikke matches. EU-retsakter genkendes med regex og får CELEX efter EUR-Lex' syntaks. `implementerer_EU` kræver et direktiv i samme bestemmelse som "gennemfører"/"til gennemførelse af"/"implementerer" (`sandsynlig`); forordninger er direkte anvendelige og får `henviser_til`.
   - Lovfamilier: historiske lovbekendtgørelser peger på den gældende version (`gaeldende_version`); hvis familiens nyeste version er markeret historisk efter datasættets sidste udstedelse, står den i `nyeste_version_afloeser_mangler`. Ændringslove peger på de love, titlen nævner (`aendrer`).
   - Krydstjek mod registry: 14 registry-noder pegede på versioner, Retsinformation har markeret historiske; de 7 med en gældende afløser i høsten har fået den (`identifikatorer.gaeldende_i_katalog`), resten er markeret med `katalog_note` og listet i huller.
6. **Proveniensfilter:** Alle kilde-URL'er er tjekket mod de 27859 URL'er, der faktisk optrådte i sessionens 3745 søgeresultater. 447 af 15995 kilder optrådte ikke og er fjernet, og påstanden er nedgraderet.
7. **Instanslag uden for de otte domæner (fase 7, fra 2026-11-11):** Én research-agent pr. retsområde kortlægger myndigheder, klage- og tilsynsveje, hjemmelslove og dokumentkilder og leverer hver påstand med kilde-URL og et ordret citat. `pipeline/populate.py` henter derefter selv hver kilde og leder efter citatet, og læser nummer, dato, titel og status for love og bekendtgørelser direkte i Retsinformations metadata. En uafhængig kontrollant bedømmer til sidst, om belægget bærer påstanden. `verificeret` kræver et genfundet citat på en officiel side, som kontrollanten godkender, eller et opslag hos Retsinformation; ellers bliver påstanden `sandsynlig`. Fra 2026-11-12 ser kontrollanten også sidens egen tekst omkring citatet og den paragraf, citatet står i; en lov, hvis citerede version er historisk, flyttes til den gældende lovbekendtgørelse fra Retsinformations tidslinje; og en `ressortansvar`-kant til en lov eller bekendtgørelse er `verificeret`, når Retsinformations ministeriefelt for det gældende dokument er det samme ministerium. Brief, rå fund, domme og kontroljournaler ligger i `pipeline/populate-brief.md` og `raw/populate/`.

## Begrænsninger

- **Fase 7 er kontrolleret mod selve siderne, fase 1–6 er ikke.** I første runde (skat, sundhed, finansiel, udlændinge) så kontrollanterne kun selve citatet og var ikke lige strenge: sundhed, finansiel og udlændinge er bedømt hårdere end skat, så `sandsynlig` betyder dér ofte kun, at en paragraf eller frist i påstanden ikke stod i citatet. Fra anden runde (social, arbejdsmarked, transport, fødevarer) får kontrollanten sidens tekst omkring citatet og paragraffen, så de to runders `sandsynlig` kan ikke sammenlignes direkte. Retsinformations ministeriefelt er ikke ført ajour for alle dokumenter (fødevare- og sociallove står fx stadig under ministerienavne fra før 3/6/2026), så det bekræfter kun et ministerium, når feltet er et nuværende ministerienavn.
- **WebFetch var blokeret i fase 1–6** af sessionens netværkspolitik for alle eksterne domæner, herunder retsinformation.dk og eur-lex.europa.eu. Al evidens er derfor søgeresultater (titel, URL og uddrag). `verificeret` betyder, at påstanden fremgår af et søgeresultat fra en officiel eller primær kilde, men siden er ikke åbnet direkte. Tillad fx `retsinformation.dk`, `eur-lex.europa.eu`, `ft.dk`, `naevneneshus.dk` og `sbst.dk` i miljøets netværksindstillinger, så kan næste iteration verificere mod selve dokumenterne.
- **Katalog-lagets kilder er datasættets egne felter**, ikke søgeresultater: hver post citerer den ELI-XML-URL, seed-filen selv angiver, og repoet. Status er Retsinformations status ved høsten 2026-06-10–12 og kan være ændret siden. Dokumenter udstedt efter 2026-02-12 mangler.
- **URL'er er aldrig konstrueret.** Er en side ikke set i et søgeresultat, står der `ikke fundet`, også når ELI-mønsteret gør adressen forudsigelig. ELI'er for 16 love og bekendtgørelser stammer fra `jakob1379/br18/xref-laws.toml`, som var tjekket mod Retsinformation 2026-10-26.
- **Sikkerhedsfordeling** over alle påstandsfelter og kanter: verificeret 73 %, sandsynlig 18 %, ukendt 9 %.
- Ressortforhold ændrer sig ofte. Kortlægningen afspejler 2026-10-28, og nedlagte eller omdøbte instanser har `status` samt `tidligere_navne` med perioder.

## Datamodel (`registry.yaml`)

**Noder** (bekendtgørelse 166, lov 145, dokumentkilde 78, eu-direktiv 68, styrelse 59, vejledning 35, privat-organisation 27, eu-forordning 25, ministerium 25, nævn 22, plan 20, klagenævn 16 …) har disse felter:

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

**Kanter** (hjemmel_for 460, ressortansvar 315, udsteder 269, henviser_til 253, implementerer_EU 125, klageinstans 95, tilsyn 77, delegation 17) har `from`, `type`, `to`, `beskrivelse`, `kilder[]`, `sikkerhed` og `domaener`. `from` er altid den aktive part:

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

uklart: 140, ikke-fundet: 88, andet: 20, ingen-api: 13, kun-pdf: 7, betalingsmur: 5. De vigtigste er:

- **Standarder og domspraksis står bag betalingsmur.** Det gælder DS/EN og Eurocodes (dog er de danske nationale annekser gratis på bygningsreglementet.dk), UfR/Karnov, BUILD/SBi, Molio og DBI.
- **Afgørelsesportaler mangler API.** Nævnenes Hus' portaler (MFKN, PKN, EKN, Byggeklageenheden), Arbejdsmiljøklagenævnets afgørelser og Domsdatabasen (API kræver ansøgning) mangler API, bulk eller indeks. Mange afgørelser findes kun som PDF.
- **Katalog-laget mangler præambel og EU-noter.** Hjemmel (`hjemmel_for`) kan derfor ikke udledes for de 62.762 katalog-dokumenter; den mest nævnte lov ramte kun hjemmelsloven i 34 af 113 kendte tilfælde og er ikke brugt. Cirkulærer, vejledninger, Lovtidende B/C og afgørelser er ikke i bulk-kilden, og dokumenter efter 2026-02-12 mangler. Retsinformations høsteservice (højst ét kald pr. 10 s) kan lukke hullerne, når netværkspolitikken tillader det.
- **Ressort og status er uafklaret flere steder.** Det gælder bl.a. miljøvurderingsloven (Miljøministeriet eller Natur og Dyrevelfærd) og affaldsbekendtgørelsen (KEFM eller Miljøstyrelsen). Det gælder også Social- og Boligstyrelsens opdeling, udfasningen af navnet Kystdirektoratet og den danske gennemførelse af EPBD-recast, IED 2.0 og gasdirektivet 2024/1788.
