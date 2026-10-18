#!/usr/bin/env python3
"""Count abstract numbers/sentences and new intro terms against SKILL.md step 3.

Input is the main .tex file (or a folder holding main.tex). \\input/\\include are
expanded, simple macros (\\newcommand, \\def) are expanded so number macros count.
Prints one JSON report. Exit code: 0 within criteria, 1 outside, 2 bad input.

Criteria (SKILL.md step 3): abstract numbers 1-3, new terms about 4 (max 5 here).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ABSTRACT_NUMBERS = (1, 3)
MAX_NEW_TERMS = 5  # "about 4"

INPUT = re.compile(r"\\(?:input|include)\s*\{([^}]+)\}")
MACRO_DEF = re.compile(
    r"\\(?:re)?newcommand\*?\s*\{?\\([A-Za-z]+)\}?\s*\{((?:[^{}]|\{[^{}]*\})*)\}"
    r"|\\def\\([A-Za-z]+)\s*\{((?:[^{}]|\{[^{}]*\})*)\}")
KEY_COMMANDS = re.compile(
    r"\\(?:cite[a-z]*|[cC]?ref|autoref|eqref|label|url|href|input|include|"
    r"includegraphics|begin|end)\*?(?:\[[^\]]*\])*\{[^}]*\}")
NUMBER = re.compile(r"(?<![A-Za-z\d])[-+]?\d+(?:[.,]\d+)*(?:\s*\\?%)?")
EMPH = re.compile(r"\\(?:emph|textit)\s*\{((?:[^{}]|\{[^{}]*\})*)\}")
ABBREV = re.compile(r"\b(?:e\.g|i\.e|et al|vs|cf|etc|Fig|Figs|Tab|Sec|Eq|resp|approx)\.",
                    re.IGNORECASE)


def strip_comments(text: str) -> str:
    return re.sub(r"(?<!\\)%.*", "", text)


def _resolve(m: re.Match, base: Path, depth: int) -> str:
    target = base / m[1].strip()
    if target.suffix != ".tex":
        target = target.with_name(target.name + ".tex")
    if not target.is_file():
        return ""
    text = strip_comments(target.read_text(encoding="utf-8", errors="replace"))
    if depth > 20:
        return text
    return INPUT.sub(lambda inner: _resolve(inner, base, depth + 1), text)


def load(main: Path) -> str:
    text = strip_comments(main.read_text(encoding="utf-8", errors="replace"))
    return INPUT.sub(lambda m: _resolve(m, main.parent, 0), text)


def macros(text: str) -> dict[str, str]:
    found = {}
    for m in MACRO_DEF.finditer(text):
        name, body = (m[1], m[2]) if m[1] else (m[3], m[4])
        if "#" not in body:  # only argument-free macros
            found[name] = body
    return found


def expand_macros(text: str, table: dict[str, str]) -> str:
    for _ in range(5):
        new = re.sub(r"\\([A-Za-z]+)(?![A-Za-z])(?:\{\})?",
                     lambda m: table.get(m[1], m[0]), text)
        if new == text:
            break
        text = new
    return text


def section(text: str, env: str | None = None, title: str | None = None) -> str:
    if env:
        m = re.search(rf"\\begin\{{{env}\}}(.*?)\\end\{{{env}\}}", text, re.S)
        return m[1] if m else ""
    m = re.search(rf"\\section\*?\s*\{{\s*{re.escape(title)}\s*\}}(.*?)(?=\\section\*?\s*\{{|"
                  r"\\end\{document\}|\Z)", text, re.S | re.IGNORECASE)
    return m[1] if m else ""


def plain(text: str) -> str:
    """Rough LaTeX to plain text: drop key commands, keep command arguments."""
    text = KEY_COMMANDS.sub(" ", text)
    text = re.sub(r"\\[A-Za-z]+\*?(?:\[[^\]]*\])?", " ", text)
    text = re.sub(r"[{}~]", " ", text).replace("\\%", "%")
    return re.sub(r"\s+", " ", text).strip()


def count_numbers(text: str) -> list[str]:
    return [m[0].strip() for m in NUMBER.finditer(plain(text))]


def count_sentences(text: str) -> int:
    body = ABBREV.sub(lambda m: m[0][:-1], plain(text))
    parts = [p for p in re.split(r"(?<=[.!?])\s+(?=[A-Z\d\"'(])", body) if p.strip()]
    return len(parts)


def new_terms(text: str) -> list[str]:
    seen, terms = set(), []
    for m in EMPH.finditer(text):
        term = plain(m[1])
        key = term.lower()
        if term and key not in seen:
            seen.add(key)
            terms.append(term)
    return terms


def report(main: Path, intro_title: str = "Introduction") -> dict:
    text = load(main)
    table = macros(text)
    abstract = expand_macros(section(text, env="abstract"), table)
    intro = section(text, title=intro_title)
    numbers = count_numbers(abstract)
    terms = new_terms(intro)
    lo, hi = ABSTRACT_NUMBERS
    result = {
        "abstract": {"found": bool(abstract.strip()), "numbers": len(numbers),
                     "number_values": numbers, "sentences": count_sentences(abstract),
                     "criterion": f"{lo}-{hi} numbers",
                     "ok": bool(abstract.strip()) and lo <= len(numbers) <= hi},
        "introduction": {"found": bool(intro.strip()), "new_terms": len(terms),
                         "terms": terms, "criterion": f"about 4 (max {MAX_NEW_TERMS})",
                         "ok": bool(intro.strip()) and len(terms) <= MAX_NEW_TERMS},
    }
    result["ok"] = result["abstract"]["ok"] and result["introduction"]["ok"]
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("tex", type=Path, help="main .tex file, or folder with main.tex")
    parser.add_argument("--intro-title", default="Introduction")
    args = parser.parse_args(argv)
    path = args.tex / "main.tex" if args.tex.is_dir() else args.tex
    if not path.is_file():
        print(json.dumps({"error": f"{path}: not found"}), file=sys.stderr)
        return 2
    result = report(path, args.intro_title)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
