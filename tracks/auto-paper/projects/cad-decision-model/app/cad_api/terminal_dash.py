"""Additional raw-geometry hypotheses for short P&ID signal branches.

The frozen extractor can omit the sole dash between a control body and a
filled junction dot. This module supplies that missing gap as a candidate to
the existing K5 route and K6 endpoint judges. It never paints a wire, changes
an object, or accepts a relation.
"""
from __future__ import annotations

import hashlib
import math
from collections import defaultdict

import cv2
import numpy as np


def _eligible_body(symbol, text_h):
    kind = str(symbol.get("class", ""))
    confidence = symbol.get("class_confidence")
    if not (kind.startswith("instrument/") or kind in {"hand_switch", "controller"}):
        return False
    if type(confidence) not in (int, float) or not math.isfinite(confidence) or confidence < .65:
        return False
    box = symbol.get("bbox")
    if not box or len(box) != 4:
        return False
    return min(box[2]-box[0]+1, box[3]-box[1]+1) >= 2*text_h


def _body_contact(point, direction, symbols, erase, text_h):
    """Find a unique central body side behind this terminal dash."""
    x, y = point
    dx, dy = direction
    found = []
    for symbol in symbols:
        if not _eligible_body(symbol, text_h):
            continue
        x0, y0, x1, y1 = map(int, symbol["bbox"])
        if dx:
            if not y0+.3*(y1-y0) <= y <= y1-.3*(y1-y0):
                continue
            edge = x1 if dx > 0 else x0
            distance = (x-edge)*dx
            side, contact = ("right" if dx > 0 else "left"), [edge, y]
        else:
            if not x0+.3*(x1-x0) <= x <= x1-.3*(x1-x0):
                continue
            edge = y1 if dy > 0 else y0
            distance = (y-edge)*dy
            side, contact = ("bottom" if dy > 0 else "top"), [x, edge]
        if erase+1 <= distance <= erase+2:
            found.append((symbol, side, contact))
    return found[0] if len(found) == 1 else None


def _filled_junction(mask, gray, labels, label, point, direction, text_h):
    """A filled dot on the same arm distinguishes a junction from a crossing."""
    x, y = point
    dx, dy = direction
    h, w = mask.shape
    radius = max(1, round(text_h/9))
    along_radius = max(2, round(text_h/5))
    span = max(4, round(.5*text_h))
    for step in range(max(4, round(text_h))):
        cx, cy = x+dx*step, y+dy*step
        if not (radius <= cx < w-radius and radius <= cy < h-radius):
            break
        if int(labels[cy, cx]) != label:
            break
        if gray[cy, cx] >= 128:
            continue
        # A compact dark patch must extend along the terminal direction as
        # well as across it. A three-pixel-thick solid pipe is still a crossing,
        # so two/three adjacent horizontal sections are insufficient evidence
        # for a dot at the end of a vertical signal dash.
        count = 0
        for offset in range(-along_radius, along_radius+1):
            px, py = cx+dx*offset, cy+dy*offset
            points = [(px-dy*k, py+dx*k) for k in range(-radius, radius+1)]
            if all(0 <= qx < w and 0 <= qy < h and labels[qy, qx] == label
                   and gray[qy, qx] < 128 for qx, qy in points):
                count += 1
        if count >= max(4, math.ceil(.8*(2*along_radius+1))):
            # The observed component must also carry perpendicular drawn ink
            # beyond the dot, rather than being an isolated filled speck.
            for sign in (-1, 1):
                arm = [(cx-dy*sign*k, cy+dx*sign*k) for k in range(1, span+1)]
                if all(0 <= qx < w and 0 <= qy < h and labels[qy, qx] == label
                       and mask[qy, qx] for qx, qy in arm):
                    fx, fy = arm[-1]
                    outside_thickness = sum(0 <= fx+dx*k < w and 0 <= fy+dy*k < h
                                            and gray[fy+dy*k, fx+dx*k] < 128
                                            for k in range(-along_radius, along_radius+1))
                    # A filled dot bulges beyond its outgoing arm. A uniformly
                    # thick solid pipe may have a dark 5x5 patch everywhere,
                    # but that cannot turn a crossing signal into a junction.
                    if count >= outside_thickness+1:
                        return [cx, cy]
    return None


def propose(gray, mask, symbols, *, cv, erase=2, text_h=9, obstacles=None, exclude=()):
    """Return isolated dash-to-junction gap hypotheses, with unchanged inputs.

    Both endpoint components must be observed in ``mask``. The junction's net
    must contain at least three uniform, regularly spaced original dashes.
    The isolated dash must attach centrally to one confidently identified body.
    Only a straight, short, otherwise empty gap is proposed. The filled junction
    dot, repeated dash pattern, obstacle checks and independent model judgments
    prevent generic dilation or arbitrary proximity from becoming a connection.
    """
    if gray.ndim != 2 or gray.shape != mask.shape:
        raise ValueError("gray and mask must be matching two-dimensional arrays")
    if not math.isfinite(text_h) or text_h <= 0:
        raise ValueError("text_h must be positive and finite")
    binary = (np.asarray(mask) != 0).astype(np.uint8)
    h, w = binary.shape
    n, labels, stats, _ = cv2.connectedComponentsWithStats(binary, connectivity=8)
    dashes = cv._dash_components(stats, max(10, round(2.2*text_h)), 2)
    strict = {label: segment for label, segment in dashes.items()
              if .5*text_h <= max(stats[label][2], stats[label][3]) <= 2.2*text_h
              and stats[label][4] >= .75*stats[label][2]*stats[label][3]}
    links, _, _ = cv.dash_links(labels, stats)
    parents = cv._DSU(n)
    for a, b, _, _ in links:
        parents.union(a, b)

    grouped = defaultdict(list)
    for label, segment in strict.items():
        orientation = segment[0]
        cross = (segment[2]+segment[4])/2 if orientation == "h" else (segment[1]+segment[3])/2
        grouped[(parents.find(label), orientation, round(cross))].append(segment)
    patterns = defaultdict(list)
    for (root, orientation, _), segments in grouped.items():
        if len(segments) < 3:
            continue
        intervals = sorted((s[1], s[3]) if orientation == "h" else (s[2], s[4]) for s in segments)
        lengths = np.asarray([b-a+1 for a, b in intervals])
        gaps = np.asarray([b[0]-a[1]-1 for a, b in zip(intervals, intervals[1:])])
        if (not len(gaps) or np.any(gaps < 1) or np.any(gaps > text_h)
                or np.ptp(lengths) > max(2, .35*float(np.median(lengths)))
                or np.ptp(gaps) > max(2, .4*float(np.median(gaps)))):
            continue
        patterns[root].append(float(np.median(gaps)))
    if not patterns:
        return []

    blocked = np.zeros_like(binary)
    for symbol in symbols:
        x0, y0, x1, y1 = map(int, symbol["bbox"])
        blocked[max(0, y0-erase):min(h, y1+erase+1), max(0, x0-erase):min(w, x1+erase+1)] = 1
    for x0, y0, x1, y1 in exclude:
        blocked[max(0, y0):min(h, y1+1), max(0, x0):min(w, x1+1)] = 1
    if obstacles is not None:
        if obstacles.shape != binary.shape:
            raise ValueError("obstacles must have the same shape as the drawing")
        blocked[obstacles != 0] = 1

    result, seen = [], set()
    for label, (orientation, x0, y0, x1, y1) in strict.items():
        if parents.find(label) in patterns:
            continue
        if orientation == "h":
            cy = (y0+y1)//2
            ends = [([x0, cy], [x1, cy], (1, 0)), ([x1, cy], [x0, cy], (-1, 0))]
        else:
            cx = (x0+x1)//2
            ends = [([cx, y0], [cx, y1], (0, 1)), ([cx, y1], [cx, y0], (0, -1))]
        for body_end, wire_end, direction in ends:
            attachment = _body_contact(body_end, direction, symbols, erase, text_h)
            if attachment is None:
                continue
            symbol, side, contact = attachment
            # The body-side endpoint is actual raw ink; the tiny erased margin
            # is reviewed by K6 rather than filled by this geometry proposal.
            if gray[body_end[1], body_end[0]] >= 200:
                continue
            dx, dy = direction
            for step in range(1, max(5, round(.8*text_h))+2):
                x, y = wire_end[0]+dx*step, wire_end[1]+dy*step
                if not (0 <= x < w and 0 <= y < h) or blocked[y, x]:
                    break
                target = int(labels[y, x])
                if not target:
                    continue
                # The first encountered ink must be the proved dashed net.
                root = parents.find(target)
                gap = step-1
                if (target == label or root not in patterns or gap < 2
                        or not any(abs(gap-reference) <= max(2, .25*text_h)
                                   for reference in patterns[root])):
                    break
                junction = _filled_junction(binary, gray, labels, target, [x, y], direction, text_h)
                if junction is None:
                    break
                path = [list(wire_end), [x, y]]
                key = tuple(tuple(p) for p in path)
                if key not in seen:
                    seen.add(key)
                    bx0, bx1 = sorted((wire_end[0], x))
                    by0, by1 = sorted((wire_end[1], y))
                    crop = np.ascontiguousarray(gray[max(0, by0-18):min(h, by1+19),
                                                    max(0, bx0-18):min(w, bx1+19)])
                    result.append({"path": path, "gap_points": path,
                                   "bbox": [max(0, bx0-18), max(0, by0-18), min(w-1, bx1+18), min(h-1, by1+18)],
                                   "reason": "terminal_dash_to_proven_junction", "symbol": symbol.get("id"),
                                   "side": side, "body_contact": contact, "junction_point": junction,
                                   "dash_arm_labels": [int(label), target], "observed_gap_pixels": gap,
                                   "reference_dash_gaps": sorted(set(patterns[root])),
                                   "raw_sha256": hashlib.sha256(crop.tobytes()).hexdigest(),
                                   "requires_original_ink_check": True, "requires_endpoint_check": True})
                break
    return result


def install(extractor):
    """Append these candidates to SIG.propose without modifying frozen files."""
    signal = extractor.SIG
    if getattr(signal, "_terminal_dash_candidate_installed", False):
        return
    original = signal.propose

    def enhanced(gray, mask, symbols, erase=2, text_h=9, obstacles=None, exclude=()):
        existing = original(gray, mask, symbols, erase, text_h, obstacles, exclude)
        extra = propose(gray, mask, symbols, cv=extractor.CV, erase=erase,
                        text_h=text_h, obstacles=obstacles, exclude=exclude)
        keys = {tuple(tuple(p) for p in item["gap_points"]) for item in existing}
        return existing + [item for item in extra if tuple(tuple(p) for p in item["gap_points"]) not in keys]

    signal.propose = enhanced
    signal._terminal_dash_candidate_installed = True
