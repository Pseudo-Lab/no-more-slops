"""Connection-only extension of the frozen v12 pipeline.

One context review is permitted for ambiguous inferred/dashed local crops. It
never lowers a threshold, retries a strong rejection, changes a symbol, or
accepts geometry without paired model evidence at both symbol attachments.
"""
from __future__ import annotations

import copy
import hashlib
import json
import math

import cv2
import numpy as np

REVISION = 'geometry-local-route-v13-connections'
BASELINE = 'geometry-local-route-v12'


def paired_support(values, threshold=.60):
    """Both orders agree on yes and their mean meets the unchanged threshold."""
    return (len(values) == 2 and all(type(p) in (int, float) and math.isfinite(p) and .5 <= p <= 1 for p in values)
            and sum(values)/2 >= threshold)


def context_detail(page, item, text_h):
    """Keep the exact route and anchors, add several dash periods of context."""
    H, W = page.shape[:2]
    detail = copy.deepcopy(item)
    for key in ('confidence', 'p_yes', 'rechecks'):
        detail.pop(key, None)
    pad = max(36, round(5 * text_h))
    x0, y0, x1, y1 = item['bbox']
    xs, ys = zip(*item['path'])
    detail['bbox'] = [max(0, min(x0, min(xs)-pad)), max(0, min(y0, min(ys)-pad)),
                      min(W-1, max(x1, max(xs)+pad)), min(H-1, max(y1, max(ys)+pad))]
    detail['context_review'] = 'one_unchanged_raw_view_with_dash_context'
    return detail


def context_view(extractor, page, detail, ca, cb):
    """External corner marks with every nonwhite original pixel restored."""
    x0, y0, x1, y1 = detail['bbox']
    scale = extractor.fit_scale(x1-x0+1, y1-y0+1, 768, up=6.0)
    view = extractor.ScaledView(page, (x0, y0, x1+1, y1+1), scale)
    raw = extractor.V.crop(page, x0, y0, x1+1, y1+1)
    raw = cv2.resize(raw, (view.img.shape[1], view.img.shape[0]), interpolation=cv2.INTER_NEAREST)
    original = cv2.cvtColor(raw, cv2.COLOR_GRAY2BGR)
    view.img = original.copy()
    radius = max(6, round(3*view.s))
    for p, color in ((detail['a'], ca), (detail['b'], cb)):
        px, py = view.p(*p)
        for sx in (-1, 1):
            for sy in (-1, 1):
                cx, cy = px+sx*radius, py+sy*radius
                cv2.line(view.img, (cx, cy), (cx+sx*6, cy), color, 2, cv2.LINE_8)
                cv2.line(view.img, (cx, cy), (cx, cy+sy*6), color, 2, cv2.LINE_8)
    # Even crowded brackets cannot obscure a junction, thin gray dash or body.
    ink = raw < 255
    view.img[ink] = original[ink]
    return view.finish()


async def recover_context(extractor, ctx, objs, rels):
    if ctx.kind != 'pid':
        return
    checks = getattr(ctx, 'route_checkpoints', {})
    from .route_context_geometry import deduplicate_spans, omit_duplicate_port_reviews, observed_arm_detail
    questions, metadata, pending = {}, {}, []
    for rel in rels:
        if rel.get('accepted') or rel.get('blockers') or not rel.get('path'):
            continue
        if not (rel.get('signal_gaps') or rel.get('dashed')) or len(rel.get('k3', [])) != 2:
            continue
        old_keys = rel.get('checkpoint_keys', [])
        values = [checks[k].get('confidence') for k in old_keys]
        # Missing evidence or a strongly broken span is not an ambiguous view.
        if not values or any(p is None or p < extractor.LOCAL_REJECT for p in values):
            continue
        original_details = [{**checks[k], '_source_checkpoint_key': k} for k in old_keys]
        canonical = omit_duplicate_port_reviews(deduplicate_spans(original_details))
        retained = [detail['_source_checkpoint_key'] for detail in canonical]
        deferred = [k for k in old_keys if k not in retained]
        weak = [k for k in retained if checks[k]['confidence'] < extractor.LOCAL_RECOVER]
        if not weak and not deferred:
            continue
        if deferred:
            # Ask the complete canonical route afresh. Old answers, including
            # omitted duplicates, remain visible and never become fake answers.
            weak = retained
            rel['deferred_endpoint_checkpoint_keys'] = [k for k in deferred
                if checks[k].get('reason') in {'instrument_terminal_port', 'inline_equipment_port_flange_gap'}]
            rel['covered_duplicate_checkpoint_keys'] = [k for k in deferred
                if k not in rel['deferred_endpoint_checkpoint_keys']]
        keys = {}
        for old in weak:
            original_detail = next(item for item in canonical if item['_source_checkpoint_key'] == old)
            observed = observed_arm_detail(ctx.page, original_detail, ctx.text_h, symbols=objs)
            detail = context_detail(ctx.page, observed or original_detail, ctx.text_h)
            key = hashlib.sha256(json.dumps(detail, sort_keys=True).encode()).hexdigest()[:16]
            keys[old] = key
            for tag, colors in (('A', (extractor.V.RED, extractor.BLUE)), ('B', (extractor.BLUE, extractor.V.RED))):
                name = f'v{key}_{tag}'
                if name in questions:
                    continue
                questions[name] = extractor.noul({
                    'route_context': extractor.Img(context_view(extractor, ctx.page, detail, *colors)),
                    'question': 'Two groups of coloured corner marks identify two positions at their centres. '
                                'All original ink is preserved. Using the surrounding drawing, can you follow '
                                'one original pipe or signal line between these positions? A position may lie '
                                'within a regular dash gap: require repeated aligned dashes or a visible elbow, '
                                'T junction or flange continuation. Reject an isolated mark, an unrelated '
                                'parallel line, an unconnected crossing, or a route through another symbol. '
                                'Neither the coloured marks nor proximity establish a connection.'},
                    'An original drawn line connects the marked positions.',
                    'No original drawn line connects the marked positions.')
                metadata[name] = detail
        pending.append((rel, keys, retained))
    answers = await ctx.jev.ask_chunked('K5_dash_context', {'task': 'Check an ambiguous local route using unchanged surrounding ink.'},
                                       questions, metadata) if questions else {}
    endpoint_questions, endpoint_meta, supported = {}, {}, []
    for rel, keys, retained in pending:
        rel['context_review_keys'] = keys
        for old, key in keys.items():
            ps = extractor.valid_noul_values(answers, [f'v{key}_{t}' for t in ('A', 'B')])
            checks[key] = {**metadata[f'v{key}_A'], 'rechecks': old, 'p_yes': ps,
                           'confidence': round(sum(ps)/2, 4) if len(ps) == 2 else None}
        # Both colour orders must support every new view, not only their mean.
        if not all(paired_support(checks[k]['p_yes'], extractor.LOCAL_RECOVER) for k in keys.values()):
            continue
        rel['context_endpoint_keys'] = []
        for index, point in ((rel['a'], rel['path'][0]), (rel['b'], rel['path'][-1])):
            box = extractor.erase_box(objs[index], ctx.k['erase_ext'])
            attachment = rel.get('endpoint_contacts', {}).get(index)
            if attachment and attachment.get('body_contact'):
                point = attachment['body_contact']
            detail = {'bbox': list(box), 'point': list(point)}
            key = hashlib.sha256(json.dumps(detail, sort_keys=True).encode()).hexdigest()[:16]
            rel['context_endpoint_keys'].append(key)
            for tag, colors in (('A', (extractor.V.RED, extractor.BLUE)), ('B', (extractor.BLUE, extractor.V.RED))):
                name = f'e{key}_{tag}'
                endpoint_questions[name] = extractor.noul({
                    'endpoint_detail': extractor.Img(extractor.endpoint_detail_view(ctx.page, box, point, *colors)),
                    'question': extractor.ENDPOINT_Q},
                    'The marked drawn line enters the target symbol.', 'The marked line does not enter that symbol.')
                endpoint_meta[name] = detail
        supported.append((rel, keys, retained))
    endpoints = await ctx.jev.ask_chunked('K6_context_endpoint', {'task': 'Check the attachment of one line to one symbol.'},
                                         endpoint_questions, endpoint_meta) if endpoint_questions else {}
    endpoint_checks = getattr(ctx, 'endpoint_checks', {})
    for rel, keys, retained in supported:
        values = []
        for key in rel['context_endpoint_keys']:
            ps = extractor.valid_noul_values(endpoints, [f'e{key}_{t}' for t in ('A', 'B')])
            endpoint_checks[key] = {**endpoint_meta[f'e{key}_A'], 'p_yes': ps,
                                    'confidence': round(sum(ps)/2, 4) if len(ps) == 2 else None}
            values += ps
        if not (paired_support(values[:2], extractor.LOCAL_RECOVER) and paired_support(values[2:], extractor.LOCAL_RECOVER)):
            continue
        rel['baseline_decision'] = rel.get('decision')
        rel['accepted'], rel['decision'] = True, 'dash_context_with_paired_endpoints'
        rel['initial_context_checkpoint_keys'] = rel['checkpoint_keys']
        rel['checkpoint_keys'] = [keys.get(k, k) for k in retained]
        rel['local_confidence'] = min(checks[k]['confidence'] for k in rel['checkpoint_keys'])
        rel['endpoint_confidence'] = min(sum(values[:2])/2, sum(values[2:])/2)
        rel['confidence'] = min(rel['local_confidence'], rel['endpoint_confidence'])
    ctx.route_checkpoints, ctx.endpoint_checks = checks, endpoint_checks


async def verify_added_pairs(extractor, ctx, objs, rels):
    """A new backup edge needs every local span and both original attachments."""
    qs, meta, pending = {}, {}, []
    for rel in rels:
        if not rel.get('candidate_source') or not rel.get('accepted'):
            continue
        if rel.get('decision') == 'dash_context_with_paired_endpoints':
            continue
        rel['accepted'] = False
        if rel.get('local_confidence') is None or rel['local_confidence'] < extractor.LOCAL_RECOVER:
            rel['decision'] = 'backup_route_unconfirmed'
            continue
        keys = []
        for index, point in ((rel['a'], rel['path'][0]), (rel['b'], rel['path'][-1])):
            box = extractor.erase_box(objs[index], ctx.k['erase_ext'])
            attachment = rel.get('endpoint_contacts', {}).get(index)
            if attachment and attachment.get('body_contact'):
                point = attachment['body_contact']
            detail = {'bbox': list(box), 'point': list(point)}
            key = hashlib.sha256(json.dumps(detail, sort_keys=True).encode()).hexdigest()[:16]
            keys.append(key)
            for tag, colors in (('A', (extractor.V.RED, extractor.BLUE)), ('B', (extractor.BLUE, extractor.V.RED))):
                name = f'e{key}_{tag}'
                qs[name] = extractor.noul({'endpoint_detail': extractor.Img(extractor.endpoint_detail_view(ctx.page, box, point, *colors)),
                                           'question': extractor.ENDPOINT_Q},
                                          'The marked drawn line enters the target symbol.', 'The marked line does not enter that symbol.')
                meta[name] = detail
        pending.append((rel, keys))
    got = await ctx.jev.ask_chunked('K6_backup_endpoint', {'task': 'Check the attachment of one line to one symbol.'}, qs, meta) if qs else {}
    checks = getattr(ctx, 'endpoint_checks', {})
    for rel, keys in pending:
        rel['backup_endpoint_keys'] = keys
        vals = []
        for key in keys:
            ps = extractor.valid_noul_values(got, [f'e{key}_{t}' for t in ('A', 'B')])
            checks[key] = {**meta[f'e{key}_A'], 'p_yes': ps,
                           'confidence': round(sum(ps)/2, 4) if len(ps) == 2 else None}
            vals += ps
        if paired_support(vals[:2], extractor.LOCAL_RECOVER) and paired_support(vals[2:], extractor.LOCAL_RECOVER):
            rel['accepted'], rel['decision'] = True, 'backup_route_with_paired_endpoints'
            rel['endpoint_confidence'] = min(sum(vals[:2])/2, sum(vals[2:])/2)
            rel['confidence'] = min(rel['local_confidence'], rel['endpoint_confidence'])
        else:
            rel['decision'] = 'backup_endpoint_unconfirmed'
    ctx.endpoint_checks = checks


def install(extractor):
    """Install only in an isolated worker; leave frozen files unmodified."""
    if getattr(extractor, '_connection_revision', None) == REVISION:
        return
    from . import connection_candidates, terminal_dash
    terminal_dash.install(extractor)
    connection_candidates.install(extractor)
    original = extractor.stage_verify

    async def verify(ctx, objs, rels):
        await original(ctx, objs, rels)
        await verify_added_pairs(extractor, ctx, objs, rels)
        await recover_context(extractor, ctx, objs, rels)
        extractor._last_connection_stage = (ctx, objs, rels)

    extractor.stage_verify = verify
    extractor._connection_revision = REVISION
