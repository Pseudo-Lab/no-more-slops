"""Finite window/ink tests; no Decision Model or model-answer fixtures."""
from __future__ import annotations

import copy
import math

import cv2
import numpy as np
import pytest

from cad_api.connection_semantics import context_windows, semantic_route_window_view


COLORS = ((0, 0, 230), (230, 80, 0))


def length(path):
    return sum(math.dist(a, b) for a, b in zip(path, path[1:]))


@pytest.mark.parametrize('distance', [3, 72, 108, 109, 162, 163, 815.25])
def test_complete_overlap_plan_covers_every_route_position(distance):
    path = [[10, 20], [10 + distance, 20]]
    before = copy.deepcopy(path)
    windows = context_windows(path, 9, (50, 1000))
    assert windows[0]['start_distance'] == 0
    assert windows[-1]['end_distance'] == pytest.approx(distance)
    assert windows[0]['path'][0] == path[0] and windows[-1]['path'][-1] == path[-1]
    assert len(windows) == max(1, math.ceil(max(0, distance - 108) / 54) + 1)
    for previous, following in zip(windows, windows[1:]):
        assert following['start_distance'] == previous['start_distance'] + 54
        assert previous['end_distance'] - following['start_distance'] == pytest.approx(54)
    for window in windows:
        assert length(window['path']) == pytest.approx(window['end_distance'] - window['start_distance'])
        assert 0 < window['end_distance'] - window['start_distance'] <= 108
    assert path == before


@pytest.mark.parametrize('text_h,expected_span', [(3, 72), (9, 108), (18, 216), (100, 1200)])
def test_inspection_length_follows_drawing_scale_without_a_108px_cap(text_h, expected_span):
    windows = context_windows([[10, 20], [2510, 20]], text_h, (100, 3000))
    assert windows[0]['end_distance'] == expected_span
    assert windows[1]['start_distance'] == expected_span / 2
    assert windows[-1]['end_distance'] == 2500


def test_turns_and_backtracking_are_kept_in_original_arclength_order():
    path = [[100, 100], [20, 100], [20, 160], [90, 160], [90, 115]]
    before = copy.deepcopy(path)
    windows = context_windows(path, 9, (200, 200))
    cumulative = [0.0]
    for a, b in zip(path, path[1:]):
        cumulative.append(cumulative[-1] + math.dist(a, b))
    for point, distance in zip(path[1:-1], cumulative[1:-1]):
        containing = [window for window in windows
                      if window['start_distance'] <= distance <= window['end_distance']]
        assert containing and all(point in window['path'] for window in containing)
    assert all(length(window['path']) == pytest.approx(window['end_distance'] - window['start_distance'])
               for window in windows)
    assert windows[-1]['end_distance'] == length(path) and path == before


def test_fractional_window_boundaries_stay_on_existing_diagonal_segments():
    path = [[10, 10], [210, 110]]
    windows = context_windows(path, 9, (250, 250))
    assert any(type(value) is float and not value.is_integer()
               for window in windows for point in window['path'] for value in point)
    for window in windows:
        for x, y in window['path']:
            assert x - 10 == pytest.approx(2 * (y - 10))


def test_review_budget_cannot_silently_truncate_the_window_plan():
    # The review gate owns its budget; the geometry planner must retain the
    # uncovered tail so the caller cannot mistake a partial review for clear.
    windows = context_windows([[10, 20], [18010, 20]], 9, (50, 19000))
    budget = 192
    assert len(windows) > budget
    reviewed, deferred = windows[:budget], windows[budget:]
    assert reviewed[-1]['end_distance'] < 18000
    assert deferred and deferred[-1]['end_distance'] == 18000
    assert all(window['start_distance'] < window['end_distance'] for window in deferred)


@pytest.mark.parametrize('path', [[[10, 10], [10, 10]], [[10, 10], [math.nan, 20]],
                                 [[10, 10], [math.inf, 20]], [[True, 10], [20, 20]],
                                 [[10, 10], [200, 20]]])
def test_invalid_geometry_is_explicit_instead_of_returning_an_empty_clear_plan(path):
    with pytest.raises(ValueError):
        context_windows(path, 9, (100, 100))


def test_raw_panel_retains_every_displayed_original_ink_value_and_inputs():
    page = np.full((180, 250), 255, np.uint8)
    for index, value in enumerate((0, 165, 210, 254)):
        cv2.line(page, (40 + index * 25, 90), (48 + index * 25, 90), value, 1)
    cv2.putText(page, 'AB', (55, 75), cv2.FONT_HERSHEY_SIMPLEX, .45, 190, 1)
    path = [[40, 90], [135, 90]]
    window = context_windows(path, 9, page.shape)[0]
    boxes = [{'id': 'real-first', 'bbox': [20, 60, 40, 89]},
             {'id': 'real-last', 'bbox': [140, 90, 160, 120]}]
    before_page, before_window, before_boxes = page.copy(), copy.deepcopy(window), copy.deepcopy(boxes)
    image = semantic_route_window_view(object(), page, window, boxes, COLORS)
    panel_width = (image.shape[1] - 12) // 2
    raw = image[32:, panel_width + 12:]
    # Independent expected original crop: 6 * text_h context on every side.
    crop = page[36:145, 0:190]
    expected = cv2.resize(cv2.cvtColor(crop, cv2.COLOR_GRAY2BGR),
                          (raw.shape[1], raw.shape[0]), interpolation=cv2.INTER_NEAREST)
    ink = np.any(expected < 255, axis=2)
    assert np.array_equal(raw[ink], expected[ink])
    assert {0, 165, 210, 254}.issubset(set(raw[..., 0][ink]))
    assert np.array_equal(page, before_page) and window == before_window and boxes == before_boxes
    assert max(image.shape[:2]) <= 1536


def test_coloured_path_exists_only_in_explicit_guide_panel():
    page = np.full((180, 250), 255, np.uint8)
    window = context_windows([[40, 90], [135, 90]], 9, page.shape)[0]
    image = semantic_route_window_view(object(), page, window, [], COLORS)
    width = (image.shape[1] - 12) // 2
    # A mid-route blank pixel is far from either boundary bracket/label.
    sx, sy = width / 190, (image.shape[0] - 32) / 109
    x, y = round(90 * sx), round((90 - 36) * sy)
    assert np.array_equal(image[32 + y, width + 12 + x], [255, 255, 255])
    assert np.array_equal(image[32 + y, x], COLORS[0])
    # Interpolated A/B window boundaries never gain endpoint-body exemptions.
    green = np.array([70, 130, 75])
    assert not np.any(np.all(image == green, axis=2))


def test_original_endpoint_boxes_are_the_only_green_body_boundaries():
    page = np.full((250, 600), 255, np.uint8)
    windows = context_windows([[10, 100], [580, 100]], 9, page.shape)
    window = windows[3]
    boxes = [[5, 80, 20, 100], [570, 90, 590, 120]]
    image = semantic_route_window_view(object(), page, window, boxes, COLORS)
    # Both actual endpoint bodies are outside this internal window's crop.
    assert not np.any(np.all(image == np.array([70, 130, 75]), axis=2))
    with pytest.raises(ValueError):
        semantic_route_window_view(object(), page, window, boxes + [[90, 80, 100, 100]], COLORS)


def test_large_scale_composite_stays_bounded_and_raw_resizing_adds_no_removed_ink():
    page = np.full((1200, 2600), 254, np.uint8)
    cv2.line(page, (100, 600), (1500, 600), 100, 3)
    window = context_windows([[100, 600], [1540, 600]], 120, page.shape)[0]
    before = page.copy()
    image = semantic_route_window_view(object(), page, window, [], COLORS)
    width = (image.shape[1] - 12) // 2
    raw = image[32:, width + 12:]
    expected = cv2.resize(cv2.cvtColor(page[:, :2261], cv2.COLOR_GRAY2BGR),
                          (width, raw.shape[0]), interpolation=cv2.INTER_NEAREST)
    # The 254 background is original nonwhite content too, so restoration
    # removes every annotation in this raw panel, including on faint pixels.
    assert np.array_equal(raw, expected)
    assert np.array_equal(page, before) and max(image.shape[:2]) <= 1536
