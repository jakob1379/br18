# Udlændinge- og Integrationsministeriet

> Genereret af `scripts/build.py` fra `registry.yaml` (dato 2026-10-28). Redigér ikke i hånden.
> Fuldt optrukne pile = `verificeret`; stiplede = `sandsynlig`/`ukendt`. Grå stiplede bokse = nedlagt/omdøbt/ophævet.

Noder: 18 · kanter: 31

```mermaid
flowchart LR
    classDef ministerium fill:#1f3a5f,stroke:#0d1b2a,color:#fff
    classDef instans fill:#d7e3f4,stroke:#1f3a5f,color:#0d1b2a
    classDef klage fill:#f6dcc2,stroke:#8a4b08,color:#3b1f00
    classDef retsakt fill:#e6f2e6,stroke:#2e6b2e,color:#103010
    classDef eu fill:#fff3b0,stroke:#7a6a00,color:#333
    classDef kilde fill:#eee,stroke:#666,color:#222
    classDef nedlagt fill:#fff,stroke:#999,color:#999,stroke-dasharray:4 3
    min_udlaendinge_og_integration["Udlændinge- og Integrationsministeriet"]:::ministerium
    sty_ankestyrelsen["Ankestyrelsen"]:::instans
    sty_hjemrejsestyrelsen["Hjemrejsestyrelsen"]:::instans
    sty_siri["Styrelsen for International Rekruttering og Integration (SIRI)"]:::instans
    sty_udlaendingestyrelsen["Udlændingestyrelsen"]:::instans
    kilde_fln_baggrundsmateriale["Flygtningenævnets baggrundsmateriale"]:::kilde
    kilde_fln_praksis["Flygtningenævnets praksis (resuméer)"]:::kilde
    kilde_nyidanmark["Nyidanmark.dk (Udlændingestyrelsen og SIRI)"]:::kilde
    kilde_udln_praksis["Udlændingenævnets praksis (udln.dk)"]:::kilde
    kilde_udln_aarsberetninger["Udlændingenævnets årsberetninger"]:::kilde
    dom_byretterne["Byretterne"]:::klage
    naevn_flygtningenaevnet["Flygtningenævnet"]:::klage
    ombud_folketingets_ombudsmand["Folketingets Ombudsmand"]:::klage
    naevn_udlaendingenaevnet["Udlændingenævnet"]:::klage
    bek_forretningsorden_flygtningenaevnet["Bekendtgørelse om forretningsorden for Flygtningenævnet"]:::retsakt
    bek_forretningsorden_udlaendingenaevnet["Bekendtgørelse om forretningsorden for Udlændingenævnet"]:::retsakt
    lov_hjemrejseloven["Hjemrejseloven (lov om hjemrejse for udlændinge uden lovligt ophold)"]:::retsakt
    lov_udlaendingeloven["Udlændingeloven"]:::retsakt
    min_udlaendinge_og_integration -.->|ressortansvar| sty_udlaendingestyrelsen
    min_udlaendinge_og_integration -.->|ressortansvar| sty_siri
    min_udlaendinge_og_integration -->|ressortansvar| sty_hjemrejsestyrelsen
    min_udlaendinge_og_integration -->|ressortansvar| naevn_udlaendingenaevnet
    min_udlaendinge_og_integration -->|ressortansvar| naevn_flygtningenaevnet
    min_udlaendinge_og_integration -->|ressortansvar| lov_udlaendingeloven
    min_udlaendinge_og_integration -.->|ressortansvar| lov_hjemrejseloven
    min_udlaendinge_og_integration -.->|ressortansvar| bek_forretningsorden_udlaendingenaevnet
    min_udlaendinge_og_integration -.->|ressortansvar| bek_forretningsorden_flygtningenaevnet
    lov_udlaendingeloven -.->|hjemmel_for| naevn_udlaendingenaevnet
    lov_udlaendingeloven -.->|hjemmel_for| naevn_flygtningenaevnet
    lov_udlaendingeloven -->|hjemmel_for| bek_forretningsorden_udlaendingenaevnet
    lov_udlaendingeloven -->|hjemmel_for| bek_forretningsorden_flygtningenaevnet
    bek_forretningsorden_udlaendingenaevnet -.->|hjemmel_for| naevn_udlaendingenaevnet
    bek_forretningsorden_flygtningenaevnet -.->|hjemmel_for| naevn_flygtningenaevnet
    lov_udlaendingeloven -.->|hjemmel_for| sty_udlaendingestyrelsen
    lov_udlaendingeloven -.->|hjemmel_for| sty_siri
    lov_hjemrejseloven -.->|hjemmel_for| sty_hjemrejsestyrelsen
    naevn_udlaendingenaevnet -->|klageinstans| sty_udlaendingestyrelsen
    naevn_udlaendingenaevnet -.->|klageinstans| sty_siri
    naevn_udlaendingenaevnet -->|klageinstans| sty_hjemrejsestyrelsen
    naevn_flygtningenaevnet -->|klageinstans| sty_udlaendingestyrelsen
    sty_ankestyrelsen -.->|klageinstans| sty_udlaendingestyrelsen
    dom_byretterne -.->|domstolsproevelse| naevn_udlaendingenaevnet
    ombud_folketingets_ombudsmand -.->|tilsyn| sty_hjemrejsestyrelsen
    naevn_udlaendingenaevnet -->|udsteder| kilde_udln_praksis
    naevn_udlaendingenaevnet -->|udsteder| kilde_udln_aarsberetninger
    naevn_flygtningenaevnet -->|udsteder| kilde_fln_praksis
    naevn_flygtningenaevnet -->|udsteder| kilde_fln_baggrundsmateriale
    sty_udlaendingestyrelsen -->|udsteder| kilde_nyidanmark
    sty_siri -->|udsteder| kilde_nyidanmark
```

[← Overblik](oversigt.md)
