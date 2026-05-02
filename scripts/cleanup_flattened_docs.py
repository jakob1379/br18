#!/usr/bin/env python3

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


DUPLICATE_ROOTS = (
    "Administrative-bestemmelser",
    "Bilag",
    "Historisk",
    "Ovrige-bestemmelser",
    "Tekniske-bestemmelser",
    "Vejledninger",
)

JUNK_DIRS = (
    "tekniske-bestemmelser/11/brv/energiberegning-af-hospitaler/andet",
    "tekniske-bestemmelser/11/brv/energiberegning-af-hospitaler/bygsagb",
    "tekniske-bestemmelser/11/brv/energiberegning-af-hospitaler/eltv",
    "tekniske-bestemmelser/11/brv/energiberegning-af-hospitaler/i",
    "tekniske-bestemmelser/11/brv/energiberegning-af-hospitaler/ink",
    "tekniske-bestemmelser/11/brv/energiberegning-af-hospitaler/tilb",
    "tekniske-bestemmelser/11/brv/energiberegning-af-hospitaler/tte",
    "tekniske-bestemmelser/11/brv/energiberegning-af-hospitaler/varmeg",
    "tekniske-bestemmelser/11/brv/energiberegning-af-hospitaler/ve_a",
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--docs-root", default="docs")
    args = parser.parse_args()

    docs_root = Path(args.docs_root).resolve()
    if not docs_root.exists():
        raise SystemExit(f"docs root not found: {docs_root}")

    removed_showall = 0
    for path in sorted(docs_root.rglob("showall")):
        if path.is_dir():
            shutil.rmtree(path)
            removed_showall += 1

    removed_roots = 0
    for name in DUPLICATE_ROOTS:
        path = docs_root / name
        if path.exists():
            shutil.rmtree(path)
            removed_roots += 1

    removed_junk = 0
    for rel_path in JUNK_DIRS:
        path = docs_root / rel_path
        if path.exists():
            shutil.rmtree(path)
            removed_junk += 1

    print(
        f"removed_showall={removed_showall} removed_roots={removed_roots} removed_junk={removed_junk}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
