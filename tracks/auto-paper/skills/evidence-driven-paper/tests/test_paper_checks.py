"""Behavioral CLI tests with invented records; no paper data or network."""
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/paper_checks.py"
HAS_PYPDF = importlib.util.find_spec("pypdf") is not None


class PaperChecksTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        # Deliberately different order: pairing by position gives the wrong result.
        self.a = [{"dataset": "a", "seed": 1, "loss": .10},
                  {"dataset": "b", "seed": 1, "loss": .20},
                  {"dataset": "c", "seed": 1, "loss": .30}]
        self.b = [{"dataset": "c", "seed": 1, "loss": .30},
                  {"dataset": "a", "seed": 1, "loss": .15},
                  {"dataset": "b", "seed": 1, "loss": .21}]
        self.write_rows("candidate.jsonl", self.a)
        self.write_rows("baseline.jsonl", self.b)
        self.spec = {
            "id": "loss", "candidate": {"name": "Candidate", "path": "candidate.jsonl"},
            "baseline": {"name": "Baseline", "path": "baseline.jsonl"},
            "keys": ["dataset", "seed"], "metric": "loss",
            "direction": "lower", "roster": "exact", "expected_pairs": 3,
        }
        self.config = {"schema_version": 1, "comparisons": [self.spec]}

    def write_rows(self, name, rows):
        (self.root / name).write_text("".join(json.dumps(row) + "\n" for row in rows))

    def invoke(self, config=None, extra=(), no_site=False):
        (self.root / "checks.json").write_text(json.dumps(self.config if config is None else config))
        command = [sys.executable] + (["-S"] if no_site else [])
        env = os.environ.copy()
        if no_site:
            env.pop("PYTHONPATH", None)
        process = subprocess.run(command + [str(SCRIPT), str(self.root / "checks.json"), *extra],
                                 capture_output=True, text=True, env=env)
        self.assertNotIn("Traceback", process.stderr)
        return process.returncode, json.loads(process.stdout)

    def failed(self, phrase, *, code=1, **kwargs):
        actual, report = self.invoke(**kwargs)
        self.assertEqual(actual, code, report)
        self.assertEqual(report["status"], "failed")
        self.assertIn(phrase, " ".join(report["errors"]))
        return report

    def test_pairing_by_keys_and_explicit_winner(self):
        code, report = self.invoke()
        self.assertEqual(code, 0, report)
        r = report["comparisons"][0]
        self.assertEqual((r["candidate_wins"], r["baseline_wins"], r["ties"]), (2, 0, 1))
        self.assertAlmostEqual(r["mean_difference"], -.02)
        self.assertIn("Candidate outperforms Baseline on 2 of 3 matched pairs", r["sentence"])
        self.assertEqual(r["sources"]["candidate"]["sha256"],
                         hashlib.sha256((self.root / "candidate.jsonl").read_bytes()).hexdigest())

    def test_higher_direction_changes_wins_not_difference_definition(self):
        self.spec["direction"] = "higher"
        code, report = self.invoke()
        self.assertEqual(code, 0)
        r = report["comparisons"][0]
        self.assertEqual((r["candidate_wins"], r["baseline_wins"], r["ties"]), (0, 2, 1))
        self.assertAlmostEqual(r["mean_difference"], -.02)
        self.assertIn("higher is better", r["sentence"])

    def test_swapping_methods_negates_mean_and_exchanges_counts(self):
        _, before = self.invoke()
        self.spec["candidate"], self.spec["baseline"] = self.spec["baseline"], self.spec["candidate"]
        _, after = self.invoke()
        a, b = before["comparisons"][0], after["comparisons"][0]
        self.assertAlmostEqual(a["mean_difference"], -b["mean_difference"])
        self.assertEqual(a["candidate_wins"], b["baseline_wins"])
        self.assertEqual(a["ties"], b["ties"])

    def test_permuting_both_files_keeps_results(self):
        _, first = self.invoke()
        self.write_rows("candidate.jsonl", list(reversed(self.a)))
        self.write_rows("baseline.jsonl", list(reversed(self.b)))
        _, second = self.invoke()
        for key in ("candidate_wins", "baseline_wins", "ties", "mean_difference", "sentence"):
            self.assertEqual(first["comparisons"][0][key], second["comparisons"][0][key])

    def test_exact_roster_rejects_extra_and_does_not_emit_winner(self):
        self.write_rows("candidate.jsonl", self.a + [{"dataset": "extra", "seed": 1, "loss": .1}])
        r = self.failed("exact roster mismatch")["comparisons"][0]
        self.assertEqual(r["candidate_only_keys"], [["extra", 1]])
        self.assertNotIn("sentence", r)

    def test_intersection_requires_expected_size_and_discloses_both_sides(self):
        self.write_rows("candidate.jsonl", self.a + [{"dataset": "extra-a", "seed": 1, "loss": .1}])
        self.write_rows("baseline.jsonl", self.b + [{"dataset": "extra-b", "seed": 1, "loss": .1}])
        self.spec["roster"] = "intersection"
        code, report = self.invoke()
        self.assertEqual(code, 0)
        r = report["comparisons"][0]
        self.assertEqual(r["matched_pairs"], 3)
        self.assertEqual(r["candidate_only_keys"], [["extra-a", 1]])
        self.assertEqual(r["baseline_only_keys"], [["extra-b", 1]])
        self.spec["expected_pairs"] = 4
        self.failed("expected 4 matched pairs, found 3")

    def test_no_overlap_fails_even_for_intersection(self):
        self.write_rows("baseline.jsonl", [{"dataset": "other", "seed": 1, "loss": .1}])
        self.spec["roster"] = "intersection"
        self.failed("found 0")

    def test_duplicate_observation_is_not_silently_overwritten(self):
        self.write_rows("candidate.jsonl", self.a + [self.a[0]])
        self.failed("duplicate observation key")

    def test_missing_fields_and_empty_input(self):
        for rows in ([{"dataset": "a", "seed": 1}], []):
            with self.subTest(rows=rows):
                self.write_rows("candidate.jsonl", rows)
                self.failed("missing key or metric" if rows else "no records")

    def test_nonfinite_boolean_and_text_metrics_fail(self):
        for value in (float("nan"), float("inf"), -float("inf"), True, "0.1", 10**400):
            with self.subTest(value=str(value)[:30]):
                rows = copy.deepcopy(self.a)
                rows[0]["loss"] = value
                self.write_rows("candidate.jsonl", rows)
                code, report = self.invoke()
                self.assertEqual(code, 1, report)

    def test_invalid_unmatched_rows_are_not_hidden_by_intersection(self):
        self.spec["roster"] = "intersection"
        self.write_rows("candidate.jsonl", self.a + [{"dataset": "extra", "seed": 1, "loss": True}])
        self.failed("metric must be a number")

    def test_pair_key_types_are_significant_and_booleans_rejected(self):
        self.b[1]["seed"] = "1"
        self.write_rows("baseline.jsonl", self.b)
        self.failed("exact roster mismatch")
        self.b[1]["seed"] = True
        self.write_rows("baseline.jsonl", self.b)
        self.failed("pairing keys must be strings or integers")

    def test_duplicate_json_fields_fail(self):
        (self.root / "candidate.jsonl").write_text(
            '{"dataset":"a","seed":1,"loss":0.1,"loss":0.2}\n')
        self.failed("duplicate JSON field")

    def test_malformed_json_includes_filename_and_line(self):
        (self.root / "candidate.jsonl").write_text('{"dataset":')
        self.failed("candidate.jsonl:1")

    def test_incorrect_claim_counts_fail_with_observed_result(self):
        self.spec["expect"] = {"candidate_wins": 3, "ties": 0}
        r = self.failed("candidate_wins: expected 3, observed 2")["comparisons"][0]
        self.assertEqual(r["candidate_wins"], 2)
        self.assertIn("ties: expected 0, observed 1", r["errors"])

    def test_invalid_configurations_fail_closed(self):
        cases = [
            {}, {"schema_version": True, "artifacts": [{"path": "candidate.jsonl"}]},
            {"schema_version": 1}, {"schema_version": 1, "comparisons": {}},
            {"schema_version": 1, "artifact": []},
        ]
        for mutate in (
            lambda c: c["comparisons"][0].update(direction="smaller"),
            lambda c: c["comparisons"][0].update(roster="guess"),
            lambda c: c["comparisons"][0].update(expected_pairs=True),
            lambda c: c["comparisons"][0].update(keys=["dataset", "dataset"]),
            lambda c: c["comparisons"][0].update(keys=["loss"]),
            lambda c: c["comparisons"][0].update(expect={"candidate_win": 2}),
            lambda c: c["comparisons"].append(copy.deepcopy(c["comparisons"][0])),
        ):
            config = copy.deepcopy(self.config)
            mutate(config)
            cases.append(config)
        for config in cases:
            with self.subTest(config=config):
                code, report = self.invoke(config)
                self.assertEqual(code, 2, report)

    def test_paths_cannot_escape_manifest_root(self):
        outside = self.root.parent / (self.root.name + "-outside")
        outside.write_text("outside")
        self.addCleanup(outside.unlink)
        link = self.root / "link"
        link.symlink_to(outside)
        for name in ("../" + outside.name, str(outside), "link"):
            with self.subTest(path=name):
                config = {"schema_version": 1, "artifacts": [{"path": name}]}
                code, report = self.invoke(config)
                self.assertEqual(code, 1, report)

    def test_hash_detects_changes_from_previously_saved_bytes(self):
        data = self.root / "candidate.jsonl"
        digest = hashlib.sha256(data.read_bytes()).hexdigest()
        config = {"schema_version": 1, "artifacts": [{"path": data.name, "sha256": digest}]}
        self.assertEqual(self.invoke(config)[0], 0)
        data.write_bytes(data.read_bytes() + b"\n")
        self.failed("differs from saved baseline", config=config)

    def test_missing_artifact_and_bad_hash_configuration(self):
        self.failed("input file not found", config={"schema_version": 1,
                                                    "artifacts": [{"path": "supplement.pdf"}]})
        self.failed("saved 64-digit", code=2, config={"schema_version": 1, "artifacts": [
            {"path": "candidate.jsonl", "sha256": "REPLACE_ME"}]})

    def test_multiple_checks_continue_after_failure(self):
        self.config["artifacts"] = [{"path": "missing.zip"}, {"path": "baseline.jsonl"}]
        report = self.failed("input file not found")
        self.assertEqual(report["comparisons"][0]["status"], "passed")
        self.assertEqual([a["status"] for a in report["artifacts"]], ["failed", "passed"])

    def test_output_is_created_and_existing_input_never_overwritten(self):
        out = self.root / "report.json"
        code, report = self.invoke(extra=["--output", str(out)])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out.read_text()), report)
        self.failed("report output", code=2, extra=["--output", str(out)])
        original = (self.root / "candidate.jsonl").read_bytes()
        self.failed("report output", code=2,
                    extra=["--output", str(self.root / "candidate.jsonl")])
        self.assertEqual((self.root / "candidate.jsonl").read_bytes(), original)

    def test_stdlib_comparisons_do_not_require_optional_packages(self):
        code, report = self.invoke(no_site=True)
        self.assertEqual(code, 0, report)

    def test_missing_pdf_dependency_is_not_a_successful_skip(self):
        config = {"schema_version": 1, "artifacts": [{"path": "candidate.jsonl", "pages": 4}]}
        self.failed("require pypdf", config=config, no_site=True)

    @unittest.skipUnless(HAS_PYPDF, "optional PDF tests require pypdf")
    def test_pdf_page_budget_and_exact_count(self):
        from pypdf import PdfWriter
        writer = PdfWriter()
        for _ in range(4):
            writer.add_blank_page(width=612, height=792)
        writer.write(self.root / "paper.pdf")
        config = {"schema_version": 1, "artifacts": [{"path": "paper.pdf", "pages": 4}]}
        self.assertEqual(self.invoke(config)[0], 0)
        config["artifacts"][0] = {"path": "paper.pdf", "max_pages": 3}
        self.failed("exceeds limit 3", config=config)
        config["artifacts"][0] = {"path": "paper.pdf", "pages": 5}
        self.failed("expected 5 PDF pages, found 4", config=config)

    @unittest.skipUnless(HAS_PYPDF, "optional PDF tests require pypdf")
    def test_non_pdf_cannot_satisfy_page_check(self):
        config = {"schema_version": 1, "artifacts": [{"path": "candidate.jsonl", "pages": 4}]}
        self.failed("cannot count PDF pages", config=config)

    def test_bundled_example_runs_after_whole_skill_copy(self):
        installed = self.root / "installed-skill"
        shutil.copytree(SCRIPT.parent.parent, installed)
        process = subprocess.run([sys.executable, str(installed / "scripts/paper_checks.py"),
                                  str(installed / "assets/example/checks.json")],
                                 capture_output=True, text=True)
        self.assertEqual(process.returncode, 0, process.stderr)
        report = json.loads(process.stdout)
        r = report["comparisons"][0]
        self.assertEqual((r["candidate_wins"], r["baseline_wins"], r["ties"]), (1, 1, 1))


if __name__ == "__main__":
    unittest.main()
