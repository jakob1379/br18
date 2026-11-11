export const meta = {
  name: 'dk-reg-domain',
  description: 'Kortlæg myndigheder, retsakter, klageveje, EU-kilder og datakilder pr. domæne; verificér adversarielt; konsolidér',
  phases: [
    { title: 'Research', detail: 'én agent pr. domæne → noder og kanter' },
    { title: 'Verify', detail: 'to uafhængige verifikatorer pr. domæne (organisation/hjemmel og kilder/identifikatorer)' },
    { title: 'Consolidate', detail: 'anvend rettelser og mangler som patch' },
  ],
}

const BASELINE_PATH = args.baseline_path

const DOMAINS = {
  byggeri: `BYGGERI: Byggeloven og bygningsreglementet (BR18 inkl. ændringer 2025-2026, fx klimakrav/LCA, og evt. ny udgave), bygningsreglementets vejledninger og "spørgsmål og svar", certificeringsordningen for statikere og brandrådgivere (certificeringsbekendtgørelsen), byggeskadeforsikring, øvrige bekendtgørelser med hjemmel i byggeloven (fx ladestanderbekendtgørelsen, skorstensfejerbekendtgørelsen, bekendtgørelse om byggesagsbehandling/gebyrer), byggevareforordningen (CPR: 305/2011 og 2024/3110) og dansk markedsovervågning/hjemmel, kommunal byggesagsbehandling (kommunalbestyrelsen som bygningsmyndighed; Byg og Miljø), klage over byggesager (Byggeklageenheden i Nævnenes Hus – retlige spørgsmål; kommunaltilsyn), AB 18/ABR 18/ABT 18 (hvem udgiver), Byggeriets Evaluerings Center, tilgængelighedskrav og handicaporganisationers klageret, bygningsreglementet.dk som kilde (HTML/PDF/API? versionshistorik), Eurocodes + danske nationale annekser (kun metadata: hvor publiceres de). Bygningsfredning ligger hos plan-agenten; brand-specifikke dele hos brand-agenten; VVS-krav hos el-gas-vvs-agenten – modellér kun kanterne dertil.`,
  bolig: `BOLIG: Lov om almene boliger, lov om leje af almene boliger, lejeloven (ny lejelov fra 2022 der samlede lejeloven og boligreguleringsloven – efterprøv), erhvervslejeloven (kun kant), andelsboligloven, ejerlejlighedsloven, byfornyelsesloven, lov om boligstøtte (Udbetaling Danmark), Landsbyggefonden, Byggeskadefonden, Grundejernes Investeringsfond, huslejenævn og beboerklagenævn (kommunale) og deres klage-/ankeveje (boligretten), kommunen som tilsynsmyndighed for almene boligorganisationer, Ankestyrelsens rolle, BPST/ansvarlig styrelses vejledninger på boligområdet (fx almenvejledningen), BL (metadata), offentliggørelse af huslejenævnsafgørelser og boligdomme, statsstøtte/SGEI-afgørelsen 2012/21/EU for almene boliger.`,
  plan: `PLAN: Planloven, landsplandirektiver (Fingerplan, kystnærhedszonen, sommerhusområder m.fl.), oversigt over statslige interesser i kommuneplanlægningen, kommuneplaner og lokalplaner (systemet; data hos kommunalt-agenten), zonetilladelser/landzone, statslig indsigelse, Planklagenævnet (lov om Planklagenævnet), plandata.dk, hvilken styrelse/hvilket ministerium har planloven nu (Bolig- og Planstyrelsen / Plan- og Landdistriktsstyrelsen / Erhvervsstyrelsen / By-, Land- og ...ministeriet – afgør det), udstykningsloven og matrikelloven (Klimadatastyrelsen; landinspektører), bygningsfredningsloven (Slots- og Kulturstyrelsen, Det Særlige Bygningssyn), bevaringsværdige bygninger (SAVE, FBB), museumsloven (arkæologi ved anlægsarbejde), BBR-loven og BBR-registeret (hvem er ansvarlig), Datafordeleren.`,
  energi: `ENERGI: Lov om fremme af energibesparelser i bygninger (energimærkning, energimærkningsbekendtgørelsen, energikonsulenter, håndbog for energikonsulenter, Energimærkeordningen/EMO), BR18 energikrav (kun kant), varmeforsyningsloven (projektbekendtgørelsen, varmeplanlægning, tilslutningspligt), elforsyningsloven, gasforsyningsloven, VE-loven, energieffektivitet/energisyn, lov om Energinet, ladestandere (kant), Forsyningstilsynet (lov om Forsyningstilsynet), Energiklagenævnet, Ankenævnet på Energiområdet, ecodesign og energimærkning af produkter (markedsovervågning), Klimaloven (perifert), Energistyrelsens og Energinets data. EU: EPBD 2024/1275 (og 2010/31), EED 2023/1791, RED III 2023/2413, ESPR 2024/1781 / ecodesign 2009/125, energimærkningsforordning 2017/1369, gasdirektiv 2024/1788, AFIR 2023/1804, ETS2 (direktiv 2023/959). Status for dansk implementering af EPBD-recast (frist 29. maj 2026).`,
  miljoe: `MILJØ: Miljøbeskyttelsesloven (forurening, godkendelse af listevirksomheder, miljøtilsyn – spildevand/drikkevand ligger hos natur-vand-kyst-agenten), miljøvurderingsloven (VVM/SMV), jordforureningsloven (kortlægning V1/V2 hos regionerne, jordflytningsbekendtgørelsen), affaldsbekendtgørelsen (bygge- og anlægsaffald, screening/kortlægning for PCB og asbest, affaldsregulativer), PCB-regler, kemikalier (REACH, CLP, POP; Miljøstyrelsen som myndighed), støj (bekendtgørelser og vejledninger om ekstern støj), godkendelsesbekendtgørelsen/BAT, bekendtgørelse om miljøregulering af visse aktiviteter (bygge- og anlægsarbejder), Miljø- og Fødevareklagenævnet, Miljøstyrelsen (mst.dk, vejledninger), Danmarks Miljøportal, regionerne, kommunerne (miljøtilsyn). Afgør ministeriets aktuelle navn. EU: IED 2010/75 og 2024/1785, EIA 2011/92 (ændret 2014/52), SEA 2001/42, affaldsrammedirektiv 2008/98, REACH 1907/2006, CLP 1272/2008, POP 2019/1021, støjdirektiv 2002/49, jordovervågningsdirektivet (Soil Monitoring Law).`,
  'natur-vand-kyst': `NATUR, VAND OG KYST: Naturbeskyttelsesloven (strand-, sø- og å-, skov-, fortids-, kirkebyggelinjer; § 3-natur; fredninger; fredningsnævn), habitatbekendtgørelsen (bilag IV-arter ved byggeri), skovloven (perifert), kystbeskyttelsesloven (Kystdirektoratet), vandløbsloven, lov om vandplanlægning, vandforsyningsloven, drikkevandsbekendtgørelsen, spildevandsbekendtgørelsen, betalingsloven for vandselskaber, vandsektorloven (Forsyningstilsynet), klimatilpasning (kystbeskyttelse/klimatilpasningslove, risikostyringsplaner), Naturstyrelsen, Miljøstyrelsen, Kystdirektoratet, fredningsnævnene, Miljø- og Fødevareklagenævnet, nedlagte nævn (Naturklagenævnet, Natur- og Miljøklagenævnet). Data: Danmarks Miljøportal/Arealinfo. EU: habitatdirektiv 92/43, fuglebeskyttelsesdirektiv 2009/147, vandrammedirektiv 2000/60, drikkevandsdirektiv 2020/2184, byspildevandsdirektiv 91/271 og recast 2024/3019, oversvømmelsesdirektiv 2007/60, naturgenopretningsforordning 2024/1991.`,
  arbejdsmiljoe: `ARBEJDSMILJØ: Arbejdsmiljøloven, bekendtgørelse om bygherrens pligter (koordinering, plan for sikkerhed og sundhed), bekendtgørelse om bygge- og anlægsarbejde, asbestbekendtgørelsen, bekendtgørelse om arbejdets udførelse, tekniske hjælpemidler (kraner, stilladser, elevatorer), maskiner, trykbærende udstyr, ATEX, kemiske agenser/grænseværdier, AT-vejledninger (fx serie om bygge og anlæg) og at.dk, Arbejdstilsynets afgørelser (påbud) og klageadgang (Arbejdsmiljøklagenævnet – afgør hvor det hører hjemme), Arbejdsmiljørådet, BFA Bygge & Anlæg (branchevejledninger – metadata), autoriserede arbejdsmiljørådgivere. EU: rammedirektiv 89/391, byggepladsdirektiv 92/57, asbestdirektiv 2009/148 (ændret 2023/2668), maskinforordning 2023/1230, PED 2014/68, ATEX 2014/34 og 1999/92, elevatordirektiv 2014/33, CMRD 2004/37, kemiske agenser 98/24.`,
  brand: `BRAND: Beredskabsloven (br18 bruger LBK-ELI 2025/1741), Beredskabsstyrelsen (afgør aktuel ressort efter juni 2026), kommunale redningsberedskaber/§ 60-selskaber, brandsyn (brandsynsbekendtgørelsen), driftsmæssige forskrifter (forsamlingslokaler, hoteller, butikker, campingpladser mv.), tekniske forskrifter for brandfarlige væsker/gasser/oplag, fyrværkeri (perifert), BR18 kap. 5 brand og brandvejledningerne (kant mod byggeri), certificerede brandrådgivere og brandklasser, skorstensfejerordningen (skorstensfejerbekendtgørelsen – br18 bruger ELI 2017/541; afgør udsteder), DBI (metadata), klageadgang over beredskabsmyndigheders afgørelser. EU: Seveso III 2012/18 (risikovirksomheder), CPR brandklassifikation (kant), ATEX (kant).`,
  'el-gas-vvs': `EL, GAS OG VVS: Elsikkerhedsloven og bekendtgørelser (elinstallationer, stærkstrøm, elektrisk materiel), gassikkerhedsloven og gasreglementet, autorisationsloven (el-, vvs- og kloakinstallationsområdet), Sikkerhedsstyrelsen (sik.dk, vejledninger, fortolkninger), klageadgang over Sikkerhedsstyrelsens afgørelser, vandinstallationer i BR18 kap. 21 (§§ 403-419) og DS 439, afløbsinstallationer og DS 432 (metadata), autoriserede kloakmestre, godkendelsesordning for byggevarer i kontakt med drikkevand, fjernvarmeinstallationer (DS 469 – metadata), olietanke/olietankbekendtgørelsen, elevatorer (kant), ladestandere (kant). Branchevejledninger: TEKNIQ, DANVA, Dansk Fjernvarme (metadata). EU: lavspændingsdirektiv 2014/35, EMC 2014/30, gasapparatforordning 2016/426, drikkevandsdirektiv 2020/2184 art. 11 + gennemførelsesretsakter (2024) om materialer i kontakt med drikkevand, CPR.`,
  'klage-tilsyn-praksis': `KLAGE, TILSYN OG PRAKSIS (tværgående): Nævnenes Hus (organisering; hvilke nævn det betjener – Planklagenævnet, Miljø- og Fødevareklagenævnet, Energiklagenævnet, Byggeklageenheden, Erhvervsankenævnet m.fl.; hjemmel), Ankestyrelsen (kommunaltilsyn efter kommunestyrelsesloven; principmeddelelser), Folketingets Ombudsmand (ombudsmandsloven; FOB-udtalelser; database), domstolene (byret/landsret/Højesteret, boligretten, Domstolsstyrelsen, Domsdatabasen – hvad offentliggøres, adgang/API), Ugeskrift for Retsvæsen (Karnov – betalingsmur), Voldgiftsnævnet for Bygge- og Anlægsvirksomhed (kendelser offentliggjort?), Klagenævnet for Udbud (perifert), huslejenævn/beboerklagenævn (kant), fredningsnævn (kant), Arbejdsmiljøklagenævnet, Erhvervsankenævnet. For hver: hjemmel, hvilke afgørelser offentliggøres og hvor (database-URL set i søgning), format, journalnr.-/citationsmønster (fx MFKN j.nr., FOB 2024-12, U.2024.1234H), adgang, opdateringsfrekvens. Nedlagte: Natur- og Miljøklagenævnet (2017), Statsforvaltningen (2019), Energitilsynet (2018).`,
  eu: `EU (tværgående): EU-retsakter der implementeres eller gælder direkte i scope (byggeri, bolig, plan, energi, miljø, natur/vand/kyst, arbejdsmiljø, brand, el/gas/VVS). For hver: titel, type, CELEX, ELI-URI (kun hvis set), EUR-Lex-URL set i søgning, gennemførelses-/anvendelsesfrist, dansk implementering (hvilken lov/bekendtgørelse – fodnoten "indeholder bestemmelser, der gennemfører ..."), ansvarligt ministerium/styrelse, status (fx EPBD-recast frist 29. maj 2026; CPR 2024/3110 anvendelse fra 8. jan. 2026). Dæk EUR-Lex som datakilde (ELI, CELEX, Cellar/SPARQL, webservice, RSS, licens jf. Kommissionens afgørelse 2011/833/EU), National Implementation Measures på EUR-Lex, og harmoniserede standarder (EUT-referencer) som metadata. Lav implementerer_EU-kanter fra danske retsakt-id’er til EU-id’er.`,
  'datakilder-standarder': `DATAKILDER OG STANDARDER (tværgående): Retsinformation (driftsansvar, ELI, API/åbne data – find den officielle dokumentation, historiske versioner, dokumenttyper, licens), Lovtidende, Statstidende, Folketingets Åbne Data (ODA; lovforslag, bemærkninger, betænkninger), Ministerialtidende, Domsdatabasen, Ombudsmanden (FOB), Nævnenes Hus’ afgørelsesportaler, Ankestyrelsens principmeddelelser, bygningsreglementet.dk, plandata.dk, Datafordeleren (BBR, Matrikel), Danmarks Miljøportal, at.dk, sik.dk, brs.dk, ens.dk, mst.dk. Standarder og branchevejledninger KUN som metadata: Dansk Standard (webshop, betalingsmur, ophavsret; EU-Domstolens dom C-588/21 P Public.Resource.Org af 5. marts 2024 om adgang til harmoniserede standarder; DS’ praksis for standarder der henvises til i lovgivning), Eurocodes og danske nationale annekser (gratis publicering?), BUILD/SBi-anvisninger, Molio, DBI, Teknologisk Institut, TEKNIQ, DANVA, BFA, Karnov/UfR. Ophavsretslovens § 9 som licensgrundlag for love/forskrifter/afgørelser. For hver kilde: URL (kun set), adgang, identifikatorer, licens, opdatering/versionshistorik, krydsreferencemønstre og ingest-vurdering.`,
  kommunalt: `KOMMUNALT OG REGIONALT: Kommunalbestyrelsen som bygnings-, plan-, miljø-, beredskabs- og tilsynsmyndighed; kommuneplaner, lokalplaner (Plandata.dk – status, PDF + geodata, plan-id), byplanvedtægter, spildevandsplaner, affaldsregulativer/-planer, vandforsyningsplaner, varmeplaner, klimatilpasningsplaner, risikostyringsplaner, beredskabsplaner/risikobaseret dimensionering, gebyrer for byggesagsbehandling, bevaringsdeklarationer, Byg og Miljø (hvem driver), KL (metadata), dagsordener/referater (format). Regioner: jordforurening (kortlægning), råstofplaner (perifert). Modellér kommuner som én node "kommune-alle" (type kommune) og regioner som "region-alle" (type region). For hver plan-/regulativtype: hjemmel (lov §), bindende/vejledende, hvor publiceret, identifikatorer, klageadgang, ingest-vurdering.`,
}

const COMMON = `
KONTEKST
- Dags dato: 2026-10-28. "Aktuel" = pr. denne dato. Formål: et krydsrefereret korpus af dansk regulering til RAG, hvor søgning skal kunne følge hjemmelskæder lov → bekendtgørelse → vejledning → praksis. Opgaven er KUN kortlægning – hent ikke dokumenterne.
- Scope (valgt): domæner byggeri, bolig, plan, energi, miljø, arbejdsmiljø, brand, el/gas/VVS; niveauer stat + kommunalt + EU; praksis (klagenævn, Ombudsmand, domme) medtages; standarder (DS/EN, Eurocodes) og branchevejledninger (BUILD/SBi, Molio m.fl.) KUN som metadata.
- Værktøjer: KUN WebSearch virker. WebFetch er blokeret af netværkspolitikken for alle eksterne domæner – brug den ikke. Evidens = WebSearch-resultater (titler, URL’er, uddrag/opsummering). Brug "standard" som udgangspunkt, "extended" til nye/svære fakta. Kør gerne flere søgninger parallelt i samme tur.
- Sikkerhedsmærker (præcis disse værdier):
  verificeret = påstanden fremgår direkte af et søgeresultat fra en officiel/primær kilde (retsinformation.dk, lovtidende.dk, ft.dk, myndighedens eget domæne, eur-lex.europa.eu) eller af to uafhængige troværdige sekundærkilder, OG afspejler tilstanden pr. 2026-10-28 (ressortforhold: kilde efter 3. juni 2026 eller baseline-afstemt).
  sandsynlig = én sekundærkilde, eller officiel kilde der kan være forældet, eller stærk faglig slutning (skriv i note hvad slutningen bygger på).
  ukendt = ingen evidens.
- URL’er: brug KUN URL’er der faktisk optrådte i dine søgeresultater, i baseline eller i seed-listen nedenfor. Konstruér/gæt aldrig URL’er, API-endpoints eller ELI’er. Mangler den: url.vaerdi = "ikke fundet". Det er bedre at skrive "ikke fundet" end at gætte.
- Seed (verificerede ELI’er for gældende versioner, fra jakob1379/br18 xref-laws.toml, tjekket mod retsinformation 2026-10-26): byggeloven https://www.retsinformation.dk/eli/lta/2016/1178 ; planloven https://www.retsinformation.dk/eli/lta/2024/572 ; udstykningsloven https://www.retsinformation.dk/eli/lta/2024/53 ; naturbeskyttelsesloven https://www.retsinformation.dk/eli/lta/2024/927 ; ladestanderbekendtgørelsen https://www.retsinformation.dk/eli/lta/2020/181 ; certificeringsbekendtgørelsen https://www.retsinformation.dk/eli/lta/2023/1693 ; beredskabsloven https://www.retsinformation.dk/eli/lta/2025/1741 ; bygningsfredningsloven https://www.retsinformation.dk/eli/lta/2018/219 ; arbejdsmiljøloven https://www.retsinformation.dk/eli/lta/2026/442 ; grundloven https://www.retsinformation.dk/eli/lta/1953/169 ; forvaltningsloven https://www.retsinformation.dk/eli/lta/2014/433 ; museumsloven https://www.retsinformation.dk/eli/lta/2025/1017 ; miljøbeskyttelsesloven https://www.retsinformation.dk/eli/lta/2026/842 ; teleloven https://www.retsinformation.dk/eli/lta/2025/681 ; masteloven https://www.retsinformation.dk/eli/lta/2021/420 ; skorstensfejerbekendtgørelsen https://www.retsinformation.dk/eli/lta/2017/541 . Kilde-URL for disse: https://github.com/jakob1379/br18/blob/main/xref-laws.toml . Disse må angives som verificeret for ELI/identifikator (ikke for andre påstande).
- Svar på dansk. Returnér rå data via StructuredOutput.

BASELINE: Læs FØRST filen ${BASELINE_PATH} med Read-værktøjet. Den er den afstemte ressortfordeling pr. 2026-10-28 (regering, ministerier, instanser, områder, ressortomlægninger, uafklarede konflikter). Brug dens id’er for ministerier og instanser; afviger du, så forklar i note og sæt sikkerhed derefter. Hovedpunkter: byggeri/bolig → min-boern-aeldre-og-bolig (administreres af sty-social-og-boligstyrelsen, organisatorisk under min-social); plan → min-by-land-og-transport (sty-plan-og-landdistriktsstyrelsen); Sikkerhedsstyrelsen fusioneret i sty-erhvervsstyrelsen 1/1/2026; affald → min-klima-energi-og-forsyning (Energistyrelsen); natur/vandmiljø/miljøvurdering → min-natur-og-dyrevelfaerd; miljøbeskyttelse/jord/kemikalier/drikkevand/spildevand/kyst → min-miljoe; beredskab → min-samfundssikkerhed-og-beredskab; arbejdsmiljø → min-beskaeftigelse-og-ligestilling; kommunaltilsyn → min-oekonomi-og-indenrigs (sty-ankestyrelsen); udstykning/matrikel → min-klima-energi-og-forsyning (sty-geodatastyrelsen).

ID-KONVENTIONER (små bogstaver, ascii: æ→ae, ø→oe, å→aa, bindestreger):
- ministerier/instanser: brug baseline-id’er. Nye instanser: sty-, naevn-, tilsyn-, raad-, fond-, dom-, ombud-, org- (private), std- (standardiseringsorgan/standard), kommune-alle, region-alle.
- love (type lov, ét node pr. lov; identifikatorer peger på gældende LBK/LOV): lov-<kortnavn>, fx lov-byggeloven, lov-planloven, lov-almenboligloven, lov-lejeloven, lov-andelsboligloven, lov-ejerlejlighedsloven, lov-byfornyelsesloven, lov-boligstoetteloven, lov-udstykningsloven, lov-matrikelloven, lov-bygningsfredningsloven, lov-museumsloven, lov-bbr-loven, lov-energimaerkningsloven (lov om fremme af energibesparelser i bygninger), lov-varmeforsyningsloven, lov-elforsyningsloven, lov-gasforsyningsloven, lov-ve-loven, lov-klimaloven, lov-forsyningstilsynsloven, lov-miljoebeskyttelsesloven, lov-miljoevurderingsloven, lov-jordforureningsloven, lov-naturbeskyttelsesloven, lov-kystbeskyttelsesloven, lov-vandloebsloven, lov-vandforsyningsloven, lov-vandsektorloven, lov-arbejdsmiljoeloven, lov-beredskabsloven, lov-elsikkerhedsloven, lov-gassikkerhedsloven, lov-autorisationsloven, lov-forvaltningsloven, lov-offentlighedsloven, lov-ombudsmandsloven, lov-kommunestyrelsesloven, lov-retsplejeloven, lov-ophavsretsloven, lov-planklagenaevnsloven, lov-mfkn-loven (lov om Miljø- og Fødevareklagenævnet). Brug disse præcist når loven er i spil.
- bekendtgørelser: bek-<kortnavn> (fx bek-br18 for bygningsreglementet, bek-certificering, bek-ladestandere, bek-skorstensfejer, bek-energimaerkning, bek-affald, bek-byggeplads/bygherrens pligter, bek-asbest); cirkulærer cirk-; vejledninger vejl-<…> (samlinger som én node, fx vejl-br18-vejledninger, vejl-at-vejledninger); tekniske forskrifter tf-<…>; planer/landsplandirektiver plan-<…>; regulativer reg-<…>.
- EU: eu-dir-YYYY-NNNN, eu-reg-YYYY-NNNN, eu-dec-YYYY-NNNN (fx eu-dir-2024-1275, eu-reg-2024-3110). Brug årstal og løbenummer som i retsaktens nummer, uden foranstillede nuller (fx eu-dir-1992-57, eu-dir-2010-31, eu-reg-2024-3110).
- dokumentkilder (type dokumentkilde): kilde-<slug>, fx kilde-retsinformation, kilde-lovtidende, kilde-eurlex, kilde-ft-oda, kilde-domsdatabasen, kilde-fob-database, kilde-bygningsreglementet-dk, kilde-plandata, kilde-datafordeleren, kilde-miljoeportal, kilde-mfkn-afgoerelser, kilde-pkn-afgoerelser, kilde-ast-principmeddelelser, kilde-at-dk, kilde-sik-dk, kilde-ens-dk, kilde-mst-dk, kilde-brs-dk.

NODETYPER (brug præcis): ministerium, styrelse, direktorat, nævn, klagenævn, tilsyn, råd, fond, domstol, ombudsmand, kommune, region, offentlig-virksomhed, eu-institution, privat-organisation, standardiseringsorgan, dokumentkilde, lov, bekendtgørelse, cirkulære, vejledning, teknisk-forskrift, plan, regulativ, eu-direktiv, eu-forordning, eu-afgørelse, standard, branchevejledning, praksissamling.

KANTTYPER (brug KUN disse; "from" er den aktive part, læses "from <type> to"):
- ressortansvar: ministerium → instans/lov (ministeriet har ressortansvaret)
- delegation: ministerium/styrelse → styrelse/kommune (kompetence delegeret; nævn delegationsbekendtgørelsen i beskrivelse)
- hjemmel_for: lov/bekendtgørelse → bekendtgørelse/vejledning/instans/plan (giver hjemmel til / opretter)
- udsteder: instans → retsakt/vejledning/dokumentkilde (udsteder/udgiver/driver)
- klageinstans: klageinstans → førsteinstans (from er klageinstans for afgørelser truffet af to; angiv lov i beskrivelse)
- tilsyn: tilsynsmyndighed → tilsynsobjekt
- implementerer_EU: dansk retsakt → EU-retsakt
- henviser_til: dokument → dokument (typisk krydsreference i teksten; fx bek-br18 henviser_til std-eurocodes)

FELTER PR. NODE (alle påkrævet; påstandsfelter har kilder[] og sikkerhed):
id, navn, type, ministerium (ministerium-id eller "ingen"), status (aktiv|nedlagt|omdøbt|ophævet|ukendt), tidligere_navne[] (navn, periode, efterfoelger-id hvis kendt, kilder, sikkerhed), hjemmel{tekst} (oprettelsesgrundlag for instanser; hjemmelslov § for bekendtgørelser; "ikke relevant" for love/EU), dokumenttyper{liste[{type, bindende: bindende|vejledende|blandet|ukendt}]} (hvad noden udsteder/indeholder: lov, lovbekendtgørelse, bekendtgørelse, cirkulære, vejledning, teknisk forskrift, afgørelse, principafgørelse, udtalelse, dom, FAQ/fortolkningsbidrag, plan, regulativ, standard, datasæt …), url{vaerdi}, adgang{vaerdier ⊆ [API, bulk, ELI, RSS, HTML, PDF, betalingsmur, ukendt, ikke-relevant], note}, identifikatorer{eli, lovtidende, celex, journalnr, andet}, licens{tekst}, opdatering{frekvens, versionshistorik}, krydsref_moenstre[] (typiske tekstmønstre, fx "§ 6 i lov om byggeri", "bekendtgørelse nr. 1399 af 12. december 2019", "BR18 § 82", "direktiv 2010/31/EU", "FOB 2019-21", "U.2020.1234H", "MFKN j.nr. 20/12345"), note. Valgfrit: ingest{vaerdi 1-5, besvaer 1-5, begrundelse} – SKAL udfyldes for dokumentkilder og for instanser/retsaktsamlinger, hvis dokumenter skal hentes fra dem (værdi = nytte for RAG/hjemmelskæder; besvær = teknisk/juridisk vanskelighed: 1 = API/bulk åben licens, 5 = betalingsmur/scannede PDF’er).
Nedlagte/omdøbte instanser: egen node med status nedlagt/omdøbt og en tidligere_navne-post hos efterfølgeren.
Omfang: dæk domænet udtømmende for instanser, klageveje og EU; for retsakter: alle love + de centrale bekendtgørelser/vejledningssamlinger der indgår i hjemmelskæder (ikke hver eneste bekendtgørelse). Typisk 30-70 noder og 60-180 kanter. Fejlagtig præcision er værre end "ukendt".
`

const CLAIM_PROPS = {
  kilder: { type: 'array', items: { type: 'string' } },
  sikkerhed: { type: 'string', enum: ['verificeret', 'sandsynlig', 'ukendt'] },
}
const claim = (extra, req = []) => ({
  type: 'object',
  properties: { ...extra, ...CLAIM_PROPS },
  required: [...req, 'kilder', 'sikkerhed'],
})
const NODE_TYPES = ['ministerium', 'styrelse', 'direktorat', 'nævn', 'klagenævn', 'tilsyn', 'råd', 'fond', 'domstol', 'ombudsmand', 'kommune', 'region', 'offentlig-virksomhed', 'eu-institution', 'privat-organisation', 'standardiseringsorgan', 'dokumentkilde', 'lov', 'bekendtgørelse', 'cirkulære', 'vejledning', 'teknisk-forskrift', 'plan', 'regulativ', 'eu-direktiv', 'eu-forordning', 'eu-afgørelse', 'standard', 'branchevejledning', 'praksissamling']
const EDGE_TYPES = ['ressortansvar', 'delegation', 'hjemmel_for', 'udsteder', 'klageinstans', 'tilsyn', 'implementerer_EU', 'henviser_til']
const ACCESS = ['API', 'bulk', 'ELI', 'RSS', 'HTML', 'PDF', 'betalingsmur', 'ukendt', 'ikke-relevant']

const NODE = {
  type: 'object',
  properties: {
    id: { type: 'string' },
    navn: { type: 'string' },
    type: { type: 'string', enum: NODE_TYPES },
    ministerium: { type: 'string' },
    status: { type: 'string', enum: ['aktiv', 'nedlagt', 'omdøbt', 'ophævet', 'ukendt'] },
    tidligere_navne: {
      type: 'array',
      items: claim({ navn: { type: 'string' }, periode: { type: 'string' }, efterfoelger: { type: 'string' } }, ['navn', 'periode']),
    },
    hjemmel: claim({ tekst: { type: 'string' } }, ['tekst']),
    dokumenttyper: claim({
      liste: {
        type: 'array',
        items: {
          type: 'object',
          properties: { type: { type: 'string' }, bindende: { type: 'string', enum: ['bindende', 'vejledende', 'blandet', 'ukendt'] }, note: { type: 'string' } },
          required: ['type', 'bindende'],
        },
      },
    }, ['liste']),
    url: claim({ vaerdi: { type: 'string' } }, ['vaerdi']),
    adgang: claim({ vaerdier: { type: 'array', items: { type: 'string', enum: ACCESS } }, note: { type: 'string' } }, ['vaerdier']),
    identifikatorer: claim({ eli: { type: 'string' }, lovtidende: { type: 'string' }, celex: { type: 'string' }, journalnr: { type: 'string' }, andet: { type: 'string' } }),
    licens: claim({ tekst: { type: 'string' } }, ['tekst']),
    opdatering: claim({ frekvens: { type: 'string' }, versionshistorik: { type: 'string' } }, ['frekvens', 'versionshistorik']),
    krydsref_moenstre: { type: 'array', items: { type: 'string' } },
    ingest: {
      type: 'object',
      properties: { vaerdi: { type: 'integer', minimum: 1, maximum: 5 }, besvaer: { type: 'integer', minimum: 1, maximum: 5 }, begrundelse: { type: 'string' } },
      required: ['vaerdi', 'besvaer', 'begrundelse'],
    },
    note: { type: 'string' },
  },
  required: ['id', 'navn', 'type', 'ministerium', 'status', 'tidligere_navne', 'hjemmel', 'dokumenttyper', 'url', 'adgang', 'identifikatorer', 'licens', 'opdatering', 'krydsref_moenstre'],
}
const EDGE = claim({
  from: { type: 'string' }, to: { type: 'string' },
  type: { type: 'string', enum: EDGE_TYPES },
  beskrivelse: { type: 'string' },
  gyldig_fra: { type: 'string' },
}, ['from', 'to', 'type', 'beskrivelse'])
const HUL = {
  type: 'object',
  properties: {
    emne: { type: 'string' },
    type: { type: 'string', enum: ['betalingsmur', 'kun-pdf', 'ingen-api', 'uklart', 'ikke-fundet', 'andet'] },
    beskrivelse: { type: 'string' },
    noder: { type: 'array', items: { type: 'string' } },
    kilder: { type: 'array', items: { type: 'string' } },
  },
  required: ['emne', 'type', 'beskrivelse', 'noder', 'kilder'],
}
const DOMAIN_SCHEMA = {
  type: 'object',
  properties: {
    nodes: { type: 'array', items: NODE },
    edges: { type: 'array', items: EDGE },
    huller: { type: 'array', items: HUL },
    noter: { type: 'array', items: { type: 'string' } },
  },
  required: ['nodes', 'edges', 'huller', 'noter'],
}
const VERIFY_SCHEMA = {
  type: 'object',
  properties: {
    fund: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          maal: { type: 'string', description: 'node-id, eller kant som "from|type|to"' },
          felt: { type: 'string' },
          vurdering: { type: 'string', enum: ['bekraeftet', 'rettet', 'afkraeftet', 'nedgraderet', 'opgraderet', 'uafklaret'] },
          korrekt_vaerdi: { type: 'string' },
          kilder: { type: 'array', items: { type: 'string' } },
          begrundelse: { type: 'string' },
        },
        required: ['maal', 'felt', 'vurdering', 'kilder', 'begrundelse'],
      },
    },
    mangler: {
      type: 'array',
      items: { type: 'object', properties: { beskrivelse: { type: 'string' }, kilder: { type: 'array', items: { type: 'string' } } }, required: ['beskrivelse', 'kilder'] },
    },
  },
  required: ['fund', 'mangler'],
}
const PATCH_SCHEMA = {
  type: 'object',
  properties: {
    node_upserts: { type: 'array', items: NODE, description: 'HELE noden (erstatter eksisterende med samme id)' },
    node_removals: { type: 'array', items: { type: 'object', properties: { id: { type: 'string' }, begrundelse: { type: 'string' } }, required: ['id', 'begrundelse'] } },
    edge_upserts: { type: 'array', items: EDGE, description: 'erstatter kant med samme from|type|to' },
    edge_removals: { type: 'array', items: { type: 'object', properties: { from: { type: 'string' }, type: { type: 'string' }, to: { type: 'string' }, begrundelse: { type: 'string' } }, required: ['from', 'type', 'to', 'begrundelse'] } },
    huller: { type: 'array', items: HUL, description: 'NYE huller (tilføjes)' },
    noter: { type: 'array', items: { type: 'string' } },
  },
  required: ['node_upserts', 'node_removals', 'edge_upserts', 'edge_removals', 'huller', 'noter'],
}

const LENSES = {
  organisation: `LINSE: ORGANISATION, RESSORT, HJEMMEL OG KLAGEVEJE. Efterprøv med egne, nye søgninger: (1) hver instans’ overordnede ministerium og status pr. 2026-10-28 (husk regeringsdannelsen 3. juni 2026 og omdøbninger), tidligere navne og datoer; (2) alle kanter af typen ressortansvar, delegation, hjemmel_for, klageinstans, tilsyn – findes de, er retningen rigtig ("from" er aktiv part), er den angivne lov rigtig; (3) hjemmel-tekster (lov og §) for instanser og bekendtgørelser; (4) bindende/vejledende-klassifikationen. Find også manglende instanser og klageveje.`,
  kilder: `LINSE: KILDER, URL’ER, ADGANG OG IDENTIFIKATORER. Efterprøv med egne, nye søgninger: (1) hver url.vaerdi – optræder netop den URL (eller et entydigt match) i søgeresultater? Gættede/konstruerede URL’er skal ændres til "ikke fundet"; (2) påstande om API, bulk, RSS, ELI – er der evidens? Ellers nedgradér; (3) ELI-, LBK/BEK-numre og CELEX-numre – er det gældende version og korrekt nummer?; (4) implementerer_EU-kanter – gennemfører den danske retsakt faktisk den EU-retsakt?; (5) licens og versionshistorik; (6) ingest-vurderinger – rimelige? Find også manglende vigtige datakilder.`,
}

const pick = (args.keys || Object.keys(DOMAINS)).filter(k => DOMAINS[k])

const results = await pipeline(
  pick,
  key => agent(`${COMMON}
DIT DOMÆNE – ${key}
${DOMAINS[key]}
(Listen er en tjekliste over hvad der skal undersøges – ikke fakta. Efterprøv alt; noget kan være forkert, omdøbt eller nedlagt.)

OPGAVE: Kortlæg alle myndigheder og instanser, der udsteder, fortolker eller håndhæver regler i domænet, med: (1) ministerium → styrelse/nævn/tilsyn (aktuel ressortfordeling), (2) for hver instans hvilke love den administrerer og hvilke dokumenttyper den udsteder, (3) klage- og tilsynsveje, (4) EU-retsakter der implementeres, (5) relevante dokumentkilder og deres adgang. Returnér noder, kanter, huller (paywall, kun PDF, ingen API, uklart, ikke fundet) og noter.`, { label: `research:${key}`, phase: 'Research', schema: DOMAIN_SCHEMA }),
  (res, key) => parallel(Object.entries(LENSES).map(([lens, text]) => () => agent(`${COMMON}
Du er adversariel verifikator for domænet "${key}". En anden agent har lavet kortlægningen nedenfor. Antag at den indeholder fejl: forældede ressortforhold, gættede URL’er, forkerte numre, forkert kantretning, overdreven sikkerhed. Din opgave er at finde dem.
${text}
Prioritér: alle påstande markeret verificeret uden primærkilde, alle url-felter, alle ressort-/klagekanter, alle CELEX/ELI. Efterprøv mindst 40 påstande (flere hvis tiden tillader). For hvert fund: maal (node-id eller "from|type|to"), felt, vurdering, korrekt_vaerdi (hvis rettet), kilder (URL’er fra DINE søgeresultater), begrundelse. Bekræftelser skal også med (vurdering "bekraeftet"), så konsolidatoren kan opgradere sikkerhed. Lister du mangler, så giv kilder.

DOMÆNETS KORTLÆGNING:
${JSON.stringify(res)}`, { label: `verify:${key}:${lens}`, phase: 'Verify', schema: VERIFY_SCHEMA })))
    .then(vs => ({ res, vs: vs.filter(Boolean) })),
  ({ res, vs }, key) => agent(`${COMMON}
Du er konsolidator for domænet "${key}". Du får (A) den oprindelige kortlægning og (B) to uafhængige verifikationsrapporter. Lav en PATCH der gør kortlægningen korrekt:
- Anvend hvert fund: rettet/afkraeftet/nedgraderet/opgraderet → opdatér noden/kanten (send HELE den opdaterede node i node_upserts; kanter i edge_upserts) eller fjern den (node_removals/edge_removals) hvis den er forkert. bekraeftet med primærkilde → må opgradere sikkerhed og tilføje kilden.
- Ved uenighed mellem verifikatorer eller mellem verifikator og original: lav selv en afgørende søgning; kan det ikke afgøres, brug den forsigtigste sikkerhed og skriv en note.
- Mangler: tilføj nye noder/kanter når der er kilde (lav selv søgninger efter behov); ellers registrér som hul.
- Bevar id-konventionerne; ret ikke id’er uden grund (en id-ændring = removal + upsert, og så skal alle kanter til den gamle id også fjernes/genindsættes).
- Kanter må kun pege på noder der findes i kortlægningen efter patch, i baseline eller er alment kendte id’er fra id-konventionerne (fx kilde-retsinformation, lov-forvaltningsloven) – opret noden i node_upserts hvis du er i tvivl.
- Uændrede noder/kanter skal IKKE med i patchen.

(A) KORTLÆGNING:
${JSON.stringify(res)}

(B) VERIFIKATIONSRAPPORTER:
${JSON.stringify(vs)}`, { label: `consolidate:${key}`, phase: 'Consolidate', schema: PATCH_SCHEMA }),
)

return pick.map((key, i) => ({ key, ok: !!results[i], upserts: results[i] ? results[i].node_upserts.length : 0, edge_upserts: results[i] ? results[i].edge_upserts.length : 0 }))
