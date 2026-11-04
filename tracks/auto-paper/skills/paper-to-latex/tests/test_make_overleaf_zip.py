"""Exercise the packaging CLI with disposable sources and archive destinations."""

import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "make_overleaf_zip.py"
SOURCE = b"\\documentclass{article}\n\\begin{document}Original manuscript\\end{document}\n"


class ArchiveOutputTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "main.tex"
        self.source.write_bytes(SOURCE)

    def package(self, output):
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(self.root), "--zip", str(output)],
            cwd=self.root, capture_output=True, text=True,
        )

    def test_main_tex_destination_preserves_manuscript(self):
        result = self.package("main.tex")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(".zip extension", result.stderr)
        self.assertEqual(self.source.read_bytes(), SOURCE)

    def test_existing_non_archive_is_preserved(self):
        output = self.root / "notes.zip"
        output.write_bytes(b"Existing notes that must survive")
        result = self.package(output)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("not a ZIP archive", result.stderr)
        self.assertEqual(output.read_bytes(), b"Existing notes that must survive")
        self.assertEqual(self.source.read_bytes(), SOURCE)

    def test_symlink_to_source_is_rejected(self):
        output = self.root / "manuscript.zip"
        output.symlink_to(self.source)
        result = self.package(output)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.source.read_bytes(), SOURCE)
        self.assertTrue(output.is_symlink())

    def test_hardlink_to_source_is_rejected(self):
        output = self.root / "manuscript.zip"
        os.link(self.source, output)
        result = self.package(output)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("conflicts with a project source", result.stderr)
        self.assertEqual(self.source.read_bytes(), SOURCE)
        self.assertTrue(output.samefile(self.source))

    def test_valid_archive_can_be_created_and_replaced(self):
        output = self.root / "paper.zip"
        first = self.package(output)
        self.assertEqual(first.returncode, 0, first.stderr)
        with zipfile.ZipFile(output) as archive:
            self.assertEqual(archive.namelist(), ["main.tex"])
            self.assertEqual(archive.read("main.tex"), SOURCE)
        with zipfile.ZipFile(output, "a") as archive:
            archive.writestr("obsolete.txt", "previous archive contents")
        second = self.package(output)
        self.assertEqual(second.returncode, 0, second.stderr)
        with zipfile.ZipFile(output) as archive:
            self.assertEqual(archive.namelist(), ["main.tex"])
            self.assertEqual(archive.read("main.tex"), SOURCE)
        self.assertEqual(self.source.read_bytes(), SOURCE)


if __name__ == "__main__":
    unittest.main()
