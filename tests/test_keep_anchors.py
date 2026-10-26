from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "keep_anchors.py"


class KeepAnchorsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.root)

    def run_script(self, markdown: str, built: str, baseline: str, *extra: str) -> tuple[subprocess.CompletedProcess[str], str]:
        (self.root / "docs" / "side").mkdir(parents=True)
        (self.root / "docs" / "side" / "index.md").write_text(markdown, encoding="utf-8")
        (self.root / "site" / "side").mkdir(parents=True)
        (self.root / "site" / "side" / "index.html").write_text(
            f'<html><body><article class="md-content__inner md-typeset">{built}</article></body></html>', encoding="utf-8"
        )
        (self.root / "required.tsv").write_text(baseline, encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--docs-root", str(self.root / "docs"), "--site-dir", str(self.root / "site"),
             "--baseline", str(self.root / "required.tsv"), *extra],
            capture_output=True,
            text=True,
        )
        return result, (self.root / "docs" / "side" / "index.md").read_text(encoding="utf-8")

    def test_anchor_of_a_renamed_heading_goes_before_that_heading(self) -> None:
        _, markdown = self.run_script(
            "# Vejledning\n\n### 1.0. Forord {#65b73685}\n\nTekst.\n",
            '<h1 id="vejledning">Vejledning</h1><h3 id="65b73685">1.0. Forord</h3><p>Tekst.</p>',
            "side/\tvejledning\tVejledning\nside/\tforord\tForord\n",
        )

        self.assertEqual(markdown, '# Vejledning\n\n<span id="forord"></span>\n\n### 1.0. Forord {#65b73685}\n\nTekst.\n')

    def test_anchor_of_a_heading_no_longer_on_the_page_goes_after_its_section(self) -> None:
        _, markdown = self.run_script(
            "# Vejledning\n\n### 1. Indledning {#sec1}\n\nGuiden indleder.\n\n### 2. Ramper {#sec2}\n\nRamper skal være jævne.\n",
            '<h1 id="vejledning">Vejledning</h1><h3 id="sec1">1. Indledning</h3><p>Guiden indleder.</p><h3 id="sec2">2. Ramper</h3><p>Ramper skal være jævne.</p>',
            "side/\tsec1\t1. Indledning\nside/\tbaggrund\tBaggrund\nside/\tformaal\tFormål\nside/\tsec2\t2. Ramper\n",
        )

        self.assertEqual(
            markdown,
            "# Vejledning\n\n### 1. Indledning {#sec1}\n\nGuiden indleder.\n\n"
            '<span id="baggrund"></span><span id="formaal"></span>\n\n'
            "### 2. Ramper {#sec2}\n\nRamper skal være jævne.\n",
        )

    def test_check_reports_missing_anchors_and_changes_nothing(self) -> None:
        result, markdown = self.run_script(
            "# Krav\n\n### § 9\n", '<h1 id="krav">Krav</h1><h3 id="9">§ 9</h3>', "side/\tparagraf-9\t§ 9\n", "--check"
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("side/#paragraf-9", result.stderr)
        self.assertEqual(markdown, "# Krav\n\n### § 9\n")


if __name__ == "__main__":
    unittest.main()
