#!/usr/bin/env python3
"""Evaluate frozen reviewed drawing windows, without Jev calls or pipeline imports.

Examples:
  python experiments/regression_review.py --baseline OLD.json --candidate NEW.json --gt experiments/gt_page-029-review.json
  python experiments/regression_review.py --self-test

Bounding boxes are inclusive pixel coordinates, compatible with existing page GT.
Greedy IoU >= .5, class accuracy, and geometry coverage are separate metrics.
Only symbol centres within reviewed windows are scored. Connections use explicit
pair labels for partial fixtures; unreviewed pairs cannot become false positives.
P&ID same-net spanning-tree edges imply component closure, without joining across
separate nets through a symbol body. All output vertices are retained during closure
so sparse reviewed windows do not artificially break a valid net.
"""
from __future__ import annotations
import argparse
from collections import defaultdict
import itertools
import json
from pathlib import Path
import statistics

IOU_MIN = .5
GEOMETRY_MIN = .9


def area(b):
    return max(0, b[2] - b[0] + 1) * max(0, b[3] - b[1] + 1)


def intersection(a, b):
    return area((max(a[0], b[0]), max(a[1], b[1]), min(a[2], b[2]), min(a[3], b[3])))


def iou(a, b):
    n = intersection(a, b)
    return n / max(1, area(a) + area(b) - n)


def in_window(b, w):
    x, y = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
    return w[0] <= x <= w[2] and w[1] <= y <= w[3]


def windows_for(gt, split=None):
    if gt.get('windows') is not None:
        return [w for w in gt['windows'] if split is None or w.get('split') == split]
    return [{'id': 'reviewed', 'bbox': gt['window']}] if gt.get('window') else [{'id': 'page', 'bbox': None}]


def select_objects(out, wins, text=False):
    return [o for o in out['objects'] if (o.get('class') == 'text') == text
            and any(w['bbox'] is None or in_window(o['bbox'], w['bbox']) for w in wins)]


def match(outs, gts):
    pairs = sorted(((iou(o['bbox'], g['bbox']), o['id'], g['id']) for o in outs for g in gts), reverse=True)
    used, found = set(), {}
    for value, oid, gid in pairs:
        if value >= IOU_MIN and oid not in found and gid not in used:
            found[oid] = gid
            used.add(gid)
    return found


def box_metrics(outs, gts):
    required = [g for g in gts if not g.get('optional')]
    optional = [g for g in gts if g.get('optional')]
    found = match(outs, required)
    # Optional matches cannot steal a required detection; duplicates remain errors.
    opt = match([o for o in outs if o['id'] not in found], optional)
    neutral = set(opt)
    counted = [o for o in outs if o['id'] not in neutral]
    ob, gb = {o['id']: o for o in counted}, {g['id']: g for g in required}
    examples = []
    for gid, g in gb.items():
        oid = next((o for o, v in found.items() if v == gid), None)
        r = {'gt_id': gid, 'label': g.get('label', gid), 'expected_class': g.get('class'), 'output_id': oid,
             'baseline_id': g.get('baseline_id'), 'found': oid is not None}
        if oid:
            o = ob[oid]; n = intersection(o['bbox'], g['bbox'])
            r.update({'iou': round(iou(o['bbox'], g['bbox']), 6),
                      'gt_coverage': round(n / area(g['bbox']), 6),
                      'output_purity': round(n / area(o['bbox']), 6),
                      'output_class': o.get('class'), 'class_correct': o.get('class') == g.get('class'),
                      'output_bbox': o['bbox'], 'expected_bbox': g['bbox']})
            r['geometry_complete'] = r['gt_coverage'] >= GEOMETRY_MIN and r['output_purity'] >= GEOMETRY_MIN
        examples.append(r)
    n = len(found)
    stats = {'gt_objects': len(required), 'outputs': len(counted), 'matched': n,
             'precision': n / len(counted) if counted else 0., 'recall': n / len(required) if required else 0.,
             'mean_iou': statistics.mean(r['iou'] for r in examples if r['found']) if n else 0.,
             'class_correct': sum(r.get('class_correct', False) for r in examples),
             'class_accuracy_matched': sum(r.get('class_correct', False) for r in examples) / n if n else 0.,
             'geometry_complete': sum(r.get('geometry_complete', False) for r in examples),
             'missed': [r['gt_id'] for r in examples if not r['found']],
             'extra': [o for o in ob if o not in found], 'optional_ignored': sorted(neutral), 'examples': examples}
    return stats, found, neutral


def connected_pairs(out, closure=False, transparent=()):
    rels = [r for r in out.get('relations', []) if r.get('type', 'connected') == 'connected']
    direct = {frozenset((r['a'], r['b'])) for r in rels if r['a'] != r['b']}
    if not closure and not transparent:
        return direct
    if closure:
        groups = defaultdict(list)
        for k, r in enumerate(rels):
            groups[('net', r['net']) if r.get('net') is not None else ('edge', k)].append(r)
        result = set()
        for rs in groups.values():
            graph = defaultdict(set)
            for r in rs:
                graph[r['a']].add(r['b']); graph[r['b']].add(r['a'])
            seen = set()
            for start in graph:
                if start in seen: continue
                todo, comp = [start], set()
                while todo:
                    p = todo.pop()
                    if p in comp: continue
                    comp.add(p); todo.extend(graph[p] - comp)
                seen |= comp
                result |= {frozenset(pair) for pair in itertools.combinations(comp, 2)}
        if transparent:
            adjacency = defaultdict(set)
            for pair in result:
                a, b = tuple(pair); adjacency[a].add(b); adjacency[b].add(a)
            seen = set()
            for start in set(transparent):
                if start in seen: continue
                todo, comp = [start], set()
                while todo:
                    a = todo.pop()
                    if a in comp: continue
                    comp.add(a); todo.extend((adjacency[a] & set(transparent)) - comp)
                seen |= comp
                ends = {b for a in comp for b in adjacency[a] if b not in transparent}
                result |= {frozenset(pair) for pair in itertools.combinations(ends, 2)}
            result = {p for p in result if not (p & set(transparent))}
        return result
    # Only optional marks can be traversed across edges when a full net closure
    # is not requested (logic mode); a real symbol body never connects its ports.
    graph = defaultdict(set)
    for r in rels:
        graph[r['a']].add(r['b']); graph[r['b']].add(r['a'])
    result = set()
    for a in graph.keys() - set(transparent):
        todo, seen = list(graph[a]), {a}
        while todo:
            b = todo.pop()
            if b in seen: continue
            seen.add(b)
            if b in transparent: todo.extend(graph[b] - seen)
            elif a != b: result.add(frozenset((a, b)))
    return result


def evaluate(out, gt, split=None, closure=None):
    wins = windows_for(gt, split)
    wids = {w['id'] for w in wins}
    gts = [g for g in gt['objects'] if split is None or g.get('window_id') in wids]
    stats, mapping, neutral = box_metrics(select_objects(out, wins), [g for g in gts if g.get('class') != 'text'])
    stats['scope'] = {'split': split or 'all', 'windows': wins, 'global_accuracy': False if gt.get('windows') or gt.get('window') else True}
    if any(g.get('class') == 'text' for g in gts):
        tstats, tmap, tneutral = box_metrics(select_objects(out, wins, text=True), [g for g in gts if g.get('class') == 'text'])
        stats['text'] = tstats; mapping |= tmap; neutral |= tneutral
    closure = gt.get('connection_mode') == 'per_net_closure' if closure is None else closure
    got = connected_pairs(out, closure, neutral)
    reverse = {g: o for o, g in mapping.items()}
    required_ids = {g['id'] for g in gts if not g.get('optional')}
    if gt.get('reviewed_pairs') is not None:
        pairs = [p for p in gt['reviewed_pairs'] if p['a'] in required_ids and p['b'] in required_ids]
        records = []
        for p in pairs:
            oa, ob = reverse.get(p['a']), reverse.get(p['b'])
            connected = bool(oa and ob and frozenset((oa, ob)) in got)
            records.append({**p, 'predicted_connected': connected, 'endpoints_found': bool(oa and ob),
                            'correct': connected == p['connected'] and (p['connected'] or bool(oa and ob))})
        positives = [p for p in records if p['connected']]; negatives = [p for p in records if not p['connected'] and p['endpoints_found']]
        unavailable_negatives = [p for p in records if not p['connected'] and not p['endpoints_found']]
        tp = sum(p['predicted_connected'] for p in positives); fp = sum(p['predicted_connected'] for p in negatives)
        stats['connections'] = {'mode': 'explicit_reviewed_pairs', 'closure': closure, 'gt_positive': len(positives),
                                'gt_negative': len(negatives), 'true_positive': tp, 'false_positive': fp,
                                'false_negative': len(positives) - tp, 'true_negative': len(negatives) - fp,
                                'negative_endpoints_missing': len(unavailable_negatives),
                                'precision_reviewed': tp / (tp + fp) if tp + fp else 0.,
                                'recall_reviewed': tp / len(positives) if positives else 0., 'pairs': records}
    else:
        # Existing 16/22 GT exhaustively labels pairs among all scored symbols.
        gold = {frozenset((r['a'], r['b'])) for r in gt.get('relations', []) if r.get('type') == 'connected'
                and r['a'] in required_ids and r['b'] in required_ids}
        counted = {o['id'] for o in select_objects(out, wins) if o['id'] not in neutral}
        inferred = {frozenset((mapping.get(a, a + '?'), mapping.get(b, b + '?')))
                    for pair in got for a, b in [tuple(pair)] if a in counted and b in counted}
        tp = len(inferred & gold)
        stats['connections'] = {'mode': 'exhaustive_within_scope', 'closure': closure, 'gt_positive': len(gold),
                                'predicted_positive': len(inferred), 'true_positive': tp,
                                'false_positive': len(inferred - gold), 'false_negative': len(gold - inferred),
                                'precision_reviewed': tp / len(inferred) if inferred else 0.,
                                'recall_reviewed': tp / len(gold) if gold else 0.,
                                'missed': sorted(sorted(p) for p in gold - inferred),
                                'extra': sorted(sorted(p) for p in inferred - gold)}
    return stats


def self_test():
    # The tests distinguish net closure, missed intervening symbols, optional
    # fittings, incomplete-GT scope, duplicates and classification failures.
    boxes = [{'id': n, 'class': 'valve/outline', 'bbox': [k * 30, 0, k * 30 + 10, 10]} for k, n in enumerate('abc')]
    gt = {'objects': boxes, 'windows': [{'id': 'win', 'bbox': [-1, -1, 71, 11]}],
          'reviewed_pairs': [{'a': 'a', 'b': 'c', 'connected': False}, {'a': 'a', 'b': 'b', 'connected': True}],
          'connection_mode': 'per_net_closure'}
    out = {'objects': list(boxes), 'relations': [{'a': 'a', 'b': 'b', 'net': '1'}, {'a': 'b', 'b': 'c', 'net': '2'}]}
    assert evaluate(out, gt)['connections']['false_positive'] == 0
    out['relations'][1]['net'] = '1'
    assert evaluate(out, gt)['connections']['false_positive'] == 1
    out['objects'] += [{'id': 'outside', 'class': 'wrong', 'bbox': [900, 900, 910, 910]}]
    assert evaluate(out, gt)['outputs'] == 3
    out['objects'] += [{'id': 'dup', 'class': 'wrong', 'bbox': boxes[0]['bbox']}]
    assert evaluate(out, gt)['outputs'] == 4
    assert len(evaluate(out, gt)['extra']) == 1
    half = {'id': 'half', 'class': 'equipment', 'bbox': [0, 50, 99, 99]}
    target = {'id': 'full', 'class': 'equipment', 'bbox': [0, 0, 99, 99]}
    a, _, _ = box_metrics([half], [target])
    assert a['matched'] == 1 and a['geometry_complete'] == 0
    out2 = {'objects': boxes[:1], 'relations': [{'a': 'a', 'b': 'fit'}, {'a': 'fit', 'b': 'c'}]}
    assert frozenset(('a', 'c')) in connected_pairs(out2, transparent={'fit'})
    assert frozenset(('a', 'c')) not in connected_pairs(out2)
    out2['relations'][0]['net'] = 'left'; out2['relations'][1]['net'] = 'right'
    assert frozenset(('a', 'c')) in connected_pairs(out2, closure=True, transparent={'fit'})
    print('self-test: 9 regression assertions passed')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--baseline'); ap.add_argument('--candidate'); ap.add_argument('--gt')
    ap.add_argument('--json', type=Path); ap.add_argument('--split', choices=['reviewed', 'heldout', 'all'], default='all')
    ap.add_argument('--closure', action=argparse.BooleanOptionalAction, default=None)
    ap.add_argument('--self-test', action='store_true'); args = ap.parse_args()
    if args.self_test: self_test(); return
    if not args.gt or not (args.baseline or args.candidate): ap.error('--gt and at least one output required')
    gt = json.loads(Path(args.gt).read_text()); report = {'gt': str(Path(args.gt).resolve()), 'metrics': {'iou_threshold': IOU_MIN,
              'geometry_area_threshold': GEOMETRY_MIN, 'geometry_definition': 'both GT coverage and predicted-box purity >= 0.9; separate from IoU detection'}}
    for label, path in [('baseline', args.baseline), ('candidate', args.candidate)]:
        if path:
            report[label] = evaluate(json.loads(Path(path).read_text()), gt, None if args.split == 'all' else args.split, args.closure)
            report[label]['source'] = str(Path(path).resolve())
    if 'baseline' in report and 'candidate' in report:
        b, c = report['baseline'], report['candidate']; before = {r['gt_id']: r for r in b['examples']}
        report['example_changes'] = [{'gt_id': r['gt_id'], 'label': r['label'],
            'before': {k: before[r['gt_id']].get(k) for k in ['output_id', 'found', 'class_correct', 'geometry_complete', 'iou']},
            'after': {k: r.get(k) for k in ['output_id', 'found', 'class_correct', 'geometry_complete', 'iou']}}
            for r in c['examples']]
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True); args.json.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    for label in ['baseline', 'candidate']:
        if label in report:
            s = report[label]; c = s['connections']
            print(f"{label}: symbols {s['matched']}/{s['gt_objects']}, extra {len(s['extra'])}, class {s['class_correct']}/{s['matched']}, geometry {s['geometry_complete']}/{s['gt_objects']}; links {c['true_positive']}/{c['gt_positive']} + {c['false_positive']} false positives (reviewed scope)")


if __name__ == '__main__': main()
