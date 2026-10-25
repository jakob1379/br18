#!/usr/bin/env python3

from __future__ import annotations

import argparse
from pathlib import Path
from urllib.parse import urlsplit
from urllib.request import Request, urlopen


SITE_ROOT = "https://www.bygningsreglementet.dk"


def target_path_for_url(docs_root: Path, url: str) -> Path:
    parsed = urlsplit(url)
    if parsed.netloc not in {"www.bygningsreglementet.dk", "bygningsreglementet.dk"}:
        raise SystemExit(f"unsupported host: {url}")

    path = parsed.path.strip("/")
    base = docs_root / path if path else docs_root

    if parsed.query == "Layout=ShowAll":
        return base / "showall" / "index.html"
    return base / "index.html"


def fetch(url: str, target: Path) -> None:
    req = Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; br18-parity-fetcher/1.0)",
        },
    )
    with urlopen(req, timeout=30) as resp:
        content = resp.read()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(content)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--docs-root", default="docs")
    parser.add_argument("urls", nargs="+")
    args = parser.parse_args()

    docs_root = Path(args.docs_root).resolve()
    for raw in args.urls:
        url = raw if raw.startswith("http") else f"{SITE_ROOT.rstrip('/')}/{raw.lstrip('/')}"
        target = target_path_for_url(docs_root, url)
        fetch(url, target)
        print(target.relative_to(docs_root.parent))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
