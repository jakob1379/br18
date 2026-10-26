#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
import signal
import sys
import time
from html import unescape
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urljoin, urlsplit
from urllib.request import Request, urlopen

from audit_br18_parity import DEFAULT_DELAY, HOSTS, SITE


MARKDOWN_LINK_RE = re.compile(r"\]\(([^)\s]+)")
HTML_ATTR_RE = re.compile(r"""(?:href|src|poster)\s*=\s*["']([^"']+)["']""")
QUERY_ALIAS_RE = re.compile(r"__q_[0-9a-f]+(?=\.[^.]+$)")
USER_AGENT = {"User-Agent": "Mozilla/5.0 (compatible; br18-parity-fetcher/1.0)"}
REPO = Path(__file__).resolve().parent.parent


def fetch(url: str, target: Path) -> None:
    with urlopen(Request(url, headers=USER_AGENT), timeout=30) as resp:
        content = resp.read()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(content)


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


def check_versions(files: dict[Path, str], docs_root: Path, origin: str, delay: float, manifest: Path) -> int:
    rows = [line.split("\t") for line in manifest.read_text(encoding="utf-8").splitlines()[1:]] if manifest.exists() else []
    recorded = {row[0]: tuple(row[1:]) for row in rows if len(row) == 4}
    signal.signal(signal.SIGTERM, lambda *_: sys.exit(143))
    try:
        failed = _check(files, docs_root, origin, delay, recorded)
    finally:
        lines = ["path\tcontent-length\tetag\tlast-modified", *("\t".join((rel, *v)) for rel, v in sorted(recorded.items()))]
        manifest.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"checked={len(files)} failed={failed}", file=sys.stderr)
    return 1 if failed else 0


def _check(files: dict[Path, str], docs_root: Path, origin: str, delay: float, recorded: dict[str, tuple[str, ...]]) -> int:
    failed = 0
    first = True
    for local_path, origin_url in sorted(files.items()):
        rel = local_path.relative_to(docs_root).as_posix()
        url = origin + origin_url.removeprefix(SITE)
        try:
            for method in ("HEAD", "GET"):
                if not first:
                    time.sleep(delay)
                first = False
                with urlopen(Request(url, method=method, headers=USER_AGENT), timeout=60) as resp:
                    version = (resp.headers.get("content-length", ""), resp.headers.get("etag", ""), resp.headers.get("last-modified", ""))
                    if method == "GET":
                        local_path.write_bytes(resp.read())
                        print(rel)
                        break
                size_differs = version[0] and int(version[0]) != local_path.stat().st_size
                if not size_differs and recorded.get(rel, version) == version:
                    break
        except (HTTPError, URLError, TimeoutError, OSError) as exc:
            failed += 1
            print(f"failed version check: {url} -> {rel} ({exc})", file=sys.stderr)
            continue
        recorded[rel] = version
    return failed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--docs-root", default="docs")
    parser.add_argument("--check-versions", action="store_true", help="download again every referenced file whose origin version differs")
    parser.add_argument("--origin", default=SITE)
    parser.add_argument("--delay", type=float, default=DEFAULT_DELAY)
    parser.add_argument("--manifest", type=Path, default=REPO / "media-versions.tsv")
    args = parser.parse_args()

    docs_root = Path(args.docs_root).resolve()
    missing: dict[Path, str] = {}
    present: dict[Path, str] = {}
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
            if not local_path.exists():
                missing.setdefault(local_path, origin_url)
            elif local_path.suffix != ".md":
                present.setdefault(local_path, origin_url)

    if args.check_versions:
        return check_versions(present, docs_root, args.origin.rstrip("/"), args.delay, args.manifest)

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
