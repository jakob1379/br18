# Klima-, Energi- og Forsyningsministeriet

> Genereret af `scripts/build.py` fra `registry.yaml` (dato 2026-10-28). Redigér ikke i hånden.
> Fuldt optrukne pile = `verificeret`; stiplede = `sandsynlig`/`ukendt`. Grå stiplede bokse = nedlagt/omdøbt/ophævet.

Noder: 128 · kanter: 224

```mermaid
flowchart LR
    classDef ministerium fill:#1f3a5f,stroke:#0d1b2a,color:#fff
    classDef instans fill:#d7e3f4,stroke:#1f3a5f,color:#0d1b2a
    classDef klage fill:#f6dcc2,stroke:#8a4b08,color:#3b1f00
    classDef retsakt fill:#e6f2e6,stroke:#2e6b2e,color:#103010
    classDef eu fill:#fff3b0,stroke:#7a6a00,color:#333
    classDef kilde fill:#eee,stroke:#666,color:#222
    classDef nedlagt fill:#fff,stroke:#999,color:#999,stroke-dasharray:4 3
    min_klima_energi_og_forsyning["Klima-, Energi- og Forsyningsministeriet"]:::ministerium
    eu_dir_1991_271["Byspildevandsdirektivet – Rådets direktiv 91/271/EØF af 21. maj 1991"]:::eu
    eu_dir_2019_944["Direktiv (EU) 2019/944 om fælles regler for det indre marked for elektricitet (elmarkedsdirektivet)"]:::eu
    eu_dir_2023_1791["Direktiv (EU) 2023/1791 om energieffektivitet og om ændring af forordning (EU) 2023/955 (omarbejdning, EED)"]:::eu
    eu_dir_2023_2413["Direktiv (EU) 2023/2413 om ændring af VE-direktivet (RED III)"]:::eu
    eu_dir_2023_959["Direktiv (EU) 2023/959 om ændring af ETS-direktivet 2003/87/EF, herunder ETS2 for bygninger og vejtransport"]:::eu
    eu_dir_2024_1785["Direktiv (EU) 2024/1785 om ændring af IE-direktivet"]:::eu
    eu_dir_2024_1788["Direktiv (EU) 2024/1788 om fælles regler for de indre markeder for vedvarende gas, naturgas og brint, om ændring af direktiv (EU) 2023/1791 og om ophævelse af direktiv 2009/73/EF (gasdirektivet)"]:::eu
    eu_dir_2002_49["Direktiv 2002/49/EF om vurdering og styring af ekstern støj (støjdirektivet)"]:::eu
    eu_dir_2003_87["Direktiv 2003/87/EF om en ordning for handel med kvoter for drivhusgasemissioner (ETS-direktivet)"]:::eu
    eu_dir_2006_7["Direktiv 2006/7/EF om forvaltning af badevandskvalitet (badevandsdirektivet)"]:::eu
    eu_dir_2007_2["Direktiv 2007/2/EF om opbygning af en infrastruktur for geografisk information i Det Europæiske Fællesskab (INSPIRE)"]:::eu
    eu_dir_2008_98["Direktiv 2008/98/EF om affald (affaldsrammedirektivet)"]:::eu
    eu_dir_2009_31["Direktiv 2009/31/EF om geologisk lagring af CO2 (CCS-direktivet)"]:::eu
    eu_dir_2010_75["Direktiv 2010/75/EU om industrielle emissioner (IED)"]:::eu
    eu_kommissionen["Europa-Kommissionen"]:::eu
    eu_dir_2018_2001["Europa-Parlamentets og Rådets direktiv (EU) 2018/2001 af 11. december 2018 om fremme af anvendelsen af energi fra vedvarende energikilder (omarbejdning) (RED II), som ændret ved direktiv (EU) 2023/2413"]:::eu
    eu_reg_2019_943["Forordning (EU) 2019/943 om det indre marked for elektricitet (elmarkedsforordningen), som ændret ved 2024/1747"]:::eu
    eu_reg_2011_1227["Forordning (EU) nr. 1227/2011 om integritet og gennemsigtighed på engrosenergimarkederne (REMIT), som ændret ved (EU) 2024/1106"]:::eu
    eu_reg_2019_1020["Markedsovervågningsforordningen (EU) 2019/1020"]:::eu
    eu_dir_2012_18["Seveso III-direktivet (direktiv 2012/18/EU om kontrol med risikoen for større uheld med farlige stoffer)"]:::eu
    org_energinet["Energinet"]:::instans
    sty_energistyrelsen["Energistyrelsen"]:::instans
    sty_erhvervsstyrelsen["Erhvervsstyrelsen"]:::instans
    tilsyn_forsyningstilsynet["Forsyningstilsynet"]:::instans
    sty_geodatastyrelsen["Geodatastyrelsen"]:::instans
    sty_klimadatastyrelsen["Klimadatastyrelsen"]:::instans
    raad_klimaraadet["Klimarådet"]:::instans
    kommune_alle["Kommunerne (98 kommunalbestyrelser)"]:::instans
    sty_miljoestyrelsen["Miljøstyrelsen"]:::instans
    tilsyn_vandsektortilsynet["Vandsektortilsynet"]:::instans
    bv_build_anvisning_213["BUILD-anvisning 213 Bygningers energibehov (tidl. SBi-anvisning 213; beregningsprogrammet Be18)"]:::kilde
    org_energimaerkningsfirmaer["Certificerede energimærkningsvirksomheder og energikonsulenter"]:::kilde
    std_ds_418["DS 418 Beregning af bygningers varmetab"]:::kilde
    kilde_datafordeleren["Datafordeleren"]:::kilde
    kilde_dma["Digital MiljøAdministration (DMA, dma.mst.dk)"]:::kilde
    kilde_energidataservice["Energi Data Service (Energinet)"]:::kilde
    org_energiforsyningsvirksomheder["Energiforsyningsvirksomheder (net-, gas- og fjernvarmeselskaber, elhandlere)"]:::kilde
    kilde_ekn_afgoerelser["Energiklagenævnets afgørelser (ekn.naevneneshus.dk)"]:::kilde
    kilde_emo["Energimærkeordningen / EMO (Energistyrelsens system og register for energimærker)"]:::kilde
    kilde_forsyningstilsynet_afgoerelser["Forsyningstilsynets afgørelser og tilsynspublikationer"]:::kilde
    kilde_kgl_res_2026_06_03["Kongelig resolution af 3. juni 2026 (ressortændringer ved dannelsen af S-SF-M-RV-regeringen)"]:::kilde
    kilde_mfkn_afgoerelser["MFKN afgørelsesportal (mfkn.naevneneshus.dk)"]:::kilde
    kilde_plandata["Plandata.dk"]:::kilde
    org_praktiserende_landinspektoerer["Praktiserende (beskikkede) landinspektører"]:::kilde
    bv_videncentret_selektiv_nedrivning["Verdibyg-vejledning om selektiv nedrivning (udgivet via GI)"]:::kilde
    kilde_ens_dk["ens.dk (Energistyrelsens website)"]:::kilde
    dom_domstolene["Domstolene (byret, landsret, Højesteret)"]:::klage
    naevn_energiklagenaevnet["Energiklagenævnet"]:::klage
    ombud_folketingets_ombudsmand["Folketingets Ombudsmand"]:::klage
    naevn_landinspektoernaevnet["Landinspektørnævnet"]:::klage
    min_miljoe["Miljøministeriet"]:::ministerium
    bek_co2_forskningslagring["Bekendtgørelse om geologisk lagring af CO2 på under 100 kt til forsknings-, udviklings- eller afprøvningsformål (BEK nr 974 af 22/06/2022) (ophævet)"]:::nedlagt
    eu_dir_2009_125["Direktiv 2009/125/EF om rammerne for krav til miljøvenligt design af energirelaterede produkter (ecodesigndirektivet) (ophævet)"]:::nedlagt
    eu_dir_2010_31["Direktiv 2010/31/EU om bygningers energimæssige ydeevne (EPBD, som ændret ved 2018/844) (ophævet)"]:::nedlagt
    tilsyn_energitilsynet["Energitilsynet (nedlagt)"]:::nedlagt
    sty_sikkerhedsstyrelsen["Sikkerhedsstyrelsen (nedlagt)"]:::nedlagt
    bek_co2_kvoter["Bekendtgørelse om CO2-kvoter m.v. (BEK nr 1386 af 02/12/2024, ændret ved BEK nr 1453 af 01/12/2025)"]:::retsakt
    bek_ens_opgaver["Bekendtgørelse om Energistyrelsens opgaver og beføjelser"]:::retsakt
    bek_haandbog_energikonsulenter["Bekendtgørelse om Håndbog for Energikonsulenter (HB2023)"]:::retsakt
    bek_vandsektortilsynet["Bekendtgørelse om Vandsektortilsynets virksomhed"]:::retsakt
    bek_affald["Bekendtgørelse om affald (affaldsbekendtgørelsen)"]:::retsakt
    bek_affaldsaktoer["Bekendtgørelse om affaldsregulativer, -gebyrer og -aktører m.v. (affaldsaktørbekendtgørelsen)"]:::retsakt
    bek_affaldstilsyn["Bekendtgørelse om affaldstilsyn (affaldstilsynsbekendtgørelsen)"]:::retsakt
    bek_jordflytning["Bekendtgørelse om anmeldelse og dokumentation i forbindelse med flytning af jord (jordflytningsbekendtgørelsen)"]:::retsakt
    bek_restprodukter["Bekendtgørelse om anvendelse af restprodukter, jord og sorteret bygge- og anlægsaffald (restproduktbekendtgørelsen)"]:::retsakt
    bek_badevand["Bekendtgørelse om badevand og badeområder (badevandsbekendtgørelsen, BEK nr. 917 af 2016)"]:::retsakt
    bek_bekaempelsesmidler["Bekendtgørelse om bekæmpelsesmidler (BEK nr. 952 af 2025)"]:::retsakt
    bek_brugerbetaling_miljoe["Bekendtgørelse om brugerbetaling for godkendelse, tilsyn m.v. (brugerbetalingsbekendtgørelsen)"]:::retsakt
    bek_energieffektivisering_offentlige["Bekendtgørelse om energieffektivisering i det offentlige"]:::retsakt
    bek_energimaerkning["Bekendtgørelse om energimærkning af bygninger (energimærkningsbekendtgørelsen)"]:::retsakt
    bek_ekn_gebyr["Bekendtgørelse om gebyr ved indbringelse af en klage for Energiklagenævnet (BEK nr 568 af 24/06/2026)"]:::retsakt
    bek_energimaerkning_gebyrer["Bekendtgørelse om gebyrer for ydelser i forbindelse med energimærkning efter lov om fremme af energibesparelser i bygninger (BEK nr. 313 af 19/03/2025)"]:::retsakt
    bek_godkendelse["Bekendtgørelse om godkendelse af listevirksomhed (godkendelsesbekendtgørelsen)"]:::retsakt
    bek_projektbekendtgoerelsen["Bekendtgørelse om godkendelse af projekter for kollektive varmeforsyningsanlæg (projektbekendtgørelsen)"]:::retsakt
    bek_co2_kvoter_henlaeggelse_erst["Bekendtgørelse om henlæggelse af visse beføjelser efter lov om CO2-kvoter til Erhvervsstyrelsen (ikrafttræden 1/1/2026)"]:::retsakt
    bek_selektiv_nedrivning["Bekendtgørelse om håndtering af affald og materialer fra bygge- og nedrivningsarbejde (selektiv nedrivning)"]:::retsakt
    bek_varme_prisregulering_indberetning["Bekendtgørelse om indberetning af oplysninger til brug for tilsyn med varmeforsyningslovens prisregulering og fastsættelse af prislofter (titel ændret ved ændringsbekendtgørelse 2025)"]:::retsakt
    bek_olietanke["Bekendtgørelse om indretning, etablering og drift af olietanke, rørsystemer og pipelines (olietankbekendtgørelsen)"]:::retsakt
    bek_indtaegtsrammer_el["Bekendtgørelse om indtægtsrammer for netvirksomheder (indtægtsrammebekendtgørelsen)"]:::retsakt
    bek_stoejkortlaegning["Bekendtgørelse om kortlægning af ekstern støj og udarbejdelse af støjhandlingsplaner (støjbekendtgørelsen)"]:::retsakt
    bek_udledning_forurenende_stoffer["Bekendtgørelse om krav til udledning af visse forurenende stoffer til vandløb, søer, overgangsvande, kystvande og havområder (BEK nr. 1433 af 21/11/2017)"]:::retsakt
    bek_matrikel["Bekendtgørelse om matrikulære arbejder (matrikelbekendtgørelsen) (BEK nr. 602 af 28/05/2025)"]:::retsakt
    bek_miljoeaktiviteter["Bekendtgørelse om miljøregulering af visse aktiviteter (miljøaktivitetsbekendtgørelsen)"]:::retsakt
    bek_miljoetilsyn["Bekendtgørelse om miljøtilsyn (miljøtilsynsbekendtgørelsen)"]:::retsakt
    bek_energisyn["Bekendtgørelse om obligatoriske energiledelsessystemer og energisyn og klimasyn i visse virksomheder (energisynsbekendtgørelsen)"]:::retsakt
    bek_affaldsvarmeprisloft["Bekendtgørelse om prisloft for affaldsvarme (affaldsvarmeprisloftbekendtgørelsen), BEK nr 1479 af 02/12/2025"]:::retsakt
    bek_spildevand["Bekendtgørelse om spildevandsplanen og spildevandstilladelser m.v. efter miljøbeskyttelseslovens kapitel 3 og 4 (spildevandsbekendtgørelsen)"]:::retsakt
    bek_systemansvar["Bekendtgørelse om systemansvarlig virksomhed og anvendelse af eltransmissionsnettet m.v. (systemansvarsbekendtgørelsen), 2025-udgave"]:::retsakt
    bek_tilslutning_varme["Bekendtgørelse om tilslutning m.v. til kollektive varmeforsyningsanlæg (tilslutningsbekendtgørelsen)"]:::retsakt
    bek_udstykningskontrol["Bekendtgørelse om udstykningskontrol (BEK nr. 601 af 28/05/2025)"]:::retsakt
    bek_energinet_oekonomi["Bekendtgørelse om økonomisk regulering af Energinet og dennes helejede datterselskaber (BEK nr 1559 af 06/12/2024)"]:::retsakt
    tf_energinet_forskrifter["Energinets tekniske forskrifter og markedsforskrifter (el og gas)"]:::retsakt
    vejl_ens_energivejledninger["Energistyrelsens vejledninger og fortolkningsbidrag (energimærkning, varmeforsyning, VE, energieffektivitet)"]:::retsakt
    vejl_forsyningstilsynet_vejledninger["Forsyningstilsynets vejledninger og udmeldinger (fx REMIT-vejledning om balanceansvarlige aktører april 2026, årlige prisloftudmeldinger for affalds- og overskudsvarme)"]:::retsakt
    plan_affaldsplan["Kommunal affaldsplan (fx Affaldsplan 2025-2036)"]:::retsakt
    plan_varmeplanlaegning["Kommunal varmeplanlægning og projektgodkendelser"]:::retsakt
    reg_affaldsregulativer["Kommunale affaldsregulativer"]:::retsakt
    reg_forskrifter_bygge_anlaeg["Kommunale forskrifter/regulativer for bygge-, anlægs- og nedrivningsaktiviteter"]:::retsakt
    lov_co2_kvoteloven["Lov om CO2-kvoter (CO2-kvoteloven), LOV nr 1767 af 28/12/2023"]:::retsakt
    lov_energiklagenaevnsloven["Lov om Energiklagenævnet"]:::retsakt
    lov_energinetloven["Lov om Energinet"]:::retsakt
    lov_forsyningstilsynsloven["Lov om Forsyningstilsynet"]:::retsakt
    lov_adresseloven["Lov om adresser og adresseregistrering (adresseloven)"]:::retsakt
    lov_undergrundsloven["Lov om anvendelse af Danmarks undergrund (undergrundsloven), LBK nr 1461 af 29/11/2023"]:::retsakt
    lov_betalingsloven["Lov om betalingsregler for spildevandsforsyningsselskaber m.v. (betalingsloven)"]:::retsakt
    lov_elforsyningsloven["Lov om elforsyning (elforsyningsloven)"]:::retsakt
    lov_effektiv_energianvendelse["Lov om fremme af effektiv energianvendelse og drivhusgasreducerende tiltag"]:::retsakt
    lov_energimaerkningsloven["Lov om fremme af energibesparelser i bygninger"]:::retsakt
    lov_ve_loven["Lov om fremme af vedvarende energi (VE-loven)"]:::retsakt
    lov_gasforsyningsloven["Lov om gasforsyning (gasforsyningsloven)"]:::retsakt
    lov_inspire_loven["Lov om infrastruktur for geografisk information (INSPIRE-loven/geodata-infrastrukturloven)"]:::retsakt
    lov_klimaloven["Lov om klima (klimaloven)"]:::retsakt
    lov_kontinentalsokkelloven["Lov om kontinentalsoklen og visse rørledningsanlæg på søterritoriet (kontinentalsokkelloven), LBK nr 1189 af 21/09/2018 med senere ændringer"]:::retsakt
    lov_landinspektoerloven["Lov om landinspektørvirksomhed (landinspektørloven)"]:::retsakt
    lov_miljoebeskyttelsesloven["Lov om miljøbeskyttelse (miljøbeskyttelsesloven)"]:::retsakt
    lov_ecodesignloven["Lov om miljøvenligt design af energirelaterede produkter (ecodesignloven)"]:::retsakt
    lov_miljoevurderingsloven["Lov om miljøvurderinger (miljøvurderingsloven, VVM/SMV)"]:::retsakt
    lov_offshoresikkerhedsloven["Lov om sikkerhed m.v. for offshoreanlæg til efterforskning, produktion og transport af kulbrinter (offshoresikkerhedsloven)"]:::retsakt
    lov_udstykningsloven["Lov om udstykning og anden registrering i matriklen (udstykningsloven)"]:::retsakt
    lov_miljoeskadeloven["Lov om undersøgelse, forebyggelse og afhjælpning af miljøskader (miljøskadeloven)"]:::retsakt
    lov_vandsektorloven["Lov om vandsektorens organisering og økonomiske forhold (vandsektorloven)"]:::retsakt
    lov_varmeforsyningsloven["Lov om varmeforsyning (varmeforsyningsloven)"]:::retsakt
    plan_national_bygningsrenoveringsplan["National bygningsrenoveringsplan (NBRP) efter EPBD 2024/1275"]:::retsakt
    bek_risiko["Risikobekendtgørelsen (bekendtgørelse om kontrol med risikoen for større uheld med farlige stoffer)"]:::retsakt
    plan_spildevandsplan["Spildevandsplan (inkl. tillæg)"]:::retsakt
    plan_stoejhandlingsplaner["Støjkortlægning og støjhandlingsplaner (kommuner, infrastrukturejere)"]:::retsakt
    vejl_udstykningskontrol["Vejledning om udstykningskontrollen (Geodatastyrelsen, pr. 17.6.2021)"]:::retsakt
    min_klima_energi_og_forsyning -->|delegation| sty_energistyrelsen
    min_klima_energi_og_forsyning -->|delegation| sty_geodatastyrelsen
    bek_affald -.->|henviser_til| bek_selektiv_nedrivning
    bek_ekn_gebyr -.->|henviser_til| lov_undergrundsloven
    bek_energimaerkning -->|henviser_til| bek_haandbog_energikonsulenter
    bek_energimaerkning -->|henviser_til| kilde_emo
    bek_energimaerkning_gebyrer -->|henviser_til| bek_energimaerkning
    bek_ens_opgaver -.->|henviser_til| lov_elforsyningsloven
    bek_ens_opgaver -.->|henviser_til| lov_gasforsyningsloven
    bek_haandbog_energikonsulenter -->|henviser_til| bv_build_anvisning_213
    bek_haandbog_energikonsulenter -.->|henviser_til| std_ds_418
    bek_projektbekendtgoerelsen -->|henviser_til| kilde_plandata
    bek_tilslutning_varme -.->|henviser_til| bek_projektbekendtgoerelsen
    bek_varme_prisregulering_indberetning -->|henviser_til| tilsyn_forsyningstilsynet
    bv_videncentret_selektiv_nedrivning -->|henviser_til| bek_selektiv_nedrivning
    kilde_ekn_afgoerelser -->|henviser_til| lov_energimaerkningsloven
    kilde_ekn_afgoerelser -->|henviser_til| lov_varmeforsyningsloven
    kilde_kgl_res_2026_06_03 -->|henviser_til| min_klima_energi_og_forsyning
    kilde_mfkn_afgoerelser -->|henviser_til| lov_miljoebeskyttelsesloven
    lov_energiklagenaevnsloven -->|henviser_til| lov_elforsyningsloven
    lov_energiklagenaevnsloven -->|henviser_til| lov_energimaerkningsloven
    lov_energiklagenaevnsloven -->|henviser_til| lov_energinetloven
    lov_energiklagenaevnsloven -->|henviser_til| lov_varmeforsyningsloven
    lov_energiklagenaevnsloven -->|henviser_til| lov_ve_loven
    lov_miljoeskadeloven -->|henviser_til| lov_miljoebeskyttelsesloven
    lov_offshoresikkerhedsloven -.->|henviser_til| lov_undergrundsloven
    plan_affaldsplan -->|henviser_til| lov_miljoevurderingsloven
    reg_affaldsregulativer -->|henviser_til| bek_affald
    vejl_forsyningstilsynet_vejledninger -->|henviser_til| eu_reg_2011_1227
    vejl_udstykningskontrol -.->|henviser_til| bek_udstykningskontrol
    vejl_udstykningskontrol -->|henviser_til| lov_udstykningsloven
    bek_affald -.->|hjemmel_for| plan_affaldsplan
    bek_affaldsaktoer -->|hjemmel_for| reg_affaldsregulativer
    bek_affaldsvarmeprisloft -->|hjemmel_for| tilsyn_forsyningstilsynet
    bek_energinet_oekonomi -.->|hjemmel_for| tilsyn_forsyningstilsynet
    bek_indtaegtsrammer_el -->|hjemmel_for| tilsyn_forsyningstilsynet
    bek_projektbekendtgoerelsen -->|hjemmel_for| plan_varmeplanlaegning
    bek_systemansvar -.->|hjemmel_for| tf_energinet_forskrifter
    bek_vandsektortilsynet -->|hjemmel_for| tilsyn_vandsektortilsynet
    lov_adresseloven -->|hjemmel_for| kommune_alle
    lov_co2_kvoteloven -.->|hjemmel_for| bek_co2_kvoter
    lov_co2_kvoteloven -->|hjemmel_for| bek_co2_kvoter_henlaeggelse_erst
    lov_co2_kvoteloven -->|hjemmel_for| sty_energistyrelsen
    lov_co2_kvoteloven -->|hjemmel_for| sty_erhvervsstyrelsen
    lov_ecodesignloven -.->|hjemmel_for| sty_erhvervsstyrelsen
    lov_ecodesignloven -->|hjemmel_for| sty_sikkerhedsstyrelsen
    lov_effektiv_energianvendelse -->|hjemmel_for| bek_energieffektivisering_offentlige
    lov_effektiv_energianvendelse -->|hjemmel_for| bek_energisyn
    lov_elforsyningsloven -->|hjemmel_for| bek_indtaegtsrammer_el
    lov_elforsyningsloven -->|hjemmel_for| bek_systemansvar
    lov_elforsyningsloven -->|hjemmel_for| naevn_energiklagenaevnet
    lov_elforsyningsloven -->|hjemmel_for| tf_energinet_forskrifter
    lov_elforsyningsloven -->|hjemmel_for| tilsyn_forsyningstilsynet
    lov_energimaerkningsloven -->|hjemmel_for| bek_energieffektivisering_offentlige
    lov_energimaerkningsloven -->|hjemmel_for| bek_energimaerkning
    lov_energimaerkningsloven -->|hjemmel_for| bek_energimaerkning_gebyrer
    lov_energimaerkningsloven -->|hjemmel_for| bek_haandbog_energikonsulenter
    lov_energimaerkningsloven -.->|hjemmel_for| org_energimaerkningsfirmaer
    lov_energinetloven -->|hjemmel_for| bek_energinet_oekonomi
    lov_energinetloven -->|hjemmel_for| bek_systemansvar
    lov_energinetloven -->|hjemmel_for| org_energinet
    lov_forsyningstilsynsloven -->|hjemmel_for| tilsyn_forsyningstilsynet
    lov_gasforsyningsloven -->|hjemmel_for| tilsyn_forsyningstilsynet
    lov_klimaloven -->|hjemmel_for| raad_klimaraadet
    lov_kontinentalsokkelloven -.->|hjemmel_for| sty_energistyrelsen
    lov_landinspektoerloven -->|hjemmel_for| naevn_landinspektoernaevnet
    lov_miljoebeskyttelsesloven -.->|hjemmel_for| bek_affald
    lov_miljoebeskyttelsesloven -.->|hjemmel_for| bek_affaldsaktoer
    lov_miljoebeskyttelsesloven -->|hjemmel_for| bek_affaldstilsyn
    lov_miljoebeskyttelsesloven -->|hjemmel_for| bek_badevand
    lov_miljoebeskyttelsesloven -->|hjemmel_for| bek_bekaempelsesmidler
    lov_miljoebeskyttelsesloven -->|hjemmel_for| bek_brugerbetaling_miljoe
    lov_miljoebeskyttelsesloven -->|hjemmel_for| bek_godkendelse
    lov_miljoebeskyttelsesloven -->|hjemmel_for| bek_jordflytning
    lov_miljoebeskyttelsesloven -->|hjemmel_for| bek_miljoeaktiviteter
    lov_miljoebeskyttelsesloven -.->|hjemmel_for| bek_miljoetilsyn
    lov_miljoebeskyttelsesloven -->|hjemmel_for| bek_olietanke
    lov_miljoebeskyttelsesloven -->|hjemmel_for| bek_restprodukter
    lov_miljoebeskyttelsesloven -->|hjemmel_for| bek_risiko
    lov_miljoebeskyttelsesloven -->|hjemmel_for| bek_selektiv_nedrivning
    lov_miljoebeskyttelsesloven -->|hjemmel_for| bek_spildevand
    lov_miljoebeskyttelsesloven -->|hjemmel_for| bek_stoejkortlaegning
    lov_miljoebeskyttelsesloven -->|hjemmel_for| bek_udledning_forurenende_stoffer
    lov_miljoebeskyttelsesloven -->|hjemmel_for| kommune_alle
    lov_miljoebeskyttelsesloven -->|hjemmel_for| plan_affaldsplan
    lov_miljoebeskyttelsesloven -->|hjemmel_for| plan_spildevandsplan
    lov_miljoebeskyttelsesloven -->|hjemmel_for| reg_affaldsregulativer
    lov_miljoebeskyttelsesloven -->|hjemmel_for| sty_miljoestyrelsen
    lov_miljoevurderingsloven -->|hjemmel_for| sty_energistyrelsen
    lov_udstykningsloven -.->|hjemmel_for| bek_matrikel
    lov_udstykningsloven -.->|hjemmel_for| bek_udstykningskontrol
    lov_udstykningsloven -->|hjemmel_for| kommune_alle
    lov_udstykningsloven -->|hjemmel_for| sty_geodatastyrelsen
    lov_undergrundsloven -->|hjemmel_for| bek_co2_forskningslagring
    lov_undergrundsloven -->|hjemmel_for| sty_energistyrelsen
    lov_vandsektorloven -->|hjemmel_for| bek_vandsektortilsynet
    lov_vandsektorloven -->|hjemmel_for| tilsyn_vandsektortilsynet
    lov_varmeforsyningsloven -->|hjemmel_for| bek_affaldsvarmeprisloft
    lov_varmeforsyningsloven -->|hjemmel_for| bek_projektbekendtgoerelsen
    lov_varmeforsyningsloven -->|hjemmel_for| bek_tilslutning_varme
    lov_varmeforsyningsloven -->|hjemmel_for| bek_varme_prisregulering_indberetning
    lov_varmeforsyningsloven -->|hjemmel_for| kommune_alle
    lov_varmeforsyningsloven -->|hjemmel_for| naevn_energiklagenaevnet
    lov_varmeforsyningsloven -->|hjemmel_for| plan_varmeplanlaegning
    lov_varmeforsyningsloven -->|hjemmel_for| tilsyn_forsyningstilsynet
    lov_ve_loven -->|hjemmel_for| bek_systemansvar
    lov_ve_loven -->|hjemmel_for| naevn_energiklagenaevnet
    lov_ve_loven -->|hjemmel_for| org_energinet
    lov_ve_loven -->|hjemmel_for| tilsyn_forsyningstilsynet
    bek_affald -.->|implementerer_EU| eu_dir_2008_98
    bek_co2_kvoter -.->|implementerer_EU| eu_dir_2003_87
    bek_energieffektivisering_offentlige -->|implementerer_EU| eu_dir_2023_1791
    bek_energimaerkning -.->|implementerer_EU| eu_dir_2010_31
    bek_energisyn -.->|implementerer_EU| eu_dir_2023_1791
    bek_haandbog_energikonsulenter -.->|implementerer_EU| eu_dir_2010_31
    bek_projektbekendtgoerelsen -.->|implementerer_EU| eu_dir_2023_1791
    lov_co2_kvoteloven -->|implementerer_EU| eu_dir_2003_87
    lov_co2_kvoteloven -->|implementerer_EU| eu_dir_2023_959
    lov_ecodesignloven -->|implementerer_EU| eu_dir_2009_125
    lov_ecodesignloven -.->|implementerer_EU| eu_reg_2019_1020
    lov_effektiv_energianvendelse -->|implementerer_EU| eu_dir_2023_1791
    lov_elforsyningsloven -->|implementerer_EU| eu_dir_2018_2001
    lov_elforsyningsloven -->|implementerer_EU| eu_dir_2019_944
    lov_elforsyningsloven -.->|implementerer_EU| eu_reg_2019_943
    lov_energimaerkningsloven -.->|implementerer_EU| eu_dir_2010_31
    lov_energinetloven -.->|implementerer_EU| eu_dir_2019_944
    lov_forsyningstilsynsloven -.->|implementerer_EU| eu_dir_2019_944
    lov_forsyningstilsynsloven -.->|implementerer_EU| eu_dir_2024_1788
    lov_gasforsyningsloven -.->|implementerer_EU| eu_dir_2024_1788
    lov_inspire_loven -->|implementerer_EU| eu_dir_2007_2
    lov_miljoebeskyttelsesloven -.->|implementerer_EU| eu_dir_1991_271
    lov_miljoebeskyttelsesloven -.->|implementerer_EU| eu_dir_2002_49
    lov_miljoebeskyttelsesloven -->|implementerer_EU| eu_dir_2008_98
    lov_miljoebeskyttelsesloven -->|implementerer_EU| eu_dir_2010_75
    lov_miljoebeskyttelsesloven -.->|implementerer_EU| eu_dir_2012_18
    lov_miljoebeskyttelsesloven -.->|implementerer_EU| eu_dir_2024_1785
    lov_undergrundsloven -->|implementerer_EU| eu_dir_2009_31
    lov_varmeforsyningsloven -->|implementerer_EU| eu_dir_2018_2001
    lov_varmeforsyningsloven -->|implementerer_EU| eu_dir_2023_1791
    lov_ve_loven -.->|implementerer_EU| eu_dir_2018_2001
    lov_ve_loven -.->|implementerer_EU| eu_dir_2023_2413
    dom_domstolene -->|klageinstans| sty_geodatastyrelsen
    naevn_energiklagenaevnet -->|klageinstans| org_energinet
    naevn_energiklagenaevnet -->|klageinstans| sty_energistyrelsen
    naevn_energiklagenaevnet -->|klageinstans| tilsyn_forsyningstilsynet
    sty_energistyrelsen -->|klageinstans| org_energimaerkningsfirmaer
    min_klima_energi_og_forsyning -->|ressortansvar| bek_affald
    min_klima_energi_og_forsyning -->|ressortansvar| bek_affaldsaktoer
    min_klima_energi_og_forsyning -.->|ressortansvar| bek_affaldsvarmeprisloft
    min_klima_energi_og_forsyning -->|ressortansvar| lov_adresseloven
    min_klima_energi_og_forsyning -->|ressortansvar| lov_betalingsloven
    min_klima_energi_og_forsyning -->|ressortansvar| lov_co2_kvoteloven
    min_klima_energi_og_forsyning -.->|ressortansvar| lov_ecodesignloven
    min_klima_energi_og_forsyning -.->|ressortansvar| lov_effektiv_energianvendelse
    min_klima_energi_og_forsyning -->|ressortansvar| lov_elforsyningsloven
    min_klima_energi_og_forsyning -.->|ressortansvar| lov_energimaerkningsloven
    min_klima_energi_og_forsyning -->|ressortansvar| lov_energinetloven
    min_klima_energi_og_forsyning -->|ressortansvar| lov_forsyningstilsynsloven
    min_klima_energi_og_forsyning -->|ressortansvar| lov_gasforsyningsloven
    min_klima_energi_og_forsyning -.->|ressortansvar| lov_inspire_loven
    min_klima_energi_og_forsyning -.->|ressortansvar| lov_klimaloven
    min_klima_energi_og_forsyning -->|ressortansvar| lov_kontinentalsokkelloven
    min_klima_energi_og_forsyning -.->|ressortansvar| lov_landinspektoerloven
    min_klima_energi_og_forsyning -.->|ressortansvar| lov_miljoebeskyttelsesloven
    min_klima_energi_og_forsyning -->|ressortansvar| lov_udstykningsloven
    min_klima_energi_og_forsyning -->|ressortansvar| lov_undergrundsloven
    min_klima_energi_og_forsyning -->|ressortansvar| lov_vandsektorloven
    min_klima_energi_og_forsyning -.->|ressortansvar| lov_varmeforsyningsloven
    min_klima_energi_og_forsyning -->|ressortansvar| lov_ve_loven
    min_klima_energi_og_forsyning -.->|ressortansvar| naevn_landinspektoernaevnet
    min_klima_energi_og_forsyning -->|ressortansvar| org_energinet
    min_klima_energi_og_forsyning -->|ressortansvar| raad_klimaraadet
    min_klima_energi_og_forsyning -->|ressortansvar| sty_energistyrelsen
    min_klima_energi_og_forsyning -->|ressortansvar| sty_geodatastyrelsen
    min_klima_energi_og_forsyning -->|ressortansvar| sty_klimadatastyrelsen
    min_klima_energi_og_forsyning -->|ressortansvar| tilsyn_energitilsynet
    min_klima_energi_og_forsyning -->|ressortansvar| tilsyn_forsyningstilsynet
    eu_kommissionen -.->|tilsyn| min_klima_energi_og_forsyning
    naevn_landinspektoernaevnet -->|tilsyn| org_praktiserende_landinspektoerer
    ombud_folketingets_ombudsmand -.->|tilsyn| sty_energistyrelsen
    ombud_folketingets_ombudsmand -.->|tilsyn| tilsyn_forsyningstilsynet
    sty_energistyrelsen -->|tilsyn| org_energimaerkningsfirmaer
    sty_geodatastyrelsen -->|tilsyn| org_praktiserende_landinspektoerer
    tilsyn_forsyningstilsynet -->|tilsyn| eu_reg_2011_1227
    tilsyn_forsyningstilsynet -->|tilsyn| org_energiforsyningsvirksomheder
    tilsyn_forsyningstilsynet -->|tilsyn| org_energinet
    kommune_alle -->|udsteder| plan_affaldsplan
    kommune_alle -->|udsteder| plan_varmeplanlaegning
    kommune_alle -->|udsteder| reg_affaldsregulativer
    min_klima_energi_og_forsyning -.->|udsteder| bek_affald
    min_klima_energi_og_forsyning -.->|udsteder| bek_ens_opgaver
    min_miljoe -.->|udsteder| bek_selektiv_nedrivning
    org_energinet -->|udsteder| kilde_energidataservice
    org_energinet -->|udsteder| tf_energinet_forskrifter
    sty_energistyrelsen -.->|udsteder| bek_affald
    sty_energistyrelsen -.->|udsteder| bek_affaldsaktoer
    sty_energistyrelsen -.->|udsteder| bek_co2_forskningslagring
    sty_energistyrelsen -.->|udsteder| bek_co2_kvoter
    sty_energistyrelsen -.->|udsteder| bek_energieffektivisering_offentlige
    sty_energistyrelsen -.->|udsteder| bek_energimaerkning
    sty_energistyrelsen -.->|udsteder| bek_energisyn
    sty_energistyrelsen -.->|udsteder| bek_haandbog_energikonsulenter
    sty_energistyrelsen -->|udsteder| bek_indtaegtsrammer_el
    sty_energistyrelsen -.->|udsteder| bek_projektbekendtgoerelsen
    sty_energistyrelsen -->|udsteder| bek_systemansvar
    sty_energistyrelsen -->|udsteder| kilde_emo
    sty_energistyrelsen -->|udsteder| kilde_ens_dk
    sty_energistyrelsen -.->|udsteder| plan_national_bygningsrenoveringsplan
    sty_energistyrelsen -->|udsteder| vejl_ens_energivejledninger
    sty_geodatastyrelsen -->|udsteder| kilde_datafordeleren
    sty_geodatastyrelsen -->|udsteder| vejl_udstykningskontrol
    sty_klimadatastyrelsen -->|udsteder| kilde_datafordeleren
    tilsyn_forsyningstilsynet -->|udsteder| kilde_forsyningstilsynet_afgoerelser
    tilsyn_forsyningstilsynet -->|udsteder| vejl_forsyningstilsynet_vejledninger
    bek_miljoeaktiviteter -->|hjemmel_for| reg_forskrifter_bygge_anlaeg
    bek_miljoetilsyn -.->|hjemmel_for| kilde_dma
    bek_spildevand -->|hjemmel_for| plan_spildevandsplan
    bek_stoejkortlaegning -->|hjemmel_for| plan_stoejhandlingsplaner
    bek_badevand -->|implementerer_EU| eu_dir_2006_7
    bek_godkendelse -->|implementerer_EU| eu_dir_2010_75
    bek_miljoetilsyn -.->|implementerer_EU| eu_dir_2010_75
    bek_risiko -->|implementerer_EU| eu_dir_2012_18
    bek_spildevand -.->|implementerer_EU| eu_dir_1991_271
    bek_stoejkortlaegning -->|implementerer_EU| eu_dir_2002_49
```

[← Overblik](oversigt.md)
