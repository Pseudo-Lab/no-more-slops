"""Claim extraction for the comparison questions, plus bias/mitigation recoding.

prepare: split included papers without results into data/synthesis/batches/<round>-NN.jsonl
collect: validate data/synthesis/results/*.jsonl, write data/synthesis/claims.csv,
         data/synthesis/codes.jsonl, and print per-question direction counts

Questions, claim fields and the recoding vocabulary are defined in docs/synthesis.md.

Usage:
  uv run synthesize.py prepare --round c1 --size 110
  uv run synthesize.py collect
"""

import argparse
import csv
import json
from collections import Counter

from common import DATA
from extract import included

SYN = DATA / "synthesis"
BATCHES, RESULTS = SYN / "batches", SYN / "results"
QUESTIONS = ("Q-FORMAT", "Q-MULTI", "Q-SCALE", "Q-SELF", "Q-HARD", "Q-COT", "Q-REF", "Q-FT", "Q-EXPERT",
             "Q-DEBIAS", "Q-ATTACK", "Q-DEFENSE")
DIRECTIONS = ("support", "refute", "conditional", "null")
BASES = ("own_method", "evaluation")
BIASES = {"position", "verbosity", "style", "anchoring", "self_preference", "authority", "sycophancy", "social",
          "inconsistency", "prompt_sensitivity", "leniency", "competence", "criteria", "leakage", "adversarial",
          "other"}
MITIGATION = {"cot", "rubric", "reference", "decomposition", "prompt_optimization", "swap", "ensemble",
              "critique_refine", "fine_tuning", "calibration", "internal", "tool_grounding", "human_in_loop",
              "abstention", "other"}


def results():
    out = {}
    for path in sorted(RESULTS.glob("*.jsonl")):
        for line in path.open(encoding="utf-8"):
            if line.strip():
                rec = json.loads(line)
                rec["batch"] = path.stem
                out[rec["key"]] = rec
    return out


def problems(rec):
    """Return a list of schema violations for one result record."""
    out = []
    for field, allowed in (("biases", BIASES), ("mitigation", MITIGATION)):
        values = rec.get(field)
        if not isinstance(values, list):
            out.append(f"{field} not a list")
        elif set(values) - allowed:
            out.append(f"{field} unknown {sorted(set(values) - allowed)}")
    claims = rec.get("claims")
    if not isinstance(claims, list):
        return out + ["claims not a list"]
    for c in claims:
        if c.get("question") not in QUESTIONS:
            out.append(f"unknown question {c.get('question')}")
        if c.get("direction") not in DIRECTIONS:
            out.append(f"unknown direction {c.get('direction')}")
        if c.get("basis") not in BASES:
            out.append(f"unknown basis {c.get('basis')}")
        if not c.get("claim"):
            out.append("empty claim")
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
                f.write(json.dumps({k: r[k] for k in ("key", "title", "year")} |
                                   {"abstract": r["abstract"][:3000]}, ensure_ascii=False) + "\n")
    print(f"{len(rows)} papers -> {-(-len(rows) // args.size)} batches ({args.round}-NN)")


def collect(args):
    papers = {r["key"]: r for r in included()}
    done = {k: r for k, r in results().items() if k in papers}
    for batch in sorted(p.stem for p in BATCHES.glob("*.jsonl")):
        keys = [json.loads(line)["key"] for line in (BATCHES / f"{batch}.jsonl").open()]
        missing = [k for k in keys if k not in done]
        if (RESULTS / f"{batch}.jsonl").exists() and missing:
            print(f"WARNING {batch}: {len(missing)} keys without results, e.g. {missing[:2]}")
    bad = {k: v for k, r in done.items() if (v := problems(r))}
    for batch, n in sorted(Counter(done[k]["batch"] for k in bad).items()):
        example = next(k for k in bad if done[k]["batch"] == batch)
        print(f"WARNING {batch}: {n} invalid records, e.g. {example}: {bad[example][:3]}")
    # Subagents sometimes skim and reuse template text; flag batches where >10% of claims repeat.
    for batch in sorted({r["batch"] for r in done.values()}):
        texts = Counter(c.get("claim") for r in done.values() if r["batch"] == batch for c in r.get("claims") or [])
        repeated, total = sum(n for n in texts.values() if n > 1), sum(texts.values())
        if total and repeated > total * 0.1:
            print(f"WARNING {batch}: {repeated}/{total} claims are repeated sentences; re-extract this batch")

    valid = {k: r for k, r in done.items() if k not in bad}
    SYN.mkdir(parents=True, exist_ok=True)
    with (SYN / "codes.jsonl").open("w", encoding="utf-8") as f:
        for k, r in valid.items():
            f.write(json.dumps({"key": k, "biases": r["biases"], "mitigation": r["mitigation"]},
                               ensure_ascii=False) + "\n")
    fields = ["question", "direction", "basis", "key", "title", "year", "claim", "condition", "evidence"]
    with (SYN / "claims.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fields, lineterminator="\n")
        writer.writeheader()
        for k, r in sorted(valid.items()):
            for c in r["claims"]:
                writer.writerow({"key": k, "title": papers[k]["title"], "year": papers[k]["year"],
                                 **{x: " ".join(str(c.get(x) or "").split()) for x in
                                    ("question", "direction", "basis", "claim", "condition", "evidence")}})

    print(f"collected {len(valid)}/{len(papers)} (invalid {len(bad)})")
    counts = Counter((c["question"], c["direction"], c["basis"]) for r in valid.values() for c in r["claims"])
    print("question   " + " ".join(f"{d:>11}" for d in DIRECTIONS) + "   (evaluation / own_method)")
    for q in QUESTIONS:
        print(f"{q:<10} " + " ".join(f"{counts[q, d, 'evaluation']:>5}/{counts[q, d, 'own_method']:<5}"
                                     for d in DIRECTIONS))
    for field in ("biases", "mitigation"):
        c = Counter(v for r in valid.values() for v in r[field])
        print(f"{field}: " + ", ".join(f"{k} {n}" for k, n in c.most_common()))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("prepare")
    p.add_argument("--round", required=True)
    p.add_argument("--size", type=int, default=110)
    sub.add_parser("collect")
    args = parser.parse_args()
    {"prepare": prepare, "collect": collect}[args.cmd](args)


if __name__ == "__main__":
    main()
