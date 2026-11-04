"""Conservative small filled arrowhead proposals from raw ink and a shaft.

These are geometry hypotheses, never symbol or connection verdicts. They are
intended to go through normal S2/C1. ``verified_small_arrow`` is a raw-shape
predicate for a post-class tiny-noise guard; a class label/confidence alone is
not sufficient to bypass that guard.
"""
from __future__ import annotations

import hashlib
import copy

import cv2
import numpy as np

import page_cv as CV


def _cross_profile(ink, axial, centre, horizontal, max_width):
    """The symmetric stroke through the shaft axis, excluding nearby letters."""
    fixed = int(axial)
    lo, hi = int(np.floor(centre)), int(np.ceil(centre))
    limit = ink.shape[0] if horizontal else ink.shape[1]
    if fixed < 0 or fixed >= (ink.shape[1] if horizontal else ink.shape[0]) or lo < 0 or hi >= limit:
        return None
    strip = ink[:, fixed] if horizontal else ink[fixed]
    if not strip[lo] or not strip[hi]:
        return None
    a, b = lo, hi
    while a > 0 and strip[a - 1] and centre - a <= max_width:
        a -= 1
    while b + 1 < limit and strip[b + 1] and b - centre <= max_width:
        b += 1
    # A dot or printed letter touching only one flank is not arrowhead ink.
    radius = min(centre - a, b - centre)
    return (int(np.ceil(centre - radius)), int(np.floor(centre + radius)))


def _find_on_axis(bw, centre, axial_range, horizontal, sign):
    th = CV.SC.text_h
    reach = max(5, round(.75 * th))
    max_len = max(8, round(1.8 * th))
    min_len = max(5, round(.55 * th))
    max_width = max(5, round(1.35 * th))
    out = []
    def span(t):
        p = _cross_profile(bw, t, centre, horizontal, max_width)
        return p, 0 if p is None else p[1] - p[0] + 1
    for base in range(*axial_range):
        cross, peak = span(base)
        if peak < 4 or peak > max_width:
            continue
        behind = [span(base - sign * j)[1] for j in range(2, reach + 2)]
        if not behind or min(behind) == 0:
            continue
        shaft = float(np.median(behind))
        if shaft > 3 or peak < shaft + 2 or sum(v <= shaft + 1 for v in behind) < .8 * len(behind):
            continue
        widths, positions, termination = [], [], None
        for j in range(max_len + 1):
            p, width = span(base + sign * j)
            if width == 0:
                termination = "finite-tip"
                break
            if width > peak + 1:
                termination = "tip-at-cross-line"
                break
            widths.append(width)
            positions.append(p)
        length = len(widths)
        if termination is None or not min_len <= length <= max_len or widths[-1] > peak - 2:
            continue
        # Both flanks converge toward the pointed end, with only raster-sized
        # reversals permitted. Parallel flanges, diamonds and blobs fail here.
        first = np.mean(widths[:max(1, length // 3)])
        last = np.mean(widths[-max(1, length // 3):])
        if first < last + 1.3 or sum(b > a + 1 for a, b in zip(widths, widths[1:])):
            continue
        # Exclude a very long parallel rectangular tab followed by one pixel.
        if sum(v >= peak - 1 for v in widths) > .78 * length:
            continue
        start, stop = sorted((base, base + sign * (length - 1)))
        perp_lo = min(p[0] for p in positions)
        perp_hi = max(p[1] for p in positions)
        # The immediately preceding shoulder can be one raster pixel narrower
        # than the flat base. Include it only inside the same arrow envelope.
        p, width = span(base - sign)
        if shaft + 1 <= width < peak and p and perp_lo <= p[0] <= p[1] <= perp_hi:
            start, stop = sorted((base - sign, base + sign * (length - 1)))
        box = (start, perp_lo, stop, perp_hi) if horizontal else (perp_lo, start, perp_hi, stop)
        out.append({"bbox": list(box), "geometry": "filled-taper-on-shaft", "orientation":
                    ("right" if sign > 0 else "left") if horizontal else ("down" if sign > 0 else "up"),
                    "shaft_width": shaft, "base_width": peak, "tip_width": widths[-1],
                    "termination": termination})
    return out


def _opposed_crossbar_pairs(bw, proposals):
    """Two shaft-backed tapers meet one finite, balanced transverse marker.

    A long process pipe, a flange with one short arm, or two valve halves cannot
    supply this evidence. Both independently observed arrowheads and a narrow
    centred crossbar are retained in metadata, so later guards can verify their
    pixels together. The arm dimensions are relative to the arrow base width.
    """
    out = []
    opposite = {"up": "down", "down": "up", "left": "right", "right": "left"}
    crosses = [p for p in proposals if p["termination"] == "tip-at-cross-line"]
    for i, a in enumerate(crosses):
        ab = a["bbox"]
        vertical = a["orientation"] in ("up", "down")
        # Current independently reviewed boundary-arrow grammar is the pair of
        # vertical shafts ending on one horizontal single-stroke marker. The
        # transposed shape overlaps valve stem/end-bar conventions, so defer it.
        if not vertical:
            continue
        centre = (ab[0] + ab[2]) / 2 if vertical else (ab[1] + ab[3]) / 2
        axis_tip = (ab[3] + 1 if a["orientation"] == "down" else ab[1] - 1 if a["orientation"] == "up"
                    else ab[2] + 1 if a["orientation"] == "right" else ab[0] - 1)
        for b in crosses[i + 1:]:
            if b["orientation"] != opposite[a["orientation"]]:
                continue
            bb = b["bbox"]
            other_centre = (bb[0] + bb[2]) / 2 if vertical else (bb[1] + bb[3]) / 2
            other_tip = (bb[3] + 1 if b["orientation"] == "down" else bb[1] - 1 if b["orientation"] == "up"
                         else bb[2] + 1 if b["orientation"] == "right" else bb[0] - 1)
            if abs(centre - other_centre) > .6 or abs(axis_tip - other_tip) > 1:
                continue
            la = ab[3] - ab[1] + 1 if vertical else ab[2] - ab[0] + 1
            lb = bb[3] - bb[1] + 1 if vertical else bb[2] - bb[0] + 1
            if max(la, lb) > 1.35 * min(la, lb) or abs(a["base_width"] - b["base_width"]) > 1:
                continue
            axis = round((axis_tip + other_tip) / 2)
            row = bw[axis] if vertical else bw[:, axis]
            c = round((centre + other_centre) / 2)
            if c < 0 or c >= len(row) or not row[c]:
                continue
            lo = hi = c
            while lo > 0 and row[lo - 1]:
                lo -= 1
            while hi + 1 < len(row) and row[hi + 1]:
                hi += 1
            width = max(a["base_width"], b["base_width"])
            arms = (c - lo, hi - c)
            # A standalone boundary marker has two comparable arms outside the
            # arrow, unlike an inline valve end bar or a long routing pipe.
            if not (2.5 * width <= min(arms) and max(arms) <= 4.5 * width
                    and max(arms) <= 1.5 * min(arms)):
                continue
            # A valve/flange stem commonly has two parallel pixels across its
            # full length. A drawn boundary marker is one transverse stroke.
            neighbours = [bw[r, lo:hi + 1].mean() for r in (axis - 1, axis + 1)
                          if 0 <= r < bw.shape[0]]
            if any(share >= .7 for share in neighbours):
                continue
            bar = (lo, axis, hi, axis) if vertical else (axis, lo, axis, hi)
            envelope = (min(ab[0], bb[0], bar[0]), min(ab[1], bb[1], bar[1]),
                        max(ab[2], bb[2], bar[2]), max(ab[3], bb[3], bar[3]))
            x0, y0, x1, y1 = envelope
            digest = hashlib.sha256(bw[y0:y1 + 1, x0:x1 + 1].tobytes()).hexdigest()
            for original, partner in ((a, b), (b, a)):
                p = copy.deepcopy(original)
                p["pair_geometry"] = {"kind": "opposed-balanced-crossbar", "partner_bbox": partner["bbox"],
                                      "crossbar_bbox": list(bar), "context_bbox": list(envelope),
                                      "context_sha256": digest}
                out.append(p)
    return out


def detect(bw, regions, exclude=(), profile_kind="pid", allow_cross_line=False):
    """Find small arrow triangles while keeping the original ink untouched."""
    if profile_kind != "pid":
        return []
    th = CV.SC.text_h
    # A 3-pixel erosion removes 1/2-pixel pipe shafts; only filled seed ink
    # remains. It is not used as the final bbox or substituted for original ink.
    core = cv2.erode(bw, np.ones((3, 3), np.uint8))
    n, _, st, centroids = cv2.connectedComponentsWithStats(core, connectivity=8)
    proposals = []
    for i in range(1, n):
        x, y, w, h, area = (int(v) for v in st[i])
        if area < 2 or min(w, h) > 1.4 * th or max(w, h) > 2.4 * th:
            continue
        cx, cy = centroids[i]
        for horizontal in (True, False):
            axis = cy if horizontal else cx
            axial_lo, axial_hi = (x, x + w) if horizontal else (y, y + h)
            axis_choices = sorted(set(round(axis * 2 + j) / 2 for j in (-2, -1, 0, 1, 2)))
            for centre in axis_choices:
                for sign in (-1, 1):
                    proposals.extend(_find_on_axis(bw, centre,
                                      (axial_lo - round(.6 * th), axial_hi + round(.6 * th)), horizontal, sign))
    pair_proposals = _opposed_crossbar_pairs(bw, proposals)
    if not allow_cross_line:
        proposals = [p for p in proposals if p["termination"] == "finite-tip"] + pair_proposals
    kept = []
    for p in sorted(proposals, key=lambda p: (CV.area(p["bbox"]), p["bbox"]), reverse=True):
        b = p["bbox"]
        # A terminating triangle with a one-sided shaft can be separated from
        # pipe marks. A triangle pointing into a cross-line can also be half of
        # a valve; retain those only in diagnostics until that ambiguity has a
        # separately verified compound-shape rule.
        if p["termination"] != "finite-tip" and not allow_cross_line and not p.get("pair_geometry"):
            continue
        if not CV._inside_any(b, regions, 4) or any(CV.inter(b, e) > .5 * CV.area(b) for e in exclude):
            continue
        x0, y0, x1, y1 = b
        if bw[y0:y1 + 1, x0:x1 + 1].mean() < .5:
            continue
        if any(CV.inter(b, q["bbox"]) >= .7 * min(CV.area(b), CV.area(q["bbox"])) for q in kept):
            continue
        p["raw_ink_sha256"] = hashlib.sha256(bw[y0:y1 + 1, x0:x1 + 1].tobytes()).hexdigest()
        kept.append(p)
    # Pixel-scale alternate fits can differ by one endpoint. Bind the evidence
    # to the final retained partner and cover both complete retained heads.
    for p in kept:
        pair = p.get("pair_geometry")
        if not pair:
            continue
        mate = next((q for q in kept if q is not p and q.get("pair_geometry", {}).get("crossbar_bbox")
                     == pair["crossbar_bbox"] and q["orientation"] != p["orientation"]), None)
        if mate is None:
            continue
        pair["partner_bbox"] = list(mate["bbox"])
        b, q, bar = p["bbox"], mate["bbox"], pair["crossbar_bbox"]
        context = (min(b[0], q[0], bar[0]), min(b[1], q[1], bar[1]),
                   max(b[2], q[2], bar[2]), max(b[3], q[3], bar[3]))
        pair["context_bbox"] = list(context)
        x0, y0, x1, y1 = context
        pair["context_sha256"] = hashlib.sha256(bw[y0:y1 + 1, x0:x1 + 1].tobytes()).hexdigest()
    return sorted(kept, key=lambda p: (p["bbox"][1], p["bbox"][0]))


def propose(bw, regions, exclude=(), boxes=(), profile_kind="pid"):
    """Return boxes plus metadata keyed by the exact added raw-ink proposal."""
    original = [tuple(b) for b in boxes]
    if profile_kind != "pid":
        return original, {}
    metadata = {}
    for p in detect(bw, regions, exclude, profile_kind):
        b = tuple(p["bbox"])
        matching = [o for o in original if CV.inter(o, b) > .6 * min(CV.area(o), CV.area(b)) or CV.contains(o, b, 1)]
        if matching:
            # A compound old box may contain both opposed heads plus a letter.
            # Preserve it for its normal class judgment and add each evidenced
            # head, rather than treating both as duplicate fragments upfront.
            if not p.get("pair_geometry"):
                continue
            if any(CV.inter(o, b) / max(1, CV.area(o) + CV.area(b) - CV.inter(o, b)) >= .8 for o in matching):
                continue
        original.append(b)
        metadata[b] = p
    return sorted(original, key=lambda b: (b[1], b[0], b[3], b[2])), metadata


def verified_small_arrow(bw, object_or_box, metadata):
    """Only an unchanged shape-backed arrow hypothesis can bypass tiny noise.

    Recheck original ink, geometry evidence and normal C1 class, rather than
    treating classifier confidence or a tiny box alone as proof of an arrow.
    """
    if not isinstance(metadata, dict) or metadata.get("geometry") != "filled-taper-on-shaft":
        return False
    if isinstance(object_or_box, dict):
        if object_or_box.get("class") != "arrow_head":
            return False
        box = object_or_box.get("start_bbox", object_or_box.get("bbox"))
    else:
        box = object_or_box
    if not box or list(box) != metadata.get("bbox"):
        return False
    x0, y0, x1, y1 = box
    if not (0 <= x0 <= x1 < bw.shape[1] and 0 <= y0 <= y1 < bw.shape[0]):
        return False
    raw_hash = hashlib.sha256(bw[y0:y1 + 1, x0:x1 + 1].tobytes()).hexdigest()
    pair = metadata.get("pair_geometry")
    if pair:
        x0, y0, x1, y1 = pair.get("context_bbox", [-1, -1, -1, -1])
        if not (pair.get("kind") == "opposed-balanced-crossbar" and 0 <= x0 <= x1 < bw.shape[1]
                and 0 <= y0 <= y1 < bw.shape[0]):
            return False
        if hashlib.sha256(bw[y0:y1 + 1, x0:x1 + 1].tobytes()).hexdigest() != pair.get("context_sha256"):
            return False
    if metadata.get("termination") == "tip-at-cross-line" and not pair:
        return False
    return (raw_hash == metadata.get("raw_ink_sha256") and metadata.get("base_width", 0) >= metadata.get("tip_width", 0) + 2
            and metadata.get("termination") in ("finite-tip", "tip-at-cross-line")
            and 0 < metadata.get("shaft_width", 0) <= 3)


def preserve_distinct_shape(a, b):
    """Pre-class dedupe must not swallow a shape-backed head into equipment.

    Normal class judgment is still required. Identical or nearly identical
    boxes remain duplicates; only a distinct, smaller raw shape is protected.
    The actual hash/class check belongs to ``verified_small_arrow`` after C1.
    """
    for shape, other in ((a, b), (b, a)):
        metadata = shape.get("shape_proposal") or {}
        sb = shape.get("start_bbox", shape.get("bbox"))
        ob = other.get("bbox")
        if metadata.get("geometry") != "filled-taper-on-shaft" or not sb or list(sb) != metadata.get("bbox") or not ob:
            continue
        overlap = CV.inter(sb, ob)
        shape_area, other_area = CV.area(sb), CV.area(ob)
        if other_area > 2 * shape_area and overlap > .6 * shape_area:
            return True
        # The two independently supported opposed heads must remain separate
        # even though their boxes both fall within a compound arrow/text box.
        pair = metadata.get("pair_geometry") or {}
        if pair and list(ob) == pair.get("partner_bbox"):
            return True
    return False


def separates_existing_ink(bw, shape, other):
    """Raw proposal survives pre-class dedupe when its arrow ink is disjoint.

    A large classless candidate may expand across an unrelated terminal arrow.
    Exact detection metadata and the original pixels prove that these are
    distinct proposals; C1 still determines each class in the normal pipeline.
    """
    metadata = shape.get("shape_proposal") or {}
    body = shape.get("start_bbox", shape.get("bbox"))
    ob = other.get("start_bbox", other.get("bbox"))
    if not body or not ob or not verified_small_arrow(bw, body, metadata):
        return False
    if CV.area(ob) <= 2 * CV.area(body):
        return False
    return CV.inter(body, ob) < .1 * CV.area(body)


def refined_compounds(bw, objects):
    """Two normally classified opposed heads supersede one compound arrow box.

    Both individual heads must pass C1 and raw geometry verification. Until
    then, the existing larger candidate remains available. This does not split
    or reclassify a valve, equipment, or an unverified glyph fragment.
    """
    verified = [o for o in objects if verified_small_arrow(bw, o, o.get("shape_proposal"))
                and (o.get("shape_proposal") or {}).get("pair_geometry")]
    drop_ids = set()
    notes = []
    for a in verified:
        meta = a["shape_proposal"]
        partner = meta["pair_geometry"]["partner_bbox"]
        b = next((o for o in verified if o is not a and list(o.get("start_bbox", o["bbox"])) == partner), None)
        if b is None:
            continue
        ab, bb = a["bbox"], b["bbox"]
        for o in objects:
            if o is a or o is b or o.get("class") != "arrow_head" or o.get("shape_proposal"):
                continue
            box = o["bbox"]
            if (CV.contains(box, ab, 1) and CV.contains(box, bb, 1)
                    and CV.area(box) > 2 * max(CV.area(ab), CV.area(bb))):
                drop_ids.add(id(o))
                notes.append({"cand": o.get("cand", o.get("id")),
                              "reason": "two individually classified opposed arrowheads supersede compound arrow/text box"})
    kept = [o for o in objects if id(o) not in drop_ids]
    dropped = [o for o in objects if id(o) in drop_ids]
    return kept, dropped, notes


# Pipeline integration name: after C1, before generic same-class containment.
postclass_compounds = refined_compounds
