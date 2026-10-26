#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat >&2 <<'EOF'
usage: scripts/regenerate_docs.sh [--cache-dir DIR] [--project DIR] DOCS_SUBDIR...
  DOCS_SUBDIR  docs-relative directories whose pages to regenerate, e.g. tekniske-bestemmelser/15
  --cache-dir  read origin pages from a parity audit snapshot instead of crawling the origin (throttled)
  --project    directory holding docs/, zensical.toml and the corpus data files (default: the repository)
EOF
  exit 2
}

repo="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
project="$repo"
cache=()
while [[ $# -gt 0 ]]; do
  case "$1" in
    --cache-dir) cache=(--cache-dir "$(realpath "$2")"); shift 2 ;;
    --project) project="$(realpath "$2")"; shift 2 ;;
    *) break ;;
  esac
done
[[ $# -gt 0 ]] || usage

docs="$project/docs"
py=(uv run --project "$repo" python)
stage="$(mktemp -d)"
work="$(mktemp -d)"
trap 'rm -rf "$stage" "$work"' EXIT

if [[ ${#cache[@]} -eq 0 ]]; then
  cache=(--cache-dir "$work/origin")
  "${py[@]}" "$repo/scripts/audit_br18_parity.py" "${cache[@]}" --list-pages "$@" >"$work/urls"
else
  "${py[@]}" "$repo/scripts/audit_br18_parity.py" --offline "${cache[@]}" --list-pages "$@" >"$work/urls"
fi
mapfile -t urls <"$work/urls"
"${py[@]}" "$repo/scripts/fetch_origin_pages.py" --docs-root "$stage" "${cache[@]}" "${urls[@]}" >/dev/null
"${py[@]}" "$repo/scripts/convert_br18_docs.py" --docs-root "$stage"

grep -o '"[^"]*\.md"' "$project/zensical.toml" | tr -d '"' | sort -u >"$work/nav"
(cd "$stage" && find . -name index.md | sed 's|^\./||' | sort) >"$work/served"
(cd "$docs" && find "$@" -name index.md 2>/dev/null | sort || true) | comm -23 - "$work/served" | comm -23 - "$work/nav" >"$work/gone"
while read -r page; do
  [[ "$page" =~ /[0-9][0-9]/brv/index\.md$ ]] || rm "$docs/$page"
done <"$work/gone"

cp -r "$stage/." "$docs/"
"${py[@]}" "$repo/scripts/build_chapter_hubs.py" --docs-root "$docs" "${cache[@]}" "$@"
"${py[@]}" "$repo/scripts/link_references.py" --docs-root "$docs" --data-dir "$project"
uv run --project "$repo" --directory "$project" zensical build --strict
"${py[@]}" "$repo/scripts/keep_anchors.py" --docs-root "$docs" --site-dir "$project/site" --baseline "$project/required-anchors.tsv"
uv run --project "$repo" --directory "$project" zensical build --strict
"${py[@]}" "$repo/scripts/fix_broken_links.py" --docs-root "$docs" --site-root "$project/site" --dead-links "$project/origin-dead-links.toml" "${cache[@]}"
"${py[@]}" "$repo/scripts/sync_referenced_files.py" --docs-root "$docs"
