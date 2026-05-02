#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path


QUERY_ALIAS_RE = re.compile(r"__q_[0-9a-f]+(?=\.[^.]+$)")
TEXT_SUFFIXES = {
    ".css",
    ".html",
    ".htm",
    ".js",
    ".json",
    ".md",
    ".py",
    ".sh",
    ".svg",
    ".toml",
    ".txt",
    ".xml",
    ".yaml",
    ".yml",
}


def canonical_name(name: str) -> str:
    without_query = name.split("?", 1)[0]
    return QUERY_ALIAS_RE.sub("", without_query)


def sha256sum(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def referenced_elsewhere(root: Path, alias_name: str) -> bool:
    for path in root.rglob("*"):
        if not path.is_file() or path.parts[:2] == ("docs", "media"):
            continue
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if alias_name in text:
            return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--docs-media-root", default="docs/media")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    media_root = (repo_root / args.docs_media_root).resolve()
    if not media_root.exists():
        raise SystemExit(f"docs media root not found: {media_root}")

    removed = 0
    skipped_missing = 0
    skipped_content = 0
    skipped_ref = 0

    for alias_path in sorted(media_root.rglob("*")):
        if not alias_path.is_file():
            continue
        canonical = canonical_name(alias_path.name)
        if canonical == alias_path.name:
            continue

        canonical_path = alias_path.with_name(canonical)
        if not canonical_path.exists():
            skipped_missing += 1
            continue
        if sha256sum(alias_path) != sha256sum(canonical_path):
            skipped_content += 1
            continue
        if referenced_elsewhere(repo_root, alias_path.name):
            skipped_ref += 1
            continue

        print(alias_path.relative_to(repo_root))
        if not args.dry_run:
            alias_path.unlink()
        removed += 1

    print(
        f"removed={removed} skipped_missing={skipped_missing} "
        f"skipped_content={skipped_content} skipped_ref={skipped_ref}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
