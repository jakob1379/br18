from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "convert_br18_docs.py"


class ConvertTest(unittest.TestCase):
    def convert(self, body: str, title: str = "BR18") -> str:
        root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, root)
        (root / "side").mkdir()
        (root / "side" / "index.html").write_text(
            f"<html><head><title>{title}</title></head><body><main>{body}</main></body></html>", encoding="utf-8"
        )
        subprocess.run([sys.executable, str(SCRIPT), "--docs-root", str(root)], check=True, capture_output=True)
        return (root / "side" / "index.md").read_text(encoding="utf-8")

    def test_page_title_is_the_origin_page_title(self) -> None:
        markdown = self.convert("<h1>Andre vejledninger</h1><p>Tekst.</p>", "Spørgsmål og svar: certificering | BR18")

        self.assertTrue(markdown.startswith('---\ntitle: "Spørgsmål og svar: certificering"\n---\n\n# Andre vejledninger\n'), markdown)

    def test_page_without_its_own_origin_title_is_titled_by_its_heading(self) -> None:
        markdown = self.convert("<h1>Adgangsforhold (§ 48 - § 62)</h1><p>Tekst.</p>")

        self.assertTrue(markdown.startswith('---\ntitle: "Adgangsforhold (§ 48 - § 62)"\n---\n\n'), markdown)

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

    def test_line_break_after_whitespace_and_emphasis_openers_moves_before_them(self) -> None:
        markdown = self.convert(
            "<p>Tekst.</p><strong>\n<em><strong><br>\nBestemmelser i lokalplan<br>\n</strong></em><strong><br>\n</strong>\n</strong>"
        )

        self.assertIn("***Bestemmelser i lokalplan***", markdown)
        self.assertNotRegex(markdown, r"(?m)^\*\*\\?$")

    def test_emphasised_multiplication_sign_is_plain(self) -> None:
        markdown = self.convert("<p>(B6 / (A<sub><em>opv</em></sub> <em>*</em> 50 år)) og 25 pct. <em>*</em> A</p>")

        self.assertIn("(B6 / (A~*opv*~ \\* 50 år)) og 25 pct. \\* A", markdown)

    def test_line_breaks_at_the_edges_of_a_link_move_out_of_it(self) -> None:
        markdown = self.convert(
            '<p>findes her:&nbsp;<a href="https://ens.dk/x" target="_blank">Energistyrelsens oversigt&nbsp;<br>\n</a>'
            "<br><em>Relevante standarder</em></p>"
            '<p>Bilag 11e (Ophævet)&nbsp;<a href="/media/m/b.pdf" title="B"><br>\n</a>&nbsp;</p>'
        )

        self.assertIn('[Energistyrelsens oversigt](https://ens.dk/x){target="_blank"}', markdown)
        self.assertIn('[](../media/m/b.pdf "B")', markdown)
        self.assertNotRegex(markdown, r"(?m)^\]")

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

    def test_show_all_links_point_at_the_page_that_holds_the_show_all_content(self) -> None:
        markdown = self.convert('<p>Se <a href="/ovrige-bestemmelser/23/krav/?Layout=ShowAll">kapitel 23</a>.</p>')

        self.assertIn("[kapitel 23](../ovrige-bestemmelser/23/krav/)", markdown)

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

    def test_text_after_an_empty_link_is_kept(self) -> None:
        markdown = self.convert('<p><a href="/media/x/b4.pdf" title="Bilag 4"></a>Version 1.0 (21.12.2018)</p>')

        self.assertIn('[](../media/x/b4.pdf "Bilag 4")Version 1.0 (21.12.2018)', markdown)

    def test_links_to_the_origins_internal_cms_host_are_dropped(self) -> None:
        markdown = self.convert(
            '<p><a rel="noopener" href="https://tbstsc.dev.local/-/media/71F0.ashx" target="_blank">Åbn r</a>'
            '<a rel="noopener" href="/media/y/r.pdf" target="_blank">ettelsesblad (Nyt vindue).</a></p>'
            '<p>Tekst.<a id="_anchor_1" href="https://tbstsc.dev.local/#_msocom_1"></a></p>'
        )

        self.assertNotIn("dev.local", markdown)
        self.assertIn('[Åbn rettelsesblad (Nyt vindue).](../media/y/r.pdf){rel="noopener" target="_blank"}', markdown)
        self.assertIn("Tekst.\n", markdown)

    def test_parenthesised_numbers_and_lettered_paragraphs_stay_in_their_sentence(self) -> None:
        markdown = self.convert(
            "<h1>Administrative bestemmelser (§ 1 - § 47)</h1>"
            "<p>Dette fremgår af byggelovens § 16 C, stk. 1. Kommunalbestyrelsen påser også det.</p>"
            "<p>Se byggeret og helhedsvurdering (kapitel 8) samt ubebyggede arealer (jf. § 256, stk. 3) plus det.</p>"
        )

        self.assertIn("# Administrative bestemmelser (§ 1 - § 47)\n", markdown)
        self.assertIn("Dette fremgår af byggelovens § 16 C, stk. 1. Kommunalbestyrelsen påser også det.", markdown)
        self.assertIn("(kapitel 8) samt ubebyggede arealer (jf. § 256, stk. 3) plus det.", markdown)

    def test_accordion_trigger_without_a_tag_still_gives_its_heading_the_id(self) -> None:
        markdown = self.convert(
            '<section><a href="/side/tabel_1/#3498d4bb-6317-4085-8a97-18bc8fae2ab3" class="accordion__trigger">'
            '<h3 class="accordion__title">Tabel 1</h3></a><p>Tekst</p></section>'
        )

        self.assertIn("### Tabel 1 {#3498d4bb-6317-4085-8a97-18bc8fae2ab3}", markdown)
        self.assertNotIn("[]", markdown)

    def test_faq_question_trigger_keeps_its_answer_and_leaves_the_next_heading_alone(self) -> None:
        markdown = self.convert(
            '<section id="aa480314-460a-49e3-a01d-ddd6aaa62881"><div class="accordion__header">'
            '<a href="/side/qa_2/#aa480314-460a-49e3-a01d-ddd6aaa62881" class="accordion__trigger">'
            '<div class="accordion__tag">?</div><h3 class="accordion__title">Altaner</h3></a></div>'
            '<div><div class="accordion__header"><a href="#aa480314-460a-49e3-a01d-ddd6aaa62881" class="accordion__trigger">'
            '<div class="accordion__tag">?</div><div class="accordion__title">Betragtes en altan som en enhed?</div></a></div>'
            "<div>Ja, der skal være niveaufri adgang.</div></div></section>"
            '<section id="334bd38a-2759-4aab-8d4a-a3689e0e2c2c"><div class="accordion__header">'
            '<a href="/side/qa_3/#334bd38a-2759-4aab-8d4a-a3689e0e2c2c" class="accordion__trigger">'
            '<div class="accordion__tag">?</div><h3 class="accordion__title">Handicaptoiletter</h3></a></div></section>'
        )

        self.assertIn("### Altaner {#aa480314-460a-49e3-a01d-ddd6aaa62881}", markdown)
        self.assertIn("[? Betragtes en altan som en enhed?](#aa480314-460a-49e3-a01d-ddd6aaa62881) Ja, der skal være", markdown)
        self.assertIn("### Handicaptoiletter {#334bd38a-2759-4aab-8d4a-a3689e0e2c2c}", markdown)

    def test_footnote_reference_link_keeps_its_brackets(self) -> None:
        markdown = self.convert('<p>som defineret i affaldsbekendtgørelsen<a href="#_ftn1">[1]</a> og [a] her.</p>')

        self.assertIn("affaldsbekendtgørelsen[\\[1\\]](#_ftn1) og \\[a\\] her.", markdown)

    def test_unresolved_cms_local_links_are_dropped(self) -> None:
        markdown = self.convert(
            '<p>som beskrevet i <em><a href="/{localLink:umb:/media/faf2ae2c}økkenerberegnes.%3C/p%3E%3Caname=">'
            "</a>Forudsætninger vedr. beregning</em> og <a href='{localLink:umb://document/abc}'>Bilag 6</a>.</p>"
        )

        self.assertNotIn("ocal", markdown.lower().replace("localt", ""))
        self.assertIn("som beskrevet i *Forudsætninger vedr. beregning* og Bilag 6.", markdown)

    def test_empty_link_to_a_fragment_of_the_page_is_dropped(self) -> None:
        markdown = self.convert('<a href="#Indholdsoversigt" class="accordion__trigger"><svg></svg></a><p>Tekst</p>')

        self.assertEqual(markdown, '---\ntitle: "BR18"\n---\n\nTekst\n')

    def test_paragraph_tag_of_an_accordion_row_becomes_its_heading(self) -> None:
        markdown = self.convert(
            '<h1>Brand (§ 82 - § 158)</h1>'
            '<div class="accordion__row"><div class="accordion__tag">§ 100</div><div class="accordion__content">'
            "<div>Brandmodstandsevnen bestemmes.</div><div><em>Stk. 2.</em> Det fulde brandforløb.</div></div></div>"
            '<div class="accordion__row"><div class="accordion__tag">§ 101</div><div class="accordion__content">'
            "<div>§ 100 kan fraviges, hvis det sikres.</div></div></div>"
        )

        self.assertIn("*Stk. 2.* Det fulde brandforløb.\n\n### § 101 {#paragraf-101}\n\n§ 100 kan fraviges", markdown)

    def test_empty_headings_are_dropped(self) -> None:
        markdown = self.convert("<p>Standarder:</p><h4><br></h4><p>DS/CEN/TR 16879:2016</p><h4>&nbsp;</h4><h4>Køb standarden</h4>")

        self.assertEqual(markdown, '---\ntitle: "BR18"\n---\n\nStandarder:\n\nDS/CEN/TR 16879:2016\n\n#### Køb standarden\n')

    def test_page_ends_with_a_single_newline(self) -> None:
        markdown = self.convert("<p>Tekst</p><div><span>&nbsp;</span></div><div></div>")

        self.assertTrue(markdown.endswith("Tekst\n"), repr(markdown[-20:]))

    def test_stk_label_followed_by_its_period_is_not_split(self) -> None:
        markdown = self.convert("<div><em>&nbsp; &nbsp;Stk. 2</em>. Oppustelige hoppepuder.</div>")

        self.assertIn("*Stk. 2.* Oppustelige hoppepuder.", markdown)

    def test_emphasis_closing_after_a_non_breaking_space_closes(self) -> None:
        markdown = self.convert("<p><strong><em>konstruktionsklasse 2-4.&nbsp; </em></strong>Mere</p>")

        self.assertIn("***konstruktionsklasse 2-4.***", markdown)


if __name__ == "__main__":
    unittest.main()
