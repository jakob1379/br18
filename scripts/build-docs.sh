#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
site_dir="${SITE_DIR:-site}"

cd "$repo_root"

uv run zensical build

root_dir="$(cd "$site_dir" && pwd)"

lychee \
  --include-fragments \
  --root-dir "$root_dir" \
  --index-files index.html \
  --fallback-extensions html \
  --exclude '^file://.*/site/404\.html#__skip$' \
  --exclude '^file://.*/site/external/' \
  --exclude '^file://.*/site/historisk/' \
  --exclude '^https://brandogkonstruktioner\.dk/' \
  --exclude '^https://www\.brandogkonstruktioner\.dk/' \
  --exclude '^https?://historisk\.bygningsreglementet\.dk/' \
  --exclude '^https://www\.radonguiden\.dk/' \
  --exclude '^https://build\.dk/Pages/Vejledning-om-haandtering-af-fugt-i-bygninger\.aspx$' \
  "$site_dir/**/*.html"
