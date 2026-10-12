#!/usr/bin/env python3
"""Check declared paired results and submission artifacts; never edit inputs."""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import math
from pathlib import Path
import re
import sys
from typing import Any


class CheckError(ValueError):
    """An actionable configuration or input error."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckError(message)


def object_fields(value: Any, required: set[str], optional: set[str], where: str) -> None:
    require(isinstance(value, dict), f"{where}: expected an object")
    require(required <= value.keys(), f"{where}: missing fields {sorted(required - value.keys())}")
    require(value.keys() <= required | optional,
            f"{where}: unknown fields {sorted(value.keys() - required - optional)}")


def nonempty(value: Any, where: str) -> None:
    require(isinstance(value, str) and bool(value.strip()), f"{where}: expected a nonempty string")


def integer(value: Any, minimum: int, where: str) -> None:
    require(type(value) is int and value >= minimum, f"{where}: expected an integer >= {minimum}")


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        require(key not in result, f"duplicate JSON field: {key}")
        result[key] = value
    return result


def reject_constant(value: str) -> None:
    raise CheckError(f"nonfinite JSON constant: {value}")


def decode(text: str) -> Any:
    return json.loads(text, object_pairs_hook=unique_object, parse_constant=reject_constant)


def validate(config: Any) -> None:
    object_fields(config, {"schema_version"}, {"comparisons", "artifacts"}, "config")
    require(type(config["schema_version"]) is int and config["schema_version"] == 1,
            "schema_version must be integer 1")
    for group in ("comparisons", "artifacts"):
        require(isinstance(config.get(group, []), list), f"{group}: expected an array")
    require(bool(config.get("comparisons") or config.get("artifacts")), "config contains no checks")
    ids: set[str] = set()
    for index, spec in enumerate(config.get("comparisons", [])):
        where = f"comparisons[{index}]"
        object_fields(spec, {"id", "candidate", "baseline", "keys", "metric", "direction",
                             "roster", "expected_pairs"}, {"expect"}, where)
        nonempty(spec["id"], f"{where}.id")
        require(spec["id"] not in ids, f"duplicate comparison id: {spec['id']}")
        ids.add(spec["id"])
        for side in ("candidate", "baseline"):
            object_fields(spec[side], {"name", "path"}, set(), f"{where}.{side}")
            for field in ("name", "path"):
                nonempty(spec[side][field], f"{where}.{side}.{field}")
        require(spec["candidate"]["name"] != spec["baseline"]["name"],
                f"{where}: candidate and baseline names must differ")
        require(isinstance(spec["keys"], list) and bool(spec["keys"]),
                f"{where}.keys: expected a nonempty array")
        for key in spec["keys"]:
            nonempty(key, f"{where}.keys")
        require(len(set(spec["keys"])) == len(spec["keys"]), f"{where}: duplicate key fields")
        nonempty(spec["metric"], f"{where}.metric")
        require(spec["metric"] not in spec["keys"], f"{where}: metric cannot be a pairing key")
        require(spec["direction"] in ("lower", "higher"), f"{where}: direction must be lower or higher")
        require(spec["roster"] in ("exact", "intersection"),
                f"{where}: roster must be exact or intersection")
        integer(spec["expected_pairs"], 1, f"{where}.expected_pairs")
        if "expect" in spec:
            object_fields(spec["expect"], set(), {"candidate_wins", "baseline_wins", "ties"},
                          f"{where}.expect")
            for key, value in spec["expect"].items():
                integer(value, 0, f"{where}.expect.{key}")
    for index, spec in enumerate(config.get("artifacts", [])):
        where = f"artifacts[{index}]"
        object_fields(spec, {"path"}, {"sha256", "pages", "max_pages"}, where)
        nonempty(spec["path"], f"{where}.path")
        if "sha256" in spec:
            require(isinstance(spec["sha256"], str) and
                    re.fullmatch(r"[0-9a-fA-F]{64}", spec["sha256"]) is not None,
                    f"{where}.sha256: expected a saved 64-digit hex digest")
        for key in ("pages", "max_pages"):
            if key in spec:
                integer(spec[key], 1, f"{where}.{key}")
        if "pages" in spec and "max_pages" in spec:
            require(spec["pages"] <= spec["max_pages"], f"{where}: pages exceeds max_pages")


def input_file(root: Path, relative: str) -> tuple[bytes, dict[str, Any]]:
    declared = Path(relative)
    require(not declared.is_absolute(), f"input path must be relative: {relative}")
    path = (root / declared).resolve()
    require(path.is_relative_to(root), f"input path escapes manifest directory: {relative}")
    require(path.is_file(), f"input file not found: {relative}")
    data = path.read_bytes()
    return data, {"path": relative, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}


def records(root: Path, side: dict[str, str], keys: list[str],
            metric: str) -> tuple[dict[tuple[Any, ...], float], dict[str, Any]]:
    data, source = input_file(root, side["path"])
    rows: dict[tuple[Any, ...], float] = {}
    for number, line in enumerate(data.decode("utf-8").splitlines(), 1):
        if not line.strip():
            continue
        where = f"{side['path']}:{number}"
        try:
            row = decode(line)
        except (ValueError, RecursionError) as exc:
            raise CheckError(f"{where}: {exc}") from exc
        require(isinstance(row, dict), f"{where}: expected a JSON object")
        require(all(key in row for key in keys + [metric]), f"{where}: missing key or metric field")
        values = tuple(row[key] for key in keys)
        require(all(type(value) in (str, int) for value in values),
                f"{where}: pairing keys must be strings or integers")
        # bool is deliberately excluded; string "1" and integer 1 stay distinct.
        require(values not in rows, f"{where}: duplicate observation key {values}")
        value = row[metric]
        require(type(value) in (int, float), f"{where}: metric must be a number, not bool or text")
        try:
            numeric = float(value)
        except OverflowError as exc:
            raise CheckError(f"{where}: metric is outside finite float range") from exc
        require(math.isfinite(numeric), f"{where}: metric must be finite")
        rows[values] = numeric
    require(bool(rows), f"{side['path']}: no records")
    source["records"] = len(rows)
    return rows, source


def key_list(keys: set[tuple[Any, ...]]) -> list[list[Any]]:
    return [list(key) for key in sorted(keys, key=lambda key: json.dumps(key, ensure_ascii=True))]


def compare(root: Path, spec: dict[str, Any]) -> dict[str, Any]:
    candidate, candidate_source = records(root, spec["candidate"], spec["keys"], spec["metric"])
    baseline, baseline_source = records(root, spec["baseline"], spec["keys"], spec["metric"])
    matched = candidate.keys() & baseline.keys()
    extra_candidate = candidate.keys() - baseline.keys()
    extra_baseline = baseline.keys() - candidate.keys()
    result: dict[str, Any] = {
        "id": spec["id"], "status": "passed", "errors": [],
        "metric": spec["metric"], "direction": spec["direction"],
        "difference_definition": "candidate minus baseline",
        "candidate": spec["candidate"]["name"], "baseline": spec["baseline"]["name"],
        "keys": spec["keys"], "roster": spec["roster"], "matched_pairs": len(matched),
        "candidate_only_keys": key_list(extra_candidate),
        "baseline_only_keys": key_list(extra_baseline),
        "sources": {"candidate": candidate_source, "baseline": baseline_source},
    }
    if spec["roster"] == "exact" and (extra_candidate or extra_baseline):
        result["errors"].append("exact roster mismatch; inspect candidate_only_keys and baseline_only_keys")
    if len(matched) != spec["expected_pairs"]:
        result["errors"].append(f"expected {spec['expected_pairs']} matched pairs, found {len(matched)}")
    # Do not emit a winner sentence for a disallowed or unexpectedly sized roster.
    if result["errors"]:
        result["status"] = "failed"
        return result
    order = sorted(matched, key=lambda key: json.dumps(key, ensure_ascii=True))
    a, b = [candidate[key] for key in order], [baseline[key] for key in order]
    n = len(order)
    differences = [x - y for x, y in zip(a, b)]
    require(all(math.isfinite(value) for value in differences), "paired differences overflowed")
    try:
        # Divide first to avoid overflowing a finite mean of large values.
        means = [math.fsum(value / n for value in values) for values in (a, b, differences)]
    except OverflowError as exc:
        raise CheckError("mean calculation overflowed") from exc
    require(all(math.isfinite(value) for value in means), "means must be finite")
    win = (lambda x, y: x < y) if spec["direction"] == "lower" else (lambda x, y: x > y)
    counts = {
        "candidate_wins": sum(win(x, y) for x, y in zip(a, b)),
        "baseline_wins": sum(win(y, x) for x, y in zip(a, b)),
        "ties": sum(x == y for x, y in zip(a, b)),
    }
    result.update(counts)
    result.update(candidate_mean=means[0], baseline_mean=means[1], mean_difference=means[2])
    result["sentence"] = (
        f"{result['candidate']} outperforms {result['baseline']} on "
        f"{counts['candidate_wins']} of {n} matched pairs for {spec['metric']} "
        f"({spec['direction']} is better); {result['baseline']} wins "
        f"{counts['baseline_wins']}, with {counts['ties']} exact ties."
    )
    for key, value in spec.get("expect", {}).items():
        if counts[key] != value:
            result["errors"].append(f"{key}: expected {value}, observed {counts[key]}")
    result["status"] = "failed" if result["errors"] else "passed"
    return result


def artifact(root: Path, spec: dict[str, Any]) -> dict[str, Any]:
    data, result = input_file(root, spec["path"])
    result.update(status="passed", errors=[])
    if "sha256" in spec and result["sha256"] != spec["sha256"].lower():
        result["errors"].append("SHA-256 differs from saved baseline")
    if "pages" in spec or "max_pages" in spec:
        try:
            from pypdf import PdfReader
        except Exception as exc:
            raise CheckError("PDF page checks require pypdf and working dependencies; "
                             f"install requirements-dev.txt in this Python environment: {exc}") from exc
        try:
            pages = len(PdfReader(io.BytesIO(data)).pages)
        except Exception as exc:
            raise CheckError(f"cannot count PDF pages: {exc}") from exc
        result["pages"] = pages
        if "pages" in spec and pages != spec["pages"]:
            result["errors"].append(f"expected {spec['pages']} PDF pages, found {pages}")
        if "max_pages" in spec and pages > spec["max_pages"]:
            result["errors"].append(f"PDF has {pages} pages, exceeds limit {spec['max_pages']}")
    result["status"] = "failed" if result["errors"] else "passed"
    return result


def run(config_path: Path) -> tuple[dict[str, Any], int]:
    report: dict[str, Any] = {
        "schema_version": 1, "status": "failed",
        "scope": "Declared record and artifact checks only; no statistical or independent certification.",
        "errors": [], "comparisons": [], "artifacts": [],
    }
    try:
        data = config_path.read_bytes()
        config = decode(data.decode("utf-8"))
        validate(config)
        report["manifest_sha256"] = hashlib.sha256(data).hexdigest()
    except (OSError, ValueError, RecursionError) as exc:
        report["errors"].append(f"configuration: {exc}")
        return report, 2
    root = config_path.resolve().parent
    for group, check in (("comparisons", compare), ("artifacts", artifact)):
        for spec in config.get(group, []):
            label = spec.get("id", spec.get("path"))
            try:
                result = check(root, spec)
            except (OSError, ValueError, OverflowError, RecursionError) as exc:
                result = {"id" if group == "comparisons" else "path": label,
                          "status": "failed", "errors": [str(exc)]}
            report[group].append(result)
            report["errors"].extend(f"{group}/{label}: {error}" for error in result["errors"])
    report["status"] = "failed" if report["errors"] else "passed"
    return report, 1 if report["errors"] else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("config", type=Path, help="JSON manifest; input paths are relative to its directory")
    parser.add_argument("--output", type=Path, help="also create a new JSON report; existing files are refused")
    args = parser.parse_args(argv)
    report, code = run(args.config)
    if args.output is not None:
        try:
            # Exclusive creation also protects input files, including symlink targets.
            with args.output.open("x", encoding="utf-8") as handle:
                handle.write(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False) + "\n")
        except OSError as exc:
            report["status"] = "failed"
            report["errors"].append(f"report output: {exc}")
            code = 2
    print(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False))
    return code


if __name__ == "__main__":
    sys.exit(main())
