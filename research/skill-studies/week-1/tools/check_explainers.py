"""Validate generated document bounds, embedded fonts and nonempty pages."""
from pathlib import Path
import hashlib
import json
import re
import unicodedata

import fitz

ROOT = Path(__file__).resolve().parents[1]


def normalized(value):
    return re.sub(r"[^\w]", "", unicodedata.normalize("NFKC", value)).replace("_", "").casefold()


def page_body(page):
    lines = page.get_text(sort=True).rstrip().splitlines()
    assert lines and lines[-1].strip() == str(page.number + 1), "numbered footer not identified"
    return "\n".join(lines[:-1])


def prose_lines(source):
    math_block = False
    for line in source.read_text(encoding="utf-8").splitlines():
        if line.strip() == "```typst-math":
            math_block = True
            continue
        if line.startswith("```"):
            math_block = False
            continue
        if not line.strip() or math_block:
            continue
        if line.startswith("|"):
            values = [x.strip() for x in line.strip().strip("|").split("|")]
            if all(re.fullmatch(r"[:\- ]+", x) for x in values):
                continue
        else:
            values = [re.sub(r"^#+\s*|^-\s*|^\d+\.\s*", "", line.strip())]
        for value in values:
            value = re.sub(r"\[([^]]+)\]\(([^)]+)\)", r"\1 (\2)", value).replace("**", "").replace("`", "")
            if len(normalized(value)) >= 10:
                yield value


def main():
    receipts = json.loads((ROOT / "explainers/build_receipt.json").read_text(encoding="utf-8"))
    for receipt in receipts:
        assert hashlib.sha256((ROOT / receipt["source"]).read_bytes()).hexdigest() == receipt["source_sha256"], "document source changed after compile"
        assert hashlib.sha256((ROOT / receipt["pdf"]).read_bytes()).hexdigest() == receipt["pdf_sha256"], "compiled PDF changed"
    results = []
    for path in sorted((ROOT / "explainers").glob("*.pdf")):
        with fitz.open(path) as doc:
            assert len(doc) > 0 and not doc.is_encrypted
            outside = []
            for page in doc:
                assert len(page.get_text()) > 40, path.name + ": blank page"
                assert "\ufffd" not in page.get_text(), path.name + ": replacement glyph"
                for word in page.get_text("words"):
                    if word[0] < -0.5 or word[1] < -0.5 or word[2] > page.rect.width + 0.5 or word[3] > page.rect.height + 0.5:
                        outside.append({"page": page.number + 1, "text": word[4]})
            fonts = {f[0]: f for page in doc for f in page.get_fonts()}
            assert all(doc.extract_font(x)[3] and f[2] != "Type3" for x, f in fonts.items()), path.name + ": font embedding"
            assert not outside, (path.name, outside)
            receipt = next(x for x in receipts if x["pdf"] == path.relative_to(ROOT).as_posix())
            full_text = "\n".join(page_body(p) for p in doc)
            corpus = normalized(full_text)
            prose = list(prose_lines(ROOT / receipt["source"]))
            missing = [line for line in prose if normalized(line) not in corpus]
            if missing:
                for line in missing[:3]:
                    expected = normalized(line)
                    start = corpus.find(expected[:40])
                    actual = corpus[start:start+len(expected)+80] if start >= 0 else "prefix not found"
                    offset = next((i for i, (a, b) in enumerate(zip(expected, actual)) if a != b), 0)
                    print(json.dumps({"file": path.name, "mismatch": offset,
                        "expected": expected[max(0, offset-15):offset+55],
                        "actual": actual[max(0, offset-15):offset+55]}, ensure_ascii=False))
            assert not missing, (path.name, "guide prose missing", missing[:3])
            results.append({"file": path.relative_to(ROOT).as_posix(), "pages": len(doc),
                            "characters": sum(len(p.get_text()) for p in doc), "fonts_embedded": True,
                            "outside_page": outside, "prose_items_verified": len(prose), "prose_omitted": 0})
            doc[0].get_pixmap(matrix=fitz.Matrix(1.2, 1.2), alpha=False).save(path.with_suffix(".png"))
    assert results, "No supporting PDFs found"
    (ROOT / "explainers" / "verification.json").write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(results, ensure_ascii=False))


if __name__ == "__main__":
    main()
