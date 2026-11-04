"""assemble.py: 컷 목록 순서 조립, 없는 컷은 자리 표시, 미리보기 컷 처리 (Blender 없이)."""
import json
import os
import shutil
import tempfile
import unittest

from _util import color_clip, probe, run_py


class AssembleTest(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp(prefix="asm-")
        os.makedirs(os.path.join(self.d, "cuts"))
        color_clip(os.path.join(self.d, "cuts", "c01.mp4"), 180, 320, 1.0, tone=440)       # 완성 컷 (소리 있음, 1.0초 → 0.8초로 잘림)
        color_clip(os.path.join(self.d, "cuts", "c03.mp4"), 180, 320, 0.5, "0x203040")    # 미리보기 컷 (소리 없음, 짧으면 마지막 프레임 유지)
        with open(os.path.join(self.d, "cuts", "c03.mp4.render.json"), "w") as f:
            json.dump({"preview": True, "samples": 12}, f)
        self.cfg = os.path.join(self.d, "project.json")
        with open(self.cfg, "w", encoding="utf-8") as f:
            json.dump({"fps": 30, "size": [1080, 1920], "cuts": [
                {"id": "c01", "duration": 0.8, "desc": "hook drop"},
                {"id": "c02", "duration": 0.6, "desc": "아직 없는 컷 (label macro)"},
                {"id": "c03", "duration": 0.9, "desc": "preview cut"}]}, f, ensure_ascii=False)

    def tearDown(self):
        shutil.rmtree(self.d, ignore_errors=True)

    def test_dry_run(self):
        code, out = run_py("assemble.py", "--config", self.cfg, "--dry-run")
        self.assertEqual(code, 0)
        self.assertIn("| 1 | c01 | 0.80 | 0.00 | final |", out)
        self.assertIn("| 2 | c02 | 0.60 | 0.80 | placeholder |", out)
        self.assertIn("placeholder(preview)", out)                     # 미리보기 컷은 기본으로 빠진다
        self.assertIn("합계 2.30초", out)
        self.assertIn("최종 아님", out)
        self.assertFalse(os.path.exists(os.path.join(self.d, "video")))

    def test_assemble_with_placeholders(self):
        out = os.path.join(self.d, "video", "a.mp4")
        run_py("assemble.py", "--config", self.cfg, "--out", out, "--size", "180x320", "--placeholder", "bitmap")
        self.assertAlmostEqual(float(probe(out)), 2.3, delta=0.1)
        self.assertEqual(probe(out, "stream=codec_type").split(), ["video", "audio"])
        self.assertEqual(probe(out, "stream=width,height").split()[0], "180,320")
        with open(os.path.join(self.d, "video", "a.json"), encoding="utf-8") as f:
            meta = json.load(f)
        self.assertFalse(meta["final"])
        self.assertEqual([c["state"] for c in meta["cuts"]], ["final", "placeholder", "placeholder(preview)"])

    def test_allow_preview_and_audio(self):
        mix = os.path.join(self.d, "mix.wav")
        from _util import ff
        ff("-f", "lavfi", "-i", "sine=frequency=880:sample_rate=48000:duration=1.0", mix)   # 조립본보다 짧은 믹스 → 무음으로 채움
        out = os.path.join(self.d, "b.mp4")
        code, txt = run_py("assemble.py", "--config", self.cfg, "--out", out, "--size", "180x320", "--placeholder", "bitmap",
                           "--allow-preview", "--audio", mix)
        self.assertIn("| 3 | c03 | 0.90 | 1.40 | preview |", txt)
        self.assertAlmostEqual(float(probe(out)), 2.3, delta=0.1)


if __name__ == "__main__":
    unittest.main()
