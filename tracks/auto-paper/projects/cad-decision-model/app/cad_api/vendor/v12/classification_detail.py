"""Original-pixel views for ambiguous compact rectangular symbol bodies.

The geometry only selects a bounded second class question.  No class is inferred
from a box, text, or this module.  The caller keeps its normal complete-legend
A/B agreement and confidence policy before accepting any new model answer.
"""
from __future__ import annotations

import hashlib

import cv2
import numpy as np


BOX_QUESTION = (
    "Which legend class matches the selected symbol BODY in detail? The original dark pixels are enlarged "
    "without changing them. Context locates the same selection but nearby text and valves outside the selected "
    "rectangle belong to other objects. Inspect the border and internal letters: a hand switch contains a full "
    "inner circle and a horizontal divider; a solenoid has an inner square as well as an outer square; a controller "
    "has a horizontal divider; a tag box has a single border containing a letter or letters. Match the actual visible "
    "shape to one of ALL legend classes. Distinguish a letter C from an enclosing circle: a circle is complete and "
    "surrounds internal text, whereas letter C is open at the right. Letter L and letter C alone have no inner "
    "enclosing outline and no horizontal internal divider. Choose other for an incomplete body or several separate symbols."
)


def _box(value, shape):
    if not isinstance(value, (list, tuple)) or len(value) != 4:
        return None
    if any(type(v) not in (int, np.int32, np.int64) for v in value):
        return None
    x0, y0, x1, y1 = map(int, value)
    if not (0 <= x0 <= x1 < shape[1] and 0 <= y0 <= y1 < shape[0]):
        return None
    return x0, y0, x1, y1


def closed_box_extent(bw, box, text_h):
    """Find four near-continuous border strokes inside a compact original box.

    Only top/bottom raster-sized attachments may be trimmed.  The left and
    right border must coincide with the candidate, so a C, a partial box, an
    internal small square, or a pair of pipe rails cannot provide this proof.
    """
    b = _box(box, bw.shape)
    if b is None or text_h <= 0:
        return None
    x0, y0, x1, y1 = b
    w, h = x1 - x0 + 1, y1 - y0 + 1
    if not (max(7, .7 * text_h) <= min(w, h) and max(w, h) <= 3 * text_h):
        return None
    ink = bw[y0:y1 + 1, x0:x1 + 1] != 0
    trim = max(1, round(.35 * text_h))
    # Full-width rows are border candidates, not a short glyph's horizontal.
    rows = np.flatnonzero((ink.mean(axis=1) >= .94) & ink[:, 0] & ink[:, -1])
    top = [int(r) for r in rows if r <= trim]
    bottom = [int(r) for r in rows if r >= h - 1 - trim]
    if not top or not bottom:
        return None
    a, z = min(top), max(bottom)
    if z - a + 1 < max(7, .7 * text_h) or (z - a + 1) / h < .65:
        return None
    sides = ink[a:z + 1, (0, -1)]
    if np.any(sides.mean(axis=0) < .94):
        return None
    # The body must contain interior ink and white space; solid blocks and an
    # empty routing loop do not get an additional symbol class question.
    inner = ink[a + 1:z, 1:-1]
    if inner.size < 9 or not .08 <= float(inner.mean()) <= .78:
        return None
    return x0, y0 + a, x1, y0 + z


def recheck_evidence(page, bw, obj, kind, text_h):
    """Return raw-view evidence for uncertain box-like classes, or None.

    A high-confidence existing classification, equipment, valve, non-P&ID
    sheet, and a rectangle without a prior symbol judgment stay untouched.
    Metadata names geometry only and deliberately contains no target class.
    """
    if kind != "pid" or obj.get("class") not in {"hand_switch", "solenoid", "controller"}:
        return None
    confidence = obj.get("class_confidence")
    if not isinstance(confidence, (int, float)) or not 0 <= confidence < .35:
        return None
    s2 = obj.get("s2") or {}
    if s2.get("symbol", 0) < .7 or (obj.get("class_probs") or {}).get("other", 0) < .20:
        return None
    if page.ndim != 2 or bw.ndim != 2 or page.shape != bw.shape:
        return None
    body = closed_box_extent(bw, obj.get("bbox"), text_h)
    if body is None:
        return None
    x0, y0, x1, y1 = body
    # A squat rectangular body is where square/circle exemplars can dominate
    # the low-resolution letter silhouette.  Nearly square HS/S enclosures
    # already match their normal exemplars and are left to the existing C1.
    if x1 - x0 + 1 < 1.25 * (y1 - y0 + 1):
        return None
    margin = max(3, round(.55 * text_h))
    return {"kind": "compact-closed-rectangle-detail", "body_bbox": list(body),
            "candidate_bbox": list(obj["bbox"]),
            "context_bbox": [x0 - margin, y0 - margin, x1 + margin, y1 + margin],
            "raw_gray_sha256": hashlib.sha256(page[y0:y1 + 1, x0:x1 + 1].tobytes()).hexdigest(),
            "raw_ink_sha256": hashlib.sha256(bw[y0:y1 + 1, x0:x1 + 1].tobytes()).hexdigest()}


def detail_view(page, evidence):
    """Enlarge the unchanged, hash-bound body; never paint over its pixels."""
    b = _box(evidence.get("body_bbox"), page.shape)
    if b is None:
        return None
    x0, y0, x1, y1 = b
    crop = page[y0:y1 + 1, x0:x1 + 1]
    if hashlib.sha256(crop.tobytes()).hexdigest() != evidence.get("raw_gray_sha256"):
        return None
    h, w = crop.shape
    scale = min(32., 448 / max(w, h))
    crop = cv2.resize(crop, (round(w * scale), round(h * scale)), interpolation=cv2.INTER_NEAREST)
    h, w = crop.shape
    out = np.full((max(280, h + 30), max(280, w + 30)), 255, np.uint8)
    a, b = (out.shape[0] - h) // 2, (out.shape[1] - w) // 2
    out[a:a + h, b:b + w] = crop
    return cv2.cvtColor(out, cv2.COLOR_GRAY2BGR)
