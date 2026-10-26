from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "link_references.py"
ELI = "https://www.retsinformation.dk/eli/lta"

KRAV_1 = """# Administrative bestemmelser (§ 1 - § 47)

## § 1 - § 3 Anvendelsesområde {#g1}

### § 1 {#paragraf-1}

### § 4 {#paragraf-4}

### § 5 {#paragraf-5}

### § 6 {#paragraf-6}

### § 6 f {#paragraf-6f}

### § 6 i {#paragraf-6i}

### § 12 {#paragraf-12}

### § 13 {#paragraf-13}

### § 14 {#paragraf-14}

### § 22 {#paragraf-22}

### § 28 {#paragraf-28}

### § 30 a {#paragraf-30a}

### § 39 {#paragraf-39}

"""

KRAV_5 = """# Brand (§ 82 - § 158)

## § 105 - § 110 Flugtveje {#g105}

### § 105 {#paragraf-105}

### § 107 {#paragraf-107}

## § 126 - § 133 Brandsektioner {#g126}

### § 126 {#paragraf-126}

### § 133 {#paragraf-133}

"""

KRAV_30 = """# Kontrol (§ 489 - § 551)

### § 489 {#paragraf-489}

### § 507 {#paragraf-507}

### § 544 {#paragraf-544}

### § 551 {#paragraf-551}

"""

KRAV_35 = """# Anerkendelse af statikere (§ 552 - § 563)

## § 552 - § 563 Anerkendelse af statikere {#g552}

### § 552 {#paragraf-552}

### § 561 {#paragraf-561}

Tekst til § 561 og § 562.

### § 563 {#paragraf-563}

"""

KRAV_13 = """# Eksisterende bygninger (§ 345 - § 351)

## § 345 Generelt {#g345}

### § 351 {#paragraf-351}

"""

BILAG_3 = """# Bilag 3: Tabeller

## Tabel 4b – Mindstekrav til kontrol {#t4b}

Tekst.
"""

LAWS = f"""[laws.byggeloven]
title = "Byggeloven"
names = ["byggeloven"]
eli = "{ELI}/2016/1178"
ids = ["P2", "P6D", "P25", "P28"]

[laws.certificeringsbekendtgoerelsen]
title = "Certificeringsbekendtgørelsen"
names = ["certificeringsbekendtgørelsen", "bekendtgørelse om certificeringsordninger for dokumentation af tekniske forhold i bygningsreglementet"]
eli = "{ELI}/2023/1693"
ids = ["P12", "P13", "P14", "P38"]

[laws.ladestanderbekendtgoerelsen]
title = "Ladestanderbekendtgørelsen"
names = ["ladestanderbekendtgørelsen"]
eli = "{ELI}/2020/181"
ids = ["P5"]
"""

SCOPE = """[scope]
"administrative-bestemmelser/brv/" = "br18"
"vejledninger/ladestander/" = "ladestanderbekendtgoerelsen"
"vejledninger/byggeloven-6-d/" = "byggeloven"
"vejledninger/certificering/" = "certificeringsbekendtgoerelsen"
"""

GUIDE = "administrative-bestemmelser/brv/gebyr"


class LinkReferencesTest(unittest.TestCase):
    def setUp(self) -> None:
        self.root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.root)
        self.docs = self.root / "docs"
        self.data = self.root / "data"
        self.data.mkdir()
        (self.data / "xref-laws.toml").write_text(LAWS, encoding="utf-8")
        (self.data / "xref-page-scope.toml").write_text(SCOPE, encoding="utf-8")
        (self.data / "xref-overrides.toml").write_text("", encoding="utf-8")
        for rel, text in {
            "administrative-bestemmelser/krav": KRAV_1,
            "tekniske-bestemmelser/05/krav": KRAV_5,
            "tekniske-bestemmelser/13/krav": KRAV_13,
            "ovrige-bestemmelser/30/krav": KRAV_30,
            "ovrige-bestemmelser/35/krav": KRAV_35,
            "bilag/b3/bilag_3": BILAG_3,
        }.items():
            self.doc(rel, text)

    def doc(self, rel: str, text: str) -> None:
        (self.docs / rel).mkdir(parents=True, exist_ok=True)
        (self.docs / rel / "index.md").write_text(text, encoding="utf-8")

    def read(self, rel: str) -> str:
        return (self.docs / rel / "index.md").read_text(encoding="utf-8")

    def run_script(self) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--docs-root", str(self.docs), "--data-dir", str(self.data)],
            capture_output=True,
            text=True,
        )

    def link(self, text: str, page: str = GUIDE) -> str:
        self.doc(page, f"# Side\n\n{text}\n")
        result = self.run_script()
        self.assertEqual(result.returncode, 0, result.stderr)
        return self.read(page).split("\n\n", 1)[1].rstrip("\n")

    def unresolved(self) -> str:
        return (self.data / "xref-unresolved.tsv").read_text(encoding="utf-8")

    # BR18 paragraphs

    def test_paragraph_in_regulation_text_links_to_its_heading_on_the_same_page(self) -> None:
        self.doc("administrative-bestemmelser/krav", KRAV_1 + "Se § 39.\n")
        self.assertEqual(self.run_script().returncode, 0)
        self.assertIn('Se [§ 39](#paragraf-39 "BR18 § 39"){ .br18-ref }.', self.read("administrative-bestemmelser/krav"))

    def test_paragraph_in_a_br18_guide_links_to_the_chapter_page_relative_to_the_guide(self) -> None:
        self.assertEqual(self.link("jf. § 39"), 'jf. [§ 39](../../krav/#paragraf-39 "BR18 § 39"){ .br18-ref }')

    def test_paragraph_of_another_chapter_links_to_that_chapter(self) -> None:
        self.doc("administrative-bestemmelser/krav", KRAV_1 + "Se § 126.\n")
        self.run_script()
        self.assertIn('[§ 126](../../tekniske-bestemmelser/05/krav/#paragraf-126 "BR18 § 126"){ .br18-ref }', self.read("administrative-bestemmelser/krav"))

    def test_stk_nr_and_litra_stay_in_the_link_text_and_target_the_paragraph(self) -> None:
        self.assertEqual(
            self.link("jf. § 22, stk. 2, nr. 3, litra a, og mere"),
            'jf. [§ 22, stk. 2, nr. 3, litra a](../../krav/#paragraf-22 "BR18 § 22"){ .br18-ref }, og mere',
        )

    def test_section_letter_is_not_taken_from_the_next_word(self) -> None:
        self.assertEqual(self.link("Efter § 22 dispenseres der."), 'Efter [§ 22](../../krav/#paragraf-22 "BR18 § 22"){ .br18-ref } dispenseres der.')

    def test_spaced_section_letter_counts_when_the_paragraph_exists(self) -> None:
        self.assertEqual(self.link("jf. § 30 a, stk. 3."), 'jf. [§ 30 a, stk. 3](../../krav/#paragraf-30a "BR18 § 30a"){ .br18-ref }.')

    def test_letter_that_is_a_word_is_left_outside_the_link(self) -> None:
        self.assertEqual(
            self.link("efter § 6 i bygningsreglementet"),
            'efter [§ 6](../../krav/#paragraf-6 "BR18 § 6"){ .br18-ref } i bygningsreglementet',
        )

    def test_range_equal_to_a_group_heading_links_to_the_group_and_keeps_the_next_word(self) -> None:
        self.assertEqual(
            self.link("jf. §§ 126-133 vedrørende brand"),
            'jf. [§§ 126-133](../../../tekniske-bestemmelser/05/krav/#g126 "BR18 §§ 126-133"){ .br18-ref } vedrørende brand',
        )

    def test_other_range_links_to_its_first_paragraph_and_ends_at_its_last_number(self) -> None:
        self.assertEqual(
            self.link("§§ 105-107 i forhold til"),
            '[§§ 105-107](../../../tekniske-bestemmelser/05/krav/#paragraf-105 "BR18 §§ 105-107"){ .br18-ref } i forhold til',
        )

    def test_ranges_are_never_cut_short(self) -> None:
        linked = self.link("§ 345-351, § 489, stk. 2-4 og § 507, stk.1, nr. 5-8.")
        self.assertIn('[§ 345-351](', linked)
        self.assertIn('"BR18 §§ 345-351"){ .br18-ref }, ', linked)
        self.assertIn('[§ 489, stk. 2-4](', linked)
        self.assertIn('[§ 507, stk.1, nr. 5-8](', linked)
        self.assertNotIn("){ .br18-ref }-", linked)

    def test_paragraph_without_own_heading_links_to_the_group_heading_that_covers_it(self) -> None:
        self.assertEqual(self.link("jf. § 562"), 'jf. [§ 562](../../../ovrige-bestemmelser/35/krav/#g552 "BR18 § 562"){ .br18-ref }')

    def test_list_gets_one_link_per_number(self) -> None:
        self.assertEqual(
            self.link("§§ 4 og 5 samt § 12, § 13 eller § 14."),
            '[§§ 4](../../krav/#paragraf-4 "BR18 § 4"){ .br18-ref } og [5](../../krav/#paragraf-5 "BR18 § 5"){ .br18-ref } samt '
            '[§ 12](../../krav/#paragraf-12 "BR18 § 12"){ .br18-ref }, [§ 13](../../krav/#paragraf-13 "BR18 § 13"){ .br18-ref } '
            'eller [§ 14](../../krav/#paragraf-14 "BR18 § 14"){ .br18-ref }.',
        )

    def test_range_of_lettered_paragraphs_ends_at_the_letter(self) -> None:
        self.assertEqual(
            self.link("omfattet af §§ 6 f - 6 i skal"),
            'omfattet af [§§ 6 f - 6 i](../../krav/#paragraf-6f "BR18 §§ 6f-6i"){ .br18-ref } skal',
        )

    def test_ordinary_words_after_a_reference_are_not_an_instrument(self) -> None:
        linked = self.link("at § 39 og § 22 til en hver tid er overholdt, og § 4, i en afstand")
        self.assertEqual(linked.count("{ .br18-ref }"), 3)

    def test_double_sign_list_with_stk_lists_is_ambiguous(self) -> None:
        text = "jf. byggelovens §§ 6, stk. 3, 7, stk. 2, 12, 14, 18 og 18 A."
        self.assertEqual(self.link(text), text)
        self.assertIn("ambiguous", self.unresolved())

    def test_second_stk_joined_by_og_stays_in_the_link(self) -> None:
        self.assertEqual(self.link("omfattet af § 5, stk. 1 og stk. 2."), 'omfattet af [§ 5, stk. 1 og stk. 2](../../krav/#paragraf-5 "BR18 § 5"){ .br18-ref }.')

    def test_number_that_is_not_a_br18_paragraph_is_unlinked_and_listed(self) -> None:
        self.assertEqual(self.link("jf. § 999."), "jf. § 999.")
        self.assertIn(f"{GUIDE}/index.md\t§ 999\t", self.unresolved())

    def test_decimal_section_number_is_not_a_paragraph(self) -> None:
        self.assertEqual(self.link("se § 5.3 i vejledningen"), "se § 5.3 i vejledningen")

    # Scope: which law

    def test_explicit_br18_overrides_the_page_default_across_a_list(self) -> None:
        self.assertEqual(
            self.link("jf. BR18, § 544, stk. 3 eller § 551, stk. 3", page="vejledninger/certificering"),
            'jf. BR18, [§ 544, stk. 3](../../ovrige-bestemmelser/30/krav/#paragraf-544 "BR18 § 544"){ .br18-ref } eller '
            '[§ 551, stk. 3](../../ovrige-bestemmelser/30/krav/#paragraf-551 "BR18 § 551"){ .br18-ref }',
        )

    def test_postfix_instrument_applies_to_the_whole_list(self) -> None:
        linked = self.link(
            "efter § 12, § 13 eller § 14 i bekendtgørelse om certificeringsordninger for dokumentation af tekniske forhold i bygningsreglementet",
            page="administrative-bestemmelser/krav/sub",
        )
        self.assertNotIn("#paragraf-", linked)
        self.assertIn(f'[§ 14]({ELI}/2023/1693#P14 "Certificeringsbekendtgørelsen § 14"){{ .br18-ref .br18-ref--ext }}', linked)

    def test_postfix_instrument_after_a_single_paragraph(self) -> None:
        linked = self.link("jf. § 14 i bekendtgørelse om certificeringsordninger for dokumentation af tekniske forhold i bygningsreglementet")
        self.assertIn(f"({ELI}/2023/1693#P14 ", linked)

    def test_genitive_law_name_links_to_that_law_on_retsinformation(self) -> None:
        self.assertEqual(
            self.link("jf. byggelovens § 25, stk. 1."),
            f'jf. byggelovens [§ 25, stk. 1]({ELI}/2016/1178#P25 "Byggeloven § 25"){{ .br18-ref .br18-ref--ext }}.',
        )

    def test_a_following_jf_citation_does_not_rescope_the_reference(self) -> None:
        linked = self.link("i strid med byggelovens § 25, jf. byggelovens § 28.")
        self.assertIn(f"({ELI}/2016/1178#P25 ", linked)
        self.assertIn(f"({ELI}/2016/1178#P28 ", linked)

    def test_footnote_marker_between_law_name_and_paragraph(self) -> None:
        linked = self.link("Byggelovens^1^ § 28, stk. 1 gælder.")
        self.assertIn(f"({ELI}/2016/1178#P28 ", linked)
        self.assertNotIn("paragraf-28", linked)

    def test_law_name_before_paragraph(self) -> None:
        linked = self.link("jf. certificeringsbekendtgørelsen § 38.")
        self.assertIn(f'[§ 38]({ELI}/2023/1693#P38 "Certificeringsbekendtgørelsen § 38")', linked)

    def test_unknown_instrument_is_never_br18(self) -> None:
        for text in (
            "parkeringsfondscirkulærets § 5, stk. 1",
            "jf. cirkulærets § 6",
            "museumslovens § 24",
            "lov om etablering og fælles udnyttelse af master til radiokommunikationsformål m.v. § 1, stk. 4, nr. 2",
            "beredskabslovens § 12, stk. 1",
            "som defineret i affaldsbekendtgørelsen[\\[1\\]](#_ftn1){#_ftnref1} § 2.",
        ):
            with self.subTest(text=text):
                self.assertEqual(self.link(text, page="administrative-bestemmelser/krav/sub"), text)
                self.assertIn("instrument not in xref-laws.toml", self.unresolved())

    def test_paragraph_missing_from_the_current_law_is_unlinked(self) -> None:
        self.assertEqual(self.link("jf. byggelovens § 99"), "jf. byggelovens § 99")
        self.assertIn("§ 99", self.unresolved())

    def test_uppercase_letter_is_byggeloven_style_never_br18(self) -> None:
        self.assertEqual(self.link("jf. § 6 D, stk. 2"), "jf. § 6 D, stk. 2")
        self.assertEqual(
            self.link("jf. § 6 D, stk. 2", page="vejledninger/byggeloven-6-d/sub"),
            f'jf. [§ 6 D, stk. 2]({ELI}/2016/1178#P6D "Byggeloven § 6D"){{ .br18-ref .br18-ref--ext }}',
        )

    def test_page_default_law_for_a_guide_about_another_instrument(self) -> None:
        self.assertEqual(
            self.link("omfattet af § 5, stk. 1", page="vejledninger/ladestander/blandet"),
            f'omfattet af [§ 5, stk. 1]({ELI}/2020/181#P5 "Ladestanderbekendtgørelsen § 5"){{ .br18-ref .br18-ref--ext }}',
        )

    def test_page_without_a_default_leaves_implicit_paragraphs_unlinked(self) -> None:
        self.assertEqual(self.link("jf. § 5", page="vejledninger/ukendt"), "jf. § 5")
        self.assertIn("vejledninger/ukendt/index.md\t§ 5\t", self.unresolved())

    def test_conflicting_scope_signals_leave_the_reference_unlinked(self) -> None:
        self.assertEqual(self.link("BR18, § 5 i byggeloven"), "BR18, § 5 i byggeloven")

    # Chapters and annexes

    def test_chapter_in_regulation_text_links_to_the_chapter_page(self) -> None:
        self.assertEqual(
            self.link("jf. kapitel 5 om brand", page="administrative-bestemmelser/krav/sub"),
            'jf. [kapitel 5](../../../tekniske-bestemmelser/05/krav/ "BR18 kapitel 5"){ .br18-ref } om brand',
        )

    def test_chapter_references_that_are_not_br18_chapters(self) -> None:
        for text in (
            "Budget- og Regnskabssystem for Kommuner, særligt kap. 9.3",
            "Bygningsreglementets vejledning til kapitel 5 – Brand",
            "kapitel 3 i Energistyrelsens bekendtgørelse",
            "miljøbeskyttelseslovens kapitel 3",
        ):
            with self.subTest(text=text):
                self.assertEqual(self.link(text, page="administrative-bestemmelser/krav/sub"), text)

    def test_chapter_in_a_guide_is_linked_only_when_br18_is_named(self) -> None:
        self.assertEqual(self.link("se kapitel 5"), "se kapitel 5")
        self.assertEqual(self.link("se BR18 kapitel 5"), 'se BR18 [kapitel 5](../../../tekniske-bestemmelser/05/krav/ "BR18 kapitel 5"){ .br18-ref }')

    def test_chapter_in_a_guide_is_linked_when_the_text_names_its_title(self) -> None:
        self.assertEqual(self.link("jf. kap. 5 om brand"), 'jf. [kap. 5](../../../tekniske-bestemmelser/05/krav/ "BR18 kapitel 5"){ .br18-ref } om brand')
        self.assertEqual(self.link("Kapitel 5: Brand"), '[Kapitel 5](../../../tekniske-bestemmelser/05/krav/ "BR18 kapitel 5"){ .br18-ref }: Brand')
        (self.data / "xref-unresolved.tsv").unlink()
        self.assertEqual(self.link("kapitel 5 om kommuneplanlægning"), "kapitel 5 om kommuneplanlægning")

    def test_chapter_list_gets_one_link_per_number(self) -> None:
        self.assertEqual(
            self.link("jf. kapitel 5 og 1.", page="ovrige-bestemmelser/30/krav"),
            'jf. [kapitel 5](../../../tekniske-bestemmelser/05/krav/ "BR18 kapitel 5"){ .br18-ref } og '
            '[1](../../../administrative-bestemmelser/krav/ "BR18 kapitel 1"){ .br18-ref }.',
        )

    def test_chapter_range_links_its_first_chapter_and_is_never_cut_short(self) -> None:
        self.assertEqual(
            self.link("jf. kapitel 1-5, og mere", page="ovrige-bestemmelser/30/krav"),
            'jf. [kapitel 1-5](../../../administrative-bestemmelser/krav/ "BR18 kapitel 1-5"){ .br18-ref }, og mere',
        )

    def test_table_list_gets_one_link_per_table_and_unknown_items_leave_it_unlinked(self) -> None:
        self.assertEqual(
            self.link("jf. bilag 3, tabel 4b og 4b.", page="ovrige-bestemmelser/30/krav"),
            'jf. [bilag 3, tabel 4b](../../../bilag/b3/bilag_3/#t4b "BR18 bilag 3, tabel 4b"){ .br18-ref } og '
            '[4b](../../../bilag/b3/bilag_3/#t4b "BR18 bilag 3, tabel 4b"){ .br18-ref }.',
        )
        (self.data / "xref-unresolved.tsv").unlink()
        for text in ("jf. kapitel 5 og 44", "jf. bilag 3, tabel 4b og 5.", "i bilag 1-10 til vejledningen"):
            with self.subTest(text=text):
                self.assertEqual(self.link(text, page="ovrige-bestemmelser/30/krav"), text)

    def test_annex_table_links_to_the_table_heading(self) -> None:
        self.assertEqual(
            self.link("jf. bilag 3, tabel 4b.", page="ovrige-bestemmelser/30/krav"),
            'jf. [bilag 3, tabel 4b](../../../bilag/b3/bilag_3/#t4b "BR18 bilag 3, tabel 4b"){ .br18-ref }.',
        )

    def test_annex_of_another_instrument_is_not_linked(self) -> None:
        text = "jf. bilag 1 til bekendtgørelse om kommunernes budget"
        self.assertEqual(self.link(text, page="ovrige-bestemmelser/30/krav"), text)

    # Markdown safety

    def test_headings_existing_links_and_code_are_never_touched(self) -> None:
        text = "### § 39 {#paragraf-39}\n\nSe [§ 39](../x/) og `§ 39` og <a href=\"y\">§ 39</a>.\n\n## § 1 - § 3 Titel"
        self.assertEqual(self.link(text), text)

    def test_raw_html_block_gets_an_html_link(self) -> None:
        linked = self.link("<table>\n<tr>\n<td> § 39, § 22</td>\n</tr>\n</table>")
        self.assertIn('<td> <a class="br18-ref" href="../../krav/#paragraf-39" title="BR18 § 39">§ 39</a>, ', linked)
        self.assertNotIn("](", linked)

    def test_second_run_is_a_no_op(self) -> None:
        self.link("jf. § 39, byggelovens § 25 og kapitel 5.")
        before = self.read(GUIDE)
        self.assertEqual(self.run_script().returncode, 0)
        self.assertEqual(self.read(GUIDE), before)

    # Overrides and the unresolved report

    def test_override_decides_an_ambiguous_reference(self) -> None:
        (self.data / "xref-overrides.toml").write_text(
            '[[override]]\npage = "vejledninger/ukendt/index.md"\ntext = "§ 5"\nlaw = "br18"\nreason = "Guide om BR18."\n', encoding="utf-8"
        )
        self.assertEqual(self.link("jf. § 5", page="vejledninger/ukendt"), 'jf. [§ 5](../../administrative-bestemmelser/krav/#paragraf-5 "BR18 § 5"){ .br18-ref }')

    def test_stale_override_fails_the_run(self) -> None:
        (self.data / "xref-overrides.toml").write_text(
            '[[override]]\npage = "vejledninger/ukendt/index.md"\ntext = "§ 7"\nlaw = "skip"\nreason = "x"\n', encoding="utf-8"
        )
        self.doc("vejledninger/ukendt", "# Side\n\njf. § 5\n")
        result = self.run_script()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("§ 7", result.stderr)

    def test_unresolved_count_may_not_grow(self) -> None:
        self.link("jf. § 999.")
        self.doc("vejledninger/ukendt", "# Side\n\njf. § 998\n")
        result = self.run_script()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("§ 998", result.stderr)
        self.assertNotIn("§ 998", self.unresolved())


if __name__ == "__main__":
    unittest.main()
