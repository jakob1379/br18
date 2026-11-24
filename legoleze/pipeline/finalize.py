#!/usr/bin/env python3
"""merged.json + fill/critic results -> dk-regulering/registry.yaml."""
import json
import sys
from collections import Counter
from pathlib import Path

import yaml

SP = Path(__file__).resolve().parent
WF = Path("/root/.claude/projects/-home-user-ai-job-search-fork/9c9ad245-1536-5d87-980d-1a4837c57ed1/subagents/workflows")
RANK = {"verificeret": 2, "sandsynlig": 1, "ukendt": 0}
EDGE_TYPES = {"ressortansvar", "delegation", "hjemmel_for", "udsteder", "klageinstans", "domstolsproevelse", "tilsyn", "implementerer_EU", "henviser_til"}
NODE_TYPES = {
    "ministerium", "styrelse", "direktorat", "nævn", "klagenævn", "tilsyn", "råd", "fond", "domstol", "ombudsmand",
    "kommune", "region", "offentlig-virksomhed", "eu-institution", "privat-organisation", "standardiseringsorgan",
    "dokumentkilde", "lov", "bekendtgørelse", "cirkulære", "vejledning", "teknisk-forskrift", "plan", "regulativ",
    "eu-direktiv", "eu-forordning", "eu-afgørelse", "standard", "branchevejledning", "praksissamling",
}
TYPE_FIX = {"eu-agentur": "eu-institution", "ændringslov": "lov", "forskningsinstitution": "offentlig-virksomhed", "eu-dom": "praksissamling", "afgørelse": "praksissamling", "dom": "praksissamling", "lovbekendtgørelse": "lov",
            "eu-domstol": "eu-institution", "eu-delegeret-forordning": "eu-forordning", "eu-gennemførelsesforordning": "eu-forordning"}
ACCESS = {"API", "bulk", "ELI", "RSS", "HTML", "PDF", "betalingsmur", "ukendt", "ikke-relevant"}
ORDER = ["id", "navn", "type", "ministerium", "status", "domaener", "tidligere_navne", "hjemmel", "dokumenttyper", "url",
         "adgang", "identifikatorer", "licens", "opdatering", "krydsref_moenstre", "ingest", "note", "baseline"]


def journal(run):
    rows = [json.loads(l) for l in open(WF / run / "journal.jsonl")]
    labels = {r["agentId"]: r["label"] for r in rows if r["type"] == "started"}
    return [(labels.get(r["agentId"], "?"), r["result"]) for r in rows if r["type"] == "result" and r.get("result")]


def urls(xs):
    return list(dict.fromkeys(x.strip().replace(" ", "%20") for x in xs or [] if isinstance(x, str) and x.strip().startswith("http")))


def sweep(c):
    """Normalise one claim: encode URLs, never 'verificeret' without a source."""
    c["kilder"] = urls(c.get("kilder"))
    if c.get("sikkerhed") not in RANK:
        c["sikkerhed"] = "ukendt"
    if c["sikkerhed"] == "verificeret" and not c["kilder"]:
        c["sikkerhed"] = "sandsynlig"


def main(cfg):
    m = json.load(open(SP / "data" / "merged.json"))
    alias = json.load(open(SP / cfg["alias"]))
    nodes = {n["id"]: n for n in m["nodes"]}
    edges = {(e["from"], e["type"], e["to"]): e for e in m["edges"]}
    log = Counter()

    fills, critics = [], []
    for run in cfg.get("fill_runs", []):
        for label, res in journal(run):
            (fills if label.startswith("fill:") else critics).append((label, res))

    # 1. fill updates
    for _, res in fills:
        for u in res["opdateringer"]:
            nid = alias.get(u["id"], u["id"])
            n = nodes.get(nid)
            if not n:
                log["fill: ukendt id"] += 1
                continue
            try:
                val = json.loads(u["vaerdi_json"])
            except Exception:
                log["fill: ugyldig json"] += 1
                continue
            k, s = urls(u["kilder"]), u["sikkerhed"]
            if s == "verificeret" and not k:
                s = "sandsynlig"
            f = u["felt"]
            if f in ("status", "ministerium"):
                v = val.get("vaerdi") if isinstance(val, dict) else val
                if s == "verificeret" and v and (f != "ministerium" or v in nodes or v == "ingen"):
                    if n[f] != v:
                        n["note"] = (n.get("note", "") + f" | {f} rettet fra '{n[f]}' til '{v}' ({u['begrundelse'][:200]})").strip(" |")
                        n[f] = v
                        log[f"fill: {f} rettet"] += 1
                continue
            if not isinstance(val, dict):
                log["fill: ikke objekt"] += 1
                continue
            val.pop("kilder", None), val.pop("sikkerhed", None)
            if f == "url" and not str(val.get("vaerdi", "")).startswith("http"):
                continue
            if f == "adgang":
                val["vaerdier"] = [a for a in val.get("vaerdier", []) if a in ACCESS] or ["ukendt"]
            old = n.get(f) or {"kilder": [], "sikkerhed": "ukendt"}
            if RANK[s] > RANK[old.get("sikkerhed", "ukendt")] or (RANK[s] == RANK[old.get("sikkerhed", "ukendt")] and f in ("url", "identifikatorer") and s != "ukendt"):
                if f == "identifikatorer":
                    merged = {kk: vv for kk, vv in old.items() if kk not in ("kilder", "sikkerhed") and vv}
                    merged.update({kk: vv for kk, vv in val.items() if vv})
                    val = merged
                n[f] = {**val, "kilder": urls(k + (old.get("kilder", []) if f == "identifikatorer" else [])), "sikkerhed": s}
                log[f"fill: {f} opdateret"] += 1
            else:
                log[f"fill: {f} sprunget over (lavere/lige sikkerhed)"] += 1

    # 2. critic additions
    disputed = []
    for label, res in critics:
        dom = label.split(":", 1)[1]
        for c in res["nye_noder"]:
            nid = alias.get(c["id"], c["id"])
            if nid in nodes:
                log["critic: node fandtes"] += 1
                continue
            k, s = urls(c["kilder"]), c["sikkerhed"]
            if s == "verificeret" and not k:
                s = "sandsynlig"
            try:
                ident = json.loads(c["identifikatorer_json"] or "{}")
            except Exception:
                ident = {}
            u = c["url"] if str(c["url"]).startswith("http") else "ikke fundet"
            nodes[nid] = {
                "id": nid, "navn": c["navn"], "type": TYPE_FIX.get(c["type"], c["type"]),
                "ministerium": c["ministerium"] if (c["ministerium"] in nodes or c["ministerium"] == "ingen") else "ingen",
                "status": c["status"], "domaener": [f"kritik:{dom}"], "tidligere_navne": [],
                "hjemmel": {"tekst": c["hjemmel_tekst"], "kilder": k, "sikkerhed": s},
                "dokumenttyper": {"liste": c["dokumenttyper"], "kilder": k, "sikkerhed": "sandsynlig" if s != "ukendt" else "ukendt"},
                "url": {"vaerdi": u, "kilder": k if u != "ikke fundet" else [], "sikkerhed": s if u != "ikke fundet" else "ukendt"},
                "adgang": {"vaerdier": [a for a in c["adgang"] if a in ACCESS] or ["ukendt"], "kilder": [], "sikkerhed": "ukendt"},
                "identifikatorer": {**{kk: vv for kk, vv in ident.items() if vv}, "kilder": k if ident else [], "sikkerhed": s if ident else "ukendt"},
                "licens": {"tekst": "ikke undersøgt", "kilder": [], "sikkerhed": "ukendt"},
                "opdatering": {"frekvens": "ukendt", "versionshistorik": "ukendt", "kilder": [], "sikkerhed": "ukendt"},
                "krydsref_moenstre": [], "note": c["note"],
            }
            if c["ministerium"] not in nodes and c["ministerium"] not in ("ingen", None):
                nodes[nid]["note"] += f" (foreslået ministerium '{c['ministerium']}' findes ikke i registry)"
            log["critic: ny node"] += 1
        for e in res["nye_kanter"]:
            f, t = alias.get(e["from"], e["from"]), alias.get(e["to"], e["to"])
            key = (f, e["type"], t)
            if e["type"] not in EDGE_TYPES or f == t:
                continue
            if f not in nodes or t not in nodes:
                log["critic: kant med ukendt node"] += 1
                continue
            if key in edges:
                log["critic: kant fandtes"] += 1
                continue
            k, s = urls(e["kilder"]), e["sikkerhed"]
            if s == "verificeret" and not k:
                s = "sandsynlig"
            edges[key] = {"type": e["type"], "from": f, "to": t, "beskrivelse": e["beskrivelse"], "kilder": k, "sikkerhed": s, "domaener": [f"kritik:{dom}"]}
            log["critic: ny kant"] += 1
        for e in res["forkerte_kanter"]:
            key = (alias.get(e["from"], e["from"]), e["type"], alias.get(e["to"], e["to"]))
            disputed.append({**e, "kritiker": dom, "findes": key in edges})

    # 2b. verification patches (verify2:<domæne>): full-node replacements made with a real search budget
    for run in cfg.get("verify_runs", []):
        for label, p in journal(run):
            if not label.startswith("verify2:"):
                continue
            dom = label.split(":", 1)[1]
            for r in p["node_removals"]:
                rid = alias.get(r["id"], r["id"])
                if rid in nodes:
                    nodes.pop(rid)
                    log["verify: node fjernet"] += 1
            for nn in p["node_upserts"]:
                nid = alias.get(nn["id"], nn["id"])
                nn["id"] = nid
                old = nodes.get(nid, {})
                nn["domaener"] = sorted(set(old.get("domaener", [])) | {dom})
                if old.get("baseline"):
                    nn["baseline"] = old["baseline"]
                if old.get("ingest") and not nn.get("ingest"):
                    nn["ingest"] = old["ingest"]
                for f in ("hjemmel", "dokumenttyper", "url", "adgang", "identifikatorer", "licens", "opdatering"):
                    if not isinstance(nn.get(f), dict):
                        nn[f] = old.get(f) or {"kilder": [], "sikkerhed": "ukendt"}
                nodes[nid] = nn
                log["verify: node opdateret" if old else "verify: ny node"] += 1
            for r in p["edge_removals"]:
                key = (alias.get(r["from"], r["from"]), r["type"], alias.get(r["to"], r["to"]))
                if edges.pop(key, None):
                    log["verify: kant fjernet"] += 1
            for e in p["edge_upserts"]:
                f, t = alias.get(e["from"], e["from"]), alias.get(e["to"], e["to"])
                if e["type"] not in EDGE_TYPES or f == t:
                    continue
                key = (f, e["type"], t)
                old = edges.get(key, {})
                edges[key] = {"type": e["type"], "from": f, "to": t, "beskrivelse": e["beskrivelse"],
                              **({"gyldig_fra": e["gyldig_fra"]} if e.get("gyldig_fra") else {}),
                              "kilder": urls(e.get("kilder")), "sikkerhed": e["sikkerhed"],
                              "domaener": sorted(set(old.get("domaener", [])) | {dom})}
                log["verify: kant opdateret" if old else "verify: ny kant"] += 1
            for h in p.get("huller", []):
                m["huller"].append({"emne": h["emne"], "type": h["type"], "beskrivelse": h["beskrivelse"],
                                    "noder": [alias.get(x, x) for x in h.get("noder", [])], "kilder": urls(h.get("kilder")), "domaene": dom})
            m.setdefault("verify_noter", []).extend(f"[{dom}] {x}" for x in p.get("noter", []))
    # drop edges whose endpoints vanished
    for key in [k for k in edges if k[0] not in nodes or k[2] not in nodes]:
        edges.pop(key)
        log["kant uden node fjernet"] += 1

    # 2c. per-node verification (v3:<batch>) and class rules (regler)
    removed_v3 = []
    for run in cfg.get("verify3_runs", []):
        for label, res in journal(run):
            if label == "regler":
                for r in res["regler"]:
                    try:
                        val = json.loads(r["vaerdi_json"])
                    except Exception:
                        log["regel: ugyldig json"] += 1
                        continue
                    if not isinstance(val, dict):
                        continue
                    val.pop("kilder", None), val.pop("sikkerhed", None)
                    k, s = urls(r["kilder"]), r["sikkerhed"]
                    if s == "verificeret" and not k:
                        s = "sandsynlig"
                    if r["felt"] == "adgang":
                        txt = val.pop("tekst", "")
                        if not val.get("vaerdier"):
                            val["vaerdier"] = ["ELI", "HTML", "PDF"] if "ELI" in txt else ["HTML", "PDF"]
                        val["vaerdier"] = [a for a in val["vaerdier"] if a in ACCESS] or ["ukendt"]
                        val["note"] = (val.get("note", "") + " " + txt + (f" Portal: {val.pop('portal')}" if val.get("portal") else "")).strip()
                    if r["felt"] == "opdatering":
                        txt = val.pop("tekst", "")
                        val.setdefault("frekvens", "ukendt")
                        val.setdefault("versionshistorik", txt or "ukendt")
                    if r["felt"] == "licens" and "tekst" not in val:
                        val["tekst"] = json.dumps(val, ensure_ascii=False)
                    for n in nodes.values():
                        if n["type"] in r["gaelder_for"] and RANK.get(n[r["felt"]].get("sikkerhed"), 0) < RANK[s]:
                            n[r["felt"]] = {**val, "kilder": k, "sikkerhed": s, "regel": r["regel"]}
                            log[f"regel {r['regel']}: anvendt"] += 1
                continue
            if not label.startswith("v3:"):
                continue
            for u in res["felter"]:
                n = nodes.get(alias.get(u["id"], u["id"]))
                if not n:
                    log["v3: ukendt id"] += 1
                    continue
                f, k, s = u["felt"], urls(u["kilder"]), u["sikkerhed"]
                if s == "verificeret" and not k:
                    s = "sandsynlig"
                if u["handling"] == "ikke_fundet":
                    log["v3: ikke fundet"] += 1
                    continue
                if f in ("status", "ministerium"):
                    try:
                        v = json.loads(u["vaerdi_json"] or "{}").get("vaerdi")
                    except Exception:
                        v = None
                    if u["handling"] == "ret" and s == "verificeret" and v and (f == "status" and v in ("aktiv", "nedlagt", "omdøbt", "ophævet") or f == "ministerium" and (v in nodes and nodes[v]["type"] == "ministerium" or v == "ingen")):
                        if n[f] != v:
                            n["note"] = (n.get("note", "") + f" | {f} rettet fra '{n[f]}' til '{v}' ved verifikation ({u['begrundelse'][:200]})").strip(" |")
                            n[f] = v
                            log[f"v3: {f} rettet"] += 1
                    continue
                old = n.get(f) or {"kilder": [], "sikkerhed": "ukendt"}
                if u["handling"] == "bekraeft":
                    if RANK[s] > RANK.get(old.get("sikkerhed"), 0) and k:
                        old["kilder"] = urls(k + old.get("kilder", []))
                        old["sikkerhed"] = s
                        old.pop("kilde_note", None)
                        n[f] = old
                        log[f"v3: {f} bekræftet"] += 1
                    continue
                try:
                    val = json.loads(u["vaerdi_json"])
                except Exception:
                    log["v3: ugyldig json"] += 1
                    continue
                if not isinstance(val, dict) or not k:
                    log["v3: ret uden kilde/objekt"] += 1
                    continue
                val.pop("kilder", None), val.pop("sikkerhed", None)
                if f == "url" and not str(val.get("vaerdi", "")).startswith("http"):
                    continue
                if f == "adgang":
                    val["vaerdier"] = [a for a in val.get("vaerdier", []) if a in ACCESS] or ["ukendt"]
                if f == "identifikatorer":
                    keep = {kk: vv for kk, vv in old.items() if kk not in ("kilder", "sikkerhed", "kilde_note") and vv}
                    keep.update({kk: vv for kk, vv in val.items() if vv})
                    val = keep
                if RANK[s] >= RANK.get(old.get("sikkerhed"), 0):
                    n[f] = {**val, "kilder": k, "sikkerhed": s}
                    log[f"v3: {f} rettet"] += 1
            for pn in res["tidligere_navne"]:
                n = nodes.get(alias.get(pn["id"], pn["id"]))
                if not n:
                    continue
                k, s = urls(pn["kilder"]), pn["sikkerhed"]
                if s == "verificeret" and not k:
                    s = "sandsynlig"
                cur = next((p for p in n.setdefault("tidligere_navne", []) if p["navn"].strip().lower() == pn["navn"].strip().lower()), None)
                if cur is None and k:
                    n["tidligere_navne"].append({"navn": pn["navn"], "periode": pn["periode"], "kilder": k, "sikkerhed": s})
                    log["v3: tidligere navn tilføjet"] += 1
                elif cur is not None and RANK[s] >= RANK.get(cur.get("sikkerhed"), 0) and k:
                    cur.update({"periode": pn["periode"] or cur.get("periode", ""), "kilder": urls(k + cur.get("kilder", [])), "sikkerhed": s})
                    log["v3: tidligere navn opdateret"] += 1
            for ke in res["kanter"]:
                key = (alias.get(ke["from"], ke["from"]), ke["type"], alias.get(ke["to"], ke["to"]))
                e = edges.get(key)
                if not e:
                    log["v3: kant findes ikke"] += 1
                    continue
                k, s = urls(ke["kilder"]), ke["sikkerhed"]
                if s == "verificeret" and not k:
                    s = "sandsynlig"
                if ke["handling"] == "fjern":
                    if k:
                        removed_v3.append({**{x: e[x] for x in ("from", "type", "to", "beskrivelse")}, "begrundelse": ke["begrundelse"], "kilder": k})
                        edges.pop(key)
                        log["v3: kant fjernet"] += 1
                    else:
                        log["v3: fjern uden kilde ignoreret"] += 1
                elif ke["handling"] == "ret":
                    if k and RANK[s] >= RANK.get(e["sikkerhed"], 0):
                        e["beskrivelse"] = ke["beskrivelse"] or e["beskrivelse"]
                        e["kilder"], e["sikkerhed"] = urls(k + e["kilder"]), s
                        log["v3: kant rettet"] += 1
                elif RANK[s] > RANK.get(e["sikkerhed"], 0) and k:
                    e["kilder"], e["sikkerhed"] = urls(k + e["kilder"]), s
                    log["v3: kant bekræftet"] += 1
    json.dump(removed_v3, open(SP / "data" / "v3_removed_edges.json", "w"), ensure_ascii=False, indent=1)

    # 3. apply reviewed decisions on disputed edges (written by hand after review)
    decisions = json.load(open(SP / cfg["disputed_decisions"])) if cfg.get("disputed_decisions") else {}
    for d in disputed:
        key = (alias.get(d["from"], d["from"]), d["type"], alias.get(d["to"], d["to"]))
        act = decisions.get("|".join(key))
        if not act or key not in edges:
            continue
        if act == "fjern":
            edges.pop(key)
            log["bestridt: fjernet"] += 1
        elif act == "historisk":
            e = edges[key]
            if "[HISTORISK" not in e["beskrivelse"]:
                e["beskrivelse"] += f" [HISTORISK – gælder ikke pr. 2026-10-28: {d['begrundelse'][:250]}]"
            e["kilder"] = urls(e["kilder"] + d.get("kilder", []))
            log["bestridt: markeret historisk"] += 1
        elif act == "bestridt":
            e = edges[key]
            if RANK.get(e["sikkerhed"], 0) > 1:
                e["sikkerhed"] = "sandsynlig"
            e["beskrivelse"] += f" [BESTRIDT af completeness-kritiker: {d['begrundelse'][:300]}]"
            e["kilder"] = urls(e["kilder"] + d.get("kilder", []))
            m["huller"].append({"emne": f"Bestridt kant: {key[0]} {key[1]} {key[2]}", "type": "uklart",
                                "beskrivelse": d["begrundelse"][:600], "noder": [key[0], key[2]], "kilder": urls(d.get("kilder", [])), "domaene": d["kritiker"]})
            log["bestridt: markeret bestridt"] += 1
        elif act == "nedgradér":
            e = edges[key]
            e["sikkerhed"] = "ukendt"
            e["beskrivelse"] += f" [BESTRIDT af kritiker: {d['begrundelse'][:300]}]"
            e["kilder"] = urls(e["kilder"] + d.get("kilder", []))
            log["bestridt: nedgraderet"] += 1
    json.dump(disputed, open(SP / "data" / "disputed.json", "w"), ensure_ascii=False, indent=1)

    # 4. normalise
    for n in nodes.values():
        n["type"] = TYPE_FIX.get(n["type"], n["type"])
        if n["type"] not in NODE_TYPES:
            log[f"ukendt type {n['type']}"] += 1
        if n.get("ministerium") in (None, "", "ukendt") or (n["ministerium"] != "ingen" and (n["ministerium"] not in nodes or nodes[n["ministerium"]]["type"] != "ministerium")):
            n["ministerium"] = "ingen"
        if n["status"] not in RANK and n["status"] not in ("aktiv", "nedlagt", "omdøbt", "ophævet", "ukendt"):
            n["status"] = "ukendt"
        u = n["url"].get("vaerdi")
        if not (isinstance(u, str) and u.startswith("http")):
            n["url"]["vaerdi"] = "ikke relevant" if u == "ikke relevant" else "ikke fundet"
        for p in n.get("tidligere_navne", []):
            if p.get("efterfoelger") and p["efterfoelger"] not in nodes:
                p["note"] = (p.get("note", "") + f" (efterfølger-id '{p['efterfoelger']}' ikke i registry)").strip()
                p.pop("efterfoelger")
            sweep(p)
        for d in n["dokumenttyper"].get("liste", []):
            if d.get("bindende") not in ("bindende", "vejledende", "blandet", "ukendt"):
                d["bindende"] = "ukendt"
        if n.get("ingest"):
            for f in ("vaerdi", "besvaer"):
                n["ingest"][f] = max(1, min(5, int(n["ingest"][f])))
        for f in ("hjemmel", "dokumenttyper", "url", "adgang", "identifikatorer", "licens", "opdatering"):
            sweep(n[f])
        if isinstance(n["url"].get("vaerdi"), str) and n["url"]["vaerdi"].startswith("http"):
            n["url"]["vaerdi"] = n["url"]["vaerdi"].strip().replace(" ", "%20")
        if n.get("baseline"):
            n["baseline"]["kilder"] = urls(n["baseline"]["kilder"])
    for e in edges.values():
        e.setdefault("domaener", [])
        sweep(e)

    m["nodes"] = [{k: n[k] for k in ORDER if k in n} for n in sorted(nodes.values(), key=lambda n: n["id"])]
    m["edges"] = sorted(edges.values(), key=lambda e: (e["type"], e["from"], e["to"]))
    m["huller"] = [{**h, "noder": [x for x in h["noder"] if x in nodes], "kilder": urls(h["kilder"])} for h in m["huller"]]
    json.dump(m, open(SP / "data" / "final.json", "w"), ensure_ascii=False, indent=1)
    print(json.dumps({"noder": len(m["nodes"]), "kanter": len(m["edges"]), "bestridte": len(disputed), **log}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main(json.load(open(sys.argv[1])))
