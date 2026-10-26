from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from audit_br18_parity import cache_file

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "fetch_origin_pages.py"
SITE = "https://www.bygningsreglementet.dk"


def page(path: str, body: str, expand_all: str | None = None, trigger: str | None = None, final: str | None = None) -> dict:
    links = f'<a href="{SITE}{expand_all}?Layout=ShowAll" class="link--expand-all">Fold alle ud</a>' if expand_all else ""
    if trigger:
        links += f'<a href="{SITE}{trigger}#0b0c2f0e-1111-2222-3333-444455556666" class="accordion__trigger">1.</a>'
    url = SITE + path
    return {"url": url, "final": SITE + (final or path), "status": 200, "html": f"<html><body><main>{links}<p>{body}</p></main></body></html>"}


class FetchFromSnapshotTest(unittest.TestCase):
    def fetch(self, records: list[dict], *paths: str) -> Path:
        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, tmp)
        cache = tmp / "cache"
        cache.mkdir()
        for record in records:
            cache_file(cache, record["url"]).write_text(json.dumps(record))
        docs = tmp / "docs"
        subprocess.run(
            [sys.executable, str(SCRIPT), "--docs-root", str(docs), "--cache-dir", str(cache), *(SITE + p for p in paths)],
            check=True,
            capture_output=True,
        )
        return docs

    def test_guide_root_gets_its_show_all_view_and_a_subpage_keeps_its_own_section(self) -> None:
        guide = "/tekniske-bestemmelser/16/vejledninger/generel_vejledning/"
        docs = self.fetch(
            [
                page(guide, "kun overskrifter", expand_all=guide, trigger=guide + "2_1/"),
                page(guide + "?Layout=ShowAll", "hele vejledningen"),
                page(guide + "2_1/", "eget afsnit", expand_all=guide + "2_1/", trigger=guide + "2_1/"),
            ],
            guide,
            guide + "2_1/",
        )

        self.assertIn("hele vejledningen", (docs / guide.strip("/") / "index.html").read_text())
        self.assertIn("eget afsnit", (docs / guide.strip("/") / "2_1" / "index.html").read_text())

    def test_krav_subpage_gets_its_chapter_roots_show_all_view(self) -> None:
        krav = "/tekniske-bestemmelser/16/krav/"
        docs = self.fetch(
            [
                page(krav + "358/", "kun § 358", expand_all=krav, trigger=krav + "358/"),
                page(krav + "?Layout=ShowAll", "hele kapitlet"),
            ],
            krav + "358/",
        )

        self.assertIn("hele kapitlet", (docs / krav.strip("/") / "358" / "index.html").read_text())

    def test_redirected_page_is_written_at_its_target_path(self) -> None:
        alias = "/ovrige-bestemmelser/29/brv/gammel-vejledning/"
        target = "/ovrige-bestemmelser/29/brv/ny-vejledning/"
        docs = self.fetch([page(alias, "vejledningen", final=target)], alias)

        self.assertIn("vejledningen", (docs / target.strip("/") / "index.html").read_text())
        self.assertFalse((docs / alias.strip("/")).exists())

    def test_page_missing_from_the_snapshot_is_reported_and_the_rest_fetched(self) -> None:
        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, tmp)
        cache = tmp / "cache"
        cache.mkdir()
        record = page("/tekniske-bestemmelser/16/krav/", "kapitlet")
        cache_file(cache, record["url"]).write_text(json.dumps(record))

        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--docs-root", str(tmp / "docs"), "--cache-dir", str(cache),
             f"{SITE}/tekniske-bestemmelser/16/", f"{SITE}/tekniske-bestemmelser/16/krav/"],
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("tekniske-bestemmelser/16/", result.stderr)
        self.assertIn("kapitlet", (tmp / "docs" / "tekniske-bestemmelser" / "16" / "krav" / "index.html").read_text())

    def test_mixed_case_url_is_written_at_the_lowercase_path(self) -> None:
        mixed = "/Tekniske-bestemmelser/17/Vejledninger/Kontorbygninger"
        record = page(mixed.lower() + "/", "kontorbyggeri", final=mixed)
        docs = self.fetch([record], mixed)

        self.assertIn("kontorbyggeri", (docs / mixed.strip("/").lower() / "index.html").read_text())


class LiveOrigin:
    def __init__(self, pages: dict[str, str]) -> None:
        self.requests: list[tuple[float, str]] = []
        origin = self

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self) -> None:
                origin.requests.append((time.monotonic(), self.path))
                body = pages.get(self.path)
                self.send_response(200 if body is not None else 404)
                self.send_header("content-type", "text/html; charset=utf-8")
                self.end_headers()
                self.wfile.write((body or "not found").encode())

            def log_message(self, *args: object) -> None:
                pass

        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.url = f"http://127.0.0.1:{self.server.server_port}"


class FetchLiveTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        rendered = "<main><p id='x'></p><script>document.getElementById('x').textContent = 'gengivet ' + 'af browseren'</script></main>"
        self.origin = LiveOrigin(
            {
                "/": '<html><body><main><a href="/tekniske-bestemmelser/06/krav/">6</a><a href="/tekniske-bestemmelser/06/vejledninger/">V</a></main></body></html>',
                "/tekniske-bestemmelser/06/krav/": f"<html><head><title>BR18</title></head><body>{rendered}</body></html>",
                "/tekniske-bestemmelser/06/vejledninger/": "<html><body><main><p>Vejledninger</p></main></body></html>",
            }
        )
        self.addCleanup(self.origin.server.shutdown)
        self.urls = [f"{SITE}/tekniske-bestemmelser/06/krav/", f"{SITE}/tekniske-bestemmelser/06/vejledninger/"]

    def run_script(self, script: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run([sys.executable, str(script), *args], capture_output=True, text=True, timeout=300)

    def test_live_fetch_renders_pages_like_the_audit_snapshot(self) -> None:
        live = self.run_script(SCRIPT, "--origin", self.origin.url, "--delay", "0", "--docs-root", str(self.tmp / "live"), *self.urls)
        audit = self.run_script(
            SCRIPT.parent / "audit_br18_parity.py", "--origin", self.origin.url, "--delay", "0", "--cache-dir", str(self.tmp / "cache"),
            "--docs-root", str(self.tmp / "none"), "--site-dir", str(self.tmp / "none"), "--output", str(self.tmp / "report.md"),
        )
        snapshot = self.run_script(SCRIPT, "--cache-dir", str(self.tmp / "cache"), "--docs-root", str(self.tmp / "snapshot"), *self.urls)

        self.assertEqual(live.returncode, 0, live.stderr)
        self.assertEqual(snapshot.returncode, 0, snapshot.stderr + audit.stderr)
        page = Path("tekniske-bestemmelser/06/krav/index.html")
        self.assertIn("gengivet af browseren", (self.tmp / "live" / page).read_text())
        for rel in (page, Path("tekniske-bestemmelser/06/vejledninger/index.html")):
            self.assertEqual((self.tmp / "live" / rel).read_text(), (self.tmp / "snapshot" / rel).read_text())

    def test_live_fetch_waits_between_origin_requests(self) -> None:
        result = self.run_script(SCRIPT, "--origin", self.origin.url, "--delay", "1.5", "--docs-root", str(self.tmp / "live"), *self.urls)

        self.assertEqual(result.returncode, 0, result.stderr)
        times = [t for t, path in self.origin.requests if path.startswith("/tekniske-bestemmelser/")]
        self.assertEqual(len(times), 2)
        self.assertGreaterEqual(times[1] - times[0], 1.5)


if __name__ == "__main__":
    unittest.main()
