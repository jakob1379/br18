# Evalueringssæt for kæderne

Genereret af `pipeline/corpus/eval.py maal`. Facit står i `facit.jsonl`: ét dokument pr. linje med de led, en annotator har læst i dokumentets egen tekst, hvert med et ordret citat.

## Udtag

189 gældende danske dokumenter med hentet tekst, trukket tilfældigt pr. domæne: hovedbekendtgørelser med og uden registry-node og vejledninger.
Runde 1 er brugt til at finde og rette fejl i udtrækkene, så dens tal er til den pæne side. Runde 2 er trukket bagefter; dens første måling, før noget blev rettet efter den, står i `kontrol-2.json` og i tabellen nedenfor.

| Domæne | Runde 1 | Runde 2 |
|---|---:|---:|
| arbejdsmiljø | 15 | 10 |
| bolig | 15 | 10 |
| brand | 14 | 3 |
| byggeri | 15 | 10 |
| el/gas/VVS | 14 | 8 |
| energi | 15 | 10 |
| miljø | 15 | 10 |
| plan | 15 | 10 |

Led i facit: hjemmel 250, eu 65, klage 40, tilsyn 44, henviser 118. Frafaldet i kontrollen: 2 led eller paragraffer. Rettet efter gennemsyn: 3 dokumenter.

## Måling

### Runde 1 (udvikling)

| Mål | Rigtige | Forkerte | Mangler | Præcision | Genfinding |
|---|---:|---:|---:|---:|---:|
| hjemmel_for | 150 | 2 | 0 | 99 % | 100 % |
| hjemmel_for, kun Retsinformations felt | 119 | 2 | 31 | 98 % | 79 % |
| bestemmelser (paragrafnummer) | 451 | 0 | 0 | 100 % | 100 % |
| implementerer_EU | 37 | 0 | 0 | 100 % | 100 % |
| EU-retsakter i XML-metadata (ikke brugt til kanter) | 36 | 28 | 1 | 56 % | 97 % |
| tilsynsmyndighed er en node | 27 | 0 | 5 | 100 % | 84 % |
| klageinstans er en node | 20 | 0 | 3 | 100 % | 87 % |
| klagekant mellem de to noder | 11 | 0 | 5 | 100 % | 69 % |
| vejledning → retsakt | 80 | – | 0 | – | 100 % |

### Runde 2 (kontrol, nuværende stand)

| Mål | Rigtige | Forkerte | Mangler | Præcision | Genfinding |
|---|---:|---:|---:|---:|---:|
| hjemmel_for | 100 | 3 | 0 | 97 % | 100 % |
| hjemmel_for, kun Retsinformations felt | 83 | 3 | 17 | 97 % | 83 % |
| bestemmelser (paragrafnummer) | 278 | 0 | 0 | 100 % | 100 % |
| implementerer_EU | 28 | 0 | 0 | 100 % | 100 % |
| EU-retsakter i XML-metadata (ikke brugt til kanter) | 27 | 5 | 1 | 84 % | 96 % |
| tilsynsmyndighed er en node | 11 | 0 | 1 | 100 % | 92 % |
| klageinstans er en node | 15 | 0 | 2 | 100 % | 88 % |
| klagekant mellem de to noder | 6 | 0 | 4 | 100 % | 60 % |
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

Rigtige og forkerte tæller katalogets eller registry'ets led, mangler tæller facit-led uden modstykke. Præcision er rigtige af rigtige plus forkerte, genfinding er andelen af facit-leddene, der har et modstykke. For vejledninger er kun genfinding målt.

## Forbehold

- Annotatoren er en sprogmodel (Haiku), ikke en jurist. Hvert led er kontrolleret mekanisk: citatet står ordret i dokumentet, nummer og år står i citatet, og paragrafferne står i indledningen. At citatet betyder det, leddet siger, er kun set efter for de afvigelser, der står som rettet.
- Annotatoren ser indledning og fodnoter og, for forskrifter, de paragraffer, der indeholder et af ordene i `SOEG`; for vejledninger de første 10000 tegn. En klagebestemmelse med andre ord, eller en henvisning længere nede i en vejledning, er ikke i facit.
- Klage og tilsyn måler kun, om myndigheden findes som node under samme navn, og om der er en klagekant mellem de to myndigheder. Registry'et knytter ikke klageadgangen til den enkelte forskrift.
- En hjemmelskant til den gældende version af en omdøbt lov tæller som forkert, når kataloget ikke kobler den citerede version til den gældende. Det samme gælder vejledningernes kanter, som Retsinformation fører under lovens gældende version.
- Hjemmel i en tekstanmærkning til finansloven eller et aktstykke er ikke i facit og tælles ikke.
- Udtaget er dokumenter fra 2010 og frem i de otte domæner, fordi ældre dokumenter sjældent har tekst i XML. Tallene siger ikke noget om resten af kataloget.
