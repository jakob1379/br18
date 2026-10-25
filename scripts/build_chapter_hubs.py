#!/usr/bin/env python3
"""Rebuild the clone's chapter hubs from the pages they stand for, so they cannot go stale.

A chapter hub (docs/<part>/<NN>/index.md, docs/administrative-bestemmelser/index.md) is the chapter's
krav page with a Krav/Vejledning tab bar, which the origin shows on its krav pages. Its guide page
(<chapter>/brv/index.md) is the page the origin's "Vejledning" tab opens, with the same tab bar; a brv page
the origin serves itself keeps its own content.
"""

from __future__ import annotations

import argparse
import posixpath
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

from fetch_origin_pages import SITE_ROOT, download

CHAPTERS = ("tekniske-bestemmelser/[0-9][0-9]", "ovrige-bestemmelser/[0-9][0-9]", "straf-og-ikrafttraedelse/[0-9][0-9]")
VEJLEDNING_TAB_RE = re.compile(rb'<a href="([^"]+)"[^>]*class="nav-tab__link[^"]*"[^>]*>\s*Vejledning')
LINK_RE = re.compile(r'(\]\(|\b(?:href|src)=")([^)"\s]+)')
BUTTON_RE = re.compile(r"^\[[^\]]*\]\([^)]*\)\{ \.md-button[^}]*\}$")


def rebase(markdown: str, src: str, dst: str) -> str:
    """Relative link targets of a page in docs dir `src`, rewritten for the same text in `dst`."""

    def repl(match: re.Match[str]) -> str:
        target = match.group(2)
        if target.startswith(("#", "/")) or re.match(r"[a-z][a-z0-9+.-]*:", target):
            return match.group(0)
        path, sep, fragment = target.partition("#")
        new = posixpath.relpath(posixpath.normpath(posixpath.join(src, path)), dst)
        if path.endswith("/") or new == ".":
            new = "./" if new == "." else f"{new}/"
        return f"{match.group(1)}{new}{sep}{fragment}"

    return LINK_RE.sub(repl, markdown)


def title_and_body(markdown: str) -> tuple[str, str]:
    """The page's H1 and what follows it, without frontmatter or a tab bar from an earlier run."""
    if markdown.startswith("---\n"):
        markdown = markdown[markdown.index("\n---\n", 4) + 5 :]
    lines = markdown.strip().splitlines()
    title = next((line[2:].strip() for line in lines if line.startswith("# ")), "")
    body = lines[next((i + 1 for i, line in enumerate(lines) if line.startswith("# ")), 0) :]
    return title, "\n".join(line for line in body if not BUTTON_RE.match(line)).strip()


def page(title: str, buttons: list[str], body: str, frontmatter_title: str | None = None) -> str:
    front = f"---\ntitle: {frontmatter_title}\n---\n\n" if frontmatter_title else ""
    return f"{front}# {title}\n\n" + "\n".join(buttons) + f"\n\n{body}\n"


def served(url: str, cache_dir: Path | None) -> tuple[bytes, str] | None:
    try:
        return download(url, cache_dir)
    except OSError:
        return None


def build(docs: Path, chapter: str, cache_dir: Path | None) -> None:
    krav = docs / chapter / "krav" / "index.md"
    if not krav.exists():
        return
    title, krav_body = title_and_body(krav.read_text(encoding="utf-8"))
    own = served(f"{SITE_ROOT}/{chapter}/krav/", cache_dir)
    tab = VEJLEDNING_TAB_RE.search(own[0]) if own else None
    guide = unquote(urlsplit(tab.group(1).decode()).path).strip("/").lower() if tab else None
    brv = docs / chapter / "brv" / "index.md"
    origin_brv = served(f"{SITE_ROOT}/{chapter}/brv/", cache_dir)
    if origin_brv and urlsplit(origin_brv[1]).path.strip("/").lower() == f"{chapter}/brv" and brv.exists():
        brv_body = title_and_body(brv.read_text(encoding="utf-8"))[1]
    elif guide and (docs / guide / "index.md").exists() and guide != f"{chapter}/brv":
        brv_body = rebase(title_and_body((docs / guide / "index.md").read_text(encoding="utf-8"))[1], guide, f"{chapter}/brv")
    else:
        brv_body = None
    buttons = ["[Krav](./){ .md-button .md-button--primary }"] + (["[Vejledning](brv/){ .md-button }"] if brv_body is not None or brv.exists() else [])
    (docs / chapter / "index.md").write_text(page(title, buttons, rebase(krav_body, f"{chapter}/krav", chapter)), encoding="utf-8")
    if brv_body is not None:
        brv_buttons = ["[Krav](../){ .md-button }", "[Vejledning](./){ .md-button .md-button--primary }"]
        brv.parent.mkdir(parents=True, exist_ok=True)
        brv.write_text(page(title, brv_buttons, brv_body, f"{title} – Vejledning"), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--docs-root", default="docs")
    parser.add_argument("--cache-dir", type=Path, help="read origin pages from a parity audit snapshot instead of the network")
    args = parser.parse_args()
    docs = Path(args.docs_root).resolve()
    chapters = sorted(p.relative_to(docs).as_posix() for pattern in CHAPTERS for p in docs.glob(pattern))
    for chapter in ["administrative-bestemmelser", *chapters]:
        build(docs, chapter, args.cache_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
