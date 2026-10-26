#!/usr/bin/env python3

from __future__ import annotations

import argparse
import os
import re
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import unquote, urlsplit

from audit_br18_parity import SITE
from fetch_origin_pages import cached

MARKDOWN_LINK_RE = re.compile(r"(\]\()([^)\s]+)")
HTML_ATTR_RE = re.compile(r"""((?:href|src)\s*=\s*["'])([^"']+)""")
ID_RE = re.compile(r"""\s(?:id|name)\s*=\s*["']([^"']+)["']""")
HEADING_ID_RE = re.compile(r"^(#{1,6} .*?) \{#([^}\s]+)\}\s*$", re.MULTILINE)
SKIP_PREFIXES = ("mailto:", "tel:", "javascript:", "data:", "/")
MAX_UPS = 8
ORIGIN_DEAD_LINKS = {
    "tekniske-bestemmelser/02/vejledninger/parkering": "tekniske-bestemmelser/20/vejledninger/parkering",
}


def fold(name: str) -> str:
    name = name.casefold().replace("å", "aa").replace("æ", "ae").replace("ø", "oe")
    return re.sub(r"-{2,}", "-", name)


class Site:
    def __init__(self, site_root: Path, cache_dir: Path | None = None) -> None:
        self.root = site_root.resolve()
        self.cache_dir = cache_dir
        self.ids: dict[Path, set[str]] = {}
        self.pages_by_id: dict[str, list[Path]] = defaultdict(list)
        for html in self.root.rglob("*.html"):
            ids = set(ID_RE.findall(html.read_text(encoding="utf-8", errors="replace")))
            self.ids[html] = ids
            for anchor in ids:
                self.pages_by_id[anchor].append(html)

    def join(self, base: Path, target: str) -> Path:
        parts = list(base.relative_to(self.root).parts)
        for part in target.split("/"):
            if part == "..":
                if parts:
                    parts.pop()
            elif part not in ("", "."):
                parts.append(part)
        return self.root.joinpath(*parts)

    def resolve(self, path: Path) -> Path | None:
        for candidate in (
            path,
            path / "index.html",
            path.with_name(path.name + ".html"),
        ):
            if candidate.is_file():
                return candidate
        return None

    def redirect_target(self, path: Path) -> Path | None:
        rel = path.relative_to(self.root).as_posix()
        if rel in ORIGIN_DEAD_LINKS:
            return self.resolve_casefold(self.root / ORIGIN_DEAD_LINKS[rel])
        if not self.cache_dir:
            return None
        try:
            _, final = cached(self.cache_dir, f"{SITE}/{rel}/")
        except OSError:
            return None
        return self.resolve_casefold(self.root / urlsplit(final).path.strip("/"))

    def resolve_casefold(self, path: Path) -> Path | None:
        return self._walk_casefold(self.root, path.relative_to(self.root).parts)

    def _walk_casefold(self, current: Path, parts: tuple[str, ...]) -> Path | None:
        if not parts:
            return current if self.resolve(current) else None
        if not current.is_dir():
            return None
        head = fold(parts[0])
        children = sorted(
            child for child in current.iterdir() if fold(child.name) == head
        )
        children.sort(key=lambda child: child.name != child.name.lower())
        for child in children:
            found = self._walk_casefold(child, parts[1:])
            if found is not None:
                return found
        return None


def page_base(md: Path, docs_root: Path, site: Site) -> Path:
    return site.root / md.relative_to(docs_root).parent


def fix_target(
    target: str, base: Path, site: Site, missing: set[tuple[Path, str]]
) -> tuple[str, bool]:
    if "://" in target or target.startswith(SKIP_PREFIXES):
        return target, True
    raw_path, _, fragment_part = target.partition("#")
    fragments = [f for f in fragment_part.split("#") if f]

    path_str = unquote(raw_path) or "."
    current = site.resolve(site.join(base, path_str))
    new_path = raw_path
    if current is None:
        trailing = "/" if raw_path.endswith("/") else ""
        stripped = re.sub(r"/?showall/?$", "", path_str) or "."
        for ups in range(MAX_UPS + 1):
            joined = site.join(base, "../" * ups + stripped)
            found = site.resolve_casefold(joined)
            if found is not None:
                current = site.resolve(found)
                new_path = os.path.relpath(found, base) + trailing
                break
        if current is None:
            found = site.redirect_target(site.join(base, stripped))
            if found is None:
                return target, False
            current = site.resolve(found)
            new_path = os.path.relpath(found, base) + trailing

    resolved = True
    if fragments:
        ids = site.ids.get(current, set())
        present = [f for f in fragments if f in ids]
        if present:
            fragments = present[-1:]
        else:
            hosts = {page for f in fragments for page in site.pages_by_id.get(f, [])}
            if len(hosts) != 1:
                fragments = []
            else:
                host = hosts.pop()
                fragments = [
                    f for f in fragments if host in site.pages_by_id.get(f, [])
                ][-1:]
                new_path = (
                    ""
                    if host.parent == base
                    else os.path.relpath(host.parent, base) + "/"
                )
    fixed = new_path + "".join(f"#{f}" for f in fragments)
    if new_path == raw_path and fragments == [f for f in fragment_part.split("#") if f]:
        return target, resolved
    return fixed, resolved


def fix_file(
    md: Path,
    docs_root: Path,
    site: Site,
    unresolved: list[str],
    missing: set[tuple[Path, str]],
) -> int:
    base = page_base(md, docs_root, site)
    text = md.read_text(encoding="utf-8")
    changes = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal changes
        target = match.group(2)
        fixed, resolved = fix_target(target, base, site, missing)
        if not resolved:
            unresolved.append(f"{md.relative_to(docs_root)}: {target}")
        if fixed == target:
            return match.group(0)
        changes += 1
        return match.group(1) + fixed

    updated = HTML_ATTR_RE.sub(repl, MARKDOWN_LINK_RE.sub(repl, text))
    if updated != text:
        md.write_text(updated, encoding="utf-8")
    return changes


def restore_heading_anchors(
    docs_root: Path, site: Site, missing: set[tuple[Path, str]]
) -> int:
    headings_by_id: dict[str, set[str]] = defaultdict(set)
    for md in docs_root.rglob("*.md"):
        for heading, anchor in HEADING_ID_RE.findall(md.read_text(encoding="utf-8")):
            headings_by_id[anchor].add(heading)

    restored = 0
    for html, anchor in sorted(missing):
        headings = headings_by_id.get(anchor, set())
        rel = html.parent.relative_to(site.root)
        md = docs_root / rel / "index.md"
        if not md.exists():
            md = (docs_root / rel).with_suffix(".md")
        if len(headings) != 1 or not md.exists():
            continue
        heading = headings.pop()
        lines = md.read_text(encoding="utf-8").split("\n")
        hits = [i for i, line in enumerate(lines) if line.rstrip() == heading]
        if len(hits) != 1:
            continue
        lines[hits[0]] = f"{heading} {{#{anchor}}}"
        md.write_text("\n".join(lines), encoding="utf-8")
        restored += 1
    return restored


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Repair relative links in docs/ against a built site/."
    )
    parser.add_argument("--docs-root", default="docs")
    parser.add_argument("--site-root", default="site")
    parser.add_argument("--cache-dir", type=Path, help="parity audit origin snapshot, to resolve links to origin redirects")
    args = parser.parse_args()

    docs_root = Path(args.docs_root).resolve()
    site = Site(Path(args.site_root), args.cache_dir)
    unresolved: list[str] = []
    missing: set[tuple[Path, str]] = set()
    total = sum(
        fix_file(md, docs_root, site, unresolved, missing)
        for md in sorted(docs_root.rglob("*.md"))
    )
    print(f"rewrote {total} links", file=sys.stderr)
    print(
        f"restored {restore_heading_anchors(docs_root, site, missing)} heading anchors",
        file=sys.stderr,
    )
    for line in sorted(set(unresolved)):
        print(f"unresolved: {line}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
