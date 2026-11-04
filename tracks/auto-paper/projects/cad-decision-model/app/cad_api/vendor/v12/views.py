"""Renderers for Jev judgements: crop, upscale to Jev's image limits, draw overlays.

All boxes are (x0, y0, x1, y1), inclusive full-resolution page pixels.
Same drawing rules as docs/prototype/views.py (used by the smoke test), plus margin caps for large symbols.
"""
from __future__ import annotations

import cv2
import numpy as np

JEV_MIN_SIDE, JEV_MAX_SIDE, JEV_MIN_PIXELS, JEV_MAX_PIXELS = 280, 1568, 78_400, 2_458_624
RED = (0, 0, 230)
GRAY = (150, 150, 150)
PALETTE = [(0, 140, 255), (0, 160, 0), (230, 80, 0), (200, 0, 200), (0, 110, 160), (120, 60, 200)]
COLOR_NAMES = ["orange", "green", "blue", "magenta", "brown", "purple"]  # same order as PALETTE (BGR)
EDGES = ("top", "bottom", "left", "right")


def load_page(path) -> np.ndarray:
    img = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(path)
    return img


def wh(b):
    return b[2] - b[0] + 1, b[3] - b[1] + 1


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def crop(page, x0, y0, x1, y1):
    """Crop [x0, x1) x [y0, y1) with white padding outside the page."""
    x0, y0, x1, y1 = int(round(x0)), int(round(y0)), int(round(x1)), int(round(y1))
    h, w = page.shape[:2]
    out = np.full((y1 - y0, x1 - x0), 255, np.uint8)
    sx0, sy0, sx1, sy1 = max(x0, 0), max(y0, 0), min(x1, w), min(y1, h)
    if sx1 > sx0 and sy1 > sy0:
        out[sy0 - y0:sy1 - y0, sx0 - x0:sx1 - x0] = page[sy0:sy1, sx0:sx1]
    return out


def scale_for_jev(w, h, target_min=448):
    s = target_min / min(w, h)
    s = min(s, JEV_MAX_SIDE / max(w, h))
    if w * h * s * s > JEV_MAX_PIXELS:
        s = (JEV_MAX_PIXELS / (w * h)) ** 0.5
    return s


def pad_aspect(img, max_ratio=JEV_MAX_SIDE / JEV_MIN_SIDE * 0.9):
    h, w = img.shape[:2]
    if max(w, h) / min(w, h) <= max_ratio:
        return img
    if w > h:
        nh = int(np.ceil(w / max_ratio)); top = (nh - h) // 2
        out = np.full((nh, w, 3), 255, np.uint8); out[top:top + h] = img
    else:
        nw = int(np.ceil(h / max_ratio)); left = (nw - w) // 2
        out = np.full((h, nw, 3), 255, np.uint8); out[:, left:left + w] = img
    return out


def dashed_line(img, a, b, color, t=1, dash=8):
    a, b = np.array(a, float), np.array(b, float)
    n = max(int(np.linalg.norm(b - a) / dash), 1)
    for i in range(0, n, 2):
        p = a + (b - a) * i / n
        q = a + (b - a) * min(i + 1, n) / n
        cv2.line(img, tuple(map(int, p)), tuple(map(int, q)), color, t)


class View:
    def __init__(self, page, rect, target_min=448):
        self.rect = tuple(int(round(v)) for v in rect)
        x0, y0, x1, y1 = self.rect
        g = crop(page, x0, y0, x1, y1)
        self.s = scale_for_jev(x1 - x0, y1 - y0, target_min)
        size = (max(1, round((x1 - x0) * self.s)), max(1, round((y1 - y0) * self.s)))
        g = cv2.resize(g, size, interpolation=cv2.INTER_AREA if self.s < 1 else cv2.INTER_CUBIC)
        self.img = cv2.cvtColor(g, cv2.COLOR_GRAY2BGR)

    def p(self, x, y):
        return (round((x - self.rect[0]) * self.s), round((y - self.rect[1]) * self.s))

    def box(self, b, color, t=2, dashed=False):
        x0, y0 = self.p(b[0] - 0.5, b[1] - 0.5)
        x1, y1 = self.p(b[2] + 0.5, b[3] + 0.5)
        if not dashed:
            cv2.rectangle(self.img, (x0, y0), (x1, y1), color, t)
        else:
            for a, c in [((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)), ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0))]:
                dashed_line(self.img, a, c, color, t)

    def hline(self, y, xa, xb, color, t=2):
        cv2.line(self.img, self.p(xa, y), self.p(xb, y), color, t)

    def vline(self, x, ya, yb, color, t=2):
        cv2.line(self.img, self.p(x, ya), self.p(x, yb), color, t)

    def label(self, text, xy, color, scale=1.0):
        cv2.putText(self.img, text, xy, cv2.FONT_HERSHEY_SIMPLEX, scale, (255, 255, 255), 4, cv2.LINE_AA)
        cv2.putText(self.img, text, xy, cv2.FONT_HERSHEY_SIMPLEX, scale, color, 2, cv2.LINE_AA)

    def finish(self):
        """Fit Jev's limits even after extra margins were added: shrink if too big, pad if too thin."""
        img = self.img
        h, w = img.shape[:2]
        f = min(1.0, JEV_MAX_SIDE / max(w, h), (JEV_MAX_PIXELS / (w * h)) ** 0.5)
        if f < 1.0:
            img = cv2.resize(img, (int(w * f), int(h * f)), interpolation=cv2.INTER_AREA)
        img = pad_aspect(img)
        h, w = img.shape[:2]
        if min(w, h) < JEV_MIN_SIDE:
            out = np.full((max(h, JEV_MIN_SIDE), max(w, JEV_MIN_SIDE), 3), 255, np.uint8)
            out[:h, :w] = img
            img = out
            h, w = img.shape[:2]
        assert JEV_MIN_SIDE <= min(w, h) and max(w, h) <= JEV_MAX_SIDE and JEV_MIN_PIXELS <= w * h <= JEV_MAX_PIXELS, (w, h)
        return img


def edge_line(v: View, b, edge, color=RED, t=3):
    """Draw the line of `edge` of box b just outside the boundary pixels (same as the smoke test)."""
    if edge == "top":
        v.hline(b[1] - 0.5, b[0] - 0.5, b[2] + 0.5, color, t)
    elif edge == "bottom":
        v.hline(b[3] + 0.5, b[0] - 0.5, b[2] + 0.5, color, t)
    elif edge == "left":
        v.vline(b[0] - 0.5, b[1] - 0.5, b[3] + 0.5, color, t)
    else:
        v.vline(b[2] + 0.5, b[1] - 0.5, b[3] + 0.5, color, t)


# ----------------------------------------------------------------------------- views

def context_view(page, b, margin=0.8, mmin=40, mmax=160):
    w, h = wh(b)
    m = int(clamp(margin * max(w, h), mmin, mmax))
    v = View(page, (b[0] - m, b[1] - m, b[2] + m + 1, b[3] + m + 1))
    v.box(b, RED, 2)
    return v.finish()


def edge_view(page, b, edge, reach=0.7, rmin=40, rmax=160, side=0.35, smin=30, smax=120):
    """Band around one edge: that edge bold red, the rest of the box thin dashed red."""
    w, h = wh(b)
    if edge in ("top", "bottom"):
        d = int(clamp(reach * h, rmin, rmax)); mx = int(clamp(side * w, smin, smax))
        y = b[1] if edge == "top" else b[3]
        rect = (b[0] - mx, y - d, b[2] + mx + 1, y + d + 1)
    else:
        d = int(clamp(reach * w, rmin, rmax)); my = int(clamp(side * h, smin, smax))
        x = b[0] if edge == "left" else b[2]
        rect = (x - d, b[1] - my, x + d + 1, b[3] + my + 1)
    v = View(page, rect)
    v.box(b, RED, 1, dashed=True)
    edge_line(v, b, edge)
    return v.finish()


def ink_candidates(page, b, edge, outward, search, max_k=6, min_gap=4):
    """Candidate edge positions in the move direction: ink-run boundaries first, a uniform ruler fills gaps."""
    bw = page < 128
    x0, y0, x1, y1 = b
    if edge in ("top", "bottom"):
        prof = bw[:, max(x0, 0):x1 + 1].sum(1).astype(int)
        cur = y0 if edge == "top" else y1
    else:
        prof = bw[max(y0, 0):y1 + 1, :].sum(0).astype(int)
        cur = x0 if edge == "left" else x1
    to_smaller = (edge in ("top", "left")) == outward
    step = -1 if to_smaller else 1
    cands, prev_p, prev = [], cur, prof[clamp(cur, 0, len(prof) - 1)]
    p = cur
    for _ in range(search):
        p += step
        if p <= 0 or p >= len(prof) - 1:
            break
        if prev > 0 and prof[p] == 0:
            cands.append(prev_p)       # outermost ink of a run
        elif prev == 0 and prof[p] > 0:
            cands.append(p)            # first ink after blank space
        elif abs(int(prof[p]) - int(prev)) >= 3:
            cands.append(p)            # profile jump: a stroke starts or ends
        prev_p, prev = p, prof[p]
    merged = []
    for c in sorted(set(cands), key=lambda q: abs(q - cur)):
        if all(abs(c - q) >= min_gap for q in merged) and abs(c - cur) >= 2:
            merged.append(c)
    merged = merged[:max_k - 2]
    for f in (0.25, 0.5, 1.0):
        r = cur + step * int(round(f * search))
        if all(abs(r - q) >= 3 * min_gap for q in merged) and abs(r - cur) >= 2:
            merged.append(r)
    return sorted(merged, key=lambda q: abs(q - cur))[:max_k]


def with_edge(b, edge, pos):
    x0, y0, x1, y1 = b
    return {"top": (x0, pos, x1, y1), "bottom": (x0, y0, x1, pos), "left": (pos, y0, x1, y1), "right": (x0, y0, pos, y1)}[edge]


def magnitude_view(page, b, edge, cands):
    """M1: all candidate lines numbered in one image (smoke-test design)."""
    w, h = wh(b)
    horiz = edge in ("top", "bottom")
    cur = {"top": b[1], "bottom": b[3], "left": b[0], "right": b[2]}[edge]
    lo, hi = min(cands + [cur]), max(cands + [cur])
    pad = 24
    if horiz:
        mx = int(clamp(0.35 * w, 30, 120))
        rect = (b[0] - mx - 40, lo - pad, b[2] + mx + 1, hi + pad + 1)
    else:
        my = int(clamp(0.35 * h, 30, 120))
        rect = (lo - pad, b[1] - my - 30, hi + pad + 1, b[3] + my + 1)
    v = View(page, rect)
    v.box(b, GRAY, 1, dashed=True)
    strip = 76
    if horiz:
        v.img = np.concatenate([np.full((v.img.shape[0], strip, 3), 255, np.uint8), v.img], axis=1)
        v.rect = (v.rect[0] - strip / v.s, v.rect[1], v.rect[2], v.rect[3])
    else:
        v.img = np.concatenate([np.full((strip, v.img.shape[1], 3), 255, np.uint8), v.img], axis=0)
        v.rect = (v.rect[0], v.rect[1] - strip / v.s, v.rect[2], v.rect[3])
    for i, c in enumerate(cands):
        col = PALETTE[i % len(PALETTE)]
        if horiz:
            yy = c - 0.5 if edge == "top" else c + 0.5
            v.hline(yy, b[0] - 0.5, b[2] + 0.5, col, 3)
            _, y = v.p(0, yy)
            dashed_line(v.img, (strip - 6, y), v.p(b[0] - 0.5, yy), col, 1, 6)
            v.label(str(i + 1), (6 + (i % 2) * 34, y + 11), col, 1.0)
        else:
            xx = c - 0.5 if edge == "left" else c + 0.5
            v.vline(xx, b[1] - 0.5, b[3] + 0.5, col, 3)
            x, _ = v.p(xx, 0)
            dashed_line(v.img, (x, strip - 6), v.p(xx, b[1] - 0.5), col, 1, 6)
            v.label(str(i + 1), (x - 10, 32 + (i % 2) * 30), col, 1.0)
    return v.finish()


def png_bytes(img) -> bytes:
    ok, buf = cv2.imencode(".png", img)
    assert ok
    return buf.tobytes()
