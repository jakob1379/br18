# Evalueringssæt for kæderne

Genereret af `pipeline/corpus/eval.py maal`. Facit står i `facit.jsonl`: ét dokument pr. linje med de led, en annotator har læst i dokumentets egen tekst, hvert med et ordret citat.

## Udtag

302 gældende danske dokumenter med hentet tekst, trukket tilfældigt pr. domæne: hovedbekendtgørelser med og uden registry-node og vejledninger.
Runde 1 er brugt til at finde og rette fejl i udtrækkene, så dens tal er til den pæne side. Runde 2 er trukket bagefter; dens første måling, før noget blev rettet efter den, står i `kontrol-2.json` og i tabellen nedenfor.
Runde 3 er trukket, efter at læseren af klage- og tilsynsbestemmelser var skrevet, og har love og lovbekendtgørelser med i stedet for vejledninger; dens første måling står i `kontrol-3.json`.
Runde 4 har samme grupper som runde 3 og er trukket, efter at læseren var rettet efter runde 1-3 ("påser", "kontrollerer", "er tilsynsmyndighed", "styrelsens kontrol med"); dens første måling står i `kontrol-4.json`. Læseren er siden rettet efter runde 4 og stikprøven nedenfor (2026-11-21 og, for to af stikprøvens fejlklasser, 2026-11-27), så runde 4 er nu også data, læseren er rettet efter.

| Domæne | Runde 1 | Runde 2 | Runde 3 | Runde 4 |
|---|---:|---:|---:|---:|
| arbejdsmiljø | 15 | 10 | 9 | 9 |
| bolig | 15 | 10 | 7 | 7 |
| brand | 14 | 3 | 3 | 0 |
| byggeri | 15 | 10 | 9 | 7 |
| el/gas/VVS | 14 | 8 | 9 | 0 |
| energi | 15 | 10 | 9 | 9 |
| miljø | 15 | 10 | 9 | 9 |
| plan | 15 | 10 | 9 | 8 |

Led i facit: hjemmel 371, eu 181, klage 103, tilsyn 154, henviser 118. Frafaldet i kontrollen: 8 led eller paragraffer. Rettet efter gennemsyn: 7 dokumenter.

## Måling

### Runde 1 (udvikling)

| Mål | Rigtige | Forkerte | Mangler | Præcision | Genfinding |
|---|---:|---:|---:|---:|---:|
| hjemmel_for | 145 | 1 | 0 | 99 % | 100 % |
| hjemmel_for, kun Retsinformations felt | 120 | 1 | 30 | 99 % | 80 % |
| bestemmelser (paragrafnummer) | 441 | 0 | 0 | 100 % | 100 % |
| implementerer_EU | 36 | 0 | 0 | 100 % | 100 % |
| EU-retsakter i XML-metadata (ikke brugt til kanter) | 36 | 28 | 1 | 56 % | 97 % |
| klageinstans pr. forskrift | 18 | 0 | 1 | 100 % | 95 % |
| afgørende myndighed på klagekanten | 7 | 0 | 6 | 100 % | 54 % |
| tilsynsmyndighed pr. forskrift | 14 | 0 | 7 | 100 % | 67 % |
| tilsynsmyndighed er en node | 29 | 0 | 4 | 100 % | 88 % |
| klageinstans er en node | 23 | 0 | 1 | 100 % | 96 % |
| klagekant mellem de to noder | 13 | 0 | 3 | 100 % | 81 % |
| vejledning → retsakt | 81 | – | 0 | – | 100 % |

### Runde 2 (kontrol, nuværende stand)

| Mål | Rigtige | Forkerte | Mangler | Præcision | Genfinding |
|---|---:|---:|---:|---:|---:|
| hjemmel_for | 94 | 0 | 0 | 100 % | 100 % |
| hjemmel_for, kun Retsinformations felt | 85 | 1 | 15 | 99 % | 85 % |
| bestemmelser (paragrafnummer) | 267 | 0 | 0 | 100 % | 100 % |
| implementerer_EU | 26 | 0 | 0 | 100 % | 100 % |
| EU-retsakter i XML-metadata (ikke brugt til kanter) | 27 | 5 | 1 | 84 % | 96 % |
| klageinstans pr. forskrift | 14 | 0 | 0 | 100 % | 100 % |
| afgørende myndighed på klagekanten | 7 | 0 | 3 | 100 % | 70 % |
| tilsynsmyndighed pr. forskrift | 8 | 0 | 0 | 100 % | 100 % |
| tilsynsmyndighed er en node | 11 | 0 | 1 | 100 % | 92 % |
| klageinstans er en node | 16 | 0 | 1 | 100 % | 94 % |
| klagekant mellem de to noder | 7 | 0 | 4 | 100 % | 64 % |
| vejledning → retsakt | 45 | – | 0 | – | 100 % |

### Runde 2 (kontrol, første måling før rettelser efter runden)

| Mål | Rigtige | Forkerte | Mangler | Præcision | Genfinding |
|---|---:|---:|---:|---:|---:|
| hjemmel_for | 99 | 4 | 0 | 96 % | 100 % |
| hjemmel_for, kun Retsinformations felt | 83 | 3 | 16 | 97 % | 84 % |
| bestemmelser (paragrafnummer) | 274 | 1 | 0 | 100 % | 100 % |
| implementerer_EU | 27 | 3 | 1 | 90 % | 96 % |
| EU-retsakter i XML-metadata (ikke brugt til kanter) | 27 | 5 | 1 | 84 % | 96 % |
| tilsynsmyndighed er en node | 11 | 0 | 1 | 100 % | 92 % |
| klageinstans er en node | 15 | 0 | 2 | 100 % | 88 % |
| klagekant mellem de to noder | 6 | 0 | 4 | 100 % | 60 % |
| vejledning → retsakt | 45 | – | 0 | – | 100 % |

### Runde 3 (kontrol, nuværende stand)

| Mål | Rigtige | Forkerte | Mangler | Præcision | Genfinding |
|---|---:|---:|---:|---:|---:|
| hjemmel_for | 46 | 1 | 1 | 98 % | 98 % |
| hjemmel_for, kun Retsinformations felt | 45 | 1 | 9 | 98 % | 83 % |
| implementerer_EU | 49 | 3 | 0 | 94 % | 100 % |
| EU-retsakter i XML-metadata (ikke brugt til kanter) | 55 | 4 | 8 | 93 % | 87 % |
| klageinstans pr. forskrift | 21 | 0 | 1 | 100 % | 95 % |
| afgørende myndighed på klagekanten | 14 | 1 | 4 | 93 % | 78 % |
| tilsynsmyndighed pr. forskrift | 24 | 2 | 4 | 92 % | 86 % |
| bestemmelser (paragrafnummer) | 129 | 0 | 3 | 100 % | 98 % |
| tilsynsmyndighed er en node | 52 | 0 | 6 | 100 % | 90 % |
| klageinstans er en node | 33 | 0 | 1 | 100 % | 97 % |
| klagekant mellem de to noder | 14 | 0 | 5 | 100 % | 74 % |

### Runde 3 (kontrol, første måling før rettelser efter runden)

| Mål | Rigtige | Forkerte | Mangler | Præcision | Genfinding |
|---|---:|---:|---:|---:|---:|
| hjemmel_for | 53 | 2 | 1 | 96 % | 98 % |
| hjemmel_for, kun Retsinformations felt | 44 | 2 | 10 | 96 % | 81 % |
| implementerer_EU | 62 | 3 | 1 | 95 % | 98 % |
| EU-retsakter i XML-metadata (ikke brugt til kanter) | 55 | 4 | 8 | 93 % | 87 % |
| klageinstans pr. forskrift | 23 | 1 | 0 | 96 % | 100 % |
| afgørende myndighed på klagekanten | 12 | 1 | 2 | 92 % | 86 % |
| tilsynsmyndighed pr. forskrift | 15 | 0 | 11 | 100 % | 58 % |
| bestemmelser (paragrafnummer) | 173 | 0 | 4 | 100 % | 98 % |
| tilsynsmyndighed er en node | 44 | 0 | 14 | 100 % | 76 % |
| klageinstans er en node | 32 | 0 | 3 | 100 % | 91 % |
| klagekant mellem de to noder | 10 | 0 | 5 | 100 % | 67 % |

### Runde 4 (kontrol, nuværende stand)

| Mål | Rigtige | Forkerte | Mangler | Præcision | Genfinding |
|---|---:|---:|---:|---:|---:|
| hjemmel_for | 65 | 1 | 0 | 98 % | 100 % |
| hjemmel_for, kun Retsinformations felt | 59 | 1 | 8 | 98 % | 88 % |
| implementerer_EU | 51 | 15 | 2 | 77 % | 96 % |
| EU-retsakter i XML-metadata (ikke brugt til kanter) | 52 | 21 | 1 | 71 % | 98 % |
| klageinstans pr. forskrift | 16 | 4 | 2 | 80 % | 89 % |
| afgørende myndighed på klagekanten | 11 | 1 | 7 | 92 % | 61 % |
| tilsynsmyndighed pr. forskrift | 20 | 1 | 6 | 95 % | 77 % |
| tilsynsmyndighed er en node | 45 | 0 | 6 | 100 % | 88 % |
| klageinstans er en node | 24 | 0 | 4 | 100 % | 86 % |
| bestemmelser (paragrafnummer) | 149 | 0 | 0 | 100 % | 100 % |
| klagekant mellem de to noder | 17 | 0 | 3 | 100 % | 85 % |

### Runde 4 (kontrol, første måling før rettelser efter runden)

| Mål | Rigtige | Forkerte | Mangler | Præcision | Genfinding |
|---|---:|---:|---:|---:|---:|
| hjemmel_for | 67 | 1 | 0 | 99 % | 100 % |
| hjemmel_for, kun Retsinformations felt | 59 | 1 | 8 | 98 % | 88 % |
| implementerer_EU | 50 | 15 | 3 | 77 % | 94 % |
| EU-retsakter i XML-metadata (ikke brugt til kanter) | 52 | 21 | 1 | 71 % | 98 % |
| klageinstans pr. forskrift | 16 | 4 | 2 | 80 % | 89 % |
| afgørende myndighed på klagekanten | 11 | 1 | 7 | 92 % | 61 % |
| tilsynsmyndighed pr. forskrift | 20 | 1 | 6 | 95 % | 77 % |
| tilsynsmyndighed er en node | 45 | 0 | 6 | 100 % | 88 % |
| klageinstans er en node | 24 | 0 | 4 | 100 % | 86 % |
| bestemmelser (paragrafnummer) | 157 | 0 | 0 | 100 % | 100 % |
| klagekant mellem de to noder | 14 | 0 | 6 | 100 % | 70 % |

Rigtige og forkerte tæller katalogets eller registry'ets led, mangler tæller facit-led uden modstykke. Præcision er rigtige af rigtige plus forkerte, genfinding er andelen af facit-leddene, der har et modstykke. For vejledninger er kun genfinding målt.

Facit er teksten, som den er udstedt, så 33 af de 302 dokumenter er holdt ude af de mål, hvor kataloget læser kanterne af en senere ændringsforskrift (feltet `affattet_ved`: hjemmel_for med paragrafnumre og implementerer_EU, det sidste også på katalogpostens `titelfodnote_affattet_ved`, når den nye titelfodnote ikke giver nogen kant; feltet `omdoebt_ved`: klageinstans pr. forskrift med afgørende myndighed og tilsynsmyndighed pr. forskrift); de måles ikke mod facit. "hjemmel_for, kun Retsinformations felt" og målene mod registry'et har alle dokumenter med. Holdt ude pr. mål: hjemmel_for 14 (runde 1: 3, runde 2: 3, runde 3: 6, runde 4: 2); implementerer_EU 19 (runde 1: 3, runde 2: 5, runde 3: 8, runde 4: 3); klageinstans pr. forskrift 2 (runde 1: 0, runde 2: 0, runde 3: 2, runde 4: 0); tilsynsmyndighed pr. forskrift 5 (runde 1: 2, runde 2: 0, runde 3: 3, runde 4: 0). De læsninger er i stedet bedømt blindt mod de ordrette tekster (`aendringer-domme.jsonl`): leddene er dømt af to sprogmodeller hver for sig (en Haiku-agent og en agent på sessionens hovedmodel; 1 led har kun den ene models dom), og de 6 led, hvor de ikke begge sagde rigtig, er afgjort af et gennemsyn. Gennemgående navneskift: 14 af 14 kanter rigtige; ny indledning: 55 af 60 forskrifter rigtige; ny eller ophævet titelfodnote: 37 af 37 forskrifter rigtige; læserens rettelser 2026-11-27 (JGA-201 og JGA-203): 17 af 17 kanter rigtige. I 5 af de 5 forkerte mangler et led, uden at nogen kant er forkert (lta-1994-518, lta-1997-996, lta-2007-1292, lta-2011-176, lta-2013-1289). På de dokumenter og mål, der er holdt ude her, er 39 af 40 domme rigtige. Bedømmelsen dækker alle forskrifter og kanter med de to felter, ikke kun dem i facit. Den måler, om det læste er rigtigt, ikke genfinding: en ændringsforskrift, hvis tekst ikke er hentet, ses ikke. Dommene er afsagt 2026-11-28; de led, rettelserne samme dag ændrede, er dømt igen (3 linjer med `runde`; `MANIFEST.md`, evalueringsafsnittet, nævner rettelserne). Den seneste dom pr. led står sidst i filen og gælder.

## Stikprøve uden for de otte domæner

`stikproeve.jsonl` har 200 kanter fra dokumenternes egne bestemmelser (metode `bestemmelse`) i dokumenter uden for de otte domæner, trukket med frø 20261121 (100 pr. type). Uafhængige dommere har givet hver kant en dom (rigtig, forkert, kan ikke afgøres) med den sætning, dommen hviler på, i `stikproeve-domme.jsonl`; de forkerte, de uafgjorte og dem med forkert afgørende myndighed er gennemset igen mod bestemmelsernes tekst, og gennemsynets dom står i feltet `gennemsyn` ved siden af dommerens. 10 domme er ændret ved gennemsyn. Tallene er målt på læseren, som den var, da stikprøven blev trukket (2026-11-21), før rettelserne efter den.

| Kanttype | Kanter | Rigtige | Forkerte | Kan ikke afgøres | Præcision | Dommernes præcision | Afgørende myndighed rigtig |
|---|---:|---:|---:|---:|---:|---:|---:|
| klageinstans | 100 | 80 | 19 | 1 | 81 % | 78 % | 39 af 40 (98 %) |
| tilsyn | 100 | 92 | 8 | 0 | 92 % | 90 % | – |

Præcision er rigtige af rigtige plus forkerte; "kan ikke afgøres" tæller ikke med. Den afgørende myndighed er kun bedømt for de kanter, der har en.

| Fejlklasse | Kanter | Beskrivelse | Behandling |
|---|---:|---|---|
| klage-over-privat | 4 | klage over en privat virksomheds eller et massemedies afgørelse eller en tvist mellem private læst som klage over en myndigheds afgørelse | kendt grænse (registry meta) |
| domstolsanke | 3 | anke af en dom til en domstol læst som klagevej | rettet i læseren |
| kompetenceafgraensning | 3 | en bestemmelse, der afgrænser et klageorgans kompetence (i dets egen lov eller forretningsorden eller over for et andet organ), læst som klagevej | kendt grænse (registry meta) |
| til-brug-for-tilsyn | 3 | "til brug for X's tilsyn med": oplysninger videregives til et tilsyn efter en anden lov | rettet i læseren |
| bemyndigelse | 2 | ministerens bemyndigelse til at fastsætte regler om klageadgang læst som klagevej (formen "fastsætte regler om, at … kan påklages til X" er rettet i læseren 2026-11-27) | kendt grænse (registry meta) |
| forkert-saetningsled | 2 | klageinstansen taget fra et andet sætningsled (en relativsætning, "adressater for X's afgørelser") | kendt grænse (registry meta) |
| frist-eller-klageberettigelse | 2 | frist- eller klageberettigelsesregel, der forudsætter en klage, men ikke giver klageadgang over dokumentets afgørelser | kendt grænse (registry meta) |
| godkendelse-eller-udbetaling | 2 | kontrol som led i behandlingen af en anmeldelse eller en udbetaling | kendt grænse (registry meta) |
| overgangsregel | 2 | overgangsregel for verserende eller ældre klagesager ("færdigbehandles") | rettet i læseren |
| tilsyn-med-person | 2 | tilsyn med en dømt eller en person under strafferetlige vilkår, ikke med at lovens regler overholdes ("fører tilsyn med den dømte" og "med, at den dømte" er rettet i læseren 2026-11-27) | kendt grænse (registry meta) |
| afgoerelse-sammensat-ord | 1 | afgørende myndighed læst af et sammensat ord ("X's afgørelseskompetence") | rettet i læseren |
| henvisning-til-andet-tilsyn | 1 | omtale af et tilsyn efter anden lovgivning ("den lovgivning, som X fører tilsyn med") | kendt grænse (registry meta) |
| undtagelse-jf-dog | 1 | klagevej, som "jf. dog" lægger hos et andet organ | kendt grænse (registry meta) |

Efter rettelserne i læseren findes 93 af stikprøvens 100 klageinstans-kanter stadig i kataloget (79 rigtige, 13 forkerte, præcision 86 %) og 97 af stikprøvens 100 tilsyn-kanter stadig i kataloget (92 rigtige, 5 forkerte, præcision 95 %). Rettelserne er lavet efter stikprøven, så dette tal er til den pæne side: stikprøven og runde 4 er fra nu af data, læseren er rettet efter, ikke uafhængige kontroller.

## Domstolsprøvelse

`domstolsproevelse-stikproeve.jsonl` har 87 `domstolsproevelse`-kanter på gældende dokumenter (metode `bestemmelse`, alle domæner), trukket med frø 20261124 (højst 100). Kanten siger, at dokumentet giver en særlig vej til domstolen for en myndigheds eller et nævns afgørelse: en bestemt domstol, en frist, et krav om indbringelse eller en pligt for myndigheden til at indbringe sagen. To uafhængige dommere har bedømt hver kant mod bestemmelsernes tekst; hvor de var uenige, eller en af dem ikke sagde rigtig, har et gennemsyn afgjort det (`domstolsproevelse-stikproeve-domme.jsonl`, feltet `gennemsyn`). 5 domme er ændret ved gennemsyn. Tallene er målt på læseren, som den var, da stikprøven blev trukket (2026-11-24).

| Kanter | Rigtige | Forkerte | Kan ikke afgøres | Præcision | Første dommers præcision | Afgørende myndighed rigtig |
|---:|---:|---:|---:|---:|---:|---:|
| 87 | 83 | 4 | 0 | 95 % | 92 % | 22 af 24 (92 %) |

| Fejlklasse | Kanter | Beskrivelse | Behandling |
|---|---:|---|---|
| forkert-afgoerende-myndighed | 2 | afgørende myndighed læst af "klager over afgørelser truffet af X", hvor kun klageinstansens afgørelse kan indbringes | rettet i læseren |
| forkert-domstol | 2 | "retten" sat til en domstol, som en anden sætning i dokumentet nævner uden at give en vej til den | rettet i læseren |
| generel-adgang | 1 | omtale af den almindelige adgang til domstolene uden bestemt domstol, frist, krav eller pligt | rettet i læseren |
| privat-afgoerelse | 1 | afgørelse truffet af private i en tvist mellem private læst som en myndigheds afgørelse (skønsmænd og revisorer er rettet i læseren) | kendt grænse (registry meta) |

Efter rettelserne i læseren er de kanter, der er nye eller har fået andet indhold (bestemmelser, første sætning eller afgørende myndighed), bedømt igen: 24 domme med feltet `runde` i de to filer, hver afsagt af to dommere eller af én dommer og et gennemsyn. Den seneste dom pr. kant gælder. Af de kanter, der har en dom, findes 94 i kataloget nu: 94 rigtige, 0 forkerte og 0, der ikke kan afgøres (præcision 100 %). Rettelserne er lavet efter den første måling, så dette tal er til den pæne side. Genfindingen er ikke målt: en vej til domstolen med andre ord end læserens, eller til en domstol uden node (skifteretten), giver ingen kant.

## Forbehold

- Annotatoren er en sprogmodel (Haiku), ikke en jurist. Hvert led er kontrolleret mekanisk: citatet står ordret i dokumentet, nummer og år står i citatet, og paragrafferne står i indledningen. At citatet betyder det, leddet siger, er kun set efter for de afvigelser, der står som rettet.
- Annotatoren ser indledning og fodnoter og, for forskrifter, de paragraffer, der indeholder et af ordene i `SOEG`; for vejledninger de første 10000 tegn. En klagebestemmelse med andre ord, eller en henvisning længere nede i en vejledning, er ikke i facit.
- Klage og tilsyn pr. forskrift måler katalogets kanter fra dokumentets egne bestemmelser (metode `bestemmelse`). En kant tæller kun med, når mindst én af dens paragraffer blev vist for annotatoren; kanter fra paragraffer uden et af ordene i `SOEG` (fx "fører kontrol med") kan facit ikke indeholde. Facit-led, hvis myndighed ikke er en node, tælles under "er en node" og ikke her.
- Læseren af klage- og tilsynsbestemmelser er rettet til efter afvigelserne i runde 1-3 og, 2026-11-21 og 2026-11-27, efter runde 4 og stikprøven uden for de otte domæner. Den første måling af runde 4 (`kontrol-4.json`) og stikprøvens domme er målt før de rettelser og var de uafhængige kontroller; fra nu af er begge data, læseren er rettet efter, og en ny uafhængig måling kræver en ny runde eller stikprøve.
- "Klagekant mellem de to noder" måler registry'ets kanter mellem myndigheder, ikke katalogets kanter til den enkelte forskrift.
- En hjemmelskant til den gældende version af en omdøbt lov tæller som forkert, når kataloget ikke kobler den citerede version til den gældende. Fra 2026-11-15 kobles gældende loves versioner efter Retsinformations tidslinje; en lov, der er afløst af en ny hovedlov, kobles ikke til afløseren. Det samme gælder vejledningernes kanter, som Retsinformation fører under lovens gældende version.
- Hjemmel i en tekstanmærkning til finansloven eller et aktstykke er ikke i facit og tælles ikke.
- Udtaget er dokumenter fra 2010 og frem i de otte domæner, fordi ældre dokumenter sjældent har tekst i XML. Tallene siger ikke noget om resten af kataloget.
