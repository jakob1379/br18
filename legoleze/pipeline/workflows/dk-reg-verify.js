export const meta = {
  name: 'dk-reg-verify',
  description: 'Adversariel verifikation med reelt søgebudget pr. domæne; returnerer patch til registry',
  phases: [{ title: 'Verify', detail: 'én verifikator+konsolidator pr. domæne' }],
}

const BASELINE_PATH = args.baseline_path
const COMMON = `
KONTEKST
- Dags dato: 2026-10-28. "Aktuel" = pr. denne dato. Formål: et krydsrefereret korpus af dansk regulering til RAG, hvor søgning skal kunne følge hjemmelskæder lov → bekendtgørelse → vejledning → praksis. Opgaven er KUN kortlægning – hent ikke dokumenterne.
- Scope (valgt): domæner byggeri, bolig, plan, energi, miljø, arbejdsmiljø, brand, el/gas/VVS; niveauer stat + kommunalt + EU; praksis (klagenævn, Ombudsmand, domme) medtages; standarder (DS/EN, Eurocodes) og branchevejledninger (BUILD/SBi, Molio m.fl.) KUN som metadata.
- Værktøjer: KUN WebSearch virker. WebFetch er blokeret af netværkspolitikken for alle eksterne domæner – brug den ikke. Evidens = WebSearch-resultater (titler, URL’er, uddrag/opsummering). Brug "standard" som udgangspunkt, "extended" til nye/svære fakta. Kør gerne flere søgninger parallelt i samme tur.
- Sikkerhedsmærker (præcis disse værdier):
  verificeret = påstanden fremgår direkte af et søgeresultat fra en officiel/primær kilde (retsinformation.dk, lovtidende.dk, ft.dk, myndighedens eget domæne, eur-lex.europa.eu) eller af to uafhængige troværdige sekundærkilder, OG afspejler tilstanden pr. 2026-10-28 (ressortforhold: kilde efter 3. juni 2026 eller baseline-afstemt).
  sandsynlig = én sekundærkilde, eller officiel kilde der kan være forældet, eller stærk faglig slutning (skriv i note hvad slutningen bygger på).
  ukendt = ingen evidens.
- URL’er: brug KUN URL’er der faktisk optrådte i dine søgeresultater, i baseline eller i seed-listen nedenfor. Konstruér/gæt aldrig URL’er, API-endpoints eller ELI’er. Mangler den: url.vaerdi = "ikke fundet". Det er bedre at skrive "ikke fundet" end at gætte.
- Seed (verificerede ELI’er for gældende versioner, fra jakob1379/br18 xref-laws.toml, tjekket mod retsinformation 2026-10-26): byggeloven https://www.retsinformation.dk/eli/lta/2016/1178 ; planloven https://www.retsinformation.dk/eli/lta/2024/572 ; udstykningsloven https://www.retsinformation.dk/eli/lta/2024/53 ; naturbeskyttelsesloven https://www.retsinformation.dk/eli/lta/2024/927 ; ladestanderbekendtgørelsen https://www.retsinformation.dk/eli/lta/2020/181 ; certificeringsbekendtgørelsen https://www.retsinformation.dk/eli/lta/2023/1693 ; beredskabsloven https://www.retsinformation.dk/eli/lta/2025/1741 ; bygningsfredningsloven https://www.retsinformation.dk/eli/lta/2018/219 ; arbejdsmiljøloven https://www.retsinformation.dk/eli/lta/2026/442 ; grundloven https://www.retsinformation.dk/eli/lta/1953/169 ; forvaltningsloven https://www.retsinformation.dk/eli/lta/2014/433 ; museumsloven https://www.retsinformation.dk/eli/lta/2025/1017 ; miljøbeskyttelsesloven https://www.retsinformation.dk/eli/lta/2026/842 ; teleloven https://www.retsinformation.dk/eli/lta/2025/681 ; masteloven https://www.retsinformation.dk/eli/lta/2021/420 ; skorstensfejerbekendtgørelsen https://www.retsinformation.dk/eli/lta/2017/541 . Kilde-URL for disse: https://github.com/jakob1379/br18/blob/main/xref-laws.toml . Disse må angives som verificeret for ELI/identifikator (ikke for andre påstande).
- Svar på dansk. Returnér rå data via StructuredOutput.

BASELINE: Læs FØRST filen ${BASELINE_PATH} med Read-værktøjet. Den er den afstemte ressortfordeling pr. 2026-10-28 (regering, ministerier, instanser, områder, ressortomlægninger, uafklarede konflikter). Brug dens id’er for ministerier og instanser; afviger du, så forklar i note og sæt sikkerhed derefter. Hovedpunkter: byggeri/bolig → min-boern-aeldre-og-bolig (administreres af sty-social-og-boligstyrelsen, organisatorisk under min-social); plan → min-by-land-og-transport (sty-plan-og-landdistriktsstyrelsen); Sikkerhedsstyrelsen fusioneret i sty-erhvervsstyrelsen 1/1/2026; affald → min-klima-energi-og-forsyning (Energistyrelsen); natur/vandmiljø/miljøvurdering → min-natur-og-dyrevelfaerd; miljøbeskyttelse/jord/kemikalier/drikkevand/spildevand/kyst → min-miljoe; beredskab → min-samfundssikkerhed-og-beredskab; arbejdsmiljø → min-beskaeftigelse-og-ligestilling; kommunaltilsyn → min-oekonomi-og-indenrigs (sty-ankestyrelsen); udstykning/matrikel → min-klima-energi-og-forsyning (sty-geodatastyrelsen).

ID-KONVENTIONER (små bogstaver, ascii: æ→ae, ø→oe, å→aa, bindestreger):
- ministerier/instanser: brug baseline-id’er. Nye instanser: sty-, naevn-, tilsyn-, raad-, fond-, dom-, ombud-, org- (private), std- (standardiseringsorgan/standard), kommune-alle, region-alle.
- love (type lov, ét node pr. lov; identifikatorer peger på gældende LBK/LOV): lov-<kortnavn>, fx lov-byggeloven, lov-planloven, lov-almenboligloven, lov-lejeloven, lov-andelsboligloven, lov-ejerlejlighedsloven, lov-byfornyelsesloven, lov-boligstoetteloven, lov-udstykningsloven, lov-matrikelloven, lov-bygningsfredningsloven, lov-museumsloven, lov-bbr-loven, lov-energimaerkningsloven (lov om fremme af energibesparelser i bygninger), lov-varmeforsyningsloven, lov-elforsyningsloven, lov-gasforsyningsloven, lov-ve-loven, lov-klimaloven, lov-forsyningstilsynsloven, lov-miljoebeskyttelsesloven, lov-miljoevurderingsloven, lov-jordforureningsloven, lov-naturbeskyttelsesloven, lov-kystbeskyttelsesloven, lov-vandloebsloven, lov-vandforsyningsloven, lov-vandsektorloven, lov-arbejdsmiljoeloven, lov-beredskabsloven, lov-elsikkerhedsloven, lov-gassikkerhedsloven, lov-autorisationsloven, lov-forvaltningsloven, lov-offentlighedsloven, lov-ombudsmandsloven, lov-kommunestyrelsesloven, lov-retsplejeloven, lov-ophavsretsloven, lov-planklagenaevnsloven, lov-mfkn-loven (lov om Miljø- og Fødevareklagenævnet). Brug disse præcist når loven er i spil.
- bekendtgørelser: bek-<kortnavn> (fx bek-br18 for bygningsreglementet, bek-certificering, bek-ladestandere, bek-skorstensfejer, bek-energimaerkning, bek-affald, bek-byggeplads/bygherrens pligter, bek-asbest); cirkulærer cirk-; vejledninger vejl-<…> (samlinger som én node, fx vejl-br18-vejledninger, vejl-at-vejledninger); tekniske forskrifter tf-<…>; planer/landsplandirektiver plan-<…>; regulativer reg-<…>.
- EU: eu-dir-YYYY-NNNN, eu-reg-YYYY-NNNN, eu-dec-YYYY-NNNN (fx eu-dir-2024-1275, eu-reg-2024-3110). Brug årstal og løbenummer som i retsaktens nummer, uden foranstillede nuller (fx eu-dir-1992-57, eu-dir-2010-31, eu-reg-2024-3110).
- dokumentkilder (type dokumentkilde): kilde-<slug>, fx kilde-retsinformation, kilde-lovtidende, kilde-eurlex, kilde-ft-oda, kilde-domsdatabasen, kilde-fob-database, kilde-bygningsreglementet-dk, kilde-plandata, kilde-datafordeleren, kilde-miljoeportal, kilde-mfkn-afgoerelser, kilde-pkn-afgoerelser, kilde-ast-principmeddelelser, kilde-at-dk, kilde-sik-dk, kilde-ens-dk, kilde-mst-dk, kilde-brs-dk.

NODETYPER (brug præcis): ministerium, styrelse, direktorat, nævn, klagenævn, tilsyn, råd, fond, domstol, ombudsmand, kommune, region, offentlig-virksomhed, eu-institution, privat-organisation, standardiseringsorgan, dokumentkilde, lov, bekendtgørelse, cirkulære, vejledning, teknisk-forskrift, plan, regulativ, eu-direktiv, eu-forordning, eu-afgørelse, standard, branchevejledning, praksissamling.

KANTTYPER (brug KUN disse; "from" er den aktive part, læses "from <type> to"):
- ressortansvar: ministerium → instans/lov (ministeriet har ressortansvaret)
- delegation: ministerium/styrelse → styrelse/kommune (kompetence delegeret; nævn delegationsbekendtgørelsen i beskrivelse)
- hjemmel_for: lov/bekendtgørelse → bekendtgørelse/vejledning/instans/plan (giver hjemmel til / opretter)
- udsteder: instans → retsakt/vejledning/dokumentkilde (udsteder/udgiver/driver)
- klageinstans: klageinstans → førsteinstans (from er klageinstans for afgørelser truffet af to; angiv lov i beskrivelse)
- tilsyn: tilsynsmyndighed → tilsynsobjekt
- implementerer_EU: dansk retsakt → EU-retsakt
- henviser_til: dokument → dokument (typisk krydsreference i teksten; fx bek-br18 henviser_til std-eurocodes)

FELTER PR. NODE (alle påkrævet; påstandsfelter har kilder[] og sikkerhed):
id, navn, type, ministerium (ministerium-id eller "ingen"), status (aktiv|nedlagt|omdøbt|ophævet|ukendt), tidligere_navne[] (navn, periode, efterfoelger-id hvis kendt, kilder, sikkerhed), hjemmel{tekst} (oprettelsesgrundlag for instanser; hjemmelslov § for bekendtgørelser; "ikke relevant" for love/EU), dokumenttyper{liste[{type, bindende: bindende|vejledende|blandet|ukendt}]} (hvad noden udsteder/indeholder: lov, lovbekendtgørelse, bekendtgørelse, cirkulære, vejledning, teknisk forskrift, afgørelse, principafgørelse, udtalelse, dom, FAQ/fortolkningsbidrag, plan, regulativ, standard, datasæt …), url{vaerdi}, adgang{vaerdier ⊆ [API, bulk, ELI, RSS, HTML, PDF, betalingsmur, ukendt, ikke-relevant], note}, identifikatorer{eli, lovtidende, celex, journalnr, andet}, licens{tekst}, opdatering{frekvens, versionshistorik}, krydsref_moenstre[] (typiske tekstmønstre, fx "§ 6 i lov om byggeri", "bekendtgørelse nr. 1399 af 12. december 2019", "BR18 § 82", "direktiv 2010/31/EU", "FOB 2019-21", "U.2020.1234H", "MFKN j.nr. 20/12345"), note. Valgfrit: ingest{vaerdi 1-5, besvaer 1-5, begrundelse} – SKAL udfyldes for dokumentkilder og for instanser/retsaktsamlinger, hvis dokumenter skal hentes fra dem (værdi = nytte for RAG/hjemmelskæder; besvær = teknisk/juridisk vanskelighed: 1 = API/bulk åben licens, 5 = betalingsmur/scannede PDF’er).
Nedlagte/omdøbte instanser: egen node med status nedlagt/omdøbt og en tidligere_navne-post hos efterfølgeren.
Omfang: dæk domænet udtømmende for instanser, klageveje og EU; for retsakter: alle love + de centrale bekendtgørelser/vejledningssamlinger der indgår i hjemmelskæder (ikke hver eneste bekendtgørelse). Typisk 30-70 noder og 60-180 kanter. Fejlagtig præcision er værre end "ukendt".
`

const CLAIM_PROPS = {
  kilder: { type: 'array', items: { type: 'string' } },
  sikkerhed: { type: 'string', enum: ['verificeret', 'sandsynlig', 'ukendt'] },
}
const claim = (extra, req = []) => ({
  type: 'object',
  properties: { ...extra, ...CLAIM_PROPS },
  required: [...req, 'kilder', 'sikkerhed'],
})
const NODE_TYPES = ['ministerium', 'styrelse', 'direktorat', 'nævn', 'klagenævn', 'tilsyn', 'råd', 'fond', 'domstol', 'ombudsmand', 'kommune', 'region', 'offentlig-virksomhed', 'eu-institution', 'privat-organisation', 'standardiseringsorgan', 'dokumentkilde', 'lov', 'bekendtgørelse', 'cirkulære', 'vejledning', 'teknisk-forskrift', 'plan', 'regulativ', 'eu-direktiv', 'eu-forordning', 'eu-afgørelse', 'standard', 'branchevejledning', 'praksissamling']
const EDGE_TYPES = ['ressortansvar', 'delegation', 'hjemmel_for', 'udsteder', 'klageinstans', 'tilsyn', 'implementerer_EU', 'henviser_til']
const ACCESS = ['API', 'bulk', 'ELI', 'RSS', 'HTML', 'PDF', 'betalingsmur', 'ukendt', 'ikke-relevant']

const NODE = {
  type: 'object',
  properties: {
    id: { type: 'string' },
    navn: { type: 'string' },
    type: { type: 'string', enum: NODE_TYPES },
    ministerium: { type: 'string' },
    status: { type: 'string', enum: ['aktiv', 'nedlagt', 'omdøbt', 'ophævet', 'ukendt'] },
    tidligere_navne: {
      type: 'array',
      items: claim({ navn: { type: 'string' }, periode: { type: 'string' }, efterfoelger: { type: 'string' } }, ['navn', 'periode']),
    },
    hjemmel: claim({ tekst: { type: 'string' } }, ['tekst']),
    dokumenttyper: claim({
      liste: {
        type: 'array',
        items: {
          type: 'object',
          properties: { type: { type: 'string' }, bindende: { type: 'string', enum: ['bindende', 'vejledende', 'blandet', 'ukendt'] }, note: { type: 'string' } },
          required: ['type', 'bindende'],
        },
      },
    }, ['liste']),
    url: claim({ vaerdi: { type: 'string' } }, ['vaerdi']),
    adgang: claim({ vaerdier: { type: 'array', items: { type: 'string', enum: ACCESS } }, note: { type: 'string' } }, ['vaerdier']),
    identifikatorer: claim({ eli: { type: 'string' }, lovtidende: { type: 'string' }, celex: { type: 'string' }, journalnr: { type: 'string' }, andet: { type: 'string' } }),
    licens: claim({ tekst: { type: 'string' } }, ['tekst']),
    opdatering: claim({ frekvens: { type: 'string' }, versionshistorik: { type: 'string' } }, ['frekvens', 'versionshistorik']),
    krydsref_moenstre: { type: 'array', items: { type: 'string' } },
    ingest: {
      type: 'object',
      properties: { vaerdi: { type: 'integer', minimum: 1, maximum: 5 }, besvaer: { type: 'integer', minimum: 1, maximum: 5 }, begrundelse: { type: 'string' } },
      required: ['vaerdi', 'besvaer', 'begrundelse'],
    },
    note: { type: 'string' },
  },
  required: ['id', 'navn', 'type', 'ministerium', 'status', 'tidligere_navne', 'hjemmel', 'dokumenttyper', 'url', 'adgang', 'identifikatorer', 'licens', 'opdatering', 'krydsref_moenstre'],
}
const EDGE = claim({
  from: { type: 'string' }, to: { type: 'string' },
  type: { type: 'string', enum: EDGE_TYPES },
  beskrivelse: { type: 'string' },
  gyldig_fra: { type: 'string' },
}, ['from', 'to', 'type', 'beskrivelse'])
const HUL = {
  type: 'object',
  properties: {
    emne: { type: 'string' },
    type: { type: 'string', enum: ['betalingsmur', 'kun-pdf', 'ingen-api', 'uklart', 'ikke-fundet', 'andet'] },
    beskrivelse: { type: 'string' },
    noder: { type: 'array', items: { type: 'string' } },
    kilder: { type: 'array', items: { type: 'string' } },
  },
  required: ['emne', 'type', 'beskrivelse', 'noder', 'kilder'],
}
const DOMAIN_SCHEMA = {
  type: 'object',
  properties: {
    nodes: { type: 'array', items: NODE },
    edges: { type: 'array', items: EDGE },
    huller: { type: 'array', items: HUL },
    noter: { type: 'array', items: { type: 'string' } },
  },
  required: ['nodes', 'edges', 'huller', 'noter'],
}
const VERIFY_SCHEMA = {
  type: 'object',
  properties: {
    fund: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          maal: { type: 'string', description: 'node-id, eller kant som "from|type|to"' },
          felt: { type: 'string' },
          vurdering: { type: 'string', enum: ['bekraeftet', 'rettet', 'afkraeftet', 'nedgraderet', 'opgraderet', 'uafklaret'] },
          korrekt_vaerdi: { type: 'string' },
          kilder: { type: 'array', items: { type: 'string' } },
          begrundelse: { type: 'string' },
        },
        required: ['maal', 'felt', 'vurdering', 'kilder', 'begrundelse'],
      },
    },
    mangler: {
      type: 'array',
      items: { type: 'object', properties: { beskrivelse: { type: 'string' }, kilder: { type: 'array', items: { type: 'string' } } }, required: ['beskrivelse', 'kilder'] },
    },
  },
  required: ['fund', 'mangler'],
}
const PATCH_SCHEMA = {
  type: 'object',
  properties: {
    node_upserts: { type: 'array', items: NODE, description: 'HELE noden (erstatter eksisterende med samme id)' },
    node_removals: { type: 'array', items: { type: 'object', properties: { id: { type: 'string' }, begrundelse: { type: 'string' } }, required: ['id', 'begrundelse'] } },
    edge_upserts: { type: 'array', items: EDGE, description: 'erstatter kant med samme from|type|to' },
    edge_removals: { type: 'array', items: { type: 'object', properties: { from: { type: 'string' }, type: { type: 'string' }, to: { type: 'string' }, begrundelse: { type: 'string' } }, required: ['from', 'type', 'to', 'begrundelse'] } },
    huller: { type: 'array', items: HUL, description: 'NYE huller (tilføjes)' },
    noter: { type: 'array', items: { type: 'string' } },
  },
  required: ['node_upserts', 'node_removals', 'edge_upserts', 'edge_removals', 'huller', 'noter'],
}


const BUDGET = args.budget || 35
const results = await parallel(args.keys.map(key => () => agent(`${COMMON}
Du er ADVERSARIEL VERIFIKATOR og KONSOLIDATOR for domænet "${key}" i et registry over dansk regulering. Tidligere verifikation blev ikke gennemført (søgebudgettet var opbrugt), så meget i filen bygger på modelviden og genbrugte kilder, der ikke nødvendigvis understøtter påstanden.
SØGEBUDGET: Du har højst ${BUDGET} WebSearch-kald i alt (budgettet deles med andre agenter – overskrid det ikke). Saml flere spørgsmål i hver søgning.

1. Læs HELE filen ${args.dir}/${key}.json med Read (den er lang – læs i bidder med offset/limit, fx 2000 linjer ad gangen, til du har læst alle linjer). Den indeholder domænets nuværende noder (fulde felter) og kanter samt alle node-id’er i registry’et.
2. Antag at der er fejl. Efterprøv med egne søgninger, i denne prioritet:
   a) instansers ministerium/status pr. 2026-10-28 og alle kanter af typen ressortansvar, delegation, klageinstans, tilsyn, hjemmel_for (findes de, rigtig retning – "from" er den aktive part – rigtig lov);
   b) påstande markeret verificeret, hvor kilden ikke ser ud til at understøtte netop den påstand (fx en baseline-kilde om ministeriet brugt som kilde for en lovs ELI);
   c) url-værdier og ELI/LBK/BEK-numre og CELEX for de vigtigste noder (love, centrale bekendtgørelser, dokumentkilder);
   d) implementerer_EU-kanter;
   e) manglende centrale instanser/love/klageveje i domænet.
3. Returnér en PATCH: node_upserts = HELE opdaterede noder (kun dem du ændrer; bevar felter du ikke har grund til at ændre, inkl. domaener ikke nødvendigt), node_removals, edge_upserts (hele kanter), edge_removals, nye huller, noter. Nedgradér sikkerhed hvor kilden ikke understøtter påstanden; opgradér kun med en kilde, du selv har set i dine søgeresultater. Brug kun URL’er fra søgeresultater. Uændrede noder/kanter skal ikke med.
4. I noter: skriv kort hvad du efterprøvede, og hvad der stadig er uafklaret.`, { label: `verify2:${key}`, phase: 'Verify', schema: PATCH_SCHEMA })))

return args.keys.map((k, i) => ({ key: k, ok: !!results[i], n: results[i] ? results[i].node_upserts.length : 0, e: results[i] ? results[i].edge_upserts.length : 0, r: results[i] ? results[i].node_removals.length + results[i].edge_removals.length : 0 }))
