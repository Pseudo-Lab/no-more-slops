"""compose_cut.py + make_grade.py: 프레임 → mp4, 채널 상한으로 255 픽셀 0개, 미리보기 표시 전달."""
import json
import os
import shutil
import tempfile
import unittest

from _util import Canvas, probe, run_py


class ComposeTest(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp(prefix="cmp-")
        self.frames = os.path.join(self.d, "frames")
        os.makedirs(self.frames)
        for i in range(6):
            c = Canvas(180, 320, (210, 225, 238))
            c.fill_rect(60, 100 + i * 4, 40, 40, (255, 255, 255))      # 완전한 흰 덩어리 (번짐 흉내)
            c.save(os.path.join(self.frames, f"f{i:04d}.png"))
        with open(os.path.join(self.frames, "render.json"), "w") as f:
            json.dump({"preview": True, "samples": 8}, f)

    def tearDown(self):
        shutil.rmtree(self.d, ignore_errors=True)

    def test_cap_grade_preview(self):
        grade = os.path.join(self.d, "grade.png")
        run_py("make_grade.py", grade, "--size", "180x320")
        out = os.path.join(self.d, "cuts", "c01.mp4")
        code, txt = run_py("compose_cut.py", self.frames, out, "--size", "180x320", "--grade", grade, "--grain", "4", "--cap", "240")
        self.assertIn("6프레임", txt)
        self.assertTrue(os.path.exists(os.path.join(self.d, "cuts", "c01-sheet.png")))
        with open(out + ".render.json") as f:
            meta = json.load(f)
        self.assertTrue(meta["preview"])                                  # 렌더 단계의 미리보기 표시가 따라온다
        code, txt = run_py("qc.py", "white", out, check=False)
        self.assertEqual(code, 0, txt)                                    # 상한 덕에 디코드 뒤에도 255 없음
        code, txt = run_py("qc.py", "white", self.frames, check=False)
        self.assertEqual(code, 1)                                         # 원본 프레임에는 있었다
        self.assertEqual(probe(out, "stream=width,height"), "180,320")


if __name__ == "__main__":
    unittest.main()
