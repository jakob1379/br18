#!/usr/bin/env python3
"""katalog/*.jsonl -> data/viz_kat.json (compact, gældende docs only) for the HTML explorer."""
import json
from collections import Counter, defaultdict
from pathlib import Path
SP = Path(__file__).resolve().parent
KD = SP / "dk-regulering" / "katalog"
docs = [json.loads(l) for l in open(KD / "retsinformation_lta.jsonl", encoding="utf-8")]
gd = {d["id"]: d for d in docs if d["status"]["vaerdi"] == "gældende"}
refs = defaultdict(list); eus = defaultdict(list)
for l in open(KD / "kanter.jsonl", encoding="utf-8"):
    e = json.loads(l)
    if e["from"] not in gd: continue
    if e["type"] == "henviser_til" and e["to"].startswith("lta-") and e.get("beskrivelse", "").startswith("nævner loven"):
        refs[e["from"]].append((e.get("gaeldende_version") or e["to"], e["sikkerhed"]))  # show the version in force today
    elif e["to"].startswith("eu-"):
        eus[e["from"]].append((e["to"], e["type"] == "implementerer_EU"))
CERT = ["verificeret", "sandsynlig", "ukendt"]
types, udst, mins, omr = [], [], [], []
def ix(lst, v):
    if v not in lst: lst.append(v)
    return lst.index(v)
bad_url = 0; rows = []
for d in sorted(gd.values(), key=lambda d: (d["datoer"].get("udstedt") or ""), reverse=True):
    y, n = d["id"][4:].split("-")
    if d["kilder"] != [f"https://www.retsinformation.dk/eli/lta/{y}/{n}/xml"]: bad_url += 1
    m = d.get("ministerium") or {"vaerdi": "ikke klassificeret", "sikkerhed": "ukendt"}
    rows.append([d["id"][4:], d["navn"], ix(types, d["type"]), d["datoer"].get("udstedt") or "", ix(udst, d["udstedt_af"]["vaerdi"]),
                 CERT.index(d["udstedt_af"]["sikkerhed"]), ix(mins, m["vaerdi"]), CERT.index(m["sikkerhed"]), ix(omr, d.get("retsomraade") or "ikke klassificeret"),
                 ",".join(d.get("registry_ids") or []),
                 ",".join(t[4:] + ("" if c == "verificeret" else "~") for t, c in refs[d["id"]][:8]),
                 ",".join(t[3:] + ("*" if imp else "") for t, imp in eus[d["id"]][:8]),
                 ",".join(t[4:] for t in (d.get("aendrer") or [])[:6]),
                 d["identifikatorer"]["lovtidende"] or ""])
out = {"n_total": len(docs), "n_hist": len(docs) - len(gd), "pr": max(d["status"]["pr"] or "" for d in docs), "max_udstedt": max(d["datoer"].get("udstedt") or "" for d in docs),
       "types": types, "udst": udst, "mins": mins, "omr": omr, "rows": rows,
       "n_edges": sum(1 for _ in open(KD / "kanter.jsonl", encoding="utf-8")), "n_eu": sum(1 for _ in open(KD / "eu_index.jsonl", encoding="utf-8"))}
assert bad_url == 0, f"{bad_url} kilde-URL'er følger ikke datasættets ELI-XML-mønster"
s = json.dumps(out, ensure_ascii=False, separators=(",", ":"))
(SP / "data" / "viz_kat.json").write_text(s, encoding="utf-8")
print(len(s), "bytes", len(rows), "rows", Counter(r[7] for r in rows))
