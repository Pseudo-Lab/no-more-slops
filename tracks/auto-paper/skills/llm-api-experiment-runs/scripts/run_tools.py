#!/usr/bin/env python3
"""Check a recorded API run and estimate the cost of the next one. Standard library only.

A run directory holds manifest.json (settings, ids, replicates, methods, config_id),
records.jsonl (one row per example x replicate x method, each with an attempt trace)
and, if anything failed, errors.jsonl. Nothing is modified and no API is called.

  check     completeness, duplicates, foreign rows, unreadable outputs, unknown usage,
            error events, and equal settings across runs that will be compared
  estimate  mean tokens and USD per row and method from recorded rows, projected to a
            planned number of rows, with time per row and wall time for given workers
"""

import argparse
import json
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

MISSING = object()


def get(obj, path, default=None):
    for part in path.split(".") if path else []:
        if isinstance(obj, dict) and part in obj:
            obj = obj[part]
        else:
            return default
    return obj


def read_jsonl(path):
    path = Path(path)
    if not path.exists():
        return []
    rows = []
    with path.open(encoding="utf-8") as handle:
        for number, line in enumerate(handle, 1):
            if line.strip():
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError:
                    raise ValueError(f"{path}: line {number} is not JSON (an interrupted write?)") from None
    return rows


def load(run_dir):
    run_dir = Path(run_dir)
    manifest_path = run_dir / "manifest.json"
    if not manifest_path.is_file():
        raise FileNotFoundError(f"{manifest_path} is missing")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    return manifest, read_jsonl(run_dir / "records.jsonl"), read_jsonl(run_dir / "errors.jsonl")


def check_run(run_dir, unreadable="proposal.incomplete", usage="accounting.complete"):
    """Facts about one run; 'problems' lists what blocks reporting it as complete."""
    manifest, rows, errors = load(run_dir)
    problems = []
    ids, methods = manifest.get("ids"), manifest.get("methods")
    replicates = manifest.get("replicates", 1)
    if not isinstance(ids, list) or not isinstance(methods, list) or not isinstance(replicates, int):
        raise ValueError(f"{run_dir}: manifest needs ids (list), methods (list) and replicates (int)")
    expected = {(i, r, m) for i in ids for r in range(replicates) for m in methods}
    if manifest.get("expected_records") not in (None, len(expected)):
        problems.append(f"manifest expected_records {manifest['expected_records']} != grid {len(expected)}")
    seen = Counter((row.get("id"), row.get("replicate", 0), row.get("method")) for row in rows)
    duplicates = [key for key, count in seen.items() if count > 1]
    foreign = [key for key in seen if key not in expected]
    wrong_config = sum(row.get("config_id") != manifest.get("config_id") for row in rows)
    missing = len(expected - set(seen))
    if duplicates:
        problems.append(f"{len(duplicates)} duplicate rows, e.g. {duplicates[0]}")
    if foreign:
        problems.append(f"{len(foreign)} rows outside the manifest grid, e.g. {foreign[0]}")
    if wrong_config:
        problems.append(f"{wrong_config} rows from another configuration")
    if missing:
        problems.append(f"{missing} of {len(expected)} rows missing (resume to finish)")
    unreadable_by_method = Counter(row.get("method") for row in rows
                                   for step in row.get("trace") or [] if get(step, unreadable))
    unknown_usage = sum(get(row, usage) is False for row in rows)
    return {"run_dir": str(run_dir), "status": "complete" if not problems else "incomplete",
            "expected_rows": len(expected), "rows": sum(seen.values()), "missing_rows": missing,
            "error_events": len(errors), "error_types": dict(Counter(e.get("error_type") for e in errors)),
            "unreadable_attempts": dict(unreadable_by_method), "rows_with_unknown_usage": unknown_usage,
            "problems": problems}


def compare(run_dirs, keys):
    """Settings that differ between runs that are meant to be compared."""
    manifests = [(str(path), load(path)[0]) for path in run_dirs]
    first_label, first = manifests[0]
    differences = []
    for label, manifest in manifests[1:]:
        for key in keys:
            if get(manifest, key, MISSING) != get(first, key, MISSING):
                differences.append(f"{label} differs from {first_label} in {key}")
    return differences


def parse_pairs(items, what):
    pairs = {}
    for item in items or []:
        name, sep, value = item.partition("=")
        if not sep:
            raise ValueError(f"{what} takes NAME=VALUE, not {item!r}")
        pairs[name] = value
    return pairs


def estimate(rows, usage_paths, prices, latency_paths=(), planned_rows=None, workers=1, methods=None):
    """Mean tokens and USD per row and method; projection for planned rows (USD per million tokens)."""
    unknown = set(prices) - set(usage_paths)
    if unknown:
        raise ValueError(f"no --usage path for priced token kinds: {sorted(unknown)}")
    per_method = defaultdict(lambda: {"rows": 0, "attempts": 0, "tokens": defaultdict(list), "usd": [], "seconds": []})
    for row in rows:
        method = row.get("method")
        if methods is not None and method not in methods:
            continue
        trace = row.get("trace") or []
        item = per_method[method]
        item["rows"] += 1
        item["attempts"] += len(trace)
        complete = True
        usd = 0.0
        for kind, path in usage_paths.items():
            optional = path.endswith("?")  # e.g. a verifier that is not called on every attempt
            path = path.rstrip("?")
            values = [get(step, path, 0 if optional else None) for step in trace]
            known = [v for v in values if isinstance(v, (int, float)) and not isinstance(v, bool)]
            if len(known) != len(values):
                complete = False
            total = sum(known)
            item["tokens"][kind].append(total)
            usd += total * float(prices.get(kind, 0)) / 1_000_000
        if complete:
            item["usd"].append(usd)
        if latency_paths:
            item["seconds"].append(sum(float(get(step, path) or 0) for step in trace for path in latency_paths))
    out = {}
    for method, item in sorted(per_method.items(), key=lambda pair: str(pair[0])):
        result = {"rows": item["rows"], "attempts_per_row": item["attempts"] / item["rows"],
                  "tokens_per_row": {k: statistics.fmean(v) for k, v in item["tokens"].items()},
                  "usd_per_row": statistics.fmean(item["usd"]) if item["usd"] else None,
                  "rows_with_unknown_usage": item["rows"] - len(item["usd"])}
        if item["seconds"]:
            result["seconds_per_row"] = statistics.fmean(item["seconds"])
        if planned_rows:
            if result["usd_per_row"] is not None:
                result["planned_usd"] = result["usd_per_row"] * planned_rows
            if item["seconds"]:
                result["planned_wall_minutes"] = result["seconds_per_row"] * planned_rows / workers / 60
        out[method] = result
    return out


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("check", help="check one or more run directories")
    p.add_argument("runs", nargs="+")
    p.add_argument("--unreadable", default="proposal.incomplete", help="step field set for unreadable outputs")
    p.add_argument("--usage-complete", default="accounting.complete", help="row field false when usage is unknown")
    p.add_argument("--same", nargs="*", default=[], help="manifest keys that must be equal across the runs")
    p = sub.add_parser("estimate", help="tokens, USD and time per row from recorded rows")
    p.add_argument("run")
    p.add_argument("--usage", action="append", required=True,
                   help="KIND=step.path, e.g. input=proposal.usage.prompt_tokens; end with ? if absence means zero")
    p.add_argument("--price", action="append", default=[], help="KIND=USD per million tokens")
    p.add_argument("--latency", action="append", default=[], help="step field with seconds, summed per row")
    p.add_argument("--rows", type=int, help="planned rows per method")
    p.add_argument("--workers", type=int, default=1)
    p.add_argument("--methods")
    args = parser.parse_args(argv)
    if args.command == "check":
        reports = [check_run(path, args.unreadable, args.usage_complete) for path in args.runs]
        differences = compare(args.runs, args.same) if len(args.runs) > 1 and args.same else []
        result = {"runs": reports, "setting_differences": differences}
        failed = differences or any(r["problems"] for r in reports)
    else:
        if args.workers < 1:
            raise ValueError("--workers must be at least 1")
        _, rows, _ = load(args.run)
        prices = {k: float(v) for k, v in parse_pairs(args.price, "--price").items()}
        methods = set(args.methods.split(",")) if args.methods else None
        result = estimate(rows, parse_pairs(args.usage, "--usage"), prices, args.latency, args.rows, args.workers, methods)
        failed = False
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 1 if failed else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, FileNotFoundError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(2)
