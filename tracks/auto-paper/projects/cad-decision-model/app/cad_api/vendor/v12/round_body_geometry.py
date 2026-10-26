"""Observe clipped round outlines and closed flow lobes in the original raster.

Only model-labelled round bodies are considered. The dark enclosed cells anchor
the circle; its grey outer contour supplies actual pixels, rather than padding.
Long axis stems are excluded from the circle fit. A side lobe needs its own
closed triangular interior and two arms tapering to an observed thin shaft.
"""
from __future__ import annotations

import hashlib

import cv2
import numpy as np


def _norm(points, ellipse):
    (cx, cy), (a, b), angle = ellipse
    t = np.deg2rad(angle)
    p = points - (cx, cy)
    u = p[:, 0] * np.cos(t) + p[:, 1] * np.sin(t)
    v = -p[:, 0] * np.sin(t) + p[:, 1] * np.cos(t)
    return np.hypot(u / (a / 2), v / (b / 2))


def _holes(mask):
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    if hierarchy is None:
        return contours, [], []
    return contours, [c for i, c in enumerate(contours) if hierarchy[0, i, 3] >= 0], \
        [c for i, c in enumerate(contours) if hierarchy[0, i, 3] < 0]


def _without_axis_shafts(points, mask, ellipse):
    """Remove a constant one/two-pixel shaft beyond a tapering round cap."""
    center = np.array(ellipse[0])
    radius = min(ellipse[1]) / 2
    limits = (mask.shape[1], mask.shape[0])
    keep = np.ones(len(points), dtype=bool)
    for axis in (0, 1):
        other = 1 - axis
        lo = max(0, int(np.floor(center[other] - radius)))
        hi = min(limits[other], int(np.ceil(center[other] + radius + 1)))
        for direction in (-1, 1):
            begin = int(round(center[axis] + direction * .65 * radius))
            stop = -1 if direction < 0 else limits[axis]
            profiles = []
            for at in range(begin, stop, direction):
                line = mask[lo:hi, at] if axis == 0 else mask[at, lo:hi]
                ink = np.flatnonzero(line) + lo
                profiles.append((at, ink))
            for i in range(len(profiles) - 2):
                at, ink = profiles[i]
                if len(ink) not in (1, 2) or abs(ink.mean() - center[other]) > max(1, .10 * radius):
                    continue
                if not all(np.array_equal(ink, profiles[j][1]) for j in (i + 1, i + 2)):
                    continue
                keep &= direction * (points[:, axis] - at) < 0
                break
    return points[keep]


def _closed_lobe(holes, light, circle, box, drift):
    """A closed, centred side triangle ends at the first shaft-width column."""
    x0, y0, x1, y1 = circle
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    diameter = y1 - y0 + 1
    found = []
    for contour in holes:
        x, y, w, h = cv2.boundingRect(contour)
        if not .12 * diameter <= h <= .40 * diameter or not .35 <= w / h <= 1.5:
            continue
        if abs(y + (h - 1) / 2 - cy) > max(1.5, .07 * diameter):
            continue
        hull = cv2.convexHull(contour)
        share = cv2.contourArea(hull) / (w * h)
        approx = cv2.approxPolyDP(hull, .09 * cv2.arcLength(hull, True), True)
        if not .30 <= share <= .70 or not 3 <= len(approx) <= 4:
            continue
        for direction in (-1, 1):
            edge = x0 if direction < 0 else x1
            base = x + w - 1 if direction < 0 else x
            if abs(base - edge) > 2 or direction * (x + (w - 1) / 2 - edge) < 1:
                continue
            # Observe the shaft beyond the proposed tip, while any returned
            # body boundary remains within the three-pixel drift limit.
            stop = box[0] - drift - 3 if direction < 0 else box[2] + drift + 3
            columns = list(range(base, stop + direction, direction))
            columns = [j for j in columns if 0 <= j < light.shape[1]]
            lo = max(0, int(round(cy - h / 2 - 2)))
            hi = min(light.shape[0], int(round(cy + h / 2 + 3)))
            profiles = []
            for j in columns:
                ink = np.flatnonzero(light[lo:hi, j]) + lo
                profiles.append((j, int(ink[0]), int(ink[-1])) if len(ink) else (j, 0, -1))
            if len(profiles) < 7 or any(b < a for _, a, b in profiles):
                continue
            widths = np.array([b - a + 1 for _, a, b in profiles])
            shaft = int(np.median(widths[-3:]))
            if shaft < 1 or shaft > 2 or np.any(widths[-3:] != shaft):
                continue
            wide = np.flatnonzero(widths > shaft)
            if len(wide) < 3 or wide[-1] + 3 >= len(widths):
                continue
            end = int(wide[-1])
            if widths[0] < shaft + 4 or np.mean(np.diff(widths[:end + 1]) <= 1) < .85:
                continue
            if sum(a < cy - .5 and b > cy + .5 for _, a, b in profiles[:end]) < 3:
                continue
            tip = profiles[end + 1][0]
            old = box[0] if direction < 0 else box[2]
            if not 0 < direction * (tip - old) <= drift:
                continue
            found.append((direction, tip))
    return found[0] if len(found) == 1 else None


def propose(gray, obj, text_h=9, max_drift=3):
    """Return an independently observed body proposal, or None when uncertain."""
    if obj.get("class") not in {"actuator/motor", "instrument/circle"}:
        return None
    gray = np.asarray(gray)
    if gray.ndim != 2 or gray.dtype != np.uint8:
        return None
    box = tuple(map(int, obj["bbox"]))
    w, h = box[2] - box[0] + 1, box[3] - box[1] + 1
    if min(w, h) < max(10, 1.2 * text_h) or h > 6 * text_h or not .85 <= w / h <= 1.45:
        return None
    # At this raster size one pixel already changes a side by six percent.
    # An unbalanced small envelope may already include the complete rim on
    # one axis. Grey fringe alone cannot prove that both axes were clipped.
    if min(w, h) < 2 * text_h and w != h:
        return None
    pad = max_drift + 3
    ox, oy = max(0, box[0] - pad), max(0, box[1] - pad)
    ex, ey = min(gray.shape[1], box[2] + pad + 1), min(gray.shape[0], box[3] + pad + 1)
    patch = gray[oy:ey, ox:ex]
    local = (box[0] - ox, box[1] - oy, box[2] - ox, box[3] - oy)
    _, dark_holes, _ = _holes((patch < 128).astype(np.uint8))
    cells = []
    for c in dark_holes:
        x, y, a, b = cv2.boundingRect(c)
        if cv2.contourArea(c) < .08 * w * h or min(a, b) < .30 * h:
            continue
        if abs(x + (a - 1) / 2 - (local[0] + local[2]) / 2) > .30 * h \
                or abs(y + (b - 1) / 2 - (local[1] + local[3]) / 2) > .30 * h:
            continue
        cells.append(c)
    if not cells:
        return None
    hull = cv2.convexHull(np.concatenate(cells))
    x, y, a, b = cv2.boundingRect(hull)
    if min(a, b) < .72 * h or not .85 <= a / b <= 1.15 \
            or not .60 <= cv2.contourArea(hull) / (a * b) <= .88:
        return None
    cx, cy = x + (a - 1) / 2, y + (b - 1) / 2
    radius = (a + b) / 4
    light = (patch < 200).astype(np.uint8)
    _, light_holes, outer = _holes(light)
    parents = [c for c in outer if cv2.pointPolygonTest(c, (float(cx), float(cy)), False) >= 0]
    if not parents:
        return None
    contour = min(parents, key=cv2.contourArea)
    points = contour.reshape(-1, 2).astype(float)
    delta = points - (cx, cy)
    distance = np.linalg.norm(delta, axis=1)
    fit = (distance >= .75 * radius) & (distance <= 1.4 * radius) \
        & (abs(delta[:, 0]) > .23 * radius) & (abs(delta[:, 1]) > .23 * radius)
    sample = points[fit]
    if len(sample) < 16:
        return None
    if any(np.sum(((sample[:, 0] > cx) == sx) & ((sample[:, 1] > cy) == sy)) < 2
           for sx, sy in ((False, False), (False, True), (True, False), (True, True))):
        return None
    initial = len(sample)
    for _ in range(3):
        ellipse = cv2.fitEllipse(sample.astype(np.float32).reshape(-1, 1, 2))
        axes = ellipse[1]
        if min(axes) <= 0 or max(axes) / min(axes) > 1.17:
            return None
        tolerance = max(.03, .8 / (min(axes) / 2))
        good = abs(_norm(sample, ellipse) - 1) <= tolerance
        if good.all():
            break
        sample = sample[good]
        if len(sample) < max(16, .82 * initial):
            return None
    if np.linalg.norm(np.array(ellipse[0]) - (cx, cy)) > .12 * h \
            or not .80 * h <= min(ellipse[1]) <= 1.20 * h:
        return None
    norm = _norm(points, ellipse)
    observed = points[abs(norm - 1) <= tolerance]
    observed = _without_axis_shafts(observed, light, ellipse)
    if len(observed) < 2 * h:
        return None
    circle = tuple(map(int, (observed[:, 0].min(), observed[:, 1].min(),
                             observed[:, 0].max(), observed[:, 1].max())))
    lobe = _closed_lobe(light_holes, light, circle, local, max_drift) \
        if obj["class"] == "instrument/circle" else None
    # Ordinary instrument circles already have a conservative dark-ink body
    # extent. Preserve it: an anti-aliased rim alone does not justify changing
    # their exported geometry. Only a separately closed flow lobe supplies
    # additional body evidence for an instrument.
    if obj["class"] == "instrument/circle" and lobe is None:
        return None
    # Only a genuinely clipped envelope restores a round rim: opposite outer
    # arcs plus a missing arc on the other axis. A merely shifted envelope or
    # a one-pixel anti-alias fringe on an otherwise complete body is retained.
    left, top = circle[0] < local[0], circle[1] < local[1]
    right, bottom = circle[2] > local[2], circle[3] > local[3]
    clipped = (left and right and (top or bottom)) or (top and bottom and (left or right))
    if not clipped and lobe is None:
        return None
    fitted = [min(local[0], circle[0]), min(local[1], circle[1]),
              max(local[2], circle[2]), max(local[3], circle[3])]
    if lobe:
        fitted[0 if lobe[0] < 0 else 2] = lobe[1]
    fitted = [fitted[0] + ox, fitted[1] + oy, fitted[2] + ox, fitted[3] + oy]
    if fitted == list(box) or max(abs(a - b) for a, b in zip(fitted, box)) > max_drift:
        return None
    return {"bbox": fitted, "kind": "closed-round-outline-and-triangular-lobe" if lobe else "clipped-closed-round-outline",
            "raw_crop_sha256": hashlib.sha256(patch.tobytes()).hexdigest(),
            "max_pixel_drift": max(abs(a - b) for a, b in zip(fitted, box)),
            "source": "original gray<200 contour anchored by dark enclosed cells"}
