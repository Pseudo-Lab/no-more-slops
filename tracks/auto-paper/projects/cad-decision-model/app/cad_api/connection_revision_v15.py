"""Drawing-notation extension; v12/v13/v14 sources remain selectable unchanged."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from . import connection_revision as previous

REVISION = 'geometry-local-route-v15-semantics'
BASELINE = previous.BASELINE
PREVIOUS = previous.REVISION
SOURCE_FILES = previous.SOURCE_FILES + ('connection_semantic_geometry.py', 'connection_semantics.py', 'connection_revision_v15.py')


def source_hashes():
    root = Path(__file__).resolve().parent
    return {name: hashlib.sha256((root/name).read_bytes()).hexdigest() for name in SOURCE_FILES}


def install(extractor):
    if getattr(extractor, '_connection_revision', None) == REVISION:
        return
    previous.install(extractor)
    previous_verify = extractor.stage_verify
    from .connection_semantics import verify_drawing_semantics

    async def verify(ctx, objs, rels):
        await previous_verify(ctx, objs, rels)
        await verify_drawing_semantics(extractor, ctx, objs, rels)
        extractor._last_connection_stage = (ctx, objs, rels)

    extractor.stage_verify = verify
    extractor._connection_revision = REVISION


def review_output(ctx, objs, rels):
    review = previous.review_output(ctx, objs, rels)
    review['algorithm_revision'] = REVISION
    review['previous_connection_revision'] = PREVIOUS
    return review


def write_review_artifacts(directory, ctx, objs, rels):
    directory = Path(directory)
    review = review_output(ctx, objs, rels)
    (directory/'input_review.json').write_text(json.dumps(review, ensure_ascii=False, indent=2, allow_nan=False))
    previous.render_review(directory/'input.png', review, directory/'input_review.png')
    return review
