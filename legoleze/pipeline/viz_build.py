#!/usr/bin/env python3
import json
from pathlib import Path
SP = Path(__file__).resolve().parent
tpl = (SP / "viz_template.html").read_text(encoding="utf-8")
data = (SP / "data" / "viz_data.json").read_text(encoding="utf-8").replace("</", "<\\/").replace("<!--", "\\u003c!--")
P = json.loads((SP / "data" / "viz_pos.json").read_text(encoding="utf-8"))
D = json.loads((SP / "data" / "viz_data.json").read_text(encoding="utf-8"))
for k, n in enumerate(x for x in D["nodes"] if x["id"] not in P):  # nodes added after the fcose layout: place next to a positioned neighbour
    nb = next((e[1] if e[0] == n["id"] else e[0] for e in D["edges"] if n["id"] in (e[0], e[1]) and (e[1] if e[0] == n["id"] else e[0]) in P), None)
    if not nb and n["type"] == "dokumentkilde" and "kilde-retsinformation" in P: nb = "kilde-retsinformation"  # isolated source nodes sit beside Retsinformation
    bx, by = P[nb] if nb else (0, 0)
    P[n["id"]] = [bx + 45 + 10 * k, by + 35]
pos = json.dumps(P)
script = (SP / "viz_script.js").read_text(encoding="utf-8")
kat = (SP / "data" / "viz_kat.json").read_text(encoding="utf-8").replace("</", "<\\/").replace("<!--", "\\u003c!--")
out = tpl.replace("__SCRIPT__", script).replace("__DATA__", data).replace("__POS__", pos).replace("__KAT__", kat)
(SP / "dk-regulering" / "reguleringskort.html").write_text(out, encoding="utf-8")
print(len(out))
