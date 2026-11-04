"""Checks check_xcstrings.py on small catalogs.

usage: python3 tests/test_check_xcstrings.py
"""
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

SCRIPT = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "check_xcstrings.py"


def unit(value, state="translated"):
    return {"stringUnit": {"state": state, "value": value}}


def catalog(strings):
    return {"sourceLanguage": "en", "version": "1.0", "strings": strings}


class CheckXcstringsTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix="xcstrings-test-")
        self.addCleanup(temp.cleanup)
        self.dir = pathlib.Path(temp.name)

    def check(self, strings, *options, raw=None):
        path = self.dir / "Localizable.xcstrings"
        path.write_text(raw if raw is not None else json.dumps(catalog(strings), ensure_ascii=False), encoding="utf-8")
        result = subprocess.run([sys.executable, str(SCRIPT), str(path), *options], capture_output=True, text=True)
        return result.returncode, result.stdout + result.stderr

    def test_complete_catalog_passes(self):
        code, out = self.check({
            "Save": {"localizations": {"ko": unit("저장"), "ja": unit("保存")}},
            "%lld photos": {"localizations": {"ko": unit("사진 %lld장"), "ja": unit("%lld枚の写真")}},
            "Internal id": {"shouldTranslate": False},
        })
        self.assertEqual(code, 0, out)
        self.assertIn("checked ja, ko", out)
        self.assertIn("PASS 2 strings", out)

    def test_missing_and_empty_translations_fail(self):
        code, out = self.check({
            "Save": {"localizations": {"ko": unit("저장"), "ja": unit("")}},
            "Share": {"localizations": {"ko": unit("공유")}},
        })
        self.assertEqual(code, 1)
        self.assertIn("[ja] missing: Save", out)
        self.assertIn("[ja] missing: Share", out)

    def test_required_languages_option(self):
        code, out = self.check({"Save": {"localizations": {"ko": unit("저장")}}}, "--languages", "ko", "fr")
        self.assertEqual(code, 1)
        self.assertIn("[fr] missing: Save", out)

    def test_format_specifiers(self):
        code, out = self.check({
            "%@ and %@": {"localizations": {"ko": unit("%2$@ 그리고 %1$@"), "ja": unit("%@")}},
        })
        self.assertEqual(code, 1)
        self.assertNotIn("[ko] format", out)
        self.assertIn("[ja] format specifiers", out)

    def test_plural_variations(self):
        plural = {"variations": {"plural": {"one": unit("사진 한 장"), "other": unit("사진 %lld장")}}}
        code, out = self.check({"%lld photos": {"localizations": {"ko": plural}}})
        self.assertEqual(code, 0, out)

    def test_korean_particles_follow_the_last_syllable(self):
        strings = {
            "a": {"localizations": {"ko": unit("톤릿은 사진을 보정해요")}},
            "b": {"localizations": {"ko": unit("톤릿를 열어요")}},
            "c": {"localizations": {"ko": unit("톤릿로서 처음")}},
            "d": {"localizations": {"ko": unit("헤이즈은 예전 이름")}},
            "e": {"localizations": {"ko": unit("서울로 가요, 서울으로 가요")}},
            "f": {"localizations": {"ko": unit("톤릿으로 저장해요")}},
        }
        code, out = self.check(strings, "--brand", "톤릿", "--brand", "헤이즈", "--brand", "서울")
        self.assertEqual(code, 1)
        self.assertIn("톤릿를", out)
        self.assertIn("톤릿로서", out)
        self.assertIn("헤이즈은", out)
        self.assertIn("서울으로", out)
        self.assertNotIn("톤릿은 사진", out)
        self.assertNotIn("'서울로 가요", out.split("서울으로")[0][-30:])
        self.assertEqual(out.count("Korean particle"), 4)

    def test_latin_brand_needs_a_reading(self):
        code, out = self.check({"a": {"localizations": {"ko": unit("Tonlit를 열어요")}}}, "--brand", "Tonlit=톤릿")
        self.assertEqual(code, 1)
        self.assertIn("Tonlit를", out)
        code, out = self.check({"a": {"localizations": {"ko": unit("x")}}}, "--brand", "Tonlit")
        self.assertIn("give the Korean reading", out)

    def test_titles_without_terminal_punctuation(self):
        titles = self.dir / "titles.txt"
        titles.write_text("Saved photos\nHow it works\n", encoding="utf-8")
        code, out = self.check({
            "Saved photos": {"localizations": {"ko": unit("저장한 사진"), "ja": unit("保存した写真。")}},
            "How it works": {"localizations": {"ko": unit("작동 방식"), "ja": unit("しくみ")}},
        }, "--titles", str(titles))
        self.assertEqual(code, 1)
        self.assertIn("[ja] title ends with punctuation: 保存した写真。", out)

    def test_forbid_and_only_in(self):
        code, out = self.check({
            "Shade 21": {"localizations": {"ko": unit("21호"), "ja": unit("21호")}},
            "Old": {"localizations": {"ko": unit("Haze로 저장"), "ja": unit("保存")}},
        }, "--forbid", r"(?<![A-Za-z])Haze(?![A-Za-z])", "--only-in", "ko:호")
        self.assertEqual(code, 1)
        self.assertIn("[ja] '호' outside ko", out)
        self.assertNotIn("[ko] '호'", out)
        self.assertIn("[ko] forbidden", out)

    def test_duplicate_json_keys_fail(self):
        raw = '{"sourceLanguage":"en","strings":{"Save":{},"Save":{}}}'
        code, out = self.check(None, raw=raw)
        self.assertEqual(code, 1)
        self.assertIn("duplicate JSON key: Save", out)

    def test_review_state_and_stale_are_warnings(self):
        strings = {
            "Save": {"localizations": {"ko": unit("저장", state="needs_review")}},
            "Gone": {"extractionState": "stale", "localizations": {"ko": unit("사라짐")}},
        }
        code, out = self.check(strings)
        self.assertEqual(code, 0, out)
        self.assertIn("WARN", out)
        code, _ = self.check(strings, "--strict")
        self.assertEqual(code, 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
