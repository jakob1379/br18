# Beskæftigelses- og Ligestillingsministeriet

> Genereret af `scripts/build.py` fra `registry.yaml` (dato 2026-10-28). Redigér ikke i hånden.
> Fuldt optrukne pile = `verificeret`; stiplede = `sandsynlig`/`ukendt`. Grå stiplede bokse = nedlagt/omdøbt/ophævet.

Noder: 113 · kanter: 202

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
    eu_dir_2023_2668["Direktiv (EU) 2023/2668 om ændring af direktiv 2009/148/EF (asbest)"]:::eu
    eu_dir_1999_92["Direktiv 1999/92/EF om minimumsforskrifter for sikkerhed og sundhed for arbejdstagere, som kan udsættes for risiko for eksplosiv atmosfære (ATEX-brugerdirektivet)"]:::eu
    eu_dir_2000_54["Direktiv 2000/54/EF om beskyttelse af arbejdstagerne mod risici i forbindelse med at være udsat for biologiske agenser under arbejdet"]:::eu
    eu_dir_2002_44["Direktiv 2002/44/EF om fysiske agenser (vibrationer)"]:::eu
    eu_dir_2003_88["Direktiv 2003/88/EF om visse aspekter i forbindelse med tilrettelæggelse af arbejdstiden (arbejdstidsdirektivet)"]:::eu
    eu_dir_2004_37["Direktiv 2004/37/EF om beskyttelse af arbejdstagerne mod risici for at blive udsat for kræftfremkaldende stoffer, mutagener eller reproduktionstoksiske stoffer under arbejdet (CMRD)"]:::eu
    eu_dir_2006_42["Direktiv 2006/42/EF om maskiner (maskindirektivet)"]:::eu
    eu_dir_2009_104["Direktiv 2009/104/EF om minimumsforskrifter for arbejdstagernes brug af arbejdsudstyr (arbejdsudstyrsdirektivet)"]:::eu
    eu_dir_2009_148["Direktiv 2009/148/EF om beskyttelse af arbejdstagerne mod risici for asbestpåvirkning"]:::eu
    eu_dir_2013_30["Direktiv 2013/30/EU om sikkerhed i forbindelse med offshore olie- og gasaktiviteter (offshoresikkerhedsdirektivet)"]:::eu
    eu_dir_2013_35["Direktiv 2013/35/EU om fysiske agenser (elektromagnetiske felter)"]:::eu
    eu_dir_2014_33["Direktiv 2014/33/EU om elevatorer og sikkerhedskomponenter til elevatorer"]:::eu
    eu_dir_2015_1535["Europa-Parlamentets og Rådets direktiv (EU) 2015/1535 af 9. september 2015 om en informationsprocedure med hensyn til tekniske forskrifter og forskrifter for informationssamfundets tjenester (informationsproceduredirektivet, TRIS)"]:::eu
    eu_dir_2005_36["Europa-Parlamentets og Rådets direktiv 2005/36/EF af 7. september 2005 om anerkendelse af erhvervsmæssige kvalifikationer"]:::eu
    eu_reg_2006_1907["Forordning (EF) nr. 1907/2006 (REACH)"]:::eu
    eu_dir_1989_391["Rådets direktiv 89/391/EØF (rammedirektivet om sikkerhed og sundhed under arbejdet)"]:::eu
    eu_dir_1989_654["Rådets direktiv 89/654/EØF om minimumsforskrifter for sikkerhed og sundhed på arbejdsstedet (arbejdsstedsdirektivet)"]:::eu
    eu_dir_1992_57["Rådets direktiv 92/57/EØF om midlertidige eller mobile byggepladser (byggepladsdirektivet)"]:::eu
    eu_dir_1994_33["Rådets direktiv 94/33/EF om beskyttelse af unge på arbejdspladsen"]:::eu
    eu_dir_1998_24["Rådets direktiv 98/24/EF om beskyttelse af arbejdstagernes sikkerhed og sundhed under arbejdet mod risici i forbindelse med kemiske agenser"]:::eu
    eu_dir_2012_18["Seveso III-direktivet (direktiv 2012/18/EU om kontrol med risikoen for større uheld med farlige stoffer)"]:::eu
    sty_ankestyrelsen["Ankestyrelsen"]:::instans
    org_arbejdsmarkedets_erhvervssikring["Arbejdsmarkedets Erhvervssikring (AES)"]:::instans
    org_atp["Arbejdsmarkedets Tillægspension (ATP)"]:::instans
    raad_arbejdsmarkedsraadet["Arbejdsmarkedsrådet"]:::instans
    sty_arbejdstilsynet["Arbejdstilsynet"]:::instans
    org_nfa["Det Nationale Forskningscenter for Arbejdsmiljø (NFA)"]:::instans
    sty_erhvervsstyrelsen["Erhvervsstyrelsen"]:::instans
    sty_forligsinstitutionen["Forligsinstitutionen"]:::instans
    kommune_alle["Kommunerne (98 kommunalbestyrelser)"]:::instans
    fond_loenmodtagernes_garantifond["Lønmodtagernes Garantifond (LG)"]:::instans
    org_seniorpensionsenheden["Seniorpensionsenheden"]:::instans
    sty_star["Styrelsen for Arbejdsmarked og Rekruttering (STAR)"]:::instans
    raad_tilsynsraadet["Tilsynsrådet (STAR)"]:::instans
    org_udbetaling_danmark["Udbetaling Danmark"]:::instans
    kilde_aes_love_og_praksis["AES: Love og praksis"]:::kilde
    org_a_kasser["Anerkendte arbejdsløshedskasser (a-kasser)"]:::kilde
    kilde_ast_amkn["Ankestyrelsen – Arbejdsmiljøklagenævnets publikationer (ast.dk)"]:::kilde
    kilde_ast_principmeddelelser["Ankestyrelsens principmeddelelser og tilsynsudtalelser"]:::kilde
    org_autoriserede_arbejdsmiljoeraadgivere["Autoriserede arbejdsmiljørådgivere"]:::kilde
    org_bfa_bygge_og_anlaeg["BFA Bygge & Anlæg (Branchefællesskabet for arbejdsmiljø i bygge og anlæg)"]:::kilde
    bv_bfa_branchevejledninger["BFA Bygge & Anlæg – branchevejledninger"]:::kilde
    org_faglige_voldgiftsretter["Faglige voldgiftsretter"]:::kilde
    kilde_star_love_og_regler["STAR: Love og regler (henvisning til Retsinformation)"]:::kilde
    kilde_at_dk["at.dk (Arbejdstilsynets hjemmeside)"]:::kilde
    kilde_regler_at_dk["regler.at.dk (Arbejdstilsynets regelportal)"]:::kilde
    naevn_ankenaevn_atp["Ankenævnet for Arbejdsmarkedets Tillægspension"]:::klage
    naevn_arbejdsmiljoeklagenaevnet["Arbejdsmiljøklagenævnet"]:::klage
    dom_arbejdsretten["Arbejdsretten"]:::klage
    dom_domstolene["Domstolene (byret, landsret, Højesteret)"]:::klage
    ombud_folketingets_ombudsmand["Folketingets Ombudsmand"]:::klage
    naevn_ligebehandlingsnaevnet["Ligebehandlingsnævnet"]:::klage
    raad_arbejdsmiljoeraadet["Arbejdsmiljørådet (nedlagt)"]:::nedlagt
    bek_autoriserede_arbejdsmiljoeraadgivere["Bekendtgørelse om brug af autoriserede arbejdsmiljørådgivere (ophævet)"]:::nedlagt
    vejl_at_bygge_og_anlaeg["AT-vejledning om bygge- og anlægsarbejde"]:::retsakt
    vejl_at_bygherrens_pligter["AT-vejledning om bygherrens pligter"]:::retsakt
    vejl_at_vejledninger["AT-vejledninger (samling)"]:::retsakt
    lov_arbejdsmiljoeloven["Arbejdsmiljøloven"]:::retsakt
    bek_at_offshore_opgaver["Bekendtgørelse om Arbejdstilsynets opgaver og beføjelser efter offshoresikkerhedsloven (BEK nr 1354 af 11/12/2019)"]:::retsakt
    bek_personlige_vaernemidler["Bekendtgørelse om anvendelse af personlige værnemidler"]:::retsakt
    bek_tekniske_hjaelpemidler_anvendelse["Bekendtgørelse om anvendelse af tekniske hjælpemidler"]:::retsakt
    bek_eksplosiv_atmosfaere["Bekendtgørelse om arbejde i forbindelse med eksplosiv atmosfære"]:::retsakt
    bek_kemiske_agenser["Bekendtgørelse om arbejde med stoffer og materialer (kemiske agenser)"]:::retsakt
    bek_udvinding_mineralske_materialer["Bekendtgørelse om arbejde med udvinding af mineralske materialer"]:::retsakt
    bek_arbejdets_udfoerelse["Bekendtgørelse om arbejdets udførelse"]:::retsakt
    bek_asbest["Bekendtgørelse om asbest i arbejdsmiljøet"]:::retsakt
    bek_vibrationer["Bekendtgørelse om beskyttelse mod udsættelse for vibrationer i forbindelse med arbejdet (ændret ved BEK nr 1882 af 19/12/2023)"]:::retsakt
    bek_biologiske_agenser["Bekendtgørelse om biologiske agenser og arbejdsmiljø (BEK nr 1652 af 19/11/2020 med senere ændringer 2023 og 2024)"]:::retsakt
    bek_bygge_og_anlaeg["Bekendtgørelse om bygge- og anlægsarbejde"]:::retsakt
    bek_bygherrens_pligter["Bekendtgørelse om bygherrens pligter"]:::retsakt
    bek_elektromagnetiske_felter["Bekendtgørelse om eksponering for elektromagnetiske felter i forbindelse med arbejdet (BEK nr 472 af 25/05/2016, ændret ved BEK nr 1883 af 19/12/2023)"]:::retsakt
    bek_faste_arbejdssteder["Bekendtgørelse om faste arbejdssteders indretning"]:::retsakt
    bek_kraeftrisiko["Bekendtgørelse om foranstaltninger til forebyggelse af risikoen ved arbejde med kræftfremkaldende, mutagene eller reproduktionstoksiske stoffer og materialer"]:::retsakt
    bek_amkn_forretningsorden["Bekendtgørelse om forretningsorden for Arbejdsmiljøklagenævnet (2026)"]:::retsakt
    bek_graensevaerdier_kemiske_agenser["Bekendtgørelse om grænseværdier for stoffer og materialer (kemiske agenser) i arbejdsmiljøet"]:::retsakt
    bek_hvileperiode["Bekendtgørelse om hvileperiode og fridøgn m.v."]:::retsakt
    bek_tekniske_hjaelpemidler_indretning["Bekendtgørelse om indretning af tekniske hjælpemidler"]:::retsakt
    bek_elevatorer["Bekendtgørelse om indretning m.v. af elevatorer og sikkerhedskomponenter til elevatorer"]:::retsakt
    bek_eksisterende_elevatorer["Bekendtgørelse om indretningskrav til eksisterende (ikke CE-mærkede) elevatorer (BEK nr 459 af 2016, ændret ved BEK nr 1448 af 2021)"]:::retsakt
    bek_eksplosionsfarlige_omraader["Bekendtgørelse om klassifikation af eksplosionsfarlige områder (BEK nr. 590 af 26/06/2003)"]:::retsakt
    bek_kontrol_risiko_stoerre_uheld["Bekendtgørelse om kontrol med arbejdsmiljøet ved risiko for større uheld med farlige stoffer"]:::retsakt
    bek_offentliggoerelse_arbejdsmiljoe["Bekendtgørelse om offentliggørelse af oplysninger om virksomheders arbejdsmiljø"]:::retsakt
    bek_psykisk_arbejdsmiljoe["Bekendtgørelse om psykisk arbejdsmiljø"]:::retsakt
    bek_skiftende_arbejdssteder["Bekendtgørelse om skiftende arbejdssteders indretning"]:::retsakt
    bek_systematisk_arbejdsmiljoearbejde["Bekendtgørelse om systematisk arbejdsmiljøarbejde"]:::retsakt
    bek_unges_arbejde["Bekendtgørelse om unges arbejde (ungebekendtgørelsen)"]:::retsakt
    lov_1656_2024_arbejdsmarkedsraad["Lov nr. 1656 af 30/12/2024 om ændring af lov om organisering og understøttelse af beskæftigelsesindsatsen m.v., lov om arbejdsmiljø og forskellige andre love (Nedlæggelse af Arbejdsmiljørådet og oprettelse af nyt Arbejdsmarkedsråd)"]:::retsakt
    lov_atp["Lov om Arbejdsmarkedets Tillægspension (ATP-loven)"]:::retsakt
    lov_arbejdsretsloven["Lov om Arbejdsretten og faglige voldgiftsretter (arbejdsretsloven)"]:::retsakt
    lov_ligebehandlingsnaevnet["Lov om Ligebehandlingsnævnet"]:::retsakt
    lov_loenmodtagernes_garantifond["Lov om Lønmodtagernes Garantifond"]:::retsakt
    lov_seniorpensionsenheden["Lov om Seniorpensionsenheden"]:::retsakt
    lov_udbetaling_danmark["Lov om Udbetaling Danmark"]:::retsakt
    lov_aktiv_socialpolitik["Lov om aktiv socialpolitik (aktivloven)"]:::retsakt
    lov_undergrundsloven["Lov om anvendelse af Danmarks undergrund (undergrundsloven), LBK nr 1461 af 29/11/2023"]:::retsakt
    lov_arbejdsloeshedsforsikring["Lov om arbejdsløshedsforsikring m.v. (arbejdsløshedsforsikringsloven)"]:::retsakt
    lov_arbejdsskadesikring["Lov om arbejdsskadesikring (arbejdsskadesikringsloven)"]:::retsakt
    lov_aes["Lov om den selvejende institution Arbejdsmarkedets Erhvervssikring"]:::retsakt
    lov_aktiv_beskaeftigelsesindsats["Lov om en aktiv beskæftigelsesindsats (LAB)"]:::retsakt
    lov_forskelsbehandlingsloven["Lov om forbud mod forskelsbehandling på arbejdsmarkedet m.v. (forskelsbehandlingsloven)"]:::retsakt
    lov_boligstoetteloven["Lov om individuel boligstøtte (boligstøtteloven)"]:::retsakt
    lov_ligebehandlingsloven["Lov om ligebehandling af mænd og kvinder med hensyn til beskæftigelse m.v. (ligebehandlingsloven)"]:::retsakt
    lov_forligsmandsloven["Lov om mægling i arbejdsstridigheder (forligsmandsloven)"]:::retsakt
    lov_organisering_beskaeftigelsesindsatsen["Lov om organisering og understøttelse af beskæftigelsesindsatsen m.v. (LOB)"]:::retsakt
    lov_funktionaerloven["Lov om retsforholdet mellem arbejdsgivere og funktionærer (funktionærloven)"]:::retsakt
    lov_retssikkerhedsloven_social["Lov om retssikkerhed og administration på det sociale område (retssikkerhedsloven)"]:::retsakt
    lov_offshoresikkerhedsloven["Lov om sikkerhed m.v. for offshoreanlæg til efterforskning, produktion og transport af kulbrinter (offshoresikkerhedsloven)"]:::retsakt
    lov_social_pension["Lov om social pension"]:::retsakt
    lov_sygedagpenge["Lov om sygedagpenge (sygedagpengeloven)"]:::retsakt
    cirk_rigsadvokatmeddelelsen_arbejdsmiljoe["Rigsadvokatmeddelelsen, afsnittet om arbejdsmiljø"]:::retsakt
    bek_risiko["Risikobekendtgørelsen (bekendtgørelse om kontrol med risikoen for større uheld med farlige stoffer)"]:::retsakt
    vejl_boligstoette_satser["Satsvejledning for 2026 med bl.a. boligstøtte (VEJ nr. 10077 af 10/11/2025)"]:::retsakt
    min_beskaeftigelse_og_ligestilling -->|delegation| sty_arbejdstilsynet
    bek_eksplosionsfarlige_omraader -->|henviser_til| bek_eksplosiv_atmosfaere
    bek_graensevaerdier_kemiske_agenser -.->|henviser_til| bek_kemiske_agenser
    bek_skiftende_arbejdssteder -->|henviser_til| bek_bygge_og_anlaeg
    bv_bfa_branchevejledninger -->|henviser_til| bek_bygge_og_anlaeg
    bv_bfa_branchevejledninger -.->|henviser_til| kilde_at_dk
    cirk_rigsadvokatmeddelelsen_arbejdsmiljoe -->|henviser_til| lov_arbejdsmiljoeloven
    kilde_ast_principmeddelelser -->|henviser_til| lov_boligstoetteloven
    lov_1656_2024_arbejdsmarkedsraad -->|henviser_til| lov_arbejdsmiljoeloven
    lov_1656_2024_arbejdsmarkedsraad -->|henviser_til| raad_arbejdsmiljoeraadet
    lov_offshoresikkerhedsloven -.->|henviser_til| lov_undergrundsloven
    vejl_at_bygge_og_anlaeg -->|henviser_til| bek_bygge_og_anlaeg
    vejl_at_bygherrens_pligter -->|henviser_til| bek_bygherrens_pligter
    vejl_at_vejledninger -->|henviser_til| lov_arbejdsmiljoeloven
    vejl_boligstoette_satser -->|henviser_til| lov_boligstoetteloven
    bek_at_offshore_opgaver -->|hjemmel_for| sty_arbejdstilsynet
    lov_1656_2024_arbejdsmarkedsraad -->|hjemmel_for| raad_arbejdsmarkedsraadet
    lov_arbejdsmiljoeloven -->|hjemmel_for| bek_amkn_forretningsorden
    lov_arbejdsmiljoeloven -->|hjemmel_for| bek_arbejdets_udfoerelse
    lov_arbejdsmiljoeloven -->|hjemmel_for| bek_asbest
    lov_arbejdsmiljoeloven -.->|hjemmel_for| bek_autoriserede_arbejdsmiljoeraadgivere
    lov_arbejdsmiljoeloven -->|hjemmel_for| bek_biologiske_agenser
    lov_arbejdsmiljoeloven -->|hjemmel_for| bek_bygge_og_anlaeg
    lov_arbejdsmiljoeloven -->|hjemmel_for| bek_bygherrens_pligter
    lov_arbejdsmiljoeloven -->|hjemmel_for| bek_eksisterende_elevatorer
    lov_arbejdsmiljoeloven -->|hjemmel_for| bek_eksplosiv_atmosfaere
    lov_arbejdsmiljoeloven -->|hjemmel_for| bek_elektromagnetiske_felter
    lov_arbejdsmiljoeloven -.->|hjemmel_for| bek_faste_arbejdssteder
    lov_arbejdsmiljoeloven -.->|hjemmel_for| bek_graensevaerdier_kemiske_agenser
    lov_arbejdsmiljoeloven -.->|hjemmel_for| bek_hvileperiode
    lov_arbejdsmiljoeloven -->|hjemmel_for| bek_kemiske_agenser
    lov_arbejdsmiljoeloven -->|hjemmel_for| bek_kontrol_risiko_stoerre_uheld
    lov_arbejdsmiljoeloven -->|hjemmel_for| bek_kraeftrisiko
    lov_arbejdsmiljoeloven -->|hjemmel_for| bek_offentliggoerelse_arbejdsmiljoe
    lov_arbejdsmiljoeloven -.->|hjemmel_for| bek_personlige_vaernemidler
    lov_arbejdsmiljoeloven -->|hjemmel_for| bek_psykisk_arbejdsmiljoe
    lov_arbejdsmiljoeloven -->|hjemmel_for| bek_risiko
    lov_arbejdsmiljoeloven -->|hjemmel_for| bek_skiftende_arbejdssteder
    lov_arbejdsmiljoeloven -->|hjemmel_for| bek_systematisk_arbejdsmiljoearbejde
    lov_arbejdsmiljoeloven -->|hjemmel_for| bek_tekniske_hjaelpemidler_anvendelse
    lov_arbejdsmiljoeloven -->|hjemmel_for| bek_tekniske_hjaelpemidler_indretning
    lov_arbejdsmiljoeloven -.->|hjemmel_for| bek_udvinding_mineralske_materialer
    lov_arbejdsmiljoeloven -->|hjemmel_for| bek_unges_arbejde
    lov_arbejdsmiljoeloven -->|hjemmel_for| bek_vibrationer
    lov_arbejdsmiljoeloven -->|hjemmel_for| naevn_arbejdsmiljoeklagenaevnet
    lov_arbejdsmiljoeloven -->|hjemmel_for| org_autoriserede_arbejdsmiljoeraadgivere
    lov_arbejdsmiljoeloven -->|hjemmel_for| org_bfa_bygge_og_anlaeg
    lov_arbejdsmiljoeloven -->|hjemmel_for| raad_arbejdsmarkedsraadet
    lov_arbejdsmiljoeloven -->|hjemmel_for| raad_arbejdsmiljoeraadet
    lov_arbejdsmiljoeloven -->|hjemmel_for| sty_arbejdstilsynet
    lov_arbejdsmiljoeloven -->|hjemmel_for| sty_erhvervsstyrelsen
    lov_boligstoetteloven -->|hjemmel_for| org_udbetaling_danmark
    lov_offshoresikkerhedsloven -->|hjemmel_for| bek_at_offshore_opgaver
    lov_offshoresikkerhedsloven -->|hjemmel_for| sty_arbejdstilsynet
    bek_asbest -->|implementerer_EU| eu_dir_2009_148
    bek_asbest -->|implementerer_EU| eu_dir_2023_2668
    bek_biologiske_agenser -->|implementerer_EU| eu_dir_2000_54
    bek_bygge_og_anlaeg -->|implementerer_EU| eu_dir_1992_57
    bek_bygherrens_pligter -->|implementerer_EU| eu_dir_1992_57
    bek_eksplosiv_atmosfaere -->|implementerer_EU| eu_dir_1999_92
    bek_elektromagnetiske_felter -->|implementerer_EU| eu_dir_2013_35
    bek_faste_arbejdssteder -->|implementerer_EU| eu_dir_1989_654
    bek_graensevaerdier_kemiske_agenser -.->|implementerer_EU| eu_dir_1998_24
    bek_graensevaerdier_kemiske_agenser -.->|implementerer_EU| eu_dir_2004_37
    bek_hvileperiode -.->|implementerer_EU| eu_dir_2003_88
    bek_kemiske_agenser -.->|implementerer_EU| eu_dir_1998_24
    bek_kontrol_risiko_stoerre_uheld -->|implementerer_EU| eu_dir_2012_18
    bek_kraeftrisiko -->|implementerer_EU| eu_dir_2004_37
    bek_systematisk_arbejdsmiljoearbejde -->|implementerer_EU| eu_dir_1989_391
    bek_tekniske_hjaelpemidler_anvendelse -->|implementerer_EU| eu_dir_2009_104
    bek_unges_arbejde -->|implementerer_EU| eu_dir_1994_33
    bek_vibrationer -.->|implementerer_EU| eu_dir_2002_44
    lov_arbejdsmiljoeloven -->|implementerer_EU| eu_dir_1989_391
    lov_offshoresikkerhedsloven -->|implementerer_EU| eu_dir_2013_30
    dom_domstolene -->|klageinstans| naevn_arbejdsmiljoeklagenaevnet
    naevn_arbejdsmiljoeklagenaevnet -->|klageinstans| sty_arbejdstilsynet
    sty_ankestyrelsen -->|klageinstans| org_udbetaling_danmark
    min_beskaeftigelse_og_ligestilling -->|ressortansvar| lov_arbejdsmiljoeloven
    min_beskaeftigelse_og_ligestilling -->|ressortansvar| lov_boligstoetteloven
    min_beskaeftigelse_og_ligestilling -->|ressortansvar| lov_offshoresikkerhedsloven
    min_beskaeftigelse_og_ligestilling -->|ressortansvar| naevn_arbejdsmiljoeklagenaevnet
    min_beskaeftigelse_og_ligestilling -->|ressortansvar| org_nfa
    min_beskaeftigelse_og_ligestilling -->|ressortansvar| org_udbetaling_danmark
    min_beskaeftigelse_og_ligestilling -->|ressortansvar| raad_arbejdsmarkedsraadet
    min_beskaeftigelse_og_ligestilling -->|ressortansvar| raad_arbejdsmiljoeraadet
    min_beskaeftigelse_og_ligestilling -->|ressortansvar| sty_arbejdstilsynet
    ombud_folketingets_ombudsmand -.->|tilsyn| naevn_arbejdsmiljoeklagenaevnet
    ombud_folketingets_ombudsmand -->|tilsyn| org_udbetaling_danmark
    ombud_folketingets_ombudsmand -.->|tilsyn| sty_arbejdstilsynet
    sty_arbejdstilsynet -->|tilsyn| eu_dir_2006_42
    sty_arbejdstilsynet -->|tilsyn| eu_reg_2006_1907
    sty_arbejdstilsynet -->|tilsyn| org_autoriserede_arbejdsmiljoeraadgivere
    min_beskaeftigelse_og_ligestilling -->|udsteder| bek_amkn_forretningsorden
    min_beskaeftigelse_og_ligestilling -->|udsteder| vejl_boligstoette_satser
    naevn_arbejdsmiljoeklagenaevnet -->|udsteder| kilde_ast_amkn
    sty_arbejdstilsynet -->|udsteder| bek_arbejdets_udfoerelse
    sty_arbejdstilsynet -->|udsteder| bek_asbest
    sty_arbejdstilsynet -.->|udsteder| bek_autoriserede_arbejdsmiljoeraadgivere
    sty_arbejdstilsynet -.->|udsteder| bek_biologiske_agenser
    sty_arbejdstilsynet -->|udsteder| bek_bygge_og_anlaeg
    sty_arbejdstilsynet -->|udsteder| bek_bygherrens_pligter
    sty_arbejdstilsynet -.->|udsteder| bek_eksisterende_elevatorer
    sty_arbejdstilsynet -->|udsteder| bek_eksplosiv_atmosfaere
    sty_arbejdstilsynet -.->|udsteder| bek_elektromagnetiske_felter
    sty_arbejdstilsynet -.->|udsteder| bek_elevatorer
    sty_arbejdstilsynet -->|udsteder| bek_faste_arbejdssteder
    sty_arbejdstilsynet -.->|udsteder| bek_graensevaerdier_kemiske_agenser
    sty_arbejdstilsynet -.->|udsteder| bek_kemiske_agenser
    sty_arbejdstilsynet -->|udsteder| bek_kontrol_risiko_stoerre_uheld
    sty_arbejdstilsynet -->|udsteder| bek_kraeftrisiko
    sty_arbejdstilsynet -.->|udsteder| bek_offentliggoerelse_arbejdsmiljoe
    sty_arbejdstilsynet -.->|udsteder| bek_personlige_vaernemidler
    sty_arbejdstilsynet -->|udsteder| bek_psykisk_arbejdsmiljoe
    sty_arbejdstilsynet -.->|udsteder| bek_skiftende_arbejdssteder
    sty_arbejdstilsynet -->|udsteder| bek_systematisk_arbejdsmiljoearbejde
    sty_arbejdstilsynet -.->|udsteder| bek_tekniske_hjaelpemidler_anvendelse
    sty_arbejdstilsynet -->|udsteder| bek_tekniske_hjaelpemidler_indretning
    sty_arbejdstilsynet -->|udsteder| bek_udvinding_mineralske_materialer
    sty_arbejdstilsynet -.->|udsteder| bek_unges_arbejde
    sty_arbejdstilsynet -->|udsteder| bek_vibrationer
    sty_arbejdstilsynet -->|udsteder| kilde_at_dk
    sty_arbejdstilsynet -.->|udsteder| kilde_regler_at_dk
    sty_arbejdstilsynet -->|udsteder| vejl_at_bygge_og_anlaeg
    sty_arbejdstilsynet -->|udsteder| vejl_at_bygherrens_pligter
    sty_arbejdstilsynet -->|udsteder| vejl_at_vejledninger
    min_beskaeftigelse_og_ligestilling -->|ressortansvar| sty_star
    min_beskaeftigelse_og_ligestilling -->|ressortansvar| lov_arbejdsloeshedsforsikring
    min_beskaeftigelse_og_ligestilling -->|ressortansvar| lov_aktiv_socialpolitik
    min_beskaeftigelse_og_ligestilling -->|ressortansvar| lov_seniorpensionsenheden
    min_beskaeftigelse_og_ligestilling -.->|ressortansvar| org_seniorpensionsenheden
    lov_arbejdsloeshedsforsikring -.->|hjemmel_for| sty_star
    lov_arbejdsloeshedsforsikring -->|hjemmel_for| org_a_kasser
    lov_seniorpensionsenheden -->|hjemmel_for| org_seniorpensionsenheden
    lov_seniorpensionsenheden -->|henviser_til| lov_retssikkerhedsloven_social
    sty_star -.->|tilsyn| org_a_kasser
    sty_star -.->|klageinstans| org_a_kasser
    sty_ankestyrelsen -->|klageinstans| sty_star
    sty_ankestyrelsen -->|klageinstans| org_seniorpensionsenheden
    min_beskaeftigelse_og_ligestilling -->|ressortansvar| lov_aktiv_beskaeftigelsesindsats
    min_beskaeftigelse_og_ligestilling -->|ressortansvar| lov_organisering_beskaeftigelsesindsatsen
    min_beskaeftigelse_og_ligestilling -->|ressortansvar| lov_sygedagpenge
    min_beskaeftigelse_og_ligestilling -->|ressortansvar| lov_social_pension
    min_beskaeftigelse_og_ligestilling -->|ressortansvar| lov_udbetaling_danmark
    min_beskaeftigelse_og_ligestilling -->|ressortansvar| lov_arbejdsskadesikring
    min_beskaeftigelse_og_ligestilling -->|ressortansvar| lov_aes
    min_beskaeftigelse_og_ligestilling -->|ressortansvar| lov_loenmodtagernes_garantifond
    min_beskaeftigelse_og_ligestilling -->|ressortansvar| lov_atp
    min_beskaeftigelse_og_ligestilling -.->|ressortansvar| org_arbejdsmarkedets_erhvervssikring
    min_beskaeftigelse_og_ligestilling -.->|ressortansvar| fond_loenmodtagernes_garantifond
    min_beskaeftigelse_og_ligestilling -->|ressortansvar| org_atp
    min_beskaeftigelse_og_ligestilling -->|ressortansvar| naevn_ankenaevn_atp
    min_beskaeftigelse_og_ligestilling -.->|ressortansvar| raad_tilsynsraadet
    lov_arbejdsskadesikring -->|hjemmel_for| org_arbejdsmarkedets_erhvervssikring
    lov_aes -->|hjemmel_for| org_arbejdsmarkedets_erhvervssikring
    lov_loenmodtagernes_garantifond -->|hjemmel_for| fond_loenmodtagernes_garantifond
    lov_atp -->|hjemmel_for| org_atp
    lov_atp -->|hjemmel_for| naevn_ankenaevn_atp
    lov_organisering_beskaeftigelsesindsatsen -->|hjemmel_for| raad_tilsynsraadet
    lov_social_pension -->|hjemmel_for| org_seniorpensionsenheden
    lov_aktiv_beskaeftigelsesindsats -->|henviser_til| lov_retssikkerhedsloven_social
    lov_sygedagpenge -->|henviser_til| lov_retssikkerhedsloven_social
    lov_udbetaling_danmark -->|henviser_til| lov_retssikkerhedsloven_social
    lov_arbejdsskadesikring -->|henviser_til| lov_atp
    lov_loenmodtagernes_garantifond -.->|henviser_til| lov_atp
    sty_ankestyrelsen -.->|klageinstans| org_arbejdsmarkedets_erhvervssikring
    naevn_ankenaevn_atp -->|klageinstans| org_atp
    naevn_ankenaevn_atp -.->|klageinstans| fond_loenmodtagernes_garantifond
    naevn_ankenaevn_atp -->|klageinstans| org_arbejdsmarkedets_erhvervssikring
    sty_star -->|tilsyn| kommune_alle
    sty_star -->|udsteder| kilde_star_love_og_regler
    org_arbejdsmarkedets_erhvervssikring -->|udsteder| kilde_aes_love_og_praksis
    min_beskaeftigelse_og_ligestilling -->|ressortansvar| lov_arbejdsretsloven
    min_beskaeftigelse_og_ligestilling -->|ressortansvar| lov_forligsmandsloven
    min_beskaeftigelse_og_ligestilling -->|ressortansvar| lov_ligebehandlingsnaevnet
    min_beskaeftigelse_og_ligestilling -->|ressortansvar| lov_ligebehandlingsloven
    min_beskaeftigelse_og_ligestilling -->|ressortansvar| lov_forskelsbehandlingsloven
    min_beskaeftigelse_og_ligestilling -->|ressortansvar| lov_funktionaerloven
    lov_arbejdsretsloven -->|hjemmel_for| dom_arbejdsretten
    lov_arbejdsretsloven -->|hjemmel_for| org_faglige_voldgiftsretter
    lov_forligsmandsloven -.->|hjemmel_for| sty_forligsinstitutionen
    lov_ligebehandlingsnaevnet -.->|hjemmel_for| naevn_ligebehandlingsnaevnet
    lov_ligebehandlingsnaevnet -->|henviser_til| lov_ligebehandlingsloven
    lov_ligebehandlingsnaevnet -->|henviser_til| lov_forskelsbehandlingsloven
    bek_arbejdets_udfoerelse -->|implementerer_EU| eu_dir_1989_391
    bek_at_offshore_opgaver -->|implementerer_EU| eu_dir_2013_30
    bek_eksisterende_elevatorer -->|implementerer_EU| eu_dir_2015_1535
    bek_psykisk_arbejdsmiljoe -->|implementerer_EU| eu_dir_1989_391
    bek_tekniske_hjaelpemidler_indretning -->|implementerer_EU| eu_dir_2009_104
    lov_arbejdsmiljoeloven -->|hjemmel_for| vejl_at_bygherrens_pligter
    lov_arbejdsmiljoeloven -->|implementerer_EU| eu_dir_1992_57
    lov_arbejdsmiljoeloven -->|implementerer_EU| eu_dir_1994_33
    lov_arbejdsmiljoeloven -->|implementerer_EU| eu_dir_2003_88
    lov_arbejdsmiljoeloven -->|implementerer_EU| eu_dir_2005_36
    lov_arbejdsmiljoeloven -->|implementerer_EU| eu_dir_2009_104
    lov_arbejdsmiljoeloven -->|implementerer_EU| eu_dir_2009_148
    lov_arbejdsmiljoeloven -->|hjemmel_for| vejl_at_bygge_og_anlaeg
    lov_offshoresikkerhedsloven -->|implementerer_EU| eu_dir_1989_391
    lov_offshoresikkerhedsloven -->|implementerer_EU| eu_dir_2003_88
    lov_offshoresikkerhedsloven -->|implementerer_EU| eu_dir_2005_36
    lov_offshoresikkerhedsloven -->|implementerer_EU| eu_dir_2006_42
    bek_elevatorer -->|implementerer_EU| eu_dir_2014_33
    bek_risiko -->|implementerer_EU| eu_dir_2012_18
```

[← Overblik](oversigt.md)
