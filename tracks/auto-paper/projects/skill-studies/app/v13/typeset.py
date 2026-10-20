"""Portable v13 document build/verification; no model, network or experiment runner."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import unicodedata

PROJECTS = {"skillmerge": "SkillMerge", "second_chance": "SecondChance", "probeflow": "ProbeFlow"}
ACKNOWLEDGEMENT = "This work was created as part of the No-More-Slops group activities at Pseudo Lab."
CITATION = re.compile(r"\[([1-9][0-9]*(?:\s*[,–-]\s*[1-9][0-9]*)*)\]")
APP = Path(__file__).resolve().parent
REPO = next(p for p in APP.parents if (p / "AGENTS.md").is_file() and (p / "LICENSE").is_file())
DEFAULT_INPUTS = APP.parents[1] / "outputs/week-01/revisions/v13-20261018"


def require(value, message):
    if not value:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def repo_path(path):
    resolved = Path(path).resolve()
    require(resolved.is_relative_to(REPO), "path must remain inside this repository checkout")
    return resolved.relative_to(REPO).as_posix()


def recorded_path(value):
    require(isinstance(value, str) and value and not re.search(r"[:\\]", value), "invalid repository-relative path")
    require(all(part not in ("", ".", "..") for part in value.split("/")), "unsafe path component")
    path = REPO / value
    require(not path.is_symlink() and repo_path(path) == value, "symlink or escaped artifact path")
    return path


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
    require(isinstance(equation, str) and not any(token in equation for token in ("#", "$", "\\")),
            "equation must be native Typst math without scripting or LaTeX escapes")
    return "$ " + equation + " $"


def validate(data, project):
    require(data["id"] == PROJECTS[project], "project identity differs")
    for key in ("title", "abstract", "status"):
        require(isinstance(data[key], str) and data[key].strip(), "missing " + key)
    require(data["contributions"] and data["sections"] and data["references"], "incomplete manuscript")
    require(data["sections"][0]["heading"].lower() == "introduction", "start with Introduction")
    refs = data["references"]
    numbers = {row["number"] for row in refs}
    require(len(numbers) == len(refs) and numbers == set(range(1, len(refs) + 1)), "duplicate/noncontiguous references")
    for row in refs:
        require(row["url"].startswith("https://") and row["text"] and row["claim_scope"], "unscoped source")
    figures = []
    for section in [*data["sections"], *data.get("appendices", [])]:
        require(section["heading"] and section.get("level", 1) in (1, 2), "invalid section")
        for equation in section.get("equations", []):
            math(equation)
        if "table" in section:
            table = section["table"]
            require(table["headers"] and table["rows"] and all(len(r) == len(table["headers"]) for r in table["rows"]), "ragged table")
        for figure in section.get("figures", []):
            require(re.fullmatch(r"[a-z][a-z0-9-]{1,60}", figure["id"]) and figure["caption"], "invalid figure")
            figures.append(figure["id"])
    require(len(figures) == len(set(figures)) == 3, "expected exactly three distinct figures")
    prose = json.dumps([data["abstract"], data["contributions"], data["sections"], data.get("appendices", [])], ensure_ascii=False)
    for match in CITATION.finditer(prose):
        cited = set()
        for part in match.group(1).replace("–", "-").split(","):
            ends = [int(n) for n in part.split("-")]
            require(ends[0] <= ends[-1], "descending citation range")
            cited.update(range(ends[0], ends[-1] + 1))
        require(cited <= numbers, "unresolved citation " + match.group())
    return figures


def section_lines(section):
    out = ["=" * section.get("level", 1) + " " + content(section["heading"]), ""]
    for paragraph in section.get("paragraphs", []):
        out += [content(paragraph), ""]
    out += ["- " + content(text) for text in section.get("bullets", [])]
    for equation in section.get("equations", []):
        out += [math(equation), ""]
    if "table" in section:
        table = section["table"]
        cells = lambda row: "(" + ",".join("[" + content(str(c)) + "]" for c in row) + ",)"
        rows = "(" + ",".join(cells(row) for row in table["rows"]) + ",)"
        out += ["#result-table(" + cells(table["headers"]) + "," + rows + "," + literal(table["caption"]) + ")", ""]
    if "algorithm" in section:
        algorithm = section["algorithm"]
        lines = "(" + ",".join("[" + content(line) + "]" for line in algorithm["lines"]) + ",)"
        out += ["#method-algorithm(" + lines + "," + literal(algorithm["caption"]) + ")", ""]
    for figure in section.get("figures", []):
        out += ["#figure(image(" + literal("figures/" + figure["id"] + ".svg") + ", width: 100%), caption: ["
                + content(figure["caption"]) + "]) <fig-" + figure["id"] + ">", ""]
    return out


def render(data):
    title = data["title"] + (": " + data["subtitle"] if data.get("subtitle") else "")
    out = ['#import "conference.typ": *', "#show: research-paper.with(title: " + literal(title) + ")",
           "#title-block(" + literal(title) + "," + literal(data["status"]) + ")",
           "#abstract-block[" + content(data["abstract"]) + "]", ""]
    for index, section in enumerate(data["sections"]):
        out += section_lines(section)
        if index == 0:
            out += ['#text(weight: "bold")[Contributions.]', ""]
            out += ["- " + content(value) for value in data["contributions"]]
            out.append("")
    out += ["#heading(numbering: none)[Acknowledgements]", "", content(ACKNOWLEDGEMENT), ""]
    out += ["#heading(numbering: none)[References]", ""]
    for row in data["references"]:
        out += ["#bibliography-entry(" + str(row["number"]) + ", [#text(" + literal(row["text"]) + ")],"
                + literal(row["url"]) + ") <bib" + str(row["number"]) + ">", ""]
    out += ["#pagebreak()", '#set heading(numbering: "A.1")', "#counter(heading).update(0)"]
    for section in data.get("appendices", []):
        out += section_lines(section)
    out += ["= Source inspection boundaries", ""]
    for row in data["references"]:
        out += [content("[" + str(row["number"]) + "] " + row["claim_scope"]), ""]
    return "\n".join(out)


ACK_BLOCK = "#heading(numbering: none)[Acknowledgements]\n\n" + content(ACKNOWLEDGEMENT) + "\n\n"


def normalize(text):
    # This PDF extraction check ignores layout punctuation; exact source/Typst hashes also bind every equation and unit.
    text = unicodedata.normalize("NFKC", text).replace("\u00ad", "")
    return "".join(c for c in text if unicodedata.category(c)[0] in "LN")


def paper_blocks(data):
    yield data["title"]
    if data.get("subtitle"):
        yield data["subtitle"]
    yield data["abstract"]
    yield data["status"]
    yield from data["contributions"]
    for section in [*data["sections"], *data.get("appendices", [])]:
        yield section["heading"]
        yield from section.get("paragraphs", [])
        yield from section.get("bullets", [])
        if "table" in section:
            table = section["table"]
            yield table["caption"]
            yield from table["headers"]
            for row in table["rows"]:
                yield from map(str, row)
        if "algorithm" in section:
            yield section["algorithm"]["caption"]
            yield from section["algorithm"]["lines"]
        for figure in section.get("figures", []):
            yield figure["caption"]
    for row in data["references"]:
        yield row["text"]
        yield row["claim_scope"]
    yield ACKNOWLEDGEMENT


def inspect_pdf(path, data):
    import fitz
    require(path.stat().st_size <= 6_000_000 and path.read_bytes().startswith(b"%PDF-"), "invalid/oversize PDF")
    with fitz.open(path) as doc:
        require(0 < len(doc) <= 80, "PDF page limit exceeded")
        require(all(page.get_text().strip() for page in doc), "empty PDF page")
        texts = [normalize("\n".join(page.get_text(sort=sort, clip=fitz.Rect(0, 0, page.rect.width, page.rect.height - 60)) for page in doc)) for sort in (False, True)]
        blocks = list(paper_blocks(data))
        missing = [value for value in blocks if not any(normalize(value) in text for text in texts)]
        require(not missing, "PDF missing authored blocks: " + repr(missing[:2]))
        outside = [(i + 1, word[4]) for i, page in enumerate(doc) for word in page.get_text("words")
                   if word[0] < 0 or word[1] < 0 or word[2] > page.rect.width or word[3] > page.rect.height]
        require(not outside, "PDF content outside page: " + repr(outside[:3]))
        lines = [line.strip() for page in doc for line in page.get_text().splitlines()]
        require(lines.count("Acknowledgements") == 1 and lines.index("Acknowledgements") < lines.index("References"), "acknowledgement heading placement")
        require(all(text.count(normalize(ACKNOWLEDGEMENT)) == 1 for text in texts), "acknowledgement must occur once")
        links = {link.get("uri") for page in doc for link in page.get_links()}
        require(all(ref["url"] in links for ref in data["references"]), "reference URL missing from PDF links")
        fonts = sorted({font[3] for page in doc for font in page.get_fonts()})
        if any(section.get("equations") for section in data["sections"] + data.get("appendices", [])):
            require(any("Math" in font for font in fonts), "native math font not embedded")
        return {"pages": len(doc), "expected_text_blocks": len(blocks), "missing_text_blocks": 0,
                "outside_page_words": 0, "references": len(data["references"]), "figures": 3,
                "acknowledgement_count": 1, "fonts": fonts, "reference_urls_verified": len(data["references"])}


def record(path):
    return {"path": repo_path(path), "bytes": Path(path).stat().st_size, "sha256": sha(path)}


def check_record(item):
    path = recorded_path(item["path"])
    require(path.is_file() and path.stat().st_size == item["bytes"] and sha(path) == item["sha256"], "artifact changed: " + item["path"])
    return path


def inputs_for(inputs):
    inputs = Path(inputs).resolve(); repo_path(inputs)
    bindings = json.loads((inputs / "ORIGINAL_BINDINGS.json").read_text(encoding="utf8"))
    require(bindings["schema"] == "nms_v13_original_bindings_v1" and set(bindings["projects"]) == set(PROJECTS), "invalid original bindings")
    for item in bindings["historical_binaries"]:
        check_record(item)
    data = {}
    for key in PROJECTS:
        original = bindings["projects"][key]
        for filename, item in original["files"].items():
            require(check_record(item) == inputs / "sources" / key / filename, "source path does not match requested package")
        data[key] = json.loads((inputs / "sources" / key / "paper.json").read_text(encoding="utf8"))
        figures = validate(data[key], key)
        require(original["references"] == len(data[key]["references"]), "reference inventory changed")
        require(original["original_source_sha256"] == sha(inputs / "sources" / key / "paper.json"), "original source identity mismatch")
        require({check_record(item) for item in original["figures"]} == {inputs / "figures" / key / (figure + ".svg") for figure in figures}, "figure inventory differs")
        baseline = render(data[key]).replace(ACK_BLOCK, "", 1)
        require(hashlib.sha256(baseline.encode("utf8")).hexdigest() == original["original_typst_normalized_sha256"], "content differs from original v13 beyond acknowledgement")
    return inputs, bindings, data


def fresh_output(out, inputs):
    out = Path(out).resolve(); repo_path(out)
    require(not out.exists(), "--out must be a new directory; existing evidence is never overwritten")
    require(not inputs.is_relative_to(out), "output cannot contain its own inputs")
    return out


def build(inputs, out):
    inputs, bindings, data = inputs_for(inputs)
    out = fresh_output(out, inputs)
    typst = shutil.which("typst"); require(typst, "Typst must already be installed")
    import fitz
    version = subprocess.run([typst, "--version"], capture_output=True, text=True, check=True, timeout=30).stdout.strip()
    out.mkdir(parents=True, exist_ok=False)
    publication = {"schema": "nms_v13_submission_publication_v1", "version": "v13-20261018", "writer": "@darkwingduck-code",
                   "track": "Auto-Paper", "week": "Week 01", "original_pr": 14,
                   "scope": "Derived repository PDF contribution, not conference submission, peer review, a new experiment or scientific-effect reproduction.",
                   "acknowledgement": ACKNOWLEDGEMENT, "only_manuscript_change": "One unnumbered Acknowledgements section immediately before References; source JSON, equations, tables, figures, references and appendices preserved.",
                   "inputs": repo_path(inputs), "output": repo_path(out), "original_bindings": record(inputs / "ORIGINAL_BINDINGS.json"),
                   "renderer": record(Path(__file__)), "style": record(APP / "conference.typ"), "regression_test": record(APP / "test_typeset.py"),
                   "environment": {"typst": version, "pymupdf": fitz.VersionBind}, "projects": []}
    checks = []
    for key, name in PROJECTS.items():
        target = out / key; target.mkdir(); (target / "figures").mkdir()
        shutil.copyfile(APP / "conference.typ", target / "conference.typ")
        for item in bindings["projects"][key]["figures"]:
            source = check_record(item); shutil.copyfile(source, target / "figures" / source.name)
        typ = target / (name + "_v13_nms.typ"); typ.write_text(render(data[key]), encoding="utf8")
        pdf = typ.with_suffix(".pdf")
        compiled = subprocess.run([typst, "compile", "--ignore-system-fonts", "--root", str(target), str(typ), str(pdf)],
                                  capture_output=True, text=True, encoding="utf8", timeout=120)
        require(compiled.returncode == 0, key + " compile failed: " + compiled.stderr)
        inspection = inspect_pdf(pdf, data[key]); inspection["project"] = key; checks.append(inspection)
        origin = bindings["projects"][key]
        publication["projects"].append({"id": key, "source": origin["files"]["paper.json"],
                                       "original_source_sha256": origin["original_source_sha256"], "original_pdf_sha256": origin["original_pdf_sha256"],
                                       "original_pdf_pages": origin["original_pdf_pages"], "submission_pdf": record(pdf), "typst_source": record(typ),
                                       "style_copy": record(target / "conference.typ"),
                                       "figure_copies": [record(p) for p in sorted((target / "figures").glob("*.svg"))],
                                       "pages": inspection["pages"], "references": len(data[key]["references"]), "figures": 3})
    publication["historical_binaries"] = bindings["historical_binaries"]
    (out / "PUBLICATION.json").write_text(json.dumps(publication, ensure_ascii=False, indent=2) + "\n", encoding="utf8")
    validation = {"schema": "nms_v13_document_validation_v1", "publication_sha256": sha(out / "PUBLICATION.json"),
                  "checks": checks, "historical_binary_count": len(bindings["historical_binaries"]), "historical_binary_changes": 0,
                  "new_model_calls": 0, "new_scientific_experiments": 0,
                  "scope": "JSON/SVG identity, ack-only generated-source difference, native math compilation, all authored PDF prose/table/caption/reference/scope blocks, URL links, page bounds and preserved historical binary hashes. PDF text normalization ignores punctuation; it does not prove mathematical or scientific validity."}
    (out / "VALIDATION.json").write_text(json.dumps(validation, ensure_ascii=False, indent=2) + "\n", encoding="utf8")
    return verify(inputs, out)


def verify(inputs, out):
    """Only read files and parse PDFs; never compiles or creates an output directory."""
    inputs, bindings, data = inputs_for(inputs)
    out = Path(out).resolve(); repo_path(out)
    publication = json.loads((out / "PUBLICATION.json").read_text(encoding="utf8"))
    validation = json.loads((out / "VALIDATION.json").read_text(encoding="utf8"))
    require(publication["schema"] == "nms_v13_submission_publication_v1" and validation["schema"] == "nms_v13_document_validation_v1", "receipt schema mismatch")
    require(validation["publication_sha256"] == sha(out / "PUBLICATION.json"), "publication receipt changed")
    require(publication["inputs"] == repo_path(inputs) and publication["output"] == repo_path(out), "receipt points to different package")
    for key in ("original_bindings", "renderer", "style", "regression_test"):
        check_record(publication[key])
    require(publication["acknowledgement"] == ACKNOWLEDGEMENT, "acknowledgement changed")
    require({row["id"] for row in publication["projects"]} == set(PROJECTS), "submission project set differs")
    checks = []
    for row in publication["projects"]:
        key = row["id"]; original = bindings["projects"][key]
        require(row["original_source_sha256"] == original["original_source_sha256"] and row["original_pdf_sha256"] == original["original_pdf_sha256"], "original hash binding changed")
        require(check_record(row["source"]) == inputs / "sources" / key / "paper.json", "wrong manuscript source")
        pdf = check_record(row["submission_pdf"]); typ = check_record(row["typst_source"])
        require(pdf == out / key / (PROJECTS[key] + "_v13_nms.pdf") and typ == pdf.with_suffix(".typ"), "wrong output artifact")
        require(typ.read_text(encoding="utf8") == render(data[key]), "rendered source differs from complete manuscript plus acknowledgement")
        require(sha(check_record(row["style_copy"])) == sha(APP / "conference.typ"), "output style differs")
        copies = {p.name: sha(p) for p in map(check_record, row["figure_copies"])}
        require(copies == {Path(item["path"]).name: item["sha256"] for item in original["figures"]}, "output SVG copies changed")
        inspection = inspect_pdf(pdf, data[key]); inspection["project"] = key; checks.append(inspection)
        require(row["pages"] == inspection["pages"] and row["references"] == inspection["references"] and row["figures"] == 3, "PDF counters differ")
    require(checks == validation["checks"], "PDF validation result changed")
    require(publication["historical_binaries"] == bindings["historical_binaries"], "historical inventory changed")
    require(validation["historical_binary_changes"] == validation["new_model_calls"] == validation["new_scientific_experiments"] == 0, "scope counters differ")
    return {"ok": True, "projects": [{"id": row["project"], "pages": row["pages"], "references": row["references"], "figures": row["figures"]} for row in checks],
            "historical_binary_changes": 0, "new_model_calls": 0, "scope": "document reproduction and hash verification only"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("build", "verify"))
    parser.add_argument("--inputs", type=Path, default=DEFAULT_INPUTS)
    parser.add_argument("--out", type=Path, required=True, help="Build requires a fresh directory inside the checkout; verify reads an existing build.")
    args = parser.parse_args()
    print(json.dumps((build if args.command == "build" else verify)(args.inputs, args.out), ensure_ascii=False, indent=2))
