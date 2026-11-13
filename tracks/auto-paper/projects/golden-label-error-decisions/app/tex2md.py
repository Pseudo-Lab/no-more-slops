"""Write outputs/week-04/paper.md, a GitHub-readable copy of paper.tex, so the two never drift apart.

build_paper.sh runs this after compiling: section, table and figure numbers come from paper.aux and
citations from references.bib, formatted like the ACL natbib style. Only the LaTeX this paper uses is
handled (sections, paragraphs, citations, inline math, booktabs tables, figures, one enumerate).
"""
import re
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "outputs/week-04"
tex = (OUT / "paper.tex").read_text()
aux = (OUT / "paper.aux").read_text()
labels = {k: v for k, v in re.findall(r"\\newlabel\{([^}]+)\}\{\{([^}]*)\}", aux)}

# ---------- bibliography ----------
bib = {}
for key, body in re.findall(r"@\w+\{([^,]+),(.*?)\n\}", (OUT / "references.bib").read_text(), re.S):
    f = {k.lower(): v.strip() for k, v in re.findall(r"(\w+)\s*=\s*\{((?:[^{}]|\{[^{}]*\})*)\}", body)}
    bib[key] = f


def strip_braces(s):
    return re.sub(r"[{}]", "", s).replace("\\'e", "é").replace("\\'", "").replace("--", "–")


def authors(f):
    names = [a.strip() for a in f["author"].split(" and ")]
    last = [strip_braces(a.split(",")[0]) for a in names]
    if "others" in names or len(names) > 2:
        return f"{last[0]} et al."
    return " and ".join(last)


def cite(keys, paren):
    parts = []
    for k in [k.strip() for k in keys.split(",")]:
        f = bib[k]
        parts.append(f"{authors(f)}, {f['year']}" if paren else f"{authors(f)} ({f['year']})")
    return "(" + "; ".join(parts) + ")" if paren else "; ".join(parts)


def reference(f):
    names = [a.strip() for a in f["author"].split(" and ")]
    full = []
    for a in names:
        if a == "others":
            continue
        last, _, first = a.partition(",")
        full.append(strip_braces(f"{first.strip()} {last.strip()}".strip()))
    if "others" in names:
        who = ", ".join(full) + ", and others"
    elif len(full) > 2:
        who = ", ".join(full[:-1]) + ", and " + full[-1]
    else:
        who = " and ".join(full)
    venue = f.get("booktitle") or f.get("journal") or f.get("howpublished") or f.get("note", "")
    pages = f", pages {strip_braces(f['pages'])}" if "pages" in f else ""
    doi = f" doi:{f['doi']}" if "doi" in f else ""
    note = ""
    if "note" in f and venue != f["note"]:
        note = " " + strip_braces(re.sub(r"\\url\{([^}]*)\}", r"\1", f["note"])) + "."
    title = strip_braces(f["title"])
    title += "" if title.endswith(("?", "!", ".")) else "."
    return f"{who}. {f['year']}. {title} *{strip_braces(venue)}*{pages}.{note}{doi}".replace("..", ".")


# ---------- inline conversion ----------
MATH = [(r"\delta", "δ"), (r"\tau", "τ"), (r"\rho", "ρ"), (r"\sim", "~"), (r"\ge", "≥"), (r"\le", "≤"),
        (r"\,", " "), (r"\mathrm", ""), (r"\sqrt", "√"), (r"\mathbb", ""), ("-", "−")]


def math(m):
    s = m.group(1)
    for a, b in MATH:
        s = s.replace(a, b)
    s = re.sub(r"_\{([^}]*)\}", r"_\1", s)
    s = re.sub(r"\^\{([^}]*)\}", r"^\1", s)
    return s.replace("{", "").replace("}", "").replace("\\", "")


def inline(s):
    s = re.sub(r"\\texorpdfstring\{((?:[^{}]|\{[^{}]*\})*)\}\{[^}]*\}", r"\1", s)
    s = re.sub(r"\\citep\{([^}]*)\}", lambda m: cite(m.group(1), True), s)
    s = re.sub(r"\\citet\{([^}]*)\}", lambda m: cite(m.group(1), False), s)
    s = re.sub(r"\\ref\{([^}]*)\}", lambda m: labels[m.group(1)], s)
    s = re.sub(r"\\label\{[^}]*\}", "", s)
    s = s.replace(r"\pp{}", "%p").replace(r"\%", "%").replace(r"\_", "_").replace(r"\&", "&")
    s = re.sub(r"\$([^$]*)\$", math, s)
    s = re.sub(r"\\textit\{([^}]*)\}", r"*\1*", s)
    s = re.sub(r"\\textbf\{([^}]*)\}", r"**\1**", s)
    s = re.sub(r"\\texttt\{([^}]*)\}", r"`\1`", s)
    s = s.replace("``", "\u201c").replace("''", "\u201d").replace("---", "—").replace("--", "–")
    s = s.replace("~", " ").replace("\\\\", " ")
    return re.sub(r"\s+", " ", s).strip()


# ---------- tables ----------
def split_row(r):
    return re.split(r"(?<!\\)&", r)


def tabular(body):
    body = re.sub(r"(?<!\\)%.*", "", body)
    body = re.sub(r"\\begin\{tabular\}\{.*?\}\s*\n", "", body, count=1).replace(r"\end{tabular}", "")
    body = re.sub(r"\\(toprule|bottomrule)", "", body)
    blocks = body.split(r"\midrule")
    rows = []
    for bi, blk in enumerate(blocks):
        for r in re.split(r"\\\\", blk):
            r = re.sub(r"\\cmidrule(\([^)]*\))?\{[^}]*\}", "", r).strip()
            if not r:
                continue
            cells = []
            for c in split_row(r):
                m = re.match(r"\s*\\multicolumn\{(\d+)\}\{(?:[^{}]|\{[^{}]*\})*\}\{(.*)\}\s*$", c, re.S)
                cells += [inline(m.group(2))] * int(m.group(1)) if m else [inline(c)]
            rows.append((bi, cells))
    ncol = max(len(c) for _, c in rows)
    head = [c for b, c in rows if b == 0]
    hdr = [" ".join(dict.fromkeys(h[j] for h in head if j < len(h) and h[j])) for j in range(ncol)]
    out = ["| " + " | ".join(hdr) + " |", "|" + " --- |" * ncol]
    for b, c in rows:
        if b == 0:
            continue
        if len(set(c)) == 1 and len(c) == ncol and ncol > 1:  # a row spanning all columns: a group label
            c = [c[0]] + [""] * (ncol - 1)
        out.append("| " + " | ".join(c + [""] * (ncol - len(c))) + " |")
    return "\n".join(out)


def float_env(env, body):
    lab = re.search(r"\\label\{([^}]*)\}", body)
    num = labels[lab.group(1)] if lab else ""
    cap = re.search(r"\\caption\{(.*)\}\s*\\label", body, re.S)
    cap = inline(cap.group(1)) if cap else ""
    if env.startswith("figure"):
        img = re.search(r"\\includegraphics\[[^]]*\]\{([^}]*)\}", body).group(1).replace(".pdf", ".png")
        return f"![그림 {num}]({img})\n\n*그림 {num}: {cap}*"
    inp = re.search(r"\\input\{([^}]*)\}", body)
    tab = (OUT / (inp.group(1) + ".tex")).read_text() if inp else re.search(r"\\begin\{tabular\}.*?\\end\{tabular\}", body, re.S).group(0)
    return f"*표 {num}: {cap}*\n\n{tabular(tab)}"


# ---------- document ----------
doc = tex[tex.index(r"\begin{document}") + len(r"\begin{document}"): tex.index(r"\end{document}")]
doc = re.sub(r"(?m)^%.*\n?", "", doc)
doc = re.sub(r"(?<!\\)%.*", "", doc)
title = inline(re.search(r"\\title\{(.*?)\}\n", tex, re.S).group(1))
out = ["---", "type: Original Research (ACL format)", f'title: "{title}"', "authors: 심사용 익명 원고", "---", "",
       "> 이 파일은 [paper.pdf](paper.pdf)의 원본 [paper.tex](paper.tex)에서 `app/tex2md.py`가 자동으로 만든 사본이다. "
       "GitHub에서 바로 읽기 위한 것이며, 문장, 표, 그림 번호는 PDF와 같다.", ""]
abstracts = re.findall(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", doc, re.S)
out += ["## 초록", "", inline(abstracts[0]), "", "## Abstract", "", inline(abstracts[1]), ""]
doc = doc[doc.index(r"\end{abstract}}") + len(r"\end{abstract}}"):]

sec = sub = 0
appendix = False
pos = 0
token = re.compile(r"\\(section\*?|subsection|paragraph)\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*)\}"
                   r"|\\begin\{(table\*?|figure\*?)\}(.*?)\\end\{\3\}"
                   r"|\\begin\{enumerate\}\[([^\]]*)\](.*?)\\end\{enumerate\}"
                   r"|\\appendix|\\bibliography\{[^}]*\}|\\maketitle", re.S)


def paragraphs(text):
    for p in re.split(r"\n\s*\n", text):
        p = inline(p)
        if p:
            out.extend([p, ""])


pending_par = None
for m in token.finditer(doc):
    paragraphs(doc[pos:m.start()]) if pending_par is None else None
    if pending_par is not None:
        chunk = doc[pos:m.start()].strip().split("\n\n")
        out.extend([f"**{pending_par}** " + inline(chunk[0]), ""])
        paragraphs("\n\n".join(chunk[1:]))
        pending_par = None
    pos = m.end()
    t = m.group(0)
    if m.group(1) == "section":
        sec += 1; sub = 0
        num = chr(64 + sec) if appendix else str(sec)
        out += [f"## {'부록 ' + num + '.' if appendix else num + '.'} {inline(m.group(2))}", ""]
    elif m.group(1) == "section*":
        out += [f"## {inline(m.group(2))}", ""]
    elif m.group(1) == "subsection":
        sub += 1
        out += [f"### {sec}.{sub} {inline(m.group(2))}", ""]
    elif m.group(1) == "paragraph":
        pending_par = inline(m.group(2))
    elif m.group(3):
        out += [float_env(m.group(3), m.group(4)), ""]
    elif m.group(5) is not None:
        lab = re.search(r"label=(.*?)\\arabic\*(.)", m.group(5))
        items = [i for i in re.split(r"\\item\s*", m.group(6)) if i.strip()]
        for i, it in enumerate(items, 1):
            prefix = re.sub(r"\\textbf\{", "", lab.group(1)) + str(i) + lab.group(2) if lab else f"{i}."
            out.append(f"- **{prefix}** {inline(it)}")
        out.append("")
    elif t == r"\appendix":
        appendix, sec = True, 0
    elif t.startswith(r"\bibliography"):
        cited = sorted({k.strip() for ks in re.findall(r"\\cite[pt]\{([^}]*)\}", tex) for k in ks.split(",")},
                       key=lambda k: (authors(bib[k]).lower(), bib[k]["year"]))
        out += ["## 참고문헌", ""] + [f"- {reference(bib[k])}" for k in cited] + [""]
if pending_par is not None:
    out.extend([f"**{pending_par}** " + inline(doc[pos:].strip()), ""])
else:
    paragraphs(doc[pos:])
(OUT / "paper.md").write_text("\n".join(out).rstrip() + "\n")
print("wrote", OUT / "paper.md")
