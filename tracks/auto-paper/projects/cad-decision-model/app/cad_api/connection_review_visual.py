"""Readable review overlay; the full candidate and raw-end ledger stays intact."""
from __future__ import annotations

import copy
import hashlib
import json
import math
from pathlib import Path

import cv2

from .connection_revision import render_review


def visualization_subset(review, objects=(), image=None):
    selected = copy.deepcopy(review)
    text_boxes = [o['bbox'] for o in objects if o.get('class') == 'text']
    def in_text(point):
        return point is not None and any(b[0]-2 <= point[0] <= b[2]+2 and b[1]-2 <= point[1] <= b[3]+2
                                         for b in text_boxes)
    needed = {identity for c in review.get('candidates', []) + review.get('alternative_candidates', [])
              if c.get('state') == 'review_needed' for identity in c.get('evidence', {}).get('entity_ids',
                  c.get('evidence', {}).get('graph', {}).get('entity_ids', []))}
    ports = []
    for entity in review.get('graph', {}).get('entities', []):
        if entity.get('kind') != 'attachment' or entity.get('state') != 'review_needed' or entity.get('id') not in needed:
            continue
        geometry = entity.get('geometry', {})
        point = geometry.get('point')
        if point is None or in_text(point):
            continue
        port = {'object': geometry.get('object'), 'side': geometry.get('side'), 'point': point, 'state': 'review_needed'}
        # Merge only displayed markers. No physical ports or data are merged.
        if any(old.get('object') == port.get('object') and old.get('side') == port.get('side')
               and math.dist(old.get('point', old.get('anchor')), point) <= 8 for old in ports):
            continue
        ports.append(port)
    grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if image is not None and image.ndim == 3 else image
    for port in review.get('coverage', {}).get('ports', []):
        if port.get('state') != 'review_needed' or port.get('candidate_ids') or grey is None:
            continue
        anchor = port.get('anchor', port.get('point'))
        direction = {'left': (-1, 0), 'right': (1, 0), 'top': (0, -1), 'bottom': (0, 1)}.get(port.get('side'))
        if anchor is None or direction is None or in_text(anchor):
            continue
        evidence = 0
        for distance in range(1, 25):
            x, y = round(anchor[0]+direction[0]*distance), round(anchor[1]+direction[1]*distance)
            if 1 <= x < grey.shape[1]-1 and 1 <= y < grey.shape[0]-1 and not in_text([x, y]):
                evidence += int((grey[y-1:y+2, x-1:x+2] < 220).any())
        if evidence < 10:
            continue
        point = port.get('point', anchor)
        if not any(old.get('object') == port.get('object') and old.get('side') == port.get('side')
                   and math.dist(old['point'], point) <= 8 for old in ports):
            ports.append(port)
    ends = [end for end in review.get('coverage', {}).get('line_ends', [])
            if end.get('state') == 'review_needed' and end.get('reason') == 'unaccounted_line_end'
            and not in_text(end.get('point'))]
    selected.setdefault('coverage', {})['ports'] = ports
    selected['coverage']['line_ends'] = ends
    # The caption describes visible marker groups, while the public summary
    # retains every unresolved raw port observation.
    selected.setdefault('summary', {})['unresolved_ports'] = len(ports)
    return selected


def write_readable_review(directory, review, objects=None):
    directory = Path(directory)
    if objects is None:
        saved = directory / 'input_output.json'
        objects = json.loads(saved.read_text()).get('objects', []) if saved.exists() else []
    image = cv2.imread(str(directory / 'input.png'), cv2.IMREAD_COLOR)
    selected = visualization_subset(review, objects, image)
    # A regular dash/flange bridge endpoint is a raw stroke endpoint rather
    # than an open logical wire. The candidate path shows the uncertain bridge.
    # Raw endpoints and their states remain in input_review.json.
    render_review(directory / 'input.png', selected, directory / 'input_review.png')
    review['visualization'] = {
        'renderer_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'policy': 'Pending routes and related physical attachments; isolated raw ports require an outward ink arm. '
                  'Text glyph ends and regular dash/bridge endpoints are omitted from the overlay but remain in the JSON ledger.',
        'displayed_port_marker_groups': len(selected['coverage']['ports']),
        'displayed_unaccounted_end_markers': len(selected['coverage']['line_ends']),
        'raw_end_records': len(review.get('coverage', {}).get('line_ends', [])),
    }
    (directory / 'input_review.json').write_text(json.dumps(review, ensure_ascii=False, indent=2, allow_nan=False))
    return review
