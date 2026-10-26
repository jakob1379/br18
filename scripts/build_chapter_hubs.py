#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import posixpath
import re
import tempfile
from pathlib import Path
from urllib.parse import unquote, urlsplit

from audit_br18_parity import SITE, OriginFetcher
from fetch_origin_pages import download, page_source

CHAPTERS = ("tekniske-bestemmelser/[0-9][0-9]", "ovrige-bestemmelser/[0-9][0-9]", "straf-og-ikrafttraedelse/[0-9][0-9]")
VEJLEDNING_TAB_RE = re.compile(rb'<a href="([^"]+)"[^>]*class="nav-tab__link[^"]*"[^>]*>\s*Vejledning')
LINK_RE = re.compile(r'(\]\(|\b(?:href|src)=")([^)"\s]+)')
BUTTON_RE = re.compile(r"^\[[^\]]*\]\([^)]*\)\{ \.md-button[^}]*\}$")
COMPAT_ANCHORS_RE = re.compile(r'^(?:<span id="[^"]+"></span>)+$')


def rebase(markdown: str, src: str, dst: str) -> str:

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
    if markdown.startswith("---\n"):
        markdown = markdown[markdown.index("\n---\n", 4) + 5 :]
    lines = markdown.strip().splitlines()
    title = next((line[2:].strip() for line in lines if line.startswith("# ")), "")
    body = lines[next((i + 1 for i, line in enumerate(lines) if line.startswith("# ")), 0) :]
    kept = "\n".join(line for line in body if not BUTTON_RE.match(line) and not COMPAT_ANCHORS_RE.match(line))
    return title, re.sub(r"\n{3,}", "\n\n", kept).strip()


def page_title(markdown: str) -> str:
    front = re.match(r"---\n(?:.*\n)*?title: (.*)\n(?:.*\n)*?---\n", markdown)
    if not front:
        return title_and_body(markdown)[0]
    value = front.group(1).strip()
    return json.loads(value) if value.startswith('"') else value


def page(title: str, buttons: list[str], body: str, page_title: str) -> str:
    front = f"---\ntitle: {json.dumps(page_title, ensure_ascii=False)}\n---\n\n"
    return f"{front}# {title}\n\n" + "\n".join(buttons) + f"\n\n{body}\n"


def served(url: str, pages: OriginFetcher) -> tuple[bytes, str] | None:
    try:
        return download(url, pages)
    except OSError:
        return None


def build(docs: Path, chapter: str, pages: OriginFetcher) -> None:
    krav = docs / chapter / "krav" / "index.md"
    if not krav.exists():
        return
    krav_md = krav.read_text(encoding="utf-8")
    title, krav_body = title_and_body(krav_md)
    own = served(f"{SITE}/{chapter}/krav/", pages)
    tab = VEJLEDNING_TAB_RE.search(own[0]) if own else None
    guide = unquote(urlsplit(tab.group(1).decode()).path).strip("/").lower() if tab else None
    brv = docs / chapter / "brv" / "index.md"
    origin_brv = served(f"{SITE}/{chapter}/brv/", pages)
    if origin_brv and urlsplit(origin_brv[1]).path.strip("/").lower() == f"{chapter}/brv" and brv.exists():
        brv_md = brv.read_text(encoding="utf-8")
        brv_body = title_and_body(brv_md)[1]
    elif guide and (docs / guide / "index.md").exists() and guide != f"{chapter}/brv":
        brv_md = (docs / guide / "index.md").read_text(encoding="utf-8")
        brv_body = rebase(title_and_body(brv_md)[1], guide, f"{chapter}/brv")
    else:
        brv_body = None
    buttons = ["[Krav](./){ .md-button .md-button--primary }"] + (["[Vejledning](brv/){ .md-button }"] if brv_body is not None or brv.exists() else [])
    (docs / chapter / "index.md").write_text(page(title, buttons, rebase(krav_body, f"{chapter}/krav", chapter), page_title(krav_md)), encoding="utf-8")
    if brv_body is not None:
        brv_buttons = ["[Krav](../){ .md-button }", "[Vejledning](./){ .md-button .md-button--primary }"]
        brv.parent.mkdir(parents=True, exist_ok=True)
        brv.write_text(page(title, brv_buttons, brv_body, page_title(brv_md)), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--docs-root", default="docs")
    parser.add_argument("--cache-dir", type=Path, help="read origin pages from a parity audit snapshot instead of the network")
    args = parser.parse_args()
    docs = Path(args.docs_root).resolve()
    chapters = sorted(p.relative_to(docs).as_posix() for pattern in CHAPTERS for p in docs.glob(pattern))
    with tempfile.TemporaryDirectory() as scratch:
        pages = page_source(args.cache_dir, Path(scratch))
        try:
            for chapter in ["administrative-bestemmelser", *chapters]:
                build(docs, chapter, pages)
        finally:
            pages.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
