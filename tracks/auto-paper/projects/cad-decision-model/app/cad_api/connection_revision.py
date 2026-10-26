"""Versioned connection graph extension and explicit review artifacts.

The frozen object extractor and the v13 supplement remain independently
selectable. Unresolved geometry never enters the confirmed relation list.
"""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import cv2

REVISION = 'geometry-local-route-v14-graph'
BASELINE = 'geometry-local-route-v12'
PREVIOUS = 'geometry-local-route-v13-connections'
SOURCE_FILES = ('connection_recovery.py', 'connection_candidates.py', 'terminal_dash.py',
                'route_context_geometry.py', 'connection_graph.py', 'connection_coverage.py',
                'connection_revision.py')


def source_hashes():
    root = Path(__file__).resolve().parent
    return {name: hashlib.sha256((root / name).read_bytes()).hexdigest() for name in SOURCE_FILES}


def install(extractor):
    if getattr(extractor, '_connection_revision', None) == REVISION:
        return
    from .connection_recovery import install as install_previous
    from .connection_coverage import install as install_coverage
    from .connection_graph import verify_shared_graph
    install_previous(extractor)
    install_coverage(extractor)
    previous_verify = extractor.stage_verify

    async def verify(ctx, objs, rels):
        await previous_verify(ctx, objs, rels)
        await verify_shared_graph(extractor, ctx, objs, rels)
        extractor._last_connection_stage = (ctx, objs, rels)

    extractor.stage_verify = verify
    extractor._connection_revision = REVISION


def review_output(ctx, objs, rels):
    """Serialize only drawing evidence; ground truth is never an input."""
    from .connection_graph import export_graph
    from .connection_coverage import finalize_coverage
    graph = copy.deepcopy(export_graph(ctx, objs, rels))
    geometry = copy.deepcopy(getattr(ctx, 'connection_geometry', {}))
    if geometry:
        updated = finalize_coverage(geometry, rels, objs, shared_graph=graph)
        if updated is not None:
            geometry = updated
    for kind in ('ports', 'line_ends'):
        for item in geometry.get(kind, []):
            item['state'] = item.get('state', item.get('status', 'review_needed'))
            item['candidate_ids'] = [f'c{int(value.split("-")[-1])+1:04d}'
                if isinstance(value, str) and value.startswith('candidate-') and value.split('-')[-1].isdigit()
                else value for value in item.get('candidate_ids', [])]
    graph_candidates = graph.get('candidate_routes', graph.get('candidates', graph.get('routes', [])))
    by_pair = {}
    by_index = {record['index']: record for record in graph_candidates if 'index' in record}
    for record in graph_candidates:
        a, b = record.get('a'), record.get('b')
        if type(a) is int:
            a = objs[a]['id']
        if type(b) is int:
            b = objs[b]['id']
        if a is not None and b is not None:
            by_pair[tuple(sorted((a, b)))] = record
    candidates = []
    for index, rel in enumerate(rels):
        a, b = objs[rel['a']]['id'], objs[rel['b']]['id']
        shared = by_index.get(index, by_pair.get(tuple(sorted((a, b))), {}))
        state = shared.get('state', rel.get('shared_graph_state', 'review_needed'))
        if rel.get('accepted'):
            state = 'confirmed'
        elif rel.get('blockers') or rel.get('decision') == 'intervening_symbol':
            state = 'rejected'
        if state not in {'confirmed', 'review_needed', 'rejected'}:
            state = 'review_needed'
        reason = shared.get('reasons', shared.get('reason', rel.get('decision', 'missing_evidence')))
        candidates.append({'id': f'c{index+1:04d}', 'a': a, 'b': b,
            'net': f"n{rel['net_rank']}" if 'net_rank' in rel else rel.get('net'),
            'a_side': rel.get('a_side'), 'b_side': rel.get('b_side'),
            'a_point': rel.get('a_point'), 'b_point': rel.get('b_point'),
            'path': copy.deepcopy(rel.get('path', [])), 'state': state,
            'accepted': bool(rel.get('accepted')), 'reason': reason,
            'evidence': {'decision': rel.get('decision'), 'k3_p_yes': rel.get('k3'),
                'entity_ids': shared.get('entity_ids', rel.get('shared_graph_entity_ids', [])),
                'candidate_source': rel.get('candidate_source'),
                'route_alternatives': copy.deepcopy(rel.get('route_alternatives', [])),
                'graph': copy.deepcopy(shared)}})
    alternatives = []
    ranked_nets = {r.get('net'): f"n{r['net_rank']}" for r in rels if 'net_rank' in r}
    for record in graph.get('alternative_routes', []):
        parent = int(record['parent_index'])
        alternative = int(record['alternative_index'])
        source = rels[parent]
        state = record.get('state', 'review_needed')
        alternatives.append({'id': f'c{parent+1:04d}-a{alternative+1}',
            'parent_id': f'c{parent+1:04d}', 'a': objs[source['a']]['id'], 'b': objs[source['b']]['id'],
            'net': ranked_nets.get(record.get('net'), f"review-net-{record.get('net')}"),
            'path': copy.deepcopy(record.get('path', [])),
            'state': state, 'accepted': bool(record.get('accepted')),
            'reason': record.get('reasons', []), 'evidence': copy.deepcopy(record)})
    primary_counts = {state: sum(c['state'] == state for c in candidates)
                      for state in ('confirmed', 'review_needed', 'rejected')}
    alternative_counts = {state: sum(c['state'] == state for c in alternatives)
                          for state in ('confirmed', 'review_needed', 'rejected')}
    summary = {f'{state}_candidates': primary_counts[state]
               for state in ('confirmed', 'review_needed', 'rejected')}
    summary['review_needed_alternatives'] = sum(c['state'] == 'review_needed' for c in alternatives)
    summary['review_needed_candidates'] += summary['review_needed_alternatives']
    ports = geometry.get('ports', [])
    ends = geometry.get('line_ends', [])
    summary.update(unresolved_ports=sum(p.get('state') == 'review_needed' for p in ports),
                   unresolved_line_ends=sum(p.get('state') == 'review_needed' for p in ends),
                   shared_entities=len(graph.get('entities', [])))
    return {'schema': 'cad_connection_review_v1', 'algorithm_revision': REVISION,
            'graph': graph, 'coverage': geometry, 'candidates': candidates,
            'alternative_candidates': alternatives, 'summary': summary,
            'candidate_counts': {'primary': primary_counts, 'alternatives': alternative_counts},
            'counting_note': 'Only output.relations of type connected count as confirmed links. '
                             'Review candidates and unresolved ports are not predicted connections. '
                             'summary.review_needed_candidates counts pending primary and alternative routes; '
                             'confirmed_candidates counts accepted primary routes only. candidate_counts provides both breakdowns.'}


def render_review(image, review, output_path):
    """Actual drawing with unresolved local spans and attachment points."""
    base = cv2.imread(str(image), cv2.IMREAD_COLOR) if isinstance(image, (str, Path)) else image.copy()
    if base is None:
        raise ValueError('Review image cannot be read')
    if base.ndim == 2:
        base = cv2.cvtColor(base, cv2.COLOR_GRAY2BGR)
    layer = base.copy()
    amber = (15, 150, 214)
    drawn = set()
    for candidate in review['candidates'] + review.get('alternative_candidates', []):
        if candidate['state'] != 'review_needed':
            continue
        path = candidate.get('path', [])
        for p, q in zip(path, path[1:]):
            p, q = tuple(map(int, p)), tuple(map(int, q))
            key = tuple(sorted((p, q)))
            if key in drawn:
                continue
            drawn.add(key)
            cv2.line(layer, p, q, amber, 2, cv2.LINE_AA)
    for port in review.get('coverage', {}).get('ports', []):
        if port.get('state') != 'review_needed':
            continue
        point = port.get('point', port.get('anchor'))
        if point is not None:
            cv2.circle(layer, tuple(map(int, point)), 7, amber, 2, cv2.LINE_AA)
    for end in review.get('coverage', {}).get('line_ends', []):
        if end.get('state') == 'review_needed' and end.get('point') is not None:
            cv2.circle(layer, tuple(map(int, end['point'])), 3, amber, 1, cv2.LINE_AA)
    rendered = cv2.addWeighted(layer, .70, base, .30, 0)
    text = f"NEEDS REVIEW: {review['summary']['review_needed_candidates']} candidates / {review['summary']['unresolved_ports']} ports"
    cv2.rectangle(rendered, (8, 8), (min(base.shape[1]-8, 820), 45), (255, 255, 255), -1)
    cv2.putText(rendered, text, (16, 33), cv2.FONT_HERSHEY_SIMPLEX, .65, (45, 65, 85), 1, cv2.LINE_AA)
    if not cv2.imwrite(str(output_path), rendered):
        raise ValueError('Review image could not be written')


def write_review_artifacts(directory, ctx, objs, rels):
    directory = Path(directory)
    review = review_output(ctx, objs, rels)
    (directory / 'input_review.json').write_text(json.dumps(review, ensure_ascii=False, indent=2, allow_nan=False))
    render_review(directory / 'input.png', review, directory / 'input_review.png')
    return review
