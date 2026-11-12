# Ministeriet for Samfundssikkerhed og Beredskab

> Genereret af `scripts/build.py` fra `registry.yaml` (dato 2026-10-28). Redigér ikke i hånden.
> Fuldt optrukne pile = `verificeret`; stiplede = `sandsynlig`/`ukendt`. Grå stiplede bokse = nedlagt/omdøbt/ophævet.

Noder: 41 · kanter: 77

```mermaid
flowchart LR
    classDef ministerium fill:#1f3a5f,stroke:#0d1b2a,color:#fff
    classDef instans fill:#d7e3f4,stroke:#1f3a5f,color:#0d1b2a
    classDef klage fill:#f6dcc2,stroke:#8a4b08,color:#3b1f00
    classDef retsakt fill:#e6f2e6,stroke:#2e6b2e,color:#103010
    classDef eu fill:#fff3b0,stroke:#7a6a00,color:#333
    classDef kilde fill:#eee,stroke:#666,color:#222
    classDef nedlagt fill:#fff,stroke:#999,color:#999,stroke-dasharray:4 3
    min_samfundssikkerhed_og_beredskab["Ministeriet for Samfundssikkerhed og Beredskab"]:::ministerium
    eu_dir_1999_92["Direktiv 1999/92/EF om minimumsforskrifter for sikkerhed og sundhed for arbejdstagere, som kan udsættes for risiko for eksplosiv atmosfære (ATEX-brugerdirektivet)"]:::eu
    eu_dir_2022_2555["Europa-Parlamentets og Rådets direktiv (EU) 2022/2555 (NIS 2-direktivet)"]:::eu
    eu_dir_2012_18["Seveso III-direktivet (direktiv 2012/18/EU om kontrol med risikoen for større uheld med farlige stoffer)"]:::eu
    sty_beredskabsstyrelsen["Beredskabsstyrelsen"]:::instans
    kommune_redningsberedskaber["Fælleskommunale redningsberedskaber (§ 60-fællesskaber med fælles beredskabskommission)"]:::instans
    kommune_alle["Kommunerne (98 kommunalbestyrelser)"]:::instans
    sty_styrelsen_for_samfundssikkerhed["Styrelsen for Samfundssikkerhed"]:::instans
    sty_soefartsstyrelsen["Søfartsstyrelsen"]:::instans
    kilde_brs_dk["brs.dk (Beredskabsstyrelsen)"]:::kilde
    naevn_ankenaevnet_for_soefartsforhold["Ankenævnet for Søfartsforhold"]:::klage
    dom_domstolene["Domstolene (byret, landsret, Højesteret)"]:::klage
    ombud_folketingets_ombudsmand["Folketingets Ombudsmand"]:::klage
    bek_driftsmaessige_forskrifter["Driftsmæssige forskrifter for hoteller m.v., plejeinstitutioner, forsamlingslokaler, undervisningslokaler, daginstitutioner og butikker (BEK nr. 212 af 27/03/2008), ophævet 1/1/2022 (ophævet)"]:::nedlagt
    sty_styrelsen_for_forsyningssikkerhed["Styrelsen for Forsyningssikkerhed (nedlagt)"]:::nedlagt
    tf_brandfarlig_virksomhed_og_oplag["Tekniske forskrifter for visse brandfarlige virksomheder og oplag (TF-visse, 1990) (ophævet)"]:::nedlagt
    bek_eksplosiv_atmosfaere["Bekendtgørelse om arbejde i forbindelse med eksplosiv atmosfære"]:::retsakt
    tf_brandfarlige_vaesker["Bekendtgørelse om brandfarlige og brændbare væsker (BEK nr. 1639 af 06/12/2016), tidligere 'tekniske forskrifter for brandfarlige væsker'"]:::retsakt
    bek_br18["Bekendtgørelse om bygningsreglement 2018 (BR18)"]:::retsakt
    bek_brs_henlaeggelse["Bekendtgørelse om henlæggelse af beføjelsen til at fastsætte regler til Beredskabsstyrelsen og om klageadgang (BEK nr. 1913 af 2015)"]:::retsakt
    bek_soefartsstyrelsen_henlaeggelse["Bekendtgørelse om henlæggelse af visse beføjelser til Søfartsstyrelsen og om klageadgang m.v. (BEK nr. 261 af 23/03/2020)"]:::retsakt
    bek_eksplosionsfarlige_omraader["Bekendtgørelse om klassifikation af eksplosionsfarlige områder (BEK nr. 590 af 26/06/2003)"]:::retsakt
    bek_brs_ophaevelse_2021["Bekendtgørelse om ophævelse af visse bekendtgørelser på Beredskabsstyrelsens område (BEK nr 2340 af 2021)"]:::retsakt
    bek_risikobaseret_dimensionering["Bekendtgørelse om risikobaseret dimensionering og planer for det kommunale redningsberedskab (dimensioneringsbekendtgørelsen)"]:::retsakt
    tf_braendbare_faste_stoffer["Bekendtgørelse om tekniske forskrifter for brændbare faste stoffer (BEK nr. 1070 af 29/06/2020)"]:::retsakt
    tf_gasser["Bekendtgørelse om tekniske forskrifter for gasser (BEK nr. 1444 af 15/12/2010), herunder F-gas (flaskegas)"]:::retsakt
    bek_campingreglement["Bekendtgørelse om tilladelse til udlejning af arealer til campering og om indretning og benyttelse af campingpladser (campingreglementet) (BEK nr. 319 af 28/03/2019)"]:::retsakt
    lov_beredskabsloven["Beredskabsloven"]:::retsakt
    vejl_brs_vejledninger["Beredskabsstyrelsens vejledninger og meddelelser (bl.a. om brandsyn, tekniske forskrifter, eksplosionsfarlige områder og risikobaseret dimensionering)"]:::retsakt
    bek_brandsyn["Brandsynsbekendtgørelsen (bekendtgørelse om brandsyn), BEK nr. 2341 af 09/12/2021"]:::retsakt
    lov_byggeloven["Byggeloven (lov om byggeri)"]:::retsakt
    lov_lodsloven["Lodsloven (Bekendtgørelse af lodslov)"]:::retsakt
    lov_dis_loven["Lov om Dansk Internationalt Skibsregister (DIS-loven)"]:::retsakt
    lov_nis2["Lov om foranstaltninger til sikring af et højt cybersikkerhedsniveau (NIS 2-loven)"]:::retsakt
    lov_telesektoren_sikkerhed["Lov om sikkerhed og beredskab i telesektoren"]:::retsakt
    lov_sikkerhed_til_soes["Lov om sikkerhed til søs"]:::retsakt
    lov_skibes_besaetning["Lov om skibes besætning"]:::retsakt
    lov_soefarendes_ansaettelsesforhold["Lov om søfarendes ansættelsesforhold m.v."]:::retsakt
    plan_risikobaseret_dimensionering["Plan for risikobaseret dimensionering af det kommunale redningsberedskab"]:::retsakt
    bek_risiko["Risikobekendtgørelsen (bekendtgørelse om kontrol med risikoen for større uheld med farlige stoffer)"]:::retsakt
    lov_soeloven["Søloven"]:::retsakt
    min_samfundssikkerhed_og_beredskab -->|delegation| sty_beredskabsstyrelsen
    bek_br18 -.->|henviser_til| lov_beredskabsloven
    bek_brandsyn -->|henviser_til| bek_br18
    bek_brandsyn -.->|henviser_til| lov_byggeloven
    bek_brs_ophaevelse_2021 -->|henviser_til| bek_driftsmaessige_forskrifter
    bek_eksplosionsfarlige_omraader -->|henviser_til| bek_eksplosiv_atmosfaere
    bek_risiko -.->|henviser_til| lov_beredskabsloven
    vejl_brs_vejledninger -->|henviser_til| bek_brandsyn
    vejl_brs_vejledninger -.->|henviser_til| bek_driftsmaessige_forskrifter
    vejl_brs_vejledninger -->|henviser_til| bek_eksplosionsfarlige_omraader
    vejl_brs_vejledninger -->|henviser_til| bek_risikobaseret_dimensionering
    vejl_brs_vejledninger -->|henviser_til| tf_brandfarlige_vaesker
    vejl_brs_vejledninger -->|henviser_til| tf_gasser
    bek_brandsyn -->|hjemmel_for| kommune_alle
    bek_brs_henlaeggelse -.->|hjemmel_for| sty_beredskabsstyrelsen
    bek_risikobaseret_dimensionering -->|hjemmel_for| plan_risikobaseret_dimensionering
    lov_beredskabsloven -->|hjemmel_for| bek_brandsyn
    lov_beredskabsloven -->|hjemmel_for| bek_brs_henlaeggelse
    lov_beredskabsloven -.->|hjemmel_for| bek_brs_ophaevelse_2021
    lov_beredskabsloven -.->|hjemmel_for| bek_driftsmaessige_forskrifter
    lov_beredskabsloven -->|hjemmel_for| bek_eksplosionsfarlige_omraader
    lov_beredskabsloven -->|hjemmel_for| bek_risiko
    lov_beredskabsloven -->|hjemmel_for| bek_risikobaseret_dimensionering
    lov_beredskabsloven -->|hjemmel_for| kommune_alle
    lov_beredskabsloven -->|hjemmel_for| kommune_redningsberedskaber
    lov_beredskabsloven -->|hjemmel_for| sty_beredskabsstyrelsen
    lov_beredskabsloven -->|hjemmel_for| tf_braendbare_faste_stoffer
    lov_beredskabsloven -.->|hjemmel_for| tf_brandfarlig_virksomhed_og_oplag
    lov_beredskabsloven -->|hjemmel_for| tf_brandfarlige_vaesker
    lov_beredskabsloven -->|hjemmel_for| tf_gasser
    bek_eksplosionsfarlige_omraader -->|implementerer_EU| eu_dir_1999_92
    dom_domstolene -.->|klageinstans| sty_beredskabsstyrelsen
    min_samfundssikkerhed_og_beredskab -->|ressortansvar| bek_brandsyn
    min_samfundssikkerhed_og_beredskab -.->|ressortansvar| bek_brs_henlaeggelse
    min_samfundssikkerhed_og_beredskab -.->|ressortansvar| bek_eksplosionsfarlige_omraader
    min_samfundssikkerhed_og_beredskab -.->|ressortansvar| bek_risikobaseret_dimensionering
    min_samfundssikkerhed_og_beredskab -->|ressortansvar| lov_beredskabsloven
    min_samfundssikkerhed_og_beredskab -->|ressortansvar| sty_beredskabsstyrelsen
    min_samfundssikkerhed_og_beredskab -->|ressortansvar| sty_styrelsen_for_forsyningssikkerhed
    min_samfundssikkerhed_og_beredskab -->|ressortansvar| sty_styrelsen_for_samfundssikkerhed
    min_samfundssikkerhed_og_beredskab -->|ressortansvar| tf_braendbare_faste_stoffer
    min_samfundssikkerhed_og_beredskab -.->|ressortansvar| tf_brandfarlig_virksomhed_og_oplag
    min_samfundssikkerhed_og_beredskab -.->|ressortansvar| tf_brandfarlige_vaesker
    min_samfundssikkerhed_og_beredskab -->|ressortansvar| tf_gasser
    min_samfundssikkerhed_og_beredskab -->|tilsyn| kommune_alle
    min_samfundssikkerhed_og_beredskab -->|tilsyn| kommune_redningsberedskaber
    ombud_folketingets_ombudsmand -.->|tilsyn| sty_beredskabsstyrelsen
    sty_beredskabsstyrelsen -->|tilsyn| kommune_alle
    sty_beredskabsstyrelsen -->|tilsyn| kommune_redningsberedskaber
    kommune_alle -->|udsteder| plan_risikobaseret_dimensionering
    min_samfundssikkerhed_og_beredskab -.->|udsteder| bek_risikobaseret_dimensionering
    sty_beredskabsstyrelsen -->|udsteder| bek_brandsyn
    sty_beredskabsstyrelsen -->|udsteder| bek_brs_ophaevelse_2021
    sty_beredskabsstyrelsen -->|udsteder| bek_driftsmaessige_forskrifter
    sty_beredskabsstyrelsen -->|udsteder| kilde_brs_dk
    sty_beredskabsstyrelsen -->|udsteder| tf_braendbare_faste_stoffer
    sty_beredskabsstyrelsen -->|udsteder| tf_brandfarlige_vaesker
    sty_beredskabsstyrelsen -->|udsteder| tf_gasser
    sty_beredskabsstyrelsen -->|udsteder| vejl_brs_vejledninger
    min_samfundssikkerhed_og_beredskab -->|ressortansvar| lov_lodsloven
    min_samfundssikkerhed_og_beredskab -.->|ressortansvar| bek_soefartsstyrelsen_henlaeggelse
    lov_lodsloven -->|hjemmel_for| sty_soefartsstyrelsen
    lov_sikkerhed_til_soes -->|hjemmel_for| bek_soefartsstyrelsen_henlaeggelse
    bek_soefartsstyrelsen_henlaeggelse -.->|hjemmel_for| naevn_ankenaevnet_for_soefartsforhold
    lov_beredskabsloven -->|hjemmel_for| bek_campingreglement
    lov_dis_loven -->|hjemmel_for| bek_soefartsstyrelsen_henlaeggelse
    lov_lodsloven -->|hjemmel_for| bek_soefartsstyrelsen_henlaeggelse
    lov_soefarendes_ansaettelsesforhold -->|hjemmel_for| bek_soefartsstyrelsen_henlaeggelse
    lov_soeloven -->|hjemmel_for| bek_soefartsstyrelsen_henlaeggelse
    lov_skibes_besaetning -->|hjemmel_for| bek_soefartsstyrelsen_henlaeggelse
    min_samfundssikkerhed_og_beredskab -->|ressortansvar| lov_nis2
    min_samfundssikkerhed_og_beredskab -->|ressortansvar| lov_telesektoren_sikkerhed
    sty_styrelsen_for_samfundssikkerhed -->|tilsyn| kommune_alle
    lov_nis2 -->|implementerer_EU| eu_dir_2022_2555
    lov_telesektoren_sikkerhed -.->|hjemmel_for| sty_styrelsen_for_samfundssikkerhed
    lov_telesektoren_sikkerhed -->|implementerer_EU| eu_dir_2022_2555
    bek_risiko -->|implementerer_EU| eu_dir_2012_18
```

[← Overblik](oversigt.md)
