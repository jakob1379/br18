from __future__ import annotations

import subprocess
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "audit_br18_parity.py"


def origin_page(body: str, links: str = "") -> str:
    return f"""<!doctype html><html><head><title>t</title></head><body>
<div class="cookie-button">Vi bruger cookies</div>
<header><a href="/">Forside</a>{links}</header>
<main>
<nav class="nav-alphabet"><a href="/tekniske-bestemmelser/02/krav/">2</a></nav>
{body}
</main>
<footer>Social- og Boligstyrelsen</footer>
</body></html>"""


def local_page(body: str) -> str:
    return f"""<!doctype html><html><body>
<nav class="md-nav">Navigation</nav>
<article class="md-content__inner md-typeset">
{body}
</article>
<footer class="md-footer">Made with Zensical</footer>
</body></html>"""


class Origin:
    def __init__(self, pages: dict[str, str], redirects: dict[str, str] | None = None) -> None:
        self.pages = pages
        self.redirects = redirects or {}
        self.requests: list[str] = []
        origin = self

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self) -> None:
                origin.requests.append(self.path)
                if self.path in origin.redirects:
                    self.send_response(301)
                    self.send_header("location", origin.redirects[self.path])
                    self.end_headers()
                    return
                body = origin.pages.get(self.path)
                self.send_response(200 if body is not None else 404)
                self.send_header("content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write((body or "not found").encode())

            def log_message(self, *args: object) -> None:
                pass

        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.url = f"http://127.0.0.1:{self.server.server_port}"

    def page_requests(self) -> list[str]:
        return [p for p in self.requests if p in self.pages]

    def close(self) -> None:
        self.server.shutdown()


class Corpus:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.docs = root / "docs"
        self.site = root / "site"
        self.docs.mkdir()
        self.site.mkdir()

    def add(self, rel: str, html: str) -> None:
        doc = self.docs / rel / "index.md" if rel else self.docs / "index.md"
        doc.parent.mkdir(parents=True, exist_ok=True)
        doc.write_text("# page\n", encoding="utf-8")
        built = self.site / rel / "index.html" if rel else self.site / "index.html"
        built.parent.mkdir(parents=True, exist_ok=True)
        built.write_text(html, encoding="utf-8")


class AuditTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp())
        self.corpus = Corpus(self.tmp)
        self.allowlist = self.tmp / "allowlist.toml"
        self.allowlist.write_text("", encoding="utf-8")
        self.report = self.tmp / "report.md"

    def serve(self, pages: dict[str, str], redirects: dict[str, str] | None = None) -> Origin:
        origin = Origin(pages, redirects)
        self.addCleanup(origin.close)
        return origin

    def audit(self, origin: Origin, *extra: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--origin", origin.url,
                "--docs-root", str(self.corpus.docs),
                "--site-dir", str(self.corpus.site),
                "--cache-dir", str(self.tmp / "cache"),
                "--allowlist", str(self.allowlist),
                "--output", str(self.report),
                "--delay", "0",
                *extra,
            ],
            capture_output=True,
            text=True,
            timeout=300,
        )

    def two_page_site(self) -> Origin:
        guides = '<ul><li><a href="/administrative-bestemmelser/brv/">Vejledning om anvendelse</a></li></ul>'
        nav = '<a href="/administrative-bestemmelser/krav/">Admin</a><a href="/tekniske-bestemmelser/02/krav/">Teknik</a>'
        self.corpus.add("", local_page("<h1>Forside</h1><p>Velkommen til reglementet.</p>"))
        self.corpus.add(
            "administrative-bestemmelser",
            local_page(
                '<h1>Anvendelsesområde<a class="headerlink" href="#x">¶</a></h1><p>Reglementet gælder for alt byggeri.</p>'
                f"{guides}"
            ),
        )
        self.corpus.add(
            "tekniske-bestemmelser/02",
            local_page("<h1>Adgangsforhold</h1><p>Bygninger skal have adgangsforhold.</p>"),
        )
        return self.serve(
            {
                "/": origin_page("<h1>Forside</h1><p>Velkommen til reglementet.</p>", nav),
                "/administrative-bestemmelser/krav/": origin_page(
                    f'<h1>Anvendelsesområde</h1><p>Reglementet gælder for alt byggeri.</p><nav class="accordion__nav">{guides}</nav>', nav
                ),
                "/tekniske-bestemmelser/02/krav/": origin_page(
                    "<h1>Adgangsforhold</h1><p>Bygninger skal have adgangsforhold.</p>"
                    "<p>Ramper må højst have en hældning på 1:20.</p>",
                    nav,
                ),
            }
        )

    def test_reports_page_with_known_difference_and_not_matching_page(self) -> None:
        origin = self.two_page_site()

        result = self.audit(origin)

        self.assertEqual(result.returncode, 1, result.stderr)
        report = self.report.read_text(encoding="utf-8")
        self.assertIn("https://www.bygningsreglementet.dk/tekniske-bestemmelser/02/krav/", report)
        self.assertIn("Ramper må højst have en hældning på 1:20.", report)
        self.assertNotIn("https://www.bygningsreglementet.dk/administrative-bestemmelser/krav/", report)
        self.assertNotIn("Vi bruger cookies", report)
        self.assertNotIn("Social- og Boligstyrelsen", report)

    def test_collapsed_page_is_compared_against_its_show_all_view(self) -> None:
        chapter = "/tekniske-bestemmelser/02/krav/"
        show_all = '<section class="accordion__actions"><a href="/tekniske-bestemmelser/02/krav/?Layout=ShowAll" class="link--expand-all">Fold alle ud</a></section>'
        nav = f'<a href="{chapter}">2</a><a href="{chapter}49/">§ 49</a>'
        whole_chapter = local_page(
            "<h2>§ 48</h2><p>Bygninger skal have adgang.</p><h2>§ 49</h2><p>Brugerne skal kunne komme frem.</p>"
        )
        self.corpus.add("", local_page("<p>Forside</p>"))
        self.corpus.add("tekniske-bestemmelser/02", whole_chapter)
        self.corpus.add("tekniske-bestemmelser/02/krav/49", whole_chapter)
        origin = self.serve(
            {
                "/": origin_page("<p>Forside</p>", nav),
                chapter: origin_page(f"{show_all}<h2>§ 48</h2><p>Bygninger skal have adgang.</p><h2>§ 49</h2>", nav),
                f"{chapter}49/": origin_page(
                    f"{show_all}<h2>§ 48</h2><h2>§ 49</h2><p>Brugerne skal kunne komme frem.</p>", nav
                ),
                f"{chapter}?Layout=ShowAll": origin_page(
                    "<h2>§ 48</h2><p>Bygninger skal have adgang.</p><h2>§ 49</h2><p>Brugerne skal kunne komme frem.</p>"
                ),
            }
        )

        result = self.audit(origin)

        self.assertEqual(result.returncode, 0, self.report.read_text(encoding="utf-8"))

    def guide_site(self, root_text: str, subpage_text: str = "<h3>1.0 Indledning</h3><h3>2.0 Ramper</h3><p>Ramper skal være jævne.</p>") -> Origin:
        guide = "/tekniske-bestemmelser/02/vejledninger/guide/"
        sections = "<h3>1.0 Indledning</h3><p>Guiden indleder.</p><h3>2.0 Ramper</h3><p>Ramper skal være jævne.</p>"
        links = f'<a href="{guide}">Guide</a><a href="{guide}ramper/">Ramper</a>'

        def expand(page: str) -> str:
            return f'<section class="accordion__actions"><a href="{page}?Layout=ShowAll" class="link--expand-all">Fold alle ud</a></section>'

        self.corpus.add("", local_page("<p>Forside</p>"))
        self.corpus.add("tekniske-bestemmelser/02/vejledninger/guide", local_page(root_text))
        self.corpus.add(
            "tekniske-bestemmelser/02/vejledninger/guide/ramper",
            local_page(subpage_text),
        )
        return self.serve(
            {
                "/": origin_page("<p>Forside</p>", links),
                guide: origin_page(f"{expand(guide)}<h3>1.0 Indledning</h3><h3>2.0 Ramper</h3>", links),
                f"{guide}?Layout=ShowAll": origin_page(sections),
                f"{guide}ramper/": origin_page(
                    f"{expand(guide + 'ramper/')}<h3>1.0 Indledning</h3><h3>2.0 Ramper</h3><p>Ramper skal være jævne.</p>", links
                ),
                f"{guide}ramper/?Layout=ShowAll": origin_page(sections),
            }
        )

    def test_guide_subpage_is_an_alias_of_a_root_that_covers_the_guide(self) -> None:
        origin = self.guide_site("<h3>1.0 Indledning</h3><p>Guiden indleder.</p><h3>2.0 Ramper</h3><p>Ramper skal være jævne.</p>")

        result = self.audit(origin)

        report = self.report.read_text(encoding="utf-8")
        self.assertEqual(result.returncode, 0, report)
        self.assertIn("Alias pages", report)
        self.assertIn("https://www.bygningsreglementet.dk/tekniske-bestemmelser/02/vejledninger/guide/ramper/", report)

    def test_guide_subpage_is_reported_when_the_root_lacks_guide_text(self) -> None:
        origin = self.guide_site("<h3>1.0 Indledning</h3><h3>2.0 Ramper</h3><p>Ramper skal være jævne.</p>")

        result = self.audit(origin)

        report = self.report.read_text(encoding="utf-8")
        self.assertEqual(result.returncode, 1, report)
        self.assertIn("### https://www.bygningsreglementet.dk/tekniske-bestemmelser/02/vejledninger/guide/ramper/", report)
        self.assertIn("missing_text: Guiden indleder.", report)

    def test_guide_subpage_text_missing_from_its_reference_is_reported(self) -> None:
        origin = self.guide_site(
            "<h3>1.0 Indledning</h3><p>Guiden indleder.</p><h3>2.0 Ramper</h3><p>Ramper skal være jævne.</p>",
            "<h3>1.0 Indledning</h3><h3>@@PROTECTED_7@@</h3><p>Ramper skal være jævne.</p>",
        )

        result = self.audit(origin)

        report = self.report.read_text(encoding="utf-8")
        self.assertEqual(result.returncode, 1, report)
        self.assertIn("### https://www.bygningsreglementet.dk/tekniske-bestemmelser/02/vejledninger/guide/ramper/", report)
        self.assertIn("@@PROTECTED_7@@", report)

    def test_guide_subpage_missing_its_own_section_body_is_reported(self) -> None:
        origin = self.guide_site(
            "<h3>1.0 Indledning</h3><p>Guiden indleder.</p><h3>2.0 Ramper</h3><p>Ramper skal være jævne.</p>",
            "<h3>1.0 Indledning</h3><h3>2.0 Ramper</h3>",
        )

        result = self.audit(origin)

        report = self.report.read_text(encoding="utf-8")
        self.assertEqual(result.returncode, 1, report)
        self.assertIn("### https://www.bygningsreglementet.dk/tekniske-bestemmelser/02/vejledninger/guide/ramper/", report)
        self.assertIn("missing_text: (own page) Ramper skal være jævne.", report)
        self.assertNotIn("Guiden indleder", report)

    def test_markup_residue_is_reported(self) -> None:
        origin = self.two_page_site()
        self.corpus.add(
            "administrative-bestemmelser",
            local_page(
                "<h1>Anvendelsesområde</h1><p>* *</p><p>Reglementet gælder for alt byggeri. **</p>"
                '<ul><li><a href="/administrative-bestemmelser/brv/">Vejledning om anvendelse</a></li></ul>'
                "<p>&lt;br/&gt;</p>"
            ),
        )

        result = self.audit(origin, "--section", "S1")

        report = self.report.read_text(encoding="utf-8")
        self.assertEqual(result.returncode, 1, report)
        self.assertIn("### https://www.bygningsreglementet.dk/administrative-bestemmelser/krav/", report)
        self.assertIn("extra_text: * *", report)
        self.assertIn("extra_text: **", report)
        self.assertIn("extra_text: <br/>", report)

    def test_origin_escaped_line_break_matches_a_rendered_line_break(self) -> None:
        origin = self.two_page_site()
        guides = '<ul><li><a href="/administrative-bestemmelser/brv/">Vejledning om anvendelse</a></li></ul>'
        origin.pages["/administrative-bestemmelser/krav/"] = origin_page(
            "<h1>Anvendelsesområde</h1><p>Reglementet gælder&lt;br/&gt;for alt&lt;br&gt;byggeri. &lt;BR /&gt;Ingen undtagelser.</p>"
            f'<nav class="accordion__nav">{guides}</nav>'
        )
        self.corpus.add(
            "administrative-bestemmelser",
            local_page(f"<h1>Anvendelsesområde</h1><p>Reglementet gælder<br/>for alt<br>byggeri. <br />Ingen undtagelser.</p>{guides}"),
        )

        result = self.audit(origin, "--section", "S1")

        report = self.report.read_text(encoding="utf-8")
        self.assertEqual(result.returncode, 0, report)
        self.assertNotIn("<br", report.lower())

    def test_differently_spelled_links_to_one_page_are_fetched_once(self) -> None:
        origin = self.two_page_site()
        origin.pages["/"] = origin_page(
            "<h1>Forside</h1><p>Velkommen til reglementet.</p>",
            '<a href="/Tekniske-bestemmelser/02/Krav">2</a><a href="/tekniske-bestemmelser/02/krav/">2</a>',
        )

        self.audit(origin)

        self.assertEqual(origin.requests.count("/tekniske-bestemmelser/02/krav/"), 1)
        self.assertNotIn("/Tekniske-bestemmelser/02/Krav", origin.requests)
        self.assertEqual(self.report.read_text(encoding="utf-8").count("### "), 1)

    def test_link_with_non_ascii_path_reaches_the_origin_page(self) -> None:
        origin = self.two_page_site()
        page = "/vejledninger/klimap%C3%A5virkning/"
        origin.pages[page] = origin_page("<p>Klima</p>")
        self.corpus.add("vejledninger/klimapåvirkning", local_page("<p>Klima</p>"))
        origin.pages["/"] = origin_page(
            "<h1>Forside</h1><p>Velkommen til reglementet.</p>",
            '<a href="/vejledninger/Klimap%C3%A5virkning">Klima</a>',
        )

        self.audit(origin)

        self.assertIn(page, origin.page_requests())

    def test_section_scope_reports_only_that_section(self) -> None:
        origin = self.two_page_site()
        self.corpus.add("administrative-bestemmelser", local_page("<h1>Anvendelsesområde</h1>"))

        result = self.audit(origin, "--section", "S1")

        self.assertEqual(result.returncode, 1, result.stderr)
        report = self.report.read_text(encoding="utf-8")
        self.assertIn("https://www.bygningsreglementet.dk/administrative-bestemmelser/krav/", report)
        self.assertIn("Reglementet gælder for alt byggeri.", report)
        self.assertNotIn("tekniske-bestemmelser/02", report)
        self.assertNotIn("Ramper", report)
        self.assertNotIn("S2", report)

    def test_allowlisted_difference_is_not_reported(self) -> None:
        origin = self.two_page_site()
        self.allowlist.write_text(
            """
[[exception]]
page = "/tekniske-bestemmelser/02/krav/"
kind = "missing_text"
item = "Ramper må højst have en hældning på 1:20."
reason = "Fixture: sentence intentionally dropped from the clone."
""",
            encoding="utf-8",
        )

        result = self.audit(origin)

        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        report = self.report.read_text(encoding="utf-8")
        self.assertNotIn("missing_text: Ramper", report)

    def test_allowlist_entry_on_a_guide_root_covers_its_alias_pages(self) -> None:
        origin = self.guide_site("<h3>1.0 Indledning</h3><h3>2.0 Ramper</h3><p>Ramper skal være jævne.</p>")
        self.allowlist.write_text(
            """
[[exception]]
page = "/tekniske-bestemmelser/02/vejledninger/guide/"
kind = "missing_text"
item = "Guiden indleder."
reason = "Fixture: sentence intentionally dropped from the guide."
""",
            encoding="utf-8",
        )

        result = self.audit(origin)

        report = self.report.read_text(encoding="utf-8")
        self.assertEqual(result.returncode, 0, report)
        self.assertNotIn("missing_text: Guiden indleder.", report)

    def redirect_site(self, clone_link: str) -> Origin:
        chapter = "/tekniske-bestemmelser/02/krav/"
        nav = f'<a href="{chapter}">2</a>'
        self.corpus.add("", local_page("<p>Forside</p>"))
        self.corpus.add("tekniske-bestemmelser/02", local_page(f'<p>Adgang</p><a href="{clone_link}">Vejledning</a>'))
        self.corpus.add("tekniske-bestemmelser/02/vejledninger/ny", local_page("<p>Ny vejledning</p>"))
        self.corpus.add("tekniske-bestemmelser/02/vejledninger/gammel", local_page("<p>Ny vejledning</p>"))
        return self.serve(
            {
                "/": origin_page("<p>Forside</p>", nav),
                chapter: origin_page('<p>Adgang</p><a href="/Tekniske-bestemmelser/02/Vejledninger/Gammel">Vejledning</a>', nav),
                "/tekniske-bestemmelser/02/vejledninger/ny/": origin_page("<p>Ny vejledning</p>", nav),
            },
            redirects={"/tekniske-bestemmelser/02/vejledninger/gammel/": "/tekniske-bestemmelser/02/vejledninger/ny/"},
        )

    def test_link_to_an_origin_redirect_matches_a_clone_link_to_its_target(self) -> None:
        origin = self.redirect_site("/tekniske-bestemmelser/02/vejledninger/ny/")

        result = self.audit(origin)

        report = self.report.read_text(encoding="utf-8")
        self.assertEqual(result.returncode, 0, report)
        self.assertNotIn("- missing_link:", report)

    def test_link_to_an_origin_redirect_matches_a_clone_link_to_the_redirect_itself(self) -> None:
        origin = self.redirect_site("/tekniske-bestemmelser/02/vejledninger/gammel/")

        result = self.audit(origin)

        report = self.report.read_text(encoding="utf-8")
        self.assertEqual(result.returncode, 0, report)
        self.assertNotIn("- missing_link:", report)

    def test_allowlist_entry_without_reason_is_rejected(self) -> None:
        origin = self.two_page_site()
        self.allowlist.write_text(
            """
[[exception]]
page = "/tekniske-bestemmelser/02/krav/"
kind = "missing_text"
item = "Ramper må højst have en hældning på 1:20."
""",
            encoding="utf-8",
        )

        result = self.audit(origin)

        self.assertEqual(result.returncode, 2)
        self.assertIn("reason", result.stderr)
        self.assertEqual(origin.page_requests(), [])

    def test_rerun_after_partial_run_does_not_refetch_completed_pages(self) -> None:
        origin = self.two_page_site()
        self.audit(origin, "--section", "S1")
        fetched_first = set(origin.page_requests())
        origin.requests.clear()

        result = self.audit(origin)

        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertEqual(fetched_first, {"/", "/administrative-bestemmelser/krav/"})
        self.assertEqual(origin.page_requests(), ["/tekniske-bestemmelser/02/krav/"])
        self.assertIn("Ramper må højst have en hældning på 1:20.", self.report.read_text(encoding="utf-8"))
        origin.requests.clear()

        self.audit(origin)

        self.assertEqual(origin.page_requests(), [])


if __name__ == "__main__":
    unittest.main()
