#!/usr/bin/env python3
"""Package a LaTeX project as an Overleaf-ready ZIP and (optionally) verify it.

Usage:
    python make_overleaf_zip.py <project_dir> [--zip <path.zip>] [--verify] [--engine pdflatex]

Default ZIP path: <project_dir>/<project_dir_name>_overleaf.zip

Included: every source file of the project (main.tex at the ZIP root,
references.bib, figures/, tables/, sections/, README.md, any local .cls/.sty/.bst).
Excluded: _build/, _conversion/, LaTeX build artefacts, the compiled main.pdf at
the root, the conversion report, and *.zip files.

--verify  extracts the ZIP into <project_dir>/_conversion/zip_verify/, lints it,
          and compiles it there (latexmk/pdflatex) to prove it is self-contained.
The script never uploads anything anywhere.
"""
import json
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from lint_project import lint  # noqa: E402


for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass

EXCLUDE_DIRS = {"_build", "_conversion", "__pycache__", ".git", ".vscode"}
EXCLUDE_EXT = {".aux", ".log", ".out", ".blg", ".bbl", ".bcf", ".run.xml", ".fls", ".fdb_latexmk",
               ".synctex.gz", ".toc", ".lof", ".lot", ".zip", ".xdv", ".dvi", ".nav", ".snm"}
EXCLUDE_ROOT_FILES = {"main.pdf", "conversion_report.md"}


def wanted(rel: Path):
    if any(part in EXCLUDE_DIRS for part in rel.parts):
        return False
    name = rel.name
    if any(name.endswith(e) for e in EXCLUDE_EXT) or name in (".DS_Store", "Thumbs.db"):
        return False
    if len(rel.parts) == 1 and name in EXCLUDE_ROOT_FILES:
        return False
    return True


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__)
        sys.exit(2)
    root = Path(args[0]).resolve()
    zip_path = Path(sys.argv[sys.argv.index("--zip") + 1]).resolve() if "--zip" in sys.argv \
        else root / f"{root.name}_overleaf.zip"
    engine = sys.argv[sys.argv.index("--engine") + 1] if "--engine" in sys.argv else "pdflatex"
    if not (root / "main.tex").exists():
        sys.exit("main.tex missing at project root; Overleaf would not find the main document")

    files = sorted(p for p in root.rglob("*") if p.is_file() and wanted(p.relative_to(root)))
    if zip_path.exists():
        zip_path.unlink()  # only ever our own previous archive (*.zip inside/next to project)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in files:
            zf.write(p, p.relative_to(root).as_posix())
    print(f"wrote {zip_path} ({zip_path.stat().st_size / 1024:.1f} KiB, {len(files)} files)")
    for p in files:
        print("   ", p.relative_to(root).as_posix())

    # every supplied visual decided "include" must be inside the archive
    manifest = root / "_conversion" / "visuals_manifest.json"
    missing_assets = []
    if manifest.exists():
        names = {p.relative_to(root).as_posix() for p in files}
        man = json.loads(manifest.read_text(encoding="utf-8"))
        for a in man.get("assets", []):
            d = a.get("decision") or {}
            if d.get("action") == "include" and (d.get("project_path") or "").replace("\\", "/") not in names:
                missing_assets.append(f"{Path(a['path']).name} -> {d.get('project_path')}")
        undecided = [Path(a["path"]).name for a in man.get("assets", []) if not (a.get("decision") or {}).get("action")]
        print(f"supplied visuals: {sum(1 for a in man.get('assets', []) if (a.get('decision') or {}).get('action') == 'include')} "
              f"included, {len(missing_assets)} missing from zip, {len(undecided)} undecided")
        for m in missing_assets:
            print("    MISSING FROM ZIP:", m)
        for u in undecided:
            print("    UNDECIDED (not allowed):", u)
        missing_assets += undecided
    if missing_assets and "--verify" not in sys.argv:
        sys.exit(1)

    if "--verify" not in sys.argv:
        return
    vdir = root / "_conversion" / "zip_verify"
    if vdir.exists():
        shutil.rmtree(vdir)
    vdir.mkdir(parents=True)
    with zipfile.ZipFile(zip_path) as zf:
        bad = [n for n in zf.namelist() if n.startswith("/") or ".." in n.split("/") or "\\" in n]
        if bad:
            sys.exit(f"unsafe/non-portable names in zip: {bad}")
        zf.extractall(vdir)
    issues, _ = lint(vdir)
    errs = [m for s, m in issues if s == "ERROR"]
    print(f"\nverify: lint on extracted zip -> {len(errs)} error(s)")
    for e in errs:
        print("    ", e)
    rc = subprocess.run([sys.executable, str(HERE / "compile_and_check.py"), str(vdir), "--pages", "0",
                         "--engine", engine], capture_output=True, text=True, errors="replace")
    ok = rc.returncode == 0 and (vdir / "main.pdf").exists()
    print(f"verify: clean compile from extracted zip -> {'OK' if ok else 'FAILED'}")
    if not ok:
        print(rc.stdout[-3000:], rc.stderr[-1000:])
    sys.exit(0 if ok and not errs and not missing_assets else 1)


if __name__ == "__main__":
    main()
