#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
site_dir="${SITE_DIR:-site}"

cd "$repo_root"

collisions="$(find docs | uv run python -c '
import collections, sys, unicodedata
names = collections.defaultdict(list)
for path in sys.stdin.read().splitlines():
    names[unicodedata.normalize("NFC", unicodedata.normalize("NFD", path).casefold())].append(path)
print("\n".join(path for paths in names.values() if len(paths) > 1 for path in sorted(paths)))
')"
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
uv run python scripts/keep_anchors.py --check --site-dir "$site_dir"
uv run python scripts/check_references.py --site-dir "$site_dir"

root_dir="$(cd "$site_dir" && pwd)"

table_text="$(rg -l --glob '*.html' -e '\+[-=:]{3,}\+' -e '-{3,} +-{3,}' "$site_dir" || true)"
if [[ -n "$table_text" ]]; then
  printf 'built pages show pandoc table syntax as text:\n%s\n' "$table_text" >&2
  exit 1
fi

space='(?:\s|&nbsp;|&#160;|\x{a0})'
residue="$(rg -n -o -P --glob '*.html' \
  -e '>[^<]*@@PROTECTED_' \
  -e '>[^<]*\*\*' \
  -e "(?:^|[\\s>])\\*{1,3}${space}+\\*{1,3}(?=[\\s<]|$)" \
  -e "<(?:p|li|h[1-6])\\b[^>]*>${space}*\\*+${space}*(?:</|<a class=\"headerlink\")" \
  -e '<(?:em|strong)>\*+</(?:em|strong)>' \
  "$site_dir" || true)"
if [[ -n "$residue" ]]; then
  printf 'built pages show markup residue as text:\n%s\n' "$residue" >&2
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
  --exclude '^https://brandogkonstruktioner\.dk/' \
  --exclude '^https://www\.brandogkonstruktioner\.dk/' \
  --exclude '^https?://historisk\.bygningsreglementet\.dk/' \
  --exclude '^https://www\.retsinformation\.dk/eli/lta/[0-9]+/[0-9]+#P' \
  --exclude '^https://www\.radonguiden\.dk/' \
  --exclude '^https://build\.dk/Pages/Vejledning-om-haandtering-af-fugt-i-bygninger\.aspx$' \
  "$site_dir/**/*.html"
