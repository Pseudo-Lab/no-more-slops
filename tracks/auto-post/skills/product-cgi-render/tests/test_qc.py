"""qc.py를 합성 이미지·영상으로 시험한다: 255 픽셀, 같은 세계 평균색, 루프 이음매, 하이라이트."""
import json
import os
import shutil
import tempfile
import unittest

from _util import Canvas, ff, run_py, solid_png


class QCTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = tempfile.mkdtemp(prefix="qc-")
        d = cls.d
        cls.clean = os.path.join(d, "clean.png")
        solid_png(cls.clean, 108, 192, (200, 215, 230))
        c = Canvas(108, 192, (200, 215, 230))
        c.fill_rect(10, 10, 3, 2, (255, 255, 255))           # 순수 흰 6픽셀
        c.fill_rect(30, 30, 2, 2, (255, 255, 254))           # 거의 흰색은 세지 않는다
        cls.white = os.path.join(d, "white.png")
        c.save(cls.white)
        cls.near = os.path.join(d, "near.png")
        solid_png(cls.near, 108, 192, (205, 220, 236))       # 기준과 최대 6 차이
        cls.far = os.path.join(d, "far.png")
        solid_png(cls.far, 108, 192, (200, 215, 250))        # 파랑 20 차이
        # 프레임 폴더 (3장, 가운데에만 흰 점)
        cls.frames = os.path.join(d, "frames")
        os.makedirs(cls.frames)
        for i in range(3):
            (Canvas(108, 192, (200, 215, 230)) if i != 1 else c).save(os.path.join(cls.frames, f"f{i:04d}.png"))
        # 영상: 첫 프레임 A색 → 마지막 프레임 B색
        for name, last in (("loop_ok", (202, 216, 231)), ("loop_bad", (150, 160, 170))):
            fd = os.path.join(d, name)
            os.makedirs(fd)
            for i in range(10):
                solid_png(os.path.join(fd, f"f{i:04d}.png"), 108, 192, (200, 215, 230) if i < 9 else last)
            ff("-framerate", 30, "-i", os.path.join(fd, "f%04d.png"), "-c:v", "libx264", "-pix_fmt", "yuv444p", "-crf", 0, os.path.join(d, name + ".mp4"))
        # 하이라이트: 점 하나 / 점 둘 / 큰 덩어리
        for name, dots in (("hl_one", [(50, 90, 4)]), ("hl_two", [(30, 90, 4), (70, 90, 4)]), ("hl_big", [(40, 70, 30)])):
            cv = Canvas(108, 192, (120, 140, 160))
            for x, y, s in dots:
                cv.fill_rect(x, y, s, s, (252, 252, 252))
            cv.save(os.path.join(d, name + ".png"))

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.d, ignore_errors=True)

    def test_white_pass_fail(self):
        code, out = run_py("qc.py", "white", self.clean, check=False)
        self.assertEqual(code, 0, out)
        code, out = run_py("qc.py", "white", self.white, "--json", check=False)
        self.assertEqual(code, 1)
        self.assertEqual(json.loads(out)[0]["white255_total"], 6)

    def test_white_frame_dir(self):
        code, out = run_py("qc.py", "white", self.frames, "--json", check=False)
        r = json.loads(out)[0]
        self.assertEqual((code, r["frames"], r["worst_frame"], r["white255_total"]), (1, 3, 1, 6))

    def test_means(self):
        code, out = run_py("qc.py", "means", self.near, "--ref", self.clean, check=False)
        self.assertEqual(code, 0, out)
        self.assertIn("PASS", out)
        code, out = run_py("qc.py", "means", self.near, self.far, "--ref", self.clean, "--json", check=False)
        self.assertEqual(code, 1)
        r = json.loads(out)
        self.assertEqual([x["pass"] for x in r], [True, False])
        self.assertAlmostEqual(r[1]["max_diff"], 20, delta=0.5)

    def test_loop(self):
        code, out = run_py("qc.py", "loop", os.path.join(self.d, "loop_ok.mp4"), check=False)
        self.assertEqual(code, 0, out)
        code, out = run_py("qc.py", "loop", os.path.join(self.d, "loop_bad.mp4"), check=False)
        self.assertEqual(code, 1, out)
        code, out = run_py("qc.py", "loop", os.path.join(self.d, "loop_bad.mp4"), "--next", os.path.join(self.d, "loop_bad.mp4"), "--tol", "100", check=False)
        self.assertEqual(code, 0, out)

    def test_highlight(self):
        roi = "0,40,108,120"
        self.assertEqual(run_py("qc.py", "highlight", os.path.join(self.d, "hl_one.png"), "--roi", roi, check=False)[0], 0)
        self.assertEqual(run_py("qc.py", "highlight", os.path.join(self.d, "hl_two.png"), "--roi", roi, check=False)[0], 1)
        code, out = run_py("qc.py", "highlight", os.path.join(self.d, "hl_big.png"), "--roi", roi, "--json", check=False)
        self.assertEqual(code, 1)
        self.assertEqual(json.loads(out)[0]["largest_diam_px"], 30)


if __name__ == "__main__":
    unittest.main()
