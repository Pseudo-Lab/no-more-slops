"""Verify exact pages, complete authored prose, citations, source pins and fonts."""
from hashlib import sha256
import json
from pathlib import Path
import re
import unicodedata

import fitz
from PIL import Image, ImageDraw
from build_papers import ROOT, STUDIES


def normalized(text):
    return re.sub(r"[^\w]", "", unicodedata.normalize("NFKC", text), flags=re.UNICODE).replace("_", "").casefold()


def prose_items(data):
    items = [data["abstract"], data["status"]]
    for page in data["pages"]:
        for section in page["sections"]:
            items.append(section["heading"])
            items.extend(section.get("paragraphs", []))
            items.extend(section.get("bullets", []))
            if "table" in section:
                table = section["table"]
                items.extend(table["headers"])
                items.extend(c for row in table["rows"] for c in row)
                items.append(table["caption"])
            if "algorithm" in section:
                items.extend(section["algorithm"]["lines"])
                items.append(section["algorithm"]["caption"])
    items.extend(r["text"] for r in data["references"])
    return items


def main():
    receipt = json.loads((ROOT / "validation/typesetting_receipt.json").read_text(encoding="utf-8"))
    preview = ROOT / "preview"
    preview.mkdir(exist_ok=True)
    sheet = Image.new("RGB", (4 * 414, 3 * 610), "#e8e8e8")
    draw = ImageDraw.Draw(sheet)
    results = {}
    for row, (key, study) in enumerate(STUDIES.items()):
        entry = receipt[key]
        source = ROOT / entry["source"]
        pdf = ROOT / entry["pdf"]
        assert sha256(source.read_bytes()).hexdigest() == entry["source_sha256"], "source changed after typesetting"
        assert sha256(pdf.read_bytes()).hexdigest() == entry["pdf_sha256"], "PDF changed after typesetting"
        data = json.loads(source.read_text(encoding="utf-8"))
        with fitz.open(pdf) as doc:
            assert len(doc) == 4, key + ": must have exactly four pages"
            fonts = {f[0]: f for page in doc for f in page.get_fonts()}
            assert all(doc.extract_font(x)[3] and f[2] != "Type3" for x, f in fonts.items()), key + ": fonts"
            assert any("NewCMMath" in f[3] for f in fonts.values()), key + ": mathematical font missing"
            assert not doc.is_encrypted and doc.embfile_count() == 0
            texts = []
            for index, page in enumerate(doc):
                text = page.get_text(sort=True)
                assert len(text) > 900 and "\ufffd" not in text and "\x00" not in text, key + ": blank/replacement text"
                assert normalized(data["pages"][index]["sections"][0]["heading"]) in normalized(text), key + ": semantic page slipped"
                for w in page.get_text("words"):
                    assert w[0] >= -0.5 and w[1] >= -0.5 and w[2] <= page.rect.width + 0.5 and w[3] <= page.rect.height + 0.5, (key, index, w[4])
                for link in page.get_links():
                    if link["kind"] == fitz.LINK_GOTO:
                        assert 0 <= link["page"] < len(doc), key + ": broken citation"
                texts.append(text)
                picture = preview / f"{key}_p{index+1:02d}.png"
                page.get_pixmap(matrix=fitz.Matrix(1.2, 1.2), alpha=False).save(picture)
                thumb = Image.open(picture).convert("RGB")
                thumb.thumbnail((400, 570))
                sheet.paste(thumb, (index * 414 + 7, row * 610 + 30))
                draw.text((index * 414 + 10, row * 610 + 10), f"{key} - {index+1}", fill="black")
            joined = "\n".join(texts)
            corpus = normalized(joined)
            missing = [p for p in prose_items(data) if normalized(p) not in corpus]
            assert not missing, (key, "prose lost", missing)
            links = {l["uri"] for page in doc for l in page.get_links() if l["kind"] == fitz.LINK_URI}
            assert {r["url"] for r in data["references"]} <= links, key + ": reference link missing"
            assert "NR" in joined and "research" in joined.casefold(), key + ": status missing"
            (preview / (key + "_extracted.txt")).write_text(joined, encoding="utf-8")
            results[key] = {"pages": len(doc), "source_sha256": entry["source_sha256"], "pdf_sha256": entry["pdf_sha256"],
                "prose_items_verified": len(prose_items(data)), "prose_omitted": 0, "reference_urls": len(links),
                "embedded_fonts": [f[3] for f in fonts.values()], "semantic_pages_match": True,
                "page_characters": [len(t) for t in texts], "text_inside_pages": True, "scientific_performance": "NR"}
    sheet.save(preview / "Three_Papers_12_Pages.png")
    (ROOT / "validation/paper_verification.json").write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({k: {"pages": v["pages"], "prose_omitted": 0} for k, v in results.items()}))


if __name__ == "__main__":
    main()
