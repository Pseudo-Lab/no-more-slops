#!/usr/bin/env python3
"""Compare the source paper's text with the compiled LaTeX PDF.

Usage:
    python compare_content.py <source_plain.txt> <compiled.pdf> [--out report.json]
                              [--min-added 80] [--refs-heading References]
                              [--visuals <project>/_conversion/visuals_manifest.json]

--visuals: text, numbers and supplied captions of visuals whose decision is
"include" are an allowed source. PDF text/numbers explained only by them are
reported under "from supplied visuals" instead of "added?". Excluded or
undecided assets are NOT allowed sources.

<source_plain.txt> is normally <project>/_conversion/source_plain.txt from
extract_source.py. If parts of the source were intentionally excluded (e.g. a
"not part of the paper" section), pass an edited copy with those parts removed
and record the exclusion in the conversion report.

Checks (all text normalised: NFKC, ligatures, unified minus/dashes; matching is
on lower-cased alphanumerics only, so hyphenation, spacing and line breaks do
not matter):
  1. NUMBERS    every numeric token in the source (count-aware) appears in the PDF;
                decimal/percent tokens in the PDF that are absent from the source
                are listed as possibly altered/added numbers.
  2. SENTENCES  every body sentence appears in the PDF. Non-exact sentences get a
                12-gram coverage score: >= 0.85 NEAR (usually math/footnote
                rendering; inspect), < 0.85 MISSING (must be resolved).
  3. TABLES     plain-text tables (pandoc grid/simple tables) are checked cell by
                cell, because PDF text extraction reads table columns out of order.
  4. REFERENCES entries after the references heading are checked separately
                (the bibliography style legitimately reformats them): quoted
                titles must appear verbatim (case-insensitive); coverage reported.
  5. ADDED      runs of PDF text (>= --min-added alnum chars) not found in the
                source. Expected: section numbers, "Figure 1:", reference
                formatting; anything else must be explained.
Exit status: 1 if any MISSING sentence, missing table cell, missing reference
title, missing number, unexplained decimal/% number only in the PDF, or ADDED
sentence (PDF sentence covered by neither the source nor an included visual
that contains novel words or numbers); else 0.
"""
import json
import re
import shutil
import subprocess
import sys
import unicodedata
from collections import Counter
from pathlib import Path

NUM_RE = re.compile(r"(?<![\w.])-?\d[\d,]*(?:\.\d+)?%?")
K = 12
RULE_LINE = re.compile(r"^\s*[-=+:|]{3,}(?:[\s+|:]+[-=:]{3,})*[\s+|]*$")
# tokens that are (part of) mathematics: TeX markup, Greek, math operators/arrows, ±, ×, ÷, ℓ
MATH_WORD = re.compile(r"[$\\_^={}Ͱ-Ͽ∀-⋿←-⇿±×÷ℓ]")

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass


def normalize(text):
    text = unicodedata.normalize("NFKC", text)
    for a, b in (("−", "-"), ("–", "-"), ("—", "-"), ("‐", "-"), ("‑", "-"),
                 ("­", ""), ("’", "'"), ("‘", "'"), ("“", '"'), ("”", '"'),
                 (" ", " "), (" ", " "), (" ", " ")):
        text = text.replace(a, b)
    return text.replace("\r\n", "\n")


def alnum(text):
    return "".join(ch.lower() for ch in text if ch.isalnum())


def alnum_map(text):
    chars, idx = [], []
    for i, ch in enumerate(text):
        if ch.isalnum():
            chars.append(ch.lower())
            idx.append(i)
    return "".join(chars), idx


def numbers(text):
    out = []
    for m in NUM_RE.finditer(text):
        tok = m.group(0).replace(",", "")
        if re.fullmatch(r"-?\d+(\.\d+)?%?", tok):
            out.append(tok)
    return out


def sentences(text):
    text = re.sub(r"[ \t]+", " ", text)
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z(\[\"'])|\n\s*\n|\n(?=[#*\-\d]+\s)", text)
    out = []
    for p in parts:
        p = " ".join(p.split())
        if len(alnum(p)) >= 25:
            out.append(p)
    return out


def split_blocks(text):
    return re.split(r"\n\s*\n", text)


def extract_tables(src):
    """Pull plain-text tables out of the source; return (text_without_tables, tables)."""
    keep, tables = [], []
    for block in split_blocks(src):
        lines = block.splitlines()
        if any(RULE_LINE.match(l) for l in lines) and len(lines) >= 2:
            cells = []
            for l in lines:
                if RULE_LINE.match(l):
                    continue
                cells += [c.strip() for c in re.split(r"\s{2,}|\|", l) if alnum(c)]
            tables.append({"text": " ".join(block.split())[:200], "cells": cells})
        else:
            keep.append(block)
    return "\n\n".join(keep), tables


def split_references(src, heading):
    """Return (body_text, reference_text). Reference section ends at the next heading-like line."""
    lines = src.splitlines()
    start = None
    for i, l in enumerate(lines):
        if re.fullmatch(r"\s*(?:\d+\.?\s+)?" + re.escape(heading) + r"\s*", l, re.I):
            start = i
            break
    if start is None:
        return src, ""
    end = len(lines)
    for j in range(start + 1, len(lines)):
        l = lines[j].strip()
        prev_blank = j == 0 or not lines[j - 1].strip()
        next_blank = j + 1 >= len(lines) or not lines[j + 1].strip()
        if l and prev_blank and next_blank and len(l) < 90 and not l.startswith("[") \
                and not re.match(r"^\d+\.\s", l) and not l.endswith((".", ",", ";")):
            end = j
            break
    body = "\n".join(lines[:start] + lines[end:])
    return body, "\n".join(lines[start + 1:end])


def pdf_text(pdf):
    if not shutil.which("pdftotext"):
        sys.exit("pdftotext not available: cannot extract compiled PDF text (comparison UNVERIFIED)")
    r = subprocess.run(["pdftotext", str(pdf), "-"], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    pages = r.stdout.split("\f")
    cleaned = []
    for pg in pages:  # drop a bare page number at the bottom of each page
        lines = pg.rstrip().splitlines()
        if lines and re.fullmatch(r"\s*\d{1,3}\s*", lines[-1]):
            lines = lines[:-1]
        cleaned.append("\n".join(lines))
    return "\n".join(cleaned)


def opt(name, default):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


def main():
    vals = {opt(o, None) for o in ("--out", "--min-added", "--refs-heading", "--visuals")}
    args = [a for a in sys.argv[1:] if not a.startswith("--") and a not in vals]
    if len(args) < 2:
        print(__doc__)
        sys.exit(2)
    out_path = opt("--out", None)
    min_added = int(opt("--min-added", "80"))
    refs_heading = opt("--refs-heading", "References")
    src = normalize(Path(args[0]).read_text(encoding="utf-8", errors="replace"))
    out = normalize(pdf_text(Path(args[1])))
    out_joined = re.sub(r"(\d)-\n(\d)", r"\1\2", out)
    out_norm, out_idx = alnum_map(out)
    grams = {out_norm[i:i + K] for i in range(max(0, len(out_norm) - K + 1))}

    # Text and numbers of supplied visuals that were INTENTIONALLY included
    # (decision.action == "include" in visuals_manifest.json): not "added" content.
    vis_text, vis_assets = "", []
    vpath = opt("--visuals", None)
    if vpath:
        man = json.loads(Path(vpath).read_text(encoding="utf-8"))
        for a in man.get("assets", []):
            d = a.get("decision") or {}
            if d.get("action") != "include":
                continue
            vis_assets.append(Path(a["path"]).name)
            parts = [" ".join(" ".join(r) for r in a.get("rows") or []), a.get("text") or ""]
            if d.get("caption_source") in ("sidecar", "asset_file", "user"):
                parts.append(d.get("caption_text") or "")
            vis_text += "\n" + normalize(" ".join(parts))
    vis_tokens = set(re.findall(r"[a-z0-9]+(?:\.[0-9]+)?", vis_text.lower()))
    placeholders = []
    if vpath:
        # "[Figure 2 here]" / "[Insert Table 1]" markers are replaced by the supplied visual
        placeholders = re.findall(r"\[(?:insert\s+|place\s+)?(?:figure|fig\.|table)\s*\d+[^\]\n]{0,60}\]", src, re.I)
        src = re.sub(r"\[(?:insert\s+|place\s+)?(?:figure|fig\.|table)\s*\d+[^\]\n]{0,60}\]", " ", src, flags=re.I)
    src_tokens = set(re.findall(r"[a-z0-9]+(?:\.[0-9]+)?", src.lower()))
    vis_norm = alnum(vis_text)
    vis_grams = {vis_norm[i:i + K] for i in range(max(0, len(vis_norm) - K + 1))}
    vis_nums = Counter(numbers(vis_text))

    def coverage(s_norm):
        windows = [s_norm[i:i + K] for i in range(max(1, len(s_norm) - K + 1))]
        return sum(1 for w in windows if w in grams) / len(windows)

    # 1. numbers (whole source)
    sn, on = Counter(numbers(src)), Counter(numbers(out_joined))
    missing_nums = sn - on
    missing_detail = []
    for tok, cnt in sorted(missing_nums.items()):
        ctx = [src[max(0, m.start() - 50):m.end() + 50].replace("\n", " ")
               for m in NUM_RE.finditer(src) if m.group(0).replace(",", "") == tok][:2]
        missing_detail.append({"number": tok, "missing_count": cnt, "source_context": ctx})
    extra_all = Counter({t: c for t, c in (on - sn).items() if ("." in t or "%" in t)})
    vis_extra = extra_all & vis_nums          # explained by intentionally included supplied visuals
    extra_nums = dict(extra_all - vis_extra)

    body, refs = split_references(src, refs_heading)
    body, tables = extract_tables(body)

    # 2. sentences
    exact, near, missing, math = 0, [], [], []
    for s in sentences(body):
        s_norm = alnum(s)
        if s_norm in out_norm:
            exact += 1
            continue
        cov = coverage(s_norm)
        if cov >= 0.85:
            near.append({"coverage": round(cov, 3), "sentence": s[:300]})
            continue
        words = s.split()
        mathy = [bool(MATH_WORD.search(w)) for w in words]
        if any(mathy):
            # PDF math glyphs often do not extract as text: verify the prose runs
            # between math tokens instead, and leave the math itself to manual review.
            runs, cur = [], []
            for w, m in zip(words, mathy):
                if m:
                    if cur:
                        runs.append(" ".join(cur))
                    cur = []
                else:
                    cur.append(w)
            if cur:
                runs.append(" ".join(cur))
            runs = [r for r in runs if len(alnum(r)) >= 6]
            lost = [r for r in runs if alnum(r) not in out_norm]
            if not lost:
                math.append({"coverage": round(cov, 3), "sentence": s[:300]})
                continue
            missing.append({"coverage": round(cov, 3), "sentence": s[:300], "prose_runs_not_found": lost})
            continue
        missing.append({"coverage": round(cov, 3), "sentence": s[:300]})

    # 3. tables
    table_report = []
    for t in tables:
        miss = [c for c in t["cells"] if alnum(c) not in out_norm]
        table_report.append({"table": t["text"][:120], "cells": len(t["cells"]), "missing_cells": miss})

    # 4. references
    ref_report = []
    entries = [e for e in re.split(r"\n\s*\n|\n(?=\s*\[\d+\]|\s*\d+\.\s)", refs) if alnum(e)]
    for e in entries:
        e1 = " ".join(e.split())
        titles = re.findall(r"\"([^\"]{8,})\"", e1)
        missing_titles = [t for t in titles if alnum(t.rstrip(".,")) not in out_norm]
        ref_report.append({"entry": e1[:200], "coverage": round(coverage(alnum(e1)), 3),
                           "missing_quoted_titles": missing_titles})

    # 5. added text
    src_norm = alnum(src)
    src_grams = {src_norm[i:i + K] for i in range(max(0, len(src_norm) - K + 1))}
    covered = [False] * len(out_norm)
    for i in range(max(0, len(out_norm) - K + 1)):
        if out_norm[i:i + K] in src_grams:
            for j in range(i, i + K):
                covered[j] = True
    added, from_visuals, i = [], [], 0
    while i < len(out_norm):
        if not covered[i]:
            j = i
            while j < len(out_norm) and not covered[j]:
                j += 1
            if j - i >= min_added:
                run_txt = " ".join(out[out_idx[i]:out_idx[j - 1] + 1].split())[:300]
                seg = out_norm[i:j]
                wins = [seg[k:k + K] for k in range(max(1, len(seg) - K + 1))]
                vcov = sum(1 for w in wins if w in vis_grams) / len(wins) if vis_grams else 0
                # tables/diagrams are often extracted column-wise: fall back to token membership
                rtoks = re.findall(r"[a-z0-9]+(?:\.[0-9]+)?", run_txt.lower())
                tcov = sum(1 for t in rtoks if t in vis_tokens or t in src_tokens) / len(rtoks) if rtoks else 0
                vis_share = sum(1 for t in rtoks if t in vis_tokens) / len(rtoks) if rtoks else 0
                (from_visuals if vis_grams and (vcov >= 0.6 or (tcov >= 0.9 and vis_share >= 0.5)) else added).append(run_txt)
            i = j
        else:
            i += 1

    # 6. reverse sentence check: every PDF sentence must be covered by the source
    #    (or by an intentionally included supplied visual). Catches added prose made
    #    of common phrases that the run-based check above splits into short pieces.
    allowed = src_grams | vis_grams
    body_pdf = re.split(r"\n\s*References\s*\n", out)[0]
    added_sentences = []
    for s in sentences(body_pdf):
        s_norm = alnum(s)
        if len(s_norm) < 40:
            continue
        wins = [s_norm[k:k + K] for k in range(max(1, len(s_norm) - K + 1))]
        cov = sum(1 for w in wins if w in allowed) / len(wins)
        if cov < 0.8:
            stoks = [t for t in re.findall(r"[a-z]{4,}", s.lower())]
            novel = sorted({t for t in stoks if t not in src_tokens and t not in vis_tokens})
            novel_nums = [n for n in numbers(s) if n not in sn and n not in vis_nums]
            if novel or novel_nums:   # low coverage with neither = math glyphs that did not extract
                added_sentences.append({"coverage": round(cov, 3), "novel_words": novel[:12], "sentence": s[:300]})

    total = exact + len(near) + len(missing) + len(math)
    n_missing_cells = sum(len(t["missing_cells"]) for t in table_report)
    n_missing_titles = sum(len(r["missing_quoted_titles"]) for r in ref_report)
    report = {
        "body_sentences": total, "exact": exact, "near": len(near), "missing": len(missing),
        "sentence_exact_rate": round(exact / total, 4) if total else None,
        "source_numeric_tokens": sum(sn.values()),
        "numbers_missing_in_pdf": missing_detail,
        "decimal_or_percent_numbers_only_in_pdf": extra_nums,
        "tables": table_report,
        "references": ref_report,
        "math_sentences_manual_check": math,
        "near_sentences": near, "missing_sentences": missing,
        "possibly_added_text": added,
        "supplied_visuals_included": vis_assets,
        "numbers_from_supplied_visuals": dict(vis_extra),
        "text_from_supplied_visuals": from_visuals,
        "placeholders_replaced_by_visuals": placeholders,
        "added_sentences": added_sentences,
    }
    if out_path:
        Path(out_path).write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"body sentences: {total} | exact {exact} | near {len(near)} | math (manual check) {len(math)} "
          f"| MISSING {len(missing)}")
    print(f"numbers: {sum(sn.values())} source tokens | missing in PDF: {sum(missing_nums.values())}")
    for d in missing_detail[:30]:
        print(f"   missing number {d['number']} x{d['missing_count']}: {d['source_context'][:1]}")
    if extra_nums:
        print(f"decimal/% numbers only in PDF (check for alteration): {dict(list(extra_nums.items())[:30])}")
    print(f"tables: {len(table_report)} | cells missing: {n_missing_cells}")
    for t in table_report:
        if t["missing_cells"]:
            print(f"   table '{t['table'][:60]}': missing cells {t['missing_cells'][:20]}")
    print(f"references: {len(ref_report)} entries | quoted titles missing: {n_missing_titles}")
    for r in ref_report:
        flag = "TITLE MISSING " if r["missing_quoted_titles"] else ""
        print(f"   {flag}cov={r['coverage']}: {r['entry'][:110]}")
    for m in missing[:30]:
        print(f"   MISSING ({m['coverage']}): {m['sentence'][:160]}")
    for m in math[:30]:
        print(f"   math ({m['coverage']}): {m['sentence'][:140]}")
    for n in near[:15]:
        print(f"   near ({n['coverage']}): {n['sentence'][:120]}")
    for a in added[:20]:
        print(f"   added?: {a[:160]}")
    if vpath:
        print(f"supplied visuals included: {len(vis_assets)} | numbers explained by them: {sum(vis_extra.values())} "
              f"| text runs explained by them: {len(from_visuals)} | placeholders replaced: {placeholders}")
    if out_path:
        print(f"report: {out_path}")
    print(f"added sentences (not in source or included visuals): {len(added_sentences)}")
    for a in added_sentences[:20]:
        print(f"   ADDED ({a['coverage']}, novel words {a['novel_words']}): {a['sentence'][:160]}")
    bad = missing or missing_detail or n_missing_cells or n_missing_titles or extra_nums or added_sentences
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
