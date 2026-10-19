"""Title/abstract screening: batch preparation, result collection, audit sample.

prepare: split unscreened candidates into data/screening/batches/<round>-NN.jsonl
collect: merge data/screening/results/*.jsonl into data/screening.csv and
         draw a human audit sample into data/screening/audit.csv
audit-import: copy decisions saved on the audit page into audit.csv

Usage:
  uv run screen.py prepare --round r1 --title-hit --size 140
  uv run screen.py prepare --round r2 --title-hit --curated
  uv run screen.py prepare --round r2s --sample 140
  uv run screen.py collect [--audit 50]
  uv run screen.py audit-import EXPORT_DIR
"""

import argparse
import csv
import json
import random
from collections import Counter
from pathlib import Path

from common import DATA

SCREEN = DATA / "screening"
BATCHES, RESULTS = SCREEN / "batches", SCREEN / "results"
OVERRIDES = SCREEN / "overrides.jsonl"  # human decisions that replace LLM screening
DECISIONS = {"include", "exclude", "maybe"}
CURATED = ("awesome", "arxiv-bib", "s2-references", "seed-survey")


def candidates():
    with (DATA / "candidates.csv").open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def results():
    out = {}
    for path in sorted(RESULTS.glob("*.jsonl")):
        for line in path.open(encoding="utf-8"):
            if line.strip():
                rec = json.loads(line)
                rec["batch"] = path.stem
                out[rec["key"]] = rec
    if OVERRIDES.exists():
        for line in OVERRIDES.open(encoding="utf-8"):
            if line.strip():
                rec = json.loads(line)
                out[rec["key"]] = {**out.get(rec["key"], {}), **rec, "batch": "human"}
    return out


def prepare(args):
    done = results()
    pending = {p.stem for p in BATCHES.glob("*.jsonl")} - {p.stem for p in RESULTS.glob("*.jsonl")}
    queued = {json.loads(line)["key"] for name in pending for line in (BATCHES / f"{name}.jsonl").open()}
    rows = [r for r in candidates() if r["key"] not in done and r["key"] not in queued]
    if args.title_hit or args.curated:
        rows = [r for r in rows if (args.title_hit and r["title_hit"] == "1")
                or (args.curated and any(s in r["sources"] for s in CURATED))]
    if args.sample:
        rows = random.Random(args.seed).sample(rows, min(args.sample, len(rows)))
    BATCHES.mkdir(parents=True, exist_ok=True)
    for n, i in enumerate(range(0, len(rows), args.size), 1):
        with (BATCHES / f"{args.round}-{n:02d}.jsonl").open("w", encoding="utf-8") as f:
            for r in rows[i:i + args.size]:
                f.write(json.dumps({k: r[k] for k in ("key", "title", "year", "venue")} |
                                   {"abstract": r["abstract"][:2000]}, ensure_ascii=False) + "\n")
    print(f"{len(rows)} papers -> {-(-len(rows) // args.size)} batches ({args.round}-NN)")


def collect(args):
    rows, done = candidates(), results()
    bad = [k for k, r in done.items() if r.get("decision") not in DECISIONS]
    fields = ["key", "title", "year", "venue", "decision", "code", "reason", "batch"]
    with (DATA / "screening.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fields, lineterminator="\n")
        writer.writeheader()
        for r in rows:
            if r["key"] in done:
                writer.writerow({k: r.get(k) or done[r["key"]].get(k, "") for k in fields})

    counts = Counter(r["decision"] for r in done.values())
    print(f"screened {len(done)}/{len(rows)}: " + ", ".join(f"{k} {counts[k]}" for k in sorted(DECISIONS)))
    print("codes: " + ", ".join(f"{k} {v}" for k, v in sorted(Counter(r.get("code") for r in done.values()).items())))
    if bad:
        print(f"invalid decisions: {len(bad)} e.g. {bad[:3]}")

    if (SCREEN / "audit.csv").exists() and not args.resample:
        print("audit sample kept: data/screening/audit.csv (pass --resample to redraw)")
        return
    rng = random.Random(20261019)
    by = {d: sorted(k for k, r in done.items() if r["decision"] == d) for d in DECISIONS}
    sample = (rng.sample(by["include"], min(args.audit, len(by["include"]))) +
              rng.sample(by["exclude"], min(args.audit, len(by["exclude"]))) + by["maybe"])
    titles = {r["key"]: r for r in rows}
    with (SCREEN / "audit.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(["key", "title", "llm_decision", "llm_code", "llm_reason", "human_decision", "human_note"])
        for k in sample:
            writer.writerow([k, titles[k]["title"], done[k]["decision"], done[k].get("code", ""),
                             done[k].get("reason", ""), "", ""])
    print(f"audit sample: {len(sample)} -> data/screening/audit.csv")


def audit_import(args):
    """Fill human_decision/human_note in audit.csv from the audit page's db export."""
    human, migrated = {}, {}
    for path in SCREEN.glob("key_migration_*.json"):
        migrated |= json.loads(path.read_text(encoding="utf-8"))
    for path in args.export.rglob("*.json"):
        doc = json.loads(path.read_text(encoding="utf-8"))
        doc = doc.get("data", doc)
        if doc.get("key"):
            human[migrated.get(doc["key"], doc["key"])] = doc
    path = SCREEN / "audit.csv"
    with path.open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        if r["key"] in human:
            r["human_decision"] = human[r["key"]]["decision"]
            r["human_note"] = human[r["key"]].get("note", "")
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, rows[0].keys(), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    done = [r for r in rows if r["human_decision"]]
    agree = sum(r["human_decision"] == r["llm_decision"] for r in done)
    print(f"imported {len(done)} human decisions; agreement {agree}/{len(done)}")
    for d in ("include", "exclude"):
        sub = [r for r in done if r["llm_decision"] == d]
        if sub:
            print(f"  LLM {d}: human agrees {sum(r['human_decision'] == d for r in sub)}/{len(sub)}, "
                  + ", ".join(f"{k} {v}" for k, v in Counter(r["human_decision"] for r in sub).items()))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("prepare")
    p.add_argument("--round", required=True)
    p.add_argument("--size", type=int, default=140)
    p.add_argument("--title-hit", action="store_true", help="only candidates with a judge-like title")
    p.add_argument("--curated", action="store_true", help="only candidates from awesome lists or survey bibliographies")
    p.add_argument("--sample", type=int, help="random sample of the remaining selection")
    p.add_argument("--seed", type=int, default=20261019)
    c = sub.add_parser("collect")
    c.add_argument("--audit", type=int, default=50)
    c.add_argument("--resample", action="store_true", help="overwrite an existing audit.csv")
    i = sub.add_parser("audit-import")
    i.add_argument("export", type=Path, help="directory written by ArtifactData list with out_dir")
    args = parser.parse_args()
    {"prepare": prepare, "collect": collect, "audit-import": audit_import}[args.cmd](args)


if __name__ == "__main__":
    main()
