from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "fix_broken_links.py"


class FixBrokenLinksTest(unittest.TestCase):
    def setUp(self) -> None:
        self.root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.root)

    def page(self, rel: str, markdown: str = "# Side\n", ids: str = "") -> None:
        (self.root / "docs" / rel).mkdir(parents=True, exist_ok=True)
        (self.root / "docs" / rel / "index.md").write_text(markdown, encoding="utf-8")
        (self.root / "site" / rel).mkdir(parents=True, exist_ok=True)
        (self.root / "site" / rel / "index.html").write_text(f"<html><body><h1{ids}>Side</h1></body></html>", encoding="utf-8")

    def fix(self, *extra: str) -> str:
        subprocess.run(
            [sys.executable, str(SCRIPT), "--docs-root", str(self.root / "docs"), "--site-root", str(self.root / "site"), *extra],
            check=True,
            capture_output=True,
        )
        return (self.root / "docs" / "kilde" / "index.md").read_text(encoding="utf-8")

    def test_fragment_no_page_has_is_dropped(self) -> None:
        self.page("kilde", "Se [§§ 126-133](../maal/#3cd45dcf-33dd-46c8-b4e6-7489f2b06d01).\n")
        self.page("maal", ids=' id="paragraf-126"')

        self.assertEqual(self.fix(), "Se [§§ 126-133](../maal/).\n")

    def test_fragment_several_other_pages_have_is_dropped(self) -> None:
        self.page("kilde", "Se [Bilag 1a](../bilag---1a/#33520e5b).\n")
        self.page("bilag-1a")
        self.page("andet", ids=' id="33520e5b"')
        self.page("tredje", ids=' id="33520e5b"')

        self.assertEqual(self.fix(), "Se [Bilag 1a](../bilag-1a/).\n")

    def test_path_that_differs_in_danish_letters_and_hyphen_runs_resolves(self) -> None:
        self.page("kilde", "Se [Bilag 1a](../enfamiliehuse/bilag-1a---præ-accepterede-løsninger/).\n")
        self.page("enfamiliehuse/bilag-1a-prae-accepterede-loesninger")

        self.assertEqual(self.fix(), "Se [Bilag 1a](../enfamiliehuse/bilag-1a-prae-accepterede-loesninger/).\n")

    def test_link_to_an_origin_redirect_points_at_its_target(self) -> None:
        self.page("kilde", "Se [kapitel 34](../34/vejledninger/vejledning-til-kap34/).\n")
        self.page("34/vejledninger/vejledning-til-kapitel-34")
        cache = self.root / "cache"
        cache.mkdir()
        url = "https://www.bygningsreglementet.dk/34/vejledninger/vejledning-til-kap34/"
        record = {"url": url, "final": "https://www.bygningsreglementet.dk/34/vejledninger/vejledning-til-kapitel-34/", "status": 200, "html": ""}
        (cache / f"{hashlib.sha256(url.encode()).hexdigest()[:32]}.json").write_text(json.dumps(record), encoding="utf-8")

        self.assertEqual(self.fix("--cache-dir", str(cache)), "Se [kapitel 34](../34/vejledninger/vejledning-til-kapitel-34/).\n")

    def test_link_to_the_origins_dead_parking_guide_points_at_the_guide(self) -> None:
        self.page("kilde", "Se [parkering](../tekniske-bestemmelser/02/vejledninger/parkering/).\n")
        self.page("tekniske-bestemmelser/20/vejledninger/parkering")

        self.assertEqual(self.fix(), "Se [parkering](../tekniske-bestemmelser/20/vejledninger/parkering/).\n")


if __name__ == "__main__":
    unittest.main()
