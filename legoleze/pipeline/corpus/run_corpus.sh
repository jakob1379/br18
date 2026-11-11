#!/usr/bin/env bash
# Seed files (Ansvar-Systems/danish-law-mcp data/seed) -> corpus/data/{docs.jsonl,prefixes.json,udsteder.json} + Haiku job batches.
set -euo pipefail
cd "$(dirname "$0")"
python3 -I extract.py "$1"
python3 -I prefixes.py >/dev/null
python3 -I udsteder.py
python3 -I make_jobs.py
