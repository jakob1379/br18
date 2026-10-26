#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
import sys
from html import unescape
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urljoin, urlsplit

from audit_br18_parity import HOSTS, SITE
from fetch_origin_pages import fetch


MARKDOWN_LINK_RE = re.compile(r"\]\(([^)\s]+)")
HTML_ATTR_RE = re.compile(r"""(?:href|src|poster)\s*=\s*["']([^"']+)["']""")
QUERY_ALIAS_RE = re.compile(r"__q_[0-9a-f]+(?=\.[^.]+$)")


def iter_targets(markdown: str) -> list[str]:
    targets = MARKDOWN_LINK_RE.findall(markdown)
    targets.extend(HTML_ATTR_RE.findall(markdown))
    return [unescape(target.strip()) for target in targets if target.strip()]


def canonicalize_asset_path(path: str, docs_root: Path) -> str:
    canonical = QUERY_ALIAS_RE.sub("", path)
    if canonical == path:
        return path

    candidate = docs_root / canonical.lstrip("/")
    return canonical if candidate.exists() else path


def resolve_local_target(source: Path, docs_root: Path, target: str) -> tuple[Path, str] | None:
    if target.startswith(("#", "mailto:", "tel:", "javascript:", "data:")):
        return None

    parsed = urlsplit(target)
    if parsed.scheme and parsed.netloc:
        if parsed.netloc not in HOSTS:
            return None
        origin_path = canonicalize_asset_path(parsed.path, docs_root)
    else:
        target_path = parsed.path
        if not target_path:
            return None
        if target_path.startswith("/"):
            local_path = (docs_root / target_path.lstrip("/")).resolve()
        else:
            local_path = (source.parent / target_path).resolve()
        if not local_path.is_relative_to(docs_root):
            return None
        origin_path = "/" + local_path.relative_to(docs_root).as_posix()
        return local_path, urljoin(SITE, quote(origin_path, safe="/"))

    local_path = (docs_root / origin_path.lstrip("/")).resolve()
    if not local_path.is_relative_to(docs_root):
        return None
    return local_path, urljoin(SITE, quote(origin_path, safe="/"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--docs-root", default="docs")
    args = parser.parse_args()

    docs_root = Path(args.docs_root).resolve()
    missing: dict[Path, str] = {}
    for source in docs_root.rglob("*.md"):
        if "showall" in source.parts:
            continue
        text = source.read_text(encoding="utf-8")
        for target in iter_targets(text):
            resolved = resolve_local_target(source, docs_root, target)
            if resolved is None:
                continue
            local_path, origin_url = resolved
            if not local_path.suffix:
                continue
            if local_path.exists():
                continue
            missing.setdefault(local_path, origin_url)

    if not missing:
        print("no missing referenced files")
        return 0

    fetched = 0
    failed = 0
    for local_path, origin_url in sorted(missing.items()):
        try:
            fetch(origin_url, local_path)
        except (HTTPError, URLError, TimeoutError, OSError) as exc:
            failed += 1
            print(f"failed fetch: {origin_url} -> {local_path} ({exc})", file=sys.stderr)
            continue
        fetched += 1
        print(local_path)

    print(f"fetched={fetched} failed={failed}", file=sys.stderr)
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
