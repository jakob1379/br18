#!/usr/bin/env python3
"""Replace raw huller in data/final.json with the consolidated list from the dk-reg-huller workflow."""
import json
import sys
from pathlib import Path

SP = Path(__file__).resolve().parent
WF = Path("/root/.claude/projects/-home-user-ai-job-search-fork/9c9ad245-1536-5d87-980d-1a4837c57ed1/subagents/workflows")

run = sys.argv[1]
rows = [json.loads(l) for l in open(WF / run / "journal.jsonl")]
results = [r["result"] for r in rows if r["type"] == "result" and r.get("result")]
raw = json.load(open(SP / "data" / "huller_raw.json"))
m = json.load(open(SP / "data" / "final.json"))
ids = {n["id"] for n in m["nodes"]}
rawsrc = {i: h for i, h in enumerate(m["huller"])}  # same order as huller_raw (last raw item is the hand-added one)

merged: dict[str, dict] = {}
for res in results:
    for h in res["huller"]:
        key = h["emne"].strip().lower()
        cur = merged.setdefault(key, {"emne": h["emne"], "type": h["type"], "beskrivelse": h["beskrivelse"], "raa": []})
        if cur["beskrivelse"] != h["beskrivelse"] and h["beskrivelse"] not in cur["beskrivelse"]:
            cur["beskrivelse"] += " " + h["beskrivelse"]
        cur["raa"] += h["raa_indeks"]

placed = {i for h in merged.values() for i in h["raa"]}
out = []
for h in merged.values():
    idx = sorted(set(i for i in h["raa"] if 0 <= i < len(raw)))
    noder, kilder, dom, emner = [], [], [], []
    for i in idx:
        r = raw[i]
        noder += [x for x in r["noder"] if x in ids and x not in noder]
        src = rawsrc.get(i, {}).get("kilder", []) if i < len(m["huller"]) else []
        kilder += [k for k in src if k not in kilder]
        if r.get("domaene") and r["domaene"] not in dom:
            dom.append(r["domaene"])
        emner.append(r["emne"])
    out.append({"emne": h["emne"], "type": h["type"], "beskrivelse": h["beskrivelse"], "noder": noder, "kilder": kilder,
                "domaener": dom, "oprindelige_emner": list(dict.fromkeys(emner))})
unplaced = [r for r in raw if r["i"] not in placed]
for r in unplaced:  # never drop a gap silently
    out.append({"emne": r["emne"], "type": r["type"], "beskrivelse": r["beskrivelse"], "noder": [x for x in r["noder"] if x in ids],
                "kilder": rawsrc.get(r["i"], {}).get("kilder", []), "domaener": [r["domaene"]] if r.get("domaene") else [], "oprindelige_emner": [r["emne"]]})
order = ["betalingsmur", "kun-pdf", "ingen-api", "uklart", "ikke-fundet", "andet"]
out.sort(key=lambda h: (order.index(h["type"]) if h["type"] in order else 9, h["emne"].lower()))
m["huller"] = out
json.dump(m, open(SP / "data" / "final.json", "w"), ensure_ascii=False, indent=1)
print(f"{len(raw)} rå → {len(out)} konsoliderede huller ({len(unplaced)} uplacerede bevaret som egne poster)")
