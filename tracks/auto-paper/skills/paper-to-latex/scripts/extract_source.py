#!/usr/bin/env python3
"""Extract a source paper into working files for conversion.

Usage:
    python extract_source.py <paper_file> <project_dir>

Never modifies <paper_file>. Writes only under <project_dir>/_conversion/:

    source_manifest.json   format, inventory, warnings, generated files
    source_plain.txt       plain-text rendering used later by compare_content.py
    pandoc_draft.tex       (md/docx/tex) pandoc's LaTeX rendering - a DRAFT to
                           copy text from, never shipped as-is
    source_markdown.md     (docx) pandoc markdown rendering, easier to read
    source_layout.txt      (pdf) pdftotext -layout output
    media/                 (docx/pdf) extracted embedded images

The inventory (headings, citations, numbers, figures, tables, equations,
footnotes) is a checklist for the conversion; it is heuristic and must be
confirmed by reading the source.
"""
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass

NUM_RE = re.compile(r"(?<![\w.])[-\u2212]?\d[\d,]*(?:\.\d+)?%?")


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8",
                          errors="replace", timeout=600, **kw)


def pandoc(args):
    if not shutil.which("pandoc"):
        return None, "pandoc not found"
    r = run(["pandoc", *args])
    return (r.returncode == 0), (r.stderr.strip() or "")


def md_inventory(text):
    inv = {}
    inv["headings"] = [m.group(0).strip() for m in re.finditer(r"(?m)^#{1,6}\s+.+$", text)]
    inv["numeric_citations"] = sorted(set(re.findall(r"\[(\d+(?:\s*[,\u2013-]\s*\d+)*)\]", text)))
    inv["pandoc_citations"] = sorted(set(re.findall(r"@([\w:.\-/]+)", text)))
    inv["images"] = [(alt, path.strip().strip("<>")) for alt, path in
                     re.findall(r'!\[([^\]]*)\]\(\s*(<[^>]+>|[^)"]+?)\s*(?:"[^"]*")?\s*\)', text)]
    inv["display_math_blocks"] = len(re.findall(r"\$\$", text)) // 2 + len(re.findall(r"\\begin\{(equation|align|gather)", text))
    inv["inline_math_approx"] = len(re.findall(r"(?<!\$)\$(?!\$)[^$\n]+?\$", text))
    inv["pipe_table_rows"] = len(re.findall(r"(?m)^\s*\|.*\|\s*$", text))
    inv["table_captions"] = re.findall(r"(?mi)^\s*\**(Table\s+\d+[.:].*)$", text)
    inv["figure_captions"] = re.findall(r"(?mi)^\s*\**(Fig(?:ure)?\.?\s+\d+[.:].*)$", text)
    inv["footnotes"] = len(re.findall(r"(?m)^\[\^[^\]]+\]:", text))
    inv["reference_list_entries"] = len(re.findall(r"(?m)^\s*(?:\[\d+\]|\d+\.)\s+\S", text.split("References")[-1])) if re.search(r"(?mi)^#+\s*(\d+\s*)?references", text) else 0
    return inv


def tex_inventory(text):
    inv = {}
    inv["documentclass"] = re.findall(r"\\documentclass(?:\[[^\]]*\])?\{([^}]*)\}", text)
    inv["packages"] = sorted({p.strip() for grp in re.findall(r"\\usepackage(?:\[[^\]]*\])?\{([^}]*)\}", text) for p in grp.split(",")})
    inv["inputs"] = re.findall(r"\\(?:input|include)\{([^}]*)\}", text)
    inv["headings"] = re.findall(r"\\((?:sub)*section|paragraph)\*?\{([^}]*)\}", text)
    inv["cite_keys"] = sorted({k.strip() for grp in re.findall(r"\\[a-zA-Z]*cite[a-zA-Z]*\*?(?:\[[^\]]*\]){0,2}\{([^}]*)\}", text) for k in grp.split(",")})
    inv["graphics"] = re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]*)\}", text)
    inv["bibliography"] = re.findall(r"\\(?:bibliography|addbibresource)\{([^}]*)\}", text)
    inv["tables"] = len(re.findall(r"\\begin\{table\*?\}", text))
    inv["figures"] = len(re.findall(r"\\begin\{figure\*?\}", text))
    inv["equations"] = len(re.findall(r"\\begin\{(equation|align|gather|multline|eqnarray)\*?\}", text)) + len(re.findall(r"\\\[", text))
    inv["footnotes"] = len(re.findall(r"\\footnote\{", text))
    inv["thebibliography"] = "\\begin{thebibliography}" in text
    return inv


def check_tex_packages(packages):
    if not shutil.which("kpsewhich"):
        return {}
    missing = []
    for p in packages:
        r = run(["kpsewhich", f"{p}.sty"])
        if not r.stdout.strip():
            missing.append(p)
    return {"packages_not_found_locally": missing}


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    src = Path(sys.argv[1]).resolve()
    proj = Path(sys.argv[2]).resolve()
    if not src.is_file():
        sys.exit(f"source not found: {src}")
    if proj == src.parent and src.suffix.lower() == ".tex" and (proj / "main.tex") == src:
        sys.exit("refusing: project dir would overwrite the source main.tex")
    work = proj / "_conversion"
    work.mkdir(parents=True, exist_ok=True)
    ext = src.suffix.lower()
    manifest = {"source": str(src), "format": ext.lstrip("."), "warnings": [], "files": {}}
    plain = work / "source_plain.txt"

    if ext in (".md", ".markdown"):
        text = src.read_text(encoding="utf-8", errors="replace")
        manifest["inventory"] = md_inventory(text)
        fmt = "markdown+tex_math_dollars+pipe_tables+footnotes+raw_tex"
        ok, err = pandoc(["-f", fmt, "-t", "latex", "--wrap=preserve", str(src), "-o", str(work / "pandoc_draft.tex")])
        manifest["files"]["pandoc_draft"] = str(work / "pandoc_draft.tex") if ok else None
        if err:
            manifest["warnings"].append(f"pandoc(latex): {err}")
        ok, err = pandoc(["-f", fmt, "-t", "plain", "--wrap=none", str(src), "-o", str(plain)])
        if not ok:
            plain.write_text(text, encoding="utf-8")
            manifest["warnings"].append("pandoc plain failed; source_plain.txt is the raw markdown")
        for _alt, path in manifest["inventory"]["images"]:
            if re.match(r"https?://", path):
                manifest["warnings"].append(f"remote image (not downloaded): {path}")
            elif not (src.parent / path).exists():
                manifest["warnings"].append(f"referenced image missing on disk: {path}")

    elif ext == ".docx":
        media = work / "media"
        ok, err = pandoc(["-f", "docx", "-t", "latex", "--wrap=preserve", f"--extract-media={media}", str(src), "-o", str(work / "pandoc_draft.tex")])
        if ok is None or not ok:
            manifest["warnings"].append(f"docx conversion failed: {err}")
        pandoc(["-f", "docx", "-t", "markdown", "--wrap=none", str(src), "-o", str(work / "source_markdown.md")])
        pandoc(["-f", "docx", "-t", "plain", "--wrap=none", str(src), "-o", str(plain)])
        mdp = work / "source_markdown.md"
        manifest["inventory"] = md_inventory(mdp.read_text(encoding="utf-8", errors="replace")) if mdp.exists() else {}
        manifest["files"]["media"] = sorted(str(p) for p in media.rglob("*") if p.is_file()) if media.exists() else []
        if err:
            manifest["warnings"].append(f"pandoc: {err}")

    elif ext == ".tex":
        text = src.read_text(encoding="utf-8", errors="replace")
        for inc in re.findall(r"\\(?:input|include)\{([^}]*)\}", text):
            p = src.parent / inc
            p = p if p.suffix else p.with_suffix(".tex")
            if p.exists():
                text += "\n" + p.read_text(encoding="utf-8", errors="replace")
            else:
                manifest["warnings"].append(f"\\input target missing: {inc}")
        manifest["inventory"] = tex_inventory(text)
        manifest["inventory"].update(check_tex_packages(manifest["inventory"]["packages"]))
        for cls in manifest["inventory"]["documentclass"]:
            if cls not in ("article", "report", "book", "IEEEtran", "acmart", "llncs", "revtex4-2", "elsarticle", "amsart"):
                if not (src.parent / f"{cls}.cls").exists():
                    manifest["warnings"].append(f"document class '{cls}' not next to source; verify it is available")
        for g in manifest["inventory"]["graphics"]:
            cands = [src.parent / g] + [src.parent / (g + e) for e in (".pdf", ".png", ".jpg", ".jpeg", ".eps")]
            if not any(c.exists() for c in cands):
                manifest["warnings"].append(f"graphic missing next to source: {g}")
        ok, err = pandoc(["-f", "latex", "-t", "plain", "--wrap=none", str(src), "-o", str(plain)])
        if not ok:
            plain.write_text(text, encoding="utf-8")
            manifest["warnings"].append("pandoc could not render the .tex to plain text; source_plain.txt is raw TeX (compare will be noisy)")

    elif ext == ".pdf":
        if not shutil.which("pdftotext"):
            sys.exit("pdftotext not available: cannot extract a PDF source reliably")
        run(["pdftotext", "-layout", str(src), str(work / "source_layout.txt")])
        run(["pdftotext", str(src), str(plain)])
        pages = None
        if shutil.which("pdfinfo"):
            m = re.search(r"Pages:\s+(\d+)", run(["pdfinfo", str(src)]).stdout)
            pages = int(m.group(1)) if m else None
        text = plain.read_text(encoding="utf-8", errors="replace") if plain.exists() else ""
        chars = len(text.strip())
        manifest["inventory"] = {
            "pages": pages,
            "text_chars": chars,
            "figure_captions": re.findall(r"(?m)^(Fig(?:ure)?\.?\s+\d+[.:].{0,80})", text),
            "table_captions": re.findall(r"(?m)^(Table\s+\d+[.:].{0,80})", text),
            "numeric_citations": sorted(set(re.findall(r"\[(\d+(?:\s*[,\u2013-]\s*\d+)*)\]", text))),
            "equation_number_tags": len(re.findall(r"\(\d+\)\s*$", text, re.M)),
        }
        if pages and chars / max(pages, 1) < 500:
            manifest["warnings"].append("very little extractable text per page: likely scanned/image PDF - text NOT reliably extractable; stop and report")
        if re.search(r"[\ufffd]", text):
            manifest["warnings"].append("replacement characters in extracted text: font encoding problems; verify affected passages manually")
        manifest["warnings"].append("PDF source: equations, tables, and reading order are reconstructed from extracted text - verify each against the PDF visually")
        if shutil.which("pdfimages"):
            media = work / "media"
            media.mkdir(exist_ok=True)
            run(["pdfimages", "-png", "-p", str(src), str(media / "img")])
            manifest["files"]["media"] = sorted(str(p) for p in media.glob("*.png"))
            manifest["files"]["pdfimages_list"] = run(["pdfimages", "-list", str(src)]).stdout
        manifest["warnings"].append("vector figures are not extracted by pdfimages; crop them with pdftoppm -r 300 -x -y -W -H (figure region only, never whole pages)")
    else:
        sys.exit(f"unsupported input format: {ext} (supported: .md .tex .docx .pdf)")

    if plain.exists():
        manifest["files"]["source_plain"] = str(plain)
        ptxt = plain.read_text(encoding="utf-8", errors="replace")
        manifest["source_word_count"] = len(ptxt.split())
        manifest["source_numeric_tokens"] = len(NUM_RE.findall(ptxt))
    (work / "source_manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({k: manifest[k] for k in manifest if k != "files"}, indent=2, ensure_ascii=False)[:6000])
    print(f"\nmanifest: {work / 'source_manifest.json'}")


if __name__ == "__main__":
    main()
