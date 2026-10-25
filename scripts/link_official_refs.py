#!/usr/bin/env python3

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DOCS_ROOT = ROOT / "docs"

SOURCE_URLS = {
    "byggeloven": "https://www.retsinformation.dk/eli/lta/2016/1178",
    "straffeloven": "https://www.retsinformation.dk/eli/lta/2024/1145",
    "planloven": "https://www.retsinformation.dk/eli/lta/2024/572",
    "naturbeskyttelsesloven": "https://www.retsinformation.dk/eli/lta/2024/927",
    "oversvømmelsesloven": "https://www.retsinformation.dk/eli/lta/2024/72",
    "udstykningsloven": "https://www.retsinformation.dk/eli/lta/2024/53",
    "ladestanderbekendtgørelsen": "https://www.retsinformation.dk/eli/lta/2020/181",
    "skorstensfejerbekendtgørelsen": "https://www.retsinformation.dk/Forms/R0710.aspx?id=191239",
    "drikkevandsbekendtgørelsen": "https://www.retsinformation.dk/eli/lta/2024/1633",
    "affaldsbekendtgørelsen": "https://www.retsinformation.dk/eli/lta/2024/1749",
    "bekendtgørelse om certificeringsordning for transportable konstruktioner": "https://www.retsinformation.dk/eli/lta/2019/673",
    "bekendtgørelse om certificeringsordninger for dokumentation af tekniske forhold i bygningsreglementet": "https://www.retsinformation.dk/eli/lta/2019/674",
    "bekendtgørelse om forberedelse til og etablering af ladestandere i forbindelse med bygninger": "https://www.retsinformation.dk/eli/lta/2020/181",
}

SHORTHAND_URLS = {
    "byggeloven": SOURCE_URLS["byggeloven"],
    "byggelovens": SOURCE_URLS["byggeloven"],
    "straffeloven": SOURCE_URLS["straffeloven"],
    "straffelovens": SOURCE_URLS["straffeloven"],
    "planloven": SOURCE_URLS["planloven"],
    "planlovens": SOURCE_URLS["planloven"],
    "naturbeskyttelsesloven": SOURCE_URLS["naturbeskyttelsesloven"],
    "naturbeskyttelseslovens": SOURCE_URLS["naturbeskyttelsesloven"],
    "oversvømmelsesloven": SOURCE_URLS["oversvømmelsesloven"],
    "oversvømmelseslovens": SOURCE_URLS["oversvømmelsesloven"],
    "udstykningsloven": SOURCE_URLS["udstykningsloven"],
    "udstykningslovens": SOURCE_URLS["udstykningsloven"],
    "ladestanderbekendtgørelsen": SOURCE_URLS["ladestanderbekendtgørelsen"],
    "skorstensfejerbekendtgørelsen": SOURCE_URLS["skorstensfejerbekendtgørelsen"],
    "drikkevandsbekendtgørelsen": SOURCE_URLS["drikkevandsbekendtgørelsen"],
    "affaldsbekendtgørelsen": SOURCE_URLS["affaldsbekendtgørelsen"],
    "certificeringsbekendtgørelsen": SOURCE_URLS[
        "bekendtgørelse om certificeringsordninger for dokumentation af tekniske forhold i bygningsreglementet"
    ],
}

MARKDOWN_PROTECT_RE = re.compile(
    r"!\[[^\]\n]*]\([^\)\n]*\)(?:\{[^}\n]*\})?"
    r"|\[[^\]\n]+]\([^\)\n]*\)(?:\{[^}\n]*\})?"
    r"|<[^>]+>",
)
HEADING_PROTECT_RE = re.compile(r"^(#{1,6}\s[^\n]*)$", re.MULTILINE)

DUPLICATE_LINK_RE = re.compile(r"\[\[([^\]]+)\]\((https?://[^)]+)\)\]\(\2\)")
POSSESSIVE_NESTED_LINK_RE = re.compile(
    r"\[\[\[([^\]]+)\]\((https?://[^)]+)\)\]\(\2\)s ([^\]]+)\]\(\2\)"
)
OUTER_WITH_LOCAL_RE = re.compile(
    r"\[\[([^\]]+)\]\((https?://[^)]+)\)\s+\[([^\]]+)\]\(([^)]+)\)\]\(\2\)"
)
OUTER_POSSESSIVE_WITH_LOCAL_RE = re.compile(
    r"\[\[([^\]]+)\]\((https?://[^)]+)\)s\s+\[([^\]]+)\]\(([^)]+)\)\]\(\2\)"
)
OUTER_WITH_TEXT_RE = re.compile(r"\[\[([^\]]+)\]\((https?://[^)]+)\)\s+([^\]]+)\]\(\2\)")
DOUBLE_SECTION_SIGN_RE = re.compile(r"§\[(§[^\]]+)\]\(([^)]+)\)")
LINKED_RANGE_RE = re.compile(
    r"\[\[([^\]]+)\]\(([^)]+)\)\s*-\s*\[([^\]]+)\]\(([^)]+)\)\](\{[^}]*\})?"
)
PARTIAL_LINKED_RANGE_RE = re.compile(
    r"\[(§§)\s*([0-9]+(?:\s*[A-Za-z])?)\]\(([^)]+)\)\s*(?:-|--|–|—)\s*§?\s*([0-9]+(?:\s*[A-Za-z])?)"
)
BROKEN_OG_LINK_RE = re.compile(r"\[(§{1,2}\s*[^\]]*?)\s+o\]\(([^)]+)\)g\b")
PARTIAL_ANNEX_NUMBER_RE = re.compile(
    r"\[((?:BR18,\s*)?[Bb]ilag\s+([1-9]))\]\((/bilag/b\2(?:/bilag_\2/)?/?)\)(\d+)"
)

SECTION_REF = (
    r"(?:"
    r"§{1,2}\s*[\dA-Za-z]+(?:\s*[A-Za-z])?"
    r"(?:\s*-\s*§?\s*[\dA-Za-z]+(?:\s*[A-Za-z])?)?"
    r"(?:,\s*stk\.\s*\d+)?"
    r"(?:,\s*nr\.\s*\d+)?"
    r"(?:,\s*litra\s*[A-Za-z])?"
    r"|"
    r"\d+\.\s*kapitel"
    r")"
)
SECTION_SINGLE_RE = re.compile(
    r"§{1,2}\s*([0-9]+(?:\s*[A-Za-z])?)(?:,\s*stk\.\s*\d+)?(?:,\s*nr\.\s*\d+)?(?:,\s*litra\s*[A-Za-z])?",
    re.IGNORECASE,
)
SECTION_RANGE_RE = re.compile(
    r"§§\s*([0-9]+(?:\s*[A-Za-z])?)\s*(?:-|--|–|—)\s*§?\s*([0-9]+(?:\s*[A-Za-z])?)",
    re.IGNORECASE,
)
SECTION_LIST_RE = re.compile(
    r"§§\s*([0-9]+(?:\s*[A-Za-z])?(?:\s*(?:,|og)\s*§?\s*[0-9]+(?:\s*[A-Za-z])?)+)",
    re.IGNORECASE,
)
SECTION_AT_LINE_START_RE = re.compile(r"^\s*§\s*(\d+(?:\s*[A-Za-z])?)\b", re.IGNORECASE)
CHAPTER_RE = re.compile(r"\b(kapitel|kap\.)\s+([0-9]{1,2})(?![0-9_])", re.IGNORECASE)
CHAPTER_LIST_RE = re.compile(
    r"\b(kapitel|kap\.)\s+([0-9]{1,2}(?:\s*(?:,|og)\s*[0-9]{1,2})+)",
    re.IGNORECASE,
)
ANNEX_RE = re.compile(
    r"\b(?:BR18,\s*)?[Bb]ilag\s+([1-9])(?!\d)(?:,\s*tabel\s+\d+(?:\.\d+)?)?",
    re.IGNORECASE,
)
PLACEHOLDER_RE = re.compile(r"(@@PROTECTED_\d+@@)")


def protect_with_regex(
    text: str, placeholders: dict[str, str], regex: re.Pattern[str]
) -> str:
    def repl(match: re.Match[str]) -> str:
        key = f"@@PROTECTED_{len(placeholders)}@@"
        placeholders[key] = match.group(0)
        return key

    return regex.sub(repl, text)


def protect_frontmatter(text: str, placeholders: dict[str, str]) -> str:
    if not text.startswith("---\n"):
        return text

    end = text.find("\n---\n", 4)
    if end == -1:
        return text

    key = f"@@PROTECTED_{len(placeholders)}@@"
    placeholders[key] = text[: end + 5]
    return key + text[end + 5 :]


def protect_spans(text: str) -> tuple[str, dict[str, str]]:
    placeholders: dict[str, str] = {}
    text = protect_frontmatter(text, placeholders)
    text = protect_with_regex(text, placeholders, MARKDOWN_PROTECT_RE)
    text = protect_with_regex(text, placeholders, HEADING_PROTECT_RE)
    return text, placeholders


def restore_spans(text: str, placeholders: dict[str, str]) -> str:
    # Later spans (headings) can contain earlier keys (links), so restore newest first.
    for key, value in reversed(placeholders.items()):
        text = text.replace(key, value)
    return text


def normalize_broken_links(text: str) -> str:
    previous = None
    while text != previous:
        previous = text
        text = POSSESSIVE_NESTED_LINK_RE.sub(r"[\1s \3](\2)", text)
        text = DUPLICATE_LINK_RE.sub(r"[\1](\2)", text)
        text = OUTER_POSSESSIVE_WITH_LOCAL_RE.sub(r"[\1s \3](\2)", text)
        text = OUTER_WITH_LOCAL_RE.sub(r"[\1 \3](\2)", text)
        text = OUTER_WITH_TEXT_RE.sub(r"[\1 \3](\2)", text)
        text = DOUBLE_SECTION_SIGN_RE.sub(r"[\1](\2)", text)
        text = PARTIAL_LINKED_RANGE_RE.sub(r"[\1 \2-\4](\3)", text)
        text = BROKEN_OG_LINK_RE.sub(r"[\1](\2) og", text)
        text = PARTIAL_ANNEX_NUMBER_RE.sub(r"\1\4", text)
        text = LINKED_RANGE_RE.sub(
            lambda match: (
                f"[{match.group(1)} - {match.group(3)}]({match.group(2)}){match.group(5) or ''}"
                if match.group(2) == match.group(4)
                else match.group(0)
            ),
            text,
        )
    return text


def build_patterns() -> list[tuple[re.Pattern[str], str]]:
    patterns: list[tuple[re.Pattern[str], str]] = []

    for term, url in SHORTHAND_URLS.items():
        patterns.append(
            (
                re.compile(
                    rf"\b{re.escape(term)}\s+{SECTION_REF}",
                    re.IGNORECASE,
                ),
                url,
            )
        )

    for term, url in sorted(SOURCE_URLS.items(), key=lambda item: len(item[0]), reverse=True):
        patterns.append((re.compile(re.escape(term), re.IGNORECASE), url))

    for term, url in sorted(SHORTHAND_URLS.items(), key=lambda item: len(item[0]), reverse=True):
        patterns.append((re.compile(rf"\b{re.escape(term)}\b", re.IGNORECASE), url))

    return patterns


PATTERNS = build_patterns()


def wrap_text(text: str, url: str) -> str:
    return f"[{text}]({url})"


def normalize_ref_token(token: str) -> str:
    return re.sub(r"\s+", "", token.strip().lower().replace("–", "-").replace("—", "-"))


def expand_alpha_range(start: str, end: str) -> list[str]:
    start_num = re.match(r"(\d+)([a-z])", start)
    end_num = re.match(r"(\d+)([a-z])", end)
    if not start_num or not end_num or start_num.group(1) != end_num.group(1):
        return [start, end]
    prefix = start_num.group(1)
    letters = range(ord(start_num.group(2)), ord(end_num.group(2)) + 1)
    return [f"{prefix}{chr(letter)}" for letter in letters]


def expand_section_range(start: str, end: str) -> list[str]:
    start = normalize_ref_token(start)
    end = normalize_ref_token(end)

    if start.isdigit() and end.isdigit():
        a = int(start)
        b = int(end)
        if a <= b:
            return [str(i) for i in range(a, b + 1)]
        return [start, end]

    if re.fullmatch(r"\d+[a-z]", start) and re.fullmatch(r"\d+[a-z]", end):
        return expand_alpha_range(start, end)

    if start.isdigit() and re.fullmatch(r"\d+[a-z]", end):
        prefix = re.match(r"(\d+)([a-z])", end)
        if prefix and prefix.group(1) == start:
            letters = range(ord("a"), ord(prefix.group(2)) + 1)
            return [start] + [f"{start}{chr(letter)}" for letter in letters]

    return [start, end]


def page_to_site_path(path: Path) -> str:
    rel = path.relative_to(DOCS_ROOT)
    rel_parts = rel.parts[:-1]
    return "/" + "/".join(rel_parts) + "/"


def build_section_targets() -> tuple[dict[str, str], dict[str, str], dict[str, str]]:
    single: dict[str, str] = {}
    ranges: dict[str, str] = {}
    chapters: dict[str, str] = {}

    for path in sorted(DOCS_ROOT.rglob("*.md")):
        if "krav" not in path.parts:
            continue
        site_path = page_to_site_path(path)
        stem = path.parent.name

        if stem != "krav":
            key = normalize_ref_token(stem.replace("_", "-"))
            ranges[key] = site_path

            if "_" in stem:
                start, end = stem.split("_", 1)
                for item in expand_section_range(start, end):
                    single[normalize_ref_token(item)] = site_path
            elif "-" in stem and not re.fullmatch(r"\d+-\d+", stem):
                start, end = stem.split("-", 1)
                for item in expand_section_range(start, end):
                    single[normalize_ref_token(item)] = site_path
            else:
                single[normalize_ref_token(stem)] = site_path

        text = path.read_text(encoding="utf-8")
        for line in text.splitlines():
            match = SECTION_AT_LINE_START_RE.match(line)
            if not match:
                continue
            single[normalize_ref_token(match.group(1))] = site_path

    for base in ["tekniske-bestemmelser", "ovrige-bestemmelser"]:
        base_path = DOCS_ROOT / base
        if not base_path.exists():
            continue
        for path in sorted(base_path.glob("*/index.md")):
            chapter = path.parent.name.lstrip("0")
            if chapter.isdigit():
                chapters[chapter] = page_to_site_path(path)

    admin_index = DOCS_ROOT / "administrative-bestemmelser" / "index.md"
    if admin_index.exists():
        chapters["1"] = page_to_site_path(admin_index)

    penalties_root = DOCS_ROOT / "straf-og-ikrafttraedelse"
    if penalties_root.exists():
        for path in sorted(penalties_root.glob("*/index.md")):
            chapter = path.parent.name
            if chapter.isdigit():
                chapters[chapter] = page_to_site_path(path)

    return single, ranges, chapters


SECTION_TARGETS, RANGE_TARGETS, CHAPTER_TARGETS = build_section_targets()


def build_annex_targets() -> dict[str, str]:
    annexes: dict[str, str] = {}
    bilag_root = DOCS_ROOT / "bilag"
    if not bilag_root.exists():
        return annexes

    for path in sorted(bilag_root.glob("b*/index.md")):
        stem = path.parent.name
        number = stem.removeprefix("b")
        if number.isdigit():
            annexes[number] = page_to_site_path(path)

    for path in sorted(bilag_root.glob("b*/bilag_*/index.md")):
        match = re.search(r"bilag_(\d+)", path.parent.name)
        if match:
            annexes[match.group(1)] = page_to_site_path(path)

    return annexes


ANNEX_TARGETS = build_annex_targets()


def split_protected(text: str) -> list[str]:
    return PLACEHOLDER_RE.split(text)


def apply_patterns(text: str, patterns: list[tuple[re.Pattern[str], str]]) -> tuple[str, int]:
    total = 0

    for pattern, url in patterns:
        def repl(match: re.Match[str]) -> str:
            nonlocal total
            total += 1
            return wrap_text(match.group(0), url)

        text = pattern.sub(repl, text)

    return text, total


def link_ranges(text: str) -> tuple[str, int]:
    total = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal total
        start = normalize_ref_token(match.group(1))
        end = normalize_ref_token(match.group(2))
        range_key = f"{start}-{end}"
        url = RANGE_TARGETS.get(range_key)
        if not url:
            expanded = expand_section_range(start, end)
            targets = {SECTION_TARGETS.get(item) for item in expanded}
            targets.discard(None)
            if len(targets) == 1:
                url = next(iter(targets))
        if not url:
            return match.group(0)
        total += 1
        return wrap_text(match.group(0), url)

    return SECTION_RANGE_RE.sub(repl, text), total


def link_sections(text: str) -> tuple[str, int]:
    total = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal total
        key_match = re.search(r"\d+(?:\s*[A-Za-z])?", match.group(0))
        if not key_match:
            return match.group(0)
        key = normalize_ref_token(key_match.group(0))
        url = SECTION_TARGETS.get(key)
        if not url:
            return match.group(0)
        total += 1
        return wrap_text(match.group(0), url)

    return SECTION_SINGLE_RE.sub(repl, text), total


def link_section_lists(text: str) -> tuple[str, int]:
    total = 0
    token_re = re.compile(r"\d+(?:\s*[A-Za-z])?", re.IGNORECASE)

    def repl(match: re.Match[str]) -> str:
        nonlocal total
        body = match.group(1)
        pieces: list[str] = []
        last = 0
        local_count = 0

        for token_match in token_re.finditer(body):
            pieces.append(body[last : token_match.start()])
            token = token_match.group(0)
            url = SECTION_TARGETS.get(normalize_ref_token(token))
            if url:
                pieces.append(wrap_text(f"§ {token.strip()}", url))
                local_count += 1
            else:
                pieces.append(token)
            last = token_match.end()

        if local_count == 0:
            return match.group(0)

        pieces.append(body[last:])
        total += local_count
        return "".join(pieces)

    return SECTION_LIST_RE.sub(repl, text), total


def link_chapters(text: str) -> tuple[str, int]:
    total = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal total
        chapter = str(int(match.group(2)))
        url = CHAPTER_TARGETS.get(chapter)
        if not url:
            return match.group(0)
        total += 1
        return wrap_text(match.group(0), url)

    return CHAPTER_RE.sub(repl, text), total


def link_chapter_lists(text: str) -> tuple[str, int]:
    total = 0
    token_re = re.compile(r"\d{1,2}")

    def repl(match: re.Match[str]) -> str:
        nonlocal total
        prefix = match.group(1)
        body = match.group(2)
        pieces: list[str] = []
        last = 0
        local_count = 0
        first = True

        for token_match in token_re.finditer(body):
            pieces.append(body[last : token_match.start()])
            chapter = str(int(token_match.group(0)))
            url = CHAPTER_TARGETS.get(chapter)
            label = f"{prefix} {chapter}" if first else chapter
            if url:
                pieces.append(wrap_text(label, url))
                local_count += 1
            else:
                pieces.append(label)
            first = False
            last = token_match.end()

        if local_count == 0:
            return match.group(0)

        pieces.append(body[last:])
        total += local_count
        return "".join(pieces)

    return CHAPTER_LIST_RE.sub(repl, text), total


def link_annexes(text: str) -> tuple[str, int]:
    total = 0

    def repl(match: re.Match[str]) -> str:
        nonlocal total
        url = ANNEX_TARGETS.get(match.group(1))
        if not url:
            return match.group(0)
        total += 1
        return wrap_text(match.group(0), url)

    return ANNEX_RE.sub(repl, text), total


def relink_phase(
    text: str, linker
) -> tuple[str, int]:
    protected, placeholders = protect_spans(text)
    linked, replacements = linker(protected)
    return restore_spans(linked, placeholders), replacements


def link_external_refs(text: str) -> tuple[str, int]:
    protected, placeholders = protect_spans(text)
    linked, replacements = apply_patterns(protected, PATTERNS)
    return restore_spans(linked, placeholders), replacements


def link_local_refs(text: str) -> tuple[str, int]:
    total = 0

    text, count = relink_phase(text, link_ranges)
    total += count
    text, count = relink_phase(text, link_section_lists)
    total += count
    text, count = relink_phase(text, link_sections)
    total += count
    text, count = relink_phase(text, link_chapter_lists)
    total += count
    text, count = relink_phase(text, link_chapters)
    total += count
    text, count = relink_phase(text, link_annexes)
    total += count

    return text, total


def linkify(text: str) -> tuple[str, int]:
    normalized = normalize_broken_links(text)
    updated, total = link_external_refs(normalized)
    updated, local_total = link_local_refs(updated)
    return updated, total + local_total


def main() -> int:
    changed_files = 0
    total_replacements = 0

    for path in sorted(DOCS_ROOT.rglob("*.md")):
        original = path.read_text(encoding="utf-8")
        updated, replacements = linkify(original)
        if updated == original:
            continue
        path.write_text(updated, encoding="utf-8")
        changed_files += 1
        total_replacements += replacements
        print(f"{path.relative_to(ROOT)}: {replacements}")

    print(f"changed_files={changed_files}")
    print(f"total_replacements={total_replacements}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
