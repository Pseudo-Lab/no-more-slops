"""Typeset four semantic pages per manuscript; never truncate authored prose."""
from hashlib import sha256
import argparse
import json
from pathlib import Path
import re
import subprocess

import fitz

ROOT = Path(__file__).resolve().parents[1]
STUDIES = {"SkillMerge": "skillmerge", "SecondChance": "second_chance", "ProbeFlow": "probeflow"}
CITATION = re.compile(r"\[([1-9][0-9]*(?:\s*[,–-]\s*[1-9][0-9]*)*)\]")


def literal(value):
    return json.dumps(value, ensure_ascii=False)


def content(value):
    parts, start = [], 0
    for match in CITATION.finditer(value):
        parts.append("#text(" + literal(value[start:match.start()]) + ")")
        first = re.match(r"[1-9][0-9]*", match.group(1)).group()
        parts.append("#link(<bib" + first + ">)[#text(" + literal(match.group()) + ")]")
        start = match.end()
    parts.append("#text(" + literal(value[start:]) + ")")
    return "".join(parts)


def math(equation):
    if not isinstance(equation, str) or any(token in equation for token in ("#", "$", "\\")):
        raise ValueError("equation must be native Typst math without scripting or LaTeX escapes")
    return "$ " + equation + " $"


def validate(data):
    assert data["id"] in STUDIES and len(data["pages"]) == 4
    assert data["abstract"] and data["status"] and "NR" in data["status"]
    assert data["contributions"] and data["references"]
    numbers = {r["number"] for r in data["references"]}
    assert len(numbers) == len(data["references"]) and all(type(n) is int and n > 0 for n in numbers)
    assert all(r["url"].startswith("https://") and r["claim_scope"] for r in data["references"])
    for page in data["pages"]:
        assert page["heading"] and page["sections"]
        for section in page["sections"]:
            assert section["heading"] and isinstance(section.get("paragraphs", []), list)
            for equation in section.get("equations", []):
                math(equation)
            if "table" in section:
                table = section["table"]
                assert table["headers"] and all(len(row) == len(table["headers"]) for row in table["rows"])
    for match in CITATION.finditer(json.dumps(data["pages"], ensure_ascii=False) + data["abstract"]):
        assert {int(n) for n in re.findall(r"\d+", match.group(1))} <= numbers, "unresolved citation"


def compile_one(key):
    source = ROOT / STUDIES[key] / "paper.json"
    data = json.loads(source.read_text(encoding="utf-8"))
    validate(data)
    title = data["title"] + (": " + data["subtitle"] if data.get("subtitle") else "")
    lines = ['#import "preprint.typ": *', "#show: scholarly-paper.with(title: " + literal(title) + ")",
             "#title-block(" + literal(title) + ", " + literal(data["status"]) + ")",
             "#abstract-block[" + content(data["abstract"]) + "]", ""]
    for page_index, page in enumerate(data["pages"]):
        if page_index:
            lines.extend(["#pagebreak()", ""])
        for section in page["sections"]:
            lines.extend(["= " + content(section["heading"]), ""])
            for paragraph in section.get("paragraphs", []):
                lines.extend([content(paragraph), ""])
            for bullet in section.get("bullets", []):
                lines.append("- " + content(bullet))
            lines.append("")
            for equation in section.get("equations", []):
                lines.extend([math(equation), ""])
            if "table" in section:
                table = section["table"]
                headers = "(" + ",".join("[" + content(c) + "]" for c in table["headers"]) + ",)"
                rows = "(" + ",".join("(" + ",".join("[" + content(c) + "]" for c in row) + ",)" for row in table["rows"]) + ",)"
                lines.extend(["#planned-table(" + headers + ", " + rows + ", " + literal(table["caption"]) + ")", ""])
            if "algorithm" in section:
                algorithm = section["algorithm"]
                entries = "(" + ",".join("[" + content(line) + "]" for line in algorithm["lines"]) + ",)"
                lines.extend(["#algorithm-block(" + entries + ", " + literal(algorithm["caption"]) + ")", ""])
    lines.extend(["= References", ""])
    for reference in data["references"]:
        lines.append("#bibliography-entry(" + str(reference["number"]) + ", [#text(" + literal(reference["text"]) + ")], "
                     + literal(reference["url"]) + ") <bib" + str(reference["number"]) + ">")
    path = ROOT / "papers" / (key + "_Week1_4p.typ")
    path.write_text("\n".join(lines), encoding="utf-8")
    result = subprocess.run(["typst", "compile", "--ignore-system-fonts", "--root", str(ROOT), str(path), str(path.with_suffix(".pdf"))],
                            capture_output=True, text=True, encoding="utf-8", timeout=60)
    logs = ROOT / "validation"
    logs.mkdir(exist_ok=True)
    (logs / (key + "_typeset.log")).write_text(result.stdout + result.stderr, encoding="utf-8")
    if result.returncode:
        raise RuntimeError(key + ": " + result.stderr)
    with fitz.open(path.with_suffix(".pdf")) as doc:
        return {"source": source.relative_to(ROOT).as_posix(), "source_sha256": sha256(source.read_bytes()).hexdigest(),
                "typst": path.relative_to(ROOT).as_posix(), "pdf": path.with_suffix(".pdf").relative_to(ROOT).as_posix(),
                "pdf_sha256": sha256(path.with_suffix(".pdf").read_bytes()).hexdigest(), "pages": len(doc),
                "semantic_page_headings": [p["heading"] for p in data["pages"]], "authored_prose_truncated": False}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--study", choices=tuple(STUDIES))
    args = parser.parse_args()
    receipt_path = ROOT / "validation/typesetting_receipt.json"
    results = json.loads(receipt_path.read_text(encoding="utf-8")) if args.study and receipt_path.exists() else {}
    results.update({key: compile_one(key) for key in ([args.study] if args.study else STUDIES)})
    receipt_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({key: {"pages": result["pages"]} for key, result in results.items()}))
