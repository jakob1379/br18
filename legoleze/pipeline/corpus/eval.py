#!/usr/bin/env python3
"""Evalueringssæt for kæderne: et tilfældigt udtag af gældende forskrifter og vejledninger, læst uafhængigt af kataloget.

    python3 eval.py udtag     # trækker de runder, der mangler -> intermediate/eval/udtag.json og én opgave pr. dokument i intermediate/eval/opgaver/<id>.txt
    python3 eval.py saml      # annotatorernes svar (raw/eval/svar-*.json) -> dk-regulering/eval/facit.jsonl, hvert led kontrolleret mod opgaven
    python3 eval.py maal      # katalogets og registry'ets kanter mod facit -> dk-regulering/eval/README.md, intermediate/eval/afvigelser.jsonl, tal på stdout
    python3 eval.py selftest

Udtaget er pr. domæne (katalog.SCOPE over retsområdet) et antal gældende danske dokumenter med hentet tekst: hovedbekendtgørelser
med og uden registry-node og vejledninger. RUNDER giver frø og antal pr. runde, og en runde trækker ikke dokumenter fra en tidligere.
Runde 1 er brugt til at finde og rette fejl i udtrækkene; en senere runde er trukket bagefter, og dens første måling gemmes af maal i
dk-regulering/eval/kontrol-<runde>.json, før noget rettes efter den. En opgave er dokumentets indledning og fodnoter og, for en
forskrift, de paragraffer der matcher SOEG (klage og tilsyn), for en vejledning tekstens første BEGYNDELSE tegn. Annotatoren ser hverken
katalog eller registry.

saml beholder kun de led, hvis citat står ordret i opgaven, hvis nummer og år står i citatet, og hvis paragraffer står i indledningen;
resten tælles som frafald. dk-regulering/eval/rettelser.json retter facit efter gennemsyn af en afvigelse: {id: {felt: [led], "fjern":
{felt: [dokument eller retsakt]}, "begrundelse": ...}}. Et felt erstattes og kontrolleres på samme måde; fjern tager enkelte led ud.

maal tæller mikro-gennemsnit pr. runde. For vejledninger måles kun genfinding, fordi facit kun dækker tekstens begyndelse. En hjemmelskant rammer, når lovens familie (gældende version) eller den citerede version
er facit-dokumentets; kanter fra dokumenter uden for Lovtidende A (tekstanmærkninger til finansloven) tælles ikke, fordi facit kun har love,
lovbekendtgørelser, bekendtgørelser og anordninger. Paragraffer sammenlignes på paragrafnummer ("§ 6"). Klage- og tilsynsmyndigheder slås
op på navn i registry'et (eksport.myndigheder; ALIAS for kommunalbestyrelsen).
"""
from __future__ import annotations

import collections
import gzip
import json
import random
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import eksport as E
import tekst as T

EVAL, UD, SVAR = E.L / "intermediate" / "eval", E.L / "dk-regulering" / "eval", E.L / "raw" / "eval"
RUNDER = ((20261115, {"forskrift-registry": 5, "forskrift": 7, "vejledning": 3}), (20261116, {"forskrift-registry": 3, "forskrift": 5, "vejledning": 2}),
          (20261117, {"forskrift-registry": 2, "forskrift": 4, "lov": 3}))
VEJLEDNING = "vejledning → retsakt"
SOEG = re.compile(r"klage|indbring|\banke|tilsyn|\bkontrol", re.IGNORECASE)  # runde 1 og 2 blev trukket med "kontrolmyndighed" i stedet for "kontrol"
BEGYNDELSE, LOFT = 10000, 1500
EU = {"direktiv": "dir", "forordning": "reg", "afgørelse": "dec", "beslutning": "dec"}
FELTER = ("hjemmel", "eu", "klage", "tilsyn", "henviser")


def gruppe(d: dict, t: dict) -> str | None:
    if d["status"]["vaerdi"] != "gældende" or not t.get("n_tegn") or d.get("territorium", "DK") != "DK":
        return None
    if d["id"].startswith("lta-") and d["type"] == "bekendtgørelse" and d.get("dokumentrolle") == "hoved":
        return "forskrift-registry" if d.get("registry_ids") else "forskrift"
    if d["id"].startswith("lta-") and d["type"] in E.LOVE and d.get("dokumentrolle") == "hoved":
        return "lov"
    return "vejledning" if d["type"] == "vejledning" else None


def udtag(poster: list[tuple[dict, dict]], n: dict, froe: int) -> dict:
    """{"domæne/gruppe": katalog-id'er}; hele puljen, når den er mindre end antallet."""
    puljer = collections.defaultdict(list)
    for d, t in poster:
        if (g := gruppe(d, t)) and (dom := E.K.SCOPE.get(d.get("retsomraade"))):
            puljer[f"{dom}/{g}"].append(d["id"])
    r = random.Random(froe)
    return {k: sorted(r.sample(sorted(ids), min(n[k.rpartition("/")[2]], len(ids)))) for k, ids in sorted(puljer.items()) if n.get(k.rpartition("/")[2])}


def flad(s: str) -> str:
    return " ".join(re.sub(r"[\u200b-\u200d\u2060\ufeff\u00ad]", "", s).split())


def opgave(d: dict, xml: str, vejledning: bool) -> str:
    u = T.udtraek(xml)
    dele = [f"ID: {d['id']}\nTITEL: {d['navn']}\nTYPE: {d['type']}", "== INDLEDNING ==\n" + (u.get("praeambel") or "(ingen)"),
            "== FODNOTER ==\n" + ("\n".join(n[:LOFT * 2] for n in u.get("noter", [])) or "(ingen)")]
    if vejledning:
        dele.append(f"== TEKSTENS BEGYNDELSE (første {BEGYNDELSE} tegn) ==\n" + T.tekst(xml)[:BEGYNDELSE])
    else:
        fund = [f"[{p or 'uden betegnelse'}] {flad(t)[:LOFT]}" for p, t in T.afsnit(xml) if SOEG.search(t)]
        dele.append("== BESTEMMELSER OM KLAGE OG TILSYN ==\n" + ("\n".join(fund) or "(ingen)"))
    return "\n\n".join(dele) + "\n"


def poster() -> tuple[dict, dict]:
    tx = {r["id"]: r for r in map(json.loads, (E.KAT / "tekst.jsonl").open(encoding="utf-8"))}
    docs = {}
    for s in ("lta", *E.ANDRE):
        with (E.KAT / f"retsinformation_{s}.jsonl").open(encoding="utf-8") as f:
            docs.update((d["id"], d) for d in map(json.loads, f))
    return docs, tx


def runder() -> list[dict]:
    return json.loads(f.read_text(encoding="utf-8")) if (f := EVAL / "udtag.json").exists() else []


def skriv_udtag() -> dict:
    docs, tx = poster()
    trukket = runder()
    (EVAL / "opgaver").mkdir(parents=True, exist_ok=True)
    for froe, n in RUNDER[len(trukket):]:
        brugt = {i for r in trukket for ids in r["udtag"].values() for i in ids}
        valgt = udtag([(docs[i], t) for i, t in tx.items() if i not in brugt], n, froe)
        for k, ids in valgt.items():
            for i in ids:
                (EVAL / "opgaver" / f"{i}.txt").write_text(opgave(docs[i], gzip.decompress(T.sti(i).read_bytes()).decode("utf-8", "replace"), k.endswith("vejledning")), encoding="utf-8")
        trukket.append({"froe": froe, "pr_domaene": n, "udtag": valgt})
    (EVAL / "udtag.json").write_text(json.dumps(trukket, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return {f"runde {n}": sum(map(len, r["udtag"].values())) for n, r in enumerate(trukket, 1)}


def paragraf(b: str) -> str | None:
    m = re.match(r"§§?\s*(\d+)(?:\s?([a-zæøåA-ZÆØÅ])\b)?", b.strip())
    return f"§ {m[1]}{' ' + m[2].lower() if m[2] else ''}" if m else None


def kontrol(svar: dict, opg: str) -> tuple[dict, int]:
    """Svaret med de led, der kan genfindes i opgaven, omsat til katalogets id'er, og antallet af led og paragraffer der faldt fra."""
    tekst, ud, frafald = flad(opg), {}, 0
    indledning = tekst.split("== FODNOTER ==")[0]
    for felt in FELTER:
        ud[felt] = []
        for led in svar.get(felt) or []:
            citat = flad(str(led.get("citat") or ""))
            tal = str(led.get("nr")) in citat and (str(led.get("aar")) in citat or str(led.get("aar"))[2:] in citat)
            if len(citat) < 12 or citat not in tekst or (felt in ("hjemmel", "henviser", "eu") and not tal):
                frafald += 1
            elif felt == "eu":
                if led.get("type") in EU:
                    ud[felt].append({"retsakt": E.K.eu_id(f"{EU[led['type']]}:{int(led['aar'])}/{int(led['nr'])}")[0], "citat": citat})
                else:
                    frafald += 1
            elif felt in ("hjemmel", "henviser"):
                ny = {"dok": f"lta-{int(led['aar'])}-{int(led['nr'])}", "citat": citat}
                if felt == "hjemmel":
                    alle = [flad(b) for b in led.get("bestemmelser") or []]
                    ny["bestemmelser"] = [b for b in alle if paragraf(b) and re.search(re.escape(paragraf(b)).replace(r"\ ", r"\s?") + r"\b", indledning, re.IGNORECASE)]
                    frafald += len(alle) - len(ny["bestemmelser"])
                ud[felt].append(ny)
            else:
                ud[felt].append({k: flad(str(v)) for k, v in led.items() if v and k in ("afgoerelse_af", "klageinstans", "myndighed", "bestemmelse")} | {"citat": citat})
    return ud, frafald


def saml() -> dict:
    hvor = {i: (n, k) for n, r in enumerate(runder(), 1) for k, ids in r["udtag"].items() for i in ids}
    svar = {s["id"]: s for f in sorted(SVAR.glob("svar-*.json")) for s in json.loads(f.read_text(encoding="utf-8"))}
    ret = json.loads(f.read_text(encoding="utf-8")) if (f := UD / "rettelser.json").exists() else {}
    assert set(svar) <= set(hvor) and set(ret) <= set(svar), (set(svar) - set(hvor), set(ret) - set(svar))
    UD.mkdir(parents=True, exist_ok=True)
    tal = collections.Counter(mangler=len(set(hvor) - set(svar)))
    with (UD / "facit.jsonl").open("w", encoding="utf-8") as ud:
        for i in sorted(svar):
            opg = (EVAL / "opgaver" / f"{i}.txt").read_text(encoding="utf-8")
            led, frafald = kontrol(svar[i], opg)
            rettet, uden = kontrol({k: v for k, v in ret.get(i, {}).items() if k in FELTER}, opg)
            assert not uden, (i, "rettelse kan ikke genfindes i opgaven")
            led.update({k: rettet[k] for k in ret.get(i, {}) if k in FELTER})
            for k, fjern in ret.get(i, {}).get("fjern", {}).items():
                assert set(fjern) <= {x.get("dok", x.get("retsakt")) for x in led[k]}, (i, k, fjern)
                led[k] = [x for x in led[k] if x.get("dok", x.get("retsakt")) not in fjern]
            dom, _, g = hvor[i][1].rpartition("/")
            ud.write(E.linje({"id": i, "runde": hvor[i][0], "domaene": dom, "gruppe": g, **led, "frafald": frafald, **({"rettet": ret[i]["begrundelse"]} if i in ret else {})}))
            tal.update(dokumenter=1, frafald=frafald, rettet=i in ret, **{k: len(v) for k, v in led.items()})
    return dict(tal)


def pr(tp: int, fp: int, fn: int, fundet: int | None = None) -> dict:
    """tp og fp tæller kanter, fundet og fn tæller facit-led; fundet er tp, når en kant højst rammer ét led."""
    fundet = tp if fundet is None else fundet
    return {"rigtige": tp, "forkerte": fp, "mangler": fn, "praecision": round(100 * tp / (tp + fp)) if tp + fp else None,
            "genfinding": round(100 * fundet / (fundet + fn)) if fundet + fn else None}


def maal(facit: list[dict], docs: dict, kanter: list[dict], reg: dict, tx: dict) -> tuple[dict, list[dict]]:
    """Tal pr. mål og listen over afvigelser (kant uden facit, facit uden kant)."""
    fam = lambda i: (docs.get(i) or {}).get("gaeldende_version") or (docs.get(i) or {}).get("nyeste_version_afloeser_mangler") or i
    ind, ud = collections.defaultdict(list), collections.defaultdict(list)
    for k in kanter:
        ind[k["to"]].append(k)
        ud[k["from"]].append(k)
    navne = E.myndigheder(reg)
    klage = {(k["from"], k["to"]) for k in reg["edges"] if k["type"] == "klageinstans"}
    node = lambda navn: E.ALIAS.get(navn.lower()) or (navne.get(E.P.norm(navn)) or (None,))[0] if navn else None
    t, afv = collections.defaultdict(collections.Counter), []

    def saet(maal_: str, i: str, facit_: set, fundet: dict) -> None:
        """fundet: {nøgle: nøgler den rammer i facit}."""
        ramt = set().union(*fundet.values()) if fundet else set()
        t[maal_].update(tp=sum(bool(v) for v in fundet.values()), fp=sum(not v for v in fundet.values()), fn=len(facit_ - ramt), fundet=len(facit_ & ramt))
        afv.extend({"id": i, "maal": maal_, "art": "kant uden facit", "led": k} for k, v in fundet.items() if not v)
        afv.extend({"id": i, "maal": maal_, "art": "facit uden kant", "led": k} for k in sorted(facit_ - ramt))

    for f in facit:
        i = f["id"]
        if f["gruppe"] == "vejledning":
            g = {x["dok"] for x in f["henviser"]}
            naboer = {k["to"] for k in ud[i] if k["type"] == "henviser_til" and not k["to"].startswith("eu-")} | {k["from"] for k in ind[i] if k["type"] == "hjemmel_for"}
            saet(VEJLEDNING, i, g, {n: {x for x in g if fam(x) == fam(n)} for n in naboer})
            continue
        g = {x["dok"]: x for x in f["hjemmel"]}
        hj = [k for k in ind[i] if k["type"] == "hjemmel_for" and k["from"].startswith("lta-") and f["gruppe"] != "lov"]
        traef = {k["from"]: {x for x in g if fam(x) == fam(k["from"]) or x == k.get("citeret_version")} for k in hj}
        saet("hjemmel_for", i, set(g), traef)
        saet("hjemmel_for, kun Retsinformations felt", i, set(g), {k["from"]: traef[k["from"]] for k in hj if k["metode"] == E.METODE})
        for k in hj:
            for x in traef[k["from"]] if k.get("from_bestemmelse") else ():
                a, b = {paragraf(p) for p in k["from_bestemmelse"]}, {paragraf(p) for p in g[x]["bestemmelser"]}
                t["bestemmelser (paragrafnummer)"].update(tp=len(a & b), fp=len(a - b), fn=len(b - a), fundet=len(a & b))
                afv.extend({"id": i, "maal": "bestemmelser", "art": art, "led": f"{x}: {p}"} for art, s in (("kant uden facit", a - b), ("facit uden kant", b - a)) for p in sorted(s))
        g = {x["retsakt"] for x in f["eu"]}
        saet("implementerer_EU", i, g, {k["to"]: {k["to"]} & g for k in ud[i] if k["type"] == "implementerer_EU"})
        saet("EU-retsakter i XML-metadata (ikke brugt til kanter)", i, g, {e: {e} & g for e in map(celex, tx.get(i, {}).get("eu", [])) if e})
        for x in f["klage"]:
            til, fra = node(x.get("klageinstans")), node(x.get("afgoerelse_af"))
            t["klageinstans er en node"].update(tp=bool(til), fn=not til, fundet=bool(til))
            if til and fra:
                t["klagekant mellem de to noder"].update(tp=(til, fra) in klage, fn=(til, fra) not in klage, fundet=(til, fra) in klage)
            if not til:
                afv.append({"id": i, "maal": "klage", "art": "facit uden node", "led": x.get("klageinstans")})
        g = {node(x.get("klageinstans")) for x in f["klage"]} - {None}
        saet("klageinstans pr. forskrift", i, g, {k["from"]: {k["from"]} & g for k in ind[i] if k["type"] == "klageinstans"})
        g = {f"{til} ← {fra}" for til, fra in ((node(x.get("klageinstans")), node(x.get("afgoerelse_af"))) for x in f["klage"]) if til and fra}
        saet("afgørende myndighed på klagekanten", i, g, {p: {p} & g for k in ind[i] if k["type"] == "klageinstans" for p in (f"{k['from']} ← {a}" for a in k.get("afgoerelse_af", []))})
        g = {node(x.get("myndighed")) for x in f["tilsyn"]} - {None}
        saet("tilsynsmyndighed pr. forskrift", i, g, {k["from"]: {k["from"]} & g for k in ind[i] if k["type"] == "tilsyn"})
        for x in f["tilsyn"]:
            t["tilsynsmyndighed er en node"].update(tp=bool(node(x.get("myndighed"))), fn=not node(x.get("myndighed")), fundet=bool(node(x.get("myndighed"))))
    return {m: pr(c["tp"], c["fp"], c["fn"], c["fundet"]) | ({"forkerte": None, "praecision": None} if m == VEJLEDNING else {}) for m, c in t.items()}, [
        a for a in afv if (a["maal"], a["art"]) != (VEJLEDNING, "kant uden facit")]


def celex(c: str) -> str | None:
    m = re.fullmatch(r"3(\d{4})([LRD])(\d{4})", c)
    return E.K.eu_id(f"{ {'L': 'dir', 'R': 'reg', 'D': 'dec'}[m[2]] }:{m[1]}/{int(m[3])}")[0] if m else None


def readme(tal: dict, facit: list[dict], foerste: dict | None = None) -> str:
    """tal: {runde: maal(...)[0]}; foerste: en kontrolrundes første måling, før noget blev rettet efter den."""
    antal = collections.Counter((f["domaene"], f["runde"]) for f in facit)
    domaener = sorted({d for d, _ in antal})
    led = {k: sum(len(f[k]) for f in facit) for k in FELTER}
    r = ["# Evalueringssæt for kæderne", "",
         "Genereret af `pipeline/corpus/eval.py maal`. Facit står i `facit.jsonl`: ét dokument pr. linje med de led, en annotator har læst i dokumentets egen tekst, hvert med et ordret citat.",
         "", "## Udtag", "", f"{len(facit)} gældende danske dokumenter med hentet tekst, trukket tilfældigt pr. domæne: hovedbekendtgørelser med og uden registry-node og vejledninger.",
         "Runde 1 er brugt til at finde og rette fejl i udtrækkene, så dens tal er til den pæne side. Runde 2 er trukket bagefter; dens første måling, før noget blev rettet efter den, står i `kontrol-2.json` og i tabellen nedenfor.",
         "Runde 3 er trukket, efter at læseren af klage- og tilsynsbestemmelser var skrevet, og har love og lovbekendtgørelser med i stedet for vejledninger; dens første måling står i `kontrol-3.json`.", "",
         "| Domæne | " + " | ".join(f"Runde {n}" for n in tal) + " |", "|---|" + "---:|" * len(tal)]
    r += [f"| {d} | " + " | ".join(str(antal[d, n]) for n in tal) + " |" for d in domaener]
    r += ["", "Led i facit: " + ", ".join(f"{k} {v}" for k, v in led.items()) + f". Frafaldet i kontrollen: {sum(f['frafald'] for f in facit)} led eller paragraffer."
          + f" Rettet efter gennemsyn: {sum('rettet' in f for f in facit)} dokumenter.", "",
          "## Måling"]
    pct = lambda v: "–" if v is None else f"{v} %"
    for n, navn, maalt in [x for nr, t in tal.items() for x in ((nr, "udvikling" if nr == 1 else "kontrol, nuværende stand", t),
                                                               *([(nr, "kontrol, første måling før rettelser efter runden", foerste[nr])] if nr in (foerste or {}) else []))]:
        r += ["", f"### Runde {n} ({navn})", "", "| Mål | Rigtige | Forkerte | Mangler | Præcision | Genfinding |", "|---|---:|---:|---:|---:|---:|"]
        r += [f"| {m} | {v['rigtige']} | {'–' if v['forkerte'] is None else v['forkerte']} | {v['mangler']} | {pct(v['praecision'])} | {pct(v['genfinding'])} |" for m, v in maalt.items()]
    r += ["", "Rigtige og forkerte tæller katalogets eller registry'ets led, mangler tæller facit-led uden modstykke. Præcision er rigtige af rigtige plus forkerte, genfinding er andelen af facit-leddene, der har et modstykke. For vejledninger er kun genfinding målt.",
          "", "## Forbehold", "",
          "- Annotatoren er en sprogmodel (Haiku), ikke en jurist. Hvert led er kontrolleret mekanisk: citatet står ordret i dokumentet, nummer og år står i citatet, og paragrafferne står i indledningen. At citatet betyder det, leddet siger, er kun set efter for de afvigelser, der står som rettet.",
          f"- Annotatoren ser indledning og fodnoter og, for forskrifter, de paragraffer, der indeholder et af ordene i `SOEG`; for vejledninger de første {BEGYNDELSE} tegn. En klagebestemmelse med andre ord, eller en henvisning længere nede i en vejledning, er ikke i facit.",
          "- Klage og tilsyn pr. forskrift måler katalogets kanter fra dokumentets egne bestemmelser (metode `bestemmelse`). En kant tæller kun med, når mindst én af dens paragraffer blev vist for annotatoren; kanter fra paragraffer uden et af ordene i `SOEG` (fx \"fører kontrol med\") kan facit ikke indeholde. Facit-led, hvis myndighed ikke er en node, tælles under \"er en node\" og ikke her.",
          "- Læseren af klage- og tilsynsbestemmelser er rettet til efter afvigelserne i begge runder, så ingen af runderne er en uafhængig kontrol af den.",
          "- \"Klagekant mellem de to noder\" måler registry'ets kanter mellem myndigheder, ikke katalogets kanter til den enkelte forskrift.",
          "- En hjemmelskant til den gældende version af en omdøbt lov tæller som forkert, når kataloget ikke kobler den citerede version til den gældende. Fra 2026-11-15 kobles gældende loves versioner efter Retsinformations tidslinje; en lov, der er afløst af en ny hovedlov, kobles ikke til afløseren. Det samme gælder vejledningernes kanter, som Retsinformation fører under lovens gældende version.",
          "- Hjemmel i en tekstanmærkning til finansloven eller et aktstykke er ikke i facit og tælles ikke.",
          "- Udtaget er dokumenter fra 2010 og frem i de otte domæner, fordi ældre dokumenter sjældent har tekst i XML. Tallene siger ikke noget om resten af kataloget.", ""]
    return "\n".join(r)


def selftest() -> None:
    kat = {"status": {"vaerdi": "gældende"}, "retsomraade": "byggeri", "type": "bekendtgørelse", "dokumentrolle": "hoved", "territorium": "DK"}
    t = {"n_tegn": 5}
    assert [gruppe(d, x) for d, x in (({**kat, "id": "lta-1"}, t), ({**kat, "id": "lta-2", "registry_ids": ["b"]}, t), ({**kat, "id": "lta-3"}, {}),
                                      ({**kat, "id": "retsinfo-4", "type": "vejledning"}, t), ({**kat, "id": "lta-5", "dokumentrolle": "ændring"}, t),
                                      ({**kat, "id": "lta-6", "territorium": "GL"}, t))] == ["forskrift", "forskrift-registry", None, "vejledning", None, None]
    mange = [({**kat, "id": f"lta-{n}"}, t) for n in range(30)] + [({**kat, "id": "lta-x", "retsomraade": "skat"}, t)]
    froe, n = RUNDER[0]
    u = udtag(mange, n, froe)
    assert u == udtag(mange, n, froe) != udtag(mange, n, froe + 1) and list(u) == ["byggeri/forskrift"] and len(u["byggeri/forskrift"]) == 7
    assert udtag(mange[:3], n, froe)["byggeri/forskrift"] == ["lta-0", "lta-1", "lta-2"]
    assert udtag([({**kat, "id": "lta-1", "retsomraade": "el-gas-vvs"}, t)], n, froe) == {"el/gas/VVS/forskrift": ["lta-1"]}
    assert [paragraf(b) for b in ("§ 6, stk. 1, litra a-d", "§ 16 C, stk. 9", "§16a", "stk. 2", "§§ 29-31")] == ["§ 6", "§ 16 c", "§ 16 a", None, "§ 29"]
    assert celex("32010L0031") == "eu-dir-2010-31" and celex("32011R0305") == "eu-reg-2011-305" and celex("x") is None
    xml = """<Dokument><Meta/><Indledning><Char>I medfør af § 5, stk. 2, og § 16 C i lov om æbler, jf. lovbekendtgørelse nr. 7 af 1. januar 2020, fastsættes:</Char>
<Nota><Char>1) Bekendtgørelsen gennemfører direktiv 2010/31/EU om æbler.</Char></Nota></Indledning>
<Paragraf><Explicatus>§ 1.</Explicatus><Char>Æbler er frugt.</Char></Paragraf>
<Paragraf><Explicatus>§ 9.</Explicatus><Char>Æblestyrelsens afgørelser kan påklages til Frugtklagenævnet.</Char></Paragraf></Dokument>"""
    opg = opgave({"id": "lta-2020-9", "navn": "Bekendtgørelse om æbler", "type": "bekendtgørelse"}, xml, False)
    assert "[§ 9] § 9. Æblestyrelsens afgørelser" in opg and "Æbler er frugt" not in opg and "gennemfører direktiv 2010/31/EU" in opg.split("== FODNOTER ==")[1]
    assert "TEKSTENS BEGYNDELSE" in opgave({"id": "retsinfo-1", "navn": "V", "type": "vejledning"}, xml, True)
    svar = {"hjemmel": [{"type": "lovbekendtgørelse", "nr": 7, "aar": 2020, "bestemmelser": ["§ 5, stk. 2", "§ 16 C", "§ 44"], "citat": "lovbekendtgørelse nr. 7 af 1. januar 2020"},
                        {"type": "lov", "nr": 8, "aar": 2020, "bestemmelser": [], "citat": "lovbekendtgørelse nr. 7 af 1. januar 2020"},
                        {"type": "lov", "nr": 7, "aar": 2020, "bestemmelser": [], "citat": "lov nr. 7 af 1. januar 2020 om pærer"}],
            "eu": [{"type": "direktiv", "aar": 2010, "nr": 31, "citat": "gennemfører direktiv 2010/31/EU om æbler"}],
            "klage": [{"afgoerelse_af": "Æblestyrelsen", "klageinstans": "Frugtklagenævnet", "bestemmelse": "§ 9", "citat": "Æblestyrelsens afgørelser kan påklages   til Frugtklagenævnet."}],
            "tilsyn": [{"myndighed": "Æblestyrelsen", "citat": "fører tilsyn med æblerne"}]}
    led, frafald = kontrol(svar, opg)
    assert led["hjemmel"] == [{"dok": "lta-2020-7", "citat": "lovbekendtgørelse nr. 7 af 1. januar 2020", "bestemmelser": ["§ 5, stk. 2", "§ 16 C"]}] and frafald == 4
    assert led["eu"][0]["retsakt"] == "eu-dir-2010-31" and led["klage"][0]["klageinstans"] == "Frugtklagenævnet" and led["tilsyn"] == [] and led["henviser"] == []
    docs = {"lta-2020-7": {"gaeldende_version": "lta-2025-1"}, "lta-2025-1": {}, "lta-2021-3": {}}
    facit = [{"id": "lta-2020-9", "runde": 1, "gruppe": "forskrift", "domaene": "byggeri", **led, "frafald": frafald},
             {"id": "retsinfo-1", "runde": 1, "gruppe": "vejledning", "domaene": "byggeri", "hjemmel": [], "eu": [], "klage": [], "tilsyn": [], "frafald": 0,
              "henviser": [{"dok": "lta-2020-9", "citat": "x"}, {"dok": "lta-2021-3", "citat": "y"}]}]
    kanter = [{"from": "lta-2025-1", "type": "hjemmel_for", "to": "lta-2020-9", "metode": E.PRAEAMBEL, "from_bestemmelse": ["§ 5, stk. 2", "§ 17"]},
              {"from": "lta-2021-3", "type": "hjemmel_for", "to": "lta-2020-9", "metode": E.METODE},
              {"from": "lta-2020-9", "type": "implementerer_EU", "to": "eu-dir-2010-31"}, {"from": "lta-2020-9", "type": "implementerer_EU", "to": "eu-dir-1999-1"},
              {"from": "retsinfo-1", "type": "henviser_til", "to": "lta-2020-9"}, {"from": "retsinfo-1", "type": "henviser_til", "to": "eu-dir-1999-1"}]
    reg = {"nodes": [{"id": "sty-aeble", "type": "styrelse", "navn": "Æblestyrelsen"}, {"id": "naevn-frugt", "type": "klagenævn", "navn": "Frugtklagenævnet"}],
           "edges": [{"from": "naevn-frugt", "type": "klageinstans", "to": "sty-aeble"}]}
    tal, afv = maal(facit, docs, kanter, reg, {"lta-2020-9": {"eu": ["32010L0031", "32011R0305"]}})
    assert tal["hjemmel_for"] == pr(1, 1, 0) and tal["hjemmel_for, kun Retsinformations felt"] == pr(0, 1, 1) and tal["bestemmelser (paragrafnummer)"] == pr(1, 1, 1)
    assert tal["implementerer_EU"] == pr(1, 1, 0) and tal["EU-retsakter i XML-metadata (ikke brugt til kanter)"] == pr(1, 1, 0) and tal[VEJLEDNING] == pr(1, 0, 1) | {"forkerte": None, "praecision": None}
    assert tal["klageinstans er en node"] == pr(1, 0, 0) == tal["klagekant mellem de to noder"] and pr(0, 0, 0)["praecision"] is None
    assert {"id": "lta-2020-9", "maal": "bestemmelser", "art": "facit uden kant", "led": "lta-2020-7: § 16 c"} in afv and "| hjemmel_for | 1 | 1 | 0 | 50 % | 100 % |" in readme({1: tal}, facit)
    assert f"| {VEJLEDNING} | 1 | – | 1 | – | 50 % |" in readme({1: tal}, facit) and "### Runde 1 (udvikling)" in readme({1: tal}, facit)
    assert "### Runde 2 (kontrol, første måling før rettelser efter runden)" in readme({1: tal, 2: tal}, facit, {2: tal})
    print("selftest ok")


if __name__ == "__main__":
    kommando = sys.argv[1] if len(sys.argv) > 1 else ""
    if kommando == "selftest":
        selftest()
    elif kommando == "udtag":
        print(json.dumps(skriv_udtag(), ensure_ascii=False))
    elif kommando == "saml":
        print(json.dumps(saml(), ensure_ascii=False))
    elif kommando == "maal":
        docs, tx = poster()
        facit = [json.loads(x) for x in (UD / "facit.jsonl").open(encoding="utf-8")]
        with (E.KAT / "kanter.jsonl").open(encoding="utf-8") as f:
            ids = {x["id"] for x in facit}
            vist = {i: set(re.findall(r"^\[([^\]]+)\]", (EVAL / "opgaver" / f"{i}.txt").read_text(encoding="utf-8"), re.MULTILINE)) for i in ids}
            kanter = [k for k in map(json.loads, f) if (k["from"] in ids or k["to"] in ids)
                      and (k.get("metode") != E.BESTEMMELSE or set(k["to_bestemmelse"]) & vist[k["to"]])]
        reg = E.P.yaml.load(E.P.REG.read_text(encoding="utf-8"), Loader=E.P.yaml.CSafeLoader)
        maalt = {n: maal([f for f in facit if f["runde"] == n], docs, kanter, reg, tx) for n in sorted({f["runde"] for f in facit})}
        tal = {n: t for n, (t, _) in maalt.items()}
        for n in [n for n in tal if n > 1 and not (UD / f"kontrol-{n}.json").exists()]:
            (UD / f"kontrol-{n}.json").write_text(json.dumps(tal[n], ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        foerste = {n: json.loads(f.read_text(encoding="utf-8")) for n in tal if (f := UD / f"kontrol-{n}.json").exists()}
        (UD / "README.md").write_text(readme(tal, facit, foerste), encoding="utf-8")
        (EVAL / "afvigelser.jsonl").write_text("".join(E.linje({"runde": n, **a}) for n, (_, afv) in maalt.items() for a in afv), encoding="utf-8")
        print(json.dumps(tal, ensure_ascii=False, indent=1))
    else:
        sys.exit(__doc__)
