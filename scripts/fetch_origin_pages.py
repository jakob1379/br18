#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit
from urllib.request import Request, urlopen

from audit_br18_parity import HOSTS, SITE, cache_file

EXPAND_ALL_RE = re.compile(rb'<a href="([^"]+\?Layout=ShowAll)" class="link--expand-all"')
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


def cached(cache_dir: Path, url: str) -> tuple[bytes, str]:
    record = json.loads(cache_file(cache_dir, url).read_text(encoding="utf-8"))
    if record["status"] != 200:
        raise OSError(f"HTTP {record['status']} in snapshot: {url}")
    return record["html"].encode(), record["final"]


def download(url: str, cache_dir: Path | None = None) -> tuple[bytes, str]:
    if cache_dir:
        return cached(cache_dir, url)
    req = Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; br18-parity-fetcher/1.0)"})
    with urlopen(req, timeout=30) as resp:
        return resp.read(), resp.geturl()


def fetch(url: str, target: Path, cache_dir: Path | None = None) -> None:
    content, _ = download(url, cache_dir)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(content)


def is_krav_subpage(url: str) -> bool:
    parts = urlsplit(url).path.lower().strip("/").split("/")
    return len(parts) > 1 and parts[-2] == "krav"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--docs-root", default="docs")
    parser.add_argument("--cache-dir", type=Path, help="read pages from a parity audit origin snapshot instead of the network")
    parser.add_argument("urls", nargs="+")
    args = parser.parse_args()

    docs_root = Path(args.docs_root).resolve()
    failed = 0
    for raw in args.urls:
        url = raw if raw.startswith("http") else f"{SITE}/{raw.lstrip('/')}"
        try:
            html, final = download(url, args.cache_dir)
            page = urlsplit(final)._replace(query="", fragment="").geturl()
            expand_all = EXPAND_ALL_RE.search(html)
            if expand_all and urlsplit(final).query != "Layout=ShowAll" and (not is_section_page(html, page) or is_krav_subpage(page)):
                html, _ = download(expand_all.group(1).decode(), args.cache_dir)
        except OSError as exc:
            failed += 1
            print(f"not fetched: {url} ({exc})", file=sys.stderr)
            continue
        target = target_path_for_url(docs_root, page)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(html)
        print(target.relative_to(docs_root.parent))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
