"""Manuscript support: per-chapter evidence packs, citation check and reference list.

packs:  write manuscript/packs/<chapter>.md with code counts, claims (with full-text checks)
        and representative papers for each body chapter
refs:   collect [@key] citations from manuscript/*.md, report keys that are not included
        papers, and write manuscript/99-references.md
render: write manuscript/build/paper.md with numbered citations and the reference list

The chapter layout is defined in docs/outline.md.

Usage:
  uv run manuscript.py packs
  uv run manuscript.py refs
  uv run manuscript.py render
"""

import argparse
import csv
import json
import re
from collections import Counter, defaultdict

from common import DATA, PROJECT
from extract import included

MS = PROJECT / "manuscript"
PACKS = MS / "packs"
CITE = re.compile(r"\[(@[^\[\]]+)\]")
CHAPTERS = {
    "03-overview": {"questions": [], "fields": ["contribution", "judge_format", "judge_setup", "domain"]},
    "04-design": {"questions": ["Q-FORMAT", "Q-MULTI"], "fields": ["judge_format", "judge_setup"]},
    "05-reliability": {"questions": ["Q-SCALE", "Q-SELF", "Q-HARD"], "fields": ["biases"]},
    "06-improvement": {"questions": ["Q-COT", "Q-REF", "Q-FT", "Q-DEBIAS"], "fields": ["mitigation"]},
    "07-applications": {"questions": ["Q-EXPERT"], "fields": ["domain"]},
    "08-security": {"questions": ["Q-ATTACK", "Q-DEFENSE"], "fields": []},
}


def load():
    papers = {r["key"]: r for r in included()}
    ext = {}
    for line in (DATA / "extraction.jsonl").open(encoding="utf-8"):
        rec = json.loads(line)
        if rec["key"] in papers:
            ext[rec["key"]] = rec
    # Recoded biases/mitigation from the claim-extraction round replace the first-pass codes.
    for line in (DATA / "synthesis" / "codes.jsonl").open(encoding="utf-8"):
        rec = json.loads(line)
        if rec["key"] in ext:
            ext[rec["key"]]["codes"].update(biases=rec["biases"], mitigation=rec["mitigation"])
    with (DATA / "synthesis" / "claims.csv").open(encoding="utf-8") as f:
        claims = [c for c in csv.DictReader(f) if c["key"] in papers]
    # Verification results line up with their batch inputs; key by claim text so two claims of one
    # paper on the same question keep their own checks.
    verified = {}
    vdir = DATA / "synthesis" / "verify"
    for batch in sorted((vdir / "batches").glob("*.jsonl")):
        result = vdir / "results" / batch.name
        if result.exists():
            for a, b in zip(batch.open(encoding="utf-8"), result.open(encoding="utf-8")):
                a, b = json.loads(a), json.loads(b)
                b["moderators"] = "; ".join(b.get("moderators") or [])
                verified[a["key"], a["question"], a["claim"]] = b
    return papers, ext, claims, verified


def cited(r):
    return int(r["cited_by"] or 0)


def paper_line(key, papers, ext):
    r, p = papers[key], ext[key]["pmdrl"]
    return (f"- [@{key}] {p['who']} — {r['title']} (인용 {cited(r)})\n"
            f"  - 문제: {p['problem']}\n  - 방법: {p['method']}\n  - 결과: {p['result']}\n")


def counts_table(field, ext):
    c = Counter(v for e in ext.values() for v in e["codes"].get(field) or [])
    rows = "\n".join(f"| {k} | {n} |" for k, n in c.most_common())
    return f"### {field} (논문 수, 중복 포함)\n\n| 값 | 편수 |\n| --- | --- |\n{rows}\n"


def claims_section(q, claims, papers, ext, verified):
    rows = [c for c in claims if c["question"] == q]
    tally = Counter((c["basis"], c["direction"]) for c in rows)
    out = [f"### {q} 주장 {len(rows)}개\n",
           "| 근거 | 지지 | 반박 | 조건부 | 효과 없음 |", "| --- | --- | --- | --- | --- |"]
    for basis in ("evaluation", "own_method"):
        out.append(f"| {basis} | " + " | ".join(str(tally[basis, d]) for d in
                                                 ("support", "refute", "conditional", "null")) + " |")
    out.append("")
    for c in sorted(rows, key=lambda c: (c["basis"], c["direction"], -cited(papers[c["key"]]))):
        v = verified.get((c["key"], q, c["claim"]))
        line = (f"- [{c['basis']}/{c['direction']}] [@{c['key']}] {ext[c['key']]['pmdrl']['who']}: {c['claim']}"
                + (f" (조건: {c['condition']})" if c["condition"] else "")
                + (f" (수치: {c['evidence']})" if c["evidence"] else ""))
        if v:
            line += (f"\n  - **본문 확인** {v['check']}, 본문 기준 방향 {v['direction']}. 조건: {v['moderators']}. "
                     f"근거: {v['evidence']}. {v['note']}")
        out.append(line)
    return "\n".join(out) + "\n"


def representatives(field, ext, papers, per=4):
    by = defaultdict(list)
    for k, e in ext.items():
        for v in e["codes"].get(field) or []:
            by[v].append(k)
    out = [f"### {field}별 대표 논문 (인용 상위 {per}편)\n"]
    for v, keys in sorted(by.items(), key=lambda x: -len(x[1])):
        out.append(f"#### {v} ({len(keys)}편)\n")
        out += [paper_line(k, papers, ext) for k in sorted(keys, key=lambda k: -cited(papers[k]))[:per]]
    return "\n".join(out)


def packs(args):
    papers, ext, claims, verified = load()
    PACKS.mkdir(parents=True, exist_ok=True)
    for name, spec in CHAPTERS.items():
        parts = [f"# 근거 묶음: {name}\n", f"포함 논문 {len(ext)}편 기준. 인용 키는 `[@키]` 그대로 쓴다.\n"]
        parts += [counts_table(f, ext) for f in spec["fields"]]
        parts += [claims_section(q, claims, papers, ext, verified) for q in spec["questions"]]
        if name == "03-overview":
            years = Counter(papers[k]["year"] for k in ext)
            parts.append("### 연도\n\n" + "\n".join(f"- {y or '미상'}: {n}" for y, n in sorted(years.items())))
            venues = Counter("arXiv" if (re.search(r"arxiv", papers[k]["venue"], re.I)
                                         or not papers[k]["venue"] and papers[k]["arxiv"])
                             else "저장소(Zenodo·OSF·SSRN·medRxiv 등)" if re.search(r"Zenodo|OSF|SSRN|Open Science|preprint|rxiv|Research Square|Figshare",
                                                                     papers[k]["venue"], re.I)
                             else "학회·저널·기타" for k in ext)
            parts.append("### 출처 유형\n\n" + "\n".join(f"- {v}: {n}" for v, n in venues.most_common()))
            models = Counter(m for e in ext.values() for m in e["codes"].get("judge_models") or [])
            parts.append("### 판정 모델 (상위 25)\n\n" + "\n".join(f"- {m}: {n}" for m, n in models.most_common(25)))
            metrics = Counter(m for e in ext.values() for m in e["codes"]["human_comparison"].get("metric") or [])
            human = sum(bool(e["codes"]["human_comparison"].get("done")) for e in ext.values())
            parts.append(f"### 사람 판정과 비교\n\n- 비교한 논문: {human}/{len(ext)}\n"
                         + "\n".join(f"- {m}: {n}" for m, n in metrics.most_common(12)))
            langs = sum(1 for e in ext.values() if e["codes"]["language"] and e["codes"]["language"] != ["en"])
            parts.append(f"### 언어\n\n- 영어 외 언어를 다룬 논문: {langs}")
            parts.append("### 인용 상위 30편\n\n" + "".join(
                paper_line(k, papers, ext) for k in sorted(ext, key=lambda k: -cited(papers[k]))[:30]))
        if name == "04-design":
            cross = Counter((f, s) for e in ext.values() for f in e["codes"]["judge_format"]
                            for s in e["codes"]["judge_setup"])
            setups = sorted({s for _, s in cross})
            parts.append("### 판정 형식 × 구성 (논문 수)\n\n| 형식 | " + " | ".join(setups) + " |\n| --- |"
                         + " --- |" * len(setups) + "\n" + "\n".join(
                f"| {f} | " + " | ".join(str(cross[f, s]) for s in setups) + " |"
                for f in sorted({f for f, _ in cross})))
            parts.append(representatives("judge_setup", ext, papers))
        if name == "05-reliability":
            parts.append(representatives("biases", ext, papers, per=3))
            bench = [k for k, e in ext.items() if "benchmark" in e["codes"]["contribution"]]
            parts.append(f"### 판정 벤치마크·메타평가 ({len(bench)}편 중 인용 상위 25)\n\n" + "".join(
                paper_line(k, papers, ext) for k in sorted(bench, key=lambda k: -cited(papers[k]))[:25]))
        if name == "06-improvement":
            parts.append(representatives("mitigation", ext, papers, per=3))
        if name == "07-applications":
            done = Counter(d for e in ext.values() if e["codes"]["human_comparison"].get("done")
                           for d in e["codes"]["domain"])
            total = Counter(d for e in ext.values() for d in e["codes"]["domain"])
            parts.append("### 분야별 사람 비교 비율\n\n| 분야 | 편수 | 사람 비교 | 비율 |\n| --- | --- | --- | --- |\n"
                         + "\n".join(f"| {d} | {n} | {done[d]} | {done[d] / n:.0%} |" for d, n in total.most_common()))
            parts.append(representatives("domain", ext, papers, per=3))
        if name == "08-security":
            sec = [k for k, e in ext.items() if "security" in e["codes"]["contribution"]
                   or "adversarial" in (e["codes"].get("biases") or [])]
            parts.append(f"### 보안 관련 논문 ({len(sec)}편, 인용순)\n\n" + "".join(
                paper_line(k, papers, ext) for k in sorted(sec, key=lambda k: -cited(papers[k]))))
        (PACKS / f"{name}.md").write_text("\n".join(parts) + "\n", encoding="utf-8")
        print(f"{name}: {sum(len(p) for p in parts):,} chars")


def citations():
    keys = []
    for path in sorted(MS.glob("[0-9][0-9]-*.md")):
        if path.name.startswith("99-"):
            continue
        for group in CITE.findall(path.read_text(encoding="utf-8")):
            keys += [k.strip().lstrip("@") for k in group.split(";")]
    return keys


def reference(r):
    authors = [a.strip() for a in r["authors"].split(";") if a.strip()]
    names = ", ".join(authors[:3]) + (" 외" if len(authors) > 3 else "")
    link = f"arXiv:{r['arxiv']}" if r["arxiv"] else (f"doi:{r['doi']}" if r["doi"] else "")
    return ". ".join(x for x in (f"{names or '저자 미상'} ({r['year'] or 'n.d.'})", r["title"], r["venue"], link) if x)


def refs(args):
    papers = {r["key"]: r for r in included()}
    keys = citations()
    unknown = sorted(set(keys) - set(papers))
    order = list(dict.fromkeys(k for k in keys if k in papers))
    lines = ["# 참고문헌\n"] + [f"{i}. {reference(papers[k])}" for i, k in enumerate(order, 1)]
    (MS / "99-references.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"citations {len(keys)}, unique papers {len(order)}, unknown keys {len(unknown)}")
    for k in unknown:
        print(f"  UNKNOWN {k}")
    return order, unknown


def render(args):
    order, unknown = refs(args)
    number = {k: i for i, k in enumerate(order, 1)}

    def repl(m):
        ks = [k.strip().lstrip("@") for k in m[1].split(";")]
        return "[" + ", ".join(str(number[k]) if k in number else f"?{k}" for k in ks) + "]"

    body = []
    for path in sorted(MS.glob("[0-9][0-9]-*.md")):
        body.append(CITE.sub(repl, path.read_text(encoding="utf-8")) if not path.name.startswith("99-")
                    else path.read_text(encoding="utf-8"))
    (MS / "build").mkdir(exist_ok=True)
    (MS / "build" / "paper.md").write_text("\n\n".join(body), encoding="utf-8")
    print(f"rendered {len(body)} files -> manuscript/build/paper.md")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)
    for name in ("packs", "refs", "render"):
        sub.add_parser(name)
    args = parser.parse_args()
    {"packs": packs, "refs": refs, "render": render}[args.cmd](args)


if __name__ == "__main__":
    main()
