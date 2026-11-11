# Skatte- og Vækstministeriet

> Genereret af `scripts/build.py` fra `registry.yaml` (dato 2026-10-28). Redigér ikke i hånden.
> Fuldt optrukne pile = `verificeret`; stiplede = `sandsynlig`/`ukendt`. Grå stiplede bokse = nedlagt/omdøbt/ophævet.

Noder: 5 · kanter: 5

```mermaid
flowchart LR
    classDef ministerium fill:#1f3a5f,stroke:#0d1b2a,color:#fff
    classDef instans fill:#d7e3f4,stroke:#1f3a5f,color:#0d1b2a
    classDef klage fill:#f6dcc2,stroke:#8a4b08,color:#3b1f00
    classDef retsakt fill:#e6f2e6,stroke:#2e6b2e,color:#103010
    classDef eu fill:#fff3b0,stroke:#7a6a00,color:#333
    classDef kilde fill:#eee,stroke:#666,color:#222
    classDef nedlagt fill:#fff,stroke:#999,color:#999,stroke-dasharray:4 3
    min_skat_og_vaekst["Skatte- og Vækstministeriet"]:::ministerium
    kommune_alle["Kommunerne (98 kommunalbestyrelser)"]:::instans
    sty_vurderingsstyrelsen["Vurderingsstyrelsen"]:::instans
    bek_bbr_ajourfoering["Bekendtgørelse om ajourføring af Bygnings- og Boligregistret (BBR) (BEK nr. 1010 af 24/10/2012)"]:::retsakt
    lov_bbr_loven["Lov om bygnings- og boligregistrering (BBR-loven)"]:::retsakt
    lov_bbr_loven -->|hjemmel_for| bek_bbr_ajourfoering
    lov_bbr_loven -->|hjemmel_for| kommune_alle
    min_skat_og_vaekst -.->|ressortansvar| lov_bbr_loven
    min_skat_og_vaekst -->|ressortansvar| sty_vurderingsstyrelsen
    sty_vurderingsstyrelsen -->|tilsyn| kommune_alle
```

[← Overblik](oversigt.md)
