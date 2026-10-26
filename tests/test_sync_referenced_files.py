from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "sync_referenced_files.py"


class FileOrigin:
    def __init__(self, files: dict[str, tuple[bytes, str]]) -> None:
        self.files = files
        self.requests: list[tuple[str, str]] = []
        origin = self

        class Handler(BaseHTTPRequestHandler):
            def reply(self, body: bool) -> None:
                origin.requests.append((self.command, self.path))
                if self.path not in origin.files:
                    self.send_response(404)
                    self.end_headers()
                    return
                content, etag = origin.files[self.path]
                self.send_response(200)
                self.send_header("content-length", str(len(content)))
                self.send_header("etag", etag)
                self.send_header("last-modified", "Mon, 11 Nov 2024 18:22:12 GMT")
                self.end_headers()
                if body:
                    self.wfile.write(content)

            def do_HEAD(self) -> None:
                self.reply(False)

            def do_GET(self) -> None:
                self.reply(True)

            def log_message(self, *args: object) -> None:
                pass

        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        threading.Thread(target=self.server.serve_forever, daemon=True).start()
        self.url = f"http://127.0.0.1:{self.server.server_port}"


class FileVersionsTest(unittest.TestCase):
    def setUp(self) -> None:
        self.root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.root)
        self.docs = self.root / "docs"
        self.manifest = self.root / "media-versions.tsv"
        (self.docs / "side").mkdir(parents=True)
        (self.docs / "side" / "index.md").write_text(
            "# Side\n\n[Skema](../media/a/skema.pdf) og [Vejledning](../media/b/vejledning.pdf).\n", encoding="utf-8"
        )
        self.local("media/a/skema.pdf", b"gammelt skema")
        self.local("media/b/vejledning.pdf", b"vejledning v1")

    def local(self, rel: str, content: bytes) -> None:
        (self.docs / rel).parent.mkdir(parents=True, exist_ok=True)
        (self.docs / rel).write_bytes(content)

    def check(self, origin: FileOrigin) -> subprocess.CompletedProcess[str]:
        self.addCleanup(origin.server.shutdown)
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--docs-root", str(self.docs), "--check-versions", "--origin", origin.url,
             "--delay", "0", "--manifest", str(self.manifest)],
            capture_output=True,
            text=True,
            timeout=120,
        )

    def test_file_whose_origin_version_differs_in_size_is_downloaded_again(self) -> None:
        origin = FileOrigin({"/media/a/skema.pdf": (b"nyt og laengere skema", '"2"'), "/media/b/vejledning.pdf": (b"vejledning v1", '"1"')})

        result = self.check(origin)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.docs / "media/a/skema.pdf").read_bytes(), b"nyt og laengere skema")
        self.assertEqual((self.docs / "media/b/vejledning.pdf").read_bytes(), b"vejledning v1")
        self.assertNotIn(("GET", "/media/b/vejledning.pdf"), origin.requests)
        self.assertIn("media/a/skema.pdf", result.stdout)

    def test_file_whose_origin_etag_changed_since_the_recorded_version_is_downloaded_again(self) -> None:
        self.check(FileOrigin({"/media/a/skema.pdf": (b"gammelt skema", '"1"'), "/media/b/vejledning.pdf": (b"vejledning v1", '"1"')}))
        origin = FileOrigin({"/media/a/skema.pdf": (b"gammelt skema", '"1"'), "/media/b/vejledning.pdf": (b"vejledning v2", '"2"')})

        result = self.check(origin)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual((self.docs / "media/b/vejledning.pdf").read_bytes(), b"vejledning v2")
        self.assertNotIn(("GET", "/media/a/skema.pdf"), origin.requests)
        self.assertIn("media/b/vejledning.pdf", result.stdout)

    def test_file_saved_under_a_query_string_alias_is_checked_against_the_origin_file(self) -> None:
        (self.docs / "side" / "index.md").write_text("# Side\n\n[Tabel](../media/c/tabel__q_01687ceb886b.xlsx)\n", encoding="utf-8")
        self.local("media/c/tabel__q_01687ceb886b.xlsx", b"tabel")

        result = self.check(FileOrigin({"/media/c/tabel.xlsx": (b"tabel", '"1"')}))

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("media/c/tabel__q_01687ceb886b.xlsx", self.manifest.read_text(encoding="utf-8"))

    def test_file_the_origin_no_longer_serves_fails_the_check(self) -> None:
        result = self.check(FileOrigin({"/media/b/vejledning.pdf": (b"vejledning v1", '"1"')}))

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("media/a/skema.pdf", result.stderr)


if __name__ == "__main__":
    unittest.main()
