#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat >&2 <<'EOF'
usage: scripts/regenerate_docs.sh [--cache-dir DIR] [--project DIR] DOCS_SUBDIR...
  DOCS_SUBDIR  docs-relative directories whose pages to regenerate, e.g. tekniske-bestemmelser/15
  --cache-dir  read origin pages from a parity audit snapshot instead of the network
  --project    directory holding docs/ and zensical.toml (default: the repository)
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
trap 'rm -rf "$stage"' EXIT

mapfile -t urls < <(cd "$docs" && find "$@" -name index.md -printf 'https://www.bygningsreglementet.dk/%h/\n' | sort)
"${py[@]}" "$repo/scripts/fetch_origin_pages.py" --docs-root "$stage" "${cache[@]}" "${urls[@]}" >/dev/null || true
"${py[@]}" "$repo/scripts/convert_br18_docs.py" --docs-root "$stage"
cp -r "$stage/." "$docs/"
"${py[@]}" "$repo/scripts/build_chapter_hubs.py" --docs-root "$docs" "${cache[@]}"
"${py[@]}" "$repo/scripts/link_references.py" --docs-root "$docs" --data-dir "$repo"
uv run --project "$repo" --directory "$project" zensical build --strict
"${py[@]}" "$repo/scripts/keep_anchors.py" --docs-root "$docs" --site-dir "$project/site" --baseline "$repo/required-anchors.tsv"
uv run --project "$repo" --directory "$project" zensical build --strict
"${py[@]}" "$repo/scripts/fix_broken_links.py" --docs-root "$docs" --site-root "$project/site" "${cache[@]}"
"${py[@]}" "$repo/scripts/sync_referenced_files.py" --docs-root "$docs"
