from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "check_references.py"
ELI = "https://www.retsinformation.dk/eli/lta"

LAWS = f"""[laws.byggeloven]
title = "Byggeloven"
names = ["byggeloven"]
eli = "{ELI}/2016/1178"
ids = ["P25", "P6D"]
"""

KRAV_5 = """<h1 id="brand">Brand (§ 82 - § 158)</h1>
<h2 id="g126">§ 126 - § 133 Brandsektioner</h2>
<h3 id="paragraf-126">§ 126</h3>
<h3 id="paragraf-127">§ 127</h3>
"""

BILAG_3 = '<h1 id="b">Bilag 3: Tabeller</h1><h2 id="t4a">Tabel 4a – Kontrol</h2><h2 id="t4b">Tabel 4b – Kontrol</h2>'


def page(article: str) -> str:
    return f'<html><body><nav><a href="x">§ 1</a></nav><article class="md-content__inner md-typeset">{article}</article></body></html>'


def ref(href: str, title: str, text: str, ext: bool = False) -> str:
    cls = "br18-ref br18-ref--ext" if ext else "br18-ref"
    return f'<p>Se <a class="{cls}" href="{href}" title="{title}">{text}</a>.</p>'


class CheckReferencesTest(unittest.TestCase):
    def setUp(self) -> None:
        self.root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.root)
        self.site = self.root / "site"
        (self.root / "xref-laws.toml").write_text(LAWS, encoding="utf-8")
        self.html("tekniske-bestemmelser/05/krav", KRAV_5)
        self.html("bilag/b3/bilag_3", BILAG_3)

    def html(self, rel: str, article: str) -> None:
        (self.site / rel).mkdir(parents=True, exist_ok=True)
        (self.site / rel / "index.html").write_text(page(article), encoding="utf-8")

    def check(self, article: str, *extra: str) -> subprocess.CompletedProcess[str]:
        self.html("tekniske-bestemmelser/05/brv", article)
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--site-dir", str(self.site), "--laws", str(self.root / "xref-laws.toml"), *extra],
            capture_output=True,
            text=True,
        )

    def assert_ok(self, article: str) -> None:
        result = self.check(article)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def assert_flagged(self, article: str) -> None:
        result = self.check(article)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("tekniske-bestemmelser/05/brv", result.stdout + result.stderr)

    def test_paragraph_link_to_its_heading_passes(self) -> None:
        self.assert_ok(ref("../krav/#paragraf-126", "BR18 § 126", "§ 126, stk. 2"))

    def test_paragraph_link_to_another_heading_is_flagged(self) -> None:
        self.assert_flagged(ref("../krav/#paragraf-127", "BR18 § 126", "§ 126"))

    def test_link_text_must_name_the_referenced_number(self) -> None:
        self.assert_flagged(ref("../krav/#paragraf-126", "BR18 § 126", "§ 127"))

    def test_group_heading_covers_paragraphs_and_ranges_inside_it(self) -> None:
        self.assert_ok(ref("../krav/#g126", "BR18 § 130", "§ 130"))
        self.assert_ok(ref("../krav/#g126", "BR18 §§ 126-133", "§§ 126-133"))

    def test_group_heading_does_not_cover_paragraphs_outside_it(self) -> None:
        self.assert_flagged(ref("../krav/#g126", "BR18 § 134", "§ 134"))

    def test_range_link_must_land_on_the_start_of_the_range(self) -> None:
        self.assert_ok(ref("../krav/#paragraf-126", "BR18 §§ 126-127", "§§ 126-127"))
        self.assert_flagged(ref("../krav/#paragraf-127", "BR18 §§ 126-127", "§§ 126-127"))

    def test_chapter_link_must_land_on_that_chapters_page(self) -> None:
        self.assert_ok(ref("../krav/", "BR18 kapitel 5", "kapitel 5"))
        self.assert_flagged(ref("../krav/", "BR18 kapitel 6", "kapitel 6"))

    def test_whole_chapter_range_may_link_the_chapter_page(self) -> None:
        self.assert_ok(ref("../krav/", "BR18 §§ 82-158", "§§ 82-158"))

    def test_annex_table_link_must_land_on_that_table(self) -> None:
        self.assert_ok(ref("../../../bilag/b3/bilag_3/#t4b", "BR18 bilag 3, tabel 4b", "bilag 3, tabel 4b"))
        self.assert_flagged(ref("../../../bilag/b3/bilag_3/#t4a", "BR18 bilag 3, tabel 4b", "bilag 3, tabel 4b"))

    def test_missing_page_or_anchor_is_flagged(self) -> None:
        self.assert_flagged(ref("../krav/#paragraf-999", "BR18 § 999", "§ 999"))
        self.assert_flagged(ref("../../06/krav/#paragraf-160", "BR18 § 160", "§ 160"))

    def test_external_link_must_use_a_cached_fragment_of_a_listed_law(self) -> None:
        self.assert_ok(ref(f"{ELI}/2016/1178#P25", "Byggeloven § 25", "§ 25, stk. 1", ext=True))
        self.assert_flagged(ref(f"{ELI}/2016/1178#P26", "Byggeloven § 26", "§ 26", ext=True))
        self.assert_flagged(ref(f"{ELI}/2019/674#P25", "Byggeloven § 25", "§ 25", ext=True))

    def test_markdown_link_syntax_shown_as_text_is_flagged(self) -> None:
        self.assert_flagged('<p>Se [§ 126](../krav/#paragraf-126 "BR18 § 126"){ .br18-ref }.</p>')


class LawStatusTest(unittest.TestCase):
    def serve(self, historical: bool) -> str:
        record = [{"isHistorical": historical, "shortName": "LBK nr 1178 af 23/09/2016", "documentHtml": '<p id="P25">§ 25</p><p id="P6D">§ 6 D</p>'}]

        class Handler(BaseHTTPRequestHandler):
            def do_POST(self) -> None:
                self.rfile.read(int(self.headers.get("Content-Length", 0)))
                body = json.dumps(record).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, *args: object) -> None:
                pass

        server = HTTPServer(("127.0.0.1", 0), Handler)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        self.addCleanup(server.shutdown)
        return f"http://127.0.0.1:{server.server_port}/api/document"

    def run_check(self, historical: bool) -> subprocess.CompletedProcess[str]:
        root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, root)
        (root / "xref-laws.toml").write_text(LAWS, encoding="utf-8")
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--laws", str(root / "xref-laws.toml"), "--laws-online", "--api", self.serve(historical), "--delay", "0"],
            capture_output=True,
            text=True,
        )

    def test_current_law_passes(self) -> None:
        result = self.run_check(historical=False)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_historical_law_is_flagged(self) -> None:
        result = self.run_check(historical=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn("byggeloven", result.stdout + result.stderr)
        self.assertIn("historical", result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
