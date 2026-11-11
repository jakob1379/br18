# Overblik: ministerium → instans

> Genereret af `scripts/build.py` fra `registry.yaml` (dato 2026-10-28). Redigér ikke i hånden.
> Fuldt optrukne pile = `verificeret`; stiplede = `sandsynlig`/`ukendt`. Grå stiplede bokse = nedlagt/omdøbt/ophævet.

```mermaid
flowchart LR
    classDef ministerium fill:#1f3a5f,stroke:#0d1b2a,color:#fff
    classDef instans fill:#d7e3f4,stroke:#1f3a5f,color:#0d1b2a
    classDef klage fill:#f6dcc2,stroke:#8a4b08,color:#3b1f00
    classDef retsakt fill:#e6f2e6,stroke:#2e6b2e,color:#103010
    classDef eu fill:#fff3b0,stroke:#7a6a00,color:#333
    classDef kilde fill:#eee,stroke:#666,color:#222
    classDef nedlagt fill:#fff,stroke:#999,color:#999,stroke-dasharray:4 3
    min_beskaeftigelse_og_ligestilling["Beskæftigelses- og Ligestillingsministeriet"]:::ministerium
    min_by_land_og_kirke["By-, Land- og Kirkeministeriet (nedlagt)"]:::nedlagt
    min_by_land_og_transport["By-, Land- og Transportministeriet"]:::ministerium
    min_boern_aeldre_og_bolig["Børne-, Ældre- og Boligministeriet"]:::ministerium
    min_erhverv["Erhvervsministeriet"]:::ministerium
    min_forsvar["Forsvarsministeriet"]:::ministerium
    min_indenrigs_og_bolig["Indenrigs- og Boligministeriet (nedlagt)"]:::nedlagt
    min_justits["Justitsministeriet"]:::ministerium
    min_klima_energi_og_forsyning["Klima-, Energi- og Forsyningsministeriet"]:::ministerium
    min_kultur["Kulturministeriet"]:::ministerium
    min_miljoe_og_ligestilling["Miljø- og Ligestillingsministeriet (2024-3/6/2026) (omdøbt)"]:::nedlagt
    min_miljoe["Miljøministeriet"]:::ministerium
    min_groen_trepart["Ministeriet for Grøn Trepart (29/8/2024-3/6/2026) (omdøbt)"]:::nedlagt
    min_natur_og_dyrevelfaerd["Ministeriet for Natur og Dyrevelfærd"]:::ministerium
    min_samfundssikkerhed_og_beredskab["Ministeriet for Samfundssikkerhed og Beredskab"]:::ministerium
    min_skat_og_vaekst["Skatte- og Vækstministeriet"]:::ministerium
    min_social["Socialministeriet"]:::ministerium
    min_sundhed_og_kirke["Sundheds- og Kirkeministeriet"]:::ministerium
    min_udlaendinge_og_integration["Udlændinge- og Integrationsministeriet"]:::ministerium
    min_oekonomi_og_indenrigs["Økonomi- og Indenrigsministeriet"]:::ministerium
    sty_administrations_og_servicestyrelsen["Administrations- og Servicestyrelsen"]:::instans
    naevn_ankenaevnet_for_patienterstatningen["Ankenævnet for Patienterstatningen"]:::klage
    naevn_ankenaevnet_for_tilsynsafgoerelser["Ankenævnet for Tilsynsafgørelser"]:::klage
    sty_ankestyrelsen["Ankestyrelsen"]:::instans
    raad_arbejdsmarkedsraadet["Arbejdsmarkedsrådet"]:::instans
    naevn_arbejdsmiljoeklagenaevnet["Arbejdsmiljøklagenævnet"]:::klage
    raad_arbejdsmiljoeraadet["Arbejdsmiljørådet (nedlagt)"]:::nedlagt
    sty_arbejdstilsynet["Arbejdstilsynet"]:::instans
    naevn_beboerklagenaevn["Beboerklagenævn (kommunale)"]:::klage
    sty_beredskabsstyrelsen["Beredskabsstyrelsen"]:::instans
    sty_bolig_og_planstyrelsen["Bolig- og Planstyrelsen (nedlagt)"]:::nedlagt
    sty_by_og_landskabsstyrelsen["By- og Landskabsstyrelsen (nedlagt)"]:::nedlagt
    naevn_byggeklageenheden["Byggeklageenheden"]:::klage
    fond_byggeskadefonden["Byggeskadefonden"]:::instans
    fond_byggeskadefonden_bygningsfornyelse["Byggeskadefonden vedrørende Bygningsfornyelse (nedlagt)"]:::nedlagt
    sty_civilstyrelsen["Civilstyrelsen"]:::instans
    org_danmarks_miljoeportal["Danmarks Miljøportal"]:::instans
    org_nfa["Det Nationale Forskningscenter for Arbejdsmiljø (NFA)"]:::instans
    naevn_det_psykiatriske_ankenaevn["Det Psykiatriske Ankenævn"]:::klage
    naevn_det_psykiatriske_patientklagenaevn["Det Psykiatriske Patientklagenævn"]:::klage
    raad_det_systemiske_risikoraad["Det Systemiske Risikoråd"]:::instans
    raad_det_saerlige_bygningssyn["Det Særlige Bygningssyn"]:::instans
    sty_domstolsstyrelsen["Domstolsstyrelsen"]:::instans
    naevn_energiklagenaevnet["Energiklagenævnet"]:::klage
    org_energinet["Energinet"]:::instans
    sty_energistyrelsen["Energistyrelsen"]:::instans
    tilsyn_energitilsynet["Energitilsynet (nedlagt)"]:::nedlagt
    naevn_erhvervsankenaevnet["Erhvervsankenævnet"]:::klage
    sty_erhvervsstyrelsen["Erhvervsstyrelsen"]:::instans
    org_finansiel_stabilitet["Finansiel Stabilitet"]:::instans
    sty_finanstilsynet["Finanstilsynet"]:::instans
    naevn_flygtningenaevnet["Flygtningenævnet"]:::klage
    fond_blandede_byer["Fonden for blandede byer"]:::instans
    tilsyn_forsyningstilsynet["Forsyningstilsynet"]:::instans
    naevn_fredningsnaevn["Fredningsnævnene"]:::klage
    sty_faerdselsstyrelsen["Færdselsstyrelsen"]:::instans
    sty_geodatastyrelsen["Geodatastyrelsen"]:::instans
    fond_grundejernes_investeringsfond["Grundejernes Investeringsfond (GI)"]:::instans
    sty_gaeldsstyrelsen["Gældsstyrelsen"]:::instans
    sty_hjemrejsestyrelsen["Hjemrejsestyrelsen"]:::instans
    naevn_huslejenaevn["Huslejenævn (kommunale)"]:::klage
    naevn_klagenaevnet_for_udbud["Klagenævnet for Udbud"]:::klage
    sty_klimadatastyrelsen["Klimadatastyrelsen"]:::instans
    raad_klimaraadet["Klimarådet"]:::instans
    sty_konkurrence_og_forbrugerstyrelsen["Konkurrence- og Forbrugerstyrelsen"]:::instans
    naevn_konkurrenceankenaevnet["Konkurrenceankenævnet"]:::klage
    sty_kulturarvsstyrelsen["Kulturarvsstyrelsen (nedlagt)"]:::nedlagt
    sty_kulturstyrelsen["Kulturstyrelsen (nedlagt)"]:::nedlagt
    sty_kystdirektoratet["Kystdirektoratet"]:::instans
    sty_landbrugsstyrelsen["Landbrugsstyrelsen (nedlagt)"]:::nedlagt
    naevn_landinspektoernaevnet["Landinspektørnævnet"]:::klage
    fond_landsbyggefonden["Landsbyggefonden"]:::instans
    naevn_landsskatteretten["Landsskatteretten"]:::klage
    raad_laegemiddelnaevnet["Lægemiddelnævnet"]:::instans
    sty_laegemiddelstyrelsen["Lægemiddelstyrelsen"]:::instans
    naevn_miljoe_og_foedevareklagenaevnet["Miljø- og Fødevareklagenævnet"]:::klage
    sty_miljoestyrelsen["Miljøstyrelsen"]:::instans
    naevn_motorankenaevn["Motorankenævn"]:::klage
    sty_motorstyrelsen["Motorstyrelsen"]:::instans
    naevn_natur_og_miljoeklagenaevnet["Natur- og Miljøklagenævnet (nedlagt)"]:::nedlagt
    sty_naturstyrelsen["Naturstyrelsen"]:::instans
    sty_naevnenes_hus["Nævnenes Hus"]:::instans
    org_patienterstatningen["Patienterstatningen"]:::kilde
    sty_plan_og_landdistriktsstyrelsen["Plan- og Landdistriktsstyrelsen"]:::instans
    naevn_planklagenaevnet["Planklagenævnet"]:::klage
    sty_planstyrelsen["Planstyrelsen (nedlagt)"]:::nedlagt
    sty_rigsadvokaten["Rigsadvokaten"]:::instans
    raad_el_og_gasteknisk_sikkerhed["Rådet for El- og Gasteknisk Sikkerhed"]:::instans
    sty_sikkerhedsstyrelsen["Sikkerhedsstyrelsen (nedlagt)"]:::nedlagt
    naevn_skatteankenaevn["Skatteankenævn"]:::klage
    sty_skatteankestyrelsen["Skatteankestyrelsen"]:::instans
    sty_skatteforvaltningen["Skatteforvaltningen"]:::instans
    raad_skatteraadet["Skatterådet"]:::instans
    sty_skattestyrelsen["Skattestyrelsen"]:::instans
    sty_slots_og_kulturstyrelsen["Slots- og Kulturstyrelsen"]:::instans
    sty_social_og_boligstyrelsen["Social- og Boligstyrelsen"]:::instans
    sty_spillemyndigheden["Spillemyndigheden"]:::instans
    sty_statens_serum_institut["Statens Serum Institut"]:::instans
    org_statsforvaltningen["Statsforvaltningen (nedlagt)"]:::nedlagt
    sty_styrelsen_for_forsyningssikkerhed["Styrelsen for Forsyningssikkerhed (nedlagt)"]:::nedlagt
    sty_groen_arealomlaegning_og_vandmiljoe["Styrelsen for Grøn Arealomlægning og Vandmiljø (SGAV)"]:::instans
    sty_siri["Styrelsen for International Rekruttering og Integration (SIRI)"]:::instans
    sty_styrelsen_for_patientklager["Styrelsen for Patientklager"]:::instans
    sty_styrelsen_for_patientsikkerhed["Styrelsen for Patientsikkerhed"]:::instans
    sty_styrelsen_for_samfundssikkerhed["Styrelsen for Samfundssikkerhed"]:::instans
    sty_sundhedsdatastyrelsen["Sundhedsdatastyrelsen"]:::instans
    sty_sundhedsstyrelsen["Sundhedsstyrelsen"]:::instans
    naevn_sundhedsvaesenets_disciplinaernaevn["Sundhedsvæsenets Disciplinærnævn"]:::klage
    naevn_taksationskommissionen["Taksationskommissionen (naturbeskyttelsesloven)"]:::klage
    naevn_taksationsmyndighederne["Taksationskommissionerne og overtaksationskommissionerne (efter vejloven)"]:::klage
    tilsyn_it_tilsynet["Tilsynet med told- og skatteforvaltningens it-område (It-tilsynet)"]:::instans
    sty_toldstyrelsen["Toldstyrelsen"]:::instans
    sty_trafik_bygge_og_boligstyrelsen["Trafik-, Bygge- og Boligstyrelsen (omdøbt)"]:::nedlagt
    naevn_tvangsbehandlingsnaevnet["Tvangsbehandlingsnævnet"]:::klage
    org_udbetaling_danmark["Udbetaling Danmark"]:::instans
    naevn_udlaendingenaevnet["Udlændingenævnet"]:::klage
    sty_udlaendingestyrelsen["Udlændingestyrelsen"]:::instans
    sty_udviklings_og_forenklingsstyrelsen["Udviklings- og Forenklingsstyrelsen"]:::instans
    tilsyn_vandsektortilsynet["Vandsektortilsynet"]:::instans
    sty_vejdirektoratet["Vejdirektoratet"]:::instans
    naevn_vurderingsankenaevn["Vurderingsankenævn"]:::klage
    sty_vurderingsstyrelsen["Vurderingsstyrelsen"]:::instans
    min_beskaeftigelse_og_ligestilling -->|ressortansvar| naevn_arbejdsmiljoeklagenaevnet
    min_beskaeftigelse_og_ligestilling -->|ressortansvar| org_nfa
    min_beskaeftigelse_og_ligestilling -->|ressortansvar| org_udbetaling_danmark
    min_beskaeftigelse_og_ligestilling -->|ressortansvar| raad_arbejdsmarkedsraadet
    min_beskaeftigelse_og_ligestilling -->|ressortansvar| raad_arbejdsmiljoeraadet
    min_beskaeftigelse_og_ligestilling -->|ressortansvar| sty_arbejdstilsynet
    min_boern_aeldre_og_bolig -->|ressortansvar| fond_blandede_byer
    min_boern_aeldre_og_bolig -.->|ressortansvar| fond_byggeskadefonden
    min_boern_aeldre_og_bolig -->|ressortansvar| fond_byggeskadefonden_bygningsfornyelse
    min_boern_aeldre_og_bolig -->|ressortansvar| fond_grundejernes_investeringsfond
    min_boern_aeldre_og_bolig -->|ressortansvar| fond_landsbyggefonden
    min_boern_aeldre_og_bolig -.->|ressortansvar| naevn_beboerklagenaevn
    min_boern_aeldre_og_bolig -.->|ressortansvar| naevn_byggeklageenheden
    min_boern_aeldre_og_bolig -.->|ressortansvar| naevn_huslejenaevn
    min_by_land_og_kirke -->|ressortansvar| sty_plan_og_landdistriktsstyrelsen
    min_by_land_og_transport -->|ressortansvar| naevn_taksationsmyndighederne
    min_by_land_og_transport -->|ressortansvar| sty_faerdselsstyrelsen
    min_by_land_og_transport -->|ressortansvar| sty_plan_og_landdistriktsstyrelsen
    min_by_land_og_transport -.->|ressortansvar| sty_trafik_bygge_og_boligstyrelsen
    min_by_land_og_transport -->|ressortansvar| sty_vejdirektoratet
    min_erhverv -.->|ressortansvar| naevn_energiklagenaevnet
    min_erhverv -.->|ressortansvar| naevn_erhvervsankenaevnet
    min_erhverv -.->|ressortansvar| naevn_klagenaevnet_for_udbud
    min_erhverv -.->|ressortansvar| naevn_konkurrenceankenaevnet
    min_erhverv -.->|ressortansvar| naevn_miljoe_og_foedevareklagenaevnet
    min_erhverv -.->|ressortansvar| naevn_planklagenaevnet
    min_erhverv -->|ressortansvar| raad_el_og_gasteknisk_sikkerhed
    min_erhverv -->|ressortansvar| sty_erhvervsstyrelsen
    min_erhverv -.->|ressortansvar| sty_konkurrence_og_forbrugerstyrelsen
    min_erhverv -->|ressortansvar| sty_naevnenes_hus
    min_erhverv -->|ressortansvar| sty_sikkerhedsstyrelsen
    min_erhverv -->|ressortansvar| tilsyn_vandsektortilsynet
    min_forsvar -->|ressortansvar| sty_beredskabsstyrelsen
    min_groen_trepart -.->|ressortansvar| sty_groen_arealomlaegning_og_vandmiljoe
    min_groen_trepart -->|ressortansvar| sty_naturstyrelsen
    min_indenrigs_og_bolig -->|ressortansvar| sty_bolig_og_planstyrelsen
    min_justits -->|ressortansvar| sty_civilstyrelsen
    min_justits -->|ressortansvar| sty_domstolsstyrelsen
    min_justits -->|ressortansvar| sty_rigsadvokaten
    min_klima_energi_og_forsyning -.->|ressortansvar| naevn_landinspektoernaevnet
    min_klima_energi_og_forsyning -->|ressortansvar| org_energinet
    min_klima_energi_og_forsyning -->|ressortansvar| raad_klimaraadet
    min_klima_energi_og_forsyning -->|ressortansvar| sty_energistyrelsen
    min_klima_energi_og_forsyning -->|ressortansvar| sty_geodatastyrelsen
    min_klima_energi_og_forsyning -->|ressortansvar| sty_klimadatastyrelsen
    min_klima_energi_og_forsyning -->|ressortansvar| tilsyn_energitilsynet
    min_klima_energi_og_forsyning -->|ressortansvar| tilsyn_forsyningstilsynet
    min_kultur -->|ressortansvar| raad_det_saerlige_bygningssyn
    min_kultur -->|ressortansvar| sty_kulturarvsstyrelsen
    min_kultur -->|ressortansvar| sty_kulturstyrelsen
    min_kultur -->|ressortansvar| sty_slots_og_kulturstyrelsen
    min_miljoe -->|ressortansvar| naevn_natur_og_miljoeklagenaevnet
    min_miljoe -.->|ressortansvar| org_danmarks_miljoeportal
    min_miljoe -->|ressortansvar| sty_by_og_landskabsstyrelsen
    min_miljoe -->|ressortansvar| sty_kystdirektoratet
    min_miljoe -->|ressortansvar| sty_miljoestyrelsen
    min_miljoe -->|ressortansvar| sty_planstyrelsen
    min_miljoe_og_ligestilling -->|ressortansvar| sty_kystdirektoratet
    min_miljoe_og_ligestilling -->|ressortansvar| sty_miljoestyrelsen
    min_natur_og_dyrevelfaerd -.->|ressortansvar| naevn_fredningsnaevn
    min_natur_og_dyrevelfaerd -->|ressortansvar| naevn_taksationskommissionen
    min_natur_og_dyrevelfaerd -->|ressortansvar| sty_groen_arealomlaegning_og_vandmiljoe
    min_natur_og_dyrevelfaerd -->|ressortansvar| sty_landbrugsstyrelsen
    min_natur_og_dyrevelfaerd -->|ressortansvar| sty_naturstyrelsen
    min_oekonomi_og_indenrigs -->|ressortansvar| org_statsforvaltningen
    min_samfundssikkerhed_og_beredskab -->|ressortansvar| sty_beredskabsstyrelsen
    min_samfundssikkerhed_og_beredskab -->|ressortansvar| sty_styrelsen_for_forsyningssikkerhed
    min_samfundssikkerhed_og_beredskab -->|ressortansvar| sty_styrelsen_for_samfundssikkerhed
    min_skat_og_vaekst -->|ressortansvar| sty_vurderingsstyrelsen
    min_social -->|ressortansvar| sty_ankestyrelsen
    min_social -.->|ressortansvar| sty_social_og_boligstyrelsen
    min_skat_og_vaekst -->|ressortansvar| sty_skatteforvaltningen
    min_skat_og_vaekst -->|ressortansvar| sty_skattestyrelsen
    min_skat_og_vaekst -->|ressortansvar| sty_toldstyrelsen
    min_skat_og_vaekst -->|ressortansvar| sty_gaeldsstyrelsen
    min_skat_og_vaekst -->|ressortansvar| sty_motorstyrelsen
    min_skat_og_vaekst -->|ressortansvar| sty_udviklings_og_forenklingsstyrelsen
    min_skat_og_vaekst -->|ressortansvar| sty_administrations_og_servicestyrelsen
    min_skat_og_vaekst -->|ressortansvar| sty_skatteankestyrelsen
    min_skat_og_vaekst -->|ressortansvar| sty_spillemyndigheden
    min_skat_og_vaekst -->|ressortansvar| raad_skatteraadet
    min_skat_og_vaekst -->|ressortansvar| naevn_landsskatteretten
    min_skat_og_vaekst -->|ressortansvar| naevn_skatteankenaevn
    min_skat_og_vaekst -->|ressortansvar| naevn_vurderingsankenaevn
    min_skat_og_vaekst -->|ressortansvar| naevn_motorankenaevn
    min_skat_og_vaekst -->|ressortansvar| tilsyn_it_tilsynet
    min_sundhed_og_kirke -.->|ressortansvar| sty_sundhedsstyrelsen
    min_sundhed_og_kirke -.->|ressortansvar| sty_styrelsen_for_patientsikkerhed
    min_sundhed_og_kirke -.->|ressortansvar| sty_styrelsen_for_patientklager
    min_sundhed_og_kirke -.->|ressortansvar| sty_laegemiddelstyrelsen
    min_sundhed_og_kirke -.->|ressortansvar| sty_sundhedsdatastyrelsen
    min_sundhed_og_kirke -->|ressortansvar| sty_statens_serum_institut
    min_sundhed_og_kirke -.->|ressortansvar| naevn_sundhedsvaesenets_disciplinaernaevn
    min_sundhed_og_kirke -.->|ressortansvar| naevn_ankenaevnet_for_patienterstatningen
    min_sundhed_og_kirke -.->|ressortansvar| naevn_tvangsbehandlingsnaevnet
    min_sundhed_og_kirke -.->|ressortansvar| naevn_ankenaevnet_for_tilsynsafgoerelser
    min_sundhed_og_kirke -.->|ressortansvar| naevn_det_psykiatriske_ankenaevn
    min_sundhed_og_kirke -.->|ressortansvar| naevn_det_psykiatriske_patientklagenaevn
    min_sundhed_og_kirke -->|ressortansvar| raad_laegemiddelnaevnet
    min_sundhed_og_kirke -.->|ressortansvar| org_patienterstatningen
    min_skat_og_vaekst -->|ressortansvar| sty_finanstilsynet
    min_skat_og_vaekst -.->|ressortansvar| org_finansiel_stabilitet
    min_skat_og_vaekst -.->|ressortansvar| raad_det_systemiske_risikoraad
    min_udlaendinge_og_integration -.->|ressortansvar| sty_udlaendingestyrelsen
    min_udlaendinge_og_integration -.->|ressortansvar| sty_siri
    min_udlaendinge_og_integration -->|ressortansvar| sty_hjemrejsestyrelsen
    min_udlaendinge_og_integration -->|ressortansvar| naevn_udlaendingenaevnet
    min_udlaendinge_og_integration -->|ressortansvar| naevn_flygtningenaevnet
```

## Ministerområder

- [Beskæftigelses- og Ligestillingsministeriet](min-beskaeftigelse-og-ligestilling.md)
- [By-, Land- og Kirkeministeriet](min-by-land-og-kirke.md)
- [By-, Land- og Transportministeriet](min-by-land-og-transport.md)
- [Børne-, Ældre- og Boligministeriet](min-boern-aeldre-og-bolig.md)
- [Erhvervsministeriet](min-erhverv.md)
- [Finansministeriet](min-finans.md)
- [Forsknings-, Uddannelses- og Digitaliseringsministeriet](min-forskning-uddannelse-og-digitalisering.md)
- [Forsvarsministeriet](min-forsvar.md)
- [Indenrigs- og Boligministeriet](min-indenrigs-og-bolig.md)
- [Justitsministeriet](min-justits.md)
- [Klima-, Energi- og Forsyningsministeriet](min-klima-energi-og-forsyning.md)
- [Kulturministeriet](min-kultur.md)
- [Miljø- og Ligestillingsministeriet (2024-3/6/2026)](min-miljoe-og-ligestilling.md)
- [Miljøministeriet](min-miljoe.md)
- [Ministeriet for Grøn Trepart (29/8/2024-3/6/2026)](min-groen-trepart.md)
- [Ministeriet for Natur og Dyrevelfærd](min-natur-og-dyrevelfaerd.md)
- [Ministeriet for Samfundssikkerhed og Beredskab](min-samfundssikkerhed-og-beredskab.md)
- [Skatte- og Vækstministeriet](min-skat-og-vaekst.md)
- [Socialministeriet](min-social.md)
- [Statsministeriet](min-statsministeriet.md)
- [Sundheds- og Kirkeministeriet](min-sundhed-og-kirke.md)
- [Udenrigsministeriet](min-udenrigs.md)
- [Udlændinge- og Integrationsministeriet](min-udlaendinge-og-integration.md)
- [Undervisningsministeriet](min-undervisning.md)
- [Økonomi- og Indenrigsministeriet](min-oekonomi-og-indenrigs.md)
