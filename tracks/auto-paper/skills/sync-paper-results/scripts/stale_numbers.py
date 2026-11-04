#!/usr/bin/env python3
"""Find numbers written outside the generated blocks that a regeneration replaced.

Compare a paper before and after its AUTO blocks were regenerated (see auto_blocks.py).
Values that were in the old blocks and are in none of the new ones changed; where the new
paper's prose, captions or abstract, or another file such as README.md, still states one of
them outside its own AUTO blocks, that is probably a stale quote. Values are compared without
sign, percent sign or thousands separators. Short values such as 8 or 1.7 coincide too often
to be evidence, so only values with at least --min-digits significant digits are reported
(default 3: 74.6 and 1.37, not 0.35). Drawing code and lengths are skipped. Standard library
only; read-only.

  cp paper/main.tex /tmp/main.before.tex && make final
  python3 stale_numbers.py --before /tmp/main.before.tex --after paper/main.tex README.md

It cannot see derived claims (a difference, a ratio, "about four times"); recheck those by
hand. Exit status: 0 nothing found, 1 candidates found, 2 malformed markers or unreadable files.
"""

import argparse
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True  # no __pycache__ next to the skill
sys.path.insert(0, str(Path(__file__).resolve().parent))
from auto_blocks import blocks  # noqa: E402

NUMBER = re.compile(r"(?<![\w.])(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?(?![\w])")
UNIT_AFTER = re.compile(r"\s*(?:pt|cm|mm|in|em|ex|bp|px)\b")
TEX_SKIP = re.compile(r"\\(?:label|ref|eqref|autoref|cref|cite\w*|url|href|includegraphics|input|bibitem|fontsize|"
                      r"[vh]space|setlength)\*?(?:\[[^\]]*\])?(?:\{[^{}]*\})+")
TEX_SKIP_ENVS = ("tikzpicture", "pgfpicture", "axis", "groupplot", "verbatim", "lstlisting", "minted")
MD_SKIP = re.compile(r"\]\([^)]*\)|https?://\S+|(?:src|href)=\"[^\"]*\"")


def values(text):
    """(value, match) for each number in text, leaving out lengths and identifiers like gpt-5."""
    for match in NUMBER.finditer(text):
        before = text[max(0, match.start() - 2):match.start()]
        if UNIT_AFTER.match(text, match.end()) or re.fullmatch(r"[A-Za-z0-9][-_]", before):
            continue
        yield float(match.group().replace(",", "")), match


def digits(number):
    """Significant digits as written: 74.6 -> 3, 0.35 -> 2, 4,980 -> 4."""
    return len(re.sub(r"[^0-9]", "", number).lstrip("0"))


def generated_values(text):
    """Every value inside the AUTO blocks of a document."""
    return {value for start, end, _, _ in blocks(text).values() for value, _ in values(text[start:end])}


def written_lines(path, text):
    """(line number, text) outside AUTO blocks and their markers; LaTeX body only, without comments."""
    inside = {line for _, _, begin, end in blocks(text).values() for line in range(begin, end + 1)}
    tex = path.suffix == ".tex"
    body = not (tex and "\\begin{document}" in text)
    skipping = []
    for number, line in enumerate(text.splitlines(), 1):
        if not body:
            body = "\\begin{document}" in line
            continue
        if number in inside:
            continue
        if not tex:
            yield number, MD_SKIP.sub(" ", line)
            continue
        line = re.split(r"(?<!\\)%", line, maxsplit=1)[0]
        skipping += [env for env in TEX_SKIP_ENVS if f"\\begin{{{env}}}" in line]
        if skipping:
            skipping = [env for env in skipping if f"\\end{{{env}}}" not in line]
            continue
        yield number, TEX_SKIP.sub(" ", line)


def stale(before, after, others=(), min_digits=3):
    """Candidates as (file, line, number, context): replaced values still written somewhere."""
    old_text, new_text = Path(before).read_text(encoding="utf-8"), Path(after).read_text(encoding="utf-8")
    new = generated_values(new_text)
    replaced = generated_values(old_text) - new
    found = []
    for path in [Path(after), *map(Path, others)]:
        text = new_text if path == Path(after) else path.read_text(encoding="utf-8")
        for number, line in written_lines(path, text):
            for value, match in values(line):
                if value in replaced and digits(match.group()) >= min_digits:
                    context = " ".join(line[max(0, match.start() - 50):match.end() + 50].split())
                    found.append((str(path), number, match.group(), context))
    return found


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--before", required=True, help="the paper before regenerating its blocks")
    parser.add_argument("--after", required=True, help="the paper after regenerating its blocks")
    parser.add_argument("others", nargs="*", help="more files to scan outside their AUTO blocks (README.md, docs)")
    parser.add_argument("--min-digits", type=int, default=3, help="report values with this many significant digits")
    args = parser.parse_args(argv)
    found = stale(args.before, args.after, args.others, args.min_digits)
    for path, line, number, context in found:
        print(f"{path}:{line}: {number}\t{context}")
    print(f"{len(found)} replaced value(s) still written outside the generated blocks", file=sys.stderr)
    return 1 if found else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(2)
