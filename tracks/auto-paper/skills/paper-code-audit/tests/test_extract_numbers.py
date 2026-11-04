"""Tests with small invented documents."""
import contextlib
import importlib.util
import io
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/extract_numbers.py"
spec = importlib.util.spec_from_file_location("extract_numbers", SCRIPT)
extract_numbers = importlib.util.module_from_spec(spec)
spec.loader.exec_module(extract_numbers)

TEX = r"""\documentclass{article}
\setlength{\columnsep}{0.25in}
\begin{document}
\begin{abstract}
On 3,051 examples, accuracy rises from 63.8\% to 74.6\% with gpt-5-nano and jev-1.13.0. % 99 hidden
\end{abstract}
\section{Results}
We use $\tau=0.5$ and $r=3$, see Table~\ref{tab:x2} and~\cite{key2024}.
\begin{tikzpicture}
\addplot coordinates {(1,72.0) (3,74.6)};
\end{tikzpicture}
\begin{tabular}{lrr}
\cmidrule(lr){2-3}
\multicolumn{2}{c}{Head} & x\\
Total & 64.1 & $-$0.35\\
\end{tabular}
Spacing \vspace{4pt} and widths of 12pt stay out; revision 6ea57973c7a6 too.
\end{document}
"""

MD = """# Results

- Accuracy rose from 64.1% to 74.8% (95% CI 9.7–11.6); cost $0.21 per 1,000.
<!-- 42 hidden -->
![chart](docs/chart-2.png) and [paper](https://example.com/v2/123)

```
make run WORKERS=8
```
"""


class ExtractTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.tex = Path(self.temp.name) / "paper.tex"
        self.tex.write_text(TEX)
        self.md = Path(self.temp.name) / "README.md"
        self.md.write_text(MD)

    def test_latex_numbers_with_sections_and_skips(self):
        items = extract_numbers.extract(self.tex)
        raws = [item["raw"] for item in items]
        self.assertEqual(raws, ["3,051", "63.8", "74.6", "0.5", "3", "64.1", "−0.35"])
        self.assertEqual(items[0]["section"], "Abstract")
        self.assertEqual(items[3]["section"], "Results")
        self.assertEqual((items[0]["value"], items[-1]["value"]), (3051.0, -0.35))

    def test_markdown_numbers_skip_code_comments_and_links(self):
        items = extract_numbers.extract(self.md)
        raws = [item["raw"] for item in items]
        self.assertEqual(raws, ["64.1%", "74.8%", "95%", "9.7", "11.6", "$0.21", "1,000"])
        self.assertTrue(items[0]["percent"])
        self.assertEqual(items[5]["value"], 0.21)

    def test_compare_lists_numbers_the_reference_does_not_state(self):
        missing = extract_numbers.missing_from(extract_numbers.extract(self.md), extract_numbers.extract(self.tex))
        self.assertEqual([item["raw"] for item in missing], ["74.8%", "95%", "9.7", "11.6", "$0.21", "1,000"])
        close = extract_numbers.missing_from(extract_numbers.extract(self.md), extract_numbers.extract(self.tex), .21)
        self.assertNotIn("74.8%", [item["raw"] for item in close])  # within tolerance of 74.6

    def test_cli_exit_code_reports_missing_numbers(self):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(extract_numbers.main([str(self.tex)]), 0)
            self.assertEqual(extract_numbers.main([str(self.md), "--compare", str(self.tex)]), 1)
            self.assertEqual(extract_numbers.main([str(self.tex), "--compare", str(self.tex)]), 0)


if __name__ == "__main__":
    unittest.main()
