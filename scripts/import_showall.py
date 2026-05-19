#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path
from posixpath import splitext
from urllib.parse import urlsplit

from fetch_origin_pages import SITE_ROOT, fetch, target_path_for_url
from convert_br18_docs import promote_legal_paragraph_headings


INLINE_DESCENDANT_LINK = re.compile(r"\]\(([^)\s]+#[^)\"\s]+)\)")


def rewrite_descendant_fragment_links(markdown: str) -> str:
    def replace(match: re.Match[str]) -> str:
        target = match.group(1)
        path, fragment = target.split("#", 1)
        if (
            not path
            or path.startswith(("#", "/", "./", "../"))
            or "://" in path
            or splitext(path)[1]
        ):
            return match.group(0)
        return f"](#${fragment})".replace("#$", "#")

    return INLINE_DESCENDANT_LINK.sub(replace, markdown)


def promote_showall_md(docs_root: Path, url: str) -> None:
    parsed = urlsplit(url)
    rel_dir = parsed.path.strip("/")
    target_dir = docs_root / rel_dir if rel_dir else docs_root
    showall_md = target_dir / "showall" / "index.md"
    target_md = target_dir / "index.md"
    if not showall_md.exists():
        raise SystemExit(f"missing converted markdown: {showall_md}")
    markdown = showall_md.read_text(encoding="utf-8")
    markdown = rewrite_descendant_fragment_links(markdown)
    for _ in range(4):
        promoted = promote_legal_paragraph_headings(markdown)
        if promoted == markdown:
            break
        markdown = promoted
    target_md.write_text(markdown, encoding="utf-8")
    showall_md.unlink()
    try:
        showall_md.parent.rmdir()
    except OSError:
        pass


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--docs-root", default="docs")
    parser.add_argument("--from-file")
    parser.add_argument("--ignore-errors", action="store_true")
    parser.add_argument("urls", nargs="*")
    args = parser.parse_args()

    docs_root = Path(args.docs_root).resolve()
    if not docs_root.exists():
        raise SystemExit(f"docs root not found: {docs_root}")

    urls = list(args.urls)
    if args.from_file:
        extra = [
            line.strip()
            for line in Path(args.from_file).read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        urls.extend(extra)

    seen: set[str] = set()
    normalized_urls: list[str] = []
    for raw in urls:
        url = raw if raw.startswith("http") else f"{SITE_ROOT.rstrip('/')}/{raw.lstrip('/')}"
        if url not in seen:
            seen.add(url)
            normalized_urls.append(url)

    rel_paths = []
    successful_urls: list[str] = []
    for url in normalized_urls:
        target = target_path_for_url(docs_root, url)
        try:
            fetch(url, target)
        except Exception as exc:
            if not args.ignore_errors:
                raise
            print(f"failed fetch: {url} ({exc})", file=sys.stderr)
            continue
        rel_paths.append(str(target.relative_to(docs_root)))
        successful_urls.append(url)

    if not rel_paths:
        print("no showall pages fetched", file=sys.stderr)
        return 0

    convert_cmd = ["uv", "run", "python", "scripts/convert_br18_docs.py", "--docs-root", str(docs_root)]
    convert_cmd.extend(rel_paths)
    subprocess.run(convert_cmd, check=True)

    for url in successful_urls:
        promote_showall_md(docs_root, url)
        print(f"promoted {urlsplit(url).path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
