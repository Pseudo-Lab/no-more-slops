"""Number citations and write manuscript/paper.md from source.md and references.md.

In source.md, cite with `[@key]` or `[@a; @b; @c]`. Keys are numbered by first citation;
consecutive numbers collapse to ranges ([3–5]). A line `<!-- references -->` marks where the
numbered reference list goes. Unknown keys stop the build; uncited references are reported.
Also prints a body length estimate (characters and whitespace-separated tokens, excluding
front matter, abstracts, tables, captions and references, as the Frontiers word limit does).

Usage:
    uv run build.py [--src source.md] [--out paper.md]   (paths relative to manuscript/)
"""
import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MS = ROOT / "manuscript"
CITE = re.compile(r"\[(@[\w-]+(?:\s*;\s*@[\w-]+)*)\]")


def load_refs():
    refs = {}
    for line in (MS / "references.md").read_text(encoding="utf-8").splitlines():
        if m := re.match(r"^- ([\w-]+): (.+)$", line):
            refs[m[1]] = m[2]
    return refs


def ranges(nums):
    nums = sorted(set(nums))
    out, start = [], nums[0]
    for prev, cur in zip(nums, nums[1:] + [None]):
        if cur != prev + 1:
            out.append(str(start) if start == prev else
                       f"{start},{prev}" if prev == start + 1 else f"{start}–{prev}")
            start = cur
    return ",".join(out)


def body_length(md):
    lines = re.split(r"<!-- references -->|^## 저자 기여", md, flags=re.M)[0].splitlines()
    start = next(i for i, l in enumerate(lines) if re.match(r"^## \d", l))
    text = [l for l in lines[start:]
            if l.strip() and not l.startswith(("|", "#", "**표", "**그림", "주: ", "<!--"))]
    joined = " ".join(text)
    return len(re.sub(r"\s", "", joined)), len(joined.split())


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--src", default="source.md")
    parser.add_argument("--out", default="paper.md")
    args = parser.parse_args()
    refs = load_refs()
    src = (MS / args.src).read_text(encoding="utf-8")
    order = []
    for m in CITE.finditer(src):
        for key in re.findall(r"@([\w-]+)", m[1]):
            if key not in refs:
                raise SystemExit(f"unknown reference key: {key}")
            if key not in order:
                order.append(key)
    number = {k: i + 1 for i, k in enumerate(order)}
    out = CITE.sub(lambda m: "[" + ranges([number[k] for k in re.findall(r"@([\w-]+)", m[1])]) + "]", src)
    reflist = "\n".join(f"{i + 1}. {refs[k]}" for i, k in enumerate(order))
    out = out.replace("<!-- references -->", reflist)
    (MS / args.out).write_text(out, encoding="utf-8")
    chars, tokens = body_length(src)
    print(f"references cited: {len(order)}; body: {chars} chars, {tokens} tokens")


if __name__ == "__main__":
    main()
