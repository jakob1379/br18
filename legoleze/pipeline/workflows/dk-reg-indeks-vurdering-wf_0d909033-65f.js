export const meta = {
  name: 'dk-reg-indeks-vurdering',
  description: 'Kortlæg danskelove.dk og jurabibliotek.dk/danske-lov via websøgning og vurdér, hvilke huller i kortlægningen de kan lukke',
  phases: [
    { title: 'Research', detail: 'én agent pr. indeks (kun WebSearch)' },
    { title: 'Verifikation', detail: 'skeptisk efterprøvning af påstandene' },
  ],
}
const SP = args.sp
const CTX = `KONTEKST: Vi kortlægger (henter ikke) dansk regulering til et RAG-korpus med hjemmelskæder lov → bekendtgørelse → vejledning → praksis. Vi har allerede et katalog over hele Lovtidende A fra Retsinformation (62.762 dokumenter, 13.819 gældende, udstedelser til 2026-02-12; se ${SP}/dk-regulering/katalog/README.md). Vores største huller (se ${SP}/dk-regulering/huller.md og ${SP}/data/audit_raw.json, nøglen "syntese:mangler"): 37 % af de gældende dokumenter mangler tekst; præambel/hjemmel og ressortministerium mangler; dokumenter efter 2026-02-12 mangler; cirkulærer, vejledninger, skrivelser og afgørelser mangler; ingen kobling lov ↔ lovforslag/forarbejder; ingen §-ankre; kortnavne for love er ufuldstændige (5.252 "lov om …"-fraser kan ikke matches).
MILJØ: Dags dato 2026-11-02. Sitet selv kan IKKE hentes (WebFetch er blokeret for dets domæne) – brug KUN WebSearch, også med site:-søgninger og forskellige formuleringer. SØGEBUDGET: højst ${args.budget} WebSearch-kald. Angiv kun URL'er, der optrådte i DINE søgeresultater; konstruér aldrig URL'er. Svar på dansk.`
const SITE = {
  type: 'object',
  properties: {
    site: { type: 'string' },
    hvad_er_det: { type: 'string', description: 'kort: hvem driver det, formål, forretningsmodel (gratis/reklame/abonnement)' },
    dokumenttyper: { type: 'array', items: { type: 'object', properties: {
      type: { type: 'string', description: 'fx lov, lovbekendtgørelse, bekendtgørelse, cirkulære, vejledning, afgørelse, dom, forarbejder, EU' },
      daekket: { type: 'string', enum: ['ja', 'delvist', 'nej', 'ukendt'] }, omfang: { type: 'string' }, kilder: { type: 'array', items: { type: 'string' } },
      sikkerhed: { type: 'string', enum: ['verificeret', 'sandsynlig', 'ukendt'] } }, required: ['type', 'daekket', 'omfang', 'kilder', 'sikkerhed'] } },
    felter: { type: 'array', items: { type: 'object', properties: {
      felt: { type: 'string', description: 'fx kortnavn, ministerium/ressort, hjemmel, Lovtidende-nr., ELI, ikrafttræden, ændringshistorik, §-niveau-sider, retsområde/kategori, link til Retsinformation, forarbejder, praksis' },
      findes: { type: 'string', enum: ['ja', 'delvist', 'nej', 'ukendt'] }, eksempel: { type: 'string' }, kilder: { type: 'array', items: { type: 'string' } },
      sikkerhed: { type: 'string', enum: ['verificeret', 'sandsynlig', 'ukendt'] } }, required: ['felt', 'findes', 'eksempel', 'kilder', 'sikkerhed'] } },
    struktur: { type: 'string', description: 'URL-mønstre og opbygning (alfabetisk, retsområder, ministerier, §-sider), som de ses i søgeresultaterne' },
    eksempel_urler: { type: 'array', items: { type: 'object', properties: { url: { type: 'string' }, titel: { type: 'string' } }, required: ['url', 'titel'] } },
    aktualitet: { type: 'string', description: 'hvor opdateret: nyeste lovversioner set (fx LBK-numre fra 2025/2026), opdateringsfrekvens' },
    adgang: { type: 'string', description: 'API, sitemap, bulk, kun HTML; robots/vilkår hvis set' },
    licens_vilkaar: { type: 'string' },
    kan_lukke: { type: 'array', items: { type: 'object', properties: {
      hul: { type: 'string' }, vurdering: { type: 'string', enum: ['lukker', 'delvist', 'nej'] }, begrundelse: { type: 'string' } }, required: ['hul', 'vurdering', 'begrundelse'] } },
    noter: { type: 'array', items: { type: 'string' } },
  },
  required: ['site', 'hvad_er_det', 'dokumenttyper', 'felter', 'struktur', 'eksempel_urler', 'aktualitet', 'adgang', 'licens_vilkaar', 'kan_lukke', 'noter'],
}
const SITES = [
  { key: 'danskelove', url: 'https://danskelove.dk', hint: 'Undersøg bl.a. om der er sider pr. paragraf (fx danskelove.dk/<kortnavn>/<paragraf>), om bekendtgørelser og vejledninger er med, om kortnavne og ministerier vises, om der er links til lovforslag/bemærkninger, og hvor nye versionerne er.' },
  { key: 'jurabibliotek', url: 'https://www.jurabibliotek.dk/danske-lov', hint: 'Undersøg hvad jurabibliotek.dk er (bibliotek, abonnement, gratis), hvad siden /danske-lov indeholder (liste over love? retsområder? kortnavne? links til Retsinformation?), og hvilke andre sektioner sitet har (fx bekendtgørelser, domme, vejledninger).' },
]
phase('Research')
const res = await pipeline(SITES,
  s => agent(`${CTX}\nOPGAVE: Kortlæg indekset ${s.url} så præcist som muligt ud fra søgeresultater. ${s.hint} Vurdér for hvert af vores huller, om sitet kan lukke det, hvis domænet blev tilladt. Returnér via StructuredOutput.`,
    { label: `research:${s.key}`, phase: 'Research', schema: SITE, effort: 'high' }),
  (r, s) => r && agent(`${CTX}\nDu er skeptisk kontrollant. En anden agent har kortlagt ${s.url} ud fra søgeresultater (JSON):\n${JSON.stringify(r)}\nEfterprøv de vigtigste påstande med egne søgninger (højst ${args.verify_budget} kald): dokumenttyper og omfang, felter (særligt ministerium, hjemmel, kortnavne, §-sider, forarbejder), aktualitet og vilkår. Ret det, der er forkert, nedgradér sikkerheden på det, du ikke kan bekræfte, og fjern URL'er, der ikke findes i søgeresultater. Returnér den rettede kortlægning i samme format via StructuredOutput, og skriv i noter, hvad du har rettet.`,
    { label: `verify:${s.key}`, phase: 'Verifikation', schema: SITE, effort: 'high' }).then(v => ({ research: r, verified: v })))
return res.map(x => x && ({ site: (x.verified || x.research || {}).site, typer: ((x.verified || x.research || {}).dokumenttyper || []).length }))
