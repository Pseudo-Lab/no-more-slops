"""Build three literal-prose documents and an offline study page from DOCUMENT.json."""
from __future__ import annotations

import argparse
import base64
from datetime import datetime, timezone
import hashlib
from html import escape
import json
import math
from pathlib import Path, PurePosixPath
import re
import shutil
import struct
import subprocess
from urllib.parse import quote, urlsplit
import xml.etree.ElementTree as ET


KINDS = ("paper", "supplement", "explainer")
KOREAN_FONTS = ("Noto Serif KR", "Malgun Gothic", "Noto Sans KR", "New Computer Modern")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def text(value, label, nonempty=True):
    require(isinstance(value, str) and (not nonempty or value.strip()), "invalid " + label)
    require(not any(ord(c) < 32 and c not in "\n\r\t" for c in value), "control character in " + label)
    return value


def breakable_text(value, wrap):
    # Long hashes, paths and policy IDs need invisible break opportunities in narrow columns.
    return re.sub(r"\S{" + str(wrap + 1) + r",}",
                  lambda match: "\u200b".join(match[0][i:i + wrap] for i in range(0, len(match[0]), wrap)), str(value))


def literal(value, wrap=24):
    return "#text(" + json.dumps(breakable_text(value, wrap), ensure_ascii=False) + ")"


def unique_keys(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate JSON key: " + key)
        result[key] = value
    return result


def math_source(value):
    text(value, "Typst equation")
    require(not any(token in value for token in ("#", "$", "\\", "//", "/*", "*/")),
            "equation must use native Typst math without code, delimiters or comments")
    return "$ " + value + " $"


def embedded_png(value):
    if not isinstance(value, str) or len(value) > 2_800_000 or not re.fullmatch(r'data:image/png;base64,[A-Za-z0-9+/=\s]+', value):
        return False
    try:
        encoded = ''.join(value.split(',', 1)[1].split())
        raw = base64.b64decode(encoded, validate=True)
    except ValueError:
        return False
    if base64.b64encode(raw).decode('ascii') != encoded:
        return False
    if len(raw) < 33 or len(raw) > 2_000_000 or raw[:16] != b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR':
        return False
    width, height = struct.unpack('>II', raw[16:24])
    return 0 < width <= 8192 and 0 < height <= 8192 and width * height <= 16_777_216


def figure_source(project, value):
    text(value, "figure path")
    normalized = value.replace("\\", "/")
    relative = PurePosixPath(normalized)
    require(not relative.is_absolute() and not re.match(r"^[A-Za-z]:", normalized)
            and all(part not in ("", ".", "..") for part in normalized.split("/"))
            and relative.suffix.lower() == ".svg", "figure path must be a contained relative SVG")
    source = project.joinpath(*relative.parts)
    require(source.is_file() and not source.is_symlink() and source.resolve().is_relative_to(project),
            "figure escapes project or is missing")
    raw = source.read_bytes()
    try:
        decoded = raw.decode("utf-8")
    except UnicodeDecodeError:
        raise ValueError("SVG must be UTF-8 without NUL bytes") from None
    require("\x00" not in decoded, "SVG must be UTF-8 without NUL bytes")
    # Matplotlib's fixed external declaration is removed from a derived copy, never resolved.
    display = re.sub(rb'<!DOCTYPE svg PUBLIC\s+"-//W3C//DTD SVG 1\.1//EN"\s+"http://www\.w3\.org/Graphics/SVG/1\.1/DTD/svg11\.dtd"(?:[ \t\r\n]*\[[ \t\r\n]*\][ \t\r\n]*)?>', b'', raw, count=1)
    require(b"<!doctype" not in display.lower() and b"<!entity" not in raw.lower(), "SVG entities are forbidden")
    root = ET.fromstring(display.decode("utf-8"))
    require(root.tag == "{http://www.w3.org/2000/svg}svg", "expected an SVG root")
    for node in root.iter():
        tag = node.tag.rsplit("}", 1)[-1].lower()
        require(tag not in ("script", "foreignobject", "iframe"), "active SVG content is forbidden")
        for name, item in node.attrib.items():
            name = name.rsplit("}", 1)[-1].lower()
            require(not name.startswith("on"), "SVG event handlers are forbidden")
            if name == "href":
                require(item.startswith("#") or node.tag == "{http://www.w3.org/2000/svg}image" and embedded_png(item), "external SVG references are forbidden")
            require("@import" not in item.lower(), "external SVG styles are forbidden")
            for target in re.findall(r"url\((.*?)\)", item, re.I):
                require(target.strip(" \"'").startswith("#"), "external SVG URLs are forbidden")
        if tag == "style":
            style = "".join(node.itertext())
            require("@import" not in style.lower(), "external SVG styles are forbidden")
            for target in re.findall(r"url\((.*?)\)", style, re.I):
                require(target.strip(" \"'").startswith("#"), "external SVG URLs are forbidden")
    if "viewBox" in root.attrib:
        box = [float(v) for v in re.split(r"[\s,]+", root.attrib["viewBox"].strip())]
        require(len(box) == 4 and all(math.isfinite(v) for v in box) and box[2] > 0 and box[3] > 0,
                "invalid SVG viewBox")
    else:
        dimensions = []
        for key in ("width", "height"):
            match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)(?:px|pt|mm|cm|in)?", root.get(key, ""))
            require(match is not None and float(match.group(1)) > 0, "SVG needs positive dimensions or viewBox")
            dimensions.append(float(match.group(1)))
        box = [0, 0, *dimensions]
    return relative.as_posix(), source, raw, display, box


def validate(project, data):
    require(isinstance(data, dict), "DOCUMENT must be an object")
    text(data.get("title"), "title")
    text(data.get("subtitle"), "subtitle", nonempty=False)
    figures = {}
    for kind in KINDS:
        sections = data.get(kind)
        require(isinstance(sections, list) and sections, "empty required sections: " + kind)
        for section in sections:
            require(isinstance(section, dict), "section must be an object")
            text(section.get("heading"), "heading")
            paragraphs = section.get("paragraphs")
            require(isinstance(paragraphs, list) and paragraphs, "section needs paragraphs")
            for paragraph in paragraphs:
                text(paragraph, "paragraph")
            if "algorithm" in section:
                algorithm = section["algorithm"]
                require(isinstance(algorithm, dict) and set(algorithm) == {"name", "inputs", "outputs", "steps"},
                        "algorithm needs exactly name, inputs, outputs and steps")
                name = text(algorithm["name"], "algorithm name")
                total = len(name.encode("utf-8"))
                require(total <= 512, "algorithm name exceeds 512 UTF-8 bytes")
                for key, count, size in (("inputs", 32, 2048), ("outputs", 32, 2048), ("steps", 128, 4096)):
                    items = algorithm[key]
                    require(isinstance(items, list) and len(items) <= count and (key != "steps" or items),
                            "invalid algorithm " + key + " count")
                    for item in items:
                        length = len(text(item, "algorithm " + key).encode("utf-8"))
                        require(length <= size, "algorithm " + key + " item exceeds UTF-8 byte limit")
                        total += length
                require(total <= 65_536, "algorithm exceeds 65536 UTF-8 bytes")
            equations = section.get("equations", [])
            require(isinstance(equations, list), "equations must be a list")
            for equation in equations:
                require(isinstance(equation, dict), "equation must be an object")
                math_source(equation.get("typst"))
                text(equation.get("explanation"), "equation explanation")
            tables = section.get("tables", [])
            require(isinstance(tables, list), "tables must be a list")
            for table in tables:
                require(isinstance(table, dict), "table must be an object")
                text(table.get("caption"), "table caption")
                columns, rows = table.get("columns"), table.get("rows")
                require(isinstance(columns, list) and columns, "empty table columns")
                for column in columns:
                    text(column, "table column")
                require(isinstance(rows, list) and rows, "empty table rows")
                for row in rows:
                    require(isinstance(row, list) and len(row) == len(columns), "invalid table row")
                    for cell in row:
                        require(type(cell) in (str, int, float), "invalid table cell")
                        if isinstance(cell, str):
                            text(cell, "table cell", nonempty=False)
                        elif isinstance(cell, float):
                            require(math.isfinite(cell), "nonfinite table cell")
            if "figure" in section:
                figure = section["figure"]
                require(isinstance(figure, dict), "figure must be an object")
                text(figure.get("caption"), "figure caption")
                relative, source, raw, display, box = figure_source(project, figure.get("path"))
                figures[relative] = {"source": source, "source_bytes": raw, "bytes": display, "viewbox": box,
                                     "artifact": "figures/" + relative}
    references = data.get("references")
    require(isinstance(references, list), "references must be a list")
    ids = set()
    for reference in references:
        require(isinstance(reference, dict), "reference must be an object")
        for key in ("id", "title", "url", "scope"):
            text(reference.get(key), "reference " + key)
        require(reference["id"] not in ids, "duplicate reference ID")
        ids.add(reference["id"])
        url = urlsplit(reference["url"])
        require(url.scheme in ("https", "http") and bool(url.netloc), "invalid reference URL")
    return figures


def render_typst(data, kind, figures):
    korean = kind == "explainer"
    fonts = KOREAN_FONTS if korean else ("New Computer Modern", "Malgun Gothic", "Noto Sans KR")
    font_tuple = "(" + ",".join(json.dumps(f) for f in fonts) + ",)"
    title = data["title"] + (" — " + kind.title() if kind != "paper" else "")
    lines = ["#set document(title: " + json.dumps(title, ensure_ascii=False) + ")",
             '#set page(paper: "a4", margin: 17mm, numbering: "1")',
             f'#set text(font: {font_tuple}, size: {"9pt" if kind == "paper" else "10.5pt"}, lang: "{"ko" if korean else "en"}")',
             '#set par(justify: false, leading: 0.65em, spacing: 0.7em)',
             '#set heading(numbering: "1.")',
             '#let fit-equation(body) = layout(size => { let natural = measure(body); '
             'let factor = calc.min(1, size.width / natural.width); '
             'align(center, scale(factor * 100%, reflow: true, body)) })',
             '#show heading.where(level: 1): set text(size: 11pt, weight: "bold")',
             '#align(center)[#text(size: 17pt, weight: "bold")[' + literal(title) + ']]',
             '#align(center)[' + literal(data["subtitle"]) + ']', '']
    if kind == "paper":
        lines += ['#show figure.where(kind: table): set block(breakable: true)',
                  '#columns(2, gutter: 13pt)[']
    paper_tables = []
    for section in data[kind]:
        lines += ["= " + literal(section["heading"]), ""]
        for paragraph in section["paragraphs"]:
            lines += [literal(paragraph), ""]
        if "algorithm" in section:
            algorithm = section["algorithm"]
            code = "\n".join(f"{i}. {step}" for i, step in enumerate(algorithm["steps"], 1))
            lines += ['#block(width: 100%, inset: 6pt, stroke: 0.4pt + rgb("#ccd5df"), breakable: true)[',
                      '#block(sticky: true)[#strong[' + literal("Algorithm: " + algorithm["name"]) + ']]', "",
                      '#strong[Inputs:] ' + literal("\n".join(algorithm["inputs"])), "",
                      '#strong[Outputs:] ' + literal("\n".join(algorithm["outputs"])), "",
                      '#show raw: set text(font: ("DejaVu Sans Mono", "Malgun Gothic", "Noto Sans KR"), size: 8pt)',
                      '#show raw.where(block: true): set block(breakable: true)',
                      '#raw(' + json.dumps(breakable_text(code, 24), ensure_ascii=False) + ', block: true, lang: none)', ']', ""]
        for equation in section.get("equations", []):
            lines += ["#fit-equation[" + math_source(equation["typst"]) + "]", "", literal(equation["explanation"]), ""]
        for table in section.get("tables", []):
            cells = lambda row: ",".join("[" + literal(cell, wrap=max(4, 24 // len(table["columns"]))) + "]" for cell in row)
            # Keep the two-column flow continuous; breakable full-width tables follow the body.
            table_lines = (["#figure(kind: table, caption: ["
                       + literal(table["caption"]) + "])[", '#set text(size: 8pt)'] if kind == "paper" else
                      ["#block[", '#set text(size: 9pt)',
                       "#block(sticky: true)[" + literal(table["caption"]) + "]", ""]) + [
                      '#table(columns: (' + ','.join('1fr' for _ in table["columns"]) + ',), inset: 3pt, stroke: 0.35pt,',
                      "table.header(" + cells(table["columns"]) + "),",
                      ",\n".join(cells(row) for row in table["rows"]) + ")", "]", ""]
            if kind == "paper":
                paper_tables += table_lines
            else:
                lines += table_lines
        if "figure" in section:
            figure = section["figure"]
            key = figure["path"].replace("\\", "/")
            lines += ['#figure(image(' + json.dumps(figures[key]["artifact"], ensure_ascii=False)
                      + (', width: 100%), placement: top, scope: "parent", caption: [' if kind == "paper" else
                         ', width: 100%, height: 88mm, fit: "contain"), caption: [')
                      + literal(figure["caption"]) + '])', '']
    lines += ["= " + literal("참고문헌과 열람 범위" if korean else "References and inspection scope"), ""]
    for reference in data["references"]:
        lines += [literal("[" + reference["id"] + "] " + reference["title"]),
                  '#link(' + json.dumps(reference["url"], ensure_ascii=False) + ')[' + literal(reference["url"]) + ']',
                  literal(reference["scope"]), ""]
    if kind == "paper":
        lines += ["]", *paper_tables]
    return "\n".join(lines) + "\n"


def artifact_url(run_id, project_id, relative):
    return f"/api/runs/{quote(run_id, safe='')}/artifact?path=documents/{quote(project_id, safe='')}/{quote(relative, safe='/')}"


def render_html(data, run_id, project_id, figures, equations):
    url = lambda relative: escape(artifact_url(run_id, project_id, relative), quote=True)
    out = ['<!doctype html><html lang="ko"><meta charset="utf-8">',
           '<meta name="viewport" content="width=device-width,initial-scale=1">',
           '<title>' + escape(data["title"]) + '</title>',
           '<style>body{max-width:980px;margin:36px auto;padding:0 22px;font:17px/1.8 "Malgun Gothic",sans-serif;color:#172331;background:#fafbfc}'
           'h1,h2,h3{line-height:1.3}nav{position:sticky;top:0;background:#fafbfc;padding:12px 0;border-bottom:1px solid #cad3dc}'
           'nav a{margin-right:18px}article{margin:44px 0}section{scroll-margin-top:76px;margin:30px 0}'
           'p{white-space:pre-wrap;overflow-wrap:anywhere}a{color:#075c88}figure{margin:24px 0}img{max-width:100%;height:auto}'
           '.equation{display:block;max-width:100%;margin:16px auto;max-height:150px}.table-wrap{overflow-x:auto}'
           'table{border-collapse:collapse;width:100%;font-size:15px}th,td{border:1px solid #ccd5df;padding:8px;text-align:left}'
           'caption,figcaption{font-size:15px;text-align:left;color:#45586b}.downloads{font-size:15px}li{margin:12px 0}</style>',
           '<h1>' + escape(data["title"]) + '</h1><p>' + escape(data["subtitle"]) + '</p>',
           '<nav>' + ''.join(f'<a href="#{kind}">{kind.title()}</a>' for kind in KINDS)
           + '<a href="#references">References</a></nav>']
    for kind in KINDS:
        out += [f'<article id="{kind}"><h2>{kind.title()}</h2>',
                f'<p class="downloads"><a href="{url(kind + ".pdf")}">PDF</a> · '
                f'<a href="{url(kind + ".typ")}">Typst source</a></p>', '<ol>']
        for index, section in enumerate(data[kind], 1):
            out += [f'<li><a href="#{kind}-{index}">{escape(section["heading"])}</a></li>']
        out += ['</ol>']
        for index, section in enumerate(data[kind], 1):
            out += [f'<section id="{kind}-{index}"><h3>{escape(section["heading"])}</h3>']
            out += ['<p>' + escape(p) + '</p>' for p in section["paragraphs"]]
            if "algorithm" in section:
                algorithm = section["algorithm"]
                code = "\n".join(f"{i}. {step}" for i, step in enumerate(algorithm["steps"], 1))
                out += ['<div class="algorithm" style="border:1px solid #ccd5df;padding:16px;background:#fff">',
                        '<h4 style="white-space:pre-wrap;overflow-wrap:anywhere">Algorithm: ' + escape(algorithm["name"]) + '</h4>',
                        '<p><strong>Inputs:</strong> ' + escape("\n".join(algorithm["inputs"])) + '</p>',
                        '<p><strong>Outputs:</strong> ' + escape("\n".join(algorithm["outputs"])) + '</p>',
                        '<pre style="white-space:pre-wrap;overflow-wrap:anywhere;font:14px/1.6 monospace"><code>'
                        + escape(code) + '</code></pre></div>']
            for eqindex, equation in enumerate(section.get("equations", []), 1):
                eqpath = equations[(kind, index, eqindex)]
                out += [f'<a href="{url(eqpath)}"><img class="equation" src="{url(eqpath)}" '
                        f'alt="{escape(equation["explanation"], quote=True)}"></a>',
                        '<p>' + escape(equation["explanation"]) + '</p>']
            for table in section.get("tables", []):
                out += ['<div class="table-wrap"><table><caption>' + escape(table["caption"]) + '</caption><thead><tr>',
                        ''.join('<th scope="col">' + escape(c) + '</th>' for c in table["columns"]), '</tr></thead><tbody>']
                out += ['<tr>' + ''.join('<td>' + escape(str(c)) + '</td>' for c in row) + '</tr>' for row in table["rows"]]
                out += ['</tbody></table></div>']
            if "figure" in section:
                figure = section["figure"]
                path = figures[figure["path"].replace("\\", "/")]["artifact"]
                out += [f'<figure><a href="{url(path)}"><img src="{url(path)}" '
                        f'alt="{escape(figure["caption"], quote=True)}"></a><figcaption>'
                        + escape(figure["caption"]) + '</figcaption></figure>']
            out += ['</section>']
        out += ['</article>']
    out += ['<section id="references"><h2>References and inspection scope</h2><ol>']
    for reference in data["references"]:
        out += ['<li>[' + escape(reference["id"]) + '] <a href="' + escape(reference["url"], quote=True)
                + '">' + escape(reference["title"]) + '</a><p>' + escape(reference["scope"]) + '</p></li>']
    return '\n'.join(out + ['</ol></section></html>']) + '\n'


def compile_typst(typst, source, target, out):
    command = [typst, "compile", "--root", str(out), str(source), str(target)]
    log = source.with_suffix(".compile.log")
    try:
        result = subprocess.run(command, capture_output=True, timeout=120)
    except subprocess.TimeoutExpired as exc:
        log.write_bytes((exc.stdout or b"") + (exc.stderr or b"") + b"\nTypst timeout after 120 seconds\n")
        raise RuntimeError("Typst timeout; original log: " + str(log)) from exc
    log.write_bytes(result.stdout + result.stderr)
    write_json(source.with_suffix(".command.json"), {"command": command, "exit_code": result.returncode})
    require(result.returncode == 0, "Typst compile failed; original log: " + str(log))


def inspect_pdf(path):
    import fitz
    pages, drawings, image_boxes, fonts = [], 0, 0, set()
    with fitz.open(path) as pdf:
        require(0 < len(pdf) <= 80 and path.stat().st_size <= 6_000_000, "PDF exceeds viewer limits")
        for page in pdf:
            require(page.get_text().strip(), "empty PDF page")
            bounds = page.rect + (-1, -1, 1, 1)
            for block in page.get_text("dict")["blocks"]:
                require(bounds.contains(fitz.Rect(block["bbox"])), "PDF content bbox leaves page")
                if block["type"] == 1:
                    image_boxes += 1
                else:
                    fonts.update(span["font"] for line in block["lines"] for span in line["spans"])
            paths = page.get_drawings()
            for drawing in paths:
                require(bounds.contains(drawing["rect"]), "PDF vector bbox leaves page")
            drawings += len(paths)
            pages.append({"page": page.number + 1, "width_pt": page.rect.width, "height_pt": page.rect.height,
                          "text_characters": len(page.get_text()), "vector_paths": len(paths)})
        extracted = '\n'.join(page.get_text(sort=True) for page in pdf)
    path.with_suffix(".txt").write_text(extracted, encoding="utf-8")
    return {"pages": len(pages), "bytes": path.stat().st_size, "sha256": sha(path),
            "page_checks": pages, "vector_paths": drawings, "image_boxes": image_boxes, "fonts": sorted(fonts),
            "bbox_check": "text, raster and vector bounds within PDF pages; not semantic figure certification"}


def build(project, out, run_id, project_id):
    project, out = Path(project).resolve(), Path(out).resolve()
    for value, name in ((run_id, "run ID"), (project_id, "project ID")):
        require(isinstance(value, str) and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", value), "invalid " + name)
    require(not out.exists(), "output directory already exists")
    source = project / "DOCUMENT.json"
    raw = source.read_bytes()
    data = json.loads(raw.decode("utf-8-sig"), object_pairs_hook=unique_keys)
    figures = validate(project, data)
    typst = shutil.which("typst")
    require(typst is not None, "installed typst executable is required")
    out.mkdir(parents=True, exist_ok=False)
    (out / "source.DOCUMENT.json").write_bytes(raw)
    receipt = {"schema": "research-expansion-document-build.v1", "status": "building", "run_id": run_id,
               "project_id": project_id, "created_at_utc": datetime.now(timezone.utc).isoformat(),
               "source": str(source), "source_sha256": hashlib.sha256(raw).hexdigest(),
               "builder_sha256": sha(Path(__file__)), "scientific_certification": False,
               "scope": "Document typesetting and local artifact integrity; no scientific validity or submission certification.",
               "model_api_calls": 0}
    try:
        receipt["typst_version"] = subprocess.run([typst, "--version"], capture_output=True, check=True).stdout.decode("utf-8").strip()
        receipt["figures"] = {}
        for relative, figure in figures.items():
            target = out / figure["artifact"]
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(figure["bytes"])
            receipt["figures"][relative] = {"artifact": figure["artifact"], "sha256": sha(target), "viewbox": figure["viewbox"]}
            if figure["source_bytes"] != figure["bytes"]:
                original = out / "source_figures" / relative
                original.parent.mkdir(parents=True, exist_ok=True)
                original.write_bytes(figure["source_bytes"])
                receipt["figures"][relative].update(source_artifact=original.relative_to(out).as_posix(),
                    source_sha256=sha(original), display_transform="matplotlib-svg11-doctype-removed-v1")
        equations = {}
        for kind in KINDS:
            for section_index, section in enumerate(data[kind], 1):
                for eq_index, equation in enumerate(section.get("equations", []), 1):
                    relative = f"equations/{kind}-{section_index}-{eq_index}.svg"
                    target = out / relative
                    target.parent.mkdir(exist_ok=True)
                    eqsource = target.with_suffix(".typ")
                    eqsource.write_text('#set page(width: auto, height: auto, margin: 6pt)\n#set text(size: 13pt)\n'
                                        + math_source(equation["typst"]) + '\n', encoding="utf-8")
                    compile_typst(typst, eqsource, target, out)
                    equations[(kind, section_index, eq_index)] = relative
        receipt["documents"] = {}
        for kind in KINDS:
            path = out / (kind + ".typ")
            path.write_text(render_typst(data, kind, figures), encoding="utf-8")
            compile_typst(typst, path, path.with_suffix(".pdf"), out)
            receipt["documents"][kind] = inspect_pdf(path.with_suffix(".pdf"))
        (out / "study.html").write_text(render_html(data, run_id, project_id, figures, equations), encoding="utf-8")
        require(source.read_bytes() == raw, "DOCUMENT source changed during build")
        for figure in figures.values():
            require(figure["source"].read_bytes() == figure["source_bytes"], "figure source changed during build")
        receipt["status"] = "complete"
        receipt["artifacts"] = {p.relative_to(out).as_posix(): {"sha256": sha(p), "bytes": p.stat().st_size}
                                for p in sorted(out.rglob("*")) if p.is_file()}
    except Exception as exc:
        receipt["status"] = "failed"
        receipt["error"] = str(exc)
        write_json(out / "BUILD.json", receipt)
        raise
    write_json(out / "BUILD.json", receipt)
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--project-id", required=True)
    args = parser.parse_args()
    receipt = build(args.project, args.out, args.run_id, args.project_id)
    print(json.dumps({"status": receipt["status"], "project_id": args.project_id,
                      "pages": {k: v["pages"] for k, v in receipt["documents"].items()}}, ensure_ascii=False))


if __name__ == "__main__":
    main()
