# Dansk regulering – datapakke

Bygget 2026-11-11 20:25 UTC. Kortlægning af danske myndigheder og retskilder til et RAG-korpus (udvidelse af jakob1379/br18).
Status for registry'et pr. 2026-10-28, med retsakternes version slået op hos Retsinformation 2026-11-12 og -13 og senest 2026-11-21; katalogets dokumentstatus pr. 2026-11-12 (udstedelser til 2026-11-11), for Lovtidende A fra 2013, 2023, 2025 og 2026 pr. 2026-11-23.

**Ændret siden pakningen (fase 7, fra 2026-11-11):** `dk-regulering/registry.yaml` rettes nu direkte med `pipeline/populate.py`, og `pipeline/views.sh` genskaber README, views, `intermediate/registry/final.json`, `viz_data.json` og kortet. Nye filer: `pipeline/populate.py`, `pipeline/populate-brief.md`, `pipeline/views.sh` og `raw/populate/` (agenternes fund, kontrollanternes domme og kontroljournaler). `dashboard/mangler.json` rettes i hånden; katalog- og registry-tallene i `fremdrift.json`, `omraader.json` og `maalt.json` genberegnes af `pipeline/corpus/eksport.py katalog`. Runde 2 (2026-11-12: social, arbejdsmarked, transport og fødevarer) ligger i `raw/populate/2026-11-12-*`. Ud over fund (`.json`), domme (`.dom.json`) og kontroljournaler (`.kontrol.json`) gemmes nu også kontrollantens grundlag (`.review.json`, med sidens egen tekst omkring hvert citat) og en efterkontrol af 16 påstande, hvis sider først kunne hentes i andet forsøg. Review-filerne er genskabt efter kontrollen, så `paragraf` kan afvige fra det, kontrollanten så, for citater fra titler. Runde 3 (samme dag: søfart, persondata, strafferet/politi og arbejdsret) og runde 4 (forbruger, erhvervsret, undervisning og familieret) ligger i samme mappe; arbejdsret har områdenøglen `arbejdsmarked`, forbruger `forbruger-konkurrence` og familieret `familie-person`. Runde 5 (samme dag: digitalisering og tele, retspleje, kultur og medier samt kirke) ligger også dér; NIS 2-tilsynet er lagt under `digitalisering-tele`. For runde 5 er review-filerne, som kontrollanten så dem: orkestratoren fjernede derefter tre kanter, der hvilede på for lidt, og rettede to tekster i fundene, og kontrollanten genbedømte to påstande i kultur-medier, efter at et afkortet citat var rettet til sidens ordlyd. Fra 2026-11-13 slår `populate.py ajour` også de retsakter op, der kun har en katalogpost og ingen adresse på Retsinformation: 48 love og bekendtgørelser i de otte oprindelige domæner (journal `raw/populate/2026-11-13T0005-ajour.kontrol.json`). `raw/populate/*-ajour.kontrol.json` er journalerne fra `populate.py ajour` (én pr. kørsel; den første har kun datoen i navnet): status hos Retsinformation for alle aktive retsakter i registry, de retsakter, der blev flyttet til gældende version, og de ressortansvar-, hjemmel_for- og implementerer_EU-kanter, Retsinformation bekræftede eller gav. Noder, hvis navn ikke svarer til det dokument, de peger på, står dér med `titel_afviger` og er ikke rørt. Seneste kørsel 2026-11-21 (journal `raw/populate/2026-11-21T2006-ajour.kontrol.json`): 395 retsakter slået op (388 gældende, 7 historiske, ingen fejlede opslag); 3 flyttet til gældende version (bek-asbest, bek-bygherrens-pligter, lov-straffuldbyrdelsesloven); 6 med `titel_afviger`, ikke rørt; én ressortansvar-kant opgraderet til verificeret og én hjemmel_for-kant tilføjet som sandsynlig (lov-produktloven → bek-trykbaerende-udstyr). 2026-11-23 (JGA-143, `raw/populate/2026-11-23-jga143.*` og `-jga143-klagepar.*`): de tre nye versioner står nu i kataloget (BEK nr. 1002 og 1003 af 2026 og LBK nr. 982 af 2026, gældende pr. 2026-11-23), og de tre nodes `katalog_id` peger på dem; de gamle versioner (BEK nr. 117 af 2013, LBK nr. 201 af 2023, BEK nr. 1328 af 2025) er historiske. Hjemmel_for-kanten fra produktloven er sandsynlig: BEK nr. 493 af 2026 § 1, nr. 2, har affattet bekendtgørelsens indledning, så den citerer produktloven, men det er den eneste retsakt, der siger det, og begge uafhængige dommere sagde delvist, hvilket `populate.py` lader give højst sandsynlig (efter review samme dag; kanten var først sat til verificeret på implementørens egen dom). Lov nr. 155 af 2013, den oprindelige hjemmel, ophæves 1. januar 2027 ved produktlovens § 40, som BEK nr. 959 af 2026 sætter i kraft den dag. Klagekanterne fra Miljø- og Fødevareklagenævnet og Styrelsen for Patientklager til Udbetaling Danmark er sænket til sandsynlig, fordi lov om Udbetaling Danmark § 4 a ikke selv angiver ruten. Af de 12 åbne klagepar fra 2026-11-21 er 7 lagt ind som sandsynlig, efter at to uafhængige dommere har læst hver påstand (`raw/populate/2026-11-23-jga143.domme.json`; én forskrift, der selv angiver ruten, er nok til sandsynlig), og 5 står åbne med grunden i registry'ets hul om klage- og tilsynskanter: Konkurrenceankenævnet over Konkurrencerådet og Forbrugerklagenævnet over Konkurrence- og Forbrugerstyrelsen blev lagt ind og fjernet igen efter review samme dag (den første hviler kun på nævnets egen bekendtgørelse med "i det omfang det er fastsat i konkurrenceloven", en kendt fejlklasse; den anden på forbrugerklageloven som udstedt, uden at ændringslovene er læst, og BEK nr. 65 af 2019 nævner Nævnenes Hus, så den afgørende myndighed er sandsynligvis forkert), Teleklagenævnet over Klimadatastyrelsen (hvilken styrelse der træffer afgørelserne efter radioudstyrsloven i dag, er ikke fundet) og Energiklagenævnet over Erhvervsministeriet og over Beskæftigelses- og Ligestillingsministeriet (beføjelserne udøves af Erhvervsstyrelsen og Arbejdstilsynet, BEK nr. 1525 af 2025 § 1 og BEK nr. 1354 af 2019 § 2). `intermediate/corpus/retsinformation_sitemap.jsonl` er Retsinformations sitemap som fortegnelse over alle 198.589 dokumenter (adresse og ændringsdato), skrevet af `populate.py sitemap`. `pipeline/corpus/eksport.py` (2026-11-12) henter Retsinformations søgeeksport til `intermediate/corpus/eksport/` og fører kataloget ajour derfra: status, de dokumenter bulk-høsten manglede, `hjemmel_for`-kanter og ministerium fra Retsinformations ressortfelt (se afsnittet om søgeeksporten nedenfor). Samme dag er de øvrige samlinger lagt i kataloget som `katalog/retsinformation_<samling>.jsonl` og koblet til lovgivningen via eksportens hjemmelsfelt, og lovforslagene i Folketingstidende er koblet til den lov, de blev til, på titel og underskriftsdato; `populate.py ajour` kobler nu også registry'ets vejledninger til deres katalogpost (journal `2026-11-12T2245-ajour.kontrol.json`). Orkestratorens egne rettelser efter ajourføringen ligger i `raw/populate/2026-11-12-retsinformation-vilkaar.*` (Civilstyrelsens vilkår og to adresser) og `raw/populate/2026-11-12-byggesagsgebyr.*`. Fra 2026-11-13 henter `pipeline/corpus/tekst.py` Retsinformations XML for et udsnit af kataloget til `intermediate/corpus/xml/` og skriver `katalog/tekst.jsonl` (se afsnittet om tekstlaget nedenfor); `eksport.py katalog` læser præamblerne derfra og lægger lovens bestemmelser på `hjemmel_for`-kanterne (`from_bestemmelse`). Samme dag er beskrivelsen af eksportens hjemmelsfelt rettet: feltet peger på den version af loven, Retsinformation fører dokumentet under, ikke på den version, dokumentet citerer. Filtabellen nederst beskriver den oprindelige pakke; git-historikken viser, hvad der er ændret siden.

## Indhold

| Mappe | Hvad |
|---|---|
| `dk-regulering/` | **Leverancen.** `registry.yaml` (sandheden: 615 noder, 1281 kanter, 216 huller), `README.md`, `datakilder.md`, `huller.md`, `diagrammer/` (Mermaid), `reguleringskort.html` (interaktivt kort, kan åbnes direkte i en browser), `scripts/build.py` (validering og views). |
| `dk-regulering/katalog/` | Katalog over Retsinformations dokumenter: `retsinformation_lta.jsonl` (hele Lovtidende A: 63515 dokumenter, 14101 gældende; status pr. 2026-11-12, for 2013, 2023, 2025 og 2026 pr. 2026-11-23), `retsinformation_retsinfo.jsonl`, `_mt`, `_ltb`, `_ltc`, `_fob` og `_ft` (de øvrige samlinger: 131080 cirkulærer, vejledninger, afgørelser, lovforslag m.m., kun metadata), `kanter.jsonl` (henviser_til, hjemmel_for, implementerer_EU, ressortansvar, udsteder), `eu_index.jsonl` (EU-retsakter med CELEX), `tekst.jsonl` (indeks over de dokumenter, hvis XML er hentet, med præambel, fodnoter, underskriftssted og EU-retsakter), `README.md` (genereret oversigt). |
| `dk-regulering/eval/` | Evalueringssæt for kæderne: `facit.jsonl` (302 dokumenter læst af annotatorer, hvert led med ordret citat), `instruks.md`, `rettelser.json`, `kontrol-2.json` til `kontrol-4.json`, stikprøven af klage- og tilsynskanter uden for de otte domæner (`stikproeve.jsonl`, `stikproeve-domme.jsonl`), stikprøven af bekræftede afløserpar (`afloeser-stikproeve.jsonl`, `afloeser-stikproeve-domme.jsonl`) og den genererede `README.md` med målingen. Se afsnittet nedenfor. |
| `dashboard/` | Data og side bag dækningsdashboardet (heatmap pr. retsområde, fremdrift, 69 mangler med status). |
| `audit/` | Opus-auditten (fire linser + syntese og dækningsmatrix), vurderingen af danskelove.dk og Jurabibliotek, stikprøvekontrollen af ressort-klassifikationen og kvalitetstal. |
| `intermediate/registry/` | Flettet og efterbehandlet registry som JSON (`final.json`), flettelog, proveniens (alle URL'er set i søgeresultater) og visualiseringsdata. |
| `intermediate/corpus/` | Udtræk fra de 62.762 seed-filer (`docs.jsonl`: metadata og tekstfeatures), opløste referencer og lovfamilier (`resolved.json`), DocumentId-præfikser, udstedende ministerium, ressort-klassifikationen og de batches, Haiku/Opus klassificerede. Efter pakningen: `retsinformation_sitemap.jsonl`, `eksport/` (metadata for alle Retsinformations samlinger, se nedenfor) og `xml/` (tekstlaget: Retsinformations XML for et udsnit af kataloget, se nedenfor). |
| `raw/workflows/` | Rå resultater fra alle 74 agent-workflows (én JSON-linje pr. agent med label og struktureret svar). |
| `pipeline/` | Al kode: fletning, verifikation, proveniensfilter, katalog, klassifikation, views, HTML og dashboard, plus workflow-scripts. Scriptsene forventer den oprindelige mappestruktur og workflow-stierne fra sessionen; brug dem som opskrift. |
| `harvest/` | Høster til Retsinformation (sitemap, XML, præambel/hjemmel, ministerium, EU-note), testet offline. Kræver adgang til www.retsinformation.dk og api.retsinformation.dk. |

## Retsinformations søgeeksport (`intermediate/corpus/eksport/`)

Hentet 2026-11-12 med `pipeline/corpus/eksport.py hent`: Retsinformations egen "Eksportér søgeresultat" (`api/documentsearch/csv`), ét kald pr. samling og årsinterval, 90 kald i alt med 10,5 sekunder imellem. Én JSON-linje pr. dokument med eksportens kolonner; tomme felter er udeladt. Kun metadata, ingen tekst. Filen `hentet` har den dato, eksporten blev hentet; kataloget daterer status og ressortfelt med den og ikke med den dag, det bygges. `eksport.py hent lta ÅR [TIL]` henter én samlings år (til og med TIL) igen med ét kald og fletter rækkerne ind med feltet `Hentet`; kataloget daterer de rækker med den dag. Begge datoer er den dag, `populate.get` hentede svaret (cachefilens tid), ikke den dag, kommandoen blev kørt: et svar fra cachen kan være op til syv dage gammelt, og `hentet` er den ældste af kaldenes datoer. 2026-11-23 (JGA-143) er Lovtidende A for 2013, 2023, 2025 og 2026 hentet igen (4 kald, alle hentet samme dag): 42 nye dokumenter, og 18 dokumenter gik fra gældende til historisk. Forbehold: en delvis hentning ajourfører kun de hentede år, så har en lov ingen tidslinje, kan en ældre version fra et andet år stå som gældende ved siden af den nyere, indtil dens år hentes igen; det er ikke rettet.

| Fil | Samling | Dokumenter | Ikke markeret historiske | År | Kun i sitemap | Kun i eksporten |
|---|---|---:|---:|---|---:|---:|
| `lta.jsonl` | Lovtidende A | 63.515 | 14.101 | 1852–2026 | 2 | 1.282 |
| `ltb.jsonl` | Lovtidende B | 45 | 7 | 1959–2026 | 0 | 0 |
| `ltc.jsonl` | Lovtidende C | 4.778 | 4.416 | 1936–2026 | 0 | 0 |
| `mt.jsonl` | Ministerialtidende | 6.421 | 1.080 | 1871–2012 | 3 | 379 |
| `retsinfo.jsonl` | Administrative forskrifter og afgørelser (cirkulærer, vejledninger, skrivelser, afgørelser, domme) | 75.237 | 39.868 | 1665–2026 | 7.671 | 2.031 |
| `ft.jsonl` | Folketingstidende (lovforslag, betænkninger, beslutningsforslag) | 41.730 | 41.730 | 1953–2026 | 34 | 0 |
| `fob.jsonl` | Folketingets Ombudsmand | 2.869 | 2.869 | 1980–2026 | 30 | 12 |

Kolonner: `DokumentType`, `Titel`, `PopulærTitel`, `Ressort` (Retsinformations ministeriefelt; føres ikke altid ajour ved ressortomlægninger), `AdministrerendeMyndighed`, `JournalNummer`, `Nummer`, `År`, `DokumentId`, `ACCN` (accessionsnummer), `Publiceringsmedie`, `GeografiskDækning`, `UnderskriftDato`, `BekendtgørelsesDato`, `PubliceretTidspunkt`, `SidstPubliceretTidspunkt`, `Historisk`, `HistoriskDato`, `HistoriskAarsagNote`, `HjemmelVedroerer` (accessionsnumre på den lovgivning, dokumentet vedrører), `SenereAendringer` og `ÆndrerI` (betegnelser som "BEK nr 1455 af 01/12/2025"), `Tiltræder`, `EliUrl` og noterne `RedaktionelNote`, `AnfoerINote`, `OmtryksNote`, `AlternativeMedierNote` og `UndtagetFraOffentliggørelse`. Datoer har formen ÅÅÅÅMMDD.

Forbehold:

- `Historisk` er Retsinformations markering og kan komme, før ophævelsen har virkning (BEK nr. 1170 af 14/11/2024 er markeret historisk 2026-11-04, men gælder til 1. januar 2027).
- `HjemmelVedroerer` peger på den version af loven, Retsinformation fører dokumentet under. For 53.592 af de 88.181 `hjemmel_for`-kanter er den udstedt senere end dokumentet selv, så den er ikke den version, dokumentet citerer. Den citerede version står kun på kanter til forskrifter i tekstlaget (`citeret_version`).
- `AdministrerendeMyndighed` er kun brugt for afgørelser, udtalelser og domme: de får en `udsteder`-kant fra den instans i registry'et, der har samme navn (et tidligere navn giver `sandsynlig`). Feltet føres ajour, så en ældre afgørelse kan stå under den myndighed, der har overtaget området (afgørelser fra 1983 står under Familieretshuset). For bekendtgørelser er feltet den myndighed, der administrerer reglerne, ikke nødvendigvis den, der har udstedt dem: blandt 200 hentede bekendtgørelser med feltet var underskriftsstedet et andet i 86.
- "Kun i sitemap" er adresser fra `retsinformation_sitemap.jsonl`, som eksporten ikke har. For den administrative samling er fem af de 7.671 prøvet, og alle gav 404; resten er ikke undersøgt.
- Alle samlinger er lagt i kataloget (`dk-regulering/katalog/retsinformation_<samling>.jsonl`). Uden for Lovtidende A er posterne skrevet direkte fra eksporten: ingen tekst, og kobling til lovgivningen kun, hvor `HjemmelVedroerer` er udfyldt og peger på et dokument i kataloget (64.485 af de 89.350 dokumenter uden for Folketingstidende). `hjemmel_for` går fra loven til forskrifter og vejledninger, `henviser_til` fra afgørelser, udtalelser og domme til loven. Ministerium og retsområde er kun sat for gældende dokumenter, når ressortfeltet med sikkerhed er aktuelt, eller der er en lov at arve fra. Folketingstidende har intet hjemmelsfelt: dér er dokumenter om samme lovforslag samlet på år, samling og nummer (feltet `lovforslag`), og den vedtagne tekst er koblet til loven (feltet `lov`), når netop én lov har samme titel og er underskrevet fra 3 dage før til 60 dage efter vedtagelsen (5.413 lovforslag).
- `klassifikation.json` er Haiku-svarene (177) for de nye katalogdokumenter, der hverken havde et aktuelt ressortfelt eller en hjemmelslov at arve fra; `klassifikation_job.json` er arbejdslisten og er tom, når alle er klassificeret.

## Tekstlaget (`intermediate/corpus/xml/`)

Hentet 2026-11-13 og 2026-11-14 med `pipeline/corpus/tekst.py hent`: dokumentets XML fra ELI-adressen plus `/xml`, ét kald pr. dokument gennem samme kø som de øvrige opslag (10,5 sekunder mellem kald, kun kl. 03:00-23:45). Filerne ligger som `xml/<samling>/<resten af katalog-id'et>.xml.gz`, fx `xml/lta/2019-1399.xml.gz` for `lta-2019-1399`, uændrede bortset fra gzip. `xml/hentet.jsonl` har én linje pr. forsøg (id, status, dato); svar fra de seneste syv dages opslag er genbrugt, så datoen kan være op til syv dage senere end selve kaldet.

Udsnittet er de dokumenter, registry'ets noder peger på, de gældende dokumenter i de otte domæner (retsområder med domæne i `katalog.SCOPE`) og, fra 2026-11-21, afløserkandidaternes lovtekster, de fleste ophævede. `tekst.py plan` viser, hvor langt hentningen er, og `katalog/README.md` tæller de hentede dokumenter pr. samling.

| Trin | Dokumenter | Hvad |
|---|---:|---|
| `registry` | 412 | Dokumenter, en registry-node peger på (`registry_ids`), uanset status |
| `afloeser` | 509 | Afløserkandidaternes lovtekster: de hovedlove, en historisk lov uden gældende version kan være afløst af (`eksport.kandidatplan`), bortset fra dem i `registry` |
| `uden-tekst` | 751 | Gældende dokumenter i Lovtidende A uden tekst i bulk-høsten |
| `vejledning` | 599 | Gældende vejledninger, cirkulærer og andre dokumenter uden for Lovtidende A, der ikke er praksis |
| `lovforslag` | 198 | Lovforslag som fremsat til de gældende love i udsnittet |
| `praksis` | 824 | Gældende afgørelser, udtalelser og domme |
| `med-tekst` | 1.179 | Gældende dokumenter i Lovtidende A med tekst i bulk-høsten (den tekst ligger ikke i dette repo) |

Tallene er fra `tekst.py plan` 2026-11-24. Hentet er alle undtagen 1 i `afloeser` (lta-2002-405, HTTP 500 fire gange); de sidste 48 i `praksis` er hentet 2026-11-24, alle kun med metadata.

`tekst.py indeks` skriver `dk-regulering/katalog/tekst.jsonl` med én linje pr. hentet dokument: `id`, `xml` (sti fra `legoleze/`), `hentet`, `n_tegn`, `n_paragraffer`, `praeambel` (indledningen uden fodnoter), `noter` (fodnoterne, herunder EU-noten), `naevner` (love og bekendtgørelser nævnt med nummer og dato: `{"katalog-id|dato": antal}`), `klage_tilsyn` (`[paragraf, sætning]` for sætninger med et klage- eller tilsynsudsagn), `underskrevet_af` (Meta-feltet `PlaceOfSignature`) og `eu` (CELEX-numre fra Meta-feltet `EuReferences`). `tekst.py fuld` skriver hele teksten som JSON-linjer på stdout, én linje pr. paragraf (`id`, `paragraf` som den står i dokumentet, fx `§ 16 C`, og `tekst`); et dokument uden paragraffer er én linje med `paragraf` null. Bestemmelserne i en kants `from_bestemmelse` kan slås op dér i den citerede lovversion. Filen ligger ikke i repo'et, fordi den er en ren funktion af XML-filerne.

Forbehold:

- XML-filen har ikke altid tekst. Af udsnittets 4.575 dokumenter (2026-11-24; 4.476 2026-11-23 og 3.871 før) har 1.571 kun metadata (`n_tegn` er 0): 1.395 af de 1.411 fra før 2005, 154 af de 388 fra 2005-2009, ingen af de 2.578 fra 2010 og frem og 22 af de 198 lovforslag. Tallene herunder er fra 2026-11-14. Af de 745 gældende dokumenter i Lovtidende A, bulk-høsten ikke havde tekst til, har XML-filen tekst for 348; af vejledninger og cirkulærer 268 af 598, af lovforslagene 176 af 198 og af afgørelser og udtalelser 493 af 738. Ét opslag på `api/pdf/<UniqueDocumentId>` for et sådant dokument gav 404; om teksten findes som PDF andetsteds, er ikke undersøgt.
- Teksten er dokumentet, som det blev udstedt. En bekendtgørelse, der senere er ændret, har ændringerne i egne dokumenter; kun lovbekendtgørelser er sammenskrevne.
- `praeambel` læses af `eksport.py katalog` med et regulært udtryk (se `praeambelhjemmel`). Bestemmelserne er dem, den citerede lovversion havde. Den nye tekst, en ændringsforskrift sætter ind i en anden forskrift (XML-elementet `AendringNyTekst`), er ikke med i `praeambel` og `noter` (fra 2026-11-24): en ny indledning eller titelfodnote til hovedforskriften blev før læst som ændringsforskriftens egen. Det fjernede 112 `hjemmel_for`-kanter (metode `praeambel`, 459 → 347) til 58 ændringsbekendtgørelser, der ikke har nogen indledning selv og nu står uden `hjemmel_for`-kant, og 90 `implementerer_EU`-kanter fra 26 ændringsforskrifter. Den nye indledning og fodnote er ikke ført over på hovedforskriften (JGA-202).
- `noter` er omsat til `implementerer_EU`-kanter (metode `fodnote`, 1.320 kanter; 1.411 før 2026-11-24, hvor ændringsforskrifternes indsatte fodnoter gik ud, og hvor en fodnote, der kun siger, at der er "henvist til visse bestemmelser" fra en forordning, holdt op med at give en kant: 1 kant, BEK nr. 1006 af 2026) og `naevner` til `henviser_til`-kanter for dokumenter uden tekst i bulk-høsten (metode `xml-tekst`, 6.498 kanter; kun når nummer og dato passer på et dokument i Lovtidende A). `eu` er ikke brugt: feltet fører alle EU-retsakter, dokumentet nævner. `underskrevet_af` er ikke omsat til `udsteder`-kanter.
- `klage_tilsyn` er omsat til `klageinstans`- og `tilsyn`-kanter fra instans til dokument for hoveddokumenter i Lovtidende A (metode `bestemmelse`, `sandsynlig`: 543 og 573 kanter; 542 og 573, før læseren fik navnet "Styrelsen for Danmarks Fængsler" (2026-11-24, efter review af JGA-198), 542 og 571 før 2026-11-24 og 483 og 512 før 2026-11-23), når sætningen navngiver en instans, der er en node i registry'et; ministerens titel ("miljøministeren") læses som ministeriet. Læste formuleringer står i `eksport.laeser` og i registry'ets `meta.metode`. `eksport.py unavngivne` lister de navne, læseren ikke fandt en node til; fortegnelsen fra 2026-11-16 med en dom pr. navn står i `raw/populate/2026-11-16-unavngivne.tsv`. Kanten gengiver teksten, som dokumentet er udstedt. Er dokumentet ændret siden, står ændringslovene, underskrevet efter det, i `senere_aendret_ved` (for love fra `intermediate/corpus/tidslinjer.jsonl`, for bekendtgørelser fra eksportens felt `SenereAendringer`): 448 kanter; hvad ændringerne flyttede, er ikke læst. Er dokumentet ikke gældende efter katalogets status, har kanten feltet `dokumentstatus` med dokumentets status (i dag altid `historisk`): 101 af de 1.116 kanter (fra 2026-11-24, JGA-199). `build.py` kræver feltet på netop de kanter og afviser andre værdier end `historisk`. Feltet viser dokumentets status pr. katalogets statusdato (`status.pr` på dokumentet), ikke den dag, en bestemmelse holdt op med at gælde; en søgning efter gældende ret kan frasortere kanterne på feltet alene.
- Indekset er kørt igen 2026-11-23 (JGA-144) for de lovtekster, der var hentet til afløserkandidaterne: 4.476 rækker (605 nye, 15 ændret af den nuværende læser). Kun 125 af de nye har tekst (78 ophævede hovedlove, 46 gældende og 1 ophævelseslov). Det gav 59 klageinstans- og 59 tilsyn-kanter mere (93 af de 118 på love, der ikke længere gælder), 110 `implementerer_EU`-kanter fra fodnoter (23 ældre samforekomst-kanter fjernet, fordi fodnoten nu er læst) og 14 `henviser_til`-kanter fra teksten. Kanter fra en ophævet lovs bestemmelser er beholdt: de gengiver loven, som den var, og er fra 2026-11-24 (JGA-199) mærket med `dokumentstatus` (se ovenfor). Evalueringen er uændret: `eval/README.md` er byte for byte den samme før og efter, og kontrolfilerne er ikke rørt. Indekseringen ventedes at flytte evalueringens tal, fordi den gav nye klage-, tilsyns-, EU- og henvisningskanter; det holdt ikke: ingen runde er trukket blandt de nye tekster, og ingen af de nye kanter starter eller ender i et dokument i facit (de 10 målte henvisninger fra vejledninger til nye tekster fandtes før og afhænger kun af vejledningens egen tekst), så alle runder gav de samme tal før og efter.
- 2026-11-24 (JGA-198) er teksten til de tre nye versioner fra JGA-143 hentet og indekseret, alle med tekst: BEK nr. 1002 af 2026 (asbest, afløser BEK nr. 1328 af 2025), BEK nr. 1003 af 2026 (bygherrens pligter, afløser BEK nr. 117 af 2013) og LBK nr. 982 af 2026 (straffuldbyrdelsesloven, afløser LBK nr. 201 af 2023). De gamle versioners kanter er uændrede, bortset fra at klage- og tilsynskanterne på LBK nr. 201 af 2023 nu har `dokumentstatus`. De nye versioner fik hver en `henviser_til`-kant til den gamle version og til de love, teksten nævner (2, 2 og 39), en `implementerer_EU`-kant fra fodnoten for de to bekendtgørelser (direktiv 2009/148/EF og 92/57/EØF) og bestemmelser i `from_bestemmelse` på `hjemmel_for`-kanten fra arbejdsmiljøloven (LBK nr. 442 af 2026). LBK nr. 982 af 2026 fik tilsyn-kanten fra Danmarks Fængsler (§§ 78 d og 103, hvor § 78 d er den kendte fejlklasse tilsyn med den dømte) og, efter review samme dag, klageinstans-kanten fra § 111: den gamle version siger "Direktoratet for Kriminalforsorgen", som læseren kender som tidligere navn, mens den nye siger "Styrelsen for Danmarks Fængsler", som læseren først fandt, da navnet kom i `eksport.ALIAS` (nodens navn er "Danmarks Fængsler (Styrelsen for Danmarks Fængsler)", og `myndigheder()` tager ikke teksten i en parentes med). Aliaset gav ingen andre kanter. 49 af de 51 instansnoder med et navn på formen "X (Y)" har stadig et Y, læseren ikke kender; de fleste er forkortelser eller præciseringer, men omkring seks er rigtige alternative navne (se hullet om klage- og tilsynskanter i registry'et). lta-2002-405 gav HTTP 500 for tredje gang og står som `ukendt` i `xml/hentet.jsonl`; næste `tekst.py hent` prøver den igen. Hentningen gik videre end opgaven: 48 dokumenter fra de senere trin blev også hentet (8 fra `uden-tekst`, 1 fra `vejledning` og 39 af 87 fra `praksis`; 39 af de 48 har kun metadata), så `praksis` har 48 dokumenter tilbage at hente. Indekset gik fra 4.476 til 4.527 rækker. De 48 gav 23 `henviser_til`-kanter fra teksten, 7 `implementerer_EU`-kanter fra fodnoter, 5 `hjemmel_for`-kanter fra præamblen, bestemmelser på 7 `hjemmel_for`-kanter fra hjemmelsfeltet og 1 tilsyn-kant (Energistyrelsen over BEK nr. 1006 af 2026 § 15), alle fra de 8 bekendtgørelser i Lovtidende A; praksisdokumenterne og vejledningen gav ingen kanter. Evalueringen er uændret: `eval/README.md` er byte for byte den samme, fordi ingen af de ændrede kanter starter i et dokument i facit (facit har de gamle versioner af de to bekendtgørelser, ikke de nye).
- De ældre `implementerer_EU`-kanter fra bulk-teksten (metode `tekst-samforekomst`) er fjernet for dokumenter med hentet tekst (115) og sat til `ukendt` for resten (1.164).
- Uden for udsnittet er der stadig kun metadata.

## Lovenes tidslinjer (`intermediate/corpus/tidslinjer.jsonl`)

Hentet fra 2026-11-15 med `pipeline/corpus/tekst.py tidslinjer`: Retsinformations tidslinje for en lov (`api/document/<UniqueDocumentId>/timeline`), ét kald pr. lov gennem samme kø som de øvrige opslag. Tidslinjen er den samme for alle versioner af en lov, så en version, der står i en hentet tidslinje, hentes ikke selv. Hver linje har `id` (det dokument, kaldet blev gjort for), `status`, `hentet` og `tidslinje` med fem af Retsinformations felter pr. dokument: `href`, `documentTypeId` (10 hovedlov, 20 ændringslov, 30 lovbekendtgørelse), `isMainLaw`, `isHistoric` og `signatureDate`.

`eksport.py katalog` samler lovens egne versioner (lovbekendtgørelserne og den hovedlov, der har `isMainLaw`) til én familie og sætter `gaeldende_version` efter den, med `familie_metode: tidslinje` på katalogposten. Hentet er 1.408 tidslinjer: alle love med en gældende version (4.435 love og lovbekendtgørelser). Fra 2026-11-23 bliver en gældende version med samme titel, nyere end tidslinjen og ikke i nogen tidslinje (en lovbekendtgørelse udstedt efter at tidslinjen blev hentet), tidslinjens gældende version, men kun når ingen af tidslinjens egne versioner er gældende; ellers kunne en ny lov med en titel, mange love deler (88 gældende love hedder "Lov om indfødsrets meddelelse"), overtage alle deres tidslinjer. Reglen flyttede straffuldbyrdelsesloven (LBK nr. 201 af 2023 → LBK nr. 982 af 2026, 9 dokumenter). Selskabsskatteloven (LBK nr. 279 af 2025 → LBK nr. 984 af 2026, 34) og STU-loven (LBK nr. 1077 af 2023 → LBK nr. 983 af 2026, 5) flyttede uden reglen: deres hentede tidslinjer har allerede den nye lovbekendtgørelse, som kom i kataloget med hentningen 2026-11-23. De 3.125 historiske love og lovbekendtgørelser uden gældende version er ikke hentet og samles som før på titlen. Ændringslovene i tidslinjen er ikke brugt. En lov, der er afløst af en ny hovedlov, har sin egen tidslinje; den kobles til afløseren som beskrevet herunder.

Afløseren (fra 2026-11-21, JGA-139): en historisk lov eller lovbekendtgørelse uden gældende version får feltet `afloeser`, når en hovedlov står i dens liste over senere ændringer (eksportens `SenereAendringer`), selv nævner den i sin liste over love, den ændrer (`ÆndrerI`), og i sin hentede tekst har en ophævelsesbestemmelse, der nævner den med nummer og dato. Feltet har bestemmelsen ordret (`ophaevelse`, `paragraf`, `paragraf_tekst`), `bevarer_regler` (sætningen om, at regler efter den gamle lov forbliver i kraft, ellers null), kilde og `sikkerhed: verificeret`. Familien følger afløserens gældende version: `gaeldende_version` og `afloeser_fra` (den afløste families nyeste version) på den gamle lovs versioner og på deres `hjemmel_for`-kanter. Kandidatlovenes tekst hentes af `tekst.py hent` (trinnet `afloeser`). `raw/populate/2026-11-21-afloeser-oprydning.tsv` er de læste par, hvor afløseren kun rydder en forældet lov op (gammel, afløser, grund); familien fortsætter ikke til dem, og en ren ophævelseslov ("Lov om ophævelse af ...") afvises i koden. Stand 2026-11-23 (JGA-144): 918 love med kandidater; 126 peger på en afløser (45 med en bestemmelse om, at reglerne forbliver i kraft), 10 oprydning, 46 afvist af bestemmelsesreglerne, 4 med en kandidat, hvis tekst ikke er hentet, og 732 med kun kandidater, hvis XML er uden tekst (mest love fra før 2005), som metoden ikke kan bekræfte. De 171 kandidatlove, der blev hentet 2026-11-23 (508 af 509 er nu hentet), har alle kun metadata, så ingen ny afløser er bekræftet, og der var ingen nye par at læse for oprydning; de 251 love, der gik fra "ikke hentet" (255) til "uden tekst" (481 → 732), er netop dem. De 4 tilbage: lta-1992-396 og lta-2001-967 venter på lta-2002-405, som gav HTTP 500 tre gange (2026-11-21, -23 og -24) og prøves igen af næste `tekst.py hent`; lta-1989-583 og lta-1992-251 hentes ikke, fordi de allerede har en gældende version gennem et nyere familiemedlem (`kandidatplan` springer dem over), men tæller med, fordi kandidaterne tælles, før afløserne fører familierne videre. 344 katalogdokumenter følger afløserens gældende version. Præcision i stikprøven herunder: 90 %. Hentningen genoptages mellem 03:00 og 23:40 dansk tid fra `legoleze/` med `S=$(( $(TZ=Europe/Copenhagen date -d 23:40 +%s) - $(date +%s) )) && timeout ${S}s env UV_CACHE_DIR=$TMPDIR/uv-cache uv run -q --offline --no-project --with pyyaml==6.0.3 python pipeline/corpus/tekst.py hent $(( S / 60 - 1 ))` (værten `www.retsinformation.dk` tilladt), derefter `eksport.py katalog`, `eval.py saml` og `maal`, `views.sh` og `build.py --check`. Nye bekræftelser efter en senere hentning skal læses for oprydning.

## Evalueringssæt (`dk-regulering/eval/`)

Lavet 2026-11-15 med `pipeline/corpus/eval.py`. `udtag` trækker pr. domæne et antal gældende danske dokumenter med hentet tekst (hovedbekendtgørelser med og uden registry-node og vejledninger) og skriver én opgave pr. dokument i `intermediate/eval/opgaver/`: indledning, fodnoter og de paragraffer, der nævner klage eller tilsyn; for vejledninger tekstens første 10.000 tegn. Annotatorerne (Haiku, 20 hold) fik kun opgaven og `instruks.md` og skrev svarene i `raw/eval/svar-*.json`. `saml` beholder de led, hvis citat står ordret i opgaven, og skriver `facit.jsonl`; `maal` måler kataloget og registry'et mod det og skriver `README.md` og `intermediate/eval/afvigelser.jsonl`.

| Runde | Dokumenter | Brug |
|---|---:|---|
| 1 | 118 | Udvikling: afvigelserne er gennemgået, og udtrækkene rettet efter dem |
| 2 | 71 | Kontrol: trukket efter rettelserne; første måling i `kontrol-2.json` |
| 3 | 64 | Kontrol af klage og tilsyn pr. forskrift: love og lovbekendtgørelser i stedet for vejledninger, trukket efter at læseren var skrevet; første måling i `kontrol-3.json` |
| 4 | 49 | Kontrol af klage og tilsyn pr. forskrift: samme grupper som runde 3, trukket efter at læseren var rettet efter runde 1-3; første måling i `kontrol-4.json` var den uafhængige; læseren er rettet efter runden 2026-11-21 |

Stikprøve uden for de otte domæner (2026-11-21, JGA-137): `eval.py stikproeve` trækker med frø 20261121 100 klageinstans- og 100 tilsyn-kanter fra dokumenternes egne bestemmelser (metode `bestemmelse`) i dokumenter uden for de otte domæner og skriver `stikproeve.jsonl`: ét led pr. kant med dokumentet, myndigheden, den afgørende myndighed, sætningen og bestemmelsernes fulde tekst. Filen skrives kun, når den mangler. `stikproeve-domme.jsonl` har samme id pr. led: uafhængige dommeres dom (`right`, `wrong`, `cannot-tell`), den sætning, dommen hviler på, grunden og dommen over den afgørende myndighed, uændret, og for de forkerte, de uafgjorte og dem med forkert afgørende myndighed et felt `gennemsyn` med gennemsynets dom, grund og fejlklasse (10 domme ændret). `maal` skriver præcisionen pr. kanttype, fejlklasserne og tallet efter rettelserne i `README.md`: klageinstans 81 % (80 rigtige, 19 forkerte, 1 kan ikke afgøres), afgørende myndighed 39 af 40, tilsyn 92 % (92 rigtige, 8 forkerte), målt før rettelserne.

Stikprøve af afløserparrene (2026-11-21, JGA-139): `afloeser-stikproeve.jsonl` er 40 af de første 137 bekræftede par (`random.seed(20261121)`, trukket af et engangsskript fra `afloeser`-felterne i `katalog/retsinformation_lta.jsonl`, før rettelserne): id, gammel og afløser (type, nummer, dato, titel, id), ophævelsesbestemmelsen ordret, paragraffen og dens fulde tekst, `bevarer_regler` og kilden. `afloeser-stikproeve-domme.jsonl` har samme id: uafhængige dommeres dom (`right`, `partial`, `wrong`), art (`replacement` eller `clean-up`) og grund, uændret, og et felt `gennemsyn` på de 4 delvise og de 4 oprydninger. Dommerne: 36 rigtige og 4 delvise (90 %), ingen forkerte; 36 afløsninger og 4 oprydninger. Gennemsynet er uenigt i de 4 delvise: loven ophæves helt, og "de hidtil gældende regler" for gamle aftaler, tilladelser og planperioder er overgangsregler, ikke en delvis ophævelse. Som afløser for lovfamilien er 36 af 40 rigtige (90 %); de 4 oprydninger står nu i oprydningslisten. Målingen af `hjemmel_for` efter afløseren: runde 3 54 rigtige og 1 forkert (før 53 og 2; kun Retsinformations felt 45 og 1, før 44 og 2), runde 1, 2 og 4 uændrede; bekendtgørelsen om personlige værnemidler (lov nr. 155 af 2013) tæller nu rigtigt.

Kontrolrundens første måling: `hjemmel_for` 96 % præcision og 100 % genfinding (kun Retsinformations felt: 84 % genfinding), paragrafnumre 274 af 275, `implementerer_EU` 90 % og 96 %, vejledningers henvisninger 45 af 45. Før rettelserne fandt kataloget i runde 1 én af 38 gennemførte EU-retsakter og 11 % af vejledningernes henvisninger.

Forbehold:

- Annotatoren er en sprogmodel. Kontrollen er mekanisk (citat, nummer, år og paragraf står i teksten); kun afvigelserne er læst efter.
- Tre dokumenter i facit er rettet efter gennemsyn (`rettelser.json` med begrundelse). Efter kontrolrunden er der rettet én fejl i læsningen af fodnoter ("EU-tidende" med lille t) og fjernet ældre EU-kanter; den nuværende stand står ved siden af første måling i `README.md`.
- De tilbageværende forkerte `hjemmel_for`-kanter er to fejl i Retsinformations hjemmelsfelt og tre kanter til den gældende version af en lov, kataloget ikke kobler til den citerede version.
- Klage og tilsyn pr. forskrift (katalogets kanter med metode `bestemmelse`) er målt uafhængigt i runde 4 (første måling 2026-11-21): klageinstans 16 rigtige, 4 forkerte, 2 manglende; afgørende myndighed 11 rigtige, 1 forkert, 7 manglende; tilsyn 20 rigtige, 1 forkert, 6 manglende. 3 af de 4 forkerte klageinstanser står i teksten, men mangler i facit. Runde 3's første måling var klageinstans 23 rigtige, 1 forkert, ingen manglende og tilsyn 15 rigtige, ingen forkerte, 11 manglende. Læseren er rettet til efter afvigelserne i runde 1-3 og, 2026-11-21, efter runde 4 og stikprøven, så alle fire runders og stikprøvens nuværende tal for de mål er til den pæne side.
- "Klagekant mellem de to noder" (registry'ets klageinstans-kanter mellem myndighederne) er målt igen 2026-11-21, efter at 11 kanter fra klageparrene var lagt ind (`raw/populate/2026-11-21-klagepar.*`, dom pr. par i `.tsv`): runde 1 13 af 16, runde 2 7 af 11, runde 3 15 af 20, runde 4 17 af 20 (før 13 af 16, 6 af 11, 11 af 20, 14 af 20), ingen forkerte. Første målinger i `kontrol-2.json` til `kontrol-4.json` er uændrede (6 af 10, 10 af 15, 14 af 20). Kanterne er lagt ind efter katalogets par, så de nye tal er til den pæne side. De 7 klagekanter fra JGA-143 (2026-11-23) ændrer ikke tallene.
- Seks dokumenter i facit er nu rettet efter gennemsyn (tre i første omgang, tre klage- og tilsynsled 2026-11-15).
- Udtaget er de otte domæner og dokumenter fra 2010 og frem. Praksis, lovforslag og de 34 øvrige retsområder er ikke med.

## Ikke med

- Bulk-høstens 62.762 seed-filer (ca. 1,7 GB): hent dem fra github.com/Ansvar-Systems/danish-law-mcp (commit da22657b7aa604e0a900d69b2b60a7b0c424b0cb, `data/seed/`).
- Fuld lovtekst uden for tekstlagets udsnit: kataloget har metadata og krydsreferencer; teksten ligger i seed-filerne eller hentes med `pipeline/corpus/tekst.py` (katalogstyret) eller `harvest/` (hele sitemappet).
- Sessionens samtale- og agent-transskripter.

## Licens og kilder

- Love, bekendtgørelser og andre offentlige aktstykker er ikke genstand for ophavsret (ophavsretslovens § 9). Bulk-høsten er Apache-2.0 (kode) og "DK-Statutory-PD" (data).
- Registry'ets påstande har egne kilder (URL'er set i søgeresultater) og sikkerhed (verificeret/sandsynlig/ukendt) pr. felt og kant.
- Katalog-kilderne er datasættets egne Retsinformation-URL'er.

## Filer i den oprindelige pakke (251)

| Fil | Bytes | SHA-256 |
|---|---:|---|
| `dk-regulering/README.md` | 21.449 | `b4139b82bfb318b3…` |
| `dk-regulering/datakilder.md` | 186.375 | `b2d1d91ee1bff56d…` |
| `dk-regulering/diagrammer/min-beskaeftigelse-og-ligestilling.md` | 18.168 | `05576c56299dc33e…` |
| `dk-regulering/diagrammer/min-boern-aeldre-og-bolig.md` | 24.850 | `add1026b9b260c2a…` |
| `dk-regulering/diagrammer/min-by-land-og-kirke.md` | 2.855 | `136ef9a8058137cc…` |
| `dk-regulering/diagrammer/min-by-land-og-transport.md` | 14.085 | `a0247c500eacfce1…` |
| `dk-regulering/diagrammer/min-erhverv.md` | 26.694 | `46ea11fac3573979…` |
| `dk-regulering/diagrammer/min-finans.md` | 804 | `63ca0ec13efaa969…` |
| `dk-regulering/diagrammer/min-forskning-uddannelse-og-digitalisering.md` | 2.086 | `9cd171f252ccdd38…` |
| `dk-regulering/diagrammer/min-forsvar.md` | 6.174 | `b85642a59cca7e55…` |
| `dk-regulering/diagrammer/min-groen-trepart.md` | 2.353 | `f15648d1de95fe18…` |
| `dk-regulering/diagrammer/min-indenrigs-og-bolig.md` | 1.854 | `7db0dbc65b938afd…` |
| `dk-regulering/diagrammer/min-justits.md` | 7.346 | `7809c2b321250208…` |
| `dk-regulering/diagrammer/min-klima-energi-og-forsyning.md` | 29.930 | `01153fa3797b1078…` |
| `dk-regulering/diagrammer/min-kultur.md` | 4.341 | `58a5a9f60fa08c43…` |
| `dk-regulering/diagrammer/min-miljoe-og-ligestilling.md` | 5.263 | `6c588c913b57677f…` |
| `dk-regulering/diagrammer/min-miljoe.md` | 21.933 | `97cf0886959ac8b9…` |
| `dk-regulering/diagrammer/min-natur-og-dyrevelfaerd.md` | 12.032 | `513f418209c5ad89…` |
| `dk-regulering/diagrammer/min-oekonomi-og-indenrigs.md` | 2.707 | `cb88a1f76ceb0d6c…` |
| `dk-regulering/diagrammer/min-samfundssikkerhed-og-beredskab.md` | 8.354 | `118dd1a143202e25…` |
| `dk-regulering/diagrammer/min-skat-og-vaekst.md` | 1.458 | `2331c32fb6d3d603…` |
| `dk-regulering/diagrammer/min-social.md` | 9.023 | `00321f7997b72679…` |
| `dk-regulering/diagrammer/min-statsministeriet.md` | 3.435 | `67cdb4388d85cc63…` |
| `dk-regulering/diagrammer/min-sundhed-og-kirke.md` | 838 | `ba1adc0c50d7ce81…` |
| `dk-regulering/diagrammer/min-udenrigs.md` | 810 | `21854252fd3f998a…` |
| `dk-regulering/diagrammer/min-udlaendinge-og-integration.md` | 868 | `b87568bfea0d302e…` |
| `dk-regulering/diagrammer/min-undervisning.md` | 824 | `16d9f55b1d6b5351…` |
| `dk-regulering/diagrammer/oversigt.md` | 13.025 | `931a16924b6d022a…` |
| `dk-regulering/huller.md` | 180.769 | `768fda0bfd7ead90…` |
| `dk-regulering/katalog/README.md` | 7.464 | `d9bc836abe8a8a5a…` |
| `dk-regulering/katalog/eu_index.jsonl` | 699.032 | `4f44c04f07e31b2d…` |
| `dk-regulering/katalog/kanter.jsonl` | 38.095.368 | `4dc55c92ee536db0…` |
| `dk-regulering/katalog/retsinformation_lta.jsonl` | 57.144.368 | `dc17a992f91881cf…` |
| `dk-regulering/registry.yaml` | 3.773.928 | `e314f95887924cd8…` |
| `dk-regulering/reguleringskort.html` | 6.675.912 | `7d4f7378241fe877…` |
| `dk-regulering/scripts/build.py` | 25.883 | `95ba48ff8c38232f…` |
| `dashboard/omraader.json` | 10.474 | `f266265c215f62da…` |
| `dashboard/maalt.json` | 26.881 | `3f8a6b7cddc8d9d8…` |
| `dashboard/vurderet.json` | 61.235 | `ae240a58998c1de1…` |
| `dashboard/fremdrift.json` | 1.505 | `0d9b21db31f38c6a…` |
| `dashboard/mangler.json` | 102.103 | `7af2f933826de1bd…` |
| `dashboard/index.html` | 30.183 | `b56a0a220ad5d7ba…` |
| `audit/audit_raw.json` | 418.631 | `b37ad1e7ca3e0db1…` |
| `audit/indeks_raw.json` | 98.995 | `f8a882fb6b52036b…` |
| `audit/ressort_quality.json` | 254 | `63d6e4975a01b392…` |
| `audit/coverage.json` | 30.226 | `9e194a3043fde9bb…` |
| `audit/provenance_stats.json` | 65 | `2a4119e015d4b82a…` |
| `audit/opus_sample.json` | 84.492 | `a13116ac3a8d2d06…` |
| `intermediate/registry/final.json` | 4.356.706 | `a3f6421e9067ba71…` |
| `intermediate/registry/merged.json` | 2.079.211 | `de5edae695874801…` |
| `intermediate/registry/merge_report.json` | 351 | `1893ee09de7e8391…` |
| `intermediate/registry/seen_urls.json` | 2.126.602 | `c7393eb0c9520c55…` |
| `intermediate/registry/alias.json` | 1.069 | `39e19dd9d0e66cb9…` |
| `intermediate/registry/disputed_decisions.json` | 1.678 | `67901926cfc17ec9…` |
| `intermediate/registry/url_fixes.json` | 485 | `fd37d9d6cc312473…` |
| `intermediate/registry/replacement_edges.json` | 2.273 | `78e80557bf1c165d…` |
| `intermediate/registry/v3_removed_edges.json` | 9.866 | `8ea22564aa0e2678…` |
| `intermediate/registry/viz_data.json` | 3.521.362 | `39af0e4f1af247fe…` |
| `intermediate/registry/viz_kat.json` | 3.030.418 | `41a8cb7e33fd30a1…` |
| `intermediate/registry/viz_pos.json` | 21.015 | `6cbafe5b55f23e9d…` |
| `intermediate/corpus/docs.jsonl` | 63.970.720 | `9f7f43195832b2da…` |
| `intermediate/corpus/resolved.json` | 76.374.201 | `ff28c4cba16aee7c…` |
| `intermediate/corpus/prefixes.json` | 146.185 | `b6e3f594cd262dbf…` |
| `intermediate/corpus/udsteder.json` | 7.995.746 | `a602639f46e74323…` |
| `intermediate/corpus/ressort.json` | 1.096.625 | `cced24fb4149dec0…` |
| `intermediate/corpus/jobs/guide.md` | 11.632 | `aacf1af561ce7ade…` |
| `intermediate/corpus/jobs/guide_v2.md` | 12.374 | `bed82b1160dba681…` |
| `intermediate/corpus/jobs/recheck/batch_00.jsonl` | 53.631 | `3f359bea650ba1e8…` |
| `intermediate/corpus/jobs/recheck/batch_01.jsonl` | 54.589 | `8920d7e8cb5d994d…` |
| `intermediate/corpus/jobs/recheck/batch_02.jsonl` | 52.700 | `ee516d98a0a8e4d0…` |
| `intermediate/corpus/jobs/recheck/batch_03.jsonl` | 54.906 | `07ff91c23e3598a8…` |
| `intermediate/corpus/jobs/recheck/batch_04.jsonl` | 57.733 | `0a828b33a9c4ef67…` |
| `intermediate/corpus/jobs/recheck/batch_05.jsonl` | 50.318 | `f1df392e6858491f…` |
| `intermediate/corpus/jobs/recheck/batch_06.jsonl` | 47.328 | `c27582226539b64d…` |
| `intermediate/corpus/jobs/recheck/batch_07.jsonl` | 1.263 | `9272d9be6e9a61eb…` |
| `intermediate/corpus/jobs/ressort/batch_000.jsonl` | 63.022 | `506842db725596a0…` |
| `intermediate/corpus/jobs/ressort/batch_001.jsonl` | 62.944 | `f49fe6a7e2e9074e…` |
| `intermediate/corpus/jobs/ressort/batch_002.jsonl` | 59.677 | `1ad152b02a3951b0…` |
| `intermediate/corpus/jobs/ressort/batch_003.jsonl` | 64.698 | `af3321687cd7e2f2…` |
| `intermediate/corpus/jobs/ressort/batch_004.jsonl` | 57.246 | `8c74b49fdde28cda…` |
| `intermediate/corpus/jobs/ressort/batch_005.jsonl` | 64.603 | `9fd5643f05e57a47…` |
| `intermediate/corpus/jobs/ressort/batch_006.jsonl` | 59.437 | `a8ac90c53922ffec…` |
| `intermediate/corpus/jobs/ressort/batch_007.jsonl` | 63.433 | `9f630903dae049bc…` |
| `intermediate/corpus/jobs/ressort/batch_008.jsonl` | 70.704 | `4024041c2f7f50ed…` |
| `intermediate/corpus/jobs/ressort/batch_009.jsonl` | 58.645 | `70613068f9279859…` |
| `intermediate/corpus/jobs/ressort/batch_010.jsonl` | 59.161 | `05f2a1e00592d437…` |
| `intermediate/corpus/jobs/ressort/batch_011.jsonl` | 55.974 | `ea798074f6147b9f…` |
| `intermediate/corpus/jobs/ressort/batch_012.jsonl` | 68.781 | `842b433bd52b41ea…` |
| `intermediate/corpus/jobs/ressort/batch_013.jsonl` | 61.500 | `b8fc235eaf2d90b4…` |
| `intermediate/corpus/jobs/ressort/batch_014.jsonl` | 60.796 | `9891dbd15ccadc30…` |
| `intermediate/corpus/jobs/ressort/batch_015.jsonl` | 59.426 | `325266b26bfc9f78…` |
| `intermediate/corpus/jobs/ressort/batch_016.jsonl` | 57.155 | `9512e14cdedbff86…` |
| `intermediate/corpus/jobs/ressort/batch_017.jsonl` | 58.935 | `51e697e6a6ae38dc…` |
| `intermediate/corpus/jobs/ressort/batch_018.jsonl` | 60.354 | `26111fd1e4fe18de…` |
| `intermediate/corpus/jobs/ressort/batch_019.jsonl` | 60.781 | `632997156d59dc7f…` |
| `intermediate/corpus/jobs/ressort/batch_020.jsonl` | 60.318 | `62b3aa9af4968eed…` |
| `intermediate/corpus/jobs/ressort/batch_021.jsonl` | 63.773 | `62daa4c5108e38ce…` |
| `intermediate/corpus/jobs/ressort/batch_022.jsonl` | 60.137 | `8fdb804ea6fe3172…` |
| `intermediate/corpus/jobs/ressort/batch_023.jsonl` | 60.205 | `590c54b76f14d2b2…` |
| `intermediate/corpus/jobs/ressort/batch_024.jsonl` | 57.176 | `7e527e6da1a2207d…` |
| `intermediate/corpus/jobs/ressort/batch_025.jsonl` | 57.681 | `5db696a8dd3be4ea…` |
| `intermediate/corpus/jobs/ressort/batch_026.jsonl` | 63.206 | `a5c6001ba551b22a…` |
| `intermediate/corpus/jobs/ressort/batch_027.jsonl` | 61.878 | `0513c6cff8e6518b…` |
| `intermediate/corpus/jobs/ressort/batch_028.jsonl` | 60.002 | `238de85625d7b2ed…` |
| `intermediate/corpus/jobs/ressort/batch_029.jsonl` | 61.603 | `bdcf2795ff757555…` |
| `intermediate/corpus/jobs/ressort/batch_030.jsonl` | 63.126 | `14ba9fa1dd72cf14…` |
| `intermediate/corpus/jobs/ressort/batch_031.jsonl` | 65.521 | `fb06225aa02c5032…` |
| `intermediate/corpus/jobs/ressort/batch_032.jsonl` | 59.595 | `a522991d85b78672…` |
| `intermediate/corpus/jobs/ressort/batch_033.jsonl` | 78.595 | `9ffb55a96e70d86a…` |
| `intermediate/corpus/jobs/ressort/batch_034.jsonl` | 55.660 | `cb4d22138005fbaa…` |
| `intermediate/corpus/jobs/ressort/batch_035.jsonl` | 62.944 | `e248e0087d82997c…` |
| `intermediate/corpus/jobs/ressort/batch_036.jsonl` | 60.601 | `d6283f6fe3b5518e…` |
| `intermediate/corpus/jobs/ressort/batch_037.jsonl` | 53.669 | `209435734e488455…` |
| `intermediate/corpus/jobs/ressort/batch_038.jsonl` | 59.442 | `330e3b9474482adc…` |
| `intermediate/corpus/jobs/ressort/batch_039.jsonl` | 64.870 | `31df6d3cbf637693…` |
| `intermediate/corpus/jobs/ressort/batch_040.jsonl` | 63.162 | `e645eaa1ee989690…` |
| `intermediate/corpus/jobs/ressort/batch_041.jsonl` | 60.216 | `3c3c72b0cd9f64f5…` |
| `intermediate/corpus/jobs/ressort/batch_042.jsonl` | 59.527 | `5dbf169e78ca9186…` |
| `intermediate/corpus/jobs/ressort/batch_043.jsonl` | 49.880 | `97f952a267c314e9…` |
| `intermediate/corpus/jobs/ressort/batch_044.jsonl` | 51.431 | `c6db2933796c8b1e…` |
| `intermediate/corpus/jobs/ressort/batch_045.jsonl` | 51.573 | `8774fea185315819…` |
| `intermediate/corpus/jobs/ressort/batch_046.jsonl` | 52.353 | `cca65d995a22d4da…` |
| `intermediate/corpus/jobs/ressort/batch_047.jsonl` | 58.686 | `21936ab9c66de1b9…` |
| `intermediate/corpus/jobs/ressort/batch_048.jsonl` | 63.263 | `54f05d83a78e6296…` |
| `intermediate/corpus/jobs/ressort/batch_049.jsonl` | 22.652 | `0f2ccf8ef780397e…` |
| `intermediate/corpus/jobs/sample/batch_0.jsonl` | 59.400 | `188a0d997a493fbe…` |
| `intermediate/corpus/jobs/sample/batch_1.jsonl` | 59.743 | `8010c37d07892671…` |
| `raw/workflows/wf_071e657e-858.jsonl` | 57.429 | `ccf51ebc43a0878a…` |
| `raw/workflows/wf_0866a312-5c1.jsonl` | 321.475 | `90d05866c1a01f12…` |
| `raw/workflows/wf_0d909033-65f.jsonl` | 92.452 | `bbc4ebb8c5a49adb…` |
| `raw/workflows/wf_116f361d-6aa.jsonl` | 28.886 | `285b788e8e98fd5d…` |
| `raw/workflows/wf_12b74310-212.jsonl` | 85.244 | `341b44935679550a…` |
| `raw/workflows/wf_133ea027-108.jsonl` | 867.165 | `f135d607277ce3f1…` |
| `raw/workflows/wf_144a95b7-6d3.jsonl` | 55.354 | `c291aa418f644c99…` |
| `raw/workflows/wf_16760e0c-8ea.jsonl` | 106.355 | `398896c42d3b161c…` |
| `raw/workflows/wf_20880a47-533.jsonl` | 16.507 | `dccb1b6f481c34ef…` |
| `raw/workflows/wf_2248df8d-a25.jsonl` | 970.803 | `b1bc9fa071bf65bd…` |
| `raw/workflows/wf_233485d9-0e4.jsonl` | 35.622 | `bad53b30a19962f0…` |
| `raw/workflows/wf_24c49f2a-cd0.jsonl` | 59.984 | `feaef2a793783e2a…` |
| `raw/workflows/wf_2847a79c-11f.jsonl` | 379 | `56869d399d2db9eb…` |
| `raw/workflows/wf_2c421c8d-f7c.jsonl` | 1.354.188 | `1e4420fb4bea2928…` |
| `raw/workflows/wf_2cd4d0a5-651.jsonl` | 68.390 | `010d0ba886b8055b…` |
| `raw/workflows/wf_3efb8cfa-c2d.jsonl` | 26.275 | `e359cb840fd719a4…` |
| `raw/workflows/wf_43e0afa7-699.jsonl` | 24.767 | `83a627d7ccd9f5d8…` |
| `raw/workflows/wf_46b15121-712.jsonl` | 51.795 | `14e4e3798160a027…` |
| `raw/workflows/wf_4cf5d5c4-0a4.jsonl` | 239.869 | `2a0006c550d73e67…` |
| `raw/workflows/wf_5452dbf7-b7d.jsonl` | 57.247 | `c862b8367bf3ca9d…` |
| `raw/workflows/wf_58d625e0-657.jsonl` | 76.766 | `9fbb23c5f6e6d763…` |
| `raw/workflows/wf_5ed575c6-457.jsonl` | 54.066 | `5d69dd7bfda20d7a…` |
| `raw/workflows/wf_61558f7c-b7d.jsonl` | 60.130 | `ed00c9dbd3ac3ef5…` |
| `raw/workflows/wf_687a21b1-ac1.jsonl` | 59.474 | `fedf58ccd5a23471…` |
| `raw/workflows/wf_6b06f7d7-d45.jsonl` | 67.608 | `96cad4fa12933638…` |
| `raw/workflows/wf_6bf57053-453.jsonl` | 388.897 | `748811a011a3c768…` |
| `raw/workflows/wf_6e1b8b5a-004.jsonl` | 72.804 | `a22b22966e43bb74…` |
| `raw/workflows/wf_7152a576-cab.jsonl` | 176.416 | `e680f2eb583992f6…` |
| `raw/workflows/wf_73713aef-3b3.jsonl` | 54.289 | `0c6d143148e04b48…` |
| `raw/workflows/wf_73e8a5d5-f45.jsonl` | 28.391 | `9040c37436eeae90…` |
| `raw/workflows/wf_74a591a5-10a.jsonl` | 49.844 | `189e80d1007d8b06…` |
| `raw/workflows/wf_78cad09e-455.jsonl` | 28.745 | `4f0ed9ab284ff7ea…` |
| `raw/workflows/wf_7d5cca50-baf.jsonl` | 52.340 | `1bfe592320ddd299…` |
| `raw/workflows/wf_7d646885-824.jsonl` | 43.338 | `94472487a1fda419…` |
| `raw/workflows/wf_8072ff40-c0f.jsonl` | 61.280 | `4c2d3fc664a1a554…` |
| `raw/workflows/wf_8e00beb5-2c4.jsonl` | 64.689 | `a5f3c3305a7e9a98…` |
| `raw/workflows/wf_93567d18-f52.jsonl` | 61.224 | `9301cb49d09dc024…` |
| `raw/workflows/wf_95d8d56d-6b0.jsonl` | 52.738 | `e0786eeac3f3ce75…` |
| `raw/workflows/wf_97db13a1-7ae.jsonl` | 98.229 | `7c7254682e6307e5…` |
| `raw/workflows/wf_997f5d45-01d.jsonl` | 28.102 | `2ca8f73ed3827113…` |
| `raw/workflows/wf_9c177447-3f2.jsonl` | 97.645 | `159e2ee091ef64a5…` |
| `raw/workflows/wf_9c6c102c-2ed.jsonl` | 69.753 | `40d9584be3070cb7…` |
| `raw/workflows/wf_9cc23364-345.jsonl` | 90.878 | `a2fc4019f026951c…` |
| `raw/workflows/wf_9d49be1e-420.jsonl` | 55.517 | `5c20e6d91f8f20a7…` |
| `raw/workflows/wf_9eef439a-f19.jsonl` | 60.297 | `a04601b7a1ae2fc7…` |
| `raw/workflows/wf_a0be858b-ee2.jsonl` | 54.997 | `3396644604b69b4f…` |
| `raw/workflows/wf_a4fcd026-73d.jsonl` | 32.245 | `9614a89cc64480a2…` |
| `raw/workflows/wf_a5875277-6ec.jsonl` | 61.733 | `39a834f121ca9429…` |
| `raw/workflows/wf_a8e6c505-849.jsonl` | 56.411 | `de6c8155c18c2a78…` |
| `raw/workflows/wf_aee0ccb5-ba9.jsonl` | 60.463 | `4e97439ac8c374ee…` |
| `raw/workflows/wf_af25d1a3-de3.jsonl` | 47.716 | `a01641aab26ba597…` |
| `raw/workflows/wf_af816b50-b42.jsonl` | 44.257 | `9452ab47ecfaa0e6…` |
| `raw/workflows/wf_b03b4870-e49.jsonl` | 64.387 | `977ba55cb6531d9b…` |
| `raw/workflows/wf_b34e2e13-60d.jsonl` | 20.577 | `9d65333cc4cbe7e2…` |
| `raw/workflows/wf_b49d965c-43b.jsonl` | 70.431 | `2e332d72d67c07fe…` |
| `raw/workflows/wf_b500ac39-797.jsonl` | 90.954 | `af40583fc08d74c0…` |
| `raw/workflows/wf_b78aacd4-325.jsonl` | 150.199 | `f563c19b2243a6ee…` |
| `raw/workflows/wf_c25aa041-8b5.jsonl` | 31.155 | `f0954598d42b3fdf…` |
| `raw/workflows/wf_c5c4d4ae-d31.jsonl` | 366.356 | `f4dafe96f66c91be…` |
| `raw/workflows/wf_c8d7894e-320.jsonl` | 61.462 | `07ac1d0f992dac78…` |
| `raw/workflows/wf_cb146e40-2bb.jsonl` | 935.883 | `6baac5ac88cc91e3…` |
| `raw/workflows/wf_cb4b53eb-4e2.jsonl` | 49.571 | `d90a57ba9dba54ce…` |
| `raw/workflows/wf_cbd67c1c-b9d.jsonl` | 63.878 | `7485d4555d3d9c8b…` |
| `raw/workflows/wf_ce801cde-95b.jsonl` | 40.958 | `4f0766bcce71756d…` |
| `raw/workflows/wf_d02616cb-f61.jsonl` | 68.855 | `9565512c1d39e14b…` |
| `raw/workflows/wf_d2b55b19-4bc.jsonl` | 227.155 | `906df8105b64aac8…` |
| `raw/workflows/wf_d3c360a7-9e2.jsonl` | 206.953 | `103091ae9df6811c…` |
| `raw/workflows/wf_d6572c22-3fe.jsonl` | 799.775 | `e5105a1eb83fc161…` |
| `raw/workflows/wf_d7345b60-c44.jsonl` | 57.291 | `8053e5d99a62ad87…` |
| `raw/workflows/wf_e47f9e2f-ff4.jsonl` | 51.795 | `c1418602504ba52e…` |
| `raw/workflows/wf_ea90c2c3-359.jsonl` | 70.300 | `779de9547e642e61…` |
| `raw/workflows/wf_eba81705-c45.jsonl` | 77.563 | `0dadd7f64231739d…` |
| `raw/workflows/wf_effb934a-82c.jsonl` | 246.737 | `502742ecee8ee603…` |
| `raw/workflows/wf_fb44e96b-74c.jsonl` | 53.005 | `33c43b1470d8b1f2…` |
| `pipeline/workflows/dk-katalog-ressort-opus-wf_7152a576-cab.js` | 4.104 | `93333d598458dd27…` |
| `pipeline/workflows/dk-katalog-ressort-wf_20880a47-533.js` | 3.452 | `b8f993494985d46d…` |
| `pipeline/workflows/dk-reg-baseline-wf_2847a79c-11f.js` | 14.499 | `20d5b6d9bd8d17c3…` |
| `pipeline/workflows/dk-reg-coverage-audit-wf_6bf57053-453.js` | 12.478 | `f8bd09696811660d…` |
| `pipeline/workflows/dk-reg-huller-wf_97db13a1-7ae.js` | 2.952 | `e808f08fdf1edc2a…` |
| `pipeline/workflows/dk-reg-indeks-vurdering-wf_0d909033-65f.js` | 5.876 | `6c2331def6c7a85d…` |
| `pipeline/workflows/reguleringskort-qa-wf_95d8d56d-6b0.js` | 4.979 | `74c0b077479b4335…` |
| `pipeline/workflows/dk-reg-domain.js` | 33.121 | `49f93dc2faa80bf7…` |
| `pipeline/workflows/dk-reg-fill.js` | 7.716 | `a1a61dbbd2edbac0…` |
| `pipeline/workflows/dk-reg-verify.js` | 18.218 | `eb3abe8469f7952d…` |
| `pipeline/workflows/dk-reg-verify3.js` | 8.114 | `2e56156a567914f3…` |
| `pipeline/run_all.sh` | 989 | `631b94499676b462…` |
| `pipeline/merge.py` | 11.877 | `e8f405954cd3417c…` |
| `pipeline/finalize.py` | 22.901 | `65d4af52776b1b03…` |
| `pipeline/seen_urls.py` | 1.503 | `ec3b0d7fdc95d96c…` |
| `pipeline/provenance.py` | 3.272 | `3a81f4ebf5adc1a0…` |
| `pipeline/manual_fixes.py` | 1.588 | `556f7ea8d4d8b52a…` |
| `pipeline/consolidate_huller.py` | 2.755 | `f8695d49ffe1601f…` |
| `pipeline/registry_sync.py` | 22.682 | `c143e071b4fc478e…` |
| `pipeline/write_registry.py` | 11.125 | `65067b72f3f03823…` |
| `pipeline/write_readme.py` | 18.163 | `4462acb0426d5cf1…` |
| `pipeline/viz_prep.py` | 2.947 | `f8a1267ed6dce89d…` |
| `pipeline/viz_kat.py` | 2.820 | `50254e1236658c54…` |
| `pipeline/viz_build.py` | 1.372 | `dfc5f3a6cafbebcb…` |
| `pipeline/viz_template.html` | 28.491 | `29343788c0c04283…` |
| `pipeline/viz_script.js` | 72.720 | `e590024632a99b28…` |
| `pipeline/coverage_prep.py` | 4.774 | `e0bbc191112a1576…` |
| `pipeline/dash_prep.py` | 12.718 | `b079188b678ca390…` |
| `pipeline/package.py` | 7.352 | `e18699ee5ce0435d…` |
| `pipeline/corpus/extract.py` | 7.981 | `78bfdd496bde8af4…` |
| `pipeline/corpus/prefixes.py` | 3.825 | `2010426567a1d9ba…` |
| `pipeline/corpus/udsteder.py` | 3.144 | `ff2bf29e07305f23…` |
| `pipeline/corpus/make_jobs.py` | 1.355 | `320603a1c54011ac…` |
| `pipeline/corpus/resolve.py` | 10.546 | `ab00b3531770f8fa…` |
| `pipeline/corpus/resolve_keys.py` | 605 | `eaf947d501e3d202…` |
| `pipeline/corpus/ressort_import.py` | 2.406 | `5c72a76e586278ac…` |
| `pipeline/corpus/ressort_quality.py` | 3.083 | `f1c228b7702af78b…` |
| `pipeline/corpus/katalog.py` | 11.396 | `531d4b16022db32d…` |
| `pipeline/corpus/census.py` | 1.044 | `6adc72d27bb4c052…` |
| `pipeline/corpus/run_corpus.sh` | 299 | `76285252fd3ae348…` |
| `pipeline/mmd/layout.js` | 1.242 | `7448250fe967d116…` |
| `pipeline/mmd/shot.js` | 2.524 | `de37a0753286cd5a…` |
| `pipeline/mmd/kshot.js` | 2.337 | `4323856d7cfe431b…` |
| `pipeline/mmd/kint.js` | 2.975 | `4b211c8bde4b7743…` |
| `pipeline/mmd/qa2.js` | 5.610 | `5d55301d382c4481…` |
| `pipeline/mmd/package.json` | 114 | `5db1274d606edb35…` |
| `harvest/harvest.py` | 12.797 | `25701114ad0f50ba…` |
| `harvest/run_harvest.sh` | 550 | `6d9e6324809c0483…` |
| `harvest/README.md` | 1.058 | `d6cf34b9f52fe5c6…` |
| `harvest/test_harvest.py` | 4.003 | `a2e5cc37a0756266…` |
