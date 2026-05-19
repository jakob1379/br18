#!/usr/bin/env python3
from __future__ import annotations

import argparse
import concurrent.futures as futures
import html
import re
import sys
from collections import deque
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote, unquote, urldefrag, urljoin, urlsplit, urlunsplit
from urllib.request import Request, urlopen

SITE = "https://www.bygningsreglementet.dk"
HOSTS = {"www.bygningsreglementet.dk", "bygningsreglementet.dk"}
ASSET_EXTS = {".pdf", ".doc", ".docx", ".xls", ".xlsx", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}
SKIP_PREFIXES = ("/historisk/",)
SKIP_HOSTS = {"historisk.bygningsreglementet.dk"}
SKIP_PATHS = {"/assets/bundle.js"}

class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[str] = []
        self.title_parts: list[str] = []
        self._in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_d = dict(attrs)
        if tag in {"a", "link"} and attrs_d.get("href"):
            self.links.append(attrs_d["href"] or "")
        if tag in {"img", "script", "source"} and attrs_d.get("src"):
            self.links.append(attrs_d["src"] or "")
        if tag == "title":
            self._in_title = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title_parts.append(data)

    @property
    def title(self) -> str:
        return html.unescape(" ".join(self.title_parts)).strip()


def normalize_url(url: str) -> str | None:
    url, _frag = urldefrag(url)
    p = urlsplit(url)
    if p.scheme not in {"http", "https"}:
        return None
    if p.netloc in SKIP_HOSTS or p.netloc not in HOSTS:
        return None
    path = quote(p.path or "/", safe="/%")
    decoded_path = unquote(path)
    if "localLink:umb:" in decoded_path or path in SKIP_PATHS:
        return None
    if any(path.lower().startswith(prefix) for prefix in SKIP_PREFIXES):
        return None
    query = "Layout=ShowAll" if p.query == "Layout=ShowAll" else ""
    return urlunsplit(("https", "www.bygningsreglementet.dk", path, query, ""))


def fetch(url: str, timeout: int = 30) -> tuple[bytes, str, str]:
    req = Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; br18-parity-audit/1.0)"})
    with urlopen(req, timeout=timeout) as resp:
        data = resp.read()
        ctype = resp.headers.get("content-type", "")
        final = resp.geturl()
    return data, ctype, final


def _case_insensitive_child(parent: Path, name: str) -> Path:
    exact = parent / name
    if exact.exists():
        return exact
    lower = parent / name.lower()
    if lower.exists():
        return lower
    if not parent.exists() or not parent.is_dir():
        return lower
    wanted = name.lower()
    for child in parent.iterdir():
        if child.name.lower() == wanted:
            return child
    return lower


def _case_insensitive_path(path: Path) -> Path:
    parts = path.parts
    if path.is_absolute():
        current = Path(parts[0])
        rest = parts[1:]
    else:
        current = Path(parts[0]) if parts else Path(".")
        rest = parts[1:]
    for part in rest:
        current = _case_insensitive_child(current, part)
    return current


def page_to_doc(path: str, docs_root: Path) -> Path:
    rel = unquote(path).strip("/")
    parts = [part.lower() for part in rel.split("/") if part] if rel else []
    if parts and parts[-1] == "krav":
        parent = _case_insensitive_path(docs_root.joinpath(*parts[:-1], "index.md"))
        if parent.exists():
            return parent
    return _case_insensitive_path(docs_root.joinpath(*parts, "index.md")) if parts else docs_root / "index.md"


def asset_to_doc(path: str, docs_root: Path) -> Path:
    return _case_insensitive_path(docs_root / unquote(path).strip("/"))


def looks_asset(path: str) -> bool:
    suffix = Path(urlsplit(path).path).suffix.lower()
    return suffix in ASSET_EXTS or path.startswith("/media/")


def crawl(seed: str, max_pages: int) -> tuple[set[str], set[str], dict[str, str], dict[str, str]]:
    todo = deque([seed])
    seen: set[str] = set()
    pages: set[str] = set()
    assets: set[str] = set()
    titles: dict[str, str] = {}
    errors: dict[str, str] = {}
    while todo and len(pages) < max_pages:
        url = todo.popleft()
        norm = normalize_url(url)
        if not norm or norm in seen:
            continue
        seen.add(norm)
        p = urlsplit(norm)
        if looks_asset(p.path):
            assets.add(norm)
            continue
        try:
            data, ctype, final = fetch(norm)
        except (HTTPError, URLError, TimeoutError, OSError) as exc:
            errors[norm] = str(exc)
            continue
        final_norm = normalize_url(final) or norm
        fp = urlsplit(final_norm)
        if looks_asset(fp.path):
            assets.add(final_norm)
            continue
        if "html" not in ctype.lower() and b"<html" not in data[:1024].lower():
            assets.add(final_norm)
            continue
        pages.add(final_norm)
        text = data.decode("utf-8", errors="ignore")
        parser = LinkParser()
        parser.feed(text)
        titles[final_norm] = parser.title
        for link in parser.links:
            joined = normalize_url(urljoin(final_norm, link))
            if not joined or joined in seen:
                continue
            jp = urlsplit(joined)
            if looks_asset(jp.path):
                assets.add(joined)
            else:
                # Crawl normal page routes; use ShowAll only where already linked/redirected.
                todo.append(joined)
    return pages, assets, titles, errors


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--docs-root", default="docs")
    ap.add_argument("--max-pages", type=int, default=2000)
    ap.add_argument("--output", default="state/br18-parity-audit.md")
    args = ap.parse_args()
    docs_root = Path(args.docs_root).resolve()
    pages, assets, titles, errors = crawl(SITE + "/", args.max_pages)

    missing_pages = []
    for url in sorted(pages):
        p = urlsplit(url)
        doc = page_to_doc(p.path, docs_root)
        if not doc.exists():
            missing_pages.append((url, doc.relative_to(docs_root)))

    missing_assets = []
    for url in sorted(assets):
        p = urlsplit(url)
        doc = asset_to_doc(p.path, docs_root)
        if not doc.exists():
            missing_assets.append((url, doc.relative_to(docs_root)))

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# BR18 parity audit", "", f"Pages crawled: {len(pages)}", f"Assets linked: {len(assets)}", f"Fetch errors: {len(errors)}", f"Missing page docs: {len(missing_pages)}", f"Missing assets: {len(missing_assets)}", ""]
    if missing_pages:
        lines += ["## Missing page docs", ""]
        lines += [f"- {url} -> `{rel}`" for url, rel in missing_pages[:500]]
        if len(missing_pages) > 500:
            lines.append(f"- ... {len(missing_pages) - 500} more")
        lines.append("")
    if missing_assets:
        lines += ["## Missing assets", ""]
        lines += [f"- {url} -> `{rel}`" for url, rel in missing_assets[:500]]
        if len(missing_assets) > 500:
            lines.append(f"- ... {len(missing_assets) - 500} more")
        lines.append("")
    if errors:
        lines += ["## Fetch errors", ""]
        lines += [f"- {url}: {err}" for url, err in sorted(errors.items())[:200]]
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(out)
    print(f"pages={len(pages)} assets={len(assets)} missing_pages={len(missing_pages)} missing_assets={len(missing_assets)} errors={len(errors)}")
    return 1 if missing_pages or missing_assets else 0

if __name__ == "__main__":
    raise SystemExit(main())
