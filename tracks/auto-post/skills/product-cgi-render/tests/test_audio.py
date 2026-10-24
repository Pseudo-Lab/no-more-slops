"""audio.py: 시각에 맞춘 효과음 믹스, 루프 꼬리, 음량 정규화, 라이선스 확인."""
import array
import json
import os
import shutil
import subprocess
import tempfile
import unittest

from _util import ff, probe, run_py


def rms_window(path, t0, t1):
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ss", str(t0), "-to", str(t1), "-ac", "1", "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    a = array.array("h", pcm)
    return (sum(x * x for x in a) / max(1, len(a))) ** 0.5


class AudioTest(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp(prefix="aud-")
        os.makedirs(os.path.join(self.d, "sfx"))
        ff("-f", "lavfi", "-i", "sine=frequency=1200:sample_rate=48000:duration=0.12", os.path.join(self.d, "sfx", "tap.wav"))
        ff("-f", "lavfi", "-i", "sine=frequency=2400:sample_rate=48000:duration=0.6", os.path.join(self.d, "sfx", "ting.wav"))
        self.cfg = os.path.join(self.d, "project.json")
        self.write({"normalize": "loudness", "lufs": -16, "true_peak": -1.5, "loop_tail": True, "sfx": [
            {"file": "sfx/tap.wav", "at": 0.5, "gain_db": -3, "fade_in": 0.002, "fade_out": 0.01, "license": "own"},
            {"file": "sfx/ting.wav", "at": 1.7, "gain_db": -6, "fade_out": 0.2, "license": "CC0"}]})

    def write(self, audio):
        with open(self.cfg, "w") as f:
            json.dump({"cuts": [{"id": "c01", "duration": 1.0}, {"id": "c02", "duration": 1.0}], "audio": audio}, f)

    def tearDown(self):
        shutil.rmtree(self.d, ignore_errors=True)

    def test_mix_loop_tail_and_loudness(self):
        out = os.path.join(self.d, "audio", "mix.wav")
        code, txt = run_py("audio.py", "--config", self.cfg)
        self.assertAlmostEqual(float(probe(out)), 2.0, delta=0.02)          # 컷 합계 길이
        self.assertGreater(rms_window(out, 0.5, 0.6), 500)                  # 0.5초 톡
        self.assertLess(rms_window(out, 0.8, 1.6), 50)                      # 사이는 조용
        self.assertGreater(rms_window(out, 0.0, 0.2), 200)                  # 2.0초를 넘은 팅 꼬리가 0초에 겹쳤다
        self.assertIn("LUFS", txt)

    def test_mux(self):
        from _util import color_clip
        v = os.path.join(self.d, "v.mp4")
        color_clip(v, 180, 320, 2.0)
        run_py("audio.py", "--config", self.cfg, "--mux", v)
        self.assertEqual(probe(os.path.join(self.d, "v-sfx.mp4"), "stream=codec_type").split(), ["video", "audio"])

    def test_license_refused(self):
        self.write({"sfx": [{"file": "sfx/tap.wav", "at": 0.1, "license": "CC-BY-NC"}]})
        code, txt = run_py("audio.py", "--config", self.cfg, check=False)
        self.assertNotEqual(code, 0)
        self.assertIn("CC0 또는 own", txt)


if __name__ == "__main__":
    unittest.main()
