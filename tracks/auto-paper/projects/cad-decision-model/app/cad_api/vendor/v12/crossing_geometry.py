"""Raw detail views of separated crossings already traversed by a CV route.

These are review hypotheses, not new connections. Only a bridge returned by
``page_cv.find_bridges`` and already present in a traced net is eligible. The
perpendicular wire remains a separate component, and no pixels are synthesized.
The caller must still obtain normal local-route and both-endpoint judgments.
"""
from __future__ import annotations

import hashlib
import math

import cv2
import numpy as np

import page_cv as CV
from connection_geometry import distance_to_segment


def _key(bridge):
    if len(bridge) != 2 or any(len(p) != 2 for p in bridge):
        return None
    a, b = sorted(tuple(int(v) for v in p) for p in bridge)
    return a, b


def _near_path(point, path, tolerance):
    return any(distance_to_segment(point, a, b) <= tolerance
               for a, b in zip(path, path[1:]))


def _traverses(path, a, b, raw_mask, tolerance):
    """Both gap ends and the blank corridors must lie on the same route."""
    if not path or len(path) < 2 or not all(_near_path(p, path, tolerance) for p in (a, b)):
        return False
    steps = max(1, round(math.dist(a, b)))
    blanks = []
    for k in range(1, steps):
        p = [round(a[j] + (b[j] - a[j]) * k / steps) for j in (0, 1)]
        if not raw_mask[p[1], p[0]]:
            blanks.append(p)
    # A continuous junction or a route along the perpendicular wire is not a
    # traversal of the opposed interrupted arms.
    if len(blanks) < 2 or not all(_near_path(p, path, tolerance) for p in blanks):
        return False
    dx, dy = b[0] - a[0], b[1] - a[1]
    length = math.hypot(dx, dy)
    for p in (a, b):
        aligned = False
        for c, d in zip(path, path[1:]):
            vx, vy = d[0] - c[0], d[1] - c[1]
            vl = math.hypot(vx, vy)
            if vl and abs((dx * vx + dy * vy) / (length * vl)) >= .94:
                aligned |= distance_to_segment(p, c, d) <= tolerance
        if not aligned:
            return False
    return True


def _arm_marker(raw_mask, endpoint, axis, direction, span, path, tolerance):
    """Place a marker on original arm ink, away from the blank crossing gap."""
    H, W = raw_mask.shape
    farthest, length = None, 0
    for step in range(span + 1):
        p = list(endpoint)
        p[axis] += direction * step
        if not (0 <= p[0] < W and 0 <= p[1] < H):
            break
        choices = []
        for offset in (0, -1, 1):
            q = p.copy()
            q[1 - axis] += offset
            if (0 <= q[0] < W and 0 <= q[1] < H and raw_mask[q[1], q[0]]
                    and _near_path(q, path, tolerance)):
                choices.append(q)
        if not choices:
            break
        farthest, length = choices[0], step
    return farthest, length


def _crossing_point(labels, a, b, la, lb):
    """Locate independent crossing ink strictly between the gap endpoints."""
    axis = 0 if a[1] == b[1] else 1
    cross = []
    for value in range(a[axis] + 1, b[axis]):
        p = list(a)
        p[axis] = value
        for offset in (0, -1, 1):
            q = p.copy()
            q[1 - axis] += offset
            if not (0 <= q[0] < labels.shape[1] and 0 <= q[1] < labels.shape[0]):
                continue
            label = int(labels[q[1], q[0]])
            if label and label not in (la, lb):
                cross.append((q, label))
                break
    if not cross:
        return None
    point, label = cross[len(cross) // 2]
    # There must be empty separation on both sides. The crossing wire cannot
    # touch either interrupted arm, including through a junction dot.
    if point[axis] <= a[axis] + 1 or point[axis] >= b[axis] - 1:
        return None
    return point, label


def checkpoints(raw_mask, path, bridges, crossings=None, labels=None, text_h=None):
    """Return detail metadata only for separated crossings used by ``path``.

    ``raw_mask`` must be the original CV.wire_mask, before inferred tee pixels.
    ``bridges`` is the existing net's two-point bridge list. For efficient batch
    use, supply the original component ``labels`` and page-level ``crossings``
    from CV.find_bridges(raw_mask, labels), computed once at the current CV scale.
    Omitting them computes the same CV hypotheses without changing the mask.

    Every result has raw-image ``a``/``b`` arm markers, inclusive ``bbox``, a
    straight detail ``path``, canonical ``bridge``, ``crossing_point`` and axis,
    three distinct component labels, and a crop ``raw_sha256``. These fields
    identify a normal A/B review crop; they never represent an accepted link.
    """
    if raw_mask.ndim != 2:
        raise ValueError("raw_mask must be a two-dimensional original ink mask")
    raw_mask = (raw_mask != 0).astype(np.uint8)
    if labels is None:
        _, labels = cv2.connectedComponents(raw_mask, connectivity=8)
    elif labels.shape != raw_mask.shape:
        raise ValueError("labels and raw_mask must have the same shape")
    th = float(CV.SC.text_h if text_h is None else text_h)
    if not math.isfinite(th) or th <= 0:
        raise ValueError("text_h must be positive and finite")
    if crossings is None:
        crossings = CV.find_bridges(raw_mask, labels, max_gap=max(8, round(24 * th / 18)),
                                    arm=max(3, round(6 * th / 18)))
    eligible = {}
    for la, lb, a, b in crossings:
        key = _key((a, b))
        if key is not None:
            eligible[key] = (int(la), int(lb)) if tuple(a) <= tuple(b) else (int(lb), int(la))
    H, W = raw_mask.shape
    span, minimum_arm = max(8, round(th)), max(3, round(th / 3))
    pad, tolerance = max(8, round(th)), 2
    out, seen = [], set()
    for bridge in bridges:
        key = _key(bridge)
        if key is None or key in seen or key not in eligible:
            continue
        a, b = key
        if not all(0 <= p[0] < W and 0 <= p[1] < H for p in (a, b)):
            continue
        # find_bridges produces exactly axis-aligned endpoint pairs.
        if (a[0] == b[0]) == (a[1] == b[1]):
            continue
        if not _traverses(path, a, b, raw_mask, tolerance):
            continue
        la, lb = eligible[key]
        if not la or not lb or la == lb:
            continue
        crossing = _crossing_point(labels, a, b, la, lb)
        if crossing is None:
            continue
        axis = 0 if a[1] == b[1] else 1
        marker_a, length_a = _arm_marker(raw_mask, a, axis, -1, span, path, tolerance)
        marker_b, length_b = _arm_marker(raw_mask, b, axis, 1, span, path, tolerance)
        if min(length_a, length_b) < minimum_arm:
            continue
        xs, ys = zip(marker_a, marker_b)
        bbox = [max(0, min(xs) - pad), max(0, min(ys) - pad),
                min(W - 1, max(xs) + pad), min(H - 1, max(ys) + pad)]
        x0, y0, x1, y1 = bbox
        crop = np.ascontiguousarray(raw_mask[y0:y1 + 1, x0:x1 + 1])
        digest = hashlib.sha256(np.asarray(crop.shape, np.int64).tobytes() + crop.tobytes()).hexdigest()
        point, lc = crossing
        out.append({"kind": "separated_crossing", "a": marker_a, "b": marker_b,
                    "path": [marker_a, marker_b], "bbox": bbox,
                    "bridge": [list(a), list(b)], "crossing_point": list(point),
                    "crossing_axis": "vertical" if axis == 0 else "horizontal",
                    "component_labels": [la, lb, lc], "raw_sha256": digest})
        seen.add(key)
    return sorted(out, key=lambda item: tuple(tuple(p) for p in item["bridge"]))
