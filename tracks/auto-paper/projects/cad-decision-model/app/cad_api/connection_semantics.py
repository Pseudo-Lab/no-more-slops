"""Finite drawing-notation judgments after the independently frozen v14 graph.

Pixel breaks are not logical disconnections. A categorical judgment may explain
an existing code-created path as regular dashes, a nonjoining underpass, or a
real junction. It cannot generate geometry or merge the axes of a crossing.
"""
from __future__ import annotations

import copy
import hashlib
import bisect
import math
import asyncio

import cv2
import numpy as np

from . import connection_graph as graph
from . import connection_semantic_geometry as _semantic_geometry
from .connection_semantic_geometry import analyze_entity, semantic_transition_allowed

REVISION = 'geometry-local-route-v15-semantics'
MAX_LINE_REVIEWS = 192
MAX_PORT_REVIEWS = 192
LINE_OPTIONS = {
    'continuation': 'The two marked ends continue along a single original line, including regular dashes, a simple elbow, or aligned flange marks, without a branching junction or a separate crossing at an underpass gap.',
    'crossing_no_join': 'The two marked ends continue straight through a deliberate underpass/crossover gap; the line crossing them belongs to a separate circuit and does not join.',
    'junction': 'The marked ends join through a real T branch or explicitly connected multi-arm junction in the original drawing.',
    'disconnected': 'These marked ends do not have a supported logical connection along the indicated local path.',
    'uncertain': 'The original marks do not establish which of these interpretations is correct.',
}
PORT_OPTIONS = {
    'attached': 'The marked outside line enters this exact boxed symbol port, possibly through regular dashes or aligned flange marks.',
    'passes_beside': 'The outside line passes beside or behind the boxed symbol without entering this port.',
    'other_arm': 'A different nearby line arm enters the symbol; the marked outside arm does not.',
    'uncertain': 'The drawing does not establish the attachment of this exact outside arm to this port.',
}


def paired_category(distributions, options, threshold=.60):
    """Require two complete distributions to select the same finite meaning."""
    if not isinstance(distributions, (list, tuple)) or len(distributions) != 2:
        return None, None
    choices, values = [], []
    for distribution in distributions:
        if (not isinstance(distribution, dict) or set(distribution) != set(options)
                or any(type(p) not in (float, int) or not math.isfinite(p) or not 0 <= p <= 1
                       for p in distribution.values())
                or abs(sum(distribution.values()) - 1) > .02):
            return None, None
        choice = max(distribution, key=distribution.get)
        # A tied winner has no unique interpretation.
        if sum(abs(p-distribution[choice]) < 1e-9 for p in distribution.values()) != 1:
            return None, None
        choices.append(choice)
        values.append(distribution[choice])
    if choices[0] != choices[1] or min(values) < .5 or sum(values)/2 < threshold:
        return None, None
    return choices[0], sum(values)/2


def permitted_meaning(analysis, meaning, path):
    hypotheses = analysis.get('hypotheses', [])
    kinds = {
        'continuation': {'solid_continuation', 'dashed_continuation'},
        'crossing_no_join': {'crossing_underpass_no_join', 'crossing_ambiguous'},
        'junction': {'junction_join'},
    }.get(meaning, set())
    return any((h.get('kind') in kinds or meaning == 'continuation' and
                h.get('kind') == 'junction_join' and h.get('junction_type') in {'elbow', 'dashed_elbow'})
               and semantic_transition_allowed(h, path, meaning=meaning) for h in hypotheses)


def apply_line_answer(entity, analysis, distributions, names, threshold=.60):
    meaning, confidence = paired_category(distributions, LINE_OPTIONS, threshold)
    record = {'stage': 'K9_drawing_notation', 'question_names': names,
              'raw_distributions': copy.deepcopy(distributions),
              'meaning': meaning, 'confidence': confidence, 'geometry': copy.deepcopy(analysis),
              'coordinates_source': 'existing_code_created_path',
              'crossing_policy': 'same_axis_continuation_only_never_union_crossing_axes'}
    entity.setdefault('pre_semantic_state', entity['state'])
    entity.setdefault('pre_semantic_reasons', copy.deepcopy(entity.get('reasons', [])))
    entity['semantic_interpretation'] = record
    if meaning is None or meaning == 'uncertain':
        entity['state'], entity['confidence'] = 'review_needed', None
        entity['reasons'] = ['drawing_notation_unresolved']
    elif meaning == 'disconnected':
        entity['state'], entity['confidence'] = 'rejected', None
        entity['reasons'] = ['drawing_notation_disconnected']
    elif not permitted_meaning(analysis, meaning, entity['path']):
        entity['state'], entity['confidence'] = 'review_needed', None
        entity['reasons'] = ['semantic_answer_incompatible_with_code_geometry']
    else:
        entity['state'], entity['confidence'] = 'confirmed', confidence
        entity['reasons'] = ['drawing_notation_' + meaning]
    return record


def apply_port_answer(entity, distributions, names, threshold=.60):
    meaning, confidence = paired_category(distributions, PORT_OPTIONS, threshold)
    entity.setdefault('pre_semantic_state', entity['state'])
    entity.setdefault('pre_semantic_reasons', copy.deepcopy(entity.get('reasons', [])))
    entity['semantic_interpretation'] = {
        'stage': 'K10_semantic_actual_port', 'question_names': names,
        'raw_distributions': copy.deepcopy(distributions), 'meaning': meaning,
        'confidence': confidence, 'coordinates_source': 'existing_observed_body_contact_and_outside_anchor'}
    observed = entity.get('detail', {}).get('contact_geometry_status') == 'observed'
    if meaning == 'attached' and observed:
        entity['state'], entity['confidence'] = 'confirmed', confidence
        entity['reasons'] = ['semantic_exact_observed_port_attached']
    elif meaning in {'passes_beside', 'other_arm'}:
        entity['state'], entity['confidence'] = 'rejected', None
        entity['reasons'] = ['semantic_exact_port_' + meaning]
    else:
        entity['state'], entity['confidence'] = 'review_needed', None
        entity['reasons'] = ['semantic_port_unresolved' if observed else 'actual_body_contact_unresolved']


def _priority(entity, routes, registry, work_rels, eligible):
    relevant = [routes[i] for i in entity['candidate_indices'] if i in eligible]
    unresolved = min((sum(registry[k]['state'] != 'confirmed' for k in r['entity_ids'])
                      for r in relevant), default=999)
    pair_support = max((sum(work_rels[r['index']].get('k3', [0, 0]))/2
                        if graph._valid_pair(work_rels[r['index']].get('k3')) else 0
                        for r in relevant), default=0)
    return unresolved, -len(relevant), -pair_support, entity['id']


async def _review_lines(extractor, ctx, selected):
    questions, metadata = {}, {}
    for entity, analysis in selected:
        detail = copy.deepcopy(entity['detail'])
        detail.update(path=entity['path'], a=entity['path'][0], b=entity['path'][-1],
                      view_pad=max(36, round(ctx.text_h*6)))
        names = []
        for tag, colors in (('A', (extractor.V.RED, extractor.BLUE)), ('B', (extractor.BLUE, extractor.V.RED))):
            name = f"sm{entity['id']}_{tag}"
            names.append(name)
            options = LINE_OPTIONS if tag == 'A' else dict(reversed(list(LINE_OPTIONS.items())))
            questions[name] = extractor.choice({
                'drawing_detail': extractor.Img(graph.raw_local_view(extractor, ctx.page, detail, colors)),
                'question': 'Interpret the original P&ID notation between the two bracket centres. '
                    'Judge the logical line represented by the original black/grey strokes, NOT uninterrupted pixels. '
                    'Regular repeated dashes and a deliberate gap where a line passes underneath another line '
                    'can continue the SAME line. A crossover/underpass does NOT join the other crossing axis. '
                    'For a path changing direction, require a real elbow or branch rather than jumping between '
                    'unconnected crossing lines. Flange bars may represent an inline connection. '
                    'Use the surrounding original arms to distinguish continuation, separate crossing, and junction. '
                    'Never travel through an intervening symbol or follow a nearby parallel line. '
                    'The colours only locate existing endpoints and never create a stroke.',
                'code_proposed_path': entity['path'],
                'code_hypotheses': [h['kind'] for h in analysis.get('hypotheses', [])]}, options)
            metadata[name] = {**detail, 'entity': entity['id'], 'analysis': analysis,
                              'options': list(options), 'coordinates_generated_by': 'code'}
        entity['_semantic_question_names'] = names
    got = await ctx.jev.ask_chunked('K9_drawing_notation', {'task': 'Interpret finite drawing line notation.'},
                                    questions, metadata) if questions else {}
    for entity, analysis in selected:
        names = entity.pop('_semantic_question_names')
        apply_line_answer(entity, analysis, [got.get(name) for name in names], names)


def semantic_port_view(extractor, page, detail, color):
    """One composite image with context and one unambiguous outside-arm marker.

    The observed port and outside anchor can be only three pixels apart. Two
    large brackets then overlap. Mark just the existing outside anchor in each
    panel; the unchanged green target boundary identifies its exact port.
    """
    marker = detail.get('outside_marker', detail.get('line_anchor'))
    context = copy.deepcopy(detail)
    context.pop('point', None)
    context.update(anchors=[marker], view_pad=max(54, int(detail.get('view_pad', 54))))
    close = copy.deepcopy(context)
    close['view_pad'] = 18
    panels = [graph.raw_local_view(extractor, page, item, (color,), ('L',))
              for item in (context, close)]
    height = max(panel.shape[0] for panel in panels)
    width = sum(panel.shape[1] for panel in panels) + 12
    image = np.full((height + 32, width, 3), 255, np.uint8)
    offset = 0
    for label, panel in zip(('Surrounding drawing', 'Exact target port'), panels):
        cv2.putText(image, label, (offset + 8, 22), cv2.FONT_HERSHEY_SIMPLEX,
                    .55, (50, 50, 50), 1, cv2.LINE_AA)
        image[32:32 + panel.shape[0], offset:offset + panel.shape[1]] = panel
        offset += panel.shape[1] + 12
    if max(image.shape[:2]) > 1536:
        scale = 1536 / max(image.shape[:2])
        image = cv2.resize(image, (max(1, round(image.shape[1] * scale)),
                                  max(1, round(image.shape[0] * scale))),
                           interpolation=cv2.INTER_NEAREST)
    return image


async def _review_ports(extractor, ctx, selected):
    questions, metadata = {}, {}
    for entity in selected:
        detail = copy.deepcopy(entity['detail'])
        detail['view_pad'] = max(36, round(ctx.text_h*6))
        names = []
        for tag, colors in (('A', (extractor.V.RED, extractor.BLUE)), ('B', (extractor.BLUE, extractor.V.RED))):
            name = f"sp{entity['id']}_{tag}"
            names.append(name)
            options = PORT_OPTIONS if tag == 'A' else dict(reversed(list(PORT_OPTIONS.items())))
            questions[name] = extractor.choice({
                'port_and_surrounding_line': extractor.Img(semantic_port_view(extractor, ctx.page, detail, colors[1])),
                'question': 'Both panels show the SAME original drawing. The green box identifies the '
                    'target symbol. The single coloured bracket labelled L marks the existing outside '
                    'line arm beside the selected boundary contact. Decide whether that exact original '
                    'arm enters the target at the specified port. The second panel enlarges the same '
                    'port; it is not another candidate. A signal line can be faint grey and regularly dashed; aligned '
                    'flange marks and intentional small gaps do not require solid pixel continuity. '
                    'Follow the same original line in context to the selected boundary. A nearby or '
                    'crossing line does not enter the symbol merely because it is close. '
                    'Do not use a different port, a different parallel arm, or the symbol body to join circuits. '
                    'The coloured bracket never creates a connection.',
                'selected_port_side': detail.get('side'),
                'code_observed_port': detail.get('body_contact', detail.get('point')),
                'code_observed_outside_anchor': detail.get('line_anchor')}, options)
            metadata[name] = {**detail, 'entity': entity['id'], 'kind': 'attachment',
                              'options': list(options), 'coordinates_generated_by': 'code'}
        entity['_semantic_question_names'] = names
    # Keep each large context/detail composite pair in its own request group.
    # Different backends can reject a multi-port image batch even when the
    # generic pixel-based token estimate fits. The backend's existing semaphore
    # still limits concurrent calls; colour orders remain paired and cacheable.
    state = {'task': 'Classify one exact observed drawing port.'}
    batches = [{name: questions[name] for name in entity['_semantic_question_names']}
               for entity in selected]
    answers = await asyncio.gather(*(ctx.jev.ask_chunked('K10_semantic_actual_port', state,
        batch, {name: metadata[name] for name in batch}) for batch in batches)) if batches else []
    got = {name: answer for batch in answers for name, answer in batch.items()}
    for entity in selected:
        names = entity.pop('_semantic_question_names')
        apply_port_answer(entity, [got.get(name) for name in names], names)


def _window_finite_path(path, shape):
    if not isinstance(path, (list, tuple)) or not 2 <= len(path) <= 8192:
        raise ValueError('A finite route needs 2–8192 points')
    h, w = shape[:2]
    points = []
    for point in path:
        if (not isinstance(point, (list, tuple)) or len(point) != 2
                or any(type(value) not in (int, float) or not math.isfinite(value) for value in point)
                or not 0 <= point[0] < w or not 0 <= point[1] < h):
            raise ValueError('Route points must remain within the original image')
        copied = list(point)
        if not points or copied != points[-1]:
            points.append(copied)
    if len(points) < 2:
        raise ValueError('A route must contain two distinct points')
    return points


def _window_arclength(path):
    distances = [0.0]
    for a, b in zip(path, path[1:]):
        distances.append(distances[-1] + math.dist(a, b))
    return distances


def _window_at_distance(path, distances, distance):
    index = min(len(path) - 2, max(0, bisect.bisect_right(distances, distance) - 1))
    if math.isclose(distance, distances[index], abs_tol=1e-9):
        return list(path[index])
    if math.isclose(distance, distances[index + 1], abs_tol=1e-9):
        return list(path[index + 1])
    share = (distance - distances[index]) / (distances[index + 1] - distances[index])
    return [path[index][axis] + (path[index + 1][axis] - path[index][axis]) * share for axis in (0, 1)]


def context_windows(path, text_h, shape):
    """Cover the unchanged route with scale-aware windows and half-length steps.

    Window length is ``max(72, 12 * text_h)`` in original pixels (108px at 9px).
    Interpolation creates inspection boundaries only; every original interior
    vertex remains present. The returned plan is complete and has no review
    budget cap: the caller must retain any windows it cannot afford to review.
    """
    if type(text_h) not in (int, float) or not math.isfinite(text_h) or text_h <= 0:
        raise ValueError('text_h must be finite and positive')
    points = _window_finite_path(path, shape)
    distances = _window_arclength(points)
    total = distances[-1]
    length = max(72.0, 12.0 * text_h)
    step = length / 2
    windows, start = [], 0.0
    while True:
        end = min(total, start + length)
        first = _window_at_distance(points, distances, start)
        last = _window_at_distance(points, distances, end)
        inner = [list(point) for point, distance in zip(points, distances)
                 if start + 1e-9 < distance < end - 1e-9]
        subpath = [first] + inner + [last]
        windows.append({'path': subpath, 'start_distance': start, 'end_distance': end,
                        'text_h': text_h, 'window_length': length, 'step_length': step})
        if math.isclose(end, total, rel_tol=0, abs_tol=1e-9):
            break
        start += step
    return windows


def _window_endpoint_items(endpointboxes, shape):
    if not isinstance(endpointboxes, (tuple, list)) or len(endpointboxes) > 2:
        raise ValueError('Only the original route endpoint boxes may be supplied')
    h, w = shape[:2]
    items = []
    for index, entry in enumerate(endpointboxes):
        box = entry.get('bbox') if isinstance(entry, dict) else entry
        if box is None:
            continue
        if (not isinstance(box, (tuple, list)) or len(box) != 4
                or any(type(value) not in (int, float) or not math.isfinite(value) for value in box)
                or not 0 <= box[0] <= box[2] < w or not 0 <= box[1] <= box[3] < h):
            raise ValueError('Endpoint boxes must use existing original-image coordinates')
        items.append((index, list(box)))
    return items


def _window_image_geometry(page, window):
    path = _window_finite_path(window.get('path'), page.shape)
    text_h = window.get('text_h', 9)
    if type(text_h) not in (int, float) or not math.isfinite(text_h) or text_h <= 0:
        raise ValueError('text_h must be finite and positive')
    if _window_arclength(path)[-1] > max(72.0, 12.0 * text_h) + 1e-7:
        raise ValueError('Use a finite local window, not a full route, for this view')
    pad = max(36, round(6 * text_h))
    xs, ys = zip(*path)
    h, w = page.shape[:2]
    rect = (max(0, math.floor(min(xs)) - pad), max(0, math.floor(min(ys)) - pad),
            min(w, math.ceil(max(xs)) + pad + 1), min(h, math.ceil(max(ys)) + pad + 1))
    return path, rect


def semantic_route_window_view(extractor, page, window, endpointboxes, colors):
    """One original/guide composite; only the guide paints the supplied path.

    The raw panel restores every original nonwhite pixel after annotations.
    Nearest-neighbour resizing preserves sampled faint grey values, and no
    annotation removes or alters original ink in the displayed raw panel.
    Green boxes identify only supplied original endpoint bodies, even when the
    ends of this particular window fall elsewhere along the route.
    """
    image = np.asarray(page)
    if image.ndim == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    elif image.ndim == 3 and image.shape[2] == 4:
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
    elif image.ndim != 3 or image.shape[2] != 3:
        raise ValueError('The original page must be grayscale, BGR, or BGRA')
    if not isinstance(colors, (tuple, list)) or len(colors) != 2:
        raise ValueError('Two window boundary colours are required')
    path, rect = _window_image_geometry(image, window)
    endpoints = _window_endpoint_items(endpointboxes, image.shape)
    x0, y0, x1, y1 = rect
    crop = image[y0:y1, x0:x1]
    header, gutter, max_side = 32, 12, 1536
    max_panel_width = (max_side - gutter) // 2
    scale = min(6.0, max_panel_width / crop.shape[1], (max_side - header) / crop.shape[0])
    width, height = max(1, math.floor(crop.shape[1] * scale)), max(1, math.floor(crop.shape[0] * scale))
    original = cv2.resize(crop, (width, height), interpolation=cv2.INTER_NEAREST)
    raw, guide = original.copy(), original.copy()

    def position(point):
        return (round((point[0] - x0) * width / crop.shape[1]),
                round((point[1] - y0) * height / crop.shape[0]))

    # This coloured stroke appears only under the explicit code-guide label.
    guide_points = np.asarray([position(point) for point in path], np.int32)
    cv2.polylines(guide, [guide_points], False, colors[0], 2, cv2.LINE_8)
    for panel in (raw, guide):
        for index, point in enumerate((path[0], path[-1])):
            x, y = position(point)
            radius = max(6, round(3 * scale))
            for sx in (-1, 1):
                for sy in (-1, 1):
                    cx, cy = x + sx * radius, y + sy * radius
                    cv2.line(panel, (cx, cy), (cx + sx * 6, cy), colors[index], 2, cv2.LINE_8)
                    cv2.line(panel, (cx, cy), (cx, cy + sy * 6), colors[index], 2, cv2.LINE_8)
            cv2.putText(panel, ('A', 'B')[index], (x + radius + 8, y - radius - 3),
                        cv2.FONT_HERSHEY_SIMPLEX, .55, colors[index], 1, cv2.LINE_AA)
        for index, box in endpoints:
            if box[0] >= x1 or box[2] < x0 or box[1] >= y1 or box[3] < y0:
                continue  # A far global endpoint never expands a local crop.
            p, q = position([box[0] - 2, box[1] - 2]), position([box[2] + 2, box[3] + 2])
            green = (70, 130, 75)
            cv2.rectangle(panel, p, q, green, 1, cv2.LINE_8)
            cv2.putText(panel, 'Endpoint ' + ('1', '2')[index], (max(2, p[0]), max(14, p[1] - 4)),
                        cv2.FONT_HERSHEY_SIMPLEX, .45, green, 1, cv2.LINE_AA)
    nonwhite = np.any(original < 255, axis=2)
    raw[nonwhite] = original[nonwhite]
    composite = np.full((height + header, 2 * width + gutter, 3), 255, np.uint8)
    for label, offset, panel in (('Code path guide only', 0, guide), ('Original drawing', width + gutter, raw)):
        cv2.putText(composite, label, (offset + 8, 22), cv2.FONT_HERSHEY_SIMPLEX,
                    .55, (50, 50, 50), 1, cv2.LINE_AA)
        composite[header:, offset:offset + width] = panel
    return composite


def _outline_valid_path(path, shape):
    h, w = shape[:2]
    if not isinstance(path, (tuple, list)) or not 2 <= len(path) <= 8192:
        raise ValueError('A finite original route is required')
    result = []
    for point in path:
        if (not isinstance(point, (tuple, list)) or len(point) != 2
                or any(type(v) not in (int, float) or not math.isfinite(v) for v in point)
                or not 0 <= point[0] < w or not 0 <= point[1] < h):
            raise ValueError('Route coordinates must remain on the original page')
        result.append(list(point))
    return result


def _outline_distance(point, a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    length2 = dx * dx + dy * dy
    t = max(0, min(1, ((point[0] - a[0]) * dx + (point[1] - a[1]) * dy) / length2)) if length2 else 0
    return math.hypot(point[0] - a[0] - t * dx, point[1] - a[1] - t * dy)


def _outline_following(path, polygon, tolerance=3):
    edges = list(zip(polygon, polygon[1:] + polygon[:1]))
    following = [0.0] * 4
    for a, b in zip(path, path[1:]):
        distance = math.dist(a, b)
        if not distance:
            continue
        count = max(1, math.ceil(distance))
        weight = distance / count
        for index in range(count):
            t = (index + .5) / count
            point = [a[axis] + (b[axis] - a[axis]) * t for axis in (0, 1)]
            distances = [_outline_distance(point, p, q) for p, q in edges]
            closest = min(range(4), key=distances.__getitem__)
            if distances[closest] <= tolerance:
                following[closest] += weight
    return following, [math.dist(a, b) for a, b in edges]


def endpoint_outline_extension_proposals(page, path, endpointboxes, text_h=9):
    """Inspect raw, closed, axis-aligned symbol-scale rectangles at endpoints.

    At least two substantial edges totalling 3*text_h, or one edge followed
    for max(4*text_h, 60% of its original length), warrants review. Endpoints,
    paths and detected contours are copied into evidence only; none are moved.
    """
    if type(text_h) not in (int, float) or not math.isfinite(text_h) or text_h <= 0:
        raise ValueError('text_h must be finite and positive')
    image = np.asarray(page)
    gray = image if image.ndim == 2 else cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY if image.shape[2] == 4 else cv2.COLOR_BGR2GRAY)
    path = _outline_valid_path(path, gray.shape)
    if not isinstance(endpointboxes, (tuple, list)) or len(endpointboxes) > 2:
        raise ValueError('Only the two original endpoint boxes may seed this proposal')
    raw = np.uint8(gray < 210)
    h, w = gray.shape
    maximum_size = max(72, round(18 * text_h))
    proposals, seen = [], set()
    for endpoint_index, endpoint in enumerate(endpointboxes):
        box = endpoint.get('bbox') if isinstance(endpoint, dict) else endpoint
        if not isinstance(box, (tuple, list)) or len(box) != 4:
            continue
        if (any(type(v) not in (int, float) or not math.isfinite(v) for v in box)
                or not 0 <= box[0] <= box[2] < w or not 0 <= box[1] <= box[3] < h):
            raise ValueError('Endpoint bbox must use original-image positions')
        identifier = endpoint.get('id', str(endpoint_index)) if isinstance(endpoint, dict) else str(endpoint_index)
        pad = maximum_size + round(2 * text_h) + 4
        x0, y0 = max(0, math.floor(box[0]) - pad), max(0, math.floor(box[1]) - pad)
        x1, y1 = min(w, math.ceil(box[2]) + pad + 1), min(h, math.ceil(box[3]) + pad + 1)
        patch = raw[y0:y1, x0:x1]
        contours, _ = cv2.findContours(patch, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            cx, cy, cw, ch = cv2.boundingRect(contour)
            if (min(cw, ch) < 2 * text_h or max(cw, ch) > maximum_size
                    or cx <= 0 or cy <= 0 or cx + cw >= patch.shape[1] or cy + ch >= patch.shape[0]):
                continue  # A crop edge cannot supply a synthetic closed side.
            area = abs(cv2.contourArea(contour))
            if area / (cw * ch) <= .85:
                continue
            approx = cv2.approxPolyDP(contour, .025 * cv2.arcLength(contour, True), True)
            if len(approx) != 4 or not cv2.isContourConvex(approx):
                continue
            polygon = (approx.reshape(-1, 2) + np.array([x0, y0])).tolist()
            if any(min(abs(b[0] - a[0]), abs(b[1] - a[1])) > 3 for a, b in zip(polygon, polygon[1:] + polygon[:1])):
                continue
            rect = [cx + x0, cy + y0, cx + x0 + cw - 1, cy + y0 + ch - 1]
            overlap_x = min(rect[2], box[2]) - max(rect[0], box[0])
            overlap_y = min(rect[3], box[3]) - max(rect[1], box[1])
            gap_x = max(0, rect[0] - box[2], box[0] - rect[2])
            gap_y = max(0, rect[1] - box[3], box[1] - rect[3])
            related = ((overlap_x >= .5 * min(cw, box[2] - box[0] + 1) and gap_y <= 2 * text_h)
                       or (overlap_y >= .5 * min(ch, box[3] - box[1] + 1) and gap_x <= 2 * text_h))
            extension = max(box[0] - rect[0], box[1] - rect[1], rect[2] - box[2], rect[3] - box[3])
            if not related or extension < 2 * text_h:
                continue
            following, edge_lengths = _outline_following(path, polygon)
            substantial = [i for i, value in enumerate(following) if value >= max(2, .5 * text_h)]
            multi_edge = len(substantial) >= 2 and sum(following) >= 3 * text_h
            long_edges = [i for i, value in enumerate(following)
                          if value >= max(4 * text_h, .6 * edge_lengths[i])]
            if not multi_edge and not long_edges:
                continue
            identity = (str(identifier), tuple(rect))
            if identity in seen:
                continue
            seen.add(identity)
            proposals.append({'kind': 'endpoint_outline_extension_suspected', 'state': 'review_needed',
                'reason': 'endpoint_outline_extension_requires_review', 'endpoint_id': identifier,
                'endpoint_bbox': list(box), 'observed_bbox': rect, 'observed_polygon': polygon,
                'original_path': [list(point) for point in path], 'raster_threshold': 210,
                'raster_tolerance': 3, 'area_bbox_ratio': area / (cw * ch),
                'bbox_extension_pixels': extension, 'edge_following_pixels': following,
                'edge_lengths': edge_lengths, 'substantial_edges': substantial,
                'long_edges': long_edges, 'trigger': 'multiple_original_outline_edges' if multi_edge else 'one_long_original_outline_edge',
                'raw_context_bbox': [x0, y0, x1, y1],
                'raw_context_sha256': hashlib.sha256(np.ascontiguousarray(gray[y0:y1, x0:x1]).tobytes()).hexdigest(),
                'body_classification': 'unknown; a closed line loop can also match',
                'safety': {'geometry_is_not_acceptance': True, 'object_bbox_changed': False,
                           'route_changed': False, 'raw_ink_changed': False,
                           'caller_must_preserve_prior_v14_accepted_routes': True}})
    return proposals


def _corner_mixed_four_arms(raw, center, text_h, objects, tables):
    radius = max(5, min(18, round(text_h)))
    solid = {name: _semantic_geometry._arm(raw, center, name, radius) for name in _semantic_geometry._DIRECTIONS}
    dashed = {name: _semantic_geometry._regular_dash_arm(raw, center, name, text_h, objects, tables)
              for name in _semantic_geometry._DIRECTIONS}
    references = [arm for arm in dashed.values() if arm and arm['periodic_context']]
    arms = []
    for name in _semantic_geometry._DIRECTIONS:
        if solid[name]['present'] and solid[name]['touches_center']:
            arms.append({**solid[name], 'ink_type': 'solid_original_arm'})
            continue
        arm = dashed[name]
        if not arm:
            continue
        supported = arm['periodic_context'] or any(
            abs(arm['median_period'] - reference['median_period']) <= max(3, .35 * reference['median_period'])
            and abs(arm['median_gap'] - reference['median_gap']) <= max(2, .35 * reference['median_gap'])
            for reference in references)
        if supported:
            arms.append({**arm, 'present': True, 'ink_type': 'periodic_original_dash_arm'})
    dot = _semantic_geometry._dot(raw, center, text_h)
    if len(arms) != 4:
        return None
    return {'kind': 'junction_join' if dot['present'] else 'crossing_ambiguous',
            'center': list(center), 'arms': arms, 'dot': dot,
            'evidence': 'four_original_arms_including_bounded_regular_dash_context_without_join_dot'}


def raw_corner_transition_proposals(page, path, objects=(), text_h=9, tables=()):
    """Inspect every original axis-changing turn, even its old confirmed entity.

    A short raw T may hide a fourth dashed arm in the wider context. Observe
    each solid or periodic dashed arm independently at one coherent centre;
    a four-arm/no-dot crossing never licenses changing axes. Underpasses also
    retain only their opposite same-axis arms. No guard applies to straight
    same-axis portions or a visible three-arm T/dot without contrary evidence.
    """
    if type(text_h) not in (int, float) or not math.isfinite(text_h) or text_h <= 0:
        raise ValueError('text_h must be finite and positive')
    gray = _semantic_geometry._gray(page)
    finite = _semantic_geometry.finite_path(path, gray.shape)
    raw = gray < _semantic_geometry.RAW_THRESHOLD
    tolerance = _semantic_geometry._raster_tolerance(text_h)
    results = []
    for turn in _semantic_geometry.classify_turns(finite):
        incoming, outgoing = turn['incoming_arm'], turn['outgoing_arm']
        if (not turn['turning'] or incoming is None or outgoing is None
                or turn['same_axis']):
            continue
        index, center = turn['index'], turn['point']
        triplet = finite[index - 1:index + 2]
        if _semantic_geometry.blocked_by_regions(triplet, objects, tables):
            continue  # Existing body protection owns this already blocked case.
        radius = max(22, max(18, min(72, round(4.5 * text_h)))) + tolerance
        local_objects = _semantic_geometry._nearby_regions(triplet, objects, radius)
        local_tables = _semantic_geometry._nearby_regions(triplet, tables, radius)
        candidates, distinct_join_dots = [], []
        x, y = map(round, center)
        for dx in range(-tolerance, tolerance + 1):
            for dy in range(-tolerance, tolerance + 1):
                observed = [x + dx, y + dy]
                if (not 0 <= observed[0] < raw.shape[1] or not 0 <= observed[1] < raw.shape[0]
                        or _semantic_geometry._protected_point(observed, local_objects, local_tables)):
                    continue
                axes = {'horizontal' if direction[0] else 'vertical' for direction in (incoming, outgoing)}
                hypotheses = [_semantic_geometry._underpass(raw, observed, axis, text_h) for axis in sorted(axes)]
                hypotheses.append(_corner_mixed_four_arms(raw, observed, text_h, local_objects, local_tables))
                for hypothesis in hypotheses:
                    if hypothesis and not _semantic_geometry._local_protected_regions(hypothesis, objects, tables):
                        if hypothesis['kind'] == 'junction_join':
                            distinct_join_dots.append(hypothesis)
                        else:
                            candidates.append((dx * dx + dy * dy, hypothesis))
        if distinct_join_dots:
            continue  # Do not misread the off-centre edge of a real join dot.
        if not candidates:
            continue
        # Closest coherent raw observation, not a maximum model probability.
        hypothesis = min(candidates, key=lambda item: item[0])[1]
        result = {'kind': 'raw_crossing_turn_requires_review', 'state': 'review_needed',
                  'reason': 'axis_change_at_raw_no_join_crossing', 'turn_index': index,
                  'original_corner': list(center), 'original_triplet': [list(p) for p in triplet],
                  'observed_center': list(hypothesis['center']),
                  'raster_offset': [hypothesis['center'][i] - center[i] for i in (0, 1)],
                  'raw_hypothesis': hypothesis,
                  'safety': {'geometry_is_not_acceptance': True, 'path_changed': False,
                             'original_ink_changed': False, 'same_axis_underpass_only': True,
                             'caller_must_preserve_prior_v14_acceptance': True}}
        results.append(result)
    return results


ROUTE_OPTIONS = {
    'line_only': 'Inside the marked route interval, the drawing contains line notation only: straight or elbow strokes, regular dashes, flanges, a junction, or a same-axis underpass. It does not pass through an intermediate symbol body.',
    'intervening_symbol': 'The marked route interval passes through a valve, instrument, device, equipment, or other intermediate graphical symbol body. Only the two original endpoint symbols identified by green boxes are exempt.',
    'uncertain': 'The original marks within this route interval do not establish whether it passes through an intermediate symbol body.',
}


async def review_route_contexts(extractor, ctx, objs, records, work_rels):
    """Inspect every part of a new route in overlapping original-raster windows.

    K9 already establishes supported line semantics and K10 the actual ports.
    K11 checks a narrower independent condition: an untracked symbol body must
    not be used as wire. Coverage, budgets and all paired answers are required.
    Neither window interpolation nor the guide modifies the accepted geometry.
    """
    limit = min(96, max(0, int(getattr(ctx, 'connection_semantic_route_context_budget', 96))))
    window_limit = max(0, int(getattr(ctx, 'connection_semantic_window_budget', 384)))
    items = list(records)
    stage = 'K11_semantic_route_context'
    available = window_limit
    plans = []
    for position, record in enumerate(items):
        index = record.get('index')
        rel = work_rels[index] if type(index) is int and 0 <= index < len(work_rels) else None
        path = copy.deepcopy(record.get('path', []))
        reason, windows = None, []
        if rel is None:
            reason = 'invalid_work_relation_index'
        elif position >= limit:
            reason = 'semantic_route_context_budget_exhausted'
        elif path != rel.get('path'):
            reason = 'invalid_or_mismatched_code_route_geometry'
        else:
            try:
                windows = context_windows(path, ctx.text_h, ctx.page.shape)
            except (TypeError, ValueError, IndexError):
                reason = 'invalid_or_mismatched_code_route_geometry'
        boxes = []
        if rel is not None:
            for end in ('a', 'b'):
                value = rel.get(end)
                obj = (objs[value] if type(value) is int and 0 <= value < len(objs)
                       else next((o for o in objs if o.get('id') == value), None))
                if obj is not None:
                    boxes.append({'id': obj.get('id'), 'bbox': copy.deepcopy(obj['bbox'])})
        outline_proposals = []
        if not reason:
            try:
                outline_proposals = endpoint_outline_extension_proposals(ctx.page, path, boxes, ctx.text_h)
            except (TypeError, ValueError, IndexError):
                reason = 'invalid_endpoint_outline_geometry'
            if outline_proposals:
                reason = 'endpoint_outline_extension_requires_review'
        crossing_proposals = []
        if not reason:
            try:
                crossing_proposals = raw_corner_transition_proposals(ctx.page, path,
                    objects=objs, text_h=ctx.text_h, tables=getattr(ctx, 'tables', ()))
            except (TypeError, ValueError, IndexError):
                reason = 'invalid_raw_crossing_transition_geometry'
            if crossing_proposals:
                reason = 'axis_change_at_raw_no_join_crossing'
        if not reason and len(windows) > available:
            reason = 'semantic_window_budget_exhausted'
        elif not reason:
            available -= len(windows)
        plans.append((record, rel, path, windows, boxes, reason, outline_proposals, crossing_proposals))

    async def one_window(index, window_index, window, boxes):
        names, questions, metadata = [], {}, {}
        for tag, colors in (('A', (extractor.V.RED, extractor.BLUE)),
                            ('B', (extractor.BLUE, extractor.V.RED))):
            name = f'src{index}_w{window_index}_{tag}'
            names.append(name)
            options = ROUTE_OPTIONS if tag == 'A' else dict(reversed(list(ROUTE_OPTIONS.items())))
            questions[name] = extractor.choice({
                'route_interval': extractor.Img(semantic_route_window_view(
                    extractor, ctx.page, window, boxes, colors)),
                'question': 'Inspect ONLY the marked route interval between A and B. The left panel '
                    'is a code-path guide and the right panel is the SAME original drawing without '
                    'a painted path. Read the original right panel to decide whether the guide runs '
                    'through an intermediate graphical SYMBOL BODY. A valve, instrument, device, '
                    'or equipment is a symbol body even if it was not extracted as an object. '
                    'Only the ORIGINAL endpoint symbols explicitly outlined in green are exempt; '
                    'the A/B interval markers themselves are not exempt endpoints. Regular grey '
                    'dashes, a line elbow, junction dot, aligned flange bars and a straight underpass '
                    'are line notation. Text beside the line and a perpendicular crossing line are '
                    'not intervening symbols. Consider the visible surrounding shape when a symbol '
                    'extends beyond A/B. Classify only this interval; do not judge the entire circuit '
                    'or create or repair coordinates.',
                'existing_code_path_interval': window['path'],
                'original_exempt_endpoint_symbols': boxes,
            }, options)
            metadata[name] = {'candidate_index': index, 'window_index': window_index,
                **copy.deepcopy(window), 'options': list(options),
                'coordinates_generated_by': 'code_interpolation_of_unchanged_existing_path',
                'exempt_endpoint_symbols': copy.deepcopy(boxes)}
        failure = None
        try:
            answer = await ctx.jev.ask_chunked(stage,
                {'task': 'Identify intermediate symbol bodies on one marked original route interval.'},
                questions, metadata)
        except Exception as error:
            if getattr(ctx.jev, 'fatal', None) or type(error).__name__ == 'Fatal':
                raise
            answer, failure = {}, type(error).__name__
        distributions = [answer.get(n) for n in names] if isinstance(answer, dict) else [None, None]
        meaning, confidence = paired_category(distributions, ROUTE_OPTIONS, .60)
        return {**copy.deepcopy(window), 'question_names': names,
            'raw_distributions': copy.deepcopy(distributions), 'meaning': meaning,
            'confidence': confidence, **({'failure_type': failure} if failure else {})}

    async def one_route(plan):
        record, rel, path, windows, boxes, reason, outline_proposals, crossing_proposals = plan
        index = record.get('index')
        results = await asyncio.gather(*(one_window(index, i, window, boxes)
                        for i, window in enumerate(windows))) if not reason and windows else []
        if reason:
            state, meaning, confidence = 'review_needed', None, None
            reasons = [reason]
        elif any(r['meaning'] == 'intervening_symbol' for r in results):
            state, meaning, confidence = 'rejected', 'intervening_symbol', None
            reasons = ['original_route_interval_intervening_symbol']
        elif not results or any(r['meaning'] != 'line_only' for r in results):
            state, meaning, confidence = 'review_needed', None, None
            reasons = ['original_route_interval_unresolved']
        else:
            state, meaning = 'confirmed', 'line_only'
            confidence = min(r['confidence'] for r in results)
            reasons = ['all_overlapping_original_route_intervals_clear']
        result = {'stage': stage, 'question_names': [n for r in results for n in r['question_names']],
            'raw_distributions': [r['raw_distributions'] for r in results],
            'meaning': meaning, 'confidence': confidence, 'path': path,
            'state': state, 'accepted': state == 'confirmed', 'reasons': reasons,
            'pre_context_state': record.get('state'),
            'pre_context_reasons': copy.deepcopy(record.get('reasons', [])),
            'windows': results, 'required_windows': len(windows),
            'outline_extension_hypotheses': copy.deepcopy(outline_proposals),
            'crossing_transition_hypotheses': copy.deepcopy(crossing_proposals),
            'coverage_complete': bool(windows) and len(results) == len(windows),
            'safety': {'coordinates_source': 'existing_code_created_route_only',
                'geometry_changed': False, 'guide_is_geometry_evidence': False,
                'original_context_source': 'unpainted_original_raster_panel',
                'previous_v14_accepted_routes': 'excluded_by_caller',
                'intermediate_symbol_body': 'never_traverse_even_if_not_in_object_list',
                'endpoint_exemptions': boxes,
                'interval_markers_are_endpoint_exemptions': False,
                'crossing_axes': 'K9 same_axis_only; never_union_axes',
                'all_overlapping_intervals_required': True,
                'endpoint_outline_extension_policy': 'review_needed_even_if_local_model_says_line_only',
                'crossing_transition_policy': 'review_needed_on_raw_unjoined_axis_change_even_if_old_entity_confirmed',
                'paired_same_winner_required': True, 'paired_average_threshold': .60,
                'paired_minimum_threshold': .50, 'finite_options': list(ROUTE_OPTIONS),
                'colour_orders': 2}}
        record['semantic_route_context'] = result
        record.update(state=state, reasons=reasons)
        if rel is not None:
            rel['semantic_route_context'] = copy.deepcopy(result)
            rel['semantic_route_context_confidence'] = confidence
            rel.update(shared_graph_state=state, shared_graph_reasons=list(reasons))
        if state != 'confirmed':
            record['accepted'] = False
            if rel is not None:
                rel.setdefault('pre_semantic_route_context_decision', rel.get('decision'))
                rel.update(accepted=False, confidence=None,
                           decision='semantic_route_context_' + (meaning or 'unresolved'))
        return result

    results = await asyncio.gather(*(one_route(plan) for plan in plans)) if plans else []
    return {'stage': stage, 'route_review_limit': limit, 'window_review_limit': window_limit,
        'eligible_routes': len(items), 'reviewed_routes': sum(bool(r['question_names']) for r in results),
        'reviewed_windows': sum(len(r['windows']) for r in results),
        'confirmed_routes': sum(r['state'] == 'confirmed' for r in results),
        'rejected_routes': sum(r['state'] == 'rejected' for r in results),
        'review_needed_routes': sum(r['state'] == 'review_needed' for r in results),
        'crossing_deferred_routes': sum('axis_change_at_raw_no_join_crossing' in r['reasons'] for r in results),
        'outline_deferred_routes': sum('endpoint_outline_extension_requires_review' in r['reasons'] for r in results),
        'budget_deferred_routes': sum(any('budget_exhausted' in s for s in r['reasons']) for r in results)}

def _accept_route(registry, record, rel):
    rel.setdefault('pre_semantic_decision', rel.get('decision'))
    rel.update(accepted=True, decision='semantic_drawing_route_with_actual_ports',
               confidence=min([registry[i]['confidence'] for i in record['entity_ids']] +
                              [record['semantic_route_context']['confidence']]),
               local_confidence=min(registry[i]['confidence'] for i in record['entity_ids']
                                    if registry[i]['kind'] != 'attachment'),
               endpoint_confidence=min(registry[i]['confidence'] for i in record['attachment_ids']),
               semantic_entity_ids=[i for i in record['entity_ids'] if registry[i].get('semantic_interpretation')])
    record['accepted'] = True


async def verify_drawing_semantics(extractor, ctx, objs, rels):
    if getattr(ctx, '_drawing_semantics_verified', False):
        return graph.export_graph(ctx)
    current = getattr(ctx, 'connection_graph', None)
    if getattr(ctx, 'kind', None) != 'pid' or not current:
        return graph.export_graph(ctx)
    registry = {e['id']: e for e in current['entities']}
    records = current['candidate_routes'] + current.get('alternative_routes', [])
    routes = {r['index']: r for r in records}
    work_rels, alternatives = graph._expand_alternatives(objs, rels)
    eligible = set()
    for record in records:
        index = record['index']
        parent = record.get('parent_index', index)
        if index >= len(work_rels) or rels[parent].get('accepted'):
            continue
        if graph._eligible(extractor, ctx, objs, work_rels[index], record):
            eligible.add(index)
    needed = {identity for i in eligible for identity in routes[i]['entity_ids']}
    analyses = []
    for entity in registry.values():
        if entity['id'] not in needed or entity['state'] == 'confirmed' or entity['kind'] == 'attachment':
            continue
        analysis = analyze_entity(ctx.page, entity, objects=objs, text_h=ctx.text_h,
                                  tables=getattr(ctx, 'tables', ()))
        entity['semantic_geometry'] = analysis
        if analysis.get('eligible') and any(h.get('kind') != 'unresolved_break' for h in analysis.get('hypotheses', [])):
            analyses.append((entity, analysis))
    key = lambda entity: _priority(entity, routes, registry, work_rels, eligible)
    line_limit = max(0, int(getattr(ctx, 'connection_semantic_line_budget', MAX_LINE_REVIEWS)))
    analyses.sort(key=lambda item: key(item[0]))
    selected = analyses[:line_limit]
    await _review_lines(extractor, ctx, selected)

    # Ports are checked independently: an uncertain upstream dash or junction
    # must not suppress the opportunity to observe the real body contact.
    ports = [e for e in registry.values() if e['id'] in needed and e['kind'] == 'attachment'
             and e['state'] != 'confirmed' and e.get('detail', {}).get('contact_geometry_status') == 'observed']
    competing = graph.competing_attachment_groups(ports, ctx.text_h)
    competing_ids = {e['id'] for group in competing for e in group}
    # Existing categorical arm-selection remains the authority for competing
    # parallel arms; two independent yes/no queries must not accept both.
    ports = sorted((e for e in ports if e['id'] not in competing_ids), key=key)
    port_limit = max(0, int(getattr(ctx, 'connection_semantic_port_budget', MAX_PORT_REVIEWS)))
    selected_ports = ports[:port_limit]
    await _review_ports(extractor, ctx, selected_ports)
    recovered = 0
    ready = []
    for record in records:
        index = record['index']
        if index not in eligible:
            continue
        state, reasons = graph._route_state(registry, record)
        record.update(state=state, reasons=reasons)
        rel = work_rels[index]
        rel.update(shared_graph_state=state, shared_graph_reasons=reasons)
        if state == 'confirmed' and not rel.get('accepted'):
            ready.append(record)
    route_context_summary = await review_route_contexts(extractor, ctx, objs, ready, work_rels)
    for record in ready:
        index = record['index']
        rel = work_rels[index]
        if record['state'] == 'confirmed':
            _accept_route(registry, record, rel)
            recovered += 1
    geometry_fields = {'a', 'b', 'a_side', 'b_side', 'a_point', 'b_point', 'a_anchor', 'b_anchor',
        'path', 'net', 'length', 'bridges', 'dashed', 'mst', 'tee_gaps', 'signal_gaps',
        'endpoint_contacts', 'net_attachment_source', 'same_original_label_net',
        'crossing_details', 'graph_id', 'candidate_source', 'net_rank', 'checkpoint_keys'}
    alternative_recoveries = 0
    for parent_index, indices in alternatives.items():
        primary = rels[parent_index]
        for index in indices:
            record = routes[index]
            target = primary['route_alternatives'][record['alternative_index']]
            target.update(shared_graph_state=record['state'], shared_graph_reasons=record['reasons'],
                          shared_graph_accepted=bool(work_rels[index].get('accepted')))
        if primary.get('accepted'):
            continue
        chosen = next((i for i in indices if i in eligible and work_rels[i].get('accepted')), None)
        if chosen is None:
            continue
        alternative, record = work_rels[chosen], routes[chosen]
        primary['pre_semantic_route'] = {k: copy.deepcopy(primary[k]) for k in geometry_fields if k in primary}
        for k in geometry_fields:
            if k in alternative:
                primary[k] = copy.deepcopy(alternative[k])
            elif k in {'tee_gaps', 'signal_gaps', 'endpoint_contacts', 'crossing_details', 'checkpoint_keys'}:
                primary[k] = {} if k == 'endpoint_contacts' else []
        primary.update(accepted=True, decision='semantic_drawing_alternative_with_actual_ports',
                       confidence=alternative['confidence'], local_confidence=alternative['local_confidence'],
                       endpoint_confidence=alternative['endpoint_confidence'],
                       semantic_entity_ids=alternative.get('semantic_entity_ids', []),
                       semantic_route_context=copy.deepcopy(alternative['semantic_route_context']),
                       shared_graph_entity_ids=list(record['entity_ids']), shared_graph_state='confirmed',
                       shared_graph_reasons=list(record['reasons']),
                       selected_semantic_alternative_index=record['alternative_index'])
        routes[parent_index]['pre_semantic_graph_path'] = copy.deepcopy(routes[parent_index]['path'])
        routes[parent_index]['pre_semantic_graph_entity_ids'] = list(routes[parent_index]['entity_ids'])
        routes[parent_index].update(state='confirmed', accepted=True,
            reasons=['fully_confirmed_semantic_alternative_selected'],
            path=copy.deepcopy(record['path']), net=record.get('net'),
            entity_ids=list(record['entity_ids']), attachment_ids=list(record['attachment_ids']),
            semantic_route_context=copy.deepcopy(record['semantic_route_context']),
            selected_semantic_alternative_index=record['alternative_index'])
        alternative_recoveries += 1
    current['revision'] = REVISION
    current['policy']['drawing_semantics'] = {
        'line_options': list(LINE_OPTIONS), 'port_options': list(PORT_OPTIONS),
        'paired_category_threshold': .60, 'colour_orders': 2,
        'crossing_axes': 'never_union; underpass allows existing opposite-axis continuation only',
        'port_schedule': 'independent_of_upstream_confirmation',
        'new_route_context': 'all_overlapping_original_intervals_paired_line_only_required',
        'endpoint_outline_extension': 'observed_closed_extension_followed_by_new_route_requires_review',
        'raw_crossing_turn': 'all_new_routes_recheck_mixed_solid_and_regular_dashed_four_arms_no_dot',
        'line_review_limit': line_limit, 'port_review_limit': port_limit}
    current['summary'].update(
        semantic_route_context=route_context_summary,
        semantic_line_reviews=len(selected), semantic_port_reviews=len(selected_ports),
        semantic_confirmed_entities=sum(e.get('semantic_interpretation') is not None and e['state']=='confirmed' for e in registry.values()),
        semantic_recovered_primary_pairs=sum(r.get('decision') in {'semantic_drawing_route_with_actual_ports', 'semantic_drawing_alternative_with_actual_ports'} for r in rels),
        semantic_recovered_alternatives=alternative_recoveries,
        confirmed_entities=sum(e['state']=='confirmed' for e in registry.values()),
        review_needed_entities=sum(e['state']=='review_needed' for e in registry.values()),
        rejected_entities=sum(e['state']=='rejected' for e in registry.values()),
        review_needed_candidates=sum(r['state']=='review_needed' for r in current['candidate_routes']),
        review_needed_alternatives=sum(r['state']=='review_needed' for r in current.get('alternative_routes', [])))
    ctx._drawing_semantics_verified = True
    return graph.export_graph(ctx)
