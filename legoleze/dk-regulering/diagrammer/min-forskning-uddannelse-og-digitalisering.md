# Forsknings-, Uddannelses- og Digitaliseringsministeriet

> Genereret af `scripts/build.py` fra `registry.yaml` (dato 2026-10-28). Redigér ikke i hånden.
> Fuldt optrukne pile = `verificeret`; stiplede = `sandsynlig`/`ukendt`. Grå stiplede bokse = nedlagt/omdøbt/ophævet.

Noder: 9 · kanter: 6

```mermaid
flowchart LR
    classDef ministerium fill:#1f3a5f,stroke:#0d1b2a,color:#fff
    classDef instans fill:#d7e3f4,stroke:#1f3a5f,color:#0d1b2a
    classDef klage fill:#f6dcc2,stroke:#8a4b08,color:#3b1f00
    classDef retsakt fill:#e6f2e6,stroke:#2e6b2e,color:#103010
    classDef eu fill:#fff3b0,stroke:#7a6a00,color:#333
    classDef kilde fill:#eee,stroke:#666,color:#222
    classDef nedlagt fill:#fff,stroke:#999,color:#999,stroke-dasharray:4 3
    min_forskning_uddannelse_og_digitalisering["Forsknings-, Uddannelses- og Digitaliseringsministeriet"]:::ministerium
    eu_dir_2019_1024["Direktiv (EU) 2019/1024 om åbne data og videreanvendelse af den offentlige sektors informationer"]:::eu
    eu_dir_2014_30["EMC-direktivet 2014/30/EU"]:::eu
    eu_dir_2014_53["Radioudstyrsdirektivet 2014/53/EU (RED)"]:::eu
    org_build_aau["BUILD – Institut for Byggeri, By og Miljø, Aalborg Universitet (tidl. SBi)"]:::instans
    bv_sbi_anvisninger["SBi-/BUILD-anvisninger"]:::kilde
    bv_tekniq_vejledninger["TEKNIQ's branchevejledninger (bl.a. om overtrædelse af autorisationsloven og elektronisk sameksistens/EMC)"]:::kilde
    lov_radioudstyrsloven["Lov om radioudstyr og elektromagnetiske forhold"]:::retsakt
    lov_videreanvendelsesloven["Lov om videreanvendelse af den offentlige sektors informationer (PSI-loven)"]:::retsakt
    bv_tekniq_vejledninger -->|henviser_til| lov_radioudstyrsloven
    lov_radioudstyrsloven -->|implementerer_EU| eu_dir_2014_30
    lov_radioudstyrsloven -->|implementerer_EU| eu_dir_2014_53
    lov_videreanvendelsesloven -->|implementerer_EU| eu_dir_2019_1024
    min_forskning_uddannelse_og_digitalisering -->|ressortansvar| lov_videreanvendelsesloven
    org_build_aau -->|udsteder| bv_sbi_anvisninger
```

[← Overblik](oversigt.md)
