#!/usr/bin/env python3
"""아래 그레이드 PNG를 만든다: 화면 아래 일부를 한 색으로 아주 조금 덮는 투명 PNG (전 컷 공통 마감).
Blender 컷, AI 영상 컷, 코드 그래픽 컷에 같은 PNG를 얹어야 한 세계로 보인다 (compose_cut.py --grade).

사용법:
  python3 make_grade.py <out.png> [--size 1080x1920] [--color 26,42,60] [--fraction 0.25] [--alpha 24]
    color: 덮는 색 (0~255), fraction: 아래에서 몇 % 높이까지, alpha: 맨 아래 알파 (0~255, 위로 갈수록 0)
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pngio import write_png  # noqa: E402


def make(out, w, h, color, fraction, alpha):
    data = bytearray()
    top = h * (1 - fraction)
    for y in range(h):
        t = 0.0 if y < top else (y - top) / max(1.0, h - top)
        t = t * t * (3 - 2 * t)                     # 부드러운 시작
        a = int(round(alpha * t))
        data += bytes((*color, a)) * w
    write_png(out, w, h, bytes(data), 4)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("out")
    p.add_argument("--size", default="1080x1920")
    p.add_argument("--color", default="26,42,60")
    p.add_argument("--fraction", type=float, default=0.25)
    p.add_argument("--alpha", type=int, default=24)
    a = p.parse_args(argv)
    w, h = (int(v) for v in a.size.split("x"))
    make(a.out, w, h, tuple(int(v) for v in a.color.split(",")), a.fraction, a.alpha)
    print(f"→ {a.out}")


if __name__ == "__main__":
    main()
