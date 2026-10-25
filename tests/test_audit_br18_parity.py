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
    def __init__(self, pages: dict[str, str]) -> None:
        self.pages = pages
        self.requests: list[str] = []
        origin = self

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self) -> None:
                origin.requests.append(self.path)
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

    def serve(self, pages: dict[str, str]) -> Origin:
        origin = Origin(pages)
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
