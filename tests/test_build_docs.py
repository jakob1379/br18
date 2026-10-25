from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


class BuildCheckTest(unittest.TestCase):
    def build(self, page: str) -> subprocess.CompletedProcess[str]:
        root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, root)
        (root / "scripts").mkdir()
        shutil.copy(REPO / "scripts" / "build-docs.sh", root / "scripts")
        config = (REPO / "zensical.toml").read_text(encoding="utf-8")
        markdown = config[config.index("[project.markdown_extensions") :]
        (root / "zensical.toml").write_text(f'[project]\nsite_name = "t"\n{markdown}', encoding="utf-8")
        (root / "docs").mkdir()
        (root / "docs" / "index.md").write_text(page, encoding="utf-8")
        return subprocess.run(
            ["bash", str(root / "scripts" / "build-docs.sh")],
            capture_output=True,
            text=True,
            timeout=300,
            env={**os.environ, "UV_PROJECT": str(REPO)},
        )

    def test_clean_page_passes(self) -> None:
        result = self.build("# Forside\n\nBygninger skal have *adgang* og **lys**: 2 m * 3 m.\n")

        self.assertEqual(result.returncode, 0, result.stderr)

    def test_leaked_placeholder_fails(self) -> None:
        result = self.build("# Forside\n\n### @@PROTECTED_17@@s bestemmelser\n\nTekst.\n")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("markup residue", result.stderr)

    def test_whitespace_only_emphasis_fails(self) -> None:
        result = self.build("# Forside\n\n* *\n\nTekst.\n")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("markup residue", result.stderr)

    def test_stray_strong_markers_fail(self) -> None:
        result = self.build("# Forside\n\n**Spørgsmål? **(11-12-2020)****\n")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("markup residue", result.stderr)

    def test_asterisk_only_line_fails(self) -> None:
        result = self.build("# Forside\n\nTekst.\n\n\\*\n\nMere tekst.\n")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("markup residue", result.stderr)

    def test_emphasised_asterisk_fails(self) -> None:
        result = self.build("# Forside\n\n> ********•******** En håndvask kan flyttes.\n")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("markup residue", result.stderr)


if __name__ == "__main__":
    unittest.main()
