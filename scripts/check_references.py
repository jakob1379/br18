#!/usr/bin/env python3

from __future__ import annotations

import argparse
import html
import http.client
import json
import posixpath
import re
import sys
import time
import tomllib
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

REPO = Path(__file__).resolve().parent.parent
API = "https://www.retsinformation.dk/api/document"
TITLE_RE = re.compile(r"^(?P<law>.+?) (?:(?P<sign>§§?) (?P<lo>\d+[a-zA-Z]?)(?:-(?P<hi>\d+[a-zA-Z]?))?|kapitel (?P<chapter>\d+)(?:-\d+)?|bilag (?P<annex>\d+)(?:, tabel (?P<table>\w+))?)$")
HEADING_RE = re.compile(r"^§\s*(\d+)\s?([a-zæøå])?(?![a-zæøå\d])(?:\s*[-–]\s*§\s*(\d+)\s?([a-zæøå])?)?")
CHAPTER_RANGE_RE = re.compile(r"\(§\s*(\d+)\s?([a-z])?\s*[-–]\s*§\s*(\d+)\s?([a-z])?\)")
ID_RE = re.compile(r'\b(?i:id)="(P\d+[A-Za-z]*,?)"')


def key(text: str) -> tuple[int, str]:
    m = re.match(r"(\d+)\s?([a-zA-Z]?)", text)
    return int(m.group(1)), m.group(2).lower()


class Page(HTMLParser):

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.inside = False
        self.ids: dict[str, str] = {}
        self.h1 = ""
        self.refs: list[dict] = []
        self.problems: list[str] = []
        self.text: list[str] = []
        self.heading: tuple[str, str] | None = None
        self.heading_text: list[str] = []
        self.anchors: list[dict | None] = []

    def handle_starttag(self, tag: str, attrs: list) -> None:
        a = dict(attrs)
        classes = (a.get("class") or "").split()
        if tag == "article":
            self.inside = True
        if not self.inside:
            return
        if a.get("id"):
            self.ids.setdefault(a["id"], "")
            if re.fullmatch(r"h[1-6]", tag):
                self.heading, self.heading_text = (tag, a["id"]), []
        elif tag == "h1":
            self.heading, self.heading_text = (tag, ""), []
        if "br18-ref" in classes and tag != "a":
            self.problems.append(f"class br18-ref on <{tag}>")
        if tag == "a":
            if "br18-ref" in classes:
                if any(self.anchors):
                    self.problems.append(f"br18-ref nested in another link: {a.get('href')}")
                ref = {"href": a.get("href", ""), "title": a.get("title", ""), "text": "", "ext": "br18-ref--ext" in classes}
                self.refs.append(ref)
                self.anchors.append(ref)
            else:
                self.anchors.append({"other": True})

    def handle_endtag(self, tag: str) -> None:
        if tag == "article":
            self.inside = False
        if not self.inside:
            return
        if tag == "a" and self.anchors:
            self.anchors.pop()
        if self.heading and tag == self.heading[0]:
            text = re.sub(r"\s+", " ", "".join(self.heading_text).replace("¶", "")).strip()
            if self.heading[1]:
                self.ids[self.heading[1]] = text
            if tag == "h1" and not self.h1:
                self.h1 = text
            self.heading = None

    def handle_data(self, data: str) -> None:
        if not self.inside:
            return
        self.text.append(data)
        if self.heading:
            self.heading_text.append(data)
        for ref in self.anchors:
            if ref and "text" in ref:
                ref["text"] += data


def load_laws(path: Path) -> dict:
    return tomllib.loads(path.read_text(encoding="utf-8")).get("laws", {})


class Site:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.cache: dict[str, Page | None] = {}

    def page(self, rel: str) -> Page | None:
        if rel not in self.cache:
            path = self.root / rel / "index.html" if rel else self.root / "index.html"
            page = None
            if path.is_file():
                page = Page()
                page.feed(path.read_text(encoding="utf-8", errors="replace"))
            self.cache[rel] = page
        return self.cache[rel]


def covers(heading: str, lo: tuple[int, str], hi: tuple[int, str] | None) -> bool:
    m = HEADING_RE.match(heading)
    if not m:
        return False
    start = (int(m.group(1)), m.group(2) or "")
    if m.group(3):
        return start <= lo <= (int(m.group(3)), m.group(4) or "")
    return start == lo


def check_local(site: Site, page_rel: str, ref: dict, m: re.Match[str]) -> str | None:
    href = urlsplit(ref["href"])
    target_rel = page_rel if not href.path else posixpath.normpath(posixpath.join(page_rel, href.path)).strip("/")
    target_rel = "" if target_rel == "." else target_rel
    target = site.page(target_rel)
    if target is None:
        return f"no page {target_rel}/"
    fragment = href.fragment
    if fragment and fragment not in target.ids:
        return f"no id #{fragment} on {target_rel}/"
    if m.group("chapter"):
        n = int(m.group("chapter"))
        expected = "administrative-bestemmelser/krav" if n == 1 else None
        parts = target_rel.split("/")
        ok = target_rel == expected or (len(parts) == 3 and parts[2] == "krav" and parts[1].isdigit() and int(parts[1]) == n and n > 1)
        return None if ok and not fragment and CHAPTER_RANGE_RE.search(target.h1) else f"{target_rel}/ is not chapter {n}"
    if m.group("annex"):
        n = m.group("annex")
        if not (target_rel == f"bilag/b{n}/bilag_{n}" or (fragment and target_rel.startswith(f"bilag/b{n}/bilag_{n}/"))):
            return f"{target_rel}/ is not bilag {n}"
        table = m.group("table")
        if table and not re.match(rf"[Tt]abel {re.escape(table)}(?![\w.])", target.ids.get(fragment, "")):
            return f"#{fragment} is not tabel {table}: {target.ids.get(fragment)!r}"
        return None if table or not fragment else f"bilag link with fragment #{fragment}"
    lo = key(m.group("lo"))
    hi = key(m.group("hi")) if m.group("hi") else None
    if not fragment:
        r = CHAPTER_RANGE_RE.search(target.h1)
        whole = r and (int(r.group(1)), r.group(2) or "") <= lo and (hi or lo) <= (int(r.group(3)), r.group(4) or "")
        return None if whole else f"{target_rel}/ ({target.h1!r}) does not cover {ref['title']}"
    heading = target.ids[fragment]
    return None if covers(heading, lo, hi) else f"#{fragment} ({heading!r}) does not cover {ref['title']}"


def check_external(laws: dict, ref: dict, m: re.Match[str]) -> str | None:
    eli, _, fragment = ref["href"].partition("#")
    law = next((entry for entry in laws.values() if entry["eli"] == eli), None)
    if law is None:
        return f"{eli} is not a law version in xref-laws.toml"
    if m.group("law") != law["title"]:
        return f"title names {m.group('law')!r}, href is {law['title']}"
    if fragment not in law.get("ids", []):
        return f"#{fragment} is not a cached fragment id of {law['title']}"
    if not m.group("sign") or not fragment.rstrip(",").lower() == f"p{m.group('lo')}".lower():
        return f"#{fragment} is not {ref['title']}"
    return None


def check_site(site_dir: Path, laws: dict) -> int:
    site = Site(site_dir)
    problems = []
    count = 0
    for path in sorted(site_dir.rglob("index.html")):
        rel = path.parent.relative_to(site_dir).as_posix()
        rel = "" if rel == "." else rel
        page = site.page(rel)
        text = html.unescape("".join(page.text))
        if re.search(r"\{\s*:?\s*\.br18-ref|\]\([^)\s]*\s+\"BR18 ", text):
            problems.append(f"{rel}/: reference markup shown as text")
        problems.extend(f"{rel}/: {p}" for p in page.problems)
        for ref in page.refs:
            count += 1
            m = TITLE_RE.match(ref["title"])
            if not m:
                problems.append(f"{rel}/: {ref['href']}: unparsable title {ref['title']!r}")
                continue
            number = m.group("lo") or m.group("chapter") or m.group("table") or m.group("annex")
            digits = re.match(r"\d+", number).group()
            error = None if re.search(rf"(?<!\d){digits}(?!\d)", ref["text"]) else f"link text {ref['text']!r} does not name {number}"
            if not ref["ext"] and m.group("law") != "BR18":
                error = error or f"local link titled {m.group('law')!r}"
            error = error or (check_external(laws, ref, m) if ref["ext"] else check_local(site, rel, ref, m))
            if error:
                problems.append(f"{rel}/: [{ref['text']}]({ref['href']}): {error}")
    for p in problems:
        print(p)
    print(f"br18-ref links: {count}, problems: {len(problems)}", file=sys.stderr)
    return 1 if problems else 0


def fetch(api: str, eli: str) -> dict:
    url = f"{api}/{urlsplit(eli).path.strip('/')}"
    request = urllib.request.Request(url, data=json.dumps({"isRawHtml": False}).encode(), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.load(response)[0]


def write_laws(path: Path, laws: dict) -> None:
    header = [line for line in path.read_text(encoding="utf-8").splitlines() if line.startswith("#")]
    lines = [*header, ""]
    for name, entry in laws.items():
        lines.append(f"[laws.{name}]")
        lines.extend(f"{k} = {json.dumps(v, ensure_ascii=False)}" for k, v in entry.items())
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def check_laws_online(path: Path, api: str, delay: float, update: bool) -> int:
    laws = load_laws(path)
    problems = []
    for i, (name, entry) in enumerate(laws.items()):
        if i:
            time.sleep(delay)
        try:
            record = fetch(api, entry["eli"])
        except (OSError, ValueError, IndexError, http.client.HTTPException) as error:
            problems.append(f"{name}: {entry['eli']}: fetch failed: {error}")
            continue
        if record.get("isHistorical"):
            problems.append(f"{name}: {entry['eli']} ({record.get('shortName')}) is historical since {record.get('historicalDate')}; find its successor")
        live = list(dict.fromkeys(ID_RE.findall(record.get("documentHtml", ""))))
        if update:
            entry["ids"] = live
            continue
        lost = [i for i in entry.get("ids", []) if i not in live]
        if lost:
            problems.append(f"{name}: {entry['eli']} no longer has fragment ids {lost[:10]}")
    if update:
        write_laws(path, laws)
    for p in problems:
        print(p)
    print(f"laws: {len(laws)}, problems: {len(problems)}", file=sys.stderr)
    return 1 if problems else 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site-dir", type=Path, default=REPO / "site")
    parser.add_argument("--laws", type=Path, default=REPO / "xref-laws.toml")
    parser.add_argument("--laws-online", action="store_true", help="check the laws' status on retsinformation.dk (network)")
    parser.add_argument("--update", action="store_true", help="with --laws-online: rewrite the cached fragment id lists")
    parser.add_argument("--api", default=API)
    parser.add_argument("--delay", type=float, default=2.0, help="seconds between retsinformation requests")
    args = parser.parse_args()
    if args.laws_online:
        return check_laws_online(args.laws, args.api, args.delay, args.update)
    return check_site(args.site_dir, load_laws(args.laws))


if __name__ == "__main__":
    raise SystemExit(main())
