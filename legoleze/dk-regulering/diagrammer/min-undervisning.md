# Undervisningsministeriet

> Genereret af `scripts/build.py` fra `registry.yaml` (dato 2026-10-28). Redigér ikke i hånden.
> Fuldt optrukne pile = `verificeret`; stiplede = `sandsynlig`/`ukendt`. Grå stiplede bokse = nedlagt/omdøbt/ophævet.

Noder: 18 · kanter: 23

```mermaid
flowchart LR
    classDef ministerium fill:#1f3a5f,stroke:#0d1b2a,color:#fff
    classDef instans fill:#d7e3f4,stroke:#1f3a5f,color:#0d1b2a
    classDef klage fill:#f6dcc2,stroke:#8a4b08,color:#3b1f00
    classDef retsakt fill:#e6f2e6,stroke:#2e6b2e,color:#103010
    classDef eu fill:#fff3b0,stroke:#7a6a00,color:#333
    classDef kilde fill:#eee,stroke:#666,color:#222
    classDef nedlagt fill:#fff,stroke:#999,color:#999,stroke-dasharray:4 3
    min_undervisning["Undervisningsministeriet"]:::ministerium
    eu_dir_2005_36["Europa-Parlamentets og Rådets direktiv 2005/36/EF af 7. september 2005 om anerkendelse af erhvervsmæssige kvalifikationer"]:::eu
    kommune_alle["Kommunerne (98 kommunalbestyrelser)"]:::instans
    sty_stil["Styrelsen for It og Læring (STIL)"]:::instans
    sty_stuk["Styrelsen for Undervisning og Kvalitet (STUK)"]:::instans
    kilde_k_meddelelser_specialundervisning["K-meddelelser fra Klagenævnet for Specialundervisning (ast.dk)"]:::kilde
    kilde_stuk_tilsynsberetninger["STUK: tilsynsplaner og tilsynsberetninger"]:::kilde
    naevn_ankenaevn_oplaeringsvirksomheder["Ankenævnet vedrørende Oplæringsvirksomheder (tidl. Ankenævnet vedrørende Praktikvirksomheder)"]:::klage
    naevn_klagenaevnet_specialundervisning["Klagenævnet for Specialundervisning"]:::klage
    naevn_tvistighedsnaevnet["Tvistighedsnævnet"]:::klage
    bek_ankenaevn_praktikvirksomheder["Bekendtgørelse om Ankenævnet vedrørende Praktikvirksomheder (BEK nr. 1517 af 13/12/2007)"]:::retsakt
    bek_tvistighedsnaevnet["Bekendtgørelse om Tvistighedsnævnet"]:::retsakt
    bek_forretningsorden_klagenaevnet_specialundervisning["Bekendtgørelse om forretningsorden for Klagenævnet for Specialundervisning (BEK nr. 998 af 15/09/2014)"]:::retsakt
    lov_folkeskoleloven["Folkeskoleloven"]:::retsakt
    lov_gymnasieloven["Lov om de gymnasiale uddannelser (gymnasieloven)"]:::retsakt
    lov_erhvervsuddannelser["Lov om erhvervsuddannelser (erhvervsuddannelsesloven)"]:::retsakt
    lov_friskoleloven["Lov om friskoler og private grundskoler m.v. (friskoleloven)"]:::retsakt
    lov_institutioner_almengymnasiale["Lov om institutioner for almengymnasiale uddannelser og almen voksenuddannelse m.v."]:::retsakt
    min_undervisning -.->|ressortansvar| lov_erhvervsuddannelser
    lov_erhvervsuddannelser -->|hjemmel_for| naevn_tvistighedsnaevnet
    lov_erhvervsuddannelser -->|hjemmel_for| bek_tvistighedsnaevnet
    min_undervisning -->|ressortansvar| sty_stuk
    min_undervisning -->|ressortansvar| sty_stil
    min_undervisning -.->|ressortansvar| naevn_klagenaevnet_specialundervisning
    min_undervisning -->|ressortansvar| bek_forretningsorden_klagenaevnet_specialundervisning
    min_undervisning -->|ressortansvar| lov_folkeskoleloven
    min_undervisning -->|ressortansvar| lov_friskoleloven
    min_undervisning -->|ressortansvar| lov_gymnasieloven
    min_undervisning -.->|ressortansvar| lov_institutioner_almengymnasiale
    lov_folkeskoleloven -.->|hjemmel_for| naevn_klagenaevnet_specialundervisning
    lov_folkeskoleloven -->|hjemmel_for| bek_forretningsorden_klagenaevnet_specialundervisning
    naevn_klagenaevnet_specialundervisning -.->|klageinstans| kommune_alle
    sty_stuk -->|udsteder| kilde_stuk_tilsynsberetninger
    naevn_klagenaevnet_specialundervisning -->|udsteder| kilde_k_meddelelser_specialundervisning
    lov_erhvervsuddannelser -->|hjemmel_for| naevn_ankenaevn_oplaeringsvirksomheder
    lov_erhvervsuddannelser -->|hjemmel_for| bek_ankenaevn_praktikvirksomheder
    lov_friskoleloven -.->|hjemmel_for| sty_stuk
    lov_gymnasieloven -.->|hjemmel_for| sty_stuk
    lov_folkeskoleloven -->|implementerer_EU| eu_dir_2005_36
    bek_tvistighedsnaevnet -.->|hjemmel_for| naevn_tvistighedsnaevnet
    bek_ankenaevn_praktikvirksomheder -->|hjemmel_for| naevn_ankenaevn_oplaeringsvirksomheder
```

[← Overblik](oversigt.md)
