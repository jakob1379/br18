from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SITE = "https://www.bygningsreglementet.dk"

sys.path.insert(0, str(REPO / "scripts"))
from audit_br18_parity import cache_file


def origin_html(title: str, body: str) -> str:
    return f"<html><head><title>{title} | BR18</title></head><body><main><h1>{title}</h1>{body}</main></body></html>"


class RegenerateTest(unittest.TestCase):
    def setUp(self) -> None:
        self.root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.root)
        self.docs = self.root / "docs"
        self.cache = self.root / "cache"
        self.cache.mkdir()
        config = re.sub(r"(?ms)^nav = \[$.*?^\]$\n", "", (REPO / "zensical.toml").read_text(encoding="utf-8"))
        nav = 'nav = [{ Hjem = "index.md" }, { Oversigt = "vejledninger/oversigt/index.md" }]\n'
        (self.root / "zensical.toml").write_text(config.replace("[project.validation]", f"{nav}\n[project.validation]", 1), encoding="utf-8")
        shutil.copytree(REPO / "overrides", self.root / "overrides")
        for theme_dir in ("assets", "stylesheets"):
            shutil.copytree(REPO / "docs" / theme_dir, self.docs / theme_dir)
        shutil.copy(REPO / "xref-laws.toml", self.root)
        for name, text in {
            "xref-overrides.toml": "",
            "xref-page-scope.toml": "",
            "required-anchors.tsv": "",
            "origin-dead-links.toml": "[dead_links]\n",
        }.items():
            (self.root / name).write_text(text, encoding="utf-8")
        self.doc("", "# Forside\n")
        self.doc("vejledninger/oversigt", "# Oversigt\n\nLokal oversigt.\n")
        self.doc("vejledninger/a", "# Vejledning A\n\nGammel tekst.\n")
        self.doc("vejledninger/c", "# Vejledning C\n\nSiden findes ikke længere.\n")

    def doc(self, rel: str, text: str) -> None:
        path = self.docs / rel / "index.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def origin(self, path: str, html: str) -> None:
        url = SITE + path
        cache_file(self.cache, url).write_text(json.dumps({"url": url, "final": url, "status": 200, "html": html}), encoding="utf-8")

    def serve(self, *links: str) -> None:
        self.origin("/", origin_html("BR18", "".join(f'<a href="{SITE}{link}">{link}</a>' for link in links)))
        self.origin("/vejledninger/a/", origin_html("Vejledning A", "<p>Ny tekst.</p>"))
        self.origin("/vejledninger/b/", origin_html("Vejledning B", "<p>Ny side.</p>"))
        url = f"{SITE}/vejledninger/"
        cache_file(self.cache, url).write_text(json.dumps({"url": url, "final": url, "status": 404, "html": ""}), encoding="utf-8")

    def regenerate(self) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["bash", str(REPO / "scripts" / "regenerate_docs.sh"), "--cache-dir", str(self.cache), "--project", str(self.root), "vejledninger"],
            capture_output=True,
            text=True,
            timeout=600,
        )

    def test_regenerates_the_pages_the_origin_serves_and_drops_the_ones_it_no_longer_serves(self) -> None:
        self.serve("/vejledninger/a/", "/vejledninger/b/")

        result = self.regenerate()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Ny tekst.", (self.docs / "vejledninger/a/index.md").read_text(encoding="utf-8"))
        self.assertIn("Ny side.", (self.docs / "vejledninger/b/index.md").read_text(encoding="utf-8"))
        self.assertFalse((self.docs / "vejledninger/c/index.md").exists())
        self.assertIn("Lokal oversigt.", (self.docs / "vejledninger/oversigt/index.md").read_text(encoding="utf-8"))

    def test_page_missing_from_the_snapshot_fails_the_run(self) -> None:
        self.serve("/vejledninger/a/", "/vejledninger/b/", "/vejledninger/d/")

        result = self.regenerate()

        self.assertNotEqual(result.returncode, 0)
        self.assertIn(f"{SITE}/vejledninger/d/", result.stderr)
        self.assertIn("Gammel tekst.", (self.docs / "vejledninger/a/index.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
