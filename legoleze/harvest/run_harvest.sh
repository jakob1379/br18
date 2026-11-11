#!/usr/bin/env bash
# Start (or resume) the Retsinformation harvest in the background. Usage: ./run_harvest.sh [SEED_DIR]
# Stop: kill "$(cat data/harvest.pid)". Progress: tail -f data/harvest.log ; python3 harvest.py status
set -euo pipefail
cd "$(dirname "$0")"; mkdir -p data
SEED="${1:-/home/user/ansvar-systems/danish-law-mcp/data/seed}"
python3 -I harvest.py probe
nohup python3 -I harvest.py run --seed-dir "$SEED" >> data/harvest.out 2>&1 &
echo $! > data/harvest.pid; echo "høst kører (pid $(cat data/harvest.pid)); log: data/harvest.log"
