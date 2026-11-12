# Kulturministeriet

> Genereret af `scripts/build.py` fra `registry.yaml` (dato 2026-10-28). Redigér ikke i hånden.
> Fuldt optrukne pile = `verificeret`; stiplede = `sandsynlig`/`ukendt`. Grå stiplede bokse = nedlagt/omdøbt/ophævet.

Noder: 27 · kanter: 42

```mermaid
flowchart LR
    classDef ministerium fill:#1f3a5f,stroke:#0d1b2a,color:#fff
    classDef instans fill:#d7e3f4,stroke:#1f3a5f,color:#0d1b2a
    classDef klage fill:#f6dcc2,stroke:#8a4b08,color:#3b1f00
    classDef retsakt fill:#e6f2e6,stroke:#2e6b2e,color:#103010
    classDef eu fill:#fff3b0,stroke:#7a6a00,color:#333
    classDef kilde fill:#eee,stroke:#666,color:#222
    classDef nedlagt fill:#fff,stroke:#999,color:#999,stroke-dasharray:4 3
    min_kultur["Kulturministeriet"]:::ministerium
    raad_dansk_sprognaevn["Dansk Sprognævn"]:::instans
    raad_det_saerlige_bygningssyn["Det Særlige Bygningssyn"]:::instans
    kommune_alle["Kommunerne (98 kommunalbestyrelser)"]:::instans
    sty_slots_og_kulturstyrelsen["Slots- og Kulturstyrelsen"]:::instans
    kilde_fbb["FBB – Fredede og Bevaringsværdige Bygninger (register, inkl. SAVE-registreringer)"]:::kilde
    kilde_retskrivningsordbogen["Retskrivningsordbogen"]:::kilde
    kilde_slks_fredningsafgoerelser["Slots- og Kulturstyrelsens og Kulturministeriets afgørelser i fredningssager (publiceret på slks.dk)"]:::kilde
    org_statsanerkendte_museer["Statsanerkendte museer (arkæologisk ansvar ved anlægsarbejde)"]:::kilde
    naevn_biblioteksafgiftsnaevnet["Biblioteksafgiftsnævnet"]:::klage
    naevn_miljoe_og_foedevareklagenaevnet["Miljø- og Fødevareklagenævnet"]:::klage
    naevn_ophavsretslicensnaevnet["Ophavsretslicensnævnet"]:::klage
    naevn_radio_og_tv_naevnet["Radio- og tv-nævnet"]:::klage
    sty_kulturarvsstyrelsen["Kulturarvsstyrelsen (nedlagt)"]:::nedlagt
    sty_kulturstyrelsen["Kulturstyrelsen (nedlagt)"]:::nedlagt
    lov_dansk_sprognaevn["Bekendtgørelse af lov om Dansk Sprognævn"]:::retsakt
    lov_radio_og_fjernsynsloven["Bekendtgørelse af lov om radio- og fjernsynsvirksomhed m.v."]:::retsakt
    bek_dansk_sprognaevns_virksomhed["Bekendtgørelse om Dansk Sprognævns virksomhed og sammensætning (BEK nr. 1059 af 22/09/2024)"]:::retsakt
    bek_slks_henlaeggelse["Bekendtgørelse om henlæggelse af kulturministerens opgaver efter bygningsfredningsloven til Slots- og Kulturstyrelsen (BEK nr. 1566 af 09/12/2024)"]:::retsakt
    bek_bygningsfredning_arbejder["Bekendtgørelse om visse typer af bygningsarbejder vedrørende fredede bygninger, der ikke kræver forudgående tilladelse (Underretningsbekendtgørelsen) (BEK nr. 1565 af 09/12/2024)"]:::retsakt
    vejl_lokalplaner_og_kulturarv["Lokalplaner og kulturarv – en guide (Slots- og Kulturstyrelsen)"]:::retsakt
    lov_bygningsfredningsloven["Lov om bygningsfredning og bevaring af bygninger og bymiljøer"]:::retsakt
    lov_ophavsretsloven["Lov om ophavsret (ophavsretsloven)"]:::retsakt
    lov_planloven["Lov om planlægning (planloven)"]:::retsakt
    lov_kulturbidragsloven["Lov om visse medietjenesteudbyderes bidrag til fremme af dansk kultur (kulturbidragsloven)"]:::retsakt
    lov_museumsloven["Museumsloven"]:::retsakt
    vejl_save["SAVE – Kortlægning og registrering af bymiljøers og bygningers bevaringsværdi (Naturstyrelsen 1997; revideret af Kulturstyrelsen 2011)"]:::retsakt
    min_kultur -->|delegation| sty_slots_og_kulturstyrelsen
    kilde_slks_fredningsafgoerelser -->|henviser_til| lov_bygningsfredningsloven
    lov_bygningsfredningsloven -->|henviser_til| lov_planloven
    vejl_lokalplaner_og_kulturarv -.->|henviser_til| lov_bygningsfredningsloven
    vejl_lokalplaner_og_kulturarv -->|henviser_til| lov_planloven
    vejl_save -.->|henviser_til| lov_bygningsfredningsloven
    lov_bygningsfredningsloven -->|hjemmel_for| bek_bygningsfredning_arbejder
    lov_bygningsfredningsloven -->|hjemmel_for| bek_slks_henlaeggelse
    lov_bygningsfredningsloven -->|hjemmel_for| kommune_alle
    lov_bygningsfredningsloven -->|hjemmel_for| raad_det_saerlige_bygningssyn
    lov_museumsloven -->|hjemmel_for| kommune_alle
    lov_museumsloven -->|hjemmel_for| naevn_miljoe_og_foedevareklagenaevnet
    lov_museumsloven -.->|hjemmel_for| org_statsanerkendte_museer
    min_kultur -->|klageinstans| sty_slots_og_kulturstyrelsen
    sty_slots_og_kulturstyrelsen -->|klageinstans| org_statsanerkendte_museer
    min_kultur -->|ressortansvar| lov_bygningsfredningsloven
    min_kultur -.->|ressortansvar| lov_museumsloven
    min_kultur -.->|ressortansvar| lov_ophavsretsloven
    min_kultur -->|ressortansvar| raad_det_saerlige_bygningssyn
    min_kultur -->|ressortansvar| sty_kulturarvsstyrelsen
    min_kultur -->|ressortansvar| sty_kulturstyrelsen
    min_kultur -->|ressortansvar| sty_slots_og_kulturstyrelsen
    min_kultur -->|udsteder| bek_slks_henlaeggelse
    sty_kulturstyrelsen -.->|udsteder| vejl_save
    sty_slots_og_kulturstyrelsen -.->|udsteder| kilde_fbb
    sty_slots_og_kulturstyrelsen -->|udsteder| kilde_slks_fredningsafgoerelser
    sty_slots_og_kulturstyrelsen -->|udsteder| vejl_lokalplaner_og_kulturarv
    min_kultur -.->|ressortansvar| lov_radio_og_fjernsynsloven
    min_kultur -->|ressortansvar| lov_kulturbidragsloven
    min_kultur -.->|ressortansvar| naevn_radio_og_tv_naevnet
    lov_radio_og_fjernsynsloven -->|hjemmel_for| naevn_radio_og_tv_naevnet
    lov_kulturbidragsloven -->|hjemmel_for| naevn_radio_og_tv_naevnet
    lov_kulturbidragsloven -->|hjemmel_for| sty_slots_og_kulturstyrelsen
    naevn_radio_og_tv_naevnet -->|klageinstans| sty_slots_og_kulturstyrelsen
    min_kultur -.->|ressortansvar| naevn_ophavsretslicensnaevnet
    lov_ophavsretsloven -->|hjemmel_for| naevn_ophavsretslicensnaevnet
    min_kultur -.->|ressortansvar| naevn_biblioteksafgiftsnaevnet
    min_kultur -.->|ressortansvar| lov_dansk_sprognaevn
    min_kultur -.->|ressortansvar| raad_dansk_sprognaevn
    lov_dansk_sprognaevn -->|hjemmel_for| raad_dansk_sprognaevn
    lov_dansk_sprognaevn -->|hjemmel_for| bek_dansk_sprognaevns_virksomhed
    raad_dansk_sprognaevn -->|udsteder| kilde_retskrivningsordbogen
```

[← Overblik](oversigt.md)
