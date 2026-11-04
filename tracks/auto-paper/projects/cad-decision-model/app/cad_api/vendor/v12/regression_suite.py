#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy>=1.24", "opencv-python-headless>=4.8"]
# ///
"""Run immutable, per-sample regression gates without importing the CAD pipeline.

Examples:
  python experiments/regression_suite.py --baseline-self-check
  python experiments/regression_suite.py --candidate-root runs/iteration-v8 --json report.json
  python experiments/regression_suite.py --pages 12,30 --candidate page012=RUN/OUTPUT.json --candidate page030=RUN/OUTPUT.json

No Jev calls are made. A missing sample or changed frozen fixture is a failure.
Known validation fixtures protect existing results; they are not fresh held-out
evidence. A suite total is a gate count, never a pooled accuracy estimate.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path

import regression_review as review
import regression_output_retention as retention

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / 'experiments/regression_samples.v7.json'


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def resolve_path(value, root=ROOT):
    path = Path(value)
    return path if path.is_absolute() else Path(root) / path


def read_fixture(spec, root=ROOT):
    path = resolve_path(spec['path'], root)
    actual = sha256(path)
    if actual != spec['sha256']:
        raise ValueError(f'Frozen fixture changed: {path}; expected {spec["sha256"]}, got {actual}')
    return path


def schema_errors(out, sample):
    """Validate the exported result, including every relation reference."""
    errors = []
    if not isinstance(out, dict):
        return ['Output must be an object']
    image = out.get('image', {})
    if not isinstance(image, dict):
        return ['image must be an object']
    if image.get('file') != f'page-{sample["page"]:03d}.png':
        errors.append('image.file does not identify this sample')
    width, height = image.get('width'), image.get('height')
    if not all(isinstance(v, int) and not isinstance(v, bool) and v > 0 for v in [width, height]):
        errors.append('image dimensions must be positive integers')
        width = height = None
    for key in ['width', 'height']:
        if key in sample.get('image', {}) and image.get(key) != sample['image'][key]:
            errors.append(f'image.{key} differs from the frozen image dimensions')
    if out.get('meta', {}).get('drawing_kind') != sample['drawing_kind']:
        errors.append('meta.drawing_kind differs from the sample manifest')
    objects = out.get('objects')
    if not isinstance(objects, list):
        return errors + ['objects must be a list']
    ids = set()
    for index, obj in enumerate(objects):
        if not isinstance(obj, dict):
            errors.append(f'objects[{index}] must be an object'); continue
        oid = obj.get('id')
        if not isinstance(oid, str) or not oid or oid in ids:
            errors.append(f'objects[{index}] has a missing or duplicate id')
        if isinstance(oid, str): ids.add(oid)
        if not isinstance(obj.get('class'), str) or not obj['class']:
            errors.append(f'objects[{index}] has no class')
        bbox = obj.get('bbox')
        if not (isinstance(bbox, list) and len(bbox) == 4 and all(
                isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v) for v in bbox)):
            errors.append(f'objects[{index}] has an invalid bbox'); continue
        if bbox[0] > bbox[2] or bbox[1] > bbox[3]:
            errors.append(f'objects[{index}] has reversed bbox coordinates')
        if width and (bbox[0] < 0 or bbox[1] < 0 or bbox[2] >= width or bbox[3] >= height):
            errors.append(f'objects[{index}] bbox lies outside the image')
        for key in ['confidence', 'class_confidence']:
            if key in obj and obj[key] is not None and not (
                    isinstance(obj[key], (int, float)) and not isinstance(obj[key], bool)
                    and math.isfinite(obj[key]) and 0 <= obj[key] <= 1):
                errors.append(f'objects[{index}].{key} is not a finite probability')
    relations = out.get('relations')
    if not isinstance(relations, list):
        return errors + ['relations must be a list']
    relation_ids = set()
    for index, relation in enumerate(relations):
        if not isinstance(relation, dict):
            errors.append(f'relations[{index}] must be an object'); continue
        rid = relation.get('id')
        if not isinstance(rid, str) or not rid or rid in relation_ids:
            errors.append(f'relations[{index}] has a missing or duplicate id')
        if isinstance(rid, str): relation_ids.add(rid)
        if relation.get('type') not in ['connected', 'inside']:
            errors.append(f'relations[{index}] has an unknown type')
        if relation.get('a') not in ids or relation.get('b') not in ids:
            errors.append(f'relations[{index}] refers to a missing object')
        if relation.get('a') == relation.get('b'):
            errors.append(f'relations[{index}] has identical endpoints')
    return errors


def pair_key(pair):
    return tuple(sorted((pair['a'], pair['b'])))


def regression_gates(baseline, candidate):
    """Preserve individual successes, not just totals that can hide lost objects."""
    failures = []
    for part in ['symbols', 'text']:
        before = baseline if part == 'symbols' else baseline.get('text')
        after = candidate if part == 'symbols' else candidate.get('text')
        if before is None:
            continue
        if after is None:
            failures.append({'gate': f'{part}_evaluated', 'lost': ['all']}); continue
        old = {r['gt_id']: r for r in before['examples']}
        new = {r['gt_id']: r for r in after['examples']}
        for metric in ['found', 'class_correct', 'geometry_complete']:
            lost = sorted(gid for gid, row in old.items() if row.get(metric)
                          and not new.get(gid, {}).get(metric))
            if lost:
                failures.append({'gate': f'{part}_{metric}_preserved', 'lost': lost})
        if len(after['extra']) > len(before['extra']):
            failures.append({'gate': f'{part}_extra_not_increased',
                             'before': len(before['extra']), 'after': len(after['extra'])})
    before, after = baseline['connections'], candidate['connections']
    if before['mode'] != after['mode'] or before['closure'] != after['closure']:
        failures.append({'gate': 'connection_semantics_unchanged'}); return failures
    if before['mode'] == 'explicit_reviewed_pairs':
        old = {pair_key(p): p for p in before['pairs']}
        new = {pair_key(p): p for p in after['pairs']}
        for positive in [True, False]:
            lost = [list(key) for key, pair in old.items()
                    if pair['connected'] == positive and pair['correct']
                    and not new.get(key, {}).get('correct')]
            if lost:
                failures.append({'gate': ('positive' if positive else 'negative') + '_pairs_preserved',
                                 'lost': sorted(lost)})
    else:
        missed_before = {tuple(pair) for pair in before['missed']}
        missed_after = {tuple(pair) for pair in after['missed']}
        if missed_after - missed_before:
            failures.append({'gate': 'positive_pairs_preserved',
                             'lost': [list(pair) for pair in sorted(missed_after - missed_before)]})
        extras_before = {tuple(pair) for pair in before['extra']}
        extras_after = {tuple(pair) for pair in after['extra']}
        if extras_after - extras_before:
            failures.append({'gate': 'no_new_exhaustive_false_positive_pair',
                             'added': [list(pair) for pair in sorted(extras_after - extras_before)]})
    if after['false_positive'] > before['false_positive']:
        failures.append({'gate': 'connection_false_positives_not_increased',
                         'before': before['false_positive'], 'after': after['false_positive']})
    return failures


def compact_metrics(metrics, connection_scored=True):
    result = {key: metrics[key] for key in ['gt_objects', 'outputs', 'matched', 'class_correct',
                                           'geometry_complete', 'mean_iou', 'missed', 'extra']}
    result['connections'] = ({key: metrics['connections'][key] for key in [
        'mode', 'closure', 'gt_positive', 'true_positive', 'false_positive', 'false_negative']}
        if connection_scored else {'scored': False, 'reason': 'no annotated connection pairs'})
    if 'text' in metrics:
        result['text'] = {key: metrics['text'][key] for key in [
            'gt_objects', 'matched', 'class_correct', 'geometry_complete', 'missed', 'extra']}
    return result


def acceptance_gates(metrics, acceptance):
    """Known critical misses need absolute targets in addition to preservation."""
    found = {row['gt_id']: row for row in metrics['examples']}
    failures = []
    for metric in ['found', 'class_correct', 'geometry_complete']:
        required = acceptance.get('required_' + metric, [])
        lost = sorted(gid for gid in required if not found.get(gid, {}).get(metric))
        if lost:
            failures.append({'gate': 'required_' + metric, 'lost': lost})
    return failures


def candidate_path(sample, mapping, candidate_root, root):
    if sample['id'] in mapping:
        return resolve_path(mapping[sample['id']], root)
    if f'page{sample["page"]:03d}' in mapping:
        return resolve_path(mapping[f'page{sample["page"]:03d}'], root)
    if candidate_root is None:
        raise ValueError(f'Missing candidate for {sample["id"]}')
    paths = list(Path(candidate_root).rglob(f'page-{sample["page"]:03d}_output.json'))
    if len(paths) != 1:
        raise ValueError(f'{sample["id"]}: expected exactly one candidate output, found {len(paths)}')
    return paths[0]


def run_suite(manifest, mapping=None, candidate_root=None, pages=None, split='all',
              baseline_self_check=False, root=ROOT):
    if manifest.get('schema') != 'cad_regression_suite_v1':
        raise ValueError('Unsupported manifest schema')
    samples = [s for s in manifest['samples'] if (pages is None or s['page'] in pages)
               and (split == 'all' or s['split'] == split)]
    if not samples:
        raise ValueError('No samples selected')
    requested = set(pages or [])
    if requested - {s['page'] for s in samples}:
        raise ValueError('Requested pages are absent from the selected manifest split')
    report = {'schema': 'cad_regression_result_v1', 'manifest_version': manifest['version'],
              'created_at': datetime.now(timezone.utc).isoformat(),
              'baseline_revision': manifest['baseline_revision'], 'split': split,
              'baseline_self_check': baseline_self_check, 'aggregate_accuracy': None,
              'scope_warning': 'Per-sample annotated scopes only; gate pass is not proof of full-page accuracy or fresh held-out performance.',
              'metric_policy': {'iou_min': review.IOU_MIN, 'geometry_min': review.GEOMETRY_MIN,
                                'geometry_rule': 'both GT area coverage and output purity',
                                'policy': manifest['policy']}, 'samples': []}
    for sample in samples:
        result = {'id': sample['id'], 'page': sample['page'], 'split': sample['split'],
                  'evaluation': sample['evaluation'], 'limits': sample['limits'], 'failures': [],
                  'validation_history': sample.get('validation_history', {})}
        for key in ['display_name', 'scope_role']:
            if key in sample:
                result[key] = sample[key]
        report['samples'].append(result)
        try:
            image_path = read_fixture(sample['image'], root)
            baseline_path = read_fixture(sample['baseline'], root)
            path = baseline_path if baseline_self_check else candidate_path(sample, mapping or {}, candidate_root, root)
            baseline = json.loads(baseline_path.read_text())
            candidate = json.loads(path.read_text())
            result['provenance'] = {'image_sha256': sha256(image_path),
                'baseline': str(baseline_path.resolve()), 'baseline_sha256': sha256(baseline_path),
                'candidate': str(path.resolve()), 'candidate_sha256': sha256(path)}
            baseline_trace_path = None
            if sample.get('baseline_trace'):
                baseline_trace_path = read_fixture(sample['baseline_trace'], root)
                result['provenance'].update({
                    'baseline_trace': str(baseline_trace_path.resolve()),
                    'baseline_trace_sha256': sha256(baseline_trace_path)})
            baseline_errors = schema_errors(baseline, sample)
            known_kind = sample.get('baseline_kind_exception')
            if known_kind:
                actual = baseline.get('meta', {}).get('drawing_kind')
                result['baseline_kind_audit'] = {'expected': sample['drawing_kind'], 'actual': actual,
                    'matches_expected': actual == sample['drawing_kind'],
                    'known_exception': known_kind, 'original_schema_errors': baseline_errors}
                if not known_kind.get('reason') or actual != known_kind.get('observed_kind'):
                    baseline_errors += ['baseline kind differs from its explicitly frozen known error']
                else:
                    baseline_errors = schema_errors(baseline, {**sample, 'drawing_kind': actual})
            if baseline_errors:
                result['failures'].append({'gate': 'baseline_schema_valid', 'errors': baseline_errors})
            # A baseline self-check audits a known broken baseline; an actual
            # candidate must always satisfy the human-reviewed expected kind.
            candidate_schema_sample = ({**sample, 'drawing_kind': known_kind['observed_kind']}
                                       if baseline_self_check and known_kind else sample)
            candidate_errors = schema_errors(candidate, candidate_schema_sample)
            if candidate_errors:
                result['failures'].append({'gate': 'candidate_schema_valid', 'errors': candidate_errors})
            if result['failures']:
                result['status'] = 'fail'; continue
            if sample['evaluation'] == 'reviewed_gt':
                gt_path = read_fixture(sample['gt'], root)
                gt = json.loads(gt_path.read_text())
                result['provenance'].update({'gt': str(gt_path.resolve()), 'gt_sha256': sha256(gt_path)})
                closure = sample['connection_mode'] == 'per_net_closure'
                b = review.evaluate(baseline, gt, closure=closure)
                c = review.evaluate(candidate, gt, closure=closure)
                scored = bool(gt.get('reviewed_pairs') or any(r.get('type') == 'connected' for r in gt.get('relations', [])))
                result.update({'scope': c['scope'], 'baseline_metrics': compact_metrics(b, scored),
                               'candidate_metrics': compact_metrics(c, scored)})
                result['failures'] += regression_gates(b, c)
                targets = acceptance_gates(c, sample.get('acceptance', {}))
                if baseline_self_check:
                    result['baseline_target_gaps'] = targets
                else:
                    result['failures'] += targets
                result['details'] = {'baseline': b, 'candidate': c}
            else:
                result['scope'] = {'global_accuracy': False, 'annotation': None,
                                   'evaluation': 'previous output retention; no GT accuracy'}
                result['counts'] = {label: {'symbols': sum(o['class'] != 'text' for o in out['objects']),
                    'text': sum(o['class'] == 'text' for o in out['objects']),
                    'connections': sum(r['type'] == 'connected' for r in out['relations'])}
                    for label, out in [('baseline', baseline), ('candidate', candidate)]}
                if baseline_trace_path is None:
                    baseline_trace_path = baseline_path.with_name(baseline_path.name.replace('_output.json', '_trace.json'))
                baseline_trace = json.loads(baseline_trace_path.read_text()) if baseline_trace_path.exists() else None
                verified = retention.verify_body_extents(baseline, candidate, image_path, baseline_trace)
                retained = retention.evaluate(baseline, candidate, verified_extents=verified)
                result['output_retention'] = retained
                result['failures'] += retained['failures']
                if baseline_trace is not None:
                    result['provenance']['retention_baseline_trace_sha256'] = sha256(baseline_trace_path)
            result['status'] = 'fail' if result['failures'] else 'pass'
        except (OSError, ValueError, KeyError, TypeError) as exc:
            result['failures'].append({'gate': 'fixtures_and_evaluation_available', 'error': str(exc)})
            result['status'] = 'fail'
    report['passed_samples'] = sum(s['status'] == 'pass' for s in report['samples'])
    report['required_samples'] = len(report['samples'])
    report['unique_pages'] = len({s['page'] for s in report['samples']})
    report['status'] = 'pass' if report['passed_samples'] == report['required_samples'] else 'fail'
    return report


def korean_report(report):
    lines = [f'기존 결과 보존 검증: {report["passed_samples"]}/{report["required_samples"]}개 검수 구역 통과({report["unique_pages"]}개 도면)', '',
             '아래 수치는 정답을 표시한 구역의 결과입니다. 검증 통과는 전체 도면 정확도나 새로운 미사용 표본의 성능을 뜻하지 않습니다.', '',
             '| 표본 | 용도 | 심볼 발견(기준 → 후보) | 정답 연결(기준 → 후보) | 판정 |',
             '|---|---|---:|---:|---|']
    for sample in report['samples']:
        purpose = ('수정에 사용' if sample['split'] == 'tuning' else
                   '신규 독립 검증' if sample.get('validation_history', {}).get('independent_this_round') else '기존 결과 보존')
        b, c = sample.get('baseline_metrics'), sample.get('candidate_metrics')
        symbols = f'{b["matched"]}/{b["gt_objects"]} → {c["matched"]}/{c["gt_objects"]}' if b else '정답 미평가'
        if b and b['connections'].get('scored') is not False:
            bc, cc = b['connections'], c['connections']
            links = f'{bc["true_positive"]}/{bc["gt_positive"]} → {cc["true_positive"]}/{cc["gt_positive"]}'
        else: links = '정답 미평가'
        if sample.get('output_retention'):
            retained = sample['output_retention']
            objects, relations = retained['objects'], retained['relations']
            symbols = f'기존 {objects["symbols_retained"]}/{objects["symbols_baseline"]}개 보존'
            links = f'기존 {relations["connected_unordered"]["retained"]}/{relations["connected_unordered"]["baseline"]}쌍 보존'
        name = sample.get('display_name') or (f'{sample["page"]}쪽' if sample['id'] == f'page{sample["page"]:03d}' else f'{sample["page"]}쪽 {sample["id"].split("-", 1)[1].upper()} 사례')
        lines.append(f'| {name} | {purpose} | {symbols} | {links} | {"통과" if sample["status"] == "pass" else "실패"} |')
    failed = [s for s in report['samples'] if s['failures']]
    if failed:
        lines.extend(['', '보존하지 못한 항목:'])
        for sample in failed:
            for failure in sample['failures']:
                lines.append(f'- {sample["page"]}쪽: {failure["gate"]}: {json.dumps({k: v for k, v in failure.items() if k != "gate"}, ensure_ascii=False)}')
    lines.extend(['', f'정답 목록 버전: {report["manifest_version"]}. 기준 알고리즘: {report["baseline_revision"]}.',
                  '심볼 클래스, 도형 범위, 추가 오검출, 텍스트와 연결 쌍의 개별 보존 여부는 JSON 결과에 따로 기록했습니다.'])
    if any(s.get('scope_role', '').startswith('supplemental_') for s in report['samples']):
        lines.extend(['', '11쪽 OPEN/CLOSE는 같은 도면의 추가 검수 구역입니다. 클래스가 정해지지 않은 명령 장치 3개는 정답 범위에서 제외했지만 출력의 추가 객체 수에는 포함될 수 있습니다. 두 구역을 별도 도면으로 세거나 전체 정밀도로 합산하지 않습니다.'])
    for sample in report['samples']:
        retained = sample.get('output_retention')
        if retained:
            objects, relations = retained['objects'], retained['relations']
            lines.extend(['', f'{sample["page"]}쪽은 전체 정답 없이 이전 출력을 비교했습니다. 기존 텍스트 영역 {objects["texts_retained"]}/{objects["texts_baseline"]}개, 클래스 {objects["class_unchanged"]}/{objects["retained"]}개와 배관별 연결 {relations["connected_per_net_closure"]["retained"]}/{relations["connected_per_net_closure"]["baseline"]}쌍을 보존했습니다. 새 객체 {len(objects["added"])}개와 새 직접 연결 {len(relations["connected_unordered"]["added_candidate_pairs"])}쌍은 미검수 추가 항목이며 정확도나 오검출 수로 세지 않습니다.'])
    kind_errors = [s for s in report['samples'] if s.get('baseline_kind_audit', {}).get('matches_expected') is False]
    if kind_errors:
        lines.extend(['', '기준 출력의 알려진 도면 종류 오류:'])
        for sample in kind_errors:
            audit = sample['baseline_kind_audit']
            lines.append(f'- {sample["page"]}쪽: 정답 종류 {audit["expected"]}, 기준 출력 종류 {audit["actual"]}. 기준 오류를 기록한 채 비교하며 후보 출력은 정답 종류를 충족해야 합니다.')
    if report['baseline_self_check']:
        lines.extend(['', '기준 출력과 기준 출력 자체를 비교했습니다. 이 실행은 검증기의 자료와 계산을 확인하며 새 알고리즘 성능을 측정하지 않습니다.'])
        gaps = [f'{sample["id"]}: {gap["gate"]} {", ".join(gap["lost"])}'
                for sample in report['samples'] for gap in sample.get('baseline_target_gaps', [])]
        if gaps:
            lines.extend(['', '기준 알고리즘이 아직 충족하지 못한 필수 사례: ' + '; '.join(gaps) + '.'])
    return '\n'.join(lines) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument('--candidate-root', type=Path)
    parser.add_argument('--candidate', action='append', default=[], metavar='SAMPLE=OUTPUT')
    parser.add_argument('--candidate-map', type=Path, help='JSON object mapping sample IDs to output paths')
    parser.add_argument('--pages', help='Comma-separated numeric page IDs')
    parser.add_argument('--split', choices=['all', 'tuning', 'validation'], default='all')
    parser.add_argument('--baseline-self-check', action='store_true')
    parser.add_argument('--json', type=Path)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    if not args.baseline_self_check and not (args.candidate_root or args.candidate or args.candidate_map):
        parser.error('Provide candidates or explicitly use --baseline-self-check')
    mapping = json.loads(args.candidate_map.read_text()) if args.candidate_map else {}
    for value in args.candidate:
        if '=' not in value: parser.error('--candidate requires SAMPLE=OUTPUT')
        key, path = value.split('=', 1)
        if key in mapping: parser.error(f'Duplicate candidate: {key}')
        mapping[key] = path
    pages = {int(p) for p in args.pages.split(',')} if args.pages else None
    report = run_suite(json.loads(args.manifest.read_text()), mapping, args.candidate_root,
                       pages, args.split, args.baseline_self_check)
    report['manifest_source'] = str(args.manifest.resolve())
    report['manifest_sha256'] = sha256(args.manifest)
    rendered = korean_report(report)
    for path, content in [(args.json, json.dumps(report, ensure_ascii=False, indent=2) + '\n'),
                          (args.report, rendered)]:
        if path:
            path.parent.mkdir(parents=True, exist_ok=True); path.write_text(content)
    print(rendered, end='')
    return 0 if report['status'] == 'pass' else 1


if __name__ == '__main__':
    raise SystemExit(main())
