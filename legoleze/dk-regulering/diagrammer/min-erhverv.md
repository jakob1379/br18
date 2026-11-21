# Erhvervsministeriet

> Genereret af `scripts/build.py` fra `registry.yaml` (dato 2026-10-28). Redigér ikke i hånden.
> Fuldt optrukne pile = `verificeret`; stiplede = `sandsynlig`/`ukendt`. Grå stiplede bokse = nedlagt/omdøbt/ophævet.

Noder: 231 · kanter: 386

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
    eu_dir_2015_849["Direktiv (EU) 2015/849 om forebyggende foranstaltninger mod anvendelse af det finansielle system til hvidvask af penge eller finansiering af terrorisme (4. hvidvaskdirektiv)"]:::eu
    eu_dir_1999_92["Direktiv 1999/92/EF om minimumsforskrifter for sikkerhed og sundhed for arbejdstagere, som kan udsættes for risiko for eksplosiv atmosfære (ATEX-brugerdirektivet)"]:::eu
    eu_dir_2000_54["Direktiv 2000/54/EF om beskyttelse af arbejdstagerne mod risici i forbindelse med at være udsat for biologiske agenser under arbejdet"]:::eu
    eu_dir_2002_44["Direktiv 2002/44/EF om fysiske agenser (vibrationer)"]:::eu
    eu_dir_2003_10["Direktiv 2003/10/EF om fysiske agenser (støj)"]:::eu
    eu_dir_2004_37["Direktiv 2004/37/EF om beskyttelse af arbejdstagerne mod risici for at blive udsat for kræftfremkaldende stoffer, mutagener eller reproduktionstoksiske stoffer under arbejdet (CMRD)"]:::eu
    eu_dir_2006_42["Direktiv 2006/42/EF om maskiner (maskindirektivet)"]:::eu
    eu_dir_2009_104["Direktiv 2009/104/EF om minimumsforskrifter for arbejdstagernes brug af arbejdsudstyr (arbejdsudstyrsdirektivet)"]:::eu
    eu_dir_2009_148["Direktiv 2009/148/EF om beskyttelse af arbejdstagerne mod risici for asbestpåvirkning"]:::eu
    eu_dir_2011_92["Direktiv 2011/92/EU om vurdering af visse offentlige og private projekters indvirkning på miljøet (VVM)"]:::eu
    eu_dir_2013_29["Direktiv 2013/29/EU om tilgængeliggørelse af pyrotekniske artikler på markedet (omarbejdning)"]:::eu
    eu_dir_2014_33["Direktiv 2014/33/EU om elevatorer og sikkerhedskomponenter til elevatorer"]:::eu
    eu_dir_2014_34["Direktiv 2014/34/EU om materiel og sikringssystemer til anvendelse i eksplosionsfarlig atmosfære (ATEX-produktdirektivet)"]:::eu
    eu_dir_2014_68["Direktiv 2014/68/EU om trykbærende udstyr (PED)"]:::eu
    eu_dir_2020_2184["Drikkevandsdirektivet – direktiv (EU) 2020/2184 af 16. december 2020 (omarbejdning)"]:::eu
    eu_dir_2005_36["Europa-Parlamentets og Rådets direktiv 2005/36/EF af 7. september 2005 om anerkendelse af erhvervsmæssige kvalifikationer"]:::eu
    eu_dir_2007_66["Europa-Parlamentets og Rådets direktiv 2007/66/EF om ændring af Rådets direktiv 89/665/EØF og 92/13/EØF om effektiviteten af klageprocedurerne vedrørende indgåelse af offentlige kontrakter (håndhævelsesdirektivet)"]:::eu
    eu_reg_2016_425["Forordning (EU) 2016/425 om personlige værnemidler (PPE-forordningen)"]:::eu
    eu_reg_2017_1369["Forordning (EU) 2017/1369 om opstilling af en ramme for energimærkning (energimærkningsforordningen for produkter)"]:::eu
    eu_reg_2023_1230["Forordning (EU) 2023/1230 om maskiner (maskinforordningen)"]:::eu
    eu_reg_2016_426["Gasapparatforordningen (EU) 2016/426 (GAR)"]:::eu
    eu_dir_2014_35["Lavspændingsdirektivet 2014/35/EU"]:::eu
    eu_reg_2019_1020["Markedsovervågningsforordningen (EU) 2019/1020"]:::eu
    eu_reg_2024_3110["Revideret byggevareforordning (EU) 2024/3110"]:::eu
    eu_dir_1989_391["Rådets direktiv 89/391/EØF (rammedirektivet om sikkerhed og sundhed under arbejdet)"]:::eu
    eu_dir_1989_656["Rådets direktiv 89/656/EØF om minimumsforskrifter for arbejdstagernes brug af personlige værnemidler"]:::eu
    eu_dir_1994_33["Rådets direktiv 94/33/EF om beskyttelse af unge på arbejdspladsen"]:::eu
    eu_dir_1998_24["Rådets direktiv 98/24/EF om beskyttelse af arbejdstagernes sikkerhed og sundhed under arbejdet mod risici i forbindelse med kemiske agenser"]:::eu
    eu_dir_2012_18["Seveso III-direktivet (direktiv 2012/18/EU om kontrol med risikoen for større uheld med farlige stoffer)"]:::eu
    sty_arbejdstilsynet["Arbejdstilsynet"]:::instans
    sty_den_maritime_havarikommission["Den Maritime Havarikommission"]:::instans
    raad_det_veterinaere_sundhedsraad["Det Veterinære Sundhedsråd"]:::instans
    org_energinet["Energinet"]:::instans
    sty_energistyrelsen["Energistyrelsen"]:::instans
    sty_erhvervsstyrelsen["Erhvervsstyrelsen"]:::instans
    org_finansiel_stabilitet["Finansiel Stabilitet"]:::instans
    sty_finanstilsynet["Finanstilsynet"]:::instans
    tilsyn_forsyningstilsynet["Forsyningstilsynet"]:::instans
    sty_faerdselsstyrelsen["Færdselsstyrelsen"]:::instans
    sty_foedevarestyrelsen["Fødevarestyrelsen"]:::instans
    kommune_alle["Kommunerne (98 kommunalbestyrelser)"]:::instans
    sty_konkurrence_og_forbrugerstyrelsen["Konkurrence- og Forbrugerstyrelsen"]:::instans
    raad_konkurrenceraadet["Konkurrencerådet"]:::instans
    sty_kystdirektoratet["Kystdirektoratet"]:::instans
    sty_miljoestyrelsen["Miljøstyrelsen"]:::instans
    sty_naevnenes_hus["Nævnenes Hus"]:::instans
    sty_patent_og_varemaerkestyrelsen["Patent- og Varemærkestyrelsen"]:::instans
    sty_plan_og_landdistriktsstyrelsen["Plan- og Landdistriktsstyrelsen"]:::instans
    region_alle["Regionerne (5 regionsråd)"]:::instans
    raad_el_og_gasteknisk_sikkerhed["Rådet for El- og Gasteknisk Sikkerhed"]:::instans
    raad_skibstilsynsraadet["Skibstilsynsrådet"]:::instans
    sty_groen_arealomlaegning_og_vandmiljoe["Styrelsen for Grøn Arealomlægning og Vandmiljø (SGAV)"]:::instans
    sty_soefartsstyrelsen["Søfartsstyrelsen"]:::instans
    org_udbetaling_danmark["Udbetaling Danmark"]:::instans
    tilsyn_vandsektortilsynet["Vandsektortilsynet"]:::instans
    org_ankenaevnet_for_bus_tog_og_metro["Ankenævnet for Bus, Tog og Metro"]:::kilde
    org_ankenaevnet_for_fondsmaeglerselskaber["Ankenævnet for Fondsmæglerselskaber"]:::kilde
    org_ankenaevnet_for_forsikring["Ankenævnet for Forsikring"]:::kilde
    kilde_apv_afgoerelser["Ankenævnet for Patenter og Varemærkers afgørelsesportal (apv.naevneneshus.dk)"]:::kilde
    kilde_autorisationsregister["Autorisationsregister (el, VVS, kloak, gas, asbest)"]:::kilde
    kilde_bke_afgoerelser["Byggeklageenhedens afgørelser"]:::kilde
    org_byggeriets_ankenaevn["Byggeriets Ankenævn"]:::kilde
    std_ds_en_50110["DS/EN 50110 Drift af elektriske anlæg"]:::kilde
    std_ds_hd_60364["DS/HD 60364 Elektriske lavspændingsinstallationer"]:::kilde
    kilde_dmaib_rapporter["Den Maritime Havarikommissions rapporter (dmaib.dk)"]:::kilde
    org_det_finansielle_ankenaevn["Det finansielle ankenævn"]:::kilde
    kilde_dnfe_kendelser["Disciplinærnævnet for Ejendomsmæglere – kendelser (dnfe.naevneneshus.dk)"]:::kilde
    kilde_ekn_afgoerelser["Energiklagenævnets afgørelser (ekn.naevneneshus.dk)"]:::kilde
    kilde_ean_afgoerelser["Erhvervsankenævnets kendelser (ean.naevneneshus.dk)"]:::kilde
    kilde_findsmiley["Find Smiley (fødevarekontrollens kontrolrapporter)"]:::kilde
    kilde_fkn_afgoerelser["Forbrugerklagenævnets afgørelser (fkn.naevneneshus.dk)"]:::kilde
    kilde_forbrugerombudsmanden_retningslinjer["Forbrugerombudsmandens retningslinjer og vejledninger (forbrugerombudsmanden.dk)"]:::kilde
    kilde_forbrugerombudsmanden_sager["Forbrugerombudsmandens sager (Find sager, forbrugerombudsmanden.dk)"]:::kilde
    org_godkendte_private_ankenaevn["Godkendte private ankenævn (godkendelsesordningen i forbrugerklagelovens kapitel 3)"]:::kilde
    org_godkendte_revisorer["Godkendte revisorer og revisionsvirksomheder"]:::kilde
    kilde_mfkn_afgoerelser["MFKN afgørelsesportal (mfkn.naevneneshus.dk)"]:::kilde
    kilde_meddelelser_fra_soefartsstyrelsen["Meddelelser fra Søfartsstyrelsen (tekniske forskrifter A, B, E, F)"]:::kilde
    kilde_mrf["Miljøretlig Forskningsportal (MRF), Københavns Universitet"]:::kilde
    kilde_naevneneshus_afgoerelser["Nævnenes Hus – afgørelser fra øvrige nævn (Energiklagenævnet, Byggeklageenheden, Erhvervsankenævnet m.fl.)"]:::kilde
    kilde_godkendte_private_ankenaevn_liste["Nævnenes Hus: oversigt over godkendte private ankenævn (naevneneshus.dk)"]:::kilde
    kilde_pkn_afgoerelser["Planklagenævnets afgørelser"]:::kilde
    kilde_rn_kendelser["Revisornævnets kendelser (rn.naevneneshus.dk)"]:::kilde
    kilde_soefartsstyrelsen_regler["Søfartsstyrelsens regler og bekendtgørelser (soefartsstyrelsen.dk)"]:::kilde
    bv_tekniq_vejledninger["TEKNIQ's branchevejledninger (bl.a. om overtrædelse af autorisationsloven og elektronisk sameksistens/EMC)"]:::kilde
    kilde_teleklagenaevn_afgoerelser["Teleklagenævnets afgørelsesportal"]:::kilde
    kilde_tvistighedsnaevnet_kendelser["Tvistighedsnævnets afgørelsesportal (tvist.naevneneshus.dk)"]:::kilde
    kilde_sik_dk["sik.dk (Sikkerhedsstyrelsens site, nu Erhvervsstyrelsen)"]:::kilde
    kilde_virk_nye_regler["virk.dk – Nye regler (oversigt over nye erhvervsrettede regler)"]:::kilde
    naevn_ankenaevnet_patenter_varemaerker["Ankenævnet for Patenter og Varemærker"]:::klage
    naevn_ankenaevnet_for_soefartsforhold["Ankenævnet for Søfartsforhold"]:::klage
    naevn_ankenaevnet_paa_energiomraadet["Ankenævnet på Energiområdet"]:::klage
    naevn_ankenaevn_oplaeringsvirksomheder["Ankenævnet vedrørende Oplæringsvirksomheder (tidl. Ankenævnet vedrørende Praktikvirksomheder)"]:::klage
    naevn_byggeklageenheden["Byggeklageenheden"]:::klage
    dom_byretterne["Byretterne"]:::klage
    naevn_bygningssagkyndige["Disciplinær- og klagenævnet for beskikkede bygningssagkyndige"]:::klage
    naevn_disciplinaernaevnet_ejendomsmaeglere["Disciplinærnævnet for Ejendomsmæglere"]:::klage
    dom_domstolene["Domstolene (byret, landsret, Højesteret)"]:::klage
    naevn_energiklagenaevnet["Energiklagenævnet"]:::klage
    naevn_erhvervsankenaevnet["Erhvervsankenævnet"]:::klage
    ombud_folketingets_ombudsmand["Folketingets Ombudsmand"]:::klage
    naevn_forbrugerklagenaevnet["Forbrugerklagenævnet"]:::klage
    ombud_forbrugerombudsmanden["Forbrugerombudsmanden"]:::klage
    naevn_fredningsnaevn["Fredningsnævnene"]:::klage
    naevn_klagenaevnet_for_udbud["Klagenævnet for Udbud"]:::klage
    naevn_konkurrenceankenaevnet["Konkurrenceankenævnet"]:::klage
    naevn_miljoe_og_foedevareklagenaevnet["Miljø- og Fødevareklagenævnet"]:::klage
    naevn_planklagenaevnet["Planklagenævnet"]:::klage
    naevn_revisornaevnet["Revisornævnet"]:::klage
    naevn_taksationskommissionen["Taksationskommissionen (naturbeskyttelsesloven)"]:::klage
    naevn_teleankenaevnet["Teleankenævnet"]:::klage
    naevn_teleklagenaevnet["Teleklagenævnet"]:::klage
    naevn_tvistighedsnaevnet["Tvistighedsnævnet"]:::klage
    min_by_land_og_transport["By-, Land- og Transportministeriet"]:::ministerium
    min_klima_energi_og_forsyning["Klima-, Energi- og Forsyningsministeriet"]:::ministerium
    min_miljoe["Miljøministeriet"]:::ministerium
    lov_visse_produkter["Lov nr. 155 af 20/02/2013 om indretning m.v. af visse produkter (ophævet)"]:::nedlagt
    sty_sikkerhedsstyrelsen["Sikkerhedsstyrelsen (nedlagt)"]:::nedlagt
    lov_arbejdsmiljoeloven["Arbejdsmiljøloven"]:::retsakt
    bek_skibstilsynsraadet_forretningsorden["Bekendtgørelse af forretningsorden for Skibstilsynsrådet (BEK nr. 883 af 03/10/1996)"]:::retsakt
    bek_klagenaevn_sagsbehandlingslofter["Bekendtgørelse om (mål for) sagsbehandlingslofter i Miljø- og Fødevareklagenævnet, Planklagenævnet og Energiklagenævnet (BEK nr. 1555 af 2025; præcis titel ikke set)"]:::retsakt
    bek_ankenaevnet_patenter_varemaerker["Bekendtgørelse om Ankenævnet for Patenter og Varemærker"]:::retsakt
    bek_ankenaevn_praktikvirksomheder["Bekendtgørelse om Ankenævnet vedrørende Praktikvirksomheder (BEK nr. 1517 af 13/12/2007)"]:::retsakt
    bek_disciplinaernaevnet_ejendomsmaeglere["Bekendtgørelse om Disciplinærnævnet for Ejendomsmæglere"]:::retsakt
    bek_faerdselsstyrelsen_opgaver["Bekendtgørelse om Færdselsstyrelsens opgaver og beføjelser samt klageadgang (BEK nr. 787 af 2025)"]:::retsakt
    bek_klagenaevnet_for_udbud["Bekendtgørelse om Klagenævnet for Udbud (klagenævnsbekendtgørelsen)"]:::retsakt
    bek_konkurrenceankenaevnet["Bekendtgørelse om Konkurrenceankenævnet"]:::retsakt
    bek_revisornaevnet["Bekendtgørelse om Revisornævnet"]:::retsakt
    bek_raad_el_og_gasteknisk_sikkerhed["Bekendtgørelse om Rådet for El- og Gasteknisk Sikkerhed (2024)"]:::retsakt
    bek_teleklagenaevnets_virksomhed["Bekendtgørelse om Teleklagenævnets virksomhed"]:::retsakt
    bek_tvistighedsnaevnet["Bekendtgørelse om Tvistighedsnævnet"]:::retsakt
    bek_vandsektortilsynet["Bekendtgørelse om Vandsektortilsynets virksomhed"]:::retsakt
    bek_autorisation["Bekendtgørelse om autorisation og drift af virksomhed på el-, vvs- og kloakinstallationsområdet"]:::retsakt
    bek_forbrugerklager_naevnenes_hus["Bekendtgørelse om behandling af forbrugerklager i Nævnenes Hus samt Forbrugerklagenævnet (BEK nr. 65 af 16/01/2019)"]:::retsakt
    bek_bygningssagkyndige_naevn["Bekendtgørelse om disciplinær- og klagenævnet for beskikkede bygningssagkyndige"]:::retsakt
    bek_ankenaevn_soefartsforhold_forretningsorden["Bekendtgørelse om forretningsorden for Ankenævnet for Søfartsforhold (BEK nr. 1121 af 19/09/2013)"]:::retsakt
    bek_ekn_forretningsorden["Bekendtgørelse om forretningsorden for Energiklagenævnet"]:::retsakt
    bek_mfkn_forretningsorden["Bekendtgørelse om forretningsorden for Miljø- og Fødevareklagenævnet"]:::retsakt
    bek_pkn_forretningsorden["Bekendtgørelse om forretningsorden for Planklagenævnet (BEK nr. 20 af 11/01/2024)"]:::retsakt
    bek_pkn_gebyr["Bekendtgørelse om gebyr for indbringelse af klager for Planklagenævnet (BEK nr. 108 af 28/01/2017)"]:::retsakt
    bek_ekn_gebyr["Bekendtgørelse om gebyr ved indbringelse af en klage for Energiklagenævnet (BEK nr 568 af 24/06/2026)"]:::retsakt
    bek_gebyrer_godkendte_private_ankenaevn["Bekendtgørelse om gebyrer ved godkendte private klage- eller ankenævn (BEK nr. 928 af 26/06/2025)"]:::retsakt
    bek_godkendelse_private_tvistloesningsorganer["Bekendtgørelse om godkendelse af private tvistløsningsorganer (BEK nr. 1151 af 30/09/2015)"]:::retsakt
    bek_co2_kvoter_henlaeggelse_erst["Bekendtgørelse om henlæggelse af visse beføjelser efter lov om CO2-kvoter til Erhvervsstyrelsen (ikrafttræden 1/1/2026)"]:::retsakt
    bek_soefartsstyrelsen_henlaeggelse["Bekendtgørelse om henlæggelse af visse beføjelser til Søfartsstyrelsen og om klageadgang m.v. (BEK nr. 261 af 23/03/2020)"]:::retsakt
    bek_elevatorer["Bekendtgørelse om indretning m.v. af elevatorer og sikkerhedskomponenter til elevatorer"]:::retsakt
    bek_personlige_vaernemidler_indretning["Bekendtgørelse om indretning m.v. af personlige værnemidler (BEK nr 210 af 14/03/2018)"]:::retsakt
    bek_trykbaerende_udstyr["Bekendtgørelse om indretning m.v. af trykbærende udstyr"]:::retsakt
    bek_fyrvaerkeri_krav["Bekendtgørelse om krav til fyrværkeri og andre pyrotekniske artikler (BEK nr. 1799 af 2021)"]:::retsakt
    bek_byggevarer_cpr2011["Bekendtgørelse om markedsføring og markedsovervågning af byggevarer (efter forordning 305/2011)"]:::retsakt
    bek_byggevarer_cpr2024["Bekendtgørelse om markedsføring og markedsovervågning af byggevarer efter den reviderede byggevareforordning"]:::retsakt
    bek_maskiner["Bekendtgørelse om maskiner"]:::retsakt
    bek_atex_produkter["Bekendtgørelse om produkter til anvendelse i en potentielt eksplosiv atmosfære (BEK nr. 811 af 03/06/2022)"]:::retsakt
    bek_forbrugerombudsmandens_virksomhed["Bekendtgørelse om regler for Forbrugerombudsmandens virksomhed (BEK nr. 1249 af 25/11/2014)"]:::retsakt
    bek_drift_elanlaeg["Bekendtgørelse om sikkerhed for drift af elektriske anlæg"]:::retsakt
    bek_elmateriel["Bekendtgørelse om sikkerhed for elektrisk materiel (elmaterielbekendtgørelsen)"]:::retsakt
    bek_gasanlaeg["Bekendtgørelse om sikkerhed for gasanlæg"]:::retsakt
    bek_gasinstallationer["Bekendtgørelse om sikkerhed for gasinstallationer"]:::retsakt
    bek_gasmateriel["Bekendtgørelse om sikkerhed for gasmateriel"]:::retsakt
    bek_roerledninger_gas["Bekendtgørelse om sikkerhed for rørledninger til gas"]:::retsakt
    bek_elanlaeg["Bekendtgørelse om sikkerhed for udførelse af elektriske anlæg (elanlægsbekendtgørelsen)"]:::retsakt
    bek_elinstallationer["Bekendtgørelse om sikkerhed for udførelse og drift af elektriske installationer (elinstallationsbekendtgørelsen)"]:::retsakt
    bek_maskinforordning_supplerende["Bekendtgørelse om supplerende bestemmelser til maskinforordningen"]:::retsakt
    bek_farligt_gods_vejtransport["Bekendtgørelse om vejtransport af farligt gods (BEK nr. 915 af 2025)"]:::retsakt
    lov_designloven["Designloven"]:::retsakt
    plan_fingerplan_2019["Fingerplan 2019 – Landsplandirektiv for hovedstadsområdets planlægning (BEK nr. 312/2019)"]:::retsakt
    bek_fyrvaerkeri["Fyrværkeribekendtgørelsen (bekendtgørelse om indførsel, fremstilling, opbevaring, overdragelse, erhvervelse og anvendelse af fyrværkeri og andre pyrotekniske artikler), BEK nr. 1798 af 09/09/2021"]:::retsakt
    lov_fyrvaerkeriloven["Fyrværkeriloven (lov om fyrværkeri og andre pyrotekniske artikler)"]:::retsakt
    lov_gassikkerhedsloven["Gassikkerhedsloven (lov om sikkerhed ved gasanlæg, gasinstallationer og rørledninger til gas)"]:::retsakt
    lov_konkurrenceloven["Konkurrenceloven"]:::retsakt
    plan_detailhandel_hovedstadsomraadet["Landsplandirektiv for detailhandel i hovedstadsområdet (bekendtgørelse af 11/12/2018, eli/lta/2018/1488)"]:::retsakt
    lov_lodsloven["Lodsloven (Bekendtgørelse af lodslov)"]:::retsakt
    lov_co2_kvoteloven["Lov om CO2-kvoter (CO2-kvoteloven), LOV nr 1767 af 28/12/2023"]:::retsakt
    lov_dis_loven["Lov om Dansk Internationalt Skibsregister (DIS-loven)"]:::retsakt
    lov_energiklagenaevnsloven["Lov om Energiklagenævnet"]:::retsakt
    lov_energinetloven["Lov om Energinet"]:::retsakt
    lov_erhvervsankenaevnsloven["Lov om Erhvervsankenævnet"]:::retsakt
    lov_klagenaevn_for_udbud_loven["Lov om Klagenævnet for Udbud (tidl. lov om håndhævelse af udbudsreglerne m.v.)"]:::retsakt
    lov_mfkn_loven["Lov om Miljø- og Fødevareklagenævnet"]:::retsakt
    lov_planklagenaevnsloven["Lov om Planklagenævnet"]:::retsakt
    lov_selskabsloven["Lov om aktie- og anpartsselskaber (selskabsloven)"]:::retsakt
    lov_forbrugerklageloven["Lov om alternativ tvistløsning i forbindelse med forbrugerklager (forbrugerklageloven)"]:::retsakt
    lov_undergrundsloven["Lov om anvendelse af Danmarks undergrund (undergrundsloven), LBK nr 1461 af 29/11/2023"]:::retsakt
    lov_autorisationsloven["Lov om autorisation af virksomheder på el-, vvs- og kloakinstallationsområdet (autorisationsloven)"]:::retsakt
    lov_beskikkede_bygningssagkyndige["Lov om beskikkede bygningssagkyndige m.v."]:::retsakt
    lov_lov_om_betalinger["Lov om betalinger"]:::retsakt
    lov_dyrlaegeloven["Lov om dyrlæger"]:::retsakt
    lov_teleloven["Lov om elektroniske kommunikationsnet og -tjenester (teleloven)"]:::retsakt
    lov_elforsyningsloven["Lov om elforsyning (elforsyningsloven)"]:::retsakt
    lov_erhvervsuddannelser["Lov om erhvervsuddannelser (erhvervsuddannelsesloven)"]:::retsakt
    lov_masteloven["Lov om etablering og fælles udnyttelse af master til radiokommunikationsformål m.v. (masteloven)"]:::retsakt
    lov_forbrugeraftaleloven["Lov om forbrugeraftaler (forbrugeraftaleloven)"]:::retsakt
    lov_ejendomsformidling["Lov om formidling af fast ejendom m.v."]:::retsakt
    lov_energimaerkningsloven["Lov om fremme af energibesparelser i bygninger"]:::retsakt
    lov_ve_loven["Lov om fremme af vedvarende energi (VE-loven)"]:::retsakt
    lov_foedevareloven["Lov om fødevarer (fødevareloven)"]:::retsakt
    lov_revisorloven["Lov om godkendte revisorer og revisionsvirksomheder (revisorloven)"]:::retsakt
    lov_tilbudsloven["Lov om indhentning af tilbud i bygge- og anlægssektoren (tilbudsloven)"]:::retsakt
    lov_kystbeskyttelsesloven["Lov om kystbeskyttelse (kystbeskyttelsesloven)"]:::retsakt
    lov_lejeloven["Lov om leje (lejeloven)"]:::retsakt
    lov_erhvervslejeloven["Lov om leje af erhvervslokaler m.v. (erhvervslejeloven)"]:::retsakt
    lov_markedsfoeringsloven["Lov om markedsføring (markedsføringsloven)"]:::retsakt
    lov_miljoebeskyttelsesloven["Lov om miljøbeskyttelse (miljøbeskyttelsesloven)"]:::retsakt
    lov_ecodesignloven["Lov om miljøvenligt design af energirelaterede produkter (ecodesignloven)"]:::retsakt
    lov_miljoevurderingsloven["Lov om miljøvurderinger (miljøvurderingsloven, VVM/SMV)"]:::retsakt
    lov_naturbeskyttelsesloven["Lov om naturbeskyttelse (naturbeskyttelsesloven)"]:::retsakt
    lov_planloven["Lov om planlægning (planloven)"]:::retsakt
    lov_produktloven["Lov om produkter og markedsovervågning (produktloven)"]:::retsakt
    lov_elsikkerhedsloven["Lov om sikkerhed for elektriske anlæg og elektriske installationer (elsikkerhedsloven)"]:::retsakt
    lov_sikkerhed_til_soes["Lov om sikkerhed til søs"]:::retsakt
    lov_sikkerhedsundersoegelse_soeulykker["Lov om sikkerhedsundersøgelse af ulykker til søs"]:::retsakt
    lov_skibes_besaetning["Lov om skibes besætning"]:::retsakt
    lov_soefarendes_ansaettelsesforhold["Lov om søfarendes ansættelsesforhold m.v."]:::retsakt
    lov_vandloebsloven["Lov om vandløb (vandløbsloven)"]:::retsakt
    lov_vandsektorloven["Lov om vandsektorens organisering og økonomiske forhold (vandsektorloven)"]:::retsakt
    lov_varmeforsyningsloven["Lov om varmeforsyning (varmeforsyningsloven)"]:::retsakt
    bek_meddelelser_a["Meddelelser fra Søfartsstyrelsen A (arbejdsmiljø i skibe), BEK nr. 1246 af 11/12/2009"]:::retsakt
    bek_meddelelser_b["Meddelelser fra Søfartsstyrelsen B (skibes bygning og udstyr), BEK nr. 1512 af 08/12/2016"]:::retsakt
    bek_meddelelser_e["Meddelelser fra Søfartsstyrelsen E (fiskeskibes bygning og udstyr), BEK nr. 1459 af 14/12/2010"]:::retsakt
    bek_meddelelser_f["Meddelelser fra Søfartsstyrelsen F (mindre erhvervsfartøjers bygning og udstyr), BEK nr. 1460 af 14/12/2010"]:::retsakt
    lov_museumsloven["Museumsloven"]:::retsakt
    lov_patentloven["Patentloven"]:::retsakt
    bek_risiko["Risikobekendtgørelsen (bekendtgørelse om kontrol med risikoen for større uheld med farlige stoffer)"]:::retsakt
    vejl_sik_vejledninger["Sikkerhedsstyrelsens/Erhvervsstyrelsens vejledninger og fortolkninger (el, gas, VVS, kloak, asbest, autorisation)"]:::retsakt
    lov_soeloven["Søloven"]:::retsakt
    lov_varemaerkeloven["Varemærkeloven"]:::retsakt
    vejl_fingerplan_2019["Vejledning om Fingerplan 2019 (VEJ nr. 9281 af 27/03/2019)"]:::retsakt
    vejl_henvisning_standarder["Vejledning om henvisning til visse internationale standarder i lovgivning (Erhvervsstyrelsen)"]:::retsakt
    vejl_planloven_vejledninger["Vejledninger til planloven (samling)"]:::retsakt
    lov_aarsregnskabsloven["Årsregnskabsloven"]:::retsakt
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
    bek_atex_produkter -->|implementerer_EU| eu_dir_2014_34
    bek_elevatorer -->|implementerer_EU| eu_dir_2014_33
    bek_elmateriel -->|implementerer_EU| eu_dir_2014_35
    bek_fyrvaerkeri -->|implementerer_EU| eu_dir_2013_29
    bek_fyrvaerkeri_krav -->|implementerer_EU| eu_dir_2013_29
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
    min_erhverv -->|ressortansvar| sty_foedevarestyrelsen
    min_erhverv -->|ressortansvar| lov_foedevareloven
    min_erhverv -->|ressortansvar| lov_dyrlaegeloven
    min_erhverv -.->|ressortansvar| raad_det_veterinaere_sundhedsraad
    lov_foedevareloven -.->|hjemmel_for| sty_foedevarestyrelsen
    lov_dyrlaegeloven -.->|hjemmel_for| raad_det_veterinaere_sundhedsraad
    naevn_miljoe_og_foedevareklagenaevnet -->|klageinstans| sty_foedevarestyrelsen
    sty_foedevarestyrelsen -.->|udsteder| kilde_findsmiley
    min_erhverv -.->|ressortansvar| bek_meddelelser_a
    lov_sikkerhed_til_soes -->|hjemmel_for| bek_meddelelser_a
    sty_soefartsstyrelsen -->|udsteder| bek_meddelelser_a
    min_erhverv -.->|ressortansvar| bek_meddelelser_b
    lov_sikkerhed_til_soes -->|hjemmel_for| bek_meddelelser_b
    sty_soefartsstyrelsen -->|udsteder| bek_meddelelser_b
    min_erhverv -.->|ressortansvar| bek_meddelelser_e
    lov_sikkerhed_til_soes -->|hjemmel_for| bek_meddelelser_e
    sty_soefartsstyrelsen -->|udsteder| bek_meddelelser_e
    min_erhverv -.->|ressortansvar| bek_meddelelser_f
    lov_sikkerhed_til_soes -->|hjemmel_for| bek_meddelelser_f
    sty_soefartsstyrelsen -->|udsteder| bek_meddelelser_f
    min_erhverv -->|ressortansvar| sty_soefartsstyrelsen
    min_erhverv -.->|ressortansvar| naevn_ankenaevnet_for_soefartsforhold
    min_erhverv -.->|ressortansvar| raad_skibstilsynsraadet
    min_erhverv -->|ressortansvar| sty_den_maritime_havarikommission
    min_erhverv -.->|ressortansvar| bek_ankenaevn_soefartsforhold_forretningsorden
    min_erhverv -.->|ressortansvar| bek_skibstilsynsraadet_forretningsorden
    min_erhverv -.->|ressortansvar| lov_sikkerhed_til_soes
    min_erhverv -.->|ressortansvar| lov_soeloven
    min_erhverv -->|ressortansvar| lov_skibes_besaetning
    min_erhverv -.->|ressortansvar| lov_soefarendes_ansaettelsesforhold
    min_erhverv -->|ressortansvar| lov_dis_loven
    min_erhverv -.->|ressortansvar| lov_sikkerhedsundersoegelse_soeulykker
    lov_sikkerhed_til_soes -->|hjemmel_for| sty_soefartsstyrelsen
    lov_sikkerhed_til_soes -->|hjemmel_for| naevn_ankenaevnet_for_soefartsforhold
    lov_sikkerhed_til_soes -->|hjemmel_for| raad_skibstilsynsraadet
    lov_sikkerhed_til_soes -->|hjemmel_for| bek_ankenaevn_soefartsforhold_forretningsorden
    lov_sikkerhed_til_soes -->|hjemmel_for| bek_skibstilsynsraadet_forretningsorden
    lov_sikkerhedsundersoegelse_soeulykker -->|hjemmel_for| sty_den_maritime_havarikommission
    lov_lodsloven -->|hjemmel_for| sty_soefartsstyrelsen
    lov_sikkerhed_til_soes -->|hjemmel_for| bek_soefartsstyrelsen_henlaeggelse
    bek_soefartsstyrelsen_henlaeggelse -.->|hjemmel_for| naevn_ankenaevnet_for_soefartsforhold
    min_erhverv -.->|delegation| sty_soefartsstyrelsen
    naevn_ankenaevnet_for_soefartsforhold -.->|klageinstans| sty_soefartsstyrelsen
    dom_domstolene -->|klageinstans| naevn_ankenaevnet_for_soefartsforhold
    sty_soefartsstyrelsen -->|udsteder| kilde_soefartsstyrelsen_regler
    sty_soefartsstyrelsen -->|udsteder| kilde_meddelelser_fra_soefartsstyrelsen
    sty_den_maritime_havarikommission -->|udsteder| kilde_dmaib_rapporter
    min_erhverv -.->|ressortansvar| bek_tvistighedsnaevnet
    min_erhverv -.->|ressortansvar| naevn_tvistighedsnaevnet
    lov_erhvervsuddannelser -->|hjemmel_for| naevn_tvistighedsnaevnet
    lov_erhvervsuddannelser -->|hjemmel_for| bek_tvistighedsnaevnet
    bek_tvistighedsnaevnet -.->|hjemmel_for| naevn_tvistighedsnaevnet
    naevn_tvistighedsnaevnet -->|udsteder| kilde_tvistighedsnaevnet_kendelser
    bek_autorisation -->|implementerer_EU| eu_dir_2020_2184
    lov_planklagenaevnsloven -->|hjemmel_for| bek_klagenaevn_sagsbehandlingslofter
    lov_energiklagenaevnsloven -->|hjemmel_for| bek_klagenaevn_sagsbehandlingslofter
    lov_produktloven -->|hjemmel_for| bek_maskinforordning_supplerende
    lov_produktloven -->|hjemmel_for| bek_faerdselsstyrelsen_opgaver
    lov_produktloven -->|implementerer_EU| eu_dir_2006_42
    lov_produktloven -->|implementerer_EU| eu_dir_2013_29
    lov_produktloven -->|implementerer_EU| eu_dir_2014_33
    lov_produktloven -->|implementerer_EU| eu_dir_2014_34
    lov_produktloven -->|implementerer_EU| eu_dir_2014_35
    lov_produktloven -->|implementerer_EU| eu_dir_2014_68
    lov_produktloven -->|implementerer_EU| eu_dir_2020_2184
    lov_dis_loven -->|hjemmel_for| bek_soefartsstyrelsen_henlaeggelse
    lov_soefarendes_ansaettelsesforhold -->|hjemmel_for| bek_soefartsstyrelsen_henlaeggelse
    lov_soeloven -->|hjemmel_for| bek_soefartsstyrelsen_henlaeggelse
    lov_skibes_besaetning -->|hjemmel_for| bek_soefartsstyrelsen_henlaeggelse
    lov_sikkerhed_til_soes -->|implementerer_EU| eu_dir_1989_391
    lov_sikkerhed_til_soes -->|implementerer_EU| eu_dir_1989_656
    lov_sikkerhed_til_soes -->|implementerer_EU| eu_dir_1994_33
    lov_sikkerhed_til_soes -->|implementerer_EU| eu_dir_1998_24
    lov_sikkerhed_til_soes -->|implementerer_EU| eu_dir_1999_92
    lov_sikkerhed_til_soes -->|implementerer_EU| eu_dir_2000_54
    lov_sikkerhed_til_soes -->|implementerer_EU| eu_dir_2002_44
    lov_sikkerhed_til_soes -->|implementerer_EU| eu_dir_2003_10
    lov_sikkerhed_til_soes -->|implementerer_EU| eu_dir_2004_37
    lov_sikkerhed_til_soes -->|implementerer_EU| eu_dir_2009_104
    lov_sikkerhed_til_soes -->|implementerer_EU| eu_dir_2009_148
    lov_soeloven -->|implementerer_EU| eu_dir_2005_36
    lov_skibes_besaetning -->|implementerer_EU| eu_dir_2005_36
    min_erhverv -.->|ressortansvar| ombud_forbrugerombudsmanden
    min_erhverv -.->|ressortansvar| naevn_forbrugerklagenaevnet
    min_erhverv -.->|ressortansvar| lov_markedsfoeringsloven
    min_erhverv -->|ressortansvar| bek_forbrugerklager_naevnenes_hus
    min_erhverv -.->|ressortansvar| bek_godkendelse_private_tvistloesningsorganer
    min_erhverv -->|ressortansvar| bek_gebyrer_godkendte_private_ankenaevn
    min_erhverv -->|ressortansvar| bek_forbrugerombudsmandens_virksomhed
    lov_markedsfoeringsloven -->|hjemmel_for| ombud_forbrugerombudsmanden
    lov_forbrugeraftaleloven -->|hjemmel_for| ombud_forbrugerombudsmanden
    lov_lov_om_betalinger -->|hjemmel_for| ombud_forbrugerombudsmanden
    bek_forbrugerombudsmandens_virksomhed -->|hjemmel_for| ombud_forbrugerombudsmanden
    lov_markedsfoeringsloven -->|hjemmel_for| bek_forbrugerombudsmandens_virksomhed
    dom_domstolene -->|klageinstans| ombud_forbrugerombudsmanden
    lov_forbrugeraftaleloven -->|henviser_til| lov_markedsfoeringsloven
    ombud_forbrugerombudsmanden -->|udsteder| kilde_forbrugerombudsmanden_sager
    ombud_forbrugerombudsmanden -->|udsteder| kilde_forbrugerombudsmanden_retningslinjer
    lov_forbrugerklageloven -->|hjemmel_for| naevn_forbrugerklagenaevnet
    bek_forbrugerklager_naevnenes_hus -->|hjemmel_for| naevn_forbrugerklagenaevnet
    dom_domstolene -->|klageinstans| naevn_forbrugerklagenaevnet
    naevn_forbrugerklagenaevnet -.->|udsteder| kilde_fkn_afgoerelser
    sty_naevnenes_hus -->|udsteder| kilde_fkn_afgoerelser
    lov_forbrugerklageloven -->|hjemmel_for| bek_forbrugerklager_naevnenes_hus
    lov_forbrugerklageloven -->|hjemmel_for| org_godkendte_private_ankenaevn
    bek_godkendelse_private_tvistloesningsorganer -->|hjemmel_for| org_godkendte_private_ankenaevn
    bek_gebyrer_godkendte_private_ankenaevn -->|hjemmel_for| org_godkendte_private_ankenaevn
    sty_naevnenes_hus -->|tilsyn| org_godkendte_private_ankenaevn
    sty_naevnenes_hus -->|udsteder| kilde_godkendte_private_ankenaevn_liste
    lov_forbrugerklageloven -.->|hjemmel_for| org_ankenaevnet_for_forsikring
    lov_forbrugerklageloven -.->|hjemmel_for| org_byggeriets_ankenaevn
    lov_forbrugerklageloven -.->|hjemmel_for| org_ankenaevnet_for_bus_tog_og_metro
    lov_forbrugerklageloven -.->|hjemmel_for| naevn_ankenaevnet_paa_energiomraadet
    min_erhverv -->|ressortansvar| sty_patent_og_varemaerkestyrelsen
    min_erhverv -.->|ressortansvar| naevn_ankenaevnet_patenter_varemaerker
    min_erhverv -.->|ressortansvar| naevn_revisornaevnet
    min_erhverv -.->|ressortansvar| naevn_disciplinaernaevnet_ejendomsmaeglere
    min_erhverv -.->|ressortansvar| naevn_bygningssagkyndige
    min_erhverv -.->|ressortansvar| lov_patentloven
    min_erhverv -.->|ressortansvar| lov_varemaerkeloven
    min_erhverv -.->|ressortansvar| lov_designloven
    min_erhverv -.->|ressortansvar| lov_revisorloven
    min_erhverv -.->|ressortansvar| lov_ejendomsformidling
    min_erhverv -.->|ressortansvar| lov_selskabsloven
    min_erhverv -.->|ressortansvar| lov_aarsregnskabsloven
    min_erhverv -->|ressortansvar| lov_beskikkede_bygningssagkyndige
    min_erhverv -.->|ressortansvar| bek_ankenaevnet_patenter_varemaerker
    min_erhverv -.->|ressortansvar| bek_revisornaevnet
    min_erhverv -.->|ressortansvar| bek_disciplinaernaevnet_ejendomsmaeglere
    min_erhverv -.->|ressortansvar| bek_bygningssagkyndige_naevn
    lov_patentloven -->|hjemmel_for| sty_patent_og_varemaerkestyrelsen
    lov_patentloven -->|hjemmel_for| naevn_ankenaevnet_patenter_varemaerker
    lov_patentloven -->|hjemmel_for| bek_ankenaevnet_patenter_varemaerker
    lov_revisorloven -->|hjemmel_for| naevn_revisornaevnet
    lov_revisorloven -->|hjemmel_for| bek_revisornaevnet
    lov_revisorloven -->|hjemmel_for| sty_erhvervsstyrelsen
    lov_ejendomsformidling -.->|hjemmel_for| naevn_disciplinaernaevnet_ejendomsmaeglere
    lov_ejendomsformidling -->|hjemmel_for| bek_disciplinaernaevnet_ejendomsmaeglere
    lov_beskikkede_bygningssagkyndige -->|hjemmel_for| naevn_bygningssagkyndige
    lov_beskikkede_bygningssagkyndige -->|hjemmel_for| bek_bygningssagkyndige_naevn
    naevn_ankenaevnet_patenter_varemaerker -.->|klageinstans| sty_patent_og_varemaerkestyrelsen
    dom_domstolene -->|klageinstans| naevn_ankenaevnet_patenter_varemaerker
    dom_domstolene -->|klageinstans| naevn_revisornaevnet
    dom_domstolene -->|klageinstans| naevn_disciplinaernaevnet_ejendomsmaeglere
    dom_domstolene -->|klageinstans| naevn_bygningssagkyndige
    sty_erhvervsstyrelsen -->|tilsyn| org_godkendte_revisorer
    sty_naevnenes_hus -->|udsteder| kilde_apv_afgoerelser
    sty_naevnenes_hus -->|udsteder| kilde_rn_kendelser
    sty_naevnenes_hus -->|udsteder| kilde_dnfe_kendelser
    naevn_revisornaevnet -->|udsteder| kilde_rn_kendelser
    naevn_disciplinaernaevnet_ejendomsmaeglere -->|udsteder| kilde_dnfe_kendelser
    min_erhverv -.->|ressortansvar| naevn_ankenaevn_oplaeringsvirksomheder
    min_erhverv -.->|ressortansvar| bek_ankenaevn_praktikvirksomheder
    lov_erhvervsuddannelser -->|hjemmel_for| naevn_ankenaevn_oplaeringsvirksomheder
    lov_erhvervsuddannelser -->|hjemmel_for| bek_ankenaevn_praktikvirksomheder
    bek_ankenaevn_praktikvirksomheder -->|hjemmel_for| naevn_ankenaevn_oplaeringsvirksomheder
    lov_forbrugerklageloven -->|hjemmel_for| bek_gebyrer_godkendte_private_ankenaevn
    lov_forbrugerklageloven -->|hjemmel_for| bek_godkendelse_private_tvistloesningsorganer
    lov_revisorloven -->|implementerer_EU| eu_dir_2005_36
    lov_ejendomsformidling -.->|hjemmel_for| bek_bygningssagkyndige_naevn
    lov_selskabsloven -->|implementerer_EU| eu_dir_2015_849
    lov_beskikkede_bygningssagkyndige -->|implementerer_EU| eu_dir_2005_36
    min_erhverv -.->|ressortansvar| naevn_teleklagenaevnet
    lov_teleloven -->|hjemmel_for| naevn_teleklagenaevnet
    lov_teleloven -->|hjemmel_for| bek_teleklagenaevnets_virksomhed
    naevn_teleklagenaevnet -->|klageinstans| sty_erhvervsstyrelsen
    naevn_teleklagenaevnet -.->|udsteder| kilde_teleklagenaevn_afgoerelser
    sty_naevnenes_hus -.->|tilsyn| naevn_teleankenaevnet
    lov_produktloven -.->|hjemmel_for| bek_personlige_vaernemidler_indretning
    naevn_energiklagenaevnet -->|klageinstans| sty_arbejdstilsynet
    naevn_energiklagenaevnet -->|klageinstans| min_klima_energi_og_forsyning
    naevn_miljoe_og_foedevareklagenaevnet -.->|klageinstans| min_miljoe
    naevn_energiklagenaevnet -.->|klageinstans| sty_erhvervsstyrelsen
    naevn_miljoe_og_foedevareklagenaevnet -->|klageinstans| org_udbetaling_danmark
    lov_produktloven -.->|hjemmel_for| bek_trykbaerende_udstyr
    bek_risiko -->|implementerer_EU| eu_dir_2012_18
    bek_faerdselsstyrelsen_opgaver -->|hjemmel_for| sty_faerdselsstyrelsen
    bek_faerdselsstyrelsen_opgaver -->|hjemmel_for| bek_farligt_gods_vejtransport
```

[← Overblik](oversigt.md)
