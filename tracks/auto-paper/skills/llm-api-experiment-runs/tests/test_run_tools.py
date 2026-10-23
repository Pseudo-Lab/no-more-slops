"""Behavioral tests with invented runs; no API calls."""
import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/run_tools.py"
spec = importlib.util.spec_from_file_location("run_tools", SCRIPT)
run_tools = importlib.util.module_from_spec(spec)
spec.loader.exec_module(run_tools)


def attempt(prompt=100, output=10, cached=0, verifier=50, incomplete=None, seconds=1.0):
    usage = {} if prompt is None else {"prompt_tokens": prompt, "completion_tokens": output,
                                       "prompt_tokens_details": {"cached_tokens": cached}}
    step = {"proposal": {"usage": usage, "latency_s": seconds, "incomplete": incomplete},
            "verification": {"latency_s": .5}}
    if verifier is not None:
        step["verification"]["usage"] = {"input_tokens": verifier}
    return step


class RunToolsTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def write_run(self, name, rows, manifest=None, errors=()):
        path = self.root / name
        path.mkdir()
        manifest = {"config_id": "cfg", "ids": ["a", "b"], "replicates": 1, "methods": ["direct", "loop"],
                    "expected_records": 4, "code_sha256": "c1", **(manifest or {})}
        (path / "manifest.json").write_text(json.dumps(manifest))
        (path / "records.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
        if errors:
            (path / "errors.jsonl").write_text("".join(json.dumps(e) + "\n" for e in errors))
        return path

    def rows(self):
        return [{"id": "a", "replicate": 0, "method": "direct", "config_id": "cfg", "trace": [attempt(verifier=None)]},
                {"id": "b", "replicate": 0, "method": "direct", "config_id": "cfg", "trace": [attempt(verifier=None)]},
                {"id": "a", "replicate": 0, "method": "loop", "config_id": "cfg",
                 "trace": [attempt(), attempt(prompt=300, output=30, cached=200)]},
                {"id": "b", "replicate": 0, "method": "loop", "config_id": "cfg", "accounting": {"complete": False},
                 "trace": [attempt(), attempt(prompt=None, incomplete="content_filter")]}]

    def test_complete_run_with_an_unreadable_output_and_unknown_usage(self):
        report = run_tools.check_run(self.write_run("run", self.rows()))
        self.assertEqual(report["status"], "complete")
        self.assertEqual(report["unreadable_attempts"], {"loop": 1})
        self.assertEqual(report["rows_with_unknown_usage"], 1)

    def test_missing_duplicate_foreign_and_other_config_rows_are_problems(self):
        rows = self.rows()
        rows = rows[:3] + [dict(rows[2]), {**rows[0], "id": "zzz"}, {**rows[1], "config_id": "old"}]
        report = run_tools.check_run(self.write_run("run", rows, errors=[{"error_type": "HTTP402"}]))
        self.assertEqual(report["status"], "incomplete")
        text = " ".join(report["problems"])
        for expected in ("duplicate", "outside the manifest grid", "another configuration", "1 of 4 rows missing"):
            self.assertIn(expected, text)
        self.assertEqual(report["error_types"], {"HTTP402": 1})

    def test_runs_to_compare_must_share_settings(self):
        first = self.write_run("one", self.rows())
        second = self.write_run("two", self.rows(), {"code_sha256": "c2"})
        self.assertEqual(run_tools.compare([first, second], ["config_id"]), [])
        self.assertIn("code_sha256", run_tools.compare([first, second], ["code_sha256"])[0])

    def test_estimate_uses_known_usage_and_optional_fields(self):
        prices = {"input": .05, "cached": -.045, "output": .4, "verifier": .042}
        usage = {"input": "proposal.usage.prompt_tokens", "cached": "proposal.usage.prompt_tokens_details.cached_tokens",
                 "output": "proposal.usage.completion_tokens", "verifier": "verification.usage.input_tokens?"}
        result = run_tools.estimate(self.rows(), usage, prices, ["proposal.latency_s", "verification.latency_s"],
                                    planned_rows=1000, workers=4)
        loop, direct = result["loop"], result["direct"]
        # Row a: 400 input (200 cached), 40 output, 100 verifier tokens; row b has unknown usage and is left out.
        expected = (400 * .05 - 200 * .045 + 40 * .4 + 100 * .042) / 1e6
        self.assertAlmostEqual(loop["usd_per_row"], expected)
        self.assertEqual(loop["rows_with_unknown_usage"], 1)
        self.assertAlmostEqual(direct["usd_per_row"], (100 * .05 + 10 * .4) / 1e6)  # no verifier: optional zero
        self.assertAlmostEqual(loop["seconds_per_row"], 3.0)
        self.assertAlmostEqual(loop["planned_wall_minutes"], 3.0 * 1000 / 4 / 60)
        self.assertAlmostEqual(loop["attempts_per_row"], 2)
        with self.assertRaisesRegex(ValueError, "no --usage path"):
            run_tools.estimate(self.rows(), {"input": usage["input"]}, prices)

    def test_cli_exit_codes(self):
        good = self.write_run("good", self.rows())
        bad = self.write_run("bad", self.rows()[:3])
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(run_tools.main(["check", str(good)]), 0)
            self.assertEqual(run_tools.main(["check", str(bad)]), 1)
            self.assertEqual(run_tools.main(["check", str(good), str(bad), "--same", "config_id"]), 1)
        with self.assertRaises(FileNotFoundError):
            run_tools.main(["check", str(self.root / "nope")])


if __name__ == "__main__":
    unittest.main()
