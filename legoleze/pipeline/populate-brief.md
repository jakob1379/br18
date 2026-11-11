# Brief til research-agenter (fase 7: udfyldning af mangler)

Du udvider et registry over danske myndigheder og retskilder: en graf, der skal bære et juridisk RAG-korpus, hvor søgning kan følge kæden lov → bekendtgørelse → vejledning → praksis. Registry'et ligger i `legoleze/dk-regulering/registry.yaml`. Det dækker byggeri, bolig, plan, energi, miljø, arbejdsmiljø, brand og el/gas/VVS i dybden og instanslaget for de retsområder, der er tilføjet siden (se `legoleze/dk-regulering/README.md`). Du får ét retsområde, som mangler.

Arbejdsmappe: `/home/jsg/.t3/worktrees/br18/t3-470b1547-0552d078007abcb8`. Dags dato er 2026-11-11. Skriv alle tekstværdier på dansk.

## Opgaven

Kortlæg instanslaget for dit område:

1. **Myndighederne**: styrelser, tilsyn, råd og nævn, der udsteder, fortolker eller håndhæver reguleringen. Aktive pr. i dag; tidligere navne og fusioner med periode.
2. **Klagekæden**: hvem behandler klager over hvem, med lov og paragraf, og om afgørelsen er endelig eller kan gå videre.
3. **Tilsyn**: hvem fører tilsyn med hvem.
4. **Hjemmelslovene**: de love, der opretter instanserne eller fastlægger klage- og tilsynsvejen, med gældende lovbekendtgørelse.
5. **Dokumentkilderne**: hvor afgørelser, praksis og vejledninger offentliggøres (databaser, samlinger), med adgangsform, vilkår og nummersystem.

Sigt efter de 8–20 vigtigste instanser, de 3–10 love, der bærer kæden, og de 3–8 vigtigste dokumentkilder. En komplet kæde er vigtigere end mange noder.

## Det, der findes i forvejen

Genbrug eksisterende noder som endepunkter i kanter; opret dem ikke igen. Se alle id'er med type, navn og ministerium:

    awk '/^- id: /{id=$3} /^  navn: /{sub(/^  navn: /,""); navn=$0} /^  type: /{type=$2} /^  ministerium: /{print id" | "type" | "navn" | "$2}' legoleze/dk-regulering/registry.yaml | grep -i <søgeord>

Ministerier (brug præcis disse id'er i `ministerium`, eller `ingen` for instanser uden for ministerierne):

    min-beskaeftigelse-og-ligestilling  Beskæftigelses- og Ligestillingsministeriet
    min-boern-aeldre-og-bolig           Børne-, Ældre- og Boligministeriet
    min-by-land-og-transport            By-, Land- og Transportministeriet
    min-erhverv                         Erhvervsministeriet
    min-finans                          Finansministeriet
    min-forskning-uddannelse-og-digitalisering  Forsknings-, Uddannelses- og Digitaliseringsministeriet
    min-forsvar                         Forsvarsministeriet
    min-justits                         Justitsministeriet
    min-klima-energi-og-forsyning       Klima-, Energi- og Forsyningsministeriet
    min-kultur                          Kulturministeriet
    min-miljoe                          Miljøministeriet
    min-natur-og-dyrevelfaerd           Ministeriet for Natur og Dyrevelfærd
    min-oekonomi-og-indenrigs           Økonomi- og Indenrigsministeriet
    min-samfundssikkerhed-og-beredskab  Ministeriet for Samfundssikkerhed og Beredskab
    min-skat-og-vaekst                  Skatte- og Vækstministeriet
    min-social                          Socialministeriet
    min-statsministeriet                Statsministeriet
    min-sundhed-og-kirke                Sundheds- og Kirkeministeriet
    min-udenrigs                        Udenrigsministeriet
    min-udlaendinge-og-integration      Udlændinge- og Integrationsministeriet
    min-undervisning                    Undervisningsministeriet

Tværgående noder, du ofte får brug for: `sty-ankestyrelsen`, `sty-naevnenes-hus`, `naevn-erhvervsankenaevnet`, `ombud-folketingets-ombudsmand`, `dom-domstolene`, `dom-byretterne`, `dom-landsretterne`, `dom-hoejesteret`, `naevn-procesbevillingsnaevnet`, `sty-rigsadvokaten`, `sty-civilstyrelsen`, `kilde-retsinformation`, `kilde-domsdatabasen`, `kilde-fob-database`, `kilde-eurlex`, `eu-domstolen`, `eu-kommissionen`, `kommune-alle`, `region-alle`.

**Regeringen skiftede 3. juni 2026, og flere ministerier blev omdøbt eller fik nye områder.** Din viden om ministerienavne er derfor forældet. Bekræft hver instans' nuværende ministerium på en officiel side (ministeriets organisationsside, instansens "om os"-side eller et dokument fra 2026 på Retsinformation), og citér den. Bruger de officielle sider stadig et ældre ministerienavn, så skriv det i `note`, og brug det ministerium, der har området i dag.

## Kilder

- **Lokalt katalog (gratis, uden web):** `legoleze/dk-regulering/katalog/retsinformation_lta.jsonl` har én JSON-linje pr. dokument i Lovtidende A til og med 12/2/2026. Find gældende lovbekendtgørelse sådan:

      grep -i '"navn":"Bekendtgørelse af skatteforvaltningsloven' legoleze/dk-regulering/katalog/retsinformation_lta.jsonl | jq -c '{id,navn,type,status:.status.vaerdi,udstedt:.datoer.udstedt,gv:.gaeldende_version,eli:.kilder[0]}'

  Status er fra juni 2026, så der kan være kommet en nyere version. Bekræft på Retsinformation, at dokumentet stadig er gældende (`<Status>Valid</Status>` i XML'en).
- **Web:** Brug WebSearch til at finde sider og WebFetch til at læse dem (indlæs dem med ToolSearch `select:WebSearch,WebFetch`, hvis de ikke er tilgængelige). Bed WebFetch om at gengive passagen "ordret, uden omskrivning".
- **Retsinformation:** ELI-siden (`https://www.retsinformation.dk/eli/lta/<år>/<nr>`) er en JavaScript-skal uden tekst. Læs teksten på samme adresse med `/xml` bagefter. Lange dokumenter kommer i stykker på 100.000 tegn; læs videre med `offset`. Vent cirka 10 sekunder mellem forskellige dokumenter, og åbn højst cirka 15.
- **Budget:** højst cirka 25 WebSearch-kald (de er en delt, begrænset ressource). Brug hellere WebFetch på officielle sider, du allerede kender.

## Belæg: den regel, der betyder mest

Hver påstand har `belaeg`: en liste af `{"url": ..., "citat": ...}`, hvor `citat` er en ordret passage på 20–600 tegn fra netop den side, som bærer påstanden.

Når du er færdig, henter orkestratoren hver URL og leder efter citatet. Et citat, der ikke står på siden, tæller som intet belæg, og påstanden nedgraderes. En død URL udgår. Derfor:

- Konstruér eller gæt aldrig en URL. Brug kun adresser, du selv har åbnet.
- Omskriv aldrig et citat. Kopiér ordlyden.
- Citatet skal bære påstandens kerne. En uafhængig kontrollant læser kun påstand og citat og sænker sikkerheden, hvis citatet ikke viser det, du hævder. Derfor:
  - Er en paragraf pointen, så tag paragrafnummeret med i citatet (fx "§ 372. Afgørelser truffet af Finanstilsynet … kan indbringes for Erhvervsankenævnet").
  - Giv ét citat pr. detalje, du skriver i `tekst` eller `beskrivelse` (frist, endelighed, hvem der kan klage). Skriv ikke detaljer, du ikke citerer.
  - En `url` belægges med et citat fra selve siden (samme domæne), hvor instansen eller kilden præsenterer sig selv. En liste af navne på en anden side beviser ikke adressen.
  - En `ressortansvar`-kant belægges med en side, der siger, at instansen eller loven hører under ministeriet. En lovtekst, der nævner en minister, gør det ikke alene.
- Citér den officielle kilde, hvor den findes: retsinformation.dk, instansens egen side, ft.dk eller eur-lex. Sekundære sider (Lovguiden, lex.dk, Wikipedia, danskelove.dk) tæller kun halvt.
- For dokumenter på Retsinformation citerer du ELI-adressen uden `/xml`; kontrollen læser selv XML'en.
- Kan du ikke finde belæg, så udelad påstanden, og skriv den under `huller` (type `ikke-fundet` eller `uklart`). Gæt ikke.

Du sætter ikke selv sikkerhed. Den beregnes af kontrollen.

## Output

Skriv én JSON-fil til `legoleze/raw/populate/2026-11-11-<omraade>.json`, og kør så:

    python3 legoleze/pipeline/populate.py check legoleze/raw/populate/2026-11-11-<omraade>.json

Ret, indtil den skriver `OK`. Redigér ingen andre filer.

```json
{
  "omraade": "eksempel",
  "noder": [
    {
      "id": "sty-eksempelstyrelsen",
      "navn": "Eksempelstyrelsen",
      "type": "styrelse",
      "ministerium": "min-erhverv",
      "status": "aktiv",
      "tidligere_navne": [
        {"navn": "Direktoratet for Eksempler", "periode": "1998–31/12/2017",
         "belaeg": [{"url": "https://eksempelstyrelsen.dk/om-os/historie", "citat": "Direktoratet for Eksempler skiftede den 1. januar 2018 navn til Eksempelstyrelsen"}]}
      ],
      "hjemmel": {"tekst": "Eksempellovens § 3: styrelsen træffer afgørelser efter loven og fører tilsyn med ...",
                  "belaeg": [{"url": "https://www.retsinformation.dk/eli/lta/2024/123", "citat": "Eksempelstyrelsen træffer afgørelse efter denne lov og fører tilsyn med overholdelsen"}]},
      "dokumenttyper": {"liste": [{"type": "afgørelse", "bindende": "bindende"}, {"type": "vejledning", "bindende": "vejledende", "note": "udgives på Retsinformation som VEJ"}],
                        "belaeg": [{"url": "https://eksempelstyrelsen.dk/afgoerelser", "citat": "Her finder du styrelsens afgørelser og vejledninger"}]},
      "url": {"vaerdi": "https://eksempelstyrelsen.dk/", "belaeg": [{"url": "https://eksempelstyrelsen.dk/om-os", "citat": "Eksempelstyrelsen er en styrelse under Erhvervsministeriet"}]},
      "krydsref_moenstre": ["Eksempelstyrelsens afgørelse af [dato]", "j.nr. ÅÅÅÅ-NNNN"],
      "note": "Kort faglig note: hvad instansen gør i kæden, og hvad der er usikkert."
    },
    {
      "id": "lov-eksempelloven",
      "navn": "Eksempelloven",
      "type": "lov",
      "ministerium": "min-erhverv",
      "status": "aktiv",
      "hjemmel": {"tekst": "ikke relevant", "belaeg": [{"url": "https://www.retsinformation.dk/eli/lta/2024/123", "citat": "Bekendtgørelse af lov om eksempler"}]},
      "url": {"vaerdi": "https://www.retsinformation.dk/eli/lta/2024/123", "belaeg": [{"url": "https://www.retsinformation.dk/eli/lta/2024/123", "citat": "Bekendtgørelse af lov om eksempler"}]},
      "identifikatorer": {"eli": "https://www.retsinformation.dk/eli/lta/2024/123", "lovtidende": "LBK nr. 123 af 01/02/2024",
                          "belaeg": [{"url": "https://www.retsinformation.dk/eli/lta/2024/123", "citat": "Herved bekendtgøres lov om eksempler, jf. lovbekendtgørelse nr. 99 af 2. januar 2020"}]}
    },
    {
      "id": "kilde-eksempel-afgoerelser",
      "navn": "Eksempelstyrelsens afgørelsesdatabase",
      "type": "dokumentkilde",
      "ministerium": "min-erhverv",
      "status": "aktiv",
      "url": {"vaerdi": "https://eksempelstyrelsen.dk/afgoerelser", "belaeg": [{"url": "https://eksempelstyrelsen.dk/afgoerelser", "citat": "Søg i styrelsens offentliggjorte afgørelser fra 2015 og frem"}]},
      "adgang": {"vaerdier": ["HTML", "PDF"], "note": "Søgeside uden API; hver afgørelse er en PDF.",
                 "belaeg": [{"url": "https://eksempelstyrelsen.dk/afgoerelser", "citat": "Søg i styrelsens offentliggjorte afgørelser fra 2015 og frem"}]},
      "identifikatorer": {"andet": "Afgørelser nummereres ES-ÅÅÅÅ-NNN.", "belaeg": [{"url": "https://eksempelstyrelsen.dk/afgoerelser/es-2024-017", "citat": "Afgørelse ES-2024-017 af 3. marts 2024"}]},
      "opdatering": {"frekvens": "løbende", "versionshistorik": "afgørelser fra 2015 og frem",
                     "belaeg": [{"url": "https://eksempelstyrelsen.dk/afgoerelser", "citat": "Søg i styrelsens offentliggjorte afgørelser fra 2015 og frem"}]},
      "ingest": {"vaerdi": 4, "besvaer": 3, "begrundelse": "Eneste samlede praksiskilde på området; PDF uden API."}
    }
  ],
  "kanter": [
    {"from": "min-erhverv", "type": "ressortansvar", "to": "sty-eksempelstyrelsen", "beskrivelse": "Styrelse under Erhvervsministeriet.",
     "belaeg": [{"url": "https://eksempelstyrelsen.dk/om-os", "citat": "Eksempelstyrelsen er en styrelse under Erhvervsministeriet"}]},
    {"from": "min-erhverv", "type": "ressortansvar", "to": "lov-eksempelloven", "beskrivelse": "Loven hører under erhvervsministeren.",
     "belaeg": [{"url": "https://www.retsinformation.dk/eli/lta/2024/123", "citat": "Erhvervsministeren fastsætter nærmere regler om"}]},
    {"from": "lov-eksempelloven", "type": "hjemmel_for", "to": "sty-eksempelstyrelsen", "beskrivelse": "§ 3 giver styrelsen afgørelses- og tilsynskompetencen.",
     "belaeg": [{"url": "https://www.retsinformation.dk/eli/lta/2024/123", "citat": "Eksempelstyrelsen træffer afgørelse efter denne lov og fører tilsyn med overholdelsen"}]},
    {"from": "naevn-erhvervsankenaevnet", "type": "klageinstans", "to": "sty-eksempelstyrelsen", "beskrivelse": "Eksempellovens § 40: klage inden 4 uger; nævnets afgørelse er endelig administrativt.",
     "belaeg": [{"url": "https://www.retsinformation.dk/eli/lta/2024/123", "citat": "Afgørelser truffet af Eksempelstyrelsen kan indbringes for Erhvervsankenævnet senest 4 uger efter"}]},
    {"from": "sty-eksempelstyrelsen", "type": "udsteder", "to": "kilde-eksempel-afgoerelser", "beskrivelse": "Styrelsen driver databasen.",
     "belaeg": [{"url": "https://eksempelstyrelsen.dk/afgoerelser", "citat": "Søg i styrelsens offentliggjorte afgørelser fra 2015 og frem"}]}
  ],
  "rettelser": [
    {"id": "naevn-erhvervsankenaevnet", "felt": "url", "vaerdi": "https://naevneneshus.dk/start-din-klage/erhvervsankenaevnet/",
     "belaeg": [{"url": "https://naevneneshus.dk/start-din-klage/erhvervsankenaevnet/", "citat": "Erhvervsankenævnet behandler klager over afgørelser truffet af Erhvervsstyrelsen og Finanstilsynet"}]}
  ],
  "huller": [
    {"emne": "Eksempelstyrelsens ældre afgørelser", "type": "ikke-fundet", "beskrivelse": "Afgørelser fra før 2015 er ikke fundet online.",
     "noder": ["kilde-eksempel-afgoerelser"], "kilder": ["https://eksempelstyrelsen.dk/afgoerelser"]}
  ],
  "noter": "Til orkestratoren: hvad du ikke nåede, og hvad der ser forkert ud i eksisterende noder, men som du ikke har belæg til at rette."
}
```

Alle værdier, adresser og citater i eksemplet er opdigtede, også rettelsen. Kopiér intet derfra.

`rettelser` ændrer ét påstandsfelt på en node, der findes i forvejen: `id`, `felt` og feltets værdinøgler som for en ny node, plus `belaeg`. En rettelse afvises, hvis dens sikkerhed bliver lavere end den eksisterende.

### Felter

- **Node:** `id`, `navn`, `type`, `ministerium`, `status` er påkrævet. Derudover de påstandsfelter, du har belæg for: `hjemmel` (`tekst`), `dokumenttyper` (`liste` af `{type, bindende, note}`), `url` (`vaerdi`), `adgang` (`vaerdier`, `note`), `identifikatorer` (`eli`, `lovtidende`, `celex`, `journalnr`, `andet`), `licens` (`tekst`), `opdatering` (`frekvens`, `versionshistorik`). Hvert påstandsfelt skal have `belaeg`; udelad feltet, hvis du ikke har belæg. Frie felter: `tidligere_navne`, `krydsref_moenstre` (typiske henvisningsmønstre i tekst, brugbare som regex), `ingest` (`vaerdi` og `besvaer` 1–5 samt `begrundelse`), `note`, `domaener`.
- **Love og bekendtgørelser:** giv `url`, `identifikatorer` og `hjemmel` (for love: `ikke relevant`; for bekendtgørelser: hjemmelsbestemmelsen). `adgang`, `licens` og `opdatering` udfyldes automatisk for dokumenter på Retsinformation.
- **type:** instanser: `styrelse`, `direktorat`, `nævn`, `klagenævn`, `tilsyn`, `råd`, `fond`, `domstol`, `ombudsmand`, `offentlig-virksomhed`, `eu-institution`, `privat-organisation`. Dokumenter: `dokumentkilde`, `lov`, `bekendtgørelse`, `cirkulære`, `vejledning`, `praksissamling`, `eu-direktiv`, `eu-forordning`, `eu-afgørelse`.
- **status:** `aktiv`, `nedlagt`, `omdøbt`, `ophævet`, `ukendt`.
- **adgang.vaerdier:** `API`, `bulk`, `ELI`, `RSS`, `HTML`, `PDF`, `betalingsmur`, `ukendt`, `ikke-relevant`.
- **bindende:** `bindende`, `vejledende`, `blandet`, `ukendt`.
- **huller.type:** `betalingsmur`, `kun-pdf`, `ingen-api`, `uklart`, `ikke-fundet`, `andet`.

### Id'er

`sty-` styrelser og direktorater · `naevn-` nævn og klagenævn · `tilsyn-` tilsyn · `raad-` råd · `fond-` fonde · `dom-` domstole · `org-` øvrige organisationer · `lov-<kortnavn>` love (én node pr. lov; identifikatorerne peger på gældende lovbekendtgørelse) · `bek-` bekendtgørelser · `vejl-` vejledninger · `cirk-` cirkulærer · `kilde-` dokumentkilder · `eu-dir-ÅÅÅÅ-N`, `eu-reg-ÅÅÅÅ-N` EU-retsakter (højst 5, og kun når kæden kræver dem). Kun små bogstaver, cifre og bindestreger; æ→ae, ø→oe, å→aa.

### Kanter

`from` er altid den aktive part. Kun disse typer:

| Type | Retning |
|------|---------|
| `ressortansvar` | ministerium → instans eller lov |
| `delegation` | ministerium/styrelse → styrelse/kommune (delegationsbekendtgørelsen i `beskrivelse`) |
| `hjemmel_for` | lov/bekendtgørelse → bekendtgørelse/vejledning/instans |
| `udsteder` | instans → retsakt/vejledning/dokumentkilde (udsteder, udgiver eller driver) |
| `klageinstans` | klageinstans → førsteinstans (`from` behandler klager over `to`'s afgørelser; lov og § i `beskrivelse`) |
| `tilsyn` | tilsynsmyndighed → tilsynsobjekt |
| `implementerer_EU` | dansk retsakt → EU-retsakt |
| `henviser_til` | dokument → dokument |

Hver instans og hver lov skal have en `ressortansvar`-kant fra sit ministerium (medmindre `ministerium` er `ingen`), og hver ny node skal have mindst én kant.

Endepunkterne kontrolleres. Instans betyder en nodetype fra instanslisten, dokument en fra dokumentlisten: `klageinstans` og `delegation` går fra instans til instans, `udsteder` fra instans til dokument, `hjemmel_for` fra dokument, `tilsyn` fra instans, og `henviser_til` og `implementerer_EU` fra dokument til dokument. Passer en relation ikke i en type (fx at en instans er sekretariat for en anden, eller indbringer sager for et nævn), så skriv den i `note`, ikke som kant.

## Afslutning

Svar med 5–10 linjer: hvad du tilføjede (antal noder, kanter, huller), hvad du ikke kunne finde, hvad der ser forkert ud i det eksisterende registry (med id), og hvor mange WebSearch-kald du brugte.

# Brief til kontrollanten

Du er uafhængig kontrollant. Hent ingen websider, og start ingen agenter. Læs `legoleze/raw/populate/<dato>-<omraade>.review.json`: en liste af påstande med `hvor` (nøgle, gengives uændret), `paastand` og `belaeg` (`{url, citat}`). Citaterne er allerede genfundet maskinelt på siderne. Din eneste opgave er at bedømme, om citaterne bærer påstanden. Brug kun det, der står i filen, og almindelig sprogforståelse; godkend ikke noget på din egen viden om dansk ret.

- `baerer`: citaterne siger direkte det, påstanden hævder, inklusive kernen (hvem, hvilken relation, og paragraf eller frist, når det er pointen).
- `delvist`: citaterne handler om det samme, men fastslår ikke kernen: en navneliste som bevis for en adresse, en instans nævnt uden relationen, forkert retning, en anden paragraf, eller centrale detaljer, som ikke fremgår.
- `baerer-ikke`: citaterne er irrelevante for påstanden eller modsiger den.

Kanter har formen `A —type→ B: beskrivelse` med retningen fra tabellen ovenfor. Feltpåstande har formen `Navn (type, ministerium …): felt = {værdi}`. Bedøm kernen, ikke hver bisætning. `hjemmel = "ikke relevant"` for en lov bæres af ethvert citat, der viser, at dokumentet er loven.

Skriv `legoleze/raw/populate/<dato>-<omraade>.dom.json`: en JSON-liste med ét objekt pr. påstand i samme rækkefølge, `{"hvor": …, "dom": "baerer" | "delvist" | "baerer-ikke", "grund": "<højst 20 ord; tom ved baerer>"}`. Svar til sidst med antal pr. dom og de vigtigste problemer.

# Orkestratorens forløb

    python3 legoleze/pipeline/populate.py check  FUND.json            # research-agenten har kørt den; kør den igen
    python3 legoleze/pipeline/populate.py review FUND.json > FUND.review.json   # til kontrollanten (Haiku, effort high), som skriver FUND.dom.json
    python3 legoleze/pipeline/populate.py hosts  FUND.json...         # værter til netværkstilladelsen
    uv run --no-project --with pyyaml python legoleze/pipeline/populate.py apply FUND.json...
    uv run --no-project --with pyyaml bash legoleze/pipeline/views.sh  # README, views, final.json og kortet

Læs kontrollantens indvendinger mod kanterne, før du fletter: en forkert typet kant er værre end en manglende, og den fjernes fra fundet med en note. `git checkout` må ikke bruges på LFS-filerne (`intermediate/`, `reguleringskort.html`, `*.jsonl`) uden `git-lfs` på stien; uden filteret sletter den dem i arbejdstræet.
