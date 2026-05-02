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

    path = canonicalize_asset_path(parsed.path or "", source_dir, docs_root)
    if not path and not parsed.fragment:
        return None

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

    directory_route = path.endswith("/") or path == "/"

    if directory_route:
        target = local_target
        rel = os.path.relpath(target, source_dir)
        return rel if rel != "." else "./"

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
            self.parts.append(f"<{tag}{self._render_attrs(attrs)} />")
            return

        if self.skip_depth > 0 or self._should_skip(tag, attrs):
            self.stack.append("skip")
            self.skip_depth += 1
            return

        if tag in FLATTEN_TAGS:
            self.stack.append("flatten")
            if tag in BLOCK_FLATTEN_TAGS:
                self.parts.append("\n\n")
            return

        self.stack.append("emit")
        attrs = self._rewrite_attrs(tag, attrs)
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
        self.parts.append(f"</{tag}>")

    def handle_data(self, data: str) -> None:
        if (
            self.skip_depth == 0
            and data.strip() != "Swipe horisontalt for at se alle emner"
        ):
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
        return path.with_suffix(".md")

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


def escape_unresolved_reference_labels(markdown: str) -> str:
    return re.sub(
        r"(?<![!\\])\[([^\]\n]+)\](?![\[(])",
        lambda match: rf"\[{match.group(1)}\]",
        markdown,
    )


UUID = r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
UUID_ANCHOR_LINK_RE = re.compile(
    rf"(?P<space>\s*)\[(?P<label>[^\]]+)\]\([^)]*#(?P<id>{UUID})\)"
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
        for match in list(UUID_ANCHOR_LINK_RE.finditer(line)):
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

            lines[heading_index] = add_heading_id(lines[heading_index], anchor_id)
            known_ids.add(anchor_id)
            line = UUID_ANCHOR_LINK_RE.sub("", line, count=1).rstrip()
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
        ["pandoc", "--from", "html", "--to", "markdown", "--wrap=none"],
        input=cleaned,
        text=True,
        capture_output=True,
        check=True,
    )

    markdown = re.sub(r"\[\]\{#[^}]+\}", "", proc.stdout)
    markdown = re.sub(r"(?m)^\[\]\([^\n]+\)\s*$", "", markdown)
    markdown = re.sub(
        r"\*\[\]\([^)]+(?:localLink:umb:|%7BlocalLink:umb:)[^)]+\)([^*]+)\*",
        r"*\1*",
        markdown,
    )
    markdown = fix_empty_english_version_links(markdown)
    markdown = normalize_media_alias_links(markdown)
    markdown = normalize_duplicate_uuid_fragments(markdown)
    markdown = attach_anchor_reference_ids(markdown)
    markdown = escape_unresolved_reference_labels(markdown)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(markdown.lstrip(), encoding="utf-8")
    if delete_html:
        path.unlink()
    return True


def iter_html_paths(docs_root: Path, selected_paths: list[str]) -> list[Path]:
    if not selected_paths:
        return sorted(docs_root.rglob("*.html"))

    paths: list[Path] = []
    seen: set[Path] = set()
    for value in selected_paths:
        candidate = (docs_root / value).resolve()
        if not candidate.exists():
            raise SystemExit(f"path not found under docs root: {value}")
        if not candidate.is_relative_to(docs_root):
            raise SystemExit(f"path escapes docs root: {value}")
        matches = (
            [candidate] if candidate.is_file() else sorted(candidate.rglob("*.html"))
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
