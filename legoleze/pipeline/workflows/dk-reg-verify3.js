export const meta = {
  name: 'dk-reg-verify3',
  description: 'Verificér usikre påstande i registry over dansk regulering node for node (felter, tidligere navne, kanter) med søgebudget',
  phases: [{ title: 'Regler', detail: 'generelle regler med én kilde (ophavsret § 9, EU-genbrug, Retsinformation/EUR-Lex)' }, { title: 'Noder', detail: 'én agent pr. batch af noder' }],
}
const DIR = args.dir
const BUDGET = args.budget || 25
const RULES = `
REGLER
- Dags dato 2026-10-30; tilstanden der kortlægges er pr. 2026-10-28. KUN WebSearch virker (WebFetch er blokeret for alle eksterne domæner) – brug ikke WebFetch.
- SØGEBUDGET: højst ${BUDGET} WebSearch-kald for dig i alt. Budgettet deles med andre agenter; overskrid det ikke. Saml flere noder/spørgsmål i hver søgning når muligt (fx "BEK nr. 1399 2019 bygningsreglement retsinformation ELI hjemmel").
- Kilder: angiv KUN URL’er der optrådte i DINE søgeresultater. Konstruér aldrig URL’er, ELI’er eller API-endpoints.
- verificeret = påstanden fremgår direkte af et søgeresultat fra en officiel/primær kilde (retsinformation.dk, lovtidende.dk, ft.dk, eur-lex.europa.eu, myndighedens eget domæne) eller af to uafhængige troværdige sekundærkilder, og gælder pr. 2026-10-28. sandsynlig = én sekundærkilde, forældet officiel kilde eller faglig slutning. ukendt = intet fundet.
- Opgradér kun med en kilde du selv har set. Er den eksisterende værdi forkert, så ret den (handling "ret") med kilde. Findes intet, så lad være at gætte (handling "ikke_fundet", eller udelad).
- Svar på dansk. Rå data via StructuredOutput.
`
const CLAIM = { kilder: { type: 'array', items: { type: 'string' } }, sikkerhed: { type: 'string', enum: ['verificeret', 'sandsynlig', 'ukendt'] }, begrundelse: { type: 'string' } }
const SCHEMA = {
  type: 'object',
  properties: {
    felter: { type: 'array', items: { type: 'object', properties: {
      id: { type: 'string' },
      felt: { type: 'string', enum: ['hjemmel', 'dokumenttyper', 'url', 'adgang', 'identifikatorer', 'licens', 'opdatering', 'status', 'ministerium'] },
      handling: { type: 'string', enum: ['bekraeft', 'ret', 'ikke_fundet'] },
      vaerdi_json: { type: 'string', description: 'Ved ret: hele feltets nye indhold som JSON uden kilder/sikkerhed – fx {"tekst":"..."} (hjemmel/licens), {"liste":[{"type":"bekendtgørelse","bindende":"bindende"}]} (dokumenttyper), {"vaerdi":"https://..."} (url), {"vaerdier":["ELI","HTML","PDF"],"note":"..."} (adgang), {"eli":"...","lovtidende":"LBK nr. ... af ...","celex":"...","journalnr":"...","andet":"..."} (identifikatorer), {"frekvens":"...","versionshistorik":"..."} (opdatering), {"vaerdi":"aktiv"} (status), {"vaerdi":"min-..."} (ministerium). Ved bekraeft/ikke_fundet: tom streng.' },
      ...CLAIM }, required: ['id', 'felt', 'handling', 'vaerdi_json', 'kilder', 'sikkerhed', 'begrundelse'] } },
    tidligere_navne: { type: 'array', items: { type: 'object', properties: { id: { type: 'string' }, navn: { type: 'string' }, periode: { type: 'string' }, ...CLAIM }, required: ['id', 'navn', 'periode', 'kilder', 'sikkerhed', 'begrundelse'] } },
    kanter: { type: 'array', items: { type: 'object', properties: {
      from: { type: 'string' }, type: { type: 'string' }, to: { type: 'string' },
      handling: { type: 'string', enum: ['bekraeft', 'ret', 'fjern'] },
      beskrivelse: { type: 'string', description: 'ny beskrivelse ved ret, ellers tom' },
      ...CLAIM }, required: ['from', 'type', 'to', 'handling', 'beskrivelse', 'kilder', 'sikkerhed', 'begrundelse'] } },
    noter: { type: 'array', items: { type: 'string' } },
  },
  required: ['felter', 'tidligere_navne', 'kanter', 'noter'],
}
const RULE_SCHEMA = {
  type: 'object',
  properties: {
    regler: { type: 'array', items: { type: 'object', properties: {
      regel: { type: 'string', description: 'kort navn, fx "ophavsret-9-love"' },
      gaelder_for: { type: 'array', items: { type: 'string' }, description: 'nodetyper reglen gælder for, fx ["lov","bekendtgørelse","cirkulære"]' },
      felt: { type: 'string', enum: ['licens', 'opdatering', 'adgang'] },
      vaerdi_json: { type: 'string', description: 'feltets indhold som JSON uden kilder/sikkerhed' },
      ...CLAIM }, required: ['regel', 'gaelder_for', 'felt', 'vaerdi_json', 'kilder', 'sikkerhed', 'begrundelse'] } },
    noter: { type: 'array', items: { type: 'string' } },
  },
  required: ['regler', 'noter'],
}

const jobs = []
if (args.rules) jobs.push(() => agent(`${RULES}
OPGAVE: Find autoritative kilder til generelle forhold, der gælder for hele klasser af noder i et registry over dansk regulering, så felterne licens, opdatering og adgang kan belægges én gang pr. klasse:
1. Ophavsretslovens § 9 (gældende lovbekendtgørelse): love, administrative forskrifter, retsafgørelser og lignende offentlige aktstykker er ikke genstand for ophavsret; stk. 2 om værker der indgår heri. → licens for lov, bekendtgørelse, cirkulære. Find også en autoritativ kilde (fx Kulturministeriet, Kammeradvokaten, Folketinget, juridisk litteratur) om hvorvidt myndigheders vejledninger og afgørelser fra klagenævn/domstole er omfattet → licens for vejledning og praksissamling/afgørelser.
2. Genbrug af EU-retsakter: Kommissionens afgørelse 2011/833/EU og EUR-Lex’ juridiske meddelelse om genbrug. → licens for eu-direktiv, eu-forordning, eu-afgørelse.
3. Retsinformation: at gældende og historiske versioner er tilgængelige, at love konsolideres i lovbekendtgørelser, ELI-identifikatorer, HTML/PDF, og opdatering (løbende/dagligt ved kundgørelse i Lovtidende). → opdatering og adgang for lov, bekendtgørelse, cirkulære (og vejledninger registreret på Retsinformation).
4. EUR-Lex: konsoliderede versioner, ELI, CELEX-nummerets opbygning (officiel hjælpeside), formater (HTML/PDF), og at ændringer og konsolideringer opdateres løbende. → opdatering og adgang for EU-retsakter.
Lav én regel pr. (klasse, felt). vaerdi_json skal være en præcis, generel formulering, der er sand for ALLE noder af de angivne typer (fx {"tekst":"Ikke genstand for ophavsret, jf. ophavsretslovens § 9, stk. 1; værker der indgår, kan være beskyttet (§ 9, stk. 2)."}). Brug sikkerhed verificeret kun når kilden er officiel/primær og siger det direkte.`, { label: 'regler', phase: 'Regler', schema: RULE_SCHEMA }))
for (const i of (args.batches || [])) jobs.push(() => agent(`${RULES}
OPGAVE: Læs HELE filen ${DIR}/batch_${i}.json med Read (brug offset/limit i bidder, hvis den er lang). Den indeholder noder fra et registry over dansk regulering (byggeri, bolig, plan, energi, miljø, arbejdsmiljø, brand, el/gas/VVS). For hver node står "usikre_felter" (felter med sikkerhed sandsynlig/ukendt), "usikre_tidligere_navne" og "usikre_kanter" (kanter der skal efterprøves; "from" er den aktive part, fx klageinstans → førsteinstans, ministerium → lov).
For hver node: efterprøv de usikre felter, tidligere navne og kanter med egne søgninger, så de enten bliver belagt (bekraeft, med kilde og ny sikkerhed), rettet (ret, med ny værdi og kilde) eller markeret som ikke fundet. Prioritér i denne rækkefølge: ministerium/ressort og status pr. 2026-10-28; hjemmel (lov og §, fx "udstedt i medfør af § X i lov om …"); identifikatorer (gældende LBK/BEK/LOV-nr. og dato, ELI, CELEX); kanonisk URL (myndighedens forside, retsinformation-ELI for gældende version, EUR-Lex-side); adgang; dokumenttyper; kanterne; licens og opdatering for dokumentkilder og organisationer. Felterne licens og opdatering for love, bekendtgørelser og EU-retsakter håndteres af en anden agent – spring dem over.
Tip: én søgning på en retsakts titel + "retsinformation" giver ofte nummer, dato, ELI, udsteder og hjemmel på én gang. Én søgning på en myndigheds navn giver typisk forside, ministerium og opgaver.`, { label: `v3:${i}`, phase: 'Noder', schema: SCHEMA }))

const res = await parallel(jobs)
return res.map((r, k) => r ? (r.regler ? { regler: r.regler.length } : { felter: r.felter.length, kanter: r.kanter.length, prev: r.tidligere_navne.length }) : null)
