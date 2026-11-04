#!/usr/bin/env python3
"""List every number a LaTeX or Markdown document states, with its location and context.

Use it to build the inventory of numeric claims to check against code and records,
or (--compare) to find numbers that one document states and another does not, e.g.
README results missing from the paper's tables. Standard library only; read-only.

LaTeX: the preamble, comments, drawing code (tikzpicture, axis), labels, references,
citations and URLs are skipped, as are lengths such as 4pt or 0.75in. Markdown:
fenced code, HTML comments and link targets are skipped.
"""

import argparse
import json
import re
import sys
from pathlib import Path

NUMBER = re.compile(r"(?<![\w.])[-−]?\$?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?%?(?![\w])")
UNIT_AFTER = re.compile(r"\s*(?:pt|cm|mm|in|em|ex|bp|sp|px)\b")
SKIP_ENVS = ("tikzpicture", "axis", "groupplot", "pgfpicture", "lstlisting", "verbatim", "minted", "algorithmic",
             "equation", "equation*", "align", "align*")
SKIP_COMMANDS = re.compile(r"\\(?:label|ref|eqref|cite\w*|url|nolinkurl|href|includegraphics|input|include|"
                           r"bibitem|usepackage|documentclass|definecolor|setlength|setcounter|renewcommand|newcommand|"
                           r"pgfplotsset|usetikzlibrary|cmidrule|vspace|hspace|addplot)\*?(?:\[[^\]]*\])?(?:\{[^{}]*\})*")
TABLE_LAYOUT = re.compile(r"\\cmidrule(?:\([^)]*\))?\{[^{}]*\}|\\multicolumn\{\d+\}\{[^{}]*\}|\\begin\{tabular\}\{[^{}]*\}")
HEADING_TEX = re.compile(r"\\(section|subsection|subsubsection|paragraph)\*?\{([^{}]*)\}")
HEADING_MD = re.compile(r"^(#{1,6})\s+(.*)")


def normalize(raw):
    text = raw.replace("−", "-").replace("$", "").replace(",", "")
    percent = text.endswith("%")
    value = float(text.rstrip("%"))
    return value, percent


def strip_tex_comment(line):
    out, escaped = [], False
    for char in line:
        if char == "%" and not escaped:
            break
        out.append(char)
        escaped = char == "\\" and not escaped
    return "".join(out)


def tex_lines(text):
    """(line number, cleaned text, section) for the document body."""
    lines = text.splitlines()
    begin = next((i for i, line in enumerate(lines) if "\\begin{document}" in line), -1)
    section, skipping = "", []
    for number, line in enumerate(lines, 1):
        if number - 1 <= begin:
            continue
        line = strip_tex_comment(line)
        for env in SKIP_ENVS:
            if f"\\begin{{{env}}}" in line:
                skipping.append(env)
        if skipping:
            for env in SKIP_ENVS:
                if f"\\end{{{env}}}" in line and env in skipping:
                    skipping.remove(env)
            continue
        heading = HEADING_TEX.search(line)
        if heading:
            section = heading.group(2).strip()
        elif "\\begin{abstract}" in line:
            section = "Abstract"
        line = line.replace("$-$", "−").replace("$+$", "+")  # math-mode signs
        yield number, SKIP_COMMANDS.sub(" ", TABLE_LAYOUT.sub(" ", line)), section


def md_lines(text):
    section, fenced, comment = "", False, False
    for number, line in enumerate(text.splitlines(), 1):
        if line.strip().startswith(("```", "~~~")):
            fenced = not fenced
            continue
        if fenced:
            continue
        if "<!--" in line:
            comment = "-->" not in line.split("<!--", 1)[1]
            line = line.split("<!--", 1)[0]
        elif comment:
            if "-->" in line:
                comment, line = False, line.split("-->", 1)[1]
            else:
                continue
        heading = HEADING_MD.match(line)
        if heading:
            section = heading.group(2).strip()
        line = re.sub(r"\]\([^)]*\)", "]", line)            # link targets
        line = re.sub(r'(?:src|href|srcset)="[^"]*"', " ", line)  # HTML attributes
        line = re.sub(r"https?://\S+", " ", line)
        yield number, line, section


def extract(path):
    path = Path(path)
    text = path.read_text(encoding="utf-8")
    lines = tex_lines(text) if path.suffix == ".tex" else md_lines(text)
    items = []
    for number, line, section in lines:
        for match in NUMBER.finditer(line):
            before = line[max(0, match.start() - 2):match.start()]
            if UNIT_AFTER.match(line, match.end()) or re.fullmatch(r"[A-Za-z0-9][-_]", before or "  "):
                continue  # a length (4pt) or part of an identifier (gpt-5-nano, jev-1.13.0)
            raw = match.group(0)
            value, percent = normalize(raw)
            start, end = max(0, match.start() - 50), min(len(line), match.end() + 50)
            items.append({"file": str(path), "line": number, "section": section, "raw": raw, "value": value,
                          "percent": percent, "context": " ".join(line[start:end].split())})
    return items


def missing_from(items, reference, tolerance=0.0):
    """Items whose value does not occur in reference (as stated, within tolerance)."""
    values = [item["value"] for item in reference]
    return [item for item in items if not any(abs(item["value"] - v) <= tolerance for v in values)]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("files", nargs="+", help=".tex or Markdown files")
    parser.add_argument("--compare", help="report numbers of FILES that this document does not state")
    parser.add_argument("--tolerance", type=float, default=0.0)
    parser.add_argument("--section", help="only items whose section contains this text")
    parser.add_argument("--format", choices=("jsonl", "table"), default="table")
    args = parser.parse_args(argv)
    items = [item for path in args.files for item in extract(path)]
    if args.section:
        items = [item for item in items if args.section.lower() in item["section"].lower()]
    if args.compare:
        items = missing_from(items, extract(args.compare), args.tolerance)
    if args.format == "jsonl":
        for item in items:
            print(json.dumps(item, ensure_ascii=False))
    else:
        print("| File:line | Section | Number | Context |\n| --- | --- | --- | --- |")
        for item in items:
            context = item["context"].replace("|", "\\|")
            print(f"| {Path(item['file']).name}:{item['line']} | {item['section']} | {item['raw']} | {context} |")
    print(f"{len(items)} numbers" + (f" not stated in {args.compare}" if args.compare else ""), file=sys.stderr)
    return 1 if args.compare and items else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(2)
