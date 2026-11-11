#!/usr/bin/env python3
"""final.json -> data/viz_data.json (compact data embedded in the HTML explorer)."""
import json
from pathlib import Path
SP = Path(__file__).resolve().parent
m = json.load(open(SP / "data" / "final.json"))
bl = m["baseline"]
CF = ("hjemmel", "dokumenttyper", "url", "adgang", "identifikatorer", "licens", "opdatering")
def c(x):
    x = dict(x); x.pop("kilde_note", None) if False else None
    return x
KRIT = {"kritik:byggeri-bolig": ["byggeri", "bolig"], "kritik:plan-kultur-kommunalt": ["plan", "kommunalt"],
        "kritik:energi-forsyning": ["energi"], "kritik:miljoe-natur": ["miljoe", "natur-vand-kyst"],
        "kritik:arbejdsmiljoe-brand-elgasvvs": ["arbejdsmiljoe", "brand", "el-gas-vvs"],
        "kritik:klage-praksis-kilder-eu": ["klage-tilsyn-praksis", "datakilder-standarder", "eu"]}
REAL = {"byggeri", "bolig", "plan", "kommunalt", "energi", "miljoe", "natur-vand-kyst", "arbejdsmiljoe", "brand", "el-gas-vvs",
        "klage-tilsyn-praksis", "eu", "datakilder-standarder", "baseline"}
def doms(ds):
    """Only real research domains; critic tags are kept apart (see kritik())."""
    return [d for d in dict.fromkeys(ds) if d in REAL]
def kritik(ds):
    return [d.split(":", 1)[-1] for d in ds if d.startswith("kritik:") or ("kritik:" + d) in KRIT]
def hdoms(ds):
    """Gap domains: expand critic-cluster slugs (with or without prefix) to the domains they cover."""
    out = []
    for d in ds:
        for x in KRIT.get(d, KRIT.get("kritik:" + d, [d])):
            if x not in out:
                out.append(x)
    return out
nodes = []
for n in m["nodes"]:
    o = {"id": n["id"], "navn": n["navn"], "type": n["type"], "min": n["ministerium"], "status": n["status"],
         "dom": doms(n.get("domaener", [])), "kritiker": kritik(n.get("domaener", [])), "prev": n.get("tidligere_navne", []), "kx": n.get("krydsref_moenstre", []),
         "note": n.get("note", ""), "kat": n.get("katalog_id")}
    for f in CF:
        o[f] = n[f]
    if n.get("ingest"):
        o["ingest"] = n["ingest"]
    nodes.append(o)
edges = [[e["from"], e["to"], e["type"], e["sikkerhed"], e.get("beskrivelse", ""), e.get("kilder", []), doms(e.get("domaener", []))] for e in m["edges"]]
huller = [{k: h[k] for k in ("emne", "type", "beskrivelse", "noder", "kilder") if k in h} | {"domaener": hdoms(h.get("domaener", []))} for h in m["huller"]]
out = {"dato": "2026-10-28", "regering": {k: bl["regering"][k] for k in ("navn", "dannet", "partier", "kilder", "sikkerhed")},
       "ressortomlaegninger": bl["ressortomlaegninger"], "omraader": bl["omraader"], "konflikter": bl["uafklarede_konflikter"],
       "nodes": nodes, "edges": edges, "huller": huller,
       "prov": json.load(open(SP / "data" / "provenance_stats.json"))}
s = json.dumps(out, ensure_ascii=False, separators=(",", ":"))
(SP / "data" / "viz_data.json").write_text(s, encoding="utf-8")
print(len(s), "bytes", len(nodes), "nodes", len(edges), "edges")
