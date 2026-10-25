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

    def test_line_breaks_inside_emphasis_close_it_on_each_line(self) -> None:
        markdown = self.convert(
            "<p><strong><span>- <strong><span>Sengestuer<br></span></strong><br>"
            "- <strong><span>Kontorer<br></span></strong><br></span></strong>Mere</p>"
            "<p><strong>Bygnings-<br> reglementets krav</strong></p>"
        )

        self.assertIn("- **Sengestuer**\n\n- **Kontorer**\n\nMere", markdown)
        self.assertIn("**Bygnings-**\n\n**reglementets krav**", markdown)

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

    def test_mixed_case_page_links_point_at_the_lowercase_corpus_paths(self) -> None:
        markdown = self.convert(
            '<p><a href="/Bilag/B2/Bilag_2/Tabel_7#abc">Tabel 7</a> <a href="/media/Ab1/Fil_Navn.PDF">PDF</a></p>'
        )

        self.assertIn("[Tabel 7](../bilag/b2/bilag_2/tabel_7/#abc)", markdown)
        self.assertIn("[PDF](../media/Ab1/Fil_Navn.PDF)", markdown)

    def test_historisk_links_stay_on_the_origin(self) -> None:
        markdown = self.convert(
            '<p><a href="/historisk/br18_version7/tekniske-bestemmelser/11/krav/267_270#9a9a97b3">Gammel</a>'
            ' <a href="http://bygningsreglementet.dk/Historisk/BR18_Version2/">Version 2</a></p>'
        )

        self.assertIn(
            "[Gammel](https://www.bygningsreglementet.dk/historisk/br18_version7/tekniske-bestemmelser/11/krav/267_270#9a9a97b3)",
            markdown,
        )
        self.assertIn("[Version 2](https://www.bygningsreglementet.dk/Historisk/BR18_Version2/)", markdown)

    def test_less_than_is_an_entity_not_a_backslash_escape(self) -> None:
        markdown = self.convert(
            "<p>5 °C &lt; T &lt; 15 °C</p><table><tr><td>Temperatur</td><td>T &lt; 5 °C</td></tr></table>"
        )

        self.assertNotIn("\\<", markdown)
        self.assertIn("5 °C &lt; T &lt; 15 °C", markdown)
        self.assertIn("T &lt; 5 °C", markdown)

    def test_whitespace_at_the_edges_of_sub_and_superscripts_moves_out(self) -> None:
        markdown = self.convert(
            "<p>T<sub>røg&nbsp;&nbsp;</sub>Røggastemperaturen, analyse<sup>&nbsp;a)&nbsp;</sup> og"
            " Sengestuer<sup><span>&nbsp; </span>a)</sup>, mere</p>"
        )

        self.assertRegex(markdown, r"T~røg~\s+Røggastemperaturen")
        self.assertRegex(markdown, r"analyse\s\^a\)\^\s+og")
        self.assertRegex(markdown, r"Sengestuer\s+\^a\)\^,")

    def test_only_accordion_triggers_give_headings_their_ids(self) -> None:
        markdown = self.convert(
            '<section id="1f0c2a3b-0000-4000-8000-000000000001"><div class="accordion__header">'
            '<a href="/side/#1f0c2a3b-0000-4000-8000-000000000001" class="accordion__trigger">'
            '<div class="accordion__tag">1.4.</div><h3 class="accordion__title">Livscyklus</h3></a></div>'
            '<div><p>Se <a href="/bilag/b2/bilag_2/tabel_7#787e83a6-b7d9-4a83-a4be-37574156daef">BR18, bilag 2, tabel 7</a></p>'
            "<h4>Tabellens opbygning</h4><p>Tekst</p></div></section>"
        )

        self.assertIn("### 1.4. Livscyklus {#1f0c2a3b-0000-4000-8000-000000000001}", markdown)
        self.assertIn("Se [BR18, bilag 2, tabel 7](../bilag/b2/bilag_2/tabel_7/#787e83a6-b7d9-4a83-a4be-37574156daef)", markdown)
        self.assertIn("#### Tabellens opbygning\n", markdown)

    def test_empty_text_links_keep_the_link_and_no_text(self) -> None:
        markdown = self.convert(
            '<p><em>English version</em><a href="/media/x/en.pdf" title="DS EN 1991-1-1 English"></a>-</p>'
            '<ul><li><a href="faq"></a></li><li><a href="/side/">Vejledning</a></li></ul>'
        )

        self.assertIn('[](../media/x/en.pdf "DS EN 1991-1-1 English")-', markdown)
        self.assertIn("- [](faq/)", markdown)

    def test_links_to_the_origins_internal_cms_host_are_dropped(self) -> None:
        markdown = self.convert(
            '<p><a rel="noopener" href="https://tbstsc.dev.local/-/media/71F0.ashx" target="_blank">Åbn r</a>'
            '<a rel="noopener" href="/media/y/r.pdf" target="_blank">ettelsesblad (Nyt vindue).</a></p>'
            '<p>Tekst.<a id="_anchor_1" href="https://tbstsc.dev.local/#_msocom_1"></a></p>'
        )

        self.assertNotIn("dev.local", markdown)
        self.assertIn('[Åbn rettelsesblad (Nyt vindue).](../media/y/r.pdf){rel="noopener" target="_blank"}', markdown)
        self.assertIn("Tekst.\n", markdown)

    def test_page_ends_with_a_single_newline(self) -> None:
        markdown = self.convert("<p>Tekst</p><p><a href='/x'></a></p>")

        self.assertTrue(markdown.endswith("Tekst\n"), repr(markdown[-20:]))

    def test_stk_label_followed_by_its_period_is_not_split(self) -> None:
        markdown = self.convert("<div><em>&nbsp; &nbsp;Stk. 2</em>. Oppustelige hoppepuder.</div>")

        self.assertIn("*Stk. 2.* Oppustelige hoppepuder.", markdown)

    def test_emphasis_closing_after_a_non_breaking_space_closes(self) -> None:
        markdown = self.convert("<p><strong><em>konstruktionsklasse 2-4.&nbsp; </em></strong>Mere</p>")

        self.assertIn("***konstruktionsklasse 2-4.***", markdown)


if __name__ == "__main__":
    unittest.main()
