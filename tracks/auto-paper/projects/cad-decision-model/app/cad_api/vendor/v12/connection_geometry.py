"""Bounded checkpoints on traced line paths. Coordinates come only from the image trace, never GT.

A global pair view shrinks a branched header too far to judge its junctions. This module
splits a route into local windows; Jev checks the raw ink between endpoint markers. It
also rejects routes crossing an already detected third symbol before requesting a judge.
"""
from __future__ import annotations

import math
import hashlib

import cv2
import numpy as np


def distance_to_segment(p, a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    t = ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / max(dx * dx + dy * dy, 1e-9)
    t = max(0.0, min(1.0, t))
    q = (a[0] + t * dx, a[1] + t * dy)
    return math.dist(p, q)


def uses_bridge(path, bridge, raw_mask, tolerance=1):
    """A route needs an inferred tee check only if it traverses inserted pixels.

    Sharing a component is insufficient: an unrelated uncertain tee must not
    veto all original routes of a common header. Existing endpoint ink does not
    count as using the proposal.
    """
    if not path or len(path) < 2:
        return False
    H, W = raw_mask.shape
    for a, b in zip(bridge, bridge[1:]):
        steps = max(1, math.ceil(math.dist(a, b)))
        for k in range(1, steps):
            p = [round(a[j]+(b[j]-a[j])*k/steps) for j in (0, 1)]
            if not 0 <= p[0] < W or not 0 <= p[1] < H or raw_mask[p[1], p[0]]:
                continue
            if any(distance_to_segment(p, c, d) <= tolerance for c, d in zip(path, path[1:])):
                return True
    return False


def intervening_symbols(path, symbols, endpoints, inset=1):
    """Detected objects that the interior of a route traverses. Mere neighbouring boxes do not count."""
    hits = []
    for i, o in enumerate(symbols):
        if i in endpoints:
            continue
        x0, y0, x1, y1 = o['bbox']
        if x1 - x0 < 2 * inset or y1 - y0 < 2 * inset:
            continue
        for a, b in zip(path or (), (path or ())[1:]):
            steps = max(1, math.ceil(math.dist(a, b)))
            if any(x0 + inset <= a[0] + (b[0] - a[0]) * k / steps <= x1 - inset and
                   y0 + inset <= a[1] + (b[1] - a[1]) * k / steps <= y1 - inset
                   for k in range(1, steps)):
                hits.append(i)
                break
    return hits


def checkpoints(path, max_span=180, bend_context=22, protected_turns=()):
    """Straight spans and junction turns as local crops. Tiny one-pixel zigzags are part of a span.

    Each item has raw-image endpoint positions, bbox, route polyline and kind. For a
    bend, marks lie on the incoming/outgoing arm, so a cropped T junction cannot be
    mistaken for a line ending at the crop. Overlapping views are deliberately kept.
    """
    if not path or len(path) < 2:
        return []
    # A geometry-supported dashed elbow has an explicit original corner.
    # Simplify only between those corners, so raster simplification cannot
    # replace the elbow by a diagonal. Other paths keep their legacy result.
    protected = {tuple(p) for p in protected_turns
                 if isinstance(p, (list, tuple)) and len(p) == 2
                 and all(type(v) in (int, float) and math.isfinite(v) for v in p)}
    stops = sorted({0, len(path)-1} | {i for i, p in enumerate(path) if tuple(p) in protected})
    simplified = []
    for start, end in zip(stops, stops[1:]):
        part = cv2.approxPolyDP(np.asarray(path[start:end+1], np.int32).reshape(-1, 1, 2),
                                3.0, False).reshape(-1, 2).tolist()
        simplified.extend(part if not simplified else part[1:])
    path = simplified
    result = []
    def add(points, kind):
        if math.dist(points[0], points[-1]) < 12:
            return
        pad = 18
        xs, ys = zip(*points)
        result.append({'path': [list(p) for p in points], 'a': list(points[0]), 'b': list(points[-1]),
                       'bbox': [math.floor(min(xs) - pad), math.floor(min(ys) - pad),
                                math.ceil(max(xs) + pad), math.ceil(max(ys) + pad)], 'kind': kind})
    # bounded straight spans, including short slanted leader lines
    for a, b in zip(path, path[1:]):
        length = math.dist(a, b)
        n = max(1, math.ceil(length / max_span))
        for k in range(n):
            p = [round(a[j] + (b[j] - a[j]) * k / n) for j in (0, 1)]
            q = [round(a[j] + (b[j] - a[j]) * (k + 1) / n) for j in (0, 1)]
            add([p, q], 'span')
    # all turns with meaningful arms: pick nearby positions on both traced sides
    for i in range(1, len(path) - 1):
        b, prev, nxt = path[i], path[i - 1], path[i + 1]
        da, db = math.dist(prev, b), math.dist(b, nxt)
        if min(da, db) < 6:
            continue
        ux, uy = (b[0] - prev[0]) / da, (b[1] - prev[1]) / da
        vx, vy = (nxt[0] - b[0]) / db, (nxt[1] - b[1]) / db
        if ux * vx + uy * vy > .94:
            continue
        a = [round(b[j] + (prev[j] - b[j]) * min(1, bend_context / da)) for j in (0, 1)]
        c = [round(b[j] + (nxt[j] - b[j]) * min(1, bend_context / db)) for j in (0, 1)]
        add([a, list(b), c], 'junction')
    # Canonical orientation makes common spans reuse the exact same question/cache.
    seen, out = set(), []
    for item in result:
        if tuple(item['a']) > tuple(item['b']):
            item['a'], item['b'] = item['b'], item['a']
            item['path'].reverse()
        key = tuple(tuple(p) for p in item['path'])
        if key not in seen:
            seen.add(key)
            out.append(item)
    return out


def anchored_checkpoint(gray, item, text_h=9, symbols=()):
    """One additional raw view when old endpoint markers obscure their arms.

    The caller should use this only for an unaccepted relation's already judged
    weak checkpoint, never replace an accepted route, and still require normal
    paired line and both-endpoint judgments at the existing thresholds. This
    helper supplies evidence; it does not accept a relation or change its path.

    Marker centres must be actual original dark/gray pixels on the same local
    arm. A two-pixel transverse raster error is allowed, but an isolated pixel,
    nearby parallel wire, symbol body or unobserved blank arm cannot supply an
    anchor. Original path vertices, crossing gaps and the complete old crop are
    retained. Bracket segments are chosen only from blank original pixels.
    ``marker_brackets`` contains raw-image line segments the renderer can draw
    with colour A/B, without circles or a painted route.
    """
    if gray.ndim != 2:
        raise ValueError("gray must be an unchanged two-dimensional page")
    if not math.isfinite(text_h) or text_h <= 0:
        raise ValueError("text_h must be positive and finite")
    path = [list(map(int, p)) for p in item.get('path', [])]
    if (len(path) < 2 or item.get('marker_style') == 'external_blank_brackets'
            or item.get('kind') not in {'span', 'junction', 'separated_crossing', 'signal_gap', 'outlet_tee_gap'}):
        return None
    H, W = gray.shape
    raw = gray < 200
    blocked = np.zeros(gray.shape, np.uint8)
    for symbol in symbols:
        x0, y0, x1, y1 = symbol['bbox']
        blocked[max(0, y0):min(H, y1+1), max(0, x0):min(W, x1+1)] = 1
    # Markers must keep a one-pixel clear margin from original ink.
    protected = cv2.dilate(raw.astype(np.uint8), np.ones((3, 3), np.uint8))
    span = max(4, round(text_h))
    support = max(3, min(5, round(text_h/3)))

    def clear_brackets(point):
        px, py = point
        for radius in range(3, max(7, round(text_h)) + 1):
            length = 2
            segments = []
            for sx in (-1, 1):
                for sy in (-1, 1):
                    corner = [px+sx*radius, py+sy*radius]
                    segments.extend([[corner, [corner[0]+sx*length, corner[1]]],
                                     [corner, [corner[0], corner[1]+sy*length]]])
            pixels = []
            for a, b in segments:
                for k in range(length+1):
                    pixels.append((round(a[0]+(b[0]-a[0])*k/length),
                                   round(a[1]+(b[1]-a[1])*k/length)))
            if all(0 <= x < W and 0 <= y < H and not protected[y, x] for x, y in pixels):
                return segments
        return None

    def anchor(first):
        p = path[0] if first else path[-1]
        neighbours = path[1:] if first else path[-2::-1]
        neighbour = next((q for q in neighbours if math.dist(p, q) >= 4), None)
        if neighbour is None or not (0 <= p[0] < W and 0 <= p[1] < H):
            return None
        dx, dy = neighbour[0]-p[0], neighbour[1]-p[1]
        norm = math.hypot(dx, dy)
        ux, uy = dx/norm, dy/norm
        # Only the endpoint portion may move. Keep the central crossing/elbow
        # between markers, including when one old endpoint falls in a dash gap.
        inward = min(span, .25*norm)
        candidates = []
        for y in range(max(0, p[1]-span-2), min(H, p[1]+span+3)):
            for x in range(max(0, p[0]-span-2), min(W, p[0]+span+3)):
                if not raw[y, x] or blocked[y, x]:
                    continue
                vx, vy = x-p[0], y-p[1]
                along, cross = vx*ux+vy*uy, abs(vx*uy-vy*ux)
                if not -span <= along <= inward or cross > 2:
                    continue
                # Exact pixels along a short observed arm reject glyph specks
                # and perpendicular crossing ink near the route centreline.
                observed = []
                half = support//2
                for k in range(-half, half+1):
                    qx, qy = round(x+k*ux), round(y+k*uy)
                    observed.append(0 <= qx < W and 0 <= qy < H
                                    and raw[qy, qx] and not blocked[qy, qx])
                if not all(observed):
                    continue
                brackets = clear_brackets([x, y])
                if brackets is not None:
                    candidates.append((cross, math.dist(p, (x, y)), x, y, brackets))
        if not candidates:
            return None
        best = min(candidates)
        # A simplified path exactly between two parallel strokes cannot tell
        # which wire it followed. Do not choose the upper/left candidate merely
        # through tuple ordering; leave that ambiguous crop to the old judge.
        tied = [c for c in candidates if abs(c[0]-best[0]) <= .05 and abs(c[1]-best[1]) <= .05]
        if any((c[2]-p[0])*uy-(c[3]-p[1])*ux > .25 for c in tied) and \
                any((c[2]-p[0])*uy-(c[3]-p[1])*ux < -.25 for c in tied):
            return None
        _, _, x, y, brackets = best
        return [x, y], brackets

    a, b = anchor(True), anchor(False)
    if a is None or b is None:
        return None
    old_a, old_b = path[0], path[-1]
    new_a, new_b = a[0], b[0]
    if math.dist(new_a, new_b) < max(12, .5*math.dist(old_a, old_b)):
        return None
    # The old ring intersects a thin line at either side of its centre. White
    # centres are a raster/interval error; existing external signal markers
    # only retry if a centre really was not ink.
    white = [name for name, p in (('a', old_a), ('b', old_b)) if not raw[p[1], p[0]]]
    if item.get('kind') == 'signal_gap' and not white:
        return None
    reasons = ['white_marker_centre'] if white else ['ring_over_observed_arm']
    changed = new_a != old_a or new_b != old_b
    reviewed = [new_a] + path + [new_b]
    # Keep original vertices verbatim for provenance, but remove consecutive
    # duplicates in the additional view's semantic route.
    reviewed = [p for i, p in enumerate(reviewed) if i == 0 or p != reviewed[i-1]]
    points = reviewed + [p for endpoint in (a, b) for segment in endpoint[1] for p in segment]
    xs, ys = zip(*points)
    pad = max(12, round(1.5*text_h))
    old_box = item.get('bbox', [min(xs), min(ys), max(xs), max(ys)])
    box = [max(0, min(old_box[0], min(xs)-pad)), max(0, min(old_box[1], min(ys)-pad)),
           min(W-1, max(old_box[2], max(xs)+pad)), min(H-1, max(old_box[3], max(ys)+pad))]
    x0, y0, x1, y1 = box
    crop = np.ascontiguousarray(gray[y0:y1+1, x0:x1+1])
    result = {'kind': 'raw_anchored_checkpoint', 'source_kind': item['kind'],
              'a': new_a, 'b': new_b, 'path': reviewed, 'bbox': box,
              'original_path': path, 'original_markers': [old_a, old_b],
              'marker_style': 'external_blank_brackets',
              'marker_brackets': {'a': a[1], 'b': b[1]}, 'retry_reasons': reasons,
              'anchors_moved': changed, 'requires_new_paired_line_check': True,
              'raw_sha256': hashlib.sha256(np.asarray(crop.shape, np.int64).tobytes()+crop.tobytes()).hexdigest()}
    for key in ('bridge', 'crossing_point', 'crossing_axis', 'original_gap_path', 'reason'):
        if key in item:
            result[key] = item[key]
    return result


def partition_crossing_spans(details, crossings):
    """Split straight spans around separately reviewed opposed crossing arms.

    A crossing's full raw view is always retained. Only ``span`` checkpoints
    whose two-point straight path contains that crossing's actual A/B markers
    are partitioned. New spans end at those exact observed marker coordinates;
    the crossing covers the interval between them. Non-collinear, partial,
    malformed or unverified overlaps leave the old span unchanged, so cropping
    cannot create an unexamined route interval. Tiny outside pieces are kept.

    This is a view partition, not a route/net or answer change. Call before K5
    on unaccepted crossing-bearing relations. Every resulting span and every
    crossing still requires normal paired judgments at the existing thresholds.
    """
    import copy
    result = []
    crossing_items = [copy.deepcopy(c) for c in crossings]

    def verified(c):
        labels = c.get('component_labels', [])
        digest = c.get('raw_sha256', '')
        points = c.get('path', [])
        return (c.get('kind') == 'separated_crossing' and len(points) == 2
                and c.get('a') == points[0] and c.get('b') == points[-1]
                and len(labels) == 3 and len(set(labels)) == 3 and all(v > 0 for v in labels)
                and isinstance(digest, str) and len(digest) == 64
                and all(ch in '0123456789abcdef' for ch in digest))

    def geometry_key(c):
        return c.get('kind'), tuple(tuple(p) for p in c.get('path', []))

    crossing_keys = {geometry_key(c) for c in crossing_items}
    eligible = [c for c in crossing_items if verified(c)]
    for old in details:
        if geometry_key(old) in crossing_keys:
            continue  # mandatory crossing views are appended once below
        item = copy.deepcopy(old)
        path = item.get('path', [])
        if item.get('kind') != 'span' or len(path) != 2:
            result.append(item)
            continue
        a, b = path
        dx, dy = b[0]-a[0], b[1]-a[1]
        length = math.hypot(dx, dy)
        if length == 0:
            result.append(item)
            continue
        intervals = []
        unsafe = False
        for c in eligible:
            first, last = c['a'], c['b']
            projections = [((p[0]-a[0])*dx+(p[1]-a[1])*dy)/length for p in (first, last)]
            points = [first, last]
            if projections[0] > projections[1]:
                projections.reverse()
                points.reverse()
            lo, hi = projections
            # A two-pixel raster mismatch is an anchor-retry concern, not a
            # reason to replace a span with a different parallel path here.
            collinear = all(abs((p[0]-a[0])*dy-(p[1]-a[1])*dx)/length <= .05 for p in points)
            if not collinear or hi <= 0 or lo >= length:
                continue
            if lo < -.05 or hi > length+.05:
                unsafe = True
                break
            if hi-lo <= 0 or math.dist(points[0], points[1]) < 2:
                continue
            intervals.append((max(0., lo), min(length, hi), points[0], points[1], c))
        # Overlapping crossing contexts could describe two closely spaced
        # jumps or contradictory hypotheses. Preserve the full old span.
        intervals.sort(key=lambda v: (v[0], v[1]))
        if unsafe or not intervals or any(v[0] < u[1]-.05 for u, v in zip(intervals, intervals[1:])):
            result.append(item)
            continue
        boundary, cursor = list(a), 0.
        pieces = []
        for lo, hi, first, last, c in intervals:
            if lo > cursor+.05:
                pieces.append((boundary, list(first)))
            boundary, cursor = list(last), hi
        if cursor < length-.05:
            pieces.append((boundary, list(b)))
        for first, last in pieces:
            xs, ys = zip(first, last)
            pad = 18
            piece = {**item, 'path': [first, last], 'a': first, 'b': last,
                     'bbox': [math.floor(min(xs)-pad), math.floor(min(ys)-pad),
                              math.ceil(max(xs)+pad), math.ceil(max(ys)+pad)],
                     'partition_of': copy.deepcopy(path),
                     'crossing_partition_boundaries': [[list(v[2]), list(v[3])] for v in intervals]}
            result.append(piece)
    result.extend(crossing_items)
    return result
