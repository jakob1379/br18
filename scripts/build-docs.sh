#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
site_dir="${SITE_DIR:-site}"

cd "$repo_root"

collisions="$(find docs | LC_ALL=C sort -f | LC_ALL=C uniq -Di)"
if [[ -n "$collisions" ]]; then
  echo "case-insensitive path collisions in docs/:" >&2
  echo "$collisions" >&2
  exit 1
fi

query_files="$(find docs -name '*\?*')"
if [[ -n "$query_files" ]]; then
  printf 'corpus filenames contain URL query strings:\n%s\n' "$query_files" >&2
  exit 1
fi

pandoc_tables="$(rg -l --glob '*.md' -e '^\+[-=:+]{3,}' -e '^ +-{3,}[- ]*$' docs || true)"
if [[ -n "$pandoc_tables" ]]; then
  printf 'corpus pages use pandoc-only table syntax:\n%s\n' "$pandoc_tables" >&2
  exit 1
fi

uv run zensical build --strict

root_dir="$(cd "$site_dir" && pwd)"

table_text="$(rg -l --glob '*.html' -e '\+[-=:]{3,}\+' -e '-{3,} +-{3,}' "$site_dir" || true)"
if [[ -n "$table_text" ]]; then
  printf 'built pages show pandoc table syntax as text:\n%s\n' "$table_text" >&2
  exit 1
fi

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
