#!/usr/bin/env python3
"""Check a LaTeX build folder for page-limit and rendering problems.

Reads the .log and .aux files in a build folder (standard library only) and
prints one JSON report. Exit code: 0 no problems, 1 problems found, 2 bad input.

Example:
    python3 check_build.py draft/build --page-limit 4 --src draft
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

LOG_WIDTH = 79  # TeX wraps log lines at max_print_line (default 79)

OVERFULL = re.compile(
    r"^(Overfull|Underfull) \\[hv]box \((?:([\d.]+)pt too (?:wide|high)|badness (\d+))\)"
    r".*?(?:lines? (\d+)(?:--(\d+))?)?\s*$")
UNDEF_REF = re.compile(r"Reference [`'](.+?)' on page (\d+) undefined(?: on input line (\d+))?")
UNDEF_CITE = re.compile(r"Citation [`'](.+?)' on page (\d+) undefined(?: on input line (\d+))?")
FLOAT_CHANGED = re.compile(r"[`']!?h' float specifier changed to [`'](!?\w+)'")
NEWLABEL = re.compile(r"\\newlabel\{([^}]*)\}\{\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}\{([^{}]*)\}")

TODO = re.compile(r"\\todo\s*[\[{]|\bTODO\b|\bXXX\b")
PERSONAL_PATH = re.compile(r"/Users/|[A-Za-z]:\\\\?Users\\|~/", re.IGNORECASE)


def unwrap_log(text: str) -> list[str]:
    """Join log lines that TeX hard-wrapped at LOG_WIDTH characters."""
    out: list[str] = []
    buf = ""
    for line in text.splitlines():
        buf += line
        if len(line) != LOG_WIDTH:
            out.append(buf)
            buf = ""
    if buf:
        out.append(buf)
    return out


def parse_log(text: str) -> dict:
    boxes = {"overfull": [], "underfull": []}
    refs, cites, floats = [], [], []
    for line in unwrap_log(text):
        m = OVERFULL.match(line)
        if m:
            kind, pt, badness, start, end = m.groups()
            entry = {
                "lines": [int(start), int(end or start)] if start else None,
                "pt": float(pt) if pt else None,
                "badness": int(badness) if badness else None,
            }
            boxes[kind.lower()].append(entry)
            continue
        for pattern, bucket in ((UNDEF_REF, refs), (UNDEF_CITE, cites)):
            m = pattern.search(line)
            if m:
                bucket.append({"key": m[1], "page": int(m[2]),
                               "input_line": int(m[3]) if m[3] else None})
        m = FLOAT_CHANGED.search(line)
        if m:
            floats.append(m[1])
    return {
        "overfull": {"count": len(boxes["overfull"]), "items": boxes["overfull"]},
        "underfull": {"count": len(boxes["underfull"]), "items": boxes["underfull"]},
        "undefined_references": {"count": len(refs), "items": refs},
        "undefined_citations": {"count": len(cites), "items": cites},
        "h_float_changed": {"count": len(floats), "changed_to": floats},
    }


def label_pages(aux_text: str) -> dict[str, str]:
    return {m[1]: m[2] for m in NEWLABEL.finditer(aux_text)}


def page_check(labels: dict[str, str], end_label: str, page_limit: int) -> dict:
    page = labels.get(end_label)
    number = int(page) if page is not None and page.isdigit() else None
    return {
        "end_label": end_label,
        "end_page": number if number is not None else page,
        "page_limit": page_limit,
        "within_limit": number is not None and number <= page_limit,
        "found": page is not None,
    }


def scan_sources(src: Path) -> dict:
    todos, paths = [], []
    for tex in sorted(src.rglob("*.tex")):
        rel = tex.relative_to(src).as_posix()
        for no, line in enumerate(tex.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            comment = re.search(r"(?<!\\)%", line)
            cut = comment.start() if comment else len(line)
            for pattern, bucket in ((TODO, todos), (PERSONAL_PATH, paths)):
                for m in pattern.finditer(line):
                    bucket.append({"file": rel, "line": no, "match": m[0].rstrip("{["),
                                   "in_comment": m.start() >= cut})
    return {"todo": {"count": len(todos), "items": todos},
            "personal_paths": {"count": len(paths), "items": paths}}


def read_all(folder: Path, suffix: str) -> str:
    return "\n".join(p.read_text(encoding="utf-8", errors="replace")
                     for p in sorted(folder.glob(f"*{suffix}")))


def check(build: Path, page_limit: int, end_label: str, src: Path | None = None) -> dict:
    log_text, aux_text = read_all(build, ".log"), read_all(build, ".aux")
    if not log_text or not aux_text:
        raise FileNotFoundError(f"{build}: needs at least one .log and one .aux file")
    report = {"pages": page_check(label_pages(aux_text), end_label, page_limit)}
    report.update(parse_log(log_text))
    if src is not None:
        report["source"] = scan_sources(src)
    problems = []
    if not report["pages"]["within_limit"]:
        problems.append("page_limit")
    for key in ("overfull", "underfull", "undefined_references", "undefined_citations",
                "h_float_changed"):
        if report[key]["count"]:
            problems.append(key)
    if src is not None:
        problems += [k for k in ("todo", "personal_paths") if report["source"][k]["count"]]
    report["problems"] = problems
    report["ok"] = not problems
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("build", type=Path, help="LaTeX build folder with .log and .aux")
    parser.add_argument("--page-limit", type=int, required=True)
    parser.add_argument("--end-label", default="sec:end-of-body")
    parser.add_argument("--src", type=Path, help="manuscript .tex folder to scan")
    args = parser.parse_args(argv)
    try:
        if args.src is not None and not args.src.is_dir():
            raise FileNotFoundError(f"{args.src}: not a folder")
        report = check(args.build, args.page_limit, args.end_label, args.src)
    except (FileNotFoundError, NotADirectoryError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 2
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
