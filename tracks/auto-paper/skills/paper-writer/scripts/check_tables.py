#!/usr/bin/env python3
"""Check results tables against conference conventions (paper_standards.md §4-§5).

Usage:
    python check_tables.py <paper.tex | paper.md | directory> [--json]

A "main-results table" is one whose label or caption mentions main/results/comparison/
state-of-the-art/SOTA/benchmark (and not ablation/appendix/statistic). Checks:

  T1 ERROR  a provenance marker (\\pub \\repro \\incompat, *, †, ‡, \\dag, \\ddag) is used
            but not defined in the caption / table notes
  T2 WARN   a baseline row in a main-results table has no citation (\\cite / [n])
            and is not the proposed method (Ours / proposed / \\ours)
  T3 WARN   experimental-configuration label in a main-results table
            (Arm, Config, Condition, Control, Setting, Variant, Run, G+P, w/, w/o ...)
  T4 WARN   p-values / confidence intervals / significance stars in a main-results table
            without a "% stats-ok: <reason>" comment (Markdown: <!-- stats-ok: ... -->)
  T5 ERROR  bold/underline inside an incompatible-protocol block (rows marked \\incompat/‡)
  T6 WARN   a row mixes "TBD"/placeholder with bold (ranking an unmeasured value)
  T7 WARN   main-results table has no row that looks like the proposed method

Exit status: 1 if any ERROR, else 0.
"""
import json
import re
import sys
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass

MAIN_RE = re.compile(r"main|result|comparison|state[- ]of[- ]the[- ]art|\bsota\b|benchmark", re.I)
NOT_MAIN_RE = re.compile(r"ablat|appendix|statistic|supplement|tab:stats|hyper", re.I)
CONFIG_RE = re.compile(r"\b(arm|config(uration)?|condition|control|setting|variant|run\s*\d|"
                       r"g\s*\+\s*p|w/o?\b|treatment|cell|only|arm\s*[a-z0-9])\b", re.I)
OURS_RE = re.compile(r"\bours\b|\(ours\)|proposed|\\ours|\\oursrow", re.I)
CITE_RE = re.compile(r"\\(?:[a-zA-Z]*cite[a-zA-Z]*)\*?(?:\[[^\]]*\])*\{[^}]+\}|\[\d+(?:[,\u2013-]\s*\d+)*\]")
STATS_RE = re.compile(r"(?<![a-zA-Z])p\s*[<=>\u2264]\s*0?\.\d|\$p\$|p[_-]?value|\b9[059]\s*\\?%\s*CI\b|\bCI\b|"
                      r"\[\s*-?\d+(?:\.\d+)?\s*,\s*-?\d+(?:\.\d+)?\s*\]|\^\{?\*{1,3}\}?|"
                      r"\\textsuperscript\{\*{2,3}\}|p_\{?\\(?:math|text)", re.I)
MARKERS = {
    "pub": re.compile(r"\\pub\b|\\textsuperscript\{\*\}|\$\^\{?\*\}?\$"),
    "repro": re.compile(r"\\repro\b|\\dag\b|†"),
    "incompat": re.compile(r"\\incompat\b|\\ddag\b|‡"),
}
BOLD_RE = re.compile(r"\\textbf\{|\\best\{|\\second\{|\\underline\{|\*\*")
PLACEHOLDER_RE = re.compile(r"\bTBD\b|xx\.x|\?\?", re.I)


def strip_comments(text):
    return "\n".join(re.sub(r"(?<!\\)%.*$", "", l) for l in text.splitlines())


def tex_tables(text, path):
    out = []
    for m in re.finditer(r"\\begin\{(table\*?)\}(.*?)\\end\{\1\}", text, re.S):
        raw = m.group(2)
        start = text.count("\n", 0, m.start()) + 1
        pre = text[max(0, m.start() - 600):m.start()]
        stats_ok = "stats-ok:" in raw or bool(re.search(r"%\s*stats-ok:", pre[-400:]))
        body = strip_comments(raw)
        cap = re.search(r"\\caption(?:\[[^\]]*\])?\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*)\}", body, re.S)
        caption = cap.group(1) if cap else ""
        label = " ".join(re.findall(r"\\label\{([^}]*)\}", body))
        notes = " ".join(re.findall(r"\\begin\{tablenotes\}(.*?)\\end\{tablenotes\}", body, re.S))
        tab = re.search(r"\\begin\{tabular[x*]?\}(?:\{[^}]*\})?(?:\{(?:[^{}]|\{[^{}]*\})*\})(.*?)\\end\{tabular[x*]?\}",
                        body, re.S)
        rows = []
        if tab:
            for r in re.split(r"\\\\", tab.group(1)):
                r2 = re.sub(r"\\(?:toprule|midrule|bottomrule|hline|cmidrule(?:\([^)]*\))?\{[^}]*\})", "", r).strip()
                if r2:
                    rows.append(r2)
        out.append({"file": str(path), "line": start, "caption": caption, "label": label,
                    "notes": notes, "rows": rows, "stats_ok": stats_ok, "fmt": "tex"})
    return out


CAP_MD = re.compile(r"^\s*(?:\*\*|_)?Table\s+\w+[.:]", re.I)


def md_tables(text, path):
    out, lines = [], text.splitlines()
    heading, tables_under_heading = "", 0
    i = 0
    while i < len(lines):
        if re.match(r"^#{1,4}\s", lines[i]):
            heading, tables_under_heading = lines[i], 0
        if lines[i].lstrip().startswith("|") and i + 1 < len(lines) and re.match(r"^\s*\|?\s*:?-{3,}", lines[i + 1]):
            j = i
            while j < len(lines) and lines[j].lstrip().startswith("|"):
                j += 1
            # caption: nearest "Table N." line within 15 lines above, without crossing another table
            cap_idx = None
            for k in range(i - 1, max(-1, i - 16), -1):
                if lines[k].lstrip().startswith("|") or re.match(r"^#{1,4}\s", lines[k]):
                    break
                if CAP_MD.match(lines[k]):
                    cap_idx = k
                    break
            caption = lines[cap_idx] if cap_idx is not None else ""
            notes = "\n".join(lines[(cap_idx + 1 if cap_idx is not None else i):i] + lines[j:j + 4])
            ctx = "\n".join(lines[max(0, (cap_idx or i) - 2):j + 4])
            rows = [lines[i]] + [lines[k] for k in range(i + 2, j)]
            first_in_results = bool(re.search(r"result", heading, re.I)) and tables_under_heading == 0
            tables_under_heading += 1
            out.append({"file": str(path), "line": i + 1, "caption": caption,
                        "label": "main-results" if first_in_results else "", "notes": notes, "rows": rows,
                        "stats_ok": "stats-ok:" in ctx, "fmt": "md"})
            i = j
        else:
            i += 1
    return out


def first_cell(row, fmt):
    if fmt == "md":
        cells = [c.strip() for c in row.strip().strip("|").split("|")]
    else:
        cells = [c.strip() for c in row.split("&")]
    return cells[0] if cells else "", cells


def check(t):
    issues = []
    where = f"{t['file']}:{t['line']}"
    defin = t["caption"] + " " + t["notes"]
    alltext = " ".join(t["rows"])
    for name, rx in MARKERS.items():
        if rx.search(alltext) and not rx.search(defin):
            if t["fmt"] == "md" and name == "pub":
                continue  # '*' is ambiguous with Markdown emphasis
            issues.append(("ERROR", "T1", where, f"provenance marker '{name}' used in rows but not defined in caption/notes"))
    is_main = bool(MAIN_RE.search(t["label"] + " " + t["caption"])) and not NOT_MAIN_RE.search(t["label"] + " " + t["caption"])
    in_incompat = False
    has_ours = False
    for r in t["rows"][1:] if t["rows"] else []:
        name, cells = first_cell(r, t["fmt"])
        if re.search(r"not directly comparable|different protocol", r, re.I):
            in_incompat = True
            continue
        if MARKERS["incompat"].search(r) or in_incompat:
            if BOLD_RE.search(" ".join(cells[1:])):
                issues.append(("ERROR", "T5", where, f"bold/underline in incompatible-protocol row: {name[:60]}"))
        if PLACEHOLDER_RE.search(r) and BOLD_RE.search(r) and t["fmt"] == "md":
            issues.append(("WARN", "T6", where, f"bold on a row with unmeasured values: {name[:60]}"))
        if not is_main or not name or re.fullmatch(r"\\multicolumn.*", name):
            continue
        if OURS_RE.search(name):
            has_ours = True
            continue
        if CONFIG_RE.search(re.sub(CITE_RE, "", name)):
            issues.append(("WARN", "T3", where, f"configuration-style label in main table: '{name[:60]}' "
                                                 "(use the established method name; move configurations to ablations)"))
        if not CITE_RE.search(name):
            issues.append(("WARN", "T2", where, f"baseline row without citation: '{name[:60]}'"))
    if is_main:
        if STATS_RE.search(alltext + " " + " ".join(t["rows"][:1])) and not t["stats_ok"]:
            issues.append(("WARN", "T4", where, "p-values/CIs/significance stars in a main-results table; move to text or "
                                                 "appendix, or justify with a 'stats-ok: <reason>' comment (paper_standards.md §5.3)"))
        if t["rows"] and not has_ours:
            issues.append(("WARN", "T7", where, "no row identified as the proposed method (Ours / proposed / \\oursrow)"))
    return is_main, issues


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    target = Path(sys.argv[1])
    files = [target] if target.is_file() else [p for p in target.rglob("*")
                                               if p.suffix in (".tex", ".md") and "_build" not in p.parts]
    tables = []
    for f in files:
        text = f.read_text(encoding="utf-8", errors="replace")
        tables += tex_tables(text, f) if f.suffix == ".tex" else md_tables(text, f)
    results, n_err = [], 0
    for t in tables:
        is_main, iss = check(t)
        n_err += sum(1 for i in iss if i[0] == "ERROR")
        results.append({"file": t["file"], "line": t["line"], "label": t["label"], "main_results": is_main,
                        "issues": [dict(zip(("severity", "rule", "where", "message"), i)) for i in iss]})
    if "--json" in sys.argv:
        print(json.dumps(results, indent=2))
    else:
        print(f"tables found: {len(tables)} (main-results: {sum(r['main_results'] for r in results)})")
        for r in results:
            tag = "MAIN" if r["main_results"] else "other"
            print(f"- [{tag}] {r['file']}:{r['line']} {r['label']}")
            for i in r["issues"]:
                print(f"    {i['severity']} {i['rule']}: {i['message']}")
        print(f"errors: {n_err}")
    sys.exit(1 if n_err else 0)


if __name__ == "__main__":
    main()
