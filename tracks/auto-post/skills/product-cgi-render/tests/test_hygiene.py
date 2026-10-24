"""공개 저장소용 위생 검사: 절대 경로·비밀 값이 없고, JSON 자산이 유효하고, SKILL.md 머리말이 폴더 이름과 맞는다."""
import json
import os
import re
import unittest

from _util import SKILL

TEXT_EXT = {".py", ".mjs", ".js", ".sh", ".html", ".json", ".md"}


def files():
    for root, dirs, fs in os.walk(SKILL):
        dirs[:] = [d for d in dirs if d not in ("node_modules", "__pycache__", ".git")]
        for f in fs:
            if os.path.splitext(f)[1] in TEXT_EXT:
                yield os.path.join(root, f)


class HygieneTest(unittest.TestCase):
    def test_no_absolute_user_paths(self):
        bad = []
        pat = re.compile(r"(/Users/[A-Za-z]|/home/[a-z]|C:\\\\Users)")
        for p in files():
            if os.path.basename(p) == "test_hygiene.py":
                continue
            with open(p, encoding="utf-8") as f:
                for i, line in enumerate(f, 1):
                    if pat.search(line):
                        bad.append(f"{os.path.relpath(p, SKILL)}:{i}")
        self.assertEqual(bad, [])

    def test_no_secrets(self):
        pat = re.compile(r"(sk-[A-Za-z0-9]{20,}|api[_-]?key\s*[:=]\s*['\"][^'\"]+)", re.I)
        for p in files():
            with open(p, encoding="utf-8") as f:
                self.assertIsNone(pat.search(f.read()), p)

    def test_json_assets(self):
        for p in files():
            if p.endswith(".json"):
                with open(p, encoding="utf-8") as f:
                    json.load(f)

    def test_skill_frontmatter(self):
        with open(os.path.join(SKILL, "SKILL.md"), encoding="utf-8") as f:
            text = f.read()
        m = re.match(r"\A---\s*\n(.*?)\n---", text, re.S)
        self.assertIsNotNone(m)
        name = re.search(r"^name:\s*(\S+)", m.group(1), re.M).group(1)
        self.assertEqual(name, os.path.basename(SKILL))
        self.assertRegex(m.group(1), r"(?m)^description:\s*\S")


if __name__ == "__main__":
    unittest.main()
