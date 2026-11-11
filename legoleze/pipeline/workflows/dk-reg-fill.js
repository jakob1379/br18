export const meta = {
  name: 'dk-reg-fill',
  description: 'Udfyld kanoniske URL’er/ELI/CELEX/adgang for noder uden fundne kilder, og find manglende noder/kanter pr. ministerområde',
  phases: [
    { title: 'Fill', detail: 'én agent pr. batch af noder: URL, identifikatorer, adgang' },
    { title: 'Critic', detail: 'completeness-kritiker pr. ministerområde: manglende instanser, love, klageveje, EU' },
  ],
}

const DIR = args.dir

const RULES = `
REGLER
- Dags dato 2026-10-28. KUN WebSearch virker (WebFetch er blokeret for alle eksterne domæner). Kør flere søgninger parallelt.
- SØGEBUDGET: højst ${args.search_budget || 20} WebSearch-kald for dig i alt (budgettet deles med andre agenter). Prioritér de vigtigste noder.
- URL’er: angiv KUN URL’er der optrådte i dine søgeresultater. Konstruér aldrig URL’er/ELI’er/API-endpoints. Ikke set → udelad opdateringen.
- Sikkerhed: verificeret = fremgår direkte af søgeresultat fra officiel/primær kilde (retsinformation.dk, eur-lex.europa.eu, myndighedens eget domæne, ft.dk) og er aktuel; sandsynlig = sekundærkilde/muligvis forældet/slutning; ukendt = intet fundet.
- Svar på dansk, rå data via StructuredOutput.
`
const FILL_SCHEMA = {
  type: 'object',
  properties: {
    opdateringer: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          id: { type: 'string' },
          felt: { type: 'string', enum: ['url', 'identifikatorer', 'adgang', 'licens', 'opdatering', 'hjemmel', 'status', 'ministerium'] },
          vaerdi_json: { type: 'string', description: 'JSON-objekt med feltets indhold UDEN kilder/sikkerhed, fx {"vaerdi":"https://..."} for url, {"eli":"...","lovtidende":"LBK nr. 465 af 24/04/2026","celex":"32024L1275"} for identifikatorer, {"vaerdier":["HTML","PDF"],"note":"..."} for adgang, {"tekst":"..."} for licens/hjemmel, {"frekvens":"...","versionshistorik":"..."} for opdatering, {"vaerdi":"aktiv"} for status, {"vaerdi":"min-..."} for ministerium' },
          kilder: { type: 'array', items: { type: 'string' } },
          sikkerhed: { type: 'string', enum: ['verificeret', 'sandsynlig', 'ukendt'] },
          begrundelse: { type: 'string' },
        },
        required: ['id', 'felt', 'vaerdi_json', 'kilder', 'sikkerhed', 'begrundelse'],
      },
    },
  },
  required: ['opdateringer'],
}

phase('Fill')
const fills = parallel((args.batches || []).map(i => () => agent(`${RULES}
OPGAVE: Læs filen ${DIR}/fill_batch_${i}.json med Read. Den indeholder noder fra et registry over dansk regulering (byggeri, bolig, plan, energi, miljø, arbejdsmiljø, brand, el/gas/VVS), hvor url/identifikatorer/adgang mangler eller er usikre, eller hvor url peger på en underside frem for den kanoniske side.
For HVER node:
1. url: find den kanoniske URL – for instanser/dokumentkilder myndighedens/kildens forside eller primære side; for danske love/bekendtgørelser retsinformation-ELI for den GÆLDENDE version (søg fx "<titel> retsinformation lovbekendtgørelse 2026"); for EU-retsakter EUR-Lex-siden (eur-lex.europa.eu/eli/... eller ?uri=CELEX:...); for nedlagte instanser: drop url medmindre en arkivside ses.
2. identifikatorer: gældende LBK/BEK/LOV nr. og dato, ELI, CELEX (for EU), og for afgørelsesdatabaser journalnr.-mønster.
3. adgang: for dokumentkilder – er der API, bulk-download, RSS, ELI, kun HTML/PDF, betalingsmur? Kun med evidens.
Spring noder over hvor intet nyt findes. Opdatér kun når du har en kilde; nedgradér aldrig eksisterende verificerede værdier uden modbevis (så angiv begrundelse).`, { label: `fill:${i}`, phase: 'Fill', schema: FILL_SCHEMA })))

phase('Critic')
const NODE_LITE = {
  type: 'object',
  properties: {
    id: { type: 'string' }, navn: { type: 'string' }, type: { type: 'string' }, ministerium: { type: 'string' },
    status: { type: 'string', enum: ['aktiv', 'nedlagt', 'omdøbt', 'ophævet', 'ukendt'] },
    hjemmel_tekst: { type: 'string' }, url: { type: 'string', description: 'kun hvis set i søgeresultat, ellers "ikke fundet"' },
    identifikatorer_json: { type: 'string', description: 'JSON {"eli":..,"lovtidende":..,"celex":..,"journalnr":..}' },
    dokumenttyper: { type: 'array', items: { type: 'object', properties: { type: { type: 'string' }, bindende: { type: 'string', enum: ['bindende', 'vejledende', 'blandet', 'ukendt'] } }, required: ['type', 'bindende'] } },
    adgang: { type: 'array', items: { type: 'string', enum: ['API', 'bulk', 'ELI', 'RSS', 'HTML', 'PDF', 'betalingsmur', 'ukendt', 'ikke-relevant'] } },
    note: { type: 'string' },
    kilder: { type: 'array', items: { type: 'string' } },
    sikkerhed: { type: 'string', enum: ['verificeret', 'sandsynlig', 'ukendt'] },
  },
  required: ['id', 'navn', 'type', 'ministerium', 'status', 'hjemmel_tekst', 'url', 'identifikatorer_json', 'dokumenttyper', 'adgang', 'note', 'kilder', 'sikkerhed'],
}
const CRITIC_SCHEMA = {
  type: 'object',
  properties: {
    nye_noder: { type: 'array', items: NODE_LITE },
    nye_kanter: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          from: { type: 'string' }, to: { type: 'string' },
          type: { type: 'string', enum: ['ressortansvar', 'delegation', 'hjemmel_for', 'udsteder', 'klageinstans', 'tilsyn', 'implementerer_EU', 'henviser_til'] },
          beskrivelse: { type: 'string' }, kilder: { type: 'array', items: { type: 'string' } },
          sikkerhed: { type: 'string', enum: ['verificeret', 'sandsynlig', 'ukendt'] },
        },
        required: ['from', 'to', 'type', 'beskrivelse', 'kilder', 'sikkerhed'],
      },
    },
    forkerte_kanter: {
      type: 'array',
      items: { type: 'object', properties: { from: { type: 'string' }, type: { type: 'string' }, to: { type: 'string' }, begrundelse: { type: 'string' }, kilder: { type: 'array', items: { type: 'string' } } }, required: ['from', 'type', 'to', 'begrundelse', 'kilder'] },
    },
    huller: { type: 'array', items: { type: 'string' } },
  },
  required: ['nye_noder', 'nye_kanter', 'forkerte_kanter', 'huller'],
}
const critics = parallel((args.clusters || []).map(c => () => agent(`${RULES}
OPGAVE: Du er completeness-kritiker for ministerområdet "${c.navn}". Læs filen ${DIR}/critic_${c.key}.json med Read: den indeholder områdets nuværende noder (id, navn, type, ministerium, status) og kanter (from|type|to) i et registry over dansk regulering, samt en liste over ALLE node-id’er i registry’et (brug dem til kanter; opfind ikke dubletter).
Spørg: Hvad mangler for at en RAG-bruger kan følge hjemmelskæden lov → bekendtgørelse → vejledning → praksis på dette område pr. 2026-10-28?
- Manglende instanser (styrelser, nævn, tilsyn, råd), herunder nedlagte/omdøbte med efterfølger.
- Manglende centrale love/bekendtgørelser/vejledningssamlinger, og hjemmel_for-kanter imellem dem.
- Manglende klage- og tilsynsveje (klageinstans: from = klageinstans, to = førsteinstans; tilsyn: from = tilsynsmyndighed).
- Manglende implementerer_EU-kanter (dansk retsakt → EU-id som eu-dir-YYYY-N / eu-reg-YYYY-N).
- Kanter der ser forkerte ud (forkert retning, forkert part, forældet ressort) → forkerte_kanter, med kilde.
Søg efter evidens for hvert forslag; foreslå kun med kilde. Brug id-konventionerne (lov-, bek-, vejl-, sty-, naevn-, tilsyn-, kilde-, eu-dir-, eu-reg-). Maks ca. 25 nye noder og 60 nye kanter – prioritér de vigtigste.`, { label: `critic:${c.key}`, phase: 'Critic', schema: CRITIC_SCHEMA })))

const [f, cr] = await Promise.all([fills, critics])
return { fills: f.filter(Boolean).map(x => x.opdateringer.length), critics: cr.filter(Boolean).map(x => [x.nye_noder.length, x.nye_kanter.length, x.forkerte_kanter.length]) }
