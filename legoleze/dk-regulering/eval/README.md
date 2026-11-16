# Evalueringssæt for kæderne

Genereret af `pipeline/corpus/eval.py maal`. Facit står i `facit.jsonl`: ét dokument pr. linje med de led, en annotator har læst i dokumentets egen tekst, hvert med et ordret citat.

## Udtag

253 gældende danske dokumenter med hentet tekst, trukket tilfældigt pr. domæne: hovedbekendtgørelser med og uden registry-node og vejledninger.
Runde 1 er brugt til at finde og rette fejl i udtrækkene, så dens tal er til den pæne side. Runde 2 er trukket bagefter; dens første måling, før noget blev rettet efter den, står i `kontrol-2.json` og i tabellen nedenfor.
Runde 3 er trukket, efter at læseren af klage- og tilsynsbestemmelser var skrevet, og har love og lovbekendtgørelser med i stedet for vejledninger; dens første måling står i `kontrol-3.json`.

| Domæne | Runde 1 | Runde 2 | Runde 3 |
|---|---:|---:|---:|
| arbejdsmiljø | 15 | 10 | 9 |
| bolig | 15 | 10 | 7 |
| brand | 14 | 3 | 3 |
| byggeri | 15 | 10 | 9 |
| el/gas/VVS | 14 | 8 | 9 |
| energi | 15 | 10 | 9 |
| miljø | 15 | 10 | 9 |
| plan | 15 | 10 | 9 |

Led i facit: hjemmel 304, eu 128, klage 76, tilsyn 103, henviser 118. Frafaldet i kontrollen: 8 led eller paragraffer. Rettet efter gennemsyn: 6 dokumenter.

## Måling

### Runde 1 (udvikling)

| Mål | Rigtige | Forkerte | Mangler | Præcision | Genfinding |
|---|---:|---:|---:|---:|---:|
| hjemmel_for | 150 | 1 | 0 | 99 % | 100 % |
| hjemmel_for, kun Retsinformations felt | 120 | 1 | 30 | 99 % | 80 % |
| bestemmelser (paragrafnummer) | 451 | 0 | 0 | 100 % | 100 % |
| implementerer_EU | 37 | 0 | 0 | 100 % | 100 % |
| EU-retsakter i XML-metadata (ikke brugt til kanter) | 36 | 28 | 1 | 56 % | 97 % |
| klageinstans pr. forskrift | 18 | 0 | 1 | 100 % | 95 % |
| afgørende myndighed på klagekanten | 7 | 0 | 6 | 100 % | 54 % |
| tilsynsmyndighed pr. forskrift | 16 | 0 | 7 | 100 % | 70 % |
| tilsynsmyndighed er en node | 29 | 0 | 4 | 100 % | 88 % |
| klageinstans er en node | 23 | 0 | 1 | 100 % | 96 % |
| klagekant mellem de to noder | 13 | 0 | 3 | 100 % | 81 % |
| vejledning → retsakt | 81 | – | 0 | – | 100 % |

### Runde 2 (kontrol, nuværende stand)

| Mål | Rigtige | Forkerte | Mangler | Præcision | Genfinding |
|---|---:|---:|---:|---:|---:|
| hjemmel_for | 100 | 1 | 0 | 99 % | 100 % |
| hjemmel_for, kun Retsinformations felt | 85 | 1 | 15 | 99 % | 85 % |
| bestemmelser (paragrafnummer) | 278 | 0 | 0 | 100 % | 100 % |
| implementerer_EU | 28 | 0 | 0 | 100 % | 100 % |
| EU-retsakter i XML-metadata (ikke brugt til kanter) | 27 | 5 | 1 | 84 % | 96 % |
| klageinstans pr. forskrift | 14 | 0 | 0 | 100 % | 100 % |
| afgørende myndighed på klagekanten | 7 | 0 | 3 | 100 % | 70 % |
| tilsynsmyndighed pr. forskrift | 8 | 0 | 0 | 100 % | 100 % |
| tilsynsmyndighed er en node | 11 | 0 | 1 | 100 % | 92 % |
| klageinstans er en node | 16 | 0 | 1 | 100 % | 94 % |
| klagekant mellem de to noder | 6 | 0 | 5 | 100 % | 55 % |
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
| hjemmel_for | 53 | 2 | 1 | 96 % | 98 % |
| hjemmel_for, kun Retsinformations felt | 44 | 2 | 10 | 96 % | 81 % |
| implementerer_EU | 62 | 3 | 1 | 95 % | 98 % |
| EU-retsakter i XML-metadata (ikke brugt til kanter) | 55 | 4 | 8 | 93 % | 87 % |
| klageinstans pr. forskrift | 24 | 0 | 1 | 100 % | 96 % |
| afgørende myndighed på klagekanten | 14 | 1 | 5 | 93 % | 74 % |
| tilsynsmyndighed pr. forskrift | 27 | 2 | 4 | 93 % | 87 % |
| bestemmelser (paragrafnummer) | 173 | 0 | 4 | 100 % | 98 % |
| tilsynsmyndighed er en node | 52 | 0 | 6 | 100 % | 90 % |
| klageinstans er en node | 34 | 0 | 1 | 100 % | 97 % |
| klagekant mellem de to noder | 11 | 0 | 9 | 100 % | 55 % |

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

Rigtige og forkerte tæller katalogets eller registry'ets led, mangler tæller facit-led uden modstykke. Præcision er rigtige af rigtige plus forkerte, genfinding er andelen af facit-leddene, der har et modstykke. For vejledninger er kun genfinding målt.

## Forbehold

- Annotatoren er en sprogmodel (Haiku), ikke en jurist. Hvert led er kontrolleret mekanisk: citatet står ordret i dokumentet, nummer og år står i citatet, og paragrafferne står i indledningen. At citatet betyder det, leddet siger, er kun set efter for de afvigelser, der står som rettet.
- Annotatoren ser indledning og fodnoter og, for forskrifter, de paragraffer, der indeholder et af ordene i `SOEG`; for vejledninger de første 10000 tegn. En klagebestemmelse med andre ord, eller en henvisning længere nede i en vejledning, er ikke i facit.
- Klage og tilsyn pr. forskrift måler katalogets kanter fra dokumentets egne bestemmelser (metode `bestemmelse`). En kant tæller kun med, når mindst én af dens paragraffer blev vist for annotatoren; kanter fra paragraffer uden et af ordene i `SOEG` (fx "fører kontrol med") kan facit ikke indeholde. Facit-led, hvis myndighed ikke er en node, tælles under "er en node" og ikke her.
- Læseren af klage- og tilsynsbestemmelser er rettet til efter afvigelserne i begge runder, så ingen af runderne er en uafhængig kontrol af den.
- "Klagekant mellem de to noder" måler registry'ets kanter mellem myndigheder, ikke katalogets kanter til den enkelte forskrift.
- En hjemmelskant til den gældende version af en omdøbt lov tæller som forkert, når kataloget ikke kobler den citerede version til den gældende. Fra 2026-11-15 kobles gældende loves versioner efter Retsinformations tidslinje; en lov, der er afløst af en ny hovedlov, kobles ikke til afløseren. Det samme gælder vejledningernes kanter, som Retsinformation fører under lovens gældende version.
- Hjemmel i en tekstanmærkning til finansloven eller et aktstykke er ikke i facit og tælles ikke.
- Udtaget er dokumenter fra 2010 og frem i de otte domæner, fordi ældre dokumenter sjældent har tekst i XML. Tallene siger ikke noget om resten af kataloget.
