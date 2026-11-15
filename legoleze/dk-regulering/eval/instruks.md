# Instruks til annotatoren

Du læser danske retsforskrifter og vejledninger og skriver ned, hvad teksten selv siger om fem ting. Svaret bruges som facit, så det skal
være præcist frem for fyldigt.

## Regler

- Brug kun det, der står i opgavefilen. Ingen anden viden, ingen andre filer, intet netopslag.
- Hvert led har et `citat`: de ord i filen, der bærer leddet, kopieret tegn for tegn (samme stavning, tegnsætning og mellemrum). Et citat,
  der ikke står ordret i filen, bliver kasseret.
- Er du i tvivl om et led, så udelad det. En tom liste er et rigtigt svar, når teksten ikke siger noget.
- Skriv ét objekt pr. opgavefil, også når alle lister er tomme.

## Felter

`TYPE` i filens hoved afgør, hvilke felter der er relevante. For en bekendtgørelse udfyldes `hjemmel`, `eu`, `klage` og `tilsyn`, og
`henviser` er tom. For en vejledning udfyldes kun `henviser`.

### hjemmel

Hver retsakt, som `== INDLEDNING ==` nævner som hjemmel ("I medfør af § … i lov om …, jf. lovbekendtgørelse nr. … af …").

- `type`: `lov`, `lovbekendtgørelse`, `bekendtgørelse` eller `anordning`, som teksten skriver det.
- `nr` og `aar`: nummer og årstal fra "nr. 1178 af 23. september 2016" (1178 og 2016).
- `bestemmelser`: de paragraffer, der står foran lovens navn, én streng pr. paragraftegn, med stykke, nummer og litra som skrevet.
  "§ 2, stk. 4, § 3 og § 6, stk. 1, litra a-d," giver `["§ 2, stk. 4", "§ 3", "§ 6, stk. 1, litra a-d"]`.
- `citat`: ordene med nummer og dato, fx `lovbekendtgørelse nr. 1178 af 23. september 2016`.

Tag den version, teksten henviser til med "jf.". Love, der kun står i en ændringsrække ("som ændret ved lov nr. … og lov nr. …"), er ikke
hjemmel og skal ikke med, medmindre teksten siger, at en af de nævnte paragraffer står i netop den lov. En bemyndigelse i en anden
bekendtgørelse ("efter bemyndigelse i henhold til § 18 i bekendtgørelse nr. … af …") er et led med `type` `bekendtgørelse`. En lov, der
kun er nævnt ved navn uden nummer og dato, udelades.

### eu

Hver EU-retsakt, som `== FODNOTER ==` eller indledningen siger, at dokumentet gennemfører ("gennemfører", "indeholder bestemmelser, der
gennemfører", "til gennemførelse af").

- `type`: `direktiv`, `forordning` eller `afgørelse`.
- `aar` og `nr`: "direktiv 2018/844/EU" er 2018 og 844; "direktiv 92/57/EØF" er 1992 og 57; "forordning (EU) nr. 305/2011" er 2011 og
  305; "forordning (EU) 2016/679" er 2016 og 679.
- `citat`: ordene med nummeret, fx `direktiv 2018/844/EU`.

Tag ikke retsakter, der kun står efter "som ændret ved", "om ændring af" eller "om ophævelse af". Tag ikke informationsproceduren
("har som udkast været notificeret i overensstemmelse med direktiv (EU) 2015/1535"): det er ikke gennemførelse.

### klage

Hver bestemmelse under `== BESTEMMELSER OM KLAGE OG TILSYN ==`, der siger, hvem man kan klage til over afgørelser efter dokumentet.

- `afgoerelse_af`: myndigheden, der træffer afgørelsen, som den er nævnt, i grundform ("kommunalbestyrelsen", "Energistyrelsen").
- `klageinstans`: myndigheden, der modtager klagen, med det fulde navn i grundform ("Energiklagenævnet", ikke "nævnet").
- `bestemmelse`: paragraffen fra den firkantede parentes, fx `§ 12`.
- `citat`: den del af sætningen, der nævner klageinstansen.

Udelad bestemmelser, der afskærer klage ("kan ikke påklages til anden administrativ myndighed"), og domstolsprøvelse, medmindre en
bestemt domstol er nævnt ved navn.

### tilsyn

Hver bestemmelse, der siger, hvilken myndighed der fører tilsyn eller kontrol med, at dokumentets regler overholdes.

- `myndighed`: det fulde navn i grundform.
- `bestemmelse` og `citat` som under klage.

Udelad steder, hvor "tilsyn" handler om noget andet end dokumentets egne regler (fx "långivere under tilsyn af Finanstilsynet").

### henviser

Kun for vejledninger: hver lov, lovbekendtgørelse, bekendtgørelse eller anordning, som den viste tekst nævner med nummer og dato.

- `type`, `nr`, `aar` og `citat` som under hjemmel. Hvert dokument én gang.

Cirkulærer, vejledninger og EU-retsakter skal ikke med her.

## Format

En JSON-liste med ét objekt pr. opgavefil:

```json
[
  {
    "id": "lta-2019-1399",
    "hjemmel": [{"type": "lovbekendtgørelse", "nr": 1178, "aar": 2016, "bestemmelser": ["§ 2, stk. 4", "§ 3"], "citat": "lovbekendtgørelse nr. 1178 af 23. september 2016"}],
    "eu": [{"type": "direktiv", "aar": 2018, "nr": 844, "citat": "direktiv 2018/844/EU"}],
    "klage": [{"afgoerelse_af": "kommunalbestyrelsen", "klageinstans": "Byggeklageenheden", "bestemmelse": "§ 12", "citat": "kan påklages til Byggeklageenheden"}],
    "tilsyn": [{"myndighed": "Sikkerhedsstyrelsen", "bestemmelse": "§ 20", "citat": "Sikkerhedsstyrelsen fører tilsyn med"}],
    "henviser": []
  }
]
```
