"""overlay.mjs + assets/overlay-type-a.html (선택): Chrome·Node·puppeteer-core가 있을 때만 돈다.
puppeteer-core: 스킬 폴더에서 `npm install`, 또는 PUPPETEER_CORE_DIR=<node_modules가 있는 폴더>."""
import os
import shutil
import subprocess
import tempfile
import unittest

from _util import ASSETS, SCRIPTS, SKILL

CHROMES = [os.environ.get("CHROME_PATH", ""), "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
           "/usr/bin/google-chrome", "/usr/bin/chromium", "/usr/bin/chromium-browser"]


def available():
    if not shutil.which("node"):
        return "node 없음"
    if not any(c and os.path.exists(c) for c in CHROMES):
        return "Chrome 없음"
    if not (os.path.isdir(os.path.join(SKILL, "node_modules", "puppeteer-core")) or os.environ.get("PUPPETEER_CORE_DIR")):
        return "puppeteer-core 없음 (npm install 또는 PUPPETEER_CORE_DIR)"
    return None


@unittest.skipIf(available(), available() or "")
class OverlayTest(unittest.TestCase):
    def test_frames_with_alpha(self):
        d = tempfile.mkdtemp(prefix="ov-")
        try:
            r = subprocess.run(["node", os.path.join(SCRIPTS, "overlay.mjs"), os.path.join(ASSETS, "overlay-type-a.html"), d,
                                "--seconds", "0.5", "--size", "270x480", "--root", SKILL,
                                "--query", "text=TEST|TWO&kicker=KICK&size=40&y=100&dur=0.5&t0=0.05"],
                               capture_output=True, text=True, timeout=120)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            files = sorted(os.listdir(d))
            self.assertEqual(len(files), 15)
            def opaque(f):  # 알파 > 0 픽셀 수
                raw = subprocess.run(["ffmpeg", "-v", "error", "-i", os.path.join(d, f), "-f", "rawvideo", "-pix_fmt", "rgba", "-"],
                                     capture_output=True, check=True).stdout
                return sum(1 for a in raw[3::4] if a)
            self.assertEqual(opaque("o0000.png"), 0)          # t0 전에는 비어 있다 (투명 배경)
            self.assertGreater(opaque("o0008.png"), 200)      # 등장 뒤에는 글자가 있다
            self.assertLess(opaque("o0014.png"), opaque("o0008.png") + 1)
        finally:
            shutil.rmtree(d, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
