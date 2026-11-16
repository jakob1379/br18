# Justitsministeriet

> Genereret af `scripts/build.py` fra `registry.yaml` (dato 2026-10-28). Redigér ikke i hånden.
> Fuldt optrukne pile = `verificeret`; stiplede = `sandsynlig`/`ukendt`. Grå stiplede bokse = nedlagt/omdøbt/ophævet.

Noder: 101 · kanter: 156

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
    eu_reg_2016_679["Databeskyttelsesforordningen, forordning (EU) 2016/679 (GDPR)"]:::eu
    eu_dir_2005_36["Europa-Parlamentets og Rådets direktiv 2005/36/EF af 7. september 2005 om anerkendelse af erhvervsmæssige kvalifikationer"]:::eu
    eu_dir_2016_680["Retshåndhævelsesdirektivet, direktiv (EU) 2016/680"]:::eu
    eu_dir_2012_18["Seveso III-direktivet (direktiv 2012/18/EU om kontrol med risikoen for større uheld med farlige stoffer)"]:::eu
    raad_advokatraadet["Advokatrådet"]:::instans
    sty_ankestyrelsen["Ankestyrelsen"]:::instans
    tilsyn_bevismiddeltilsynet["Bevismiddeltilsynet (Det Uafhængige Tilsyn med Bevismidler)"]:::instans
    sty_civilstyrelsen["Civilstyrelsen"]:::instans
    sty_danmarks_faengsler["Danmarks Fængsler (Styrelsen for Danmarks Fængsler)"]:::instans
    raad_dataraadet["Datarådet"]:::instans
    tilsyn_datatilsynet["Datatilsynet"]:::instans
    sty_politiklagemyndigheden["Den Uafhængige Politiklagemyndighed (Politiklagemyndigheden)"]:::instans
    raad_det_dyreetiske_raad["Det Dyreetiske Råd"]:::instans
    raad_dommerudnaevnelsesraadet["Dommerudnævnelsesrådet"]:::instans
    sty_domstolsstyrelsen["Domstolsstyrelsen"]:::instans
    sty_familieretshuset["Familieretshuset"]:::instans
    sty_politikredsene["Politikredsene (politidirektørerne)"]:::instans
    raad_retslaegeraadet["Retslægerådet"]:::instans
    sty_rigsadvokaten["Rigsadvokaten"]:::instans
    sty_rigspolitiet["Rigspolitiet"]:::instans
    sty_statsadvokaterne["Statsadvokaterne"]:::instans
    kilde_vidensbasen["Anklagemyndighedens Vidensbase"]:::kilde
    kilde_datatilsynet_afgoerelser["Datatilsynets afgørelser (datatilsynet.dk/afgoerelser)"]:::kilde
    kilde_datatilsynet_vejledninger["Datatilsynets vejledninger og regler (datatilsynet.dk/regler-og-vejledning)"]:::kilde
    org_advokatsamfundet["Det Danske Advokatsamfund"]:::kilde
    kilde_domsdatabasen["Domsdatabasen"]:::kilde
    kilde_eurlex["EUR-Lex"]:::kilde
    kilde_eurlex_nim["EUR-Lex: nationale gennemførelsesforanstaltninger (NIM) for direktiver"]:::kilde
    kilde_fob_database["Folketingets Ombudsmands udtalelser"]:::kilde
    kilde_folketingstidende["Folketingstidende og ft.dk-samlinger (lovforslag, bemærkninger, betænkninger, svar)"]:::kilde
    kilde_lovguiden["Lovguiden (lovguiden.dk)"]:::kilde
    kilde_lovtidende["Lovtidende"]:::kilde
    kilde_politiklagemyndigheden_udgivelser["Politiklagemyndighedens årsberetninger og årsrapporter"]:::kilde
    kilde_pressenaevnet_kendelser["Pressenævnets kendelser"]:::kilde
    kilde_retsinformation["Retsinformation"]:::kilde
    kilde_rigsadvokatmeddelelsen["Rigsadvokatmeddelelsen (samlingen, afsnit for afsnit)"]:::kilde
    kilde_statstidende["Statstidende"]:::kilde
    kilde_ugeskrift_for_retsvaesen["Ugeskrift for Retsvæsen (UfR, Karnov Group)"]:::kilde
    kilde_danish_law_mcp["danish-law-mcp (Ansvar Systems): bulk-høst af Retsinformation, Lovtidende A"]:::kilde
    naevn_advokatnaevnet["Advokatnævnet"]:::klage
    dom_byretterne["Byretterne"]:::klage
    dom_den_saerlige_klageret["Den Særlige Klageret"]:::klage
    dom_domstolene["Domstolene (byret, landsret, Højesteret)"]:::klage
    naevn_erstatningsnaevnet["Erstatningsnævnet"]:::klage
    ombud_forbrugerombudsmanden["Forbrugerombudsmanden"]:::klage
    dom_hoejesteret["Højesteret"]:::klage
    naevn_indsamlingsnaevnet["Indsamlingsnævnet"]:::klage
    dom_landsretterne["Landsretterne (Østre og Vestre Landsret)"]:::klage
    naevn_ligebehandlingsnaevnet["Ligebehandlingsnævnet"]:::klage
    naevn_pressenaevnet["Pressenævnet"]:::klage
    naevn_procesbevillingsnaevnet["Procesbevillingsnævnet"]:::klage
    dom_soe_og_handelsretten["Sø- og Handelsretten"]:::klage
    dom_tinglysningsretten["Tinglysningsretten"]:::klage
    naevn_ungdomskriminalitetsnaevnet["Ungdomskriminalitetsnævnet"]:::klage
    eu_dir_2010_31["Direktiv 2010/31/EU om bygningers energimæssige ydeevne (EPBD, som ændret ved 2018/844) (ophævet)"]:::nedlagt
    eu_dir_2012_27["Europa-Parlamentets og Rådets direktiv 2012/27/EU af 25. oktober 2012 om energieffektivitet (EED) (ophævet)"]:::nedlagt
    kilde_ministerialtidende["Ministerialtidende (nedlagt)"]:::nedlagt
    lov_arbejdsmiljoeloven["Arbejdsmiljøloven"]:::retsakt
    lov_medieansvarsloven["Bekendtgørelse af medieansvarsloven"]:::retsakt
    bek_advokatnaevnets_virksomhed["Bekendtgørelse om Advokatnævnets virksomhed ved behandling af klager over advokater m.v."]:::retsakt
    bek_domsdatabasen["Bekendtgørelse om Domsdatabasen"]:::retsakt
    bek_erstatningsnaevnets_behandling_af_ansoegninger["Bekendtgørelse om Erstatningsnævnets behandling af ansøgninger om erstatning fra staten til ofre for forbrydelser"]:::retsakt
    bek_energimaerkning["Bekendtgørelse om energimærkning af bygninger (energimærkningsbekendtgørelsen)"]:::retsakt
    bek_dataraadet_forretningsorden["Bekendtgørelse om forretningsorden for Datarådet (BEK nr. 454 af 01/01/2019)"]:::retsakt
    bek_forretningsorden_erstatningsnaevnet["Bekendtgørelse om forretningsorden for Erstatningsnævnet"]:::retsakt
    bek_pressenaevn_forretningsorden["Bekendtgørelse om forretningsorden for Pressenævnet (BEK nr. 86 af 09/02/1998)"]:::retsakt
    bek_drikkevand_byggevarer["Bekendtgørelse om markedsføring og salg af byggevarer i kontakt med drikkevand (GDV-ordningen)"]:::retsakt
    bek_lag["Bekendtgørelse om tilskud til lokale aktionsgrupper – lokalt styret udvikling (LEADER) (BEK nr. 948 af 2025)"]:::retsakt
    bek_ungekriminalforsorgens_reaktioner["Bekendtgørelse om ungekriminalforsorgens reaktioner ved overtrædelse af Ungdomskriminalitetsnævnets afgørelse"]:::retsakt
    bek_ungekriminalforsorgens_tilsyn["Bekendtgørelse om ungekriminalforsorgens tilsyn med barnets eller den unges efterlevelse af Ungdomskriminalitetsnævnets afgørelse"]:::retsakt
    cirk_retsinformation_afgoerelser["Cirkulære om indlæggelse af afgørelser i Retsinformation"]:::retsakt
    lov_databeskyttelsesloven["Databeskyttelsesloven"]:::retsakt
    vejl_fob_myndighedsguiden["Folketingets Ombudsmands Myndighedsguide"]:::retsakt
    lov_forvaltningsloven["Forvaltningsloven"]:::retsakt
    lov_domstolsstyrelsesloven["Lov om Domstolsstyrelsen"]:::retsakt
    lov_miljoeoplysningsloven["Lov om aktindsigt i miljøoplysninger (miljøoplysningsloven)"]:::retsakt
    lov_ungdomskriminalitetsloven["Lov om bekæmpelse af ungdomskriminalitet"]:::retsakt
    lov_dyrevelfaerdsloven["Lov om dyrevelfærd (dyrevelfærdsloven)"]:::retsakt
    lov_offererstatningsloven["Lov om erstatning fra staten til ofre for forbrydelser (offererstatningsloven)"]:::retsakt
    lov_forbrugeraftaleloven["Lov om forbrugeraftaler (forbrugeraftaleloven)"]:::retsakt
    lov_straffuldbyrdelsesloven["Lov om fuldbyrdelse af straf m.v. (straffuldbyrdelsesloven)"]:::retsakt
    lov_indsamlingsloven["Lov om indsamling m.v."]:::retsakt
    lov_koebeloven["Lov om køb (købeloven)"]:::retsakt
    lov_markedsfoeringsloven["Lov om markedsføring (markedsføringsloven)"]:::retsakt
    lov_offentlighedsloven["Lov om offentlighed i forvaltningen (offentlighedsloven)"]:::retsakt
    lov_politiloven["Lov om politiets virksomhed (politiloven)"]:::retsakt
    lov_retslaegeraadet["Lov om retslægerådet"]:::retsakt
    lov_retssikkerhedsloven_tvangsindgreb["Lov om retssikkerhed ved forvaltningens anvendelse af tvangsindgreb og oplysningspligter"]:::retsakt
    lov_lovtidendeloven["Lov om udgivelsen af en Lovtidende (lovtidendeloven)"]:::retsakt
    lov_retshaandhaevelsesloven["Retshåndhævelsesloven (lov om retshåndhævende myndigheders behandling af personoplysninger)"]:::retsakt
    lov_retsplejeloven["Retsplejeloven"]:::retsakt
    cirk_rigsadvokatmeddelelsen_arbejdsmiljoe["Rigsadvokatmeddelelsen, afsnittet om arbejdsmiljø"]:::retsakt
    bek_risiko["Risikobekendtgørelsen (bekendtgørelse om kontrol med risikoen for større uheld med farlige stoffer)"]:::retsakt
    lov_straffeloven["Straffeloven"]:::retsakt
    lov_tv_overvaagningsloven["Tv-overvågningsloven"]:::retsakt
    vejl_administrative_forskrifter["Vejledning om administrative forskrifter (Justitsministeriet)"]:::retsakt
    vejl_forvaltningsloven["Vejledning om forvaltningsloven (Justitsministeriet)"]:::retsakt
    vejl_offentlighedsloven["Vejledning om lov om offentlighed i forvaltningen (Justitsministeriet)"]:::retsakt
    vejl_lovkvalitet["Vejledning om lovkvalitet (Justitsministeriet)"]:::retsakt
    lov_vaergemaalsloven["Værgemålsloven"]:::retsakt
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
    min_justits -->|ressortansvar| lov_dyrevelfaerdsloven
    lov_dyrevelfaerdsloven -->|hjemmel_for| raad_det_dyreetiske_raad
    min_justits -->|ressortansvar| tilsyn_datatilsynet
    min_justits -.->|ressortansvar| raad_dataraadet
    min_justits -.->|ressortansvar| lov_databeskyttelsesloven
    min_justits -.->|ressortansvar| lov_retshaandhaevelsesloven
    min_justits -->|ressortansvar| lov_tv_overvaagningsloven
    min_justits -.->|ressortansvar| bek_dataraadet_forretningsorden
    lov_databeskyttelsesloven -->|hjemmel_for| tilsyn_datatilsynet
    lov_databeskyttelsesloven -->|hjemmel_for| raad_dataraadet
    lov_databeskyttelsesloven -->|hjemmel_for| bek_dataraadet_forretningsorden
    lov_databeskyttelsesloven -.->|hjemmel_for| sty_domstolsstyrelsen
    lov_retshaandhaevelsesloven -.->|hjemmel_for| tilsyn_datatilsynet
    lov_retshaandhaevelsesloven -->|hjemmel_for| sty_domstolsstyrelsen
    lov_tv_overvaagningsloven -->|hjemmel_for| tilsyn_datatilsynet
    lov_databeskyttelsesloven -.->|henviser_til| eu_reg_2016_679
    lov_retshaandhaevelsesloven -->|implementerer_EU| eu_dir_2016_680
    sty_domstolsstyrelsen -.->|tilsyn| dom_domstolene
    dom_domstolene -.->|klageinstans| tilsyn_datatilsynet
    tilsyn_datatilsynet -->|udsteder| kilde_datatilsynet_afgoerelser
    tilsyn_datatilsynet -->|udsteder| kilde_datatilsynet_vejledninger
    min_justits -.->|ressortansvar| sty_rigspolitiet
    min_justits -.->|ressortansvar| sty_politikredsene
    min_justits -.->|ressortansvar| sty_statsadvokaterne
    min_justits -.->|ressortansvar| sty_politiklagemyndigheden
    min_justits -->|ressortansvar| sty_danmarks_faengsler
    min_justits -.->|ressortansvar| naevn_erstatningsnaevnet
    min_justits -.->|ressortansvar| naevn_ungdomskriminalitetsnaevnet
    min_justits -.->|ressortansvar| lov_straffeloven
    min_justits -.->|ressortansvar| lov_politiloven
    min_justits -.->|ressortansvar| lov_straffuldbyrdelsesloven
    min_justits -->|ressortansvar| lov_offererstatningsloven
    min_justits -.->|ressortansvar| lov_ungdomskriminalitetsloven
    lov_retsplejeloven -->|hjemmel_for| sty_rigspolitiet
    lov_retsplejeloven -.->|hjemmel_for| sty_politikredsene
    lov_retsplejeloven -.->|hjemmel_for| sty_statsadvokaterne
    lov_retsplejeloven -->|hjemmel_for| sty_politiklagemyndigheden
    lov_straffuldbyrdelsesloven -.->|hjemmel_for| sty_danmarks_faengsler
    lov_offererstatningsloven -.->|hjemmel_for| naevn_erstatningsnaevnet
    lov_ungdomskriminalitetsloven -->|hjemmel_for| naevn_ungdomskriminalitetsnaevnet
    lov_offererstatningsloven -->|hjemmel_for| bek_erstatningsnaevnets_behandling_af_ansoegninger
    lov_offererstatningsloven -->|hjemmel_for| bek_forretningsorden_erstatningsnaevnet
    lov_ungdomskriminalitetsloven -->|hjemmel_for| bek_ungekriminalforsorgens_tilsyn
    lov_ungdomskriminalitetsloven -->|hjemmel_for| bek_ungekriminalforsorgens_reaktioner
    sty_rigspolitiet -->|klageinstans| sty_politikredsene
    sty_statsadvokaterne -.->|klageinstans| sty_politikredsene
    sty_rigsadvokaten -.->|klageinstans| sty_statsadvokaterne
    sty_ankestyrelsen -->|klageinstans| naevn_ungdomskriminalitetsnaevnet
    dom_byretterne -->|klageinstans| sty_danmarks_faengsler
    sty_rigspolitiet -->|tilsyn| sty_politikredsene
    sty_statsadvokaterne -->|tilsyn| sty_politikredsene
    sty_rigsadvokaten -->|tilsyn| sty_statsadvokaterne
    sty_rigsadvokaten -->|udsteder| kilde_rigsadvokatmeddelelsen
    sty_rigsadvokaten -.->|udsteder| kilde_vidensbasen
    sty_politiklagemyndigheden -->|udsteder| kilde_politiklagemyndigheden_udgivelser
    naevn_ligebehandlingsnaevnet -->|udsteder| kilde_retsinformation
    lov_forvaltningsloven -->|hjemmel_for| bek_energimaerkning
    lov_forvaltningsloven -->|hjemmel_for| bek_lag
    lov_politiloven -->|hjemmel_for| bek_risiko
    min_justits -.->|ressortansvar| lov_forbrugeraftaleloven
    min_justits -->|ressortansvar| lov_koebeloven
    lov_forbrugeraftaleloven -->|hjemmel_for| ombud_forbrugerombudsmanden
    lov_forbrugeraftaleloven -->|henviser_til| lov_markedsfoeringsloven
    min_justits -.->|ressortansvar| lov_vaergemaalsloven
    lov_vaergemaalsloven -->|hjemmel_for| sty_familieretshuset
    sty_civilstyrelsen -->|klageinstans| sty_familieretshuset
    min_justits -->|ressortansvar| lov_indsamlingsloven
    min_justits -->|ressortansvar| lov_retslaegeraadet
    min_justits -->|ressortansvar| bek_advokatnaevnets_virksomhed
    min_justits -.->|ressortansvar| naevn_indsamlingsnaevnet
    lov_retsplejeloven -->|hjemmel_for| org_advokatsamfundet
    lov_retsplejeloven -->|hjemmel_for| raad_advokatraadet
    lov_retsplejeloven -->|hjemmel_for| naevn_advokatnaevnet
    bek_advokatnaevnets_virksomhed -->|hjemmel_for| naevn_advokatnaevnet
    lov_retsplejeloven -->|hjemmel_for| dom_soe_og_handelsretten
    lov_retsplejeloven -->|hjemmel_for| dom_tinglysningsretten
    lov_retsplejeloven -->|hjemmel_for| raad_dommerudnaevnelsesraadet
    lov_retsplejeloven -->|hjemmel_for| dom_den_saerlige_klageret
    lov_retslaegeraadet -.->|hjemmel_for| raad_retslaegeraadet
    lov_indsamlingsloven -->|hjemmel_for| naevn_indsamlingsnaevnet
    min_justits -.->|ressortansvar| lov_medieansvarsloven
    min_justits -.->|ressortansvar| naevn_pressenaevnet
    lov_medieansvarsloven -->|hjemmel_for| naevn_pressenaevnet
    lov_medieansvarsloven -->|hjemmel_for| bek_pressenaevn_forretningsorden
    naevn_pressenaevnet -->|udsteder| kilde_pressenaevnet_kendelser
    lov_forvaltningsloven -->|hjemmel_for| bek_drikkevand_byggevarer
    lov_offentlighedsloven -->|hjemmel_for| bek_drikkevand_byggevarer
    lov_offentlighedsloven -->|hjemmel_for| bek_lag
    lov_offentlighedsloven -->|hjemmel_for| vejl_offentlighedsloven
    lov_retsplejeloven -->|hjemmel_for| bek_advokatnaevnets_virksomhed
    min_justits -.->|ressortansvar| tilsyn_bevismiddeltilsynet
    lov_retsplejeloven -->|hjemmel_for| tilsyn_bevismiddeltilsynet
    bek_energimaerkning -->|implementerer_EU| eu_dir_2010_31
    bek_risiko -->|implementerer_EU| eu_dir_2012_18
    bek_energimaerkning -->|implementerer_EU| eu_dir_2005_36
    bek_energimaerkning -->|implementerer_EU| eu_dir_2012_27
```

[← Overblik](oversigt.md)
