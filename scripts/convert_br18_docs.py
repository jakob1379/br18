#!/usr/bin/env python3

from __future__ import annotations

import argparse
import concurrent.futures as futures
import html
import os
import posixpath
import subprocess
import sys
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qsl, urlsplit, urlunsplit


SITE_HOSTS = {"www.bygningsreglementet.dk", "bygningsreglementet.dk"}
QUERY_ALIAS_RE = re.compile(r"__q_[0-9a-f]+(?=\.[^.]+$)")
TABLE_BLOCK_RE = re.compile(r"^<table\b[^>]*>$.*?^</table>$|^\|[^\n]*(?:\n\|[^\n]*)*", re.MULTILINE | re.DOTALL)
TABLE_TOKEN_RE = re.compile(r"BR18TABLE(\d+)")

DROP_TAGS = {
    "footer",
    "header",
    "noscript",
    "script",
    "style",
    "svg",
    "path",
    "circle",
    "g",
    "defs",
    "symbol",
    "use",
}

DROP_CLASSES = (
    "accordion__actions",
    "anchor-reference__tooltip",
    "anchor-reference__trigger",
    "bg-imagehandler",
    "button--unstyled",
    "cookie",
    "footer__address",
    "loading",
    "monsido",
    "nav-alphabet",
    "nav-tab",
    "page-fullwidth",
    "scroll-to-top",
    "section-module__actions",
    "search-field",
    "search-modal",
    "skip-links",
    "sitenav",
    "square__icon",
    "square__icon--wrapper",
    "version-selector",
    "warningbanner",
)

DROP_IDS = {
    "CookieConsent",
}

VOID_TAGS = {
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr",
}

FLATTEN_TAGS = {
    "aside",
    "div",
    "main",
    "nav",
    "section",
    "span",
}

# Inline markup that markdown writes with delimiters, which cannot open or close next to whitespace.
EMPHASIS_TAGS = {"b", "em", "i", "strong", "sub", "sup"}
EMPHASIS_KIND = {"b": "strong", "strong": "strong", "em": "em", "i": "em", "sub": "sub", "sup": "sup"}
EMPHASIS_OPEN_RE = re.compile(r"^<(?:b|em|i|strong|sub|sup)\b[^>]*>$")

BLOCK_FLATTEN_TAGS = {
    "aside",
    "div",
    "main",
    "nav",
    "section",
}


def should_drop(tag: str, attrs: dict[str, str]) -> bool:
    if tag in DROP_TAGS:
        return True

    ident = attrs.get("id", "")
    if ident in DROP_IDS or any(
        token in ident for token in ("cookie", "monsido", "search-modal")
    ):
        return True

    classes = attrs.get("class", "")
    return any(token in classes for token in DROP_CLASSES)


def is_same_site_url(url: str) -> bool:
    parsed = urlsplit(url)
    return bool(parsed.netloc and parsed.netloc in SITE_HOSTS)


def canonicalize_asset_path(path: str, source_dir: Path, docs_root: Path) -> str:
    canonical = QUERY_ALIAS_RE.sub("", path)
    if canonical == path:
        return path

    candidate = (
        docs_root / canonical.lstrip("/")
        if canonical.startswith("/")
        else (source_dir / canonical).resolve()
    )
    return canonical if candidate.exists() else path


def rel_path_for_url(url: str, source_dir: Path, docs_root: Path) -> str | None:
    parsed = urlsplit(url)

    if parsed.scheme in {"mailto", "tel", "javascript", "data"}:
        return None

    if parsed.netloc and parsed.netloc not in SITE_HOSTS:
        return None

    if parsed.path.lower().startswith("/historisk/"):
        # Historisk content is out of scope, so it stays on the origin.
        return urlunsplit(("https", "www.bygningsreglementet.dk", parsed.path, parsed.query, ""))

    path = canonicalize_asset_path(parsed.path or ("/" if parsed.netloc else ""), source_dir, docs_root)
    if not path:
        return "" if parsed.fragment else None

    if path.startswith("/"):
        local_target = docs_root / path.lstrip("/")
    else:
        local_target = (source_dir / path).resolve()
        if not local_target.is_relative_to(docs_root):
            return None

    query = dict(parse_qsl(parsed.query, keep_blank_values=True))
    show_all = query == {"Layout": "ShowAll"}

    if show_all:
        target = local_target / "showall"
        rel = os.path.relpath(target, source_dir)
        return rel if rel != "." else "./"

    # Origin pages are directories (`/x/vejledning` serves `/x/vejledning/`); only files have a suffix.
    if path.endswith("/") or not local_target.suffix:
        rel = os.path.relpath(local_target, source_dir)
        return "./" if rel == "." else f"{rel}/"

    suffix = local_target.suffix.lower()
    if suffix in {".html", ".htm", ".xhtml"}:
        target = local_target.with_suffix(".md")
    else:
        target = local_target

    rel = os.path.relpath(target, source_dir)
    return rel


class Cleaner(HTMLParser):
    def __init__(self, source_dir: Path, docs_root: Path) -> None:
        super().__init__(convert_charrefs=True)
        self.source_dir = source_dir
        self.docs_root = docs_root
        self.parts: list[str] = []
        self.skip_depth = 0
        self.stack: list[str] = []
        self.emphasis: list[str] = []  # open emitted emphasis tags

    def _before_emphasis_opens(self) -> int:
        """Index before the emphasis tags just opened, where leading whitespace and breaks belong."""
        index = len(self.parts)
        while index and EMPHASIS_OPEN_RE.match(self.parts[index - 1]):
            index -= 1
        return index

    def _attrs(self, attrs: list[tuple[str, str | None]]) -> dict[str, str]:
        return {name: value or "" for name, value in attrs}

    def _render_attrs(self, attrs: list[tuple[str, str | None]]) -> str:
        rendered = []
        for name, value in attrs:
            if value is None:
                rendered.append(name)
            else:
                rendered.append(f'{name}="{html.escape(value, quote=True)}"')
        return (" " + " ".join(rendered)) if rendered else ""

    def _rewrite_attrs(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> list[tuple[str, str | None]]:
        rewritten: list[tuple[str, str | None]] = []
        for name, value in attrs:
            if (
                name in {"class", "id", "style", "role", "tabindex"}
                or name.startswith("data-")
                or name.startswith("aria-")
            ):
                continue

            if value is None:
                rewritten.append((name, value))
                continue

            if name in {"href", "src", "data-href", "action", "poster"}:
                rel = rel_path_for_url(value, self.source_dir, self.docs_root)
                if rel is not None:
                    fragment = urlsplit(value).fragment
                    if fragment:
                        rel = f"{rel}#{fragment}"
                    value = rel

            rewritten.append((name, value))
        return rewritten

    def _should_skip(self, tag: str, attrs: list[tuple[str, str | None]]) -> bool:
        return should_drop(tag, self._attrs(attrs))

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in VOID_TAGS:
            if self.skip_depth > 0 or self._should_skip(tag, attrs):
                return
            attrs = self._rewrite_attrs(tag, attrs)
            if tag == "br" and self.emphasis:
                # The converter turns line breaks into paragraph breaks, which emphasis cannot span.
                for open_tag in reversed(self.emphasis):
                    self._close(open_tag)
                self.parts.append("<br />")
                self.parts.extend(f"<{open_tag}>" for open_tag in self.emphasis)
                return
            self.parts.append(f"<{tag}{self._render_attrs(attrs)} />")
            return

        if self.skip_depth > 0 or self._should_skip(tag, attrs):
            self.stack.append("skip")
            self.skip_depth += 1
            return

        # Markdown cannot nest emphasis of one kind (`**a **b****`), and the inner one adds nothing visible.
        nested = tag in EMPHASIS_TAGS and EMPHASIS_KIND[tag] in {EMPHASIS_KIND[t] for t in self.emphasis}
        if nested or tag in FLATTEN_TAGS or (tag == "a" and "href" not in self._attrs(attrs)):
            self.stack.append("flatten")
            if tag in BLOCK_FLATTEN_TAGS:
                self.parts.append("\n\n")
            return

        self.stack.append("emit")
        if tag in EMPHASIS_TAGS:
            self.emphasis.append(tag)
        trigger = tag == "a" and "accordion__trigger" in self._attrs(attrs).get("class", "")
        attrs = self._rewrite_attrs(tag, attrs)
        if trigger:
            attrs = [(n, v) for n, v in attrs if n != "title"] + [("title", TRIGGER_TITLE)]
        self.parts.append(f"<{tag}{self._render_attrs(attrs)}>")

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if self.skip_depth > 0 or self._should_skip(tag, attrs):
            return
        if tag in FLATTEN_TAGS:
            return
        attrs = self._rewrite_attrs(tag, attrs)
        self.parts.append(f"<{tag}{self._render_attrs(attrs)} />")

    def handle_endtag(self, tag: str) -> None:
        if not self.stack:
            return
        state = self.stack.pop()
        if state == "skip":
            self.skip_depth -= 1
            return
        if state == "flatten":
            if tag in BLOCK_FLATTEN_TAGS:
                self.parts.append("\n\n")
            return
        if tag in EMPHASIS_TAGS and self.emphasis:
            self.emphasis.pop()
        self._close(tag)

    def _close(self, tag: str) -> None:
        moved: list[str] = []
        if tag in EMPHASIS_TAGS:
            while self.parts and (self.parts[-1] == "<br />" or not self.parts[-1].strip(" \t\n ")):
                moved.insert(0, self.parts.pop())
            if self.parts and not self.parts[-1].startswith("<"):
                text = self.parts.pop()
                kept = text.rstrip(" \t\n ")
                self.parts.append(kept)
                moved.insert(0, text[len(kept):])
            opened = next((i for i in range(len(self.parts) - 1, -1, -1) if re.match(rf"<{tag}\b", self.parts[i])), None)
            if opened is not None and not re.sub(r"<[^>]*>", "", "".join(self.parts[opened + 1 :])).strip(" \t\n\u00a0"):
                # Emphasis around nothing visible renders as literal `* *`.
                del self.parts[opened]
                self.parts.extend(moved)
                return
        self.parts.append(f"</{tag}>")
        self.parts.extend(moved)

    def handle_data(self, data: str) -> None:
        if (
            self.skip_depth == 0
            and data.strip() != "Swipe horisontalt for at se alle emner"
        ):
            lead = data[: len(data) - len(data.lstrip(" \t\n "))]
            if lead and self.parts and EMPHASIS_OPEN_RE.match(self.parts[-1]):
                self.parts.insert(self._before_emphasis_opens(), lead)
                data = data[len(lead):]
            self.parts.append(data)

    def handle_entityref(self, name: str) -> None:
        if self.skip_depth == 0:
            self.parts.append(f"&{name};")

    def handle_charref(self, name: str) -> None:
        if self.skip_depth == 0:
            self.parts.append(f"&#{name};")

    def handle_comment(self, data: str) -> None:
        return

    def clean(self, html_text: str) -> str:
        self.feed(html_text)
        self.close()
        return "".join(self.parts)


def output_path_for_html(path: Path) -> Path | None:
    name = path.name
    if "?" not in name:
        if path.suffix.lower() in {".html", ".htm", ".xhtml"}:
            return path.with_suffix(".md")
        if path.suffix == "":
            return path / "index.md"
        return None

    prefix, _, query_suffix = name.partition("?")
    if query_suffix != "Layout=ShowAll.html":
        return None

    if prefix == "index.html":
        return path.parent / "showall" / "index.md"

    stem = Path(prefix).stem if prefix.endswith(".html") else prefix
    if not stem:
        return None
    return path.parent / stem / "showall" / "index.md"


def fix_empty_english_version_links(markdown: str) -> str:
    pattern = re.compile(
        r"(?m)(\*English version[^*]*\*)\[\]\(([^)\s]+)(?: \"([^\"]+)\")?\)-"
    )

    def replace(match: re.Match[str]) -> str:
        prefix = match.group(1)
        url = match.group(2)
        title = match.group(3) or "English version"
        return f'{prefix}[{title}]({url} "{title}")'

    return pattern.sub(replace, markdown)


def normalize_media_alias_links(markdown: str) -> str:
    return re.sub(r"(/media/[^)\s\"']+)__q_[0-9a-f]+(\.[^)\\s\"']+)", r"\1\2", markdown)


def normalize_duplicate_uuid_fragments(markdown: str) -> str:
    uuid = r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
    return re.sub(rf"(#{uuid})#{uuid}", r"\1", markdown)


def normalize_markdown_linebreak_artifacts(markdown: str) -> str:
    """Turn source-site ``<br>`` artifacts into readable Markdown blocks.

    Pandoc represents many BR18 ``<br>`` tags as literal Markdown hard-break
    backslashes.  In the legal text this often produces visible ``\\`` lines or
    one very long paragraph containing multiple list items and ``Stk.`` clauses.
    The original site uses those breaks as paragraph/list layout, so normalize
    them to blank-line separated Markdown before heading promotion.
    """
    normalized_lines: list[str] = []
    for raw in markdown.splitlines():
        stripped = raw.strip()
        if stripped == "\\":
            if normalized_lines and normalized_lines[-1] != "":
                normalized_lines.append("")
            continue
        if raw.endswith("\\") and not raw.lstrip().startswith("|"):
            raw = raw[:-1].rstrip()
            normalized_lines.append(raw)
            if normalized_lines[-1] != "":
                normalized_lines.append("")
            continue
        normalized_lines.append(raw)

    text = "\n".join(normalized_lines)

    # Normalize legal subsection labels so Markdown emphasis parses despite
    # non-breaking spaces and inconsistent source punctuation.
    text = re.sub(
        r"\*\s*\u00a0?(Stk\.\s*\d+[a-z]?)\.?\s*\*\.?+(?=\S)",
        r"*\1.* ",
        text,
    )
    text = re.sub(
        r"\*\s*\u00a0?(Stk\.\s*\d+[a-z]?)\.?\s*\*\.?(?=\s|$)",
        r"*\1.*",
        text,
    )

    # Split inline legal subsection clauses: "...  *Stk. 2.* ...".
    text = re.sub(
        r"(?<!^)\s+(?=\*Stk\.\s*\d+[a-z]?\.\*)",
        "\n\n",
        text,
    )

    # Split numbered and lettered legal list items that were flattened into one
    # paragraph. Require whitespace before the marker to avoid touching words,
    # section references, or URLs.
    text = re.sub(r"(?<!^)(?<!\\)\s+(?=\d{1,2}\)\s*\S)", "\n\n", text)
    text = re.sub(r"(?<!^)(?<!\\)\s+(?=[a-zæøå]\)\s*\S)", "\n\n", text)

    # An emphasised "- item" line (the origin's typed dash list) becomes a list item like the unemphasised ones.
    text = re.sub(r"(?m)^(\*{1,3})- (?=\S)", r"- \1", text)

    text = re.sub(r"\n{3,}", "\n\n", text)
    return text + ("\n" if markdown.endswith("\n") else "")


def escape_unresolved_reference_labels(markdown: str) -> str:
    return re.sub(
        r"(?<![!\\])\[([^\]\n]+)\](?![\[(])",
        lambda match: rf"\[{match.group(1)}\]",
        markdown,
    )

LEGAL_PARAGRAPH = r"§\s*\d+(?:\s*[a-zæøå](?![a-zæøå]))?"
LEGAL_PARAGRAPH_RE = re.compile(rf"^(?P<label>{LEGAL_PARAGRAPH})(?P<rest>.*)$", re.IGNORECASE)
LINKED_LEGAL_PARAGRAPH_RE = re.compile(
    rf"^\[(?P<label>{LEGAL_PARAGRAPH})\]\([^)]*\)(?P<rest>.*)$",
    re.IGNORECASE,
)
LEGAL_SECTION_LINK_RE = re.compile(r"^\[(?P<label>§[^\]]+)\]\([^)]*\)\s*$")
HEADING_LINE_RE = re.compile(r"^(?P<marks>#{1,6})\s+(?P<title>.*?)(?:\s+\{(?P<attrs>[^}]*)\})?\s*$")
INLINE_LEGAL_SPLIT_RE = re.compile(rf"(?<![§\w/])(?={LEGAL_PARAGRAPH}\s+[A-ZÆØÅ])")
TRAILING_LEGAL_MARKER_RE = re.compile(rf"^(?P<prefix>.+?)(?P<label>{LEGAL_PARAGRAPH})\s*$", re.IGNORECASE)


def legal_anchor(label: str) -> str:
    suffix = re.sub(r"\s+", "", label.replace("§", "")).lower()
    return f"paragraf-{suffix}"


def add_attr_id_to_heading(line: str, anchor_id: str) -> str:
    match = HEADING_LINE_RE.match(line)
    if not match:
        return line
    attrs = (match.group("attrs") or "").strip()
    if re.search(rf"(?:^|\s)#{re.escape(anchor_id)}(?:\s|$)", attrs):
        return line
    attrs = f"{attrs} #{anchor_id}".strip()
    return f"{match.group('marks')} {match.group('title')} {{{attrs}}}"


def promote_legal_paragraph_headings(markdown: str) -> str:
    """Make official legal paragraph markers addressable Markdown headings.

    BR18 pages often contain bare text rows like ``§ 5`` or linked rows like
    ``[§ 6a](...) Følgende ...``.  Zensical cannot infer that these legal
    markers are section headings, and CSS-only decoration would not create TOC,
    search, or anchor targets.  Convert the markers to explicit headings with
    stable ``paragraf-*`` ids while keeping source UUIDs on enclosing section
    headings.
    """
    lines = markdown.splitlines()
    first_h1 = next((line for line in lines if line.startswith("# ")), "")
    if first_h1 and "§" not in first_h1:
        return markdown
    out: list[str] = []
    pending_section_label: str | None = None

    def append_heading(line: str) -> None:
        if out and out[-1] != "":
            out.append("")
        out.append(line)

    def emit_paragraph(label: str, rest: str = "") -> None:
        append_heading(f"### {label.strip()} {{#{legal_anchor(label)}}}")
        rest = rest.strip()
        if rest:
            out.append("")
            out.append(rest)

    def is_inline_reference_continuation(text: str) -> bool:
        """Return true when text following a § marker is reference syntax, not heading text."""
        text = text.strip()
        return bool(text and (re.match(r"[,.;:]", text) or re.match(r"[a-zæøå]", text)))

    i = 0
    while i < len(lines):
        raw = lines[i].rstrip()
        stripped = raw.strip()

        if stripped in {"[]", "Linket er kopieret", "Til top []", "Fold alle ind"}:
            i += 1
            continue

        linked = LINKED_LEGAL_PARAGRAPH_RE.match(stripped)
        if linked:
            rest = linked.group("rest").strip()
            next_text = ""
            if not rest:
                for candidate in lines[i + 1 : min(i + 4, len(lines))]:
                    if candidate.strip():
                        next_text = candidate.strip()
                        break
            if is_inline_reference_continuation(rest) or (not rest and next_text and is_inline_reference_continuation(next_text)):
                out.append(raw)
            else:
                emit_paragraph(linked.group("label"), rest)
            i += 1
            continue

        section_link = LEGAL_SECTION_LINK_RE.match(stripped)
        if section_link:
            pending_section_label = section_link.group("label").strip()
            i += 1
            continue

        heading = HEADING_LINE_RE.match(stripped)
        if heading and pending_section_label and not heading.group("title").startswith("§"):
            attrs = (heading.group("attrs") or "").strip()
            attr_text = f" {{{attrs}}}" if attrs else ""
            append_heading(f"{heading.group('marks')} {pending_section_label} {heading.group('title')}{attr_text}")
            pending_section_label = None
            i += 1
            continue
        pending_section_label = None

        if heading:
            if heading.group("title").startswith("§"):
                label_match = LEGAL_PARAGRAPH_RE.match(heading.group("title"))
                if label_match and " - " not in heading.group("title") and len(heading.group("marks")) >= 3:
                    append_heading(add_attr_id_to_heading(stripped, legal_anchor(label_match.group("label"))))
                else:
                    append_heading(raw)
            else:
                out.append(raw)
            i += 1
            continue

        para = LEGAL_PARAGRAPH_RE.match(stripped)
        chunks = [chunk.strip() for chunk in INLINE_LEGAL_SPLIT_RE.split(stripped) if chunk.strip()]
        if para and not stripped.startswith("#"):
            label = para.group("label")
            rest = para.group("rest").strip()
            if is_inline_reference_continuation(rest):
                out.append(raw)
                i += 1
                continue
            if not rest:
                next_text = ""
                for candidate in lines[i + 1 : min(i + 4, len(lines))]:
                    if candidate.strip():
                        next_text = candidate.strip()
                        break
                if next_text and re.match(r"[a-zæøå]", next_text):
                    out.append(raw)
                    i += 1
                    continue
            # Split paragraphs that pandoc glued together: "§ 1 text § 2 text".
            if len(chunks) > 1 and all(LEGAL_PARAGRAPH_RE.match(chunk) for chunk in chunks):
                for chunk in chunks:
                    m = LEGAL_PARAGRAPH_RE.match(chunk)
                    if m:
                        emit_paragraph(m.group("label"), m.group("rest"))
                        out.append("")
                while out and out[-1] == "":
                    out.pop()
            else:
                emit_paragraph(label, rest)
            i += 1
            continue

        if len(chunks) > 1 and any(LEGAL_PARAGRAPH_RE.match(chunk) for chunk in chunks[1:]):
            first = chunks[0]
            if first:
                out.append(first)
                out.append("")
            for chunk in chunks[1:]:
                m = LEGAL_PARAGRAPH_RE.match(chunk)
                if m:
                    emit_paragraph(m.group("label"), m.group("rest"))
                    out.append("")
                else:
                    out.append(chunk)
                    out.append("")
            while out and out[-1] == "":
                out.pop()
            i += 1
            continue

        trailing = TRAILING_LEGAL_MARKER_RE.match(stripped)
        if trailing and not stripped.startswith("#"):
            next_text = ""
            for candidate in lines[i + 1 : min(i + 4, len(lines))]:
                if candidate.strip():
                    next_text = candidate.strip()
                    break
            if next_text and re.match(r"[A-ZÆØÅ]", next_text):
                out.append(trailing.group("prefix").rstrip())
                out.append("")
                emit_paragraph(trailing.group("label"))
                i += 1
                continue

        if heading and heading.group("title").startswith("§"):
            label_match = LEGAL_PARAGRAPH_RE.match(heading.group("title"))
            if label_match and " - " not in heading.group("title"):
                out.append(add_attr_id_to_heading(stripped, legal_anchor(label_match.group("label"))))
                i += 1
                continue

        out.append(raw)
        i += 1

    text = "\n".join(out)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text + ("\n" if markdown.endswith("\n") else "")

UUID = r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"

TRIGGER_TITLE = "br18-accordion-trigger"
# Accordion triggers, marked by the Cleaner; other uuid links point at other pages' sections.
UUID_ANCHOR_LINK_RE = re.compile(
    rf"(?P<space>\s*)\[(?P<label>[^\]]+)\]\([^)\s]*#(?P<id>{UUID}) \"{TRIGGER_TITLE}\"\)"
)
HEADING_RE = re.compile(r"^(#{1,6}\s+.*?)(?:\s+\{[^}]*\})?\s*$")
HEADING_ATTR_RE = re.compile(r"^(?P<head>#{1,6}\s+.*?)(?:\s+\{(?P<attrs>[^}]*)\})?\s*$")
EXPLICIT_ANCHOR_RE = re.compile(
    r"(?:\{[^}]*#(?P<attr>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})[^}]*\}|<[^>]+\bid=[\"'](?P<html>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})[\"'][^>]*>)"
)


def explicit_anchor_ids(markdown: str) -> set[str]:
    ids: set[str] = set()
    for match in EXPLICIT_ANCHOR_RE.finditer(markdown):
        ids.add(match.group("attr") or match.group("html"))
    return ids


def add_heading_id(line: str, anchor_id: str) -> str:
    match = HEADING_ATTR_RE.match(line)
    if not match:
        return line
    attrs = (match.group("attrs") or "").strip()
    attrs = re.sub(rf"\s*#(?:{UUID})\b", "", attrs).strip()
    new_attrs = f"#{anchor_id}" if not attrs else f"{attrs} #{anchor_id}"
    return f"{match.group('head')} {{{new_attrs}}}"


def attach_anchor_reference_ids(markdown: str) -> str:
    """Move Bygningsreglementet accordion UUID anchors onto their headings.

    The source site renders each content block as a ``section.anchor-reference``
    with a UUID ``id`` and an accordion link such as ``[Kap. 8](#uuid)``.  The
    cleaner intentionally removes the chrome around those accordions, leaving
    the trigger link immediately before the section heading.  Zensical validates
    local anchors, so keep the original section destination by converting the
    following Markdown heading to ``## Heading { #uuid }`` and removing only the
    leftover trigger link.
    """
    lines = markdown.splitlines()
    known_ids = explicit_anchor_ids(markdown)

    for index, line in enumerate(lines):
        for match in reversed(list(UUID_ANCHOR_LINK_RE.finditer(line))):
            anchor_id = match.group("id")
            label = match.group("label").strip().lower()
            if label.startswith("gå til") or len(label) > 80:
                continue

            heading_index = None
            for candidate in range(index + 1, min(index + 5, len(lines))):
                if not lines[candidate].strip():
                    continue
                if HEADING_RE.match(lines[candidate]):
                    heading_index = candidate
                break

            if heading_index is None:
                continue

            heading_line = add_heading_id(lines[heading_index], anchor_id)
            if re.search(r"\w", label):
                hm = HEADING_ATTR_RE.match(heading_line)
                marks, _, title = hm.group("head").partition(" ") if hm else ("", "", "")
                tag = match.group("label").strip()
                if hm and not title.strip().startswith(tag) and not (label.startswith("§") and title.startswith("§")):
                    heading_line = f"{marks} {tag} {title.strip()}".rstrip()
                    attrs = (hm.group("attrs") or "").strip()
                    if attrs:
                        heading_line = f"{heading_line} {{{attrs}}}"
            lines[heading_index] = heading_line
            known_ids.add(anchor_id)
            line = (line[: match.start()] + line[match.end() :]).rstrip()
            lines[index] = line

    return "\n".join(lines) + ("\n" if markdown.endswith("\n") else "")


def convert_file(path: Path, docs_root: Path, delete_html: bool) -> bool:
    output = output_path_for_html(path)
    if output is None:
        return False
    html_text = path.read_text(encoding="utf-8")
    cleaner = Cleaner(path.parent, docs_root)
    cleaned = cleaner.clean(html_text)

    proc = subprocess.run(
        [
            "pandoc",
            "--from",
            "html",
            "--to",
            "markdown-smart-grid_tables-simple_tables-multiline_tables",
            "--wrap=none",
        ],
        input=cleaned,
        text=True,
        capture_output=True,
        check=True,
    )

    # Python-Markdown cannot unescape `\<`, so the page would show the backslash.
    markdown = re.sub(r"\[\]\{#[^}]+\}", "", proc.stdout.replace("\\<", "&lt;"))
    markdown = re.sub(r"(?m)^\[\]\([^\n]+\)\s*$", "", markdown)
    markdown = re.sub(
        r"\*\[\]\([^)]+(?:localLink:umb:|%7BlocalLink:umb:)[^)]+\)([^*]+)\*",
        r"*\1*",
        markdown,
    )
    markdown = fix_empty_english_version_links(markdown)
    markdown = normalize_media_alias_links(markdown)
    markdown = normalize_duplicate_uuid_fragments(markdown)
    # The prose passes below split "1)" items and rewrite lines, which breaks table rows.
    tables: list[str] = []

    def stash_table(match: re.Match[str]) -> str:
        tables.append(match.group(0))
        return f"BR18TABLE{len(tables) - 1}"

    markdown = TABLE_BLOCK_RE.sub(stash_table, markdown)
    markdown = normalize_markdown_linebreak_artifacts(markdown)
    markdown = attach_anchor_reference_ids(markdown)
    for _ in range(4):
        promoted = promote_legal_paragraph_headings(markdown)
        if promoted == markdown:
            break
        markdown = promoted
    markdown = escape_unresolved_reference_labels(markdown)
    markdown = TABLE_TOKEN_RE.sub(lambda m: tables[int(m.group(1))], markdown)
    markdown = markdown.replace(f' "{TRIGGER_TITLE}")', ")")
    if output.parent == path:
        if not delete_html:
            raise RuntimeError(f"cannot keep extensionless route HTML while writing {output}")
        path.unlink()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(markdown.strip() + "\n", encoding="utf-8")
    if delete_html and path.exists() and path.is_file():
        path.unlink()
    return True


def looks_like_html_file(path: Path) -> bool:
    if path.suffix.lower() in {".html", ".htm", ".xhtml"} or "?" in path.name:
        return True
    if path.suffix != "":
        return False
    try:
        head = path.read_bytes()[:1024].lower()
    except OSError:
        return False
    stripped = head.lstrip()
    return stripped.startswith(b"<!doctype html") or stripped.startswith(b"<html") or b"<html" in head


def iter_html_paths(docs_root: Path, selected_paths: list[str]) -> list[Path]:
    if not selected_paths:
        return sorted(
            path
            for path in docs_root.rglob("*")
            if path.is_file()
            and "historisk" not in path.relative_to(docs_root).parts
            and looks_like_html_file(path)
        )

    paths: list[Path] = []
    seen: set[Path] = set()
    for value in selected_paths:
        candidate = (docs_root / value).resolve()
        if not candidate.exists():
            raise SystemExit(f"path not found under docs root: {value}")
        if not candidate.is_relative_to(docs_root):
            raise SystemExit(f"path escapes docs root: {value}")
        matches = (
            [candidate]
            if candidate.is_file()
            else sorted(path for path in candidate.rglob("*") if path.is_file() and looks_like_html_file(path))
        )
        for match in matches:
            if match not in seen:
                seen.add(match)
                paths.append(match)
    return sorted(paths)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--docs-root", default="docs")
    parser.add_argument("--keep-html", action="store_true")
    parser.add_argument("paths", nargs="*")
    args = parser.parse_args()

    docs_root = Path(args.docs_root).resolve()
    if not docs_root.exists():
        raise SystemExit(f"docs root not found: {docs_root}")

    converted = 0
    skipped = 0
    paths = iter_html_paths(docs_root, args.paths)
    workers = min(8, os.cpu_count() or 1)
    with futures.ThreadPoolExecutor(max_workers=workers) as pool:
        future_map = {
            pool.submit(convert_file, path, docs_root, not args.keep_html): path
            for path in paths
        }
        for future in futures.as_completed(future_map):
            path = future_map[future]
            try:
                ok = future.result()
            except Exception as exc:  # pragma: no cover - batch conversion guard
                print(f"failed: {path} ({exc})", file=sys.stderr)
                skipped += 1
                continue
            if ok:
                converted += 1
            else:
                skipped += 1

    print(f"converted={converted} skipped={skipped}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
