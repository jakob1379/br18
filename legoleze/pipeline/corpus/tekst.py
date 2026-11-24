#!/usr/bin/env python3
"""Tekstlaget: Retsinformations XML for et udsnit af kataloget, hentet i prioriteret rækkefølge.

    python3 tekst.py plan             # udsnittet pr. trin: dokumenter i alt og hvor mange der er hentet
    python3 tekst.py hent [MINUTTER]  # hent manglende dokumenter i højst MINUTTER (105) -> intermediate/corpus/xml/<samling>/<resten af id>.xml.gz
    python3 tekst.py tidslinjer [MIN] # hent Retsinformations tidslinje pr. lov i højst MIN (105) minutter -> intermediate/corpus/tidslinjer.jsonl
    python3 tekst.py indeks           # katalog/tekst.jsonl: sti, hentedato, omfang, præambel, fodnoter, nævnte retsakter, underskriftssted og EU-retsakter pr. hentet dokument
    python3 tekst.py fuld             # hele teksten som JSON-linjer på stdout: id, paragraf og tekst, én linje pr. paragraf
    python3 tekst.py selftest

Udsnittet er de dokumenter, registry'ets noder peger på, og de gældende dokumenter i de otte domæner (katalog.SCOPE over retsområdet).
Trinene (TRIN) hentes i rækkefølge: registry; afløserkandidaterne (eksport.kandidatplan: de hovedlove, en historisk lov uden gældende
version kan være afløst af, først dem for love, gældende forskrifter har hjemmel i); Lovtidende A uden tekst i bulk-høsten; vejledninger, cirkulærer og andre dokumenter uden for
Lovtidende A, der ikke er praksis; lovforslag som fremsat til de gældende love i udsnittet; praksis (afgørelser, udtalelser, domme); og
til sidst Lovtidende A med tekst i bulk-høsten, fordi den tekst ikke ligger i dette repo.

Kaldene går gennem populate.get: 10,5 sekunder mellem kald til Retsinformation, delt med alle andre opslag, og svar fra de seneste syv
dage genbruges (hentedatoen kan derfor være op til syv dage senere end selve kaldet). Nogle ældre dokumenter har kun metadata i XML-filen;
de står i indekset med n_tegn 0. hent stopper uden for høsterens åbningstid
(03:00-23:45 dansk tid) og efter fem fejl i træk. Hvert forsøg står i xml/hentet.jsonl; adresser, der er døde eller ikke giver XML,
prøves ikke igen.

tidslinjer henter lovens versionskæde (hovedlov, ændringslove og lovbekendtgørelser) for hver lov og lovbekendtgørelse i Lovtidende A gennem
samme kø. Kæden er den samme for alle versioner af en lov, så der bruges ét kald pr. lov. eksport.py katalog læser filen og samler
lovfamilierne efter den i stedet for efter titlen.
"""
from __future__ import annotations

import collections
import datetime
import gzip
import json
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import eksport as E

H = E.modul("harvest", E.L / "harvest" / "harvest.py")
XML = E.L / "intermediate" / "corpus" / "xml"
NAEVNT = re.compile(r"(?:lovbekendtgørelse|bekendtgørelse|lov|anordning|LBK|BEK)(?:n|en)?\s+nr\.?\s*(\d+)\s+af\s+(?:(\d{1,2})\.? ?(" + "|".join(E.X.MONTHS)
                    + r") (\d{4})|(\d{1,2})[./-](\d{1,2})[./-](\d{4}))", re.IGNORECASE)
TRIN = ("registry", "afloeser", "uden-tekst", "vejledning", "lovforslag", "praksis", "med-tekst")


def trin(d: dict) -> str | None:
    """Trinnet for en katalogpost uden for Folketingstidende; None når den ikke er i udsnittet."""
    if d.get("registry_ids"):
        return "registry"
    if d["status"]["vaerdi"] != "gældende" or not E.K.SCOPE.get(d.get("retsomraade")):
        return None
    if d["id"].startswith("lta-"):
        return "med-tekst" if d.get("n_paragraffer") else "uden-tekst"
    return "praksis" if d["type"] in E.PRAKSIS else "vejledning"


def plan() -> dict:
    """{trin: katalog-id'er, nyeste først}. Et lovforslag er med, når den lov, det blev til, er et gældende dokument i udsnittet."""
    ud, love, ft = {t: [] for t in TRIN}, set(), []
    for s in ("lta", *E.ANDRE):
        with (E.KAT / f"retsinformation_{s}.jsonl").open(encoding="utf-8") as f:
            for d in map(json.loads, f):
                if s == "ft":
                    ft.append((d["id"], d["type"], d.get("lovforslag"), d.get("lov")))
                elif t := trin(d):
                    ud[t].append(d["id"])
                    love |= {d["id"]} if d["status"]["vaerdi"] == "gældende" else set()
    sager = {sag for _, _, sag, lov in ft if lov in love}
    ud["lovforslag"] = [i for i, t, sag, _ in ft if t == "lovforslag-som-fremsat" and sag in sager]
    ud = {t: sorted(v, reverse=True) for t, v in ud.items()}
    return {**ud, "afloeser": [i for i in E.kandidatplan() if i not in ud["registry"]]}


def sti(i: str) -> Path:
    samling, _, rest = i.partition("-")
    return XML / samling / f"{rest}.xml.gz"


def aaben(nu: datetime.datetime | None = None) -> bool:
    nu = nu or datetime.datetime.now(H.CPH)
    return H.OPEN <= (nu.hour, nu.minute) < H.CLOSE


def hent(minutter: float) -> dict:
    """Henter de dokumenter, der mangler, i planens rækkefølge. Efter en fejl ventes der dobbelt så længe for hver fejl i træk (fra et minut)."""
    journal, start = XML / "hentet.jsonl", time.monotonic()
    XML.mkdir(parents=True, exist_ok=True)
    opgivet = {r["id"] for r in map(json.loads, journal.open(encoding="utf-8")) if r["status"] in ("død", "ikke-xml")} if journal.exists() else set()
    tal, fejl = collections.Counter(), 0
    for i in (i for ids in plan().values() for i in ids):
        if sti(i).exists() or i in opgivet:
            continue
        if time.monotonic() - start >= minutter * 60 or fejl >= 5 or not aaben():
            break
        status, raw = E.P.get(f"{E.P.RI}/eli/{i.replace('-', '/')}")
        if status == "ok" and b"<Dokument" not in raw[:4000]:
            status = "ikke-xml"
        if status == "ok":
            sti(i).parent.mkdir(parents=True, exist_ok=True)
            tmp = sti(i).with_suffix(".tmp")
            tmp.write_bytes(gzip.compress(raw, mtime=0))
            tmp.replace(sti(i))
        with journal.open("a", encoding="utf-8") as f:
            f.write(E.linje({"id": i, "status": status, "hentet": str(datetime.date.today()), **({} if status == "ok" else {"svar": raw[:120].decode("utf-8", "replace")})}))
        tal[status] += 1
        fejl = fejl + 1 if status == "ukendt" else 0
        if fejl:
            time.sleep(30 * 2**fejl)
    return dict(tal)


def tidslinjer(minutter: float) -> dict:
    """Henter tidslinjen for de love og lovbekendtgørelser, der ikke står i en allerede hentet tidslinje; gældende og nyeste først."""
    with (E.KAT / "retsinformation_lta.jsonl").open(encoding="utf-8") as f:
        love = [d for d in map(json.loads, f) if d["type"] in E.LOVE and d["dokumentrolle"] == "hoved" and d["identifikatorer"].get("unique_document_id")]
    love.sort(key=lambda d: (d["status"]["vaerdi"] == "gældende", d["datoer"].get("udstedt", "")), reverse=True)
    kendt = {i for r in E.tidslinjer(("ok", "død", "ikke-json")) for i in (r["id"], *E.lovversioner(r.get("tidslinje", [])))}
    start, tal, fejl = time.monotonic(), collections.Counter(), 0
    for d in love:
        if d["id"] in kendt:
            continue
        if time.monotonic() - start >= minutter * 60 or fejl >= 5 or not aaben():
            break
        status, raw = E.P.get(f"{E.P.RI}/api/document/{d['identifikatorer']['unique_document_id']}/timeline")
        try:
            tl = json.loads(raw) if status == "ok" else None
        except ValueError:
            tl = None
        if status == "ok" and not isinstance(tl, list):
            status = "ikke-json"
        raekke = {"id": d["id"], "status": status, "hentet": str(datetime.date.today())}
        if status == "ok":
            raekke["tidslinje"] = [{k: e.get(k) for k in E.TIDSLINJEFELTER} for e in tl]
            kendt.update(E.lovversioner(raekke["tidslinje"]))
        with E.TL.open("a", encoding="utf-8") as f:
            f.write(E.linje(raekke))
        tal[status] += 1
        fejl = fejl + 1 if status == "ukendt" else 0
        if fejl:
            time.sleep(30 * 2**fejl)
    return {**tal, "mangler": sum(d["id"] not in kendt for d in love)}


def udtraek(xml: str) -> dict:
    """Omfang, præambel uden fodnoter, fodnoter, de love og bekendtgørelser teksten nævner med nummer og dato ({"katalog-id|dato": antal})
    og, fra Meta, underskriftssted og EU-retsakter (CELEX); tomme felter udelades."""
    led = lambda navn, x: [t for t in (re.sub(r"\s+", " ", H.text_of(m)) for m in re.findall(rf"<{navn}\b[^>]*>(.*?)</{navn}>", x, re.DOTALL)) if t]
    meta = H.meta_of(xml)
    liste = lambda v: [v] if isinstance(v, str) else v or []
    naevner = collections.Counter(f"lta-{m[4] or m[7]}-{int(m[1])}|{m[4] or m[7]}-{E.X.MONTHS[m[3].lower()] if m[3] else int(m[6]):02d}-{int(m[2] or m[5]):02d}"
                                  for m in NAEVNT.finditer(tekst(xml)))
    instansled = [[par, s[:600]] for par, t in afsnit(xml) if par for s in E.SAETNING.split(" ".join(re.sub(r"[\u200b-\u200d\u2060\ufeff\u00ad]", "", t).split()))
           if any(r.search(s) for r in E.LED)]
    felter = {"praeambel": E.P.praeambel(xml), "klage_tilsyn": instansled[:80], "noter": led("Nota", E.P.NYTEKST.sub("", xml)), "naevner": dict(sorted(naevner.items())),
              "underskrevet_af": "; ".join(liste(meta.get("PlaceOfSignature"))), "eu": liste(meta.get("EuReferences"))}
    return {"n_tegn": len(tekst(xml)), "n_paragraffer": len(re.findall(r"<Paragraf\b", xml)), **{k: v for k, v in felter.items() if v}}


def tekst(xml: str) -> str:
    return H.text_of(re.sub(r"<Meta[^>]*>.*?</Meta>", "", xml, flags=re.DOTALL))


def afsnit(xml: str) -> list[tuple[str | None, str]]:
    """(paragraf, tekst) for hver paragraf i dokumentet, med paragraffens betegnelse som den står ("§ 5", "§ 16 C"). Et dokument uden
    paragraffer giver hele teksten som ét afsnit uden betegnelse, og et dokument uden tekst giver ingen."""
    ud = []
    for blok in re.findall(r"<Paragraf\b[^>]*>(.*?)</Paragraf>", xml, re.DOTALL):
        navn = re.search(r"<Explicatus\b[^>]*>(.*?)</Explicatus>", blok, re.DOTALL)
        ud.append((" ".join(H.text_of(navn[1]).split()).rstrip(". ") if navn else None, "\n".join(linje.strip() for linje in H.text_of(blok).splitlines())))
    return ud or [(None, t) for t in [tekst(xml)] if t]


def hentede():
    """(katalog-id, sti, XML) for hvert hentet dokument."""
    for f in sorted(XML.glob("*/*.xml.gz")):
        yield f"{f.parent.name}-{f.name[:-7]}", f, gzip.decompress(f.read_bytes()).decode("utf-8", "replace")


def indeks() -> dict:
    dage = {r["id"]: r["hentet"] for r in map(json.loads, (XML / "hentet.jsonl").open(encoding="utf-8")) if r["status"] == "ok"}
    with (E.KAT / "tekst.jsonl").open("w", encoding="utf-8") as ud:
        tal = collections.Counter()
        for i, f, xml in hentede():
            ud.write(E.linje({"id": i, "xml": str(f.relative_to(E.L)), "hentet": dage[i], **udtraek(xml)}))
            tal[i.split("-")[0]] += 1
    return dict(tal)


def selftest() -> None:
    kat = {"status": {"vaerdi": "gældende"}, "retsomraade": "byggeri", "type": "bekendtgørelse", "n_paragraffer": 0}
    poster = [{**kat, "id": "lta-2020-1"}, {**kat, "id": "lta-2020-2", "n_paragraffer": 3}, {**kat, "id": "retsinfo-2020-9001", "type": "vejledning"},
              {**kat, "id": "retsinfo-2020-9002", "type": "afgørelse"}, {**kat, "id": "lta-2020-3", "retsomraade": "skat"},
              {**kat, "id": "lta-2020-4", "status": {"vaerdi": "historisk"}}, {**kat, "id": "lta-2020-5", "status": {"vaerdi": "historisk"}, "registry_ids": ["bek-x"]}]
    assert [trin(d) for d in poster] == ["uden-tekst", "med-tekst", "vejledning", "praksis", None, None, "registry"]
    assert sti("lta-2019-1399") == XML / "lta" / "2019-1399.xml.gz" and sti("ft-202523LB0017") == XML / "ft" / "202523LB0017.xml.gz"
    assert aaben(datetime.datetime(2026, 11, 2, 12, 0)) and not aaben(datetime.datetime(2026, 11, 2, 23, 50)) and not aaben(datetime.datetime(2026, 11, 3, 1, 0))
    xml = """<Dokument><Meta><DocumentTitle>Bekendtgørelse om æbler</DocumentTitle><EuReferences>32010L0031</EuReferences><PlaceOfSignature>Æblestyrelsen</PlaceOfSignature>
</Meta><DokumentIndhold><Indledning><Exitus><Linea><Char>I medfør af § 5, stk. 2, i lov om æbler,</Char><Nota><Explicatus>1)</Explicatus><Exitus><Linea>
<Char>Ressortansvaret er overført.</Char></Linea></Exitus></Nota></Linea><Linea><Char>jf. lovbekendtgørelse nr. 7 af 1. januar 2020, fastsættes:</Char></Linea></Exitus></Indledning>
<ParagrafGruppe><Paragraf localId="1"><Explicatus>§ 1.</Explicatus><Stk><Exitus><Linea><Char>Æbler er frugt.</Char></Linea></Exitus></Stk></Paragraf></ParagrafGruppe>
</DokumentIndhold><UnderskriftGruppe><UnderskriftStedDato /><Underskriver /></UnderskriftGruppe></Dokument>"""
    u = udtraek(xml)
    assert u["praeambel"] == "I medfør af § 5, stk. 2, i lov om æbler, jf. lovbekendtgørelse nr. 7 af 1. januar 2020, fastsættes:" and u["n_paragraffer"] == 1
    assert u["naevner"] == {"lta-2020-7|2020-01-01": 1}
    naevnt = udtraek("<Dokument><Char>Se LBK nr. 943 af 16. oktober 2000, ændringsbekendtgørelsen nr. 1434 af 25/11/2025 og lov nr. 5 af 3. maj 2021. Jf. lov nr. 5 af 3.5.2021.</Char></Dokument>")
    assert naevnt["naevner"] == {"lta-2000-943|2000-10-16": 1, "lta-2021-5|2021-05-03": 2, "lta-2025-1434|2025-11-25": 1}
    klage = udtraek("<Dokument><Paragraf><Explicatus>§ 9.</Explicatus><Char>Reglerne gælder for æbler. Afgørelser kan påklages til Frugtklagenævnet. Nævnet fører tilsyn.</Char></Paragraf></Dokument>")
    assert klage["klage_tilsyn"] == [["§ 9", "Afgørelser kan påklages til Frugtklagenævnet."], ["§ 9", "Nævnet fører tilsyn."]] and "klage_tilsyn" not in u
    assert u["noter"] == ["1) Ressortansvaret er overført."] and u["underskrevet_af"] == "Æblestyrelsen" and u["eu"] == ["32010L0031"]
    assert "Æbler er frugt." in tekst(xml) and "Bekendtgørelse om æbler" not in tekst(xml) and u["n_tegn"] == len(tekst(xml))
    assert udtraek("<Dokument><Paragraf>x</Paragraf></Dokument>") == {"n_tegn": 1, "n_paragraffer": 1}
    nyt = udtraek("<Dokument><Nota><Char>1) Egen note.</Char></Nota><Paragraf><AendringNyTekst><Nota><Char>1) Hovedbekendtgørelsens nye note.</Char></Nota></AendringNyTekst></Paragraf></Dokument>")
    assert nyt["noter"] == ["1) Egen note."]
    assert afsnit(xml) == [("§ 1", "§ 1.\nÆbler er frugt.")] and afsnit("<Dokument><Meta><Year>1996</Year></Meta></Dokument>") == []
    assert afsnit("<Dokument><Meta/><TekstGruppe><Exitus><Char>En afgørelse.</Char></Exitus></TekstGruppe></Dokument>") == [(None, "En afgørelse.")]
    to = "<Paragraf localId='16C'><Explicatus>§ 16 C. </Explicatus><Stk><Char>A</Char></Stk></Paragraf><Paragraf><Stk><Char>B</Char></Stk></Paragraf>"
    assert [x for x, _ in afsnit(to)] == ["§ 16 C", None]
    print("selftest ok")


if __name__ == "__main__":
    kommando = sys.argv[1] if len(sys.argv) > 1 else ""
    if kommando == "selftest":
        selftest()
    elif kommando == "plan":
        print(json.dumps({t: {"dokumenter": len(ids), "hentet": sum(sti(i).exists() for i in ids)} for t, ids in plan().items()}, ensure_ascii=False, indent=1))
    elif kommando == "hent":
        print(json.dumps(hent(float(sys.argv[2]) if len(sys.argv) > 2 else 105), ensure_ascii=False))
    elif kommando == "tidslinjer":
        print(json.dumps(tidslinjer(float(sys.argv[2]) if len(sys.argv) > 2 else 105), ensure_ascii=False))
    elif kommando == "indeks":
        print(json.dumps(indeks(), ensure_ascii=False))
    elif kommando == "fuld":
        for i, _, xml in hentede():
            sys.stdout.writelines(E.linje({"id": i, "paragraf": p, "tekst": t}) for p, t in afsnit(xml))
    else:
        sys.exit(__doc__)
