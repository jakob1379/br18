export const meta = {
  name: 'reguleringskort-qa',
  description: 'Uafhængig QA af HTML-udforskeren: interaktioner i headless Chromium og datakorrekthed mod registry',
  phases: [{ title: 'QA', detail: 'to agenter med hver sin linse; rapporterer kun, retter ikke' }],
}
const SP = args.sp
const SETUP = `
Siden: ${SP}/dk-regulering/reguleringskort.html (et artifact-fragment uden <html>/<body>; wrap det i et minimalt skelet før test, som ${SP}/mmd/shot.js gør).
Test i headless Chromium med Playwright (require('playwright') virker; kør scripts fra mappen ${SP}/mmd hvor node_modules ligger). Netværk er blokeret: rout https://cdn.jsdelivr.net/npm/cytoscape@3.30.2/dist/cytoscape.min.js til ${SP}/mmd/node_modules/cytoscape/dist/cytoscape.min.js og Google Fonts til en tom CSS-respons (se ${SP}/mmd/shot.js for mønstret). Skriv dine egne testscripts i ${SP}/qa/ (opret mappen). RET IKKE i HTML-filen eller i andre filer – rapportér kun.
Data: ${SP}/data/viz_data.json (det indlejrede datasæt) og ${SP}/dk-regulering/registry.yaml (sandheden).
For hvert fund: alvor (kritisk = noget virker ikke/viser forkert data; mellem = forvirrende/inkonsistent; lav = kosmetisk), hvor (fane/komponent), hvordan det reproduceres, forventet vs. faktisk, og et konkret rettelsesforslag (gerne med kodelinje fra HTML-filen). Kun reelle, reproducerede fund – ingen gætterier.`
const SCHEMA = {
  type: 'object',
  properties: {
    fund: { type: 'array', items: { type: 'object', properties: {
      alvor: { type: 'string', enum: ['kritisk', 'mellem', 'lav'] }, hvor: { type: 'string' }, repro: { type: 'string' },
      forventet: { type: 'string' }, faktisk: { type: 'string' }, forslag: { type: 'string' } },
      required: ['alvor', 'hvor', 'repro', 'forventet', 'faktisk', 'forslag'] } },
    testet: { type: 'array', items: { type: 'string' }, description: 'hvad der blev testet og virkede' },
  },
  required: ['fund', 'testet'],
}
phase('QA')
const [a, b] = await parallel([
  () => agent(`${SETUP}
LINSE: FUNKTIONEL TEST AF INTERAKTIONER. Test mindst: (1) søgning (skriv "byggeloven", piletaster, Enter → noden vælges, detaljepanel udfyldes, hash bliver #node-…); (2) klik på node i grafen og på links i detaljepanelet (Udgående/Indgående) – skifter valg korrekt?; (3) "Fokus: naboer", "Fokus: 2 led", "Hele kortet", og at filtre derefter stadig virker; (4) hvert filter (nodetyper, domæner, kanttyper, "Nedlagte og historiske", "Kanter med ukendt sikkerhed", "Nulstil filtre") skjuler/viser det forventede (tæl synlige noder/kanter via cytoscape: grafinstansen er ikke global, men du kan tælle via DOM/visuelt eller tilføje window-eksport i din egen kopi af filen i qa-mappen); (5) Hjemmelskæder: vælg andre udgangspunkter i dropdown, klik på bekendtgørelse i kæden (skal skifte rod), "Åbn i netværket"; (6) Ressort-fanen: klik på instans → netværk; (7) Datakilder: segmentknapper, søgning, sortering pr. kolonne (begge retninger), klik på matrixcelle (filtrerer) og igen (fjerner); tastatur Enter på celle; (8) Huller: typeknapper, domænevælger, søgning, klik på node-link; (9) hash-routing: direkte indlæsning af #ressort, #kilder, #huller, #om, #kaede-lov-planloven, #node-bek-br18, ugyldig hash, browser tilbage/frem; (10) mørk tilstand via colorScheme og via data-theme="dark"/"light" på <html> (graf skal omfarves); (11) telefonbredde 400px: ingen vandret scroll, filtre foldet sammen, alt betjenbart; (12) konsolfejl.`, { label: 'qa:funktionel', phase: 'QA', schema: SCHEMA }),
  () => agent(`${SETUP}
LINSE: DATAKORREKTHED OG FORMIDLING. Kontrollér med egne scripts at det siden viser stemmer med registry.yaml/viz_data.json: (1) opsummeringstal (noder, kanter, aktive ministerier, huller, sikkerhedsfordelingens procenter – genberegn selv); (2) nodetype-tællinger i filterpanelet og domæne-tællinger; (3) for 8 tilfældige noder plus lov-byggeloven, bek-br18, naevn-byggeklageenheden, kilde-retsinformation: detaljepanelets felter, sikkerhedsmærker, kilder, og at "Udgående"/"Indgående" lister præcis kanterne med from=noden/to=noden med rigtige kanttype-etiketter og retning (klageinstans: from er klageinstansen; tjek at ordlyden "← klage til" osv. er sproglig korrekt og ikke vildledende – foreslå bedre ordlyd hvis nødvendigt); (4) Hjemmelskæde for lov-byggeloven og lov-planloven: er hver node i den rigtige kolonne ifølge kantreglerne i buildChain(), mangler der noget åbenlyst?; (5) Ressort-kortene: minister-linjen, tællinger af instanser/love, at nedlagte instanser ikke står som aktive; (6) Datakilder: prioritet = værdi/besvær, sortering, matrixtællinger summer til antal vurderede; (7) Huller: antal pr. type; (8) at kanter markeret [HISTORISK]/[BESTRIDT] i beskrivelsen vises som sådan; (9) dansk sprog og stavning i UI-tekster (labels, knapper, hjælpetekster), og at intet påstår mere sikkerhed end data har.`, { label: 'qa:data', phase: 'QA', schema: SCHEMA }),
])
return { a, b }
