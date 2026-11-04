"""Closed vessel and framed coil proposals from the drawing's own geometry.

The normal symbol proposals use individual white holes. A tank crossed by
internal lines has several holes, and a dense heater coil has only tiny holes.
This module recovers those envelopes without naming equipment from text or
assigning a model class. Only verified large closed silhouettes are retained as
routing obstacles; a coil or an uncertain rectangular wire loop is never one.

All boxes are inclusive page pixels. Thresholds follow ``page_cv.SC.text_h``.
"""
from __future__ import annotations

import cv2
import numpy as np

import page_cv as CV


def _wh(box):
    return box[2] - box[0] + 1, box[3] - box[1] + 1


def _union(a, b):
    return min(a[0], b[0]), min(a[1], b[1]), max(a[2], b[2]), max(a[3], b[3])


def _iou(a, b):
    inter = CV.inter(a, b)
    return inter / max(1, CV.area(a) + CV.area(b) - inter)


def _close(a, b, gap=2):
    return a[0] <= b[2] + gap and b[0] <= a[2] + gap and a[1] <= b[3] + gap and b[1] <= a[3] + gap


def _holes(bw):
    """Retain contours too small for generic holes, needed for dense coils."""
    contours, hierarchy = cv2.findContours(bw, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    if hierarchy is None:
        return []
    out = []
    for contour, entry in zip(contours, hierarchy[0]):
        if entry[3] < 0:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        box = (x, y, x + w - 1, y + h - 1)
        out.append({"bbox": box, "contour": contour, "area": cv2.contourArea(contour)})
    return out


def _edge_runs(patch, band=3):
    return (np.count_nonzero(patch[:, :band].sum(axis=1)),
            np.count_nonzero(patch[:, -band:].sum(axis=1)),
            np.count_nonzero(patch[:band].sum(axis=0)),
            np.count_nonzero(patch[-band:].sum(axis=0)))


def _rounded(bw, box):
    """Four sided support and rounded ends exclude grids and pipe envelopes."""
    w, h = _wh(box)
    th = CV.SC.text_h
    if min(w, h) < 5 * th or max(w, h) < 10 * th or max(w, h) > 5.5 * min(w, h):
        return False
    patch = bw[box[1]:box[3] + 1, box[0]:box[2] + 1]
    corner = max(3, int(.09 * min(w, h)))
    corners = [patch[:corner, :corner], patch[:corner, -corner:],
               patch[-corner:, :corner], patch[-corner:, -corner:]]
    if sum(part.mean() < .04 for part in corners) < 3:
        return False
    left, right, top, bottom = _edge_runs(patch)
    if min(left, right) < .20 * h or min(top, bottom) < .20 * w:
        return False
    edge = max(3, int(.08 * min(w, h)))
    horizontal = (patch[:edge].sum(axis=1).max() >= .65 * w
                  and patch[-edge:].sum(axis=1).max() >= .65 * w)
    vertical = (patch[:, :edge].sum(axis=0).max() >= .65 * h
                and patch[:, -edge:].sum(axis=0).max() >= .65 * h)
    if not (horizontal or vertical):
        return False
    # A rounded cap progressively reaches the bounding box at mid-height or
    # mid-width. A text/pipe cluster with empty corners has no such silhouette.
    if horizontal:
        rows = np.flatnonzero(patch[:, :3].any(axis=1))
        rr = np.flatnonzero(patch[:, -3:].any(axis=1))
        return (rows[0] > .08 * h and rows[-1] < .92 * h
                and rr[0] > .08 * h and rr[-1] < .92 * h)
    cols = np.flatnonzero(patch[:3].any(axis=0))
    cc = np.flatnonzero(patch[-3:].any(axis=0))
    return (cols[0] > .08 * w and cols[-1] < .92 * w
            and cc[0] > .08 * w and cc[-1] < .92 * w)


def _pitched_vessel(bw, box, contour):
    """A closed tank with two upright walls, a pitched roof and flat base."""
    w, h = _wh(box)
    th = CV.SC.text_h
    if min(w, h) < 10 * th or not .7 <= h / w <= 4:
        return False
    patch = bw[box[1]:box[3] + 1, box[0]:box[2] + 1]
    left, right, top, bottom = _edge_runs(patch)
    if min(left, right) < .65 * h or bottom < .9 * w or top > .35 * w:
        return False
    # Open-ended internal pipe strokes indent the white-hole contour. They
    # cannot change the supported outer silhouette, so examine its convex
    # hull only after the original four edge-support checks above.
    hull = cv2.convexHull(contour)
    approx = cv2.approxPolyDP(hull, .004 * cv2.arcLength(hull, True), True).reshape(-1, 2)
    # Original ink must bound a simple five/six-vertex tank, not a polygonal
    # pipe network, equipment list or generic rectangle.
    if not 5 <= len(approx) <= 7 or cv2.contourArea(contour) < .80 * w * h:
        return False
    roof = approx[approx[:, 1] < box[1] + .23 * h]
    apex = roof[np.argmin(roof[:, 1])] if len(roof) else None
    return (len(roof) >= 3 and box[0] + .25 * w <= apex[0] <= box[0] + .75 * w
            and .035 * h <= np.ptp(roof[:, 1]) <= .23 * h)


def _supported_hull(bw, box, holes):
    """The entire convex outside boundary must exist in the original ink.

    Empty corners and supported bbox sides alone allow a nearby closed pipe
    loop to extend a tank. That extension invents an unsupported diagonal on
    their convex envelope, which this raw-pixel check rejects.
    """
    contours = [h["contour"] for h in holes if CV.contains(box, h["bbox"], 1)]
    if not contours:
        return False
    hull = cv2.convexHull(np.concatenate(contours))
    local = hull - np.array([[[box[0], box[1]]]], np.int32)
    w, h = _wh(box)
    border = np.zeros((h, w), np.uint8)
    cv2.drawContours(border, [local], -1, 1, 1)
    distances = cv2.distanceTransform(1 - bw[box[1]:box[3] + 1, box[0]:box[2] + 1], cv2.DIST_L2, 3)
    values = distances[border != 0]
    return bool(len(values) and np.mean(values <= 2.2) >= .96)


def _vessels(bw, holes):
    th = CV.SC.text_h
    large = [h for h in holes if min(_wh(h["bbox"])) >= 2.5 * th and h["area"] >= 18 * th * th]
    trial_boxes = {h["bbox"] for h in large}
    # Examine local pair envelopes instead of unioning an entire touching
    # cluster. A pipe loop outside a tank can share an edge with its interior.
    for i, first in enumerate(large):
        for second in large[i + 1:]:
            if _close(first["bbox"], second["bbox"]):
                trial_boxes.add(_union(first["bbox"], second["bbox"]))
    # A tank may be divided both horizontally and vertically. Grow local
    # envelopes a few cells further, keeping trials smaller than a page region;
    # none become proposals until their raw cap/wall support is verified.
    frontier = set(trial_boxes)
    for _ in range(3):
        expanded = set()
        for box in frontier:
            for item in large:
                cell = item["bbox"]
                if not _close(box, cell) or CV.contains(box, cell, 1):
                    continue
                union = _union(box, cell)
                w, h = _wh(union)
                if (min(w, h) < 3 * th or max(w, h) > 100 * th
                        or max(w, h) > 7 * min(w, h) or union in trial_boxes):
                    continue
                expanded.add(union)
        if not expanded:
            break
        trial_boxes |= expanded
        frontier = expanded
    rounded = [CV.snap_out(bw, b, max_grow=2, frac=.25) for b in trial_boxes
               if _rounded(bw, b) and _supported_hull(bw, b, holes)]
    pitched = [(h["bbox"], h) for h in large if _pitched_vessel(bw, h["bbox"], h["contour"])]
    out = []
    for box in sorted(set(rounded), key=CV.area, reverse=True):
        if any(CV.contains(other["bbox"], box, 2) for other in out):
            continue
        out.append({"bbox": box, "kind": "rounded_vessel", "body_bbox": box,
                    "routing_obstacle": True, "evidence": "closed rounded outer silhouette"})
    for body, hole in pitched:
        box = CV.snap_out(bw, body, max_grow=2, frac=.25)
        attachments = []
        # A narrow closed sump protrudes below the flat body and shares its
        # base. Do not absorb adjacent instrument circles or outgoing pipes.
        for small in holes:
            b = small["bbox"]
            sw, sh = _wh(b)
            w, h = _wh(body)
            patch = bw[b[1]:b[3] + 1, b[0]:b[2] + 1]
            l, r, t, bottom = _edge_runs(patch, 2)
            if (2 * th <= sw <= .25 * w and 1.5 * th <= sh <= .20 * h
                    and body[0] + .10 * w < b[0] and b[2] < body[2] - .02 * w
                    and abs(b[1] - body[3]) <= 2 and b[3] > body[3] + th
                    and min(l, r) >= .85 * sh and min(t, bottom) >= .85 * sw):
                attachments.append(b)
                box = _union(box, CV.snap_out(bw, b, max_grow=1, frac=.4))
        out.append({"bbox": box, "kind": "pitched_vessel", "body_bbox": body,
                    "attachments": attachments, "routing_obstacle": True,
                    "evidence": "closed pitched roof and parallel walls"})
    return out


def _horizontal_coils(bw, holes):
    th = CV.SC.text_h
    thin = []
    for item in holes:
        box = item["bbox"]
        w, h = _wh(box)
        if 2 <= w <= .6 * th and .65 * th <= h <= 1.7 * th and h >= 1.8 * w:
            thin.append(box)
    groups = []
    for box in sorted(thin, key=lambda b: (b[1], b[0])):
        group = next((g for g in groups if abs(g[0][1] - box[1]) <= 1
                      and abs(g[0][3] - box[3]) <= 1), None)
        if group is None:
            groups.append([box])
        else:
            group.append(box)
    out = []
    for aligned in groups:
        aligned.sort(key=lambda b: b[0])
        runs = [[]]
        for b in aligned:
            if runs[-1] and b[0] - runs[-1][-1][2] > .6 * th:
                runs.append([])
            runs[-1].append(b)
        for run in runs:
            if len(run) < 6:
                continue
            centres = np.array([(b[0] + b[2]) / 2 for b in run])
            gaps = np.diff(centres)
            if np.max(abs(gaps - np.median(gaps))) > max(1, .15 * np.median(gaps)):
                continue
            box = run[0]
            for b in run[1:]:
                box = _union(box, b)
            box = CV.snap_out(bw, box, max_grow=2, frac=.75)
            w, h = _wh(box)
            patch = bw[box[1]:box[3] + 1, box[0]:box[2] + 1]
            if min(patch[:2].any(axis=0).mean(), patch[-2:].any(axis=0).mean()) < .9:
                continue
            terminal = None
            for item in holes:
                b = item["bbox"]
                sw, sh = _wh(b)
                if (sw < .6 * th or not h <= sh <= 3 * h
                        or abs((b[1] + b[3]) - (box[1] + box[3])) > .35 * sh
                        or not (abs(b[0] - box[2]) <= 3 or abs(b[2] - box[0]) <= 3)):
                    continue
                p = bw[b[1]:b[3] + 1, b[0]:b[2] + 1]
                l, r, t, bottom = _edge_runs(p, 2)
                if min(l, r) < .8 * sh or min(t, bottom) < .8 * sw:
                    continue
                terminal = b
                break
            if terminal is None:
                continue
            out.append({"bbox": _union(box, terminal), "kind": "framed_coil",
                        "coil_bbox": box, "terminal_bbox": terminal, "cells": len(run),
                        "routing_obstacle": False,
                        "evidence": "uniform narrow enclosed cells and attached closed terminal"})
    return out


def _coils(bw, holes):
    out = _horizontal_coils(bw, holes)
    rotated_holes = [{**item, "bbox": (item["bbox"][1], item["bbox"][0],
                                       item["bbox"][3], item["bbox"][2])} for item in holes]
    for proposal in _horizontal_coils(bw.T, rotated_holes):
        proposal = dict(proposal)
        for key in ("bbox", "coil_bbox", "terminal_bbox"):
            b = proposal[key]
            proposal[key] = (b[1], b[0], b[3], b[2])
        out.append(proposal)
    return out


def detect(bw, regions=None, exclude=(), profile_kind="pid"):
    """Return geometric proposals and provenance, with no model class guess."""
    if profile_kind != "pid":
        return []
    regions = regions or [(0, 0, bw.shape[1] - 1, bw.shape[0] - 1)]
    holes = _holes(bw)
    proposals = _vessels(bw, holes) + _coils(bw, holes)
    return [item for item in proposals if CV._inside_any(item["bbox"], regions, 4)
            and not any(CV.inter(item["bbox"], box) > .5 * CV.area(item["bbox"]) for box in exclude)]


def propose(bw, regions=None, exclude=(), profile_kind="pid"):
    """Candidate boxes for S2/C1; existing candidates can be retained."""
    return [item["bbox"] for item in detect(bw, regions, exclude, profile_kind)]


def obstacle_mask(bw, proposals):
    """Fill verified closed body cells, including its outline, for wire tracing.

    The mask follows silhouettes rather than the whole candidate rectangle: an
    external pipe beside a protruding sump remains traceable. Classification
    uncertainty cannot turn a verified tank silhouette into a wire junction.
    """
    mask = np.zeros(bw.shape, np.uint8)
    holes = _holes(bw)
    for proposal in proposals:
        if not proposal.get("routing_obstacle"):
            continue
        body = proposal.get("body_bbox", proposal["bbox"])
        valid = [body] + list(proposal.get("attachments", []))
        for box in valid:
            # Closed vessel silhouettes and the checked rectangular sump are
            # convex. Internal open pipes indent their hole contours, so fill
            # their joint hull to stop those pipes becoming external junctions.
            contours = [item["contour"] for item in holes if CV.contains(box, item["bbox"], 2)]
            if contours:
                hull = cv2.convexHull(np.concatenate(contours))
                cv2.drawContours(mask, [hull], -1, 1, cv2.FILLED)
    # Covers the actual outline thickness. Does not fill an enclosing bbox or
    # synthesize a connection across a boundary that the raw ink did not draw.
    return cv2.dilate(mask, np.ones((3, 3), np.uint8))
