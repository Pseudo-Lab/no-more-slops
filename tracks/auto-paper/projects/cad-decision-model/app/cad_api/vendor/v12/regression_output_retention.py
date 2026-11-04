#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy>=1.24", "opencv-python-headless>=4.8"]
# ///
"""Preserve a previous output without treating it as exhaustive ground truth.

Objects match one-to-one by geometry, independent of class, text and ID.
Old classes, available text content and relations are then checked separately.
New output is reported as additions, never as false positives or accuracy.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import datetime, timezone
import hashlib
import itertools
import json
from pathlib import Path

import regression_review as review

IOU_MIN = .85
MAX_VERIFIED_DRIFT = 3


def _drift(a, b):
    return max(abs(x - y) for x, y in zip(a, b))


def verify_body_extents(baseline, candidate, image_path, baseline_trace=None):
    """Recompute narrow exceptions from original ink; never trust a reason tag.

    The frozen geometry mechanism is imported only for this optional original
    raster check. Candidate classes/provenance do not guide object matching.
    """
    import cv2
    import page_cv as CV
    import symbol_geometry as SG

    gray = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
    if gray is None:
        raise ValueError(f'Original image cannot be read: {image_path}')
    bw = CV.binarize(gray)
    trace = baseline_trace or {}
    CV.set_scale(trace.get('text_height') or CV.estimate_text_height(bw))
    verified = []
    for old in baseline['objects']:
        if old.get('class') == 'text':
            continue
        source = {**old, **{k: v for k, v in trace.get('objects', {}).get(old['id'], {}).items()
                           if v is not None}}
        fitted = list(SG.body_extent(bw, source, gray=gray))
        if fitted == old['bbox'] or _drift(fitted, old['bbox']) > MAX_VERIFIED_DRIFT:
            continue
        for new in candidate['objects']:
            if new['bbox'] == fitted and review.iou(old['bbox'], new['bbox']) < IOU_MIN:
                verified.append({'baseline_id': old['id'], 'candidate_id': new['id'],
                                 'before_bbox': old['bbox'], 'after_bbox': fitted,
                                 'max_pixel_drift': _drift(old['bbox'], fitted),
                                 'method': 'recomputed SG.body_extent on original raster'})
    return verified


def _matching(baseline, candidate, min_iou, verified):
    exceptions = {(p['baseline_id'], p['candidate_id']) for p in verified
                  if p['max_pixel_drift'] <= MAX_VERIFIED_DRIFT}
    neighbors, edge = {}, {}
    for old in baseline:
        options = []
        for new in candidate:
            value = review.iou(old['bbox'], new['bbox'])
            special = (old['id'], new['id']) in exceptions
            if value >= min_iou or special:
                edge[(old['id'], new['id'])] = (value, special)
                options.append((value, new['id']))
        neighbors[old['id']] = [oid for _, oid in sorted(options, key=lambda p: (-p[0], p[1]))]
    # Solve small disconnected spatial components with weighted assignment.
    # Cardinality dominates total IoU; class/ID equality/content/relations do
    # not influence the score. IDs only order equal alternatives for reporting.
    reverse = defaultdict(set)
    for old_id, choices in neighbors.items():
        for new_id in choices:
            reverse[new_id].add(old_id)
    mapping, ambiguous, visited = {}, [], set()
    for start in sorted(neighbors):
        if start in visited or not neighbors[start]:
            continue
        todo, olds, news = [start], set(), set()
        while todo:
            old_id = todo.pop()
            if old_id in olds:
                continue
            olds.add(old_id)
            for new_id in neighbors[old_id]:
                news.add(new_id); todo.extend(reverse[new_id] - olds)
        visited |= olds
        olds, news = sorted(olds), sorted(news)
        bonus = (len(olds) + 1) * 1_000_001
        weights = [[bonus + round(edge[(a, b)][0] * 1_000_000) if (a, b) in edge else None
                    for b in news] for a in olds]
        assignment, score = _weighted_assignment(weights)
        for i, j in assignment.items():
            mapping[olds[i]] = news[j]
        # Equally good geometric assignments cannot be resolved using a class
        # or a wire link. Report ambiguity and require review instead.
        if len(olds) > 1 or len(news) > 1:
            for i, j in assignment.items():
                alternative = [row[:] for row in weights]; alternative[i][j] = None
                _, alternative_score = _weighted_assignment(alternative)
                if alternative_score == score:
                    ambiguous.append({'baseline_ids': olds, 'candidate_ids': news}); break
    return mapping, edge, ambiguous


def _weighted_assignment(weights):
    """Rectangular Hungarian assignment with one unmatched dummy per row."""
    n = len(weights)
    real = len(weights[0]) if n else 0
    m = real + n
    costs = [[(-value if value is not None else 10**18) for value in row] + [0] * n
             for row in weights]
    u, v, owner, way = [0] * (n + 1), [0] * (m + 1), [0] * (m + 1), [0] * (m + 1)
    for i in range(1, n + 1):
        owner[0] = i
        j0, distance, used = 0, [10**20] * (m + 1), [False] * (m + 1)
        while True:
            used[j0] = True
            i0, delta, j1 = owner[j0], 10**20, 0
            for j in range(1, m + 1):
                if not used[j]:
                    cost = costs[i0 - 1][j - 1] - u[i0] - v[j]
                    if cost < distance[j]:
                        distance[j], way[j] = cost, j0
                    if distance[j] < delta:
                        delta, j1 = distance[j], j
            for j in range(m + 1):
                if used[j]:
                    u[owner[j]] += delta; v[j] -= delta
                else:
                    distance[j] -= delta
            j0 = j1
            if owner[j0] == 0:
                break
        while True:
            j1 = way[j0]; owner[j0] = owner[j1]; j0 = j1
            if j0 == 0:
                break
    result = {owner[j] - 1: j - 1 for j in range(1, real + 1)
              if owner[j] and weights[owner[j] - 1][j - 1] is not None}
    return result, sum(weights[i][j] for i, j in result.items())


def _closure(out):
    # A shared symbol may participate in several wire nets. Never merge net
    # groups through that symbol body; net IDs need not agree across runs.
    groups = defaultdict(list)
    for k, relation in enumerate(out['relations']):
        if relation['type'] == 'connected':
            groups[('net', relation['net']) if relation.get('net') is not None else ('edge', k)].append(relation)
    pairs = set()
    for relations in groups.values():
        adjacency = defaultdict(set)
        for r in relations:
            adjacency[r['a']].add(r['b']); adjacency[r['b']].add(r['a'])
        seen = set()
        for start in adjacency:
            if start in seen:
                continue
            todo, component = [start], set()
            while todo:
                node = todo.pop()
                if node in component:
                    continue
                component.add(node); todo.extend(adjacency[node] - component)
            seen |= component
            pairs |= {tuple(sorted(p)) for p in itertools.combinations(component, 2)}
    return pairs


def _relation_sets(out):
    directed = {(r['a'], r['b']) for r in out['relations'] if r['type'] == 'connected'}
    return {'connected_directed': directed,
            'connected_unordered': {tuple(sorted(p)) for p in directed},
            'connected_per_net_closure': _closure(out),
            'inside_directed': {(r['a'], r['b']) for r in out['relations'] if r['type'] == 'inside'}}


def evaluate(baseline, candidate, min_iou=IOU_MIN, verified_extents=()):
    """Compare complete exported outputs; schema validation is caller-owned."""
    old = {o['id']: o for o in baseline['objects']}
    new = {o['id']: o for o in candidate['objects']}
    if len(old) != len(baseline['objects']) or len(new) != len(candidate['objects']):
        raise ValueError('Duplicate object IDs cannot be matched safely')
    mapping, edge, ambiguous = _matching(list(old.values()), list(new.values()), min_iou, verified_extents)
    matched, class_changes, content_changes = [], [], []
    for old_id in sorted(mapping):
        new_id = mapping[old_id]
        a, b = old[old_id], new[new_id]
        value, special = edge[(old_id, new_id)]
        row = {'baseline_id': old_id, 'candidate_id': new_id,
               'baseline_class': a['class'], 'candidate_class': b['class'],
               'iou': round(value, 6), 'bbox_exact': a['bbox'] == b['bbox'],
               'before_bbox': a['bbox'], 'after_bbox': b['bbox'],
               'max_pixel_drift': _drift(a['bbox'], b['bbox']),
               'raw_verified_extent_exception': special}
        matched.append(row)
        if a['class'] != b['class']:
            class_changes.append(row)
        # Current exported text objects contain regions/line count rather than
        # OCR content. Check content only if it was present in the baseline.
        if a['class'] == 'text':
            for key in ['text', 'lines', 'content', 'chars']:
                if key in a and a[key] != b.get(key):
                    content_changes.append({'baseline_id': old_id, 'candidate_id': new_id,
                                            'field': key, 'before': a[key], 'after': b.get(key)})
            count = a.get('evidence', {}).get('lines')
            if count is not None and count != b.get('evidence', {}).get('lines'):
                content_changes.append({'baseline_id': old_id, 'candidate_id': new_id,
                                        'field': 'evidence.lines', 'before': count,
                                        'after': b.get('evidence', {}).get('lines')})
    missing = sorted(set(old) - set(mapping))
    added = sorted(set(new) - set(mapping.values()))
    failures = []
    if missing:
        failures.append({'gate': 'previous_objects_preserved', 'lost': missing})
    if ambiguous:
        failures.append({'gate': 'object_identity_unambiguous', 'components': ambiguous})
    if class_changes:
        failures.append({'gate': 'previous_classes_preserved', 'changed': class_changes})
    if content_changes:
        failures.append({'gate': 'previous_text_fields_preserved', 'changed': content_changes})
    before_rel, after_rel = _relation_sets(baseline), _relation_sets(candidate)
    relations = {}
    for kind, original in before_rel.items():
        mapped = {((mapping[a], mapping[b]) if kind.endswith('directed') and kind != 'connected_unordered'
                   else tuple(sorted((mapping[a], mapping[b]))))
                  for a, b in original if a in mapping and b in mapping}
        lost = [list((a, b)) for a, b in sorted(original) if a not in mapping or b not in mapping or
                ((mapping[a], mapping[b]) if kind.endswith('directed') and kind != 'connected_unordered'
                 else tuple(sorted((mapping[a], mapping[b])))) not in after_rel[kind]]
        additions = sorted(after_rel[kind] - mapped)
        relations[kind] = {'baseline': len(original), 'candidate': len(after_rel[kind]),
                           'retained': len(original) - len(lost), 'lost_baseline_pairs': lost,
                           'added_candidate_pairs': [list(p) for p in additions]}
        # P&ID connections are undirected. Report directed serialization
        # changes, but require the unordered direct pairs and per-net closure.
        if lost and kind != 'connected_directed':
            failures.append({'gate': 'previous_' + kind + '_preserved', 'lost': lost})
    symbols = [r for r in matched if old[r['baseline_id']]['class'] != 'text']
    texts = [r for r in matched if old[r['baseline_id']]['class'] == 'text']
    text_fields_present = any(any(k in o for k in ['text', 'lines', 'content', 'chars'])
                              for o in old.values() if o['class'] == 'text')
    return {'schema': 'cad_output_retention_v1', 'created_at': datetime.now(timezone.utc).isoformat(),
            'status': 'fail' if failures else 'pass', 'accuracy': None,
            'scope': 'Whole previous exported output retention only; baseline errors may be retained. No GT accuracy or false-positive claim.',
            'policy': {'identity': 'maximum cardinality then maximum total IoU; one-to-one geometry matching independent of class/text/ID',
                       'min_iou': min_iou, 'max_raw_verified_drift': MAX_VERIFIED_DRIFT,
                       'raw_exception': 'actual original raster body_extent recomputation; candidate explanation tags are not proof',
                       'connections': 'unordered direct pairs and per-net closure must remain; connected serialization direction reported; inside direction required'},
            'objects': {'baseline': len(old), 'candidate': len(new), 'retained': len(mapping),
                        'symbols_baseline': sum(o['class'] != 'text' for o in old.values()),
                        'symbols_retained': len(symbols), 'symbols_exact_bbox': sum(r['bbox_exact'] for r in symbols),
                        'texts_baseline': sum(o['class'] == 'text' for o in old.values()),
                        'texts_retained': len(texts), 'texts_exact_bbox': sum(r['bbox_exact'] for r in texts),
                        'class_unchanged': len(mapping) - len(class_changes), 'class_changes': class_changes,
                        'missing': missing, 'added': [new[oid] for oid in added],
                        'ambiguous_identity_components': ambiguous,
                        'changed_bboxes': [r for r in matched if not r['bbox_exact']],
                        'max_pixel_drift': max((r['max_pixel_drift'] for r in matched), default=0),
                        'raw_verified_extent_exceptions': [r for r in matched if r['raw_verified_extent_exception']],
                        'text_content_scored': text_fields_present,
                        'text_content_limit': 'Exported text may contain only bbox/evidence.lines; absent OCR content is not claimed preserved.',
                        'text_field_changes': content_changes, 'matching': matched},
            'relations': relations, 'failures': failures}


def korean_report(report):
    o, r = report['objects'], report['relations']
    lines = [f'이전 출력 보존 검사: {"통과" if report["status"] == "pass" else "실패"}', '',
             f'기존 심볼 {o["symbols_retained"]}/{o["symbols_baseline"]}개와 텍스트 영역 {o["texts_retained"]}/{o["texts_baseline"]}개를 대응시켰습니다. 클래스는 {o["class_unchanged"]}/{o["retained"]}개가 같습니다.',
             f'박스가 같은 심볼은 {o["symbols_exact_bbox"]}개, 텍스트 영역은 {o["texts_exact_bbox"]}개입니다. 바뀐 경계의 최대 차이는 {o["max_pixel_drift"]}픽셀입니다.',
             f'기존 직접 연결 {r["connected_unordered"]["retained"]}/{r["connected_unordered"]["baseline"]}쌍과 배관별 연결 {r["connected_per_net_closure"]["retained"]}/{r["connected_per_net_closure"]["baseline"]}쌍을 보존했습니다.',
             f'새 객체 {len(o["added"])}개와 새 직접 연결 {len(r["connected_unordered"]["added_candidate_pairs"])}쌍을 따로 기록했습니다. 정답이 없으므로 이 값은 오검출 수나 정확도가 아닙니다.']
    if not o['text_content_scored']:
        lines.extend(['', '텍스트 출력에는 원문 문자열이 없어 영역과 기록된 줄 수를 확인했습니다. 문자열 내용 보존은 평가하지 않았습니다.'])
    if report['failures']:
        lines.extend(['', '보존하지 못한 항목:'])
        for failure in report['failures']:
            lines.append(f'- {failure["gate"]}: {json.dumps({k: v for k, v in failure.items() if k != "gate"}, ensure_ascii=False)}')
    return '\n'.join(lines) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline', type=Path, required=True)
    parser.add_argument('--candidate', type=Path, required=True)
    parser.add_argument('--image', type=Path, help='Original raster to verify narrow body-extent exceptions')
    parser.add_argument('--baseline-trace', type=Path)
    parser.add_argument('--json', type=Path)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    baseline, candidate = json.loads(args.baseline.read_text()), json.loads(args.candidate.read_text())
    trace = json.loads(args.baseline_trace.read_text()) if args.baseline_trace else None
    verified = verify_body_extents(baseline, candidate, args.image, trace) if args.image else []
    result = evaluate(baseline, candidate, verified_extents=verified)
    result['provenance'] = {label: {'path': str(path.resolve()), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
                            for label, path in [('baseline', args.baseline), ('candidate', args.candidate),
                                                ('image', args.image)] if path}
    rendered = korean_report(result)
    for path, content in [(args.json, json.dumps(result, ensure_ascii=False, indent=2) + '\n'),
                          (args.report, rendered)]:
        if path:
            path.parent.mkdir(parents=True, exist_ok=True); path.write_text(content)
    print(rendered, end='')
    return 0 if result['status'] == 'pass' else 1


if __name__ == '__main__':
    raise SystemExit(main())
