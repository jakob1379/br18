#!/usr/bin/env python3
"""Per-retsområde coverage facts from registry + katalog -> data/coverage.json (input to the Opus audit and the heatmap)."""
import json
from collections import Counter, defaultdict
from pathlib import Path
SP = Path(__file__).resolve().parent
KD = SP / "dk-regulering" / "katalog"
AREAS = ["statsret", "kommuner", "valg", "international", "forsvar", "beredskab-brand", "strafferet-politi", "retspleje", "familie-person", "erhvervsret", "finansiel", "skat",
         "offentlig-oekonomi", "arbejdsmarked", "arbejdsmiljoe", "social", "aeldre", "boern-dagtilbud", "sundhed", "undervisning", "forskning-videregaaende", "kultur-medier", "kirke",
         "udlaendinge", "transport", "soefart", "plan-landdistrikter", "byggeri", "bolig", "energi-forsyning", "klima", "el-gas-vvs", "miljoe", "affald", "natur-vandmiljoe",
         "landbrug-dyr", "foedevarer", "fiskeri", "digitalisering-tele", "persondata", "forbruger-konkurrence", "andet"]
DOM2AREA = {"byggeri": ["byggeri"], "bolig": ["bolig"], "plan": ["plan-landdistrikter"], "energi": ["energi-forsyning", "klima"], "miljoe": ["miljoe", "affald"],
            "natur-vand-kyst": ["natur-vandmiljoe"], "arbejdsmiljoe": ["arbejdsmiljoe"], "brand": ["beredskab-brand"], "el-gas-vvs": ["el-gas-vvs"]}
INST = {"styrelse", "direktorat", "nævn", "klagenævn", "tilsyn", "råd", "fond", "domstol", "ombudsmand", "offentlig-virksomhed", "kommune", "region"}
PRAKSIS = {"klagenævn", "nævn", "domstol", "ombudsmand", "praksissamling"}
reg = json.load(open(SP / "data" / "final.json"))
nodes = {n["id"]: n for n in reg["nodes"]}
def areas_of(n):
    out = set()
    for d in n.get("domaener") or []:
        out.update(DOM2AREA.get(d.split(":")[-1], []))
    return out
F = {a: {"katalog": Counter(), "katalog_typer": Counter(), "reg_noder": Counter(), "reg_kanter": Counter(), "reg_huller": 0} for a in AREAS}
for n in reg["nodes"]:
    for a in areas_of(n):
        t = n["type"]
        F[a]["reg_noder"]["instanser" if t in INST else t] += 1
        if t in PRAKSIS: F[a]["reg_noder"]["praksis"] += 1
for e in reg["edges"]:
    aa = areas_of(nodes[e["from"]]) | areas_of(nodes[e["to"]])
    for a in aa: F[a]["reg_kanter"][e["type"]] += 1
for h in reg["huller"]:
    for a in {x for d in h.get("domaener") or [] for x in DOM2AREA.get(d.split(":")[-1], [])}: F[a]["reg_huller"] += 1
docs = [json.loads(l) for l in open(KD / "retsinformation_lta.jsonl", encoding="utf-8")]
refs = Counter(); eu = Counter(); edges_from = defaultdict(set)
for l in open(KD / "kanter.jsonl", encoding="utf-8"):
    e = json.loads(l)
    edges_from[e["from"]].add("eu" if e["to"].startswith("eu-") else ("lov" if e["type"] == "henviser_til" and e["to"].startswith("lta-") else e["type"]))
gd = [d for d in docs if d["status"]["vaerdi"] == "gældende"]
uncl = 0
for d in gd:
    a = d.get("retsomraade")
    if not a: uncl += 1; continue
    k = F.setdefault(a, {"katalog": Counter(), "katalog_typer": Counter(), "reg_noder": Counter(), "reg_kanter": Counter(), "reg_huller": 0})
    c = k["katalog"]; c["gaeldende"] += 1; k["katalog_typer"][d["type"]] += 1
    c["ressort_sandsynlig"] += (d.get("ministerium") or {}).get("sikkerhed") == "sandsynlig"
    c["udsteder_kendt"] += d["udstedt_af"]["vaerdi"] != "ukendt"
    c["med_lovhenvisning"] += "lov" in edges_from[d["id"]]
    c["med_eu"] += "eu" in edges_from[d["id"]] or "implementerer_EU" in edges_from[d["id"]]
    c["i_registry"] += bool(d.get("registry_ids"))
    c["regulering"] += d["type"] in ("bekendtgørelse", "ændringsbekendtgørelse", "ikrafttrædelsesbekendtgørelse", "anordning", "ændringsanordning", "ikrafttrædelsesanordning", "bekendtgørelse-af-anordning")
    c["love"] += d["type"] in ("lov", "lovbekendtgørelse", "ændringslov")
out = {"genereret_af": "coverage_prep.py", "katalog": {"dokumenter": len(docs), "gaeldende": len(gd), "endnu_ikke_klassificeret": uncl, "klassificeret": len(gd) - uncl,
       "max_udstedt": max(d["datoer"].get("udstedt") or "" for d in docs), "status_pr": max(d["status"]["pr"] or "" for d in docs)},
       "registry": {"noder": len(reg["nodes"]), "kanter": len(reg["edges"]), "huller": len(reg["huller"])},
       "omraader": {a: {"katalog": dict(F[a]["katalog"]), "katalog_typer": dict(F[a]["katalog_typer"]), "registry_noder": dict(F[a]["reg_noder"]),
                        "registry_kanter": dict(F[a]["reg_kanter"]), "registry_huller": F[a]["reg_huller"], "registry_domaene": any(a in v for v in DOM2AREA.values())} for a in F}}
(SP / "data" / "coverage.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps(out["katalog"], ensure_ascii=False)); print({a: (v["katalog"].get("gaeldende", 0), sum(v["registry_noder"].values())) for a, v in out["omraader"].items()})
