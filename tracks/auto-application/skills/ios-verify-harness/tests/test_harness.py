"""Checks noop_audit.py on synthetic renders and the shell scripts in dry-run mode.

usage: python3 tests/test_harness.py   (needs Pillow; the shell checks need bash)
"""
import pathlib
import random
import subprocess
import sys
import tempfile
import unittest

from PIL import Image, ImageDraw

SCRIPTS = pathlib.Path(__file__).resolve().parents[1] / "scripts"


class NoopAuditTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix="noop-audit-test-")
        self.addCleanup(temp.cleanup)
        self.dir = pathlib.Path(temp.name)
        self.base = Image.new("RGB", (400, 500), (180, 150, 130))
        ImageDraw.Draw(self.base).ellipse((120, 80, 280, 280), fill=(200, 160, 140))
        self.base.save(self.dir / "baseline.png")

    def render(self, name, edit):
        image = self.base.copy()
        edit(image)
        image.save(self.dir / f"{name}.png")

    def audit(self, *options):
        result = subprocess.run([sys.executable, str(SCRIPTS / "noop_audit.py"), str(self.dir), *options],
                                capture_output=True, text=True)
        return result.returncode, result.stdout + result.stderr

    def test_classifies_tools(self):
        self.render("lips", lambda im: ImageDraw.Draw(im).rectangle((170, 220, 230, 240), fill=(200, 60, 80)))
        self.render("nose", lambda im: None)

        def noise(im):
            rng = random.Random(1)
            px = im.load()
            for i in rng.sample(range(im.width * im.height), 4000):  # +2 on distinct pixels: compression-level noise
                x, y = i % im.width, i // im.width
                r, g, b = px[x, y]
                px[x, y] = (r + 2, g, b)
        self.render("redness", noise)

        def tint(im):
            px = im.load()
            for y in range(im.height):
                for x in range(im.width):
                    r, g, b = px[x, y]
                    px[x, y] = (r + 10, g, b)
        self.render("undertone", tint)
        code, out = self.audit()
        self.assertEqual(code, 1, out)
        lines = {line.split()[1].rstrip(":"): line.split()[0] for line in out.splitlines() if line[:5].strip() in {"OK", "NO-OP", "WEAK"}}
        self.assertEqual(lines, {"lips": "OK", "nose": "NO-OP", "redness": "NO-OP", "undertone": "WEAK"})
        self.assertIn("box (170, 220, 231, 241)", out)
        self.assertTrue((self.dir / "audit-sheet.jpg").exists())

    def test_weak_passes_unless_strict(self):
        self.render("glow", lambda im: ImageDraw.Draw(im).rectangle((100, 100, 300, 300), fill=(190, 158, 138)))
        code, out = self.audit()
        self.assertEqual(code, 0, out)
        self.assertIn("WEAK  glow", out)
        self.assertEqual(self.audit("--strict")[0], 1)

    def test_size_mismatch_fails(self):
        Image.new("RGB", (200, 200)).save(self.dir / "crop.png")
        code, out = self.audit("--sheet", "")
        self.assertEqual(code, 1)
        self.assertIn("FAIL crop: size", out)


class ShellScriptTests(unittest.TestCase):
    def dry(self, script, *args):
        return subprocess.run(["bash", str(SCRIPTS / script), *args, "-n"], capture_output=True, text=True, check=True).stdout

    def test_sim_check_dry_run(self):
        out = self.dry("sim_check.sh", "-p", "App.xcodeproj", "-s", "App", "-b", "com.example.app", "-l", "en de", "-a", "-selfCheck -acceptTerms")
        self.assertIn("platform=iOS\\ Simulator\\,name=iPhone\\ 17\\ Pro", out)
        self.assertIn("simctl launch booted com.example.app -selfCheck -acceptTerms -AppleLanguages \\(de\\)", out)
        self.assertEqual(out.count("# wait for DONE"), 2)

    def test_device_run_dry_run(self):
        out = self.dry("device_run.sh", "-p", "App.xcodeproj", "-s", "App", "-b", "com.example.app", "-d", "DEV",
                       "-a", "-perfReport", "-f", "Documents/perf.txt", "-o", "out")
        self.assertIn("process launch --device DEV --terminate-existing com.example.app -- -perfReport", out)
        self.assertIn("copy from --device DEV --domain-type appDataContainer --domain-identifier com.example.app --source Documents/perf.txt", out)

    def test_missing_arguments_exit_2(self):
        for script in ("sim_check.sh", "device_run.sh"):
            result = subprocess.run(["bash", str(SCRIPTS / script), "-s", "App", "-n"], capture_output=True, text=True)
            self.assertEqual(result.returncode, 2, script)


if __name__ == "__main__":
    unittest.main(verbosity=2)
