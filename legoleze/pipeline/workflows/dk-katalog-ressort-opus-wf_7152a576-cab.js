export const meta = {
  name: 'dk-katalog-ressort-opus',
  description: 'Opus: genklassificér usikre ressort-klassifikationer og verificér en stratificeret stikprøve af de sikre (ingen websøgning)',
  phases: [
    { title: 'Genklassificering', detail: 'Opus high på de 1.755 usikre dokumenter', model: 'opus' },
    { title: 'Stikprøve', detail: 'uafhængig Opus-kontrol af 437 "sandsynlige" (20 pr. ministerium)', model: 'opus' },
  ],
}
const DIR = args.dir
const M = ['STM','OIM','UM','EM','FM','JM','FUD','KEFM','BLT','UIM','UVM','BLM','FMN','SVM','SKM','MND','KUM','MSB','BAB','SOM','MIM','FT','UKENDT']
const O = ['statsret','kommuner','valg','international','forsvar','beredskab-brand','strafferet-politi','retspleje','familie-person','erhvervsret','finansiel','skat','offentlig-oekonomi','arbejdsmarked','arbejdsmiljoe','social','aeldre','boern-dagtilbud','sundhed','undervisning','forskning-videregaaende','kultur-medier','kirke','udlaendinge','transport','soefart','plan-landdistrikter','byggeri','bolig','energi-forsyning','klima','el-gas-vvs','miljoe','affald','natur-vandmiljoe','landbrug-dyr','foedevarer','fiskeri','digitalisering-tele','persondata','forbruger-konkurrence','andet']
const RE = { type: 'object', properties: { items: { type: 'array', items: { type: 'object', properties: {
  id: { type: 'string' }, m: { type: 'string', enum: M }, o: { type: 'string', enum: O }, s: { type: 'string', enum: ['s', 'u'] } }, required: ['id', 'm', 'o', 's'] } } }, required: ['items'] }
const VER = { type: 'object', properties: { items: { type: 'array', items: { type: 'object', properties: {
  id: { type: 'string' }, ministerium_korrekt: { type: 'string', enum: ['ja', 'nej', 'tvivl'] }, rettet_m: { type: 'string', enum: M },
  omraade_korrekt: { type: 'string', enum: ['ja', 'nej', 'tvivl'] }, rettet_o: { type: 'string', enum: O }, begrundelse: { type: 'string' } },
  required: ['id', 'ministerium_korrekt', 'rettet_m', 'omraade_korrekt', 'rettet_o', 'begrundelse'] } } }, required: ['items'] }
const COMMON = `Du arbejder med danske retsforskrifter fra Retsinformation (Lovtidende A). INGEN websøgning og INGEN WebFetch – brug kun Read. Læs først HELE ressortguiden ${DIR}/guide_v2.md (ressortfordeling pr. 2026-10-28 efter kgl. res. 3/6/2026 / BEK 514/2026, særregler og historiske ministerier → nuværende).`
phase('Genklassificering')
const re = args.recheck.map(b => () => agent(`${COMMON}
Læs derefter HELE ${DIR}/recheck/batch_${b}.jsonl (én JSON-linje pr. dokument: id, t = type, aar, titel, udsteder = udstedende ministerium dengang). En hurtigere model var usikker på netop disse dokumenter. Klassificér hvert dokument omhyggeligt:
- m: det NUVÆRENDE ressortministerium (guidens koder) for dokumentets emne. Tænk over hvilken lov dokumentet typisk er udstedt efter, og følg ressortomlægningerne fra udsteder til i dag. Ikrafttrædelsesanordninger for Grønland/Færøerne følger den pågældende lovs ressort.
- o: retsområde (guidens koder).
- s: "s" når du med rimelig sikkerhed kan placere emnet efter guiden; "u" kun når emnet reelt er tvetydigt eller ukendt.
Returnér præcis ét element pr. id via StructuredOutput.`, { label: `opus-re:${b}`, phase: 'Genklassificering', schema: RE, model: 'opus', effort: 'high' }))
const ve = args.sample.map(b => () => agent(`${COMMON}
Læs derefter HELE ${DIR}/sample/batch_${b}.jsonl. Hver linje er et dokument (id, t, aar, titel, udsteder) med en klassifikation fra en anden model: klassificeret_m (nuværende ressortministerium) og klassificeret_o (retsområde). Vær en skeptisk kontrollant: afgør uafhængigt for hvert dokument, om klassifikationen er korrekt pr. 2026-10-28 efter guiden.
- ministerium_korrekt: ja/nej/tvivl; rettet_m: dit bud (samme kode, hvis korrekt).
- omraade_korrekt: ja/nej/tvivl; rettet_o: dit bud.
- begrundelse: højst 20 ord.
Returnér præcis ét element pr. id via StructuredOutput.`, { label: `opus-ver:${b}`, phase: 'Stikprøve', schema: VER, model: 'opus', effort: 'high' }))
const res = await parallel([...re, ...ve])
return res.map(r => r ? r.items.length : null)
