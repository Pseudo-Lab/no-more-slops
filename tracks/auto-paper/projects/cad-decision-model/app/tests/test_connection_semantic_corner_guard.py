"""Raw review proposals; all geometry stays original and no model is used."""
import copy
import json

import cv2
import numpy as np
import pytest

from cad_api.connection_semantics import raw_corner_transition_proposals


def page():
    return np.full((160, 160), 255, np.uint8)


def dash(image, center, direction, count=5, first=4, width=6, gap=4):
    for n in range(count):
        offset = first + n * (width + gap)
        a = tuple(center[i] + direction[i] * offset for i in (0, 1))
        b = tuple(center[i] + direction[i] * (offset + width - 1) for i in (0, 1))
        cv2.line(image, a, b, 165, 1)


def cross(image, center=(80, 80), dot=False):
    x, y = center
    cv2.line(image, (20, y), (140, y), 0, 1)
    cv2.line(image, (x, 20), (x, 140), 0, 1)
    if dot:
        cv2.circle(image, center, 3, 0, -1)


def test_raw_four_arm_solid_turn_without_dot_stays_review_needed():
    image = page()
    cross(image)
    path = [[30, 80], [80, 80], [80, 125]]
    result = raw_corner_transition_proposals(image, path)
    assert len(result) == 1 and result[0]['raw_hypothesis']['kind'] == 'crossing_ambiguous'
    assert result[0]['state'] == 'review_needed' and 'accepted' not in result[0]
    assert result[0]['original_triplet'] == path


@pytest.mark.parametrize('offset', [(0, 0), (-2, 0), (0, 2)])
def test_distinct_original_dot_is_not_reinterpreted_from_its_offcentre_slice(offset):
    image = page()
    cross(image, dot=True)
    x, y = 80 + offset[0], 80 + offset[1]
    assert not raw_corner_transition_proposals(image, [[30, y], [x, y], [x, 125]])


def test_three_arm_visible_T_has_no_no_join_crossing_guard():
    image = page()
    cv2.line(image, (20, 80), (140, 80), 0, 1)
    cv2.line(image, (80, 80), (80, 140), 0, 1)
    assert not raw_corner_transition_proposals(image, [[30, 80], [80, 80], [80, 125]])


@pytest.mark.parametrize('solid_axis', ['vertical', 'horizontal'])
def test_four_mixed_solid_and_regular_dash_arms_keep_axis_change_pending(solid_axis):
    image = page()
    center = [80, 80]
    if solid_axis == 'vertical':
        cv2.line(image, (80, 20), (80, 140), 0, 1)
        directions = [[-1, 0], [1, 0]]
    else:
        cv2.line(image, (20, 80), (140, 80), 0, 1)
        directions = [[0, -1], [0, 1]]
    for direction in directions:
        dash(image, center, direction)
    result = raw_corner_transition_proposals(image, [[30, 80], center, [80, 125]])
    assert result and len(result[0]['raw_hypothesis']['arms']) == 4
    assert any(a['ink_type'] == 'periodic_original_dash_arm' for a in result[0]['raw_hypothesis']['arms'])


def test_one_dashed_fourth_arm_outside_short_solid_context_is_observed():
    image = page()
    cv2.line(image, (20, 80), (80, 80), 0, 1)
    cv2.line(image, (80, 20), (80, 140), 0, 1)
    dash(image, [80, 80], [1, 0], first=6, width=6, gap=4)
    result = raw_corner_transition_proposals(image, [[30, 80], [79, 80], [80, 125]])
    assert result and result[0]['observed_center'] == [80, 80]
    assert result[0]['original_corner'] == [79, 80] and result[0]['raster_offset'] == [1, 0]


@pytest.mark.parametrize('third_arm', [False, True])
def test_regular_dash_elbow_and_T_with_white_center_are_not_four_arm_crossings(third_arm):
    image = page()
    for direction in [[-1, 0], [0, 1]] + ([[1, 0]] if third_arm else []):
        dash(image, [80, 80], direction)
    assert image[80, 80] == 255
    assert not raw_corner_transition_proposals(image, [[30, 80], [80, 80], [80, 125]])


def test_only_two_irregular_fragments_cannot_supply_a_fourth_arm():
    image = page()
    cv2.line(image, (20, 80), (80, 80), 0, 1)
    cv2.line(image, (80, 20), (80, 140), 0, 1)
    cv2.line(image, (86, 80), (91, 80), 165, 1)
    cv2.line(image, (112, 80), (115, 80), 165, 1)
    assert not raw_corner_transition_proposals(image, [[30, 80], [80, 80], [80, 125]])


def test_underpass_turn_is_pending_but_same_axis_straight_path_is_untouched():
    image = page()
    cv2.line(image, (20, 80), (74, 80), 0, 1)
    cv2.line(image, (86, 80), (140, 80), 0, 1)
    cv2.line(image, (80, 20), (80, 140), 0, 1)
    result = raw_corner_transition_proposals(image, [[30, 80], [80, 80], [80, 125]])
    assert result and result[0]['raw_hypothesis']['kind'] == 'crossing_underpass_no_join'
    assert not raw_corner_transition_proposals(image, [[30, 80], [80, 80], [125, 80]])


@pytest.mark.parametrize('protected', ['text', 'instrument', 'table'])
def test_body_glyph_or_table_cannot_supply_the_dashed_fourth_arm(protected):
    image = page()
    cv2.line(image, (20, 80), (80, 80), 0, 1)
    cv2.line(image, (80, 20), (80, 140), 0, 1)
    dash(image, [80, 80], [1, 0])
    objects, tables = [], []
    box = [84, 75, 140, 85]
    if protected == 'table':
        tables = [box]
    else:
        objects = [{'id': 'protected', 'class': protected, 'bbox': box}]
    assert not raw_corner_transition_proposals(image, [[30, 80], [80, 80], [80, 125]], objects, tables=tables)


def test_original_image_path_and_objects_remain_exact_and_proposal_serializes():
    image = page()
    cross(image)
    path = [[30, 80], [80, 80], [80, 125]]
    objects = [{'id': 'remote', 'class': 'text', 'bbox': [10, 10, 15, 15]}]
    old_image, old_path, old_objects = image.copy(), copy.deepcopy(path), copy.deepcopy(objects)
    result = raw_corner_transition_proposals(image, path, objects)
    assert result and np.array_equal(image, old_image) and path == old_path and objects == old_objects
    assert result[0]['safety']['caller_must_preserve_prior_v14_acceptance']
    json.dumps(result)


@pytest.mark.parametrize('path', [[[10, 10], [float('nan'), 20]], [[10, 10], [160, 20]], []])
def test_nonfinite_or_outside_geometry_cannot_become_raw_evidence(path):
    with pytest.raises(ValueError):
        raw_corner_transition_proposals(page(), path)
