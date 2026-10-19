"""Data extraction (PMDRL summary + taxonomy codes) for included papers.

prepare: split included papers without results into data/extraction/batches/<round>-NN.jsonl
collect: validate data/extraction/results/*.jsonl, add `who` from candidates.csv,
         and write data/extraction.jsonl

Fields are defined in docs/extraction.md.

Usage:
  uv run extract.py prepare --round e1 --size 70
  uv run extract.py collect
"""

import argparse
import json
from collections import Counter

from common import DATA
from screen import candidates, results as screening

EXTRACT = DATA / "extraction"
BATCHES, RESULTS = EXTRACT / "batches", EXTRACT / "results"
PMDRL = ("problem", "method", "data", "result", "limitation", "gap")
REQUIRED = ("problem", "method", "data", "result")
CODES = {
    "contribution": {"method", "analysis", "training", "benchmark", "application", "security", "survey"},
    "judge_format": {"pointwise", "pairwise", "listwise", "binary", "rubric", "reference", "critique"},
    "judge_setup": {"single", "ensemble", "debate", "reasoning", "agent", "finetuned"},
    "domain": {"general", "code", "math", "medical", "legal", "education", "science", "finance", "ir_rag",
               "dialogue", "summarization", "translation", "safety", "agent", "multimodal", "creative", "other"},
    "biases": {"position", "verbosity", "self_preference", "authority", "sycophancy", "inconsistency",
               "prompt_sensitivity", "leakage", "adversarial", "other"},
    "mitigation": {"swap", "calibration", "ensemble", "fine_tuning", "rubric", "cot", "reference", "other"},
}


def included():
    done = screening()
    return [r for r in candidates() if done.get(r["key"], {}).get("decision") == "include"]


def results():
    out = {}
    for path in sorted(RESULTS.glob("*.jsonl")):
        for line in path.open(encoding="utf-8"):
            if line.strip():
                rec = json.loads(line)
                rec["batch"] = path.stem
                out[rec["key"]] = rec
    return out


def who(r):
    authors = [a.strip() for a in r["authors"].split(";") if a.strip()]
    first = (authors[0] + (" 외" if len(authors) > 1 else "")) if authors else "저자 미상"
    return ", ".join(x for x in (first, r["year"], r["venue"]) if x)


def problems(rec):
    """Return a list of schema violations for one result record."""
    out = []
    p, c = rec.get("pmdrl") or {}, rec.get("codes") or {}
    out += [f"pmdrl.{k} missing" for k in PMDRL if k not in p]
    out += [f"pmdrl.{k} empty" for k in REQUIRED if not p.get(k)]
    for field, allowed in CODES.items():
        values = c.get(field)
        if not isinstance(values, list):
            out.append(f"codes.{field} not a list")
        elif set(values) - allowed:
            out.append(f"codes.{field} unknown {sorted(set(values) - allowed)}")
    if not isinstance(c.get("judge_models"), list):
        out.append("codes.judge_models not a list")
    if not isinstance(c.get("language"), list):
        out.append("codes.language not a list")
    if not isinstance(c.get("human_comparison"), dict) or "done" not in c["human_comparison"]:
        out.append("codes.human_comparison malformed")
    return out


def prepare(args):
    done = results()
    pending = {p.stem for p in BATCHES.glob("*.jsonl")} - {p.stem for p in RESULTS.glob("*.jsonl")}
    queued = {json.loads(line)["key"] for name in pending for line in (BATCHES / f"{name}.jsonl").open()}
    rows = [r for r in included() if r["key"] not in done and r["key"] not in queued]
    BATCHES.mkdir(parents=True, exist_ok=True)
    for n, i in enumerate(range(0, len(rows), args.size), 1):
        with (BATCHES / f"{args.round}-{n:02d}.jsonl").open("w", encoding="utf-8") as f:
            for r in rows[i:i + args.size]:
                f.write(json.dumps({k: r[k] for k in ("key", "title", "year", "venue")} |
                                   {"abstract": r["abstract"][:3000]}, ensure_ascii=False) + "\n")
    print(f"{len(rows)} papers -> {-(-len(rows) // args.size)} batches ({args.round}-NN)")


def collect(args):
    papers = {r["key"]: r for r in included()}
    done = results()
    stray = sorted(set(done) - set(papers))
    for batch in sorted(p.stem for p in BATCHES.glob("*.jsonl")):
        keys = [json.loads(line)["key"] for line in (BATCHES / f"{batch}.jsonl").open()]
        missing = [k for k in keys if done.get(k, {}).get("batch") != batch]
        if (RESULTS / f"{batch}.jsonl").exists() and missing:
            print(f"WARNING {batch}: {len(missing)} keys without results, e.g. {missing[:2]}")

    bad = {k: problems(r) for k, r in done.items() if k in papers}
    bad = {k: v for k, v in bad.items() if v}
    for batch, n in sorted(Counter(done[k]["batch"] for k in bad).items()):
        example = next(k for k in bad if done[k]["batch"] == batch)
        print(f"WARNING {batch}: {n} invalid records, e.g. {example}: {bad[example][:3]}")
    if stray:
        print(f"WARNING {len(stray)} results for papers not included, e.g. {stray[:3]}")
    # Subagents sometimes skim and reuse template text; flag batches where >10% of summaries repeat.
    for batch in sorted({r["batch"] for r in done.values()}):
        texts = Counter((r.get("pmdrl") or {}).get("result") for r in done.values() if r["batch"] == batch)
        repeated, total = sum(n for n in texts.values() if n > 1), sum(texts.values())
        if repeated > total * 0.1:
            print(f"WARNING {batch}: {repeated}/{total} results are repeated sentences; re-extract this batch")
    # Parallel subagents once shared scratch files, attaching one batch's text to another's keys.
    seen = {}
    for r in done.values():
        text = (r.get("pmdrl") or {}).get("problem") or ""
        if len(text) > 30:
            seen.setdefault(text, set()).add(r["batch"])
    shared = Counter(b for batches in seen.values() if len(batches) > 1 for b in batches)
    for batch, n in sorted(shared.items()):
        if n > 3:
            print(f"WARNING {batch}: {n} problems also appear in other batches; check for mixed-up results")

    with (DATA / "extraction.jsonl").open("w", encoding="utf-8") as f:
        for key, r in papers.items():
            if key in done and key not in bad:
                rec = {k: v for k, v in done[key].items() if k != "batch"}
                rec["pmdrl"] = {"who": who(r), **rec["pmdrl"]}
                f.write(json.dumps(rec | {"title": r["title"], "batch": done[key]["batch"]},
                                   ensure_ascii=False) + "\n")
    valid = [done[k] for k in papers if k in done and k not in bad]
    print(f"extracted {len(valid)}/{len(papers)} (invalid {len(bad)})")
    for field in CODES:
        counts = Counter(v for r in valid for v in r["codes"][field])
        print(f"{field}: " + ", ".join(f"{k} {n}" for k, n in counts.most_common()))
    human = sum(bool(r["codes"]["human_comparison"].get("done")) for r in valid)
    print(f"human_comparison done: {human}/{len(valid)}; "
          f"limitation stated: {sum(bool(r['pmdrl'].get('limitation')) for r in valid)}; "
          f"gap stated: {sum(bool(r['pmdrl'].get('gap')) for r in valid)}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("prepare")
    p.add_argument("--round", required=True)
    p.add_argument("--size", type=int, default=70)
    sub.add_parser("collect")
    args = parser.parse_args()
    {"prepare": prepare, "collect": collect}[args.cmd](args)


if __name__ == "__main__":
    main()
