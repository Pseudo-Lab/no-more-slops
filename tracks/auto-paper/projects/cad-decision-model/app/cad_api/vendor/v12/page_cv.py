"""Code-side image processing for the page pipeline. No Jev calls here: code proposes, Jev decides.

- set_scale / estimate_text_height: every size threshold follows the letter height of the sheet
  (CLD sheets: about 18 px, P&ID sheets: about 9 px), so the same code works at both resolutions.
- layout_regions / table_regions: big ink clusters (S1 decides which are logic diagrams) and ruled tables
  (title block, revision block, equipment lists), which are never searched for symbols or diagram text.
- symbol_candidates: interiors of closed shapes + small filled shapes, with touching pieces grouped.
  Holes inside letters are skipped. S2 (Jev) decides which candidates are symbols.
- attached_extent: the symbol ink attached to an outline (a gate's input bar, lamp rays) for the B6 comparison.
- text_candidates: letters -> lines (horizontal or 90-degree rotated) -> blocks. T1 (Jev) confirms each block.
  loose=True is the low-resolution (P&ID) mode: broken glyphs are reassembled and letters touching a symbol outline
  are freed first.
- wire_nets: ink left after erasing the symbol boxes. Each connected wire is a net; a line broken to jump over a
  crossing line is joined across the crossing; optionally (P&ID) the dashes of a dashed signal line are chained (through
  junction dots, up to the symbol they point at) and pipes are joined across flange gaps (gap_links).
  A box touched by a net gets a port on that side. wire_path gives the drawn route between two ports.
- faint_lines: straight strokes drawn in light gray (P&ID signal lines), which the ink threshold misses.
All boxes are (x0, y0, x1, y1), inclusive full-resolution page pixels.
"""
from __future__ import annotations

from collections import deque

import cv2
import numpy as np

INK = 128            # gray < INK is ink


class _Scale:
    """Size thresholds were tuned on CLD sheets with 18 px letters; px() rescales them to the current sheet."""

    def __init__(self, text_h=18):
        self.text_h = int(text_h)
        self.s = self.text_h / 18.0

    def px(self, v, lo=1):
        return max(lo, int(round(v * self.s)))


SC = _Scale(18)
ERASE = 3            # symbol boxes are erased with this margin before tracing wires (tolerates small box errors)
RING = ERASE + 2     # band around a box where a wire end counts as touching it


def set_scale(text_h):
    global SC, ERASE, RING
    SC = _Scale(text_h)
    ERASE = SC.px(3, 2)
    RING = ERASE + 2
    return SC


def estimate_text_height(bw, lo=5, hi=40):
    """Most common height of letter-sized ink components (the cap height of the drawing's main text)."""
    _, _, st, _ = cv2.connectedComponentsWithStats(bw, connectivity=8)
    hs, ws, ar = st[1:, 3], st[1:, 2], st[1:, 4]
    m = (hs >= lo) & (hs <= hi) & (ws >= 2) & (ws <= hi) & (ar >= 8)
    if m.sum() < 30:
        return 18
    vals, cnts = np.unique(hs[m], return_counts=True)
    return int(vals[np.argmax(cnts)])


# ----------------------------------------------------------------------------- basics

def binarize(gray, thr=INK):
    return (gray < thr).astype(np.uint8)


def faint_lines(gray, lo=INK, hi=200, min_len=None):
    """Straight strokes drawn in light gray, which the ink threshold misses (P&ID dashed signal lines are often light gray,
    about 165). Gray halos along dark lines do not count: only light pixels away from dark ink, in straight runs of at
    least min_len; each run is then grown by two light pixels at its ends so it meets the dark line it continues."""
    min_len = (min_len or SC.px(10, 5)) | 1                         # odd kernels: no one-pixel shift in the opening
    dark = (gray < lo).astype(np.uint8)
    light = (gray < hi).astype(np.uint8)
    cand = light & (1 - dark) & (1 - cv2.dilate(dark, np.ones((3, 3), np.uint8)))
    h = cv2.morphologyEx(cand, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (min_len, 1)))
    v = cv2.morphologyEx(cand, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (1, min_len)))
    grown = cv2.dilate(h, np.ones((1, 5), np.uint8)) | cv2.dilate(v, np.ones((5, 1), np.uint8))
    return (grown & light & (1 - dark)).astype(np.uint8)


def remove_frame(bw, frac=0.5):
    """Erase lines longer than half the page (drawing frame). Returns (ink without them, removed lines)."""
    H, W = bw.shape
    h = cv2.morphologyEx(bw, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (int(W * frac), 1)))
    v = cv2.morphologyEx(bw, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (1, int(H * frac))))
    lines = (h | v).astype(np.uint8)
    return (bw & (1 - lines)).astype(np.uint8), lines


def area(b):
    return max(0, b[2] - b[0] + 1) * max(0, b[3] - b[1] + 1)


def inter(a, b):
    return area((max(a[0], b[0]), max(a[1], b[1]), min(a[2], b[2]), min(a[3], b[3])))


def contains(outer, inner, tol=0):
    return (inner[0] >= outer[0] - tol and inner[1] >= outer[1] - tol and
            inner[2] <= outer[2] + tol and inner[3] <= outer[3] + tol)


def _inside_any(b, rects, tol=0):
    return any(contains(r, b, tol) for r in rects)


# ----------------------------------------------------------------------------- regions and candidates

def layout_regions(bw, k=None, min_area=None):
    """Clusters of ink (dilated by k). Regions nested inside a bigger one are dropped (the bigger one covers them)."""
    k = k or (SC.px(31, 9) | 1)
    min_area = min_area or int(4000 * SC.s ** 2)
    d = cv2.dilate(bw, cv2.getStructuringElement(cv2.MORPH_RECT, (k, k)))
    n, _, st, _ = cv2.connectedComponentsWithStats(d, connectivity=8)
    boxes = []
    for i in range(1, n):
        x, y, w, h, _ = st[i]
        if w * h >= min_area:
            boxes.append((int(x + k // 2), int(y + k // 2), int(x + w - 1 - k // 2), int(y + h - 1 - k // 2)))
    boxes.sort(key=area, reverse=True)
    out = []
    for b in boxes:
        if not any(contains(o, b, 2) for o in out):
            out.append(b)
    return out


def table_regions(bw, min_lines=3, span=0.8, line_share=0.75):
    """Ruled tables (title block, revision block, equipment list): one ink component made mostly of long
    horizontal and vertical lines, with at least `min_lines` rules across most of its width and height."""
    n, lab, st, _ = cv2.connectedComponentsWithStats(bw, connectivity=8)
    th = SC.text_h
    out = []
    for i in range(1, n):
        x, y, w, h, a = st[i]
        if w < 8 * th or h < 3 * th:
            continue
        comp = (lab[y:y + h, x:x + w] == i).astype(np.uint8)
        hor = cv2.morphologyEx(comp, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (max(int(w * span), 3), 1)))
        ver = cv2.morphologyEx(comp, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (1, max(int(h * span), 3))))
        nh = cv2.connectedComponents(hor, connectivity=8)[0] - 1
        nv = cv2.connectedComponents(ver, connectivity=8)[0] - 1
        if nh < min_lines or nv < 2:
            continue
        hv = cv2.morphologyEx(comp, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (2 * th, 1))) | \
            cv2.morphologyEx(comp, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (1, 2 * th)))
        if hv.sum() < line_share * a:                               # pipework and symbols have many short/curved strokes
            continue
        out.append((int(x), int(y), int(x + w - 1), int(y + h - 1)))
    return out


def holes(bw, min_side=None, min_area=None, max_frac=0.45, letter_max=None):
    """Bounding boxes of the white interiors of closed shapes (circles, rectangles, chevrons, valve triangles).
    Holes of letters (O, A, 8, ...) are skipped: their ink component is letter-sized."""
    min_side = min_side or SC.px(12, 4)
    min_area = min_area or int(150 * SC.s ** 2)
    letter_max = letter_max or int(1.6 * SC.text_h)
    H, W = bw.shape
    cnts, hier = cv2.findContours(bw, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    out = []
    if hier is None:
        return out
    for c, hh in zip(cnts, hier[0]):
        if hh[3] == -1:          # outer boundary of an ink component, not a hole
            continue
        x, y, w, h = cv2.boundingRect(c)
        if min(w, h) < min_side or cv2.contourArea(c) < min_area or w > W * max_frac or h > H * max_frac:
            continue
        px, py, pw, ph = cv2.boundingRect(cnts[hh[3]])
        if max(pw, ph) <= letter_max:
            continue                                                 # a hole inside a letter or digit
        out.append((int(x), int(y), int(x + w - 1), int(y + h - 1)))
    return out


def solid_blobs(bw, min_side=None, max_side=None, fill=0.6):
    """Small filled shapes (I/O squares and diamonds, filled valves, arrow heads). Junction dots are smaller.
    fill: share of the bounding box that must be ink (a filled triangle or diamond fills about half of it)."""
    min_side = min_side or SC.px(14, 5)
    max_side = max_side or SC.px(40, 12)
    k = SC.px(7, 3) | 1
    o = cv2.morphologyEx(bw, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k)))
    n, _, st, _ = cv2.connectedComponentsWithStats(o, connectivity=8)
    out = []
    for i in range(1, n):
        x, y, w, h, a = st[i]
        if min_side <= min(w, h) and max(w, h) <= max_side and a >= fill * w * h:
            out.append((int(x), int(y), int(x + w - 1), int(y + h - 1)))
    return out


def group(boxes, gap=None, max_side=None):
    """Merge touching SMALL boxes (pieces of one symbol: S/R cells, valve triangles). Big ones stay alone."""
    gap = gap if gap is not None else max(2, SC.px(3))
    max_side = max_side or SC.px(150, 40)
    big = [tuple(b) for b in boxes if max(b[2] - b[0], b[3] - b[1]) > max_side]
    work = [list(b) for b in boxes if max(b[2] - b[0], b[3] - b[1]) <= max_side]
    changed = True
    while changed:
        changed = False
        out = []
        while work:
            a = work.pop()
            merged = True
            while merged:
                merged = False
                for b in work[:]:
                    if a[0] - gap <= b[2] and b[0] - gap <= a[2] and a[1] - gap <= b[3] and b[1] - gap <= a[3]:
                        a = [min(a[0], b[0]), min(a[1], b[1]), max(a[2], b[2]), max(a[3], b[3])]
                        work.remove(b)
                        merged = changed = True
            out.append(a)
        work = out
    return [tuple(b) for b in work] + big


def snap_out(bw, b, max_grow=None, frac=0.15):
    """Grow each side over the rest of the outline stroke: while the next row/column outside the box has ink over
    at least `frac` of the side. A wire touching the side covers only a few pixels, so it does not pull the side."""
    max_grow = max_grow or SC.px(4, 2)
    H, W = bw.shape
    x0, y0, x1, y1 = b
    for _ in range(max_grow):
        if y0 > 0 and bw[y0 - 1, x0:x1 + 1].sum() >= frac * (x1 - x0 + 1):
            y0 -= 1
        else:
            break
    for _ in range(max_grow):
        if y1 < H - 1 and bw[y1 + 1, x0:x1 + 1].sum() >= frac * (x1 - x0 + 1):
            y1 += 1
        else:
            break
    for _ in range(max_grow):
        if x0 > 0 and bw[y0:y1 + 1, x0 - 1].sum() >= frac * (y1 - y0 + 1):
            x0 -= 1
        else:
            break
    for _ in range(max_grow):
        if x1 < W - 1 and bw[y0:y1 + 1, x1 + 1].sum() >= frac * (y1 - y0 + 1):
            x1 += 1
        else:
            break
    return (x0, y0, x1, y1)


def attached_extent(bw, box, others=(), frac=0.6, min_margin=None, max_margin=None, min_run=None):
    """Box of the symbol ink attached to a candidate outline: a gate's input bar, lamp rays.
    In a window around the box, straight runs that reach the window border or another candidate's box are wires
    and are dropped (keeping pixels shared with a perpendicular run, so a bar crossed by input wires stays whole);
    the ink still connected to the outline is the symbol. Returns (box, window rect) in page pixels."""
    min_margin = min_margin or SC.px(8, 4)
    max_margin = max_margin or SC.px(40, 12)
    min_run = min_run or SC.px(8, 4)
    H, W = bw.shape
    x0, y0, x1, y1 = box
    solid = bw[y0:y1 + 1, x0:x1 + 1].mean() >= 0.45                # filled valve, arrow head
    m = int(min(max_margin, max(min_margin, frac * max(x1 - x0 + 1, y1 - y0 + 1))))
    if solid:
        m = max(m, SC.px(12, 6))                                    # room for an arrow's thin tip inside the window
    X0, Y0, X1, Y1 = max(x0 - m, 0), max(y0 - m, 0), min(x1 + m, W - 1), min(y1 + m, H - 1)
    win = bw[Y0:Y1 + 1, X0:X1 + 1].copy()
    h, w = win.shape
    near = [(o[0] - X0 - 2, o[1] - Y0 - 2, o[2] - X0 + 2, o[3] - Y0 + 2) for o in others
            if o[0] <= X1 and o[2] >= X0 and o[1] <= Y1 and o[3] >= Y0 and tuple(o) != tuple(box)
            and not inter(o, box)]                                   # boxes overlapping this one (containers) don't count
    runs_of = win
    if solid:
        # a filled candidate (filled valve, arrow head): its thick body is never a wire, and a line running out of it is
        # cut at the body, so the line's far part (an arrow's shaft) can be dropped without the near part (the arrow's tip)
        k = SC.px(5, 3) | 1
        thick = cv2.morphologyEx(win, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k)))
        n, tl = cv2.connectedComponents(thick, connectivity=8)
        own = [v for v in np.unique(tl[y0 - Y0:y1 - Y0 + 1, x0 - X0:x1 - X0 + 1]) if v]
        body = np.isin(tl, own).astype(np.uint8)                    # only the thick part of this candidate, not a nearby letter
        runs_of = win & (1 - body)
    hor = cv2.morphologyEx(runs_of, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (min_run, 1)))
    ver = cv2.morphologyEx(runs_of, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (1, min_run)))
    drop = np.zeros_like(win)
    for runs, cross in ((hor, ver), (ver, hor)):
        n, lab, st, _ = cv2.connectedComponentsWithStats(runs, connectivity=8)
        for i in range(1, n):
            rx, ry, rw, rh, _ = st[i]
            leaves = rx == 0 or ry == 0 or rx + rw >= w or ry + rh >= h
            hits = any(rx <= o[2] and rx + rw - 1 >= o[0] and ry <= o[3] and ry + rh - 1 >= o[1] for o in near)
            if leaves or hits:
                drop |= ((lab == i) & (cross == 0)).astype(np.uint8)
    if solid and body.any():
        # a straight line the body touches over a short stretch only, running on past the body on both sides, is not part
        # of the symbol (the boundary tick an arrow head points at); the edges of a filled valve touch it along their length
        bys, bxs = np.nonzero(body)
        bb = (bxs.min(), bys.min(), bxs.max(), bys.max())
        touch = cv2.dilate(body, np.ones((3, 3), np.uint8)) & (1 - body)
        for orient in ("h", "v"):
            k2 = (min_run, 1) if orient == "h" else (1, min_run)
            full = cv2.morphologyEx(win, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, k2))
            n, lab, st, _ = cv2.connectedComponentsWithStats(full, connectivity=8)
            for i in range(1, n):
                rx, ry, rw, rh, _ = st[i]
                comp = lab == i
                if orient == "v":
                    both, length = ry <= bb[1] - 2 and ry + rh - 1 >= bb[3] + 2, rh
                    along = len(set(np.nonzero(comp & (touch > 0))[0]))
                    rows = body[ry:ry + rh]                         # body on both sides of the line: the line runs through it
                    through = bool(rows[:, :rx].any() and rows[:, rx + rw:].any())
                else:
                    both, length = rx <= bb[0] - 2 and rx + rw - 1 >= bb[2] + 2, rw
                    along = len(set(np.nonzero(comp & (touch > 0))[1]))
                    cols = body[:, rx:rx + rw]
                    through = bool(cols[:ry].any() and cols[ry + rh:].any())
                if both and not through and along <= 0.5 * length:
                    drop |= (comp & (body == 0)).astype(np.uint8)
    win[drop > 0] = 0
    n, lab, st, _ = cv2.connectedComponentsWithStats(win, connectivity=8)
    cx0, cy0, cx1, cy1 = x0 - X0, y0 - Y0, x1 - X0, y1 - Y0
    core = lab[max(cy0, 0):cy1 + 1, max(cx0, 0):cx1 + 1]
    keep = [int(v) for v in np.unique(core) if v]
    if not keep:
        return tuple(box), (X0, Y0, X1, Y1)
    ys, xs = np.nonzero(np.isin(lab, keep))
    ext = (int(min(xs.min() + X0, x0)), int(min(ys.min() + Y0, y0)), int(max(xs.max() + X0, x1)), int(max(ys.max() + Y0, y1)))
    return ext, (X0, Y0, X1, Y1)


def symbol_candidates(bw, regions, exclude=(), blob=None):
    """Candidate symbol boxes inside the given regions (and outside `exclude`, e.g. tables): closed-shape outlines
    (hole boundary grown over the stroke) and small filled shapes, with touching pieces grouped. Parts outside the
    outline (a gate's input bar, lamp rays) are proposed later by attached_extent.
    blob: optional {"min_side", "max_side", "fill"} for solid_blobs (P&ID: filled valves and arrow heads)."""
    def keep(b):
        return _inside_any(b, regions, 4) and not any(inter(b, e) > 0.5 * area(b) for e in exclude)
    bl = blob or {}
    hs = [snap_out(bw, h) for h in holes(bw)]
    blobs = solid_blobs(bw, bl.get("min_side"), bl.get("max_side"), bl.get("fill", 0.6))
    boxes = [b for b in hs + blobs if keep(b)]
    out = group(boxes)
    return sorted(out, key=lambda b: (b[1], b[0]))


# ----------------------------------------------------------------------------- dashed lines

def _dash_components(st, max_len, max_thick):
    """Thin straight pieces that may be dashes of a dashed line: {label: ("h"|"v", x0, y0, x1, y1)}."""
    out = {}
    for i in range(1, len(st)):
        x, y, w, h, a = st[i]
        if max(w, h) > max_len or max(w, h) < 3:
            continue
        if w >= h and h <= max_thick and w >= 2 * h:
            out[i] = ("h", int(x), int(y), int(x + w - 1), int(y + h - 1))
        elif h > w and w <= max_thick and h >= 2 * w:
            out[i] = ("v", int(x), int(y), int(x + w - 1), int(y + h - 1))
    return out


_SIDE_AHEAD = {(0, 1): "top", (0, -1): "bottom", (1, 0): "left", (-1, 0): "right"}   # box side met when moving that way


def dash_links(lab, st, max_len=None, max_thick=None, max_gap=None, min_chain=3, boxmap=None, max_joint=None):
    """Chain the dashes of dashed lines (P&ID instrument signal lines). Two dashes link when they are collinear and
    the gap between them is short. A dash end also links to a small piece lying straight ahead across a short gap
    (a junction dot with a dash stuck to it: a 'joint'), so a chain runs through junctions. A chain with at least
    `min_chain` dashes is a dashed line; at its ends it continues to a solid line or other ink straight ahead, and
    when nothing is ahead but a symbol box (erased from the mask; `boxmap` holds box index + 1), the end touches that box.
    Returns (links [(label_a, label_b, (x, y) end of a, (x, y) start of b)], labels of dashes and joints in chains,
             end hits [(label, box index, (x, y) dash end, side of the box)])."""
    max_len = max_len or SC.px(30, 10)
    max_thick = max_thick or 3
    max_gap = max_gap or SC.px(16, 6)
    max_joint = max_joint or SC.px(24, 12)
    dashes = _dash_components(st, max_len, max_thick)
    H, W = lab.shape
    links, chain = [], _DSU(len(st))
    for orient in ("h", "v"):
        ds = [(k, d) for k, d in dashes.items() if d[0] == orient]
        if orient == "h":
            ds.sort(key=lambda kd: ((kd[1][2] + kd[1][4]) // 2, kd[1][1]))
        else:
            ds.sort(key=lambda kd: ((kd[1][1] + kd[1][3]) // 2, kd[1][2]))
        buckets = {}
        for k, d in ds:
            c = (d[2] + d[4]) // 2 if orient == "h" else (d[1] + d[3]) // 2
            buckets.setdefault(c, []).append((k, d))
        for c, items in buckets.items():
            cand = items + buckets.get(c - 1, []) + buckets.get(c + 1, [])
            for ka, a in items:
                for kb, b in cand:
                    if ka == kb:
                        continue
                    if orient == "h":
                        gap = b[1] - a[3] - 1
                        if 1 <= gap <= max_gap:
                            chain.union(ka, kb)
                            links.append((ka, kb, (a[3], (a[2] + a[4]) // 2), (b[1], (b[2] + b[4]) // 2)))
                    else:
                        gap = b[2] - a[4] - 1
                        if 1 <= gap <= max_gap:
                            chain.union(ka, kb)
                            links.append((ka, kb, ((a[1] + a[3]) // 2, a[4]), ((b[1] + b[3]) // 2, b[2])))
    # every dash end looks straight ahead over a short gap
    probes = []                                                     # (dash, end point, direction, label hit, point hit)
    for k, (o, x0, y0, x1, y1) in dashes.items():
        if o == "h":
            yc = (y0 + y1) // 2
            ends = (((x1, yc), (1, 0)), ((x0, yc), (-1, 0)))
        else:
            xc = (x0 + x1) // 2
            ends = (((xc, y1), (0, 1)), ((xc, y0), (0, -1)))
        for (ex, ey), (dx, dy) in ends:
            hit, hp = 0, None
            for step in range(1, max_gap + 2):
                px, py = ex + dx * step, ey + dy * step
                if not (0 <= px < W and 0 <= py < H):
                    break
                v = int(lab[py, px])
                if v and v != k:
                    hit, hp = v, (px, py)
                    break
            probes.append((k, (ex, ey), (dx, dy), hit, hp))
    joint_links = []
    for k, e, d, hit, hp in probes:
        if hit and hit not in dashes and max(st[hit][2], st[hit][3]) <= max_joint:
            chain.union(k, hit)                                     # junction dot (maybe with a dash stuck to it)
            joint_links.append((k, hit, e, hp))
    def box_ahead(ex, ey, dx, dy):
        if boxmap is None:
            return None
        for step in range(1, max_gap + RING + 2):
            px, py = ex + dx * step, ey + dy * step
            if not (0 <= px < W and 0 <= py < H) or lab[py, px]:
                return None
            if boxmap[py, px]:
                return int(boxmap[py, px]) - 1, _SIDE_AHEAD[(dx, dy)]
        return None

    sizes = {}
    for k in dashes:
        sizes[chain.find(k)] = sizes.get(chain.find(k), 0) + 1      # only dashes count towards the chain length
    in_chain = {k for k in dashes if sizes[chain.find(k)] >= min_chain}
    # a chain of only two dashes still counts when both of its ends run straight into other ink or a symbol box
    outer = {}
    for k, (ex, ey), (dx, dy), hit, hp in probes:
        r = chain.find(k)
        if 2 <= sizes[r] < min_chain and ((hit and chain.find(hit) != r) or (not hit and box_ahead(ex, ey, dx, dy))):
            outer[r] = outer.get(r, 0) + 1
    in_chain |= {k for k in dashes if outer.get(chain.find(k), 0) >= 2}
    joints = {j for k, j, _, _ in joint_links if k in in_chain}
    links = [lk for lk in links if lk[0] in in_chain and lk[1] in in_chain] + [lk for lk in joint_links if lk[0] in in_chain]
    # chain ends: continue to other ink straight ahead, or touch the symbol box ahead
    end_hits = []
    for k, (ex, ey), (dx, dy), hit, hp in probes:
        if k not in in_chain:
            continue
        if hit:
            if hit not in in_chain and hit not in joints:
                links.append((k, hit, (ex, ey), hp))
            continue
        b = box_ahead(ex, ey, dx, dy)
        if b:
            end_hits.append((k, b[0], (ex, ey), b[1]))
    return links, in_chain | joints, end_hits


def gap_links(mask, lab, st=None, max_gap=None, bar_min=None, bar_max=None):
    """A pipe interrupted by a flange or an orifice plate, drawn '-| |-': two short bars across the pipe face each other
    over a small empty gap, and the pipe continues on the outer side of each bar (one side belongs to a long line and the
    other at least to a stub longer than a letter, so two letters of a label never match). Returns links like find_bridges."""
    max_gap = max_gap or SC.px(16, 8)
    bar_min = bar_min or SC.px(16, 6)
    bar_max = bar_max or SC.px(44, 20)
    if st is None:
        st = cv2.connectedComponentsWithStats(mask, connectivity=8)[2]
    long_line, stub = 3 * SC.text_h, SC.px(22, 11)
    H, W = mask.shape
    out = []
    for orient in ("v", "h"):                                       # 'v' bars sit on a horizontal pipe
        k = (1, bar_min) if orient == "v" else (bar_min, 1)
        m = cv2.morphologyEx(mask, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, k))
        n, _, bst, _ = cv2.connectedComponentsWithStats(m, connectivity=8)
        bars = []
        for i in range(1, n):
            x, y, w, h, _ = bst[i]
            length, thick = (h, w) if orient == "v" else (w, h)
            if bar_min <= length <= bar_max and thick <= 3:
                bars.append((int(x), int(y), int(x + w - 1), int(y + h - 1)))
        if orient == "h":                                           # work in transposed coordinates
            bars = [(b[1], b[0], b[3], b[2]) for b in bars]
            mk, lb = mask.T, lab.T
        else:
            mk, lb = mask, lab
        bars.sort()
        for i, a in enumerate(bars):
            for b in bars[i + 1:]:
                gap = b[0] - a[2] - 1
                if gap > max_gap:
                    break
                lo, hi = max(a[1], b[1]), min(a[3], b[3])
                if gap < 2 or hi - lo + 1 < 0.6 * min(a[3] - a[1] + 1, b[3] - b[1] + 1):
                    continue
                rows = [r for r in range(lo, hi + 1)                # (the two pipe ends may sit one pixel apart)
                        if a[0] > 0 and b[2] + 1 < mk.shape[1] and mk[max(r - 1, 0):r + 2, a[0] - 1].any()
                        and mk[max(r - 1, 0):r + 2, b[2] + 1].any()]
                if not rows:
                    continue                                        # no pipe on the outer side of both bars
                r = rows[len(rows) // 2]
                if mk[max(r - 1, 0):r + 2, a[2] + 1:b[0]].any():
                    continue                                        # the gap at the pipe is not empty
                la, lb_ = int(lb[r, a[2]]) or int(lb[r, a[0]]), int(lb[r, b[0]]) or int(lb[r, b[2]])
                ea, eb = (max(st[la][2], st[la][3]), max(st[lb_][2], st[lb_][3])) if la and lb_ else (0, 0)
                if la and lb_ and la != lb_ and min(ea, eb) >= stub and max(ea, eb) >= long_line:
                    pa, pb = (a[2], r), (b[0], r)
                    if orient == "h":
                        pa, pb = (r, a[2]), (r, b[0])
                    out.append((la, lb_, pa, pb))
    return out


# ----------------------------------------------------------------------------- text

def _assemble_glyphs(comps, th, clear):
    """Pieces of one broken glyph (thresholding splits thin strokes at low resolution: the three bars of an E, the arcs of
    a C, the 1, slash and 2 of a fraction) are joined first: pieces stacked within 2 px across the reading direction
    whose union is still one letter high, with nothing drawn between them."""
    d = _DSU(len(comps))
    order = sorted(range(len(comps)), key=lambda k: comps[k][0])
    for ii, a in enumerate(order):
        A = comps[a]
        for b in order[ii + 1:]:
            B = comps[b]
            if B[0] > A[2] + 2:
                break
            for (p0, p1, q0, q1) in ((0, 2, 1, 3), (1, 3, 0, 2)):   # upright pieces stacked in y, rotated pieces side by side in x
                ov = min(A[p1], B[p1]) - max(A[p0], B[p0]) + 1
                gap = max(A[q0], B[q0]) - min(A[q1], B[q1]) - 1
                span = max(A[q1], B[q1]) - min(A[q0], B[q0]) + 1
                if ov >= 0.5 * min(A[p1] - A[p0] + 1, B[p1] - B[p0] + 1) and gap <= 2 and span <= th + 2:
                    lo, hi = (A, B) if A[q0] <= B[q0] else (B, A)
                    between = ((max(A[0], B[0]), lo[3] + 1, min(A[2], B[2]), hi[1] - 1) if q0 == 1 else
                               (lo[2] + 1, max(A[1], B[1]), hi[0] - 1, min(A[3], B[3])))
                    if clear(*between):
                        d.union(a, b)
                        break
    groups = {}
    for k in range(len(comps)):
        groups.setdefault(d.find(k), []).append(comps[k])
    return [(min(c[0] for c in g), min(c[1] for c in g), max(c[2] for c in g), max(c[3] for c in g)) for g in groups.values()]


def text_candidates(bw, regions, exclude=(), max_side=None, min_area=4, line_gap=1.2, block_gap=0.9, skip_dashes=False,
                    loose=False, word_gap=0.6, free_from=()):
    """Text blocks inside the regions (code proposal; Jev T1 confirms each one).
    Letters are small ink components that touch nothing else (wires and symbols form big connected components).
    Letters join into lines - horizontal lines when their tops and bottoms line up, vertical lines (text rotated by
    90 degrees) when their left and right edges line up; each letter takes the orientation that gives it the longer
    line. Lines join into a block (one box) when stacked closely. Two pieces never join across a stroke of a symbol
    or a wire (e.g. the S and R of an S-R memory stay apart because the cell border runs between them).
    loose (P&ID lettering at low resolution): only letter-shaped pieces count; thin bars and hyphens may belong to
    either orientation (a hyphen in rotated text looks like an upright I); overlapping pieces of one glyph (the 1, slash
    and 2 of a fraction) join.
    free_from: symbol boxes whose straight border strokes are taken out first, so letters touching the outline from
    inside (the drawing number in an off-page connector) come free.
    Returns [{"bbox": (x0, y0, x1, y1), "lines": [bbox, ...], "words": [[bbox, ...] per line], "chars": n,
              "orient": "h"|"v"}]."""
    max_side = max_side or SC.px(40, 12)
    th = SC.text_h
    m = np.zeros_like(bw)
    for (x0, y0, x1, y1) in regions:
        m[y0:y1 + 1, x0:x1 + 1] = bw[y0:y1 + 1, x0:x1 + 1]
    for (x0, y0, x1, y1) in exclude:
        m[y0:y1 + 1, x0:x1 + 1] = 0
    letters_from = m
    big = [b for b in free_from if min(b[2] - b[0], b[3] - b[1]) + 1 >= 2 * th]   # small symbols: nothing to free, only to break
    if big:
        L = SC.px(40, 20)
        hor = cv2.morphologyEx(m, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (L, 1)))
        ver = cv2.morphologyEx(m, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (1, L)))
        hb, vb = np.zeros_like(m), np.zeros_like(m)
        for (x0, y0, x1, y1) in big:                                # only strokes running along the border
            hb[max(y0 - 2, 0):y0 + 3, x0:x1 + 1] = 1
            hb[max(y1 - 2, 0):y1 + 3, x0:x1 + 1] = 1
            vb[y0:y1 + 1, max(x0 - 2, 0):x0 + 3] = 1
            vb[y0:y1 + 1, max(x1 - 2, 0):x1 + 3] = 1
        letters_from = m & (1 - ((hor & hb) | (ver & vb)))
    n, lab, st, _ = cv2.connectedComponentsWithStats(letters_from, connectivity=8)

    def letter_like(i):
        w, h = st[i][2], st[i][3]
        if max(w, h) > max_side or st[i][4] < min_area:
            return False
        if not loose:
            return True
        return abs(h - th) <= 3 or abs(w - th) <= 3 or max(w, h) <= th + 3   # upright, rotated, or a small mark
    small = [i for i in range(1, n) if letter_like(i)]
    if skip_dashes:
        _, dashed, _ = dash_links(lab, st)
        small = [i for i in small if i not in dashed]
    struct = m.copy()
    struct[np.isin(lab, small)] = 0                                 # wires + symbols only
    if loose:                                                       # specks left over from thresholding thin glyphs are not walls
        struct[np.isin(lab, [i for i in range(1, n) if st[i][4] < min_area])] = 0
    comps = [(int(st[i][0]), int(st[i][1]), int(st[i][0] + st[i][2] - 1), int(st[i][1] + st[i][3] - 1)) for i in small]

    def clear(x0, y0, x1, y1):
        """No wire/symbol ink in the rectangle between two pieces."""
        if x1 < x0 or y1 < y0:
            return True
        return not struct[max(y0, 0):y1 + 1, max(x0, 0):x1 + 1].any()

    def shape(c):
        """'up' = clearly an upright letter (cap height tall, narrower than tall), 'rot' = clearly rotated 90 degrees.
        loose: glyphs break into pieces at low resolution, so no piece is trusted to show its orientation ('?');
        the line vote below decides instead."""
        if loose:
            return "?"
        w, h = c[2] - c[0] + 1, c[3] - c[1] + 1
        if abs(h - th) <= 2 and w <= 0.8 * h:
            return "up"
        if abs(w - th) <= 2 and h <= 0.8 * w:
            return "rot"
        return "?"
    if loose:
        comps = _assemble_glyphs(comps, th, clear)
    shapes = [shape(c) for c in comps]

    def link(axis):
        """Union letters along one axis. axis 'h': reading left to right, 'v': reading along y (rotated text)."""
        dsu = _DSU(len(comps))
        a0, a1, b0, b1 = (0, 2, 1, 3) if axis == "h" else (1, 3, 0, 2)     # along-axis / cross-axis coordinates
        wrong = "rot" if axis == "h" else "up"
        order = sorted(range(len(comps)), key=lambda k: comps[k][a0])
        for ii, a in enumerate(order):
            A = comps[a]
            if shapes[a] == wrong:
                continue
            for b in order[ii + 1:]:
                B = comps[b]
                if shapes[b] == wrong:
                    continue
                ref = max(A[b1] - A[b0], B[b1] - B[b0], 0.45 * th) + 1    # cross-axis size ~ letter height
                gap = B[a0] - A[a1] - 1
                if gap > line_gap * ref:
                    break
                if gap < -1 and not loose:
                    continue                                        # (loose: overlapping pieces of one glyph may join)
                ca, cb = A[b1] - A[b0] + 1, B[b1] - B[b0] + 1
                ov = min(A[b1], B[b1]) - max(A[b0], B[b0]) + 1
                small_one = min(ca, cb) <= 0.55 * th                # dash, dot, comma: must sit inside the other's band
                inside = (B[b0] >= A[b0] - 1 and B[b1] <= A[b1] + 1) if cb <= ca else (A[b0] >= B[b0] - 1 and A[b1] <= B[b1] + 1)
                if not ((not small_one and ov >= 0.6 * min(ca, cb)) or (small_one and inside)):
                    continue
                if axis == "h":
                    ok = clear(A[2] + 1, max(A[1], B[1]), B[0] - 1, min(A[3], B[3]))
                else:
                    ok = clear(max(A[0], B[0]), A[3] + 1, min(A[2], B[2]), B[1] - 1)
                if ok:
                    dsu.union(a, b)
        size = {}
        for k in range(len(comps)):
            size[dsu.find(k)] = size.get(dsu.find(k), 0) + 1
        return dsu, size

    dh, sh = link("h")
    dv, sv = link("v")
    lines = {}
    min_v = 3 if loose else 2                                       # loose: a vertical line needs 3 letters (a digit under a word is not one)
    for k in range(len(comps)):
        nh, nv = sh[dh.find(k)], sv[dv.find(k)]
        key = ("v", dv.find(k)) if nv > nh and nv >= min_v else ("h", dh.find(k))
        lines.setdefault(key, []).append(comps[k])

    def words_of(cs, orient):
        """Split a line where the gap between letters is at least word_gap x letter height."""
        a0, a1 = (0, 2) if orient == "h" else (1, 3)
        cs = sorted(cs, key=lambda c: c[a0])
        groups, end = [], None
        for c in cs:
            if end is None or c[a0] - end - 1 >= word_gap * th:
                groups.append([])
            groups[-1].append(c)
            end = c[a1] if end is None else max(end, c[a1])
        return [(min(c[0] for c in g), min(c[1] for c in g), max(c[2] for c in g), max(c[3] for c in g)) for g in groups]
    lines = [(min(c[0] for c in cs), min(c[1] for c in cs), max(c[2] for c in cs), max(c[3] for c in cs), len(cs), key[0],
              words_of(cs, key[0]))
             for key, cs in lines.items()]
    lines = [ln for ln in lines if max(ln[3] - ln[1], ln[2] - ln[0]) + 1 >= 0.6 * th or ln[4] > 1]   # a lone speck is not text
    if loose:                                                       # nor a lone short dash (a dash of a dashed separator line)
        lines = [ln for ln in lines if ln[4] > 1 or max(ln[3] - ln[1], ln[2] - ln[0]) + 1 >= th
                 or min(ln[3] - ln[1], ln[2] - ln[0]) + 1 > 2]

    dsu2 = _DSU(len(lines))
    for i, A in enumerate(lines):
        for j in range(i + 1, len(lines)):
            B = lines[j]
            if A[5] != B[5]:
                continue
            if A[5] == "h":
                top, bot = (A, B) if A[1] <= B[1] else (B, A)
                hh = max(top[3] - top[1], bot[3] - bot[1]) + 1
                gap = bot[1] - top[3] - 1
                if gap < 0 or gap > block_gap * hh:
                    continue
                if min(A[2], B[2]) < max(A[0], B[0]) and abs(A[0] - B[0]) > 2 * hh:
                    continue                                        # neither overlapping nor left-aligned
                ok = clear(max(A[0], B[0]), top[3] + 1, min(A[2], B[2]), bot[1] - 1)
            else:
                lef, rig = (A, B) if A[0] <= B[0] else (B, A)
                ww = max(lef[2] - lef[0], rig[2] - rig[0]) + 1
                gap = rig[0] - lef[2] - 1
                if gap < 0 or gap > block_gap * ww:
                    continue
                if min(A[3], B[3]) < max(A[1], B[1]) and abs(A[3] - B[3]) > 2 * ww:
                    continue                                        # neither overlapping nor bottom-aligned
                ok = clear(lef[2] + 1, max(A[1], B[1]), rig[0] - 1, min(A[3], B[3]))
            if ok:
                dsu2.union(i, j)
    blocks = {}
    for i in range(len(lines)):
        blocks.setdefault(dsu2.find(i), []).append(lines[i])
    out = []
    for ls in blocks.values():
        ls.sort(key=lambda ln: (ln[1], ln[0]))
        out.append({"bbox": (min(ln[0] for ln in ls), min(ln[1] for ln in ls), max(ln[2] for ln in ls), max(ln[3] for ln in ls)),
                    "lines": [tuple(ln[:4]) for ln in ls], "words": [ln[6] for ln in ls], "chars": sum(ln[4] for ln in ls),
                    "orient": ls[0][5]})
    return sorted(out, key=lambda t: (t["bbox"][1], t["bbox"][0]))


# ----------------------------------------------------------------------------- wires

class _DSU:
    def __init__(self, n):
        self.p = list(range(n))

    def find(self, a):
        while self.p[a] != a:
            self.p[a] = self.p[self.p[a]]
            a = self.p[a]
        return a

    def union(self, a, b):
        a, b = self.find(a), self.find(b)
        if a != b:
            self.p[max(a, b)] = min(a, b)


def wire_mask(bw, boxes, regions, erase=None, exclude=()):
    erase = ERASE if erase is None else erase
    m = np.zeros_like(bw)
    for (x0, y0, x1, y1) in regions:
        m[y0:y1 + 1, x0:x1 + 1] = bw[y0:y1 + 1, x0:x1 + 1]
    for (x0, y0, x1, y1) in exclude:
        m[y0:y1 + 1, x0:x1 + 1] = 0
    for (x0, y0, x1, y1) in boxes:
        m[max(y0 - erase, 0):y1 + erase + 1, max(x0 - erase, 0):x1 + erase + 1] = 0
    return m


def _segments(mask, min_len=None):
    """Straight horizontal / vertical runs: (orient, x0, y0, x1, y1)."""
    min_len = min_len or SC.px(9, 4)
    segs = []
    for orient, k in (("h", (min_len, 1)), ("v", (1, min_len))):
        m = cv2.morphologyEx(mask, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, k))
        n, _, st, _ = cv2.connectedComponentsWithStats(m, connectivity=8)
        for i in range(1, n):
            x, y, w, h, _ = st[i]
            segs.append((orient, int(x), int(y), int(x + w - 1), int(y + h - 1)))
    return segs


def _label_at(lab, xs, ys):
    for x, y in zip(xs, ys):
        v = lab[y, x]
        if v:
            return int(v)
    return 0


def find_bridges(mask, lab, max_gap=None, align=2, arm=None):
    """Line pieces that face each other across a crossing line (the 'broken line = not connected' jump).
    Returns [(label_a, label_b, (x, y) end of a, (x, y) start of b)]."""
    max_gap = max_gap or SC.px(24, 8)
    arm = arm or SC.px(6, 3)
    H, W = mask.shape
    segs = _segments(mask)
    out = []
    for orient in ("v", "h"):
        ss = [s for s in segs if s[0] == orient]
        # bucket by the line's position across its direction, so only nearly collinear pieces are compared
        buckets = {}
        for s in ss:
            c = int(round(((s[1] + s[3]) if orient == "v" else (s[2] + s[4])) / 2))
            buckets.setdefault(c, []).append(s)
        for c, items in buckets.items():
            cand = [s for d in range(-align, align + 1) for s in buckets.get(c + d, [])]
            for a in items:
                for b in cand:
                    if a is b:
                        continue
                    if orient == "v":
                        ca, cb = (a[1] + a[3]) / 2, (b[1] + b[3]) / 2
                        lo, hi = a[4] + 1, b[2] - 1                 # rows strictly between a (above) and b (below)
                        if abs(ca - cb) > align or not (2 <= hi - lo + 1 <= max_gap):
                            continue
                        x = int(round((ca + cb) / 2))
                        band = mask[lo:hi + 1, max(x - 1, 0):x + 2]
                        rows = [lo + r for r in range(band.shape[0]) if band[r].any()]
                        if not rows:
                            continue
                        r = rows[len(rows) // 2]
                        if mask[r, max(x - arm, 0):x - 1].sum() < arm - 2 or mask[r, x + 2:min(x + arm + 1, W)].sum() < arm - 2:
                            continue                                # the thing in the gap is not a crossing line
                        pa, pb = (x, a[4]), (x, b[2])
                        la = _label_at(lab, [x, a[1], a[3]], [a[4]] * 3)
                        lb = _label_at(lab, [x, b[1], b[3]], [b[2]] * 3)
                        mid = lab[r, x]
                    else:
                        ca, cb = (a[2] + a[4]) / 2, (b[2] + b[4]) / 2
                        lo, hi = a[3] + 1, b[1] - 1                 # columns strictly between a (left) and b (right)
                        if abs(ca - cb) > align or not (2 <= hi - lo + 1 <= max_gap):
                            continue
                        y = int(round((ca + cb) / 2))
                        band = mask[max(y - 1, 0):y + 2, lo:hi + 1]
                        cols = [lo + cc for cc in range(band.shape[1]) if band[:, cc].any()]
                        if not cols:
                            continue
                        cc = cols[len(cols) // 2]
                        if mask[max(y - arm, 0):y - 1, cc].sum() < arm - 2 or mask[y + 2:min(y + arm + 1, H), cc].sum() < arm - 2:
                            continue
                        pa, pb = (a[3], y), (b[1], y)
                        la = _label_at(lab, [a[3]] * 3, [y, a[2], a[4]])
                        lb = _label_at(lab, [b[1]] * 3, [y, b[2], b[4]])
                        mid = lab[y, cc]
                    if la and lb and la != lb and mid and mid != la and mid != lb:   # the crossing line is another wire
                        out.append((la, lb, pa, pb))
    return out


def wire_nets(bw, boxes, regions, erase=None, ring=None, min_extent=None, min_area=6, exclude=(), dashes=False, wire_override=None):
    """Nets touching the symbol boxes. Returns (nets, label image).
    net = {"id", "labels": [component labels], "bbox", "ports": [{"obj", "side", "point", "anchor", "contact"}],
           "bridges": [[[x, y], [x, y]], ...], "dashed": bool}
    exclude: rectangles never traced (tables). dashes (P&ID): also chain dashed signal lines (through junction dots, up
    to the symbol they point at) and join pipes across flange gaps."""
    erase = ERASE if erase is None else erase
    ring = RING if ring is None else ring
    min_extent = min_extent or SC.px(30, 10)
    H, W = bw.shape
    mask = wire_mask(bw, boxes, regions, erase, exclude)
    if wire_override is not None:
        if wire_override.shape != mask.shape:
            raise ValueError("wire_override must have the same shape as the drawing")
        mask = (wire_override != 0).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(mask, connectivity=8)
    dsu = _DSU(n)
    bridges = find_bridges(mask, lab)
    dashed, end_hits = set(), []
    if dashes:
        boxmap = np.zeros(mask.shape, np.int32)
        for bi, (x0, y0, x1, y1) in enumerate(boxes):
            boxmap[max(y0 - erase, 0):y1 + erase + 1, max(x0 - erase, 0):x1 + erase + 1] = bi + 1
        links, dashed, end_hits = dash_links(lab, st, boxmap=boxmap)
        bridges = bridges + links + gap_links(mask, lab, st)
    for la, lb, _, _ in bridges:
        dsu.union(la, lb)

    # contacts: component pixels in the band around each box
    contacts = {}                                                   # (root, obj, side) -> list of (x, y)
    names = ("left", "top", "right", "bottom")
    for bi, (x0, y0, x1, y1) in enumerate(boxes):
        ex0, ey0, ex1, ey1 = max(x0 - ring, 0), max(y0 - ring, 0), min(x1 + ring, W - 1), min(y1 + ring, H - 1)
        sub = lab[ey0:ey1 + 1, ex0:ex1 + 1]
        ys, xs = np.nonzero(sub)
        if len(xs) == 0:
            continue
        ls = sub[ys, xs]
        xs, ys = xs + ex0, ys + ey0
        d = np.stack([np.abs(xs - x0), np.abs(ys - y0), np.abs(xs - x1), np.abs(ys - y1)])
        side_idx = d.argmin(0)
        for x, y, l, s in zip(xs.tolist(), ys.tolist(), ls.tolist(), side_idx.tolist()):
            if st[l][4] < min_area and l not in dashed:
                continue
            contacts.setdefault((dsu.find(l), bi, names[s]), []).append((x, y))
    for l, bi, (x, y), side in end_hits:                            # a dashed line ending a little short of a symbol
        contacts.setdefault((dsu.find(l), bi, side), []).extend([(x, y), (x, y)])

    roots = {}
    for l in range(1, n):
        roots.setdefault(dsu.find(l), []).append(l)
    by_root = {}
    for (r, bi, side), pts in contacts.items():
        by_root.setdefault(r, []).append((bi, side, pts))
    br_by_root = {}
    for la, lb, pa, pb in bridges:
        br_by_root.setdefault(dsu.find(la), []).append([list(pa), list(pb)])
    nets = []
    for root, labels in sorted(roots.items()):
        ports = []
        for bi, side, pts in by_root.get(root, []):
            if len(pts) < 2:
                continue
            pts_a = np.array(pts, float)
            mx, my = pts_a.mean(0)
            k = int(np.argmin(((pts_a - (mx, my)) ** 2).sum(1)))
            ports.append({"obj": bi, "side": side, "point": [round(float(mx), 1), round(float(my), 1)],
                          "anchor": [int(pts[k][0]), int(pts[k][1])], "contact": len(pts)})
        xs0 = [st[l][0] for l in labels]
        ys0 = [st[l][1] for l in labels]
        xs1 = [st[l][0] + st[l][2] - 1 for l in labels]
        ys1 = [st[l][1] + st[l][3] - 1 for l in labels]
        bbox = [int(min(xs0)), int(min(ys0)), int(max(xs1)), int(max(ys1))]
        extent = max(bbox[2] - bbox[0], bbox[3] - bbox[1]) + 1
        if not ports and extent < min_extent:
            continue                                                # letters, specks
        if sum(st[l][4] for l in labels) < min_area:
            continue
        ports.sort(key=lambda p: (p["obj"], p["side"]))
        nets.append({"id": len(nets), "labels": [int(l) for l in labels], "bbox": bbox, "ports": ports,
                     "bridges": br_by_root.get(root, []), "dashed": any(l in dashed for l in labels)})
    return nets, lab


def wire_dists(lab, net, points):
    """Length of the drawn route (pixel steps; a bridge counts as one step) between every two of `points` (anchor pixels
    of one net). Returns a matrix (None where unreachable). Used to pick neighbouring symbols along a big net."""
    x0, y0, x1, y1 = net["bbox"]
    x0, y0 = max(x0 - 2, 0), max(y0 - 2, 0)
    sub = np.isin(lab[y0:y1 + 3, x0:x1 + 3], net["labels"])
    h, w = sub.shape
    ys, xs = np.nonzero(sub)
    n = len(points)
    D = [[None] * n for _ in range(n)]
    if len(xs) == 0:
        return D
    ids = np.full(h * w, -1, np.int64)
    flat_idx = ys * w + xs
    ids[flat_idx] = np.arange(len(flat_idx))

    def snap(p):
        px, py = int(p[0] - x0), int(p[1] - y0)
        if 0 <= px < w and 0 <= py < h and sub[py, px]:
            return int(ids[py * w + px])
        k = int(np.argmin((xs - px) ** 2 + (ys - py) ** 2))
        return k
    jumps = {}
    for pa, pb in net["bridges"]:
        a, b = snap(pa), snap(pb)
        jumps.setdefault(a, []).append(b)
        jumps.setdefault(b, []).append(a)
    src = [snap(p) for p in points]
    steps = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
    for i, s in enumerate(src):
        dist = {s: 0}
        want = {t for t in src if t != s}
        q = deque([s])
        while q and want:
            c = q.popleft()
            want.discard(c)
            cy, cx = int(ys[c]), int(xs[c])
            nb = []
            for dy, dx in steps:
                yy, xx = cy + dy, cx + dx
                if 0 <= yy < h and 0 <= xx < w and sub[yy, xx]:
                    nb.append(int(ids[yy * w + xx]))
            nb += jumps.get(c, [])
            for v in nb:
                if v not in dist:
                    dist[v] = dist[c] + 1
                    q.append(v)
        for j, t in enumerate(src):
            D[i][j] = dist.get(t)
    return D


def _raw_bridge_path_records(net, shape):
    """Bind optional raster polylines to exact existing bridge endpoint pairs.

    This validates metadata only. It does not establish that a proposed gap is
    a connected wire; the normal model's route and endpoint checks still apply.
    Conflicting paths for the same original bridge are deliberately ignored.
    """
    records = net.get("bridge_paths")
    if not isinstance(records, (list, tuple)):
        return {}

    def point(p):
        if not isinstance(p, (list, tuple)) or len(p) != 2:
            return None
        if any(type(v) not in (int, float, np.int32, np.int64, np.float32, np.float64) for v in p):
            return None
        if not (0 <= p[0] < shape[1] and 0 <= p[1] < shape[0]):
            return None
        if any(not np.isfinite(v) or float(v) != int(v) for v in p):
            return None
        x, y = map(int, p)
        return (x, y) if 0 <= x < shape[1] and 0 <= y < shape[0] else None

    allowed = set()
    for pa, pb in net["bridges"]:
        a, b = point(pa), point(pb)
        if a is not None and b is not None and a != b:
            allowed.add(tuple(sorted((a, b))))
    choices = {}
    for record in records:
        if not isinstance(record, dict):
            continue
        endpoints, raw = record.get("endpoints"), record.get("path")
        if not isinstance(endpoints, (list, tuple)) or len(endpoints) != 2 \
                or not isinstance(raw, (list, tuple)) or len(raw) < 2:
            continue
        a, b = point(endpoints[0]), point(endpoints[1])
        path = [point(p) for p in raw]
        if a is None or b is None or a == b or any(p is None for p in path):
            continue
        key = tuple(sorted((a, b)))
        if key not in allowed:
            continue
        if path[0] == b and path[-1] == a:
            path.reverse()
        if path[0] != a or path[-1] != b:
            continue
        # Drop redundant collinear samples, keeping exact bends and reversals.
        compact = []
        for p in path:
            if compact and p == compact[-1]:
                continue
            while len(compact) >= 2:
                u, v = compact[-2], compact[-1]
                dx0, dy0, dx1, dy1 = v[0]-u[0], v[1]-u[1], p[0]-v[0], p[1]-v[1]
                if dx0*dy1 != dy0*dx1 or dx0*dx1 + dy0*dy1 <= 0:
                    break
                compact.pop()
            compact.append(p)
        if len(set(compact)) != len(compact):
            continue
        if compact[0] != key[0]:
            compact.reverse()
        choices.setdefault(key, set()).add(tuple(compact))
    return {key: next(iter(paths)) for key, paths in choices.items() if len(paths) == 1}


def wire_path(lab, net, a_xy, b_xy, eps=1.5):
    """Shortest drawn route between two anchor pixels of one net (bridges jump over crossing lines and dash gaps).
    Optional bridge_paths preserve a proposal's raw bends only when that bridge
    is used. A bend on this net's actual ink becomes an exact graph node, so a
    route can stop or branch there. Blank bends remain virtual waypoints. This
    affects route geometry only; wire_dists retains its old two-point bridges.
    Returns a simplified polyline [[x, y], ...] or None."""
    x0, y0, x1, y1 = net["bbox"]
    x0, y0 = max(x0 - 2, 0), max(y0 - 2, 0)
    sub = np.isin(lab[y0:y1 + 3, x0:x1 + 3], net["labels"])
    h, w = sub.shape
    ys, xs = np.nonzero(sub)
    if len(xs) == 0:
        return None

    def snap(p):
        px, py = int(p[0] - x0), int(p[1] - y0)
        if 0 <= px < w and 0 <= py < h and sub[py, px]:
            return py * w + px
        k = int(np.argmin((xs - px) ** 2 + (ys - py) ** 2))
        return int(ys[k]) * w + int(xs[k])

    records = _raw_bridge_path_records(net, lab.shape)
    bridges = [(pa, pb, snap(pa), snap(pb)) for pa, pb in net["bridges"]]
    # Distinct raw bridges snapping onto the same nodes are ambiguous. Do not
    # substitute another nearby shape's path merely because snap agrees.
    snap_groups = {}
    for pa, pb, a, b in bridges:
        raw_key = tuple(sorted((tuple(pa), tuple(pb))))
        snap_groups.setdefault(tuple(sorted((a, b))), set()).add(raw_key)
    plans = []
    for pa, pb, a, b in bridges:
        raw_key = tuple(sorted((tuple(pa), tuple(pb))))
        raw = records.get(raw_key)
        if raw is not None and tuple(pa) != raw[0]:
            raw = tuple(reversed(raw))
        if raw is None or a == b or len(snap_groups[tuple(sorted((a, b)))]) != 1:
            plans.append(([(a, b, None)], set()))
            continue
        anchors = [(0, a)]
        for index, (x, y) in enumerate(raw[1:-1], 1):
            px, py = x-x0, y-y0
            if 0 <= px < w and 0 <= py < h and sub[py, px]:
                anchors.append((index, py*w+px))
        anchors.append((len(raw)-1, b))
        if len({node for _, node in anchors}) != len(anchors):
            plans.append(([(a, b, None)], set()))
            continue
        edges = [(u, v, tuple(raw[i:j+1])) for (i, u), (j, v) in zip(anchors, anchors[1:])]
        plans.append((edges, set(raw[1:-1])))
    # A shared graph edge with different raw virtual bends has no unique route
    # provenance. Fall back to each affected original two-point bridge.
    edge_paths = {}
    for origin, (edges, _) in enumerate(plans):
        for a, b, path in edges:
            if path is None:
                continue
            canonical = path if a < b else tuple(reversed(path))
            edge_paths.setdefault(tuple(sorted((a, b))), {}).setdefault(canonical, set()).add(origin)
    conflicting = {origin for paths in edge_paths.values() if len(paths) > 1
                   for origins in paths.values() for origin in origins}
    jumps, jump_routes = {}, {}
    for origin, (edges, corners) in enumerate(plans):
        if origin in conflicting:
            _, _, a, b = bridges[origin]
            edges, corners = [(a, b, None)], set()
        for a, b, raw in edges:
            jumps.setdefault(a, []).append(b)
            jumps.setdefault(b, []).append(a)
            jump_routes.setdefault(a, []).append((raw, corners) if raw is not None else None)
            jump_routes.setdefault(b, []).append((tuple(reversed(raw)), corners) if raw is not None else None)
    s, t = snap(a_xy), snap(b_xy)
    flat = sub.ravel()
    parent = np.full(h * w, -1, np.int64)
    parent_jump = {}
    parent[s] = s
    q = deque([s])
    steps = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
    while q:
        p = q.popleft()
        if p == t:
            break
        py, px = divmod(p, w)
        nbrs = [(py + dy) * w + (px + dx) for dy, dx in steps if 0 <= py + dy < h and 0 <= px + dx < w]
        ordinary = len(nbrs)
        nbrs += jumps.get(p, ())
        for index, nb in enumerate(nbrs):
            if flat[nb] and parent[nb] < 0:
                parent[nb] = p
                if index >= ordinary:
                    detail = jump_routes[p][index-ordinary]
                    if detail is not None:
                        parent_jump[nb] = detail
                q.append(nb)
    if parent[t] < 0:
        return None
    pts = []
    preserved_corners = set()
    jump_endpoint_candidates = set()
    p = t
    while True:
        py, px = divmod(int(p), w)
        pts.append((px + x0, py + y0))
        if p == s:
            break
        if int(p) in parent_jump:
            raw, corners = parent_jump[int(p)]
            pts.extend(reversed(raw[1:-1]))
            preserved_corners.update(corners)
            jump_endpoint_candidates.add((px+x0, py+y0))
            ay, ax = divmod(int(parent[p]), w)
            jump_endpoint_candidates.add((ax+x0, ay+y0))
        p = parent[p]
    pts.reverse()
    def protected(index):
        p = pts[index]
        if p in preserved_corners:
            return True
        if p not in jump_endpoint_candidates:
            return False
        a, b = pts[index-1], pts[index+1]
        return (p[0]-a[0])*(b[1]-p[1]) != (p[1]-a[1])*(b[0]-p[0])
    anchors = [0] + [i for i in range(1, len(pts)-1) if protected(i)] + [len(pts)-1]
    if len(anchors) == 2:
        poly = cv2.approxPolyDP(np.array(pts, np.int32).reshape(-1, 1, 2), eps, False).reshape(-1, 2)
    else:
        segments = [cv2.approxPolyDP(np.array(pts[a:b+1], np.int32).reshape(-1, 1, 2), eps, False).reshape(-1, 2)
                    for a, b in zip(anchors, anchors[1:])]
        poly = np.concatenate([segments[0]] + [part[1:] for part in segments[1:]])
    return [[int(x), int(y)] for x, y in poly]
