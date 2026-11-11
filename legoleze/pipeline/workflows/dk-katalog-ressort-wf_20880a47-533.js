export const meta = {
  name: 'dk-katalog-ressort',
  description: 'Haiku: klassificér gældende Retsinformation-dokumenter efter nuværende ressortministerium og retsområde (ingen websøgning)',
  phases: [{ title: 'Klassifikation', detail: 'én Haiku-agent pr. batch á 280 dokumenter' }],
}
const DIR = args.dir
const M = ['STM','OIM','UM','EM','FM','JM','FUD','KEFM','BLT','UIM','UVM','BLM','FMN','SVM','SKM','MND','KUM','MSB','BAB','SOM','MIM','FT','UKENDT']
const O = ['statsret','kommuner','valg','international','forsvar','beredskab-brand','strafferet-politi','retspleje','familie-person','erhvervsret','finansiel','skat','offentlig-oekonomi','arbejdsmarked','arbejdsmiljoe','social','aeldre','boern-dagtilbud','sundhed','undervisning','forskning-videregaaende','kultur-medier','kirke','udlaendinge','transport','soefart','plan-landdistrikter','byggeri','bolig','energi-forsyning','klima','el-gas-vvs','miljoe','affald','natur-vandmiljoe','landbrug-dyr','foedevarer','fiskeri','digitalisering-tele','persondata','forbruger-konkurrence','andet']
const SCHEMA = {
  type: 'object',
  properties: {
    items: { type: 'array', items: { type: 'object', properties: {
      id: { type: 'string' },
      m: { type: 'string', enum: M, description: 'nuværende ressortministerium (kode fra guiden)' },
      o: { type: 'string', enum: O, description: 'retsområde' },
      s: { type: 'string', enum: ['s', 'u'], description: 's = sandsynlig (titlens emne og/eller udsteder peger klart på ministeriet), u = usikkert gæt' },
    }, required: ['id', 'm', 'o', 's'] } },
  },
  required: ['items'],
}
const jobs = (args.batches || []).map(b => () => agent(`Du klassificerer danske retsforskrifter fra Retsinformation (Lovtidende A). INGEN websøgning og INGEN WebFetch – brug kun Read på de to filer nedenfor.
1. Læs HELE ressortguiden ${DIR}/guide.md.
2. Læs HELE ${DIR}/ressort/batch_${b}.jsonl (én JSON-linje pr. dokument: id, t = dokumenttype, aar = udstedelsesår, titel, udsteder = det ministerium der udstedte dokumentet dengang, udledt af Retsinformations dokument-id; "ukendt" hvis ikke udledt). Filen har ca. 280 linjer – læs den i bidder med offset/limit, hvis nødvendigt, og spring ingen linjer over.
For HVERT dokument:
- m: hvilket NUVÆRENDE ministerium (pr. 2026-10-28, guidens koder) der har ressortansvaret for dokumentets emne i dag. Gå ud fra titlens emne og brug udsteder + afsnittet "Historiske ministerier → nuværende" til at følge ressortomlægninger. Eksempel: en bekendtgørelse om almene boliger udstedt af Social- og Boligministeriet → BAB; om fiskeri udstedt af Ministeriet for Fødevarer, Landbrug og Fiskeri → MIM; om dagpenge → BLM; en traktat-bekendtgørelse → UM; en anordning om ikrafttræden for Grønland/Færøerne af en lov → det ministerium der har ressort for den pågældende lov.
- o: retsområde (én kode fra guidens liste).
- s: "s" når emnet klart hører under ministeriet efter guiden (eller udsteder uden ressortændring dækker emnet); "u" når det er et usikkert gæt (fx uklar titel, udsteder ukendt og emnet tvetydigt, eller emnet ikke står i guiden).
Returnér præcis ét element pr. id i batchen – ingen udeladelser, ingen dubletter, ingen nye id'er. Rå data via StructuredOutput.`, { label: `ressort:${b}`, phase: 'Klassifikation', schema: SCHEMA, model: 'haiku', effort: 'high' }))
const res = await parallel(jobs)
return res.map(r => r ? r.items.length : null)
