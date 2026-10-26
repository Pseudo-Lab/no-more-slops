from __future__ import annotations

import asyncio
import fcntl
import hashlib
import importlib
import json
import math
import os
import sys
import threading
from pathlib import Path

from .config import PACKAGE_ROOT
from .decision import create_decision_client
from .jobs import ARTIFACTS


def start_parent_watchdog(api_pid: int) -> threading.Event:
    """Stop model work if an API crash or SIGKILL bypasses normal shutdown."""
    stopped = threading.Event()

    def watch():
        while not stopped.is_set():
            if os.getppid() != api_pid:
                # Exit also releases a blocking cache flock and active sockets.
                os._exit(4)
            stopped.wait(.25)

    threading.Thread(target=watch, name='api-parent-watchdog', daemon=True).start()
    return stopped


def valid_cache_entry(path: Path) -> bool:
    try:
        entry = json.loads(path.read_text())
        if not isinstance(entry, dict) or not isinstance(entry.get('model'), str) or 'answer' not in entry:
            return False
        answer = entry['answer']
        probability = lambda p: type(p) in (int, float) and math.isfinite(p) and 0 <= p <= 1
        if isinstance(answer, dict):
            return bool(answer) and all(isinstance(k, str) and probability(v) for k, v in answer.items()) and abs(sum(answer.values()) - 1) <= .02000000001
        return probability(answer)
    except (ValueError, OSError, TypeError):
        return False


async def extract(spec: dict) -> int:
    directory = Path(spec['job_dir'])
    resources = Path(spec['resources_dir'])
    source = PACKAGE_ROOT / 'vendor' / 'v12'
    manifest = json.loads((PACKAGE_ROOT / 'vendor' / 'freeze.json').read_text())
    for name, expected in manifest['source_files'].items():
        if hashlib.sha256((source / name).read_bytes()).hexdigest() != expected:
            raise ValueError('Frozen source digest mismatch')
    sys.path.insert(0, str(source))
    extractor = importlib.import_module('run_page')

    revision = spec.get('algorithm_revision', manifest['revision'])
    if revision == 'geometry-local-route-v13-connections':
        from .connection_recovery import install
        install(extractor)
    elif revision == 'geometry-local-route-v14-graph':
        from .connection_revision import install
        install(extractor)
    elif revision == 'geometry-local-route-v15-semantics':
        from .connection_revision_v15 import install
        install(extractor)
    elif revision != manifest['revision']:
        raise ValueError('Unsupported extraction revision')
    supplemental_start = None
    if revision == 'geometry-local-route-v14-graph':
        from .connection_revision import source_hashes
        supplemental_start = source_hashes()
    elif revision == 'geometry-local-route-v15-semantics':
        from .connection_revision_v15 import source_hashes
        supplemental_start = source_hashes()

    # v12 stays byte-for-byte frozen. A versioned connection supplement is installed
    # only in this process and keeps all object stages and decision thresholds.
    client = create_decision_client(spec['backend'])
    import typesafe_sdk
    typesafe_sdk.AsyncTypeSafeClient = lambda **kwargs: client
    extractor.load_env = lambda path: None
    os.environ.setdefault('TYPESAFE_API_KEY', 'worker-client-injected')
    extractor.ROOT = directory
    extractor.HERE = resources / 'experiments'
    extractor.VZ.ROOT = directory
    extractor.REQ_TOKENS = spec['backend']['max_request_tokens']

    def legend_loader(name):
        if spec.get('legend'):
            data = spec['legend']
        else:
            data = json.loads((resources / 'experiments' / name).read_text())
        pages, choices = {}, {}
        for entry in data['classes']:
            if entry.get('crop'):
                filename = entry.get('page') or data.get('legend_page')
                image = (resources / 'image' / filename).resolve()
                if not image.is_relative_to((resources / 'image').resolve()):
                    raise ValueError('Invalid legend resource')
                if filename not in pages:
                    pages[filename] = extractor.V.load_page(image)
                choices[entry['key']] = {'description': entry['text'], 'example': extractor.Img(extractor.exemplar_view(pages[filename], entry['crop']))}
            else:
                choices[entry['key']] = entry['text']
        return choices

    extractor.load_legend = legend_loader
    cache = Path(spec['cache_dir'])
    cache.mkdir(parents=True, exist_ok=True)
    (directory / '.cache').mkdir(exist_ok=True)
    (directory / '.cache' / 'jev').symlink_to(cache, target_is_directory=True)
    # Frozen cache writes are not atomic. Serialize jobs sharing a backend
    # namespace; other backends still run in independent worker processes.
    cache_lock = (cache / 'cache.lock').open('a')
    fcntl.flock(cache_lock, fcntl.LOCK_EX)
    original_cache_path = extractor.Jev._cache_path

    def checked_cache_path(jev, key):
        path = original_cache_path(jev, key)
        # A killed frozen write may leave truncated JSON. Re-query only that
        # corrupt entry instead of letting it break every future extraction.
        if path.exists() and not valid_cache_entry(path):
            path.unlink()
        return path

    extractor.Jev._cache_path = checked_cache_path
    try:
        code = await extractor.main([str(directory / 'input.png'), '--kind', spec['kind'], '--model', spec['backend']['model'],
                                     '--concurrency', str(spec['backend']['concurrency']), '--refine', 'compare',
                                     '--gt', str(directory / '_no_ground_truth.json'), '--out', str(directory)])
    finally:
        await client.close()
        fcntl.flock(cache_lock, fcntl.LOCK_UN)
        cache_lock.close()
    if code:
        (directory / '_worker_error.json').write_text(json.dumps({'code': 'extraction_failed', 'message': 'The extractor stopped. Check the configured Decision Model service and credentials.'}))
        return code
    if supplemental_start is not None and source_hashes() != supplemental_start:
        raise ValueError('Connection source changed during extraction')
    output_path = directory / 'input_output.json'
    trace_path = directory / 'input_trace.json'
    output = json.loads(output_path.read_text())
    trace = json.loads(trace_path.read_text())
    stats = trace.get('jev', {})
    errors = sum(record.get('errors', 0) for record in stats.values())
    service = {'job_id': spec['job_id'], 'backend_id': spec['backend']['id'], 'provider': spec['backend']['provider'],
               'configured_model': spec['backend']['model'], 'algorithm_revision': revision,
               'original_filename': spec['original_filename'], 'input_sha256': spec['input_sha256'],
               'normalized_input_sha256': spec['normalized_input_sha256']}
    output['meta']['api'] = service
    trace['api'] = service
    if revision != manifest['revision']:
        source_names = ('connection_recovery.py', 'connection_candidates.py', 'terminal_dash.py', 'route_context_geometry.py')
        if revision == 'geometry-local-route-v14-graph':
            from .connection_revision import SOURCE_FILES
            source_names = SOURCE_FILES
        elif revision == 'geometry-local-route-v15-semantics':
            from .connection_revision_v15 import SOURCE_FILES
            source_names = SOURCE_FILES
        supplements = supplemental_start or {name: hashlib.sha256((PACKAGE_ROOT / name).read_bytes()).hexdigest() for name in source_names}
        output['meta'].update(algorithm_revision=revision, baseline_revision=manifest['revision'], supplement_hashes=supplements)
        output['meta']['relation_note'] += ' Versioned connection checks require traced route and attachment evidence; review-needed candidates do not count as confirmed relations.'
        trace.update(algorithm_revision=revision, baseline_revision=manifest['revision'], supplement_hashes=supplements)
        stage = getattr(extractor, '_last_connection_stage', None)
        if stage:
            ctx, objs, relations = stage
            extras = {tuple(sorted((objs[r['a']]['id'], objs[r['b']]['id']))): r for r in relations}
            fields = ('candidate_source', 'candidate_net_source', 'net_attachment_source',
                      'same_original_label_net', 'context_review_keys', 'context_endpoint_keys',
                      'backup_endpoint_keys', 'deferred_endpoint_checkpoint_keys', 'baseline_decision',
                      'shared_graph_entity_ids', 'shared_graph_state', 'shared_graph_reasons',
                      'pre_graph_decision', 'pre_graph_route', 'selected_graph_alternative_index', 'route_alternatives',
                      'semantic_entity_ids', 'pre_semantic_decision', 'pre_semantic_route', 'selected_semantic_alternative_index',
                      'semantic_route_context')
            for rel in trace['relation_candidates']:
                source_rel = extras[tuple(sorted((rel['a'], rel['b'])))]
                rel.update({key: source_rel[key] for key in fields if key in source_rel})
            for rel in output['relations']:
                if rel['type'] == 'connected':
                    source_rel = extras[tuple(sorted((rel['a'], rel['b'])))]
                    rel['evidence'].update({key: source_rel[key] for key in fields if key in source_rel})
            trace['connection_candidate_supplement'] = getattr(ctx, 'connection_candidate_supplement', {})
            if revision in {'geometry-local-route-v14-graph', 'geometry-local-route-v15-semantics'}:
                if revision == 'geometry-local-route-v15-semantics':
                    from .connection_revision_v15 import write_review_artifacts
                else:
                    from .connection_revision import write_review_artifacts
                from .connection_review_visual import write_readable_review
                review = write_review_artifacts(directory, ctx, objs, relations)
                write_readable_review(directory, review, output['objects'])
                output['connection_review'] = review
                trace['connection_review'] = review
                output['meta']['previous_connection_revision'] = 'geometry-local-route-v13-connections'
                output['meta']['pipeline'] = output['meta']['pipeline'].replace(
                    ' → T1/T2', ' → v13 route recovery → K7 shared physical segments/junctions/gaps → K8 actual ports/alternative routes → T1/T2')
                if revision == 'geometry-local-route-v15-semantics':
                    output['meta']['previous_connection_revision'] = 'geometry-local-route-v14-graph'
                    output['meta']['pipeline'] = output['meta']['pipeline'].replace(
                        ' → T1/T2', ' → K9 drawing notation semantics → K10 independent actual port semantics → K11 overlapping original-route windows → T1/T2')
    output_path.write_text(json.dumps(output, ensure_ascii=False, indent=2))
    trace_path.write_text(json.dumps(trace, ensure_ascii=False, indent=2))
    if errors:
        (directory / '_worker_error.json').write_text(json.dumps({'code': 'decision_model_error', 'message': 'One or more Decision Model requests failed. Partial trace is available; submit a new job after correcting the backend.'}))
        return 3
    summary = {'symbols': sum(o.get('class') != 'text' for o in output['objects']),
               'text_regions': sum(o.get('class') == 'text' for o in output['objects']),
               'connections': sum(r['type'] == 'connected' for r in output['relations']),
               'review_needed_candidates': output.get('connection_review', {}).get('summary', {}).get('review_needed_candidates', 0),
               'unresolved_ports': output.get('connection_review', {}).get('summary', {}).get('unresolved_ports', 0),
               'containments': sum(r['type'] == 'inside' for r in output['relations']),
               'model': output['meta']['model'], 'model_requests': sum(s.get('requests', 0) for s in stats.values()),
               'cached_questions': sum(s.get('cached', 0) for s in stats.values()),
               'artifacts': sorted(name for name in ARTIFACTS if (directory / name).is_file())}
    (directory / '_worker_result.json').write_text(json.dumps(summary))
    return 0


def main() -> int:
    spec = json.loads(Path(sys.argv[1]).read_text())
    api_pid = spec.get('api_pid')
    if type(api_pid) is not int or api_pid != os.getppid():
        return 4
    stopped = start_parent_watchdog(api_pid)
    try:
        return asyncio.run(extract(spec))
    except Exception:
        (Path(spec['job_dir']) / '_worker_error.json').write_text(json.dumps({'code': 'worker_failed', 'message': 'The extraction worker failed. Verify backend configuration and bundled resources.'}))
        return 1
    finally:
        stopped.set()


if __name__ == '__main__':
    raise SystemExit(main())
