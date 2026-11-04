import copy

from cad_api.connection_review_visual import visualization_subset


def test_overlay_removes_redundant_glyph_and_dash_marks_without_deleting_evidence():
    review = {'summary': {'unresolved_ports': 25},
              'candidates': [{'state': 'review_needed', 'evidence': {'entity_ids': ['port1']}}],
              'alternative_candidates': [],
              'graph': {'entities': [
                  {'id': 'port1', 'kind': 'attachment', 'state': 'review_needed',
                   'geometry': {'object': 's1', 'side': 'right', 'point': [60, 50]}},
                  {'id': 'unused', 'kind': 'attachment', 'state': 'review_needed',
                   'geometry': {'object': 's2', 'side': 'left', 'point': [70, 50]}}]},
              'coverage': {'ports': [], 'line_ends': [
                  {'point': [10, 10], 'state': 'review_needed', 'reason': 'unaccounted_line_end'},
                  {'point': [30, 30], 'state': 'review_needed', 'reason': 'existing_bridge_endpoint_unverified'},
                  {'point': [80, 80], 'state': 'review_needed', 'reason': 'unaccounted_line_end'}]}}
    original = copy.deepcopy(review)
    selected = visualization_subset(review, [{'class': 'text', 'bbox': [5, 5, 15, 15]}])
    assert review == original
    assert [p['point'] for p in selected['coverage']['ports']] == [[60, 50]]
    assert [p['point'] for p in selected['coverage']['line_ends']] == [[80, 80]]
    assert selected['summary']['unresolved_ports'] == 1
    assert review['summary']['unresolved_ports'] == 25
