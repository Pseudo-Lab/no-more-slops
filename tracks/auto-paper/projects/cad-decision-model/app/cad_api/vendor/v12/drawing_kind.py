"""Conservative drawing-profile review using separate raw content views.

No model calls, page identifiers, ground truth or size-based profile assignment
live here. The pipeline supplies normal A/B visual judgments for several broad
original-image crops only when its whole-sheet S0 decision is ambiguous.
"""
from __future__ import annotations

import math

import cv2
import numpy as np

import page_cv as CV

KINDS = ("logic", "pid", "other")
CONFIDENT_WHOLE = .80
WHOLE_MARGIN = .35
STRONG_CROP = .78
STRONG_CROP_MARGIN = .50

REVIEW_QUESTION = (
    "`region` is a broad crop from the original engineering drawing, shown larger than the whole sheet. "
    "`page` shows its location. Which kind of drawing is the cropped drawing content? Use the symbols and "
    "the way the drawn lines connect them. Distinguish pipes with valves and tagged instrument bubbles "
    "from logic gates, timers, memories and lamps. Choose other for a legend, notes, title block or table."
)


def valid_distribution(value):
    return (isinstance(value, dict) and set(value) == set(KINDS)
            and all(type(p) in (int, float) and math.isfinite(p) and 0 <= p <= 1 for p in value.values())
            and abs(sum(value.values()) - 1) <= .02)


def winner_and_margin(probs):
    if not valid_distribution(probs):
        return None, 0., 0.
    ordered = sorted(probs.items(), key=lambda item: (-item[1], item[0]))
    return ordered[0][0], ordered[0][1], ordered[0][1] - ordered[1][1]


def needs_review(probs):
    """Only ambiguous whole-sheet answers request additional visual evidence."""
    answer, confidence, margin = winner_and_margin(probs)
    return answer is None or confidence < CONFIDENT_WHOLE or margin < WHOLE_MARGIN


def _iou(a, b):
    z = CV.inter(a, b)
    return z / max(1, CV.area(a) + CV.area(b) - z)


def select_review_crops(bw, exclude=(), frame=None, max_views=3):
    """Select broad, spatially distinct raw content crops without choosing kind.

    Grid content crops avoid selecting only a single interesting valve/circle.
    An integral ink map ranks them after removing only known tables for ranking;
    the actual returned rectangle always refers to the unchanged original page.
    Connected layout regions provide alternatives on very sparse sheets.
    """
    H, W = bw.shape
    full = (0, 0, W - 1, H - 1)
    f = tuple(frame) if frame is not None else full
    if len(f) != 4 or not (0 <= f[0] <= f[2] < W and 0 <= f[1] <= f[3] < H):
        f = full
    x0, y0, x1, y1 = f
    # Prevent a frame stroke by itself from becoming a high-score content crop.
    pad = max(2, round(.012 * min(x1 - x0 + 1, y1 - y0 + 1)))
    x0, y0, x1, y1 = x0 + pad, y0 + pad, x1 - pad, y1 - pad
    if x1 <= x0 or y1 <= y0:
        return []
    mask = (bw > 0).astype(np.uint8)
    for b in exclude:
        a, c, u, v = (int(z) for z in b)
        mask[max(0, c):min(H, v + 1), max(0, a):min(W, u + 1)] = 0
    integral = cv2.integral(mask)
    def ink(b):
        a, c, u, v = b
        return int(integral[v + 1, u + 1] - integral[c, u + 1] - integral[v + 1, a] + integral[c, a])
    fw, fh = x1 - x0 + 1, y1 - y0 + 1
    candidates = []
    # Four broad quadrants resolve detail lost in a sheet-sized thumbnail, while
    # permitting two independent pieces of evidence from different locations.
    for iy in range(2):
        for ix in range(2):
            box = (x0 + ix * fw // 2, y0 + iy * fh // 2,
                   x0 + (ix + 1) * fw // 2 - 1, y0 + (iy + 1) * fh // 2 - 1)
            candidates.append((box, "content-grid"))
    # Sparse diagrams can occupy a fraction of the sheet. Their broad layout
    # cluster is another view, provided it cannot displace all independent grid
    # crops or shrink the view down to a single letter or symbol.
    for b in CV.layout_regions(mask, min_area=max(100, round(.03 * fw * fh))):
        if CV.area(b) < .12 * fw * fh or CV.area(b) > .65 * fw * fh:
            continue
        if min(b[2] - b[0] + 1, b[3] - b[1] + 1) < .2 * min(fw, fh):
            continue
        if b[0] >= x0 and b[1] >= y0 and b[2] <= x1 and b[3] <= y1:
            candidates.append((tuple(b), "layout-region"))
    ranked = []
    for box, source in candidates:
        if any(CV.inter(box, t) > .4 * CV.area(box) for t in exclude):
            continue
        count = ink(box)
        if count < max(30, .0025 * CV.area(box)):
            continue
        # Raw ink count favours substantial drawing content, while a cap keeps
        # a dense table or paragraph from winning solely through glyph density.
        density = count / CV.area(box)
        score = min(density, .12) * math.sqrt(CV.area(box))
        ranked.append((score, box, source, count, density))
    selected = []
    for score, box, source, count, density in sorted(ranked, key=lambda r: (-r[0], r[1])):
        if any(CV.inter(box, r["bbox"]) > .25 * min(CV.area(box), CV.area(r["bbox"])) for r in selected):
            continue
        selected.append({"id": f"kind-region-{len(selected) + 1}", "bbox": list(box), "source": source,
                         "ink_pixels": count, "ink_density": round(density, 6)})
        if len(selected) >= max_views:
            break
    return selected


def paired_review(a, b):
    """Require valid paired responses and consistent order-reversed answers."""
    if not valid_distribution(a) or not valid_distribution(b):
        return None
    ka, pa, ma = winner_and_margin(a)
    kb, pb, mb = winner_and_margin(b)
    if ka != kb or min(pa, pb) < .70 or min(ma, mb) < .35:
        return None
    return {k: (a[k] + b[k]) / 2 for k in KINDS}


def resolve_review(initial_probs, crop_reviews):
    """Switch only on strong agreeing evidence from at least two crops.

    A single crop, invalid/missing A/B response, other-only views or conflicting
    strong profile evidence preserve the whole-sheet answer. Text height never
    overrides a model decision in this helper.
    """
    initial, _, _ = winner_and_margin(initial_probs)
    result = {"answer": initial, "changed": False, "reviewed": needs_review(initial_probs),
              "reason": "whole-sheet answer preserved", "support": [], "conflicts": []}
    if not result["reviewed"]:
        result["reason"] = "whole-sheet answer is already confident"
        return result
    votes = []
    ids = set()
    for r in crop_reviews:
        rid = r.get("id")
        if rid in ids or rid is None:
            continue
        ids.add(rid)
        probs = paired_review(r.get("A"), r.get("B"))
        kind, confidence, margin = winner_and_margin(probs)
        if kind not in ("logic", "pid") or confidence < STRONG_CROP or margin < STRONG_CROP_MARGIN:
            continue
        bbox = r.get("bbox")
        if not bbox or len(bbox) != 4:
            continue
        votes.append({"id": rid, "kind": kind, "confidence": confidence, "margin": margin, "bbox": bbox})
    kinds = {v["kind"] for v in votes}
    if len(kinds) > 1:
        result["conflicts"] = votes
        result["reason"] = "strong crop answers disagree; whole-sheet answer preserved"
        return result
    independent = []
    for v in votes:
        if any(CV.inter(v["bbox"], q["bbox"]) > .25 * min(CV.area(v["bbox"]), CV.area(q["bbox"])) for q in independent):
            continue
        independent.append(v)
    if len(independent) < 2:
        result["reason"] = "fewer than two independent strong paired crop answers"
        result["support"] = independent
        return result
    result["answer"] = independent[0]["kind"]
    result["changed"] = result["answer"] != initial
    result["support"] = independent
    result["reason"] = "independent broad content crops agree with strong paired confidence"
    return result
