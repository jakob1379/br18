export const meta = {
  name: 'dk-reg-huller',
  description: 'Konsolidér 461 rå huller i registry over dansk regulering til en dublet-fri, kategoriseret liste med sporbarhed',
  phases: [{ title: 'Consolidate', detail: 'én agent grupperer; ét kontrolpas finder uplacerede' }],
}
const F = args.file
const SCHEMA = {
  type: 'object',
  properties: {
    huller: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          emne: { type: 'string', description: 'kort, præcis overskrift' },
          type: { type: 'string', enum: ['betalingsmur', 'kun-pdf', 'ingen-api', 'uklart', 'ikke-fundet', 'andet'] },
          beskrivelse: { type: 'string', description: 'samlet beskrivelse: hvad mangler/er uklart, konsekvens for RAG-ingest, evt. hvad der skal til' },
          raa_indeks: { type: 'array', items: { type: 'integer' }, description: 'ALLE i-værdier fra rå-listen der indgår' },
        },
        required: ['emne', 'type', 'beskrivelse', 'raa_indeks'],
      },
    },
  },
  required: ['huller'],
}
phase('Consolidate')
const r = await agent(`Læs HELE filen ${F} med Read (brug offset/limit i bidder af 2000 linjer til du har læst alt). Den indeholder 461 rå "huller" (mangler/usikkerheder) fra en kortlægning af dansk regulering, hvert med indeks i.
Konsolidér dem til en dublet-fri liste: slå poster sammen der handler om samme forhold (fx flere poster om UfR/Karnov-betalingsmur, flere om Retsinformations API, flere om Nævnenes Hus' afgørelsesportaler). Behold forskellige forhold adskilt – også når de ligner hinanden (fx klagevej efter beredskabsloven vs. efter gassikkerhedsloven). Vælg den mest passende type: betalingsmur (inkl. ophavsret på standarder), kun-pdf, ingen-api (ingen API/bulk/maskinel adgang), uklart (ressort, hjemmel, gældende version, status, bestridte kanter), ikke-fundet, andet.
Hvert rå indeks SKAL optræde i præcis én konsolideret post (raa_indeks). Skriv på dansk, sagligt og kort. Bevar konkrete numre/datoer/navne fra de rå poster. Ingen søgning nødvendig.`, { label: 'konsolidér huller', phase: 'Consolidate', schema: SCHEMA })
const used = new Set(r.huller.flatMap(h => h.raa_indeks))
const missing = Array.from({ length: args.n }, (_, i) => i).filter(i => !used.has(i))
let extra = null
if (missing.length) {
  log(`${missing.length} rå huller ikke placeret – kører kontrolpas`)
  extra = await agent(`Læs filen ${F} med Read (i bidder). Følgende rå indeks blev ikke placeret i den konsoliderede liste: ${JSON.stringify(missing)}. Konsolidér KUN disse til poster (samme format); hvis et af dem tydeligt hører under en af disse eksisterende overskrifter, så opret alligevel en post med samme emne-tekst, så de kan flettes: ${JSON.stringify(r.huller.map(h => h.emne))}`, { label: 'kontrolpas', phase: 'Consolidate', schema: SCHEMA })
}
return { n: r.huller.length, missing: missing.length, extra: extra ? extra.huller.length : 0 }
