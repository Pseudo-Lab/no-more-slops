"""Structure-aware symbol proposals, without model calls or sheet coordinates.

P&ID ink often has touching, separate components (a valve and a small N marker),
or several enclosed white cells belonging to one component (a tank crossed by
its internal pipes).  These proposals retain that distinction before Jev judges
them.  The logic-diagram path intentionally keeps the established proposals.
"""
from __future__ import annotations

import copy

import cv2
import numpy as np

import page_cv as CV
import arrow_geometry as AG
import round_body_geometry as RBG


def _wh(b):
    return b[2] - b[0] + 1, b[3] - b[1] + 1


def _union(a, b):
    return min(a[0], b[0]), min(a[1], b[1]), max(a[2], b[2]), max(a[3], b[3])


def _iou(a, b):
    i = CV.inter(a, b)
    return i / max(1, CV.area(a) + CV.area(b) - i)


def _near(a, b, gap):
    return a[0] <= b[2] + gap and b[0] <= a[2] + gap and a[1] <= b[3] + gap and b[1] <= a[3] + gap


def _aligned(a, b, gap):
    """Adjacent cells can share an edge; a tangent N ring is not such a cell."""
    if _iou(a, b) >= .35:
        return True
    wa, ha = _wh(a)
    wb, hb = _wh(b)
    if not _near(a, b, gap):
        return False
    cx = abs(a[0] + a[2] - b[0] - b[2]) / 2
    cy = abs(a[1] + a[3] - b[1] - b[3]) / 2
    horizontal = cy <= .22 * min(ha, hb) and min(ha, hb) >= .65 * max(ha, hb)
    vertical = cx <= .22 * min(wa, wb) and min(wa, wb) >= .65 * max(wa, wb)
    return horizontal or vertical


def _group_aligned(boxes, gap=2, max_side=None):
    max_side = max_side or CV.SC.px(150, 40)
    work = [tuple(map(int, b)) for b in boxes]
    changed = True
    while changed:
        changed = False
        for i, a in enumerate(work):
            for j in range(i + 1, len(work)):
                b = work[j]
                if max(*_wh(a), *_wh(b), *_wh(_union(a, b))) > max_side or not _aligned(a, b, gap):
                    continue
                work[i] = _union(a, b)
                work.pop(j)
                changed = True
                break
            if changed:
                break
    return work


def _line_residual(bw):
    """Remove long pipe runs so diagonal open-valve ink remains detectable."""
    length = max(18, int(round(2.4 * CV.SC.text_h)))
    h = cv2.morphologyEx(bw, cv2.MORPH_OPEN, np.ones((1, length), np.uint8))
    v = cv2.morphologyEx(bw, cv2.MORPH_OPEN, np.ones((length, 1), np.uint8))
    return bw & (1 - (h | v))


def hatch_regions(bw):
    """Thin framed bands of regularly repeated, single diagonal hatch strokes.

    A chain of actual valves has two complementary diagonals, distinct body
    frames and separating pipe segments. Material hatching instead has at
    least six same-direction strokes at near-uniform spacing, bounded by two
    continuous long parallel strokes. Only that narrow hatch band is excluded.
    """
    th = CV.SC.text_h
    residual = _line_residual(bw)
    n, lab, st, _ = cv2.connectedComponentsWithStats(residual, connectivity=8)
    diagonals = []
    for i, (x, y, w, h, a) in enumerate(st[1:], 1):
        x, y, w, h, a = map(int, (x, y, w, h, a))
        if min(w, h) < .55 * th or max(w, h) > 2.3 * th or not .55 <= w / h <= 1.8:
            continue
        ys, xs = np.nonzero(lab[y:y + h, x:x + w] == i)
        if len(xs) < 5:
            continue
        covariance = np.cov(np.array([xs, ys]))
        values, vectors = np.linalg.eigh(covariance)
        if values[-1] <= 0 or values[0] > .10 * values[-1]:
            continue
        vector = vectors[:, -1]
        if not .4 <= abs(vector[0]) <= .92 or not .4 <= abs(vector[1]) <= .92:
            continue
        diagonals.append((x, y, x + w - 1, y + h - 1, 1 if vector[0] * vector[1] > 0 else -1))
    out = []
    for vertical in (True, False):
        groups = {}
        for b in diagonals:
            # Width and aligned origin of a continuous strip; tolerate 2px
            # raster shifts, while retaining diagonal direction.
            across0 = b[0] if vertical else b[1]
            across1 = b[2] if vertical else b[3]
            key = (int(round(across0 / 3)), int(round(across1 / 3)), b[4])
            matching = next((k for k, values in groups.items() if k[2] == b[4]
                             and abs((values[0][0] if vertical else values[0][1]) - across0) <= 3
                             and abs((values[0][2] if vertical else values[0][3]) - across1) <= 3), key)
            groups.setdefault(matching, []).append(b)
        for group in groups.values():
            axis = 1 if vertical else 0
            group.sort(key=lambda b: b[axis])
            if len(group) < 6:
                continue
            centres = np.array([(b[axis] + b[axis + 2]) / 2 for b in group])
            gaps = np.diff(centres)
            step = float(np.median(gaps))
            if step < .6 * th or step > 2.4 * th or np.mean(abs(gaps - step) <= max(2, .18 * step)) < .85:
                continue
            b = group[0][:4]
            for other in group[1:]:
                b = _union(b, other[:4])
            # Find both continuous parallel frame sides close to the stroke
            # endpoints; repeated valves do not have these continuous rails.
            if vertical:
                strip = bw[b[1]:b[3] + 1, max(0, b[0] - 3):min(bw.shape[1], b[2] + 4)]
                share = strip.mean(axis=0)
                left = np.flatnonzero(share[:5] >= .85)
                right = np.flatnonzero(share[-5:] >= .85)
                if not len(left) or not len(right):
                    continue
                x0 = max(0, b[0] - 3) + int(left[0])
                x1 = max(0, b[0] - 3) + strip.shape[1] - 5 + int(right[-1])
                out.append((x0, b[1], x1, b[3]))
            else:
                strip = bw[max(0, b[1] - 3):min(bw.shape[0], b[3] + 4), b[0]:b[2] + 1]
                share = strip.mean(axis=1)
                top = np.flatnonzero(share[:5] >= .85)
                bottom = np.flatnonzero(share[-5:] >= .85)
                if not len(top) or not len(bottom):
                    continue
                y0 = max(0, b[1] - 3) + int(top[0])
                y1 = max(0, b[1] - 3) + strip.shape[0] - 5 + int(bottom[-1])
                out.append((b[0], y0, b[2], y1))
    return out


def _open_inline_shapes(bw):
    """Recover unclosed valve bodies on a pipe, proposed for Jev to classify.

    An open switch-style valve has two end bars and a diagonal connecting them;
    there may be no enclosed white area.  A non-straight residual component must
    have a pipe continuing at both ends.  The same criterion admits conventional
    outlined valves and reducers, which are useful existing symbols.
    """
    th = CV.SC.text_h
    residual = _line_residual(bw)
    # Restore short stroke gaps caused only by the removed pipe thickness.
    residual |= cv2.morphologyEx(residual, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8)) & bw
    n, _, st, _ = cv2.connectedComponentsWithStats(residual, connectivity=8)
    H, W = bw.shape
    out = []
    components = [tuple(map(int, row)) for row in st[1:]]
    small = sorted([c for c in components if .7 * th <= max(c[2], c[3]) <= 2.5 * th
                    and min(c[2], c[3]) >= .45 * th and c[4] >= .12 * c[2] * c[3]], key=lambda c: c[1])
    extra = []
    for i, (x, y, w, h, a) in enumerate(small):
        for xx, yy, ww, hh, aa in small[i + 1:]:
            if yy > y + h + 4:
                break
            if xx > x + w + 4 or x > xx + ww + 4:
                continue
            gapx = max(0, xx - (x + w), x - (xx + ww))
            gapy = max(0, yy - (y + h), y - (yy + hh))
            # Complementary diagonals split at the removed pipe share most of
            # one axis and a narrow gap on the other.
            overlap_y = min(y + h, yy + hh) - max(y, yy)
            overlap_x = min(x + w, xx + ww) - max(x, xx)
            if overlap_y >= .65 * min(h, hh) and gapx <= 4:
                if min(w, ww) < .55 * min(h, hh):
                    continue
                pa = residual[y:y + h, x:x + w]
                pb = residual[yy:yy + hh, xx:xx + ww]
                # Complementary half-X strokes taper toward the crossing.
                # Require an upright end at the outside of both halves.
                if x < xx:
                    upright_a, upright_b = np.count_nonzero(pa[:, :2].sum(1)), np.count_nonzero(pb[:, -2:].sum(1))
                else:
                    upright_a, upright_b = np.count_nonzero(pa[:, -2:].sum(1)), np.count_nonzero(pb[:, :2].sum(1))
                if upright_a < .7 * h or upright_b < .7 * hh:
                    continue
            if ((gapx <= 4 and overlap_y >= .65 * min(h, hh))
                    or (gapy <= 4 and overlap_x >= .65 * min(w, ww))):
                u = _union((x, y, x + w - 1, y + h - 1), (xx, yy, xx + ww - 1, yy + hh - 1))
                if (x + w < xx or xx + ww < x):
                    start, end = (x + w, xx) if x < xx else (xx + ww, x)
                    bridge = bw[max(y, yy):min(y + h, yy + hh), start:end]
                    # A removed thick pipe crossed both half-diagonals. A mere
                    # close pair of glyphs has no original ink bridging the gap.
                    if bridge.size and bridge.sum() < max(2, .6 * (end - start)):
                        continue
                extra.append((u[0], u[1], *_wh(u), a + aa))
    for x, y, w, h, a in components + extra:
        x, y, w, h, a = map(int, (x, y, w, h, a))
        if a < .12 * w * h:
            continue
        # Test both orientations. Size follows drawing letter height, not page IDs.
        horizontal = 2.0 * th <= w <= 4.5 * th and .9 * th <= h <= 2.4 * th and 1.45 <= w / h <= 3.2
        vertical = 2.0 * th <= h <= 4.5 * th and .9 * th <= w <= 2.4 * th and 1.45 <= h / w <= 3.2
        if not horizontal and not vertical:
            continue
        reach = max(8, int(round(1.3 * th)))
        if horizontal:
            cy = y + h // 2
            left = bw[max(0, cy - 2):cy + 3, max(0, x - reach):x].sum()
            right = bw[max(0, cy - 2):cy + 3, x + w:min(W, x + w + reach)].sum()
            ok = left >= reach * .65 and right >= reach * .65
        else:
            cx = x + w // 2
            top = bw[max(0, y - reach):y, max(0, cx - 2):cx + 3].sum()
            bottom = bw[y + h:min(H, y + h + reach), max(0, cx - 2):cx + 3].sum()
            ok = top >= reach * .65 and bottom >= reach * .65
        if ok:
            out.append(CV.snap_out(bw, (x, y, x + w - 1, y + h - 1), max_grow=2, frac=.30))
    return out


def _filled_pairs(bw, blobs):
    """Join complementary thick valve triangles across their narrow centre.

    Erosion separates filled bowties at their tips. Their parallel bounding
    boxes and shared pipe axis identify the pair without absorbing an actuator
    on a perpendicular stem or an adjacent circular letter marker.
    """
    gap = max(3, CV.SC.px(11))
    out = []
    for i, a in enumerate(blobs):
        wa, ha = _wh(a)
        if min(wa, ha) < max(5, int(.65 * CV.SC.text_h)):
            continue
        for b in blobs[i + 1:]:
            wb, hb = _wh(b)
            if min(wb, hb) < max(5, int(.65 * CV.SC.text_h)):
                continue
            if not _aligned(a, b, gap) or CV.inter(a, b):
                continue
            u = _union(a, b)
            wu, hu = _wh(u)
            if max(wu, hu) > 4 * CV.SC.text_h or min(wu, hu) > 2 * CV.SC.text_h:
                continue
            if max(wu, hu) / min(wu, hu) < 1.5:
                continue
            # A filled triangular edge tapers toward the wire. Require more
            # than its thin shaft, but retain the last few body pixels that a
            # fractional side-coverage rule otherwise clips.
            out.append(CV.snap_out(bw, u, max_grow=3, frac=.12))
    return out


def _vessels(bw, holes):
    """Join large adjacent enclosed cells only when their union is rounded.

    Tanks crossed by internal lines have several hole contours. A rounded outer
    silhouette has empty bounding-box corners and long top/bottom strokes; wire
    grids and rectangular table cells do not meet this condition.
    """
    th = CV.SC.text_h
    large = [b for b in holes if min(_wh(b)) >= 2 * th and CV.area(b) >= 18 * th * th]
    groups = [{i} for i in range(len(large))]
    changed = True
    while changed:
        changed = False
        for i in range(len(groups)):
            for j in range(i + 1, len(groups)):
                if any(_near(large[a], large[b], 1) for a in groups[i] for b in groups[j]):
                    groups[i] |= groups.pop(j)
                    changed = True
                    break
            if changed:
                break
    def rounded(b):
        w, h = _wh(b)
        if min(w, h) < 5 * th or max(w, h) < 10 * th:
            return False
        patch = bw[b[1]:b[3] + 1, b[0]:b[2] + 1]
        m = max(3, int(.08 * min(w, h)))
        corners = [patch[:m, :m], patch[:m, -m:], patch[-m:, :m], patch[-m:, -m:]]
        if sum(c.mean() < .035 for c in corners) < 3:
            return False
        # Rounded ends must touch all four sides. This rejects an envelope
        # extended into an adjacent instrument connected by its pipe.
        left_edge = patch[:, :3].sum(axis=1)
        right_edge = patch[:, -3:].sum(axis=1)
        top_edge = patch[:3].sum(axis=0)
        bottom_edge = patch[-3:].sum(axis=0)
        if min(np.count_nonzero(left_edge), np.count_nonzero(right_edge)) < .20 * h:
            return False
        if min(np.count_nonzero(top_edge), np.count_nonzero(bottom_edge)) < .20 * w:
            return False
        rows = patch[:max(3, int(.08 * h))].sum(axis=1)
        bottom = patch[-max(3, int(.08 * h)):].sum(axis=1)
        cols = patch[:, :max(3, int(.08 * w))].sum(axis=0)
        right = patch[:, -max(3, int(.08 * w)):].sum(axis=0)
        return ((max(rows) >= .65 * w and max(bottom) >= .65 * w)
                or (max(cols) >= .65 * h and max(right) >= .65 * h))
    out = []
    for group in groups:
        if len(group) < 2:
            continue
        b = large[next(iter(group))]
        for i in group:
            b = _union(b, large[i])
        if rounded(b):
            out.append(b)
        else:
            # An adjoining instrument can extend the white-cell cluster. Try
            # each cell envelope endpoint; accept only closed rounded bodies.
            xs = sorted({large[i][2] for i in group})
            ys = sorted({large[i][3] for i in group})
            candidates = []
            for x1 in xs:
                for y1 in ys:
                    trial = (b[0], b[1], x1, y1)
                    if rounded(trial):
                        candidates.append(trial)
            if candidates:
                out.append(max(candidates, key=CV.area))
    return out


def _compound_reducers(bw, holes, filled_bodies):
    """Separate a trapezoid reducer touching a bowtie valve on one pipe.

    A reducer has parallel upright ends of unequal height. The adjacent valve
    is either two filled lobes or two equal triangular hole cells. Shared
    geometry is sufficient to propose their separate boxes before any labels.
    """
    out = []
    th = CV.SC.text_h
    for reducer in holes:
        w, h = _wh(reducer)
        if not (.8 * th <= min(w, h) <= 2 * th) or max(w, h) > 2.6 * th:
            continue
        for rotate in (False, True):
            patch = bw[reducer[1]:reducer[3] + 1, reducer[0]:reducer[2] + 1]
            if rotate:
                patch = patch.T
            ph, pw = patch.shape
            if not .65 <= pw / ph <= 1.8:
                continue
            lengths = [int(np.count_nonzero(patch[:, :2].sum(axis=1))),
                       int(np.count_nonzero(patch[:, -2:].sum(axis=1)))]
            if min(lengths) < .35 * ph or max(lengths) < .8 * ph or min(lengths) > .85 * max(lengths):
                continue
            # The tall end is the end touching the valve body.
            right = lengths[1] > lengths[0]
            candidates = filled_bodies + holes
            # A merged outlined bowtie may already include the reducer cell;
            # recover the part beyond its tall shared end. Filled morphology
            # also overgrows into the reducer's tall end by a few pixels.
            body_proposals = []
            for candidate in candidates:
                if candidate == reducer:
                    continue
                if rotate:
                    cy0, cy1 = candidate[1], candidate[3]
                    if right and cy0 <= reducer[3] + 3 and cy1 - reducer[3] >= 1.2 * h:
                        body_proposals.append((candidate[0], reducer[3], candidate[2], cy1))
                    elif not right and cy1 >= reducer[1] - 3 and reducer[1] - cy0 >= 1.2 * h:
                        body_proposals.append((candidate[0], cy0, candidate[2], reducer[1]))
                else:
                    cx0, cx1 = candidate[0], candidate[2]
                    if right and cx0 <= reducer[2] + 3 and cx1 - reducer[2] >= 1.2 * w:
                        body_proposals.append((reducer[2], candidate[1], cx1, candidate[3]))
                    elif not right and cx1 >= reducer[0] - 3 and reducer[0] - cx0 >= 1.2 * w:
                        body_proposals.append((cx0, candidate[1], reducer[0], candidate[3]))
            candidates = candidates + body_proposals
            for body in candidates:
                if body == reducer:
                    continue
                wb, hb = _wh(body)
                along_b, across_b = (hb, wb) if rotate else (wb, hb)
                along_r, across_r = (h, w) if rotate else (w, h)
                if not 1.5 <= along_b / across_b <= 3.8 or not .65 <= across_b / across_r <= 1.45:
                    continue
                if rotate:
                    gap = body[1] - reducer[3] if right else reducer[1] - body[3]
                    centred = abs(body[0] + body[2] - reducer[0] - reducer[2]) <= .4 * across_r
                else:
                    gap = body[0] - reducer[2] if right else reducer[0] - body[2]
                    centred = abs(body[1] + body[3] - reducer[1] - reducer[3]) <= .4 * across_r
                if -6 <= gap <= 3 and centred:
                    # A whole valve extends beyond the tall reducer end. Avoid
                    # treating the reducer's own small neighbouring letter as it.
                    if along_b < 1.2 * along_r:
                        continue
                    if gap < -3:
                        if rotate:
                            body = (body[0], reducer[3] - 1 if right else body[1], body[2],
                                    body[3] if right else reducer[1] + 1)
                        else:
                            body = (reducer[2] - 1 if right else body[0], body[1],
                                    body[2] if right else reducer[0] + 1, body[3])
                    out.append((reducer, body))
    return out


def _small_noise(b, bw):
    w, h = _wh(b)
    th = CV.SC.text_h
    if min(w, h) <= 4 or (max(w, h) <= .75 * th):
        return True
    H, W = bw.shape
    margin = .02 * min(H, W)
    cx, cy = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
    return max(w, h) <= 2.2 * th and (cx < margin or cy < margin or cx > W - margin or cy > H - margin)


def propose(bw, regions, exclude=(), profile_kind="pid", blob=None):
    """Drop-in candidate proposal API; all coordinates are inclusive pixels."""
    if profile_kind != "pid":
        return CV.symbol_candidates(bw, regions, exclude=exclude, blob=blob)
    hatches = hatch_regions(bw)
    def keep(b):
        return (not _small_noise(b, bw) and CV._inside_any(b, regions, 4)
                and not any(CV.inter(b, e) > .5 * CV.area(b) for e in exclude)
                and not any(CV.inter(b, e) > .75 * CV.area(b) for e in hatches))
    bl = blob or {}
    hs = [CV.snap_out(bw, h) for h in CV.holes(bw)]
    bs = CV.solid_blobs(bw, bl.get("min_side"), bl.get("max_side"), bl.get("fill", .6))
    hs, bs = [b for b in hs if keep(b)], [b for b in bs if keep(b)]
    bodies = _filled_pairs(bw, bs)
    # Raw small cells have meaningful edge alignment, unlike generic proximity.
    boxes = _group_aligned(hs, gap=max(3, CV.SC.px(5))) + bs
    # Flow-element circles have a small triangular side lobe as part of the
    # circle body; join that lobe while not joining a much smaller N marker.
    for a in hs:
        wa, ha = _wh(a)
        if min(wa, ha) < 3 * CV.SC.text_h or max(wa, ha) / min(wa, ha) > 1.4:
            continue
        for b in hs:
            wb, hb = _wh(b)
            if b == a or min(wb, hb) > .4 * min(wa, ha):
                continue
            centred = abs((a[1] + a[3]) - (b[1] + b[3])) <= .25 * ha
            side = b[0] <= a[2] + 1 and b[2] >= a[2] - 2 or b[2] >= a[0] - 1 and b[0] <= a[0] + 2
            if centred and side:
                u = _union(a, b)
                boxes = [old for old in boxes if old not in (a, b)]
                boxes.append(u)
    for body in bodies:
        boxes = [b for b in boxes if not CV.contains(body, b, 2)]
        boxes.append(body)
    compound_choices = {}
    for reducer, body in _compound_reducers(bw, hs, bodies + boxes):
        previous = compound_choices.get(reducer)
        if previous is None or CV.area(body) > CV.area(previous):
            compound_choices[reducer] = body
    compounds = list(compound_choices.items())
    for reducer, body in compounds:
        envelope = _union(reducer, body)
        boxes = [b for b in boxes if not (CV.contains(envelope, b, 2) and CV.area(b) > 1.1 * CV.area(body))]
        boxes.extend((reducer, body))
    open_shapes, vessels = _open_inline_shapes(bw), _vessels(bw, hs)
    for b in open_shapes + vessels:
        if not keep(b):
            continue
        # A stronger whole-body proposal replaces matching partial cells.
        if b in vessels:
            boxes = [old for old in boxes if not (CV.contains(b, old, 2) and CV.area(old) < .85 * CV.area(b))]
        if not any(_iou(b, old) >= .9 for old in boxes):
            boxes.append(b)
    # Residual whole-cell detections must not merge the two recovered shapes.
    for reducer, body in compounds:
        envelope = _union(reducer, body)
        boxes = [b for b in boxes if not (CV.contains(envelope, b, 2)
                 and b not in (reducer, body) and CV.area(b) > 1.1 * min(CV.area(body), CV.area(reducer))
                 and CV.inter(b, reducer) > .25 * CV.area(reducer)
                 and CV.inter(b, body) > .25 * CV.area(body))]
    # Near-identical alternatives are the same candidate, rather than a
    # containing symbol plus its child. Prefer the wider complete envelope.
    distinct = []
    for b in sorted(set(boxes), key=CV.area, reverse=True):
        if not any(_iou(b, previous) >= .92 for previous in distinct):
            distinct.append(b)
    boxes = distinct
    # A complete proposed box can overlap a remaining partial cell by a few
    # outline pixels. Prefer the whole proposal, keeping different neighbours.
    boxes = [b for i, b in enumerate(boxes) if not any(
        i != j and CV.area(q) > 1.2 * CV.area(b) and CV.area(q) < 12 * CV.area(b)
        and min(_wh(q)) >= 3 * CV.SC.text_h and max(_wh(q)) < 6 * CV.SC.text_h
        and CV.contains(q, b, 2)
        for j, q in enumerate(boxes))]
    return sorted(set(b for b in boxes if keep(b)), key=lambda b: (b[1], b[0], b[3], b[2]))


def protect_extent(bw, box, ext, cands=(), profile_kind="pid"):
    """Keep a complete small inline body separate from tangential neighbours.

    Thin handles/stems and the N ring beside a valve are separate from its
    symbol body. ``attached_extent`` is needed for CLD gate bars and lamp rays,
    but an inline P&ID body's complete parallel sides must not be expanded in
    the perpendicular direction merely because those neighbours touch it.
    The returned envelope remains a proposal, rather than a class assignment.
    """
    if profile_kind != "pid" or tuple(box) == tuple(ext):
        return tuple(ext)
    # Distinct proposed shapes which touch on the pipe must retain their own
    # boundaries; especially an adjacent reducer and valve body.
    raw_boxes = [c.get("bbox") if isinstance(c, dict) else c for c in cands]
    for neighbour in raw_boxes:
        if not neighbour or tuple(neighbour) == tuple(box) or CV.area(neighbour) < .25 * CV.area(box):
            continue
        overlap_before = CV.inter(neighbour, box)
        overlap_after = CV.inter(neighbour, ext)
        if overlap_before < .22 * min(CV.area(box), CV.area(neighbour)) and \
                overlap_after > max(overlap_before + .10 * CV.area(neighbour), .25 * CV.area(neighbour)):
            return tuple(box)
    w, h = _wh(box)
    th = CV.SC.text_h
    if min(w, h) < .8 * th or max(w, h) > 5 * th:
        return tuple(ext)
    horizontal = 1.45 <= w / h <= 3.8
    vertical = 1.45 <= h / w <= 3.8
    if not horizontal and not vertical:
        return tuple(ext)
    # A pair of near-parallel terminal sides belongs to a whole inline body.
    p = bw[box[1]:box[3] + 1, box[0]:box[2] + 1]
    if horizontal:
        sides = (p[:, :2].sum(), p[:, -2:].sum())
        complete = min(sides) >= .55 * h
        perpendicular = box[1] - ext[1] > 2 or ext[3] - box[3] > 2
        along = box[0] - ext[0] > .3 * w or ext[2] - box[2] > .3 * w
    else:
        sides = (p[:2].sum(), p[-2:].sum())
        complete = min(sides) >= .55 * w
        perpendicular = box[0] - ext[0] > 2 or ext[2] - box[2] > 2
        along = box[1] - ext[1] > .3 * h or ext[3] - box[3] > .3 * h
    if complete and (perpendicular or along):
        return tuple(box)
    return tuple(ext)


# Spelled-out name used by the page pipeline integration.
protected_extent = protect_extent


def _longest_ink_run(values):
    indices = np.flatnonzero(values)
    if not len(indices):
        return 0, 0, -1
    runs = np.split(indices, np.flatnonzero(np.diff(indices) > 1) + 1)
    run = max(runs, key=len)
    return len(run), int(run[0]), int(run[-1])


def body_extent(bw, obj, gray=None):
    """Refit only verified body ink, without changing a model's class.

    A closed round instrument's original outline can be more precise than B6's
    envelope containing a tangent marker. For a small vertical valve, matching
    continuous terminal bars recover the width of the bowtie and distinguish
    it from the continuing narrow shaft. The search is bounded to three raster
    pixels; uncertain shapes and horizontal valve variants retain their boxes.
    """
    box = tuple(obj["bbox"])
    cls = obj.get("class")
    if gray is not None:
        proposal = RBG.propose(gray, obj, text_h=CV.SC.text_h)
        if proposal is not None:
            return tuple(proposal["bbox"])
    if cls in {"instrument/circle", "valve_tag"}:
        start = tuple(obj.get("start_bbox") or box)
        w, h = _wh(start)
        # A tag leader can legitimately enlarge a moderate envelope. Restrict
        # the new tag correction to gross compound envelopes (approximately
        # twice the body area, allowing raster rounding); preserve smaller
        # previously judged envelopes.
        if cls == "valve_tag" and CV.area(box) < 1.9 * CV.area(start):
            return box
        if CV.area(box) <= 1.08 * CV.area(start) or min(w, h) < 3 * CV.SC.text_h or not .85 <= w / h <= 1.15:
            return box
        patch = bw[start[1]:start[3] + 1, start[0]:start[2] + 1]
        contours, hierarchy = cv2.findContours(patch, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        if hierarchy is None:
            return box
        holes = [c for i, c in enumerate(contours) if hierarchy[0][i][3] >= 0
                 and cv2.contourArea(c) >= .1 * w * h]
        if not holes:
            return box
        joined = np.concatenate(holes)
        _, _, inner_w, inner_h = cv2.boundingRect(joined)
        # The whole circle can contain a divider and text holes. Its dominant
        # enclosed cells still span a near-square, mostly white body.
        if min(inner_w, inner_h) < .85 * min(w, h) or not .85 <= inner_w / inner_h <= 1.15 \
                or sum(cv2.contourArea(c) for c in holes) < .45 * w * h \
                or not .60 <= cv2.contourArea(cv2.convexHull(joined)) / (inner_w * inner_h) <= .88:
            return box
        return start
    if cls not in ("valve/filled", "valve/outline"):
        return box
    w, h = _wh(box)
    if h <= w or min(w, h) < 7 or not 1.45 <= h / w <= 3.8 or h > 5 * CV.SC.text_h:
        return box
    pad = 3
    x0, y0 = max(0, box[0] - pad), max(0, box[1] - pad)
    x1, y1 = min(bw.shape[1] - 1, box[2] + pad), min(bw.shape[0] - 1, box[3] + pad)
    patch = bw[y0:y1 + 1, x0:x1 + 1].T
    along0 = box[1] - y0
    terminals = []
    for expected in (along0, along0 + h - 1):
        trials = []
        for j in range(max(0, expected - pad), min(patch.shape[1], expected + pad + 1)):
            count, low, high = _longest_ink_run(patch[:, j])
            if count >= .65 * w:
                trials.append((count, -abs(j - expected), j, low, high))
        if not trials:
            return box
        _, _, j, low, high = max(trials)
        terminals.append((j, low, high))
    top, bottom = terminals
    if bottom[0] - top[0] < .75 * (h - 1) or max(abs(top[k] - bottom[k]) for k in (1, 2)) > 2:
        return box
    if _longest_ink_run(patch[:, (top[0] + bottom[0]) // 2])[0] > \
            .82 * min(top[2] - top[1] + 1, bottom[2] - bottom[1] + 1):
        return box
    low, high = min(top[1], bottom[1]), max(top[2], bottom[2])
    if cls == "valve/outline":
        # One side of the open bowtie is a continuous rail; the other consists
        # of two oblique halves. A nearby handwheel has no matching end rails.
        if max(_longest_ink_run(row[along0:along0 + h])[0] for row in patch) < .75 * h:
            return box
        fitted = (x0 + low, box[1], x0 + high, box[3])
    else:
        fitted = (x0 + low, y0 + top[0], x0 + high, y0 + bottom[0])
    if max(abs(a - b) for a, b in zip(fitted, box)) > pad:
        return box
    return fitted


def refine(bw, objects, cands, profile_kind="pid", gray=None):
    """Post-classification guard against tiny junctions and duplicate fragments.

    This guard does not invent labels. New/replaced proposals go through the
    normal S2 and C1 questions. It refits verified body ink, removes clear
    structural duplicates and tiny junctions; richer replacements are made by
    ``propose`` before judgment.
    """
    if profile_kind != "pid":
        return objects, [], []
    out, dropped, notes = [], [], []
    refitted = 0
    for original in objects:
        o = copy.deepcopy(original)
        if _small_noise(o["bbox"], bw) and not AG.verified_small_arrow(bw, o, o.get("shape_proposal")):
            o["geometry_reason"] = "tiny junction/noise or sheet-border mark"
            dropped.append(o)
            continue
        fitted = body_extent(bw, o, gray=gray)
        if fitted != tuple(o["bbox"]):
            o["geometry_reason"] = f"verified body ink extent; previous bbox {o['bbox']}"
            o["bbox"] = list(fitted)
            refitted += 1
        out.append(o)
    # A complete, same-class body supersedes an overlapping contained fragment.
    keep = []
    for i, o in enumerate(out):
        b = o["bbox"]
        separate_coil = o.get("equipment_geometry", {}).get("kind") == "framed_coil"
        separate_arrow = AG.verified_small_arrow(bw, o, o.get("shape_proposal"))
        duplicate = next((p for j, p in enumerate(out) if j != i and p.get("class") == o.get("class")
                          and CV.inter(b, p["bbox"]) / max(1, CV.area(b) + CV.area(p["bbox"]) - CV.inter(b, p["bbox"])) >= .95
                          and (CV.area(p["bbox"]) > CV.area(b) or (CV.area(p["bbox"]) == CV.area(b) and j < i))), None)
        bigger = next((p for j, p in enumerate(out) if not separate_coil and not separate_arrow and j != i and p.get("class") == o.get("class")
                       and (CV.area(p["bbox"]) > 1.12 * CV.area(b)
                            or (p.get("equipment_geometry", {}).get("routing_obstacle")
                                and CV.area(p["bbox"]) > CV.area(b)
                                and CV.area(b) >= .45 * CV.area(p["bbox"])))
                       and CV.contains(p["bbox"], b, 2)), None)
        fragment = None
        if not separate_coil and not separate_arrow and (o.get("s2") or {}).get("symbol_part", 0) > .8:
            for j, p in enumerate(out):
                if j == i or p.get("class") != o.get("class"):
                    continue
                overlap = CV.inter(b, p["bbox"])
                # A partial candidate covering only one end of a verified
                # same-class body plus unrelated label ink is redundant.
                if overlap >= .35 * CV.area(b) and overlap < .75 * CV.area(p["bbox"]) \
                        and (p.get("class_confidence") or 0) > (o.get("class_confidence") or 0) + .1:
                    fragment = p
                    break
        if bigger or fragment or duplicate:
            o["geometry_reason"] = "same-class fragment contained by a more complete proposal"
            dropped.append(o)
        else:
            keep.append(o)
    if dropped:
        notes.append(f"geometry removed {len(dropped)} tiny or contained duplicate proposals")
    if refitted:
        notes.append(f"geometry refitted {refitted} verified body extents without changing classes")
    return keep, dropped, notes
