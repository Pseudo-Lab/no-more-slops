#!/usr/bin/env python3
"""Static checks on a generated LaTeX project (no compilation needed).

Usage:
    python lint_project.py <project_dir> [--main main.tex] [--json]

Checks:
  * main.tex at project root; every \\input/\\include target exists
  * \\includegraphics targets exist, use relative forward-slash paths
  * bibliography file exists; every \\cite key is defined; duplicate / unused keys
  * every \\ref-like target has a \\label; duplicate labels
  * page-limit markers (pl:refsstart) present
  * formatting "cheats" that violate the skill's typesetting rules
    (font shrinking, \\linespread, margin/textheight edits, negative \\vspace,
    \\resizebox on tables, \\enlargethispage ...)
  * absolute or machine-specific paths anywhere in the sources

Exit status 1 when any ERROR is found, else 0.
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path


for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass

GRAPHIC_EXTS = ("", ".pdf", ".png", ".jpg", ".jpeg", ".eps")
CITE_RE = re.compile(r"\\(?:[a-zA-Z]*cite[a-zA-Z]*|nocite)\*?(?:\[[^\]]*\]){0,2}\{([^}]*)\}")
REF_RE = re.compile(r"\\(?:ref|eqref|autoref|pageref|cref|Cref|nameref|vref)\*?\{([^}]*)\}")
LABEL_RE = re.compile(r"\\label\{([^}]*)\}")
GRAPHICS_RE = re.compile(r"\\includegraphics\*?(?:\[[^\]]*\])?\{([^}]*)\}")
INPUT_RE = re.compile(r"\\(?:input|include|subfile)\{([^}]*)\}")
BIB_RE = re.compile(r"\\(?:bibliography|addbibresource)\{([^}]*)\}")
BIBKEY_RE = re.compile(r"@(\w+)\s*[{(]\s*([^,\s]+)\s*,")
ABS_PATH_RE = re.compile(r"(?:\{|\s)((?:[A-Za-z]:[\\/]|/(?:home|Users|mnt|tmp|var|c)/|~/)[^}\s]*)")

CHEATS = [
    (r"\\fontsize\s*\{", "ERROR", "\\fontsize changes the font size"),
    (r"\\linespread\s*\{", "ERROR", "\\linespread changes line spacing"),
    (r"\\renewcommand\s*\{?\\baselinestretch", "ERROR", "\\baselinestretch changes line spacing"),
    (r"\\(?:set|addto)length\s*\{?\\(?:textheight|textwidth|topmargin|oddsidemargin|evensidemargin|headheight|headsep|footskip|marginparwidth|baselineskip|columnsep)\b", "ERROR", "page-geometry / baseline edit"),
    (r"\\enlargethispage", "ERROR", "\\enlargethispage stretches the text block"),
    (r"\\usepackage(?:\[[^\]]*\])?\{[^}]*\b(?:savetrees|titlesec)\b", "WARN", "space-squeezing package; confirm it does not shrink fonts or margins"),
    (r"\\vspace\*?\s*\{\s*-", "ERROR", "negative \\vspace (space hack)"),
    (r"\\(?:resizebox|scalebox)\s*\{", "WARN", "\\resizebox/\\scalebox shrinks text inside tables/figures; prefer column-width layout"),
    (r"\\(?:tiny|scriptsize)\b", "ERROR", "\\tiny/\\scriptsize used; too small for body or tables"),
    (r"\\footnotesize\b", "WARN", "\\footnotesize used; allowed only for code/table notes with user approval"),
    (r"\\setlength\s*\{?\\(?:abovedisplayskip|belowdisplayskip|textfloatsep|floatsep|intextsep|abovecaptionskip|belowcaptionskip|parskip|parindent)", "WARN", "float/display spacing edit; record in report as a formatting adjustment"),
]


def strip_comments(text):
    return "\n".join(re.sub(r"(?<!\\)%.*$", "", line) for line in text.splitlines())


def load_tex_tree(root, main, issues):
    """Return list of (relpath, text_without_comments) for main + inputs."""
    seen, out = set(), []
    stack = [main]
    while stack:
        rel = stack.pop()
        p = (root / rel)
        if p.suffix == "":
            p = p.with_suffix(".tex")
        key = p.resolve()
        if key in seen:
            continue
        seen.add(key)
        if not p.exists():
            issues.append(("ERROR", f"input file missing: {rel}"))
            continue
        raw = p.read_text(encoding="utf-8", errors="replace")
        text = strip_comments(raw)
        out.append((str(p.relative_to(root)).replace("\\", "/"), text))
        for inc in INPUT_RE.findall(text):
            stack.append(inc.strip())
    return out


def line_of(text, pos):
    return text.count("\n", 0, pos) + 1


def lint(root, main="main.tex"):
    root = Path(root).resolve()
    issues = []
    stats = {}
    if not (root / main).exists():
        return [("ERROR", f"{main} not found at project root")], stats
    files = load_tex_tree(root, main, issues)
    alltext = "\n".join(t for _, t in files)

    gp_groups = "".join(re.findall(r"\\graphicspath\s*\{((?:\{[^{}]*\})+)\}", alltext))
    gpaths = [""] + re.findall(r"\{([^{}]*)\}", gp_groups)
    for d in gpaths[1:]:
        if re.match(r"^([A-Za-z]:|/|~)", d) or "\\" in d:
            issues.append(("ERROR", f"non-portable \\graphicspath entry '{d}'"))
    for rel, text in files:
        for m in GRAPHICS_RE.finditer(text):
            g = m.group(1).strip()
            ln = line_of(text, m.start())
            if "\\" in g or re.match(r"^([A-Za-z]:|/|~)", g):
                issues.append(("ERROR", f"{rel}:{ln}: non-portable graphics path '{g}' (use relative forward-slash path)"))
            if not any((root / d / (g + e)).is_file() for d in gpaths for e in GRAPHIC_EXTS):
                issues.append(("ERROR", f"{rel}:{ln}: graphic not found: {g}"))
        for m in ABS_PATH_RE.finditer(text):
            issues.append(("ERROR", f"{rel}:{line_of(text, m.start())}: absolute/machine-specific path: {m.group(1)}"))
        for pat, sev, msg in CHEATS:
            for m in re.finditer(pat, text):
                issues.append((sev, f"{rel}:{line_of(text, m.start())}: {msg}"))

    # bibliography
    bibs = [b.strip() for grp in BIB_RE.findall(alltext) for b in grp.split(",")]
    bibkeys = []
    for b in bibs:
        bp = root / (b if b.endswith(".bib") else b + ".bib")
        if not bp.exists():
            issues.append(("ERROR", f"bibliography file missing: {bp.name}"))
            continue
        btxt = bp.read_text(encoding="utf-8", errors="replace")
        bibkeys += [k for t, k in BIBKEY_RE.findall(btxt) if t.lower() not in ("string", "preamble", "comment")]
        for m in ABS_PATH_RE.finditer(btxt):
            if not re.match(r"https?:", m.group(1)):
                issues.append(("WARN", f"{bp.name}: possible absolute path: {m.group(1)}"))
    stats["bib_entries"] = len(bibkeys)
    for k, c in Counter(bibkeys).items():
        if c > 1:
            issues.append(("ERROR", f"duplicate bib key: {k}"))
    cited = [k.strip() for grp in CITE_RE.findall(alltext) for k in grp.split(",") if k.strip()]
    stats["cite_commands_keys"] = len(cited)
    nocite_all = "*" in cited
    cited_set = {k for k in cited if k != "*"}
    for k in sorted(cited_set - set(bibkeys)):
        issues.append(("ERROR", f"cited key not in bibliography: {k}"))
    if not nocite_all:
        for k in sorted(set(bibkeys) - cited_set):
            issues.append(("WARN", f"bib entry never cited (will not print): {k}"))
    if not bibs and cited_set:
        issues.append(("ERROR", "citations present but no \\bibliography/\\addbibresource"))

    # labels / refs
    labels = LABEL_RE.findall(alltext)
    stats["labels"] = len(labels)
    for k, c in Counter(labels).items():
        if c > 1:
            issues.append(("ERROR", f"duplicate label: {k}"))
    refs = {k.strip() for grp in REF_RE.findall(alltext) for k in grp.split(",")}
    for k in sorted(refs - set(labels)):
        issues.append(("ERROR", f"reference to undefined label: {k}"))

    if "pl:refsstart" not in labels:
        issues.append(("WARN", "page-limit marker \\label{pl:refsstart} missing; page checks will be impossible"))

    # asset files shipped in figures/ or tables/ but never used (forgotten or redundant visuals)
    used = set()
    for g in GRAPHICS_RE.findall(alltext):
        for d in gpaths:
            used.add(str(Path(d + g.strip()).with_suffix("")).replace("\\", "/").lower())
    for inc in INPUT_RE.findall(alltext):
        used.add(str(Path(inc.strip()).with_suffix("")).replace("\\", "/").lower())
    for sub in ("figures", "tables"):
        for p in sorted((root / sub).rglob("*")) if (root / sub).is_dir() else []:
            if p.is_file():
                rel = str(p.relative_to(root).with_suffix("")).replace("\\", "/").lower()
                if rel not in used:
                    issues.append(("WARN", f"{p.relative_to(root).as_posix()} is never used by main.tex (remove it or record why it is shipped)"))

    stats["figures"] = len(re.findall(r"\\begin\{figure\*?\}", alltext))
    stats["tables"] = len(re.findall(r"\\begin\{table\*?\}", alltext))
    stats["equations_numbered"] = len(re.findall(r"\\begin\{(?:equation|align|gather|multline)\}", alltext))
    stats["footnotes"] = len(re.findall(r"\\footnote\{", alltext))
    stats["small_in_floats"] = len(re.findall(r"\\small\b", alltext))
    stats["tex_files"] = [r for r, _ in files]
    return issues, stats


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__)
        sys.exit(2)
    main_tex = "main.tex"
    if "--main" in sys.argv:
        main_tex = sys.argv[sys.argv.index("--main") + 1]
        args = [a for a in args if a != main_tex]
    issues, stats = lint(args[0], main_tex)
    if "--json" in sys.argv:
        print(json.dumps({"issues": issues, "stats": stats}, indent=2))
    else:
        for sev, msg in issues:
            print(f"[{sev}] {msg}")
        print("stats:", json.dumps(stats))
        n_err = sum(1 for s, _ in issues if s == "ERROR")
        print(f"\n{n_err} error(s), {len(issues) - n_err} warning(s)")
    sys.exit(1 if any(s == "ERROR" for s, _ in issues) else 0)


if __name__ == "__main__":
    main()
