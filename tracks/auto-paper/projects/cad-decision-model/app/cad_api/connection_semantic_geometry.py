"""Finite raw-ink hypotheses for a later Decision Model semantic judgment.

Geometry proposes what to inspect. It never accepts a link, paints a gap,
modifies an object, or combines nets. A straight underpass can continue only
between opposite arms of its own axis; it cannot join the crossing line.
"""
from __future__ import annotations

import hashlib
import math

import cv2
import numpy as np

REVISION = "geometry-local-route-v15-semantic-geometry"
HYPOTHESIS_KINDS = ("solid_continuation", "dashed_continuation", "crossing_underpass_no_join",
                    "crossing_ambiguous", "junction_join", "unresolved_break")
RAW_THRESHOLD = 210
_DIRECTIONS = {"left": (-1, 0), "right": (1, 0), "top": (0, -1), "bottom": (0, 1)}


def finite_path(path, shape):
    """Validate finite code coordinates without moving/snapping their centres."""
    if not isinstance(path, (tuple, list)) or not 2 <= len(path) <= 8192:
        raise ValueError("A path must contain 2–8192 finite points")
    h, w = shape[:2]
    result = []
    for point in path:
        if (not isinstance(point, (tuple, list)) or len(point) != 2
                or not all(type(v) in (int, float) and math.isfinite(v) for v in point)
                or not 0 <= point[0] < w or not 0 <= point[1] < h):
            raise ValueError("Path coordinates must be finite original-image positions")
        p = [int(v) if float(v).is_integer() else float(v) for v in point]
        if not result or p != result[-1]:
            result.append(p)
    if len(result) < 2:
        raise ValueError("A path requires two distinct positions")
    return result


def _axis(a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    if dx and abs(dx) >= 4 * abs(dy):
        return "horizontal", (1 if dx > 0 else -1, 0)
    if dy and abs(dy) >= 4 * abs(dx):
        return "vertical", (0, 1 if dy > 0 else -1)
    return None, None


def classify_turns(path):
    """Describe only the requested path; no inferred branch is created."""
    result = []
    for index in range(1, len(path) - 1):
        previous, point, following = path[index - 1:index + 2]
        incoming_axis, incoming = _axis(point, previous)
        outgoing_axis, outgoing = _axis(point, following)
        opposite = incoming is not None and outgoing == (-incoming[0], -incoming[1])
        result.append({"index": index, "point": list(point), "incoming_arm": incoming,
                       "outgoing_arm": outgoing, "same_axis": bool(incoming_axis and incoming_axis == outgoing_axis),
                       "opposite_arms": opposite, "turning": not opposite})
    return result


def _path_samples(path):
    points = []
    for a, b in zip(path, path[1:]):
        steps = max(1, math.ceil(max(abs(b[0] - a[0]), abs(b[1] - a[1]))))
        for step in range(steps + 1):
            p = [round(a[0] + (b[0] - a[0]) * step / steps),
                 round(a[1] + (b[1] - a[1]) * step / steps)]
            if not points or p != points[-1]:
                points.append(p)
    return points


def _region_box(region):
    box = region.get("bbox") if isinstance(region, dict) else region
    return box if isinstance(box, (tuple, list)) and len(box) == 4 else None


def blocked_by_regions(path, objects=(), tables=()):
    """Reject an interior bridge; touching an observed body boundary is allowed."""
    samples = np.asarray(_path_samples(path), dtype=float)
    blockers = []
    for source, regions in (("object", objects), ("table", tables)):
        for index, region in enumerate(regions):
            box = _region_box(region)
            if box is None:
                continue
            x0, y0, x1, y1 = box
            # Interiors, not merely the surrounding figure context, exclude a
            # candidate. Every object class including text is protected.
            if source == "table" or isinstance(region, dict) and region.get("class") == "text":
                inside = ((samples[:, 0] >= x0) & (samples[:, 0] <= x1)
                          & (samples[:, 1] >= y0) & (samples[:, 1] <= y1))
            else:
                inside = ((samples[:, 0] > x0) & (samples[:, 0] < x1)
                          & (samples[:, 1] > y0) & (samples[:, 1] < y1))
            if inside.any():
                blockers.append({"source": source,
                                 "id": region.get("id", str(index)) if isinstance(region, dict) else str(index),
                                 "class": region.get("class") if isinstance(region, dict) else None,
                                 "bbox": list(box)})
    return blockers


def _gray(page):
    array = np.asarray(page)
    if array.ndim == 2:
        return array
    if array.ndim == 3 and array.shape[2] in (3, 4):
        return cv2.cvtColor(array, cv2.COLOR_BGRA2GRAY if array.shape[2] == 4 else cv2.COLOR_BGR2GRAY)
    raise ValueError("The original page must be a grayscale, BGR, or BGRA image")


def _ink(raw, point):
    x, y = map(round, point)
    return 0 <= y < raw.shape[0] and 0 <= x < raw.shape[1] and bool(raw[y, x])


def _runs(values):
    result = []
    for index, value in enumerate(values):
        if not result or result[-1]["ink"] != bool(value):
            result.append({"ink": bool(value), "start": index, "end": index})
        else:
            result[-1]["end"] = index
    return result


def _hypothesis(kind, center, **fields):
    return {"kind": kind, "status": "hypothesis", "model_required": True,
            "center": list(center), **fields}


def _raster_tolerance(text_h):
    # This is an observation corridor, not a coordinate correction. A single
    # coherent original row/column must supply each proposed arm.
    return max(1, min(3, round(.30 * text_h)))


def _protected_point(point, objects, tables):
    x, y = point
    for source, regions in (("object", objects), ("table", tables)):
        for region in regions:
            box = _region_box(region)
            if box is None:
                continue
            x0, y0, x1, y1 = box
            inclusive = source == "table" or isinstance(region, dict) and region.get("class") == "text"
            if ((x0 <= x <= x1 and y0 <= y <= y1) if inclusive
                    else (x0 < x < x1 and y0 < y < y1)):
                return True
    return False


def _nearby_regions(path, regions, radius):
    """Prune observation lookups only; final body/path checks stay global."""
    xs, ys = zip(*path)
    x0, y0, x1, y1 = min(xs) - radius, min(ys) - radius, max(xs) + radius, max(ys) + radius
    return [region for region in regions if (box := _region_box(region)) is not None
            and box[0] <= x1 and box[2] >= x0 and box[1] <= y1 and box[3] >= y0]


def _observed_ray(raw, center, direction, radius, objects=(), tables=()):
    """Stop context at a protected region; never mask or bridge its pixels."""
    dx, dy = direction
    points = []
    for distance in range(1, radius + 1):
        point = [round(center[0] + dx * distance), round(center[1] + dy * distance)]
        if (not 0 <= point[0] < raw.shape[1] or not 0 <= point[1] < raw.shape[0]
                or _protected_point(point, objects, tables)):
            break
        points.append(point)
    return points, [_ink(raw, point) for point in points]


def _regular_pattern(values, text_h, minimum_strokes=3):
    """A clipped first/last dash may be short; two full gaps still need support.

    Dash-centre periods, rather than starts, tolerate a partial stroke at an
    elbow or the boundary of a small local view. Isolated long stroke breaks
    and irregular fragments cannot establish a periodic pattern.
    """
    runs = [r for r in _runs(values) if r["ink"] and r["end"] - r["start"] + 1 >= 2]
    maximum_width, maximum_gap = max(6, round(2.5 * text_h)), max(4, round(1.5 * text_h))
    chains, chain = [], []
    for run in runs:
        width = run["end"] - run["start"] + 1
        gap = run["start"] - chain[-1]["end"] - 1 if chain else None
        if width > maximum_width or gap is not None and not 2 <= gap <= maximum_gap:
            if len(chain) >= minimum_strokes:
                chains.append(chain)
            chain = []
        if width <= maximum_width:
            chain.append(run)
    if len(chain) >= minimum_strokes:
        chains.append(chain)
    patterns = []
    for chain in chains:
        gaps = [b["start"] - a["end"] - 1 for a, b in zip(chain, chain[1:])]
        centres = [(r["start"] + r["end"]) / 2 for r in chain]
        periods = [b - a for a, b in zip(centres, centres[1:])]
        period, gap = float(np.median(periods)), float(np.median(gaps))
        if (period < max(4, .60 * text_h)
                or max(abs(p - period) for p in periods) > max(2, .35 * period)
                or max(abs(g - gap) for g in gaps) > max(2, .35 * gap)):
            continue
        patterns.append({"runs": chain, "regular_gap_lengths": gaps, "median_period": period,
                         "median_gap": gap, "observed_stroke_runs": len(chain),
                         "periodic_context": len(chain) >= 3})
    return patterns


def _observe(hypothesis, requested_center, tolerance):
    hypothesis["observed_center"] = list(hypothesis["center"])
    hypothesis["center"] = list(requested_center)
    hypothesis["raster_offset"] = [hypothesis["observed_center"][i] - requested_center[i] for i in (0, 1)]
    hypothesis["raster_tolerance"] = tolerance
    return hypothesis


def _tolerant_local(callback, raw, center, text_h, *, ink_only=True, objects=(), tables=()):
    """Observe one coherent nearby raster junction, retaining the code centre."""
    tolerance = _raster_tolerance(text_h)
    x, y = map(round, center)
    offsets = [(dx, dy) for dx in range(-tolerance, tolerance + 1)
               for dy in range(-tolerance, tolerance + 1)]
    offsets.sort(key=lambda p: (p[0] * p[0] + p[1] * p[1], p))
    found = []
    for dx, dy in offsets:
        observation = [x + dx, y + dy]
        if (not 0 <= observation[0] < raw.shape[1] or not 0 <= observation[1] < raw.shape[0]
                or _protected_point(observation, objects, tables)
                or ink_only and not _ink(raw, observation)):
            continue
        hypothesis = callback(raw, observation, text_h)
        if not hypothesis:
            continue
        if dx == dy == 0:
            return _observe(hypothesis, center, tolerance)
        arm_count = (len(hypothesis.get("dashed_arms", [])) or
                     sum(arm.get("present", False) for arm in hypothesis.get("arms", [])))
        # Preserve four-arm ambiguity when the same tiny observation corridor
        # also contains a three-arm slice of a thick crossing.
        found.append((arm_count, -(dx * dx + dy * dy), hypothesis))
    if not found:
        return None
    hypothesis = max(found, key=lambda item: item[:2])[2]
    return _observe(hypothesis, center, tolerance)


def _dash_hypothesis(raw, path, text_h, objects=(), tables=()):
    axis, direction = _axis(path[0], path[-1])
    if axis is None or any(_axis(a, b)[0] != axis for a, b in zip(path, path[1:])):
        return None
    points = _path_samples(path)
    along, across = (0, 1) if axis == "horizontal" else (1, 0)
    low, high = min(p[along] for p in points), max(p[along] for p in points)
    normal = round(float(np.median([p[across] for p in points])))
    tolerance, radius = _raster_tolerance(text_h), max(18, min(72, round(4.5 * text_h)))
    candidates = []
    for offset in sorted(range(-tolerance, tolerance + 1), key=lambda value: (abs(value), value)):
        observed_normal = normal + offset
        if max(abs(p[across] - observed_normal) for p in points) > tolerance:
            continue
        start = [low, observed_normal] if axis == "horizontal" else [observed_normal, low]
        end = [high, observed_normal] if axis == "horizontal" else [observed_normal, high]
        observed = _path_samples([start, end])
        if blocked_by_regions([start, end], objects, tables):
            continue
        before, _ = _observed_ray(raw, start, (-1, 0) if axis == "horizontal" else (0, -1),
                                  radius, objects, tables)
        after, _ = _observed_ray(raw, end, (1, 0) if axis == "horizontal" else (0, 1),
                                 radius, objects, tables)
        context = list(reversed(before)) + observed + after
        values = [_ink(raw, point) for point in context]
        for pattern in _regular_pattern(values, text_h):
            runs = pattern["runs"]
            # Repetition must actually cover this short route, including both
            # anchors; periodic ink far beyond an unexplained break is unused.
            support = [context[i][along] for run in runs for i in range(run["start"], run["end"] + 1)]
            max_gap = max(4, round(1.5 * text_h))
            if (not any(low <= value <= high for value in support)
                    or any(min(abs(anchor - value) for value in support) > max_gap for anchor in (low, high))
                    or min(support) > low + max_gap or max(support) < high - max_gap):
                continue
            breaks = [{"a": context[a["end"]], "b": context[b["start"]], "white_pixels": gap}
                      for a, b, gap in zip(runs, runs[1:], pattern["regular_gap_lengths"])]
            hypothesis = _hypothesis("dashed_continuation", points[len(points) // 2], axis=axis,
                         observed_stroke_runs=pattern["observed_stroke_runs"], observed_regular_gaps=breaks,
                         median_period=pattern["median_period"],
                         observed_paths=[[context[runs[0]["start"]], context[runs[-1]["end"]]]],
                         raster_tolerance=tolerance, raster_normal_offset=offset,
                         transition={"mode": "opposite_arms_only", "axis": axis, "joins_crossing_axis": False},
                         evidence="three_or_more_original_aligned_strokes_in_bounded_unprotected_context")
            candidates.append((offset, hypothesis))
    if candidates:
        supported_offsets = sorted({offset for offset, _ in candidates})
        # A coherent exact raster row/column is preferred. Otherwise two
        # separate parallel strokes cannot be selected by taking their maximum.
        if 0 not in supported_offsets and any(b - a > 1 for a, b in zip(supported_offsets, supported_offsets[1:])):
            return None
        return min(candidates, key=lambda item: (abs(item[0]), -item[1]["observed_stroke_runs"]))[1]
    # A body-adjacent arm can contain only two dashes. It needs an independently
    # repeating perpendicular arm with matching periods, not an invented third
    # stroke inside the object.
    for center in (path[0], path[-1]):
        callback = lambda ink, point, height: _dashed_junction(ink, point, height, objects, tables)
        junction = _tolerant_local(callback, raw, center, text_h, ink_only=False, objects=objects, tables=tables)
        if not junction or junction["kind"] != "junction_join":
            continue
        matching = [arm for arm in junction["dashed_arms"] if
                    _DIRECTIONS[arm["direction"]][across] == 0 and arm["observed_stroke_runs"] >= 2]
        references = [arm for arm in junction["dashed_arms"] if
                      _DIRECTIONS[arm["direction"]][along] == 0 and arm["periodic_context"]]
        if not matching or not references:
            continue
        arm = matching[0]
        reference = references[0]
        support_path = arm["observed_path"]
        support_low, support_high = sorted(point[along] for point in support_path)
        max_gap = max(4, round(1.5 * text_h))
        if low < support_low - max_gap or high > support_high + max_gap:
            continue
        return _hypothesis("dashed_continuation", points[len(points) // 2], axis=axis,
                          observed_stroke_runs=arm["observed_stroke_runs"],
                          observed_regular_gaps=arm["regular_gap_lengths"],
                          median_period=arm["median_period"], raster_tolerance=tolerance,
                          observed_paths=[arm["observed_path"], reference["observed_path"]],
                          periodic_reference_arm=reference,
                          transition={"mode": "opposite_arms_only", "axis": axis, "joins_crossing_axis": False},
                          evidence="two_original_short_arm_strokes_match_a_repeating_perpendicular_context_arm")
    return None


def _arm_values(raw, center, direction, radius):
    dx, dy = direction
    return [_ink(raw, [center[0] + dx * distance, center[1] + dy * distance])
            for distance in range(1, radius + 1)]


def _arm(raw, center, name, radius):
    values = _arm_values(raw, center, _DIRECTIONS[name], radius)
    near = values[:min(3, radius)]
    return {"direction": name, "observed_pixels": sum(values), "samples": radius,
            "support": round(sum(values) / radius, 4),
            "near_support": round(sum(near) / len(near), 4),
            "present": sum(values) >= max(3, math.ceil(.65 * radius)),
            "touches_center": sum(near) >= max(2, math.ceil(.65 * len(near)))}


def _dot(raw, center, text_h):
    x, y = map(round, center)
    radius = max(2, min(4, round(.30 * text_h)))
    diagonal = [(dx, dy) for dx in range(-radius, radius + 1) for dy in range(-radius, radius + 1)
                if dx and dy and dx * dx + dy * dy <= radius * radius]
    count = sum(_ink(raw, [x + dx, y + dy]) for dx, dy in diagonal)
    return {"radius": radius, "diagonal_ink": count, "diagonal_samples": len(diagonal),
            "present": bool(diagonal and count >= .60 * len(diagonal))}


def _underpass(raw, center, axis, text_h):
    directions = (("left", "right", "top", "bottom") if axis == "horizontal"
                  else ("top", "bottom", "left", "right"))
    radius = max(7, min(22, round(1.4 * text_h)))
    own_a, own_b, cross_a, cross_b = directions
    perpendicular = [_arm(raw, center, name, radius) for name in (cross_a, cross_b)]
    if not all(arm["present"] and arm["touches_center"] for arm in perpendicular):
        return None
    gap_lengths = []
    original_anchors = []
    for name in (own_a, own_b):
        values = _arm_values(raw, center, _DIRECTIONS[name], radius)
        # The crossing axis itself occupies the centre. At least two white
        # original positions separate that axis from each opposite own arm.
        first = next((i for i in range(1, len(values) - 2)
                      if all(values[i:i + 3])), None)
        if first is None or sum(not v for v in values[:first]) < 2:
            return None
        if sum(values[first:]) / len(values[first:]) < .70:
            return None
        gap_lengths.append(first)
        dx, dy = _DIRECTIONS[name]
        original_anchors.append([round(center[0] + dx * (first + 1)), round(center[1] + dy * (first + 1))])
    if max(gap_lengths) > max(6, round(1.3 * text_h)):
        return None
    return _hypothesis("crossing_underpass_no_join", center, axis=axis,
                       opposite_arm_anchors=original_anchors, observed_white_gaps=gap_lengths,
                       crossing_axis="vertical" if axis == "horizontal" else "horizontal",
                       perpendicular_arms=perpendicular,
                       transition={"mode": "opposite_arms_only", "axis": axis, "joins_crossing_axis": False},
                       evidence="original_opposite_arms_gapped_around_an_observed_perpendicular_stroke")


def _local_junction(raw, center, text_h):
    radius = max(5, min(18, round(text_h)))
    arms = [_arm(raw, center, name, radius) for name in _DIRECTIONS]
    present = [arm for arm in arms if arm["present"]]
    touching = [arm for arm in present if arm["touches_center"]]
    if len(touching) < 2 or not _ink(raw, center):
        return None
    dot = _dot(raw, center, text_h)
    if len(touching) == 4 and not dot["present"]:
        return _hypothesis("crossing_ambiguous", center, arms=arms, dot=dot,
                           transition={"mode": "model_must_decide_crossing_vs_join"},
                           evidence="four_original_arms_with_no_distinct_join_dot")
    directions = {_DIRECTIONS[arm["direction"]] for arm in touching}
    elbow = len(touching) == 2 and not any((-dx, -dy) in directions for dx, dy in directions)
    if len(touching) >= 3 or elbow:
        return _hypothesis("junction_join", center, arms=arms, dot=dot,
                           junction_type="dot" if dot["present"] else "T" if len(touching) == 3 else "elbow",
                           transition={"mode": "observed_touching_arms_after_model_confirmation",
                                       "observed_arms": [arm["direction"] for arm in touching]},
                           evidence="original_visible_arm_contacts_at_the_same_T_dot_or_elbow")
    return None


def _regular_dash_arm(raw, center, name, text_h, objects=(), tables=()):
    radius = max(18, min(72, round(4.5 * text_h)))
    points, values = _observed_ray(raw, center, _DIRECTIONS[name], radius, objects, tables)
    patterns = _regular_pattern(values, text_h, minimum_strokes=2)
    patterns = [pattern for pattern in patterns if
                pattern["runs"][0]["start"] + 1 <= max(4, round(1.5 * text_h))]
    if not patterns:
        return None
    pattern = max(patterns, key=lambda p: (p["observed_stroke_runs"], -p["runs"][0]["start"]))
    runs = pattern.pop("runs")
    return {"direction": name, **pattern, "first_observed_distance": runs[0]["start"] + 1,
            "observed_positions": [r["start"] + 1 for r in runs],
            "observed_path": [points[runs[0]["start"]], points[runs[-1]["end"]]]}


def _dashed_junction(raw, center, text_h, objects=(), tables=()):
    arms = [_regular_dash_arm(raw, center, name, text_h, objects, tables) for name in _DIRECTIONS]
    observed = [arm for arm in arms if arm]
    references = [arm for arm in observed if arm["periodic_context"]]
    if len(observed) < 2 or not references:
        return None
    # Two-stroke arms are allowed only beside a independently repeating arm
    # whose spacing matches. They are not themselves proof of periodicity.
    observed = [arm for arm in observed if arm["periodic_context"] or any(
                abs(arm["median_period"] - reference["median_period"]) <=
                max(3, .35 * reference["median_period"])
                and abs(arm["median_gap"] - reference["median_gap"]) <= max(2, .35 * reference["median_gap"])
                for reference in references)]
    if len(observed) < 2:
        return None
    directions = {_DIRECTIONS[arm["direction"]] for arm in observed}
    opposite_only = len(observed) == 2 and any((-dx, -dy) in directions for dx, dy in directions)
    if opposite_only:
        return None
    dot = _dot(raw, center, text_h)
    if len(observed) == 4 and not dot["present"]:
        return _hypothesis("crossing_ambiguous", center, dashed_arms=observed, dot=dot,
                           transition={"mode": "opposite_arms_only_no_join_until_distinct_dot_or_T_evidence"},
                           evidence="four_repeating_dashed_arms_without_a_distinct_join_dot")
    return _hypothesis("junction_join", center, dashed_arms=observed, dot=dot,
                       center_ink_observed=_ink(raw, center),
                       junction_type="dashed_T" if len(observed) == 3 else "dashed_elbow" if len(observed) == 2 else "dot",
                       observed_paths=[arm["observed_path"] for arm in observed],
                       transition={"mode": "repeating_aligned_requested_arms_after_model_confirmation",
                                   "observed_arms": [arm["direction"] for arm in observed]},
                       evidence="repeating_original_dashes_with_matching_spacing_on_each_proposed_junction_arm")


def semantic_transition_allowed(hypothesis, path, meaning=None):
    """Check a selected meaning's finite transition, without accepting it."""
    kind = hypothesis.get("kind")
    if kind not in HYPOTHESIS_KINDS or len(path) < 2:
        return False
    if meaning == "junction" and kind != "junction_join":
        return False
    if kind in {"crossing_underpass_no_join", "dashed_continuation", "solid_continuation", "crossing_ambiguous"}:
        if meaning == "junction" and kind in {"crossing_underpass_no_join", "crossing_ambiguous"}:
            return False
        axis = hypothesis.get("axis") or _axis(path[0], path[-1])[0]
        if axis not in {"horizontal", "vertical"}:
            return False
        if any(_axis(a, b)[0] != axis for a, b in zip(path, path[1:])):
            return False
        if any(turn["turning"] for turn in classify_turns(path)):
            return False
        return True
    if kind == "junction_join":
        observed = hypothesis.get("transition", {}).get("observed_arms", [])
        if observed:
            names = {tuple(value): key for key, value in _DIRECTIONS.items()}
            for turn in classify_turns(path):
                if turn["turning"]:
                    # A flange/glyph T somewhere else along this route cannot
                    # justify the requested elbow. Raster tolerance is bounded
                    # around that exact code-created transition only.
                    if (max(abs(turn["point"][i] - hypothesis.get("observed_center", hypothesis["center"])[i])
                            for i in (0, 1)) >
                            hypothesis.get("raster_tolerance", 0)
                            or not all(names.get(tuple(turn[arm] or ())) in observed
                                       for arm in ("incoming_arm", "outgoing_arm"))):
                        return False
        return True  # Semantic confirmation still belongs to the Decision Model.
    return False


def _local_protected_regions(hypothesis, objects, tables):
    """A glyph/body arm beside the requested path cannot establish a junction."""
    center = hypothesis.get("observed_center", hypothesis["center"])
    arms = [arm for arm in hypothesis.get("arms", []) if arm.get("present")]
    arms += hypothesis.get("perpendicular_arms", [])
    arms += hypothesis.get("dashed_arms", [])
    blockers = []
    for path in hypothesis.get("observed_paths", []):
        blockers += blocked_by_regions(path, objects, tables)
    for arm in arms:
        name = arm["direction"]
        dx, dy = _DIRECTIONS[name]
        if arm.get("observed_path"):
            # Context stopped at the body; do not extrapolate an extra arm
            # through a body merely because the last supported dash is nearby.
            blockers += blocked_by_regions([center, arm["observed_path"][-1]], objects, tables)
        else:
            distance = arm.get("samples", max(arm.get("observed_positions", [5])) + 2)
            arm_end = [center[0] + dx * distance, center[1] + dy * distance]
            blockers += blocked_by_regions([center, arm_end], objects, tables)
    return blockers


def analyze_entity(page, entity, objects=(), text_h=9, tables=()):
    """Create inspectable semantic alternatives for an existing physical path.

    ``eligible`` authorizes a model inspection only. It is never evidence that
    the two objects connect. Protected region interiors keep false glyph/body
    bridges out of candidate generation instead of painting them away.
    """
    if type(text_h) not in (int, float) or not math.isfinite(text_h) or text_h <= 0:
        raise ValueError("text_h must be finite and positive")
    gray = _gray(page)
    result = {"revision": REVISION, "entity_id": entity.get("id"), "eligible": False,
              "hypotheses": [], "reasons": [],
              "safety": {"geometry_is_not_acceptance": True, "original_ink_unchanged": True,
                         "no_symbol_or_table_interior_bridge": True, "no_crossing_axis_union": True}}
    if entity.get("kind") == "attachment":
        result["reasons"] = ["attachment_requires_separate_body_contact_judgment"]
        return result
    raw_path = entity.get("path") or entity.get("geometry", {}).get("path") or entity.get("detail", {}).get("path")
    try:
        path = finite_path(raw_path, gray.shape)
    except ValueError:
        result["reasons"] = ["invalid_or_missing_finite_path"]
        return result
    result.update(path=path, anchors=[path[0], path[-1]], requested_turns=classify_turns(path))
    blockers = blocked_by_regions(path, objects, tables)
    if blockers:
        result.update(blockers=blockers, reasons=["path_crosses_protected_region_interior"])
        return result
    raw = gray < RAW_THRESHOLD
    samples = _path_samples(path)
    hypotheses = []
    context_radius = max(22, max(18, min(72, round(4.5 * text_h)))) + _raster_tolerance(text_h)
    nearby_objects = _nearby_regions(path, objects, context_radius)
    nearby_tables = _nearby_regions(path, tables, context_radius)
    dash = _dash_hypothesis(raw, path, text_h, nearby_objects, nearby_tables)
    if dash:
        # This global check also protects any separate periodic reference arm.
        if not _local_protected_regions(dash, objects, tables):
            hypotheses.append(dash)
    # Check centers on the requested raw route. No new off-route bridge or
    # nearest-line snapping is proposed by this inspection.
    axes = {_axis(a, b)[0] for a, b in zip(path, path[1:])} - {None}
    centers = [turn["point"] for turn in classify_turns(path) if turn["turning"]] + samples
    local = []
    for center in centers:
        underpasses = [_tolerant_local(lambda ink, point, height: _underpass(ink, point, axis, height),
                       raw, center, text_h, objects=nearby_objects, tables=nearby_tables) for axis in sorted(axes)]
        found = [hyp for hyp in underpasses if hyp]
        junction = _tolerant_local(_local_junction, raw, center, text_h,
                                 objects=nearby_objects, tables=nearby_tables)
        if junction:
            found.append(junction)
        for hypothesis in found:
            if any(old["kind"] == hypothesis["kind"] and old.get("axis") == hypothesis.get("axis")
                   and math.dist(old.get("observed_center", old["center"]),
                                 hypothesis.get("observed_center", hypothesis["center"])) <= 2 for old in local):
                continue
            hypothesis["requested_transition_compatible"] = semantic_transition_allowed(hypothesis, path)
            local.append(hypothesis)
    # A regular dashed elbow/T may have a white center. Its repeated aligned
    # raw arms form a finite hypothesis; only the model can establish a join.
    dash_centers = [turn["point"] for turn in classify_turns(path) if turn["turning"]] + [path[0], path[-1]]
    for center in dash_centers:
        callback = lambda ink, point, height: _dashed_junction(ink, point, height, nearby_objects, nearby_tables)
        hypothesis = _tolerant_local(callback, raw, center, text_h, ink_only=False,
                                    objects=nearby_objects, tables=nearby_tables)
        if hypothesis and not any(old["kind"] == hypothesis["kind"] and math.dist(old["center"], center) <= 2
                                  for old in local):
            hypothesis["requested_transition_compatible"] = semantic_transition_allowed(hypothesis, path)
            local.append(hypothesis)
    # Ordering is stable and bounded for one finite semantic query. All raw
    # points remain in path; limiting proposed local explanations is not a link
    # acceptance or a deletion from the upstream candidate ledger.
    permitted_local, suppressed = [], []
    for hypothesis in local:
        blockers = _local_protected_regions(hypothesis, objects, tables)
        if blockers:
            suppressed.append({"kind": hypothesis["kind"], "center": hypothesis["center"],
                               "reason": "a_claimed_arm_enters_a_protected_region", "blockers": blockers})
        else:
            permitted_local.append(hypothesis)
    permitted_local.sort(key=lambda hyp: (not hyp["requested_transition_compatible"],
                                          min((math.dist(turn["point"], hyp["center"])
                                               for turn in classify_turns(path) if turn["turning"]), default=0)))
    hypotheses += permitted_local[:12]
    values = [_ink(raw, point) for point in samples]
    axis, _ = _axis(path[0], path[-1])
    if not hypotheses and axis and sum(values) / len(values) >= .90:
        hypotheses.append(_hypothesis("solid_continuation", samples[len(samples) // 2], axis=axis,
                                       raw_path_support=round(sum(values) / len(values), 4),
                                       transition={"mode": "opposite_arms_only", "axis": axis, "joins_crossing_axis": False},
                                       evidence="original_supported_straight_stroke"))
    if not hypotheses:
        hypotheses.append(_hypothesis("unresolved_break", samples[len(samples) // 2],
                                       raw_path_support=round(sum(values) / len(values), 4),
                                       transition={"mode": "no_geometry_supported_continuation"},
                                       evidence="original_route_is_weak_or_has_an_unexplained_gap"))
    xs, ys = zip(*path)
    pad = max(18, round(3 * text_h))
    h, w = gray.shape
    bbox = [max(0, math.floor(min(xs)) - pad), max(0, math.floor(min(ys)) - pad),
            min(w - 1, math.ceil(max(xs)) + pad), min(h - 1, math.ceil(max(ys)) + pad)]
    x0, y0, x1, y1 = bbox
    result.update(eligible=True, hypotheses=hypotheses, bbox=bbox,
                  suppressed_local_hypotheses=suppressed,
                  raw_sha256=hashlib.sha256(np.ascontiguousarray(gray[y0:y1 + 1, x0:x1 + 1]).tobytes()).hexdigest(),
                  proposed_meanings=list(dict.fromkeys(hyp["kind"] for hyp in hypotheses)),
                  raw_threshold=RAW_THRESHOLD,
                  reasons=["finite_raw_geometry_requires_semantic_model_judgment"])
    return result
