from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


class BuildCheckTest(unittest.TestCase):
    def build(self, page: str, required_anchors: str = "", files: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
        root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, root)
        (root / "scripts").mkdir()
        shutil.copy(REPO / "scripts" / "build-docs.sh", root / "scripts")
        shutil.copy(REPO / "scripts" / "keep_anchors.py", root / "scripts")
        shutil.copy(REPO / "scripts" / "check_references.py", root / "scripts")
        shutil.copy(REPO / "scripts" / "link_references.py", root / "scripts")
        shutil.copy(REPO / "xref-laws.toml", root)
        shutil.copytree(REPO / "overrides", root / "overrides")
        (root / "required-anchors.tsv").write_text(required_anchors, encoding="utf-8")
        config = (REPO / "zensical.toml").read_text(encoding="utf-8")
        (root / "zensical.toml").write_text(re.sub(r"(?ms)^nav = \[$.*?^\]$\n", "", config), encoding="utf-8")
        for theme_dir in ("assets", "stylesheets"):
            shutil.copytree(REPO / "docs" / theme_dir, root / "docs" / theme_dir)
        (root / "docs" / "index.md").write_text(page, encoding="utf-8")
        for rel, text in (files or {}).items():
            (root / "docs" / rel).parent.mkdir(parents=True, exist_ok=True)
            (root / "docs" / rel).write_text(text, encoding="utf-8")
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

    def test_page_keeping_its_required_anchors_passes(self) -> None:
        result = self.build("# Forside\n\n### § 9 {#paragraf-9}\n\nTekst.\n", "\tparagraf-9\t§ 9\n")

        self.assertEqual(result.returncode, 0, result.stderr)

    def test_missing_required_anchor_fails(self) -> None:
        result = self.build("# Forside\n\n### § 9\n\nTekst.\n", "\tparagraf-9\t§ 9\n")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing required anchors", result.stderr)
        self.assertIn("#paragraf-9", result.stderr)

    def test_placeholder_in_a_kept_old_anchor_id_passes(self) -> None:
        result = self.build(
            '# Forside\n\n<span id="lovens-@@PROTECTED_32@@s-formaal"></span>\n\nTekst.\n',
            "\tlovens-@@PROTECTED_32@@s-formaal\t\n",
        )

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

    def test_broken_local_link_fails(self) -> None:
        result = self.build("# Forside\n\nSe [kapitel 2](tekniske-bestemmelser/02/).\n")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("tekniske-bestemmelser/02", result.stdout + result.stderr)

    def test_broken_anchor_fails(self) -> None:
        result = self.build("# Forside\n\nSe [§ 9](side/#paragraf-9).\n", files={"side/index.md": "# Side\n\n### § 8 {#paragraf-8}\n"})

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("paragraf-9", result.stdout + result.stderr)

    def test_broken_image_fails(self) -> None:
        result = self.build("# Forside\n\n![Figur 1](media/figur-1.png)\n")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("figur-1.png", result.stdout + result.stderr)

    def test_broken_download_fails(self) -> None:
        result = self.build("# Forside\n\nHent [vejledningen](media/vejledning.pdf).\n")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("vejledning.pdf", result.stdout + result.stderr)

    def test_existing_link_image_and_download_pass(self) -> None:
        result = self.build(
            "# Forside\n\nSe [§ 8](side/#paragraf-8), ![Figur 1](media/figur-1.png) og [vejledningen](media/vejledning.pdf).\n",
            files={"side/index.md": "# Side\n\n### § 8 {#paragraf-8}\n", "media/figur-1.png": "png", "media/vejledning.pdf": "pdf"},
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_case_insensitive_path_collision_fails(self) -> None:
        result = self.build("# Forside\n", files={"Administrative-bestemmelser/index.md": "# A\n", "administrative-bestemmelser/index.md": "# a\n"})

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("case-insensitive path collisions", result.stderr)

    def test_query_string_filename_fails(self) -> None:
        result = self.build("# Forside\n", files={"media/logo.png?v=2": "png"})

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("URL query strings", result.stderr)


if __name__ == "__main__":
    unittest.main()
