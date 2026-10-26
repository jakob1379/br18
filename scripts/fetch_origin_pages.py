#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
import sys
import tempfile
from pathlib import Path
from urllib.parse import unquote, urlsplit

from audit_br18_parity import DEFAULT_DELAY, HOSTS, SITE, OriginFetcher

EXPAND_ALL_RE = re.compile(rb'<a href="([^"]+\?Layout=ShowAll)" class="link--expand-all"')
TITLE_TAG_RE = re.compile(rb"<title>.*?</title>", re.IGNORECASE | re.DOTALL)
TRIGGER_RE = re.compile(rb'<a href="([^"#]*)#[0-9a-f-]{36}"[^>]*class="accordion__trigger')


def is_section_page(html: bytes, url: str) -> bool:
    page = urlsplit(url)._replace(query="", fragment="").geturl().rstrip("/").lower()
    return any(t.decode().rstrip("/").lower() == page for t in TRIGGER_RE.findall(html))


def target_path_for_url(docs_root: Path, url: str) -> Path:
    parsed = urlsplit(url)
    if parsed.netloc not in HOSTS:
        raise SystemExit(f"unsupported host: {url}")

    path = unquote(parsed.path).strip("/").lower()
    base = docs_root / path if path else docs_root

    if parsed.query == "Layout=ShowAll":
        return base / "showall" / "index.html"
    return base / "index.html"


def page_source(cache_dir: Path | None, scratch: Path, origin: str = SITE, delay: float = DEFAULT_DELAY) -> OriginFetcher:
    return OriginFetcher(None, cache_dir, 0) if cache_dir else OriginFetcher(origin, scratch, delay)


def download(url: str, pages: OriginFetcher) -> tuple[bytes, str]:
    record = pages.get(url)
    if record["status"] != 200:
        raise OSError(record.get("error") or f"HTTP {record['status']}")
    return record["html"].encode(), record["final"]


def is_krav_subpage(url: str) -> bool:
    parts = urlsplit(url).path.lower().strip("/").split("/")
    return len(parts) > 1 and parts[-2] == "krav"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--docs-root", default="docs")
    parser.add_argument("--cache-dir", type=Path, help="read pages from a parity audit origin snapshot instead of the network")
    parser.add_argument("--origin", default=SITE)
    parser.add_argument("--delay", type=float, default=DEFAULT_DELAY)
    parser.add_argument("urls", nargs="+")
    args = parser.parse_args()

    docs_root = Path(args.docs_root).resolve()
    failed = 0
    with tempfile.TemporaryDirectory() as scratch:
        pages = page_source(args.cache_dir, Path(scratch), args.origin, args.delay)
        try:
            for raw in args.urls:
                url = raw if raw.startswith("http") else f"{SITE}/{raw.lstrip('/')}"
                try:
                    html, final = download(url, pages)
                    page = urlsplit(final)._replace(query="", fragment="").geturl()
                    expand_all = EXPAND_ALL_RE.search(html)
                    if expand_all and urlsplit(final).query != "Layout=ShowAll" and (not is_section_page(html, page) or is_krav_subpage(page)):
                        own_title = TITLE_TAG_RE.search(html)
                        html, _ = download(expand_all.group(1).decode(), pages)
                        if own_title:
                            html = TITLE_TAG_RE.sub(lambda _: own_title.group(0), html, count=1)
                except OSError as exc:
                    failed += 1
                    print(f"not fetched: {url} ({exc})", file=sys.stderr)
                    continue
                target = target_path_for_url(docs_root, page)
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(html)
                print(target.relative_to(docs_root.parent))
        finally:
            pages.close()
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
