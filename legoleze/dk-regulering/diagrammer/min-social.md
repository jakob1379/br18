# Socialministeriet

> Genereret af `scripts/build.py` fra `registry.yaml` (dato 2026-10-28). Redigér ikke i hånden.
> Fuldt optrukne pile = `verificeret`; stiplede = `sandsynlig`/`ukendt`. Grå stiplede bokse = nedlagt/omdøbt/ophævet.

Noder: 45 · kanter: 55

```mermaid
flowchart LR
    classDef ministerium fill:#1f3a5f,stroke:#0d1b2a,color:#fff
    classDef instans fill:#d7e3f4,stroke:#1f3a5f,color:#0d1b2a
    classDef klage fill:#f6dcc2,stroke:#8a4b08,color:#3b1f00
    classDef retsakt fill:#e6f2e6,stroke:#2e6b2e,color:#103010
    classDef eu fill:#fff3b0,stroke:#7a6a00,color:#333
    classDef kilde fill:#eee,stroke:#666,color:#222
    classDef nedlagt fill:#fff,stroke:#999,color:#999,stroke-dasharray:4 3
    min_social["Socialministeriet"]:::ministerium
    eu_reg_2011_305["Byggevareforordningen (EU) nr. 305/2011 (CPR)"]:::eu
    eu_dir_2024_1275["Direktiv (EU) 2024/1275 om bygningers energimæssige ydeevne (omarbejdning, EPBD)"]:::eu
    eu_reg_2019_1020["Markedsovervågningsforordningen (EU) 2019/1020"]:::eu
    eu_reg_2024_3110["Revideret byggevareforordning (EU) 2024/3110"]:::eu
    sty_ankestyrelsen["Ankestyrelsen"]:::instans
    fond_danak["DANAK (nationalt akkrediteringsorgan)"]:::instans
    sty_erhvervsstyrelsen["Erhvervsstyrelsen"]:::instans
    kommune_redningsberedskaber["Fælleskommunale redningsberedskaber (§ 60-fællesskaber med fælles beredskabskommission)"]:::instans
    kommune_alle["Kommunerne (98 kommunalbestyrelser)"]:::instans
    region_alle["Regionerne (5 regionsråd)"]:::instans
    sty_social_og_boligstyrelsen["Social- og Boligstyrelsen"]:::instans
    org_udbetaling_danmark["Udbetaling Danmark"]:::instans
    org_certificeringsorganer["Akkrediterede certificeringsorganer for brandrådgivere (og statikere)"]:::kilde
    org_almene_boligorganisationer["Almene boligorganisationer og afdelinger"]:::kilde
    kilde_ast_amkn["Ankestyrelsen – Arbejdsmiljøklagenævnets publikationer (ast.dk)"]:::kilde
    kilde_ast_principmeddelelser["Ankestyrelsens principmeddelelser og tilsynsudtalelser"]:::kilde
    kilde_ast_tilsynsudtalelser["Ankestyrelsens udtalelsesdatabase (kommunaltilsynet)"]:::kilde
    std_eurocodes["Eurocodes (DS/EN 1990-1999) med danske nationale annekser"]:::kilde
    kilde_parallelsamfundslister["Liste over parallelsamfund og liste over omdannelsesområder (offentliggøres årligt 1. december efter almenboligloven § 61 a)"]:::kilde
    kilde_bygningsreglementet_dk["bygningsreglementet.dk"]:::kilde
    naevn_arbejdsmiljoeklagenaevnet["Arbejdsmiljøklagenævnet"]:::klage
    ombud_folketingets_ombudsmand["Folketingets Ombudsmand"]:::klage
    min_boern_aeldre_og_bolig["Børne-, Ældre- og Boligministeriet"]:::ministerium
    min_oekonomi_og_indenrigs["Økonomi- og Indenrigsministeriet"]:::ministerium
    eu_dir_2010_31["Direktiv 2010/31/EU om bygningers energimæssige ydeevne (EPBD, som ændret ved 2018/844) (ophævet)"]:::nedlagt
    eu_dec_2012_21["Kommissionens afgørelse 2012/21/EU af 20. december 2011 om SGEI-kompensation (ophævet)"]:::nedlagt
    bek_danak_byggevarer["Bekendtgørelse om DANAK's opgaver vedrørende notificerede organer, der fører 3. partskontrol med byggevarer, og om tekniske vurderingsorganer (BEK nr. 1744 af 2025)"]:::retsakt
    bek_sbst_opgaver["Bekendtgørelse om Social- og Boligstyrelsens opgaver og beføjelser samt klageadgang på bolig- og byggeområdet (BEK nr. 519/2023)"]:::retsakt
    bek_br18["Bekendtgørelse om bygningsreglement 2018 (BR18)"]:::retsakt
    bek_certificering["Bekendtgørelse om certificeringsordninger for dokumentation af tekniske forhold i bygningsreglementet (statikere og brandrådgivere)"]:::retsakt
    bek_almen_drift["Bekendtgørelse om drift af almene boliger m.v. (driftsbekendtgørelsen)"]:::retsakt
    bek_byggevarer_cpr2011["Bekendtgørelse om markedsføring og markedsovervågning af byggevarer (efter forordning 305/2011)"]:::retsakt
    bek_byggevarer_cpr2024["Bekendtgørelse om markedsføring og markedsovervågning af byggevarer efter den reviderede byggevareforordning"]:::retsakt
    bek_almen_udlejning["Bekendtgørelse om udlejning af almene boliger m.v."]:::retsakt
    vejl_br18_vejledninger["Bygningsreglementets vejledninger og 'Spørgsmål og svar' (samling)"]:::retsakt
    reg_byggesagsgebyr["Kommunale gebyrer for byggesagsbehandling (gebyrinstruks/takstblad)"]:::retsakt
    lov_kommunestyrelsesloven["Kommunestyrelsesloven (lov om kommunernes styrelse)"]:::retsakt
    lov_boligstoetteloven["Lov om individuel boligstøtte (boligstøtteloven)"]:::retsakt
    lov_regionsloven["Lov om regioner og om nedlæggelse af amtskommunerne, Hovedstadens Udviklingsråd og Hovedstadens Sygehusfællesskab (regionsloven)"]:::retsakt
    lov_retssikkerhedsloven_social["Lov om retssikkerhed og administration på det sociale område (retssikkerhedsloven)"]:::retsakt
    vejl_satsvejledning_leje_almen["Vejledning om regulering af satser i lejelovgivningen og almenboligloven for 2026 (VEJ 9886/2025)"]:::retsakt
    vejl_tilsyn_almen_boligsektor["Vejledning om tilsyn med den almene boligsektor (Social- og Boligstyrelsen, juni 2023)"]:::retsakt
    vejl_almen_vejledninger["Vejledninger på almenområdet fra Social- og Boligstyrelsen og forgængere (samling)"]:::retsakt
    vejl_br18_brandvejledninger["Vejledninger til BR18 kapitel 5 Brand (brandvejledningerne: præaccepterede løsninger, brandklasser, certificerede brandrådgivere, brandteknisk dimensionering, kontrol)"]:::retsakt
    min_boern_aeldre_og_bolig -.->|delegation| sty_social_og_boligstyrelsen
    kilde_ast_principmeddelelser -->|henviser_til| lov_boligstoetteloven
    kilde_ast_principmeddelelser -->|henviser_til| lov_kommunestyrelsesloven
    bek_sbst_opgaver -->|hjemmel_for| sty_social_og_boligstyrelsen
    lov_kommunestyrelsesloven -->|hjemmel_for| sty_ankestyrelsen
    lov_regionsloven -->|hjemmel_for| sty_ankestyrelsen
    lov_retssikkerhedsloven_social -->|hjemmel_for| sty_ankestyrelsen
    min_boern_aeldre_og_bolig -.->|klageinstans| sty_social_og_boligstyrelsen
    sty_ankestyrelsen -->|klageinstans| kommune_alle
    sty_ankestyrelsen -->|klageinstans| org_udbetaling_danmark
    min_social -.->|ressortansvar| lov_retssikkerhedsloven_social
    min_social -->|ressortansvar| sty_ankestyrelsen
    min_social -.->|ressortansvar| sty_social_og_boligstyrelsen
    min_oekonomi_og_indenrigs -->|tilsyn| sty_ankestyrelsen
    ombud_folketingets_ombudsmand -.->|tilsyn| sty_ankestyrelsen
    ombud_folketingets_ombudsmand -.->|tilsyn| sty_social_og_boligstyrelsen
    sty_ankestyrelsen -->|tilsyn| kommune_alle
    sty_ankestyrelsen -->|tilsyn| kommune_redningsberedskaber
    sty_ankestyrelsen -->|tilsyn| region_alle
    sty_social_og_boligstyrelsen -->|tilsyn| fond_danak
    sty_social_og_boligstyrelsen -.->|tilsyn| org_almene_boligorganisationer
    min_social -->|udsteder| bek_almen_drift
    min_social -->|udsteder| bek_almen_udlejning
    min_social -->|udsteder| kilde_parallelsamfundslister
    naevn_arbejdsmiljoeklagenaevnet -->|udsteder| kilde_ast_amkn
    sty_ankestyrelsen -->|udsteder| kilde_ast_amkn
    sty_ankestyrelsen -->|udsteder| kilde_ast_principmeddelelser
    sty_ankestyrelsen -->|udsteder| kilde_ast_tilsynsudtalelser
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
    bek_br18 -->|hjemmel_for| reg_byggesagsgebyr
    bek_byggevarer_cpr2011 -->|hjemmel_for| sty_erhvervsstyrelsen
    bek_byggevarer_cpr2024 -.->|hjemmel_for| sty_erhvervsstyrelsen
    bek_certificering -->|hjemmel_for| org_certificeringsorganer
    bek_danak_byggevarer -->|hjemmel_for| fond_danak
    bek_almen_drift -->|implementerer_EU| eu_dec_2012_21
    bek_br18 -.->|implementerer_EU| eu_dir_2010_31
    bek_br18 -.->|implementerer_EU| eu_dir_2024_1275
    bek_byggevarer_cpr2011 -->|implementerer_EU| eu_reg_2011_305
    bek_byggevarer_cpr2011 -.->|implementerer_EU| eu_reg_2019_1020
    bek_byggevarer_cpr2024 -.->|implementerer_EU| eu_reg_2019_1020
    bek_byggevarer_cpr2024 -->|implementerer_EU| eu_reg_2024_3110
    bek_danak_byggevarer -->|implementerer_EU| eu_reg_2011_305
    bek_danak_byggevarer -->|implementerer_EU| eu_reg_2024_3110
```

[← Overblik](oversigt.md)
