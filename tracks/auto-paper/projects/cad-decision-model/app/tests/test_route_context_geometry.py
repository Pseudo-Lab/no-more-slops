"""Geometry-only checks; no model answers or changed relation routes."""
import copy

import numpy as np

from cad_api.route_context_geometry import deduplicate_spans, observed_arm_detail, omit_duplicate_port_reviews


def test_exact_junction_arms_cover_spans_but_parallel_partial_and_shortcuts_stay():
    joint = {"kind": "junction", "path": [[20, 40], [60, 40], [60, 80]]}
    covered = {"kind": "span", "path": [[30, 40], [60, 40]]}
    other = [{"kind": "span", "path": [[30, 41], [60, 41]]},
             {"kind": "span", "path": [[10, 40], [30, 40]]},
             {"kind": "span", "path": [[20, 40], [60, 80]]}]
    details = [covered, joint]+other
    before = copy.deepcopy(details)
    got = deduplicate_spans(details)
    assert len(got) == 4 and got[0]["kind"] == "junction"
    assert got[0]["covered_span_paths"] == [covered["path"]]
    assert got[1:] == other and details == before


def test_port_review_removed_only_with_other_route_evidence():
    port = {"kind": "signal_gap", "reason": "instrument_terminal_port", "path": [[20, 20], [20, 35]]}
    line = {"kind": "span", "path": [[20, 35], [20, 70]]}
    assert omit_duplicate_port_reviews([port]) == [port]
    assert omit_duplicate_port_reviews([port, line]) == [line]


def test_white_marker_moves_to_same_observed_arm_while_exact_elbow_gap_stays():
    gray = np.full((140, 140), 255, np.uint8)
    gray[70, 55:91] = 165
    gray[45:51, 50] = 165
    gray[55:61, 50] = 165
    gray[65:71, 50] = 165
    core = [[55, 70], [50, 70], [50, 60]]
    item = {"kind": "signal_gap", "reason": "raw_supported_dashed_elbow",
            "path": [[80, 70]]+core+[[50, 52]], "original_gap_path": core,
            "a": [80, 70], "b": [50, 52], "bbox": [30, 30, 100, 90]}
    before = gray.copy(), copy.deepcopy(item)
    got = observed_arm_detail(gray, item, 9)
    assert got is not None and got["b"] == [50, 49]
    assert got["original_gap_path"] == core and all(p in got["path"] for p in core)
    assert gray[got["a"][1], got["a"][0]] < 200 and gray[got["b"][1], got["b"][0]] < 200
    assert np.array_equal(gray, before[0]) and item == before[1]


def test_ambiguous_parallel_raster_correction_is_rejected():
    gray = np.full((140, 140), 255, np.uint8)
    gray[30:100, 49] = 89
    gray[30:100, 51] = 89
    item = {"kind": "span", "path": [[50, 45], [50, 85]], "bbox": [40, 35, 60, 95]}
    assert observed_arm_detail(gray, item) is None


def test_marker_never_moves_inside_a_symbol_body():
    gray = np.full((140, 140), 255, np.uint8)
    gray[70, 55:91] = 165
    gray[45:51, 50] = 165
    core = [[55, 70], [50, 70], [50, 60]]
    item = {"kind": "signal_gap", "path": [[80, 70]]+core+[[50, 52]],
            "original_gap_path": core, "bbox": [30, 30, 100, 90]}
    assert observed_arm_detail(gray, item, symbols=[{"bbox": [45, 40, 55, 54]}]) is None


def test_already_observed_gray_center_is_not_shifted_to_white_neighbour():
    gray = np.full((140, 140), 255, np.uint8)
    gray[20:110, 60] = 165
    gray[20:110, 61] = 223
    item = {"kind": "span", "path": [[60, 40], [60, 80]], "bbox": [40, 20, 80, 100]}
    assert observed_arm_detail(gray, item) is None


def test_isolated_pixels_do_not_supply_an_observed_arm():
    gray = np.full((140, 140), 255, np.uint8)
    gray[40, 60] = gray[80, 60] = 0
    item = {"kind": "span", "path": [[60, 40], [60, 80]], "bbox": [40, 20, 80, 100]}
    assert observed_arm_detail(gray, item) is None
