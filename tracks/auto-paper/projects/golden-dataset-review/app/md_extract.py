"""Convert manuscript/source.md to the extract format of the toego:revise skill.

toego's own extractor reads .hwp files. This writes the same files from Markdown so that its
lint_ko.py and build_html.py can run on this manuscript unchanged:
    paragraphs.json  [{"id": "2.1-P1", "section": "2.1", "text": ..., "sentences": [...]}]
    tables.json      [{"caption": ..., "rows": [[...], ...]}]
    captions.json    ["표 1. ...", ...]
Abstract paragraphs get section "abs" (Korean) and "abs-en". Citations stay as [@key].

Usage:
    uv run md_extract.py OUT_DIR [--src ../manuscript/source.md]
"""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SENT_END = re.compile(r"(?<=[다요음함]\.)\s+|(?<=\.)\s+(?=[A-Z])")


def sentences(text):
    return [s.strip() for s in SENT_END.split(text) if s.strip()]


def extract(md):
    lines = md.splitlines()
    if lines and lines[0] == "---":
        lines = lines[lines.index("---", 1) + 1:]
    paras, tables, captions = [], [], []
    section, count, i = None, 0, 0
    while i < len(lines):
        line = lines[i].strip()
        i += 1
        if not line or line.startswith("<!--"):
            continue
        if m := re.match(r"^#{2,3}\s+(.*)$", line):
            title = m[1]
            num = re.match(r"^(\d+(?:\.\d+)?)\.?\s", title)
            section = (num[1] if num else {"초록": "abs", "Abstract": "abs-en"}.get(title, title))
            count = 0
            continue
        if line.startswith("**표") or line.startswith("**그림"):
            captions.append(re.sub(r"\*\*", "", line))
            rows = []
            while i < len(lines) and (lines[i].startswith("|") or not lines[i].strip()):
                if lines[i].startswith("|") and not re.match(r"^\|\s*-", lines[i]):
                    rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
                if rows and i < len(lines) and not lines[i].startswith("|"):
                    break
            tables.append({"caption": captions[-1], "rows": rows})
            continue
        if line.startswith("|") or section is None:
            continue
        count += 1
        paras.append({"id": f"{section}-P{count}", "section": section, "text": line,
                      "sentences": sentences(line)})
    return paras, tables, captions


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("out", type=Path)
    parser.add_argument("--src", type=Path, default=ROOT / "manuscript" / "source.md")
    args = parser.parse_args()
    paras, tables, captions = extract(args.src.read_text(encoding="utf-8"))
    args.out.mkdir(parents=True, exist_ok=True)
    for name, data in (("paragraphs", paras), ("tables", tables), ("captions", captions)):
        (args.out / f"{name}.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(paras)} paragraphs, {len(tables)} tables -> {args.out}")


if __name__ == "__main__":
    main()
