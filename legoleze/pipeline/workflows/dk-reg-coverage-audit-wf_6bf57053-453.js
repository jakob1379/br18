export const meta = {
  name: 'dk-reg-coverage-audit',
  description: 'Opus xhigh: audit hvad kortlægningen af dansk regulering mangler (retskilder, myndigheder, retsområder, metode) og vurdér dækning pr. retsområde',
  phases: [
    { title: 'Audit', detail: '4 Opus-auditorer med hver sin linse og eget søgebudget', model: 'opus' },
    { title: 'Syntese', detail: 'prioriteret mangelliste + dækningsmatrix pr. retsområde × lag', model: 'opus' },
  ],
}
const SP = args.sp
const BUDGET = args.budget || 35
const AREAS = args.areas
const CTX = `
KONTEKST (læs først; rør ikke filerne – kun læsning og analyse, ingen skrivning):
Projektet kortlægger (henter ikke) alle danske myndigheder og retskilder, der udsteder, fortolker eller håndhæver regulering, til et RAG-korpus (udvidelse af github.com/jakob1379/br18), så søgning kan følge hjemmelskæder lov → bekendtgørelse → vejledning → praksis. Brugeren har udvidet scope: "Alle typer offentlig lovgivning er relevant … Vi skal have alt i denne database af love osv."
To lag:
1) Registry (${SP}/dk-regulering/registry.yaml, 3,7 MB – grep/læs i bidder; kortere: ${SP}/dk-regulering/README.md, huller.md, datakilder.md): 613 håndkuraterede noder (ministerier, styrelser, nævn, love, bekendtgørelser, vejledninger, EU-retsakter, dokumentkilder) og 1.281 kanter for 8 domæner (byggeri, bolig, plan, energi, miljø, arbejdsmiljø, brand, el/gas/VVS). Kanttyper: ressortansvar, delegation, hjemmel_for, udsteder, klageinstans, tilsyn, implementerer_EU, henviser_til. Sikkerhed pr. påstand.
2) Katalog (${SP}/dk-regulering/katalog/README.md; data i retsinformation_lta.jsonl 53 MB, kanter.jsonl, eu_index.jsonl – brug Bash+python3 til optællinger, læs ikke filerne i hele): hele Lovtidende A fra Retsinformation via bulk-høsten github.com/Ansvar-Systems/danish-law-mcp (62.762 dokumenter, 13.819 gældende; status pr. 2026-06-12; udstedelser til 2026-02-12). Kun Lovtidende A (love, lovbekendtgørelser, bekendtgørelser, anordninger) – ingen cirkulærer, vejledninger, skrivelser, Lovtidende B/C, afgørelser. Ingen præambel/hjemmel og ingen EU-noter i teksten. Nuværende ressort og retsområde klassificeres lige nu af Haiku-agenter (2.800 af 13.819 færdige). Pr.-område-fakta: ${SP}/data/coverage.json. Ressortguide brugt til klassifikationen: ${SP}/corpus/jobs/guide.md.
Miljø: Dags dato 2026-11-02. KUN WebSearch virker (WebFetch og direkte HTTP til retsinformation.dk, eur-lex m.fl. er blokeret). SØGEBUDGET: højst ${BUDGET} WebSearch-kald for dig i alt (budgettet deles med andre agenter). Angiv KUN kilde-URL'er, der optrådte i DINE søgeresultater; konstruér aldrig URL'er. Svar på dansk.
Retsområdekoder (brug præcis disse i feltet omraade, eller "tvaergaaende"): ${AREAS.join(', ')}.
`
const FIND = {
  type: 'object',
  properties: {
    fund: { type: 'array', items: { type: 'object', properties: {
      omraade: { type: 'string', description: 'retsområdekode eller tvaergaaende' },
      kategori: { type: 'string', enum: ['retskilde-dokumenttype', 'myndighed', 'klage-tilsyn', 'vejledning-cirkulaere', 'praksis', 'forarbejder', 'eu-international', 'kommunalt-regionalt', 'rigsfaellesskab', 'datakilde-adgang', 'datakvalitet-metode'] },
      emne: { type: 'string' },
      beskrivelse: { type: 'string', description: 'hvad mangler eller er svagt, og hvordan det er konstateret (fil/optælling/søgning)' },
      har_vi: { type: 'string', enum: ['nej', 'delvist', 'kun-metadata'] },
      tilgaengelighed: { type: 'string', enum: ['API', 'bulk', 'HTML', 'PDF', 'betalingsmur', 'ukendt'] },
      volumen: { type: 'string', description: 'skøn over omfang, fx "ca. 3.000 vejledninger"' },
      prioritet: { type: 'integer', minimum: 1, maximum: 5, description: '5 = vigtigst for RAG/hjemmelskæder' },
      naeste_skridt: { type: 'string' },
      kilder: { type: 'array', items: { type: 'string' } },
      sikkerhed: { type: 'string', enum: ['verificeret', 'sandsynlig', 'ukendt'] },
    }, required: ['omraade', 'kategori', 'emne', 'beskrivelse', 'har_vi', 'tilgaengelighed', 'volumen', 'prioritet', 'naeste_skridt', 'kilder', 'sikkerhed'] } },
    noter: { type: 'array', items: { type: 'string' } },
  },
  required: ['fund', 'noter'],
}
const LENSES = [
  { key: 'retskilder', title: 'Retskilder og dokumenttyper', prompt: `LINSE: RETSKILDER OG DOKUMENTTYPER. Lav en udtømmende fortegnelse over typer af offentlig dansk regulering og retskilder, der findes (fx Lovtidende A/B/C, cirkulærer, vejledninger, skrivelser, Folketingstidende/lovforslag og bemærkninger (forarbejder), betænkninger, Ombudsmandens udtalelser (FOB), Ankestyrelsens principmeddelelser, klagenævnsafgørelser, domme (Domsdatabasen, domstol.dk, UfR), SKAT's Juridiske Vejledning, styresignaler, bindende svar, Arbejdstilsynets AT-vejledninger, tekniske forskrifter, kommunale regulativer/lokalplaner/kommuneplaner (Plandata), regionale planer, EU-retsakter og CJEU-praksis, Lovtidende C/traktater, særlovgivning for Grønland og Færøerne, standarder). For hver: dækker registry eller katalog den (tjek filerne)? Hvor findes den, i hvilket format/API, hvor stor er den, og hvor vigtig er den for hjemmelskæder? Fokusér på det, der mangler.` },
  { key: 'myndigheder', title: 'Myndigheder og institutioner', prompt: `LINSE: MYNDIGHEDER OG INSTITUTIONER. Sammenlign registry'ets instansnoder (grep 'type: styrelse|nævn|klagenævn|tilsyn|råd|direktorat|domstol|ombudsmand' i registry.yaml) med hele den danske statsforvaltning pr. 2026-10-28 (21 ministerier efter kgl. res. 3/6/2026). Nu hvor al lovgivning er i scope: hvilke styrelser, direktorater, nævn/klagenævn, tilsyn, råd og selvstændige myndigheder, der udsteder, fortolker eller håndhæver regulering, mangler? Gå ministerium for ministerium (brug katalogets udstedere/ressorter som pejlemærke for hvor meget lovgivning hvert område har). Angiv for hver manglende myndighed område, rolle (udsteder/klageinstans/tilsyn) og om den har en afgørelses- eller vejledningsdatabase.` },
  { key: 'omraader', title: 'Retsområder og dybde', prompt: `LINSE: RETSOMRÅDER OG DYBDE. Brug ${SP}/data/coverage.json og katalogfilerne (klassifikationen er delvis – ekstrapolér forsigtigt, og sig det). For hvert retsområde: hvad har vi (katalog-dokumenter, registry-dybde: myndigheder, klage-/tilsynsveje, vejledninger, praksis, EU-kobling), og hvad mangler for at kunne følge hjemmelskæder lov → bekendtgørelse → vejledning → praksis? Identificér de områder med mest lovgivning og mindst dybde, de vigtigste klage-/tilsynsveje uden for de 8 domæner (fx skat: Skatteankestyrelsen/Landsskatteretten; social: Ankestyrelsen; sundhed: Styrelsen for Patientklager; udlændinge: Udlændingenævnet/Flygtningenævnet; arbejdsmarked; erhverv: Erhvervsankenævnet; konkurrence: Konkurrenceankenævnet osv.), og områder hvor selv Lovtidende A-dækningen er svag (fx dokumenter efter 2026-02-12, grønlandske/færøske anordninger).` },
  { key: 'metode', title: 'Datakvalitet og metode', prompt: `LINSE: DATAKVALITET OG METODE. Find blinde vinkler og fejlkilder i, hvordan vi har afdækket: (a) katalogets afledninger – udstedende ministerium fra DocumentId-præfiks (${SP}/corpus/data/prefixes.json; præfikset CM dækker 17.182 dokumenter før 1998 uden udsteder), lovfamilier og titelmatch (13.187 umatchede "lov om …"-fraser), EU-referencer via regex, implementerer_EU fra samforekomst; (b) ressortguiden (${SP}/corpus/jobs/guide.md) – er der fejl eller huller i forhold til kgl. res. 3/6/2026 / BEK nr. 514 af 08/06/2026 og senere ressortændringer (fx kgl. res. 2/9/2026 om GUDP)? Efterprøv de mest tvivlsomme påstande med søgning; (c) status pr. 2026-06-12 vs. 2026-10-28; (d) registry-noder med forældede versioner. Lav stikprøver med Bash/python3 på katalogfilerne (fx 30 tilfældige gældende dokumenter: er type, udsteder og lovhenvisninger rimelige?). Kvantificér, hvor du kan.` },
]
phase('Audit')
const audits = await parallel(LENSES.map(l => () => agent(`${CTX}\n${l.prompt}\nReturnér 15–40 konkrete fund (prioriteret, ingen gentagelser af det, huller.md allerede siger, medmindre du kan uddybe/kvantificere det) via StructuredOutput.`,
  { label: `audit:${l.key}`, phase: 'Audit', schema: FIND, model: 'opus', effort: 'xhigh' })))
const all = audits.map((a, i) => a ? { linse: LENSES[i].key, ...a } : null).filter(Boolean)
log(`${all.reduce((s, a) => s + a.fund.length, 0)} fund fra ${all.length} auditorer`)
const LAYERS = ['myndigheder', 'klage_tilsyn', 'vejledninger', 'praksis', 'eu_kobling', 'kommunalt']
const SYN = {
  type: 'object',
  properties: {
    mangler: { type: 'array', items: { type: 'object', properties: {
      omraade: { type: 'string' }, kategori: { type: 'string' }, emne: { type: 'string' }, beskrivelse: { type: 'string' },
      tilgaengelighed: { type: 'string' }, volumen: { type: 'string' }, prioritet: { type: 'integer', minimum: 1, maximum: 5 },
      naeste_skridt: { type: 'string' }, kilder: { type: 'array', items: { type: 'string' } }, sikkerhed: { type: 'string', enum: ['verificeret', 'sandsynlig', 'ukendt'] },
      linser: { type: 'array', items: { type: 'string' } },
    }, required: ['omraade', 'kategori', 'emne', 'beskrivelse', 'tilgaengelighed', 'volumen', 'prioritet', 'naeste_skridt', 'kilder', 'sikkerhed', 'linser'] } },
    sammenfatning: { type: 'string' },
  },
  required: ['mangler', 'sammenfatning'],
}
const MATRIX = {
  type: 'object',
  properties: {
    celler: { type: 'array', items: { type: 'object', properties: {
      omraade: { type: 'string' }, lag: { type: 'string', enum: LAYERS },
      daekning: { type: 'integer', minimum: 0, maximum: 100, description: 'skønnet dækning i procent af det, der findes i Danmark for dette område og lag' },
      har: { type: 'string', description: 'kort: hvad vi har (fra registry/katalog)' },
      mangler: { type: 'string', description: 'kort: det vigtigste der mangler' },
      sikkerhed: { type: 'string', enum: ['sandsynlig', 'ukendt'] },
    }, required: ['omraade', 'lag', 'daekning', 'har', 'mangler', 'sikkerhed'] } },
  },
  required: ['celler'],
}
const FUND = JSON.stringify(all)
phase('Syntese')
const [syn, mat] = await parallel([
  () => agent(`${CTX}\nDu er syntetiserende reviewer. Her er fundene fra fire uafhængige auditorer (JSON):\n${FUND}\nSlå dubletter sammen (behold kilder og linser fra alle), kassér fund der modsiges af filerne (tjek dem), og ret prioriteter, så de afspejler værdi for RAG/hjemmelskæder i forhold til besvær. Spørg til sidst dig selv, hvad ingen af auditorerne har dækket (en completeness-kritik), og tilføj det med linse "kritik". Ingen nye søgninger er nødvendige, men du må bruge op til 10. Returnér den samlede, prioriterede mangelliste og en kort sammenfatning via StructuredOutput.`,
    { label: 'syntese:mangler', phase: 'Syntese', schema: SYN, model: 'opus', effort: 'xhigh' }),
  () => agent(`${CTX}\nDu laver en dækningsmatrix til et heatmap. For HVERT retsområde (alle ${AREAS.length} koder) og HVERT af lagene ${LAYERS.join(', ')} skal du skønne, hvor stor en del (0–100 %) af det, der findes i Danmark, vi har kortlagt i registry'et (katalog-laget dækker kun Lovtidende A og tæller ikke her):
- myndigheder: relevante styrelser/nævn/tilsyn/råd for området som noder i registry.
- klage_tilsyn: klageveje og tilsynsrelationer som kanter.
- vejledninger: vejledninger, cirkulærer, tekniske forskrifter som noder/kilder.
- praksis: afgørelsesdatabaser, klagenævn, domstolspraksis som noder/kilder.
- eu_kobling: implementerer_EU-kanter til relevante EU-retsakter.
- kommunalt: kommunale/regionale forskrifter og planer (kun hvor relevant; ellers skøn ud fra relevans).
Brug ${SP}/data/coverage.json (registry_noder/registry_kanter pr. område) og grep i registry.yaml. Områder uden for de 8 domæner har typisk kun ministeriet som node – sæt dem lavt, men skeln mellem 0 og fx 5 %, hvis noget findes. Auditorernes fund (JSON) kan bruges som evidens for hvad der mangler:\n${FUND}\nReturnér præcis ${AREAS.length * LAYERS.length} celler via StructuredOutput. Hold "har" og "mangler" korte (højst ca. 20 ord hver).`,
    { label: 'syntese:matrix', phase: 'Syntese', schema: MATRIX, model: 'opus', effort: 'xhigh' }),
])
return { auditorer: all.map(a => ({ linse: a.linse, fund: a.fund.length })), mangler: syn ? syn.mangler.length : null, celler: mat ? mat.celler.length : null }
