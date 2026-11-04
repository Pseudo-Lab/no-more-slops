#!/usr/bin/env python3
"""Derive, check and compare recorded LLM-run trajectories without new API calls.

Records are JSON Lines, one object per row (example x replicate x method) with a
``trace`` list of attempts in order. Field paths are dotted and configurable, so
existing record formats work without conversion. Standard library only; inputs are
never modified.

Commands:
  derive   cut stop-at-pass trajectories at a smaller repair limit and/or choose the
           final attempt by a rule (last or first proposal when none passed)
  pairing  check that methods (and reruns) start from the same first proposal
  overlap  check that a continued run reproduces its source up to the source limit
  paired   paired difference between two methods, averaged per example over runs,
           with an example-level bootstrap interval
  plan     count rows that a continuation or a rerun after the first rejection
           would send new requests for
"""

import argparse
import hashlib
import json
import random
import statistics
import sys
from collections import defaultdict
from pathlib import Path

MISSING = object()


def get(obj, path, default=MISSING):
    """Value at a dotted path; default (or KeyError) when absent."""
    for part in path.split(".") if path else []:
        if isinstance(obj, dict) and part in obj:
            obj = obj[part]
        else:
            if default is MISSING:
                raise KeyError(path)
            return default
    return obj


def put(obj, path, value):
    """Set a dotted path, creating objects on the way."""
    parts = path.split(".")
    for part in parts[:-1]:
        if not isinstance(obj.get(part), dict):
            obj[part] = {}
        obj = obj[part]
    obj[parts[-1]] = value


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def records_path(path):
    path = Path(path)
    return path / "records.jsonl" if path.is_dir() else path


def read_rows(path):
    rows = []
    with records_path(path).open(encoding="utf-8") as handle:
        for number, line in enumerate(handle, 1):
            if line.strip():
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError as exc:
                    raise ValueError(f"{path}: line {number} is not JSON ({exc.msg})") from None
    return rows


def sha256(path):
    digest = hashlib.sha256()
    with records_path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def key_of(row):
    return (row["id"], row.get("replicate", 0))


def unique_rows(rows, label):
    seen = set()
    for row in rows:
        key = (*key_of(row), row["method"])
        if key in seen:
            raise ValueError(f"{label}: duplicate row {key}")
        seen.add(key)
    return rows


def methods_filter(text):
    return set(text.split(",")) if text else None


class Fields:
    def __init__(self, args):
        self.passed, self.correct = args.passed, args.correct
        self.proposal, self.row_correct = args.proposal, args.row_correct

    def step_passed(self, step):
        value = get(step, self.passed)
        if not isinstance(value, bool):
            raise ValueError(f"step field {self.passed!r} must be true or false")
        return value

    def final_correct(self, row):
        """Row-level correctness if recorded, else the final step's."""
        value = get(row, self.row_correct, None)
        if value is None:
            trace = row["trace"]
            value = get(trace[row.get("final_attempt", len(trace) - 1)], self.correct, None)
        return value


def check_stop_at_pass(row, fields, limit):
    """A stop-at-pass trajectory: no pass before its last attempt, and it ends at a pass or at the limit."""
    trace = row.get("trace")
    if not isinstance(trace, list) or not trace:
        raise ValueError(f"row {key_of(row)} {row['method']}: empty trace")
    passes = [fields.step_passed(step) for step in trace]
    if any(passes[:-1]) or len(trace) > limit + 1 or (not passes[-1] and len(trace) != limit + 1):
        raise ValueError(f"row {key_of(row)} {row['method']}: trace does not follow stop-at-pass with limit {limit}")
    return passes


def derive(rows, fields, limit, rule, source_limit, methods=None, sums=()):
    """Rows as a run with the smaller limit and the rule would have recorded them (stop-at-pass methods)."""
    if limit > source_limit:
        raise ValueError(f"cannot derive limit {limit} from runs that stopped at {source_limit}; continue them instead")
    out = []
    for row in rows:
        row = json.loads(json.dumps(row))
        if methods is not None and row["method"] not in methods:
            out.append(row)
            continue
        passes = check_stop_at_pass(row, fields, source_limit)
        trace = row["trace"][:limit + 1]
        passed = passes[:limit + 1]
        if passed[-1]:
            final = len(trace) - 1
        else:
            final = 0 if rule == "first" else len(trace) - 1
        step = trace[final]
        row.update(trace=trace, final_attempt=final, passed=passed[-1], exhausted=not passed[-1] and len(trace) == limit + 1,
                   repairs=len(trace) - 1, final_proposal=get(step, fields.proposal, None),
                   derived={"limit": limit, "rule": rule})
        if fields.row_correct:
            put(row, fields.row_correct, get(step, fields.correct, None))
        if sums:
            row["sums"] = {path: sum(float(get(s, path, 0) or 0) for s in trace) for path in sums}
        out.append(row)
    return out


def first_proposals(rows, fields):
    firsts = defaultdict(dict)
    for row in rows:
        firsts[key_of(row)][row["method"]] = canonical(get(row["trace"][0], fields.proposal))
    return firsts


def check_pairing(runs, fields, methods=None, expect=None):
    """Within each run every method shares a key's first proposal; across runs report how many keys match run 1."""
    report = {"runs": [], "errors": []}
    reference = None
    for label, rows in runs:
        rows = [row for row in rows if methods is None or row["method"] in methods]
        firsts = first_proposals(rows, fields)
        split = [key for key, by_method in firsts.items() if len(set(by_method.values())) > 1]
        if split:
            report["errors"].append(f"{label}: {len(split)} keys have methods with different first proposals, e.g. {split[0]}")
        shared = {key: next(iter(by_method.values())) for key, by_method in firsts.items()}
        entry = {"run": label, "keys": len(shared), "methods": sorted({row["method"] for row in rows})}
        if reference is None:
            reference = shared
        else:
            common = [key for key in shared if key in reference]
            same = sum(shared[key] == reference[key] for key in common)
            entry.update(common_keys=len(common), same_as_first_run=same)
            if expect == "shared" and same != len(common):
                report["errors"].append(f"{label}: {len(common) - same} of {len(common)} first proposals differ from run 1")
            if expect == "new" and common and same == len(common):
                report["errors"].append(f"{label}: every first proposal equals run 1's; a repeat needs new samples")
        report["runs"].append(entry)
    return report


def check_overlap(extended, source, fields, limit, methods=None):
    """The continued run, cut at the source limit, must reproduce every source row."""
    ext = {(*key_of(row), row["method"]): row for row in extended}
    errors = []
    for row in source:
        if methods is not None and row["method"] not in methods:
            continue
        key = (*key_of(row), row["method"])
        other = ext.get(key)
        if other is None:
            errors.append(f"{key}: missing from the continued run")
            continue
        head = other["trace"][:limit + 1]
        mine = row["trace"][:limit + 1]
        if len(head) < len(mine):
            errors.append(f"{key}: continued run has fewer attempts than the source")
            continue
        for index, (a, b) in enumerate(zip(mine, head)):
            if (canonical(get(a, fields.proposal, None)) != canonical(get(b, fields.proposal, None))
                    or fields.step_passed(a) != fields.step_passed(b)):
                errors.append(f"{key}: attempt {index} differs")
                break
        else:
            if fields.step_passed(mine[-1]) and len(other["trace"]) != len(mine):
                errors.append(f"{key}: the source passed at attempt {len(mine) - 1} but the continued run kept going")
    return errors


def percentile(values, q):
    values = sorted(values)
    position = (len(values) - 1) * q
    low, high = int(position), min(int(position) + 1, len(values) - 1)
    return values[low] + (values[high] - values[low]) * (position - low)


def paired(runs, fields, method_a, method_b, exclude=(), samples=2000, seed=1729):
    """a minus b on matching keys; each example averaged over runs first, then examples resampled."""
    per_example = defaultdict(list)
    pairs = 0
    for _, rows in runs:
        values = defaultdict(dict)
        for row in rows:
            if row["method"] not in (method_a, method_b) or any(str(get(row, f, None)) == v for f, v in exclude):
                continue
            correct = fields.final_correct(row)
            if correct is not None:
                values[key_of(row)][row["method"]] = float(bool(correct))
        for (example, _), pair in values.items():
            if method_a in pair and method_b in pair:
                per_example[example].append(pair[method_a] - pair[method_b])
                pairs += 1
    if not per_example:
        return {"n_examples": 0, "n_pairs": 0, "delta": None, "ci95": None}
    examples = sorted(per_example, key=str)  # fixed order: the same seed gives the same interval
    means = [statistics.fmean(per_example[e]) for e in examples]
    rng = random.Random(seed)
    boot = [statistics.fmean(rng.choices(means, k=len(means))) for _ in range(samples)]
    return {"n_examples": len(means), "n_pairs": pairs, "delta": statistics.fmean(means),
            "ci95": [percentile(boot, .025), percentile(boot, .975)], "samples": samples, "seed": seed}


def plan(rows, fields, source_limit, new_limit=None, methods=None):
    """Rows that need new requests: continuation to new_limit, or a rerun after the first rejection."""
    counts = defaultdict(lambda: {"rows": 0, "reached_limit": 0, "first_rejected": 0})
    for row in rows:
        if methods is not None and row["method"] not in methods:
            continue
        passes = check_stop_at_pass(row, fields, source_limit)
        item = counts[row["method"]]
        item["rows"] += 1
        item["reached_limit"] += not passes[-1]
        item["first_rejected"] += not passes[0]
    out = {}
    for method, item in sorted(counts.items()):
        if new_limit is not None:
            item["continuation_max_new_attempts"] = item["reached_limit"] * max(0, new_limit - source_limit)
        out[method] = item
    return out


def source_limit_of(path, given):
    if given is not None:
        return given
    manifest = Path(path) / "manifest.json"
    if Path(path).is_dir() and manifest.is_file():
        value = json.loads(manifest.read_text(encoding="utf-8")).get("max_repairs")
        if isinstance(value, int) and not isinstance(value, bool):
            return value
    raise ValueError(f"{path}: give --source-limit (no manifest.json with an integer max_repairs)")


def write_rows(out_dir, rows, provenance):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "records.jsonl"
    if target.exists():
        raise ValueError(f"{target} exists; choose a new output directory")
    with target.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    (out_dir / "derived.json").write_text(json.dumps(provenance, indent=2) + "\n", encoding="utf-8")


def parse_exclude(items):
    pairs = []
    for item in items or []:
        field, sep, value = item.partition("=")
        if not sep:
            raise ValueError(f"--exclude takes FIELD=VALUE, not {item!r}")
        pairs.append((field, value))
    return pairs


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--passed", default="passed", help="step field: did the attempt pass the gate (bool)")
    parser.add_argument("--correct", default="correct", help="step field: is the attempt correct (bool/null)")
    parser.add_argument("--proposal", default="proposal", help="step field compared for pairing and overlap")
    parser.add_argument("--row-correct", default="correct", help="row field with the final correctness ('' to skip)")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("derive", help="cut at a smaller limit and/or choose the final attempt")
    p.add_argument("source")
    p.add_argument("output")
    p.add_argument("--limit", type=int, required=True)
    p.add_argument("--rule", choices=("last", "first"), default="last")
    p.add_argument("--source-limit", type=int)
    p.add_argument("--methods", help="comma-separated stop-at-pass methods to derive; others are copied")
    p.add_argument("--sum", action="append", default=[], help="step field to total over the kept attempts")

    p = sub.add_parser("pairing", help="check shared first proposals within and across runs")
    p.add_argument("runs", nargs="+")
    p.add_argument("--methods")
    p.add_argument("--expect", choices=("shared", "new"))

    p = sub.add_parser("overlap", help="check that a continued run reproduces its source")
    p.add_argument("extended")
    p.add_argument("source")
    p.add_argument("--limit", type=int)
    p.add_argument("--methods")

    p = sub.add_parser("paired", help="paired difference with an example-level bootstrap")
    p.add_argument("runs", nargs="+")
    p.add_argument("--a", required=True, help="method whose correctness is minuend")
    p.add_argument("--b", required=True, help="baseline method")
    p.add_argument("--exclude", action="append", help="skip rows whose FIELD equals VALUE (FIELD=VALUE)")
    p.add_argument("--samples", type=int, default=2000)
    p.add_argument("--seed", type=int, default=1729)

    p = sub.add_parser("plan", help="count rows a continuation or partial rerun would request")
    p.add_argument("run")
    p.add_argument("--source-limit", type=int)
    p.add_argument("--new-limit", type=int)
    p.add_argument("--methods")
    args = parser.parse_args(argv)
    fields = Fields(args)

    if args.command == "derive":
        limit = source_limit_of(args.source, args.source_limit)
        rows = unique_rows(read_rows(args.source), args.source)
        out = derive(rows, fields, args.limit, args.rule, limit, methods_filter(args.methods), args.sum)
        write_rows(args.output, out, {"source": str(records_path(args.source)), "source_sha256": sha256(args.source),
                                      "source_limit": limit, "limit": args.limit, "rule": args.rule,
                                      "methods": args.methods, "rows": len(out)})
        result = {"rows": len(out), "output": str(Path(args.output) / "records.jsonl")}
    elif args.command == "pairing":
        runs = [(path, unique_rows(read_rows(path), path)) for path in args.runs]
        result = check_pairing(runs, fields, methods_filter(args.methods), args.expect)
    elif args.command == "overlap":
        limit = source_limit_of(args.source, args.limit)
        errors = check_overlap(read_rows(args.extended), read_rows(args.source), fields, limit, methods_filter(args.methods))
        result = {"limit": limit, "errors": errors}
    elif args.command == "paired":
        runs = [(path, unique_rows(read_rows(path), path)) for path in args.runs]
        result = paired(runs, fields, args.a, args.b, parse_exclude(args.exclude), args.samples, args.seed)
    else:
        limit = source_limit_of(args.run, args.source_limit)
        result = plan(read_rows(args.run), fields, limit, args.new_limit, methods_filter(args.methods))
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 1 if isinstance(result, dict) and result.get("errors") else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, KeyError, FileNotFoundError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(2)
