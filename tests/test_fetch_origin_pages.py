from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "fetch_origin_pages.py"
SITE = "https://www.bygningsreglementet.dk"


def page(path: str, body: str, expand_all: str | None = None, trigger: str | None = None, final: str | None = None) -> dict:
    links = f'<a href="{SITE}{expand_all}?Layout=ShowAll" class="link--expand-all">Fold alle ud</a>' if expand_all else ""
    if trigger:
        links += f'<a href="{SITE}{trigger}#0b0c2f0e-1111-2222-3333-444455556666" class="accordion__trigger">1.</a>'
    url = SITE + path
    return {"url": url, "final": SITE + (final or path), "status": 200, "html": f"<html><body><main>{links}<p>{body}</p></main></body></html>"}


class FetchFromSnapshotTest(unittest.TestCase):
    def fetch(self, records: list[dict], *paths: str) -> Path:
        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, tmp)
        cache = tmp / "cache"
        cache.mkdir()
        for record in records:
            (cache / f"{hashlib.sha256(record['url'].encode()).hexdigest()[:32]}.json").write_text(json.dumps(record))
        docs = tmp / "docs"
        subprocess.run(
            [sys.executable, str(SCRIPT), "--docs-root", str(docs), "--cache-dir", str(cache), *(SITE + p for p in paths)],
            check=True,
            capture_output=True,
        )
        return docs

    def test_guide_root_gets_its_show_all_view_and_a_subpage_keeps_its_own_section(self) -> None:
        guide = "/tekniske-bestemmelser/16/vejledninger/generel_vejledning/"
        docs = self.fetch(
            [
                page(guide, "kun overskrifter", expand_all=guide, trigger=guide + "2_1/"),
                page(guide + "?Layout=ShowAll", "hele vejledningen"),
                page(guide + "2_1/", "eget afsnit", expand_all=guide + "2_1/", trigger=guide + "2_1/"),
            ],
            guide,
            guide + "2_1/",
        )

        self.assertIn("hele vejledningen", (docs / guide.strip("/") / "index.html").read_text())
        self.assertIn("eget afsnit", (docs / guide.strip("/") / "2_1" / "index.html").read_text())

    def test_krav_subpage_gets_its_chapter_roots_show_all_view(self) -> None:
        krav = "/tekniske-bestemmelser/16/krav/"
        docs = self.fetch(
            [
                page(krav + "358/", "kun § 358", expand_all=krav, trigger=krav + "358/"),
                page(krav + "?Layout=ShowAll", "hele kapitlet"),
            ],
            krav + "358/",
        )

        self.assertIn("hele kapitlet", (docs / krav.strip("/") / "358" / "index.html").read_text())

    def test_redirected_page_is_written_at_its_target_path(self) -> None:
        alias = "/ovrige-bestemmelser/29/brv/gammel-vejledning/"
        target = "/ovrige-bestemmelser/29/brv/ny-vejledning/"
        docs = self.fetch([page(alias, "vejledningen", final=target)], alias)

        self.assertIn("vejledningen", (docs / target.strip("/") / "index.html").read_text())
        self.assertFalse((docs / alias.strip("/")).exists())

    def test_page_missing_from_the_snapshot_is_reported_and_the_rest_fetched(self) -> None:
        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, tmp)
        cache = tmp / "cache"
        cache.mkdir()
        record = page("/tekniske-bestemmelser/16/krav/", "kapitlet")
        (cache / f"{hashlib.sha256(record['url'].encode()).hexdigest()[:32]}.json").write_text(json.dumps(record))

        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--docs-root", str(tmp / "docs"), "--cache-dir", str(cache),
             f"{SITE}/tekniske-bestemmelser/16/", f"{SITE}/tekniske-bestemmelser/16/krav/"],
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("tekniske-bestemmelser/16/", result.stderr)
        self.assertIn("kapitlet", (tmp / "docs" / "tekniske-bestemmelser" / "16" / "krav" / "index.html").read_text())

    def test_mixed_case_url_is_written_at_the_lowercase_path(self) -> None:
        mixed = "/Tekniske-bestemmelser/17/Vejledninger/Kontorbygninger"
        record = page(mixed.lower() + "/", "kontorbyggeri", final=mixed)
        docs = self.fetch([record], mixed)

        self.assertIn("kontorbyggeri", (docs / mixed.strip("/").lower() / "index.html").read_text())


if __name__ == "__main__":
    unittest.main()
