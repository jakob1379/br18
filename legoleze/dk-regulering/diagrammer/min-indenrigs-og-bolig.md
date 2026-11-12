# Indenrigs- og Boligministeriet

> Genereret af `scripts/build.py` fra `registry.yaml` (dato 2026-10-28). Redigér ikke i hånden.
> Fuldt optrukne pile = `verificeret`; stiplede = `sandsynlig`/`ukendt`. Grå stiplede bokse = nedlagt/omdøbt/ophævet.

Noder: 5 · kanter: 4

```mermaid
flowchart LR
    classDef ministerium fill:#1f3a5f,stroke:#0d1b2a,color:#fff
    classDef instans fill:#d7e3f4,stroke:#1f3a5f,color:#0d1b2a
    classDef klage fill:#f6dcc2,stroke:#8a4b08,color:#3b1f00
    classDef retsakt fill:#e6f2e6,stroke:#2e6b2e,color:#103010
    classDef eu fill:#fff3b0,stroke:#7a6a00,color:#333
    classDef kilde fill:#eee,stroke:#666,color:#222
    classDef nedlagt fill:#fff,stroke:#999,color:#999,stroke-dasharray:4 3
    min_indenrigs_og_bolig["Indenrigs- og Boligministeriet (nedlagt)"]:::nedlagt
    sty_bolig_og_planstyrelsen["Bolig- og Planstyrelsen (nedlagt)"]:::nedlagt
    bek_administration_private_udlejningsejendomme["Bekendtgørelse om administration af private udlejningsejendomme efter § 25 i lov om boligforhold (BEK nr. 750 af 30/05/2022)"]:::retsakt
    bek_vedligeholdelsesplaner["Bekendtgørelse om vedligeholdelsesplaner for private udlejningsejendomme (BEK nr. 752 af 30/05/2022)"]:::retsakt
    vejl_vindmoeller["Vejledning om planlægning for og tilladelse til opstilling af vindmøller (VEJ nr. 9317, januar 2022)"]:::retsakt
    min_indenrigs_og_bolig -->|ressortansvar| sty_bolig_og_planstyrelsen
    min_indenrigs_og_bolig -->|udsteder| bek_administration_private_udlejningsejendomme
    min_indenrigs_og_bolig -->|udsteder| bek_vedligeholdelsesplaner
    sty_bolig_og_planstyrelsen -->|udsteder| vejl_vindmoeller
```

[← Overblik](oversigt.md)
