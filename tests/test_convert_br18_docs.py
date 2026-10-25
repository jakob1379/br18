from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "convert_br18_docs.py"


class ConvertTest(unittest.TestCase):
    def convert(self, body: str) -> str:
        root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, root)
        (root / "side").mkdir()
        (root / "side" / "index.html").write_text(f"<html><body><main>{body}</main></body></html>", encoding="utf-8")
        subprocess.run([sys.executable, str(SCRIPT), "--docs-root", str(root)], check=True, capture_output=True)
        return (root / "side" / "index.md").read_text(encoding="utf-8")

    def test_whitespace_only_emphasis_is_dropped(self) -> None:
        markdown = self.convert(
            "<p>Tekst<strong><em>&nbsp;</em></strong>slut</p>"
            "<p>Projektkrav<em><sup><span> </span></sup></em><sup>2)</sup></p>"
        )

        self.assertNotIn("*", markdown)
        self.assertIn("Tekst slut", markdown)
        self.assertIn("Projektkrav", markdown)

    def test_nested_emphasis_of_one_kind_is_merged(self) -> None:
        markdown = self.convert(
            "<p><strong><strong><em>Overskrift<br></em><br></strong></strong>Tekst</p>"
            "<p><strong>Spørgsmål? <strong>(11-12-2020)</strong></strong></p>"
        )

        self.assertIn("***Overskrift***", markdown)
        self.assertNotIn("****", markdown)
        self.assertIn("**Spørgsmål? (11-12-2020)**", markdown)

    def test_line_break_opening_an_emphasis_moves_out_of_it(self) -> None:
        markdown = self.convert("<p><em><br>SBi-anvisning 231, Fundering af mindre bygninger</em></p>")

        self.assertIn("*SBi-anvisning 231, Fundering af mindre bygninger*", markdown)
        self.assertNotRegex(markdown, r"(?m)^\*\s*$")

    def test_links_to_origin_pages_point_at_directories(self) -> None:
        markdown = self.convert(
            '<p><a href="/side/vejledning">Vejledning</a> <a href="https://www.bygningsreglementet.dk/side">Her</a>'
            ' <a href="/andet/krav#paragraf-1">Krav</a> <a href="/media/abc/fil.pdf">PDF</a> <a href="#afsnit">Afsnit</a></p>'
        )

        self.assertIn("[Vejledning](vejledning/)", markdown)
        self.assertIn("[Her](./)", markdown)
        self.assertIn("[Krav](../andet/krav/#paragraf-1)", markdown)
        self.assertIn("[PDF](../media/abc/fil.pdf)", markdown)
        self.assertIn("[Afsnit](#afsnit)", markdown)

    def test_page_ends_with_a_single_newline(self) -> None:
        markdown = self.convert("<p>Tekst</p><p><a href='/x'></a></p>")

        self.assertTrue(markdown.endswith("Tekst\n"), repr(markdown[-20:]))

    def test_emphasis_closing_after_a_non_breaking_space_closes(self) -> None:
        markdown = self.convert("<p><strong><em>konstruktionsklasse 2-4.&nbsp; </em></strong>Mere</p>")

        self.assertIn("***konstruktionsklasse 2-4.***", markdown)


if __name__ == "__main__":
    unittest.main()
