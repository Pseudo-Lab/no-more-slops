"""Tests with invented two-column pages shaped like `pdftotext -layout` output."""
import contextlib
import importlib.util
import io
import unittest
from pathlib import Path
from unittest import mock

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/check_layout.py"
spec = importlib.util.spec_from_file_location("check_layout", SCRIPT)
check_layout = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check_layout)

HEAD = "Short Title of the Paper"


def page(*rows, number, head=HEAD):
    """Rows of (left column, right column) text, the right column 40 characters in; a running
    head on top and the page number centred below."""
    lines = [head] if head else []
    lines += [f"{left:<40}{right}".rstrip() for left, right in rows]
    return "\n".join(lines + ["", f"{number:>40}"])


PAGES = [
    page(("        Abstract", "1   Introduction"), ("We study a thing.", "We propose a method."), number=1, head=None),
    page(("2   Method", "3   Experiments"), ("It works like this.", "4   Conclusion"), ("", "It works."), number=2),
    page(("Acknowledgements", "Appendix notes go to the end."), ("We thank the group.", ""), number=3),
    page(("References", "[2] B. Author. Another paper. 2025."), ("[1] A. Author. A paper. 2024.", ""), number=4),
]
LOG = """Overfull \\hbox (3.2pt too wide) in paragraph at lines 10--12
LaTeX Warning: Reference `tab:x' on page 2 undefined on input line 40.
LaTeX Warning: Citation `key' on page 1 undefined on input line 9.
Missing character: There is no ^^A in font cmr10!
LaTeX Warning: Label(s) may have changed. Rerun to get cross-references right.
"""
SECTIONS = ["Abstract", "Introduction", "Method", "Experiments", "Conclusion", "Acknowledgements"]


class LayoutTextTest(unittest.TestCase):
    def test_reading_order_and_headings(self):
        texts = [text for *_, text in check_layout.runs(PAGES[1])]
        self.assertEqual(texts, [HEAD, "2", "Method", "It works like this.", "3", "Experiments",
                                 "4", "Conclusion", "It works.", "2"])  # the centred page number reads last
        self.assertEqual([number for number, _ in check_layout.find_heading(PAGES, "conclusion")], [2])
        self.assertEqual(check_layout.find_heading(["7. References", "References to earlier work"], "References"),
                         [(1, (0, 0, 0))])

    def test_running_lines(self):
        self.assertEqual(check_layout.running_lines(PAGES + ["Page 7 of 9\nx", "y\nPage 8 of 9"]),
                         {HEAD, "#", "Page # of #"})


class AssessTest(unittest.TestCase):
    def test_clean_paper(self):
        self.assertEqual(check_layout.assess(PAGES, body_pages=3, max_pages=4, sections=SECTIONS), [])
        self.assertEqual(check_layout.assess(PAGES, body_pages=4), [])  # a shorter body is fine

    def test_body_overflow(self):
        self.assertEqual(check_layout.assess(PAGES, body_pages=2, max_pages=3), [
            "4 pages; at most 3 allowed", "'References' starts on page 4: the body runs past page 2"])
        for spill in [page(("One last body line.", "References"), ("", "[1] A. Author."), number=4),
                      page(("One last body line.", ""), ("References", ""), number=4)]:
            with self.subTest(spill):
                self.assertEqual(check_layout.assess(PAGES[:3] + [spill], body_pages=3),
                                 ["text precedes 'References' on page 4: the body runs past page 3"])

    def test_headings_must_come_before_the_references(self):
        self.assertEqual(check_layout.assess(PAGES[:3], body_pages=2),
                         ["no 'References' heading, so the end of the 2-page body is unknown"])
        shared = page(("Acknowledgements", "References"), ("We thank the group.", "[1] A. Author."),
                      ("", "A   Appendix"), number=3)
        self.assertEqual(check_layout.assess(PAGES[:2] + [shared], body_pages=3,
                                             sections=["Acknowledgements", "Appendix", "Discussion"]), [
            "no 'Appendix' heading before the references (first on page 3)",
            "no 'Discussion' heading before the references"])

    def test_unresolved_log_and_fonts(self):
        pages = PAGES[:1] + [PAGES[1] + "\nSee Table ??."] + PAGES[2:]
        self.assertEqual(check_layout.assess(pages, log=LOG, fonts=["T3Font_0"], allow=["overfull"]), [
            "'??' on page 2 (an unresolved reference or citation)",
            "1 x undefined-reference in the LaTeX log", "1 x undefined-citation in the LaTeX log",
            "1 x missing-character in the LaTeX log", "1 x rerun in the LaTeX log", "Type 3 fonts: T3Font_0"])


class CommandTest(unittest.TestCase):
    def test_report_and_exit_status(self):
        out = io.StringIO()
        with mock.patch.object(check_layout, "page_texts", return_value=PAGES), \
                mock.patch.object(check_layout, "type3_fonts", return_value=None), contextlib.redirect_stdout(out):
            self.assertEqual(check_layout.main(["paper.pdf", "--body-pages", "3"]), 0)
            self.assertEqual(check_layout.main(["paper.pdf", "--body-pages", "2"]), 1)
        self.assertEqual(out.getvalue().splitlines(), [
            "paper.pdf: 4 pages; 'References' from page 4; Type 3 fonts not checked (no pdffonts)",
            "paper.pdf: 4 pages; 'References' from page 4; Type 3 fonts not checked (no pdffonts)",
            "PROBLEM: 'References' starts on page 4: the body runs past page 2"])


if __name__ == "__main__":
    unittest.main()
