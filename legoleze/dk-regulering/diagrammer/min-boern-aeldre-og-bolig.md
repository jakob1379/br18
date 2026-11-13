# Børne-, Ældre- og Boligministeriet

> Genereret af `scripts/build.py` fra `registry.yaml` (dato 2026-10-28). Redigér ikke i hånden.
> Fuldt optrukne pile = `verificeret`; stiplede = `sandsynlig`/`ukendt`. Grå stiplede bokse = nedlagt/omdøbt/ophævet.

Noder: 104 · kanter: 232

```mermaid
flowchart LR
    classDef ministerium fill:#1f3a5f,stroke:#0d1b2a,color:#fff
    classDef instans fill:#d7e3f4,stroke:#1f3a5f,color:#0d1b2a
    classDef klage fill:#f6dcc2,stroke:#8a4b08,color:#3b1f00
    classDef retsakt fill:#e6f2e6,stroke:#2e6b2e,color:#103010
    classDef eu fill:#fff3b0,stroke:#7a6a00,color:#333
    classDef kilde fill:#eee,stroke:#666,color:#222
    classDef nedlagt fill:#fff,stroke:#999,color:#999,stroke-dasharray:4 3
    min_boern_aeldre_og_bolig["Børne-, Ældre- og Boligministeriet"]:::ministerium
    eu_reg_2011_305["Byggevareforordningen (EU) nr. 305/2011 (CPR)"]:::eu
    eu_dir_2023_1791["Direktiv (EU) 2023/1791 om energieffektivitet og om ændring af forordning (EU) 2023/955 (omarbejdning, EED)"]:::eu
    eu_dir_2024_1275["Direktiv (EU) 2024/1275 om bygningers energimæssige ydeevne (omarbejdning, EPBD)"]:::eu
    eu_kommissionen["Europa-Kommissionen"]:::eu
    eu_dir_2015_1535["Europa-Parlamentets og Rådets direktiv (EU) 2015/1535 af 9. september 2015 om en informationsprocedure med hensyn til tekniske forskrifter og forskrifter for informationssamfundets tjenester (informationsproceduredirektivet, TRIS)"]:::eu
    eu_dir_2005_36["Europa-Parlamentets og Rådets direktiv 2005/36/EF af 7. september 2005 om anerkendelse af erhvervsmæssige kvalifikationer"]:::eu
    eu_reg_2019_1020["Markedsovervågningsforordningen (EU) 2019/1020"]:::eu
    eu_reg_2024_3110["Revideret byggevareforordning (EU) 2024/3110"]:::eu
    fond_byggeskadefonden["Byggeskadefonden"]:::instans
    fond_danak["DANAK (nationalt akkrediteringsorgan)"]:::instans
    sty_erhvervsstyrelsen["Erhvervsstyrelsen"]:::instans
    fond_blandede_byer["Fonden for blandede byer"]:::instans
    fond_grundejernes_investeringsfond["Grundejernes Investeringsfond (GI)"]:::instans
    kommune_alle["Kommunerne (98 kommunalbestyrelser)"]:::instans
    fond_landsbyggefonden["Landsbyggefonden"]:::instans
    sty_naevnenes_hus["Nævnenes Hus"]:::instans
    sty_social_og_boligstyrelsen["Social- og Boligstyrelsen"]:::instans
    org_certificeringsorganer["Akkrediterede certificeringsorganer for brandrådgivere (og statikere)"]:::kilde
    org_almene_boligorganisationer["Almene boligorganisationer og afdelinger"]:::kilde
    bv_build_anvisning_213["BUILD-anvisning 213 Bygningers energibehov (tidl. SBi-anvisning 213; beregningsprogrammet Be18)"]:::kilde
    kilde_bke_afgoerelser["Byggeklageenhedens afgørelser"]:::kilde
    bv_dbi_vejledninger["DBI-retningslinjer og DBI-vejledninger (brandteknik, ABA, sprinkler, vandtåge m.v.)"]:::kilde
    std_ds_418["DS 418 Beregning af bygningers varmetab"]:::kilde
    std_ds_432["DS 432 Norm for afløbsinstallationer"]:::kilde
    std_ds_439["DS 439 Norm for vandinstallationer"]:::kilde
    std_en_13501["DS/EN 13501-1 og -2 (brandklassifikation af byggevarer og bygningsdele)"]:::kilde
    std_ds_en_1717["DS/EN 1717 Beskyttelse mod tilbagestrømning i drikkevandsinstallationer"]:::kilde
    std_ds_en_iso_iec_17024["DS/EN ISO/IEC 17024 (certificering af personer)"]:::kilde
    std_ds_standarder_br18["Danske standarder som BR18 og vejledningerne henviser til (fx DS 418, DS/EN 13501-1, DS 428, DS 447)"]:::kilde
    std_eurocodes["Eurocodes (DS/EN 1990-1999) med danske nationale annekser"]:::kilde
    kilde_fob_database["Folketingets Ombudsmands udtalelser"]:::kilde
    std_harmoniserede_standarder_cpr["Harmoniserede standarder (hEN) under byggevareforordningen"]:::kilde
    kilde_huslejenaevn_dk["Huslejenævnsdatabasen (huslejenævn.dk)"]:::kilde
    kilde_parallelsamfundslister["Liste over parallelsamfund og liste over omdannelsesområder (offentliggøres årligt 1. december efter almenboligloven § 61 a)"]:::kilde
    kilde_lovguiden["Lovguiden (lovguiden.dk)"]:::kilde
    kilde_mrf["Miljøretlig Forskningsportal (MRF), Københavns Universitet"]:::kilde
    kilde_naevneneshus_afgoerelser["Nævnenes Hus – afgørelser fra øvrige nævn (Energiklagenævnet, Byggeklageenheden, Erhvervsankenævnet m.fl.)"]:::kilde
    bv_roercenter_anvisninger["Rørcenter-anvisninger (fx 017 Legionella, 027 Vandinstallationer)"]:::kilde
    bv_sbi_anvisninger["SBi-/BUILD-anvisninger"]:::kilde
    org_skorstensfejere["Skorstensfejere (lovpligtigt skorstensfejerarbejde)"]:::kilde
    kilde_tris["TRIS – Kommissionens database over notificerede tekniske forskrifter (direktiv (EU) 2015/1535)"]:::kilde
    kilde_tilbudsportalen["Tilbudsportalen"]:::kilde
    kilde_bygningsreglementet_dk["bygningsreglementet.dk"]:::kilde
    naevn_ankenaevn_koebenhavn["Ankenævnet for huslejenævnene i Københavns Kommune"]:::klage
    naevn_beboerklagenaevn["Beboerklagenævn (kommunale)"]:::klage
    dom_boligretten["Boligretten (ved byretterne)"]:::klage
    naevn_byggeklageenheden["Byggeklageenheden"]:::klage
    dom_byretterne["Byretterne"]:::klage
    dom_domstolene["Domstolene (byret, landsret, Højesteret)"]:::klage
    ombud_folketingets_ombudsmand["Folketingets Ombudsmand"]:::klage
    naevn_huslejenaevn["Huslejenævn (kommunale)"]:::klage
    min_social["Socialministeriet"]:::ministerium
    fond_byggeskadefonden_bygningsfornyelse["Byggeskadefonden vedrørende Bygningsfornyelse (nedlagt)"]:::nedlagt
    eu_dir_2018_844["Direktiv (EU) 2018/844 om ændring af direktiv 2010/31/EU om bygningers energimæssige ydeevne og direktiv 2012/27/EU om energieffektivitet (ophævet)"]:::nedlagt
    eu_dir_2010_31["Direktiv 2010/31/EU om bygningers energimæssige ydeevne (EPBD, som ændret ved 2018/844) (ophævet)"]:::nedlagt
    eu_dir_2012_27["Europa-Parlamentets og Rådets direktiv 2012/27/EU af 25. oktober 2012 om energieffektivitet (EED) (ophævet)"]:::nedlagt
    min_indenrigs_og_bolig["Indenrigs- og Boligministeriet (nedlagt)"]:::nedlagt
    eu_dec_2012_21["Kommissionens afgørelse 2012/21/EU af 20. december 2011 om SGEI-kompensation (ophævet)"]:::nedlagt
    lov_lejeloven_1979["Lov om leje (den tidligere lejelov fra 1979; senest LBK 927/2019) (ophævet)"]:::nedlagt
    sty_trafik_bygge_og_boligstyrelsen["Trafik-, Bygge- og Boligstyrelsen (omdøbt)"]:::nedlagt
    bek_ressortoverfoersel_bolig_2026["Bekendtgørelse nr. 514 af 8. juni 2026 om ressortoverførsel (kgl. resolution): bolig- og byggeområdet overføres fra Social- og Boligministeriet til Børne-, Ældre- og Boligministeriet"]:::retsakt
    bek_danak_byggevarer["Bekendtgørelse om DANAK's opgaver vedrørende notificerede organer, der fører 3. partskontrol med byggevarer, og om tekniske vurderingsorganer (BEK nr. 1744 af 2025)"]:::retsakt
    bek_sbst_opgaver["Bekendtgørelse om Social- og Boligstyrelsens opgaver og beføjelser samt klageadgang på bolig- og byggeområdet (BEK nr. 519/2023)"]:::retsakt
    bek_administration_private_udlejningsejendomme["Bekendtgørelse om administration af private udlejningsejendomme efter § 25 i lov om boligforhold (BEK nr. 750 af 30/05/2022)"]:::retsakt
    bek_br18["Bekendtgørelse om bygningsreglement 2018 (BR18)"]:::retsakt
    bek_certificering["Bekendtgørelse om certificeringsordninger for dokumentation af tekniske forhold i bygningsreglementet (statikere og brandrådgivere)"]:::retsakt
    bek_almen_drift["Bekendtgørelse om drift af almene boliger m.v. (driftsbekendtgørelsen)"]:::retsakt
    bek_bsf_eftersyn["Bekendtgørelse om eftersyn under Byggeskadefonden (BEK nr. 2137 af 21/12/2020)"]:::retsakt
    bek_friplejeboliger_etablering["Bekendtgørelse om etablering af friplejeboliger (2025-udgave; afløser BEK nr. 1066/2015)"]:::retsakt
    bek_byggesagsgebyr["Bekendtgørelse om gebyrer på byggeområdet fastsat af Social- og Boligstyrelsen (byggesagsgebyr)"]:::retsakt
    bek_individuel_maaling["Bekendtgørelse om individuel måling af el, gas, vand, varme og køling (BEK nr. 563 af 02/06/2014, ændret ved BEK 1291/2014, 1383/2020 og 1147/2025)"]:::retsakt
    bek_ladestandere["Bekendtgørelse om ladestandere og tomrør i forbindelse med bygninger (ladestanderbekendtgørelsen)"]:::retsakt
    bek_byggevarer_cpr2011["Bekendtgørelse om markedsføring og markedsovervågning af byggevarer (efter forordning 305/2011)"]:::retsakt
    bek_byggevarer_cpr2024["Bekendtgørelse om markedsføring og markedsovervågning af byggevarer efter den reviderede byggevareforordning"]:::retsakt
    bek_drikkevand_byggevarer["Bekendtgørelse om markedsføring og salg af byggevarer i kontakt med drikkevand (GDV-ordningen)"]:::retsakt
    bek_andelsbolig_oplysningspligt["Bekendtgørelse om oplysningspligt ved salg af andelsboliger m.v. (BEK nr. 1333 af 11/06/2021) inkl. nøgleoplysningsskema og indberetning til andelsboliginfo.dk"]:::retsakt
    bek_sideaktiviteter_almene["Bekendtgørelse om sideaktiviteter i almene boligorganisationer m.v. (BEK nr. 953 af 26/06/2025)"]:::retsakt
    bek_almen_udlejning["Bekendtgørelse om udlejning af almene boliger m.v."]:::retsakt
    bek_vedligeholdelsesplaner["Bekendtgørelse om vedligeholdelsesplaner for private udlejningsejendomme (BEK nr. 752 af 30/05/2022)"]:::retsakt
    lov_beredskabsloven["Beredskabsloven"]:::retsakt
    bek_brandsyn["Brandsynsbekendtgørelsen (bekendtgørelse om brandsyn), BEK nr. 2341 af 09/12/2021"]:::retsakt
    lov_byggeloven["Byggeloven (lov om byggeri)"]:::retsakt
    vejl_br18_vejledninger["Bygningsreglementets vejledninger og 'Spørgsmål og svar' (samling)"]:::retsakt
    lov_forvaltningsloven["Forvaltningsloven"]:::retsakt
    reg_byggesagsgebyr["Kommunale gebyrer for byggesagsbehandling (gebyrinstruks/takstblad)"]:::retsakt
    reg_lbf_regulativer["Landsbyggefondens regulativer (samling)"]:::retsakt
    lov_almenboligloven["Lov om almene boliger m.v. (almenboligloven)"]:::retsakt
    lov_andelsboligloven["Lov om andelsboligforeninger og andre boligfællesskaber (andelsboligloven)"]:::retsakt
    lov_boligforholdsloven["Lov om boligforhold"]:::retsakt
    lov_byfornyelsesloven["Lov om byfornyelse og udvikling af byer (byfornyelsesloven)"]:::retsakt
    lov_ejerlejlighedsloven["Lov om ejerlejligheder (ejerlejlighedsloven)"]:::retsakt
    lov_friplejeboligloven["Lov om friplejeboliger (friplejeboligloven)"]:::retsakt
    lov_lejeloven["Lov om leje (lejeloven)"]:::retsakt
    lov_almenlejeloven["Lov om leje af almene boliger (almenlejeloven)"]:::retsakt
    lov_erhvervslejeloven["Lov om leje af erhvervslokaler m.v. (erhvervslejeloven)"]:::retsakt
    lov_offentlighedsloven["Lov om offentlighed i forvaltningen (offentlighedsloven)"]:::retsakt
    bek_skorstensfejer["Skorstensfejerbekendtgørelsen (brandværnsforanstaltninger for aftrækssystemer og fyringsanlæg)"]:::retsakt
    bek_almen_stoette["Støttebekendtgørelsen (bekendtgørelse om støtte til almene boliger m.v.)"]:::retsakt
    vejl_individuel_maaling["Vejledning om individuel måling (VEJ nr. 9880 af 03/12/2020)"]:::retsakt
    vejl_satsvejledning_leje_almen["Vejledning om regulering af satser i lejelovgivningen og almenboligloven for 2026 (VEJ 9886/2025)"]:::retsakt
    vejl_tilsyn_almen_boligsektor["Vejledning om tilsyn med den almene boligsektor (Social- og Boligstyrelsen, juni 2023)"]:::retsakt
    vejl_almen_vejledninger["Vejledninger på almenområdet fra Social- og Boligstyrelsen og forgængere (samling)"]:::retsakt
    vejl_br18_brandvejledninger["Vejledninger til BR18 kapitel 5 Brand (brandvejledningerne: præaccepterede løsninger, brandklasser, certificerede brandrådgivere, brandteknisk dimensionering, kontrol)"]:::retsakt
    min_boern_aeldre_og_bolig -.->|delegation| sty_social_og_boligstyrelsen
    bek_almen_stoette -.->|henviser_til| bek_bsf_eftersyn
    bek_br18 -->|henviser_til| bek_certificering
    bek_br18 -.->|henviser_til| bek_skorstensfejer
    bek_br18 -->|henviser_til| bv_build_anvisning_213
    bek_br18 -->|henviser_til| bv_roercenter_anvisninger
    bek_br18 -->|henviser_til| eu_dir_2015_1535
    bek_br18 -.->|henviser_til| eu_reg_2011_305
    bek_br18 -.->|henviser_til| lov_beredskabsloven
    bek_br18 -->|henviser_til| std_ds_418
    bek_br18 -->|henviser_til| std_ds_439
    bek_br18 -->|henviser_til| std_ds_en_1717
    bek_br18 -->|henviser_til| std_ds_standarder_br18
    bek_br18 -.->|henviser_til| std_eurocodes
    bek_brandsyn -->|henviser_til| bek_br18
    bek_brandsyn -.->|henviser_til| lov_byggeloven
    bek_bsf_eftersyn -->|henviser_til| lov_almenboligloven
    bek_byggevarer_cpr2011 -.->|henviser_til| bek_drikkevand_byggevarer
    bek_byggevarer_cpr2024 -.->|henviser_til| eu_dir_2015_1535
    bek_byggevarer_cpr2024 -.->|henviser_til| std_harmoniserede_standarder_cpr
    bek_certificering -.->|henviser_til| std_ds_en_iso_iec_17024
    bek_ressortoverfoersel_bolig_2026 -.->|henviser_til| bek_br18
    bek_ressortoverfoersel_bolig_2026 -->|henviser_til| lov_almenboligloven
    bek_ressortoverfoersel_bolig_2026 -->|henviser_til| lov_byfornyelsesloven
    bek_ressortoverfoersel_bolig_2026 -.->|henviser_til| lov_byggeloven
    bek_ressortoverfoersel_bolig_2026 -.->|henviser_til| lov_lejeloven
    bv_sbi_anvisninger -.->|henviser_til| bek_br18
    kilde_bke_afgoerelser -->|henviser_til| bek_br18
    kilde_bke_afgoerelser -->|henviser_til| lov_byggeloven
    kilde_fob_database -.->|henviser_til| lov_byggeloven
    kilde_lovguiden -->|henviser_til| kilde_bke_afgoerelser
    kilde_mrf -->|henviser_til| lov_byggeloven
    kilde_tris -->|henviser_til| bek_byggevarer_cpr2024
    lov_almenboligloven -.->|henviser_til| eu_dec_2012_21
    lov_almenlejeloven -.->|henviser_til| lov_lejeloven
    lov_almenlejeloven -.->|henviser_til| lov_lejeloven_1979
    lov_erhvervslejeloven -.->|henviser_til| lov_lejeloven
    vejl_almen_vejledninger -->|henviser_til| bek_almen_udlejning
    vejl_almen_vejledninger -->|henviser_til| lov_almenboligloven
    vejl_br18_brandvejledninger -->|henviser_til| bek_br18
    vejl_br18_brandvejledninger -->|henviser_til| bek_certificering
    vejl_br18_brandvejledninger -.->|henviser_til| bv_dbi_vejledninger
    vejl_br18_brandvejledninger -.->|henviser_til| std_en_13501
    vejl_br18_vejledninger -->|henviser_til| bek_br18
    vejl_br18_vejledninger -->|henviser_til| bek_certificering
    vejl_br18_vejledninger -->|henviser_til| bek_skorstensfejer
    vejl_br18_vejledninger -.->|henviser_til| bv_dbi_vejledninger
    vejl_br18_vejledninger -.->|henviser_til| bv_sbi_anvisninger
    vejl_br18_vejledninger -.->|henviser_til| lov_byggeloven
    vejl_br18_vejledninger -->|henviser_til| reg_byggesagsgebyr
    vejl_br18_vejledninger -->|henviser_til| std_ds_432
    vejl_br18_vejledninger -->|henviser_til| std_ds_standarder_br18
    vejl_br18_vejledninger -->|henviser_til| std_eurocodes
    vejl_individuel_maaling -->|henviser_til| bek_individuel_maaling
    vejl_satsvejledning_leje_almen -->|henviser_til| lov_almenboligloven
    vejl_satsvejledning_leje_almen -->|henviser_til| lov_almenlejeloven
    vejl_satsvejledning_leje_almen -->|henviser_til| lov_boligforholdsloven
    vejl_satsvejledning_leje_almen -->|henviser_til| lov_lejeloven
    vejl_tilsyn_almen_boligsektor -->|henviser_til| lov_almenboligloven
    vejl_tilsyn_almen_boligsektor -->|henviser_til| naevn_beboerklagenaevn
    bek_br18 -->|hjemmel_for| reg_byggesagsgebyr
    bek_byggevarer_cpr2011 -->|hjemmel_for| sty_erhvervsstyrelsen
    bek_byggevarer_cpr2024 -.->|hjemmel_for| sty_erhvervsstyrelsen
    bek_certificering -->|hjemmel_for| org_certificeringsorganer
    bek_danak_byggevarer -->|hjemmel_for| fond_danak
    bek_sbst_opgaver -->|hjemmel_for| bek_byggevarer_cpr2011
    bek_sbst_opgaver -->|hjemmel_for| bek_byggevarer_cpr2024
    bek_sbst_opgaver -->|hjemmel_for| bek_certificering
    bek_sbst_opgaver -->|hjemmel_for| bek_danak_byggevarer
    bek_sbst_opgaver -->|hjemmel_for| sty_social_og_boligstyrelsen
    bek_skorstensfejer -->|hjemmel_for| kommune_alle
    bek_skorstensfejer -->|hjemmel_for| org_skorstensfejere
    lov_almenboligloven -->|hjemmel_for| bek_almen_drift
    lov_almenboligloven -->|hjemmel_for| bek_almen_stoette
    lov_almenboligloven -->|hjemmel_for| bek_almen_udlejning
    lov_almenboligloven -->|hjemmel_for| bek_bsf_eftersyn
    lov_almenboligloven -->|hjemmel_for| bek_sbst_opgaver
    lov_almenboligloven -->|hjemmel_for| bek_sideaktiviteter_almene
    lov_almenboligloven -->|hjemmel_for| fond_blandede_byer
    lov_almenboligloven -->|hjemmel_for| fond_byggeskadefonden
    lov_almenboligloven -->|hjemmel_for| fond_landsbyggefonden
    lov_almenboligloven -->|hjemmel_for| kilde_parallelsamfundslister
    lov_almenboligloven -->|hjemmel_for| kommune_alle
    lov_almenlejeloven -->|hjemmel_for| naevn_beboerklagenaevn
    lov_andelsboligloven -.->|hjemmel_for| bek_andelsbolig_oplysningspligt
    lov_boligforholdsloven -->|hjemmel_for| bek_administration_private_udlejningsejendomme
    lov_boligforholdsloven -->|hjemmel_for| bek_sbst_opgaver
    lov_boligforholdsloven -->|hjemmel_for| dom_boligretten
    lov_boligforholdsloven -->|hjemmel_for| fond_grundejernes_investeringsfond
    lov_boligforholdsloven -->|hjemmel_for| naevn_ankenaevn_koebenhavn
    lov_boligforholdsloven -->|hjemmel_for| naevn_huslejenaevn
    lov_byfornyelsesloven -.->|hjemmel_for| fond_byggeskadefonden
    lov_byggeloven -->|hjemmel_for| bek_br18
    lov_byggeloven -->|hjemmel_for| bek_byggesagsgebyr
    lov_byggeloven -->|hjemmel_for| bek_byggevarer_cpr2011
    lov_byggeloven -->|hjemmel_for| bek_byggevarer_cpr2024
    lov_byggeloven -->|hjemmel_for| bek_certificering
    lov_byggeloven -->|hjemmel_for| bek_danak_byggevarer
    lov_byggeloven -->|hjemmel_for| bek_drikkevand_byggevarer
    lov_byggeloven -->|hjemmel_for| bek_individuel_maaling
    lov_byggeloven -->|hjemmel_for| bek_ladestandere
    lov_byggeloven -->|hjemmel_for| bek_sbst_opgaver
    lov_byggeloven -->|hjemmel_for| bek_skorstensfejer
    lov_byggeloven -->|hjemmel_for| kommune_alle
    lov_byggeloven -->|hjemmel_for| naevn_byggeklageenheden
    lov_byggeloven -->|hjemmel_for| reg_byggesagsgebyr
    lov_friplejeboligloven -->|hjemmel_for| bek_friplejeboliger_etablering
    lov_lejeloven -->|hjemmel_for| bek_vedligeholdelsesplaner
    lov_lejeloven -->|hjemmel_for| dom_boligretten
    bek_almen_drift -->|implementerer_EU| eu_dec_2012_21
    bek_br18 -.->|implementerer_EU| eu_dir_2010_31
    bek_br18 -.->|implementerer_EU| eu_dir_2024_1275
    bek_byggevarer_cpr2011 -->|implementerer_EU| eu_reg_2011_305
    bek_byggevarer_cpr2011 -.->|implementerer_EU| eu_reg_2019_1020
    bek_byggevarer_cpr2024 -.->|implementerer_EU| eu_reg_2019_1020
    bek_byggevarer_cpr2024 -->|implementerer_EU| eu_reg_2024_3110
    bek_danak_byggevarer -->|implementerer_EU| eu_reg_2011_305
    bek_danak_byggevarer -->|implementerer_EU| eu_reg_2024_3110
    bek_individuel_maaling -->|implementerer_EU| eu_dir_2012_27
    bek_individuel_maaling -->|implementerer_EU| eu_dir_2023_1791
    bek_ladestandere -.->|implementerer_EU| eu_dir_2010_31
    bek_ladestandere -->|implementerer_EU| eu_dir_2018_844
    lov_byggeloven -->|implementerer_EU| eu_dir_2018_844
    lov_byggeloven -.->|implementerer_EU| eu_dir_2024_1275
    dom_boligretten -->|klageinstans| naevn_ankenaevn_koebenhavn
    dom_boligretten -->|klageinstans| naevn_beboerklagenaevn
    dom_boligretten -->|klageinstans| naevn_huslejenaevn
    dom_byretterne -->|klageinstans| naevn_byggeklageenheden
    dom_domstolene -->|klageinstans| naevn_byggeklageenheden
    min_boern_aeldre_og_bolig -.->|klageinstans| sty_social_og_boligstyrelsen
    naevn_ankenaevn_koebenhavn -->|klageinstans| naevn_huslejenaevn
    naevn_byggeklageenheden -->|klageinstans| kommune_alle
    min_boern_aeldre_og_bolig -->|ressortansvar| bek_administration_private_udlejningsejendomme
    min_boern_aeldre_og_bolig -->|ressortansvar| bek_almen_drift
    min_boern_aeldre_og_bolig -->|ressortansvar| bek_almen_stoette
    min_boern_aeldre_og_bolig -->|ressortansvar| bek_almen_udlejning
    min_boern_aeldre_og_bolig -->|ressortansvar| bek_andelsbolig_oplysningspligt
    min_boern_aeldre_og_bolig -->|ressortansvar| bek_br18
    min_boern_aeldre_og_bolig -.->|ressortansvar| bek_bsf_eftersyn
    min_boern_aeldre_og_bolig -.->|ressortansvar| bek_byggesagsgebyr
    min_boern_aeldre_og_bolig -.->|ressortansvar| bek_byggevarer_cpr2011
    min_boern_aeldre_og_bolig -.->|ressortansvar| bek_byggevarer_cpr2024
    min_boern_aeldre_og_bolig -.->|ressortansvar| bek_certificering
    min_boern_aeldre_og_bolig -.->|ressortansvar| bek_danak_byggevarer
    min_boern_aeldre_og_bolig -.->|ressortansvar| bek_drikkevand_byggevarer
    min_boern_aeldre_og_bolig -->|ressortansvar| bek_friplejeboliger_etablering
    min_boern_aeldre_og_bolig -.->|ressortansvar| bek_individuel_maaling
    min_boern_aeldre_og_bolig -.->|ressortansvar| bek_ladestandere
    min_boern_aeldre_og_bolig -.->|ressortansvar| bek_sbst_opgaver
    min_boern_aeldre_og_bolig -->|ressortansvar| bek_sideaktiviteter_almene
    min_boern_aeldre_og_bolig -.->|ressortansvar| bek_skorstensfejer
    min_boern_aeldre_og_bolig -.->|ressortansvar| bek_vedligeholdelsesplaner
    min_boern_aeldre_og_bolig -->|ressortansvar| fond_blandede_byer
    min_boern_aeldre_og_bolig -.->|ressortansvar| fond_byggeskadefonden
    min_boern_aeldre_og_bolig -->|ressortansvar| fond_byggeskadefonden_bygningsfornyelse
    min_boern_aeldre_og_bolig -->|ressortansvar| fond_grundejernes_investeringsfond
    min_boern_aeldre_og_bolig -->|ressortansvar| fond_landsbyggefonden
    min_boern_aeldre_og_bolig -->|ressortansvar| kilde_parallelsamfundslister
    min_boern_aeldre_og_bolig -->|ressortansvar| lov_almenboligloven
    min_boern_aeldre_og_bolig -->|ressortansvar| lov_almenlejeloven
    min_boern_aeldre_og_bolig -->|ressortansvar| lov_andelsboligloven
    min_boern_aeldre_og_bolig -->|ressortansvar| lov_boligforholdsloven
    min_boern_aeldre_og_bolig -->|ressortansvar| lov_byfornyelsesloven
    min_boern_aeldre_og_bolig -->|ressortansvar| lov_byggeloven
    min_boern_aeldre_og_bolig -.->|ressortansvar| lov_ejerlejlighedsloven
    min_boern_aeldre_og_bolig -->|ressortansvar| lov_friplejeboligloven
    min_boern_aeldre_og_bolig -->|ressortansvar| lov_lejeloven
    min_boern_aeldre_og_bolig -.->|ressortansvar| naevn_beboerklagenaevn
    min_boern_aeldre_og_bolig -.->|ressortansvar| naevn_byggeklageenheden
    min_boern_aeldre_og_bolig -.->|ressortansvar| naevn_huslejenaevn
    min_boern_aeldre_og_bolig -.->|ressortansvar| vejl_br18_vejledninger
    min_boern_aeldre_og_bolig -->|ressortansvar| vejl_tilsyn_almen_boligsektor
    eu_kommissionen -.->|tilsyn| min_boern_aeldre_og_bolig
    kommune_alle -->|tilsyn| org_almene_boligorganisationer
    min_boern_aeldre_og_bolig -.->|tilsyn| fond_landsbyggefonden
    min_boern_aeldre_og_bolig -.->|tilsyn| org_almene_boligorganisationer
    ombud_folketingets_ombudsmand -.->|tilsyn| naevn_beboerklagenaevn
    ombud_folketingets_ombudsmand -->|tilsyn| naevn_byggeklageenheden
    ombud_folketingets_ombudsmand -.->|tilsyn| naevn_huslejenaevn
    ombud_folketingets_ombudsmand -.->|tilsyn| sty_social_og_boligstyrelsen
    sty_erhvervsstyrelsen -->|tilsyn| bek_byggevarer_cpr2024
    sty_social_og_boligstyrelsen -->|tilsyn| fond_danak
    sty_social_og_boligstyrelsen -.->|tilsyn| org_almene_boligorganisationer
    fond_grundejernes_investeringsfond -.->|udsteder| kilde_huslejenaevn_dk
    fond_landsbyggefonden -->|udsteder| reg_lbf_regulativer
    kommune_alle -->|udsteder| reg_byggesagsgebyr
    min_indenrigs_og_bolig -->|udsteder| bek_administration_private_udlejningsejendomme
    min_indenrigs_og_bolig -->|udsteder| bek_vedligeholdelsesplaner
    min_social -->|udsteder| bek_almen_drift
    min_social -->|udsteder| bek_almen_udlejning
    min_social -->|udsteder| kilde_parallelsamfundslister
    naevn_byggeklageenheden -->|udsteder| kilde_bke_afgoerelser
    naevn_byggeklageenheden -->|udsteder| kilde_naevneneshus_afgoerelser
    sty_naevnenes_hus -->|udsteder| kilde_bke_afgoerelser
    sty_social_og_boligstyrelsen -->|udsteder| bek_br18
    sty_social_og_boligstyrelsen -->|udsteder| bek_byggevarer_cpr2011
    sty_social_og_boligstyrelsen -->|udsteder| bek_byggevarer_cpr2024
    sty_social_og_boligstyrelsen -->|udsteder| bek_certificering
    sty_social_og_boligstyrelsen -.->|udsteder| bek_danak_byggevarer
    sty_social_og_boligstyrelsen -.->|udsteder| kilde_bygningsreglementet_dk
    sty_social_og_boligstyrelsen -->|udsteder| kilde_parallelsamfundslister
    sty_social_og_boligstyrelsen -->|udsteder| std_eurocodes
    sty_social_og_boligstyrelsen -->|udsteder| vejl_almen_vejledninger
    sty_social_og_boligstyrelsen -.->|udsteder| vejl_br18_brandvejledninger
    sty_social_og_boligstyrelsen -.->|udsteder| vejl_br18_vejledninger
    sty_social_og_boligstyrelsen -->|udsteder| vejl_satsvejledning_leje_almen
    sty_social_og_boligstyrelsen -->|udsteder| vejl_tilsyn_almen_boligsektor
    sty_trafik_bygge_og_boligstyrelsen -->|udsteder| bek_br18
    sty_trafik_bygge_og_boligstyrelsen -->|udsteder| vejl_individuel_maaling
    sty_social_og_boligstyrelsen -.->|udsteder| kilde_tilbudsportalen
    lov_almenlejeloven -->|hjemmel_for| bek_almen_drift
    bek_almen_drift -->|hjemmel_for| vejl_satsvejledning_leje_almen
    bek_br18 -->|implementerer_EU| eu_dir_2012_27
    bek_certificering -->|implementerer_EU| eu_dir_2005_36
    lov_almenlejeloven -->|hjemmel_for| bek_sbst_opgaver
    lov_friplejeboligloven -->|hjemmel_for| bek_sbst_opgaver
    bek_skorstensfejer -->|implementerer_EU| eu_dir_2005_36
    lov_almenboligloven -->|hjemmel_for| vejl_satsvejledning_leje_almen
    lov_almenlejeloven -->|hjemmel_for| vejl_satsvejledning_leje_almen
    lov_boligforholdsloven -->|hjemmel_for| vejl_satsvejledning_leje_almen
    sty_social_og_boligstyrelsen -->|udsteder| bek_byggesagsgebyr
    lov_forvaltningsloven -->|hjemmel_for| bek_drikkevand_byggevarer
    lov_offentlighedsloven -->|hjemmel_for| bek_drikkevand_byggevarer
    lov_andelsboligloven -->|hjemmel_for| bek_sbst_opgaver
    lov_byfornyelsesloven -->|hjemmel_for| bek_sbst_opgaver
    lov_byfornyelsesloven -->|hjemmel_for| vejl_satsvejledning_leje_almen
    lov_lejeloven -->|hjemmel_for| vejl_satsvejledning_leje_almen
    bek_sbst_opgaver -->|hjemmel_for| bek_almen_stoette
    bek_sbst_opgaver -->|hjemmel_for| bek_almen_udlejning
    bek_sbst_opgaver -->|hjemmel_for| bek_byggesagsgebyr
    bek_sbst_opgaver -->|hjemmel_for| bek_friplejeboliger_etablering
    bek_sbst_opgaver -->|hjemmel_for| bek_sideaktiviteter_almene
```

[← Overblik](oversigt.md)
