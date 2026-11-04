"""Canonical route checks and observed marker positions for P&ID review.

These helpers change only the additional review's crop/markers. They never
change a graph route, body, mask, model threshold, or acceptance decision.
"""
from __future__ import annotations

import copy
import hashlib
import math

import numpy as np

PORT_REASONS = {"instrument_terminal_port", "inline_equipment_port_flange_gap"}


def _on_segment(point, a, b, tolerance=1e-6):
    dx, dy = b[0]-a[0], b[1]-a[1]
    length2 = dx*dx+dy*dy
    if not length2:
        return math.dist(point, a) <= tolerance
    t = ((point[0]-a[0])*dx+(point[1]-a[1])*dy)/length2
    return (-tolerance <= t <= 1+tolerance
            and math.dist(point, (a[0]+t*dx, a[1]+t*dy)) <= tolerance)


def deduplicate_spans(details):
    """Keep every turn check; omit only straight spans it exactly covers.

    Exact collinear containment is required. Nearby parallel strokes, partial
    overlap, a shortcut across a corner, and a different inferred route remain
    independent checks. Call before asking questions, not to erase a rejection.
    """
    out = copy.deepcopy(details)
    turns = [item for item in out if item.get("kind") == "junction" and len(item.get("path", [])) >= 3]
    kept = []
    for item in out:
        path = item.get("path", [])
        owner = None
        if item.get("kind") == "span" and len(path) == 2:
            for turn in turns:
                if any(_on_segment(path[0], a, b) and _on_segment(path[1], a, b)
                       for a, b in zip(turn["path"], turn["path"][1:])):
                    owner = turn
                    break
        if owner is None:
            kept.append(item)
        else:
            owner.setdefault("covered_span_paths", []).append(path)
    return kept


def omit_duplicate_port_reviews(details):
    """Body attachment is K6 evidence; keep other K5 route evidence present.

    The frozen port review tests an outside anchor against another outside
    position, duplicating a span rather than observing the actual body contact.
    Omit it only when another non-port route check exists. The caller must keep
    both original attachment judgments mandatory for inferred relations.
    """
    other = [item for item in details if item.get("reason") not in PORT_REASONS
             and len(item.get("path", [])) >= 2]
    if not other:
        return copy.deepcopy(details)
    return copy.deepcopy([item for item in details if item.get("reason") not in PORT_REASONS])


def _axis(direction):
    dx, dy = direction
    if not (dx or dy):
        return None
    if abs(dx) >= 4*abs(dy):
        return (1 if dx > 0 else -1, 0)
    if abs(dy) >= 4*abs(dx):
        return (0, 1 if dy > 0 else -1)
    return None


def observed_arm_detail(gray, item, text_h=9, symbols=()):
    """Move a white/gap marker onto its uniquely observed original route arm.

    A gap review may already extend beyond its actual gap. Preserve that exact
    ``original_gap_path`` and choose visible arm pixels beyond both gap ends.
    In particular a marker before a nearby body can fall into a regular dash
    gap even though a three-pixel neighbourhood contains ink. Every fresh
    centre itself and three collinear pixels must be observed. Markers never
    enter bodies or switch to another parallel arm. No fresh verdict is implied.
    """
    if gray.ndim != 2 or not math.isfinite(text_h) or text_h <= 0:
        raise ValueError("gray must be two dimensional and text_h positive")
    if item.get("reason") in PORT_REASONS:
        return None
    reviewed = [list(map(int, p)) for p in item.get("path", [])]
    if len(reviewed) < 2:
        return None
    core = [list(map(int, p)) for p in item.get("original_gap_path", reviewed)]
    if len(core) < 2:
        return None
    h, w = gray.shape
    raw = gray < 200
    blocked = np.zeros_like(raw)
    for symbol in symbols:
        x0, y0, x1, y1 = map(int, symbol["bbox"])
        blocked[max(0, y0):min(h, y1+1), max(0, x0):min(w, x1+1)] = True

    def outward(first):
        reference = core[0] if first else core[-1]
        matches = [i for i, p in enumerate(reviewed) if p == reference]
        if first and matches and matches[0] > 0:
            neighbour = reviewed[matches[0]-1]
            vector = (neighbour[0]-reference[0], neighbour[1]-reference[1])
        elif not first and matches and matches[-1] < len(reviewed)-1:
            neighbour = reviewed[matches[-1]+1]
            vector = (neighbour[0]-reference[0], neighbour[1]-reference[1])
        else:
            neighbour = core[1] if first else core[-2]
            vector = (reference[0]-neighbour[0], reference[1]-neighbour[1])
        return reference, _axis(vector)

    def anchor(first):
        old = reviewed[0] if first else reviewed[-1]
        reference, axis = outward(first)
        if axis is None:
            return None
        dx, dy = axis
        old_step = (old[0]-reference[0])*dx+(old[1]-reference[1])*dy
        candidates = []
        # Short outward travel includes the nearest complete dash, while the
        # exact core interval and all its turns stay between the fresh marks.
        for step in range(0, max(4, round(2.2*text_h))+1):
            cx, cy = reference[0]+dx*step, reference[1]+dy*step
            if not (0 <= cx < w and 0 <= cy < h) or blocked[cy, cx]:
                break
            for transverse in range(-2, 3):
                x, y = cx-dy*transverse, cy+dx*transverse
                points = [(x+dx*k, y+dy*k) for k in (-1, 0, 1)]
                if all(0 <= px < w and 0 <= py < h and raw[py, px] and not blocked[py, px]
                       for px, py in points):
                    intensity = float(np.mean([gray[py, px] for px, py in points]))
                    candidates.append((abs(step-old_step), abs(transverse), intensity, transverse, x, y))
        if not candidates:
            return None
        aligned = [c for c in candidates if c[1] == 0]
        if aligned:
            candidates = aligned
        else:
            nearest = min(c[1] for c in candidates)
            candidates = [c for c in candidates if c[1] == nearest]
            # A route between two parallel arms has no unique raster correction.
            if any(c[3] < 0 for c in candidates) and any(c[3] > 0 for c in candidates):
                return None
        best = min(candidates)
        return [best[-2], best[-1]]

    a, b = anchor(True), anchor(False)
    if a is None or b is None or math.dist(a, b) < 12:
        return None
    if a == reviewed[0] and b == reviewed[-1]:
        return None
    result = copy.deepcopy(item)
    for key in ("p_yes", "confidence", "rechecks"):
        result.pop(key, None)
    path = [a]+core+[b]
    result["path"] = [p for i, p in enumerate(path) if i == 0 or p != path[i-1]]
    result.update(a=a, b=b, original_marker_path=reviewed,
                  original_markers=[reviewed[0], reviewed[-1]],
                  marker_geometry="uniquely_observed_original_arm_pixels",
                  requires_new_paired_line_check=True)
    xs, ys = zip(*result["path"])
    pad = max(18, round(5*text_h))
    old = item.get("bbox", [min(xs), min(ys), max(xs), max(ys)])
    result["bbox"] = [max(0, min(old[0], min(xs)-pad)), max(0, min(old[1], min(ys)-pad)),
                      min(w-1, max(old[2], max(xs)+pad)), min(h-1, max(old[3], max(ys)+pad))]
    x0, y0, x1, y1 = result["bbox"]
    result["raw_sha256"] = hashlib.sha256(np.ascontiguousarray(gray[y0:y1+1, x0:x1+1]).tobytes()).hexdigest()
    return result
