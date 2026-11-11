# By-, Land- og Kirkeministeriet

> Genereret af `scripts/build.py` fra `registry.yaml` (dato 2026-10-28). Redigér ikke i hånden.
> Fuldt optrukne pile = `verificeret`; stiplede = `sandsynlig`/`ukendt`. Grå stiplede bokse = nedlagt/omdøbt/ophævet.

Noder: 12 · kanter: 13

```mermaid
flowchart LR
    classDef ministerium fill:#1f3a5f,stroke:#0d1b2a,color:#fff
    classDef instans fill:#d7e3f4,stroke:#1f3a5f,color:#0d1b2a
    classDef klage fill:#f6dcc2,stroke:#8a4b08,color:#3b1f00
    classDef retsakt fill:#e6f2e6,stroke:#2e6b2e,color:#103010
    classDef eu fill:#fff3b0,stroke:#7a6a00,color:#333
    classDef kilde fill:#eee,stroke:#666,color:#222
    classDef nedlagt fill:#fff,stroke:#999,color:#999,stroke-dasharray:4 3
    min_by_land_og_kirke["By-, Land- og Kirkeministeriet (nedlagt)"]:::nedlagt
    kommune_alle["Kommunerne (98 kommunalbestyrelser)"]:::instans
    sty_plan_og_landdistriktsstyrelsen["Plan- og Landdistriktsstyrelsen"]:::instans
    kilde_plandata["Plandata.dk"]:::kilde
    naevn_planklagenaevnet["Planklagenævnet"]:::klage
    min_by_land_og_transport["By-, Land- og Transportministeriet"]:::ministerium
    bek_plandata["Bekendtgørelse om Plandata.dk (BEK nr. 508 af 16/05/2025)"]:::retsakt
    bek_plst_henlaeggelse["Bekendtgørelse om henlæggelse af visse opgaver og beføjelser til Plan- og Landdistriktsstyrelsen (BEK nr. 470/2023)"]:::retsakt
    plan_kyst_sommerhusomraader_2025["Landsplandirektiv for udlægning og omplacering af sommerhusområder i kystnærhedszonen 2025 (BEK nr. 1152/2025)"]:::retsakt
    plan_kyst_udviklingsomraader_2025["Landsplandirektiv for udviklingsområder i kystnærhedszonen 2025 (BEK nr. 1153/2025)"]:::retsakt
    vejl_nationale_interesser["Oversigt over nationale interesser i kommuneplanlægning (1. oktober 2025)"]:::retsakt
    vejl_planloven_vejledninger["Vejledninger til planloven (samling)"]:::retsakt
    min_by_land_og_kirke -->|delegation| sty_plan_og_landdistriktsstyrelsen
    min_by_land_og_transport -.->|delegation| sty_plan_og_landdistriktsstyrelsen
    naevn_planklagenaevnet -.->|klageinstans| sty_plan_og_landdistriktsstyrelsen
    min_by_land_og_kirke -->|ressortansvar| sty_plan_og_landdistriktsstyrelsen
    sty_plan_og_landdistriktsstyrelsen -->|tilsyn| kommune_alle
    min_by_land_og_kirke -->|udsteder| plan_kyst_sommerhusomraader_2025
    min_by_land_og_kirke -->|udsteder| plan_kyst_udviklingsomraader_2025
    sty_plan_og_landdistriktsstyrelsen -.->|udsteder| bek_plandata
    sty_plan_og_landdistriktsstyrelsen -->|udsteder| kilde_plandata
    sty_plan_og_landdistriktsstyrelsen -->|udsteder| vejl_nationale_interesser
    sty_plan_og_landdistriktsstyrelsen -->|udsteder| vejl_planloven_vejledninger
    min_by_land_og_kirke -->|udsteder| bek_plst_henlaeggelse
    bek_plandata -->|hjemmel_for| kilde_plandata
```

[← Overblik](oversigt.md)
