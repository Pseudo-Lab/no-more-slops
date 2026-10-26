"""Conservative geometry cleanup of Jev-confirmed diagram text.

This module performs no OCR, model calls, or coordinate-specific corrections. It
normalizes *after* T1/T2: retain text inside symbols, remove external actuator
cap strokes only when their geometry and a nearby valve agree, remove regions
explicitly excluded by the caller, and suppress nested fragments of one line.

``normalize_texts(bw, texts, symbols, regions, exclude=())`` returns deep-copied
``(kept, removed)`` lists. Removed records carry ``geometry_reason``; changed
records retain ``geometry_before_bbox`` and ``geometry_removed_lines``.
``bw`` is a 2-D binary ink array (nonzero = ink), boxes are inclusive xyxy page
coordinates, texts keep their existing IDs/metadata, and symbols are records
with at least ``bbox`` and preferably ``class``. Empty ``regions`` means no
search-area restriction. Do not pass all symbol boxes as ``exclude``: internal
S/R, tag numbers, and lamp letters are required text.
"""
from __future__ import annotations

from copy import deepcopy
import cv2
import numpy as np


def _box(value):
    return tuple(int(v) for v in (value["bbox"] if isinstance(value, dict) else value))


def _area(b):
    return max(0, b[2] - b[0] + 1) * max(0, b[3] - b[1] + 1)


def _intersection(a, b):
    return (max(a[0], b[0]), max(a[1], b[1]), min(a[2], b[2]), min(a[3], b[3]))


def _contains(outer, inner):
    return outer[0] <= inner[0] and outer[1] <= inner[1] and outer[2] >= inner[2] and outer[3] >= inner[3]


def _union(boxes):
    return [min(b[0] for b in boxes), min(b[1] for b in boxes),
            max(b[2] for b in boxes), max(b[3] for b in boxes)]


def _coverage(b, region_boxes):
    # Compute union coverage, so adjacent search regions together can contain a line.
    m = np.zeros((b[3] - b[1] + 1, b[2] - b[0] + 1), np.uint8)
    for rb in region_boxes:
        q = _intersection(b, rb)
        if _area(q):
            m[q[1] - b[1]:q[3] - b[1] + 1, q[0] - b[0]:q[2] - b[0] + 1] = 1
    return float(m.mean())


def _near_valve(b, symbols):
    # A cap can sit above a valve, or alongside it in a rotated drawing. Use
    # relative size/distance, never a fixed sheet coordinate or a tag name.
    reach = 2.5 * max(b[2] - b[0] + 1, b[3] - b[1] + 1)
    cx, cy = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
    for s in symbols:
        cls = str(s.get("class", ""))
        if not (cls.startswith("valve/") or cls.startswith("actuator/")):
            continue
        q = _box(s)
        dx = max(q[0] - cx, cx - q[2], 0)
        dy = max(q[1] - cy, cy - q[3], 0)
        aligned = dx <= 0.4 * max(q[2] - q[0] + 1, b[2] - b[0] + 1) or dy <= 0.4 * max(q[3] - q[1] + 1, b[3] - b[1] + 1)
        if max(dx, dy) <= reach and aligned:
            return True
    return False


def _orthogonal_cap(crop, labels, stats, b):
    """Recognize a simple T attached to structure, or an external inverted-U cap.

    A normal free printed T is preserved. Curves, diagonals, and extra internal
    strokes disqualify a cap; the separate nearby-valve test supplies context.
    """
    h, w = crop.shape
    if min(h, w) < 4 or not crop.any():
        return False
    ink = crop != 0
    thickness = max(1, min(2, int(round(min(h, w) * 0.2))))
    rows = ink.mean(axis=1)
    # Top/bottom crossbar must span almost the full candidate.
    for top in (True, False):
        edge_rows = range(min(thickness + 1, h)) if top else range(max(0, h - thickness - 1), h)
        r = max(edge_rows, key=lambda y: rows[y])
        if rows[r] < 0.8:
            continue
        bar = np.zeros_like(ink)
        bar[max(0, r - thickness + 1):min(h, r + thickness), :] = True
        col = int(np.argmax(ink.sum(axis=0)))
        if abs(col - (w - 1) / 2) <= 0.2 * w and ink[:, col].mean() >= 0.7:
            allowed = bar.copy()
            allowed[:, max(0, col - thickness + 1):min(w, col + thickness)] = True
            if int((ink & ~allowed).sum()) <= max(1, int(0.03 * ink.sum())):
                # Only a T connected to a larger drawn structure is discarded.
                component_ids = np.unique(labels[b[1]:b[3] + 1, b[0]:b[2] + 1][ink])
                for k in component_ids:
                    x, y, ww, hh, aa = stats[int(k)]
                    if k and (ww > 2 * w or hh > 2 * h) and aa > 2 * int(ink.sum()):
                        return True
        # A staple has two edge stems and no glyph strokes between them.
        # Standard actuator caps have their crossbar on top; printed U is not it.
        if top and w >= 1.2 * h:
            left = int(np.argmax(ink[:, :thickness + 1].sum(axis=0)))
            right = w - thickness - 1 + int(np.argmax(ink[:, w - thickness - 1:].sum(axis=0)))
            if ink[:, left].mean() >= 0.65 and ink[:, right].mean() >= 0.65:
                allowed = bar.copy()
                allowed[:, :left + thickness] = True
                allowed[:, max(0, right - thickness + 1):] = True
                if int((ink & ~allowed).sum()) <= max(2, int(0.05 * ink.sum())):
                    return True
    return False


def _same_line(a, b):
    aa, bb = _box(a), _box(b)
    vertical = a.get("orient") == "v" or b.get("orient") == "v"
    j0, j1 = (0, 2) if vertical else (1, 3)
    short = min(aa[j1] - aa[j0] + 1, bb[j1] - bb[j0] + 1)
    ov = min(aa[j1], bb[j1]) - max(aa[j0], bb[j0]) + 1
    return ov >= 0.85 * short and abs((aa[j0] + aa[j1]) - (bb[j0] + bb[j1])) <= max(2, 0.3 * short)


def normalize_texts(bw, texts, symbols, regions, exclude=()):
    """Clean retained text records without changing model probabilities or inputs.

    Only nearly contained, same-line candidates are deduplicated. Disjoint labels
    and partly overlapping different rows stay separate; T2's grouping is kept.
    Returned removal reasons are suitable for the existing trace, not accuracy
    claims. Geometry coordinates change only when entire structural/out-of-scope
    lines are removed from a block.
    """
    ink = (np.asarray(bw) != 0).astype(np.uint8)
    if ink.ndim != 2:
        raise ValueError("bw must be a 2-D binary ink image")
    h, w = ink.shape
    symbols = [s if isinstance(s, dict) else {"bbox": s} for s in symbols]
    regions = [_box(r) for r in regions]
    exclude = [_box(r) for r in exclude]
    _, labels, stats, _ = cv2.connectedComponentsWithStats(ink, connectivity=8)
    kept, removed = [], []
    for original in texts:
        t = deepcopy(original)
        source_lines = t.get("lines") or [t["bbox"]]
        lines, rejected = [], []
        for line in source_lines:
            b = _box(line)
            reason = None
            if not (0 <= b[0] <= b[2] < w and 0 <= b[1] <= b[3] < h):
                reason = "outside_image"
            elif exclude and _coverage(b, exclude) >= 0.5:
                reason = "excluded_region"
            elif regions and _coverage(b, regions) < 0.5:
                reason = "outside_diagram_region"
            elif not any(_contains(_box(s), b) for s in symbols) and _near_valve(b, symbols):
                crop = ink[b[1]:b[3] + 1, b[0]:b[2] + 1]
                if _orthogonal_cap(crop, labels, stats, b):
                    reason = "external_actuator_stroke"
            if reason:
                rejected.append({"bbox": list(b), "reason": reason})
            else:
                lines.append(list(b))
        if not lines:
            t["geometry_reason"] = rejected[0]["reason"] if len({r["reason"] for r in rejected}) == 1 else "all_lines_removed"
            t["geometry_removed_lines"] = rejected
            removed.append(t)
            continue
        if rejected:
            t["geometry_before_bbox"] = list(t["bbox"])
            t["geometry_removed_lines"] = rejected
            t["bbox"], t["lines"] = _union(lines), lines
        kept.append(t)

    # Prefer the complete line over a nested fragment even if the fragment's
    # model confidence is higher. A full label and its substring are one object.
    ordered = sorted(kept, key=lambda x: (-_area(_box(x)), str(x.get("id", ""))))
    winners, duplicates = [], []
    for t in ordered:
        b = _box(t)
        host = None
        for a in winners:
            q = _box(a)
            if len(t.get("lines") or [b]) != 1 or len(a.get("lines") or [q]) != 1 or not _same_line(a, t):
                continue
            inter = _intersection(b, q)
            if _area(inter) / max(1, _area(b)) >= 0.95:
                host = a
                break
        if host is None:
            winners.append(t)
        else:
            t["geometry_reason"] = "nested_same_line_fragment"
            t["geometry_merged_into"] = host.get("id")
            host.setdefault("geometry_merged_fragments", []).append(t.get("id"))
            duplicates.append(t)
    winner_ids = {id(t) for t in winners}
    return [t for t in kept if id(t) in winner_ids], removed + duplicates
