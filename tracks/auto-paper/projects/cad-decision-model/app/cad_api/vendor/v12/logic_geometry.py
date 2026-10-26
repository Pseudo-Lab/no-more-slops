"""Raw-ink proposals for CLD terminal circles, arrow tags and finite gate bars.

The helpers do not assign classes or accept connections. New candidates still
need S2/C1. The class-aware extent pass only adds a demonstrably finite input
bar or four short radial lamp strokes to an already classified body. There are
no drawing numbers, page coordinates or ground-truth lookups in this module.
"""
from __future__ import annotations

import copy
import math

import cv2
import numpy as np

import page_cv as CV
import arrow_geometry as AG


def _wh(b):
    return b[2] - b[0] + 1, b[3] - b[1] + 1


def _union(a, b):
    return min(a[0], b[0]), min(a[1], b[1]), max(a[2], b[2]), max(a[3], b[3])


def _iou(a, b):
    z = CV.inter(a, b)
    return z / max(1, CV.area(a) + CV.area(b) - z)


def _valid(bw, box):
    return (len(box) == 4 and 0 <= box[0] <= box[2] < bw.shape[1]
            and 0 <= box[1] <= box[3] < bw.shape[0])


def _small_terminal_circles(bw):
    """Open or slightly broken rings at one end of a long horizontal wire.

    Removing long straight runs detaches the ring from its outgoing wire. The
    perimeter test permits an antialiased one-pixel break, unlike hole finding.
    A centre gap, all eight perimeter sectors and one-sided wire support reject
    filled junctions, letter O's and inline instruments.
    """
    th = CV.SC.text_h
    length = max(9, round(2 * th)) | 1
    straight = cv2.morphologyEx(bw, cv2.MORPH_OPEN, np.ones((1, length), np.uint8))
    residual = bw & (1 - straight)
    n, lab, st, _ = cv2.connectedComponentsWithStats(residual, connectivity=8)
    out = []
    for i in range(1, n):
        x, y, w, h, a = (int(v) for v in st[i])
        if not (.65 * th <= min(w, h) <= 1.4 * th and max(w, h) <= 1.45 * th
                and .72 <= w / h <= 1.35 and .11 <= a / (w * h) <= .45):
            continue
        ys, xs = np.nonzero(lab[y:y + h, x:x + w] == i)
        dx = (xs - (w - 1) / 2) / max(1, (w - 1) / 2)
        dy = (ys - (h - 1) / 2) / max(1, (h - 1) / 2)
        radial = np.sqrt(dx * dx + dy * dy)
        if np.mean((radial >= .68) & (radial <= 1.28)) < .88:
            continue
        sectors = np.floor((np.arctan2(dy, dx) + math.pi) * 4 / math.pi).astype(int) % 8
        if len(set(sectors[radial >= .68])) != 8:
            continue
        cy = y + (h - 1) / 2
        thickness = max(1, CV.SC.px(2))
        y0, y1 = max(0, round(cy) - thickness), min(bw.shape[0], round(cy) + thickness + 1)
        support = []
        for lo, hi in ((x - length, x), (x + w, x + w + length)):
            if lo < 0 or hi > bw.shape[1]:
                support.append(False)
                continue
            band = bw[y0:y1, lo:hi]
            support.append(bool(np.max(band.mean(axis=1)) >= .88))
        if sum(support) == 1:
            out.append((x, y, x + w - 1, y + h - 1))
    return out


def _arrow_outline(bw, box):
    """A tag has both a finite left notch and a right arrow flank."""
    x0, y0, x1, y1 = box
    w, h = _wh(box)
    if h < CV.SC.px(24, 10) or h > 5 * CV.SC.text_h or w < 1.7 * h or w > 12 * h:
        return False
    # Text is inside the tag. Only the outside third of its flank is sampled.
    side = min(round(.7 * h), w // 3)
    profiles = []
    for left in (True, False):
        vals = []
        for dy in (.1, .25, .5, .75, .9):
            yy = min(y1, max(y0, round(y0 + dy * (h - 1))))
            lo, hi = (x0, x0 + side) if left else (x1 - side, x1 + 1)
            cols = np.where(bw[max(y0, yy - 1):min(y1 + 1, yy + 2), lo:hi].any(axis=0))[0]
            if not len(cols):
                return False
            vals.append(int(cols.min() + lo if left else cols.max() + lo))
        profiles.append(vals)
    left, right = profiles
    # A rectangle, memory cell or two adjacent boxes lack one or both slopes.
    return (left[2] - max(left[0], left[4]) >= .16 * h
            and right[2] - max(right[0], right[4]) >= .16 * h
            and left[0] <= left[1] <= left[2] and left[2] >= left[3] >= left[4]
            and right[0] <= right[1] <= right[2] and right[2] >= right[3] >= right[4])


def _whole_arrow_tags(bw, boxes):
    replacements = []
    for i, a in enumerate(boxes):
        for b in boxes[i + 1:]:
            wa, ha = _wh(a)
            wb, hb = _wh(b)
            if abs(a[1] - b[1]) > 2 or abs(a[3] - b[3]) > 2:
                continue
            if abs(a[2] - b[0]) > 3 and abs(b[2] - a[0]) > 3:
                continue
            u = _union(a, b)
            if min(wa, wb) < .65 * min(ha, hb) or not _arrow_outline(bw, u):
                continue
            boundary = round((a[2] + b[0]) / 2) if a[0] < b[0] else round((b[2] + a[0]) / 2)
            # The number and drawing-name cells share a vertical divider. Two
            # consecutive arrow tags touching at their tips are two symbols.
            cols = bw[max(a[1], b[1]):min(a[3], b[3]) + 1,
                      max(0, boundary - 2):min(bw.shape[1], boundary + 3)]
            if not cols.size or cols.mean(axis=0).max() < .85:
                continue
            replacements.append((u, a, b))
    return replacements


def propose(bw, regions, exclude=(), boxes=None, profile_kind="logic", blob=None):
    """Preserve original proposals except proven parts of one arrow outline."""
    original = list(boxes if boxes is not None else CV.symbol_candidates(bw, regions, exclude, blob))
    if profile_kind != "logic":
        return original
    def keep(b):
        return (CV._inside_any(b, regions, 4)
                and not any(CV.inter(b, e) > .5 * CV.area(b) for e in exclude))
    out = list(original)
    for whole, a, b in _whole_arrow_tags(bw, original):
        if keep(whole):
            out = [old for old in out if tuple(old) not in (tuple(a), tuple(b))]
            out.append(whole)
    for b in _small_terminal_circles(bw):
        if keep(b) and not any(_iou(b, old) >= .7 or CV.contains(old, b, 1) for old in out):
            out.append(b)
    # CLD process arrows use the same observed taper and terminal shaft as
    # P&ID arrows, scaled to this sheet's letter height. Classification remains
    # a normal S2/C1 judgment against the CLD legend.
    for shape in AG.detect(bw, regions, exclude, profile_kind="pid"):
        b = tuple(shape["bbox"])
        if keep(b) and not any((CV.contains(old, b, 1) and CV.area(old) <= 2*CV.area(b))
                              or _iou(b, old) >= .7 for old in out):
            out.append(b)
    return sorted(set(tuple(b) for b in out), key=lambda b: (b[1], b[0], b[3], b[2]))


def _long_bar_has_terminal_arms(bw, body, x, top, bottom, sign, heights):
    """Extra ownership evidence for a bar longer than eight body heights.

    Both observed ends must be short tails beyond entering arms. The opposite
    face must be blank away from the body, and the body's centre must have its
    own outgoing arm. A shared bus, oversized frame or unsupported extension
    therefore cannot become a long gate merely by being finite.
    """
    x0, y0, x1, y1 = body
    _, h = _wh(body)
    if min(heights) - top > 1.25 * h or bottom - max(heights) > 1.25 * h:
        return False
    length = round(.65 * h)
    lo, hi = (x + 1, x + 1 + length) if sign < 0 else (x - length, x)
    if lo < 0 or hi > bw.shape[1]:
        return False
    rows = np.where(bw[top:bottom + 1, lo:hi].mean(axis=1) >= .85)[0] + top
    margin = max(1, CV.SC.px(2))
    if any(yy < y0 - margin or yy > y1 + margin for yy in rows):
        return False
    # The square/circular body's far edge, rather than the finite bar, owns
    # this output. Looking beyond it avoids mistaking its top/bottom outline
    # for an outgoing wire.
    lo, hi = (x1 + 1, x1 + 1 + length) if sign < 0 else (x0 - length, x0)
    if lo < 0 or hi > bw.shape[1]:
        return False
    cy = (y0 + y1) / 2
    a = max(y0, round(cy - .2 * h))
    b = min(y1, round(cy + .2 * h)) + 1
    return bool(np.any(bw[a:b, lo:hi].mean(axis=1) >= .85))


def finite_input_bar(bw, body, others=()):
    """Return an edge-connected straight bar with observed finite endpoints.

    Input wires must meet the opposite face at two separated heights. Bars up
    to eight body heights retain the original policy. Longer bars require both
    finite terminal tails, no opposite-face branches outside the body, and a
    separate centre output. A very long bus or a line touching a second body is
    left alone; this helper never assigns a class or accepts a connection.
    """
    if not _valid(bw, body):
        return None
    x0, y0, x1, y1 = (int(v) for v in body)
    w, h = _wh(body)
    if not (.7 <= w / h <= 1.35 and 1.7 * CV.SC.text_h <= min(w, h) <= 5 * CV.SC.text_h):
        return None
    margin = max(1, CV.SC.px(2))
    ordinary_span = round(8 * h)
    max_span = round(16 * h)
    for edge, sign in ((x0, -1), (x1, 1)):
        for x in range(max(0, edge - margin), min(bw.shape[1], edge + margin + 1)):
            column = bw[:, x]
            seed = min(y1, max(y0, (y0 + y1) // 2))
            if not column[seed]:
                continue
            top = seed
            while top > 0 and column[top - 1] and seed - top <= max_span:
                top -= 1
            bottom = seed
            while bottom + 1 < len(column) and column[bottom + 1] and bottom - seed <= max_span:
                bottom += 1
            if top == 0 or bottom == len(column) - 1 or bottom - top + 1 > max_span:
                continue
            if top >= y0 - .18 * h and bottom <= y1 + .18 * h:
                continue
            if top > y0 + .2 * h or bottom < y1 - .2 * h:
                continue
            lo, hi = (x - round(.65 * h), x) if sign < 0 else (x + 1, x + 1 + round(.65 * h))
            if lo < 0 or hi > bw.shape[1]:
                continue
            ys = np.where(bw[top:bottom + 1, lo:hi].mean(axis=1) >= .85)[0] + top
            runs = np.split(ys, np.where(np.diff(ys) > 1)[0] + 1)
            heights = [float(r.mean()) for r in runs if len(r)]
            if len(heights) < 2 or max(heights) - min(heights) < .45 * h:
                continue
            if (bottom - top + 1 > ordinary_span
                    and not _long_bar_has_terminal_arms(bw, body, x, top, bottom, sign, heights)):
                continue
            bar = (min(x, x0), top, max(x, x1), bottom)
            neighbours = [o.get("start_bbox", o.get("bbox")) if isinstance(o, dict) else o for o in others]
            if any(b is not None and tuple(b) != tuple(body) and not CV.inter(b, body)
                   and b[0] - 2 <= x <= b[2] + 2 and b[1] <= bottom and b[3] >= top
                   for b in neighbours):
                continue
            return bar
    return None


def compact_gate_output_pair(bw, gate_obj, other_obj, path, output_side, others=()):
    """Propose bounded verification boxes for an observed long-gate output.

    The actual full gate, class, route and net are never changed. A caller may
    ask fresh normal paired questions using the compact body only when the
    long bar is independently reproduced, the port is on its output face, and
    a short original horizontal neck reaches a compact second body. This is
    view geometry, never permission to accept a connection.
    """
    if gate_obj.get('class') not in ('logic_gate/and', 'logic_gate/or', 'logic_gate/coincidence'):
        return None
    if not other_obj.get('class') or other_obj.get('class') in ('other', 'text'):
        return None
    body = tuple(gate_obj.get('start_bbox', ()))
    full = tuple(gate_obj.get('bbox', ()))
    other = tuple(other_obj.get('bbox', ()))
    if not all(_valid(bw, box) for box in (body, full, other)):
        return None
    try:
        points = np.asarray(path, dtype=float)
    except (TypeError, ValueError):
        return None
    if (points.ndim != 2 or points.shape[1] != 2 or points.shape[0] < 2
            or not np.isfinite(points).all()):
        return None
    _, h = _wh(body)
    if _wh(full)[1] <= 8 * h or max(_wh(other)) > 6 * CV.SC.text_h:
        return None
    observed = finite_input_bar(bw, body, others)
    if observed is None or tuple(observed) != full:
        return None
    # Find the one straight bar face from the original ink, rather than
    # assuming all CLD input bars are on the left.
    margin = max(1, CV.SC.px(2))
    faces = []
    for edge, side in ((body[0], 'left'), (body[2], 'right')):
        cols = range(max(0, edge - margin), min(bw.shape[1], edge + margin + 1))
        if any(bw[full[1]:full[3] + 1, x].all() for x in cols):
            faces.append(side)
    if len(faces) != 1 or output_side != ('right' if faces[0] == 'left' else 'left'):
        return None
    if np.max(points[:, 1]) - np.min(points[:, 1]) > margin:
        return None
    direction = 1 if output_side == 'right' else -1
    if np.any(direction * np.diff(points[:, 0]) < 0):
        return None
    gate_edge = body[2] if direction > 0 else body[0]
    other_edge = other[0] if direction > 0 else other[2]
    if not (0 < direction * (other_edge - gate_edge) <= 6 * CV.SC.text_h):
        return None
    cy = (body[1] + body[3]) / 2
    if abs(points[0, 1] - cy) > .2 * h:
        return None
    if not (0 < direction * (points[0, 0] - gate_edge) <= 2 * CV.SC.text_h
            and 0 < direction * (other_edge - points[-1, 0]) <= 2 * CV.SC.text_h):
        return None
    if not (other[1] <= points[-1, 1] <= other[3]):
        return None
    # Every supplied checkpoint is an observed ink point. The full neck has
    # one common original row, including entry pixels on both actual bodies.
    for px, py in points:
        xx, yy = round(px), round(py)
        if not (0 <= xx < bw.shape[1] and 0 <= yy < bw.shape[0] and bw[yy, xx]):
            return None
    lo, hi = sorted((gate_edge, other_edge))
    y0 = max(body[1], other[1], round(points[:, 1].min()) - margin)
    y1 = min(body[3], other[3], round(points[:, 1].max()) + margin)
    if y0 > y1:
        return None
    rows = np.where(bw[y0:y1 + 1, lo:hi + 1].all(axis=1))[0] + y0
    if not len(rows):
        return None
    yy = int(min(rows, key=lambda y: abs(y - points[:, 1].mean())))
    neck = (lo, yy, hi, yy)
    for obj in others:
        if obj is gate_obj or obj is other_obj:
            continue
        if isinstance(obj, dict):
            if (obj.get('id') is not None
                    and obj.get('id') in (gate_obj.get('id'), other_obj.get('id'))):
                continue
            box = obj.get('bbox')
        else:
            box = obj
        if box is not None and CV.inter(neck, box):
            return None
    return {'gate_bbox': list(body), 'other_bbox': list(other), 'full_gate_bbox': list(full),
            'path': [[float(v) if float(v) != int(v) else int(v) for v in p] for p in path],
            'raw_neck': [[gate_edge, yy], [other_edge, yy]],
            'output_side': output_side,
            'reason': 'raw-reproduced long finite gate; central output face; short continuous original neck to a compact body'}


def four_ray_extent(bw, body):
    """Return all four observed short diagonal rays of a circular lamp."""
    if not _valid(bw, body):
        return None
    x0, y0, x1, y1 = (int(v) for v in body)
    w, h = _wh(body)
    if not (.82 <= w / h <= 1.2 and 1.7 * CV.SC.text_h <= min(w, h) <= 5 * CV.SC.text_h):
        return None
    margin = round(.35 * max(w, h))
    X0, Y0 = max(0, x0 - margin), max(0, y0 - margin)
    X1, Y1 = min(bw.shape[1] - 1, x1 + margin), min(bw.shape[0] - 1, y1 + margin)
    crop = bw[Y0:Y1 + 1, X0:X1 + 1]
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    radius = (w + h - 2) / 4
    rays = {}
    yy, xx = np.indices(crop.shape)
    dx, dy = xx + X0 - cx, yy + Y0 - cy
    radial = np.hypot(dx, dy)
    # A narrow diagonal corridor retains all observed pixels of a ray, including
    # an antialiased endpoint which a Hough fit can omit. Four independent
    # corner components are required, so a circular letter or one callout line
    # cannot enlarge an indicator.
    for qx, qy in ((-1, -1), (-1, 1), (1, -1), (1, 1)):
        diagonal = (abs(qx * dx - qy * dy) <= max(1.7, .055 * h))
        sector = ((qx * dx >= .2 * w) & (qy * dy >= .2 * h)
                  & (radial >= .76 * radius) & (radial <= 1.9 * radius))
        ink = (crop & diagonal & sector).astype(np.uint8)
        n, lab, st, _ = cv2.connectedComponentsWithStats(ink, connectivity=8)
        found = []
        for i in range(1, n):
            ys, xs = np.nonzero(lab == i)
            rs = radial[ys, xs]
            if rs.min() > 1.1 * radius or rs.max() < 1.2 * radius:
                continue
            if st[i, 2] < .15 * h or st[i, 3] < .15 * h:
                continue
            found.append((float(rs.max()), (int(xs.min() + X0), int(ys.min() + Y0),
                                            int(xs.max() + X0), int(ys.max() + Y0))))
        if found:
            rays[(qx, qy)] = max(found)
    if len(rays) != 4:
        return None
    result = tuple(body)
    for _, b in rays.values():
        result = _union(result, b)
    return result


def attached_extent(bw, body, ext=None, others=(), profile_kind="logic"):
    """Propose a finite gate-bar envelope for B6 before class is available."""
    ext = tuple(ext if ext is not None else body)
    if profile_kind != "logic":
        return ext
    bar = finite_input_bar(bw, body, others)
    # Use the observed bar and body alone. Generic extent may include a callout
    # arrow that happens to touch the AND outline and would spoil the B6 crop.
    return tuple(bar) if bar is not None else ext


def filled_square_body(bw, body):
    """Separate a filled I/O square from a diagonal wire touching its corner."""
    if not _valid(bw, body):
        return None
    x0, y0, x1, y1 = body
    w, h = _wh(body)
    if not (.7 <= w / h <= 1.4 and .65 * CV.SC.text_h <= min(w, h) <= 1.8 * CV.SC.text_h):
        return None
    ink = bw[y0:y1+1, x0:x1+1]
    if ink.mean() < .65:
        return None
    ys = np.where(ink.mean(axis=1) >= .85)[0]
    xs = np.where(ink.mean(axis=0) >= .85)[0]
    if len(xs) < .7*w or len(ys) < .7*h:
        return None
    b = (x0+int(xs.min()), y0+int(ys.min()), x0+int(xs.max()), y0+int(ys.max()))
    sw, sh = _wh(b)
    if not (.8 <= sw/sh <= 1.25 and bw[b[1]:b[3]+1, b[0]:b[2]+1].mean() >= .93):
        return None
    return b


def refine(bw, objects, cands=(), profile_kind="logic"):
    """Add only class-supported finite bars and complete four-ray envelopes."""
    if profile_kind != "logic":
        return objects, [], []
    out, notes = [], []
    for original in objects:
        o = copy.deepcopy(original)
        body = tuple(o.get("start_bbox", o["bbox"]))
        ext = None
        reason = None
        if o.get("class") in ("logic_gate/or", "logic_gate/and", "logic_gate/coincidence"):
            ext = finite_input_bar(bw, body, objects)
            reason = "observed finite input bar with multiple entering wires"
        elif o.get("class") == "indicator_light":
            ext = four_ray_extent(bw, body)
            reason = "four observed short diagonal lamp rays"
        elif o.get("class") == "io_marker/hardwired":
            square = filled_square_body(bw, body)
            if square is not None:
                o["bbox"], o["ext_bbox"] = list(square), list(square)
                reason = "filled square core excludes attached diagonal wire"
        corrected = _union(o["bbox"], ext) if ext is not None else tuple(o["bbox"])
        if tuple(original["bbox"]) != tuple(corrected):
            o["bbox"] = list(corrected)
            if ext is not None:
                o["ext_bbox"] = list(_union(o.get("ext_bbox", body), ext))
            o["logic_geometry_reason"] = reason
            notes.append({"cand": o.get("cand", o.get("id")), "before": list(original["bbox"]),
                          "after": o["bbox"], "reason": reason})
        out.append(o)
    return out, [], notes
