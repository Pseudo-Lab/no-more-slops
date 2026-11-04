#!/usr/bin/env python3
"""Check a built paper's layout: page budget, where the references start, required section
headings, LaTeX log warnings and Type 3 fonts. Standard library, plus poppler-utils (pdfinfo,
pdftotext, pdffonts) when installed or else pypdf for the page text. Read-only.

Headings are found as text runs in `pdftotext -layout` output, which keeps the two columns of
a page side by side; reading order is the left column, then the right. The pypdf fallback has
no layout, so its column order is only approximate.

Example: a four-page body with references after it, at most six pages in all:
  python3 check_layout.py paper/main.pdf --body-pages 4 --max-pages 6 --log paper/main.log \
      --sections Abstract Introduction Conclusion
Exit status: 0 no problems, 1 problems found, 2 the PDF or log could not be read.
"""

import argparse
import re
import shutil
import subprocess
import sys
from collections import Counter
from pathlib import Path

LOG_PATTERNS = {
    "overfull": re.compile(r"^Overfull \\[hv]box", re.M),
    "undefined-reference": re.compile(r"LaTeX Warning: Reference .* undefined"),
    "undefined-citation": re.compile(r"(?:LaTeX|Package natbib) Warning: Citation .* undefined"),
    "missing-character": re.compile(r"Missing character: There is no"),
    "rerun": re.compile(r"Rerun to get (?:cross-references|outlines) right"),
}


def page_texts(pdf):
    """Text of each page; `pdftotext -layout` keeps two-column lines side by side."""
    if shutil.which("pdfinfo") and shutil.which("pdftotext"):
        info = subprocess.run(["pdfinfo", str(pdf)], check=True, capture_output=True, text=True).stdout
        count = int(re.search(r"^Pages:\s+(\d+)", info, re.M).group(1))
        return [subprocess.run(["pdftotext", "-layout", "-f", str(i), "-l", str(i), str(pdf), "-"], check=True,
                               capture_output=True, text=True).stdout for i in range(1, count + 1)]
    try:
        from pypdf import PdfReader
    except ImportError:
        raise RuntimeError("install poppler-utils (pdftotext, pdfinfo) or pypdf to read the PDF") from None
    return [page.extract_text() or "" for page in PdfReader(str(pdf)).pages]


def type3_fonts(pdf):
    """Names of Type 3 (bitmap) fonts, or None when pdffonts is not installed."""
    if not shutil.which("pdffonts"):
        return None
    listing = subprocess.run(["pdffonts", str(pdf)], check=True, capture_output=True, text=True).stdout
    return [line.split()[0] for line in listing.splitlines()[2:] if " Type 3 " in f" {line} "]


RUN = re.compile(r"\S+(?: \S+)*")  # text separated from its neighbours by two or more spaces


def runs(page):
    """Text runs of a `pdftotext -layout` page as (column, line, offset, text) in reading order:
    the left column top to bottom, then the right. A run starting in the right half of the
    page's widest line is in the right column; single-column text starts in the left half."""
    lines = page.expandtabs().splitlines()
    width = max((len(line.rstrip()) for line in lines), default=0)
    found = [(1 if match.start() >= width / 2 else 0, number, match.start(), match.group())
             for number, line in enumerate(lines) for match in RUN.finditer(line)]
    return sorted(found)


def find_heading(pages, name):
    """(page number, reading position) of each run that is `name`, optionally numbered ("4", "4.1",
    "IV."). Any run with that exact text counts, so a table cell reading "Method" does too."""
    pattern = re.compile(rf"(?:(?:\d+(?:\.\d+)*|[IVXLC]+)\.?\s+)?{re.escape(name)}", re.I)
    return [(number, run[:3]) for number, page in enumerate(pages, 1) for run in runs(page)
            if pattern.fullmatch(run[3])]


def _edges(page):
    """(index, text with digits as #) of a page's first and last non-empty lines."""
    lines = page.expandtabs().splitlines()
    filled = [i for i, line in enumerate(lines) if line.strip()]
    return [(i, re.sub(r"\d+", "#", " ".join(lines[i].split()))) for i in dict.fromkeys(filled[:1] + filled[-1:])]


def running_lines(pages):
    """Running heads and feet, page numbers included: first or last lines that recur, digits
    aside, on two or more pages."""
    counts = Counter(text for page in pages for text in {text for _, text in _edges(page)})
    return {text for text, count in counts.items() if count >= 2}


def text_before(page, position, running=()):
    """Text read before `position` on a page, leaving out running heads and feet."""
    skip = {index for index, text in _edges(page) if text in running}
    return [text for column, line, offset, text in runs(page) if (column, line, offset) < position and line not in skip]


def assess(pages, body_pages=None, max_pages=None, references="References", sections=(), log="", fonts=None,
           allow=()):
    """Problems with a paper's layout, from page texts, the LaTeX log and the Type 3 font list."""
    problems = []
    if max_pages is not None and len(pages) > max_pages:
        problems.append(f"{len(pages)} pages; at most {max_pages} allowed")
    refs = find_heading(pages, references)
    if body_pages is not None:
        if not refs and len(pages) > body_pages:
            problems.append(f"no '{references}' heading, so the end of the {body_pages}-page body is unknown")
        elif refs:
            number, position = refs[0]
            if number > body_pages + 1:
                problems.append(f"'{references}' starts on page {number}: the body runs past page {body_pages}")
            elif number == body_pages + 1 and text_before(pages[number - 1], position, running_lines(pages)):
                problems.append(f"text precedes '{references}' on page {number}: the body runs past page {body_pages}")
    for section in sections:
        found = find_heading(pages, section)
        if not any(not refs or place < refs[0] for place in found):
            where = f" (first on page {found[0][0]})" if found else ""
            problems.append(f"no '{section}' heading before the references{where}")
    unresolved = [str(number) for number, text in enumerate(pages, 1) if "??" in text]
    if unresolved:
        problems.append(f"'??' on page {', '.join(unresolved)} (an unresolved reference or citation)")
    for name, pattern in LOG_PATTERNS.items():
        hits = pattern.findall(log or "")
        if hits and name not in allow:
            problems.append(f"{len(hits)} x {name} in the LaTeX log")
    if fonts:
        problems.append(f"Type 3 fonts: {', '.join(fonts)}")
    return problems


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("pdf")
    parser.add_argument("--body-pages", type=int, help="page budget for everything before the references")
    parser.add_argument("--max-pages", type=int, help="limit on the whole PDF")
    parser.add_argument("--references", default="References", help="heading that starts the references")
    parser.add_argument("--sections", nargs="*", default=[], help="headings that must come before the references")
    parser.add_argument("--log", help="LaTeX log to scan for warnings")
    parser.add_argument("--allow", nargs="*", default=[], choices=sorted(LOG_PATTERNS), help="log warnings to accept")
    args = parser.parse_args(argv)
    pages = page_texts(Path(args.pdf))
    log = Path(args.log).read_text(encoding="utf-8", errors="replace") if args.log else ""
    fonts = type3_fonts(Path(args.pdf))
    refs = find_heading(pages, args.references)
    summary = f"{args.pdf}: {len(pages)} pages; " + (
        f"'{args.references}' from page {refs[0][0]}" if refs else f"no '{args.references}' heading")
    print(summary + ("" if fonts is not None else "; Type 3 fonts not checked (no pdffonts)"))
    problems = assess(pages, args.body_pages, args.max_pages, args.references, args.sections, log, fonts, args.allow)
    for problem in problems:
        print(f"PROBLEM: {problem}")
    return 1 if problems else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(2)
