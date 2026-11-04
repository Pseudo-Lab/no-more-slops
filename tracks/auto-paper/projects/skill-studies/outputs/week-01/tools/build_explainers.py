"""Render authored supporting Markdown with installed Typst; input text is escaped."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess
from build_papers import math, STUDIES

ROOT = Path(__file__).resolve().parents[1]


def text(value):
    value = value.replace("**", "").replace("`", "")
    return "#text(" + json.dumps(value, ensure_ascii=False) + ")"


def render(path):
    lines = path.read_text(encoding="utf-8").splitlines()
    korean = bool(re.search(r"[가-힣]", "".join(lines)))
    out = ['#set page(paper: "a4", margin: 22mm, numbering: "1")',
           '#set text(font: ("Malgun Gothic", "New Computer Modern"), size: 10.5pt, lang: "ko")'
           if korean else '#set text(font: "New Computer Modern", size: 11pt, lang: "en")',
           '#set par(justify: false, leading: 0.55em, spacing: 0.7em)',
           '#show heading: set text(weight: "bold")',
           '#show heading.where(level: 1): set text(size: 18pt)',
           '#show heading.where(level: 2): set text(size: 13pt)']
    i, code = 0, False
    while i < len(lines):
        line = lines[i]
        if line.strip() == "```typst-math":
            equations = []
            i += 1
            while i < len(lines) and lines[i].strip() != "```":
                if lines[i].strip():
                    equations.append(math(lines[i].strip()))
                i += 1
            assert i < len(lines), path.name + ": unclosed math fence"
            out.extend(equations)
            i += 1
            continue
        if line.startswith("```"):
            code = not code
            i += 1
            continue
        if not line.strip():
            out.append("")
        elif not code and line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                cells = [s.strip() for s in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r"[:\- ]+", s) for s in cells):
                    rows.append(cells)
                i += 1
            width = len(rows[0])
            assert all(len(r) == width for r in rows), path.name + ": ragged table"
            out.append('#block[\n#set text(size: 8.5pt)\n#table(columns: ' + str(width)
                       + ', stroke: none, inset: 4pt, table.hline(stroke: 0.6pt), table.header('
                       + ','.join('[' + text(c) + ']' for c in rows[0]) + '), table.hline(stroke: 0.3pt),'
                       + ','.join('[' + text(c) + ']' for row in rows[1:] for c in row)
                       + ', table.hline(stroke: 0.6pt))\n]')
            continue
        elif code:
            out.append('#block(inset: 5pt)[' + text(line) + ']')
        elif line.startswith("#"):
            level = len(line) - len(line.lstrip("#"))
            out.extend(["=" * level + " " + text(line[level:].strip()), ""])
        elif line.startswith("- ") or re.match(r"^\d+\. ", line):
            ordered = not line.startswith("- ")
            body = re.sub(r"^\d+\. ", "", line) if ordered else line[2:]
            body = re.sub(r"\[([^]]+)\]\(([^)]+)\)", r"\1 (\2)", body)
            out.append(("+ " if ordered else "- ") + text(body))
        else:
            # Keep content and links visible; Markdown control punctuation is removed only.
            line = re.sub(r"\[([^]]+)\]\(([^)]+)\)", r"\1 (\2)", line)
            line = line.replace("**", "").replace("`", "")
            out.append(text(line))
        i += 1
    target = ROOT / "explainers" / (path.parent.name + "_" + path.stem + ".typ")
    target.parent.mkdir(exist_ok=True)
    target.write_text("\n".join(out), encoding="utf-8")
    completed = subprocess.run(["typst", "compile", "--root", str(ROOT), str(target), str(target.with_suffix(".pdf"))],
                               capture_output=True, text=True, encoding="utf-8", timeout=60)
    if completed.returncode:
        raise RuntimeError(completed.stderr)
    return target.with_suffix(".pdf")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--study", choices=tuple(STUDIES))
    args = parser.parse_args()
    paths = [ROOT / STUDIES[args.study] / "EXPLAINER_KO.md"] if args.study else [ROOT / study / "EXPLAINER_KO.md" for study in STUDIES.values()]
    receipt_path = ROOT / "explainers/build_receipt.json"
    receipts = json.loads(receipt_path.read_text(encoding="utf-8")) if args.study and receipt_path.exists() else []
    receipts = [r for r in receipts if r["source"] not in {p.relative_to(ROOT).as_posix() for p in paths}]
    for path in paths:
        pdf = render(path)
        receipts.append({"source": path.relative_to(ROOT).as_posix(),
                         "source_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                         "pdf": pdf.relative_to(ROOT).as_posix(),
                         "pdf_sha256": hashlib.sha256(pdf.read_bytes()).hexdigest()})
        print(pdf.relative_to(ROOT).as_posix())
    receipt_path.write_text(json.dumps(receipts, ensure_ascii=False, indent=2), encoding="utf-8")
