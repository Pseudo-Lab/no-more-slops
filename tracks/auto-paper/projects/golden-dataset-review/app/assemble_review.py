"""Assemble toego's review.json for one round and build its before/after HTML.

Inputs in reviews/<round>/:
    extract/            md_extract.py output of the manuscript before the round
    sent-*.json         toego:sentence-auditor results (lists of paragraph edits)
    sections.json       per-section flow, verdict and structure notes from toego:paragraph-auditor,
                        plus global_flow, structure, author_checks and fact_checks
    abstract-after.txt  English abstract after the round (optional)
Writes reviews/<round>/review.json and reviews/<round>/퇴고_비교.html via toego's build_html.py.

Usage:
    uv run assemble_review.py round1
"""
import json
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOEGO = Path.home() / ".claude/plugins/cache/toego/toego/0.1.0/skills/revise/scripts/build_html.py"

RULES = {
    "tense": [["서론·본론의 선행연구 보고", "과거", "보고하였다, 보였다"],
              ["정의·일반 사실·표 설명", "현재", "표 1은 … 비교한다"],
              ["이 리뷰의 주장·제안", "현재", "제안한다, 본다"]],
    "structure": [["서론", "깔때기형, 문단 두괄식", "맥락 → 문제 → 공백 → 질문"],
                  ["본론 소절", "두괄식", "주장 → 문헌 근거 → 함의"],
                  ["논의·결론", "양괄식", "요약 → 근거 → 범위와 한계"]],
    "flags": [["사실오류", "근거 기록·원문과 다른 서술"], ["근거부족", "인용이 뒷받침하지 않는 주장"],
              ["과잉일반화", "한 연구·한 데이터셋 결과를 일반 성질로 서술"], ["논리연결", "문장 간 인과·대조 오류"],
              ["AI상투", "내용 없는 주제문·수사"], ["시제", "시제 규칙 위반"], ["용어통일", "같은 개념의 다른 표기"],
              ["문법", "주술 호응·조사"], ["구조", "문단·절 배치"]],
}


def main():
    rnd = ROOT / "reviews" / sys.argv[1]
    src = {p["id"]: p for p in json.loads((rnd / "extract" / "paragraphs.json").read_text(encoding="utf-8"))}
    meta = json.loads((rnd / "sections.json").read_text(encoding="utf-8"))
    paras = []
    for f in sorted(rnd.glob("sent-*.json")):
        data = json.loads(f.read_text(encoding="utf-8"))
        paras += data if isinstance(data, list) else data.get("paras", [])
    by_sec = {}
    abstract_edits = []
    for q in paras:
        if q["id"].startswith("abs-en"):
            abstract_edits += q.get("edits", [])
            continue
        sec = src.get(q["id"], {}).get("section") or q["id"].split("-P")[0]
        by_sec.setdefault(sec, []).append(q)
    sections = []
    for s in meta["sections"]:
        s = dict(s)
        s["paras"] = by_sec.pop(s["id"], [])
        sections.append(s)
    for sec, qs in by_sec.items():  # tables and anything not mapped to a section
        sections.append({"id": sec, "title": sec, "pattern": "-", "flow_before": "-", "flow_after": "-",
                         "verdict": "-", "paras": qs})
    en_before = next((p["text"] for p in src.values() if p["section"] == "abs-en"), "")
    after_path = rnd / "abstract-after.txt"
    review = {
        "meta": {"title": meta["title"], "source": "manuscript/source.md", "date": date.today().isoformat(),
                 "reviewer_comment": meta["reviewer_comment"], "evidence_sources": meta["evidence_sources"]},
        "rules": RULES,
        "structure": meta["structure"],
        "sections": sections,
        "abstract": {"before": en_before,
                     "after": after_path.read_text(encoding="utf-8").strip() if after_path.exists() else en_before,
                     "edits": abstract_edits, "note": meta.get("abstract_note", "")},
        "captions": meta.get("captions", []), "references": meta.get("references", []),
        "global_flow": meta["global_flow"], "author_checks": meta["author_checks"],
        "fact_checks": meta["fact_checks"],
    }
    out = rnd / "review.json"
    out.write_text(json.dumps(review, ensure_ascii=False, indent=1), encoding="utf-8")
    subprocess.run(["uv", "run", "--frozen", "--quiet", "--no-project", "python", str(TOEGO),
                    str(out), str(rnd / "extract"), str(rnd / "퇴고_비교.html")], check=True)


if __name__ == "__main__":
    main()
