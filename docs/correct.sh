#!/usr/bin/env bash
set -euo pipefail

queue=".codex-md-queue"

if [[ ! -f "$queue" ]]; then
  fd -e md --threads 1 > "$queue"
fi

remaining="$(wc -l < "$queue" | tr -d ' ')"

if [[ "$remaining" -eq 0 ]]; then
  exit 0
fi

fifo="$(mktemp -u)"
mkfifo "$fifo"

cleanup() {
  exec 3>&- 2>/dev/null || true
  rm -f "$fifo"
  kill "${pv_pid:-}" 2>/dev/null || true
}

trap cleanup EXIT

pv -f -l -s "$remaining" -N md-files < "$fifo" > /dev/null &
pv_pid="$!"

exec 3> "$fifo"

while [[ -s "$queue" ]]; do
  IFS= read -r file < "$queue"

  codex exec \
    "correct malformed references and links that have accidental linebreaks, in @$file - if there are none, fine, then exit with \"no accidental linebreaks found in $file\""

  tmp="$(mktemp)"
  tail -n +2 "$queue" > "$tmp"
  mv "$tmp" "$queue"

  printf '\n' >&3
done
