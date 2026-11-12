#!/usr/bin/env python3
"""Retsinformations søgeeksport som kilde til kataloget og til fortegnelsen over administrative forskrifter.

    python3 eksport.py hent       # metadata for alle dokumenter pr. samling -> intermediate/corpus/eksport/<samling>.jsonl
    python3 eksport.py katalog    # ajourfør katalog/retsinformation_lta.jsonl og kanter.jsonl fra eksporten (kræver PyYAML)
    python3 eksport.py selftest

Eksporten er sidens egen "Eksportér søgeresultat" (api/documentsearch/csv). Ét kald giver alle dokumenter i en samling for et
årsinterval med type, titel, ressort, myndighed, status, hjemmel (accessionsnumre), ændringer og ELI-adresse. Intervallerne lægges
efter sitemap-fortegnelsen (populate.py sitemap), så hvert kald giver ca. 3.000 dokumenter, og alle samlinger hentes på under 100 kald.
Kaldene går gennem populate.get, som holder 10,5 sekunder mellem kald til Retsinformation og husker svarene.

katalog gør fem ting med Lovtidende A: tilføjer de dokumenter, kataloget mangler; sætter status for alle dokumenter til eksportens;
peger lovfamilier på den nyeste gældende version; skriver hjemmel_for-kanter fra eksportens hjemmelsfelt; og sætter ministerium fra
Retsinformations ressortfelt på alle gældende dokumenter, hvor feltet med sikkerhed er aktuelt (populate.ressort). Nye gældende
dokumenter uden et sådant felt får ministerium og retsområde fra den lov, de er udstedt efter eller ændrer. Resten står i
eksport/klassifikation_job.json; svarene læses fra eksport/klassifikation.json. Ressortkanter til dokumenter, der ikke længere gælder, fjernes.
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
EKS = L / "intermediate" / "corpus" / "eksport"
SAMLINGER = {"lta": 1, "ltb": 2, "ltc": 3, "mt": 4, "retsinfo": 5, "ft": 6, "fob": 7}
METODE = "retsinformation-eksport"
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


def raekker(raw: bytes) -> list[dict]:
    """Eksportens rækker som dicts uden tomme felter; filen er UTF-16 uden BOM med semikolon som skilletegn."""
    text = raw.decode("utf-16-le" if raw[1:2] == b"\x00" else "utf-8-sig").lstrip("﻿")
    return [{k: v for k, v in r.items() if v and k != "Rank"} for r in csv.DictReader(io.StringIO(text), delimiter=";")]


def hent() -> dict:
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
        (EKS / f"{navn}.jsonl").write_text("".join(json.dumps(ud[k], ensure_ascii=False) + "\n" for k in sorted(ud)), encoding="utf-8")
        stats[navn] = {"eksport": len(ud), "sitemap": sum(aar[navn].values()), "gældende": sum(r.get("Historisk") != "True" for r in ud.values())}
    return stats


def dato(s: str | None) -> str | None:
    return f"{s[:4]}-{s[4:6]}-{s[6:8]}" if s and len(s) >= 8 else None


def nid(eli: str) -> str:
    return "lta-" + "-".join(eli.rstrip("/").split("/")[-2:])


def titelnoegle(navn: str) -> str:
    return P.norm(re.sub(r"\(\*\s*\d+\)", " ", navn)).removeprefix("bekendtgørelse af ")


def henvist(tekst: str | None, ids: dict) -> list[str]:
    """Katalog-id'er for de dokumenter i Lovtidende A, en liste af betegnelser ("LBK nr 1031 af 06/09/2024,…") nævner."""
    fundet = (f"lta-{m[2]}-{m[1]}" for m in re.finditer(r"\b[A-ZÆØÅ]{3} nr (\d+) af \d\d/\d\d/(\d{4})", tekst or ""))
    return list(dict.fromkeys(i for i in fundet if i in ids))


def post(r: dict, idag: str) -> dict:
    """En katalogpost for et dokument i Lovtidende A ud fra eksportens række."""
    typ = TYPER.get(r["DokumentType"]) or X.norm_type(r["DokumentType"], r["Titel"])
    aar, nr = r["EliUrl"].rstrip("/").split("/")[-2:]
    u = dato(r.get("UnderskriftDato")) or f"{aar}-01-01"
    omraade = {"Kun Grønland": "GL", "Kun Færøerne": "FO"}.get(r.get("GeografiskDækning"))
    udsteder = r.get("AdministrerendeMyndighed") or r.get("Ressort")
    datoer = {"udstedt": u, "historisk_markeret": dato(r.get("HistoriskDato")), "ri_registreret": dato(r.get("PubliceretTidspunkt")),
              "ri_aendret": dato(r.get("SidstPubliceretTidspunkt"))}
    return {
        "id": f"lta-{aar}-{nr}", "navn": r["Titel"], "type": typ, "kilder": [f"{P.RI}/eli/lta/{aar}/{nr}/xml"],
        "status": {"vaerdi": "historisk" if r.get("Historisk") == "True" else "gældende", "pr": idag, "sikkerhed": "verificeret"},
        "identifikatorer": {"lovtidende": f"{X.ABBR[typ]} nr. {nr} af {u[8:]}/{u[5:7]}/{u[:4]}", "document_id": r.get("DokumentId"),
                            "accession": r.get("ACCN"), "sikkerhed": "verificeret"},
        "datoer": {k: v for k, v in datoer.items() if v},
        "territorium": omraade if omraade and K.territorium(r["Titel"]) == "DK" else K.territorium(r["Titel"]),
        "dokumentrolle": K.rolle({"type": typ, "titel": r["Titel"]}),
        "udstedt_af": {"vaerdi": udsteder or "ukendt", "metode": METODE if udsteder else "ingen", "praefiks": (r.get("DokumentId") or "")[:2],
                       "sikkerhed": "verificeret" if udsteder else "ukendt"},
        "n_paragraffer": 0, "n_definitioner": 0,
    }


def familier(docs: list[dict], blev_historisk: set) -> dict:
    """Peg lovfamilier på den nyeste gældende lov eller lovbekendtgørelse med samme titel; returnér {gammel version: ny version}."""
    ids = {d["id"]: d for d in docs}
    gaeldende = collections.defaultdict(list)
    for d in docs:
        if d["status"]["vaerdi"] == "gældende" and d["type"] in LOVE and d["dokumentrolle"] == "hoved":
            gaeldende[titelnoegle(d["navn"])].append(d)

    def nyere(g: dict) -> str | None:
        kand = [d for d in gaeldende[titelnoegle(g["navn"])] if d["datoer"].get("udstedt", "") > g["datoer"].get("udstedt", "")]
        return max(kand, key=lambda d: d["datoer"]["udstedt"])["id"] if kand else None

    ompeg = {}
    for d in docs:
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


def klassificer(docs: list[dict], foraeldre: dict, eks: dict, reg: dict, svar: dict, idag: str) -> list[dict]:
    """Sæt ministerium fra Retsinformations ressortfelt på alle gældende dokumenter, hvor feltet med sikkerhed er aktuelt, også når en
    klassifikation siger noget andet. Giv derefter gældende dokumenter uden klassifikation ministerium og retsområde fra forældre og svar;
    returnér dem, der stadig mangler noget."""
    ids = {d["id"]: d for d in docs}
    ministerier = {n["navn"]: n["id"] for n in reg["nodes"] if n["type"] == "ministerium" and n.get("status") == "aktiv"}
    for d in docs:
        felt = P.ressort({"Status": "Valid", "Ministry": eks.get(d["id"], {}).get("Ressort"), "DiesSigni": d["datoer"].get("udstedt", "")}, reg)
        if d["status"]["vaerdi"] == "gældende" and ministerier.get(felt):
            d["ministerium"] = {"vaerdi": ministerier[felt], "sikkerhed": "verificeret", "metode": "retsinformation", "pr": idag}
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
    idag = str(datetime.date.today())
    eks = {nid(r["EliUrl"]): r for r in map(json.loads, (EKS / "lta.jsonl").open(encoding="utf-8"))}
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
        d["status"] = {**d["status"], "vaerdi": ny, "pr": idag}
    kendte = {d["id"] for d in docs}
    nye = [post(r, idag) for i, r in sorted(eks.items()) if i not in kendte]
    stats["nye med ukendt type (udeladt)"] = sum(d["type"] == "ukendt" for d in nye)
    nye = [d for d in nye if d["type"] != "ukendt"]
    stats["nye dokumenter"] = len(nye)
    stats["heraf gældende"] = sum(d["status"]["vaerdi"] == "gældende" for d in nye)
    docs += nye
    ids = {d["id"]: d for d in docs}
    accession = {d["identifikatorer"].get("accession"): d["id"] for d in docs}
    for d in nye:
        if d["dokumentrolle"] == "ændring" and (maal := henvist(eks[d["id"]].get("ÆndrerI"), ids)):
            d["aendrer"] = maal
    ompeg = familier(docs, blev_historisk)
    stats["lovfamilier flyttet til ny gældende version"] = len(ompeg)

    hjemmel = {i: [accession[a] for a in r.get("HjemmelVedroerer", "").split(",") if a in accession and accession[a] != i] for i, r in eks.items() if i in ids}
    versioner = collections.defaultdict(list)
    for d in docs:
        if d["type"] in LOVE and d["dokumentrolle"] == "hoved":
            versioner[titelnoegle(d["navn"])].append(d)

    def forgaenger(d: dict) -> list[str]:
        aeldre = [v for v in versioner[titelnoegle(d["navn"])] if v["datoer"].get("udstedt", "") < d["datoer"].get("udstedt", "")] if d["type"] in LOVE else []
        return [max(aeldre, key=lambda v: v["datoer"]["udstedt"])["id"]] if aeldre else []

    foraeldre = {d["id"]: [*hjemmel.get(d["id"], []), *d.get("aendrer", []), *forgaenger(d)] for d in nye}
    reg = P.yaml.load(P.REG.read_text(encoding="utf-8"), Loader=P.yaml.CSafeLoader)
    svarfil = EKS / "klassifikation.json"
    omraader = {o["omraade"] for o in json.loads((L / "dashboard" / "omraader.json").read_text(encoding="utf-8"))}
    svar = json.loads(svarfil.read_text(encoding="utf-8")) if svarfil.exists() else {}
    foer = {d["id"]: (d.get("ministerium") or {}).get("vaerdi") for d in docs}
    rest = klassificer(docs, foraeldre, eks, reg, {i: {**v, "retsomraade": v.get("retsomraade") if v.get("retsomraade") in omraader else None} for i, v in svar.items()}, idag)
    stats["gældende uden fuld klassifikation"] = len(rest)
    ri = {d["id"] for d in docs if d["status"]["vaerdi"] == "gældende" and (d.get("ministerium") or {}).get("metode") == "retsinformation"}
    stats["ministerium fra Retsinformations ressortfelt"] = len(ri)
    stats["heraf rettet fra et andet ministerium"] = sum(foer[i] not in (None, ids[i]["ministerium"]["vaerdi"]) for i in ri)
    (EKS / "klassifikation_job.json").write_text(json.dumps(
        [{"id": d["id"], "navn": d["navn"], "type": d["type"], "ressortfelt": eks.get(d["id"], {}).get("Ressort"), "myndighed": eks.get(d["id"], {}).get("AdministrerendeMyndighed"),
          "ministerium": (d.get("ministerium") or {}).get("vaerdi"), "retsomraade": d.get("retsomraade")} for d in rest], ensure_ascii=False, indent=1), encoding="utf-8")

    kanter = [e for e in map(json.loads, (KAT / "kanter.jsonl").open(encoding="utf-8")) if e.get("metode") != METODE
              and not (e["type"] == "ressortansvar" and (e["to"] in ri or ids.get(e["to"], {}).get("status", {}).get("vaerdi") == "historisk"))]
    for e in kanter:
        if e["type"] == "henviser_til" and (e.get("gaeldende_version") or e["to"]) in ompeg:
            e["gaeldende_version"] = ompeg[e.get("gaeldende_version") or e["to"]]
    for i in sorted(hjemmel):
        for lov in dict.fromkeys(hjemmel[i]):
            if ids[i]["type"] in FORSKRIFTER:
                gv = ids[lov].get("gaeldende_version")
                kanter.append({"from": lov, "type": "hjemmel_for", "to": i, "beskrivelse": "hjemmel ifølge Retsinformation (den version, forskriften henviser til)",
                               "kilder": [f"{P.RI}/eli/{i.replace('-', '/')}"], "sikkerhed": "verificeret", "metode": METODE, **({"gaeldende_version": gv} if gv else {})})
    nye_ids = {d["id"] for d in nye}
    for d in docs:
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
    stats["dokumenter koblet til registry"] = sum("registry_ids" in d for d in docs)

    med = {e["to"] for e in kanter if e["type"] == "hjemmel_for"}
    kid = {n["id"]: n.get("katalog_id") for n in reg["nodes"]}
    med |= {kid[e["to"]] for e in reg["edges"] if e["type"] == "hjemmel_for" and kid.get(e["to"])}
    tal = daekning(docs, kanter, med)
    stats["gældende danske forskrifter"] = sum(c["regulering"] for c in tal.values())
    stats["heraf med hjemmel_for"] = sum(c["hjemmel"] for c in tal.values())
    dashboard(tal, docs, reg)
    (KAT / "retsinformation_lta.jsonl").write_text("".join(json.dumps(d, ensure_ascii=False) + "\n" for d in docs), encoding="utf-8")
    (KAT / "kanter.jsonl").write_text("".join(json.dumps(e, ensure_ascii=False) + "\n" for e in kanter), encoding="utf-8")
    return dict(stats)


def selftest() -> None:
    assert intervaller({"2001": 2000, "2002": 900, "2004": 2500, "2005": 100}) == [("", "2003", 2900), ("2004", "", 2600)]
    assert intervaller({}) == [] and intervaller({"1999": 5}) == [("", "", 5)]
    csvtekst = '"Rank";"DokumentType";"Titel";"Historisk";"EliUrl"\r\n"B";"Bekendtgørelse";"Bekendtgørelse om æbler";"";"https://retsinformation.dk/eli/lta/2026/5"\r\n'
    assert raekker(csvtekst.encode("utf-16-le")) == [{"DokumentType": "Bekendtgørelse", "Titel": "Bekendtgørelse om æbler", "EliUrl": "https://retsinformation.dk/eli/lta/2026/5"}]
    r = {"DokumentType": "Ændringsbekendtgørelse", "Titel": "Bekendtgørelse om ændring af bekendtgørelse om æbler for Grønland", "Ressort": "Æbleministeriet", "Nummer": "5",
         "DokumentId": "AB000001", "ACCN": "B20260000505", "UnderskriftDato": "20260702", "PubliceretTidspunkt": "20260704", "Historisk": "True", "HistoriskDato": "20261001",
         "GeografiskDækning": "Kun Grønland", "EliUrl": "https://retsinformation.dk/eli/lta/2026/5"}
    d = post(r, "2026-11-12")
    assert (d["id"], d["type"], d["dokumentrolle"], d["territorium"], d["status"]["vaerdi"]) == ("lta-2026-5", "ændringsbekendtgørelse", "ændring", "GL", "historisk")
    assert d["identifikatorer"]["lovtidende"] == "BEK nr. 5 af 02/07/2026" and d["datoer"] == {"udstedt": "2026-07-02", "historisk_markeret": "2026-10-01", "ri_registreret": "2026-07-04"}
    assert d["udstedt_af"] == {"vaerdi": "Æbleministeriet", "metode": METODE, "praefiks": "AB", "sikkerhed": "verificeret"} and "seed_fil" not in d
    assert post({**r, "DokumentType": "Anordningsbekendtgørelse", "GeografiskDækning": ""}, "x")["type"] == "bekendtgørelse-af-anordning"
    assert henvist("LBK nr 1031 af 06/09/2024,VEJ nr 9139 af 25/02/2019,LOV nr 7 af 01/01/2020", {"lta-2024-1031": 1, "lta-2020-7": 1}) == ["lta-2024-1031", "lta-2020-7"]

    def lov(i, navn, aar, status, **mere):
        return {"id": i, "navn": navn, "type": "lovbekendtgørelse", "dokumentrolle": "hoved", "status": {"vaerdi": status}, "datoer": {"udstedt": f"{aar}-01-01"}, **mere}

    fam = [lov("a", "Bekendtgørelse af æbleloven (* 1)", 2020, "historisk", gaeldende_version="b"), lov("b", "Bekendtgørelse af æbleloven", 2025, "historisk"),
           lov("c", "Bekendtgørelse af æbleloven", 2026, "gældende"), lov("p", "Bekendtgørelse af pæreloven", 2019, "historisk", nyeste_version_afloeser_mangler="q"),
           lov("q", "Bekendtgørelse af pæreloven", 2024, "historisk", afloeser_mangler=True), lov("k", "Bekendtgørelse af kirsebærloven", 2024, "historisk")]
    assert familier(fam, {"b", "k"}) == {"b": "c"}
    assert [x.get("gaeldende_version") for x in fam] == ["c", "c", None, None, None, None] and fam[3]["nyeste_version_afloeser_mangler"] == "q"
    assert fam[4]["afloeser_mangler"] and fam[5]["afloeser_mangler"] and "afloeser_mangler" not in fam[1]
    reg = {"regering": {"dannet": "2026-06-03"}, "nodes": [{"id": "min-ae", "type": "ministerium", "status": "aktiv", "navn": "Æbleministeriet"}]}
    ny = [{"id": "n1", "status": {"vaerdi": "gældende"}, "datoer": {"udstedt": "2026-07-02"}}, {"id": "n2", "status": {"vaerdi": "gældende"}, "datoer": {"udstedt": "2026-01-02"}},
          {"id": "n3", "status": {"vaerdi": "gældende"}, "datoer": {"udstedt": "2026-01-02"}}, {"id": "c", "status": {"vaerdi": "gældende"}, "datoer": {},
                                                                                              "ministerium": {"vaerdi": "min-ae"}, "retsomraade": "frugt"}]
    ny[3]["gaeldende_version"] = "n1"
    ny += [{"id": "o", "status": {"vaerdi": "gældende"}, "datoer": {"udstedt": "2026-07-02"}, "ministerium": {"vaerdi": "min-pære", "sikkerhed": "sandsynlig"}, "retsomraade": "frugt"},
           {"id": "h", "status": {"vaerdi": "historisk"}, "datoer": {"udstedt": "2026-07-02"}, "ministerium": {"vaerdi": "min-pære"}}]
    felt = {i: {"Ressort": "Æbleministeriet"} for i in ("n1", "n2", "o", "h")}
    rest = klassificer(ny, {"n1": ["c"], "n2": ["n1"]}, felt, reg, {"n3": {"ministerium": "min-ae"}}, "2026-11-12")
    assert ny[0]["ministerium"] == ny[4]["ministerium"] == {"vaerdi": "min-ae", "sikkerhed": "verificeret", "metode": "retsinformation", "pr": "2026-11-12"}
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
        print(json.dumps({"hent": hent, "katalog": katalog}[kommando](), ensure_ascii=False, indent=1))
    else:
        sys.exit(__doc__)
