from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "link_official_refs.py"


class LinkOfficialRefsTest(unittest.TestCase):
    def linkify(self, text: str) -> str:
        docs = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, docs)
        (docs / "administrative-bestemmelser" / "krav" / "22d").mkdir(parents=True)
        (docs / "administrative-bestemmelser" / "krav" / "22d" / "index.md").write_text("# § 22 d\n", encoding="utf-8")
        (docs / "side").mkdir()
        (docs / "side" / "index.md").write_text(text, encoding="utf-8")
        subprocess.run([sys.executable, str(SCRIPT), "--docs-root", str(docs)], check=True, capture_output=True)
        return (docs / "side" / "index.md").read_text(encoding="utf-8")

    def test_section_letter_is_not_taken_from_the_next_word(self) -> None:
        markdown = self.linkify("Efter § 22 dispenseres der, jf. § 22 d i reglementet.\n")

        self.assertEqual(
            markdown,
            "Efter § 22 dispenseres der, jf. [§ 22 d](/administrative-bestemmelser/krav/22d/) i reglementet.\n",
        )


if __name__ == "__main__":
    unittest.main()
