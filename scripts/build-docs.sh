#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
site_dir="${SITE_DIR:-site}"

cd "$repo_root"

query_files="$(find docs -name '*\?*')"
if [[ -n "$query_files" ]]; then
  printf 'corpus filenames contain URL query strings:\n%s\n' "$query_files" >&2
  exit 1
fi

uv run zensical build --strict

root_dir="$(cd "$site_dir" && pwd)"

network_flag=(--offline)
if [[ "${CHECK_EXTERNAL_LINKS:-}" == 1 ]]; then
  network_flag=()
fi

lychee \
  "${network_flag[@]}" \
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
