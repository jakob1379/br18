# Statsministeriet

> Genereret af `scripts/build.py` fra `registry.yaml` (dato 2026-10-28). Redigér ikke i hånden.
> Fuldt optrukne pile = `verificeret`; stiplede = `sandsynlig`/`ukendt`. Grå stiplede bokse = nedlagt/omdøbt/ophævet.

Noder: 17 · kanter: 15

```mermaid
flowchart LR
    classDef ministerium fill:#1f3a5f,stroke:#0d1b2a,color:#fff
    classDef instans fill:#d7e3f4,stroke:#1f3a5f,color:#0d1b2a
    classDef klage fill:#f6dcc2,stroke:#8a4b08,color:#3b1f00
    classDef retsakt fill:#e6f2e6,stroke:#2e6b2e,color:#103010
    classDef eu fill:#fff3b0,stroke:#7a6a00,color:#333
    classDef kilde fill:#eee,stroke:#666,color:#222
    classDef nedlagt fill:#fff,stroke:#999,color:#999,stroke-dasharray:4 3
    min_statsministeriet["Statsministeriet"]:::ministerium
    kilde_kgl_res_2024_08_29["Kongelig resolution af 29. august 2024 (oprettelse af Ministeriet for Grøn Trepart)"]:::kilde
    kilde_kgl_res_2026_06_03["Kongelig resolution af 3. juni 2026 (ressortændringer ved dannelsen af S-SF-M-RV-regeringen)"]:::kilde
    ombud_folketingets_ombudsmand["Folketingets Ombudsmand"]:::klage
    min_klima_energi_og_forsyning["Klima-, Energi- og Forsyningsministeriet"]:::ministerium
    min_miljoe["Miljøministeriet"]:::ministerium
    min_natur_og_dyrevelfaerd["Ministeriet for Natur og Dyrevelfærd"]:::ministerium
    min_miljoe_og_ligestilling["Miljø- og Ligestillingsministeriet (2024-3/6/2026) (omdøbt)"]:::nedlagt
    min_groen_trepart["Ministeriet for Grøn Trepart (29/8/2024-3/6/2026) (omdøbt)"]:::nedlagt
    bek_ressortoverfoersel_bolig_2026["Bekendtgørelse nr. 514 af 8. juni 2026 om ressortoverførsel (kgl. resolution): bolig- og byggeområdet overføres fra Social- og Boligministeriet til Børne-, Ældre- og Boligministeriet"]:::retsakt
    bek_br18["Bekendtgørelse om bygningsreglement 2018 (BR18)"]:::retsakt
    lov_byggeloven["Byggeloven (lov om byggeri)"]:::retsakt
    lov_grundloven["Danmarks Riges Grundlov"]:::retsakt
    lov_almenboligloven["Lov om almene boliger m.v. (almenboligloven)"]:::retsakt
    lov_byfornyelsesloven["Lov om byfornyelse og udvikling af byer (byfornyelsesloven)"]:::retsakt
    lov_husdyrbrugloven["Lov om husdyrbrug og anvendelse af gødning m.v. (husdyrbrugloven; tidl. lov om miljøgodkendelse m.v. af husdyrbrug)"]:::retsakt
    lov_lejeloven["Lov om leje (lejeloven)"]:::retsakt
    bek_ressortoverfoersel_bolig_2026 -.->|henviser_til| bek_br18
    bek_ressortoverfoersel_bolig_2026 -->|henviser_til| lov_almenboligloven
    bek_ressortoverfoersel_bolig_2026 -->|henviser_til| lov_byfornyelsesloven
    bek_ressortoverfoersel_bolig_2026 -.->|henviser_til| lov_byggeloven
    bek_ressortoverfoersel_bolig_2026 -.->|henviser_til| lov_lejeloven
    kilde_kgl_res_2024_08_29 -->|henviser_til| lov_husdyrbrugloven
    kilde_kgl_res_2024_08_29 -->|henviser_til| min_groen_trepart
    kilde_kgl_res_2026_06_03 -->|henviser_til| min_groen_trepart
    kilde_kgl_res_2026_06_03 -->|henviser_til| min_klima_energi_og_forsyning
    kilde_kgl_res_2026_06_03 -->|henviser_til| min_miljoe
    kilde_kgl_res_2026_06_03 -->|henviser_til| min_miljoe_og_ligestilling
    kilde_kgl_res_2026_06_03 -->|henviser_til| min_natur_og_dyrevelfaerd
    lov_grundloven -->|hjemmel_for| ombud_folketingets_ombudsmand
    min_statsministeriet -.->|ressortansvar| lov_grundloven
    min_statsministeriet -.->|udsteder| bek_ressortoverfoersel_bolig_2026
```

[← Overblik](oversigt.md)
