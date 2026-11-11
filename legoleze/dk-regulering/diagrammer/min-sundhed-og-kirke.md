# Sundheds- og Kirkeministeriet

> Genereret af `scripts/build.py` fra `registry.yaml` (dato 2026-10-28). Redigér ikke i hånden.
> Fuldt optrukne pile = `verificeret`; stiplede = `sandsynlig`/`ukendt`. Grå stiplede bokse = nedlagt/omdøbt/ophævet.

Noder: 36 · kanter: 71

```mermaid
flowchart LR
    classDef ministerium fill:#1f3a5f,stroke:#0d1b2a,color:#fff
    classDef instans fill:#d7e3f4,stroke:#1f3a5f,color:#0d1b2a
    classDef klage fill:#f6dcc2,stroke:#8a4b08,color:#3b1f00
    classDef retsakt fill:#e6f2e6,stroke:#2e6b2e,color:#103010
    classDef eu fill:#fff3b0,stroke:#7a6a00,color:#333
    classDef kilde fill:#eee,stroke:#666,color:#222
    classDef nedlagt fill:#fff,stroke:#999,color:#999,stroke-dasharray:4 3
    min_sundhed_og_kirke["Sundheds- og Kirkeministeriet"]:::ministerium
    kommune_alle["Kommunerne (98 kommunalbestyrelser)"]:::instans
    raad_laegemiddelnaevnet["Lægemiddelnævnet"]:::instans
    sty_laegemiddelstyrelsen["Lægemiddelstyrelsen"]:::instans
    region_alle["Regionerne (5 regionsråd)"]:::instans
    sty_statens_serum_institut["Statens Serum Institut"]:::instans
    sty_styrelsen_for_patientklager["Styrelsen for Patientklager"]:::instans
    sty_styrelsen_for_patientsikkerhed["Styrelsen for Patientsikkerhed"]:::instans
    sty_sundhedsdatastyrelsen["Sundhedsdatastyrelsen"]:::instans
    sty_sundhedsstyrelsen["Sundhedsstyrelsen"]:::instans
    kilde_stpk_klageafgoerelser["Afgørelser fra Styrelsen for Patientklager (stpk.dk)"]:::kilde
    kilde_stpk_disciplinaernaevn_afgoerelser["Afgørelser fra Sundhedsvæsenets Disciplinærnævn (stpk.dk)"]:::kilde
    kilde_stpk_erstatningsdomme["Domme fra erstatningsområdet (stpk.dk)"]:::kilde
    org_patienterstatningen["Patienterstatningen"]:::kilde
    kilde_stpk_publikationer["Publikationer, årsrapporter og praksissammenfatninger (stpk.dk)"]:::kilde
    kilde_stps_tilsynsrapporter["Tilsynsrapporter (Styrelsen for Patientsikkerhed)"]:::kilde
    naevn_ankenaevnet_for_patienterstatningen["Ankenævnet for Patienterstatningen"]:::klage
    naevn_ankenaevnet_for_tilsynsafgoerelser["Ankenævnet for Tilsynsafgørelser"]:::klage
    naevn_det_psykiatriske_ankenaevn["Det Psykiatriske Ankenævn"]:::klage
    naevn_det_psykiatriske_patientklagenaevn["Det Psykiatriske Patientklagenævn"]:::klage
    naevn_sundhedsvaesenets_disciplinaernaevn["Sundhedsvæsenets Disciplinærnævn"]:::klage
    naevn_tvangsbehandlingsnaevnet["Tvangsbehandlingsnævnet"]:::klage
    bek_patientklager_screening_af_klager["Bekendtgørelse om Styrelsen for Patientklagers screening af klager og videregivelse af sagsakter til Styrelsen for Patientsikkerhed"]:::retsakt
    bek_forretningsorden_ankenaevnet_for_patienterstatningen["Bekendtgørelse om forretningsorden for Ankenævnet for Patienterstatningen"]:::retsakt
    bek_forretningsorden_psykiatriske_ankenaevn["Bekendtgørelse om forretningsorden for Det Psykiatriske Ankenævn"]:::retsakt
    bek_forretningsorden_psykiatriske_patientklagenaevn["Bekendtgørelse om forretningsorden for Det Psykiatriske Patientklagenævn"]:::retsakt
    bek_forretningsorden_laegemiddelnaevnet["Bekendtgørelse om forretningsorden for Lægemiddelnævnet"]:::retsakt
    bek_forretningsorden_disciplinaernaevn["Bekendtgørelse om forretningsorden for Sundhedsvæsenets Disciplinærnævn"]:::retsakt
    bek_forretningsorden_tvangsbehandlingsnaevnet["Bekendtgørelse om forretningsorden for Tvangsbehandlingsnævnet"]:::retsakt
    bek_ikke_autoriserede_persongrupper_disciplinaernaevn["Bekendtgørelse om ikke-autoriserede persongrupper, der er omfattet af Sundhedsvæsenets Disciplinærnævns virksomhed"]:::retsakt
    bek_vedtaegter_patienterstatningen["Bekendtgørelse om vedtægter for Patienterstatningen"]:::retsakt
    lov_psykiatriloven["Lov om anvendelse af tvang i psykiatrien m.v. (psykiatriloven)"]:::retsakt
    lov_autorisation_sundhedspersoner["Lov om autorisation af sundhedspersoner og om sundhedsfaglig virksomhed (autorisationsloven)"]:::retsakt
    lov_klage_og_erstatningsloven["Lov om klage- og erstatningsadgang inden for sundhedsvæsenet"]:::retsakt
    lov_laegemiddelloven["Lov om lægemidler (lægemiddelloven)"]:::retsakt
    lov_sundhedsloven["Sundhedsloven"]:::retsakt
    min_sundhed_og_kirke -.->|ressortansvar| sty_sundhedsstyrelsen
    min_sundhed_og_kirke -.->|ressortansvar| sty_styrelsen_for_patientsikkerhed
    min_sundhed_og_kirke -.->|ressortansvar| sty_styrelsen_for_patientklager
    min_sundhed_og_kirke -.->|ressortansvar| sty_laegemiddelstyrelsen
    min_sundhed_og_kirke -.->|ressortansvar| sty_sundhedsdatastyrelsen
    min_sundhed_og_kirke -->|ressortansvar| sty_statens_serum_institut
    min_sundhed_og_kirke -.->|ressortansvar| naevn_sundhedsvaesenets_disciplinaernaevn
    lov_klage_og_erstatningsloven -->|hjemmel_for| naevn_sundhedsvaesenets_disciplinaernaevn
    min_sundhed_og_kirke -.->|ressortansvar| naevn_ankenaevnet_for_patienterstatningen
    lov_klage_og_erstatningsloven -->|hjemmel_for| naevn_ankenaevnet_for_patienterstatningen
    min_sundhed_og_kirke -.->|ressortansvar| naevn_tvangsbehandlingsnaevnet
    lov_klage_og_erstatningsloven -->|hjemmel_for| naevn_tvangsbehandlingsnaevnet
    min_sundhed_og_kirke -.->|ressortansvar| naevn_ankenaevnet_for_tilsynsafgoerelser
    lov_klage_og_erstatningsloven -->|hjemmel_for| naevn_ankenaevnet_for_tilsynsafgoerelser
    lov_klage_og_erstatningsloven -->|hjemmel_for| org_patienterstatningen
    min_sundhed_og_kirke -.->|ressortansvar| naevn_det_psykiatriske_ankenaevn
    min_sundhed_og_kirke -.->|ressortansvar| naevn_det_psykiatriske_patientklagenaevn
    min_sundhed_og_kirke -->|ressortansvar| raad_laegemiddelnaevnet
    min_sundhed_og_kirke -.->|ressortansvar| org_patienterstatningen
    min_sundhed_og_kirke -.->|ressortansvar| lov_sundhedsloven
    min_sundhed_og_kirke -.->|ressortansvar| lov_autorisation_sundhedspersoner
    min_sundhed_og_kirke -.->|ressortansvar| lov_klage_og_erstatningsloven
    min_sundhed_og_kirke -->|ressortansvar| lov_laegemiddelloven
    min_sundhed_og_kirke -.->|ressortansvar| lov_psykiatriloven
    lov_sundhedsloven -->|hjemmel_for| sty_sundhedsstyrelsen
    lov_sundhedsloven -->|hjemmel_for| sty_styrelsen_for_patientsikkerhed
    lov_autorisation_sundhedspersoner -->|hjemmel_for| sty_styrelsen_for_patientsikkerhed
    lov_klage_og_erstatningsloven -.->|hjemmel_for| sty_styrelsen_for_patientklager
    lov_psykiatriloven -->|hjemmel_for| naevn_det_psykiatriske_patientklagenaevn
    lov_psykiatriloven -->|hjemmel_for| naevn_det_psykiatriske_ankenaevn
    lov_laegemiddelloven -->|hjemmel_for| raad_laegemiddelnaevnet
    lov_klage_og_erstatningsloven -->|hjemmel_for| bek_forretningsorden_disciplinaernaevn
    bek_forretningsorden_disciplinaernaevn -.->|hjemmel_for| naevn_sundhedsvaesenets_disciplinaernaevn
    min_sundhed_og_kirke -.->|ressortansvar| bek_forretningsorden_disciplinaernaevn
    lov_klage_og_erstatningsloven -->|hjemmel_for| bek_forretningsorden_ankenaevnet_for_patienterstatningen
    bek_forretningsorden_ankenaevnet_for_patienterstatningen -.->|hjemmel_for| naevn_ankenaevnet_for_patienterstatningen
    min_sundhed_og_kirke -.->|ressortansvar| bek_forretningsorden_ankenaevnet_for_patienterstatningen
    lov_klage_og_erstatningsloven -->|hjemmel_for| bek_forretningsorden_tvangsbehandlingsnaevnet
    bek_forretningsorden_tvangsbehandlingsnaevnet -.->|hjemmel_for| naevn_tvangsbehandlingsnaevnet
    min_sundhed_og_kirke -.->|ressortansvar| bek_forretningsorden_tvangsbehandlingsnaevnet
    lov_psykiatriloven -->|hjemmel_for| bek_forretningsorden_psykiatriske_patientklagenaevn
    bek_forretningsorden_psykiatriske_patientklagenaevn -.->|hjemmel_for| naevn_det_psykiatriske_patientklagenaevn
    min_sundhed_og_kirke -.->|ressortansvar| bek_forretningsorden_psykiatriske_patientklagenaevn
    lov_psykiatriloven -->|hjemmel_for| bek_forretningsorden_psykiatriske_ankenaevn
    bek_forretningsorden_psykiatriske_ankenaevn -.->|hjemmel_for| naevn_det_psykiatriske_ankenaevn
    min_sundhed_og_kirke -.->|ressortansvar| bek_forretningsorden_psykiatriske_ankenaevn
    lov_klage_og_erstatningsloven -->|hjemmel_for| bek_vedtaegter_patienterstatningen
    bek_vedtaegter_patienterstatningen -.->|hjemmel_for| org_patienterstatningen
    min_sundhed_og_kirke -.->|ressortansvar| bek_vedtaegter_patienterstatningen
    lov_laegemiddelloven -->|hjemmel_for| bek_forretningsorden_laegemiddelnaevnet
    bek_forretningsorden_laegemiddelnaevnet -.->|hjemmel_for| raad_laegemiddelnaevnet
    min_sundhed_og_kirke -.->|ressortansvar| bek_forretningsorden_laegemiddelnaevnet
    lov_klage_og_erstatningsloven -->|hjemmel_for| bek_patientklager_screening_af_klager
    bek_patientklager_screening_af_klager -.->|hjemmel_for| sty_styrelsen_for_patientklager
    min_sundhed_og_kirke -.->|ressortansvar| bek_patientklager_screening_af_klager
    lov_klage_og_erstatningsloven -->|hjemmel_for| bek_ikke_autoriserede_persongrupper_disciplinaernaevn
    bek_ikke_autoriserede_persongrupper_disciplinaernaevn -.->|hjemmel_for| naevn_sundhedsvaesenets_disciplinaernaevn
    min_sundhed_og_kirke -.->|ressortansvar| bek_ikke_autoriserede_persongrupper_disciplinaernaevn
    naevn_ankenaevnet_for_patienterstatningen -.->|klageinstans| org_patienterstatningen
    naevn_ankenaevnet_for_tilsynsafgoerelser -->|klageinstans| sty_styrelsen_for_patientsikkerhed
    sty_styrelsen_for_patientklager -.->|klageinstans| kommune_alle
    sty_styrelsen_for_patientklager -.->|klageinstans| region_alle
    sty_styrelsen_for_patientklager -->|klageinstans| sty_sundhedsstyrelsen
    naevn_det_psykiatriske_ankenaevn -->|klageinstans| naevn_det_psykiatriske_patientklagenaevn
    sty_styrelsen_for_patientklager -.->|udsteder| kilde_stpk_klageafgoerelser
    naevn_sundhedsvaesenets_disciplinaernaevn -.->|udsteder| kilde_stpk_disciplinaernaevn_afgoerelser
    naevn_ankenaevnet_for_patienterstatningen -.->|udsteder| kilde_stpk_erstatningsdomme
    sty_styrelsen_for_patientklager -.->|udsteder| kilde_stpk_publikationer
    sty_styrelsen_for_patientsikkerhed -.->|udsteder| kilde_stps_tilsynsrapporter
    sty_styrelsen_for_patientsikkerhed -.->|tilsyn| region_alle
    sty_styrelsen_for_patientsikkerhed -.->|tilsyn| kommune_alle
```

[← Overblik](oversigt.md)
