# Justitsministeriet

> Genereret af `scripts/build.py` fra `registry.yaml` (dato 2026-10-28). Redigér ikke i hånden.
> Fuldt optrukne pile = `verificeret`; stiplede = `sandsynlig`/`ukendt`. Grå stiplede bokse = nedlagt/omdøbt/ophævet.

Noder: 37 · kanter: 60

```mermaid
flowchart LR
    classDef ministerium fill:#1f3a5f,stroke:#0d1b2a,color:#fff
    classDef instans fill:#d7e3f4,stroke:#1f3a5f,color:#0d1b2a
    classDef klage fill:#f6dcc2,stroke:#8a4b08,color:#3b1f00
    classDef retsakt fill:#e6f2e6,stroke:#2e6b2e,color:#103010
    classDef eu fill:#fff3b0,stroke:#7a6a00,color:#333
    classDef kilde fill:#eee,stroke:#666,color:#222
    classDef nedlagt fill:#fff,stroke:#999,color:#999,stroke-dasharray:4 3
    min_justits["Justitsministeriet"]:::ministerium
    sty_civilstyrelsen["Civilstyrelsen"]:::instans
    sty_domstolsstyrelsen["Domstolsstyrelsen"]:::instans
    sty_rigsadvokaten["Rigsadvokaten"]:::instans
    kilde_domsdatabasen["Domsdatabasen"]:::kilde
    kilde_eurlex["EUR-Lex"]:::kilde
    kilde_eurlex_nim["EUR-Lex: nationale gennemførelsesforanstaltninger (NIM) for direktiver"]:::kilde
    kilde_fob_database["Folketingets Ombudsmands udtalelser"]:::kilde
    kilde_folketingstidende["Folketingstidende og ft.dk-samlinger (lovforslag, bemærkninger, betænkninger, svar)"]:::kilde
    kilde_lovguiden["Lovguiden (lovguiden.dk)"]:::kilde
    kilde_lovtidende["Lovtidende"]:::kilde
    kilde_retsinformation["Retsinformation"]:::kilde
    kilde_statstidende["Statstidende"]:::kilde
    kilde_ugeskrift_for_retsvaesen["Ugeskrift for Retsvæsen (UfR, Karnov Group)"]:::kilde
    kilde_danish_law_mcp["danish-law-mcp (Ansvar Systems): bulk-høst af Retsinformation, Lovtidende A"]:::kilde
    dom_byretterne["Byretterne"]:::klage
    dom_domstolene["Domstolene (byret, landsret, Højesteret)"]:::klage
    dom_hoejesteret["Højesteret"]:::klage
    dom_landsretterne["Landsretterne (Østre og Vestre Landsret)"]:::klage
    naevn_procesbevillingsnaevnet["Procesbevillingsnævnet"]:::klage
    kilde_ministerialtidende["Ministerialtidende (nedlagt)"]:::nedlagt
    lov_arbejdsmiljoeloven["Arbejdsmiljøloven"]:::retsakt
    bek_domsdatabasen["Bekendtgørelse om Domsdatabasen"]:::retsakt
    cirk_retsinformation_afgoerelser["Cirkulære om indlæggelse af afgørelser i Retsinformation"]:::retsakt
    vejl_fob_myndighedsguiden["Folketingets Ombudsmands Myndighedsguide"]:::retsakt
    lov_forvaltningsloven["Forvaltningsloven"]:::retsakt
    lov_domstolsstyrelsesloven["Lov om Domstolsstyrelsen"]:::retsakt
    lov_miljoeoplysningsloven["Lov om aktindsigt i miljøoplysninger (miljøoplysningsloven)"]:::retsakt
    lov_offentlighedsloven["Lov om offentlighed i forvaltningen (offentlighedsloven)"]:::retsakt
    lov_retssikkerhedsloven_tvangsindgreb["Lov om retssikkerhed ved forvaltningens anvendelse af tvangsindgreb og oplysningspligter"]:::retsakt
    lov_lovtidendeloven["Lov om udgivelsen af en Lovtidende (lovtidendeloven)"]:::retsakt
    lov_retsplejeloven["Retsplejeloven"]:::retsakt
    cirk_rigsadvokatmeddelelsen_arbejdsmiljoe["Rigsadvokatmeddelelsen, afsnittet om arbejdsmiljø"]:::retsakt
    vejl_administrative_forskrifter["Vejledning om administrative forskrifter (Justitsministeriet)"]:::retsakt
    vejl_forvaltningsloven["Vejledning om forvaltningsloven (Justitsministeriet)"]:::retsakt
    vejl_offentlighedsloven["Vejledning om lov om offentlighed i forvaltningen (Justitsministeriet)"]:::retsakt
    vejl_lovkvalitet["Vejledning om lovkvalitet (Justitsministeriet)"]:::retsakt
    bek_domsdatabasen -->|henviser_til| kilde_domsdatabasen
    cirk_retsinformation_afgoerelser -->|henviser_til| kilde_retsinformation
    cirk_rigsadvokatmeddelelsen_arbejdsmiljoe -->|henviser_til| lov_arbejdsmiljoeloven
    kilde_eurlex_nim -.->|henviser_til| kilde_retsinformation
    kilde_fob_database -->|henviser_til| lov_forvaltningsloven
    kilde_fob_database -->|henviser_til| lov_offentlighedsloven
    kilde_lovguiden -.->|henviser_til| kilde_retsinformation
    kilde_lovtidende -->|henviser_til| kilde_retsinformation
    kilde_retsinformation -.->|henviser_til| kilde_eurlex
    kilde_retsinformation -->|henviser_til| kilde_folketingstidende
    kilde_ugeskrift_for_retsvaesen -.->|henviser_til| kilde_domsdatabasen
    lov_miljoeoplysningsloven -->|henviser_til| lov_forvaltningsloven
    lov_miljoeoplysningsloven -->|henviser_til| lov_offentlighedsloven
    naevn_procesbevillingsnaevnet -->|henviser_til| dom_hoejesteret
    naevn_procesbevillingsnaevnet -->|henviser_til| dom_landsretterne
    vejl_administrative_forskrifter -->|henviser_til| kilde_lovtidende
    vejl_administrative_forskrifter -->|henviser_til| kilde_retsinformation
    vejl_administrative_forskrifter -->|henviser_til| lov_lovtidendeloven
    vejl_fob_myndighedsguiden -->|henviser_til| lov_forvaltningsloven
    vejl_fob_myndighedsguiden -->|henviser_til| lov_offentlighedsloven
    vejl_forvaltningsloven -->|henviser_til| lov_forvaltningsloven
    vejl_lovkvalitet -->|henviser_til| vejl_administrative_forskrifter
    vejl_offentlighedsloven -->|henviser_til| lov_offentlighedsloven
    lov_domstolsstyrelsesloven -->|hjemmel_for| bek_domsdatabasen
    lov_domstolsstyrelsesloven -->|hjemmel_for| kilde_domsdatabasen
    lov_domstolsstyrelsesloven -->|hjemmel_for| sty_domstolsstyrelsen
    lov_lovtidendeloven -->|hjemmel_for| kilde_lovtidende
    lov_lovtidendeloven -->|hjemmel_for| kilde_ministerialtidende
    lov_retsplejeloven -->|hjemmel_for| dom_byretterne
    lov_retsplejeloven -->|hjemmel_for| dom_domstolene
    lov_retsplejeloven -->|hjemmel_for| dom_hoejesteret
    lov_retsplejeloven -->|hjemmel_for| dom_landsretterne
    lov_retsplejeloven -->|hjemmel_for| naevn_procesbevillingsnaevnet
    lov_retsplejeloven -->|hjemmel_for| sty_rigsadvokaten
    min_justits -.->|ressortansvar| bek_domsdatabasen
    min_justits -->|ressortansvar| lov_domstolsstyrelsesloven
    min_justits -->|ressortansvar| lov_forvaltningsloven
    min_justits -.->|ressortansvar| lov_lovtidendeloven
    min_justits -->|ressortansvar| lov_offentlighedsloven
    min_justits -.->|ressortansvar| lov_retsplejeloven
    min_justits -->|ressortansvar| lov_retssikkerhedsloven_tvangsindgreb
    min_justits -->|ressortansvar| sty_civilstyrelsen
    min_justits -->|ressortansvar| sty_domstolsstyrelsen
    min_justits -->|ressortansvar| sty_rigsadvokaten
    dom_byretterne -.->|udsteder| kilde_domsdatabasen
    dom_hoejesteret -.->|udsteder| kilde_domsdatabasen
    dom_landsretterne -.->|udsteder| kilde_domsdatabasen
    min_justits -.->|udsteder| cirk_retsinformation_afgoerelser
    min_justits -->|udsteder| vejl_administrative_forskrifter
    min_justits -->|udsteder| vejl_forvaltningsloven
    min_justits -->|udsteder| vejl_lovkvalitet
    min_justits -->|udsteder| vejl_offentlighedsloven
    sty_civilstyrelsen -->|udsteder| kilde_lovtidende
    sty_civilstyrelsen -.->|udsteder| kilde_ministerialtidende
    sty_civilstyrelsen -->|udsteder| kilde_retsinformation
    sty_civilstyrelsen -->|udsteder| kilde_statstidende
    sty_domstolsstyrelsen -->|udsteder| bek_domsdatabasen
    sty_domstolsstyrelsen -->|udsteder| kilde_domsdatabasen
    sty_rigsadvokaten -->|udsteder| cirk_rigsadvokatmeddelelsen_arbejdsmiljoe
    kilde_danish_law_mcp -->|henviser_til| kilde_retsinformation
```

[← Overblik](oversigt.md)
