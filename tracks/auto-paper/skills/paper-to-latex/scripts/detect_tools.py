#!/usr/bin/env python3
"""Detect LaTeX / conversion tooling available on this machine.

Usage: python detect_tools.py [--json]

Prints which compilers, bibliography tools, converters and PDF utilities are
on PATH, plus whether the optional `pypdf` Python module is importable, and a
recommended build route. Read-only: never installs anything.
"""
import importlib.util
import json
import shutil
import subprocess
import sys


for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass

TOOLS = [
    "latexmk", "pdflatex", "xelatex", "lualatex", "bibtex", "biber",
    "kpsewhich", "pandoc", "pdftotext", "pdfimages", "pdftoppm", "pdfinfo",
    "pdffonts", "epstopdf", "inkscape", "rsvg-convert",
]
PY_MODULES = ["pypdf", "PIL", "cairosvg", "svglib", "openpyxl"]


def first_version_line(path):
    try:
        r = subprocess.run([path, "--version"], capture_output=True, text=True,
                           timeout=60, errors="replace")
        for line in (r.stdout or r.stderr).splitlines():
            line = line.strip()
            if line and "major issue" not in line.lower():
                return line
    except Exception as exc:  # noqa: BLE001 - report, never crash
        return f"(version check failed: {exc})"
    return ""


def detect():
    found = {}
    for tool in TOOLS:
        path = shutil.which(tool)
        found[tool] = {"path": path, "version": first_version_line(path) if path else None}
    for mod in PY_MODULES:
        found[f"python:{mod}"] = {"path": "importable" if importlib.util.find_spec(mod) else None,
                                  "version": None}

    has = lambda t: bool(found[t]["path"])  # noqa: E731
    if has("latexmk") and has("pdflatex"):
        route = "latexmk -pdf (pdflatex + bibtex/biber handled automatically)"
    elif has("pdflatex") and has("bibtex"):
        route = "manual: pdflatex -> bibtex -> pdflatex -> pdflatex"
    elif has("xelatex") or has("lualatex"):
        route = "xelatex/lualatex available but no pdflatex; adapt template (fontspec)"
    else:
        route = None
    return {
        "tools": found,
        "can_compile": route is not None,
        "recommended_route": route,
        "can_count_pages": has("pdfinfo") or found["python:pypdf"]["path"] is not None,
        "can_extract_pdf_text": has("pdftotext"),
        "can_convert_md_docx": has("pandoc"),
        "can_convert_svg": any(has(t) for t in ("inkscape", "rsvg-convert", "python:cairosvg", "python:svglib")),
        "can_convert_eps": has("epstopdf"),
        "can_convert_raster": has("python:PIL"),
    }


def main():
    info = detect()
    if "--json" in sys.argv:
        print(json.dumps(info, indent=2))
        return
    for name, d in info["tools"].items():
        status = d["path"] or "MISSING"
        ver = f"  [{d['version']}]" if d.get("version") else ""
        print(f"{name:14s} {status}{ver}")
    print()
    print("can_compile          :", info["can_compile"])
    print("recommended_route    :", info["recommended_route"])
    print("can_count_pages      :", info["can_count_pages"])
    print("can_extract_pdf_text :", info["can_extract_pdf_text"])
    print("can_convert_md_docx  :", info["can_convert_md_docx"])
    print("can_convert_svg      :", info["can_convert_svg"], "(Windows convert.exe is NOT ImageMagick; never used)")
    print("can_convert_eps      :", info["can_convert_eps"])
    print("can_convert_raster   :", info["can_convert_raster"])


if __name__ == "__main__":
    main()
