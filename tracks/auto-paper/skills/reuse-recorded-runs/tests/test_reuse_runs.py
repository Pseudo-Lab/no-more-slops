"""Behavioral tests with invented trajectories; no API calls or project data."""
import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/reuse_runs.py"
spec = importlib.util.spec_from_file_location("reuse_runs", SCRIPT)
reuse_runs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reuse_runs)

# (passed, correct) per attempt of a stop-at-pass loop with limit 3. a: right first answer that never passes,
# then wrong repairs; b: fixed by a passing repair; c: wrong first answer, right last repair that never passes;
# d: passes at once.
LOOP = {"a": [(0, 1), (0, 0), (0, 0), (0, 0)], "b": [(0, 0), (1, 1)], "c": [(0, 0), (0, 0), (0, 0), (0, 1)],
        "d": [(1, 1)]}


def step(example, attempt, passed, correct, run=1):
    return {"attempt": attempt, "proposal": {"call": f"{example}-{attempt}", "run": run},
            "passed": bool(passed), "correct": bool(correct), "latency_s": 1.0}


def rows(run=1, loop=LOOP, method="loop", limit=3):
    out = []
    for example, attempts in loop.items():
        trace = [step(example, i, p, c, run) for i, (p, c) in enumerate(attempts)]
        out.append({"id": example, "replicate": 0, "method": method, "max_repairs": limit, "trace": trace,
                    "correct": trace[-1]["correct"]})
        first = trace[0]
        out.append({"id": example, "replicate": 0, "method": "direct", "trace": [{**first, "passed": True}],
                    "correct": first["correct"]})
    return out


class Args:
    passed, correct, proposal, row_correct = "passed", "correct", "proposal", "correct"


FIELDS = reuse_runs.Fields(Args)


def accuracy(derived, method="loop"):
    picked = [r["correct"] for r in derived if r["method"] == method]
    return sum(picked) / len(picked)


class DeriveTest(unittest.TestCase):
    def test_final_rule_changes_only_unpassed_rows(self):
        first = reuse_runs.derive(rows(), FIELDS, 3, "first", 3, {"loop"})
        last = reuse_runs.derive(rows(), FIELDS, 3, "last", 3, {"loop"})
        self.assertEqual(accuracy(first), .75)  # a kept right, b fixed, c lost, d right
        self.assertEqual(accuracy(last), .75)   # a broken, b fixed, c fixed, d right
        by_id = {r["id"]: r for r in first if r["method"] == "loop"}
        self.assertEqual((by_id["a"]["final_attempt"], by_id["b"]["final_attempt"]), (0, 1))
        self.assertTrue(by_id["a"]["exhausted"] and not by_id["b"]["exhausted"])
        self.assertEqual(len(by_id["a"]["trace"]), 4)  # the loop ran as recorded; only the answer differs
        self.assertEqual(by_id["a"]["final_proposal"], {"call": "a-0", "run": 1})

    def test_cut_at_a_smaller_limit(self):
        cut = reuse_runs.derive(rows(), FIELDS, 1, "last", 3, {"loop"}, sums=("latency_s",))
        by_id = {r["id"]: r for r in cut if r["method"] == "loop"}
        self.assertEqual([len(by_id[k]["trace"]) for k in "abcd"], [2, 2, 2, 1])
        self.assertEqual(accuracy(cut), .5)  # b passes at 1; a and c stop wrong at 1
        self.assertEqual(by_id["a"]["sums"], {"latency_s": 2.0})
        self.assertEqual(by_id["a"]["derived"], {"limit": 1, "rule": "last"})
        direct = [r for r in cut if r["method"] == "direct"]
        self.assertNotIn("derived", direct[0])  # other methods are copied unchanged

    def test_refuses_a_larger_limit_or_a_broken_trajectory(self):
        with self.assertRaisesRegex(ValueError, "continue them"):
            reuse_runs.derive(rows(), FIELDS, 5, "last", 3, {"loop"})
        broken = rows(loop={"x": [(1, 1), (0, 0)]})
        with self.assertRaisesRegex(ValueError, "stop-at-pass"):
            reuse_runs.derive(broken, FIELDS, 1, "last", 3, {"loop"})
        short = rows(loop={"x": [(0, 0), (0, 0)]})  # stopped early without passing
        with self.assertRaisesRegex(ValueError, "stop-at-pass"):
            reuse_runs.derive(short, FIELDS, 1, "last", 3, {"loop"})


class PairingTest(unittest.TestCase):
    def test_methods_and_reruns_share_first_proposals(self):
        report = reuse_runs.check_pairing([("run1", rows()), ("rerun", rows())], FIELDS, expect="shared")
        self.assertEqual(report["errors"], [])
        self.assertEqual(report["runs"][1]["same_as_first_run"], 4)

    def test_repeats_need_new_samples(self):
        report = reuse_runs.check_pairing([("run1", rows()), ("run2", rows(run=2))], FIELDS, expect="new")
        self.assertEqual(report["errors"], [])
        copied = reuse_runs.check_pairing([("run1", rows()), ("run2", rows())], FIELDS, expect="new")
        self.assertIn("needs new samples", copied["errors"][0])

    def test_a_method_with_another_first_proposal_is_reported(self):
        data = rows()
        data[0]["trace"][0]["proposal"] = {"call": "other"}
        report = reuse_runs.check_pairing([("run1", data)], FIELDS)
        self.assertIn("different first proposals", report["errors"][0])


class OverlapTest(unittest.TestCase):
    def extended(self):
        longer = {k: v + ([(0, 0), (1, 1)] if not v[-1][0] else []) for k, v in LOOP.items()}
        return rows(loop=longer, limit=5)

    def test_continuation_reproduces_the_source(self):
        self.assertEqual(reuse_runs.check_overlap(self.extended(), rows(), FIELDS, 3, {"loop"}), [])

    def test_changed_attempt_or_continued_pass_is_reported(self):
        ext = self.extended()
        ext[0]["trace"][2]["proposal"] = {"call": "changed"}
        self.assertIn("attempt 2 differs", reuse_runs.check_overlap(ext, rows(), FIELDS, 3, {"loop"})[0])
        ext = self.extended()
        b = next(r for r in ext if r["id"] == "b" and r["method"] == "loop")
        b["trace"].append(step("b", 2, 1, 1))
        self.assertIn("kept going", reuse_runs.check_overlap(ext, rows(), FIELDS, 3, {"loop"})[0])


class PairedTest(unittest.TestCase):
    def test_examples_are_averaged_over_runs_before_resampling(self):
        run1 = reuse_runs.derive(rows(), FIELDS, 3, "first", 3, {"loop"})
        run2 = reuse_runs.derive(rows(run=2), FIELDS, 3, "last", 3, {"loop"})
        result = reuse_runs.paired([("1", run1), ("2", run2)], FIELDS, "loop", "direct")
        # loop - direct per example: a (0, -1) -> -.5, b (1, 1) -> 1, c (0, 1) -> .5, d (0, 0) -> 0
        self.assertEqual((result["n_examples"], result["n_pairs"]), (4, 8))
        self.assertAlmostEqual(result["delta"], .25)
        again = reuse_runs.paired([("1", run1), ("2", run2)], FIELDS, "loop", "direct")
        self.assertEqual(result["ci95"], again["ci95"])  # fixed seed and example order

    def test_excluded_rows_are_left_out(self):
        data = rows()
        for row in data:
            if row["id"] == "b":
                row["category"] = "presence_only"
        result = reuse_runs.paired([("1", data)], FIELDS, "loop", "direct", exclude=[("category", "presence_only")])
        self.assertEqual(result["n_examples"], 3)


class PlanAndCliTest(unittest.TestCase):
    def test_plan_counts_rows_needing_new_requests(self):
        result = reuse_runs.plan(rows(), FIELDS, 3, new_limit=10, methods={"loop"})
        self.assertEqual(result["loop"], {"rows": 4, "reached_limit": 2, "first_rejected": 3,
                                          "continuation_max_new_attempts": 14})

    def test_cli_derive_writes_provenance_and_never_overwrites(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "run"
            source.mkdir()
            (source / "manifest.json").write_text(json.dumps({"max_repairs": 3}))
            (source / "records.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows()))
            out = Path(tmp) / "first"
            with contextlib.redirect_stdout(io.StringIO()):
                code = reuse_runs.main(["derive", str(source), str(out), "--limit", "3", "--rule", "first",
                                        "--methods", "loop"])
            self.assertEqual(code, 0)
            provenance = json.loads((out / "derived.json").read_text())
            self.assertEqual((provenance["source_limit"], provenance["rule"], provenance["rows"]), (3, "first", 8))
            self.assertEqual(len(provenance["source_sha256"]), 64)
            with self.assertRaisesRegex(ValueError, "exists"):
                reuse_runs.main(["derive", str(source), str(out), "--limit", "3", "--methods", "loop"])
            buffer = io.StringIO()
            with contextlib.redirect_stdout(buffer):
                code = reuse_runs.main(["pairing", str(source), str(out), "--expect", "shared"])
            self.assertEqual(code, 0)
            self.assertEqual(json.loads(buffer.getvalue())["errors"], [])


if __name__ == "__main__":
    unittest.main()
