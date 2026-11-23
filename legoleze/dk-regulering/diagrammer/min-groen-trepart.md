# Ministeriet for Grøn Trepart (29/8/2024-3/6/2026)

> Genereret af `scripts/build.py` fra `registry.yaml` (dato 2026-10-28). Redigér ikke i hånden.
> Fuldt optrukne pile = `verificeret`; stiplede = `sandsynlig`/`ukendt`. Grå stiplede bokse = nedlagt/omdøbt/ophævet.

Noder: 9 · kanter: 10

```mermaid
flowchart LR
    classDef ministerium fill:#1f3a5f,stroke:#0d1b2a,color:#fff
    classDef instans fill:#d7e3f4,stroke:#1f3a5f,color:#0d1b2a
    classDef klage fill:#f6dcc2,stroke:#8a4b08,color:#3b1f00
    classDef retsakt fill:#e6f2e6,stroke:#2e6b2e,color:#103010
    classDef eu fill:#fff3b0,stroke:#7a6a00,color:#333
    classDef kilde fill:#eee,stroke:#666,color:#222
    classDef nedlagt fill:#fff,stroke:#999,color:#999,stroke-dasharray:4 3
    min_groen_trepart["Ministeriet for Grøn Trepart (29/8/2024-3/6/2026) (omdøbt)"]:::nedlagt
    sty_naturstyrelsen["Naturstyrelsen"]:::instans
    sty_groen_arealomlaegning_og_vandmiljoe["Styrelsen for Grøn Arealomlægning og Vandmiljø (SGAV)"]:::instans
    kilde_kgl_res_2024_08_29["Kongelig resolution af 29. august 2024 (oprettelse af Ministeriet for Grøn Trepart)"]:::kilde
    kilde_kgl_res_2026_06_03["Kongelig resolution af 3. juni 2026 (ressortændringer ved dannelsen af S-SF-M-RV-regeringen)"]:::kilde
    naevn_miljoe_og_foedevareklagenaevnet["Miljø- og Fødevareklagenævnet"]:::klage
    min_natur_og_dyrevelfaerd["Ministeriet for Natur og Dyrevelfærd"]:::ministerium
    lov_naturbeskyttelsesloven["Lov om naturbeskyttelse (naturbeskyttelsesloven)"]:::retsakt
    plan_natura2000_planer["Natura 2000-planer (3. planperiode 2022-2027)"]:::retsakt
    min_natur_og_dyrevelfaerd -.->|delegation| sty_groen_arealomlaegning_og_vandmiljoe
    min_natur_og_dyrevelfaerd -.->|delegation| sty_naturstyrelsen
    kilde_kgl_res_2024_08_29 -->|henviser_til| min_groen_trepart
    kilde_kgl_res_2026_06_03 -->|henviser_til| min_groen_trepart
    lov_naturbeskyttelsesloven -.->|hjemmel_for| sty_groen_arealomlaegning_og_vandmiljoe
    naevn_miljoe_og_foedevareklagenaevnet -->|klageinstans| sty_groen_arealomlaegning_og_vandmiljoe
    min_groen_trepart -.->|ressortansvar| sty_groen_arealomlaegning_og_vandmiljoe
    min_groen_trepart -->|ressortansvar| sty_naturstyrelsen
    sty_groen_arealomlaegning_og_vandmiljoe -.->|udsteder| plan_natura2000_planer
    naevn_miljoe_og_foedevareklagenaevnet -.->|klageinstans| sty_naturstyrelsen
```

[← Overblik](oversigt.md)
