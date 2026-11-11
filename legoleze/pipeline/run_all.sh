#!/usr/bin/env bash
# Full rebuild: journals -> registry.yaml + katalog/ -> views + HTML. Usage: run_all.sh <huller-run-id> [ressort-run-id ...]
# Corpus pre-processing (seed files -> corpus/data/*.json) is separate: corpus/run_corpus.sh <seed-dir>
set -euo pipefail
cd "$(dirname "$0")"
HULLER="$1"; shift
python3 merge.py data/cfg.json >/dev/null
python3 finalize.py data/cfg_final.json >/dev/null
python3 seen_urls.py
python3 provenance.py >/dev/null
python3 manual_fixes.py
python3 consolidate_huller.py "$HULLER"
python3 -I corpus/resolve.py >/dev/null
if [ "$#" -gt 0 ]; then python3 -I corpus/ressort_import.py "$@"; fi
python3 -I corpus/ressort_quality.py
python3 -I registry_sync.py
python3 write_registry.py
python3 -I corpus/katalog.py
python3 write_readme.py
python3 dk-regulering/scripts/build.py
python3 dk-regulering/scripts/build.py --check
python3 -I viz_prep.py
python3 -I viz_kat.py
python3 -I viz_build.py
python3 -I coverage_prep.py >/dev/null
python3 -I dash_prep.py
