"""Closed-outline suspicion tests: no model calls, device labels or acceptance."""
import copy

import cv2
import numpy as np
import pytest

from cad_api.connection_semantics import endpoint_outline_extension_proposals


def fixture():
    page = np.full((240, 260), 255, np.uint8)
    endpoint = {'id': 'existing-endpoint', 'class': 'controller', 'bbox': [60, 30, 110, 70]}
    cv2.rectangle(page, (60, 30), (110, 70), 0, 1)
    cv2.rectangle(page, (70, 70), (100, 140), 0, 1)
    return page, endpoint


def test_multiple_closed_outline_edges_propose_review_without_geometry_changes():
    page, endpoint = fixture()
    path = [[45, 80], [70, 80], [70, 140], [100, 140], [100, 72]]
    original, old_endpoint, old_path = page.copy(), copy.deepcopy(endpoint), copy.deepcopy(path)
    proposals = endpoint_outline_extension_proposals(page, path, [endpoint])
    assert proposals
    proposal = max(proposals, key=lambda p: sum(p['edge_following_pixels']))
    assert proposal['trigger'] == 'multiple_original_outline_edges'
    assert len(proposal['substantial_edges']) >= 2 and sum(proposal['edge_following_pixels']) >= 27
    assert proposal['state'] == 'review_needed' and proposal['body_classification'].startswith('unknown')
    assert 'accepted' not in proposal
    assert proposal['original_path'] == path and proposal['endpoint_bbox'] == endpoint['bbox']
    assert np.array_equal(page, original) and endpoint == old_endpoint and path == old_path


def test_one_long_original_edge_also_stays_pending_instead_of_clear():
    page, endpoint = fixture()
    path = [[100, 72], [100, 134], [130, 134]]
    proposals = endpoint_outline_extension_proposals(page, path, [endpoint])
    assert proposals and any(p['trigger'] == 'one_long_original_outline_edge' for p in proposals)
    assert all(p['reason'] == 'endpoint_outline_extension_requires_review' for p in proposals)


def test_short_touch_at_an_endpoint_extension_does_not_invent_a_body_traversal():
    page, endpoint = fixture()
    assert not endpoint_outline_extension_proposals(page, [[100, 72], [100, 80], [130, 80]], [endpoint])


def test_adjacent_closed_line_loop_is_suspected_not_classified_as_a_device():
    page, endpoint = fixture()
    proposals = endpoint_outline_extension_proposals(page, [[70, 80], [70, 140], [100, 140]], [endpoint])
    assert proposals and all(p['state'] == 'review_needed' and p['body_classification'].startswith('unknown')
                             for p in proposals)


def test_unsupported_open_flange_bars_cannot_supply_closed_rectangle_geometry():
    page = np.full((240, 260), 255, np.uint8)
    endpoint = {'id': 'endpoint', 'bbox': [60, 30, 110, 70]}
    cv2.rectangle(page, (60, 30), (110, 70), 0, 1)
    for y in (100, 110, 120):
        cv2.line(page, (70, y), (100, y), 0, 1)
    assert not endpoint_outline_extension_proposals(page, [[85, 72], [85, 160]], [endpoint])


def test_unrelated_rectangle_never_borrows_a_distant_endpoint_exemption():
    page, endpoint = fixture()
    cv2.rectangle(page, (180, 100), (220, 170), 0, 1)
    assert not endpoint_outline_extension_proposals(page, [[180, 110], [180, 170], [220, 170]], [endpoint])


def test_large_page_frame_and_round_symbols_are_not_rectangle_extensions():
    page = np.full((400, 400), 255, np.uint8)
    cv2.rectangle(page, (5, 5), (395, 395), 0, 1)
    cv2.circle(page, (100, 110), 30, 0, 1)
    endpoint = {'id': 'endpoint', 'bbox': [85, 50, 115, 80]}
    assert not endpoint_outline_extension_proposals(page, [[70, 90], [70, 130], [100, 140]], [endpoint])


def test_simple_dashed_elbows_between_original_endpoint_bodies_are_not_closed_outline_suspects():
    page = np.full((240, 260), 255, np.uint8)
    first = {'id': 'first', 'bbox': [160, 20, 205, 60]}
    last = {'id': 'last', 'bbox': [65, 130, 85, 150]}
    cv2.rectangle(page, (160, 20), (205, 60), 0, 1)
    cv2.circle(page, (75, 140), 9, 0, 1)
    path = [[182, 63], [182, 80], [75, 80], [75, 127]]
    for a, b in zip(path, path[1:]):
        distance = int(max(abs(b[0] - a[0]), abs(b[1] - a[1])))
        for offset in range(0, distance, 12):
            p = tuple(round(a[i] + (b[i] - a[i]) * offset / distance) for i in (0, 1))
            q = tuple(round(a[i] + (b[i] - a[i]) * min(distance, offset + 7) / distance) for i in (0, 1))
            cv2.line(page, p, q, 170, 1)
    assert not endpoint_outline_extension_proposals(page, path, [first, last])


@pytest.mark.parametrize('path', [[[10, 10], [float('nan'), 20]], [[10, 10], [260, 20]]])
def test_nonfinite_or_outside_paths_cannot_be_inspected_as_known_geometry(path):
    page, endpoint = fixture()
    with pytest.raises(ValueError):
        endpoint_outline_extension_proposals(page, path, [endpoint])


def test_only_original_endpoints_may_seed_an_outline_proposal():
    page, endpoint = fixture()
    with pytest.raises(ValueError):
        endpoint_outline_extension_proposals(page, [[10, 10], [20, 20]], [endpoint] * 3)
