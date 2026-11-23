#!/usr/bin/env python3
"""Retsinformations søgeeksport som kilde til kataloget og til fortegnelsen over administrative forskrifter.

    python3 eksport.py hent       # metadata for alle dokumenter pr. samling -> intermediate/corpus/eksport/<samling>.jsonl
    python3 eksport.py hent lta 2025 [TIL]  # ét kald: samlingens dokumenter fra året (til og med TIL) flettes ind i <samling>.jsonl med feltet Hentet (dagens dato)
    python3 eksport.py katalog    # ajourfør katalog/retsinformation_<samling>.jsonl og kanter.jsonl fra eksporten (kræver PyYAML)
    python3 eksport.py unavngivne # de navne i klage- og tilsynssætningerne, registry'et ikke har, som TSV (navn, sætninger, dokumenter, eksempel)
    python3 eksport.py selftest

Eksporten er sidens egen "Eksportér søgeresultat" (api/documentsearch/csv). Ét kald giver alle dokumenter i en samling for et
årsinterval med type, titel, ressort, myndighed, status, hjemmel (accessionsnumre), ændringer og ELI-adresse. Intervallerne lægges
efter sitemap-fortegnelsen (populate.py sitemap), så hvert kald giver ca. 3.000 dokumenter, og alle samlinger hentes på under 100 kald.
Kaldene går gennem populate.get, som holder 10,5 sekunder mellem kald til Retsinformation og husker svarene.

Status og ressortfelt dateres med den dag, eksporten blev hentet (eksport/hentet), ikke med den dag, kataloget bygges. En række fra en
delvis hentning har sin egen dato i feltet Hentet, og den bruges i stedet; eksport/hentet ændres ikke af den.

katalog gør fem ting med Lovtidende A: tilføjer de dokumenter, kataloget mangler; sætter status for alle dokumenter til eksportens;
peger lovfamilier på den nyeste gældende version; skriver hjemmel_for-kanter fra eksportens hjemmelsfelt; og sætter ministerium fra
Retsinformations ressortfelt på alle gældende dokumenter, hvor feltet med sikkerhed er aktuelt (populate.ressort). Nye gældende
dokumenter uden et sådant felt får ministerium og retsområde fra den lov, de er udstedt efter eller ændrer. Resten står i
eksport/klassifikation_job.json; svarene læses fra eksport/klassifikation.json. Ressortkanter til dokumenter, der ikke længere gælder, fjernes.

De øvrige samlinger (ANDRE: Lovtidende B og C, Ministerialtidende, administrative forskrifter og afgørelser, Folketingets Ombudsmand og
Folketingstidende) skrives som katalog/retsinformation_<samling>.jsonl direkte fra eksporten. Hjemmelsfeltet kobler dem til lovgivningen
(hjemmelkant), og gældende dokumenter får ministerium fra ressortfeltet efter samme regel eller arver ministerium og retsområde fra den
lovgivning, de vedrører. I Folketingstidende har alle dokumenter om samme lovforslag samme nøgle i feltet lovforslag, og den vedtagne tekst
har feltet lov: den lov, den blev til (lovkobling). Lovforslagets dokumenter får en henviser_til-kant til loven (forarbejde, sandsynlig).
Afgørelser, udtalelser og domme får en udsteder-kant fra den instans i registry'et, der har samme navn som eksportens AdministrerendeMyndighed
(myndigheder). For bekendtgørelser bruges feltet ikke: dér er det den myndighed, der administrerer reglerne, ikke altid den, der har udstedt dem.

katalog læser også katalog/tekst.jsonl (tekst.py). For forskrifter, hvis XML er hentet, lægges de bestemmelser i loven, præamblen nævner, på
hjemmel_for-kanten (from_bestemmelse, og citeret_version når præamblen citerer en anden version end Retsinformations), og en lov eller
bekendtgørelse, der kun nævnes i præamblen, får sin egen hjemmel_for-kant (metode praeambel). Et dokument i Lovtidende A får en
implementerer_EU-kant til hver EU-retsakt, dets fodnote siger, det gennemfører (gennemfoerer, metode fodnote, sandsynlig). Et hentet dokument
uden tekst i bulk-høsten får en henviser_til-kant til hvert dokument, dets tekst nævner med nummer og den rigtige dato (metode xml-tekst).
katalog/eu_index.jsonl ajourføres med de retsakter, kun fodnoterne nævner (euindeks). De ældre implementerer_EU-kanter fra bulk-høsten (metode
tekst-samforekomst: retsakten står i samme bestemmelse som "gennemfører") fjernes for dokumenter, hvis tekst er hentet, fordi fodnoten dér er læst,
og sættes ellers til ukendt: i evalueringssættet (eval.py) var de kun rigtige, når fodnoten også nævnte retsakten.

En historisk lov eller lovbekendtgørelse uden gældende version får feltet afloeser, når en af dens kandidater (kandidater: hovedlove i dens
SenereAendringer, der selv nævner den i ÆndrerI) har en ophævelsesbestemmelse, der nævner den med nummer og dato (afloeser, i kandidatens hentede
tekst). Lovfamilien fortsætter så til afløserens gældende version (foelg_afloeser: gaeldende_version og afloeser_fra), også på hjemmel_for-kanterne.
Kandidater uden hentet tekst hentes af tekst.py hent (trinnet afloeser) og står indtil da ubekræftede. En lov, der kun rydder en forældet lov
op, er ikke afløser: de læste par står i raw/populate/2026-11-21-afloeser-oprydning.tsv, og familien fortsætter ikke til dem.
"""
from __future__ import annotations

import collections
import csv
import datetime
import importlib.util
import io
import json
import re
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent


def modul(navn: str, sti: Path):
    spec = importlib.util.spec_from_file_location(navn, sti)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


P = modul("populate", HERE.parent / "populate.py")
X = modul("extract", HERE / "extract.py")
K = modul("katalog", HERE / "katalog.py")

L = HERE.parents[1]
KAT = L / "dk-regulering" / "katalog"
OPRYDNING = L / "raw" / "populate" / "2026-11-21-afloeser-oprydning.tsv"
EKS = L / "intermediate" / "corpus" / "eksport"
TL = L / "intermediate" / "corpus" / "tidslinjer.jsonl"
TIDSLINJEFELTER = ("href", "documentTypeId", "isMainLaw", "isHistoric", "signatureDate")
SAMLINGER = {"lta": 1, "ltb": 2, "ltc": 3, "mt": 4, "retsinfo": 5, "ft": 6, "fob": 7}
ANDRE = ("ltb", "ltc", "mt", "retsinfo", "fob", "ft")
PRAKSIS = {"endelig-adm-afgørelse", "afgørelse", "udtalelse", "udtalelser", "dom", "kommentar"}
METODE = "retsinformation-eksport"
PRAEAMBEL = "praeambel"
FODNOTE = "fodnote"
XMLTEKST = "xml-tekst"
SAMFOREKOMST = "tekst-samforekomst"
BESTEMMELSE = "bestemmelse"
TYPER = {"Anordningsbekendtgørelse": "bekendtgørelse-af-anordning"}
LOVE = ("lov", "lovbekendtgørelse")
FORSKRIFTER = {"bekendtgørelse", "ændringsbekendtgørelse", "ikrafttrædelsesbekendtgørelse", "anordning", "ændringsanordning", "ikrafttrædelsesanordning",
               "bekendtgørelse-af-anordning"}


def intervaller(aar: dict, loft: int = 3000) -> list[tuple[str, str, int]]:
    """Sammenhængende årsintervaller (fra, til, antal) med højst loft dokumenter hver, medmindre ét år alene har flere.
    Første interval har ingen nedre og sidste ingen øvre grænse, så dokumenter fra år uden for fortegnelsen også kommer med."""
    start, cur, n = [], [], 0
    for y in sorted(aar):
        if cur and n + aar[y] > loft:
            start.append((cur[0], n))
            cur, n = [], 0
        cur.append(y)
        n += aar[y]
    start += [(cur[0], n)] if cur else []
    return [("" if i == 0 else fra, str(int(start[i + 1][0]) - 1) if i + 1 < len(start) else "", antal) for i, (fra, antal) in enumerate(start)]


def linje(d: dict) -> str:
    """Én JSON-linje. NEL, U+2028 og U+2029 skrives som escapes, så læsere, der regner dem for linjeskift (str.splitlines), ikke deler posten."""
    return json.dumps(d, ensure_ascii=False).translate({0x85: "\\u0085", 0x2028: "\\u2028", 0x2029: "\\u2029"}) + "\n"


def raekker(raw: bytes) -> list[dict]:
    """Eksportens rækker som dicts uden tomme felter; filen er UTF-16 uden BOM med semikolon som skilletegn."""
    text = raw.decode("utf-16-le" if raw[1:2] == b"\x00" else "utf-8-sig").lstrip("﻿")
    return [{k: v for k, v in r.items() if v and k != "Rank"} for r in csv.DictReader(io.StringIO(text), delimiter=";")]


def hent(samling: str | None = None, fra: str | None = None, til: str | None = None) -> dict:
    if samling:
        status, raw = P.get(f"{P.RI}/api/documentsearch/csv?ppm={SAMLINGER[samling]}&yl={fra}" + f"&yh={til}" * bool(til))
        if status != "ok":
            raise SystemExit(f"{samling} {fra}-{til or ''}: {status}")
        fil = EKS / f"{samling}.jsonl"
        ud = {r["EliUrl"]: r for r in map(json.loads, fil.open(encoding="utf-8"))}
        nye = {r["EliUrl"]: {**r, "Hentet": str(datetime.date.today())} for r in raekker(raw) if r.get("EliUrl")}
        stats = {samling: {"nye": len(nye.keys() - ud.keys()), "ajourført": len(nye.keys() & ud.keys()), "uændrede": len(ud.keys() - nye.keys())}}
        ud.update(nye)
        fil.write_text("".join(linje(ud[k]) for k in sorted(ud)), encoding="utf-8")
        return stats
    aar = collections.defaultdict(collections.Counter)
    for line in P.SITEMAP.open(encoding="utf-8"):
        dele = json.loads(line)["eli"].split("/")
        aar[dele[2]][dele[3][:4]] += 1
    EKS.mkdir(parents=True, exist_ok=True)
    stats = {}
    for navn, ppm in SAMLINGER.items():
        ud = {}
        for y1, y2, _ in intervaller(aar[navn]):
            status, raw = P.get(f"{P.RI}/api/documentsearch/csv?ppm={ppm}" + f"&yl={y1}" * bool(y1) + f"&yh={y2}" * bool(y2))
            if status != "ok":
                raise SystemExit(f"{navn} {y1}-{y2}: {status}")
            ud.update((r["EliUrl"], r) for r in raekker(raw) if r.get("EliUrl"))
        (EKS / f"{navn}.jsonl").write_text("".join(linje(ud[k]) for k in sorted(ud)), encoding="utf-8")
        stats[navn] = {"eksport": len(ud), "sitemap": sum(aar[navn].values()), "gældende": sum(r.get("Historisk") != "True" for r in ud.values())}
    (EKS / "hentet").write_text(str(datetime.date.today()), encoding="utf-8")
    return stats


def dato(s: str | None) -> str | None:
    return f"{s[:4]}-{s[4:6]}-{s[6:8]}" if s and len(s) >= 8 else None


def nid(eli: str) -> str:
    return eli.rstrip("/").split("/eli/")[1].replace("/", "-")


def titelnoegle(navn: str) -> str:
    return P.norm(re.sub(r"\(\*\s*\d+\)", " ", navn)).removeprefix("bekendtgørelse af ")


def henvist(tekst: str | None, ids: dict) -> list[str]:
    """Katalog-id'er for de dokumenter i Lovtidende A, en liste af betegnelser ("LBK nr 1031 af 06/09/2024,…") nævner."""
    fundet = (f"lta-{m[2]}-{m[1]}" for m in re.finditer(r"\b[A-ZÆØÅ]{3} nr (\d+) af \d\d/\d\d/(\d{4})", tekst or ""))
    return list(dict.fromkeys(i for i in fundet if i in ids))


def post(r: dict, idag: str) -> dict:
    """En katalogpost ud fra eksportens række. Lovtidende-betegnelse, dokumentrolle og tekstfelter findes kun for Lovtidende A; i de
    andre samlinger er typen Retsinformations egen dokumenttype, når den ikke er en af katalogets. I Folketingstidende er id'et år og
    samling (5 cifre), en art (et ciffer for dokumenter om et lovforslag), et bogstav og et løbenummer; feltet lovforslag er år og samling
    plus lovforslagets nummer, så fremsat og vedtaget tekst, betænkninger og ændringsforslag om samme lovforslag får samme nøgle."""
    i = nid(r["EliUrl"])
    samling, *_, nr = i.split("-")
    aar, lta = i.split("-")[1][:4], samling == "lta"
    typ = TYPER.get(r["DokumentType"]) or X.norm_type(r["DokumentType"], r["Titel"])
    if typ == "ukendt" and not lta:
        typ = re.sub(r"[^a-zæøå0-9]+", "-", re.sub(r"\(\d sp\)", "", r["DokumentType"].lower())).strip("-")
    u = dato(r.get("UnderskriftDato")) or (f"{aar}-01-01" if lta else None)
    sag = re.search(r"\d+", r.get("Nummer", "")) if samling == "ft" and nr[5].isdigit() else None
    omraade = {"Kun Grønland": "GL", "Kun Færøerne": "FO", "Kun Grønland og Færøerne": "GL+FO"}.get(r.get("GeografiskDækning"))
    udsteder = r.get("AdministrerendeMyndighed") or r.get("Ressort")
    datoer = {"udstedt": u, "historisk_markeret": dato(r.get("HistoriskDato")), "ri_registreret": dato(r.get("PubliceretTidspunkt")),
              "ri_aendret": dato(r.get("SidstPubliceretTidspunkt"))}
    return {
        "id": i, "navn": r["Titel"], "type": typ, "kilder": [f"{P.RI}/eli/{i.replace('-', '/')}" + "/xml" * lta],
        "status": {"vaerdi": "historisk" if r.get("Historisk") == "True" else "gældende", "pr": r.get("Hentet", idag), "sikkerhed": "verificeret"},
        "identifikatorer": {**({"lovtidende": f"{X.ABBR[typ]} nr. {nr} af {u[8:]}/{u[5:7]}/{u[:4]}"} if lta else {}), "document_id": r.get("DokumentId"),
                            "accession": r.get("ACCN"), "sikkerhed": "verificeret"},
        "datoer": {k: v for k, v in datoer.items() if v},
        "territorium": omraade if omraade and K.territorium(r["Titel"]) == "DK" else K.territorium(r["Titel"]),
        **({"dokumentrolle": K.rolle({"type": typ, "titel": r["Titel"]})} if lta else {}),
        "udstedt_af": {"vaerdi": udsteder or "ukendt", "metode": METODE if udsteder else "ingen", "praefiks": (r.get("DokumentId") or "")[:2],
                       "sikkerhed": "verificeret" if udsteder else "ukendt"},
        **({"n_paragraffer": 0, "n_definitioner": 0} if lta else {}),
        **({"lovforslag": f"{nr[:5]}-{int(sag[0])}"} if sag else {}),
    }


def lovkobling(ft: list[dict], love: list[dict]) -> dict:
    """{id på den vedtagne tekst: lov-id}: den lov, hvis titel er den vedtagne teksts uden "Forslag til", og som er underskrevet fra 3 dage
    før til 60 dage efter vedtagelsen. Vedtagne tekster med ingen eller flere sådanne love kobles ikke."""
    titel = lambda t: re.sub(r"\W+", " ", re.sub(r"(?i)^\s*forslag\s+til\s+", "", t.replace("\\n", " ")).lower()).strip()
    dag = lambda d: datetime.date.fromisoformat(d["datoer"]["udstedt"])
    kand = collections.defaultdict(list)
    for d in love:
        kand[titel(d["navn"])].append(d)
    ud = {}
    for d in ft:
        if d["type"] == "lovforslag-som-vedtaget" and d["datoer"].get("udstedt"):
            hit = [x["id"] for x in kand.get(titel(d["navn"]), []) if -3 <= (dag(x) - dag(d)).days <= 60]
            if len(hit) == 1:
                ud[d["id"]] = hit[0]
    return ud


def hjemmelkant(d: dict, lov: dict, citeret: list | None = None) -> dict:
    """Kanten mellem et dokument og den lovgivning, Retsinformation fører det under: hjemmel_for fra loven til forskrifter og vejledninger,
    henviser_til fra afgørelser, udtalelser og domme (PRAKSIS) til loven. citeret er præamblens henvisninger til samme lov (populate.praeambelhjemmel):
    bestemmelserne skrives i from_bestemmelse og den citerede version i citeret_version, når den er en anden end Retsinformations."""
    praksis, gv = d["type"] in PRAKSIS, lov.get("gaeldende_version")
    tekst = ("hjemmel ifølge Retsinformation (den lovversion, Retsinformation fører forskriften under)" if d["id"].startswith("lta-")
             else "lovgivning, dokumentet vedrører, ifølge Retsinformation (den version, Retsinformation fører dokumentet under)")
    fra = {"from_bestemmelse": list(dict.fromkeys(b for _, bs in citeret for b in bs)),
           **({"citeret_version": citeret[0][0]} if citeret[0][0] != lov["id"] else {})} if citeret and not praksis else {}
    return {"from": d["id"] if praksis else lov["id"], "type": "henviser_til" if praksis else "hjemmel_for", "to": lov["id"] if praksis else d["id"],
            "beskrivelse": tekst, "kilder": [f"{P.RI}/eli/{d['id'].replace('-', '/')}"], "sikkerhed": "verificeret", "metode": METODE,
            **({"gaeldende_version": gv} if gv else {}), **fra}


def myndigheder(reg: dict) -> dict:
    """{normaliseret navn: (node-id, er det nuværende navn)} for registry'ets instanser, med og uden parentes i navnet, med tidligere navne og med ministerens titel for hvert ministerium.
    Instansens eget navn går forud for et tidligere navn på en anden instans; et navn, flere instanser ellers deler, er udeladt."""
    ud = collections.defaultdict(set)
    for n in reg["nodes"]:
        if n["type"] in P.B.INSTANCE_TYPES:
            for navn, nu in [(n["navn"], True), *((t["navn"], False) for t in n.get("tidligere_navne") or [])]:
                ud[P.norm(navn)].add((n["id"], nu))
                ud[P.norm(re.sub(r"\([^)]*\)", "", navn))].add((n["id"], nu))
    valg = {k: nu if len(nu := {x for x in v if x[1]}) == 1 else v for k, v in ud.items()}
    navne = {k: max(v, key=lambda x: x[1]) for k, v in valg.items() if k and len({i for i, _ in v}) == 1}
    return {**{re.sub(r"ministeriet\b", "ministeren", k): v for k, v in navne.items() if v[0].startswith("min-")}, **navne}


ALIAS = {"kommunalbestyrelsen": "kommune-alle", "kommunen": "kommune-alle", "kommunalbestyrelserne": "kommune-alle", "regionsrådet": "region-alle",
         "rigspolitichefen": "sty-rigspolitiet", "biskoppen": "tilsyn-biskopperne", "socialtilsynet": "tilsyn-socialtilsynene",
         "ankestyrelsens beskæftigelsesudvalg": "sty-ankestyrelsen", "taksationsmyndighederne": "naevn-taksationsmyndighederne",
         "overtaksationskommissionen": "naevn-taksationsmyndighederne", "kirkeministeren": "min-sundhed-og-kirke",
         "direktoratet for kriminalforsorgen": "sty-danmarks-faengsler"}
SAETNING = re.compile(r"(?<=[.;])\s+(?=[A-ZÆØÅ])")
KLAGE = re.compile(r"(?:\b(?:påklages?|klages|indbringes?|anke[sr]?)\b(?P<m>[^.;]{0,160}?)\b(?:til|for)|\bklager? til)\s+(?P<end>(?:en\s+)?anden administrativ myndighed end\s+)?",
                   re.IGNORECASE)
SAG = re.compile(r"\b(?:sag(?:en|er|erne)?|tvist(?:en|er|erne)?|spørgsmål(?:et)?)\b", re.IGNORECASE)
BEHANDLER = re.compile(r"\s+(?:behandler|afgør|træffer afgørelse (?:i|om)) klager\b", re.IGNORECASE)
TILSYN = re.compile(r"\b(?:(?:kan|skal)\s+)?(?:fører?|udøver|varetager)\s+(?P<m>(?:(?!ikke\b|hverken\b)[\w,-]+\s+){0,7}?)(?:tilsyn|kontrol)(?:et|len)?\b", re.IGNORECASE)
TILSYN_AF = re.compile(r"\b(?:tilsyn|kontrol)(?:et|len)?\b[^.;]{0,120}?\b(?:føres|udøves|varetages|foretages|udføres)\s+af\s+", re.IGNORECASE)
KONTROL = re.compile(r"\b(?:(?:kan|skal)\s+)?(?:(?:påser?|kontrollerer?)(?!\s+ikke\b)(?=(?:(?!,\s+(?:og|men|eller|samt)\s).)*?\b(?:at\b.*?\b)?(?:overhold|efterlev|lovlig))|er\s+(?:(?!ikke\b)\w+\s+){0,2}?tilsynsmyndighed(?:en)?)\b|(?<=s)\s+(?:tilsyn|kontrol)\s+med\b",
                     re.IGNORECASE)
LED = (KLAGE, BEHANDLER, TILSYN, TILSYN_AF, KONTROL)
TILBAGE = {"styrelsens": "sty-", "nævnets": "naevn-", "tilsynets": "tilsyn-"}
AFGOERELSE = {"afgørelse", "afgørelsen", "afgørelser", "afgørelserne"}
OVERGANG = re.compile(r"\bfærdigbehandles\b", re.IGNORECASE)
TIL_BRUG = re.compile(r"\btil brug for\s+(?:[^\s,;]+\s+){0,5}[^\s,;]+$", re.IGNORECASE)


FORLED = {"den", "det", "de", "en", "et", "anden", "andre", "vedkommende", "pågældende", "kompetente", "relevante", "overordnede"}


def frase(tekst: str, bagfra: bool = False) -> str:
    """Det navn, der står forrest (eller bagerst) i tekst, normaliseret: ord med stort begyndelsesbogstav, ord efter bindestreg, "og" og "for" mellem dem,
    og ordet efter et forled som "den" eller "kompetente". Til fortegnelsen over de navne, læseren ikke kender."""
    w = re.findall(r"[\w/]+-?|[^\w\s]", re.sub(r"-\s*,", "-", tekst[-200:] if bagfra else tekst[:200]))[::-1 if bagfra else 1]
    w = w[:next((i for i, x in enumerate(w) if not re.match(r"\w", x)), len(w))]
    ud = w[:1]
    for x in w[1:]:
        a = x if bagfra else ud[-1]
        if not (x[:1].isupper() or a.endswith("-") or x in ("og", "for") or (not bagfra and a.lower() in FORLED)
                or (not bagfra and ud[-1] == "og" and len(ud) > 1 and ud[-2].endswith("-"))):
            break
        ud.append(x)
    while ud and ud[-1] in ("og", "for"):
        ud.pop()
    return P.norm(" ".join(ud[::-1] if bagfra else ud))


def laeser(reg: dict):
    """(klager, tilsyn, ukendte): tre funktioner, der læser én sætning mod registry'ets instansnavne (myndigheder, med ALIAS og genitiv-s).
    klager(sætning) giver [(klageinstans, afgørende myndighed eller None)] for "kan påklages til X", "kan indbringes for X", "klage til X",
    "ikke … anden administrativ myndighed end X" og "X behandler klager"; ikke for "kan ikke påklages til X", ikke for domstolene under ét, ikke når
    det er en sag eller en tvist, der indbringes, ikke for en sætning, der opregner andre forskrifter, ikke i en overgangsregel ("færdigbehandles") og ikke for en dom, der ankes til
    en domstol. De afgørende myndigheder er instanserne i samme sætning i formen "X's afgørelser" (ikke et sammensat ord som "X's afgørelseskompetence")
    eller "truffet af X", og en instans, der står lige efter en af dem med "og" eller "eller"; én tupel pr. afgørende myndighed. tilsyn(sætning) giver instanserne i "X fører tilsyn",
    "X kan føre kontrol", "fører X tilsyn", "tilsynet føres af X", "X påser, at", "X kontrollerer", "kontrollerer X" (efter et komma
    eller uden instans foran), "X er tilsynsmyndighed" og "X's kontrol (tilsyn) med" (ikke "til brug for X's tilsyn med"), hvor "styrelsens", "nævnets" og "tilsynets" er den sidste
    styrelse, det sidste nævn eller tilsyn (også en instans, hvis navn ender på "tilsynet"), sætningen har nævnt før; "påser" og "kontrollerer" kun, når verbets sætningsled
    eller den at-sætning, der følger det, taler om at overholde eller efterleve noget, eller om lovlighed; ikke "påser ikke", "er ikke tilsynsmyndighed", "fører ikke tilsyn" og "fører hverken tilsyn".
    ukendte(sætning) giver navnet (frase) de steder, hvor klager eller tilsyn venter en instans, men ikke finder én i registry'et."""
    navne = {**{k: v[0] for k, v in myndigheder(reg).items()}, **ALIAS}
    laengde = max(len(k.split()) for k in navne)

    def ved(w: list[str], i: int) -> tuple[str | None, int, bool]:
        for n in range(min(laengde, len(w) - i), 0, -1):
            k = " ".join(w[i:i + n])
            if k in navne or k.removesuffix("s") in navne:
                return navne.get(k) or navne[k.removesuffix("s")], n, k not in navne
        return None, 0, False

    def sidst(tekst: str) -> str | None:
        w = P.norm(tekst).split()
        if w and w[-1] in TILBAGE:
            ud, i = None, 0
            while i < len(w) - 1:
                node, n, _ = ved(w, i)
                ud = node if node and (node.startswith(TILBAGE[w[-1]]) or w[-1] == "tilsynets" and w[i + n - 1].removesuffix("s").endswith("tilsynet")) else ud
                i += n or 1
            return ud
        return next((ved(w, i)[0] for i in range(max(0, len(w) - laengde), len(w)) if ved(w, i)[1] == len(w) - i), None)

    def foerst(tekst: str) -> str | None:
        return ved(P.norm(tekst[:200]).split(), 0)[0]

    def navn(tekst: str, bagfra: bool) -> str | None:
        return sidst(tekst) if bagfra else foerst(tekst)

    def afgoerer(saetning: str, til: str) -> list[str]:
        w, ud, i, slut = P.norm(saetning).split(), [], 0, -1
        while i < len(w):
            node, n, genitiv = ved(w, i)
            if node and node != til and ((genitiv and any(x in AFGOERELSE for x in w[i + n:i + n + 4])) or (ud and w[slut:i] in (["og"], ["eller"], ["og", "af"], ["eller", "af"]))
                                         or w[max(0, i - 2):i] in (["truffet", "af"], ["afgørelser", "af"], ["afgørelse", "af"], ["meddelt", "af"])):
                ud.append(node)
                slut = i + n
            i += n or 1
        return list(dict.fromkeys(ud))

    def steder(saetning: str) -> tuple[list[tuple[str, bool]], list[tuple[str, bool]]]:
        ophaever = re.match(r"(?:Bekendtgørelse|Lov|Lovbekendtgørelse) nr\.", saetning)
        klage = [] if ophaever or OVERGANG.search(saetning) else [
            *((saetning[m.end():], False) for m in KLAGE.finditer(saetning)
              if (m["end"] or not (re.search(r"\bikke\b[^,]{0,40}$", saetning[:m.start()]) or re.search(r"\bikke\b", m["m"] or "") or SAG.search(saetning[:m.end()])))
              and not (m[0][:4].lower() == "anke" and (foerst(saetning[m.end():]) or "").startswith("dom-"))),
            *((saetning[:m.start()], True) for m in BEHANDLER.finditer(saetning))]
        tils = [(m["m"], False) if len(m["m"].split()) > 2 or foerst(m["m"]) else (saetning[:m.start()], True) for m in TILSYN.finditer(saetning)]
        paa = [(saetning[m.end():], False) if m[0].lower().endswith(("påse", "påser", "kontrollere", "kontrollerer")) and (saetning[:m.start()].rstrip().endswith(",")
               or not sidst(saetning[:m.start()]) and foerst(saetning[m.end():])) else (saetning[:m.start()], True) for m in KONTROL.finditer(saetning)
               if not (ophaever or re.fullmatch(r"\s+(?:tilsyn|kontrol)\s+med", m[0], re.IGNORECASE) and TIL_BRUG.search(saetning[:m.start()]))]
        return klage, tils + [(saetning[m.end():], False) for m in TILSYN_AF.finditer(saetning)] + paa

    def klager(saetning: str) -> list[tuple[str, str | None]]:
        til = [navn(*x) for x in steder(saetning)[0]]
        return [(t, a) for t in dict.fromkeys(til) if t and t != "dom-domstolene" for a in afgoerer(saetning, t) or [None]]

    def tilsyn(saetning: str) -> list[str]:
        return [x for x in dict.fromkeys(navn(*x) for x in steder(saetning)[1]) if x]

    def ukendte(saetning: str) -> list[str]:
        return [f for f in dict.fromkeys(frase(*x) for led in steder(saetning) for x in led if not navn(*x)) if f]

    return klager, tilsyn, ukendte


EUNAEVNT = re.compile("|".join(r.pattern for r in (X.R_DIR, X.R_REG_OLD, X.R_REG_NEW, X.R_DEC)), re.IGNORECASE)
SLUT = re.compile(r"notificeret|medtaget visse|Ifølge artikel")
KAEDE = re.compile(r"ændret ved|senest ved|og ved\b")
TITEL = re.compile(r"ændring af|ophævelse af|i henhold til")


def gennemfoerer(noter: list[str]) -> list[str]:
    """EU-retsakter (katalog-id), som en fodnote siger, at dokumentet gennemfører. Læst fra "gennemfører" til notens slutning eller til
    informationsproceduren ("notificeret") og gengivne forordninger ("medtaget visse bestemmelser"). En retsakt efter "som ændret ved" eller
    "senest ved" er en ændringsretsakt og er ikke med, og det er de følgende heller ikke, før teksten igen siger "dele af" eller "gennemfører",
    eller der efter en henvisning til EU-Tidende kommer en retsakt, hvis egen titel ikke begynder med "om ændring af".
    Retsakter i en anden retsakts titel (efter "om ændring af", "om ophævelse af" eller "i henhold til" og frem til henvisningen til EU-Tidende
    eller en slutparentes) er heller ikke med."""
    ud = []
    for note in noter:
        for start in (m.end() for m in X.R_GF.finditer(note)):
            slut = SLUT.search(note, start)
            led, pos, kaede, titel = note[start:slut.start() if slut else len(note)], 0, False, False
            for m in EUNAEVNT.finditer(led):
                mellem, pos = led[pos:m.start()], m.end()
                aendrer = re.match(r"[^,;]{0,60}?\bom ændring af", led[m.end():])
                efter = re.split(r"(?i)tidende", mellem)
                kaede = bool(KAEDE.search(mellem)) or (kaede and not re.search(r"dele af|gennemfører", mellem) and (len(efter) == 1 or bool(aendrer)))
                titel = bool(TITEL.search(efter[-1])) or (titel and len(efter) == 1 and ")" not in mellem)
                if not kaede and not titel:
                    ud += [K.eu_id(k)[0] for k in X.eu_refs(m[0])]
    return list(dict.fromkeys(ud))


def euindeks(kanter: list[dict], ids: dict) -> None:
    """Ajourfører katalog/eu_index.jsonl: antal implementerer_EU-kanter pr. retsakt, og en post for hver retsakt, kun en fodnote nævner
    (fra: fodnote; n_dok og n_gaeldende tæller dér de dokumenter, hvis fodnote nævner den)."""
    fra = collections.defaultdict(set)
    for e in kanter:
        if e["type"] == "implementerer_EU":
            fra[e["to"]].add(e["from"])
    eu = {r["id"]: r for r in map(json.loads, (KAT / "eu_index.jsonl").open(encoding="utf-8")) if r.get("fra") != FODNOTE}
    for eid in sorted(set(fra) - set(eu)):
        t, aar, nr = eid.split("-")[1:]
        eu[eid] = {"id": eid, "type": {"dir": "eu-direktiv", "reg": "eu-forordning", "dec": "eu-afgørelse"}[t],
                   "identifikatorer": {"celex": K.eu_id(f"{t}:{aar}/{nr}")[1], "kilder": [K.CELEX_HELP], "sikkerhed": "verificeret",
                                       "kilde_note": "CELEX afledt af den citerede retsakts år og nummer efter EUR-Lex' CELEX-syntaks (sektor 3)."},
                   "registry_id": None, "n_dok": len(fra[eid]), "n_gaeldende": sum(ids[i]["status"]["vaerdi"] == "gældende" for i in fra[eid]), "fra": FODNOTE}
    (KAT / "eu_index.jsonl").write_text("".join(linje({**r, "n_implementerer": len(fra.get(r["id"], ()))}) for r in eu.values()), encoding="utf-8")


def udstederkant(d: dict, node: str, nuvaerende: bool) -> dict:
    """udsteder fra den instans, Retsinformation fører som administrerende myndighed for en afgørelse eller udtalelse; sandsynlig, når navnet er et
    tidligere navn. Feltet føres ajour: en ældre afgørelse kan stå under den myndighed, der har overtaget området."""
    return {"from": node, "type": "udsteder", "to": d["id"], "kilder": d["kilder"], "sikkerhed": "verificeret" if nuvaerende else "sandsynlig", "metode": METODE,
            "beskrivelse": "administrerende myndighed for afgørelsen eller udtalelsen ifølge Retsinformation" + ("" if nuvaerende else " (under et tidligere navn)")}


def tidslinjer(statusser: tuple = ("ok",)) -> list[dict]:
    """Rækkerne i den hentede tidslinjefil med en af statusserne; tom, når filen ikke findes."""
    return [r for r in map(json.loads, TL.open(encoding="utf-8")) if r["status"] in statusser] if TL.exists() else []


def lovversioner(tl: list[dict]) -> list[str]:
    """Katalog-id'er for lovens egne versioner i en tidslinje: hovedloven og lovbekendtgørelserne. Ændringslove og andre hovedlove, der har
    ændret loven, står også i tidslinjen, men er ikke versioner af den."""
    return [nid(e["href"]) for e in tl if (e.get("documentTypeId") == 30 or e.get("isMainLaw")) and "/eli/" in (e.get("href") or "")]


def senere_aendret(udstedt: str, tl: list[dict] | None, felt: str | None, ids: dict) -> list[str]:
    """Katalog-id'er for de love, der har ændret dokumentet og er underskrevet efter udstedt. Med tidslinje: ændringslovene (documentTypeId 20)
    og de andre hovedlove, der har ændret loven (10 uden isMainLaw); ikrafttrædelsesbekendtgørelser (90) og lovens egne versioner tæller ikke.
    Uden tidslinje (bekendtgørelser): eksportens felt SenereAendringer. Ingen, når udstedt mangler."""
    if not udstedt:
        return []
    if tl is not None:
        kand = [(nid(e["href"]), "-".join(reversed(e["signatureDate"].split("/")))) for e in tl
                if (e.get("documentTypeId") == 20 or (e.get("documentTypeId") == 10 and not e.get("isMainLaw"))) and "/eli/" in (e.get("href") or "")]
    else:
        kand = [(i, ids[i]["datoer"].get("udstedt", "")) for i in henvist(felt, ids)]
    return list(dict.fromkeys(i for i, u in kand if i in ids and u > udstedt))


def familier(docs: list[dict], blev_historisk: set, kaeder: list[list[str]] = ()) -> dict:
    """Peg lovfamilier på den nyeste gældende version; returnér {gammel version: ny version} for dem, der er flyttet på titlen. En lov med
    hentet tidslinje (kaeder: versionerne pr. lov) samles efter den og får familie_metode "tidslinje": er ingen version gældende, peger de
    ældre på den nyeste. En gældende version med samme titel, nyere end tidslinjen og ikke i nogen tidslinje (udstedt efter at tidslinjen
    blev hentet), bliver tidslinjens gældende version. Andre love samles på titlen."""
    ids = {d["id"]: d for d in docs}
    gaeldende = collections.defaultdict(list)
    for d in docs:
        if d["status"]["vaerdi"] == "gældende" and d["type"] in LOVE and d["dokumentrolle"] == "hoved":
            gaeldende[titelnoegle(d["navn"])].append(d)
    hoved, i_kaede = {}, {i for kaede in kaeder for i in kaede}
    for kaede in kaeder:
        v = [i for i in kaede if i in ids]
        udstedt = lambda i: ids[i]["datoer"].get("udstedt", "")
        nu = max([i for i in v if ids[i]["status"]["vaerdi"] == "gældende"] or v, key=udstedt, default=None)
        senere = [d["id"] for d in gaeldende[titelnoegle(ids[nu]["navn"])] if d["id"] not in i_kaede and udstedt(d["id"]) > max(map(udstedt, v))] if nu else []
        hoved.update(dict.fromkeys(v, max(senere, key=udstedt, default=nu)))

    def nyere(g: dict) -> str | None:
        kand = [d for d in gaeldende[titelnoegle(g["navn"])] if d["datoer"].get("udstedt", "") > g["datoer"].get("udstedt", "")]
        return max(kand, key=lambda d: d["datoer"]["udstedt"])["id"] if kand else None

    ompeg = {}
    for d in docs:
        if d["id"] in hoved:
            for k in ("gaeldende_version", "nyeste_version_afloeser_mangler", "afloeser_mangler"):
                d.pop(k, None)
            d["familie_metode"] = "tidslinje"
            if (nu := hoved[d["id"]]) != d["id"]:
                d["gaeldende_version" if ids[nu]["status"]["vaerdi"] == "gældende" else "nyeste_version_afloeser_mangler"] = nu
            continue
        g = d.get("gaeldende_version") or d.pop("nyeste_version_afloeser_mangler", None)
        if not g and d["status"]["vaerdi"] == "historisk" and d["type"] in LOVE and (d.get("afloeser_mangler") or d["id"] in blev_historisk):
            g = d["id"]
        if not g:
            continue
        if ids[g]["status"]["vaerdi"] == "gældende":
            if g != d["id"]:
                d["gaeldende_version"] = g
            continue
        ny = ompeg[g] = ompeg.get(g) or nyere(ids[g])
        d.pop("gaeldende_version", None)
        d.pop("afloeser_mangler", None)
        if ny:
            d["gaeldende_version"] = ny
        elif g == d["id"]:
            d["afloeser_mangler"] = True
        else:
            d["nyeste_version_afloeser_mangler"] = g
    return {g: ny for g, ny in ompeg.items() if ny}


def kandidater(ids: dict, eks: dict) -> dict:
    """{historisk lov eller lovbekendtgørelse uden gældende version: de hovedlove (type lov), der står i dens SenereAendringer og selv nævner
    den i ÆndrerI}. Listerne skelner ikke ophævelse fra ændring; afløseren bekræftes af ophævelsesbestemmelsen (afloeser)."""
    ud = {}
    for i, d in ids.items():
        if i.startswith("lta-") and d["type"] in LOVE and d["status"]["vaerdi"] == "historisk" and not d.get("gaeldende_version"):
            k = [c for c in henvist(eks.get(i, {}).get("SenereAendringer"), ids) if ids[c]["type"] == "lov" and i in henvist(eks.get(c, {}).get("ÆndrerI"), ids)]
            ud.update({i: k} if k else {})
    return ud


LOVNR = re.compile(r"\b(lov|lovbekendtgørelse)\s+nr\.\s*(\d+)\s+af\s+(\d{1,2})\.\s*(" + "|".join(X.MONTHS) + r")\s+(\d{4})", re.IGNORECASE)
LISTE = re.compile(r"\bophæves\b[^.]*:\s*$")
DELVIS = re.compile(r"§|\bkapitel\b|\bafsnit\b|\bstk\.", re.IGNORECASE)
UNDTAGEN = re.compile(r"\bbortset fra\b|\bmed undtagelse af\b", re.IGNORECASE)
GENNEM = re.compile(r"\b(?:affattet|ændret)\s+ved\s*$", re.IGNORECASE)
BEVAR = re.compile(r"\b(?:fastsat|udstedt)\s+(?:i henhold til|i medfør af|efter|med hjemmel i)\b.*\bforbliver i kraft\b", re.IGNORECASE)


def afloeser(gammel: dict, kandidat: dict, afsnit: list[tuple[str | None, str]]) -> dict | str:
    """Afløserfeltet til den gamle lov, når kandidatens egen tekst (afsnit: tekst.afsnit) har en ophævelsesbestemmelse, der nævner den med
    nummer og dato: "Lov nr. X af <dato> ... ophæves", "Lov om ..., jf. lovbekendtgørelse nr. X af <dato>, ophæves" eller et punkt under
    "... ophæves ...:". Ikke en ophævelse: en bemyndigelse (kan), en delvis ophævelse (bortset fra, med undtagelse af, enkelte paragraffer) og et
    nummer fra "som affattet ved" eller "som ændret ved". En lovbekendtgørelse gentager bestemmelser fra de love, der har ændret den, så kun
    en hovedlov (type lov) kan være afløser, og ikke en ren ophævelseslov ("Lov om ophævelse af ..."). bevarer_regler er den sætning, der lader
    regler fastsat efter den gamle lov forblive i kraft. Returnerer "uden-tekst" uden afsnit og ellers "afvist", når ingen bestemmelse holder."""
    if not afsnit:
        return "uden-tekst"
    if kandidat["type"] != "lov" or kandidat["navn"].startswith("Lov om ophævelse af"):
        return "afvist"
    nr, dag = gammel["id"].split("-")[2], gammel["datoer"].get("udstedt")
    nyt = lambda m: m[2] == nr and f"{m[5]}-{X.MONTHS[m[4].lower()]:02d}-{int(m[3]):02d}" == dag and {"lov": "lov"}.get(m[1].lower(), "lovbekendtgørelse") == gammel["type"]
    fund = bevar = None
    for par, tekst in afsnit:
        linjer = []
        for x in tekst.split("\n"):
            if linjer and not re.match(r"\d+\)", x) and not re.search(r"[.:;]\s*$", linjer[-1]):
                linjer[-1] += " " + x
            else:
                linjer.append(x)
        for n, linje in enumerate(linjer):
            for s in SAETNING.split(linje):
                if BEVAR.search(s) and not bevar and any(nyt(m) for m in LOVNR.finditer(s)):
                    bevar = s
                for m in LOVNR.finditer(s) if not fund else ():
                    intro = next((x for x in reversed(linjer[:n]) if not re.match(r"\d+\)", x)), "")
                    liste = "ophæves" not in s and LISTE.search(intro) and re.match(r"\d+\)", linje)
                    pre = s[:m.start()]
                    if (nyt(m) and ("ophæves" in s or liste) and not GENNEM.search(pre) and not DELVIS.search(re.split(LOVNR.pattern + r"|\bophæves\b|\bsamt\b|:|;", pre, flags=re.IGNORECASE)[-1])
                            and not UNDTAGEN.search(s) and not re.search(r"\bkan\b", s + (intro if liste else ""))):
                        fund = (s, par, tekst)
    if not fund:
        return "afvist"
    if not bevar:
        bevar = next((s for p, t in afsnit if p == fund[1] for s in SAETNING.split(" ".join(t.split())) if BEVAR.search(s)), None)
    return {"vaerdi": kandidat["id"], "ophaevelse": fund[0], "paragraf": fund[1], "paragraf_tekst": fund[2], "kilder": kandidat["kilder"][:1], "sikkerhed": "verificeret",
            "metode": "ophaevelsesbestemmelse", "bevarer_regler": bevar}


def foelg_afloeser(ids: dict, fund: dict) -> int:
    """Skriv afløserfeltet (fund: {gammel lov: afloeser}) og lad lovfamilien fortsætte: den gamle lovs familie (den selv eller den version,
    nyeste_version_afloeser_mangler peger på, og dens øvrige versioner) får afløserens gældende version som gaeldende_version og afloeser_fra
    (familiens nyeste version), også gennem flere afløsere i træk. Returnerer antallet af dokumenter, der har fået en gældende version."""
    hoved = lambda i: ids[i].get("nyeste_version_afloeser_mangler") or i
    videre = {hoved(o): f["vaerdi"] for o, f in fund.items()}
    medlem = collections.defaultdict(list)
    for d in ids.values():
        if d.get("nyeste_version_afloeser_mangler") in videre:
            medlem[d["nyeste_version_afloeser_mangler"]].append(d)

    def maal(s: str) -> str | None:
        for _ in range(20):
            d = ids[s]
            if d["status"]["vaerdi"] == "gældende" or d.get("gaeldende_version"):
                return d.get("gaeldende_version") or s
            if hoved(s) not in videre:
                return None
            s = videre[hoved(s)]
        return None

    for o, f in fund.items():
        ids[o]["afloeser"] = f
    flyttet = 0
    for h, s in videre.items():
        if t := maal(s):
            for d in [ids[h], *medlem[h]]:
                d.pop("afloeser_mangler", None)
                d.pop("nyeste_version_afloeser_mangler", None)
                d.update(gaeldende_version=t, afloeser_fra=h)
                flyttet += 1
    return flyttet


def lovled(ids: dict, i: str) -> str:
    """Lovfamilien, men med en lov og dens afløser som to led: paragrafnumre gælder kun inden for samme lov."""
    d = ids.get(i) or {}
    return d.get("afloeser_fra") or d.get("gaeldende_version") or d.get("nyeste_version_afloeser_mangler") or i


def nulstil_afloeser(docs: list[dict]) -> None:
    """Fjern sidste kørsels afløserfelter, så familier og afloeser regner forfra."""
    for d in docs:
        d.pop("afloeser", None)
        if h := d.pop("afloeser_fra", None):
            d.pop("gaeldende_version", None)
            d.update({"afloeser_mangler": True} if h == d["id"] else {"nyeste_version_afloeser_mangler": h})


def kandidatplan() -> list[str]:
    """Kandidatlovene fra det skrevne katalog i hente-rækkefølge: først kandidaterne til de gamle love, en gældende forskrift har hjemmel i
    (hjemmel_for til en lovfamilie uden gældende version, og love med afloeser_mangler), så resten; nyeste først inden for hver."""
    ids = {d["id"]: d for d in map(json.loads, (KAT / "retsinformation_lta.jsonl").open(encoding="utf-8"))}
    kand = kandidater(ids, {nid(r["EliUrl"]): r for r in map(json.loads, (EKS / "lta.jsonl").open(encoding="utf-8"))})
    brugt = {d["id"] for d in ids.values() if d.get("afloeser_mangler")}
    for e in map(json.loads, (KAT / "kanter.jsonl").open(encoding="utf-8")):
        if e["type"] == "hjemmel_for" and e["from"] in kand and not e.get("gaeldende_version") and ids.get(e["to"], {}).get("status", {}).get("vaerdi") == "gældende":
            brugt |= {e["from"], ids[e["from"]].get("nyeste_version_afloeser_mangler")}
    foerst = sorted({c for g in brugt & kand.keys() for c in kand[g]}, reverse=True)
    return foerst + sorted({c for k in kand.values() for c in k} - set(foerst), reverse=True)


def klassificer(docs: list[dict], foraeldre: dict, eks: dict, reg: dict, svar: dict, idag: str) -> list[dict]:
    """Sæt ministerium fra Retsinformations ressortfelt på alle gældende dokumenter, hvor feltet med sikkerhed er aktuelt, også når en
    klassifikation siger noget andet. Giv derefter gældende dokumenter uden klassifikation ministerium og retsområde fra forældre og svar;
    returnér dem, der stadig mangler noget."""
    ids = {d["id"]: d for d in docs}
    ministerier = {n["navn"]: n["id"] for n in reg["nodes"] if n["type"] == "ministerium" and n.get("status") == "aktiv"}
    for d in docs:
        felt = P.ressort({"Status": "Valid", "Ministry": eks.get(d["id"], {}).get("Ressort"), "DiesSigni": d["datoer"].get("udstedt", "")}, reg)
        if d["status"]["vaerdi"] == "gældende" and ministerier.get(felt):
            d["ministerium"] = {"vaerdi": ministerier[felt], "sikkerhed": "verificeret", "metode": "retsinformation", "pr": eks.get(d["id"], {}).get("Hentet", idag)}
    mangler = [d for d in docs if d["status"]["vaerdi"] == "gældende" and not ((d.get("ministerium") or {}).get("vaerdi") and d.get("retsomraade"))]

    def klasse(i: str) -> tuple:
        d = ids.get(i) or {}
        g = ids.get(d.get("gaeldende_version")) or {}
        return (d.get("ministerium") or g.get("ministerium") or {}).get("vaerdi"), d.get("retsomraade") or g.get("retsomraade")

    aendret = True
    while aendret:
        aendret = False
        for d in mangler:
            arv = [klasse(p) for p in foraeldre.get(d["id"], [])]
            for felt, vaerdier in (("ministerium", [m for m, _ in arv if m and m not in ("ukendt", "ingen")]), ("retsomraade", [o for _, o in arv if o])):
                if vaerdier and not d.get(felt):
                    valgt = collections.Counter(vaerdier).most_common(1)[0][0]
                    d[felt] = {"vaerdi": valgt, "sikkerhed": "sandsynlig", "metode": "arvet"} if felt == "ministerium" else valgt
                    aendret = True
    for d in mangler:
        s = svar.get(d["id"], {})
        if s.get("ministerium") in ministerier.values() and not d.get("ministerium"):
            d["ministerium"] = {"vaerdi": s["ministerium"], "sikkerhed": "sandsynlig", "metode": "haiku"}
        if s.get("retsomraade") and not d.get("retsomraade"):
            d["retsomraade"] = s["retsomraade"]
    return [d for d in mangler if not (d.get("ministerium") and d.get("retsomraade"))]


def daekning(docs: list[dict], kanter: list[dict], med: set) -> dict:
    """Dashboardets tal pr. retsområde for gældende dokumenter: dokumenttal og de fem målte lag. Lagene tæller kun danske hoveddokumenter;
    med er de forskrifter, der har en hjemmel_for-kant."""
    lov = {e["from"] for e in kanter if e["type"] == "henviser_til" and e["to"].startswith("lta-") and e.get("beskrivelse", "").startswith("nævner loven")}
    tal = collections.defaultdict(collections.Counter)
    for d in docs:
        if d["status"]["vaerdi"] != "gældende":
            continue
        c = tal[d.get("retsomraade") or "ikke-klassificeret"]
        c["gaeldende_alle"] += 1
        if d.get("territorium") != "DK":
            c["gl_fo"] += 1
        elif d.get("dokumentrolle") != "hoved":
            c["aendring_ikraft_ophaev"] += 1
        else:
            forskrift = d["type"] in FORSKRIFTER
            c.update(gaeldende=1, udsteder=d["udstedt_af"]["vaerdi"] != "ukendt", lovhenv=d["id"] in lov, registry=bool(d.get("registry_ids")),
                     ressort=(d.get("ministerium") or {}).get("sikkerhed") in ("verificeret", "sandsynlig"), regulering=forskrift,
                     hjemmel=forskrift and d["id"] in med, love=d["type"] in ("lov", "lovbekendtgørelse", "ændringslov"))
    return tal


def dashboard(tal: dict, docs: list[dict], reg: dict) -> None:
    """Skriv katalogets tal i dashboard/omraader.json, maalt.json og fremdrift.json; de vurderede lag og manglerne røres ikke."""
    dash = L / "dashboard"

    def ret(navn: str, fn) -> None:
        rows = json.loads((dash / navn).read_text(encoding="utf-8"))
        for row in rows:
            fn(row)
        (dash / navn).write_text(json.dumps(rows, ensure_ascii=False), encoding="utf-8")

    def lag(row: dict) -> None:
        c = tal[row["omraade"]]
        row["taeller"], row["naevner"] = c[row["lag"]], c["regulering" if row["lag"] == "hjemmel" else "gaeldende"]
        row["daekning"] = round(100 * row["taeller"] / row["naevner"]) if row["naevner"] else None

    gd = sum(c["gaeldende_alle"] for c in tal.values())
    klass = sum(bool(d.get("retsomraade")) for d in docs if d["status"]["vaerdi"] == "gældende")
    sikre = collections.Counter(n[f]["sikkerhed"] for n in reg["nodes"] for f in P.B.CLAIM_FIELDS) + collections.Counter(e["sikkerhed"] for e in reg["edges"])
    mangler = json.loads((dash / "mangler.json").read_text(encoding="utf-8"))
    nyt = {"katalog_dokumenter": (len(docs), None), "katalog_gaeldende": (gd, len(docs)), "normative_dk": (sum(c["gaeldende"] for c in tal.values()), gd),
           "klassificeret": (klass, gd), "klassificeret_pct": (round(100 * klass / gd), 100), "registry_noder": (len(reg["nodes"]), None),
           "registry_verificeret_pct": (round(100 * sikre["verificeret"] / sum(sikre.values())), 100),
           "mangler_loest": (sum(m["status"] != "åben" for m in mangler), len(mangler))}
    ret("omraader.json", lambda row: row.update({k: tal[row["omraade"]][k] for k in ("gaeldende", "gaeldende_alle", "gl_fo", "aendring_ikraft_ophaev", "love", "regulering")}))
    ret("maalt.json", lag)
    ret("fremdrift.json", lambda row: row.update(zip(("vaerdi", "total"), nyt.get(row["metric"], (row["vaerdi"], row["total"])))))


def katalog() -> dict:
    idag = (EKS / "hentet").read_text(encoding="utf-8").strip()
    eks = {nid(r["EliUrl"]): r for s in ("lta", *ANDRE) for r in map(json.loads, (EKS / f"{s}.jsonl").open(encoding="utf-8"))}
    docs = [d for d in map(json.loads, (KAT / "retsinformation_lta.jsonl").open(encoding="utf-8")) if "seed_fil" in d]
    stats = collections.Counter(katalog_foer=len(docs))
    blev_historisk = set()
    for d in docs:
        r = eks.get(d["id"])
        if r is None:
            stats["uden for eksporten"] += 1
            continue
        ny = "historisk" if r.get("Historisk") == "True" else "gældende"
        if ny != d["status"]["vaerdi"]:
            stats[f"status {d['status']['vaerdi']} → {ny}"] += 1
            blev_historisk |= {d["id"]} if ny == "historisk" else set()
            d["datoer"].pop("historisk_markeret", None)
            if ny == "historisk" and dato(r.get("HistoriskDato")):
                d["datoer"]["historisk_markeret"] = dato(r["HistoriskDato"])
        d["status"] = {**d["status"], "vaerdi": ny, "pr": r.get("Hentet", idag)}
    kendte = {d["id"] for d in docs}
    fra_eksport = [post(r, idag) for i, r in sorted(eks.items()) if i not in kendte]
    nye = [d for d in fra_eksport if d["id"].startswith("lta-")]
    andre = [d for d in fra_eksport if not d["id"].startswith("lta-")]
    stats["nye med ukendt type (udeladt)"] = sum(d["type"] == "ukendt" for d in nye)
    nye = [d for d in nye if d["type"] != "ukendt"]
    stats["nye dokumenter"] = len(nye)
    stats["heraf gældende"] = sum(d["status"]["vaerdi"] == "gældende" for d in nye)
    docs += nye
    alle = andre + docs
    ids = {d["id"]: d for d in alle}
    accession = {d["identifikatorer"].get("accession"): d["id"] for d in alle}
    for d in nye:
        if d["dokumentrolle"] == "ændring" and (maal := henvist(eks[d["id"]].get("ÆndrerI"), ids)):
            d["aendrer"] = maal
    familie = lambda i: ids[i].get("gaeldende_version") or ids[i].get("nyeste_version_afloeser_mangler") or i
    tls = [r["tidslinje"] for r in tidslinjer()]
    nulstil_afloeser(docs)
    ompeg = familier(docs, blev_historisk, [lovversioner(tl) for tl in tls])
    stats["lovfamilier flyttet til ny gældende version"] = len(ompeg)
    stats["love samlet efter Retsinformations tidslinje"] = sum(d.get("familie_metode") == "tidslinje" for d in docs)
    T, fund, udfald = modul("tekst", HERE / "tekst.py"), {}, collections.Counter()
    oprydning = {tuple(r.split("\t")[:2]) for r in OPRYDNING.read_text(encoding="utf-8").splitlines()[1:]}
    for o, cs in kandidater(ids, eks).items():
        u = [afloeser(ids[o], ids[c], T.afsnit(T.gzip.decompress(T.sti(c).read_bytes()).decode("utf-8", "replace"))) if T.sti(c).exists() else "ikke-hentet" for c in cs]
        bek = [x for x in u if isinstance(x, dict)]
        ok = sorted((x for x in bek if (o, x["vaerdi"]) not in oprydning), key=lambda x: ids[x["vaerdi"]]["datoer"].get("udstedt", ""))
        fund.update({o: ok[0]} if ok else {})
        udfald["bekræftet" if ok else "oprydning" if bek else "ikke-hentet" if "ikke-hentet" in u else "uden-tekst" if "uden-tekst" in u else "afvist"] += 1
        udfald["flere bekræftede"] += len(ok) > 1
    stats["love med afløserkandidater"] = dict(udfald)
    stats["dokumenter ført videre til afløserens gældende version"] = foelg_afloeser(ids, fund)

    hjemmel = {i: [accession[a] for a in r.get("HjemmelVedroerer", "").split(",") if a in accession and accession[a] != i] for i, r in eks.items() if i in ids}
    versioner = collections.defaultdict(list)
    for d in docs:
        if d["type"] in LOVE and d["dokumentrolle"] == "hoved":
            versioner[titelnoegle(d["navn"])].append(d)

    def forgaenger(d: dict) -> list[str]:
        aeldre = [v for v in versioner[titelnoegle(d["navn"])] if v["datoer"].get("udstedt", "") < d["datoer"].get("udstedt", "")] if d["type"] in LOVE else []
        return [max(aeldre, key=lambda v: v["datoer"]["udstedt"])["id"]] if aeldre else []

    kob = lovkobling(andre, [d for d in docs if d["type"] in ("lov", "ændringslov") and d["datoer"].get("udstedt")])
    sag = collections.defaultdict(list)
    for i, lov in kob.items():
        ids[i]["lov"] = lov
        sag[ids[i]["lovforslag"]].append(lov)
    stats["lovforslag koblet til lov"] = len(sag)
    foraeldre = {d["id"]: [*hjemmel.get(d["id"], []), *d.get("aendrer", []), *forgaenger(d), *sag.get(d.get("lovforslag"), [])] for d in nye + andre}
    reg = P.yaml.load(P.REG.read_text(encoding="utf-8"), Loader=P.yaml.CSafeLoader)
    svarfil = EKS / "klassifikation.json"
    omraader = {o["omraade"] for o in json.loads((L / "dashboard" / "omraader.json").read_text(encoding="utf-8"))}
    svar = json.loads(svarfil.read_text(encoding="utf-8")) if svarfil.exists() else {}
    foer = {d["id"]: (d.get("ministerium") or {}).get("vaerdi") for d in alle}
    rest = [d for d in klassificer(alle, foraeldre, eks, reg, {i: {**v, "retsomraade": v.get("retsomraade") if v.get("retsomraade") in omraader else None} for i, v in svar.items()}, idag) if d["id"].startswith("lta-")]
    stats["gældende uden fuld klassifikation"] = len(rest)
    ri = {d["id"] for d in alle if d["status"]["vaerdi"] == "gældende" and (d.get("ministerium") or {}).get("metode") == "retsinformation"}
    stats["ministerium fra Retsinformations ressortfelt"] = sum(i.startswith("lta-") for i in ri)
    stats["heraf rettet fra et andet ministerium"] = sum(foer[i] not in (None, ids[i]["ministerium"]["vaerdi"]) for i in ri)
    (EKS / "klassifikation_job.json").write_text(json.dumps(
        [{"id": d["id"], "navn": d["navn"], "type": d["type"], "ressortfelt": eks.get(d["id"], {}).get("Ressort"), "myndighed": eks.get(d["id"], {}).get("AdministrerendeMyndighed"),
          "ministerium": (d.get("ministerium") or {}).get("vaerdi"), "retsomraade": d.get("retsomraade")} for d in rest], ensure_ascii=False, indent=1), encoding="utf-8")

    kanter = [e for e in map(json.loads, (KAT / "kanter.jsonl").open(encoding="utf-8")) if e.get("metode") not in (METODE, PRAEAMBEL, FODNOTE, XMLTEKST, BESTEMMELSE)
              and not (e["type"] == "ressortansvar" and (e["to"] in ri or ids.get(e["to"], {}).get("status", {}).get("vaerdi") == "historisk"))]
    for e in kanter:
        if e["type"] == "henviser_til" and (e.get("gaeldende_version") or e["to"]) in ompeg:
            e["gaeldende_version"] = ompeg[e.get("gaeldende_version") or e["to"]]
        if (ids.get(e["to"], {}).get("familie_metode") == "tidslinje" or "afloeser_fra" in ids.get(e["to"], {})) and e["type"] == "henviser_til":
            for k in ("gaeldende_version", "nyeste_version_afloeser_mangler"):
                e.pop(k, None)
                if ids[e["to"]].get(k):
                    e[k] = ids[e["to"]][k]
    tekstfil = KAT / "tekst.jsonl"
    hentet = [t for t in map(json.loads, tekstfil.open(encoding="utf-8")) if t["id"] in ids] if tekstfil.exists() else []
    praeambel = {t["id"]: t["praeambel"] for t in hentet if "praeambel" in t}
    findes = {(e["from"], e["type"], e["to"]) for e in kanter}
    for i in sorted(hjemmel):
        if ids[i]["type"] in FORSKRIFTER or not i.startswith("lta-"):
            citeret = [(c, b) for c, b in P.praeambelhjemmel(praeambel.get(i, "")) if c in ids and c != i]
            love = list(dict.fromkeys(hjemmel[i]))
            kanter += [hjemmelkant(ids[i], ids[lov], [x for x in citeret if lovled(ids, x[0]) == lovled(ids, lov)]) for lov in love]
            stats["præamblens henvisninger"] += len(citeret)
            stats["hjemmelsfeltets dokumenter uden for præamblen"] += sum(all(familie(c) != familie(lov) for c, _ in citeret) for lov in love) if citeret else 0
            stats["forskrifter med læst præambel"] += bool(citeret)
            stats["præamblens henvisninger genfundet i hjemmelsfeltet"] += sum(any(familie(c) == familie(lov) for lov in love) for c, _ in citeret)
            kun = collections.defaultdict(list)
            for c, b in citeret:
                if (c, "hjemmel_for", i) not in findes and all(lovled(ids, c) != lovled(ids, lov) for lov in love):
                    kun[c] += b
            kanter += [{"from": c, "type": "hjemmel_for", "to": i, "beskrivelse": "hjemmel ifølge forskriftens præambel", "kilder": ids[i]["kilder"][:1],
                        "sikkerhed": "verificeret", "metode": PRAEAMBEL, **({"gaeldende_version": gv} if (gv := ids[c].get("gaeldende_version")) else {}),
                        "from_bestemmelse": list(dict.fromkeys(b))} for c, b in kun.items()]
    stats["hjemmel_for med bestemmelser"] = sum("from_bestemmelse" in e for e in kanter)
    stats["heraf kun fra præamblen"] = sum(e.get("metode") == PRAEAMBEL for e in kanter)
    for d in andre:
        love = [d["lov"]] if "lov" in d else [] if d["type"] == "lovforslag-som-vedtaget" else sag.get(d.get("lovforslag"), [])
        kanter += [{"from": d["id"], "type": "henviser_til", "to": lov, "beskrivelse": "forarbejde til loven (koblet på den vedtagne teksts titel og dato)",
                    "kilder": d["kilder"], "sikkerhed": "sandsynlig", "metode": METODE} for lov in dict.fromkeys(love)]
    laest = {t["id"] for t in hentet if t.get("n_tegn") and t["id"].startswith("lta-")}
    stats["implementerer_EU fra samforekomst fjernet (fodnoten er læst)"] = sum(e.get("metode") == SAMFOREKOMST and e["from"] in laest for e in kanter)
    kanter = [{**e, "sikkerhed": "ukendt"} if e.get("metode") == SAMFOREKOMST else e for e in kanter if not (e.get("metode") == SAMFOREKOMST and e["from"] in laest)]
    findes = {(e["from"], e["type"], e["to"]) for e in kanter}
    for t in hentet:
        i, d = t["id"], ids[t["id"]]
        for eid in gennemfoerer(t.get("noter", [])) if i.startswith("lta-") else ():
            if (i, "implementerer_EU", eid) not in findes:
                kanter.append({"from": i, "type": "implementerer_EU", "to": eid, "beskrivelse": "dokumentets fodnote siger, at det gennemfører retsakten",
                               "kilder": d["kilder"][:1], "sikkerhed": "sandsynlig", "metode": FODNOTE})
        for noegle, n in (t.get("naevner") or {}).items() if not d.get("n_paragraffer") else ():
            c, dag = noegle.split("|")
            if c in ids and c != i and ids[c]["datoer"].get("udstedt") == dag and (i, "henviser_til", c) not in findes:
                kanter.append({"from": i, "type": "henviser_til", "to": c, "beskrivelse": f"nævner dokumentet (nr. og dato) {n} gang(e) i den hentede tekst",
                               "kilder": d["kilder"][:1], "sikkerhed": "verificeret", "metode": XMLTEKST,
                               **({"gaeldende_version": gv} if (gv := ids[c].get("gaeldende_version")) else {})})
    klager, tilsyn, _ = laeser(reg)
    tidslinje_for = {i: tl for tl in tls for i in lovversioner(tl)}
    for t in hentet:
        led = collections.defaultdict(lambda: collections.defaultdict(list))
        for par, saetning in t.get("klage_tilsyn", []) if t["id"].startswith("lta-") and ids[t["id"]].get("dokumentrolle") == "hoved" else ():
            for til, fra in klager(saetning):
                led[til, "klageinstans"]["afgoerelse_af"] += [fra] if fra else []
                led[til, "klageinstans"]["her"].append((par, saetning))
            for myndighed in tilsyn(saetning):
                led[myndighed, "tilsyn"]["her"].append((par, saetning))
        senere = senere_aendret(ids[t["id"]]["datoer"].get("udstedt", ""), tidslinje_for.get(t["id"]), eks.get(t["id"], {}).get("SenereAendringer"), ids) if led else []
        kanter += [{"from": node, "type": type_, "to": t["id"], "beskrivelse": x["her"][0][1][:400], "kilder": ids[t["id"]]["kilder"][:1], "sikkerhed": "sandsynlig",
                    "metode": BESTEMMELSE, "to_bestemmelse": list(dict.fromkeys(par for par, _ in x["her"])),
                    **({"afgoerelse_af": list(dict.fromkeys(x["afgoerelse_af"]))} if x["afgoerelse_af"] else {}), **({"senere_aendret_ved": senere} if senere else {})}
                   for (node, type_), x in led.items() if (node, type_, t["id"]) not in findes]
    stats["klageinstans fra dokumentets bestemmelser"] = sum(e.get("metode") == BESTEMMELSE and e["type"] == "klageinstans" for e in kanter)
    stats["heraf med afgørende myndighed"] = sum(e.get("metode") == BESTEMMELSE and "afgoerelse_af" in e for e in kanter)
    stats["tilsyn fra dokumentets bestemmelser"] = sum(e.get("metode") == BESTEMMELSE and e["type"] == "tilsyn" for e in kanter)
    stats["heraf klage og tilsyn fra en tekst, der siden er ændret"] = sum(e.get("metode") == BESTEMMELSE and "senere_aendret_ved" in e for e in kanter)
    stats["implementerer_EU fra fodnoter"] = sum(e.get("metode") == FODNOTE for e in kanter)
    stats["henviser_til fra hentet tekst"] = sum(e.get("metode") == XMLTEKST for e in kanter)
    euindeks(kanter, ids)
    instans = myndigheder(reg)
    for d in andre:
        fra = instans.get(P.norm(eks[d["id"]].get("AdministrerendeMyndighed", ""))) if d["type"] in PRAKSIS or d["id"].startswith("fob-") else None
        if fra:
            kanter.append(udstederkant(d, *fra))
    stats["udsteder-kanter"] = sum(e["type"] == "udsteder" for e in kanter)
    nye_ids = {d["id"] for d in nye}
    for d in alle:
        m = d.get("ministerium") or {}
        if d["status"]["vaerdi"] == "gældende" and m.get("vaerdi") and (d["id"] in ri or d["id"] in nye_ids):
            kanter.append({"from": m["vaerdi"], "type": "ressortansvar", "to": d["id"], "beskrivelse": f"Nuværende ressort ({m['metode']})",
                           "kilder": d["kilder"] if m["sikkerhed"] == "verificeret" else [], "sikkerhed": m["sikkerhed"], "metode": METODE})
    stats["hjemmel_for-kanter"] = sum(e["type"] == "hjemmel_for" for e in kanter)
    for d in docs:
        d.pop("registry_ids", None)
    for n in reg["nodes"]:
        if n.get("katalog_id") in ids:
            ids[n["katalog_id"]].setdefault("registry_ids", []).append(n["id"])
    stats["dokumenter koblet til registry"] = sum("registry_ids" in d for d in alle)

    med = {e["to"] for e in kanter if e["type"] == "hjemmel_for"}
    kid = {n["id"]: n.get("katalog_id") for n in reg["nodes"]}
    med |= {kid[e["to"]] for e in reg["edges"] if e["type"] == "hjemmel_for" and kid.get(e["to"])}
    tal = daekning(docs, kanter, med)
    stats["gældende danske forskrifter"] = sum(c["regulering"] for c in tal.values())
    stats["heraf med hjemmel_for"] = sum(c["hjemmel"] for c in tal.values())
    dashboard(tal, docs, reg)
    (KAT / "retsinformation_lta.jsonl").write_text("".join(map(linje, docs)), encoding="utf-8")
    (KAT / "kanter.jsonl").write_text("".join(map(linje, kanter)), encoding="utf-8")
    koblet = {e["from"] if e["type"] == "henviser_til" else e["to"] for e in kanter if e.get("metode") == METODE and e["type"] in ("hjemmel_for", "henviser_til")}
    for s in ANDRE:
        ds = [d for d in andre if d["id"].startswith(s + "-")]
        gd = [d for d in ds if d["status"]["vaerdi"] == "gældende"]
        (KAT / f"retsinformation_{s}.jsonl").write_text("".join(map(linje, ds)), encoding="utf-8")
        stats[s] = {"dokumenter": len(ds), "gældende": len(gd), "gældende koblet til lovgivning": sum(d["id"] in koblet for d in gd),
                    "ministerium": dict(collections.Counter((d.get("ministerium") or {}).get("metode", "ingen") for d in gd)),
                    "med retsområde": sum(bool(d.get("retsomraade")) for d in gd), "koblet til registry": sum("registry_ids" in d for d in ds)}
    return dict(stats)


def unavngivne() -> str:
    """Navnene på de steder i klage- og tilsynssætningerne (tekst.jsonl), hvor læseren venter en instans uden at finde én, for de dokumenter, katalog læser:
    antal sætninger og dokumenter pr. navn, flest dokumenter først, og et eksempel."""
    reg = P.yaml.load(P.REG.read_text(encoding="utf-8"), Loader=P.yaml.CSafeLoader)
    hoved = {d["id"] for d in map(json.loads, (KAT / "retsinformation_lta.jsonl").open(encoding="utf-8")) if d.get("dokumentrolle") == "hoved"}
    ukendte = laeser(reg)[2]
    saetninger, dok, eks = collections.Counter(), collections.defaultdict(set), {}
    for t in map(json.loads, (KAT / "tekst.jsonl").open(encoding="utf-8")):
        for par, saetning in t.get("klage_tilsyn", []) if t["id"] in hoved else ():
            for f in ukendte(saetning):
                saetninger[f] += 1
                dok[f].add(t["id"])
                eks.setdefault(f, f"{t['id']} {par}: {saetning[:200]}")
    raekker = sorted(saetninger, key=lambda f: (-len(dok[f]), -saetninger[f], f))
    return "navn\tsætninger\tdokumenter\teksempel\n" + "".join(f"{f}\t{saetninger[f]}\t{len(dok[f])}\t{eks[f]}\n" for f in raekker)


def selftest() -> None:
    assert intervaller({"2001": 2000, "2002": 900, "2004": 2500, "2005": 100}) == [("", "2003", 2900), ("2004", "", 2600)]
    assert intervaller({}) == [] and intervaller({"1999": 5}) == [("", "", 5)]
    assert linje({"a": "æ\u2029b\x85c"}) == '{"a": "æ\\u2029b\\u0085c"}\n' and json.loads(linje({"a": "æ\u2029b"})) == {"a": "æ\u2029b"}
    csvtekst = '"Rank";"DokumentType";"Titel";"Historisk";"EliUrl"\r\n"B";"Bekendtgørelse";"Bekendtgørelse om æbler";"";"https://retsinformation.dk/eli/lta/2026/5"\r\n'
    assert raekker(csvtekst.encode("utf-16-le")) == [{"DokumentType": "Bekendtgørelse", "Titel": "Bekendtgørelse om æbler", "EliUrl": "https://retsinformation.dk/eli/lta/2026/5"}]
    global EKS
    EKS, gem_get, kald = Path(tempfile.mkdtemp()), P.get, []
    (EKS / "hentet").write_text("2026-11-12", encoding="utf-8")
    (EKS / "lta.jsonl").write_text(linje({"EliUrl": "https://retsinformation.dk/eli/lta/2026/5", "Historisk": "False"}) + linje({"EliUrl": "https://retsinformation.dk/eli/lta/2001/2"}), encoding="utf-8")
    P.get = lambda url: kald.append(url) or ("ok", (csvtekst + '"A";"Bekendtgørelse";"Bekendtgørelse om pærer";"";"https://retsinformation.dk/eli/lta/2026/6"\r\n').encode("utf-16-le"))
    try:
        assert hent("lta", "2025") == {"lta": {"nye": 1, "ajourført": 1, "uændrede": 1}} and kald == [P.RI + "/api/documentsearch/csv?ppm=1&yl=2025"]
        flettet = {r["EliUrl"][-6:]: r for r in map(json.loads, (EKS / "lta.jsonl").open(encoding="utf-8"))}
        assert flettet["2026/5"] == {"DokumentType": "Bekendtgørelse", "Titel": "Bekendtgørelse om æbler", "EliUrl": "https://retsinformation.dk/eli/lta/2026/5", "Hentet": str(datetime.date.today())}
        assert flettet["2001/2"] == {"EliUrl": "https://retsinformation.dk/eli/lta/2001/2"} and (EKS / "hentet").read_text(encoding="utf-8") == "2026-11-12"
        assert hent("lta", "2013", "2013")["lta"]["nye"] == 0 and kald[-1] == P.RI + "/api/documentsearch/csv?ppm=1&yl=2013&yh=2013"
    finally:
        P.get = gem_get
    assert post({**flettet["2026/5"], "Hentet": "2026-11-23"}, "2026-11-12")["status"]["pr"] == "2026-11-23"
    r = {"DokumentType": "Ændringsbekendtgørelse", "Titel": "Bekendtgørelse om ændring af bekendtgørelse om æbler for Grønland", "Ressort": "Æbleministeriet", "Nummer": "5",
         "DokumentId": "AB000001", "ACCN": "B20260000505", "UnderskriftDato": "20260702", "PubliceretTidspunkt": "20260704", "Historisk": "True", "HistoriskDato": "20261001",
         "GeografiskDækning": "Kun Grønland", "EliUrl": "https://retsinformation.dk/eli/lta/2026/5"}
    d = post(r, "2026-11-12")
    assert (d["id"], d["type"], d["dokumentrolle"], d["territorium"], d["status"]["vaerdi"]) == ("lta-2026-5", "ændringsbekendtgørelse", "ændring", "GL", "historisk")
    assert d["identifikatorer"]["lovtidende"] == "BEK nr. 5 af 02/07/2026" and d["datoer"] == {"udstedt": "2026-07-02", "historisk_markeret": "2026-10-01", "ri_registreret": "2026-07-04"}
    assert d["udstedt_af"] == {"vaerdi": "Æbleministeriet", "metode": METODE, "praefiks": "AB", "sikkerhed": "verificeret"} and "seed_fil" not in d
    assert post({**r, "DokumentType": "Anordningsbekendtgørelse", "GeografiskDækning": ""}, "x")["type"] == "bekendtgørelse-af-anordning"
    v = post({"DokumentType": "Cirkulære (1 sp)", "Titel": "Cirkulære om æbler", "Ressort": "Æbleministeriet", "DokumentId": "AB000002", "ACCN": "C20260990109",
              "UnderskriftDato": "20260702", "Historisk": "False", "EliUrl": "https://retsinformation.dk/eli/retsinfo/2026/9901"}, "2026-11-12")
    assert (v["id"], v["type"], v["kilder"]) == ("retsinfo-2026-9901", "cirkulære", [P.RI + "/eli/retsinfo/2026/9901"])
    assert "dokumentrolle" not in v and "lovtidende" not in v["identifikatorer"] and v["datoer"] == {"udstedt": "2026-07-02"}
    afg = post({**r, "DokumentType": "Endelig adm. afgørelse", "UnderskriftDato": "", "EliUrl": "https://retsinformation.dk/eli/mt/2001/12"}, "x")
    assert (afg["id"], afg["type"], "udstedt" in afg["datoer"]) == ("mt-2001-12", "endelig-adm-afgørelse", False)
    lov = {"id": "lta-2020-7", "gaeldende_version": "lta-2024-1031"}
    assert [(k["from"], k["type"], k["to"], k.get("gaeldende_version")) for k in (hjemmelkant(v, lov), hjemmelkant(afg, lov), hjemmelkant(d, {"id": "lta-2019-1"}))] == [
        ("lta-2020-7", "hjemmel_for", "retsinfo-2026-9901", "lta-2024-1031"), ("mt-2001-12", "henviser_til", "lta-2020-7", "lta-2024-1031"),
        ("lta-2019-1", "hjemmel_for", "lta-2026-5", None)]
    assert hjemmelkant(d, lov)["beskrivelse"].startswith("hjemmel ifølge") and hjemmelkant(afg, lov)["kilder"] == [P.RI + "/eli/mt/2001/12"]
    med = hjemmelkant(d, lov, [("lta-2010-3", ["§ 1", "§ 2"]), ("lta-2010-3", ["§ 2", "§ 4"])])
    assert (med["from_bestemmelse"], med["citeret_version"]) == (["§ 1", "§ 2", "§ 4"], "lta-2010-3") and "from_bestemmelse" not in hjemmelkant(afg, lov, [("lta-2020-7", ["§ 1"])])
    assert "citeret_version" not in hjemmelkant(d, lov, [("lta-2020-7", ["§ 1"])]) and "from_bestemmelse" not in hjemmelkant(d, lov, [])
    ft = [post({"DokumentType": t, "Titel": n, "Nummer": nr, "UnderskriftDato": u, "EliUrl": "https://retsinformation.dk/eli/ft/" + k}, "x")
          for t, n, nr, u, k in (("Lovforslag som vedtaget", "Forslag til Lov om æbler\\n(Flere æbler)", "17 B", "20260601", "202523LB0017"),
                                 ("Lovforslag som fremsat", "Forslag til Lov om æbler og pærer", "17", "20260301", "202522L00017"),
                                 ("Lovforslag som vedtaget", "Forslag til Lov om pærer", "18", "20260601", "202523L00018"),
                                 ("Beslutningsforslag som fremsat", "Forslag til folketingsbeslutning om æbler", "17", "20260301", "20252BB00017"))]
    assert [(x["id"], x["type"], x.get("lovforslag")) for x in ft[:2]] == [("ft-202523LB0017", "lovforslag-som-vedtaget", "20252-17"), ("ft-202522L00017", "lovforslag-som-fremsat", "20252-17")]
    assert ft[0]["kilder"] == [P.RI + "/eli/ft/202523LB0017"] and "lovforslag" not in ft[3] and nid("https://retsinformation.dk/eli/lta/2026/5/") == "lta-2026-5"
    love = [{"id": i, "navn": n, "datoer": {"udstedt": u}} for i, n, u in (("l1", "Lov om æbler (Flere æbler)", "2026-06-09"), ("l2", "Lov om pærer", "2026-06-02"),
                                                                           ("l3", "Lov om pærer", "2026-06-20"), ("l4", "Lov om æbler (Flere æbler)", "2025-06-09"))]
    assert lovkobling(ft, love) == {"ft-202523LB0017": "l1"}
    assert henvist("LBK nr 1031 af 06/09/2024,VEJ nr 9139 af 25/02/2019,LOV nr 7 af 01/01/2020", {"lta-2024-1031": 1, "lta-2020-7": 1}) == ["lta-2024-1031", "lta-2020-7"]

    def lov(i, navn, aar, status, **mere):
        return {"id": i, "navn": navn, "type": "lovbekendtgørelse", "dokumentrolle": "hoved", "status": {"vaerdi": status}, "datoer": {"udstedt": f"{aar}-01-01"}, **mere}

    fam = [lov("a", "Bekendtgørelse af æbleloven (* 1)", 2020, "historisk", gaeldende_version="b"), lov("b", "Bekendtgørelse af æbleloven", 2025, "historisk"),
           lov("c", "Bekendtgørelse af æbleloven", 2026, "gældende"), lov("p", "Bekendtgørelse af pæreloven", 2019, "historisk", nyeste_version_afloeser_mangler="q"),
           lov("q", "Bekendtgørelse af pæreloven", 2024, "historisk", afloeser_mangler=True), lov("k", "Bekendtgørelse af kirsebærloven", 2024, "historisk")]
    assert familier(fam, {"b", "k"}) == {"b": "c"}
    assert [x.get("gaeldende_version") for x in fam] == ["c", "c", None, None, None, None] and fam[3]["nyeste_version_afloeser_mangler"] == "q"
    assert fam[4]["afloeser_mangler"] and fam[5]["afloeser_mangler"] and "afloeser_mangler" not in fam[1]
    tl = [{"href": "/eli/lta/1998/452", "documentTypeId": 30}, {"href": "/eli/lta/2001/228", "documentTypeId": 20}, {"href": "/eli/lta/1996/485", "documentTypeId": 10, "isMainLaw": False},
          {"href": "/eli/lta/1975/323", "documentTypeId": 10, "isMainLaw": True}, {"href": None, "documentTypeId": 30}]
    klager, tilsyn, _ = laeser({"nodes": [{"id": "naevn-frugt", "type": "nævn", "navn": "Frugtklagenævnet"}, {"id": "sty-aeble", "type": "styrelse", "navn": "Æblestyrelsen"},
                                       {"id": "dom-domstolene", "type": "domstol", "navn": "Domstolene"}, {"id": "naevn-ae-og-p", "type": "nævn", "navn": "Æble- og Pærenævnet"}]})
    for saetning, ventet in (("Æblestyrelsens afgørelser efter § 4 kan påklages til Frugtklagenævnet.", [("naevn-frugt", "sty-aeble")]),
                             ("Afgørelser efter bekendtgørelsen kan indbringes for Æble- og Pærenævnet inden 4 uger.", [("naevn-ae-og-p", None)]),
                             ("Afgørelser efter § 4 kan ikke påklages til Frugtklagenævnet.", []),
                             ("Afgørelser kan ikke indbringes for anden administrativ myndighed end Frugtklagenævnet.", [("naevn-frugt", None)]),
                             ("Frugtklagenævnet behandler klager over afgørelser truffet af kommunalbestyrelsen.", [("naevn-frugt", "kommune-alle")]),
                             ("Klage til Frugtklagenævnet over kommunalbestyrelsens afgørelser indgives skriftligt.", [("naevn-frugt", "kommune-alle")]),
                             ("Klagen sendes til Æblestyrelsen.", []), ("Kommunalbestyrelsen skal indbringe en sag for Frugtklagenævnet.", []), ("Afgørelsen kan indbringes for domstolene.", []),
                             ("Bekendtgørelse nr. 3 af 2. maj 2017 om klage til Frugtklagenævnet ophæves.", []),
                             ("Frugtklagenævnet behandler klager over afgørelser truffet af kommunalbestyrelsen eller af Æblestyrelsen.", [("naevn-frugt", "kommune-alle"), ("naevn-frugt", "sty-aeble")]),
                             ("Kommunalbestyrelsens og Æblestyrelsens afgørelser kan ikke indbringes for anden administrativ myndighed end Frugtklagenævnet.",
                              [("naevn-frugt", "kommune-alle"), ("naevn-frugt", "sty-aeble")]),
                             ("Afgørelser truffet af Æblestyrelsen eller kommunalbestyrelsen kan påklages til Frugtklagenævnet.", [("naevn-frugt", "sty-aeble"), ("naevn-frugt", "kommune-alle")]),
                             ("Frugtklagenævnet behandler klager over frugt, der falder uden for Æblestyrelsens afgørelseskompetence.", [("naevn-frugt", None)]),
                             ("Klager over afgørelser truffet før den 1. januar 2007, som indbringes for Frugtklagenævnet, færdigbehandles efter de hidtil gældende regler.", [])):
        assert klager(saetning) == ventet, (saetning, klager(saetning))
    for saetning, ventet in (("Æblestyrelsen fører tilsyn med, at reglerne overholdes.", ["sty-aeble"]), ("I disse sager fører kommunalbestyrelsen tilsyn med anlægget.", ["kommune-alle"]),
                             ("Tilsynet med overholdelsen føres af Æblestyrelsen.", ["sty-aeble"]), ("Æblestyrelsen varetager tilsynet.", ["sty-aeble"]),
                             ("Virksomheder under tilsyn af Æblestyrelsen skal indberette.", []), ("Den, der fører tilsyn, skal have adgang.", []), ("Æblestyrelsen kan føre kontrol og tilsyn med frugten.", ["sty-aeble"]),
                             ("Æblestyrelsen påser, at reglerne overholdes.", ["sty-aeble"]), ("Æblestyrelsen kontrollerer, at kravet overholdes.", ["sty-aeble"]),
                             ("Ved syn kontrollerer Æblestyrelsen, at kravene overholdes.", ["sty-aeble"]), ("Æblestyrelsen påser, at ansøgningen indeholder oplysningerne.", []),
                             ("Æblestyrelsen påser, at betingelserne for tilskud er opfyldt.", []), ("Bekendtgørelse nr. 3 af 2. maj 2017 om Æblestyrelsens tilsyn med frugt ophæves.", []),
                             ("Når en afgørelse er indbragt for Frugtklagenævnet, påser Æblestyrelsen, at fristen overholdes.", ["sty-aeble"]), ("Enhver, der ejer eller kontrollerer virksomheden, skal oplyse det.", []),
                             ("Æblestyrelsen er dog tilsynsmyndighed for frugtplantager.", ["sty-aeble"]),
                             ("Kommunalbestyrelsen er ikke tilsynsmyndighed for frugtplantager.", []), ("Æblestyrelsen påser ikke, at reglerne overholdes.", []),
                             ("Æblestyrelsen kontrollerer ansøgningen, og ansøgeren skal overholde fristen.", []),
                             ("Æblestyrelsen fører ikke tilsyn med frugtplantager.", []), ("Tilsynet med frugtplantager udøves ikke af Æblestyrelsen.", []),
                             ("Æblestyrelsen fører ikke længere tilsyn med frugtplantager.", []), ("Æblestyrelsen fører hverken tilsyn eller kontrol med frugten.", []),
                             ("Modtageren skal give de oplysninger, der har betydning for Æblestyrelsens kontrol med, at vilkårene overholdes.", ["sty-aeble"]),
                             ("Æblestyrelsens tilsyn med plantagerne sker ved stikprøver.", ["sty-aeble"]),
                             ("Avleren skal efter anmodning fra Æblestyrelsen give de oplysninger, der har betydning for styrelsens kontrol med, at vilkårene overholdes.", ["sty-aeble"]),
                             ("Kommunalbestyrelsen skal give de oplysninger, der har betydning for styrelsens kontrol med, at vilkårene overholdes.", []), ("Avlerens kontrol med egen frugt dokumenteres.", []),
                             ("Afgørelsen sendes desuden til Æblestyrelsen til brug for Æblestyrelsens tilsyn med frugt efter frugtloven.", [])):
        assert tilsyn(saetning) == ventet, (saetning, tilsyn(saetning))
    klager, tilsyn, ukendte = laeser({"nodes": [{"id": "naevn-frugt", "type": "nævn", "navn": "Frugtklagenævnet"}, {"id": "min-ae", "type": "ministerium", "navn": "Æbleministeriet",
                                                "tidligere_navne": [{"navn": "Frugt- og Bærministeriet"}]}, {"id": "min-p", "type": "ministerium", "navn": "Ministeriet for Pærer"}]})
    for saetning, ventet in (("Afgørelser kan påklages til Pærestyrelsen inden 4 uger.", ["pærestyrelsen"]), ("Afgørelser kan påklages til Frugtklagenævnet.", []),
                             ("Afgørelser efter § 4 kan ikke påklages til Pærestyrelsen.", []), ("Styrelsen for Pæresikkerhed behandler klager over afgørelser.", ["styrelsen for pæresikkerhed"]),
                             ("Tilsynet føres af den kompetente myndighed.", ["den kompetente myndighed"]), ("Kirsebær-, blomme- og sveskeministeren fører tilsyn med loven.", ["kirsebær blomme og sveskeministeren"]),
                             ("Afgørelsen kan påklages til Rigsfrugtchefen, og Pærenævnet fører tilsyn.", ["rigsfrugtchefen", "pærenævnet"]), ("Afgørelsen kan påklages til æbleministeren.", []),
                             ("Tilsynet føres af (jf. § 3) Pærestyrelsen.", [])):
        assert ukendte(saetning) == ventet, (saetning, ukendte(saetning))
    assert klager("Afgørelsen kan påklages til frugt- og bærministeren.") == [("min-ae", None)] and tilsyn("Ministeren for Pærer fører tilsyn.") == ["min-p"]
    assert klager("Æbleministerens afgørelser kan påklages til Frugtklagenævnet.") == [("naevn-frugt", "min-ae")]
    to = laeser({"nodes": [{"id": "sty-ae-og-p", "type": "styrelse", "navn": "Æble- og Pærestyrelsen"}, {"id": "sty-p", "type": "styrelse", "navn": "Pærestyrelsen"}]})[1]
    assert to("Avleren skal efter anmodning fra Æble- og Pærestyrelsen give oplysninger til styrelsens kontrol med, at vilkårene overholdes.") == ["sty-ae-og-p"]
    assert to("Sagen sendes til brug for Æble- og Pærestyrelsens tilsyn med frugt efter frugtloven.") == []
    assert tilsyn("Avleren giver Æblestyrelsen og Frugtklagenævnet de oplysninger, der har betydning for nævnets kontrol med, at vilkårene overholdes.") == ["naevn-frugt"]
    ft = laeser({"nodes": [{"id": "sty-frugttilsynet", "type": "styrelse", "navn": "Frugttilsynet"}, {"id": "sty-p", "type": "styrelse", "navn": "Pærestyrelsen"}]})[1]
    assert ft("Avleren giver Frugttilsynet og Pærestyrelsen de oplysninger, der har betydning for tilsynets kontrol med, at vilkårene overholdes.") == ["sty-frugttilsynet"]
    ret = laeser({"nodes": [{"id": "dom-hoejesteret", "type": "domstol", "navn": "Højesteret"}, {"id": "naevn-frugt", "type": "nævn", "navn": "Frugtklagenævnet"}]})[0]
    assert ret("Dommen kan ankes til Højesteret.") == [] == ret("Fristen for ansøgning om tilladelse til anke til Højesteret er udløbet.")
    assert ret("Klagerettens afgørelse kan indbringes for Højesteret efter reglerne om kære.") == [("dom-hoejesteret", None)] and ret("Afgørelsen kan ankes til Frugtklagenævnet.") == [("naevn-frugt", None)]
    kirke = {"nodes": [{"id": "min-by-land-og-kirke", "type": "ministerium", "navn": "By-, Land- og Kirkeministeriet", "status": "nedlagt", "tidligere_navne": [{"navn": "Kirkeministeriet"}]}]}
    assert laeser(kirke)[1]("Kirkeministeren fører tilsyn med provstiudvalgene.") == ["min-sundhed-og-kirke"] and laeser(kirke)[1]("Direktoratet for Kriminalforsorgen fører tilsyn.") == ["sty-danmarks-faengsler"]
    assert klager("Klage til taksationsmyndighederne skal være indgivet inden 4 uger.") == [("naevn-taksationsmyndighederne", None)]
    assert klager("Regionsrådets afgørelser kan påklages til Frugtklagenævnet.") == [("naevn-frugt", "region-alle")]
    assert tilsyn("Tilsyn med menighedsrådenes funktion udøves af biskoppen.") == ["tilsyn-biskopperne"] and tilsyn("Rigspolitichefen fører tilsyn med politidirektørerne.") == ["sty-rigspolitiet"]
    assert lovversioner(tl) == ["lta-1998-452", "lta-1975-323"]
    byg = [{"href": "/eli/lta/2016/1178", "documentTypeId": 30, "signatureDate": "25/09/2016"}, {"href": "/eli/lta/2014/1", "documentTypeId": 20, "signatureDate": "01/01/2014"},
           {"href": "/eli/lta/2018/734", "documentTypeId": 20, "signatureDate": "08/06/2018"}, {"href": "/eli/lta/2019/9", "documentTypeId": 10, "isMainLaw": False, "signatureDate": "01/03/2019"},
           {"href": "/eli/lta/2020/5", "documentTypeId": 90, "signatureDate": "01/01/2020"}, {"href": "/eli/lta/2018/734", "documentTypeId": 20, "signatureDate": "08/06/2018"},
           {"href": "/eli/lta/2021/7", "documentTypeId": 20, "signatureDate": "01/01/2021"}, {"href": "/eli/lta/2025/1", "documentTypeId": 30, "signatureDate": "01/01/2025"}]
    kendt = {i: {"datoer": {"udstedt": u}} for i, u in (("lta-2014-1", "2014-01-01"), ("lta-2018-734", "2018-06-08"), ("lta-2019-9", "2019-03-01"), ("lta-2020-5", "2020-01-01"),
                                                        ("lta-2025-1", "2025-01-01"), ("lta-2024-3", "2024-03-01"), ("lta-2010-2", "2010-01-01"))}
    assert senere_aendret("2016-09-25", byg, None, kendt) == ["lta-2018-734", "lta-2019-9"]
    assert senere_aendret("2025-01-01", byg, "LOV nr 3 af 01/03/2024", kendt) == []
    assert senere_aendret("2020-01-01", None, "BEK nr 3 af 01/03/2024,BEK nr 2 af 01/01/2010", kendt) == ["lta-2024-3"] and senere_aendret("2020-01-01", None, None, kendt) == []
    assert senere_aendret("", byg, None, kendt) == [] == senere_aendret("", None, "BEK nr 3 af 01/03/2024", kendt)
    omdoebt = [lov("s", "Bekendtgørelse af lov om sommerhuse", 2013, "historisk", afloeser_mangler=True), lov("u", "Bekendtgørelse af lov om udlejning", 2024, "gældende"),
               lov("g", "Bekendtgørelse af gammel lov", 1990, "historisk", gaeldende_version="u"), lov("h", "Bekendtgørelse af den gamle lov", 1995, "historisk")]
    assert familier(omdoebt, set(), [["s", "u", "findes-ikke"], ["g", "h"]]) == {}
    assert [(x.get("gaeldende_version"), x.get("nyeste_version_afloeser_mangler"), x.get("afloeser_mangler")) for x in omdoebt] == [("u", None, None), (None, None, None), (None, "h", None), (None, None, None)]
    assert all(x["familie_metode"] == "tidslinje" for x in omdoebt) and "familie_metode" not in fam[0]
    straf = [lov("f1", "Bekendtgørelse af lov om fuldbyrdelse af straf m.v.", 2019, "historisk"), lov("f2", "Bekendtgørelse af lov om fuldbyrdelse af straf m.v.", 2023, "historisk"),
             lov("f3", "Bekendtgørelse af lov om fuldbyrdelse af straf m.v.", 2026, "gældende"), lov("f0", "Bekendtgørelse af lov om fuldbyrdelse af straf m.v.", 2010, "gældende"),
             lov("z1", "Bekendtgørelse af lov om zoner", 2020, "gældende"), lov("z2", "Bekendtgørelse af lov om zoner", 2026, "gældende")]
    assert familier(straf, set(), [["f1", "f2"], ["z1"]]) == {}
    assert [x.get("gaeldende_version") for x in straf] == ["f3", "f3", None, None, "z2", None] and "familie_metode" not in straf[2]
    gl = {"lta-2013-155": {**lov("lta-2013-155", "Lov om visse produkter", 2013, "historisk"), "type": "lov"},
          "lta-2010-9": lov("lta-2010-9", "Bekendtgørelse af æbleloven", 2010, "historisk", gaeldende_version="lta-2024-1"),
          "lta-2024-500": {**lov("lta-2024-500", "Lov om produkter", 2024, "gældende"), "type": "lov"},
          "lta-2015-10": {**lov("lta-2015-10", "Lov om ændring af lov om visse produkter", 2015, "historisk"), "type": "ændringslov", "dokumentrolle": "ændring"},
          "lta-2020-3": {**lov("lta-2020-3", "Lov om pærer", 2020, "gældende"), "type": "lov"}, "lta-2024-1": lov("lta-2024-1", "Bekendtgørelse af æbleloven", 2024, "gældende")}
    rows = {"lta-2013-155": {"SenereAendringer": "LOV nr 10 af 01/01/2015,LOV nr 3 af 01/01/2020,LOV nr 500 af 01/01/2024"},
            "lta-2010-9": {"SenereAendringer": "LOV nr 500 af 01/01/2024"}, "lta-2015-10": {"ÆndrerI": "LOV nr 155 af 01/01/2013"},
            "lta-2020-3": {"ÆndrerI": "LOV nr 1 af 01/01/2019"}, "lta-2024-500": {"ÆndrerI": "LOV nr 155 af 01/01/2013,LBK nr 9 af 01/01/2010"}}
    assert kandidater(gl, rows) == {"lta-2013-155": ["lta-2024-500"]}
    gammel, ny, lbk = gl["lta-2013-155"] | {"datoer": {"udstedt": "2013-02-20"}}, gl["lta-2024-500"] | {"kilder": [P.RI + "/eli/lta/2024/500/xml"]}, gl["lta-2010-9"] | {"datoer": {"udstedt": "2010-03-04"}}
    bevar = "Regler, der er fastsat i henhold til lov nr. 155 af 20. februar 2013, forbliver i kraft, indtil de ophæves."
    for tekster, gl_, kand, ventet in (
            ([("§ 40", f"§ 40. Loven træder i kraft den 1. juli 2024.\nStk. 2. Lov nr. 155 af 20. februar 2013 om visse produkter ophæves.\nStk. 3. {bevar}")], gammel, ny,
             ("Lov nr. 155 af 20. februar 2013 om visse produkter ophæves.", "§ 40", bevar)),
            ([("§ 9", "§ 9. Lov om æbler, jf. lovbekendtgørelse nr. 9 af 4. marts 2010, ophæves.")], lbk, ny, ("Lov om æbler, jf. lovbekendtgørelse nr. 9 af 4. marts 2010, ophæves.", "§ 9", None)),
            ([("§ 9", "§ 9. Samtidig ophæves:\n1) lov nr. 3 af 1. maj 1999 om pærer,\n2) lov om æbler, jf. lovbekendtgørelse nr. 9 af 4. marts 2010.")], lbk, ny,
             ("2) lov om æbler, jf. lovbekendtgørelse nr. 9 af 4. marts 2010.", "§ 9", None)),
            ([("§ 9", "§ 9. Følgende love ophæves ved lovens ikrafttræden:\n1) Lov om æbler, jf. lovbekendtgørelse nr. 9 af 4. marts 2010.")], lbk, ny,
             ("1) Lov om æbler, jf. lovbekendtgørelse nr. 9 af 4. marts 2010.", "§ 9", None)),
            ([("§ 9", "§ 9. Ministeren kan fastsætte, at lov nr. 155 af 20. februar 2013 ophæves.")], gammel, ny, "afvist"),
            ([("§ 9", "§ 9. Lov om æbler, jf. lovbekendtgørelse nr. 9 af 4. marts 2010, ophæves, bortset fra §§ 8-11.")], lbk, ny, "afvist"),
            ([("§ 9", "§ 9. Lov om æbler, jf. lovbekendtgørelse nr. 9 af 4. marts 2010, ophæves med undtagelse af § 3.")], lbk, ny, "afvist"),
            ([("§ 9", "§ 9. § 2 og § 5 i lov nr. 155 af 20. februar 2013 ophæves.")], gammel, ny, "afvist"),
            ([("§ 9", "§ 9. Retsplejelovens § 7, jf. lovbekendtgørelse nr. 9 af 4. marts 2010, ophæves.")], lbk, ny, "afvist"),
            ([("§ 9", "§ 9. § 14\ni lov om æbler og pærer, jf. lovbekendtgørelse nr. 9 af 4. marts 2010, ophæves.")], lbk, ny, "afvist"),
            ([("§ 9", ("§ 9. Lov om pærer, jf. lovbekendtgørelse nr. 2 af 4. marts 2009, som ændret ved § 3 i lov nr. 1 af 1. maj 2009, og lov om æbler og\n"
                       "pærer, jf. lovbekendtgørelse nr. 9 af 4. marts 2010, ophæves."))], lbk, ny,
             ("Lov om pærer, jf. lovbekendtgørelse nr. 2 af 4. marts 2009, som ændret ved § 3 i lov nr. 1 af 1. maj 2009, og lov om æbler og pærer, jf. lovbekendtgørelse nr. 9 af 4. marts 2010, ophæves.", "§ 9", None)),
            ([("§ 9", "§ 9. Lov om visse produkter, som affattet ved lov nr. 155 af 20. februar 2013, ophæves.")], gammel, ny, "afvist"),
            ([("§ 9", "§ 9. Lov om visse produkter, som ændret ved lov nr. 155 af 20. februar 2013, ophæves.")], gammel, ny, "afvist"),
            ([("§ 9", "§ 9. Lov nr. 155 af 20. februar 2013 om visse produkter ophæves.")], gammel, gl["lta-2024-1"], "afvist"),
            ([("§ 1", "§ 1. Lov nr. 155 af 20. februar 2013 om visse produkter ophæves.")], gammel, ny | {"navn": "Lov om ophævelse af lov om visse produkter"}, "afvist"),
            ([("§ 9", "§ 9. Lov nr. 155 af 20. februar 2012 om visse produkter ophæves.")], gammel, ny, "afvist"),
            ([], gammel, ny, "uden-tekst")):
        u = afloeser(gl_, kand, tekster)
        assert (u if isinstance(u, str) else (u["ophaevelse"], u["paragraf"], u.get("bevarer_regler"))) == ventet, (tekster, u)
    u = afloeser(gammel, ny, [("§ 40", "§ 40. Lov nr. 155 af 20. februar 2013 om visse produkter ophæves.")])
    assert u == {"vaerdi": "lta-2024-500", "ophaevelse": "Lov nr. 155 af 20. februar 2013 om visse produkter ophæves.", "paragraf": "§ 40",
                 "paragraf_tekst": "§ 40. Lov nr. 155 af 20. februar 2013 om visse produkter ophæves.", "kilder": [P.RI + "/eli/lta/2024/500/xml"],
                 "sikkerhed": "verificeret", "metode": "ophaevelsesbestemmelse", "bevarer_regler": None}
    pdl = [{**lov("lta-2000-429", "Lov om behandling af personoplysninger", 2000, "historisk", afloeser_mangler=True), "type": "lov"},
           lov("lta-2001-1", "Bekendtgørelse af lov om behandling af personoplysninger", 2001, "historisk", nyeste_version_afloeser_mangler="lta-2000-429"),
           {**lov("lta-2018-502", "Databeskyttelsesloven", 2018, "historisk", gaeldende_version="lta-2024-289"), "type": "lov"},
           lov("lta-2024-289", "Bekendtgørelse af databeskyttelsesloven", 2024, "gældende"), {**lov("lta-1990-5", "Lov om x", 1990, "historisk", afloeser_mangler=True), "type": "lov"}]
    pids = {d["id"]: d for d in pdl}
    fund = {"lta-2001-1": {"vaerdi": "lta-2018-502"}, "lta-1990-5": {"vaerdi": "lta-2000-429"}}
    assert foelg_afloeser(pids, fund) == 3
    assert [(d.get("gaeldende_version"), d.get("afloeser_fra"), "afloeser_mangler" in d or "nyeste_version_afloeser_mangler" in d) for d in pdl] == [
        ("lta-2024-289", "lta-2000-429", False), ("lta-2024-289", "lta-2000-429", False), ("lta-2024-289", None, False), (None, None, False), ("lta-2024-289", "lta-1990-5", False)]
    assert pdl[1]["afloeser"] == {"vaerdi": "lta-2018-502"} and "afloeser" not in pdl[0]
    assert [lovled(pids, i) for i in pids] == ["lta-2000-429", "lta-2000-429", "lta-2024-289", "lta-2024-289", "lta-1990-5"] and lovled(pids, "x") == "x"
    nulstil_afloeser(pdl)
    assert [(d.get("gaeldende_version"), d.get("afloeser_mangler"), d.get("nyeste_version_afloeser_mangler"), "afloeser" in d) for d in pdl] == [
        (None, True, None, False), (None, None, "lta-2000-429", False), ("lta-2024-289", None, None, False), (None, None, None, False), (None, True, None, False)]
    reg = {"regering": {"dannet": "2026-06-03"}, "nodes": [{"id": "min-ae", "type": "ministerium", "status": "aktiv", "navn": "Æbleministeriet"}]}
    inst = [{"id": "naevn-ae", "type": "nævn", "navn": "Æblenævnet (ÆN)", "tidligere_navne": [{"navn": "Frugtnævnet"}, {"navn": "Det Gamle Nævn"}]},
            {"id": "naevn-p", "type": "nævn", "navn": "Pærenævnet", "tidligere_navne": [{"navn": "Det Gamle Nævn"}]}, {"id": "lov-x", "type": "lov", "navn": "Lovnævnet"}]
    uk = [udstederkant(afg, "naevn-ae", nu) for nu in (True, False)]
    assert [(k["from"], k["to"], k["sikkerhed"], k["beskrivelse"].endswith("Retsinformation")) for k in uk] == [("naevn-ae", "mt-2001-12", "verificeret", True),
                                                                                                                ("naevn-ae", "mt-2001-12", "sandsynlig", False)]
    assert uk[1]["beskrivelse"] == uk[0]["beskrivelse"] + " (under et tidligere navn)" and uk[0]["kilder"] == [P.RI + "/eli/mt/2001/12"]
    note = ("1) Bekendtgørelsen indeholder bestemmelser, der gennemfører dele af Europa-Parlamentets og Rådets direktiv 2012/27/EU af 25. oktober 2012 om energieffektivitet, "
            "om ændring af direktiv 2009/125/EF og 2010/30/EU samt om ophævelse af direktiv 2004/8/EF og 2006/32/EF, EU-Tidende 2012, nr. L 315, side 1, som ændret ved "
            "Rådets direktiv 2013/12/EU af 13. maj 2013, EU-Tidende 2013, nr. L 141, side 28, og senest ved Europa-Parlamentets og Rådets direktiv 2018/2002/EU, og dele "
            "af Rådets direktiv 98/24/EF af 7. april 1998 (fjortende særdirektiv i henhold til direktiv 89/391/EØF, artikel 16, stk. 1), EF-Tidende 1998, nr. L 131, "
            "side 11. I bekendtgørelsen er der medtaget visse bestemmelser fra forordning (EU) 2016/426. Bekendtgørelsen har som udkast været notificeret i "
            "overensstemmelse med Europa-Parlamentets og Rådets direktiv (EU) 2015/1535.")
    assert gennemfoerer([note, "2) Ressortansvaret er overført."]) == ["eu-dir-2012-27", "eu-dir-1998-24"] and gennemfoerer([]) == []
    assert gennemfoerer([("1) Bekendtgørelsen gennemfører direktiv 2018/2001/EU om vedvarende energi, EU-Tidende 2018, nr. L 328, s. 82, og direktiv (EU) 2023/2413 om ændring af "
                         "direktiv (EU) 2018/2001, forordning (EU) 2018/1999 og direktiv 98/70/EF og om ophævelse af direktiv (EU) 2015/652, EU-Tidende, L af 31. oktober 2023, "
                         "som ændret ved direktiv (EU) 2023/958 om passende gennemførelse af en ordning, EU-Tidende 2023, side 115 og ved direktiv (EU) 2023/959.")]) == ["eu-dir-2018-2001", "eu-dir-2023-2413"]
    assert gennemfoerer([("1) Bekendtgørelsen gennemfører direktiv 2013/64/EU om ændring af direktiv 91/271/EØF og direktiv 2000/60/EF, EU-tidende 2013, nr. L 353, side 8, dele af "
                         "direktiv 2000/60/EF om vandpolitiske foranstaltninger, EF-Tidende 2000, nr. L 327, side 1.")]) == ["eu-dir-2013-64", "eu-dir-2000-60"]
    assert gennemfoerer([("1) Bekendtgørelsen gennemfører direktiv 89/656/EØF (tredje særdirektiv i henhold til artikel 16, stk. 1, i direktiv 89/391/EØF), EF-Tidende 1989, nr. L 393, "
                         "side 18, som ændret ved direktiv 2007/30/EF af 20. juni 2007 om ændring af Rådets direktiv 89/391/EØF, EU-Tidende 2007, nr. L 165, side 21, og Rådets "
                         "direktiv 89/686/EØF af 21. december 1989 om personlige værnemidler, EF-Tidende 1989, nr. L 399, side 18.")]) == ["eu-dir-1989-656", "eu-dir-1989-686"]
    assert gennemfoerer([("1) Bekendtgørelsen gennemfører dele af direktiv 2005/36/EF, EU-tidende 2005, nr. L 255, side 22, som ændret ved Kommissionens forordning (EU) nr. "
                         "623/2012, EU-tidende 2012 nr. L 180, side 9 og Europa-Parlamentets og Rådets direktiv 2013/55/EU af 20. november 2013 om ændring af direktiv 2005/36/EF.")]) == ["eu-dir-2005-36"]
    delt = [{"id": "naevn-nm", "type": "klagenævn", "navn": "Frugtklagenævnet"}, {"id": "naevn-ny", "type": "klagenævn", "navn": "Æbleklagenævnet",
                                                                                "tidligere_navne": [{"navn": "Frugtklagenævnet (æblesager)"}, {"navn": "Bærnævnet"}]},
            {"id": "naevn-ny2", "type": "klagenævn", "navn": "Pæreklagenævnet", "tidligere_navne": [{"navn": "Bærnævnet"}]}]
    assert myndigheder({"nodes": delt})["frugtklagenævnet"] == ("naevn-nm", True) and "bærnævnet" not in myndigheder({"nodes": delt})
    assert myndigheder({"nodes": [{"id": "min-ae", "type": "ministerium", "navn": "Æbleministeriet", "tidligere_navne": [{"navn": "Frugtministeriet"}]}]}) == {
        "æbleministeriet": ("min-ae", True), "frugtministeriet": ("min-ae", False), "æbleministeren": ("min-ae", True), "frugtministeren": ("min-ae", False)}
    assert myndigheder({"nodes": inst}) == {"æblenævnet æn": ("naevn-ae", True), "æblenævnet": ("naevn-ae", True), "frugtnævnet": ("naevn-ae", False), "pærenævnet": ("naevn-p", True)}
    ny = [{"id": "n1", "status": {"vaerdi": "gældende"}, "datoer": {"udstedt": "2026-07-02"}}, {"id": "n2", "status": {"vaerdi": "gældende"}, "datoer": {"udstedt": "2026-01-02"}},
          {"id": "n3", "status": {"vaerdi": "gældende"}, "datoer": {"udstedt": "2026-01-02"}}, {"id": "c", "status": {"vaerdi": "gældende"}, "datoer": {},
                                                                                              "ministerium": {"vaerdi": "min-ae"}, "retsomraade": "frugt"}]
    ny[3]["gaeldende_version"] = "n1"
    ny += [{"id": "o", "status": {"vaerdi": "gældende"}, "datoer": {"udstedt": "2026-07-02"}, "ministerium": {"vaerdi": "min-pære", "sikkerhed": "sandsynlig"}, "retsomraade": "frugt"},
           {"id": "h", "status": {"vaerdi": "historisk"}, "datoer": {"udstedt": "2026-07-02"}, "ministerium": {"vaerdi": "min-pære"}}]
    felt = {i: {"Ressort": "Æbleministeriet"} for i in ("n1", "n2", "o", "h")}
    felt["o"]["Hentet"] = "2026-11-23"
    rest = klassificer(ny, {"n1": ["c"], "n2": ["n1"]}, felt, reg, {"n3": {"ministerium": "min-ae"}}, "2026-11-12")
    assert ny[0]["ministerium"] == {**ny[4]["ministerium"], "pr": "2026-11-12"} == {"vaerdi": "min-ae", "sikkerhed": "verificeret", "metode": "retsinformation", "pr": "2026-11-12"}
    assert ny[4]["ministerium"]["pr"] == "2026-11-23"
    assert ny[5]["ministerium"] == {"vaerdi": "min-pære"} and ny[0]["retsomraade"] == "frugt"
    assert ny[1]["ministerium"] == {"vaerdi": "min-ae", "sikkerhed": "sandsynlig", "metode": "arvet"} and ny[1]["retsomraade"] == "frugt"
    assert ny[2]["ministerium"]["metode"] == "haiku" and [x["id"] for x in rest] == ["n3"]
    bek = {"id": "b1", "type": "bekendtgørelse", "status": {"vaerdi": "gældende"}, "territorium": "DK", "dokumentrolle": "hoved", "retsomraade": "frugt",
           "udstedt_af": {"vaerdi": "X"}, "ministerium": {"sikkerhed": "verificeret"}, "registry_ids": ["bek-x"]}
    maalt = [bek, {**bek, "id": "b2", "ministerium": {"sikkerhed": "ukendt"}, "registry_ids": []}, {**bek, "id": "l1", "type": "lov"}, {**bek, "id": "g1", "territorium": "GL"},
             {**bek, "id": "a1", "dokumentrolle": "ændring"}, {**bek, "id": "h1", "status": {"vaerdi": "historisk"}}, {**bek, "id": "u1", "retsomraade": None}]
    tal = daekning(maalt, [{"from": "b2", "type": "henviser_til", "to": "lta-1-1", "beskrivelse": "nævner loven"}], {"b1", "l1"})
    assert dict(tal["frugt"]) == {"gaeldende_alle": 5, "gaeldende": 3, "udsteder": 3, "lovhenv": 1, "registry": 2, "ressort": 2, "regulering": 2, "hjemmel": 1, "love": 1,
                                  "gl_fo": 1, "aendring_ikraft_ophaev": 1} and tal["ikke-klassificeret"]["gaeldende"] == 1
    print("selftest ok")


if __name__ == "__main__":
    kommando = sys.argv[1] if len(sys.argv) > 1 else ""
    if kommando == "selftest":
        selftest()
    elif kommando in ("hent", "katalog"):
        print(json.dumps({"hent": hent, "katalog": katalog}[kommando](*sys.argv[2:5]), ensure_ascii=False, indent=1))
    elif kommando == "unavngivne":
        sys.stdout.write(unavngivne())
    else:
        sys.exit(__doc__)
