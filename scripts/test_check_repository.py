import tempfile
from pathlib import Path
import unittest

from check_repository import inspect


class RepositoryRulesTest(unittest.TestCase):
    def check(self, files):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for path, content in files.items():
                target = root / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(content, encoding="utf-8")
            return inspect(root, files)[0]

    def test_valid_skill_and_result(self):
        self.assertEqual(self.check({
            "tracks/auto-paper/skills/review-paper/SKILL.md": "---\nname: review-paper\ndescription: Review evidence.\n---\n",
            "tracks/auto-paper/projects/study/README.md": "Study",
            "tracks/auto-paper/projects/study/outputs/week-01/README.md": "Results",
            "tracks/auto-paper/projects/study/outputs/week-01/paper.pdf": "fixture",
        }), [])

    def test_duplicate_names_across_tracks(self):
        skill = "---\nname: review-paper\ndescription: Review.\n---\n"
        errors = self.check({f"tracks/{track}/skills/review-paper/SKILL.md": skill
                             for track in ("auto-paper", "auto-post")})
        self.assertTrue(any("duplicate skill" in error for error in errors))

    def test_legacy_and_project_local_skill(self):
        errors = self.check({"auto-paper/demo/.claude/skills/demo/SKILL.md": "---\nname: demo\ndescription: Demo.\n---\n"})
        self.assertTrue(any("move contributions" in error for error in errors))
        self.assertTrue(any("SKILL.md must use" in error for error in errors))

    def test_result_requires_week_and_index(self):
        errors = self.check({"tracks/auto-paper/projects/study/outputs/paper.pdf": "fixture"})
        self.assertTrue(any("week-NN" in error for error in errors))
        self.assertTrue(any("missing README.md" in error for error in errors))

    def test_reject_mismatch_and_missing_description(self):
        errors = self.check({"tracks/auto-post/skills/demo/SKILL.md": "---\nname: wrong\n---\n"})
        self.assertTrue(any("must match" in error for error in errors))
        self.assertTrue(any("missing frontmatter description" in error for error in errors))

    def test_skill_assets_are_not_final_deliverables(self):
        self.assertEqual(self.check({
            "tracks/auto-paper/skills/demo/SKILL.md": "---\nname: demo\ndescription: Example.\n---\n",
            "tracks/auto-paper/skills/demo/assets/example.pdf": "fixture",
        }), [])

    def test_reject_arbitrary_root_project(self):
        errors = self.check({"my-new-project/README.md": "Project"})
        self.assertTrue(any("project directories belong" in error for error in errors))

    def test_project_source_fixtures_are_allowed(self):
        self.assertEqual(self.check({
            "tracks/auto-application/projects/demo/README.md": "Project",
            "tracks/auto-application/projects/demo/app/tests/fixtures/sample.pdf": "fixture",
        }), [])


if __name__ == "__main__":
    unittest.main()
