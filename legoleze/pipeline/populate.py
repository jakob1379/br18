#!/usr/bin/env python3
"""Fase 7: flet agent-fund ind i registry.yaml med maskinel citatkontrol.

    python3 populate.py check FUND.json      # skematjek uden netværk og uden PyYAML (agenter kører det selv)
    python3 populate.py lov ELI-ADRESSE      # status, gældende version, ministerium og Retsinformations henvisninger (hjemmel, ændringer, afledte forskrifter)
    python3 populate.py tekst URL MØNSTER    # sidens egen tekst omkring hvert træf på et regulært udtryk (til ordrette citater)
    python3 populate.py hosts FUND.json...   # værter der skal kunne nås af review og apply
    python3 populate.py review FUND.json     # hent kilder; påstand, citat, kontekst og paragraf til en kontrollant, som skriver FUND.dom.json
    python3 populate.py apply FUND.json...   # tjek citater (kilderne ligger i cachen efter review), flet, skriv registry.yaml + FUND.kontrol.json
    python3 populate.py ajour                # slå alle aktive retsakter op: gældende version, senere ændringer og de kanter, Retsinformation fører;
                                             # journal i raw/populate/DATO-ajour.kontrol.json
    python3 populate.py selftest

En agent leverer noder, kanter og rettelser med belaeg: [{url, citat}]. Sikkerheden sættes her, ikke af agenten:
verificeret = citatet er genfundet på en officiel side eller på to uafhængige sekundære sider (for url: på selve siden),
eller feltet er læst direkte af Retsinformation (nummer, dato, titel, status og ministerium for love og bekendtgørelser;
gældende version af en lov fra tidslinjen),
sandsynlig = der er belæg, men det er ikke genfundet maskinelt eller kun på én sekundær side,
ukendt = intet belæg, eller alle kilder er døde.
Findes FUND.dom.json ([{hvor, dom, grund}] med dom baerer | delvist | baerer-ikke), sænker delvist til højst sandsynlig
og baerer-ikke til ukendt. Kør scripts/build.py bagefter.
"""
from __future__ import annotations

import copy
import datetime
import fcntl
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
         "eller feltet er læst af Retsinformations metadata. Ellers sandsynlig. Rå fund, domme og kontroljournaler ligger i raw/populate/. "
         "Fra 2026-11-12 ser kontrollanten også sidens egen tekst omkring citatet og den paragraf, citatet står i; en lov, hvis citerede version "
         "er historisk, flyttes til den gældende lovbekendtgørelse fra Retsinformations tidslinje; og en ressortansvar-kant til en lov eller "
         "bekendtgørelse er verificeret, når Retsinformations ministeriefelt er det samme ministerium og med sikkerhed er sat efter "
         "regeringsdannelsen: dokumentet er udstedt efter den, eller ministeriet fik sit navn ved den (feltet på ældre dokumenter er ikke "
         "altid ført ajour). populate.py ajour slår alle aktive retsakter op hos Retsinformation og skriver gældende version, nummer, dato og "
         "senere ændringer samt de hjemmel_for- og implementerer_EU-kanter, Retsinformation selv fører mellem registry'ets noder.")
RI = "https://www.retsinformation.dk"
SENERE, LOVGIVNING, IMPLEMENTERER = "Senere ændringer til forskriften", "Lovgivning forskriften vedrører", "Forskrifter, som implementerer EU direktiv "
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


def get(url: str) -> tuple[str, bytes]:
    """(status, indhold): ok | død (404/410) | ukendt (botmur, timeout). Én forespørgsel ad gangen pr. site, også på tværs af processer."""
    p = urllib.parse.urlsplit(url)
    target = url
    if site(url) == "retsinformation.dk" and p.path.startswith("/eli/"):
        target = RI + re.sub(r"/(pdf|xml|html)$", "", p.path.rstrip("/")) + "/xml"
    CACHE.mkdir(parents=True, exist_ok=True)
    cache = CACHE / (hashlib.sha1(target.encode()).hexdigest() + ".raw")
    fresh = lambda: cache.exists() and time.time() - cache.stat().st_mtime < 7 * 86400
    if fresh():
        return "ok", cache.read_bytes()
    with open(CACHE / (site(url) + ".lock"), "a+", encoding="utf-8") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        if fresh():
            return "ok", cache.read_bytes()
        lock.seek(0)
        wait = float(lock.read() or 0) + (10.5 if site(url) == "retsinformation.dk" else 2) - time.time()
        if wait > 0:
            time.sleep(wait)
        try:
            accept = {"Accept": "application/json"} if p.path.startswith("/api/") else {}
            req = urllib.request.Request(urllib.parse.quote(target, safe=":/?&=%#@+,;~()!*'[]$"), headers={"User-Agent": UA, "Accept-Language": "da", **accept})
            with urllib.request.urlopen(req, timeout=45) as r:
                raw = r.read(30_000_000)
        except urllib.error.HTTPError as ex:
            return ("død" if ex.code in (404, 410) else "ukendt"), f"HTTP {ex.code}".encode()
        except (OSError, http.client.HTTPException, ValueError) as ex:
            return "ukendt", str(ex)[:120].encode()
        finally:
            lock.seek(0)
            lock.truncate()
            lock.write(str(time.time()))
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
    text = " ".join(text.split())
    return ("ok", text) if text else ("ukendt", "tom side")


def ri_meta(url: str) -> dict:
    """Retsinformations egne metadata for et ELI-dokument; tom, hvis de ikke kan læses eller ikke passer til adressen."""
    status, raw = get(url)
    block = re.search(rb"(?s)<Meta\b.*?</Meta>", raw) if status == "ok" else None
    fields = "DocumentType|Year|Number|DiesSigni|DocumentTitle|PopularTitle|Status|DateOfHistoricMark|Ministry|UniqueDocumentId"
    m = dict(re.findall(rf"<({fields})>([^<]*)<", block.group(0).decode("utf-8", "replace"))) if block else {}
    path = re.sub(r"/(pdf|xml|html)$", "", urllib.parse.urlsplit(url).path.rstrip("/"))
    return m if m.get("DiesSigni") and path.endswith(f"/{m.get('Year')}/{m.get('Number')}") else {}


def betegnelse(meta: dict) -> str:
    y, mo, d = meta["DiesSigni"].split("-")
    kind = meta["DocumentType"].split("#")[0].split()[0]
    return f"{DOC_KINDS.get(kind, kind)} nr. {meta['Number']} af {d}/{mo}/{y}"


def ressort(meta: dict, reg: dict) -> str | None:
    """Retsinformations ministerium for et gældende dokument, når feltet med sikkerhed er sat efter regeringsdannelsen: dokumentet er
    udstedt efter den, eller ministeriet fik sit navn ved den og hed noget andet, da dokumentet blev udstedt. Ellers None, for feltet
    på ældre dokumenter er ikke altid ført ajour."""
    m, dato, dannet = meta.get("Ministry"), meta.get("DiesSigni", ""), str(reg.get("regering", {}).get("dannet", ""))
    omdoebt = any(n["navn"] == m and str(p.get("periode", "")).endswith(dannet) and str(p.get("periode", "")).split("–")[0].strip() <= dato
                  for n in reg["nodes"] if n["type"] == "ministerium" for p in n.get("tidligere_navne", []))
    return m if meta.get("Status") == "Valid" and (dato >= dannet or omdoebt) else None


def doktype(meta: dict) -> list[dict]:
    """dokumenttyper.liste for en lov, lovbekendtgørelse eller bekendtgørelse ud fra Retsinformations dokumenttype; ellers tom."""
    kind = (meta.get("DocumentType") or "").split("#")[0].split()
    code = DOC_KINDS.get(kind[0], kind[0]) if kind else ""
    navn = {"LOV": "lov", "LBK": "lovbekendtgørelse", "BEK": "bekendtgørelse"}.get(code)
    return [{"type": navn, "bindende": "bindende"}] if navn else []


def _dato(d: dict) -> datetime.date:
    return datetime.datetime.strptime(d["signatureDate"], "%d/%m/%Y").date()


def tidslinje(meta: dict) -> list[dict]:
    """Retsinformations tidslinje for en lov (hovedlov, ændringslove og lovbekendtgørelser); tom, hvis den ikke kan læses."""
    if not meta.get("UniqueDocumentId"):
        return []
    status, raw = get(f"{RI}/api/document/{meta['UniqueDocumentId']}/timeline")
    try:
        tl = json.loads(raw) if status == "ok" else []
    except ValueError:
        return []
    return tl if isinstance(tl, list) else []


def gaeldende(tl: list[dict]) -> dict:
    """Den nyeste ikke-historiske hovedlov eller lovbekendtgørelse i en tidslinje; tom, hvis ingen."""
    return max((d for d in tl if (d.get("documentTypeId") == 30 or d.get("isMainLaw")) and not d.get("isHistoric")), key=_dato, default={})


def henvisninger(meta: dict) -> dict:
    """Retsinformations henvisninger for et dokument som {overskrift: [poster]}; tom, hvis de ikke kan læses."""
    if not meta.get("UniqueDocumentId"):
        return {}
    status, raw = get(f"{RI}/api/document/{meta['UniqueDocumentId']}/references/1")
    try:
        d = json.loads(raw) if status == "ok" else {}
    except ValueError:
        return {}
    grupper = [g for k in ("referenceGroups", "documentLinkGroups") for g in d.get(k) or []] if isinstance(d, dict) else []
    return {g["header"]: g.get("references") or [] for g in grupper if g.get("header")}


def afloeser(meta: dict) -> dict:
    """Metadata (plus eli) for den gældende version af et historisk dokument; ellers tom. For en hovedlov eller lovbekendtgørelse er det den
    nyeste gældende i tidslinjen, for en bekendtgørelse den gældende bekendtgørelse med samme titel blandt dem, der har ændret eller ophævet den."""
    kind = meta.get("DocumentType", "").split("#")[0].split()
    code = DOC_KINDS.get(kind[0], kind[0]) if kind else ""
    href = None
    if meta.get("Status") == "Historic" and "Æ" not in kind[1:] and code in ("LBK", "LOV"):
        href = gaeldende(tidslinje(meta)).get("href")
    elif meta.get("Status") == "Historic" and "Æ" not in kind[1:] and code == "BEK":
        samme = [r for r in henvisninger(meta).get(SENERE, []) if not r.get("isHistorical") and norm(r.get("title", "")) == norm(meta.get("DocumentTitle", ""))]
        href = max(samme, key=lambda r: r.get("offentliggoerelsesDato", "").split("-")[::-1])["eliPath"] if samme else None
    ny_meta = ri_meta(RI + href) if href else {}
    return {**ny_meta, "eli": RI + href} if ny_meta else {}


def numre(tekst: str) -> set[str]:
    """Dokumentnumre nævnt i en tekst: tallet efter "nr." eller efter en dokumenttype som BEK eller VEJ."""
    return set(re.findall(r"(?:\bnr\.?\s*|\b(?:LOV|LBK|BEK|VEJ|CIR|CIS|SKR)\s+)(\d+)", tekst, re.IGNORECASE))


def hedder(navn: str, meta: dict, nummer: bool = True) -> bool:
    """Om et nodenavn svarer til dokumentet hos Retsinformation: ordene dækker titlen eller populærtitlen, eller navnet nævner dokumentets
    nummer. Nummeret tæller kun med nummer=True; vejledningers numre forveksles for let."""
    names = [set(norm(x).split()) - {"bekendtgørelse", "af"} for x in (navn, re.sub(r"\([^)]*\)", " ", navn))]
    titles = [set(norm(meta.get(k, "")).split()) - {"bekendtgørelse", "af"} for k in ("PopularTitle", "DocumentTitle")]
    return nummer and meta.get("Number") in numre(navn) or any(t and len(t & name) >= 0.8 * min(len(t), len(name)) for t in titles for name in names)


def kontekst(citat: str, text: str, pad: int = 300) -> str | None:
    """Sidens egen tekst omkring citatet eller dets første genfundne 5-ords-vindue; None, hvis intet af det står der."""
    w, text = norm(citat).split(), text.replace("\N{SOFT HYPHEN}", "")
    for part in [w] + [w[i:i + 5] for i in range(max(1, len(w) - 4))]:
        m = re.search(r"[\W_]+".join(map(re.escape, part)), text, re.IGNORECASE)
        if m:
            return text[max(0, m.start() - pad):m.end() + pad]
    return None


def paragraf(citat: str, xml: str) -> str | None:
    """Den eller de paragraffer i et dokument fra Retsinformation, citatet står i; None, hvis det også står i titlen eller indledningen."""
    hits = [(quoted(citat, re.sub(r"<[^>]+>", " ", chunk)), i and re.search(r"<Explicatus>\s*([^<]*?)\.?\s*</Explicatus>", chunk))
            for i, chunk in enumerate(re.split(r"(?=<Paragraf\b)", xml))]
    best = max(andel for andel, _ in hits)
    heads = [head.group(1) if head else None for andel, head in hits if andel == best]
    return " / ".join(dict.fromkeys(heads[:3])) if best >= OK and None not in heads else None


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


def spor(b: dict, page: tuple[str, str]) -> dict:
    """Det, kontrollen selv fandt for ét belæg: om citatet står på siden, teksten omkring det og paragraffen."""
    status, text = page
    if status != "ok":
        return {"genfundet": False, "side": status}
    out = {"genfundet": quoted(b["citat"], text) >= OK, "kontekst": kontekst(b["citat"], text)}
    if site(b["url"]) == "retsinformation.dk":
        out["paragraf"] = paragraf(b["citat"], get(b["url"])[1].decode("utf-8", "replace"))
    return {k: v for k, v in out.items() if v is not None}


def review(f: dict, pages: dict | None = None) -> list[dict]:
    """Hver påstand som {hvor, paastand, belaeg}; hvor er samme nøgle som i kontroljournalen. Med pages får hvert belæg også spor()."""
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
    for o in out if pages is not None else []:
        o["belaeg"] = [{**b, **spor(b, pages[b["url"]])} for b in o["belaeg"]]
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
    ri_min = {}
    rank = ["ukendt", "sandsynlig", "verificeret"]
    for n in f.get("noder", []):
        nid = n["id"]
        own_url[nid] = str((n.get("url") or {}).get("vaerdi"))
        on_ri = n["type"] in RI_TYPES and site(own_url[nid]) == "retsinformation.dk"
        meta = ri_meta(own_url[nid]) if on_ri else {}
        ny = afloeser(meta) if n["type"] in ("lov", "bekendtgørelse") else {}
        hist = meta if ny else {}
        if ny:
            own_url[nid], meta = ny["eli"], ny
        ri_min[nid] = ressort(meta, reg)
        named = hedder(n["navn"], meta)
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
                ids = {"eli": own_url[nid], "lovtidende": betegnelse(meta)}
                given = {k: v for k, v in n.get(c, {}).items() if k != "belaeg"}
                ids.update({k: v for k, v in given.items() if k not in ids})
                if hist:
                    ids["katalog_note"] = (f"Fundet citerede {betegnelse(hist)}, som Retsinformation markerer som historisk "
                                           f"({hist.get('DateOfHistoricMark', 'dato ukendt')}); gældende version er læst hos Retsinformation "
                                           f"({datetime.date.today()}).")
                elif meta.get("Status") == "Historic":
                    ids["katalog_note"] = (f"Retsinformation markerer denne version som historisk ({meta.get('DateOfHistoricMark', 'dato ukendt')}); "
                                           f"den gældende afløser er ikke identificeret (kontrolleret {datetime.date.today()}).")
                out[c] = from_meta(nid, c, ids, meta, given)
                if hist:
                    journal[-1]["flyttet_fra"] = f"{betegnelse(hist)} → {betegnelse(meta)} {meta.get('DocumentTitle')}"
            elif meta and named and c == "url":
                out[c] = from_meta(nid, c, {"vaerdi": own_url[nid]}, meta, None)
            elif meta and c == "hjemmel" and n.get(c, {}).get("tekst") == "ikke relevant":
                out[c] = from_meta(nid, c, {"tekst": "ikke relevant"}, meta, None)
            elif c == "dokumenttyper" and c not in n and doktype(meta):
                out[c] = from_meta(nid, c, {"liste": doktype(meta)}, meta, None)
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
    ministre = {n["id"]: n["navn"] for n in reg["nodes"] if n["type"] == "ministerium" and n.get("status") == "aktiv"}
    for e in f.get("kanter", []):
        c = claim("kant " + "|".join((e["from"], e["type"], e["to"])), e, e["from"], e["to"])
        m = ri_min.get(e["to"]) if e["type"] == "ressortansvar" else None
        if m and m == ministre.get(e["from"]):
            c["sikkerhed"], c["kilder"] = "verificeret", list(dict.fromkeys([own_url[e["to"]], *c["kilder"]]))
            journal[-1].update(sikkerhed="verificeret", metadata={"Ministry": m})
        elif m in ministre.values() and not any(ministre.get(x["from"]) == m and (x["type"], x["to"]) == ("ressortansvar", e["to"]) for x in f["kanter"]):
            c["sikkerhed"] = min(c["sikkerhed"], "sandsynlig", key=rank.index)
            journal[-1].update(sikkerhed=c["sikkerhed"], konflikt=f"Retsinformation angiver {m} som ministerium for {e['to']}")
        reg["edges"].append({"type": e["type"], "from": e["from"], "to": e["to"], "beskrivelse": e["beskrivelse"],
                             "kilder": c["kilder"], "sikkerhed": c["sikkerhed"], "domaener": [omr]})
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


def hent(f: dict) -> dict:
    pages = {}
    for i, u in enumerate(us := urls(f), 1):
        pages[u] = fetch(u)
        print(f"\r  henter {i}/{len(us)}", end="", file=sys.stderr)
    return pages


def ajour(reg: dict) -> list:
    """Slå hver aktiv retsakt op hos Retsinformation. Historiske versioner flyttes til den gældende; nummer, dato, dokumenttype og senere
    ændringer skrives fra kilden; og de ressortansvar-, hjemmel_for- og implementerer_EU-kanter, Retsinformation selv fører mellem
    registry'ets noder, bekræftes eller tilføjes. En node, hvis navn ikke svarer til det dokument, den peger på, røres ikke (titel_afviger).
    Har noden i forvejen en lovtidende-tekst om samme dokument, beholdes teksten og dens sikkerhed; ellers skrives betegnelsen fra kilden.
    Returnér journalen over noder og berørte kanter."""
    journal, ri_min, node_af, relationer = [], {}, {}, []
    for n in reg["nodes"]:
        if n["type"] not in RI_TYPES or n["status"] != "aktiv":
            continue
        ids = n["identifikatorer"]
        url = str(n["url"].get("vaerdi"))
        found = re.search(r"\b(?:lta|retsinfo|mt)/\d{4}/\d+", f"{ids.get('eli', '')} {url if site(url) == 'retsinformation.dk' else ''}")
        if not found:
            continue
        eli = f"{RI}/eli/{found.group(0)}"
        meta = ri_meta(eli)
        j = {"hvor": f"{n['id']}.identifikatorer", "eli": eli, "status": meta.get("Status", "ulæselig"), "ministerium": meta.get("Ministry")}
        journal.append(j)
        if not meta:
            continue
        if not hedder(n["navn"], meta, nummer=n["type"] in ("lov", "bekendtgørelse")):
            j["titel_afviger"] = meta.get("DocumentTitle")
            continue
        ny = afloeser(meta) if n["type"] in ("lov", "bekendtgørelse") else {}
        nu, nu_eli = ny or meta, ny.get("eli", eli)
        ri_min[n["id"]] = (ressort(nu, reg), nu_eli)
        if node_af.setdefault(nu_eli, n["id"]) != n["id"]:
            j["samme_dokument_som"] = node_af[nu_eli]
        gammel = str(ids.get("lovtidende") or "")
        behold = not ny and meta["Number"] in numre(gammel) and gammel != betegnelse(nu)
        nyt = {"eli": nu_eli} if behold else {"lovtidende": betegnelse(nu), "eli": nu_eli}
        if gammel and not behold and gammel != betegnelse(nu):
            nyt["lovtidende_tidligere"] = gammel
        h = henvisninger(nu)
        if h:
            nyt["senere_aendringer"] = [{"betegnelse": r["shortName"].strip(), "eli": RI + r["eliPath"]} for r in h.get(SENERE, [])]
            nyt["aendringer_kontrolleret"] = str(datetime.date.today())
            relationer += [(RI + r["eliPath"], "hjemmel_for", nu_eli, nu_eli) for r in h.get(LOVGIVNING, [])]
            relationer += [(nu_eli, "hjemmel_for", RI + r["eliPath"], nu_eli) for hd, refs in h.items() if hd.startswith("Alle ") and " til denne " in hd for r in refs]
            relationer += [(nu_eli, "implementerer_EU", hd[len(IMPLEMENTERER):].strip(), nu_eli) for hd, refs in h.items()
                           if hd.startswith(IMPLEMENTERER) and any(str(r.get("id")) == nu.get("UniqueDocumentId") for r in refs)]
        aendring = "Æ" in meta.get("DocumentType", "").split("#")[0].split()[1:]
        if ny:
            j["flyttet_til"] = f"{betegnelse(ny)} {ny.get('DocumentTitle')}"
            nyt["katalog_note"] = (f"Tidligere registreret version {betegnelse(meta)} er historisk ({meta.get('DateOfHistoricMark', 'dato ukendt')}); "
                                   f"gældende version er læst hos Retsinformation ({datetime.date.today()}).")
            if re.sub(r"/(pdf|xml|html)$", "", url.rstrip("/")) == eli:
                n["url"] = {**n["url"], "vaerdi": ny["eli"], "kilder": list(dict.fromkeys([ny["eli"], *n["url"].get("kilder", [])])), "sikkerhed": "verificeret"}
        elif meta.get("Status") == "Historic" and "katalog_note" not in ids and not aendring:
            nyt["katalog_note"] = (f"Retsinformation markerer denne version som historisk ({meta.get('DateOfHistoricMark', 'dato ukendt')}); "
                                   f"den gældende afløser er ikke identificeret (kontrolleret {datetime.date.today()}).")
        n["identifikatorer"] = {**{k: v for k, v in ids.items() if k not in ("kilder", "sikkerhed")}, **nyt,
                                "kilder": list(dict.fromkeys([nu_eli, *ids.get("kilder", [])])),
                                "sikkerhed": ids.get("sikkerhed", "ukendt") if behold else "verificeret"}
        if n["dokumenttyper"]["sikkerhed"] == "ukendt" and not n["dokumenttyper"].get("liste") and doktype(nu):
            n["dokumenttyper"] = {"liste": doktype(nu), "kilder": [nu_eli], "sikkerhed": "verificeret"}
            j["dokumenttyper"] = n["dokumenttyper"]["liste"][0]["type"]
    ministre = {n["id"]: n["navn"] for n in reg["nodes"] if n["type"] == "ministerium" and n.get("status") == "aktiv"}
    delt = {(ministre.get(e["from"]), e["to"]) for e in reg.get("edges", []) if e["type"] == "ressortansvar"}
    for e in reg.get("edges", []):
        m, kilde = ri_min.get(e["to"], (None, None)) if e["type"] == "ressortansvar" else (None, None)
        hvor = "kant " + "|".join((e["from"], e["type"], e["to"]))
        if m and m == ministre.get(e["from"]) and e["sikkerhed"] != "verificeret":
            journal.append({"hvor": hvor, "ministerium": m, "opgraderet_fra": e["sikkerhed"]})
            e["sikkerhed"], e["kilder"] = "verificeret", list(dict.fromkeys([kilde, *e["kilder"]]))
        elif m in ministre.values() and (m, e["to"]) not in delt:
            journal.append({"hvor": hvor, "ministerium": m, "konflikt": f"Retsinformation angiver {m}; registry har {e['from']}"})
    node_af.update({n["identifikatorer"]["celex"]: n["id"] for n in reg["nodes"] if n["type"] == "eu-direktiv" and n["identifikatorer"].get("celex")})
    kanter = {(e["from"], e["type"], e["to"]): e for e in reg.get("edges", [])}
    domaener = {n["id"]: n.get("domaener", []) for n in reg["nodes"]}
    tekst = {"hjemmel_for": "Retsinformation fører den første som lovgivning, den anden vedrører.",
             "implementerer_EU": "Retsinformation fører forskriften blandt dem, der implementerer direktivet."}
    for a, typ, b, kilde in dict.fromkeys(relationer):
        fra, til = node_af.get(a), node_af.get(b)
        if not fra or not til or fra == til:
            continue
        e, hvor = kanter.get((fra, typ, til)), f"kant {fra}|{typ}|{til}"
        if e is None:
            kanter[fra, typ, til] = {"type": typ, "from": fra, "to": til, "beskrivelse": tekst[typ], "kilder": [kilde], "sikkerhed": "verificeret",
                                     "domaener": domaener[til if typ == "hjemmel_for" else fra]}
            reg["edges"].append(kanter[fra, typ, til])
            journal.append({"hvor": hvor, "ny": True})
        elif e["sikkerhed"] != "verificeret":
            journal.append({"hvor": hvor, "opgraderet_fra": e["sikkerhed"]})
            e["sikkerhed"], e["kilder"] = "verificeret", list(dict.fromkeys([kilde, *e["kilder"]]))
    return journal


class Dumper(yaml.SafeDumper if yaml else object):
    pass


def gem(raw: str, reg: dict) -> None:
    Dumper.add_representer(str, lambda d, s: d.represent_scalar("tag:yaml.org,2002:str", s, style="|" if "\n" in s else None))
    reg["meta"]["opdateret"] = f"{datetime.date.today()} (fase 7: instanslag uden for de otte domæner, flettet med pipeline/populate.py)"
    reg["meta"]["metode"] = [m for m in reg["meta"]["metode"] if not m.startswith("Fase 7 ")] + [FASE7]
    REG.write_text("".join(raw.splitlines(True)[:2]) + yaml.dump(reg, Dumper=Dumper, allow_unicode=True, sort_keys=False, width=140, default_flow_style=False), encoding="utf-8")


def apply(paths: list[str]) -> int:
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
        pages = hent(f)
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
        print(*(f"  {k} {j['hvor']}: {j[k]}\n" for j in journal for k in ("afvist", "konflikt", "flyttet_fra") if k in j), sep="", end="")
        print(f"  kontrollant: {'ingen dom-fil' if dom is None else {v: sum(j['dom'] == v for j in journal) for v in ('baerer', 'delvist', 'baerer-ikke', None)}}")
        print("  primære domæner brugt:", sorted(used & primary), "\n  øvrige:", sorted(used - primary))
        for j in journal:
            for b in j["belaeg"]:
                if (b["andel"] or 0) < OK:
                    print(f"  ikke genfundet [{b['status']} {b['andel']}] {j['hvor']}: {b['url']}")
    if not merged:
        return 1
    gem(raw, reg)
    return 1 if bad else 0


def selftest() -> None:
    global CACHE
    CACHE = Path(tempfile.mkdtemp())

    def offline(*_args, **_kwargs):
        raise AssertionError("selftest må ikke bruge netværk")

    urllib.request.urlopen = offline
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
    assert got["dokumenttyper"] == {"liste": [{"type": "lovbekendtgørelse", "bindende": "bindende"}], "kilder": [eli], "sikkerhed": "verificeret"}
    assert doktype({"DocumentType": "Bekendtgørelse"})[0]["type"] == "bekendtgørelse" and doktype({"DocumentType": "VEJ H#X"}) == doktype({}) == []
    felt = {"Status": "Valid", "Ministry": "X", "DiesSigni": "2026-06-02"}
    nu = {"regering": {"dannet": "2026-06-03"}, "nodes": [{"type": "ministerium", "navn": "X", "tidligere_navne": [{"navn": "Y", "periode": "2011-10 – 2016"}]}]}
    assert ressort(felt, nu) is None and ressort({**felt, "DiesSigni": "2026-06-03"}, nu) == "X" and ressort({**felt, "DiesSigni": "2012-01-01"}, nu) is None
    nu["nodes"][0]["tidligere_navne"].append({"navn": "Z", "periode": "2021-01-21 – 2026-06-03"})
    assert ressort(felt, nu) == "X" and ressort({**felt, "DiesSigni": "2020-01-01"}, nu) is None and ressort({**felt, "Status": "Historic"}, nu) is None
    law.update(id="lov-y", navn="Lov om noget helt andet")
    merge({"omraade": "x", "noder": [law]}, reg0, {}, set())
    assert reg0["nodes"][2]["url"]["sikkerhed"] == "ukendt"

    def put(target: str, body: str) -> None:
        (CACHE / (hashlib.sha1(target.encode()).hexdigest() + ".raw")).write_bytes(body.encode())

    meta = "<Dokument><Meta><DocumentType>LBK H#X</DocumentType><DocumentTitle>Bekendtgørelse af sundhedsloven</DocumentTitle><Year>{0}</Year>"
    meta += "<DiesSigni>{0}-0{1}-01</DiesSigni><Status>{2}</Status><Number>{1}</Number><Ministry>Sundhedsministeriet</Ministry><UniqueDocumentId>{1}</UniqueDocumentId></Meta>"
    par = "<Paragraf><Explicatus>§ 98.</Explicatus><Char>A-kassens afgørelser kan indbringes for direktøren</Char></Paragraf><Paragraf><Explicatus>§ 99.</Explicatus><Char>Direktørens afgørelser kan indbringes for Ankestyrelsens Beskæftigelsesudvalg inden 4 uger</Char></Paragraf>"
    put(RI + "/eli/lta/2025/7/xml", meta.format(2025, 7, "Historic") + par + "</Dokument>")
    put(RI + "/eli/lta/2026/9/xml", meta.format(2026, 9, "Valid") + "</Dokument>")
    put(RI + "/api/document/7/timeline", json.dumps([
        {"documentTypeId": 30, "isHistoric": True, "signatureDate": "01/07/2025", "href": "/eli/lta/2025/7"},
        {"documentTypeId": 20, "isHistoric": False, "signatureDate": "01/10/2026", "href": "/eli/lta/2026/10"},
        {"documentTypeId": 30, "isHistoric": False, "signatureDate": "01/09/2026", "href": "/eli/lta/2026/9"}]))
    old = RI + "/eli/lta/2025/7"
    reg0["nodes"] += [{"id": m, "type": "ministerium", "status": "aktiv", "navn": navn, "adgang": {}, "licens": {}, "opdatering": {}}
                      for m, navn in (("min-s", "Sundhedsministeriet"), ("min-a", "Andet Ministerium"))]
    law.update(id="lov-z", navn="Sundhedsloven", url={"vaerdi": old, "belaeg": []})
    kanter = [{"from": m, "type": "ressortansvar", "to": "lov-z", "beskrivelse": "x", "belaeg": []} for m in ("min-s", "min-a")]
    j = merge({"omraade": "x", "noder": [law], "kanter": kanter}, reg0, {}, set())
    got = reg0["nodes"][-1]["identifikatorer"]
    assert got["eli"] == RI + "/eli/lta/2026/9" and got["lovtidende"] == "LBK nr. 9 af 01/09/2026" and "LBK nr. 7 af 01/07/2025" in got["katalog_note"]
    assert [e["sikkerhed"] for e in reg0["edges"][-2:]] == ["verificeret", "ukendt"] and not any("konflikt" in x for x in j)
    assert "konflikt" in merge({"omraade": "x", "noder": [{**law, "id": "lov-w"}], "kanter": [{**kanter[1], "to": "lov-w"}]}, reg0, {}, set())[-1]
    hit = spor({"url": old, "citat": "afgørelser kan indbringes for Ankestyrelsens Beskæftigelsesudvalg"}, fetch(old))
    assert hit["genfundet"] and hit["paragraf"] == "§ 99" and "§ 99. Direktørens" in hit["kontekst"]
    assert paragraf("denne sætning står ikke i dokumentet overhovedet", par) is None and kontekst("står ikke her", par) is None
    assert paragraf("afgørelser kan indbringes for", par) == "§ 98 / § 99" and paragraf("afgørelser kan indbringes for", "<T>afgørelser kan indbringes for</T>" + par) is None
    gl = {"id": "lov-g", "navn": "Sundhedsloven", "type": "lov", "status": "aktiv", "domaener": ["d"],
          "identifikatorer": {"eli": "eli/lta/2025/7", "lovtidende": "gammel", "kilder": [old], "sikkerhed": "sandsynlig"},
          "url": {"vaerdi": old + "/pdf", "kilder": [], "sikkerhed": "ukendt"}, "dokumenttyper": {"liste": [], "kilder": [], "sikkerhed": "ukendt"}}
    bek = {**copy.deepcopy(gl), "id": "bek-b", "navn": "Noget helt andet", "type": "bekendtgørelse",
           "identifikatorer": {"eli": RI + "/eli/lta/2026/3", "lovtidende": "BEK nr. 3 af 01/03/2026 (i kraft 1/4/2026)", "kilder": [], "sikkerhed": "sandsynlig"}}
    eu = {"id": "eu-dir-2012-34", "type": "eu-direktiv", "status": "aktiv", "identifikatorer": {"celex": "32012L0034"}}
    put(RI + "/eli/lta/2026/3/xml", meta.format(2026, 3, "Valid") + "</Dokument>")
    put(RI + "/api/document/9/references/1", json.dumps({
        "referenceGroups": [{"header": SENERE, "references": [{"shortName": "LOV nr 10 af 01/10/2026 § 2 ", "eliPath": "/eli/lta/2026/10"}]}],
        "documentLinkGroups": [{"header": IMPLEMENTERER + "32012L0034", "references": [{"id": 9}]}, {"header": IMPLEMENTERER + "31999L0001", "references": [{"id": 8}]}]}))
    put(RI + "/api/document/3/references/1", json.dumps({"referenceGroups": [{"header": LOVGIVNING, "references": [{"eliPath": "/eli/lta/2026/9"}]}]}))
    kant = [{"type": "ressortansvar", "from": m, "to": to, "kilder": [], "sikkerhed": "ukendt"} for m, to in (("min-s", "lov-g"), ("min-a", "lov-g"), ("min-a", "lov-k"))]
    ministre = [n for n in reg0["nodes"] if n["type"] == "ministerium"]
    forkert = {**copy.deepcopy(bek), "id": "bek-f", "navn": "Noget helt andet"}
    bek["navn"] = "Bekendtgørelse om noget (BEK nr. 3 af 2026)"
    log = ajour({"nodes": [gl, {**copy.deepcopy(gl), "id": "lov-k"}, {**copy.deepcopy(gl), "id": "lov-h", "status": "ophævet"}, bek, forkert, eu, *ministre], "edges": kant})
    assert [j["hvor"] for j in log] == ["lov-g.identifikatorer", "lov-k.identifikatorer", "bek-b.identifikatorer", "bek-f.identifikatorer", "kant min-s|ressortansvar|lov-g",
                                        "kant min-a|ressortansvar|lov-k", "kant lov-g|implementerer_EU|eu-dir-2012-34", "kant lov-g|hjemmel_for|bek-b"]
    assert "LBK nr. 9" in log[0]["flyttet_til"] and log[1]["samme_dokument_som"] == "lov-g" and "titel_afviger" in log[3] and "titel_afviger" not in log[2]
    assert gl["url"]["vaerdi"] == gl["identifikatorer"]["eli"] == RI + "/eli/lta/2026/9" and forkert["identifikatorer"]["sikkerhed"] == "sandsynlig"
    assert "senere_aendringer" not in forkert["identifikatorer"] and gl["identifikatorer"]["lovtidende_tidligere"] == "gammel"
    assert bek["identifikatorer"]["lovtidende"] == "BEK nr. 3 af 01/03/2026 (i kraft 1/4/2026)" and bek["identifikatorer"]["sikkerhed"] == "sandsynlig"
    assert gl["identifikatorer"]["senere_aendringer"] == [{"betegnelse": "LOV nr 10 af 01/10/2026 § 2", "eli": RI + "/eli/lta/2026/10"}]
    assert list(gl["identifikatorer"])[-2:] == ["kilder", "sikkerhed"] and gl["identifikatorer"]["sikkerhed"] == "verificeret" and bek["identifikatorer"]["senere_aendringer"] == []
    assert kant[0]["sikkerhed"] == "verificeret" and kant[0]["kilder"] == [RI + "/eli/lta/2026/9"] and "konflikt" in log[5]
    assert kant[1]["sikkerhed"] == kant[2]["sikkerhed"] == "ukendt" and log[6]["ny"] and kant[3]["to"] == "eu-dir-2012-34"
    assert kant[4] == {"type": "hjemmel_for", "from": "lov-g", "to": "bek-b", "beskrivelse": kant[4]["beskrivelse"], "kilder": [RI + "/eli/lta/2026/3"],
                       "sikkerhed": "verificeret", "domaener": ["d"]}
    put(RI + "/eli/lta/2020/4/xml", meta.format(2020, 4, "Historic").replace("LBK H#X", "BEK H#X") + "</Dokument>")
    put(RI + "/api/document/4/references/1", json.dumps({"referenceGroups": [{"header": SENERE, "references": [
        {"title": "Bekendtgørelse om ændring af sundhedsloven", "eliPath": "/eli/lta/2026/5", "offentliggoerelsesDato": "02-09-2026"},
        {"title": "Bekendtgørelse af sundhedsloven", "eliPath": "/eli/lta/2026/9", "offentliggoerelsesDato": "01-09-2026"},
        {"title": "Bekendtgørelse af sundhedsloven", "eliPath": "/eli/lta/2021/1", "offentliggoerelsesDato": "01-12-2021", "isHistorical": True}]}]}))
    assert afloeser(ri_meta(RI + "/eli/lta/2020/4"))["eli"] == RI + "/eli/lta/2026/9" and henvisninger({}) == {}
    vej = {"DocumentType": "VEJ#LOKDOK15", "Number": "10226", "DiesSigni": "2019-12-19", "DocumentTitle": "Vejledning om beskyttede naturtyper"}
    assert betegnelse(vej) == "VEJ nr. 10226 af 19/12/2019" and hedder("Habitatvejledningen (VEJ nr. 10226 af 2019)", vej)
    assert not hedder("Habitatvejledningen (VEJ nr. 10226 af 2019)", vej, nummer=False) and hedder("Vejledning om naturtyper (VEJ nr. 1 af 2019)", vej, nummer=False)
    assert gl["identifikatorer"]["kilder"] == [RI + "/eli/lta/2026/9", old] and "LBK nr. 7" in gl["identifikatorer"]["katalog_note"]
    assert gl["dokumenttyper"]["liste"][0]["type"] == "lovbekendtgørelse" and gl["dokumenttyper"]["kilder"] == [RI + "/eli/lta/2026/9"]
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
        hosts = {urllib.parse.urlsplit(u).hostname for a in args for u in urls(json.loads(Path(a).read_text(encoding="utf-8")))} | {"www.retsinformation.dk"}
        print(json.dumps(sorted(hosts | {h.removeprefix("www.") for h in hosts} | {"www." + h.removeprefix("www.") for h in hosts})))
    elif cmd == "review" and args:
        fund = json.loads(Path(args[0]).read_text(encoding="utf-8"))
        print(json.dumps(review(fund, hent(fund)), ensure_ascii=False, indent=1))
    elif cmd == "lov" and args:
        doc = ri_meta(args[0])
        tl = tidslinje(doc)
        ny = gaeldende(tl)
        nu = (ri_meta(RI + ny["href"]) if ny else {}) or afloeser(doc) or doc
        print(json.dumps({
            "citeret": {"betegnelse": betegnelse(doc), **{k: doc.get(k) for k in ("DocumentTitle", "Status", "DateOfHistoricMark", "Ministry")}} if doc else "ikke fundet",
            "gaeldende": {"betegnelse": betegnelse(nu), "eli": nu.get("eli") or RI + ny.get("href", urllib.parse.urlsplit(args[0]).path), "ministerium": nu.get("Ministry")}
            if nu.get("Status") == "Valid" else "ikke fundet",
            "henvisninger_for_gaeldende": {hd: [f"{r['shortName'].strip()} {RI}{r['eliPath']}" + " (historisk)" * bool(r.get("isHistorical")) for r in refs[:40]]
                                           + [f"... {len(refs) - 40} flere"] * (len(refs) > 40)
                                           for hd, refs in henvisninger(nu).items() if refs and not hd.startswith(IMPLEMENTERER)},
            "implementerer_direktiver": [hd[len(IMPLEMENTERER):].strip() for hd, refs in henvisninger(nu).items()
                                         if hd.startswith(IMPLEMENTERER) and any(str(r.get("id")) == nu.get("UniqueDocumentId") for r in refs)],
        }, ensure_ascii=False, indent=1))
    elif cmd == "tekst" and len(args) == 2:
        status, text = fetch(args[0])
        hits = list(re.finditer(args[1], text, re.IGNORECASE)) if status == "ok" else []
        print(*(text[max(0, m.start() - 300):m.end() + 600] for m in hits[:20]), f"{status}: {len(hits)} træf", sep="\n\n")
    elif cmd == "apply" and args:
        sys.exit(apply(args))
    elif cmd == "ajour":
        text = REG.read_text(encoding="utf-8")
        registry = yaml.load(text, Loader=yaml.CSafeLoader)
        log = ajour(registry)
        gem(text, registry)
        (ROOT / "raw" / "populate" / f"{datetime.date.today()}-ajour.kontrol.json").write_text(json.dumps(log, ensure_ascii=False, indent=1), encoding="utf-8")
        noder = [j for j in log if not j["hvor"].startswith("kant ")]
        vis = ("flyttet_til", "konflikt", "titel_afviger", "samme_dokument_som")
        print({k: sum(j["status"] == k for j in noder) for k in ("Valid", "Historic", "ulæselig")},
              {k: sum(k in j for j in log) for k in (*vis, "ny", "opgraderet_fra")},
              *(f"  {j['hvor']}: {' | '.join(f'{k}: {j[k]}' for k in vis if k in j)}" for j in log if j.keys() & set(vis)), sep="\n")
    else:
        sys.exit(__doc__)
