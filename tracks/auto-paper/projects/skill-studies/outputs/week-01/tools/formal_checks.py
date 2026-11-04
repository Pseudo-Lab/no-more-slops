"""Author-constructed mathematical examples, never empirical model performance."""
from collections import Counter, defaultdict
from fractions import Fraction
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


def terminal_risk(observed, abstain_penalty=Fraction(3, 10)):
    """Exact uniform XOR-world Bayes risk with a fixed abstention action."""
    groups = defaultdict(list)
    for x in (0, 1):
        for y in (0, 1):
            bits = {"x": x, "y": y}
            groups[tuple(bits[name] for name in observed)].append(x ^ y)
    return sum(Fraction(len(values), 4) * min(Fraction(min(Counter(values).get(0, 0), Counter(values).get(1, 0)), len(values)),
                                                  abstain_penalty) for values in groups.values())


def proxy_terminal_risk(observed):
    groups = defaultdict(Counter)
    for x in (0, 1):
        for y in (0, 1):
            for noise, probability in ((0, Fraction(4, 5)), (1, Fraction(1, 5))):
                label = x ^ y
                features = {"x": x, "y": y, "proxy": label ^ noise}
                groups[tuple(features[name] for name in observed)][label] += probability / 4
    return sum(min(min(weights.get(0, 0), weights.get(1, 0)), Fraction(3, 10) * sum(weights.values()))
               for weights in groups.values())


def shared_read_cost(actions, already_read=()):
    charged = set(already_read)
    total = 0
    for sources in actions:
        for identity, cost in sources:
            if cost < 0:
                raise ValueError("negative cost")
            if identity not in charged:
                charged.add(identity)
                total += cost
    return total


def left_step_rauc(grid, utilities):
    if len(grid) != len(utilities) or len(grid) < 2 or grid[0] != 0 or grid[-1] != 1:
        raise ValueError("complete normalized grid required")
    if any(a >= b for a, b in zip(grid, grid[1:])):
        raise ValueError("grid must increase")
    if any(value is None for value in utilities[:-1]):
        return None
    return sum((b - a) * utilities[i] for i, (a, b) in enumerate(zip(grid, grid[1:])))


def affected_nodes(starts, edges):
    """Closure in the declared graph; unrecorded dependencies remain unknowable."""
    outgoing = defaultdict(set)
    for source, target in edges:
        outgoing[source].add(target)
    found, pending = set(starts), list(starts)
    while pending:
        for target in outgoing[pending.pop()] - found:
            found.add(target)
            pending.append(target)
    return found


def contract_witness():
    """A strict local output pattern; this does not qualify global branch gains."""
    raw = {"amount": 2, "unit": "thousand_won"}
    parse_ancestor = lambda row: dict(row)
    parse_normalized = lambda row: {"amount": row["amount"] * 1000, "unit": "won"}
    report_ancestor = lambda row: row["amount"] * (1000 if row["unit"] == "thousand_won" else 1)
    report_implicit_unit = lambda row: row["amount"] * 1000
    outputs = [r(p(raw)) for p, r in ((parse_ancestor, report_ancestor), (parse_normalized, report_ancestor),
                                    (parse_ancestor, report_implicit_unit), (parse_normalized, report_implicit_unit))]
    return {"state_order": ["S0", "A", "B", "AB"], "outputs_won": outputs,
            "passes": [value == 2000 for value in outputs], "independent_gain_qualified": False,
            "origin": "author_constructed_interface_example_not_natural_failure_prevalence"}


def tagged_contract_outputs(row):
    """Independent implementation of the manuscript's restricted three-input model."""
    factor = 1000 if row["unit"] == "thousand_won" else 1
    native_amount = int(row["text"].replace(",", ""))
    results = []
    for arm in ("S0", "A", "B", "AB", "adapter"):
        use_a = arm in ("A", "AB", "adapter")
        if not use_a and "," in row["text"]:
            results.append(None)
            continue
        kind = "Native" if use_a else "Won"
        amount = native_amount if use_a else native_amount * factor
        if arm == "adapter":
            kind, amount = "Won", amount * factor
        use_b = arm in ("B", "AB", "adapter")
        if use_b and kind != "Won":
            results.append(None)
            continue
        output = {"amount_won": amount if kind == "Won" else amount * factor}
        if use_b:
            output["record_id"] = row["record_id"]
        results.append(output)
    return results


class FormalExamples(unittest.TestCase):
    def test_manuscript_three_input_gain_and_joint_failure_table(self):
        model = json.loads((ROOT / "skillmerge/METHODS_CONTRACT.json").read_text(encoding="utf-8"))["formal_statements"]
        expected = {row["task"]: row["values"] for row in model["success_table"]["rows"]}
        matrix = []
        for row in model["inputs"]:
            passes = [int(output is not None and output["amount_won"] == row["expected_amount_won"]
                          and (not row["require_id"] or output.get("record_id") == row["record_id"]))
                      for output in tagged_contract_outputs(row)]
            self.assertEqual(passes, expected[row["id"]])
            matrix.append(passes)
        self.assertEqual([sum(column) for column in zip(*matrix)], [1, 2, 2, 0, 3])

    def test_strict_output_pattern_not_global_improvement(self):
        witness = contract_witness()
        self.assertEqual(witness["passes"], [True, True, True, False])
        self.assertFalse(witness["independent_gain_qualified"])

    def test_negative_interaction_not_strict_collapse(self):
        probabilities = list(map(Fraction, (".70", ".85", ".80", ".91")))
        contrast = probabilities[3] - probabilities[1] - probabilities[2] + probabilities[0]
        self.assertEqual(contrast, Fraction(-4, 100))
        self.assertGreater(probabilities[3], probabilities[0])

    def test_rank_reversal_margin(self):
        old = {"winner": Fraction(9, 10), "archived": Fraction(6, 10)}
        corrected = {"winner": Fraction(65, 100), "archived": Fraction(82, 100)}
        self.assertGreater(old["winner"], old["archived"])
        self.assertGreater(corrected["archived"], corrected["winner"] + Fraction(5, 100))

    def test_declared_lineage_closure_and_unaffected_branch(self):
        edges = [("grader-v1", "rejection"), ("rejection", "lesson"), ("lesson", "current"),
                 ("grader-v1", "selection"), ("selection", "current"), ("unrelated", "other")]
        self.assertEqual(affected_nodes(["grader-v1"], edges), {"grader-v1", "rejection", "lesson", "current", "selection"})

    def test_cycle_does_not_break_closure(self):
        self.assertEqual(affected_nodes(["a"], [("a", "b"), ("b", "a")]), {"a", "b"})

    def test_left_step_not_mean_and_nonmonotonic(self):
        grid = [Fraction(0), Fraction(1, 4), Fraction(7, 10), Fraction(1)]
        utilities = [Fraction(1, 5), Fraction(3, 5), Fraction(4, 5), Fraction(1, 2)]
        self.assertEqual(left_step_rauc(grid, utilities), Fraction(14, 25))
        self.assertNotEqual(left_step_rauc(grid, utilities), sum(utilities) / 4)
        self.assertLess(utilities[-1], utilities[-2])

    def test_missing_positive_width_checkpoint_is_not_zero(self):
        self.assertIsNone(left_step_rauc([0, Fraction(1, 2), 1], [Fraction(1, 5), None, Fraction(4, 5)]))

    def test_invalid_budget_grid(self):
        with self.assertRaises(ValueError):
            left_step_rauc([0, 1, 1], [0, 0, 1])

    def test_xor_information_complementarity(self):
        self.assertEqual(terminal_risk(()), Fraction(3, 10))
        self.assertEqual(terminal_risk(("x",)), Fraction(3, 10))
        self.assertEqual(terminal_risk(("y",)), Fraction(3, 10))
        self.assertEqual(terminal_risk(("x", "y")), 0)
        self.assertGreater(terminal_risk(("x",)) - terminal_risk(("x", "y")),
                           terminal_risk(()) - terminal_risk(("y",)))

    def test_shared_source_charge(self):
        a = (("PS1:full", 6000), ("FS1:full", 600))
        b = (("PS1:full", 6000), ("TS1:full", 60))
        self.assertEqual(shared_read_cost((a, b)), 6660)
        self.assertEqual(shared_read_cost((a,)) + shared_read_cost((b,)), 12660)

    def test_eighty_percent_proxy_traps_immediate_gain_greedy(self):
        self.assertEqual(proxy_terminal_risk(()), Fraction(3, 10))
        self.assertEqual(proxy_terminal_risk(("x",)), Fraction(3, 10))
        self.assertEqual(proxy_terminal_risk(("proxy",)), Fraction(1, 5))
        self.assertEqual(proxy_terminal_risk(("proxy", "x")), Fraction(1, 5))
        self.assertEqual(proxy_terminal_risk(("x", "y")), 0)

    def test_distinct_window_is_distinct_source(self):
        self.assertEqual(shared_read_cost(((("PS1:[0,6000)", 6000),), (("PS1:[0,3000)", 3000),))), 9000)

    def test_same_disclosed_evidence_different_cache_different_cost(self):
        action = (("PS1:full", 6000),)
        self.assertEqual(shared_read_cost((action,)), 6000)
        self.assertEqual(shared_read_cost((action,), already_read=("PS1:full",)), 0)

    def test_failure_cache_same_budget_changes_feasibility(self):
        pressure_failed_cost = flow_failed_cost = 4 + 1
        budget_a = 8 - pressure_failed_cost
        budget_b = 8 - flow_failed_cost
        self.assertEqual(budget_a, budget_b)
        pressure_action = (("PS1:full", 4),)
        next_a = shared_read_cost((pressure_action,), already_read=("PS1:full",)) + 1
        next_b = shared_read_cost((pressure_action,), already_read=("FS1:full",)) + 1
        self.assertEqual((next_a, next_b), (1, 5))
        self.assertLessEqual(next_a, budget_a)
        self.assertGreater(next_b, budget_b)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(FormalExamples)
    outcome = unittest.TextTestRunner(verbosity=2).run(suite)
    if not outcome.wasSuccessful():
        raise SystemExit(1)
    report = {"origin": "author_constructed_mathematical_and_contract_examples", "scientific_performance": "NR",
        "model_calls": 0, "tests": outcome.testsRun, "failures": len(outcome.failures), "errors": len(outcome.errors),
        "skillmerge": {"simple_strict_witness": contract_witness(),
                       "manuscript_three_input_pass_counts": [1, 2, 2, 0, 3],
                       "scope": "toy mathematical mean gains and adapter correctness, not empirical Q-qualified histories"},
        "second_chance": {"left_step_rauc_example": "14/25 = 0.56", "genuine_correction_histories": 0,
                          "closure_claim": "declared dependency reachability only, not minimal semantic repair certificate"},
        "probeflow": {"xor_terminal_risks": {"none": "3/10", "x": "3/10", "y": "3/10", "xy": "0"},
                      "shared_samples": 6660, "naive_separate_samples": 12660,
                      "failure_cache_counterexample": {"same_empty_observation_mask": True, "same_remaining_budget": 3,
                          "next_pressure_costs": [1, 5], "condition": "source retained after value-independent analysis failures",
                          "scope": "compressed feature/mask/budget state is insufficient in this admitted case; not always insufficient"},
                      "noisy_proxy_example": {"noise_rate": "1/5", "proxy_plus_one_bit_risk": "1/5", "two_bits_risk": "0",
                                              "unit_costs": True, "budget": 2, "scope": "author analytic example, not new greedy impossibility theorem"},
                      "scope": "exact constructed finite examples; no industrial policy benefit measured"}}
    folder = ROOT / "validation"
    folder.mkdir(exist_ok=True)
    (folder / "formal_examples.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
