#!/usr/bin/env bash
# Regenerate everything derived from dk-regulering/registry.yaml: final.json, README.md, the build.py views and the map.
# The generators expect the folder layout of the session that wrote them, so it is rebuilt in a temp dir. Needs PyYAML.
set -euo pipefail
L="$(cd "$(dirname "$0")/.." && pwd)"
SP="$(mktemp -d)"
trap 'rm -rf "$SP"' EXIT
mkdir -p "$SP/data" "$SP/corpus"
cp "$L"/pipeline/{write_readme.py,viz_prep.py,viz_build.py,viz_template.html,viz_script.js} "$SP/"
cp "$L"/audit/{provenance_stats.json,ressort_quality.json} "$L"/intermediate/registry/{viz_pos.json,viz_kat.json} "$SP/data/"
ln -s "$L/dk-regulering" "$SP/dk-regulering"
ln -s "$L/dashboard" "$SP/dash"
ln -s "$L/intermediate/corpus" "$SP/corpus/data"
python3 - "$L" "$SP" <<'PY'
import json, sys, yaml
L, SP = sys.argv[1:]
reg = yaml.load(open(f"{L}/dk-regulering/registry.yaml", encoding="utf-8"), Loader=yaml.CSafeLoader)
final = json.load(open(f"{L}/intermediate/registry/final.json", encoding="utf-8"))
final.update(nodes=reg["nodes"], edges=reg["edges"], huller=reg["huller"], opdateret=reg["meta"]["opdateret"])
final["baseline"].update({k: reg[k] for k in ("regering", "ressortomlaegninger", "uafklarede_konflikter")})
json.dump(final, open(f"{SP}/data/final.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
PY
python3 "$SP/write_readme.py"
python3 "$L/dk-regulering/scripts/build.py"
python3 "$SP/viz_prep.py"
python3 "$SP/viz_build.py"
cp "$SP"/data/{final.json,viz_data.json} "$L/intermediate/registry/"
