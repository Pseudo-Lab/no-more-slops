"""Synthetic signal topology checks; these do not assert model accuracy."""
from __future__ import annotations

import copy
import importlib.util
from pathlib import Path
from types import SimpleNamespace

import cv2
import numpy as np
import pytest

from cad_api.terminal_dash import install, propose


@pytest.fixture
def page_cv():
    path = Path(__file__).parents[1]/"cad_api/vendor/v12/page_cv.py"
    spec = importlib.util.spec_from_file_location("terminal_dash_page_cv", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.set_scale(9)
    return module


def fixture(page_cv):
    gray = np.full((160, 160), 255, np.uint8)
    body = {"id": "s1", "class": "hand_switch", "class_confidence": .99, "bbox": [38, 10, 78, 52]}
    cv2.rectangle(gray, (38, 10), (78, 52), 0, 1)
    gray[55:62, 58] = 89  # Only one terminal dash between body and junction.
    cv2.circle(gray, (58, 71), 3, 0, -1)
    # The dot plus its stub is wider than the old compact-joint limit, just as
    # the page020 dot is 13 pixels wide at a nine-pixel drawing text scale.
    gray[71, 58:68] = 89
    for x in (71, 84, 97):
        gray[71, x:x+8] = 89
    for y in (80, 93, 106):
        gray[y:y+8, 58] = 89
    mask = page_cv.wire_mask(page_cv.binarize(gray), [body["bbox"]], [[0, 0, 159, 159]], 2)
    return gray, mask, [body]


def test_single_terminal_dash_on_true_filled_junction_adds_candidate(page_cv):
    gray, mask, bodies = fixture(page_cv)
    got = propose(gray, mask, bodies, cv=page_cv)
    assert len(got) == 1
    assert got[0]["path"] == [[58, 61], [58, 68]]
    assert got[0]["symbol"] == "s1"
    assert got[0]["requires_original_ink_check"] and got[0]["requires_endpoint_check"]
    assert "accepted" not in got[0]


def test_proposal_preserves_pixels_objects_and_boxes(page_cv):
    gray, mask, bodies = fixture(page_cv)
    before = gray.copy(), mask.copy(), copy.deepcopy(bodies)
    propose(gray, mask, bodies, cv=page_cv)
    assert np.array_equal(gray, before[0]) and np.array_equal(mask, before[1])
    assert bodies == before[2]


def test_unmarked_thin_crossing_is_not_a_filled_junction(page_cv):
    gray, mask, bodies = fixture(page_cv)
    gray[68:75, 55:62] = 255
    gray[71, 55:66] = 89
    gray[68:75, 58] = 89
    mask = page_cv.wire_mask(page_cv.binarize(gray), [bodies[0]["bbox"]], [[0, 0, 159, 159]], 2)
    assert propose(gray, mask, bodies, cv=page_cv) == []


@pytest.mark.parametrize("thickness", [3, 5])
def test_thick_solid_pipe_crossing_is_not_a_junction_dot(page_cv, thickness):
    gray, mask, bodies = fixture(page_cv)
    gray[68:75, 55:62] = 255
    radius = thickness//2
    gray[71-radius:72+radius, 40:68] = 0
    mask = page_cv.wire_mask(page_cv.binarize(gray), [bodies[0]["bbox"]], [[0, 0, 159, 159]], 2)
    assert propose(gray, mask, bodies, cv=page_cv) == []


def test_short_glyph_without_three_regular_dashes_is_rejected(page_cv):
    gray, mask, bodies = fixture(page_cv)
    gray[70:72, 70:110] = 255
    gray[79:115, 57:60] = 255
    mask = page_cv.wire_mask(page_cv.binarize(gray), [bodies[0]["bbox"]], [[0, 0, 159, 159]], 2)
    assert propose(gray, mask, bodies, cv=page_cv) == []


def test_near_parallel_branch_is_not_snapped_sideways(page_cv):
    gray, mask, bodies = fixture(page_cv)
    gray[55:62, 58] = 255
    gray[55:62, 63] = 89
    mask = page_cv.wire_mask(page_cv.binarize(gray), [bodies[0]["bbox"]], [[0, 0, 159, 159]], 2)
    assert propose(gray, mask, bodies, cv=page_cv) == []


@pytest.mark.parametrize("blocker", ["symbol", "equipment", "excluded"])
def test_gap_never_crosses_another_body_or_excluded_region(page_cv, blocker):
    gray, mask, bodies = fixture(page_cv)
    kwargs = {}
    if blocker == "symbol":
        bodies.append({"id": "s2", "class": "valve/filled", "bbox": [56, 63, 60, 65]})
    elif blocker == "equipment":
        obstacle = np.zeros_like(mask)
        obstacle[63:66, 56:61] = 1
        kwargs["obstacles"] = obstacle
    else:
        kwargs["exclude"] = [[56, 63, 60, 65]]
    assert propose(gray, mask, bodies, cv=page_cv, **kwargs) == []


def test_body_class_or_confidence_does_not_create_a_signal_attachment(page_cv):
    gray, mask, bodies = fixture(page_cv)
    bodies[0]["class_confidence"] = .4
    assert propose(gray, mask, bodies, cv=page_cv) == []
    bodies[0]["class_confidence"] = .99
    bodies[0]["class"] = "text"
    assert propose(gray, mask, bodies, cv=page_cv) == []


def test_irregular_long_empty_gap_is_rejected(page_cv):
    gray, mask, bodies = fixture(page_cv)
    gray[55:62, 58] = 255
    gray[55:58, 58] = 89
    mask = page_cv.wire_mask(page_cv.binarize(gray), [bodies[0]["bbox"]], [[0, 0, 159, 159]], 2)
    assert propose(gray, mask, bodies, cv=page_cv) == []


def test_install_keeps_original_candidates_and_is_idempotent(page_cv):
    gray, mask, bodies = fixture(page_cv)
    base = {"path": [[120, 20], [120, 25]], "gap_points": [[120, 20], [120, 25]], "reason": "original"}
    signal = SimpleNamespace(propose=lambda *args, **kwargs: [base])
    extractor = SimpleNamespace(SIG=signal, CV=page_cv)
    install(extractor)
    first = signal.propose(gray, mask, bodies)
    install(extractor)
    second = signal.propose(gray, mask, bodies)
    assert first == second and len(first) == 2 and first[0] is base


def test_transposed_geometry_supports_horizontal_terminal_branch(page_cv):
    gray, mask, bodies = fixture(page_cv)
    body = bodies[0]
    x0, y0, x1, y1 = body["bbox"]
    transposed = [{**body, "bbox": [y0, x0, y1, x1]}]
    got = propose(gray.T, mask.T, transposed, cv=page_cv)
    assert len(got) == 1 and got[0]["path"] == [[61, 58], [68, 58]]
