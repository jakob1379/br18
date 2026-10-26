from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from audit_br18_parity import cache_file

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "build_chapter_hubs.py"
SITE = "https://www.bygningsreglementet.dk"


class ChapterHubsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.root)
        self.docs = self.root / "docs"
        self.cache = self.root / "cache"
        self.cache.mkdir()

    def doc(self, rel: str, text: str) -> None:
        (self.docs / rel).mkdir(parents=True, exist_ok=True)
        (self.docs / rel / "index.md").write_text(text, encoding="utf-8")

    def origin(self, path: str, html: str = "") -> None:
        url = SITE + path
        record = {"url": url, "final": url, "status": 200, "html": f"<html><body><main>{html}</main></body></html>"}
        cache_file(self.cache, url).write_text(json.dumps(record), encoding="utf-8")

    def build(self) -> None:
        subprocess.run([sys.executable, str(SCRIPT), "--docs-root", str(self.docs), "--cache-dir", str(self.cache)], check=True, capture_output=True)

    def read(self, rel: str) -> str:
        return (self.docs / rel / "index.md").read_text(encoding="utf-8")

    def test_chapter_hub_is_its_krav_page_and_its_guide_page_the_origins_vejledning_tab(self) -> None:
        chapter = "tekniske-bestemmelser/07"
        self.doc(chapter, "# Gammel kopi\n\nForældet tekst.\n")
        self.doc(f"{chapter}/brv", "# Gammel kopi\n\nForældet vejledning.\n")
        self.doc(
            f"{chapter}/krav",
            "# Byggepladsen (§ 161 - § 165)\n\n### § 161 {#paragraf-161}\n\n<span id=\"p161\"></span>\n\n"
            "Se [§ 162](162/#x) og [bilag](../../../bilag/b1/).\n",
        )
        self.doc(f"{chapter}/vejledninger", "# Byggepladsen (§ 161 - § 165)\n\n- [Generel vejledning](generel_vejledning/)\n")
        tab = f'<a href="{SITE}/{chapter}/vejledninger/" class="nav-tab__link">Vejledning</a>'
        self.origin(f"/{chapter}/krav/", tab)

        self.build()
        self.build()

        self.assertEqual(
            self.read(chapter),
            "# Byggepladsen (§ 161 - § 165)\n\n"
            "[Krav](./){ .md-button .md-button--primary }\n[Vejledning](brv/){ .md-button }\n\n"
            "### § 161 {#paragraf-161}\n\nSe [§ 162](krav/162/#x) og [bilag](../../bilag/b1/).\n",
        )
        self.assertEqual(
            self.read(f"{chapter}/brv"),
            "---\ntitle: Byggepladsen (§ 161 - § 165) – Vejledning\n---\n\n# Byggepladsen (§ 161 - § 165)\n\n"
            "[Krav](../){ .md-button }\n[Vejledning](./){ .md-button .md-button--primary }\n\n"
            "- [Generel vejledning](../vejledninger/generel_vejledning/)\n",
        )

    def test_guide_page_the_origin_serves_keeps_its_own_content(self) -> None:
        chapter = "ovrige-bestemmelser/23"
        self.doc(f"{chapter}/krav", "# Beregningsregler (§ 453 - § 458)\n\nKrav.\n")
        self.doc(f"{chapter}/brv", "# Beregningsregler (§ 453 - § 458)\n\n- [Udnyttelige tagetager](udnyttelige-tagetager/)\n")
        self.origin(f"/{chapter}/krav/", f'<a href="{SITE}/{chapter}/brv/" class="nav-tab__link">Vejledning</a>')
        self.origin(f"/{chapter}/brv/", "Se alle vejledninger")

        self.build()
        self.build()

        self.assertEqual(
            self.read(f"{chapter}/brv"),
            "---\ntitle: Beregningsregler (§ 453 - § 458) – Vejledning\n---\n\n# Beregningsregler (§ 453 - § 458)\n\n"
            "[Krav](../){ .md-button }\n[Vejledning](./){ .md-button .md-button--primary }\n\n"
            "- [Udnyttelige tagetager](udnyttelige-tagetager/)\n",
        )

    def test_chapter_without_guides_has_no_vejledning_tab(self) -> None:
        chapter = "tekniske-bestemmelser/06"
        self.doc(f"{chapter}/krav", "# Brugerbetjente anlæg (§ 159 - § 160)\n\nKrav.\n")
        self.origin(f"/{chapter}/krav/")

        self.build()

        self.assertEqual(self.read(chapter), "# Brugerbetjente anlæg (§ 159 - § 160)\n\n[Krav](./){ .md-button .md-button--primary }\n\nKrav.\n")
        self.assertFalse((self.docs / chapter / "brv").exists())


if __name__ == "__main__":
    unittest.main()
