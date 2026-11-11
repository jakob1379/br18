# Erhvervsministeriet

> Genereret af `scripts/build.py` fra `registry.yaml` (dato 2026-10-28). Redigér ikke i hånden.
> Fuldt optrukne pile = `verificeret`; stiplede = `sandsynlig`/`ukendt`. Grå stiplede bokse = nedlagt/omdøbt/ophævet.

Noder: 136 · kanter: 209

```mermaid
flowchart LR
    classDef ministerium fill:#1f3a5f,stroke:#0d1b2a,color:#fff
    classDef instans fill:#d7e3f4,stroke:#1f3a5f,color:#0d1b2a
    classDef klage fill:#f6dcc2,stroke:#8a4b08,color:#3b1f00
    classDef retsakt fill:#e6f2e6,stroke:#2e6b2e,color:#103010
    classDef eu fill:#fff3b0,stroke:#7a6a00,color:#333
    classDef kilde fill:#eee,stroke:#666,color:#222
    classDef nedlagt fill:#fff,stroke:#999,color:#999,stroke-dasharray:4 3
    min_erhverv["Erhvervsministeriet"]:::ministerium
    eu_reg_2011_305["Byggevareforordningen (EU) nr. 305/2011 (CPR)"]:::eu
    eu_dir_2006_42["Direktiv 2006/42/EF om maskiner (maskindirektivet)"]:::eu
    eu_dir_2011_92["Direktiv 2011/92/EU om vurdering af visse offentlige og private projekters indvirkning på miljøet (VVM)"]:::eu
    eu_dir_2013_29["Direktiv 2013/29/EU om tilgængeliggørelse af pyrotekniske artikler på markedet (omarbejdning)"]:::eu
    eu_dir_2014_33["Direktiv 2014/33/EU om elevatorer og sikkerhedskomponenter til elevatorer"]:::eu
    eu_dir_2014_34["Direktiv 2014/34/EU om materiel og sikringssystemer til anvendelse i eksplosionsfarlig atmosfære (ATEX-produktdirektivet)"]:::eu
    eu_dir_2014_68["Direktiv 2014/68/EU om trykbærende udstyr (PED)"]:::eu
    eu_dir_2005_36["Europa-Parlamentets og Rådets direktiv 2005/36/EF af 7. september 2005 om anerkendelse af erhvervsmæssige kvalifikationer"]:::eu
    eu_dir_2007_66["Europa-Parlamentets og Rådets direktiv 2007/66/EF om ændring af Rådets direktiv 89/665/EØF og 92/13/EØF om effektiviteten af klageprocedurerne vedrørende indgåelse af offentlige kontrakter (håndhævelsesdirektivet)"]:::eu
    eu_reg_2016_425["Forordning (EU) 2016/425 om personlige værnemidler (PPE-forordningen)"]:::eu
    eu_reg_2017_1369["Forordning (EU) 2017/1369 om opstilling af en ramme for energimærkning (energimærkningsforordningen for produkter)"]:::eu
    eu_reg_2023_1230["Forordning (EU) 2023/1230 om maskiner (maskinforordningen)"]:::eu
    eu_reg_2016_426["Gasapparatforordningen (EU) 2016/426 (GAR)"]:::eu
    eu_dir_2014_35["Lavspændingsdirektivet 2014/35/EU"]:::eu
    eu_reg_2019_1020["Markedsovervågningsforordningen (EU) 2019/1020"]:::eu
    eu_reg_2024_3110["Revideret byggevareforordning (EU) 2024/3110"]:::eu
    eu_dir_2012_18["Seveso III-direktivet (direktiv 2012/18/EU om kontrol med risikoen for større uheld med farlige stoffer)"]:::eu
    sty_arbejdstilsynet["Arbejdstilsynet"]:::instans
    org_energinet["Energinet"]:::instans
    sty_energistyrelsen["Energistyrelsen"]:::instans
    sty_erhvervsstyrelsen["Erhvervsstyrelsen"]:::instans
    org_finansiel_stabilitet["Finansiel Stabilitet"]:::instans
    sty_finanstilsynet["Finanstilsynet"]:::instans
    tilsyn_forsyningstilsynet["Forsyningstilsynet"]:::instans
    kommune_alle["Kommunerne (98 kommunalbestyrelser)"]:::instans
    sty_konkurrence_og_forbrugerstyrelsen["Konkurrence- og Forbrugerstyrelsen"]:::instans
    raad_konkurrenceraadet["Konkurrencerådet"]:::instans
    sty_kystdirektoratet["Kystdirektoratet"]:::instans
    sty_miljoestyrelsen["Miljøstyrelsen"]:::instans
    sty_naevnenes_hus["Nævnenes Hus"]:::instans
    sty_plan_og_landdistriktsstyrelsen["Plan- og Landdistriktsstyrelsen"]:::instans
    region_alle["Regionerne (5 regionsråd)"]:::instans
    raad_el_og_gasteknisk_sikkerhed["Rådet for El- og Gasteknisk Sikkerhed"]:::instans
    sty_groen_arealomlaegning_og_vandmiljoe["Styrelsen for Grøn Arealomlægning og Vandmiljø (SGAV)"]:::instans
    tilsyn_vandsektortilsynet["Vandsektortilsynet"]:::instans
    org_ankenaevnet_for_fondsmaeglerselskaber["Ankenævnet for Fondsmæglerselskaber"]:::kilde
    kilde_autorisationsregister["Autorisationsregister (el, VVS, kloak, gas, asbest)"]:::kilde
    kilde_bke_afgoerelser["Byggeklageenhedens afgørelser"]:::kilde
    std_ds_en_50110["DS/EN 50110 Drift af elektriske anlæg"]:::kilde
    std_ds_hd_60364["DS/HD 60364 Elektriske lavspændingsinstallationer"]:::kilde
    org_det_finansielle_ankenaevn["Det finansielle ankenævn"]:::kilde
    kilde_ekn_afgoerelser["Energiklagenævnets afgørelser (ekn.naevneneshus.dk)"]:::kilde
    kilde_ean_afgoerelser["Erhvervsankenævnets kendelser (ean.naevneneshus.dk)"]:::kilde
    kilde_mfkn_afgoerelser["MFKN afgørelsesportal (mfkn.naevneneshus.dk)"]:::kilde
    kilde_mrf["Miljøretlig Forskningsportal (MRF), Københavns Universitet"]:::kilde
    kilde_naevneneshus_afgoerelser["Nævnenes Hus – afgørelser fra øvrige nævn (Energiklagenævnet, Byggeklageenheden, Erhvervsankenævnet m.fl.)"]:::kilde
    kilde_pkn_afgoerelser["Planklagenævnets afgørelser"]:::kilde
    bv_tekniq_vejledninger["TEKNIQ's branchevejledninger (bl.a. om overtrædelse af autorisationsloven og elektronisk sameksistens/EMC)"]:::kilde
    kilde_sik_dk["sik.dk (Sikkerhedsstyrelsens site, nu Erhvervsstyrelsen)"]:::kilde
    kilde_virk_nye_regler["virk.dk – Nye regler (oversigt over nye erhvervsrettede regler)"]:::kilde
    naevn_byggeklageenheden["Byggeklageenheden"]:::klage
    dom_byretterne["Byretterne"]:::klage
    dom_domstolene["Domstolene (byret, landsret, Højesteret)"]:::klage
    naevn_energiklagenaevnet["Energiklagenævnet"]:::klage
    naevn_erhvervsankenaevnet["Erhvervsankenævnet"]:::klage
    ombud_folketingets_ombudsmand["Folketingets Ombudsmand"]:::klage
    naevn_fredningsnaevn["Fredningsnævnene"]:::klage
    naevn_klagenaevnet_for_udbud["Klagenævnet for Udbud"]:::klage
    naevn_konkurrenceankenaevnet["Konkurrenceankenævnet"]:::klage
    naevn_miljoe_og_foedevareklagenaevnet["Miljø- og Fødevareklagenævnet"]:::klage
    naevn_planklagenaevnet["Planklagenævnet"]:::klage
    naevn_taksationskommissionen["Taksationskommissionen (naturbeskyttelsesloven)"]:::klage
    min_by_land_og_transport["By-, Land- og Transportministeriet"]:::ministerium
    lov_visse_produkter["Lov nr. 155 af 20/02/2013 om indretning m.v. af visse produkter (ophævet)"]:::nedlagt
    sty_sikkerhedsstyrelsen["Sikkerhedsstyrelsen (nedlagt)"]:::nedlagt
    lov_arbejdsmiljoeloven["Arbejdsmiljøloven"]:::retsakt
    bek_klagenaevn_sagsbehandlingslofter["Bekendtgørelse om (mål for) sagsbehandlingslofter i Miljø- og Fødevareklagenævnet, Planklagenævnet og Energiklagenævnet (BEK nr. 1555 af 2025; præcis titel ikke set)"]:::retsakt
    bek_klagenaevnet_for_udbud["Bekendtgørelse om Klagenævnet for Udbud (klagenævnsbekendtgørelsen)"]:::retsakt
    bek_konkurrenceankenaevnet["Bekendtgørelse om Konkurrenceankenævnet"]:::retsakt
    bek_raad_el_og_gasteknisk_sikkerhed["Bekendtgørelse om Rådet for El- og Gasteknisk Sikkerhed (2024)"]:::retsakt
    bek_vandsektortilsynet["Bekendtgørelse om Vandsektortilsynets virksomhed"]:::retsakt
    bek_autorisation["Bekendtgørelse om autorisation og drift af virksomhed på el-, vvs- og kloakinstallationsområdet"]:::retsakt
    bek_ekn_forretningsorden["Bekendtgørelse om forretningsorden for Energiklagenævnet"]:::retsakt
    bek_mfkn_forretningsorden["Bekendtgørelse om forretningsorden for Miljø- og Fødevareklagenævnet"]:::retsakt
    bek_pkn_forretningsorden["Bekendtgørelse om forretningsorden for Planklagenævnet (BEK nr. 20 af 11/01/2024)"]:::retsakt
    bek_pkn_gebyr["Bekendtgørelse om gebyr for indbringelse af klager for Planklagenævnet (BEK nr. 108 af 28/01/2017)"]:::retsakt
    bek_ekn_gebyr["Bekendtgørelse om gebyr ved indbringelse af en klage for Energiklagenævnet (BEK nr 568 af 24/06/2026)"]:::retsakt
    bek_co2_kvoter_henlaeggelse_erst["Bekendtgørelse om henlæggelse af visse beføjelser efter lov om CO2-kvoter til Erhvervsstyrelsen (ikrafttræden 1/1/2026)"]:::retsakt
    bek_elevatorer["Bekendtgørelse om indretning m.v. af elevatorer og sikkerhedskomponenter til elevatorer"]:::retsakt
    bek_personlige_vaernemidler_indretning["Bekendtgørelse om indretning m.v. af personlige værnemidler (BEK nr 210 af 14/03/2018)"]:::retsakt
    bek_trykbaerende_udstyr["Bekendtgørelse om indretning m.v. af trykbærende udstyr"]:::retsakt
    bek_fyrvaerkeri_krav["Bekendtgørelse om krav til fyrværkeri og andre pyrotekniske artikler (BEK nr. 1799 af 2021)"]:::retsakt
    bek_byggevarer_cpr2011["Bekendtgørelse om markedsføring og markedsovervågning af byggevarer (efter forordning 305/2011)"]:::retsakt
    bek_byggevarer_cpr2024["Bekendtgørelse om markedsføring og markedsovervågning af byggevarer efter den reviderede byggevareforordning"]:::retsakt
    bek_maskiner["Bekendtgørelse om maskiner"]:::retsakt
    bek_atex_produkter["Bekendtgørelse om produkter til anvendelse i en potentielt eksplosiv atmosfære (BEK nr. 811 af 03/06/2022)"]:::retsakt
    bek_drift_elanlaeg["Bekendtgørelse om sikkerhed for drift af elektriske anlæg"]:::retsakt
    bek_elmateriel["Bekendtgørelse om sikkerhed for elektrisk materiel (elmaterielbekendtgørelsen)"]:::retsakt
    bek_gasanlaeg["Bekendtgørelse om sikkerhed for gasanlæg"]:::retsakt
    bek_gasinstallationer["Bekendtgørelse om sikkerhed for gasinstallationer"]:::retsakt
    bek_gasmateriel["Bekendtgørelse om sikkerhed for gasmateriel"]:::retsakt
    bek_roerledninger_gas["Bekendtgørelse om sikkerhed for rørledninger til gas"]:::retsakt
    bek_elanlaeg["Bekendtgørelse om sikkerhed for udførelse af elektriske anlæg (elanlægsbekendtgørelsen)"]:::retsakt
    bek_elinstallationer["Bekendtgørelse om sikkerhed for udførelse og drift af elektriske installationer (elinstallationsbekendtgørelsen)"]:::retsakt
    bek_maskinforordning_supplerende["Bekendtgørelse om supplerende bestemmelser til maskinforordningen"]:::retsakt
    plan_fingerplan_2019["Fingerplan 2019 – Landsplandirektiv for hovedstadsområdets planlægning (BEK nr. 312/2019)"]:::retsakt
    bek_fyrvaerkeri["Fyrværkeribekendtgørelsen (bekendtgørelse om indførsel, fremstilling, opbevaring, overdragelse, erhvervelse og anvendelse af fyrværkeri og andre pyrotekniske artikler), BEK nr. 1798 af 09/09/2021"]:::retsakt
    lov_fyrvaerkeriloven["Fyrværkeriloven (lov om fyrværkeri og andre pyrotekniske artikler)"]:::retsakt
    lov_gassikkerhedsloven["Gassikkerhedsloven (lov om sikkerhed ved gasanlæg, gasinstallationer og rørledninger til gas)"]:::retsakt
    lov_konkurrenceloven["Konkurrenceloven"]:::retsakt
    plan_detailhandel_hovedstadsomraadet["Landsplandirektiv for detailhandel i hovedstadsområdet (bekendtgørelse af 11/12/2018, eli/lta/2018/1488)"]:::retsakt
    lov_co2_kvoteloven["Lov om CO2-kvoter (CO2-kvoteloven), LOV nr 1767 af 28/12/2023"]:::retsakt
    lov_energiklagenaevnsloven["Lov om Energiklagenævnet"]:::retsakt
    lov_energinetloven["Lov om Energinet"]:::retsakt
    lov_erhvervsankenaevnsloven["Lov om Erhvervsankenævnet"]:::retsakt
    lov_klagenaevn_for_udbud_loven["Lov om Klagenævnet for Udbud (tidl. lov om håndhævelse af udbudsreglerne m.v.)"]:::retsakt
    lov_mfkn_loven["Lov om Miljø- og Fødevareklagenævnet"]:::retsakt
    lov_planklagenaevnsloven["Lov om Planklagenævnet"]:::retsakt
    lov_forbrugerklageloven["Lov om alternativ tvistløsning i forbindelse med forbrugerklager (forbrugerklageloven)"]:::retsakt
    lov_undergrundsloven["Lov om anvendelse af Danmarks undergrund (undergrundsloven), LBK nr 1461 af 29/11/2023"]:::retsakt
    lov_autorisationsloven["Lov om autorisation af virksomheder på el-, vvs- og kloakinstallationsområdet (autorisationsloven)"]:::retsakt
    lov_elforsyningsloven["Lov om elforsyning (elforsyningsloven)"]:::retsakt
    lov_masteloven["Lov om etablering og fælles udnyttelse af master til radiokommunikationsformål m.v. (masteloven)"]:::retsakt
    lov_energimaerkningsloven["Lov om fremme af energibesparelser i bygninger"]:::retsakt
    lov_ve_loven["Lov om fremme af vedvarende energi (VE-loven)"]:::retsakt
    lov_tilbudsloven["Lov om indhentning af tilbud i bygge- og anlægssektoren (tilbudsloven)"]:::retsakt
    lov_kystbeskyttelsesloven["Lov om kystbeskyttelse (kystbeskyttelsesloven)"]:::retsakt
    lov_lejeloven["Lov om leje (lejeloven)"]:::retsakt
    lov_erhvervslejeloven["Lov om leje af erhvervslokaler m.v. (erhvervslejeloven)"]:::retsakt
    lov_miljoebeskyttelsesloven["Lov om miljøbeskyttelse (miljøbeskyttelsesloven)"]:::retsakt
    lov_ecodesignloven["Lov om miljøvenligt design af energirelaterede produkter (ecodesignloven)"]:::retsakt
    lov_miljoevurderingsloven["Lov om miljøvurderinger (miljøvurderingsloven, VVM/SMV)"]:::retsakt
    lov_naturbeskyttelsesloven["Lov om naturbeskyttelse (naturbeskyttelsesloven)"]:::retsakt
    lov_planloven["Lov om planlægning (planloven)"]:::retsakt
    lov_produktloven["Lov om produkter og markedsovervågning (produktloven)"]:::retsakt
    lov_elsikkerhedsloven["Lov om sikkerhed for elektriske anlæg og elektriske installationer (elsikkerhedsloven)"]:::retsakt
    lov_vandloebsloven["Lov om vandløb (vandløbsloven)"]:::retsakt
    lov_vandsektorloven["Lov om vandsektorens organisering og økonomiske forhold (vandsektorloven)"]:::retsakt
    lov_varmeforsyningsloven["Lov om varmeforsyning (varmeforsyningsloven)"]:::retsakt
    lov_museumsloven["Museumsloven"]:::retsakt
    bek_risiko["Risikobekendtgørelsen (bekendtgørelse om kontrol med risikoen for større uheld med farlige stoffer)"]:::retsakt
    vejl_sik_vejledninger["Sikkerhedsstyrelsens/Erhvervsstyrelsens vejledninger og fortolkninger (el, gas, VVS, kloak, asbest, autorisation)"]:::retsakt
    vejl_fingerplan_2019["Vejledning om Fingerplan 2019 (VEJ nr. 9281 af 27/03/2019)"]:::retsakt
    vejl_henvisning_standarder["Vejledning om henvisning til visse internationale standarder i lovgivning (Erhvervsstyrelsen)"]:::retsakt
    vejl_planloven_vejledninger["Vejledninger til planloven (samling)"]:::retsakt
    min_erhverv -.->|delegation| sty_erhvervsstyrelsen
    min_erhverv -.->|delegation| sty_sikkerhedsstyrelsen
    bek_drift_elanlaeg -->|henviser_til| std_ds_en_50110
    bek_ekn_gebyr -.->|henviser_til| lov_undergrundsloven
    bek_ekn_gebyr -.->|henviser_til| naevn_energiklagenaevnet
    bek_elinstallationer -->|henviser_til| std_ds_hd_60364
    bv_tekniq_vejledninger -->|henviser_til| lov_autorisationsloven
    kilde_ekn_afgoerelser -->|henviser_til| lov_energimaerkningsloven
    kilde_ekn_afgoerelser -->|henviser_til| lov_varmeforsyningsloven
    kilde_mfkn_afgoerelser -.->|henviser_til| lov_kystbeskyttelsesloven
    kilde_mfkn_afgoerelser -->|henviser_til| lov_miljoebeskyttelsesloven
    kilde_mfkn_afgoerelser -.->|henviser_til| lov_miljoevurderingsloven
    kilde_mfkn_afgoerelser -->|henviser_til| lov_naturbeskyttelsesloven
    kilde_mfkn_afgoerelser -->|henviser_til| lov_vandloebsloven
    kilde_mrf -->|henviser_til| kilde_mfkn_afgoerelser
    kilde_mrf -->|henviser_til| kilde_pkn_afgoerelser
    kilde_pkn_afgoerelser -.->|henviser_til| eu_dir_2011_92
    kilde_pkn_afgoerelser -->|henviser_til| lov_miljoevurderingsloven
    kilde_pkn_afgoerelser -->|henviser_til| lov_planloven
    lov_energiklagenaevnsloven -->|henviser_til| lov_elforsyningsloven
    lov_energiklagenaevnsloven -->|henviser_til| lov_energimaerkningsloven
    lov_energiklagenaevnsloven -->|henviser_til| lov_energinetloven
    lov_energiklagenaevnsloven -->|henviser_til| lov_varmeforsyningsloven
    lov_energiklagenaevnsloven -->|henviser_til| lov_ve_loven
    lov_erhvervslejeloven -.->|henviser_til| lov_lejeloven
    lov_gassikkerhedsloven -.->|henviser_til| eu_reg_2016_426
    lov_klagenaevn_for_udbud_loven -->|henviser_til| lov_tilbudsloven
    lov_produktloven -->|henviser_til| lov_visse_produkter
    vejl_sik_vejledninger -.->|henviser_til| lov_elsikkerhedsloven
    bek_byggevarer_cpr2011 -->|hjemmel_for| sty_erhvervsstyrelsen
    bek_byggevarer_cpr2024 -.->|hjemmel_for| sty_erhvervsstyrelsen
    bek_raad_el_og_gasteknisk_sikkerhed -->|hjemmel_for| raad_el_og_gasteknisk_sikkerhed
    bek_vandsektortilsynet -->|hjemmel_for| tilsyn_vandsektortilsynet
    lov_arbejdsmiljoeloven -->|hjemmel_for| sty_erhvervsstyrelsen
    lov_autorisationsloven -->|hjemmel_for| bek_autorisation
    lov_autorisationsloven -.->|hjemmel_for| sty_erhvervsstyrelsen
    lov_co2_kvoteloven -->|hjemmel_for| bek_co2_kvoter_henlaeggelse_erst
    lov_co2_kvoteloven -->|hjemmel_for| sty_erhvervsstyrelsen
    lov_ecodesignloven -.->|hjemmel_for| sty_erhvervsstyrelsen
    lov_ecodesignloven -->|hjemmel_for| sty_sikkerhedsstyrelsen
    lov_elforsyningsloven -->|hjemmel_for| naevn_energiklagenaevnet
    lov_elsikkerhedsloven -->|hjemmel_for| bek_drift_elanlaeg
    lov_elsikkerhedsloven -->|hjemmel_for| bek_elanlaeg
    lov_elsikkerhedsloven -->|hjemmel_for| bek_elinstallationer
    lov_elsikkerhedsloven -->|hjemmel_for| bek_raad_el_og_gasteknisk_sikkerhed
    lov_elsikkerhedsloven -->|hjemmel_for| raad_el_og_gasteknisk_sikkerhed
    lov_elsikkerhedsloven -->|hjemmel_for| sty_erhvervsstyrelsen
    lov_energiklagenaevnsloven -->|hjemmel_for| bek_ekn_forretningsorden
    lov_energiklagenaevnsloven -->|hjemmel_for| naevn_energiklagenaevnet
    lov_erhvervsankenaevnsloven -->|hjemmel_for| naevn_erhvervsankenaevnet
    lov_fyrvaerkeriloven -->|hjemmel_for| bek_fyrvaerkeri
    lov_fyrvaerkeriloven -->|hjemmel_for| bek_risiko
    lov_fyrvaerkeriloven -->|hjemmel_for| kommune_alle
    lov_fyrvaerkeriloven -->|hjemmel_for| sty_erhvervsstyrelsen
    lov_gassikkerhedsloven -->|hjemmel_for| bek_gasanlaeg
    lov_gassikkerhedsloven -->|hjemmel_for| bek_gasinstallationer
    lov_gassikkerhedsloven -.->|hjemmel_for| bek_gasmateriel
    lov_gassikkerhedsloven -->|hjemmel_for| bek_roerledninger_gas
    lov_gassikkerhedsloven -->|hjemmel_for| sty_erhvervsstyrelsen
    lov_klagenaevn_for_udbud_loven -->|hjemmel_for| bek_klagenaevnet_for_udbud
    lov_klagenaevn_for_udbud_loven -->|hjemmel_for| naevn_klagenaevnet_for_udbud
    lov_konkurrenceloven -->|hjemmel_for| bek_konkurrenceankenaevnet
    lov_konkurrenceloven -->|hjemmel_for| raad_konkurrenceraadet
    lov_konkurrenceloven -->|hjemmel_for| sty_konkurrence_og_forbrugerstyrelsen
    lov_masteloven -->|hjemmel_for| naevn_planklagenaevnet
    lov_mfkn_loven -->|hjemmel_for| bek_klagenaevn_sagsbehandlingslofter
    lov_mfkn_loven -->|hjemmel_for| bek_mfkn_forretningsorden
    lov_mfkn_loven -->|hjemmel_for| naevn_miljoe_og_foedevareklagenaevnet
    lov_miljoevurderingsloven -->|hjemmel_for| naevn_planklagenaevnet
    lov_museumsloven -->|hjemmel_for| naevn_miljoe_og_foedevareklagenaevnet
    lov_planklagenaevnsloven -->|hjemmel_for| bek_pkn_forretningsorden
    lov_planklagenaevnsloven -->|hjemmel_for| bek_pkn_gebyr
    lov_planklagenaevnsloven -->|hjemmel_for| naevn_planklagenaevnet
    lov_planloven -->|hjemmel_for| naevn_planklagenaevnet
    lov_produktloven -->|hjemmel_for| bek_atex_produkter
    lov_produktloven -->|hjemmel_for| bek_elmateriel
    lov_produktloven -->|hjemmel_for| bek_maskiner
    lov_produktloven -->|hjemmel_for| sty_erhvervsstyrelsen
    lov_vandsektorloven -->|hjemmel_for| tilsyn_vandsektortilsynet
    lov_varmeforsyningsloven -->|hjemmel_for| naevn_energiklagenaevnet
    lov_ve_loven -->|hjemmel_for| naevn_energiklagenaevnet
    lov_visse_produkter -->|hjemmel_for| bek_elevatorer
    lov_visse_produkter -->|hjemmel_for| bek_personlige_vaernemidler_indretning
    bek_atex_produkter -.->|implementerer_EU| eu_dir_2014_34
    bek_elevatorer -->|implementerer_EU| eu_dir_2014_33
    bek_elmateriel -->|implementerer_EU| eu_dir_2014_35
    bek_fyrvaerkeri -.->|implementerer_EU| eu_dir_2013_29
    bek_fyrvaerkeri_krav -.->|implementerer_EU| eu_dir_2013_29
    bek_gasmateriel -.->|implementerer_EU| eu_reg_2016_426
    bek_maskiner -->|implementerer_EU| eu_dir_2006_42
    bek_maskinforordning_supplerende -->|implementerer_EU| eu_reg_2023_1230
    bek_personlige_vaernemidler_indretning -->|implementerer_EU| eu_reg_2016_425
    bek_trykbaerende_udstyr -->|implementerer_EU| eu_dir_2014_68
    lov_autorisationsloven -.->|implementerer_EU| eu_dir_2005_36
    lov_gassikkerhedsloven -.->|implementerer_EU| eu_reg_2016_426
    lov_klagenaevn_for_udbud_loven -->|implementerer_EU| eu_dir_2007_66
    lov_produktloven -->|implementerer_EU| eu_reg_2019_1020
    dom_byretterne -->|klageinstans| naevn_energiklagenaevnet
    dom_byretterne -->|klageinstans| naevn_miljoe_og_foedevareklagenaevnet
    dom_byretterne -->|klageinstans| naevn_planklagenaevnet
    dom_domstolene -->|klageinstans| naevn_energiklagenaevnet
    dom_domstolene -.->|klageinstans| naevn_klagenaevnet_for_udbud
    dom_domstolene -->|klageinstans| naevn_miljoe_og_foedevareklagenaevnet
    naevn_energiklagenaevnet -->|klageinstans| kommune_alle
    naevn_energiklagenaevnet -->|klageinstans| org_energinet
    naevn_energiklagenaevnet -->|klageinstans| sty_energistyrelsen
    naevn_energiklagenaevnet -->|klageinstans| tilsyn_forsyningstilsynet
    naevn_erhvervsankenaevnet -->|klageinstans| sty_erhvervsstyrelsen
    naevn_klagenaevnet_for_udbud -.->|klageinstans| kommune_alle
    naevn_konkurrenceankenaevnet -->|klageinstans| sty_konkurrence_og_forbrugerstyrelsen
    naevn_konkurrenceankenaevnet -->|klageinstans| tilsyn_vandsektortilsynet
    naevn_miljoe_og_foedevareklagenaevnet -->|klageinstans| kommune_alle
    naevn_miljoe_og_foedevareklagenaevnet -->|klageinstans| min_by_land_og_transport
    naevn_miljoe_og_foedevareklagenaevnet -->|klageinstans| naevn_fredningsnaevn
    naevn_miljoe_og_foedevareklagenaevnet -->|klageinstans| region_alle
    naevn_miljoe_og_foedevareklagenaevnet -->|klageinstans| sty_groen_arealomlaegning_og_vandmiljoe
    naevn_miljoe_og_foedevareklagenaevnet -->|klageinstans| sty_kystdirektoratet
    naevn_miljoe_og_foedevareklagenaevnet -->|klageinstans| sty_miljoestyrelsen
    naevn_planklagenaevnet -->|klageinstans| kommune_alle
    naevn_planklagenaevnet -.->|klageinstans| sty_plan_og_landdistriktsstyrelsen
    naevn_taksationskommissionen -->|klageinstans| naevn_miljoe_og_foedevareklagenaevnet
    min_erhverv -->|ressortansvar| bek_atex_produkter
    min_erhverv -->|ressortansvar| bek_fyrvaerkeri
    min_erhverv -->|ressortansvar| bek_maskiner
    min_erhverv -.->|ressortansvar| lov_autorisationsloven
    min_erhverv -->|ressortansvar| lov_elsikkerhedsloven
    min_erhverv -.->|ressortansvar| lov_energiklagenaevnsloven
    min_erhverv -->|ressortansvar| lov_erhvervsankenaevnsloven
    min_erhverv -.->|ressortansvar| lov_erhvervslejeloven
    min_erhverv -.->|ressortansvar| lov_fyrvaerkeriloven
    min_erhverv -.->|ressortansvar| lov_gassikkerhedsloven
    min_erhverv -->|ressortansvar| lov_klagenaevn_for_udbud_loven
    min_erhverv -.->|ressortansvar| lov_konkurrenceloven
    min_erhverv -.->|ressortansvar| lov_mfkn_loven
    min_erhverv -.->|ressortansvar| lov_planklagenaevnsloven
    min_erhverv -.->|ressortansvar| lov_produktloven
    min_erhverv -->|ressortansvar| lov_tilbudsloven
    min_erhverv -.->|ressortansvar| naevn_energiklagenaevnet
    min_erhverv -.->|ressortansvar| naevn_erhvervsankenaevnet
    min_erhverv -.->|ressortansvar| naevn_klagenaevnet_for_udbud
    min_erhverv -.->|ressortansvar| naevn_konkurrenceankenaevnet
    min_erhverv -.->|ressortansvar| naevn_miljoe_og_foedevareklagenaevnet
    min_erhverv -.->|ressortansvar| naevn_planklagenaevnet
    min_erhverv -->|ressortansvar| raad_el_og_gasteknisk_sikkerhed
    min_erhverv -->|ressortansvar| sty_erhvervsstyrelsen
    min_erhverv -.->|ressortansvar| sty_konkurrence_og_forbrugerstyrelsen
    min_erhverv -->|ressortansvar| sty_naevnenes_hus
    min_erhverv -->|ressortansvar| sty_sikkerhedsstyrelsen
    min_erhverv -->|ressortansvar| tilsyn_vandsektortilsynet
    ombud_folketingets_ombudsmand -.->|tilsyn| naevn_energiklagenaevnet
    ombud_folketingets_ombudsmand -.->|tilsyn| naevn_erhvervsankenaevnet
    ombud_folketingets_ombudsmand -->|tilsyn| naevn_konkurrenceankenaevnet
    ombud_folketingets_ombudsmand -->|tilsyn| naevn_miljoe_og_foedevareklagenaevnet
    ombud_folketingets_ombudsmand -->|tilsyn| naevn_planklagenaevnet
    ombud_folketingets_ombudsmand -.->|tilsyn| sty_erhvervsstyrelsen
    ombud_folketingets_ombudsmand -->|tilsyn| sty_naevnenes_hus
    sty_erhvervsstyrelsen -.->|tilsyn| bek_atex_produkter
    sty_erhvervsstyrelsen -->|tilsyn| bek_byggevarer_cpr2024
    sty_erhvervsstyrelsen -->|tilsyn| bek_fyrvaerkeri
    sty_erhvervsstyrelsen -->|tilsyn| eu_dir_2006_42
    sty_erhvervsstyrelsen -->|tilsyn| eu_dir_2014_35
    sty_erhvervsstyrelsen -->|tilsyn| eu_reg_2011_305
    sty_erhvervsstyrelsen -->|tilsyn| eu_reg_2016_425
    sty_erhvervsstyrelsen -.->|tilsyn| eu_reg_2016_426
    sty_erhvervsstyrelsen -->|tilsyn| eu_reg_2023_1230
    sty_erhvervsstyrelsen -->|tilsyn| eu_reg_2024_3110
    sty_sikkerhedsstyrelsen -->|tilsyn| eu_reg_2017_1369
    min_erhverv -->|udsteder| bek_co2_kvoter_henlaeggelse_erst
    min_erhverv -->|udsteder| bek_ekn_forretningsorden
    min_erhverv -->|udsteder| bek_klagenaevn_sagsbehandlingslofter
    min_erhverv -->|udsteder| bek_pkn_forretningsorden
    min_erhverv -->|udsteder| bek_pkn_gebyr
    min_erhverv -->|udsteder| plan_detailhandel_hovedstadsomraadet
    min_erhverv -->|udsteder| plan_fingerplan_2019
    min_erhverv -->|udsteder| vejl_fingerplan_2019
    naevn_byggeklageenheden -->|udsteder| kilde_naevneneshus_afgoerelser
    naevn_energiklagenaevnet -->|udsteder| kilde_ekn_afgoerelser
    naevn_energiklagenaevnet -->|udsteder| kilde_naevneneshus_afgoerelser
    naevn_erhvervsankenaevnet -->|udsteder| kilde_ean_afgoerelser
    naevn_miljoe_og_foedevareklagenaevnet -->|udsteder| kilde_mfkn_afgoerelser
    naevn_planklagenaevnet -->|udsteder| kilde_pkn_afgoerelser
    sty_arbejdstilsynet -.->|udsteder| bek_elevatorer
    sty_erhvervsstyrelsen -.->|udsteder| bek_trykbaerende_udstyr
    sty_erhvervsstyrelsen -->|udsteder| kilde_autorisationsregister
    sty_erhvervsstyrelsen -->|udsteder| kilde_sik_dk
    sty_erhvervsstyrelsen -->|udsteder| kilde_virk_nye_regler
    sty_erhvervsstyrelsen -->|udsteder| vejl_henvisning_standarder
    sty_erhvervsstyrelsen -->|udsteder| vejl_planloven_vejledninger
    sty_erhvervsstyrelsen -->|udsteder| vejl_sik_vejledninger
    sty_naevnenes_hus -->|udsteder| kilde_bke_afgoerelser
    sty_naevnenes_hus -->|udsteder| kilde_ekn_afgoerelser
    sty_naevnenes_hus -->|udsteder| kilde_mfkn_afgoerelser
    sty_naevnenes_hus -->|udsteder| kilde_naevneneshus_afgoerelser
    sty_naevnenes_hus -->|udsteder| kilde_pkn_afgoerelser
    sty_sikkerhedsstyrelsen -->|udsteder| bek_atex_produkter
    sty_sikkerhedsstyrelsen -->|udsteder| bek_autorisation
    sty_sikkerhedsstyrelsen -.->|udsteder| bek_elinstallationer
    sty_sikkerhedsstyrelsen -.->|udsteder| bek_gasinstallationer
    sty_sikkerhedsstyrelsen -->|udsteder| bek_gasmateriel
    sty_sikkerhedsstyrelsen -->|udsteder| bek_maskiner
    sty_sikkerhedsstyrelsen -->|udsteder| bek_maskinforordning_supplerende
    sty_sikkerhedsstyrelsen -->|udsteder| kilde_sik_dk
    lov_produktloven -->|hjemmel_for| bek_fyrvaerkeri_krav
    min_erhverv -.->|ressortansvar| lov_forbrugerklageloven
    lov_forbrugerklageloven -.->|hjemmel_for| org_det_finansielle_ankenaevn
    lov_forbrugerklageloven -->|hjemmel_for| org_ankenaevnet_for_fondsmaeglerselskaber
    naevn_erhvervsankenaevnet -.->|klageinstans| sty_finanstilsynet
    naevn_erhvervsankenaevnet -.->|klageinstans| org_finansiel_stabilitet
    bek_risiko -->|implementerer_EU| eu_dir_2012_18
```

[← Overblik](oversigt.md)
