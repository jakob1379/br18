#!/usr/bin/env python3
"""Validate registry.yaml and generate the derived Markdown views.

registry.yaml is the single source of truth. Everything under diagrammer/,
plus datakilder.md and huller.md, is generated from it by this script and
must not be edited by hand.

    python3 dk-regulering/scripts/build.py            # validate + write views
    python3 dk-regulering/scripts/build.py --check    # validate + fail if views are stale
    python3 dk-regulering/scripts/build.py --selftest

Requires PyYAML.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "registry.yaml"
DIAGRAM_DIR = ROOT / "diagrammer"
KATALOG_DIR = ROOT / "katalog"

EDGE_TYPES = {
    "ressortansvar",
    "delegation",
    "hjemmel_for",
    "udsteder",
    "klageinstans",
    "tilsyn",
    "implementerer_EU",
    "henviser_til",
}
CERTAINTY = {"verificeret", "sandsynlig", "ukendt"}
STATUS = {"aktiv", "nedlagt", "omdøbt", "ophævet", "ukendt"}
ACCESS = {"API", "bulk", "ELI", "RSS", "HTML", "PDF", "betalingsmur", "ukendt", "ikke-relevant"}
BINDING = {"bindende", "vejledende", "blandet", "ukendt"}

INSTANCE_TYPES = {
    "ministerium", "styrelse", "direktorat", "nævn", "klagenævn", "tilsyn", "råd", "fond",
    "domstol", "ombudsmand", "kommune", "region", "offentlig-virksomhed", "eu-institution",
    "privat-organisation", "standardiseringsorgan",
}
DOCUMENT_TYPES = {
    "dokumentkilde", "lov", "bekendtgørelse", "cirkulære", "vejledning", "teknisk-forskrift",
    "plan", "regulativ", "eu-direktiv", "eu-forordning", "eu-afgørelse", "standard",
    "branchevejledning", "praksissamling",
}
NODE_TYPES = INSTANCE_TYPES | DOCUMENT_TYPES

# Claim fields every node carries: {..., kilder: [url], sikkerhed: ...}
CLAIM_FIELDS = ("hjemmel", "dokumenttyper", "url", "adgang", "identifikatorer", "licens", "opdatering")

ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
URL_RE = re.compile(r"^https?://\S+$")
NOT_FOUND = "ikke fundet"
NO_URL = {NOT_FOUND, "ikke relevant"}


def load() -> dict:
    with REGISTRY.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


# ---------------------------------------------------------------- validation


def validate(reg: dict) -> list[str]:
    errors: list[str] = []
    err = errors.append

    for key in ("meta", "nodes", "edges", "huller"):
        if key not in reg:
            err(f"top-level key mangler: {key}")
    if errors:
        return errors

    ids: dict[str, dict] = {}
    for n in reg["nodes"]:
        nid = n.get("id", "<uden id>")
        if not ID_RE.match(str(nid)):
            err(f"{nid}: ugyldigt id (små bogstaver, cifre, bindestreger)")
        if nid in ids:
            err(f"{nid}: dublet-id")
        ids[nid] = n

    for nid, n in ids.items():
        for f in ("navn", "type", "ministerium", "status"):
            if f not in n:
                err(f"{nid}: felt mangler: {f}")
        if n.get("type") not in NODE_TYPES:
            err(f"{nid}: ukendt type {n.get('type')!r}")
        if n.get("status") not in STATUS:
            err(f"{nid}: ukendt status {n.get('status')!r}")
        parent = n.get("ministerium")
        if parent not in (None, "ingen") and parent not in ids:
            err(f"{nid}: ministerium {parent!r} findes ikke som node")
        elif parent in ids and ids[parent].get("type") != "ministerium":
            err(f"{nid}: ministerium {parent!r} er ikke af type ministerium")
        for f in CLAIM_FIELDS:
            claim = n.get(f)
            if not isinstance(claim, dict):
                err(f"{nid}.{f}: mangler eller er ikke et objekt")
                continue
            errors.extend(_check_claim(f"{nid}.{f}", claim))
        url = n.get("url", {}).get("vaerdi")
        if url is not None and url not in NO_URL and not URL_RE.match(str(url)):
            err(f"{nid}.url: hverken URL eller {sorted(NO_URL)}: {url!r}")
        for a in n.get("adgang", {}).get("vaerdier", []) or []:
            if a not in ACCESS:
                err(f"{nid}.adgang: ukendt værdi {a!r}")
        for d in n.get("dokumenttyper", {}).get("liste", []) or []:
            if d.get("bindende") not in BINDING:
                err(f"{nid}.dokumenttyper: ukendt bindende-værdi {d.get('bindende')!r}")
        for p in n.get("tidligere_navne", []) or []:
            if "navn" not in p:
                err(f"{nid}.tidligere_navne: post uden navn")
            if p.get("efterfoelger") and p["efterfoelger"] not in ids:
                err(f"{nid}.tidligere_navne: efterfølger {p['efterfoelger']!r} findes ikke")
            errors.extend(_check_claim(f"{nid}.tidligere_navne[{p.get('navn')}]", p))
        ing = n.get("ingest")
        if ing is not None:
            for f in ("vaerdi", "besvaer"):
                if not isinstance(ing.get(f), int) or not 1 <= ing[f] <= 5:
                    err(f"{nid}.ingest.{f}: skal være heltal 1-5")

    seen_edges = set()
    for e in reg["edges"]:
        key = (e.get("from"), e.get("type"), e.get("to"))
        label = "|".join(map(str, key))
        if e.get("type") not in EDGE_TYPES:
            err(f"kant {label}: ukendt kanttype")
        for end in ("from", "to"):
            if e.get(end) not in ids:
                err(f"kant {label}: {end}-node findes ikke")
        if key in seen_edges:
            err(f"kant {label}: dublet")
        seen_edges.add(key)
        errors.extend(_check_claim(f"kant {label}", e))

    for i, h in enumerate(reg["huller"]):
        for nid in h.get("noder", []) or []:
            if nid not in ids:
                err(f"huller[{i}]: node {nid!r} findes ikke")
    return errors


def _check_claim(where: str, claim: dict) -> list[str]:
    out = []
    s = claim.get("sikkerhed")
    if s not in CERTAINTY:
        out.append(f"{where}: sikkerhed skal være en af {sorted(CERTAINTY)}, fik {s!r}")
    kilder = claim.get("kilder")
    if not isinstance(kilder, list):
        out.append(f"{where}: kilder skal være en liste")
        return out
    for k in kilder:
        if not URL_RE.match(str(k)):
            out.append(f"{where}: kilde er ikke en URL: {k!r}")
    if s == "verificeret" and not kilder:
        out.append(f"{where}: verificeret uden kilde")
    return out


# ---------------------------------------------------------------- katalog (bulk-lag)

CAT_TYPES = {
    "lov", "ændringslov", "lovbekendtgørelse", "bekendtgørelse", "ændringsbekendtgørelse", "ikrafttrædelsesbekendtgørelse",
    "bekendtgørelse-international", "anordning", "ændringsanordning", "ikrafttrædelsesanordning", "bekendtgørelse-af-anordning", "åbent-brev",
}
CAT_ID = re.compile(r"^((lta|ltb|ltc|mt|retsinfo|fob)-\d{4}-\d+|ft-\d{5}[0-9A-Z]{7})$")
CAT_TYPE = re.compile(r"^[a-zæøå0-9]+(?:-[a-zæøå0-9]+)*$")
CAT_SAMLINGER = {"ltb": "Lovtidende B", "ltc": "Lovtidende C", "mt": "Ministerialtidende",
                 "retsinfo": "Retsinformation (administrative forskrifter og afgørelser)", "fob": "Folketingets Ombudsmand",
                 "ft": "Folketingstidende (lovforslag, betænkninger, beslutningsforslag)"}
EU_ID = re.compile(r"^eu-(dir|reg|dec)-\d{4}-\d+$")
CELEX = re.compile(r"^3\d{4}[LRD]\d{4,}$")


def load_katalog() -> dict | None:
    f = KATALOG_DIR / "retsinformation_lta.jsonl"
    if not f.exists():
        return None
    rd = lambda p: [json.loads(l) for l in p.open(encoding="utf-8")] if p.exists() else []
    docs = [d for p in sorted(KATALOG_DIR.glob("retsinformation_*.jsonl")) for d in rd(p)]
    return {"docs": docs, "edges": rd(KATALOG_DIR / "kanter.jsonl"), "eu": rd(KATALOG_DIR / "eu_index.jsonl"), "tekst": rd(KATALOG_DIR / "tekst.jsonl")}


def validate_katalog(reg: dict, kat: dict) -> list[str]:
    errors: list[str] = []
    err = errors.append
    reg_ids = {n["id"] for n in reg["nodes"]}
    mins = {n["id"] for n in reg["nodes"] if n["type"] == "ministerium"}
    docs = {}
    for d in kat["docs"]:
        i = d.get("id")
        if not CAT_ID.match(str(i)):
            err(f"katalog {i}: ugyldigt id")
        if i in docs:
            err(f"katalog {i}: dublet")
        docs[i] = d
    for i, d in docs.items():
        if d.get("type") not in CAT_TYPES and (str(i).startswith("lta-") or not CAT_TYPE.match(str(d.get("type")))):
            err(f"katalog {i}: ukendt type {d.get('type')!r}")
        kilder = d.get("kilder")
        if not isinstance(kilder, list) or any(not URL_RE.match(str(k)) for k in kilder):
            err(f"katalog {i}: kilder skal være en liste af URL'er")
            kilder = []
        if (d.get("status") or {}).get("vaerdi") not in ("gældende", "historisk"):
            err(f"katalog {i}: ukendt status")
        for f in ("status", "identifikatorer", "udstedt_af", "ministerium"):
            c = d.get(f)
            if c is None:
                continue
            if c.get("sikkerhed") not in CERTAINTY:
                err(f"katalog {i}.{f}: ugyldig sikkerhed {c.get('sikkerhed')!r}")
            if c.get("sikkerhed") == "verificeret" and not kilder:
                err(f"katalog {i}.{f}: verificeret uden kilde")
        m = (d.get("ministerium") or {}).get("vaerdi")
        if m is not None and m not in mins and m not in ("ingen", "ukendt"):
            err(f"katalog {i}: ministerium {m!r} findes ikke")
        for r in d.get("registry_ids") or []:
            if r not in reg_ids:
                err(f"katalog {i}: registry_id {r!r} findes ikke")
        if (af := d.get("afloeser")) is not None:
            tekst, ophaevelse = (" ".join(str(af.get(k) or "").split()) for k in ("paragraf_tekst", "ophaevelse"))
            if (af.get("vaerdi") not in docs or af.get("sikkerhed") != "verificeret" or not af.get("kilder") or any(not URL_RE.match(str(k)) for k in af["kilder"])
                    or not ophaevelse or ophaevelse not in tekst or "ophæves" not in tekst or f"nr. {str(i).split('-')[-1]} " not in ophaevelse
                    or not isinstance(af.get("bevarer_regler"), (str, type(None)))):
                err(f"katalog {i}: ugyldigt afloeser-felt (afløser i kataloget, verificeret, kilde og ordret ophævelse af nr. og dato i paragraffen)")
        for t in [d.get("gaeldende_version"), d.get("lov"), d.get("afloeser_fra")] + list(d.get("aendrer") or []):
            if t and t not in docs:
                err(f"katalog {i}: henvisning til ukendt dokument {t!r}")
    eus = set()
    for e in kat["eu"]:
        if not EU_ID.match(str(e.get("id"))):
            err(f"eu_index {e.get('id')}: ugyldigt id")
        if not CELEX.match(str((e.get("identifikatorer") or {}).get("celex"))):
            err(f"eu_index {e.get('id')}: ugyldigt CELEX")
        eus.add(e.get("id"))
    known = reg_ids | set(docs) | eus
    seen = set()
    for e in kat["edges"]:
        key = (e.get("from"), e.get("type"), e.get("to"))
        label = "|".join(map(str, key))
        if e.get("type") not in EDGE_TYPES:
            err(f"katalog-kant {label}: ukendt kanttype")
        for end in ("from", "to"):
            if e.get(end) not in known:
                err(f"katalog-kant {label}: {end}-node findes ikke")
        if key in seen:
            err(f"katalog-kant {label}: dublet")
        seen.add(key)
        errors.extend(_check_claim(f"katalog-kant {label}", e))
        if "from_bestemmelse" in e and not (e["from_bestemmelse"] and all(str(b).startswith("§") for b in e["from_bestemmelse"])):
            err(f"katalog-kant {label}: from_bestemmelse skal være en ikke-tom liste af bestemmelser")
        if "to_bestemmelse" in e and not (e["to_bestemmelse"] and all(str(b).startswith("§") for b in e["to_bestemmelse"])):
            err(f"katalog-kant {label}: to_bestemmelse skal være en ikke-tom liste af bestemmelser")
        for a in e.get("afgoerelse_af") or []:
            if a not in reg_ids:
                err(f"katalog-kant {label}: afgoerelse_af {a!r} findes ikke")
        if "senere_aendret_ved" in e and not (isinstance(e["senere_aendret_ved"], list) and e["senere_aendret_ved"] and all(isinstance(a, str) and a in docs for a in e["senere_aendret_ved"])):
            err(f"katalog-kant {label}: senere_aendret_ved skal være en ikke-tom liste af dokumenter i kataloget")
        if e.get("citeret_version") and e["citeret_version"] not in docs:
            err(f"katalog-kant {label}: citeret_version {e['citeret_version']!r} findes ikke")
    for t in kat["tekst"]:
        if t.get("id") not in docs:
            err(f"tekst {t.get('id')}: dokumentet findes ikke i kataloget")
        if not (ROOT.parent / str(t.get("xml"))).is_file():
            err(f"tekst {t.get('id')}: XML-filen {t.get('xml')!r} findes ikke")
    return errors[:200] + ([f"... {len(errors) - 200} flere"] if len(errors) > 200 else [])


def gen_katalog(reg: dict, kat: dict) -> str:
    docs = [d for d in kat["docs"] if d["id"].startswith("lta-")]
    andre = [d for d in kat["docs"] if not d["id"].startswith("lta-")]
    C = lambda it: sorted(defaultdict_count(it).items(), key=lambda x: (-x[1], str(x[0])))
    reg_names = {n["id"]: n["navn"] for n in reg["nodes"]}
    gd = [d for d in docs if d["status"]["vaerdi"] == "gældende"]
    lines = [
        "# Katalog: Retsinformations dokumenter",
        "",
        "> Genereret af `scripts/build.py` fra `katalog/*.jsonl`. Redigér ikke i hånden.",
        "",
        f"- Lovtidende A: **{len(docs)}** dokumenter (gældende: {len(gd)}, historiske: {len(docs) - len(gd)}); tabellerne herunder gælder Lovtidende A, hvor andet ikke står",
        f"- Øvrige samlinger: **{len(andre)}** dokumenter (cirkulærer, vejledninger, afgørelser m.m., se nederst)",
        f"- Seneste udstedelsesdato i datasættet: {max(d['datoer'].get('udstedt') or '' for d in docs)}",
        f"- Status høstet: {min(d['status']['pr'] or '9' for d in docs)} – {max(d['status']['pr'] or '' for d in docs)}",
        f"- Kanter: {len(kat['edges'])} · EU-retsakter refereret: {len(kat['eu'])} · koblet til registry-noder: {sum(len(d.get('registry_ids') or []) for d in kat['docs'])}",
        "",
        "## Dokumenttyper",
        "",
        "| Type | Gældende | Historisk |",
        "|------|---------:|----------:|",
    ]
    tg = defaultdict_count(d["type"] for d in gd)
    th = defaultdict_count(d["type"] for d in docs if d["status"]["vaerdi"] != "gældende")
    for t in sorted(set(tg) | set(th), key=lambda t: -(tg.get(t, 0) + th.get(t, 0))):
        lines.append(f"| {t} | {tg.get(t, 0)} | {th.get(t, 0)} |")
    lines += ["", "## Gældende dokumenter pr. nuværende ressortministerium (Retsinformations ressortfelt eller klassifikation)", "",
              "| Ministerium | Antal | heraf sandsynlig | heraf ukendt |", "|---|---:|---:|---:|"]
    by = defaultdict(lambda: [0, 0, 0])
    for d in gd:
        m = d.get("ministerium") or {"vaerdi": "ikke klassificeret", "sikkerhed": "ukendt"}
        b = by[m["vaerdi"]]
        b[0] += 1
        b[1 if m["sikkerhed"] == "sandsynlig" else 2] += 1
    for m, (n, s, u) in sorted(by.items(), key=lambda x: -x[1][0]):
        lines.append(f"| {md_cell(reg_names.get(m, m))} (`{m}`) | {n} | {s} | {u} |")
    lines += ["", "## Gældende dokumenter pr. retsområde", "", "| Retsområde | Antal |", "|---|---:|"]
    lines += [f"| {k} | {v} |" for k, v in C(d.get("retsomraade", "ikke klassificeret") for d in gd)]
    lines += ["", "## Udstedende ministerium (historisk navn, alle dokumenter, top 40)", "", "| Udsteder | Antal |", "|---|---:|"]
    lines += [f"| {md_cell(k)} | {v} |" for k, v in C(d["udstedt_af"]["vaerdi"] for d in docs)[:40]]
    lines += ["", "## Kanter", "", "| Kanttype | verificeret | sandsynlig | ukendt |", "|---|---:|---:|---:|"]
    ec = defaultdict(lambda: defaultdict(int))
    for e in kat["edges"]:
        ec[e["type"]][e["sikkerhed"]] += 1
    for t, c in sorted(ec.items()):
        lines.append(f"| {t} | {c['verificeret']} | {c['sandsynlig']} | {c['ukendt']} |")
    laest = [e for e in kat["edges"] if e.get("metode") == "bestemmelse"]
    lines += ["", (f"Klageinstans- og tilsynskanter fra dokumentets egne bestemmelser, hvor dokumentet siden er ændret (`senere_aendret_ved`): "
                   f"{sum('senere_aendret_ved' in e for e in laest)} af {len(laest)}.")]
    koblet = {e["from"] if e["type"] == "henviser_til" else e["to"] for e in kat["edges"]
              if e.get("metode") == "retsinformation-eksport" and e["type"] in ("hjemmel_for", "henviser_til")}
    lines += ["", "## Øvrige samlinger", "",
              ("Dokumenter uden for Lovtidende A, direkte fra Retsinformations søgeeksport (kun metadata). Koblet til lovgivning: dokumentet har mindst én kant fra "
               "eksportens hjemmelsfelt, `hjemmel_for` fra loven til forskrifter og vejledninger og `henviser_til` fra afgørelser, udtalelser og domme til loven. "
               "I Folketingstidende har alle dokumenter om samme lovforslag samme nøgle i feltet `lovforslag`, og den vedtagne tekst har feltet `lov`: den lov, "
               "den blev til (samme titel, underskrevet højst 60 dage efter vedtagelsen); lovforslagets dokumenter har så en `henviser_til`-kant til loven (sandsynlig). "
               "Ministerium er Retsinformations ressortfelt, når det med sikkerhed er aktuelt, og ellers arvet fra den lovgivning, dokumentet vedrører (sandsynlig)."), "",
              "| Samling | Fil | Dokumenter | Gældende | heraf koblet til lovgivning | med ministerium | heraf sandsynlig | med retsområde |", "|---|---|---:|---:|---:|---:|---:|---:|"]
    for s, navn in CAT_SAMLINGER.items():
        ds = [d for d in andre if d["id"].startswith(s + "-")]
        g = [d for d in ds if d["status"]["vaerdi"] == "gældende"]
        mins = [d["ministerium"]["sikkerhed"] for d in g if d.get("ministerium")]
        lines.append(f"| {navn} | `retsinformation_{s}.jsonl` | {len(ds)} | {len(g)} | {sum(d['id'] in koblet for d in g)} | {len(mins)} | {mins.count('sandsynlig')} "
                     f"| {sum(bool(d.get('retsomraade')) for d in g)} |")
    ag = defaultdict_count(d["type"] for d in andre if d["status"]["vaerdi"] == "gældende")
    ah = defaultdict_count(d["type"] for d in andre if d["status"]["vaerdi"] != "gældende")
    ak = defaultdict_count(d["type"] for d in andre if d["status"]["vaerdi"] == "gældende" and d["id"] in koblet)
    typer = sorted(set(ag) | set(ah), key=lambda t: (-(ag.get(t, 0) + ah.get(t, 0)), t))
    lines += ["", f"### Dokumenttyper i de øvrige samlinger (top 30 af {len(typer)})", "", "| Type | Gældende | Historisk | Gældende koblet til lovgivning |", "|------|---------:|----------:|---------:|"]
    lines += [f"| {t} | {ag.get(t, 0)} | {ah.get(t, 0)} | {ak.get(t, 0)} |" for t in typer[:30]]
    med = {t["id"]: t for t in kat["tekst"]}
    lines += ["", "## Tekst", "",
              ("Retsinformations XML er hentet for et udsnit af kataloget med `pipeline/corpus/tekst.py`: de dokumenter, registry'ets noder peger på, og gældende "
               "dokumenter i de otte domæner. `tekst.jsonl` har én linje pr. hentet dokument med stien til XML-filen (`intermediate/corpus/xml/`), hentedato, omfang, "
               "præambel, fodnoter, underskriftssted og de EU-retsakter, Retsinformation fører på dokumentet. For en del ældre dokumenter har XML-filen kun metadata og "
               "ingen tekst (`n_tegn` er 0). Alle andre dokumenter har kun metadata."), "",
              "| Samling | XML hentet | heraf med tekst | heraf gældende med tekst | Tegn (mio.) | med præambel | med EU-retsakt |", "|---|---:|---:|---:|---:|---:|---:|"]
    for s, navn in {"lta": "Lovtidende A", **CAT_SAMLINGER}.items():
        ts = [(d, med[d["id"]]) for d in kat["docs"] if d["id"].startswith(s + "-") and d["id"] in med]
        if ts:
            lines.append(f"| {navn} | {len(ts)} | {sum(t['n_tegn'] > 0 for _, t in ts)} | {sum(d['status']['vaerdi'] == 'gældende' and t['n_tegn'] > 0 for d, t in ts)} "
                         f"| {sum(t['n_tegn'] for _, t in ts) / 1e6:.1f} "
                         f"| {sum('praeambel' in t for _, t in ts)} | {sum('eu' in t for _, t in ts)} |")
    lines += ["", "## Mest refererede EU-retsakter (top 30)", "", "| Id | CELEX | Dokumenter | heraf gældende | Gennemførelses-kanter | I registry |", "|---|---|---:|---:|---:|---|"]
    for e in kat["eu"][:30]:
        lines.append(f"| `{e['id']}` | {e['identifikatorer']['celex']} | {e['n_dok']} | {e['n_gaeldende']} | {e['n_implementerer']} | {'ja' if e.get('registry_id') else ''} |")
    lines.append("")
    return "\n".join(lines)


def defaultdict_count(it) -> dict:
    c: dict = defaultdict(int)
    for x in it:
        c[x] += 1
    return dict(c)


# ---------------------------------------------------------------- mermaid


def mid(node_id: str) -> str:
    return node_id.replace("-", "_")


def mlabel(text: str) -> str:
    return text.replace('"', "#quot;").replace("<", "#lt;").replace(">", "#gt;")


CLASSDEFS = """    classDef ministerium fill:#1f3a5f,stroke:#0d1b2a,color:#fff
    classDef instans fill:#d7e3f4,stroke:#1f3a5f,color:#0d1b2a
    classDef klage fill:#f6dcc2,stroke:#8a4b08,color:#3b1f00
    classDef retsakt fill:#e6f2e6,stroke:#2e6b2e,color:#103010
    classDef eu fill:#fff3b0,stroke:#7a6a00,color:#333
    classDef kilde fill:#eee,stroke:#666,color:#222
    classDef nedlagt fill:#fff,stroke:#999,color:#999,stroke-dasharray:4 3"""


def node_class(n: dict) -> str:
    if n.get("status") in ("nedlagt", "omdøbt", "ophævet"):
        return "nedlagt"
    t = n["type"]
    if t == "ministerium":
        return "ministerium"
    if t in ("nævn", "klagenævn", "domstol", "ombudsmand"):
        return "klage"
    if t.startswith("eu-"):
        return "eu"
    if t in ("dokumentkilde", "standard", "branchevejledning", "praksissamling", "standardiseringsorgan", "privat-organisation"):
        return "kilde"
    if t in INSTANCE_TYPES:
        return "instans"
    return "retsakt"


def node_line(n: dict) -> str:
    name = n["navn"]
    if n.get("status") in ("nedlagt", "omdøbt", "ophævet"):
        name += f" ({n['status']})"
    return f'    {mid(n["id"])}["{mlabel(name)}"]:::{node_class(n)}'


def mermaid(nodes: list[dict], edges: list[dict], direction: str = "LR") -> str:
    lines = ["```mermaid", f"flowchart {direction}", CLASSDEFS]
    lines += [node_line(n) for n in nodes]
    for e in edges:
        arrow = "-.->" if e.get("sikkerhed") != "verificeret" else "-->"
        lines.append(f'    {mid(e["from"])} {arrow}|{e["type"]}| {mid(e["to"])}')
    lines.append("```")
    return "\n".join(lines)


def is_instance(n: dict) -> bool:
    return n["type"] in INSTANCE_TYPES and n["type"] != "ministerium"


def gen_diagrams(reg: dict) -> dict[Path, str]:
    nodes = {n["id"]: n for n in reg["nodes"]}
    edges = reg["edges"]
    ministries = sorted((n for n in nodes.values() if n["type"] == "ministerium"), key=lambda n: n["navn"])
    date = reg["meta"]["dato"]
    legend = (
        f"> Genereret af `scripts/build.py` fra `registry.yaml` (dato {date}). Redigér ikke i hånden.\n"
        "> Fuldt optrukne pile = `verificeret`; stiplede = `sandsynlig`/`ukendt`. "
        "Grå stiplede bokse = nedlagt/omdøbt/ophævet.\n"
    )
    out: dict[Path, str] = {}

    # Overview: ministry -> instance (ressortansvar), active ministries only.
    ov_edges = [
        e for e in edges
        if e["type"] == "ressortansvar"
        and nodes[e["from"]]["type"] == "ministerium"
        and is_instance(nodes[e["to"]])
    ]
    ov_ids = {e["from"] for e in ov_edges} | {e["to"] for e in ov_edges}
    ov_nodes = [n for n in ministries if n["id"] in ov_ids] + sorted(
        (nodes[i] for i in ov_ids if nodes[i]["type"] != "ministerium"), key=lambda n: n["navn"]
    )
    body = [
        "# Overblik: ministerium → instans",
        "",
        legend,
        mermaid(ov_nodes, ov_edges),
        "",
        "## Ministerområder",
        "",
    ]
    for m in ministries:
        body.append(f"- [{m['navn']}]({m['id']}.md)")
    out[DIAGRAM_DIR / "oversigt.md"] = "\n".join(body) + "\n"

    # One diagram per ministry: its instances, the acts it is responsible for,
    # what those instances issue, appeal/supervision edges touching them, and the
    # EU acts its acts implement.
    for m in ministries:
        area = {m["id"]}
        area |= {e["to"] for e in edges if e["from"] == m["id"] and e["type"] in ("ressortansvar", "delegation")}
        area |= {n["id"] for n in nodes.values() if n.get("ministerium") == m["id"]}
        core = set(area)
        sel = [
            e for e in edges
            if (e["from"] in core or e["to"] in core)
            and not (e["type"] == "ressortansvar" and nodes[e["from"]]["type"] == "ministerium" and e["from"] != m["id"])
        ]
        # Second hop only for hjemmel/implementering, so chains lov -> bek -> EU stay visible.
        hop = {e["to"] for e in sel if e["type"] in ("hjemmel_for", "udsteder")}
        sel += [
            e for e in edges
            if e["from"] in hop and e["type"] in ("implementerer_EU", "hjemmel_for") and e not in sel
        ]
        ids = {m["id"]} | {e["from"] for e in sel} | {e["to"] for e in sel}
        sel_nodes = sorted((nodes[i] for i in ids), key=lambda n: (n["id"] != m["id"], node_class(n), n["navn"]))
        body = [
            f"# {m['navn']}",
            "",
            legend,
            f"Noder: {len(sel_nodes)} · kanter: {len(sel)}",
            "",
            mermaid(sel_nodes, sel),
            "",
            "[← Overblik](oversigt.md)",
        ]
        out[DIAGRAM_DIR / f"{m['id']}.md"] = "\n".join(body) + "\n"
    return out


# ---------------------------------------------------------------- tables


def md_cell(text) -> str:
    return str(text if text is not None else "").replace("|", "\\|").replace("\n", " ")


def priority(n: dict) -> float:
    ing = n["ingest"]
    return round(ing["vaerdi"] / ing["besvaer"], 2)


SOURCE_TYPES = {"dokumentkilde", "praksissamling"}


def source_rows(rows: list[dict]) -> list[str]:
    rows = sorted(rows, key=lambda n: (-priority(n), -n["ingest"]["vaerdi"], n["navn"]))
    out = [
        "| # | Kilde | Id | Værdi | Besvær | Prioritet | Adgang | Licens | Sikkerhed (adgang) | Begrundelse |",
        "|---|-------|----|------:|-------:|----------:|--------|--------|--------------------|-------------|",
    ]
    for i, n in enumerate(rows, 1):
        url = n["url"]["vaerdi"]
        name = f"[{md_cell(n['navn'])}]({url})" if url and url not in NO_URL else md_cell(n["navn"])
        out.append(
            "| {} | {} | `{}` | {} | {} | {} | {} | {} | {} | {} |".format(
                i, name, n["id"], n["ingest"]["vaerdi"], n["ingest"]["besvaer"], priority(n),
                ", ".join(n["adgang"].get("vaerdier") or []), md_cell(n["licens"].get("tekst")),
                n["adgang"]["sikkerhed"], md_cell(n["ingest"].get("begrundelse")),
            )
        )
    return out


def gen_sources(reg: dict) -> str:
    date = reg["meta"]["dato"]
    rated = [n for n in reg["nodes"] if n.get("ingest")]
    portals = [n for n in rated if n["type"] in SOURCE_TYPES]
    issuers = [n for n in rated if n["type"] in INSTANCE_TYPES]
    acts = [n for n in rated if n["type"] not in SOURCE_TYPES | INSTANCE_TYPES]
    lines = [
        "# Datakilder efter ingest-prioritet",
        "",
        f"> Genereret af `scripts/build.py` fra `registry.yaml` (dato {date}). Redigér ikke i hånden.",
        "> Prioritet = værdi ÷ besvær (begge 1-5), højest først. Værdi = nytte for RAG/hjemmelskæder;",
        "> besvær = teknisk/juridisk vanskelighed (1 = API/bulk med åben licens, 5 = betalingsmur/scannede PDF'er).",
        "> Sikkerhed gælder adgangsoplysningen.",
        "",
        f"## 1. Portaler, databaser og praksissamlinger ({len(portals)})",
        "",
        *source_rows(portals),
        "",
        f"## 2. Udstedende instanser (egne hjemmesider/publikationer) ({len(issuers)})",
        "",
        *source_rows(issuers),
        "",
        f"## 3. Retsakter, vejledningssamlinger, planer og standarder ({len(acts)})",
        "",
        *source_rows(acts),
    ]
    return "\n".join(lines) + "\n"


def gen_gaps(reg: dict) -> str:
    date = reg["meta"]["dato"]
    nodes = reg["nodes"]
    by_type: dict[str, list[dict]] = defaultdict(list)
    for h in reg["huller"]:
        by_type[h["type"]].append(h)
    lines = [
        "# Huller og usikkerheder",
        "",
        f"> Genereret af `scripts/build.py` fra `registry.yaml` (dato {date}). Redigér ikke i hånden.",
        "",
        "## Registrerede huller",
        "",
    ]
    titles = {
        "betalingsmur": "Betalingsmur / ophavsret",
        "kun-pdf": "Kun PDF (ingen struktureret tekst)",
        "ingen-api": "Ingen API eller bulk-adgang",
        "uklart": "Uklart (ressort, hjemmel, status)",
        "ikke-fundet": "Ikke fundet",
        "andet": "Andet",
    }
    for t in titles:
        if t not in by_type:
            continue
        lines += [f"### {titles[t]} ({len(by_type[t])})", ""]
        for h in by_type[t]:
            refs = ", ".join(f"`{x}`" for x in h.get("noder", []) or [])
            src = " ".join(f"[kilde]({k})" for k in h.get("kilder", []) or [])
            dom = ", ".join(h.get("domaener") or [])
            lines.append(
                f"- **{md_cell(h['emne'])}** – {md_cell(h['beskrivelse'])}"
                + (f" Noder: {refs}." if refs else "")
                + (f" Domæner: {dom}." if dom else "")
                + (f" {src}" if src else "")
            )
        lines.append("")

    paywalled = [n for n in nodes if "betalingsmur" in (n["adgang"].get("vaerdier") or [])]
    pdf_only = [
        n for n in nodes
        if (v := set(n["adgang"].get("vaerdier") or [])) and "PDF" in v and not v & {"API", "bulk", "ELI", "HTML"}
    ]
    no_url = [n for n in nodes if n["url"].get("vaerdi") in (None, NOT_FOUND) and n.get("status") == "aktiv"]
    lines += ["## Afledt af registry'et", ""]
    for title, group in (
        ("Noder med betalingsmur", paywalled),
        ("Noder der kun findes som PDF", pdf_only),
        ("Aktive noder uden fundet kanonisk URL", no_url),
    ):
        lines += [f"### {title} ({len(group)})", ""]
        lines += [f"- `{n['id']}` – {md_cell(n['navn'])}" for n in sorted(group, key=lambda n: n["id"])] or ["- (ingen)"]
        lines.append("")

    counts: dict[str, int] = defaultdict(int)
    unknown: list[str] = []
    for n in nodes:
        for f in CLAIM_FIELDS:
            s = n[f]["sikkerhed"]
            counts[s] += 1
            if s == "ukendt" and f in ("hjemmel", "url", "adgang"):
                unknown.append(f"`{n['id']}`.{f}")
    for e in reg["edges"]:
        counts[e["sikkerhed"]] += 1
    lines += [
        "## Sikkerhedsfordeling (node-felter + kanter)",
        "",
        "| Sikkerhed | Antal |",
        "|-----------|------:|",
        *[f"| {s} | {counts[s]} |" for s in ("verificeret", "sandsynlig", "ukendt")],
        "",
        f"### Ukendt hjemmel/URL/adgang ({len(unknown)})",
        "",
        ", ".join(unknown) if unknown else "(ingen)",
        "",
    ]
    return "\n".join(lines)


def outputs(reg: dict, kat: dict | None = None) -> dict[Path, str]:
    out = gen_diagrams(reg)
    out[ROOT / "datakilder.md"] = gen_sources(reg)
    out[ROOT / "huller.md"] = gen_gaps(reg)
    if kat is not None:
        out[KATALOG_DIR / "README.md"] = gen_katalog(reg, kat)
    return out


def selftest() -> None:
    reg = {"nodes": [{"id": "naevn-x", "type": "nævn"}]}
    doc = lambda i: {"id": i, "type": "lov", "kilder": [], "status": {"vaerdi": "gældende", "sikkerhed": "sandsynlig"}}
    kant = {"from": "naevn-x", "type": "klageinstans", "to": "lta-2016-1178", "kilder": [], "sikkerhed": "sandsynlig"}
    kat = lambda **e: {"docs": [doc("lta-2016-1178"), doc("lta-2018-734")], "edges": [{**kant, **e}], "eu": [], "tekst": []}
    assert validate_katalog(reg, kat()) == [] and validate_katalog(reg, kat(senere_aendret_ved=["lta-2018-734"])) == []
    for galt in ("lta-2018-734", [], ["lta-2099-1"], [["lta-2018-734"]]):
        fejl = validate_katalog(reg, kat(senere_aendret_ved=galt))
        assert len(fejl) == 1 and "senere_aendret_ved" in fejl[0], (galt, fejl)
    af = {"vaerdi": "lta-2018-734", "ophaevelse": "Lov nr. 1178 af 25. september 2016 ophæves.", "paragraf": "§ 9", "paragraf_tekst": "§ 9. Lov nr. 1178 af 25. september 2016 ophæves.",
          "kilder": ["https://www.retsinformation.dk/eli/lta/2018/734/xml"], "sikkerhed": "verificeret", "metode": "ophaevelsesbestemmelse", "bevarer_regler": None}
    med = lambda **f: {**kat(), "docs": [{**doc("lta-2016-1178"), **f}, doc("lta-2018-734")]}
    assert validate_katalog(reg, med(afloeser=af, afloeser_fra="lta-2016-1178", gaeldende_version="lta-2018-734")) == []
    for galt in ({**af, "vaerdi": "lta-2099-1"}, {**af, "sikkerhed": "sandsynlig"}, {**af, "kilder": []}, {**af, "ophaevelse": "Lov nr. 1178 ophæves."}, {**af, "bevarer_regler": 1}):
        fejl = validate_katalog(reg, med(afloeser=galt))
        assert len(fejl) == 1 and "afloeser" in fejl[0], (galt, fejl)
    assert len(validate_katalog(reg, med(afloeser_fra="lta-2099-1"))) == 1
    print("selftest ok")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="fail if generated files differ from registry.yaml")
    ap.add_argument("--selftest", action="store_true", help="run the self-checks and exit")
    args = ap.parse_args()
    if args.selftest:
        selftest()
        return 0

    reg = load()
    kat = load_katalog()
    errors = validate(reg)
    if kat is not None:
        errors += validate_katalog(reg, kat)
    if errors:
        print(f"registry.yaml: {len(errors)} fejl", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    expected = outputs(reg, kat)
    stale_diagrams = {p for p in DIAGRAM_DIR.glob("*.md")} - set(expected)
    if args.check:
        stale = [p for p, text in expected.items() if not p.exists() or p.read_text(encoding="utf-8") != text]
        stale += sorted(stale_diagrams)
        if stale:
            print("Forældede genererede filer (kør build.py):", file=sys.stderr)
            for p in stale:
                print(f"  - {p.relative_to(ROOT)}", file=sys.stderr)
            return 1
        ks = f", katalog: {len(kat['docs'])} dokumenter/{len(kat['edges'])} kanter" if kat else ""
        print(f"OK: {len(reg['nodes'])} noder, {len(reg['edges'])} kanter{ks}, {len(expected)} genererede filer er aktuelle")
        return 0

    DIAGRAM_DIR.mkdir(exist_ok=True)
    for p in stale_diagrams:
        p.unlink()
    for p, text in expected.items():
        p.write_text(text, encoding="utf-8")
    print(f"OK: {len(reg['nodes'])} noder, {len(reg['edges'])} kanter → {len(expected)} filer skrevet")
    return 0


if __name__ == "__main__":
    sys.exit(main())
