"""Small checks for source integrity and safe prose/math rendering boundaries."""
import json
from types import SimpleNamespace
import unittest
import build_papers as b
import check_explainers as guides


def manuscript():
    return {"id": "SkillMerge", "abstract": "Design [1].", "status": "Empirical results NR.",
            "contributions": ["Protocol"], "pages": [{"heading": "page", "sections": [{"heading": "section", "paragraphs": ["text"]}]} for _ in range(4)],
            "references": [{"number": 1, "text": "Reference", "url": "https://example.org/primary", "claim_scope": "example"}]}


class TypesettingInputs(unittest.TestCase):
    def test_valid_schema(self):
        b.validate(manuscript())

    def test_page_and_nr_contract(self):
        for key in ("pages", "status"):
            data = manuscript()
            data[key] = data[key][:-1] if key == "pages" else "completed"
            with self.assertRaises(AssertionError):
                b.validate(data)

    def test_unresolved_reference_rejected(self):
        data = manuscript()
        data["abstract"] = "Unsupported [2]."
        with self.assertRaises(AssertionError):
            b.validate(data)

    def test_math_scripting_and_tex_rejected(self):
        for equation in ("#read(\"private\")", "$ a $", r"\frac{a}{b}"):
            with self.assertRaises(ValueError):
                b.math(equation)
        self.assertEqual(b.math("frac(a,b)"), "$ frac(a,b) $")

    def test_prose_keeps_literal_control_characters_in_text(self):
        output = b.content('Example "#read(\"x\")" [1].')
        self.assertIn("#text(", output)
        self.assertIn("#link(<bib1>)", output)
        self.assertIn('\\"', output)

    def test_table_shape_rejected(self):
        data = manuscript()
        data["pages"][0]["sections"][0]["table"] = {"headers": ["a", "b"], "rows": [["a"]]}
        with self.assertRaises(AssertionError):
            b.validate(data)

    def test_guide_footer_removed_without_losing_body_numbers(self):
        page = SimpleNamespace(number=1, get_text=lambda **kwargs: "body\n2\n2\n")
        self.assertEqual(guides.page_body(page), "body\n2")
        invalid = SimpleNamespace(number=1, get_text=lambda **kwargs: "body\n3\n")
        with self.assertRaises(AssertionError):
            guides.page_body(invalid)


if __name__ == "__main__":
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(TypesettingInputs))
    folder = b.ROOT / "validation"
    folder.mkdir(exist_ok=True)
    (folder / "typesetting_checks.json").write_text(json.dumps({"tests": result.testsRun, "failures": len(result.failures),
        "errors": len(result.errors), "scope": "source schema and escaping checks; not scientific results"}), encoding="utf-8")
    if not result.wasSuccessful():
        raise SystemExit(1)
