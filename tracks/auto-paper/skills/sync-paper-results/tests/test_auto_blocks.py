"""Tests with small invented documents."""
import contextlib
import importlib.util
import io
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/auto_blocks.py"
spec = importlib.util.spec_from_file_location("auto_blocks", SCRIPT)
auto_blocks = importlib.util.module_from_spec(spec)
spec.loader.exec_module(auto_blocks)

TEX = r"""\section{Results}
Written prose stays as it is.
% BEGIN AUTO RESULTS
old table
% END AUTO RESULTS
More prose.
  % BEGIN AUTO EMPTY
  % END AUTO EMPTY
"""

MD = """# Notes
<!-- BEGIN AUTO SUMMARY -->
| a | b |
<!-- END AUTO SUMMARY -->
"""


def run(*argv, stdin=""):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        try:
            code = auto_blocks.main(list(argv))
        except ValueError as exc:
            print(exc, file=err)
            code = 2
    return code, out.getvalue(), err.getvalue()


class BlocksTest(unittest.TestCase):
    def test_finds_latex_and_markdown_blocks(self):
        found = auto_blocks.blocks(TEX)
        self.assertEqual(list(found), ["RESULTS", "EMPTY"])
        start, end, begin, finish = found["RESULTS"]
        self.assertEqual((TEX[start:end], begin, finish), ("old table\n", 3, 5))
        start, end, _, _ = found["EMPTY"]
        self.assertEqual(TEX[start:end], "")
        start, end, _, _ = auto_blocks.blocks(MD)["SUMMARY"]
        self.assertEqual(MD[start:end], "| a | b |\n")

    def test_rejects_malformed_markers(self):
        cases = {
            "nested": "% BEGIN AUTO A\n% BEGIN AUTO B\n% END AUTO B\n% END AUTO A\n",
            "twice": "% BEGIN AUTO A\n% END AUTO A\n% BEGIN AUTO A\n% END AUTO A\n",
            "unclosed": "% BEGIN AUTO A\ntext\n",
            "stray end": "text\n% END AUTO A\n",
            "mismatched": "% BEGIN AUTO A\n% END AUTO B\n",
        }
        for label, text in cases.items():
            with self.subTest(label), self.assertRaises(ValueError):
                auto_blocks.blocks(text)

    def test_replace_touches_only_the_block(self):
        new = auto_blocks.replace(TEX, "RESULTS", "new table")
        self.assertEqual(new, TEX.replace("old table\n", "new table\n"))
        self.assertEqual(auto_blocks.replace(new, "RESULTS", "new table\n"), new)
        self.assertIn("  % BEGIN AUTO EMPTY\nfilled\n  % END AUTO EMPTY", auto_blocks.replace(TEX, "EMPTY", "filled"))
        with self.assertRaises(ValueError):
            auto_blocks.replace(TEX, "MISSING", "x")


class CommandTest(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.dir.cleanup)
        self.paper = Path(self.dir.name) / "paper.tex"
        self.paper.write_text(TEX, encoding="utf-8")
        self.table = Path(self.dir.name) / "table.tex"

    def test_list_and_show(self):
        code, out, _ = run("list", str(self.paper))
        self.assertEqual((code, out), (0, "RESULTS\tlines 3-5\nEMPTY\tlines 7-8\n"))
        self.assertEqual(run("show", str(self.paper), "RESULTS")[:2], (0, "old table\n"))

    def test_replace_then_check(self):
        self.table.write_text("new table\n", encoding="utf-8")
        self.assertEqual(run("check", str(self.paper), "RESULTS", "--from", str(self.table))[0], 1)
        code, _, err = run("replace", str(self.paper), "RESULTS", "--from", str(self.table), "--require", "EMPTY")
        self.assertEqual((code, err.strip()), (0, "RESULTS: replaced"))
        self.assertEqual(self.paper.read_text(encoding="utf-8"), TEX.replace("old table", "new table"))
        self.assertEqual(run("check", str(self.paper), "RESULTS", "--from", str(self.table))[0], 0)

    def test_refusals_leave_the_file_unchanged(self):
        self.table.write_text("% BEGIN AUTO X\n% END AUTO X\n", encoding="utf-8")
        self.assertEqual(run("replace", str(self.paper), "RESULTS", "--from", str(self.table))[0], 2)
        self.table.write_text("new\n", encoding="utf-8")
        self.assertEqual(run("replace", str(self.paper), "RESULTS", "--from", str(self.table),
                             "--require", "FIGURE")[0], 2)
        self.assertEqual(run("replace", str(self.paper), "FIGURE", "--from", str(self.table))[0], 2)
        self.assertEqual(self.paper.read_text(encoding="utf-8"), TEX)


if __name__ == "__main__":
    unittest.main()
