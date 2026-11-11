#!/usr/bin/env python3
"""Fase 7: flet agent-fund ind i registry.yaml med maskinel citatkontrol.

    python3 populate.py check FUND.json      # skematjek uden netværk og uden PyYAML (agenter kører det selv)
    python3 populate.py hosts FUND.json...   # værter der skal kunne nås af apply
    python3 populate.py review FUND.json     # påstand/citat-par til en uafhængig kontrollant, som skriver FUND.dom.json
    python3 populate.py apply FUND.json...   # hent kilder, tjek citater, flet, skriv registry.yaml + FUND.kontrol.json
    python3 populate.py selftest

En agent leverer noder, kanter og rettelser med belaeg: [{url, citat}]. Sikkerheden sættes her, ikke af agenten:
verificeret = citatet er genfundet på en officiel side eller på to uafhængige sekundære sider (for url: på selve siden),
eller feltet er læst direkte af Retsinformations metadata (nummer, dato, titel og status for love og bekendtgørelser),
sandsynlig = der er belæg, men det er ikke genfundet maskinelt eller kun på én sekundær side,
ukendt = intet belæg, eller alle kilder er døde.
Findes FUND.dom.json ([{hvor, dom, grund}] med dom baerer | delvist | baerer-ikke), sænker delvist til højst sandsynlig
og baerer-ikke til ukendt. Kør scripts/build.py bagefter.
"""
from __future__ import annotations

import copy
import datetime
import hashlib
import html
import http.client
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import types
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

try:
    import yaml
except ModuleNotFoundError:
    yaml = None
    sys.modules["yaml"] = types.ModuleType("yaml")

ROOT = Path(__file__).resolve().parents[1]
REG = ROOT / "dk-regulering" / "registry.yaml"
_spec = importlib.util.spec_from_file_location("build", REG.parent / "scripts" / "build.py")
B = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(B)

HUL_TYPES = {"betalingsmur", "kun-pdf", "ingen-api", "uklart", "ikke-fundet", "andet"}
VALUE_KEYS = {
    "hjemmel": ("tekst",), "dokumenttyper": ("liste",), "url": ("vaerdi",), "adgang": ("vaerdier", "note"),
    "identifikatorer": ("eli", "lovtidende", "celex", "journalnr", "andet"), "licens": ("tekst",),
    "opdatering": ("frekvens", "versionshistorik"),
}
EMPTY = {
    "hjemmel": {"tekst": "ikke undersøgt"}, "dokumenttyper": {"liste": []}, "url": {"vaerdi": B.NOT_FOUND},
    "adgang": {"vaerdier": ["ukendt"]}, "identifikatorer": {}, "licens": {"tekst": "ikke undersøgt"},
    "opdatering": {"frekvens": "ukendt", "versionshistorik": "ukendt"},
}
RULES = {"adgang": "retsinformation-adgang", "licens": "ophavsret-9-forskrifter", "opdatering": "retsinformation-opdatering"}
RI_TYPES = {"lov", "bekendtgørelse", "cirkulære", "vejledning"}
DOC_KINDS = {"Lov": "LOV", "Lovbekendtgørelse": "LBK", "Bekendtgørelse": "BEK", "Anordning": "AND", "Cirkulære": "CIR", "Vejledning": "VEJ"}
PUBLIC = B.INSTANCE_TYPES - {"privat-organisation", "standardiseringsorgan"}
ENDS = {
    "ressortansvar": ({"ministerium"}, None), "delegation": (B.INSTANCE_TYPES, B.INSTANCE_TYPES), "hjemmel_for": (B.DOCUMENT_TYPES, None),
    "udsteder": (B.INSTANCE_TYPES, B.DOCUMENT_TYPES), "klageinstans": (B.INSTANCE_TYPES, B.INSTANCE_TYPES), "tilsyn": (B.INSTANCE_TYPES, None),
    "implementerer_EU": (B.DOCUMENT_TYPES, B.DOCUMENT_TYPES), "henviser_til": (B.DOCUMENT_TYPES, B.DOCUMENT_TYPES),
}
PRIMARY = {"retsinformation.dk", "lovtidende.dk", "ft.dk", "europa.eu", "domstol.dk", "stm.dk", "regeringen.dk"}
SECONDARY = {"lovguiden.dk", "lex.dk", "wikipedia.org", "danskelove.dk", "jurabibliotek.dk", "jurabibliotek.ai", "themis.dk"}
FASE7 = ("Fase 7 (fra 2026-11-11): Instanslag uden for de otte domæner. Én research-agent pr. retsområde leverer noder og kanter med kilde-URL "
         "og ordret citat for hver påstand (pipeline/populate-brief.md). pipeline/populate.py henter selv hver kilde og leder efter citatet, læser "
         "nummer, dato, titel og status for love og bekendtgørelser direkte i Retsinformations metadata, og en uafhængig kontrollant bedømmer, om "
         "citatet bærer påstanden. For disse påstande betyder verificeret: citatet er genfundet på en officiel side og godkendt af kontrollanten, "
         "eller feltet er læst af Retsinformations metadata. Ellers sandsynlig. Rå fund, domme og kontroljournaler ligger i raw/populate/.")
UA = "Mozilla/5.0 (compatible; registry-citatkontrol)"
CACHE = Path(os.environ.get("TMPDIR", "/tmp")) / "legoleze-citatkontrol"
OK = 0.6


def site(url: str) -> str:
    return ".".join((urllib.parse.urlsplit(url).hostname or "").split(".")[-2:])


def index(reg) -> tuple[dict, set]:
    """({id: type}, {(from, type, to)}) fra registry'et, enten indlæst eller som rå YAML-tekst."""
    if isinstance(reg, dict):
        return {n["id"]: n["type"] for n in reg["nodes"]}, {(e["from"], e["type"], e["to"]) for e in reg["edges"]}
    ids, cur = {}, None
    for line in reg.splitlines():
        if line.startswith("- id: "):
            cur = line[6:].strip()
        elif cur and line.startswith("  type: "):
            ids[cur], cur = line[8:].strip(), None
    return ids, {(f, t, to) for t, f, to in re.findall(r"^- type: (\S+)\n  from: (\S+)\n  to: (\S+)$", reg, re.MULTILINE)}



def _belaeg(where: str, b, err) -> None:
    if not isinstance(b, list) or not b:
        return err(f"{where}: belaeg mangler (udelad feltet, hvis du ikke har belæg)")
    for x in b:
        if not isinstance(x, dict) or not B.URL_RE.match(str(x.get("url"))):
            err(f"{where}: belaeg uden gyldig url")
        elif not 20 <= len(str(x.get("citat", ""))) <= 600:
            err(f"{where}: citat skal være 20-600 tegn, ordret fra siden")


def _claim(where: str, c: str, val, err) -> None:
    if not isinstance(val, dict):
        return err(f"{where}: skal være et objekt")
    extra = set(val) - set(VALUE_KEYS[c]) - {"belaeg", "id", "felt"}
    if extra:
        err(f"{where}: ukendte nøgler {sorted(extra)}")
    _belaeg(where, val.get("belaeg"), err)
    if c == "url" and val.get("vaerdi") not in B.NO_URL and not B.URL_RE.match(str(val.get("vaerdi"))):
        err(f"{where}.vaerdi: ikke en URL")
    for a in val.get("vaerdier", []) if c == "adgang" else []:
        if a not in B.ACCESS:
            err(f"{where}: ukendt værdi {a!r}; tilladt: {sorted(B.ACCESS)}")
    for d in val.get("liste", []) if c == "dokumenttyper" else []:
        if not d.get("type") or d.get("bindende") not in B.BINDING:
            err(f"{where}: hver post skal have type og bindende i {sorted(B.BINDING)}")


def check(f: dict, ids: dict, edges: set) -> list[str]:
    errs: list[str] = []
    err = errs.append
    if not isinstance(f.get("omraade"), str):
        err("omraade mangler")
    new: dict[str, str] = {}
    mins: dict[str, str] = {}
    for n in f.get("noder", []):
        nid = str(n.get("id"))
        if not B.ID_RE.match(nid):
            err(f"{nid}: ugyldigt id (små bogstaver, cifre, bindestreger)")
        elif nid in ids or nid in new:
            err(f"{nid}: findes allerede – brug den eksisterende node i kanter, og skriv ændringsforslag i noter")
        new[nid] = n.get("type")
        if n.get("type") not in B.NODE_TYPES:
            err(f"{nid}: ukendt type {n.get('type')!r}")
        if n.get("status") not in B.STATUS:
            err(f"{nid}: ukendt status {n.get('status')!r}")
        if not n.get("navn"):
            err(f"{nid}: navn mangler")
        m = mins[nid] = n.get("ministerium")
        if m != "ingen" and ids.get(m) != "ministerium":
            err(f"{nid}: ministerium {m!r} er hverken et eksisterende ministerie-id eller 'ingen'")
        if not any(c in n for c in B.CLAIM_FIELDS):
            err(f"{nid}: ingen påstandsfelter")
        for c in B.CLAIM_FIELDS:
            if c in n:
                _claim(f"{nid}.{c}", c, n[c], err)
        for p in n.get("tidligere_navne", []):
            if not p.get("navn"):
                err(f"{nid}.tidligere_navne: post uden navn")
            _belaeg(f"{nid}.tidligere_navne[{p.get('navn')}]", p.get("belaeg"), err)
        ing = n.get("ingest")
        if ing is not None and not all(isinstance(ing.get(k), int) and 1 <= ing[k] <= 5 for k in ("vaerdi", "besvaer")):
            err(f"{nid}.ingest: vaerdi og besvaer skal være heltal 1-5")

    known = {**ids, **new}
    seen = set(edges)
    linked = set()
    for e in f.get("kanter", []):
        key = (e.get("from"), e.get("type"), e.get("to"))
        lab = "|".join(map(str, key))
        if e.get("type") not in B.EDGE_TYPES:
            err(f"kant {lab}: ukendt kanttype; tilladt: {sorted(B.EDGE_TYPES)}")
        for end in ("from", "to"):
            if e.get(end) not in known:
                err(f"kant {lab}: {end}-node findes ikke")
        if key in seen:
            err(f"kant {lab}: findes allerede")
        seen.add(key)
        linked.update(key)
        for end, allowed in zip(("from", "to"), ENDS.get(e.get("type"), (None, None))):
            if allowed and known.get(e.get(end)) not in allowed | {None}:
                kind = "ministerium" if allowed == {"ministerium"} else "instans" if allowed == B.INSTANCE_TYPES else "dokument"
                err(f"kant {lab}: {end} skal være {kind}, men {e.get(end)} er {known.get(e.get(end))}")
        if not e.get("beskrivelse"):
            err(f"kant {lab}: beskrivelse mangler")
        _belaeg(f"kant {lab}", e.get("belaeg"), err)
    for nid, typ in new.items():
        if nid not in linked:
            err(f"{nid}: noden har ingen kanter")
        if (typ in PUBLIC or typ == "lov") and mins[nid] != "ingen" and (mins[nid], "ressortansvar", nid) not in seen:
            err(f"{nid}: mangler kanten {mins[nid]}|ressortansvar|{nid} med belæg")

    for r in f.get("rettelser", []):
        where = f"rettelse {r.get('id')}.{r.get('felt')}"
        if r.get("id") not in ids:
            err(f"{where}: noden findes ikke")
        if r.get("felt") not in B.CLAIM_FIELDS:
            err(f"{where}: felt skal være et af {list(B.CLAIM_FIELDS)}")
        else:
            _claim(where, r["felt"], r, err)

    for i, h in enumerate(f.get("huller", [])):
        if not h.get("emne") or not h.get("beskrivelse") or h.get("type") not in HUL_TYPES:
            err(f"huller[{i}]: kræver emne, beskrivelse og type i {sorted(HUL_TYPES)}")
        for nid in h.get("noder", []):
            if nid not in known:
                err(f"huller[{i}]: node {nid!r} findes ikke")
    return errs


_last: dict[str, float] = {}


def get(url: str) -> tuple[str, bytes]:
    """(status, indhold): ok | død (404/410) | ukendt (botmur, timeout)."""
    p = urllib.parse.urlsplit(url)
    target = url
    if site(url) == "retsinformation.dk" and p.path.startswith("/eli/"):
        target = "https://www.retsinformation.dk" + re.sub(r"/(pdf|xml|html)$", "", p.path.rstrip("/")) + "/xml"
    CACHE.mkdir(parents=True, exist_ok=True)
    cache = CACHE / (hashlib.sha1(target.encode()).hexdigest() + ".raw")
    if cache.exists():
        return "ok", cache.read_bytes()
    wait = _last.get(site(url), 0) + (10.5 if site(url) == "retsinformation.dk" else 2) - time.time()
    if wait > 0:
        time.sleep(wait)
    try:
        req = urllib.request.Request(urllib.parse.quote(target, safe=":/?&=%#@+,;~()!*'[]$"), headers={"User-Agent": UA, "Accept-Language": "da"})
        with urllib.request.urlopen(req, timeout=45) as r:
            raw = r.read(30_000_000)
    except urllib.error.HTTPError as ex:
        return ("død" if ex.code in (404, 410) else "ukendt"), f"HTTP {ex.code}".encode()
    except (OSError, http.client.HTTPException, ValueError) as ex:
        return "ukendt", str(ex)[:120].encode()
    finally:
        _last[site(url)] = time.time()
    cache.write_bytes(raw)
    return "ok", raw


def fetch(url: str) -> tuple[str, str]:
    """(status, tekst) som get, med siden som ren tekst; en tom side er ukendt."""
    status, raw = get(url)
    if status != "ok":
        return status, raw.decode()
    if raw[:5] == b"%PDF-":
        text = subprocess.run(["pdftotext", "-", "-"], input=raw, capture_output=True, check=False).stdout.decode("utf-8", "replace")
    else:
        try:
            page = raw.decode("utf-8")
        except UnicodeDecodeError:
            page = raw.decode("latin-1")
        text = html.unescape(re.sub(r"(?s)<(script|style)\b.*?</\1>|<[^>]+>", " ", page))
    return ("ok", text) if text.strip() else ("ukendt", "tom side")


def ri_meta(url: str) -> dict:
    """Retsinformations egne metadata for et ELI-dokument; tom, hvis de ikke kan læses eller ikke passer til adressen."""
    status, raw = get(url)
    block = re.search(rb"(?s)<Meta\b.*?</Meta>", raw) if status == "ok" else None
    fields = "DocumentType|Year|Number|DiesSigni|DocumentTitle|PopularTitle|Status|DateOfHistoricMark"
    m = dict(re.findall(rf"<({fields})>([^<]*)<", block.group(0).decode("utf-8", "replace"))) if block else {}
    path = re.sub(r"/(pdf|xml|html)$", "", urllib.parse.urlsplit(url).path.rstrip("/"))
    return m if m.get("DiesSigni") and path.endswith(f"/{m.get('Year')}/{m.get('Number')}") else {}


def norm(s: str) -> str:
    return " ".join(re.sub(r"[\W_]+", " ", html.unescape(s).replace("\N{SOFT HYPHEN}", "").casefold()).split())


def quoted(citat: str, text: str) -> float:
    """Andel af citatets 5-ords-vinduer, der står på siden (1.0 = ordret)."""
    w, t = norm(citat).split(), f" {norm(text)} "
    sh = [" ".join(w[i:i + 5]) for i in range(max(1, len(w) - 4))]
    return sum(f" {s} " in t for s in sh) / len(sh)


def certainty(belaeg: list, primary: set, pages: dict, must: str = "") -> tuple[str, list, list]:
    """(sikkerhed, kilder, kontrol) for én påstand; døde kilder udgår. must: det domæne, citatet skal stå på."""
    res = []
    for b in belaeg or []:
        status, text = pages[b["url"]]
        res.append({"url": b["url"], "status": status, "andel": round(quoted(b["citat"], text), 2) if status == "ok" else None})
    ok = [r["url"] for r in res if (r["andel"] or 0) >= OK]
    alive = [r["url"] for r in res if r["status"] != "død"]
    sites = {site(u) for u in ok}
    if must in sites if must else sites & primary or len(sites) >= 2:
        s = "verificeret"
    else:
        s = "sandsynlig" if alive else "ukendt"
    return s, list(dict.fromkeys(ok + alive)), res


def review(f: dict) -> list[dict]:
    """Hver påstand som {hvor, paastand, belaeg}; hvor er samme nøgle som i kontroljournalen."""
    names = {n["id"]: n["navn"] for n in f.get("noder", [])}
    out = []
    for n in f.get("noder", []):
        head = f"{n['navn']} ({n['type']}, ministerium {n['ministerium']})"
        for p in n.get("tidligere_navne", []):
            out.append({"hvor": f"{n['id']}.tidligere_navne[{p['navn']}]", "paastand": f"{head} hed tidligere {p['navn']} ({p.get('periode')})", "belaeg": p["belaeg"]})
        for c in B.CLAIM_FIELDS:
            if c in n:
                val = json.dumps({k: v for k, v in n[c].items() if k != "belaeg"}, ensure_ascii=False)
                out.append({"hvor": f"{n['id']}.{c}", "paastand": f"{head}: {c} = {val}", "belaeg": n[c]["belaeg"]})
    for e in f.get("kanter", []):
        out.append({"hvor": "kant " + "|".join((e["from"], e["type"], e["to"])), "belaeg": e["belaeg"],
                    "paastand": f"{names.get(e['from'], e['from'])} —{e['type']}→ {names.get(e['to'], e['to'])}: {e['beskrivelse']}"})
    for r in f.get("rettelser", []):
        val = json.dumps({k: v for k, v in r.items() if k not in ("belaeg", "id", "felt")}, ensure_ascii=False)
        out.append({"hvor": f"rettelse {r['id']}.{r['felt']}", "paastand": f"{r['id']}: {r['felt']} = {val}", "belaeg": r["belaeg"]})
    return out


def merge(f: dict, reg: dict, pages: dict, primary: set, dom: dict | None = None) -> list:
    """Føj fundets noder, kanter, rettelser og huller til reg; returnér kontroljournalen."""
    journal = []
    omr = f["omraade"]
    cap = {"delvist": "sandsynlig", "baerer-ikke": "ukendt"}

    own = {n["id"]: site(str((n.get("url") or {}).get("vaerdi"))) for n in reg["nodes"] + f.get("noder", [])}

    def claim(where: str, val: dict, *about: str, felt: str = "") -> dict:
        prim = (primary | {own.get(a, "") for a in about}) - SECONDARY - {""}
        s, kilder, res = certainty(val.get("belaeg"), prim, pages, site(str(val.get("vaerdi"))) if felt == "url" else "")
        verdict = (dom or {}).get(where)
        if verdict in cap and (s == "verificeret" or verdict == "baerer-ikke"):
            s = cap[verdict]
        journal.append({"hvor": where, "sikkerhed": s, "dom": verdict, "belaeg": res})
        return {**{k: v for k, v in val.items() if k not in ("belaeg", "id", "felt")}, "kilder": kilder, "sikkerhed": s}

    def rule(field: str, name: str) -> dict:
        return next(copy.deepcopy(n[field]) for n in reg["nodes"] if n[field].get("regel") == name)

    def from_meta(nid: str, felt: str, val: dict, meta: dict, agent) -> dict:
        journal.append({"hvor": f"{nid}.{felt}", "sikkerhed": "verificeret", "dom": None, "metadata": meta, "agent": agent, "belaeg": []})
        return {**val, "kilder": [own_url[nid]], "sikkerhed": "verificeret"}

    own_url = {}
    for n in f.get("noder", []):
        nid = n["id"]
        own_url[nid] = str((n.get("url") or {}).get("vaerdi"))
        on_ri = n["type"] in RI_TYPES and site(own_url[nid]) == "retsinformation.dk"
        meta = ri_meta(own_url[nid]) if on_ri else {}
        name = set(norm(n["navn"]).split())
        titles = [set(norm(meta.get(k, "")).split()) - {"bekendtgørelse", "af"} for k in ("PopularTitle", "DocumentTitle")]
        named = any(t and len(t & name) >= 0.8 * min(len(t), len(name)) for t in titles)
        out = {
            "id": nid, "navn": n["navn"], "type": n["type"], "ministerium": n["ministerium"], "status": n["status"],
            "domaener": list(dict.fromkeys([omr] + n.get("domaener", []))),
            "tidligere_navne": [
                {"navn": p["navn"], "periode": p.get("periode", "ukendt"), "efterfoelger": nid,
                 **claim(f"{nid}.tidligere_navne[{p['navn']}]", {"belaeg": p["belaeg"]}, nid)}
                for p in n.get("tidligere_navne", [])
            ],
        }
        for c in B.CLAIM_FIELDS:
            if meta and c == "identifikatorer":
                y, mo, d = meta["DiesSigni"].split("-")
                kind = meta["DocumentType"].split()[0]
                ids = {"eli": own_url[nid], "lovtidende": f"{DOC_KINDS.get(kind, kind)} nr. {meta['Number']} af {d}/{mo}/{y}"}
                given = {k: v for k, v in n.get(c, {}).items() if k != "belaeg"}
                ids.update({k: v for k, v in given.items() if k not in ids})
                if meta.get("Status") == "Historic":
                    ids["katalog_note"] = (f"Retsinformation markerer denne version som historisk ({meta.get('DateOfHistoricMark', 'dato ukendt')}); "
                                           f"den gældende afløser er ikke identificeret (kontrolleret {datetime.date.today()}).")
                out[c] = from_meta(nid, c, ids, meta, given)
            elif meta and named and c == "url":
                out[c] = from_meta(nid, c, {"vaerdi": own_url[nid]}, meta, None)
            elif meta and c == "hjemmel" and n.get(c, {}).get("tekst") == "ikke relevant":
                out[c] = from_meta(nid, c, {"tekst": "ikke relevant"}, meta, None)
            elif c in n:
                out[c] = claim(f"{nid}.{c}", n[c], nid, felt=c)
            elif on_ri and c in RULES:
                out[c] = rule(c, RULES[c] + ("-vejledninger" if n["type"] == "vejledning" else ""))
            elif c == "licens" and n["type"] in B.INSTANCE_TYPES:
                out[c] = {"tekst": "ikke relevant (instans)", "kilder": [], "sikkerhed": "sandsynlig"}
            else:
                out[c] = {**copy.deepcopy(EMPTY[c]), "kilder": [], "sikkerhed": "ukendt"}
        out["krydsref_moenstre"] = n.get("krydsref_moenstre", [])
        if "ingest" in n:
            out["ingest"] = n["ingest"]
        out["note"] = n.get("note", "")
        reg["nodes"].append(out)
    for e in f.get("kanter", []):
        c = claim("kant " + "|".join((e["from"], e["type"], e["to"])), e, e["from"], e["to"])
        reg["edges"].append({"type": e["type"], "from": e["from"], "to": e["to"], "beskrivelse": e["beskrivelse"],
                             "kilder": c["kilder"], "sikkerhed": c["sikkerhed"], "domaener": [omr]})
    rank = ["ukendt", "sandsynlig", "verificeret"]
    for r in f.get("rettelser", []):
        node = next(n for n in reg["nodes"] if n["id"] == r["id"])
        if r["felt"] == "url":
            own[r["id"]] = site(str(r.get("vaerdi")))
        old, new = node[r["felt"]], claim(f"rettelse {r['id']}.{r['felt']}", r, r["id"], felt=r["felt"])
        if rank.index(new["sikkerhed"]) < rank.index(old["sikkerhed"]):
            journal[-1]["afvist"] = f"ny sikkerhed {new['sikkerhed']} er lavere end den eksisterende {old['sikkerhed']}"
            continue
        vals = {k: v for k, v in new.items() if k not in ("kilder", "sikkerhed")}
        same = all(old.get(k) == v for k, v in vals.items())
        node[r["felt"]] = {**old, **new, "kilder": list(dict.fromkeys(new["kilder"] + (old["kilder"] if same else [])))}
    for h in f.get("huller", []):
        reg["huller"].append({"emne": h["emne"], "type": h["type"], "beskrivelse": h["beskrivelse"], "noder": h.get("noder", []),
                              "kilder": [k for k in h.get("kilder", []) if B.URL_RE.match(str(k))], "domaener": [omr],
                              "oprindelige_emner": [h["emne"]]})
    return journal


def urls(f: dict) -> list[str]:
    out = []

    def walk(x):
        if isinstance(x, dict):
            out.extend(b["url"] for b in x.get("belaeg") or [] if isinstance(b, dict) and "url" in b)
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)

    walk(f)
    return list(dict.fromkeys(out))


class Dumper(yaml.SafeDumper if yaml else object):
    pass


def apply(paths: list[str]) -> int:
    Dumper.add_representer(str, lambda d, s: d.represent_scalar("tag:yaml.org,2002:str", s, style="|" if "\n" in s else None))
    raw = REG.read_text(encoding="utf-8")
    reg = yaml.load(raw, Loader=yaml.CSafeLoader)
    bad = merged = 0
    for path in paths:
        f = json.loads(Path(path).read_text(encoding="utf-8"))
        errs = check(f, *index(reg))
        if errs:
            print(f"{path}: {len(errs)} skemafejl, ikke flettet", *errs[:40], sep="\n  ")
            bad += 1
            continue
        pages = {}
        for i, u in enumerate(us := urls(f), 1):
            pages[u] = fetch(u)
            print(f"\r  henter {i}/{len(us)}", end="", file=sys.stderr)
        public = [n for n in reg["nodes"] + f.get("noder", [])
                  if n["type"] in PUBLIC or n["type"] in ("dokumentkilde", "praksissamling") and n["ministerium"] != "ingen"]
        own = {site(str((n.get("url") or {}).get("vaerdi"))) for n in public} - {""}
        primary = (PRIMARY | own) - SECONDARY
        domfile = Path(path).with_suffix(".dom.json")
        dom = {d["hvor"]: d["dom"] for d in json.loads(domfile.read_text(encoding="utf-8"))} if domfile.exists() else None
        journal = merge(f, reg, pages, primary, dom)
        merged += 1
        Path(path).with_suffix(".kontrol.json").write_text(json.dumps(journal, ensure_ascii=False, indent=1), encoding="utf-8")
        tal = {s: sum(j["sikkerhed"] == s for j in journal) for s in sorted(B.CERTAINTY)}
        used = {site(b["url"]) for j in journal for b in j["belaeg"]}
        print(f"\n{path}: {len(f.get('noder', []))} noder, {len(f.get('kanter', []))} kanter, {len(f.get('rettelser', []))} rettelser, {len(f.get('huller', []))} huller; påstande {tal}")
        print(*(f"  afvist {j['hvor']}: {j['afvist']}" for j in journal if "afvist" in j), sep="\n", end="")
        print(f"  kontrollant: {'ingen dom-fil' if dom is None else {v: sum(j['dom'] == v for j in journal) for v in ('baerer', 'delvist', 'baerer-ikke', None)}}")
        print("  primære domæner brugt:", sorted(used & primary), "\n  øvrige:", sorted(used - primary))
        for j in journal:
            for b in j["belaeg"]:
                if (b["andel"] or 0) < OK:
                    print(f"  ikke genfundet [{b['status']} {b['andel']}] {j['hvor']}: {b['url']}")
    if not merged:
        return 1
    reg["meta"]["opdateret"] = f"{datetime.date.today()} (fase 7: instanslag uden for de otte domæner, flettet med pipeline/populate.py)"
    if FASE7 not in reg["meta"]["metode"]:
        reg["meta"]["metode"].append(FASE7)
    REG.write_text("".join(raw.splitlines(True)[:2]) + yaml.dump(reg, Dumper=Dumper, allow_unicode=True, sort_keys=False, width=140, default_flow_style=False), encoding="utf-8")
    return 1 if bad else 0


def selftest() -> None:
    global CACHE
    CACHE = Path(tempfile.mkdtemp())
    page = "<p>§ 1. Told- og skatte&shy;forvaltningen udøver forvaltningen af lovgivning om skatter og lov om vurdering.</p>"
    q = "Told- og skatteforvaltningen udøver forvaltningen af lovgivning om skatter"
    assert quoted(q, page) == 1.0 and quoted("noget helt andet som slet ikke står på denne side", page) == 0.0
    eli = "https://www.retsinformation.dk/eli/lta/2025/275"
    (CACHE / (hashlib.sha1((eli + "/xml").encode()).hexdigest() + ".raw")).write_bytes(
        "<Dokument><Meta><DocumentType>LBK H#X</DocumentType><DocumentTitle>Bekendtgørelse af sundhedsloven</DocumentTitle><Year>2025</Year>"
        "<DiesSigni>2025-03-12</DiesSigni><Status>Historic</Status><Number>275</Number></Meta><Char>§ 1. Tekst</Char></Dokument>".encode())
    assert ri_meta(eli)["Status"] == "Historic" and ri_meta(eli + "/pdf")["Number"] == "275" and "§ 1. Tekst" in fetch(eli)[1]
    law = {"id": "lov-x", "navn": "Sundhedsloven", "type": "lov", "ministerium": "ingen", "status": "aktiv", "url": {"vaerdi": eli, "belaeg": []},
           "identifikatorer": {"lovtidende": "LBK nr. 999 af 01/01/2020", "belaeg": []}}
    reg0 = {"nodes": [{"id": "t", "type": "lov", "adgang": {"regel": RULES["adgang"]}, "licens": {"regel": RULES["licens"]}, "opdatering": {"regel": RULES["opdatering"]}}], "edges": [], "huller": []}
    merge({"omraade": "x", "noder": [law]}, reg0, {}, set())
    got = reg0["nodes"][1]
    assert got["identifikatorer"]["lovtidende"] == "LBK nr. 275 af 12/03/2025" and "historisk" in got["identifikatorer"]["katalog_note"]
    assert got["url"] == {"vaerdi": eli, "kilder": [eli], "sikkerhed": "verificeret"} and got["adgang"]["regel"] == RULES["adgang"]
    law.update(id="lov-y", navn="Lov om noget helt andet")
    merge({"omraade": "x", "noder": [law]}, reg0, {}, set())
    assert reg0["nodes"][2]["url"]["sikkerhed"] == "ukendt"
    b = [{"url": "https://www.retsinformation.dk/eli/lta/1/1", "citat": q}]
    assert certainty(b, PRIMARY, {b[0]["url"]: ("ok", page)})[0] == "verificeret"
    assert certainty(b, set(), {b[0]["url"]: ("ok", page)})[0] == "sandsynlig"
    assert certainty(b, PRIMARY, {b[0]["url"]: ("ukendt", "HTTP 403")})[0] == "sandsynlig"
    assert certainty(b, PRIMARY, {b[0]["url"]: ("død", "HTTP 404")})[:2] == ("ukendt", [])
    assert certainty(b, PRIMARY, {b[0]["url"]: ("ok", page)}, must="sst.dk")[0] == "sandsynlig"
    ids, edges = index(REG.read_text(encoding="utf-8"))
    assert ids["min-skat-og-vaekst"] == "ministerium" and len(ids) > 600 and len(edges) > 1200
    dup = {"omraade": "x", "noder": [{"id": "sty-ankestyrelsen", "navn": "A", "type": "styrelse", "ministerium": "min-social", "status": "aktiv"}]}
    assert any("findes allerede" in e for e in check(dup, ids, edges))
    wrong = {"omraade": "x", "kanter": [{"from": "sty-ankestyrelsen", "type": "henviser_til", "to": "sty-civilstyrelsen", "beskrivelse": "x", "belaeg": b}]}
    assert any("skal være dokument" in e for e in check(wrong, ids, edges))
    fix = {"omraade": "x", "rettelser": [{"id": "sty-ankestyrelsen", "felt": "url", "vaerdi": "https://ast.dk/", "belaeg": b}]}
    assert check(fix, ids, edges) == [] and check({"omraade": "x", "rettelser": [{"id": "findes-ikke", "felt": "url", "belaeg": b}]}, ids, edges)
    reg = {"nodes": [{"id": "n", "type": "styrelse", "url": {"vaerdi": "ikke fundet", "kilder": [], "sikkerhed": "ukendt"}}], "edges": [], "huller": []}
    u = "https://n.dk/om"
    fix["rettelser"] = [{"id": "n", "felt": "url", "vaerdi": "https://n.dk/", "belaeg": [{"url": u, "citat": q}]}]
    merge(fix, reg, {u: ("ok", page)}, set())
    assert reg["nodes"][0]["url"] == {"vaerdi": "https://n.dk/", "kilder": [u], "sikkerhed": "verificeret"}
    assert merge(fix, reg, {u: ("ok", page)}, set(), {review(fix)[0]["hvor"]: "delvist"})[0]["sikkerhed"] == "sandsynlig"
    fix["rettelser"][0]["vaerdi"] = "https://andet.dk/"
    assert "afvist" in merge(fix, reg, {u: ("død", "HTTP 404")}, set())[0] and reg["nodes"][0]["url"]["vaerdi"] == "https://n.dk/"
    print("selftest ok")


if __name__ == "__main__":
    cmd, args = (sys.argv[1] if len(sys.argv) > 1 else ""), sys.argv[2:]
    if cmd == "selftest":
        selftest()
    elif cmd == "check" and args:
        problems = check(json.loads(Path(args[0]).read_text(encoding="utf-8")), *index(REG.read_text(encoding="utf-8")))
        print(*problems, f"{len(problems)} fejl" if problems else "OK", sep="\n")
        sys.exit(1 if problems else 0)
    elif cmd == "hosts" and args:
        print(json.dumps(sorted({urllib.parse.urlsplit(u).hostname for a in args for u in urls(json.loads(Path(a).read_text(encoding="utf-8")))} | {"www.retsinformation.dk"})))
    elif cmd == "review" and args:
        print(json.dumps(review(json.loads(Path(args[0]).read_text(encoding="utf-8"))), ensure_ascii=False, indent=1))
    elif cmd == "apply" and args:
        sys.exit(apply(args))
    else:
        sys.exit(__doc__)
