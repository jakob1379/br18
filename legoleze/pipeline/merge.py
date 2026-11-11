#!/usr/bin/env python3
"""Merge baseline + per-domain research/patches (from workflow journals) into registry.yaml."""
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import yaml

SP = Path(__file__).resolve().parent
WF = Path("/root/.claude/projects/-home-user-ai-job-search-fork/9c9ad245-1536-5d87-980d-1a4837c57ed1/subagents/workflows")
OUT = SP / "dk-regulering" / "registry.yaml"
RANK = {"verificeret": 2, "sandsynlig": 1, "ukendt": 0}
CLAIMS = ("hjemmel", "dokumenttyper", "url", "adgang", "identifikatorer", "licens", "opdatering")
EMPTY = {
    "hjemmel": {"tekst": "ikke undersøgt"},
    "dokumenttyper": {"liste": []},
    "url": {"vaerdi": "ikke fundet"},
    "adgang": {"vaerdier": ["ukendt"]},
    "identifikatorer": {},
    "licens": {"tekst": "ikke undersøgt"},
    "opdatering": {"frekvens": "ukendt", "versionshistorik": "ukendt"},
}
TYPE_MAP = [
    (r"^ministerium", "ministerium"), (r"klageinstans|klagenævn", "klagenævn"), (r"^nævn", "nævn"),
    (r"direktorat", "direktorat"), (r"^styrelse|forvaltningsmyndighed", "styrelse"), (r"^tilsyn", "tilsyn"),
    (r"^råd", "råd"), (r"fond", "fond"), (r"ombudsmand", "ombudsmand"), (r"domstol", "domstol"),
    (r"offentlig virksomhed|partnerskab|offentlig myndighed", "offentlig-virksomhed"),
]


def journal_results(run_dirs):
    """Yield (label, result) for every completed agent in the given workflow run dirs."""
    for d in run_dirs:
        rows = [json.loads(l) for l in open(WF / d / "journal.jsonl")]
        labels = {r["agentId"]: r["label"] for r in rows if r["type"] == "started"}
        for r in rows:
            if r["type"] == "result" and r.get("result"):
                yield labels.get(r["agentId"], "?"), r["result"]


def norm_type(t):
    for pat, val in TYPE_MAP:
        if re.search(pat, t):
            return val
    return t


def claim(c, default):
    c = dict(c) if isinstance(c, dict) else {}
    for k, v in default.items():
        c.setdefault(k, v)
    c["kilder"] = [k for k in (c.get("kilder") or []) if isinstance(k, str) and k.startswith("http")]
    if c.get("sikkerhed") not in RANK:
        c["sikkerhed"] = "ukendt"
    if c["sikkerhed"] == "verificeret" and not c["kilder"]:
        c["sikkerhed"] = "sandsynlig"
    return c


def baseline_nodes(c):
    nodes, edges = [], []
    for m in c["ministerier"]:
        nedlagt = "nedlagt" in m["navn"]
        nodes.append({
            "id": m["id"], "navn": re.sub(r"\s*\(nedlagt[^)]*\)", "", m["navn"]), "type": "ministerium",
            "ministerium": "ingen", "status": "nedlagt" if nedlagt else "aktiv",
            "tidligere_navne": m["tidligere_navne"],
            "hjemmel": {"tekst": "Kongelig resolution; forretningsfordeling jf. BEK nr. 514 af 08/06/2026 om forretningernes fordeling mellem ministrene" if not nedlagt else "Nedlagt ved kongelig resolution",
                        "kilder": [k for k in m["kilder"] if "514" in k or "256544" in k or "kgl-resolution" in k][:3],
                        "sikkerhed": "verificeret" if not nedlagt and any("514" in k or "256544" in k for k in m["kilder"]) else "sandsynlig"},
            "note": (f"Minister pr. 2026-10-28: {m['minister']}. " if not nedlagt else "") + (m.get("note") or ""),
            "_kilder": m["kilder"], "_sikkerhed": m["sikkerhed"], "_domaener": ["baseline"],
        })
    for i in c["instanser"]:
        nodes.append({
            "id": i["id"], "navn": i["navn"], "type": norm_type(i["type"]), "ministerium": i["ministerium_id"],
            "status": i["status"], "tidligere_navne": i["tidligere_navne"],
            "note": i.get("note") or "", "_kilder": i["kilder"], "_sikkerhed": i["sikkerhed"], "_domaener": ["baseline"],
            "_hjemmesider": i.get("hjemmesider_set") or [],
        })
        if i["ministerium_id"] not in ("ingen", None):
            edges.append({"from": i["ministerium_id"], "to": i["id"], "type": "ressortansvar",
                          "beskrivelse": "Organisatorisk ressortansvar (baseline pr. 2026-10-28)" + (f" – instansen er {i['status']}" if i["status"] != "aktiv" else ""),
                          "kilder": i["kilder"][:4], "sikkerhed": i["sikkerhed"], "_domaener": ["baseline"]})
    return nodes, edges


def best(claims):
    return max(claims, key=lambda c: (RANK[c["sikkerhed"]], len(c["kilder"])))


def merge_nodes(group, alias):
    out = {"id": group[0]["id"]}
    base = [n for n in group if "baseline" in n.get("_domaener", [])]
    pref = base[0] if base else group[0]
    for f in ("navn", "type", "ministerium", "status"):
        vals = [n.get(f) for n in group if n.get(f) not in (None, "", "ukendt")]
        if base and pref.get(f) not in (None, "", "ukendt"):
            out[f] = pref[f]
        else:
            out[f] = Counter(vals).most_common(1)[0][0] if vals else (group[0].get(f) or "ukendt")
    out["ministerium"] = alias.get(out["ministerium"], out["ministerium"])
    prev = {}
    for n in group:
        for p in n.get("tidligere_navne") or []:
            p = claim(p, {})
            if p.get("efterfoelger"):
                p["efterfoelger"] = alias.get(p["efterfoelger"], p["efterfoelger"])
            k = p["navn"].strip().lower()
            if k not in prev or RANK[p["sikkerhed"]] > RANK[prev[k]["sikkerhed"]]:
                prev[k] = p
    out["tidligere_navne"] = list(prev.values())
    for f in CLAIMS:
        cs = [claim(n[f], EMPTY[f]) for n in group if isinstance(n.get(f), dict)]
        if not cs:
            # baseline-only nodes: hjemmesider seen become url candidates is NOT done (no guessing); mark unknown.
            out[f] = claim({}, EMPTY[f])
            continue
        b = dict(best(cs))
        if f == "adgang":
            vals = []
            for c in cs:
                if RANK[c["sikkerhed"]] >= RANK[b["sikkerhed"]]:
                    vals += [v for v in c.get("vaerdier") or [] if v not in vals]
            if len(vals) > 1:
                vals = [v for v in vals if v != "ukendt"]
            b["vaerdier"] = vals or ["ukendt"]
        same = [c for c in cs if {k: v for k, v in c.items() if k not in ("kilder", "sikkerhed")} == {k: v for k, v in b.items() if k not in ("kilder", "sikkerhed")}]
        b["kilder"] = list(dict.fromkeys(k for c in same for k in c["kilder"]))
        out[f] = b
    out["krydsref_moenstre"] = list(dict.fromkeys(x for n in group for x in n.get("krydsref_moenstre") or []))
    ing = [n["ingest"] for n in group if n.get("ingest")]
    pick = [n["ingest"] for n in group if n.get("ingest") and "datakilder-standarder" in n.get("_domaener", [])]
    if pick or ing:
        g = (pick or ing)
        out["ingest"] = {"vaerdi": round(sum(x["vaerdi"] for x in g) / len(g)), "besvaer": round(sum(x["besvaer"] for x in g) / len(g)),
                         "begrundelse": " / ".join(dict.fromkeys(x.get("begrundelse", "") for x in g if x.get("begrundelse")))}
    notes = list(dict.fromkeys(n.get("note", "").strip() for n in group if n.get("note", "").strip()))
    out["note"] = " | ".join(notes)
    out["domaener"] = sorted({d for n in group for d in n.get("_domaener", [])} - {"baseline"}) or ["baseline"]
    # baseline-level sources: attach to note-less fields only via 'kilder_baseline'
    kb = list(dict.fromkeys(k for n in group for k in n.get("_kilder", [])))
    if kb:
        out["baseline"] = {"kilder": kb[:6], "sikkerhed": max((n.get("_sikkerhed", "ukendt") for n in group if n.get("_sikkerhed")), key=lambda s: RANK[s], default="ukendt")}
    return out


def main(domain_runs, baseline_run, alias_file=None):
    alias = json.load(open(alias_file)) if alias_file else {}
    bl = None
    for label, res in journal_results([baseline_run]):
        if label.startswith("C:"):
            bl = res
    nodes_all, edges_all = baseline_nodes(bl)
    huller, noter = [], []
    research, patches = {}, {}
    for label, res in journal_results(domain_runs):
        kind, _, key = label.partition(":")
        if kind == "research":
            research[key] = res
        elif kind == "consolidate":
            patches[key] = res
    report = {"domæner": sorted(research), "uden_patch": sorted(set(research) - set(patches))}
    for key, res in research.items():
        nodes = {n["id"]: n for n in res["nodes"]}
        edges = {(e["from"], e["type"], e["to"]): e for e in res["edges"]}
        hl = list(res.get("huller", []))
        p = patches.get(key)
        if p:
            for r in p["node_removals"]:
                nodes.pop(r["id"], None)
            for n in p["node_upserts"]:
                nodes[n["id"]] = n
            for r in p["edge_removals"]:
                edges.pop((r["from"], r["type"], r["to"]), None)
            for e in p["edge_upserts"]:
                edges[(e["from"], e["type"], e["to"])] = e
            hl += p.get("huller", [])
            noter += [f"[{key}] {x}" for x in p.get("noter", [])]
        noter += [f"[{key}] {x}" for x in res.get("noter", [])]
        for n in nodes.values():
            n["_domaener"] = [key]
            nodes_all.append(n)
        for e in edges.values():
            e["_domaener"] = [key]
            edges_all.append(e)
        for h in hl:
            h["_domaene"] = key
            huller.append(h)

    # alias + group
    groups = defaultdict(list)
    for n in nodes_all:
        n["id"] = alias.get(n["id"], n["id"])
        groups[n["id"]].append(n)
    merged = {nid: merge_nodes(g, alias) for nid, g in groups.items()}

    eg = defaultdict(list)
    for e in edges_all:
        e["from"], e["to"] = alias.get(e["from"], e["from"]), alias.get(e["to"], e["to"])
        if e["from"] == e["to"]:
            continue
        eg[(e["from"], e["type"], e["to"])].append(e)
    edges = []
    dangling = Counter()
    for (f, t, to), g in eg.items():
        if f not in merged or to not in merged:
            for x in (f, to):
                if x not in merged:
                    dangling[x] += 1
            continue
        cs = [claim(e, {}) for e in g]
        b = best(cs)
        edges.append({"type": t, "from": f, "to": to, "beskrivelse": b.get("beskrivelse", ""),
                      **({"gyldig_fra": b["gyldig_fra"]} if b.get("gyldig_fra") else {}),
                      "kilder": list(dict.fromkeys(k for c in cs for k in c["kilder"])), "sikkerhed": b["sikkerhed"],
                      "domaener": sorted({d for e in g for d in e.get("_domaener", [])})})
    # parent refs
    bad_parent = Counter()
    for n in merged.values():
        if n["ministerium"] not in ("ingen", None) and (n["ministerium"] not in merged or merged[n["ministerium"]]["type"] != "ministerium"):
            bad_parent[n["ministerium"]] += 1
    hu, seen = [], set()
    for h in huller:
        k = h["emne"].strip().lower()
        if k in seen:
            continue
        seen.add(k)
        hu.append({"emne": h["emne"], "type": h["type"], "beskrivelse": h["beskrivelse"],
                   "noder": [alias.get(x, x) for x in h.get("noder", []) if alias.get(x, x) in merged],
                   "kilder": [k for k in h.get("kilder", []) if k.startswith("http")], "domaene": h["_domaene"]})
    report.update(noder=len(merged), kanter=len(edges), huller=len(hu), dangling=dangling.most_common(), bad_parent=bad_parent.most_common())
    json.dump({"nodes": list(merged.values()), "edges": edges, "huller": hu, "noter": noter, "baseline": bl}, open(SP / "data" / "merged.json", "w"), ensure_ascii=False, indent=1)
    json.dump(report, open(SP / "data" / "merge_report.json", "w"), ensure_ascii=False, indent=1)
    print(json.dumps({k: (v if not isinstance(v, list) or len(v) < 40 else v[:40]) for k, v in report.items()}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    cfg = json.load(open(sys.argv[1]))
    main(cfg["domain_runs"], cfg["baseline_run"], cfg.get("alias"))
