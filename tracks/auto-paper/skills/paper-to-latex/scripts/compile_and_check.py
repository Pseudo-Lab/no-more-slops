#!/usr/bin/env python3
"""Compile a LaTeX project and verify layout / page-limit requirements.

Usage:
    python compile_and_check.py <project_dir> [--pages N] [--engine pdflatex|xelatex|lualatex]
                                [--main main.tex] [--outdir _build] [--timeout 600]

--pages N   required main-paper length (default 4). 0 disables the page check.

Builds into <project_dir>/<outdir> (default _build), copies the PDF to
<project_dir>/main.pdf, writes <project_dir>/_conversion/compile_report.json,
and prints a summary.

Page accounting relies on markers that the skill's template places in main.tex:
    \\label{pl:refsstart}     immediately after the \\clearpage before the bibliography
    \\label{pl:appendixstart} (optional) first page of appendices placed after references
main pages     = page(pl:refsstart) - 1
reference pages = page(pl:appendixstart) - page(pl:refsstart)   (or total - refsstart + 1)

Exit status: 0 = compiled without LaTeX errors, 1 = errors, 2 = no compiler.
Page-limit pass/fail is reported in the JSON (page_check.ok) - it does not change
the exit status.
"""
import json
import os
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


def arg(name, default):
    if name in sys.argv:
        return sys.argv[sys.argv.index(name) + 1]
    return default


def run(cmd, cwd, timeout):
    """Run cmd; on timeout kill the WHOLE process tree (latexmk -> perl -> pdflatex -> makepk ...)."""
    kw = {"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP} if os.name == "nt" else {"start_new_session": True}
    p = subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                         encoding="utf-8", errors="replace", **kw)
    try:
        out, _ = p.communicate(timeout=timeout)
        return p.returncode, out
    except subprocess.TimeoutExpired:
        if os.name == "nt":
            subprocess.run(["taskkill", "/T", "/F", "/PID", str(p.pid)], capture_output=True)
        else:
            import signal
            os.killpg(p.pid, signal.SIGKILL)
        p.communicate()
        return 124, (f"TIMEOUT after {timeout}s: {' '.join(cmd)}. Process tree killed. Likely cause: the TeX "
                     "distribution is installing a missing package on the fly or generating bitmap (PK) "
                     "fonts (MiKTeX: miktex-makepk/gsf2pk). Check the MiKTeX/TeX Live logs, let the "
                     "install finish (or install the package manually), then re-run.")


def page_count(pdf):
    try:
        from pypdf import PdfReader  # type: ignore
        return len(PdfReader(str(pdf)).pages)
    except Exception:
        pass
    if shutil.which("pdfinfo"):
        out = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True, errors="replace").stdout
        m = re.search(r"Pages:\s+(\d+)", out)
        if m:
            return int(m.group(1))
    return None


def page_text(pdf, p):
    if not shutil.which("pdftotext"):
        return None
    r = subprocess.run(["pdftotext", "-f", str(p), "-l", str(p), "-layout", str(pdf), "-"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.stdout


def label_page(aux_text, label):
    m = re.search(r"\\newlabel\{" + re.escape(label) + r"\}\{\{[^{}]*\}\{([^{}]*)\}", aux_text)
    if not m:
        return None
    try:
        return int(m.group(1))
    except ValueError:
        return m.group(1)


def parse_log(log):
    res = {"errors": [], "undefined_citations": [], "undefined_references": [], "missing_files": [],
           "overfull": [], "underfull_count": 0, "float_too_large": [], "rerun_needed": False,
           "other_warnings": []}
    lines = log.splitlines()
    for i, line in enumerate(lines):
        if line.startswith("!") or re.match(r"^\S+\.tex:\d+: ", line):
            ctx = " | ".join(l.strip() for l in lines[i:i + 3] if l.strip())
            res["errors"].append(ctx[:300])
        m = re.search(r"Citation [`']([^']+)' on page (\d+) undefined", line)
        if m:
            res["undefined_citations"].append(m.group(1))
        m = re.search(r"Reference [`']([^']+)' on page (\d+) undefined", line)
        if m:
            res["undefined_references"].append(m.group(1))
        m = re.search(r"File [`']([^']+)' not found", line)
        if m:
            res["missing_files"].append(m.group(1))
        m = re.match(r"Overfull \\[hv]box \(([\d.]+)pt too (?:wide|high)\) (.*)", line)
        if m and float(m.group(1)) > 1.0:
            res["overfull"].append({"pt": float(m.group(1)), "where": m.group(2)[:120]})
        if line.startswith("Underfull"):
            res["underfull_count"] += 1
        if "Float too large" in line:
            res["float_too_large"].append(line.strip())
        if "Label(s) may have changed" in line or "Rerun to get" in line:
            res["rerun_needed"] = True
        if re.search(r"LaTeX Warning: (?!Citation|Reference|Label\(s\)|There were undefined)", line):
            res["other_warnings"].append(line.strip()[:200])
    for k in ("undefined_citations", "undefined_references", "missing_files"):
        res[k] = sorted(set(res[k]))
    return res


def parse_blg(blg):
    res = {"warnings": [], "errors": []}
    for line in blg.splitlines():
        if line.startswith("Warning--") or line.startswith("WARN"):
            res["warnings"].append(line.strip())
        if "I couldn't open" in line or "I didn't find a database entry" in line or line.startswith("ERROR") \
                or re.search(r"\(There (?:was|were) \d+ error", line):
            res["errors"].append(line.strip())
    return res


def main():
    args = [a for a in sys.argv[1:]]
    if not args or args[0].startswith("--"):
        print(__doc__)
        sys.exit(2)
    root = Path(args[0]).resolve()
    pages_req = int(arg("--pages", "4"))
    engine = arg("--engine", "pdflatex")
    main_tex = arg("--main", "main.tex")
    outdir = arg("--outdir", "_build")
    timeout = int(arg("--timeout", "600"))
    stem = Path(main_tex).stem
    build = root / outdir
    build.mkdir(exist_ok=True)
    (root / "_conversion").mkdir(exist_ok=True)
    report = {"project": str(root), "engine": engine, "pages_required": pages_req, "steps": []}

    uses_biber = "biblatex" in (root / main_tex).read_text(encoding="utf-8", errors="replace") and \
        not re.search(r"backend\s*=\s*bibtex", (root / main_tex).read_text(encoding="utf-8", errors="replace"))

    # BibTeX/biber run inside the build dir; without this they can resolve
    # "references.bib" to a same-named file shipped with the TeX distribution.
    os.environ["BIBINPUTS"] = str(root) + os.pathsep + os.environ.get("BIBINPUTS", "")

    if shutil.which("latexmk") and shutil.which(engine):
        flag = {"pdflatex": "-pdf", "xelatex": "-xelatex", "lualatex": "-lualatex"}[engine]
        cmd = ["latexmk", flag, "-g", "-interaction=nonstopmode", "-file-line-error", "-halt-on-error",
               f"-outdir={outdir}", main_tex]
        rc, out = run(cmd, root, timeout)
        report["steps"].append({"cmd": " ".join(cmd), "rc": rc})
    elif shutil.which(engine):
        bibtool = "biber" if uses_biber else "bibtex"
        rc = 0
        seq = [[engine, "-interaction=nonstopmode", "-file-line-error", f"-output-directory={outdir}", main_tex],
               [bibtool, stem] if bibtool == "bibtex" else [bibtool, f"--input-directory={root}", stem],
               [engine, "-interaction=nonstopmode", "-file-line-error", f"-output-directory={outdir}", main_tex],
               [engine, "-interaction=nonstopmode", "-file-line-error", f"-output-directory={outdir}", main_tex]]
        for cmd in seq:
            cwd = build if cmd[0] in ("bibtex", "biber") else root
            r, out = run(cmd, cwd, timeout)
            report["steps"].append({"cmd": " ".join(cmd), "rc": r})
            rc = rc or (r if cmd[0] == engine else 0)
    else:
        report["compiled"] = False
        report["note"] = "No LaTeX compiler found: compilation and page-count verification are UNVERIFIED."
        (root / "_conversion" / "compile_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
        print(report["note"])
        sys.exit(2)

    log_p, aux_p, pdf_p = build / f"{stem}.log", build / f"{stem}.aux", build / f"{stem}.pdf"
    blg_p = build / f"{stem}.blg"
    log = log_p.read_text(encoding="utf-8", errors="replace") if log_p.exists() else ""
    report["log"] = parse_log(log)
    report["bibliography_tool"] = parse_blg(blg_p.read_text(encoding="utf-8", errors="replace")) if blg_p.exists() else None
    report["timed_out"] = rc == 124
    report["compiled"] = pdf_p.exists() and not report["log"]["errors"] and rc == 0
    report["pdf_produced"] = pdf_p.exists()

    if pdf_p.exists():
        shutil.copy2(pdf_p, root / f"{stem}.pdf")
        total = page_count(pdf_p)
        aux = aux_p.read_text(encoding="utf-8", errors="replace") if aux_p.exists() else ""
        rs = label_page(aux, "pl:refsstart")
        ap = label_page(aux, "pl:appendixstart")
        pc = {"total_pages": total, "refs_start_page": rs, "appendix_start_page": ap}
        if isinstance(rs, int):
            pc["main_pages"] = rs - 1
            end = (ap - 1) if isinstance(ap, int) else total
            pc["reference_pages"] = (end - rs + 1) if end else None
            pc["appendix_pages"] = (total - ap + 1) if isinstance(ap, int) and total else 0
            last = page_text(pdf_p, rs - 1) if rs > 1 else ""
            if last is not None:
                body_lines = [l for l in last.splitlines() if l.strip() and not re.fullmatch(r"\s*\d+\s*", l)]
                pc["last_main_page_nonblank_lines"] = len(body_lines)
            if pages_req:
                problems = []
                if pc["main_pages"] != pages_req:
                    problems.append(f"main paper is {pc['main_pages']} page(s); required {pages_req}")
                if rs != pages_req + 1:
                    problems.append(f"references start on page {rs}; required page {pages_req + 1}")
                if pc.get("last_main_page_nonblank_lines", 1) == 0:
                    problems.append(f"page {rs - 1} is blank (do not pad with empty pages)")
                pc["ok"] = not problems
                pc["problems"] = problems
        else:
            pc["ok"] = False if pages_req else None
            pc["problems"] = ["marker \\label{pl:refsstart} not found in .aux; cannot measure main-paper length"]
        report["page_check"] = pc

    (root / "_conversion" / "compile_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    L = report["log"]
    print(f"compiled: {report['compiled']}  (pdf produced: {report['pdf_produced']})")
    for s in report["steps"]:
        print(f"  rc={s['rc']}  {s['cmd']}")
    if rc == 124 or not log:
        print("  tail of build output:\n" + out[-1500:])
    print(f"errors: {len(L['errors'])}")
    for e in L["errors"][:15]:
        print("   ", e)
    print(f"undefined citations: {L['undefined_citations']}")
    print(f"undefined references: {L['undefined_references']}")
    print(f"missing files: {L['missing_files']}")
    print(f"overfull boxes >1pt: {len(L['overfull'])}")
    for o in L["overfull"][:15]:
        print(f"    {o['pt']}pt {o['where']}")
    print(f"float too large: {len(L['float_too_large'])}; rerun needed: {L['rerun_needed']}")
    if report["bibliography_tool"]:
        b = report["bibliography_tool"]
        print(f"bibtex/biber: {len(b['errors'])} error(s), {len(b['warnings'])} warning(s)")
        for w in (b["errors"] + b["warnings"])[:15]:
            print("   ", w)
    if "page_check" in report:
        print("page check:", json.dumps(report["page_check"]))
    print(f"report: {root / '_conversion' / 'compile_report.json'}")
    sys.exit(0 if report["compiled"] else 1)


if __name__ == "__main__":
    main()
