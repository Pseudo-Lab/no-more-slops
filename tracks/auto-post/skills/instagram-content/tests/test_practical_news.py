import importlib.util
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/check_practical_news.py"
spec = importlib.util.spec_from_file_location("practical_news", SCRIPT)
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class PracticalNewsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        (self.base / "prompt.txt").write_text("첨부한 회의록으로 주간 보고서 초안을 작성해줘", encoding="utf-8")
        (self.base / "caption.txt").write_text("새 기능으로 보고서 초안 만들기\n#AI #업무 #프롬프트\n", encoding="utf-8")
        self.story = {"title": "Local workflow", "change_summary": "New local execution",
                      "announcement_url": "https://example.org/launch", "announcement_date": "2026-10-20",
                      "entry_url": "https://example.org/start", "access_conditions": "Paid account",
                      "evidence_status": "Authored prompt, not executed", "prompt_file": "prompt.txt",
                      "caption_file": "caption.txt", "caption_max_characters": 499, "max_hashtags": 3}
        self.manifest = {"edition_date": "2026-10-26", "freshness_window_days": 7, "stories": [self.story]}

    def test_current_story_and_unicode_caption(self):
        errors, results = checker.inspect(self.manifest, self.base)
        self.assertEqual(errors, [])
        self.assertEqual(results[0]["announcement_age_days"], 6)
        self.assertEqual(results[0]["caption_characters"], len((self.base / "caption.txt").read_text()))

    def test_new_help_check_cannot_refresh_old_launch(self):
        self.story.update(announcement_date="2026-09-01", checked_at="2026-10-26")
        errors, _ = checker.inspect(self.manifest, self.base)
        self.assertTrue(any("original announcement" in error for error in errors))

    def test_future_launch_is_rejected(self):
        self.story["announcement_date"] = "2026-10-27"
        self.assertTrue(checker.inspect(self.manifest, self.base)[0])

    def test_missing_access_condition_is_rejected(self):
        self.story["access_conditions"] = ""
        self.assertTrue(any("access_conditions" in error for error in checker.inspect(self.manifest, self.base)[0]))

    def test_companion_cannot_escape_edition(self):
        self.story["prompt_file"] = "../outside.txt"
        self.assertTrue(any("inside" in error for error in checker.inspect(self.manifest, self.base)[0]))

    def test_caption_and_hashtag_overflow_are_rejected(self):
        self.story.update(caption_max_characters=3, max_hashtags=2)
        errors, _ = checker.inspect(self.manifest, self.base)
        self.assertTrue(any("characters" in error for error in errors))
        self.assertTrue(any("hashtags" in error for error in errors))

    def test_invalid_window_and_empty_stories(self):
        self.manifest["freshness_window_days"] = True
        self.assertTrue(checker.inspect(self.manifest, self.base)[0])
        self.manifest.update(freshness_window_days=7, stories=[])
        self.assertTrue(checker.inspect(self.manifest, self.base)[0])

    def test_missing_prompt_is_rejected(self):
        (self.base / "prompt.txt").unlink()
        self.assertTrue(any("prompt_file" in error for error in checker.inspect(self.manifest, self.base)[0]))


if __name__ == "__main__":
    unittest.main()
