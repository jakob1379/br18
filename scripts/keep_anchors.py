#!/usr/bin/env python3

from __future__ import annotations

import argparse
import html
import re
import sys
from collections import defaultdict
from pathlib import Path

ELEM_RE = re.compile(r"""<(\w+)\b[^>]*?\sid=["']([^"']+)["'][^>]*>""")
HEADING_RE = re.compile(r"^#{1,6}\s")


def words(text: str) -> list[str]:
    return re.findall(r"\w+", text.lower())


def heading_words(line: str) -> list[str]:
    text = re.sub(r"\s*\{[^}]*\}\s*$", "", line.lstrip("#"))
    text = re.sub(r"\]\([^)]*\)|<[^>]+>", " ", text)
    return words(html.unescape(text))


def built_ids(page: Path) -> dict[str, str]:
    text = page.read_text(encoding="utf-8", errors="replace")
    start = text.find('class="md-content__inner')
    body = text[start : text.find("</article>", start)] if start >= 0 else ""
    ids: dict[str, str] = {}
    for m in ELEM_RE.finditer(body):
        tag, ident = m.group(1), m.group(2)
        heading = ""
        if re.fullmatch(r"h[1-6]", tag):
            heading = re.sub(r"<[^>]+>", " ", body[m.end() : body.find(f"</{tag}>", m.end())])
        ids.setdefault(ident, html.unescape(heading))
    return ids


def load_baseline(path: Path) -> dict[str, list[tuple[str, str]]]:
    pages: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            page, ident, text = (line.split("\t") + ["", ""])[:3]
            pages[page].append((ident, text))
    return pages


def section_end(lines: list[str], index: int) -> int:
    return next((i for i in range(index + 1, len(lines)) if HEADING_RE.match(lines[i])), len(lines))


def locate(lines: list[str], ident: str, heading: str) -> int | None:
    explicit = re.compile(rf"\{{[^}}]*#{re.escape(ident)}(?=[\s}}])|\bid=\"{re.escape(ident)}\"")
    for i, line in enumerate(lines):
        if explicit.search(line):
            return i
    target = words(heading)
    if target:
        for i, line in enumerate(lines):
            if HEADING_RE.match(line) and heading_words(line) == target:
                return i
    return None


def fix_page(markdown: str, required: list[tuple[str, str]], built: dict[str, str]) -> str:
    lines = markdown.split("\n")
    before: dict[int, list[str]] = defaultdict(list)
    after: dict[int, list[str]] = defaultdict(list)
    for k, (ident, old_heading) in enumerate(required):
        if ident in built:
            continue
        anchor_line = None
        for prev, _ in reversed(required[:k]):
            if prev in built:
                anchor_line = locate(lines, prev, built[prev])
                if anchor_line is not None:
                    break
        if anchor_line is None:
            anchor_line = next((i for i, line in enumerate(lines) if line.startswith("# ")), -1)
        old = words(old_heading)
        renamed = [i for i, line in enumerate(lines) if old and HEADING_RE.match(line) and heading_words(line)[-len(old) :] == old]
        if renamed:
            before[next((i for i in renamed if i > anchor_line), renamed[0])].append(ident)
            continue
        after[section_end(lines, anchor_line) if anchor_line >= 0 else 0].append(ident)
    inserts: dict[int, list[str]] = defaultdict(list)
    for index, idents in before.items():
        inserts[index] += idents
    for index, idents in after.items():
        inserts[index] = idents + inserts[index]
    for index in sorted(inserts, reverse=True):
        spans = "".join(f'<span id="{i}"></span>' for i in inserts[index])
        lines[index:index] = (["", spans, ""] if index else [spans, ""])
    return re.sub(r"\n{3,}", "\n\n", "\n".join(lines))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--docs-root", default="docs")
    parser.add_argument("--site-dir", default="site")
    parser.add_argument("--baseline", default="required-anchors.tsv")
    parser.add_argument("--check", action="store_true", help="only report missing anchors")
    args = parser.parse_args()
    docs, site = Path(args.docs_root), Path(args.site_dir)
    missing: list[str] = []
    fixed = 0
    for page, required in sorted(load_baseline(Path(args.baseline)).items()):
        built_page = site / page / "index.html"
        built = built_ids(built_page) if built_page.exists() else {}
        lacking = [ident for ident, _ in required if ident not in built]
        if not lacking:
            continue
        missing += [f"{page}#{ident}" for ident in lacking]
        source = docs / page / "index.md"
        if not args.check and built_page.exists() and source.exists():
            source.write_text(fix_page(source.read_text(encoding="utf-8"), required, built), encoding="utf-8")
            fixed += 1
    if args.check:
        if missing:
            print(f"missing required anchors ({len(missing)}):", *missing[:200], sep="\n", file=sys.stderr)
            return 1
        return 0
    print(f"added {len(missing)} anchors on {fixed} pages", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
