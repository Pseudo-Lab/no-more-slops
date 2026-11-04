"""Raw geometry proposal tests; they never simulate or invoke model acceptance."""
from __future__ import annotations

import json

import cv2
import numpy as np
import pytest

from cad_api import connection_semantic_geometry as geometry


def entity(path, kind="segment"):
    return {"id": "fixture-entity", "kind": kind, "path": path, "state": "review_needed"}


def page():
    return np.full((120, 120), 255, np.uint8)


def meanings(result):
    return {h["kind"] for h in result["hypotheses"]}


def draw_dashed_arm(image, center, direction, count=6, width=3, gap=3, first=3):
    for index in range(count):
        distance = first + index * (width + gap)
        start = tuple(center[j] + direction[j] * distance for j in (0, 1))
        end = tuple(center[j] + direction[j] * (distance + width - 1) for j in (0, 1))
        cv2.line(image, start, end, 165, 1)


def test_aligned_regular_dashes_are_finite_continuation_hypotheses():
    image = page()
    draw_dashed_arm(image, [15, 60], [1, 0], count=12)
    path = [[18, 60], [86, 60]]
    before = image.copy()
    result = geometry.analyze_entity(image, entity(path), text_h=9)
    assert result["eligible"] and "dashed_continuation" in meanings(result)
    dash = next(h for h in result["hypotheses"] if h["kind"] == "dashed_continuation")
    assert dash["observed_stroke_runs"] >= 3 and len(dash["observed_regular_gaps"]) >= 2
    assert geometry.semantic_transition_allowed(dash, path)
    assert not geometry.semantic_transition_allowed(dash, [[18, 60], [50, 60], [50, 85]])
    assert result["safety"]["geometry_is_not_acceptance"]
    assert "accepted" not in result and all(h["status"] == "hypothesis" and h["model_required"] for h in result["hypotheses"])
    assert np.array_equal(image, before)
    json.dumps(result)


def test_underpass_preserves_opposite_arms_without_joining_crossing_axis():
    image = page()
    cv2.line(image, (15, 60), (55, 60), 0, 1)
    cv2.line(image, (65, 60), (105, 60), 0, 1)
    cv2.line(image, (60, 15), (60, 105), 0, 1)
    result = geometry.analyze_entity(image, entity([[25, 60], [95, 60]]))
    underpass = next(h for h in result["hypotheses"] if h["kind"] == "crossing_underpass_no_join")
    assert underpass["axis"] == "horizontal" and underpass["crossing_axis"] == "vertical"
    assert underpass["transition"]["joins_crossing_axis"] is False
    assert geometry.semantic_transition_allowed(underpass, [[25, 60], [95, 60]])
    assert not geometry.semantic_transition_allowed(underpass, [[25, 60], [60, 60], [60, 95]])
    assert not geometry.semantic_transition_allowed(underpass, [[25, 60], [95, 60]], meaning="junction")
    assert "junction_join" not in meanings(result)


def test_requested_turn_at_an_underpass_cannot_be_a_branch_shortcut():
    image = page()
    cv2.line(image, (15, 60), (55, 60), 0, 1)
    cv2.line(image, (65, 60), (105, 60), 0, 1)
    cv2.line(image, (60, 15), (60, 105), 0, 1)
    path = [[25, 60], [60, 60], [60, 95]]
    result = geometry.analyze_entity(image, entity(path, "junction"))
    proposals = [h for h in result["hypotheses"] if h["kind"] == "crossing_underpass_no_join"]
    assert proposals and all(not geometry.semantic_transition_allowed(h, path) for h in proposals)


@pytest.mark.parametrize("dot", [False, True])
def test_true_original_T_or_dot_is_only_a_model_required_join_hypothesis(dot):
    image = page()
    cv2.line(image, (15, 60), (105, 60), 0, 1)
    cv2.line(image, (60, 60), (60, 105), 0, 1)
    if dot:
        cv2.circle(image, (60, 60), 3, 0, -1)
    path = [[25, 60], [60, 60], [60, 95]]
    result = geometry.analyze_entity(image, entity(path, "junction"))
    branch = next(h for h in result["hypotheses"] if h["kind"] == "junction_join")
    assert branch["junction_type"] == ("dot" if dot else "T")
    assert branch["model_required"] and geometry.semantic_transition_allowed(branch, path)
    assert "accepted" not in branch


def test_four_arm_X_without_dot_is_ambiguous_and_never_allows_a_turn_join():
    image = page()
    cv2.line(image, (15, 60), (105, 60), 0, 1)
    cv2.line(image, (60, 15), (60, 105), 0, 1)
    result = geometry.analyze_entity(image, entity([[25, 60], [95, 60]]))
    assert "crossing_ambiguous" in meanings(result) and "junction_join" not in meanings(result)
    ambiguous = next(h for h in result["hypotheses"] if h["kind"] == "crossing_ambiguous")
    assert geometry.semantic_transition_allowed(ambiguous, [[25, 60], [95, 60]])
    assert not geometry.semantic_transition_allowed(ambiguous, [[25, 60], [60, 60], [60, 95]])
    assert not geometry.semantic_transition_allowed(ambiguous, [[25, 60], [95, 60]], meaning="junction")


def test_distinct_dot_can_propose_a_four_way_junction():
    image = page()
    cv2.line(image, (15, 60), (105, 60), 0, 1)
    cv2.line(image, (60, 15), (60, 105), 0, 1)
    cv2.circle(image, (60, 60), 3, 0, -1)
    result = geometry.analyze_entity(image, entity([[25, 60], [60, 60], [60, 95]], "junction"))
    branch = next(h for h in result["hypotheses"] if h["kind"] == "junction_join")
    assert branch["dot"]["present"] and branch["junction_type"] == "dot"


@pytest.mark.parametrize("third_arm", [False, True])
def test_regular_dashed_elbow_or_T_can_be_inspected_with_a_white_center(third_arm):
    image = page()
    center = [60, 60]
    draw_dashed_arm(image, center, [-1, 0])
    draw_dashed_arm(image, center, [0, 1])
    if third_arm:
        draw_dashed_arm(image, center, [1, 0])
    assert image[60, 60] == 255
    path = [[25, 60], center, [60, 95]]
    result = geometry.analyze_entity(image, entity(path, "junction"))
    branch = next(h for h in result["hypotheses"] if h["kind"] == "junction_join")
    assert branch["junction_type"] == ("dashed_T" if third_arm else "dashed_elbow")
    assert branch["center_ink_observed"] is False and branch["model_required"]
    assert geometry.semantic_transition_allowed(branch, path)


def test_four_repeating_dash_arms_without_dot_cannot_establish_a_join():
    image = page()
    center = [60, 60]
    for direction in ([-1, 0], [1, 0], [0, -1], [0, 1]):
        draw_dashed_arm(image, center, direction)
    path = [[25, 60], center, [60, 95]]
    result = geometry.analyze_entity(image, entity(path, "junction"))
    assert "crossing_ambiguous" in meanings(result) and "junction_join" not in meanings(result)
    assert all(not geometry.semantic_transition_allowed(h, path, meaning="junction") for h in result["hypotheses"])


@pytest.mark.parametrize("protected", ["symbol", "glyph", "table"])
def test_symbol_glyph_and_table_interiors_never_create_bridge_hypotheses(protected):
    image = page()
    cv2.line(image, (15, 60), (105, 60), 0, 1)
    cv2.line(image, (60, 20), (60, 100), 0, 1)
    objects, tables = [], []
    box = [50, 50, 70, 70]
    if protected == "table":
        tables = [box]
    else:
        objects = [{"id": "protected", "class": "text" if protected == "glyph" else "instrument", "bbox": box}]
    result = geometry.analyze_entity(image, entity([[25, 60], [95, 60]]), objects, tables=tables)
    assert not result["eligible"] and not result["hypotheses"]
    assert result["reasons"] == ["path_crosses_protected_region_interior"]


def test_glyph_arm_next_to_a_path_does_not_supply_branch_evidence():
    image = page()
    cv2.line(image, (15, 60), (105, 60), 0, 1)
    cv2.line(image, (60, 30), (60, 60), 0, 1)
    objects = [{"id": "glyph", "class": "text", "bbox": [55, 25, 65, 55]}]
    result = geometry.analyze_entity(image, entity([[25, 60], [95, 60]]), objects)
    assert result["eligible"] and "junction_join" not in meanings(result)
    assert result["suppressed_local_hypotheses"]


def test_an_isolated_gap_is_not_invented_as_a_regular_dashed_line():
    image = page()
    cv2.line(image, (15, 60), (45, 60), 0, 1)
    cv2.line(image, (65, 60), (105, 60), 0, 1)
    result = geometry.analyze_entity(image, entity([[25, 60], [95, 60]]))
    assert meanings(result) == {"unresolved_break"}


@pytest.mark.parametrize("path", [[[10, 10], [float("nan"), 20]], [[10, 10], [float("inf"), 20]],
                                 [[True, 10], [20, 20]], [[10, 10], [-1, 20]], [[10, 10], [120, 20]]])
def test_invalid_or_out_of_image_coordinates_do_not_become_proposals(path):
    result = geometry.analyze_entity(page(), entity(path))
    assert not result["eligible"] and result["reasons"] == ["invalid_or_missing_finite_path"]


def test_finite_path_does_not_snap_neighbouring_lines_or_modify_input():
    original = [[10, 50], [10, 50], [90, 51]]
    result = geometry.finite_path(original, (120, 120))
    assert result == [[10, 50], [90, 51]] and original == [[10, 50], [10, 50], [90, 51]]


@pytest.mark.parametrize("offset", [-3, 0, 3])
def test_short_dash_path_uses_coherent_original_context_without_moving_anchors(offset):
    image = page()
    draw_dashed_arm(image, [15, 60 + offset], [1, 0], count=12)
    path = [[48, 60], [55, 60]]
    before = image.copy()
    result = geometry.analyze_entity(image, entity(path))
    dash = next(h for h in result["hypotheses"] if h["kind"] == "dashed_continuation")
    assert dash["observed_stroke_runs"] >= 3
    assert dash["raster_normal_offset"] == offset
    assert dash["observed_paths"][0][0][0] < path[0][0]
    assert dash["observed_paths"][0][1][0] > path[-1][0]
    assert result["path"] == path and result["anchors"] == [path[0], path[-1]]
    assert np.array_equal(image, before)


def test_periodic_context_outside_raster_tolerance_cannot_supply_a_route():
    image = page()
    draw_dashed_arm(image, [15, 64], [1, 0], count=12)
    result = geometry.analyze_entity(image, entity([[48, 60], [55, 60]]))
    assert meanings(result) == {"unresolved_break"}


def test_two_distinct_parallel_context_lines_do_not_select_an_optimistic_offset():
    image = page()
    for y in (59, 61):
        draw_dashed_arm(image, [15, y], [1, 0], count=12)
    result = geometry.analyze_entity(image, entity([[48, 60], [55, 60]]))
    assert "dashed_continuation" not in meanings(result)


@pytest.mark.parametrize("offset", [(-3, 0), (0, 3), (2, -2), (-3, 3)])
def test_T_junction_uses_one_bounded_original_raster_center(offset):
    image = page()
    cx, cy = 60 + offset[0], 60 + offset[1]
    cv2.line(image, (20, cy), (100, cy), 0, 1)
    cv2.line(image, (cx, cy), (cx, 100), 0, 1)
    path = [[35, 60], [60, 60], [60, 85]]
    result = geometry.analyze_entity(image, entity(path, "junction"))
    hypotheses = [h for h in result["hypotheses"] if h["kind"] == "junction_join"
                  and geometry.semantic_transition_allowed(h, path, "junction")]
    assert hypotheses
    hypothesis = hypotheses[0]
    assert hypothesis["observed_center"] == [cx, cy]
    assert result["path"] == path
    assert max(abs(v) for v in hypothesis["raster_offset"]) <= 3
    assert hypothesis["model_required"] and "accepted" not in hypothesis


def test_shifted_underpass_can_never_justify_turn_or_join():
    image = page()
    cv2.line(image, (15, 62), (55, 62), 0, 1)
    cv2.line(image, (65, 62), (105, 62), 0, 1)
    cv2.line(image, (60, 15), (60, 105), 0, 1)
    path = [[25, 60], [60, 60], [60, 95]]
    result = geometry.analyze_entity(image, entity(path, "junction"))
    underpasses = [h for h in result["hypotheses"] if h["kind"] == "crossing_underpass_no_join"]
    assert underpasses
    assert all(not geometry.semantic_transition_allowed(h, path, "junction") for h in underpasses)
    assert not any(geometry.semantic_transition_allowed(h, path, "junction") for h in result["hypotheses"])


def test_short_two_dash_elbow_arm_needs_matching_periodic_raw_context_outside_body():
    image = page()
    # Only two horizontal strokes fit between the body boundary and the elbow.
    # The short last stroke is clipped by the elbow, rather than a new period.
    cv2.line(image, (46, 60), (54, 60), 165, 1)
    cv2.line(image, (59, 60), (61, 60), 165, 1)
    cv2.line(image, (61, 60), (61, 65), 165, 1)
    draw_dashed_arm(image, [61, 60], [0, 1], count=4, width=9, gap=4, first=10)
    objects = [{"id": "body", "class": "instrument", "bbox": [20, 50, 46, 70]}]
    path = [[48, 60], [61, 60], [61, 82]]
    result = geometry.analyze_entity(image, entity(path, "junction"), objects)
    branch = next(h for h in result["hypotheses"] if h["kind"] == "junction_join"
                  and geometry.semantic_transition_allowed(h, path, "junction"))
    arms = {arm["direction"]: arm for arm in branch["dashed_arms"]}
    assert arms["left"]["observed_stroke_runs"] == 2
    assert not arms["left"]["periodic_context"] and arms["bottom"]["periodic_context"]
    assert all(point[0] >= 46 for point in arms["left"]["observed_path"])
    # The same evidence may support a finite straight local-span question.
    straight = geometry.analyze_entity(image, entity(path[:2]), objects)
    dash = next(h for h in straight["hypotheses"] if h["kind"] == "dashed_continuation")
    assert dash["observed_stroke_runs"] == 2 and dash["periodic_reference_arm"]["periodic_context"]


def test_two_short_strokes_without_periodic_reference_remain_unresolved():
    image = page()
    cv2.line(image, (46, 60), (54, 60), 165, 1)
    cv2.line(image, (59, 60), (67, 60), 165, 1)
    result = geometry.analyze_entity(image, entity([[48, 60], [65, 60]]))
    assert meanings(result) == {"unresolved_break"}


def test_dense_glyph_fragments_do_not_turn_a_short_dashed_elbow_into_a_T():
    image = page()
    center = [61, 60]
    cv2.line(image, (46, 60), (54, 60), 165, 1)
    cv2.line(image, (59, 60), (61, 60), 165, 1)
    cv2.line(image, (61, 60), (61, 65), 165, 1)
    draw_dashed_arm(image, center, [0, 1], count=4, width=9, gap=4, first=10)
    # Small strokes of an adjacent annotation have a period below the observed
    # drawing's dash scale; they cannot supply a third signal-line arm.
    draw_dashed_arm(image, center, [0, -1], count=3, width=2, gap=2, first=10)
    path = [[48, 60], center, [61, 82]]
    result = geometry.analyze_entity(image, entity(path, "junction"))
    branch = next(h for h in result["hypotheses"] if h["kind"] == "junction_join"
                  and geometry.semantic_transition_allowed(h, path, "junction"))
    assert branch["junction_type"] == "dashed_elbow"
    assert {arm["direction"] for arm in branch["dashed_arms"]} == {"left", "bottom"}


def test_four_dash_arms_with_short_partial_strokes_remain_no_turn_ambiguous():
    image = page()
    center = [60, 60]
    for direction in ([0, -1], [0, 1]):
        draw_dashed_arm(image, center, direction, count=5, width=3, gap=3)
    for direction in ([-1, 0], [1, 0]):
        draw_dashed_arm(image, center, direction, count=2, width=3, gap=3)
    path = [[48, 60], center, [60, 85]]
    result = geometry.analyze_entity(image, entity(path, "junction"))
    assert "crossing_ambiguous" in meanings(result)
    assert not any(geometry.semantic_transition_allowed(h, path, "junction") for h in result["hypotheses"])


def test_context_dashes_inside_a_glyph_cannot_supply_missing_repetition():
    image = page()
    cv2.line(image, (46, 60), (54, 60), 165, 1)
    cv2.line(image, (59, 60), (67, 60), 165, 1)
    draw_dashed_arm(image, [70, 60], [1, 0], count=4)
    objects = [{"id": "glyph", "class": "text", "bbox": [70, 55, 115, 65]}]
    result = geometry.analyze_entity(image, entity([[48, 60], [65, 60]]), objects)
    assert "dashed_continuation" not in meanings(result)


def test_an_observed_flange_T_cannot_justify_an_unobserved_distant_elbow():
    image = page()
    cv2.line(image, (60, 20), (60, 77), 0, 1)
    cv2.line(image, (35, 77), (85, 77), 0, 1)
    path = [[60, 80], [60, 60], [82, 60]]
    result = geometry.analyze_entity(image, entity(path, "junction"))
    assert any(h["kind"] == "junction_join" for h in result["hypotheses"])
    assert all(not geometry.semantic_transition_allowed(h, path, "junction") for h in result["hypotheses"])
