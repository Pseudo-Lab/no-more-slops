"""Tests with small invented documents."""
import contextlib
import importlib.util
import io
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/stale_numbers.py"
spec = importlib.util.spec_from_file_location("stale_numbers", SCRIPT)
stale_numbers = importlib.util.module_from_spec(spec)
spec.loader.exec_module(stale_numbers)

BEFORE = r"""\documentclass{article}
\setlength{\columnsep}{0.25in}
\begin{document}
\begin{abstract}
Accuracy rises from 63.8\% to 74.6\% on 3,051 examples with gpt-5-nano.
\end{abstract}
% BEGIN AUTO RESULTS
\begin{tabular}{lrr}
Direct & 63.8 & 1,204 & 0.35 \\
JBFC & 74.6 & 4,980 & 1.7 \\
\end{tabular}
% END AUTO RESULTS
JBFC gains 10.8 points (Table~\ref{tab:74}); see Section 3. % was 74.6 before
The interval is 0.4--1.7 {\fontsize{74.6}{9}\selectfont x}.
\begin{tikzpicture}
\node at (74.6, 1) {};
\end{tikzpicture}
\end{document}
"""
AFTER = BEFORE.replace("JBFC & 74.6 & 4,980 & 1.7", "JBFC & 74.8 & 5,012 & 1.8")
README = """# Results
<!-- BEGIN AUTO TABLE -->
| JBFC | 74.6 |
<!-- END AUTO TABLE -->
JBFC reaches 74.6% ([chart](docs/74.6.png)); costs 4,980 USD per https://example.com/74.6.
"""


class StaleTest(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.dir = Path(tmp.name)
        for name, text in {"before.tex": BEFORE, "after.tex": AFTER, "README.md": README}.items():
            (self.dir / name).write_text(text, encoding="utf-8")

    def test_generated_values_ignore_identifiers(self):
        self.assertEqual(stale_numbers.generated_values(BEFORE), {63.8, 1204.0, 0.35, 74.6, 4980.0, 1.7})
        self.assertEqual([stale_numbers.digits(n) for n in ["74.6", "0.35", "4,980", "8", "1.70"]], [3, 2, 4, 1, 3])

    def test_finds_replaced_values_outside_blocks(self):
        found = stale_numbers.stale(self.dir / "before.tex", self.dir / "after.tex", [self.dir / "README.md"])
        self.assertEqual([(Path(path).name, line, number) for path, line, number, _ in found],
                         [("after.tex", 5, "74.6"), ("README.md", 5, "74.6"), ("README.md", 5, "4,980")])
        self.assertIn("rises from 63.8\\% to 74.6\\%", found[0][3])
        short = stale_numbers.stale(self.dir / "before.tex", self.dir / "after.tex", min_digits=1)
        self.assertEqual([(line, number) for _, line, number, _ in short], [(5, "74.6"), (14, "1.7")])

    def test_command(self):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = stale_numbers.main(["--before", str(self.dir / "before.tex"), "--after", str(self.dir / "after.tex")])
            same = stale_numbers.main(["--before", str(self.dir / "after.tex"), "--after", str(self.dir / "after.tex")])
        self.assertEqual((code, same), (1, 0))
        self.assertTrue(out.getvalue().startswith(f"{self.dir / 'after.tex'}:5: 74.6\t"))


if __name__ == "__main__":
    unittest.main()
