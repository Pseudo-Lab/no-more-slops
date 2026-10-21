#!/usr/bin/env python3
"""Compile a LaTeX paper and enforce a page limit on the ACTUAL compiled PDF.

Usage:
    python check_page_limit.py <latex_dir> [--limit N] [--venue ID] [--main main.tex]
                               [--engine pdflatex|xelatex|lualatex]
                               [--timeout 300] [--reset] [--no-record] [--json]

Configuration: <latex_dir>/pagelimit.json (optional; CLI flags override it):
    {"venue": "default-4", "limit": 4, "main": "main.tex", "engine": "pdflatex",
     "references_count": false, "appendix_counts": false, "max_iterations": 6,
     "required_sections": ["Introduction", "Method", "Experiment|Results",
                           "Limitation", "Conclusion"],
     "required_labels": ["tab:main"], "enforce": true}
Venue defaults come from ~/.claude/skills/paper-writer/references/venue_profiles.json.

Body-end markers (first one found wins):
    \\label{pl:bodyend}     placed right after the last line of the Conclusion
    \\label{pl:refsstart}   paper-to-latex template (after \\clearpage before refs)
    fallback: first PDF page with a "References"/"Bibliography" heading (heuristic, WARN)

What it does:
    1. static checks: forbidden formatting hacks (lint_project.CHEATS), venue template
       (documentclass, font size, required options/packages, geometry), required
       sections and labels (guards against silently deleting essential content);
    2. compiles with compile_and_check.py (latexmk);
    3. counts the pages that count toward the limit from the compiled PDF;
    4. if over: estimates the overflow in words/lines from the PDF text;
    5. records the attempt in <latex_dir>/_pagecheck/history.jsonl and stops the
       revision loop after max_iterations distinct failed revisions.

Exit codes:
    0 PASS                         4 CONFIG ERROR
    1 OVER LIMIT (revise + rerun)  5 MAX ITERATIONS reached (failure: report to user)
    2 COMPILE FAILURE              6 ESSENTIAL CONTENT MISSING (restore it)
    3 FORMAT / TEMPLATE VIOLATION
Outputs: _pagecheck/report.json, _pagecheck/report.md, _pagecheck/history.jsonl,
         _pagecheck/PAGE_LIMIT_FAILURE.md (exit 5 only).
"""
import datetime as _dt
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import compile_and_check as cc  # noqa: E402
import lint_project as lp  # noqa: E402

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass

VENUES = HERE.parents[1] / "paper-writer" / "references" / "venue_profiles.json"
STATUS_EXIT = {"PASS": 0, "OVER_LIMIT": 1, "COMPILE_FAILURE": 2, "FORMAT_VIOLATION": 3,
               "CONFIG_ERROR": 4, "MAX_ITERATIONS": 5, "ESSENTIAL_CONTENT_MISSING": 6}
REF_HEAD = re.compile(r"^\s*(?:\d+\.?\s+)?(References|Bibliography|REFERENCES|BIBLIOGRAPHY)\s*$")


def opt(name, default=None, flag=False):
    if flag:
        return name in sys.argv
    if name in sys.argv:
        i = sys.argv.index(name)
        if i + 1 < len(sys.argv):
            return sys.argv[i + 1]
    return default


def load_config(root):
    cfg, problems = {}, []
    p = root / "pagelimit.json"
    if p.exists():
        try:
            cfg = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            problems.append(f"pagelimit.json is not valid JSON: {e}")
    try:
        venues = json.loads(VENUES.read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        venues = {"default": "default-4", "profiles": {}}
        problems.append(f"cannot read venue profiles {VENUES}: {e}")
    vid = opt("--venue") or cfg.get("venue") or venues.get("default", "default-4")
    prof = venues.get("profiles", {}).get(vid)
    if prof is None:
        problems.append(f"unknown venue profile '{vid}' (known: {sorted(venues.get('profiles', {}))})")
        prof = {}
    eff = {
        "venue": vid,
        "limit": prof.get("limit"),
        "references_count": prof.get("references_count", False),
        "appendix_counts": prof.get("appendix_counts", False),
        "min_font_pt": prof.get("min_font_pt", 10),
        "documentclass": prof.get("documentclass"),
        "required_options": prof.get("required_options", []),
        "required_packages": prof.get("required_packages", []),
        "main": "main.tex", "engine": "pdflatex", "max_iterations": 6,
        "required_sections": [], "required_labels": [], "enforce": True,
        "allow_geometry": vid == "default-4",
        "required_geometry": prof.get("required_geometry", []),
        "soft_limit": prof.get("soft_limit", False),
        "kit": prof.get("kit"),
    }
    venue_keys = {"venue", "limit", "references_count", "appendix_counts"}
    for k, v in cfg.items():
        if opt("--venue") and k in venue_keys:
            continue  # an explicit --venue replaces the file's venue-derived settings
        eff[k] = v
    if opt("--limit"):
        eff["limit"] = float(opt("--limit"))
    if opt("--main"):
        eff["main"] = opt("--main")
    if opt("--engine"):
        eff["engine"] = opt("--engine")
    if eff["limit"] is None:
        problems.append("no page limit: give --limit, a pagelimit.json 'limit', or a venue profile")
    elif float(eff["limit"]) <= 0:
        problems.append("page limit must be positive")
    if not (root / eff["main"]).exists():
        problems.append(f"main file not found: {root / eff['main']}")
    return eff, problems


def static_checks(root, cfg):
    violations, warnings, missing = [], [], []
    issues = []
    tree = lp.load_tex_tree(root, cfg["main"], issues)
    for sev, msg in issues:
        (violations if sev == "ERROR" else warnings).append(msg)
    alltext = "\n".join(t for _, t in tree)
    for rel, text in tree:
        for pat, sev, why in lp.CHEATS:
            for m in re.finditer(pat, text):
                line = text.count("\n", 0, m.start()) + 1
                (violations if sev == "ERROR" else warnings).append(f"{rel}:{line}: {why}")
    main_text = tree[0][1] if tree else ""
    m = re.search(r"\\documentclass\s*(?:\[([^\]]*)\])?\s*\{([^}]*)\}", main_text)
    if not m:
        violations.append("no \\documentclass found in main file")
    else:
        opts = [o.strip() for o in (m.group(1) or "").split(",") if o.strip()]
        cls = m.group(2).strip()
        if cfg.get("documentclass") and cls != cfg["documentclass"]:
            violations.append(f"template mismatch: documentclass '{cls}' but venue '{cfg['venue']}' "
                              f"expects '{cfg['documentclass']}'")
        if cls.startswith("ext") or cls in ("extarticle",):
            violations.append(f"documentclass '{cls}' allows sub-10pt body fonts")
        for o in opts:
            fm = re.fullmatch(r"(\d+(?:\.\d+)?)pt", o)
            if fm and float(fm.group(1)) < float(cfg.get("min_font_pt", 10)):
                violations.append(f"body font option {o} is below the venue minimum "
                                  f"{cfg.get('min_font_pt', 10)}pt")
        for ro in cfg.get("required_options", []):
            if ro not in opts:
                violations.append(f"template mismatch: documentclass option '{ro}' required by "
                                  f"venue '{cfg['venue']}' is missing")
    used = re.findall(r"\\(?:usepackage|RequirePackage)\s*(?:\[[^\]]*\])?\s*\{([^}]*)\}", alltext)
    pkgs = [p.strip() for grp in used for p in grp.split(",")]
    for rp in cfg.get("required_packages", []):
        if not any(p.startswith(rp) for p in pkgs):
            violations.append(f"template mismatch: venue style package '{rp}*' not loaded "
                              f"(venue '{cfg['venue']}' requires its official style)")
    if re.search(r"\\usepackage\s*(?:\[[^\]]*\])?\s*\{geometry\}", alltext) and not cfg.get("allow_geometry"):
        violations.append("geometry package loaded on top of a venue style (margins are fixed by the venue)")
    gm = re.search(r"\\usepackage\s*\[([^\]]*)\]\s*\{geometry\}", alltext)
    if gm and cfg.get("required_geometry"):
        gopts = {o.strip().replace(" ", "") for o in gm.group(1).split(",")}
        for req in cfg["required_geometry"]:
            if req.replace(" ", "") not in gopts:
                violations.append(f"geometry options {sorted(gopts)} differ from the template's "
                                  f"required '{req}' (margins must not be changed)")
    if re.search(r"\\newgeometry|\\geometry\s*\{", alltext):
        violations.append("\\newgeometry/\\geometry{} changes the page layout")
    if re.search(r"\\(?:clearpage|newpage|cleardoublepage)\s*(?:\\phantomsection\s*)?\\label\{pl:bodyend\}", alltext):
        violations.append("\\label{pl:bodyend} sits right after a page break, so it marks the next page; "
                          "move it before the \\clearpage, directly after the Conclusion's last line")
    titles = re.findall(r"\\section\*?\s*(?:\[[^\]]*\])?\s*\{([^}]*)\}", alltext)
    for pat in cfg.get("required_sections", []):
        if not any(re.search(pat, t, re.I) for t in titles):
            missing.append(f"required section matching '{pat}' not found (sections: {titles})")
    labels = set(re.findall(r"\\label\{([^}]*)\}", alltext))
    for lab in cfg.get("required_labels", []):
        if lab not in labels:
            missing.append(f"required label '{lab}' not found (essential table/figure removed?)")
    return violations, warnings, missing, alltext


def page_texts(pdf, first, last):
    """Reading-order text per page (no -layout: two-column lines must not be merged)."""
    out = {}
    if not shutil.which("pdftotext"):
        return {p: "" for p in range(first, last + 1)}
    for p in range(first, last + 1):
        r = subprocess.run(["pdftotext", "-f", str(p), "-l", str(p), str(pdf), "-"],
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        out[p] = r.stdout or ""
    return out


def body_words(text):
    lines = [l for l in text.splitlines() if l.strip() and not re.fullmatch(r"\s*\d+\s*", l)]
    cut = None
    for i, l in enumerate(lines):
        if REF_HEAD.match(l):
            cut = i
            break
    if cut is not None:
        lines = lines[:cut]
    return len(" ".join(lines).split()), len(lines)


def tex_hash(root, cfg):
    h = hashlib.sha256()
    for p in sorted(root.rglob("*")):
        if p.suffix in (".tex", ".bib", ".sty", ".cls") and "_build" not in p.parts and "_pagecheck" not in p.parts:
            h.update(p.relative_to(root).as_posix().encode())
            h.update(p.read_bytes())
    for p in sorted((root / "figures").rglob("*")) if (root / "figures").exists() else []:
        if p.is_file():
            h.update(p.relative_to(root).as_posix().encode())
            h.update(str(p.stat().st_size).encode())
    return h.hexdigest()[:16]


def main():
    if len(sys.argv) < 2 or sys.argv[1].startswith("--"):
        print(__doc__)
        sys.exit(4)
    root = Path(sys.argv[1]).resolve()
    pc = root / "_pagecheck"
    pc.mkdir(exist_ok=True)
    hist_p = pc / "history.jsonl"
    if opt("--reset", flag=True) and hist_p.exists():
        hist_p.unlink()
    cfg, cfg_problems = load_config(root)
    rep = {"project": str(root), "checked_at": _dt.datetime.now().isoformat(timespec="seconds"),
           "config": cfg, "violations": [], "warnings": [], "missing_content": [], "problems": []}

    status = None
    if cfg_problems:
        rep["problems"] = cfg_problems
        status = "CONFIG_ERROR"
    else:
        v, w, miss, alltext = static_checks(root, cfg)
        rep["violations"], rep["warnings"], rep["missing_content"] = v, w, miss
        cmd = [sys.executable, str(HERE / "compile_and_check.py"), str(root), "--pages", "0",
               "--main", cfg["main"], "--engine", cfg["engine"], "--timeout", str(opt("--timeout", "300"))]
        import time as _time
        t_start = _time.time() - 2  # filesystem timestamp slack
        try:
            r = subprocess.run(cmd, stdin=subprocess.DEVNULL, capture_output=True, text=True, encoding="utf-8",
                               errors="replace", timeout=int(opt("--timeout", "300")) + 120)
        except subprocess.TimeoutExpired:
            # an orphaned grandchild (e.g. bibtex) kept the pipe open past compile_and_check's own timeout
            r = subprocess.CompletedProcess(cmd, 124, stdout="TIMEOUT: compile did not finish (orphaned "
                                            "LaTeX/BibTeX process?)", stderr="")
        crep_p = root / "_conversion" / "compile_report.json"
        crep = json.loads(crep_p.read_text(encoding="utf-8")) if crep_p.exists() else {}
        rep["compile"] = {"rc": r.returncode, "compiled": crep.get("compiled"),
                          "errors": (crep.get("log") or {}).get("errors", [])[:10],
                          "undefined_citations": (crep.get("log") or {}).get("undefined_citations", []),
                          "undefined_references": (crep.get("log") or {}).get("undefined_references", [])}
        stem = Path(cfg["main"]).stem
        pdf = root / "_build" / f"{stem}.pdf"
        aux = root / "_build" / f"{stem}.aux"
        stale = pdf.exists() and pdf.stat().st_mtime < t_start
        if stale:
            rep["compile"]["errors"].append("the PDF was not rebuilt by this check (stale output from an earlier "
                                            "build); latexmk failed before writing a new PDF")
        if crep.get("steps") and any(s.get("rc") not in (0, None) for s in crep["steps"]) and not stale:
            rep["warnings"].append(f"latexmk exited non-zero ({[s.get('rc') for s in crep['steps']]}); "
                                   "the PDF was rebuilt but check the build log")
        if not pdf.exists() or rep["compile"]["errors"]:
            status = "COMPILE_FAILURE"
            rep["compile"]["output_tail"] = r.stdout[-1500:]
        else:
            total = cc.page_count(pdf)
            auxt = aux.read_text(encoding="utf-8", errors="replace") if aux.exists() else ""
            bodyend = cc.label_page(auxt, "pl:bodyend")
            refs = cc.label_page(auxt, "pl:refsstart")
            appx = cc.label_page(auxt, "pl:appendixstart")
            method, counted = None, None
            for lab, val in (("pl:bodyend", bodyend), ("pl:refsstart", refs)):
                if ("\\label{" + lab + "}") in alltext and val is None:
                    v.append(f"\\label{{{lab}}} is in the source but not in the compiled .aux (placed after "
                             "\\end{document}, or inside an unused branch); move it right after the Conclusion")
            if cfg["references_count"]:
                if cfg["appendix_counts"] or not isinstance(appx, int):
                    counted, method = total, "total pages (references count)"
                else:
                    counted, method = appx - 1, "pages before pl:appendixstart (references count)"
            elif isinstance(bodyend, int):
                counted, method = bodyend, "page of \\label{pl:bodyend}"
            elif isinstance(refs, int):
                counted, method = refs - 1, "pages before \\label{pl:refsstart}"
            else:
                texts = page_texts(pdf, 1, total or 0)
                for p in range(1, (total or 0) + 1):
                    lines = [l for l in texts[p].splitlines() if l.strip()]
                    idx = next((i for i, l in enumerate(lines) if REF_HEAD.match(l)), None)
                    if idx is not None:
                        counted = p - 1 if idx <= 1 else p
                        break
                counted = counted if counted is not None else total
                method = "HEURISTIC: first 'References' heading in PDF text"
                rep["warnings"].append("no pl:bodyend / pl:refsstart marker; page count is heuristic. "
                                       "Add \\label{pl:bodyend} after the Conclusion.")
            limit = float(cfg["limit"])
            rep["pages"] = {"total_pdf_pages": total, "counted_pages": counted, "limit": limit,
                            "method": method, "bodyend_page": bodyend, "refs_start_page": refs,
                            "appendix_start_page": appx}
            over = counted > limit
            if counted < limit:
                rep["warnings"].append(f"underflow: {counted} counted page(s) < limit {limit:g}. "
                                       "Never pad; report it if the venue requires exactly N pages.")
            if counted > limit:
                first_over = int(limit) + 1
                texts = page_texts(pdf, first_over, counted)
                words = lines = 0
                for p in range(first_over, counted + 1):
                    wd, ln = body_words(texts.get(p, ""))
                    words, lines = words + wd, lines + ln
                rep["pages"]["overflow"] = {"pages_over": counted - limit, "body_words_beyond_limit": words,
                                            "body_lines_beyond_limit": lines,
                                            "advice": f"Cut at least ~{words} words (~{lines} text lines) or "
                                                      "equivalent float space, following the cut ladder in "
                                                      "paper_standards.md §6. Never shrink fonts/margins."}
            if miss:
                status = "ESSENTIAL_CONTENT_MISSING"
            elif v:
                status = "FORMAT_VIOLATION"
            elif over and cfg.get("soft_limit"):
                status = "PASS"
                rep["warnings"].append(f"over the SOFT limit ({counted} > {limit:g}); venue has no hard limit, "
                                       "justify the length or shorten")
            elif over:
                status = "OVER_LIMIT"
            elif method.startswith("HEURISTIC"):
                # A heading-based count can UNDER-count (e.g. a section titled "References" inside the body),
                # so it may never certify compliance. Verified on the IJCAI-26 kit: heuristic said 3, true is 6.
                status = "FORMAT_VIOLATION"
                rep["violations"].append("no body-end marker: the heuristic count cannot certify the limit. "
                                         "Put \\label{pl:bodyend} right after the Conclusion's last line "
                                         "(or use paper-to-latex's pl:refsstart marker) and re-run.")
            else:
                status = "PASS"

    # ---- iteration bookkeeping -------------------------------------------------------
    history = []
    if hist_p.exists():
        for line in hist_p.read_text(encoding="utf-8").splitlines():
            try:
                history.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    sha = tex_hash(root, cfg) if status != "CONFIG_ERROR" else None
    entry = {"ts": rep["checked_at"], "status": status, "sha": sha,
             "counted": (rep.get("pages") or {}).get("counted_pages"), "limit": cfg.get("limit"),
             "words_over": ((rep.get("pages") or {}).get("overflow") or {}).get("body_words_beyond_limit")}
    tail = []
    for h in reversed(history):
        if h.get("status") == "PASS":
            break
        tail.append(h)
    if status not in ("PASS", "CONFIG_ERROR"):
        shas = {h.get("sha") for h in tail} | {sha}
        rep["failed_revisions"] = len(shas)
        if tail and tail[0].get("sha") == sha:
            rep["warnings"].append("no source change since the previous failed check")
        maxit = int(cfg.get("max_iterations", 6))
        rep["max_iterations"] = maxit
        if len(shas) >= maxit:
            rep["underlying_status"] = status
            status = "MAX_ITERATIONS"
    entry["final_status"] = status
    if not opt("--no-record", flag=True):
        with hist_p.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
    rep["status"] = status
    rep["sha"] = sha
    rep["exit_code"] = STATUS_EXIT[status]
    rep["enforce"] = bool(cfg.get("enforce", True))

    (pc / "report.json").write_text(json.dumps(rep, indent=2), encoding="utf-8")
    md = [f"# Page check: {status}", "", f"- project: `{root}`", f"- venue: `{cfg.get('venue')}`  limit: {cfg.get('limit')}"]
    if "pages" in rep:
        P = rep["pages"]
        md.append(f"- counted pages: **{P['counted_pages']}** of {P['total_pdf_pages']} PDF pages ({P['method']})")
        if "overflow" in P:
            md.append(f"- overflow: {P['overflow']['advice']}")
    for k in ("problems", "violations", "missing_content", "warnings"):
        if rep.get(k):
            md += ["", f"## {k}"] + [f"- {x}" for x in rep[k]]
    if rep.get("compile", {}).get("errors"):
        md += ["", "## compile errors"] + [f"- {x}" for x in rep["compile"]["errors"]]
    if status not in ("PASS",):
        md += ["", f"failed revisions in this campaign: {rep.get('failed_revisions', '-')}"
               f" / max {rep.get('max_iterations', cfg.get('max_iterations'))}"]
    (pc / "report.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    if status == "MAX_ITERATIONS":
        (pc / "PAGE_LIMIT_FAILURE.md").write_text(
            "# Page limit not met: author decision needed\n\n"
            f"After {rep.get('failed_revisions')} distinct revisions the paper still fails "
            f"({rep.get('underlying_status')}).\n\n"
            + "\n".join(md[2:]) +
            "\n\nDo NOT cut protected content (paper_standards.md §6 item 4) to force compliance. "
            "Report to the user: measured overflow, what was already cut, what remains and why it is "
            "essential, and options (approve specific cuts / move named items to an appendix / "
            "change the limit or venue). Re-run with --reset after the user decides.\n",
            encoding="utf-8")

    if opt("--json", flag=True):
        print(json.dumps(rep, indent=2))
    else:
        print("\n".join(md))
        print(f"\nreport: {pc / 'report.json'}")
    sys.exit(rep["exit_code"])


if __name__ == "__main__":
    main()
