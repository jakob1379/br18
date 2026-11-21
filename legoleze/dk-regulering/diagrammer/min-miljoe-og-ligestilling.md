# Miljø- og Ligestillingsministeriet (2024-3/6/2026)

> Genereret af `scripts/build.py` fra `registry.yaml` (dato 2026-10-28). Redigér ikke i hånden.
> Fuldt optrukne pile = `verificeret`; stiplede = `sandsynlig`/`ukendt`. Grå stiplede bokse = nedlagt/omdøbt/ophævet.

Noder: 30 · kanter: 34

```mermaid
flowchart LR
    classDef ministerium fill:#1f3a5f,stroke:#0d1b2a,color:#fff
    classDef instans fill:#d7e3f4,stroke:#1f3a5f,color:#0d1b2a
    classDef klage fill:#f6dcc2,stroke:#8a4b08,color:#3b1f00
    classDef retsakt fill:#e6f2e6,stroke:#2e6b2e,color:#103010
    classDef eu fill:#fff3b0,stroke:#7a6a00,color:#333
    classDef kilde fill:#eee,stroke:#666,color:#222
    classDef nedlagt fill:#fff,stroke:#999,color:#999,stroke-dasharray:4 3
    min_miljoe_og_ligestilling["Miljø- og Ligestillingsministeriet (2024-3/6/2026) (omdøbt)"]:::nedlagt
    eu_dir_1991_271["Byspildevandsdirektivet – Rådets direktiv 91/271/EØF af 21. maj 1991"]:::eu
    eu_dir_2010_75["Direktiv 2010/75/EU om industrielle emissioner (IED)"]:::eu
    eu_dir_2020_2184["Drikkevandsdirektivet – direktiv (EU) 2020/2184 af 16. december 2020 (omarbejdning)"]:::eu
    eu_dir_2018_2001["Europa-Parlamentets og Rådets direktiv (EU) 2018/2001 af 11. december 2018 om fremme af anvendelsen af energi fra vedvarende energikilder (omarbejdning) (RED II), som ændret ved direktiv (EU) 2023/2413"]:::eu
    eu_reg_2006_1907["Forordning (EF) nr. 1907/2006 (REACH)"]:::eu
    eu_dir_2012_18["Seveso III-direktivet (direktiv 2012/18/EU om kontrol med risikoen for større uheld med farlige stoffer)"]:::eu
    kommune_alle["Kommunerne (98 kommunalbestyrelser)"]:::instans
    sty_kystdirektoratet["Kystdirektoratet"]:::instans
    sty_miljoestyrelsen["Miljøstyrelsen"]:::instans
    kilde_dma["Digital MiljøAdministration (DMA, dma.mst.dk)"]:::kilde
    kilde_kgl_res_2026_06_03["Kongelig resolution af 3. juni 2026 (ressortændringer ved dannelsen af S-SF-M-RV-regeringen)"]:::kilde
    kilde_mst_dk["mst.dk (Miljøstyrelsens hjemmeside)"]:::kilde
    ombud_folketingets_ombudsmand["Folketingets Ombudsmand"]:::klage
    naevn_miljoe_og_foedevareklagenaevnet["Miljø- og Fødevareklagenævnet"]:::klage
    min_miljoe["Miljøministeriet"]:::ministerium
    bek_olietanke["Bekendtgørelse om indretning, etablering og drift af olietanke, rørsystemer og pipelines (olietankbekendtgørelsen)"]:::retsakt
    bek_spildevand["Bekendtgørelse om spildevandsplanen og spildevandstilladelser m.v. efter miljøbeskyttelseslovens kapitel 3 og 4 (spildevandsbekendtgørelsen)"]:::retsakt
    bek_vandindvinding["Bekendtgørelse om vandindvinding og vandforsyning (BEK nr. 867 af 20/06/2025)"]:::retsakt
    vejl_habitatvejledning["Habitatvejledningen (VEJ nr. 10226 af 2019)"]:::retsakt
    lov_kemikalieloven["Lov om kemikalier (kemikalieloven)"]:::retsakt
    lov_kystbeskyttelsesloven["Lov om kystbeskyttelse (kystbeskyttelsesloven)"]:::retsakt
    lov_miljoebeskyttelsesloven["Lov om miljøbeskyttelse (miljøbeskyttelsesloven)"]:::retsakt
    lov_miljoevurderingsloven["Lov om miljøvurderinger (miljøvurderingsloven, VVM/SMV)"]:::retsakt
    lov_naturbeskyttelsesloven["Lov om naturbeskyttelse (naturbeskyttelsesloven)"]:::retsakt
    vejl_mst_vejledninger["Miljøstyrelsens vejledninger (samling: godkendelse, tilsyn, støj, midlertidige aktiviteter, jord m.m.)"]:::retsakt
    bek_risiko["Risikobekendtgørelsen (bekendtgørelse om kontrol med risikoen for større uheld med farlige stoffer)"]:::retsakt
    plan_spildevandsplan["Spildevandsplan (inkl. tillæg)"]:::retsakt
    vejl_miljoeoplysningsloven["Vejledning om aktindsigt i miljøoplysninger (VEJ nr. 10564 af 2006)"]:::retsakt
    vejl_naturbeskyttelse_vejledninger["Vejledninger efter naturbeskyttelsesloven (§ 3-natur, byggelinjer, fredning m.v.)"]:::retsakt
    min_miljoe -.->|delegation| sty_kystdirektoratet
    min_miljoe -.->|delegation| sty_miljoestyrelsen
    kilde_kgl_res_2026_06_03 -->|henviser_til| min_miljoe_og_ligestilling
    lov_kemikalieloven -->|hjemmel_for| sty_miljoestyrelsen
    lov_kystbeskyttelsesloven -->|hjemmel_for| sty_kystdirektoratet
    lov_miljoebeskyttelsesloven -->|hjemmel_for| sty_miljoestyrelsen
    lov_miljoevurderingsloven -.->|hjemmel_for| sty_miljoestyrelsen
    lov_naturbeskyttelsesloven -->|hjemmel_for| sty_kystdirektoratet
    lov_naturbeskyttelsesloven -->|hjemmel_for| sty_miljoestyrelsen
    naevn_miljoe_og_foedevareklagenaevnet -->|klageinstans| sty_kystdirektoratet
    naevn_miljoe_og_foedevareklagenaevnet -->|klageinstans| sty_miljoestyrelsen
    min_miljoe_og_ligestilling -->|ressortansvar| sty_kystdirektoratet
    min_miljoe_og_ligestilling -->|ressortansvar| sty_miljoestyrelsen
    ombud_folketingets_ombudsmand -->|tilsyn| sty_miljoestyrelsen
    sty_kystdirektoratet -.->|tilsyn| kommune_alle
    sty_miljoestyrelsen -->|tilsyn| eu_reg_2006_1907
    sty_miljoestyrelsen -.->|tilsyn| kommune_alle
    min_miljoe_og_ligestilling -->|udsteder| bek_vandindvinding
    sty_miljoestyrelsen -.->|udsteder| bek_olietanke
    sty_miljoestyrelsen -->|udsteder| bek_risiko
    sty_miljoestyrelsen -.->|udsteder| bek_spildevand
    sty_miljoestyrelsen -->|udsteder| kilde_dma
    sty_miljoestyrelsen -->|udsteder| kilde_mst_dk
    sty_miljoestyrelsen -->|udsteder| vejl_habitatvejledning
    sty_miljoestyrelsen -->|udsteder| vejl_miljoeoplysningsloven
    sty_miljoestyrelsen -->|udsteder| vejl_mst_vejledninger
    sty_miljoestyrelsen -->|udsteder| vejl_naturbeskyttelse_vejledninger
    min_miljoe -->|klageinstans| sty_miljoestyrelsen
    bek_spildevand -->|hjemmel_for| plan_spildevandsplan
    bek_risiko -->|implementerer_EU| eu_dir_2012_18
    bek_spildevand -->|implementerer_EU| eu_dir_1991_271
    bek_vandindvinding -->|implementerer_EU| eu_dir_2020_2184
    bek_spildevand -->|implementerer_EU| eu_dir_2010_75
    bek_spildevand -->|implementerer_EU| eu_dir_2018_2001
```

[← Overblik](oversigt.md)
