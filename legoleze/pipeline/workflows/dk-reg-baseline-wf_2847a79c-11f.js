export const meta = {
  name: 'dk-reg-baseline',
  description: 'Fastlæg dansk ressortfordeling pr. 2026-10-28 for bygge-/bolig-/plan-/energi-/miljø-/arbejdsmiljø-/brand-/el-gas-VVS-området',
  phases: [
    { title: 'Research', detail: 'to uafhængige agenter: regering/ministerier og område→myndighed' },
    { title: 'Reconcile', detail: 'afstem, løs konflikter, tildel kanoniske id’er' },
  ],
}

const COMMON = `
KONTEKST (gælder hele opgaven)
- Dags dato: 2026-10-28. "Aktuel" betyder pr. denne dato.
- Værktøjer: KUN WebSearch virker. WebFetch er blokeret af netværkspolitikken for ALLE eksterne domæner (retsinformation.dk, regeringen.dk, eur-lex, wikipedia m.fl.) – brug den ikke. Evidens = WebSearch-resultater (titler, URL'er, uddrag/opsummering). Brug mode "standard" som udgangspunkt og "extended" til nyere/svære fakta (2026-ressortændringer). Kør gerne flere søgninger parallelt.
- Sikkerhedsmærker (brug præcis disse): 
  verificeret = påstanden fremgår direkte af et søgeresultat fra en officiel/primær kilde (retsinformation.dk, lovtidende.dk, ft.dk, stm.dk, regeringen.dk, ministeriers/styrelsers egne domæner, eur-lex) ELLER af to uafhængige troværdige sekundærkilder (fx lex.dk + dr.dk), og kilden afspejler tilstanden pr. 2026-10-28 (for ressortforhold: kilde fra efter 3. juni 2026 eller eksplicit om ændringen).
  sandsynlig = én sekundærkilde, eller officiel kilde der kan være forældet (fx før regeringsdannelsen 3. juni 2026), eller stærk slutning.
  ukendt = ingen evidens fundet.
- URL'er: angiv KUN URL'er, der faktisk optrådte i dine søgeresultater. Konstruér/gæt aldrig URL'er. Mangler den, skriv "ikke fundet".
- Kendt fra forundersøgelse (skal efterprøves, ikke bare gentages): Folketingsvalg 24. marts 2026; Regeringen Mette Frederiksen III dannet 3. juni 2026 (S, SF, RV, M; 21 ministre). Ifølge lex.dk forlod Signe Munk (SF) regeringen 27. oktober 2026, og Karina Lorentzen Dehnhardt blev by-, land- og transportminister. Kilder set: https://lex.dk/Regeringen_Mette_Frederiksen_III , https://lex.dk/folketingsvalg_2026 , https://da.wikipedia.org/wiki/Regeringen_Mette_Frederiksen_III . Kongelig resolution af 15. december 2022 overførte Bolig- og Planstyrelsens byggeri- og boligområder til Social-, Bolig- og Ældreministeriet (kilde: https://ft.dk/samling/20222/almdel/BOU/bilag/13/2649406.pdf) – sandsynligvis ændret igen i 2024 og/eller juni 2026.
- Svar på dansk. Returnér rå data via StructuredOutput – ingen prosa til mennesker.
`

const SCOPE = `
SCOPE-OMRÅDER: byggeri (byggeloven, bygningsreglementet BR18, certificering af statikere/brandrådgivere, byggeskadeforsikring, byggevarer/CPR-markedsovervågning), bolig (almene boliger, Landsbyggefonden, lejeloven/privat udlejning, andelsboliger, ejerlejligheder, byfornyelse, boligstøtte), plan (planloven, landsplandirektiver, Fingerplan, kystnærhedszone, zoneregler), udstykning/matrikel, bygningsfredning/bevaring, energi (energimærkning af bygninger, energieffektivitet, varmeforsyning, el- og gasforsyning, VE, ladestandere), forsyningstilsyn, miljø (miljøbeskyttelse, miljøvurdering/VVM, jordforurening, affald inkl. bygge-/anlægsaffald, kemikalier, støj), natur (naturbeskyttelse, habitat), kyst (kystbeskyttelse), vand (drikkevand, spildevand, vandsektor), arbejdsmiljø (inkl. byggepladser, asbest), beredskab/brand, elsikkerhed, gassikkerhed, autorisation af el/VVS/kloak, klagenævn (Nævnenes Hus m.fl.), kommunaltilsyn (Ankestyrelsen), Folketingets Ombudsmand.
`

const CLAIM = {
  type: 'object',
  properties: {
    kilder: { type: 'array', items: { type: 'string' }, description: 'URL’er set i søgeresultater' },
    sikkerhed: { type: 'string', enum: ['verificeret', 'sandsynlig', 'ukendt'] },
  },
  required: ['kilder', 'sikkerhed'],
}
const PREV = {
  type: 'array',
  items: {
    type: 'object',
    properties: {
      navn: { type: 'string' },
      periode: { type: 'string', description: 'fx "2021-02-01 – 2022-12-15" eller "–2026-06-03"' },
      note: { type: 'string' },
      kilder: { type: 'array', items: { type: 'string' } },
      sikkerhed: { type: 'string', enum: ['verificeret', 'sandsynlig', 'ukendt'] },
    },
    required: ['navn', 'periode', 'kilder', 'sikkerhed'],
  },
}

const SCHEMA_A = {
  type: 'object',
  properties: {
    regering: {
      type: 'object',
      properties: {
        navn: { type: 'string' }, dannet: { type: 'string' }, partier: { type: 'array', items: { type: 'string' } },
        ...CLAIM.properties,
      },
      required: ['navn', 'dannet', 'partier', 'kilder', 'sikkerhed'],
    },
    ministerier: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          navn: { type: 'string', description: 'officielt ministerienavn pr. 2026-10-28' },
          minister: { type: 'string' },
          ministertitel: { type: 'string' },
          oprettet_eller_omdoebt: { type: 'string', description: 'dato hvis kendt' },
          tidligere_navne: PREV,
          ressortomraader_i_scope: { type: 'array', items: { type: 'string' } },
          kilder: CLAIM.properties.kilder, sikkerhed: CLAIM.properties.sikkerhed,
          note: { type: 'string' },
        },
        required: ['navn', 'minister', 'tidligere_navne', 'ressortomraader_i_scope', 'kilder', 'sikkerhed'],
      },
    },
    ressortomlaegninger: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          dato: { type: 'string' }, retsakt: { type: 'string', description: 'fx kongelig resolution, bekendtgørelse nr.' },
          omraade: { type: 'string' }, fra: { type: 'string' }, til: { type: 'string' },
          kilder: CLAIM.properties.kilder, sikkerhed: CLAIM.properties.sikkerhed,
        },
        required: ['dato', 'omraade', 'fra', 'til', 'kilder', 'sikkerhed'],
      },
    },
    noter: { type: 'array', items: { type: 'string' } },
  },
  required: ['regering', 'ministerier', 'ressortomlaegninger', 'noter'],
}

const SCHEMA_B = {
  type: 'object',
  properties: {
    omraader: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          omraade: { type: 'string' },
          ministerium: { type: 'string', description: 'aktuelt ressortministerium' },
          instanser: { type: 'array', items: { type: 'string' }, description: 'styrelser/nævn/tilsyn der administrerer' },
          vigtigste_love: { type: 'array', items: { type: 'string' } },
          seneste_aendring: { type: 'string', description: 'dato + hvad' },
          tidligere_placering: { type: 'string' },
          kilder: CLAIM.properties.kilder, sikkerhed: CLAIM.properties.sikkerhed,
          note: { type: 'string' },
        },
        required: ['omraade', 'ministerium', 'instanser', 'vigtigste_love', 'kilder', 'sikkerhed'],
      },
    },
    instanser: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          navn: { type: 'string' },
          type: { type: 'string', description: 'styrelse | direktorat | nævn | klagenævn | tilsyn | råd | fond | ombudsmand | domstol | andet' },
          ministerium: { type: 'string' },
          status: { type: 'string', enum: ['aktiv', 'nedlagt', 'omdøbt', 'ukendt'] },
          tidligere_navne: PREV,
          hjemmesider_set: { type: 'array', items: { type: 'string' }, description: 'domæner/URL’er set i søgeresultater' },
          kilder: CLAIM.properties.kilder, sikkerhed: CLAIM.properties.sikkerhed,
          note: { type: 'string' },
        },
        required: ['navn', 'type', 'ministerium', 'status', 'tidligere_navne', 'kilder', 'sikkerhed'],
      },
    },
    noter: { type: 'array', items: { type: 'string' } },
  },
  required: ['omraader', 'instanser', 'noter'],
}

const SCHEMA_C = {
  type: 'object',
  properties: {
    dato: { type: 'string' },
    regering: SCHEMA_A.properties.regering,
    ministerier: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          id: { type: 'string', description: 'min-<slug>, ascii (æ→ae, ø→oe, å→aa), fx min-beskaeftigelse' },
          navn: { type: 'string' }, minister: { type: 'string' },
          tidligere_navne: PREV,
          kilder: CLAIM.properties.kilder, sikkerhed: CLAIM.properties.sikkerhed,
          note: { type: 'string' },
        },
        required: ['id', 'navn', 'minister', 'tidligere_navne', 'kilder', 'sikkerhed'],
      },
    },
    instanser: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          id: { type: 'string', description: 'sty-<slug> styrelse/direktorat, naevn-<slug> nævn/klagenævn, tilsyn-<slug>, raad-<slug>, fond-<slug>, dom-<slug>, ombud-<slug>, org-<slug>' },
          navn: { type: 'string' },
          type: { type: 'string' },
          ministerium_id: { type: 'string', description: 'id fra ministerier[] eller "ingen" (fx Ombudsmanden/domstole)' },
          status: { type: 'string', enum: ['aktiv', 'nedlagt', 'omdøbt', 'ukendt'] },
          tidligere_navne: PREV,
          hjemmesider_set: { type: 'array', items: { type: 'string' } },
          kilder: CLAIM.properties.kilder, sikkerhed: CLAIM.properties.sikkerhed,
          note: { type: 'string' },
        },
        required: ['id', 'navn', 'type', 'ministerium_id', 'status', 'tidligere_navne', 'kilder', 'sikkerhed'],
      },
    },
    omraader: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          omraade: { type: 'string' }, ministerium_id: { type: 'string' },
          instans_ids: { type: 'array', items: { type: 'string' } },
          vigtigste_love: { type: 'array', items: { type: 'string' } },
          seneste_aendring: { type: 'string' },
          kilder: CLAIM.properties.kilder, sikkerhed: CLAIM.properties.sikkerhed,
          note: { type: 'string' },
        },
        required: ['omraade', 'ministerium_id', 'instans_ids', 'vigtigste_love', 'kilder', 'sikkerhed'],
      },
    },
    ressortomlaegninger: SCHEMA_A.properties.ressortomlaegninger,
    uafklarede_konflikter: { type: 'array', items: { type: 'string' } },
  },
  required: ['dato', 'regering', 'ministerier', 'instanser', 'omraader', 'ressortomlaegninger', 'uafklarede_konflikter'],
}

phase('Research')
const [a, b] = await parallel([
  () => agent(`${COMMON}
OPGAVE A: Fastlæg regeringens sammensætning og den aktuelle ressortfordeling pr. 2026-10-28.
1. Find den nuværende regering (navn, dannelsesdato, partier) og ALLE ministerier med officielle navne og ministre pr. 2026-10-28 (husk ændringen 27. oktober 2026 og evt. andre ændringer efter 3. juni 2026).
2. Find de kongelige resolutioner/ressortomlægninger fra 2022 til i dag, der flyttede opgaver inden for scope mellem ministerier (særligt 15. dec. 2022, 2024-omlægninger fx Ministeriet for Samfundssikkerhed og Beredskab / Ministeriet for Grøn Trepart / Ministeriet for Byer og Landdistrikter, og omlægningen ved regeringsdannelsen 3. juni 2026). Notér dato, retsakt, område, fra → til.
3. For hvert ministerium: hvilke scope-områder ligger der nu, og hvilke tidligere navne har det haft (med periode).
${SCOPE}
Søg bredt: "kongelig resolution ressortoverførsel 2026", "ressortomlægning juni 2026", ministeriernes egne sider (stm.dk, regeringen.dk), lex.dk, Altinget, DR, ft.dk, retsinformation (bekendtgørelser om ændring af ressort/delegation). Markér sikkerhed ærligt.`, { label: 'A: regering & ministerier', phase: 'Research', schema: SCHEMA_A }),
  () => agent(`${COMMON}
OPGAVE B: Kortlæg for hvert scope-område hvilket ministerium og hvilke styrelser/nævn/tilsyn der administrerer det pr. 2026-10-28, og hvordan placeringen har ændret sig siden 2019 (tidligere navne og placeringer, med datoer).
${SCOPE}
Dæk mindst disse instanser (og find flere): Bolig- og Planstyrelsen (og evt. efterfølger/omdøbning), Plan- og Landdistriktsstyrelsen (hvis den findes), Erhvervsstyrelsen, Sikkerhedsstyrelsen, Energistyrelsen, Forsyningstilsynet, Energinet, Miljøstyrelsen, Naturstyrelsen, Kystdirektoratet, Klimadatastyrelsen (tidligere SDFI/Geodatastyrelsen), Slots- og Kulturstyrelsen, Arbejdstilsynet, Beredskabsstyrelsen, Nævnenes Hus (Planklagenævnet, Miljø- og Fødevareklagenævnet, Energiklagenævnet, Byggeklageenheden, Erhvervsankenævnet?), Arbejdsmiljøklagenævnet, Ankestyrelsen, Landsbyggefonden, Byggeskadefonden, Grundejernes Investeringsfond, huslejenævn/beboerklagenævn, Folketingets Ombudsmand, Danmarks Miljøportal, Udbetaling Danmark (boligstøtte). Notér nedlagte instanser (fx Natur- og Miljøklagenævnet, Statsforvaltningen, Trafik-, Bygge- og Boligstyrelsen, Planstyrelsen, Energitilsynet) med efterfølger og dato.
Hver påstand skal have kilde-URL’er fra dine søgeresultater og sikkerhedsmærke.`, { label: 'B: område → myndighed', phase: 'Research', schema: SCHEMA_B }),
])

phase('Reconcile')
const c = await agent(`${COMMON}
OPGAVE C: Du får to uafhængige kortlægninger (A og B) af dansk ressortfordeling pr. 2026-10-28. Afstem dem til ÉN kanonisk baseline:
- Hvor A og B er enige og har gode kilder: behold (opgradér til verificeret kun hvis kriteriet er opfyldt).
- Hvor de er uenige, eller hvor kilderne er fra før 3. juni 2026 for ressortforhold: lav selv nye WebSearch-søgninger for at afgøre det. Kan det ikke afgøres, vælg det bedst underbyggede, markér sandsynlig/ukendt og skriv konflikten i uafklarede_konflikter.
- Tildel stabile id’er: ministerier "min-<slug>", styrelser/direktorater "sty-<slug>", nævn/klagenævn "naevn-<slug>", tilsyn "tilsyn-<slug>", råd "raad-<slug>", fonde "fond-<slug>", domstole "dom-<slug>", ombudsmand "ombud-<slug>", andre "org-<slug>". Slug: små bogstaver, ascii (æ→ae, ø→oe, å→aa), bindestreger, kort men entydigt (fx sty-bolig-og-planstyrelsen, naevn-planklagenaevnet, min-social-og-bolig). Nedlagte/omdøbte instanser får egne id’er med status nedlagt/omdøbt og en note om efterfølger-id.
- Medtag alle scope-relevante ministerier (også dem med kun et lille scope-område, fx Kulturministeriet for bygningsfredning, Justitsministeriet for domstole/Domsdatabasen, Digitaliseringsministeriet hvis det ejer Retsinformation/Datafordeler-relevante opgaver – Retsinformation drives af Civilstyrelsen under Justitsministeriet; efterprøv).
${SCOPE}

KORTLÆGNING A:
${JSON.stringify(a)}

KORTLÆGNING B:
${JSON.stringify(b)}`, { label: 'C: afstemning', phase: 'Reconcile', schema: SCHEMA_C })

return c
