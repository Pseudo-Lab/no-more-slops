"""cgi_config: 단면 계산, 키 보간, 프레임 범위 (bpy 없이)."""
import json
import os
import tempfile
import unittest

from _util import ASSETS  # noqa: F401  (경로 설정)
from cgi_config import Config, bottle_surfaces, cut_frames, inner_offset, interp, parse_frames, r_at, split_inner


class ProfileTest(unittest.TestCase):
    def test_inner_offset_cylinder(self):
        outer = [(0, 0), (0.5, 0), (0.5, 1.0), (0.3, 1.2)]
        inner = inner_offset(outer, wall=0.05, base=0.08)
        self.assertEqual(inner[-1], (0.0, 0.08))           # 축 바닥 = base 두께
        r_mid = r_at(list(reversed(inner)), 0.5)
        self.assertAlmostEqual(r_mid, 0.45, places=3)       # 곧은 벽 = 반지름 - wall
        self.assertTrue(all(z >= 0.08 for _, z in inner))

    def test_split_and_surfaces(self):
        with open(os.path.join(ASSETS, "test-bottle.json"), encoding="utf-8") as f:
            b = json.load(f)["bottle"]
        s = bottle_surfaces(b)
        self.assertEqual(s["level"], 1.80)
        self.assertEqual(s["top"][0], (0.0, 1.80))
        self.assertAlmostEqual(s["glass"][-1][1], 1.80)     # 유리 면은 액체 높이에서 끝난다
        self.assertEqual(s["wet"][0][0], 0.0)               # 유리↔액체 면은 축에서 시작
        self.assertAlmostEqual(s["wet"][-1][1], 1.80)
        self.assertAlmostEqual(s["wet"][-1][0], s["top"][1][0])
        with self.assertRaises(ValueError):
            split_inner(s["inner"], 99)

    def test_empty_bottle(self):
        s = bottle_surfaces({"outer": [(0, 0), (0.5, 0), (0.5, 1)], "wall": 0.05})
        self.assertIsNone(s["wet"])


class KeysTest(unittest.TestCase):
    keys = [{"f": 0, "yaw": -180, "target": [0, 0, 1]}, {"f": 10, "yaw": 0, "ease": "linear", "target": [0, 0, 2]}, {"f": 20, "dist": 5}]

    def test_interp(self):
        self.assertEqual(interp(self.keys, -5, "yaw"), -180)
        self.assertAlmostEqual(interp(self.keys, 5, "yaw"), -90)
        self.assertEqual(interp(self.keys, 15, "yaw"), 0)
        self.assertEqual(interp(self.keys, 5, "dist", 12), 5)       # 키 하나뿐이면 그 값
        self.assertEqual(interp(self.keys, 5, "fov", 26), 26)       # 없으면 기본값
        t = interp(self.keys, 5, "target")
        self.assertAlmostEqual(t[2], 1.5)                           # 리스트는 성분별 보간

    def test_parse_frames(self):
        self.assertEqual(parse_frames("", 3), [0, 1, 2])
        self.assertEqual(parse_frames("0-2,9", 5), [0, 1, 2])
        self.assertEqual(parse_frames("0,15,29", 30), [0, 15, 29])

    def test_config_paths(self):
        cfg = Config(os.path.join(ASSETS, "example-project.json"))
        self.assertEqual(cfg.product["name"], "generic-dropper-bottle")
        self.assertEqual(cut_frames(cfg.cut("c01"), cfg.fps), 45)
        self.assertEqual(cfg.look["liquid"]["ior"], 1.34)            # 기본값 유지
        self.assertEqual(cfg.look["render"]["persistent_data"], False)
        with self.assertRaises(KeyError):
            cfg.cut("nope")
        d = tempfile.mkdtemp()
        p = os.path.join(d, "p.json")
        with open(p, "w") as f:
            json.dump({"product": {"bottle": {"outer": [[0, 0], [1, 0], [1, 1]]}}, "cuts": []}, f)
        self.assertEqual(Config(p).size, (1080, 1920))


if __name__ == "__main__":
    unittest.main()
