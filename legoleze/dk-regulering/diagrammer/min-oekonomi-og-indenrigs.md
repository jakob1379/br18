# Økonomi- og Indenrigsministeriet

> Genereret af `scripts/build.py` fra `registry.yaml` (dato 2026-10-28). Redigér ikke i hånden.
> Fuldt optrukne pile = `verificeret`; stiplede = `sandsynlig`/`ukendt`. Grå stiplede bokse = nedlagt/omdøbt/ophævet.

Noder: 11 · kanter: 14

```mermaid
flowchart LR
    classDef ministerium fill:#1f3a5f,stroke:#0d1b2a,color:#fff
    classDef instans fill:#d7e3f4,stroke:#1f3a5f,color:#0d1b2a
    classDef klage fill:#f6dcc2,stroke:#8a4b08,color:#3b1f00
    classDef retsakt fill:#e6f2e6,stroke:#2e6b2e,color:#103010
    classDef eu fill:#fff3b0,stroke:#7a6a00,color:#333
    classDef kilde fill:#eee,stroke:#666,color:#222
    classDef nedlagt fill:#fff,stroke:#999,color:#999,stroke-dasharray:4 3
    min_oekonomi_og_indenrigs["Økonomi- og Indenrigsministeriet"]:::ministerium
    sty_ankestyrelsen["Ankestyrelsen"]:::instans
    kommune_redningsberedskaber["Fælleskommunale redningsberedskaber (§ 60-fællesskaber med fælles beredskabskommission)"]:::instans
    kommune_alle["Kommunerne (98 kommunalbestyrelser)"]:::instans
    region_alle["Regionerne (5 regionsråd)"]:::instans
    kilde_ast_principmeddelelser["Ankestyrelsens principmeddelelser og tilsynsudtalelser"]:::kilde
    kilde_ast_tilsynsudtalelser["Ankestyrelsens udtalelsesdatabase (kommunaltilsynet)"]:::kilde
    kilde_kommunale_dagsordener["Kommunale og regionale dagsordener og referater (beslutningsprotokoller)"]:::kilde
    org_statsforvaltningen["Statsforvaltningen (nedlagt)"]:::nedlagt
    lov_kommunestyrelsesloven["Kommunestyrelsesloven (lov om kommunernes styrelse)"]:::retsakt
    lov_regionsloven["Lov om regioner og om nedlæggelse af amtskommunerne, Hovedstadens Udviklingsråd og Hovedstadens Sygehusfællesskab (regionsloven)"]:::retsakt
    kilde_ast_principmeddelelser -->|henviser_til| lov_kommunestyrelsesloven
    lov_kommunestyrelsesloven -->|hjemmel_for| kilde_kommunale_dagsordener
    lov_kommunestyrelsesloven -->|hjemmel_for| kommune_alle
    lov_kommunestyrelsesloven -->|hjemmel_for| kommune_redningsberedskaber
    lov_kommunestyrelsesloven -->|hjemmel_for| sty_ankestyrelsen
    lov_regionsloven -->|hjemmel_for| region_alle
    lov_regionsloven -->|hjemmel_for| sty_ankestyrelsen
    min_oekonomi_og_indenrigs -->|ressortansvar| lov_kommunestyrelsesloven
    min_oekonomi_og_indenrigs -.->|ressortansvar| lov_regionsloven
    min_oekonomi_og_indenrigs -->|ressortansvar| org_statsforvaltningen
    min_oekonomi_og_indenrigs -->|tilsyn| kommune_alle
    min_oekonomi_og_indenrigs -->|tilsyn| region_alle
    min_oekonomi_og_indenrigs -->|tilsyn| sty_ankestyrelsen
    sty_ankestyrelsen -->|udsteder| kilde_ast_tilsynsudtalelser
```

[← Overblik](oversigt.md)
