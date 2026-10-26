#!/usr/bin/env python3

from __future__ import annotations

import argparse
import posixpath
import re
import sys
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BR18 = "br18"
OTHER = "other"
S = r"[ \t ]"
L = "a-zæøåA-ZÆØÅ"

REGULATION_PAGE_RE = re.compile(
    r"^(?:(?:administrative-bestemmelser|(?:tekniske-bestemmelser|ovrige-bestemmelser|straf-og-ikrafttraedelse)/\d\d)/(?:index\.md|krav/.*)|bilag/b\d/bilag_\d/.*)$"
)
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*(?:\{#([^}\s]+)[^}]*\})?\s*$")
SECTION_HEADING_RE = re.compile(rf"^§{S}*(\d+){S}?([a-zæøå])?(?![{L}\d])(?:{S}*[-–]{S}*§{S}*(\d+){S}?([a-zæøå])?(?![{L}\d]))?")
CHAPTER_RANGE_RE = re.compile(rf"\(§{S}*(\d+){S}?([a-z])?{S}*[-–]{S}*§{S}*(\d+){S}?([a-z])?\)\s*$")
TABLE_HEADING_RE = re.compile(r"^[Tt]abel\s+(\d+[a-z]?)(?![\w.])")
BLOCK_TAG_RE = re.compile(r"^\s{0,3}<(table|div|p|ul|ol|li|dl|tr|td|th|thead|tbody|blockquote|section|details|figure|center)\b", re.I)
PROTECTED_RE = re.compile(
    r"(`+).*?\1"
    r"|!?\[(?:[^\[\]]|\[[^\]]*\])*\]\([^)]*\)(?:\{[^}]*\})?"
    r"|\[\^[^\]]+\]|\[[^\]]*\]\[[^\]]*\]"
    r"|<a\b.*?(?:</a>|$)"
    r"|<[A-Za-z/!][^>]*>?"
    r"|\{[^}]*\}"
    r"|https?://\S+"
)
FENCE_RE = re.compile(r"^\s*(```|~~~)")
SKIP_LINE_RE = re.compile(r"^\s{0,3}(?:#{1,6}\s|\*\[|[=-]{3,}\s*$|\|?\s*:?-{3,})")

SECTION_SIGN_RE = re.compile(r"§§?")
NUMBER_RE = re.compile(rf"{S}*(\d+)(?![\d])(?![.,]\d)")
LETTER_RE = re.compile(rf"({S}?)([{L}])(?![{L}\d])")
RANGE_SEP_RE = re.compile(rf"{S}*(?:-|–|—|{S}til{S}){S}*(§{S}*)?")
NUMBERS = rf"\d+(?![\d]|\.{S}*pkt)(?:{S}*(?:-|–|,{S}*(?:og|eller)?|og|eller){S}*\d+(?![\d]|\.{S}*pkt))*"
TAIL_RE = re.compile(
    rf",?{S}*(?:(?:(?:og|eller){S}+)?stk\.{S}*{NUMBERS}|(?:(?:og|eller){S}+)?nr\.{S}*{NUMBERS}|litra{S}+[a-zæø](?![\wæøå])(?:{S}*(?:,|og|eller|-){S}*[a-zæø](?![\wæøå]))*|\d+\.{S}*(?:pkt|punktum)\.?)"
)
STK_LIST_RE = re.compile(rf"(?:stk|nr)\.{S}*\d+{S}*(?:,|og|eller){S}*\d")
LIST_SEP_RE = re.compile(rf"{S}*,{S}*(?:(?:og|eller|samt){S}+)?|{S}+(?:og|eller|samt){S}+")
BARE_END_RE = re.compile(rf"{S}*(?:[,.;:)\]]|$|,?{S}*stk\.)")
CHAPTER_RE = re.compile(rf"\b([Kk]apitel|[Kk]ap\.){S}*(\d{{1,2}})(?![\d]|[.,]\d)")
ANNEX_RE = re.compile(rf"\b[Bb]ilag{S}+(\d{{1,2}})(?![\d]|[.,]\d)(?:{S}*,?{S}*[Tt]abel{S}+(\d+[a-z]?)(?![\w]|\.\d))?")
CHAPTER_TOPIC_RE = re.compile(rf"{S}*(?:om{S}+|[–:-]{S}*|vedr\.{S}+|vedrørende{S}+|\({S}*)?[\"”“]?([{L}]+)")
MORE_RE = re.compile(rf"(?:{S}*,{S}*(?:(?:og|eller){S}+)?|{S}+(?:og|eller){S}+)(\d{{1,2}}[a-z]?)(?![\w]|[.,]\d|\.{S}*pkt)")
RANGE_TAIL_RE = re.compile(rf"{S}*[-–]{S}*(\d{{1,2}})(?![\d]|[.,]\d)")

BR18_BEFORE_RE = re.compile(
    rf"(?:\bBR{S}?18s?|\bbygningsreglement(?:et|ets){S}*(?:2018)?|\breglementets){S}*(?:\(BR{S}?18\))?{S}*,?{S}*(?:(?:kap\.|kapitel){S}*\d+{S}*,?{S}*)?$",
    re.I,
)
BR18_AFTER_RE = re.compile(rf"^{S}*,?{S}*(?:i|efter){S}+(?:dette{S}+)?(?:bygningsreglement(?:et)?\b|BR{S}?18\b)", re.I)
GENITIVE_RE = re.compile(rf"([{L}][{L}\-]{{2,}}s){S}*,?{S}*$")
NOT_GENITIVE = {
    "hvis", "mens", "henholdsvis", "dels", "tværs", "indtil", "ifølge", "bortses", "anvendes", "angives",
    "nævnes", "fastsættes", "opfyldes", "henvises", "kræves", "følges", "gælds", "ses", "findes", "skønnes",
    "omfattes", "behandles", "regnes", "foretages", "tages", "udføres", "fremgås", "jvf", "rs", "bygningsreglementets",
    "reglementets", "br18s", "kapitels", "stks",
}
INSTRUMENT_BEFORE_RE = re.compile(
    rf"(?:loven|lov|lovs|bekendtgørelsen|bekendtgørelse|cirkulæret|cirkulære|forordningen|forordning|direktivet|direktiv|reglementet|vedtægten|regulativet|m\.v\.|mv\.|\b(?:19|20)\d\d){S}*,?{S}*$",
    re.I,
)
INSTRUMENT_AFTER_RE = re.compile(
    rf"^{S}*,?{S}*(?:i|efter|til){S}+(?:den{S}+|denne{S}+|dette{S}+|nævnte{S}+|samme{S}+|gældende{S}+)*"
    rf"(?:[\w\-]*lov(?:en|ens|s)?\b|lov{S}+(?:om|nr)|[\w\-]*bekendtgørelse|[\w\-]*cirkulære|forordning|direktiv|(?-i:DS|EN|ISO|SBi)\b|[\w\-]*vejledning|rapport|regulativ|standard|anvisning|(?-i:[A-ZÆØÅ][\w\-]*s)\b)",
    re.I,
)
GUIDE_TITLE_BEFORE_RE = re.compile(rf"vejledning(?:en)?{S}+(?:om|til){S}+(?:BR{S}?18{S}*,?{S}*|bygningsreglementets{S}+|bygningsreglementet{S}*,?{S}*)?$", re.I)
OTHER_DOC_AFTER_RE = re.compile(rf"^{S}*,?{S}*(?:i|til|efter){S}+(?!bygningsreglement|BR{S}?18)\S", re.I)
CLEAN_RE = re.compile(r"\[\\?\[\d+\\?\]\]\([^)]*\)(?:\{[^}]*\})?|\]\([^)]*\)(?:\{[^}]*\})?|<[^>]+>|\^[^^\s]{1,4}\^|\[\^?\d+\]|[\[\]*_\\]")


@dataclass
class Item:
    start: int
    end: int
    key: tuple[int, str]
    end_key: tuple[int, str] | None = None
    letter_end: int = 0
    bare_end: int = 0


@dataclass
class Ref:
    start: int
    end: int
    items: list[Item] = field(default_factory=list)
    ambiguous: bool = False


@dataclass
class Target:
    page: str
    anchor: str = ""


@dataclass
class Corpus:
    sections: dict[tuple[int, str], Target]
    groups: list[tuple[tuple[int, str], tuple[int, str], Target]]
    chapters: dict[int, tuple[str, tuple[int, str], tuple[int, str], str]]
    tables: dict[tuple[int, str], Target]


def key_of(number: str, letter: str | None) -> tuple[int, str]:
    return int(number), (letter or "")


def key_text(key: tuple[int, str]) -> str:
    return f"{key[0]}{key[1]}"


def chapter_dir(rel: str) -> str:
    return posixpath.dirname(rel)


def load_corpus(docs: Path) -> Corpus:
    sections: dict[tuple[int, str], Target] = {}
    groups = []
    chapters = {}
    tables = {}
    roots = sorted(docs.glob("*/krav/index.md")) + sorted(docs.glob("*/[0-9][0-9]/krav/index.md"))
    for root in roots:
        page = root.relative_to(docs).parent.as_posix()
        chapter = 1 if page.startswith("administrative-bestemmelser/") else int(page.split("/")[1])
        for line in root.read_text(encoding="utf-8").splitlines():
            m = HEADING_RE.match(line)
            if not m:
                continue
            level, text, anchor = len(m.group(1)), m.group(2), m.group(3)
            if level == 1:
                r = CHAPTER_RANGE_RE.search(text)
                if r:
                    chapters[chapter] = (page, key_of(r.group(1), r.group(2)), key_of(r.group(3), r.group(4)), text.split()[0].lower())
                continue
            s = SECTION_HEADING_RE.match(text)
            if not s or not anchor:
                continue
            lo = key_of(s.group(1), s.group(2))
            if s.group(3):
                groups.append((lo, key_of(s.group(3), s.group(4)), Target(page, anchor)))
            elif lo not in sections or anchor.startswith("paragraf-"):
                sections[lo] = Target(page, anchor)
    for annex in sorted(docs.glob("bilag/b[0-9]/bilag_[0-9]/index.md")):
        page = annex.relative_to(docs).parent.as_posix()
        number = int(page[-1])
        for line in annex.read_text(encoding="utf-8").splitlines():
            m = HEADING_RE.match(line)
            t = m and m.group(3) and TABLE_HEADING_RE.match(m.group(2))
            if t:
                tables.setdefault((number, t.group(1)), Target(page, m.group(3)))
        tables[(number, "")] = Target(page)
    return Corpus(sections, groups, chapters, tables)


def load_toml(path: Path) -> dict:
    return tomllib.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


class Laws:
    def __init__(self, data: dict) -> None:
        self.laws = data.get("laws", {})
        names = [(name.lower(), law) for law, entry in self.laws.items() for name in entry.get("names", [])]
        self.names = sorted(names, key=lambda n: -len(n[0]))

    def before(self, prefix: str) -> str | None:
        low = prefix.lower().rstrip(" \t ,")
        for name, law in self.names:
            for form in (name, name + "s"):
                if low.endswith(form) and not re.match(rf"[{L}]", low[-len(form) - 1 : -len(form)] or " "):
                    return law
        return None

    def after(self, postfix: str) -> str | None:
        m = re.match(rf"^{S}*,?{S}*(?:i|efter){S}+(?:den{S}+|gældende{S}+)*", postfix, re.I)
        if not m:
            return None
        low = postfix[m.end() :].lower()
        for name, law in self.names:
            if low.startswith(name) and not re.match(rf"[{L}]", low[len(name) : len(name) + 1] or " "):
                return law
        return None

    def fragment(self, law: str, key: tuple[int, str]) -> str | None:
        wanted = f"p{key_text(key)}".lower()
        return next((i for i in self.laws[law].get("ids", []) if i.rstrip(",").lower() == wanted), None)


def clean(text: str) -> str:
    return CLEAN_RE.sub("", text)


class Context:

    def __init__(self, line: str) -> None:
        self.line = line

    def __call__(self, start: int, end: int) -> str:
        return (clean(self.line[:start])[-60:] + clean(self.line[start:end]) + clean(self.line[end:])[:30]).strip()


def protected_mask(line: str, in_anchor: bool) -> tuple[str, bool]:
    chars = list(line)
    pos = 0
    if in_anchor:
        close = line.find("</a>")
        end = len(line) if close < 0 else close + 4
        chars[:end] = "\0" * end
        if close < 0:
            return "".join(chars), True
        pos = end
    open_anchor = False
    for m in PROTECTED_RE.finditer(line, pos):
        chars[m.start() : m.end()] = "\0" * (m.end() - m.start())
        if m.group(0).startswith("<a") and not m.group(0).endswith("</a>"):
            open_anchor = True
    return "".join(chars), open_anchor


def parse_item(text: str, pos: int, item_start: int, letter_expected: bool = False) -> Item | None:
    m = NUMBER_RE.match(text, pos)
    if not m:
        return None
    number_end = m.end()
    item = Item(item_start, number_end, (int(m.group(1)), ""), bare_end=number_end)
    letter = LETTER_RE.match(text, number_end)
    if letter:
        after = text[letter.end() :]
        spaced_word = not letter_expected and letter.group(1) and letter.group(2) == "i" and not re.match(rf"{S}*(?:[,.;:)\]]|$)", after)
        if not spaced_word:
            item.key = (item.key[0], letter.group(2))
            item.letter_end = letter.end()
    end = item.letter_end or number_end
    rng = RANGE_SEP_RE.match(text, end)
    if rng and (rng.group(1) or text.startswith("§§", item_start) or not re.search(r"til", rng.group(0))):
        hi = parse_item(text, rng.end(), item_start, letter_expected=bool(item.key[1]))
        if hi and not hi.end_key:
            item.end_key = hi.key
            item.bare_end = hi.bare_end
            item.letter_end = hi.letter_end
            end = hi.letter_end or hi.bare_end
    while tail := TAIL_RE.match(text, end):
        end = tail.end()
    item.end = end
    return item


def followers(text: str, pos: int) -> list[re.Match[str]]:
    found = []
    while m := MORE_RE.match(text, pos):
        found.append(m)
        pos = m.end()
    return found


def scan_refs(text: str) -> list[Ref]:
    refs = []
    pos = 0
    while m := SECTION_SIGN_RE.search(text, pos):
        double = m.group(0) == "§§"
        first = parse_item(text, m.end(), m.start())
        if not first:
            pos = m.end()
            continue
        ref = Ref(m.start(), first.end, [first])
        while sep := LIST_SEP_RE.match(text, ref.end):
            nxt = sep.end()
            sign = SECTION_SIGN_RE.match(text, nxt)
            if sign:
                item = parse_item(text, sign.end(), nxt)
            else:
                item = parse_item(text, nxt, nxt)
                bare_ok = double or (re.search(r"og|eller", sep.group(0)) and item and BARE_END_RE.match(text, item.end))
                if item and not bare_ok:
                    item = None
            if not item:
                break
            ref.items.append(item)
            ref.end = item.end
        ref.ambiguous = double and any(STK_LIST_RE.search(text, i.start, i.end) for i in ref.items)
        refs.append(ref)
        pos = ref.end
    return refs


class Linker:
    def __init__(self, docs: Path, data: Path) -> None:
        self.docs = docs
        self.corpus = load_corpus(docs)
        self.laws = Laws(load_toml(data / "xref-laws.toml"))
        self.scope = sorted(load_toml(data / "xref-page-scope.toml").get("scope", {}).items(), key=lambda kv: -len(kv[0]))
        self.overrides = load_toml(data / "xref-overrides.toml").get("override", [])
        for entry in self.overrides:
            if entry.get("law") not in {BR18, "skip", *self.laws.laws} or not entry.get("reason", "").strip() or not entry.get("page") or not entry.get("text"):
                raise SystemExit(f"invalid override (needs page, text, reason and law = br18, skip or a law in xref-laws.toml): {entry}")
        self.used_overrides: set[int] = set()
        self.unresolved: dict[tuple[str, str, str], list[str]] = {}

    def page_law(self, rel: str) -> str | None:
        if REGULATION_PAGE_RE.match(rel):
            return BR18
        return next((law for prefix, law in self.scope if rel.startswith(prefix)), None)

    def note(self, rel: str, text: str, reason: str, context: str) -> None:
        self.unresolved.setdefault((text, reason, context), []).append(rel)

    def override(self, rel: str, text: str) -> str | None:
        for i, entry in enumerate(self.overrides):
            if entry.get("page") == rel and entry.get("text") == text:
                self.used_overrides.add(i)
                return entry["law"]
        return None

    def href(self, rel: str, target: Target, own_ids: set[str]) -> str:
        if target.anchor and target.anchor in own_ids:
            return f"#{target.anchor}"
        here = chapter_dir(rel)
        path = posixpath.relpath(target.page, here) if here else target.page
        path = "./" if path == "." else f"{path}/"
        return path + (f"#{target.anchor}" if target.anchor else "")

    def section_target(self, key: tuple[int, str]) -> Target | None:
        if key in self.corpus.sections:
            return self.corpus.sections[key]
        if key[1]:
            return None
        covering = [g for g in self.corpus.groups if g[0] <= key <= g[1]]
        return min(covering, key=lambda g: (g[1][0] - g[0][0]))[2] if covering else None

    def br18_item(self, item: Item) -> tuple[Target, str] | str:
        if item.end_key:
            lo, hi = item.key, item.end_key
            if not (lo < hi and self.section_target(lo) and self.section_target(hi)):
                return f"§§ {key_text(lo)}-{key_text(hi)} is not a BR18 range"
            title = f"BR18 §§ {key_text(lo)}-{key_text(hi)}"
            group = next((g[2] for g in self.corpus.groups if g[0] == lo and g[1] == hi), None)
            if group:
                return group, title
            chapter = next((c for c in self.corpus.chapters.values() if c[1] == lo and c[2] == hi), None)
            if chapter:
                return Target(chapter[0]), title
            return self.section_target(lo), title
        target = self.section_target(item.key)
        if not target:
            return f"§ {key_text(item.key)} is not a BR18 paragraph"
        return target, f"BR18 § {key_text(item.key)}"

    def law_item(self, law: str, item: Item) -> tuple[str, str] | str:
        entry = self.laws.laws[law]
        lo = self.laws.fragment(law, item.key)
        if not lo or (item.end_key and not self.laws.fragment(law, item.end_key)):
            return f"§ {key_text(item.key)} not in the current {entry['title']} ({entry['eli']})"
        sign = f"§§ {key_text(item.key)}-{key_text(item.end_key)}" if item.end_key else f"§ {key_text(item.key)}"
        return f"{entry['eli']}#{lo}", f"{entry['title']} {sign}"

    def ref_law(self, rel: str, line: str, ref: Ref, text: str) -> tuple[str | None, str]:
        prefix, postfix = clean(line[: ref.start]), clean(line[ref.end :])
        signals = set()
        if BR18_BEFORE_RE.search(prefix):
            signals.add(BR18)
        elif law := self.laws.before(prefix):
            signals.add(law)
        else:
            g = GENITIVE_RE.search(prefix)
            if (g and g.group(1).lower() not in NOT_GENITIVE) or INSTRUMENT_BEFORE_RE.search(prefix):
                signals.add(OTHER)
        if law := self.laws.after(postfix):
            signals.add(law)
        elif BR18_AFTER_RE.match(postfix):
            signals.add(BR18)
        elif INSTRUMENT_AFTER_RE.match(postfix):
            signals.add(OTHER)
        if len(signals) > 1:
            return None, "conflicting instruments named"
        if signals:
            law = signals.pop()
            return (None, "instrument not in xref-laws.toml") if law == OTHER else (law, "named")
        forced = self.override(rel, text)
        if forced:
            return forced, "override"
        law = self.page_law(rel)
        if law == BR18 and any(item.key[1].isupper() or (item.end_key and item.end_key[1].isupper()) for item in ref.items):
            return None, "uppercase letter: not BR18, no law named"
        return (law, "page") if law else (None, "page has no default law (xref-page-scope.toml)")

    def link_line(self, rel: str, line: str, masked: str, html: bool, own_ids: set[str], regulation: bool) -> str:
        edits: list[tuple[int, int, str, str, bool]] = []
        context = Context(line)
        for ref in scan_refs(masked):
            text = line[ref.start : ref.end]
            law, why = self.ref_law(rel, line, ref, text)
            if law == "skip":
                continue
            if ref.ambiguous and why != "override":
                self.note(rel, text, "§§ list with stk./nr. lists: items ambiguous", context(ref.start, ref.end))
                continue
            if not law:
                self.note(rel, text, why, context(ref.start, ref.end))
                continue
            planned = []
            for i, item in enumerate(ref.items):
                if law == BR18 and (item.key[1].isupper() or (item.end_key or (0, ""))[1].isupper()):
                    resolved: tuple | str = "uppercase letter is not BR18"
                elif law == BR18:
                    resolved = self.br18_item(item)
                    if isinstance(resolved, tuple):
                        resolved = (self.href(rel, resolved[0], own_ids), resolved[1])
                else:
                    resolved = self.law_item(law, item)
                if isinstance(resolved, str):
                    self.note(rel, line[item.start : item.end], resolved, context(ref.start, ref.end))
                    continue
                planned.append((item.start, item.end, resolved[0], resolved[1], law != BR18))
            edits.extend(planned)
        for m in CHAPTER_RE.finditer(masked):
            self.chapter(rel, line, masked, m, edits, own_ids, regulation, context)
        for m in ANNEX_RE.finditer(masked):
            self.annex(rel, line, masked, m, edits, own_ids, regulation, context)
        for start, end, href, title, ext in sorted(edits, reverse=True):
            label = line[start:end]
            cls = "br18-ref br18-ref--ext" if ext else "br18-ref"
            if html:
                new = f'<a class="{cls}" href="{href}" title="{title}">{label}</a>'
            else:
                new = f'[{label}]({href} "{title}"){{ .{cls.replace(" ", " .")} }}'
            line = line[:start] + new + line[end:]
        return line

    def scoped_doc(self, line: str, m: re.Match[str]) -> str | None:
        prefix, postfix = clean(line[: m.start()]), clean(line[m.end() :])
        if GUIDE_TITLE_BEFORE_RE.search(prefix):
            return OTHER
        if BR18_BEFORE_RE.search(prefix) or BR18_AFTER_RE.match(postfix):
            return BR18
        g = GENITIVE_RE.search(prefix)
        if (g and g.group(1).lower() not in NOT_GENITIVE) or self.laws.before(prefix) or INSTRUMENT_BEFORE_RE.search(prefix):
            return OTHER
        if OTHER_DOC_AFTER_RE.match(postfix) or INSTRUMENT_AFTER_RE.match(postfix):
            return OTHER
        return None

    def chapter(self, rel, line, masked, m, edits, own_ids, regulation, context) -> None:
        scope = self.scoped_doc(line, m)
        number = int(m.group(2))
        if scope == OTHER or number not in self.corpus.chapters:
            return
        rng = RANGE_TAIL_RE.match(masked, m.end())
        if rng:
            items = [(m.start(), rng.end(), number, f"BR18 kapitel {number}-{rng.group(1)}")]
            valid = number < int(rng.group(1)) and int(rng.group(1)) in self.corpus.chapters
        else:
            more = followers(masked, m.end())
            items = [(m.start(), m.end(), number, f"BR18 kapitel {number}")]
            items += [(f.start(1), f.end(1), f.group(1), f"BR18 kapitel {f.group(1)}") for f in more]
            valid = all(str(n).isdigit() and int(n) in self.corpus.chapters for *_, n, _ in items)
        if not valid:
            self.note(rel, line[m.start() : items[-1][1]], "chapter list or range with a number that is not a BR18 chapter", context(m.start(), m.end()))
            return
        named = CHAPTER_TOPIC_RE.match(line, m.end())
        confirmed = len(items) == 1 and not rng and named and named.group(1).lower() == self.corpus.chapters[number][3]
        if scope != BR18 and not regulation and not confirmed:
            self.note(rel, line[m.start() : items[-1][1]], "guide page: may be the guide's own chapter", context(m.start(), m.end()))
            return
        for start, end, n, title in items:
            edits.append((start, end, self.href(rel, Target(self.corpus.chapters[int(n)][0]), own_ids), title, False))

    def annex(self, rel, line, masked, m, edits, own_ids, regulation, context) -> None:
        number, table = int(m.group(1)), (m.group(2) or "")
        scope = self.scoped_doc(line, m)
        if scope == OTHER or (number, "") not in self.corpus.tables:
            return
        if RANGE_TAIL_RE.match(masked, m.end()) or re.match(rf"{S}*[-–]{S}*\d", masked[m.end() :]):
            self.note(rel, m.group(0), "annex or table range", context(m.start(), m.end()))
            return
        more = followers(masked, m.end())
        keys = [(number, table)] + [((number, f.group(1)) if table else (int(f.group(1)) if f.group(1).isdigit() else 0, "")) for f in more]
        spans = [(m.start(), m.end())] + [(f.start(1), f.end(1)) for f in more]
        text = line[m.start() : spans[-1][1]]
        if scope != BR18 and not regulation:
            self.note(rel, text, "guide page: may be the guide's own annex", context(m.start(), m.end()))
            return
        missing = [k for k in keys if k not in self.corpus.tables]
        if missing:
            self.note(rel, text, f"no BR18 bilag {missing[0][0]}" + (f" tabel {missing[0][1]}" if missing[0][1] else ""), context(m.start(), m.end()))
            return
        for (start, end), key in zip(spans, keys):
            title = f"BR18 bilag {key[0]}" + (f", tabel {key[1]}" if key[1] else "")
            edits.append((start, end, self.href(rel, self.corpus.tables[key], own_ids), title, False))

    def link_page(self, rel: str, markdown: str) -> str:
        lines = markdown.split("\n")
        own_ids = set(re.findall(r"\{#([^}\s]+)", markdown))
        regulation = bool(REGULATION_PAGE_RE.match(rel))
        in_front = bool(lines) and lines[0] == "---"
        in_fence = False
        html_tag, html_depth = None, 0
        in_anchor = False
        for i, line in enumerate(lines):
            if in_front:
                in_front = not (i > 0 and line == "---")
                continue
            if FENCE_RE.match(line):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            if html_tag is None:
                block = BLOCK_TAG_RE.match(line)
                if block:
                    html_tag, html_depth = block.group(1).lower(), 0
            if html_tag is not None:
                html_depth += len(re.findall(rf"<{html_tag}\b", line, re.I)) - len(re.findall(rf"</{html_tag}>", line, re.I))
                if not line.strip() and html_depth <= 0:
                    html_tag = None
                    continue
            nxt = lines[i + 1] if i + 1 < len(lines) else ""
            if SKIP_LINE_RE.match(line) or (line.strip() and re.match(r"^\s{0,3}(=+|-+)\s*$", nxt) and html_tag is None):
                continue
            masked, in_anchor = protected_mask(line, in_anchor)
            if "§" in masked or "apitel" in masked or "ap." in masked or "ilag" in masked:
                lines[i] = self.link_line(rel, line, masked, html_tag is not None, own_ids, regulation)
        return "\n".join(lines)

    def mark_applied(self, rel: str, markdown: str) -> None:
        for i, entry in enumerate(self.overrides):
            text = re.escape(entry["text"])
            if entry["page"] == rel and re.search(rf'\[{text}\]\([^)]*\)\{{ \.br18-ref|class="br18-ref[^"]*"[^>]*>{text}</a>', markdown):
                self.used_overrides.add(i)

    def stale_overrides(self) -> list[dict]:
        return [o for i, o in enumerate(self.overrides) if i not in self.used_overrides]


def report_rows(unresolved: dict[tuple[str, str, str], list[str]]) -> list[str]:
    rows = []
    for (text, reason, context), pages in unresolved.items():
        rows.append("\t".join([sorted(pages)[0], text, reason, str(len(pages)), context]))
    return sorted(set(rows))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--docs-root", type=Path, default=REPO / "docs")
    parser.add_argument("--data-dir", type=Path, default=REPO, help="directory with the xref-*.toml files and xref-unresolved.tsv")
    args = parser.parse_args()
    docs = args.docs_root.resolve()
    linker = Linker(docs, args.data_dir)
    changed = {}
    for path in sorted(docs.rglob("*.md")):
        rel = path.relative_to(docs).as_posix()
        if rel.startswith(("assets/", "stylesheets/", "media/")):
            continue
        markdown = path.read_text(encoding="utf-8")
        new = linker.link_page(rel, markdown)
        linker.mark_applied(rel, new)
        if new != markdown:
            changed[path] = new
    stale = linker.stale_overrides()
    if stale:
        for o in stale:
            print(f"stale override (no such reference on the page): {o.get('page')}: {o.get('text')}", file=sys.stderr)
        return 1
    report = args.data_dir / "xref-unresolved.tsv"
    header = "page\treference\treason\tpages\tcontext"
    rows = report_rows(linker.unresolved)
    if report.exists():
        old = [r for r in report.read_text(encoding="utf-8").splitlines()[1:] if r]
        if len(rows) > len(old):
            for row in sorted(set(rows) - set(old)):
                print(f"new unresolved reference: {row}", file=sys.stderr)
            print(f"unresolved references would grow {len(old)} -> {len(rows)}; resolve them (override) or delete {report.name} to accept", file=sys.stderr)
            return 1
    for path, new in changed.items():
        path.write_text(new, encoding="utf-8")
    report.write_text("\n".join([header, *rows]) + "\n", encoding="utf-8")
    print(f"linked pages changed: {len(changed)}, unresolved references: {len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
