#!/usr/bin/env python3
"""시험용 라벨 PNG(투명 바탕 + 검은 글자·선)를 만든다. 실제 제품 라벨은 사람이 준비한다.

실제 라벨 만들기: 공식 정면 사진에서 글자 위치·크기를 재서 HTML/SVG로 다시 조판하고 투명 PNG로 뽑는다.
  라벨 텍스처는 최종 화면에서 가장 작은 글자 줄이 2,000px 이상 되게 (매크로 컷이면 2배 판을 따로).
  글자는 실제 제품과 철자·줄 배치·구분선까지 같아야 한다. 다르면 쓰지 않는다.

사용법: python3 make_label_placeholder.py <out.png> [--size 1024]
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pngio import Canvas  # noqa: E402


def make(out, size):
    c = Canvas(size, size, (0, 0, 0, 0), channels=4)
    ink = (10, 10, 12, 255)
    s = max(1, size // 200)   # 정면 투영은 가장자리가 눌리므로 글자는 가운데 60% 폭 안에 둔다
    rows = [("SAMPLE", s * 3), ("TEST BOTTLE", s * 3 // 2), ("", 0), ("PLACEHOLDER LABEL", s), ("NOT A REAL PRODUCT", s), ("", 0), ("50 ML", s)]
    y = size // 5
    for text, sc in rows:
        if not text:
            c.fill_rect(size * 0.3, y + s * 2, size * 0.4, max(1, s // 2), ink)   # 구분선
            y += s * 6
            continue
        w = Canvas.text_width(text, sc)
        c.text((size - w) // 2, y, text, sc, ink)
        y += 7 * sc + s * 5
    c.save(out)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--size", type=int, default=1024)
    a = ap.parse_args()
    make(a.out, a.size)
    print(f"→ {a.out}")
