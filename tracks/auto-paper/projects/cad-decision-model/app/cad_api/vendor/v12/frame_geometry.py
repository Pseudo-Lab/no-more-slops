"""Find a coherent drawing frame and remove its outside coordinate strips.

Long rules are only candidates: a process header can span most of a sheet. The
four selected sides must meet at supported corners and their detected extents
must end at those corners. Cropped/open frames fall back to the original image.
No page coordinates, tags, or ground truth are used.
"""
from __future__ import annotations
from itertools import product
import cv2
import numpy as np


def inside_frame(bw):
    H, W = bw.shape
    full = [0, 0, W - 1, H - 1]
    ink = (np.asarray(bw) != 0).astype(np.uint8)
    horizontal = cv2.morphologyEx(ink, cv2.MORPH_OPEN,
                                cv2.getStructuringElement(cv2.MORPH_RECT, (max(1, int(.75 * W)), 1)))
    vertical = cv2.morphologyEx(ink, cv2.MORPH_OPEN,
                              cv2.getStructuringElement(cv2.MORPH_RECT, (1, max(1, int(.75 * H)))))
    hs = [tuple(map(int, q)) for q in cv2.connectedComponentsWithStats(horizontal, connectivity=8)[2][1:]]
    vs = [tuple(map(int, q)) for q in cv2.connectedComponentsWithStats(vertical, connectivity=8)[2][1:]]
    # Ignore the raster's one-pixel outer boundary. The frame must lie in the
    # outer 15% bands; inner diagram rules are not independently used as sides.
    tops = [q for q in hs if .01 * H < q[1] < .15 * H]
    bottoms = [q for q in hs if .85 * H < q[1] < .99 * H]
    lefts = [q for q in vs if .01 * W < q[0] < .15 * W]
    rights = [q for q in vs if .85 * W < q[0] < .99 * W]
    frames = []
    for top, bottom, left, right in product(tops, bottoms, lefts, rights):
        tx, ty, tw, th, _ = top
        bx, by, bw_, bh, _ = bottom
        lx, ly, lw, lh, _ = left
        rx, ry, rw, rh, _ = right
        # The tolerance follows line thickness, not page size: allowing a
        # percentage of a large sheet would admit process lines many pixels in.
        tol = max(3, 2 * max(th, bh, lw, rw))
        x_left, x_right = lx + (lw - 1) / 2, rx + (rw - 1) / 2
        y_top, y_bottom = ty + (th - 1) / 2, by + (bh - 1) / 2
        if x_right <= x_left or y_bottom <= y_top:
            continue
        # Each side must start and end at the corresponding opposite sides. A
        # header can touch both verticals but cannot become their top endpoint.
        ends = [(tx, x_left), (tx + tw - 1, x_right),
                (bx, x_left), (bx + bw_ - 1, x_right),
                (ly, y_top), (ly + lh - 1, y_bottom),
                (ry, y_top), (ry + rh - 1, y_bottom)]
        if any(abs(actual - expected) > tol for actual, expected in ends):
            continue
        # Require actual ink around all four intersections. This also rejects
        # open sides whose projections happen to have matching extents.
        corners = [(x_left, y_top), (x_right, y_top), (x_left, y_bottom), (x_right, y_bottom)]
        if any(not ink[max(0, round(y) - tol):min(H, round(y) + tol + 1),
                       max(0, round(x) - tol):min(W, round(x) + tol + 1)].any() for x, y in corners):
            continue
        inside = [lx + lw, ty + th, rx - 1, by - 1]
        if inside[0] > inside[2] or inside[1] > inside[3]:
            continue
        frames.append(((x_right - x_left) * (y_bottom - y_top), inside))
    # Prefer the largest supported internal rectangle, preserving useful sheet
    # content when several nested complete borders are present.
    return max(frames, key=lambda item: item[0])[1] if frames else full


def remove_coordinate_strips(bw):
    box = inside_frame(bw)
    x0, y0, x1, y1 = box
    out = np.zeros_like(bw)
    out[y0:y1 + 1, x0:x1 + 1] = bw[y0:y1 + 1, x0:x1 + 1]
    return out, box
