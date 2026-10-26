"""The public review artifact preserves uncertainty and reference integrity."""
import copy
from types import SimpleNamespace

import cv2
import numpy as np

from cad_api.connection_coverage import _port_id
from cad_api.connection_revision import render_review, review_output


def test_review_states_and_alternatives_do_not_become_confirmed_relations(monkeypatch, tmp_path):
    objects = [{'id': f's{i}'} for i in range(4)]
    relations = [
        {'a': 0, 'b': 1, 'a_side': 'right', 'b_side': 'left', 'a_point': [10, 20],
         'b_point': [30, 20], 'path': [[10, 20], [30, 20]], 'net': 10, 'net_rank': 1, 'accepted': True},
        {'a': 1, 'b': 2, 'path': [[30, 20], [50, 20]], 'net': 11, 'net_rank': 2, 'accepted': False},
        {'a': 2, 'b': 3, 'path': [[50, 20], [70, 20]], 'net': 12, 'net_rank': 3, 'accepted': False},
    ]
    original = copy.deepcopy(relations)
    identity = _port_id('s2', 'right', [50, 20])
    geometry = {'ports': [{'id': identity, 'object': 's2', 'side': 'right', 'anchor': [50, 20],
                          'point': [50, 20], 'status': 'review_needed', 'candidate_ids': ['candidate-2']}],
                'line_ends': [{'id': 'end', 'point': [85, 85], 'status': 'review_needed', 'port_ids': [],
                               'candidate_ids': []}], 'summary': {}}
    graph = {'entities': [{'id': 'physical-port', 'kind': 'attachment', 'state': 'confirmed',
                          'coverage_port_id': identity}],
             'candidate_routes': [
                 {'index': 0, 'a': 's0', 'b': 's1', 'state': 'confirmed', 'entity_ids': ['e0']},
                 {'index': 1, 'a': 's1', 'b': 's2', 'state': 'rejected', 'entity_ids': ['e1'], 'reasons': ['no_line']},
                 {'index': 2, 'a': 's2', 'b': 's3', 'state': 'review_needed', 'entity_ids': ['physical-port', 'e2'],
                  'reasons': ['conflicting_crop_judgments']}],
             'alternative_routes': [{'parent_index': 2, 'alternative_index': 0, 'a': 's2', 'b': 's3',
                                     'net': 14, 'path': [[50, 20], [50, 70], [70, 70]],
                                     'state': 'review_needed', 'reasons': ['unasked_budget']}]}
    monkeypatch.setattr('cad_api.connection_graph.export_graph', lambda *_: copy.deepcopy(graph))
    review = review_output(SimpleNamespace(connection_geometry=geometry), objects, relations)
    assert relations == original
    assert [c['state'] for c in review['candidates']] == ['confirmed', 'rejected', 'review_needed']
    assert review['summary']['confirmed_candidates'] == 1
    assert review['summary']['review_needed_candidates'] == 2
    assert review['summary']['unresolved_ports'] == 0  # independent actual attachment was confirmed
    assert review['summary']['unresolved_line_ends'] == 1
    assert review['coverage']['ports'][0]['candidate_ids'] == ['c0003']
    assert review['candidates'][2]['evidence']['entity_ids'] == ['physical-port', 'e2']
    assert review['alternative_candidates'][0]['parent_id'] == 'c0003'
    assert review['alternative_candidates'][0]['net'] == 'review-net-14'
    image = np.full((100, 110, 3), 255, np.uint8)
    dest = tmp_path / 'review.png'
    render_review(image, review, dest)
    rendered = cv2.imread(str(dest))
    assert rendered.shape == image.shape
    assert not np.array_equal(rendered[70, 60], image[70, 60])  # alternative drawn, not silently omitted

