#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
import tomllib
import unicodedata
from collections import deque
from difflib import SequenceMatcher
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote, unquote, urldefrag, urljoin, urlsplit, urlunsplit

SITE = "https://www.bygningsreglementet.dk"
HOSTS = {"www.bygningsreglementet.dk", "bygningsreglementet.dk"}
ASSET_EXTS = {".pdf", ".doc", ".docx", ".xls", ".xlsx", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}
SKIP_PREFIXES = ("/historisk/",)
SKIP_HOSTS = {"historisk.bygningsreglementet.dk"}
SKIP_PATHS = {"/assets/bundle.js"}

SKIP_TAGS = {"nav", "button", "svg", "script", "style", "noscript", "aside", "form", "template", "header", "footer"}
ORIGIN_SKIP_CLASSES = {
    "accordion__actions",
    "anchor-reference__tooltip",
    "cookie-button",
    "search-modal",
    "section-module__actions",
    "skip-links",
    "square__icon",
    "version-selector",
    "visible--xs",
    "visuallyhidden",
}
# md-button links emulate the origin's Krav/Vejledning tab bar, which is chrome on the origin.
LOCAL_SKIP_CLASSES = {"headerlink", "md-button", "md-content__button", "md-source-file"}
LINK_SKIP_CLASSES = {"accordion__trigger"}
VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
BLOCK_TAGS = {
    "address", "article", "blockquote", "caption", "dd", "details", "div", "dl", "dt", "figcaption", "figure",
    "h1", "h2", "h3", "h4", "h5", "h6", "li", "main", "ol", "p", "pre", "section", "summary", "table", "tbody",
    "td", "tfoot", "th", "thead", "tr", "ul",
}
SECTIONS = {
    "S1": "Administrative bestemmelser (krav and vejledning)",
    "S2": "Tekniske bestemmelser chapters 02-04 and 06-08",
    "S3": "Tekniske bestemmelser chapter 05 (Brand)",
    "S4": "Tekniske bestemmelser chapters 09, 10 and 12-14",
    "S5": "Tekniske bestemmelser chapter 11 (Energiforbrug og klimapåvirkning)",
    "S6": "Tekniske bestemmelser chapters 15-18",
    "S7": "Tekniske bestemmelser chapters 19-22",
    "S8": "Øvrige bestemmelser (23-35) and Straf og ikrafttrædelse (36-37)",
    "S9": "Bilag, Nationale annekser, Vejledninger, the front page and all other pages",
}
CHAPTER_SECTIONS = {
    **dict.fromkeys(["02", "03", "04", "06", "07", "08"], "S2"),
    "05": "S3",
    **dict.fromkeys(["09", "10", "12", "13", "14"], "S4"),
    "11": "S5",
    **dict.fromkeys(["15", "16", "17", "18"], "S6"),
    **dict.fromkeys(["19", "20", "21", "22"], "S7"),
}
TYPOGRAPHY = str.maketrans({"\u201c": '"', "\u201d": '"', "\u201e": '"', "\u00ab": '"', "\u00bb": '"', "\u2018": "'", "\u2019": "'", "\u2013": "-", "\u2014": "-", "\u00ad": None, "\u200b": None})
LIST_MARKER = re.compile(r"^\(?(\d{1,3}|[a-zæøå]|[ivxl]{1,5})[.)]$", re.IGNORECASE)
# Differing runs without a word still matter when they carry markdown/markup characters (`* *`, `**`, `\*`).
SIGNIFICANT = re.compile(r"[\w*_`\\#@\[\]{}<>|~^]")
# The origin CMS escapes some line breaks, so they show as literal `<br/>` text where the clone breaks the line.
ESCAPED_BR = re.compile(r"<br\s*/?>", re.IGNORECASE)


class ContentParser(HTMLParser):
    def __init__(self, root_tag: str, root_class: str | None, skip_classes: set[str]) -> None:
        super().__init__(convert_charrefs=True)
        self.root_tag = root_tag
        self.root_class = root_class
        self.skip_classes = skip_classes
        self.all_links: list[str] = []
        self.links: list[str] = []
        self.images: list[str] = []
        self.text: list[str] = []
        self._root: list = []
        self._skip: list = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_d = {k: v or "" for k, v in attrs}
        classes = set(attrs_d.get("class", "").split())
        if tag == "a" and attrs_d.get("href"):
            self.all_links.append(attrs_d["href"])
        if self._skip:
            if tag == self._skip[0]:
                self._skip[1] += 1
            return
        if not self._root:
            if tag == self.root_tag and (self.root_class is None or self.root_class in classes):
                self._root = [tag, 1]
            return
        if tag in VOID_TAGS:
            if tag == "br":
                self.text.append(" ")
            elif tag == "img" and attrs_d.get("src"):
                self.images.append(attrs_d["src"])
            return
        if (tag in SKIP_TAGS and "accordion__nav" not in classes) or classes & self.skip_classes:
            self._skip = [tag, 1]
            return
        if tag == self._root[0]:
            self._root[1] += 1
        if tag in BLOCK_TAGS:
            self.text.append(" ")
        if tag == "a" and attrs_d.get("href") and not classes & LINK_SKIP_CLASSES:
            self.links.append(attrs_d["href"])

    def handle_endtag(self, tag: str) -> None:
        if tag in VOID_TAGS:
            return
        if self._skip:
            if tag == self._skip[0]:
                self._skip[1] -= 1
                if not self._skip[1]:
                    self._skip = []
            return
        if self._root and tag == self._root[0]:
            self._root[1] -= 1
            if not self._root[1]:
                self._root = []
                self.root_tag = ""
        if tag in BLOCK_TAGS:
            self.text.append(" ")

    def handle_data(self, data: str) -> None:
        if self._root and not self._skip:
            self.text.append(data)


def parse(html_text: str, root_tag: str, root_class: str | None, skip_classes: set[str]) -> ContentParser:
    parser = ContentParser(root_tag, root_class, skip_classes)
    parser.feed(html_text)
    parser.close()
    return parser


def words(text: str) -> list[str]:
    text = unicodedata.normalize("NFKC", text).translate(TYPOGRAPHY)
    return [w for w in text.split() if not LIST_MARKER.match(w)]


def text_diff(origin: list[str], local: list[str]) -> tuple[list[str], list[str]]:
    missing: list[str] = []
    extra: list[str] = []
    for op, i1, i2, j1, j2 in SequenceMatcher(None, origin, local, autojunk=False).get_opcodes():
        if op in {"delete", "replace"}:
            missing.append(" ".join(origin[i1:i2]))
        if op in {"insert", "replace"}:
            extra.append(" ".join(local[j1:j2]))
    return [r for r in missing if SIGNIFICANT.search(r)], [r for r in extra if SIGNIFICANT.search(r)]


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
    exact = _case_insensitive_path(docs_root.joinpath(*parts, "index.md"))
    if exact.exists():
        return exact
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


def section_of(url: str) -> str:
    parts = unquote(urlsplit(url).path).lower().strip("/").split("/")
    if parts[0] == "administrative-bestemmelser":
        return "S1"
    if parts[0] == "tekniske-bestemmelser" and len(parts) > 1:
        return CHAPTER_SECTIONS.get(parts[1], "S9")
    if parts[0] in {"ovrige-bestemmelser", "straf-og-ikrafttraedelse"}:
        return "S8"
    return "S9"


class OriginFetcher:
    def __init__(self, origin: str, cache_dir: Path, delay: float) -> None:
        self.origin = origin.rstrip("/")
        self.cache_dir = cache_dir
        self.delay = delay
        self._pw = None
        self._page = None

    def _cache_file(self, url: str) -> Path:
        return self.cache_dir / f"{hashlib.sha256(url.encode()).hexdigest()[:32]}.json"

    def cached(self, url: str) -> bool:
        return self._cache_file(url).exists()

    def get(self, url: str) -> dict:
        target = self._cache_file(url)
        if target.exists():
            return json.loads(target.read_text(encoding="utf-8"))
        rec = self._render(url)
        if rec["status"] is not None and rec["status"] < 500:
            target.parent.mkdir(parents=True, exist_ok=True)
            tmp = target.with_suffix(".tmp")
            tmp.write_text(json.dumps(rec, ensure_ascii=False), encoding="utf-8")
            tmp.replace(target)
        return rec

    def _render(self, url: str) -> dict:
        from playwright.sync_api import Error as PlaywrightError
        from playwright.sync_api import sync_playwright

        if self._page is None:
            self._pw = sync_playwright().start()
            browser = self._pw.chromium.launch(executable_path=os.environ.get("CHROMIUM_PATH") or None)
            self._page = browser.new_page()
            self._page.route(
                "**/*",
                lambda route: route.abort()
                if route.request.resource_type in {"image", "media", "font"}
                else route.continue_(),
            )
        elif self.delay:
            time.sleep(self.delay)
        p = urlsplit(url)
        fetch_url = self.origin + p.path + (f"?{p.query}" if p.query else "")
        print(f"fetch {fetch_url}", file=sys.stderr, flush=True)
        try:
            resp = self._page.goto(fetch_url, wait_until="load", timeout=60_000)
            try:
                self._page.wait_for_load_state("networkidle", timeout=10_000)
            except PlaywrightError:
                pass
            html_text = self._page.content()
        except PlaywrightError as exc:
            return {"url": url, "final": url, "status": None, "error": str(exc).splitlines()[0], "html": ""}
        final = self._page.url
        if final.startswith(self.origin):
            final = SITE + final[len(self.origin):]
        return {"url": url, "final": final, "status": resp.status if resp else None, "html": html_text}

    def close(self) -> None:
        if self._pw is not None:
            self._pw.stop()


def canonical_page(url: str) -> str:
    """The origin serves page paths case-insensitively, with or without a trailing slash."""
    p = urlsplit(url)
    path = quote(unquote(p.path).lower(), safe="/")
    if not path.endswith("/") and not Path(path).suffix:
        path += "/"
    return urlunsplit((p.scheme, p.netloc, path, p.query, ""))


def _show_all_html(fetcher: OriginFetcher, url: str, links: list[str]) -> str | None:
    """Accordion pages load collapsed sections on click; their ShowAll view holds the full content."""
    path = urlsplit(url).path
    for link in sorted({canonical_page(u) for u in links}):
        p = urlsplit(link)
        if p.query == "Layout=ShowAll" and path.startswith(p.path):
            rec = fetcher.get(link)
            return rec["html"] if rec["status"] == 200 else None
    return None


def crawl(
    fetcher: OriginFetcher, sections: set[str], max_pages: int
) -> tuple[dict[str, str], dict[str, str], dict[str, str], dict[str, str], dict[str, str]]:
    """Returns (reference html, own html as served on the page's URL, redirect alias -> target page, fetch errors, origin 4xx)."""
    seed = SITE + "/"
    todo = deque([seed])
    seen: set[str] = set()
    pages: dict[str, str] = {}
    own: dict[str, str] = {}
    redirects: dict[str, str] = {}
    errors: dict[str, str] = {}
    origin_broken: dict[str, str] = {}
    while todo and len(pages) < max_pages:
        url = todo.popleft()
        if url in seen:
            continue
        seen.add(url)
        if section_of(url) not in sections and url != seed and not fetcher.cached(url):
            continue
        rec = fetcher.get(url)
        if rec["status"] != 200:
            if section_of(url) in sections:
                target = errors if rec["status"] is None or rec["status"] >= 500 else origin_broken
                target[url] = rec.get("error") or f"HTTP {rec['status']}"
            continue
        final = canonical_page(normalize_url(rec["final"]) or url)
        page_url = final.split("?", 1)[0]
        if page_url != url:
            redirects[url] = page_url
        if page_url != url and page_url in pages:
            continue
        seen.update({final, page_url})
        hrefs = parse(rec["html"], "main", None, ORIGIN_SKIP_CLASSES).all_links
        links = [u for u in (normalize_url(urljoin(final, href)) for href in hrefs) if u]
        if section_of(final) in sections:
            show_all = urlsplit(final).query == "Layout=ShowAll"
            pages[page_url] = (None if show_all else _show_all_html(fetcher, final, links)) or rec["html"]
            own[page_url] = rec["html"]
        todo.extend(canonical_page(u) for u in links if "?" not in u and not looks_asset(urlsplit(u).path))
    return pages, own, redirects, errors, origin_broken


def _origin_refs(hrefs: list[str], base: str, docs_root: Path, redirects: dict[str, str]) -> tuple[set[str], set[str]]:
    pages: set[str] = set()
    assets: set[str] = set()
    for href in hrefs:
        url = normalize_url(urljoin(base, href))
        if not url:
            continue
        path = urlsplit(url).path
        if path.startswith("/assets/"):
            continue
        if looks_asset(path):
            assets.add(asset_to_doc(path, docs_root).relative_to(docs_root).as_posix())
        else:
            rel = page_to_doc(path, docs_root).relative_to(docs_root).as_posix()
            pages.add(redirects.get(rel, rel))
    return pages, assets


def _local_refs(hrefs: list[str], base: str) -> tuple[set[str], set[str]]:
    pages: set[str] = set()
    assets: set[str] = set()
    for href in hrefs:
        p = urlsplit(urljoin(base, urldefrag(href)[0]))
        if p.netloc != "local":
            continue
        path = unquote(p.path)
        if looks_asset(path):
            assets.add(path.strip("/"))
            continue
        if path.endswith("/index.html"):
            path = path[: -len("index.html")]
        rel = path.strip("/")
        pages.add(f"{rel}/index.md" if rel else "index.md")
    return pages, assets


def _built_page(doc: Path, docs_root: Path, site_dir: Path) -> Path:
    return site_dir / doc.relative_to(docs_root).parent / "index.html"


def _local_view(doc: Path, docs_root: Path, site_dir: Path) -> tuple[ContentParser, str]:
    local = parse(_built_page(doc, docs_root, site_dir).read_text(encoding="utf-8", errors="replace"), "article", "md-content__inner", LOCAL_SKIP_CLASSES)
    return local, "http://local/" + (doc.relative_to(docs_root).parent.as_posix().strip(".") + "/").lstrip("/")


def compare(
    url: str, origin_html: str, docs_root: Path, site_dir: Path, root_url: str | None = None, own_html: str | None = None,
    redirects: dict[str, str] | None = None,
) -> list[tuple[str, str]]:
    """root_url: an alias's guide root; its built page supplies the text, links count from both pages.
    own_html: what the origin shows on the alias's own URL (its own section open); the subpage must keep that text.
    redirects: doc of an origin redirect alias -> doc of its target; links on both sides count as the target."""
    redirects = redirects or {}
    doc = page_to_doc(urlsplit(url).path, docs_root)
    doc_rel = doc.relative_to(docs_root).as_posix()
    built = _built_page(doc, docs_root, site_dir)
    if not root_url and not doc.exists():
        return [("missing_page", f"docs/{doc_rel}")]
    if not root_url and not built.exists():
        return [("missing_page", f"{built.name} not built for docs/{doc_rel}")]
    origin = parse(origin_html, "main", None, ORIGIN_SKIP_CLASSES)
    views = [_local_view(doc, docs_root, site_dir)] if built.exists() else []
    excluded = {doc_rel}
    if root_url:
        root_doc = page_to_doc(urlsplit(root_url).path, docs_root)
        views.insert(0, _local_view(root_doc, docs_root, site_dir))
        excluded.add(root_doc.relative_to(docs_root).as_posix())
    local_pages: set[str] = set()
    local_files: set[str] = set()
    local_images: set[str] = set()
    for view, base in views:
        pages_, files_ = _local_refs(view.links, base)
        pages_ = {redirects.get(p, p) for p in pages_}
        local_pages |= pages_
        local_files |= files_
        local_images |= _local_refs(view.images, base)[1]
    origin_words = words(ESCAPED_BR.sub(" ", "".join(origin.text)))
    missing_text, extra_text = text_diff(origin_words, words("".join(views[0][0].text)))
    if root_url and built.exists():
        # A subpage keeps only its own section of the guide, so only its text that the reference lacks counts.
        own_words = words("".join(views[-1][0].text))
        shown = words(ESCAPED_BR.sub(" ", "".join(parse(own_html, "main", None, ORIGIN_SKIP_CLASSES).text))) if own_html else []
        # The word diff against the long reference can misalign a section-only page; text its own origin page shows is not extra.
        shown_text = f" {' '.join(shown)} "
        extra_text += [f"(own page) {t}" for t in text_diff(origin_words, own_words)[1] if f" {t} " not in shown_text]
        if own_html:
            missing_text += [f"(own page) {t}" for t in text_diff(shown, own_words)[0]]
    origin_pages, origin_files = _origin_refs(origin.links, url, docs_root, redirects)
    origin_images = _origin_refs(origin.images, url, docs_root, redirects)[1]
    diffs = [("missing_text", t) for t in missing_text] + [("extra_text", t) for t in extra_text]
    diffs += [("missing_link", f"docs/{p}") for p in sorted(origin_pages - local_pages - excluded)]
    diffs += [("missing_image", f"docs/{p}") for p in sorted(origin_images - local_images)]
    diffs += [("missing_file", f"docs/{p}") for p in sorted(origin_files - local_files)]
    return diffs


def alias_roots(pages: dict[str, str]) -> dict[str, str]:
    """Guide subpages render the whole guide: a page whose reference text equals an ancestor page's is that guide root's alias."""
    texts = {u: words("".join(parse(h, "main", None, ORIGIN_SKIP_CLASSES).text)) for u, h in pages.items()}
    roots: dict[str, str] = {}
    for url in pages:
        path = urlsplit(url).path
        same = [r for r in pages if r != url and path.startswith(urlsplit(r).path) and texts[r] == texts[url]]
        if same:
            roots[url] = min(same, key=len)
    return roots


KINDS = ("missing_page", "missing_text", "extra_text", "missing_link", "missing_image", "missing_file")


def load_allowlist(path: Path) -> list[dict]:
    entries = tomllib.loads(path.read_text(encoding="utf-8")).get("exception", []) if path.exists() else []
    for n, entry in enumerate(entries, 1):
        if not str(entry.get("reason", "")).strip():
            raise ValueError(f"{path}: exception #{n} has no reason; every allowlist entry must state why")
        if entry.get("kind") not in KINDS or not str(entry.get("page", "")).startswith("/"):
            raise ValueError(f"{path}: exception #{n} needs page (a path like /bilag/b1/) and kind (one of {', '.join(KINDS)})")
    return entries


def apply_allowlist(
    url: str, diffs: list[tuple[str, str]], allowlist: list[dict], root_url: str | None = None
) -> tuple[list[tuple[str, str]], int]:
    """An alias's items other than its (own page) ones are its guide root's, so the root's entries cover them too."""
    path = urlsplit(url).path
    root = urlsplit(root_url).path if root_url else None
    rules = [(e["kind"], e.get("item"), e["page"] == path) for e in allowlist if e["page"] in (path, root)]
    kept = [
        (k, i) for k, i in diffs
        if not any(k == rk and ri in (None, i) and (own or not i.startswith("(own page) ")) for rk, ri, own in rules)
    ]
    return kept, len(diffs) - len(kept)


def render_report(
    results: dict[str, list[tuple[str, str]]],
    allowed: dict[str, int],
    errors: dict[str, str],
    origin_broken: dict[str, str],
    sections: list[str],
    roots: dict[str, str],
) -> str:
    aliases = {u: r for u, r in roots.items() if u in results and not results[u]}
    by_section = {s: {u: d for u, d in sorted(results.items()) if section_of(u) == s} for s in sections}
    lines = [
        "# BR18 content parity audit",
        "",
        f"Sections: {', '.join(sections)}",
        f"Origin pages audited: {len(results)}",
        f"Pages with unexplained differences: {sum(1 for d in results.values() if d)}",
        f"Allowlisted differences: {sum(allowed.values())}",
        f"Alias pages (guide subpages whose guide root covers their reference): {len(aliases)}",
        f"Fetch errors (retried on the next run): {len(errors)}",
        f"Origin URLs answering 4xx (origin's own broken links, not counted): {len(origin_broken)}",
        "",
        "| Section | Pages | With differences | " + " | ".join(KINDS) + " | allowlisted |",
        "|---" * (4 + len(KINDS)) + "|",
    ]
    for s, pages in by_section.items():
        counts = [sum(1 for d in pages.values() for kind, _ in d if kind == k) for k in KINDS]
        lines.append(f"| {s} | {len(pages)} | {sum(1 for d in pages.values() if d)} | " + " | ".join(map(str, counts)) + f" | {sum(allowed[u] for u in pages)} |")
    lines.append("")
    for s, pages in by_section.items():
        lines += [f"## {s} {SECTIONS[s]}", ""]
        for url, diffs in pages.items():
            if not diffs:
                continue
            lines += [f"### {url}", ""]
            if url in roots:
                lines += [f"Compared against its guide root {roots[url]}.", ""]
            lines += [f"- {kind}: {item}" for kind, item in diffs]
            lines.append("")
    if aliases:
        lines += ["## Alias pages", ""]
        lines += [f"- {url} -> {root}" for url, root in sorted(aliases.items())]
        lines.append("")
    if errors:
        lines += ["## Fetch errors", ""]
        lines += [f"- {url}: {err}" for url, err in sorted(errors.items())]
        lines.append("")
    if origin_broken:
        lines += ["## Origin URLs answering 4xx", ""]
        lines += [f"- {url}: {err}" for url, err in sorted(origin_broken.items())]
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--section", action="append", choices=sorted(SECTIONS), help="repeatable; default: all sections")
    ap.add_argument("--docs-root", default="docs")
    ap.add_argument("--site-dir", default="site")
    ap.add_argument("--origin", default=SITE)
    ap.add_argument("--cache-dir", default=".cache/parity-origin")
    ap.add_argument("--allowlist", default="parity-allowlist.toml")
    ap.add_argument("--delay", type=float, default=2.0)
    ap.add_argument("--max-pages", type=int, default=2000)
    ap.add_argument("--output", default="state/br18-parity-audit.md")
    args = ap.parse_args()
    docs_root = Path(args.docs_root).resolve()
    site_dir = Path(args.site_dir).resolve()
    sections = sorted(set(args.section or SECTIONS))
    try:
        allowlist = load_allowlist(Path(args.allowlist))
    except (ValueError, tomllib.TOMLDecodeError) as exc:
        ap.error(str(exc))
    fetcher = OriginFetcher(args.origin, Path(args.cache_dir), args.delay)
    try:
        pages, own, redirects, errors, origin_broken = crawl(fetcher, set(sections), args.max_pages)
    finally:
        fetcher.close()
    results: dict[str, list[tuple[str, str]]] = {}
    allowed: dict[str, int] = {}
    roots = {
        u: r for u, r in alias_roots(pages).items()
        if _built_page(page_to_doc(urlsplit(r).path, docs_root), docs_root, site_dir).exists()
    }
    def doc_of(u: str) -> str:
        return page_to_doc(urlsplit(u).path, docs_root).relative_to(docs_root).as_posix()

    doc_redirects = {doc_of(a): doc_of(t) for a, t in redirects.items()}
    for url, html_text in pages.items():
        diffs = compare(url, html_text, docs_root, site_dir, roots.get(url), own.get(url), doc_redirects)
        results[url], allowed[url] = apply_allowlist(url, diffs, allowlist, roots.get(url))
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render_report(results, allowed, errors, origin_broken, sections, roots), encoding="utf-8")
    print(out)
    for s in sections:
        pages_in = [u for u in results if section_of(u) == s]
        print(f"{s}: pages={len(pages_in)} with_differences={sum(1 for u in pages_in if results[u])}")
    return 1 if errors or any(results.values()) else 0


if __name__ == "__main__":
    raise SystemExit(main())
