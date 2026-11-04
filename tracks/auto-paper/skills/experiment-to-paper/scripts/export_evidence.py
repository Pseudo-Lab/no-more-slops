#!/usr/bin/env python3
"""Transcribe selected saved JSON measurements and hash their inputs; no inference."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
import tempfile
import shutil


def read_input(root, relative):
    if not isinstance(relative, str) or Path(relative).is_absolute():
        raise ValueError('Input paths must be relative to --root')
    path = (root / relative).resolve()
    if not path.is_relative_to(root) or not path.is_file():
        raise ValueError(f'Input must be a file inside --root: {relative}')
    return path


def select(value, pointer):
    if not isinstance(pointer, str) or (pointer and not pointer.startswith('/')):
        raise ValueError('Use an RFC 6901 JSON pointer, or an empty pointer for the root')
    for token in pointer.split('/')[1:] if pointer else []:
        if re.search(r'~(?![01])', token):
            raise ValueError('Invalid JSON pointer escape')
        token = token.replace('~1', '/').replace('~0', '~')
        if isinstance(value, list):
            if not re.fullmatch(r'0|[1-9][0-9]*', token):
                raise ValueError('Invalid array index')
            value = value[int(token)]
        elif isinstance(value, dict):
            value = value[token]
        else:
            raise ValueError('Pointer traverses a scalar')
    return value


def export(root, spec_relative, out):
    root, out = Path(root).resolve(), Path(out).resolve()
    spec_path = read_input(root, spec_relative)
    raw_inputs = {spec_relative: spec_path.read_bytes()}
    spec = json.loads(raw_inputs[spec_relative])
    if not isinstance(spec, dict) or type(spec.get('schema_version')) is not int or spec['schema_version'] != 1 or not isinstance(spec.get('measurements'), list) or not spec['measurements']:
        raise ValueError('Spec needs schema_version 1 and a nonempty measurements list')
    rows, ids = [], set()
    for entry in spec['measurements']:
        if not isinstance(entry, dict):
            raise ValueError('Each measurement must be an object')
        key = entry['id']
        if not isinstance(key, str) or not re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9_.-]*', key) or key in ids:
            raise ValueError('Measurement IDs must be unique simple identifiers')
        ids.add(key)
        unit = entry['unit']
        if not isinstance(unit, str) or not unit.strip() or any(c in unit for c in '|\r\n'):
            raise ValueError('Supply a single-line unit without table delimiters')
        source = read_input(root, entry['file'])
        raw_inputs.setdefault(entry['file'], source.read_bytes())
        value = select(json.loads(raw_inputs[entry['file']]), entry['pointer'])
        if value is not None and (type(value) not in (int, float) or not math.isfinite(value)):
            raise ValueError(f'{key}: expected a finite number or null')
        denominator = entry.get('denominator')
        if denominator is not None and (type(denominator) is not int or denominator <= 0):
            raise ValueError('Denominator must be a positive integer or null')
        rows.append({'id': key, 'value': value, 'unit': unit, 'denominator': denominator,
                     'source': {'file': entry['file'], 'pointer': entry['pointer']},
                     'status': 'unavailable' if value is None else 'saved_measurement'})
    try:
        revision = subprocess.run(['git', '-C', str(root), 'rev-parse', 'HEAD'],
                                  capture_output=True, text=True)
        snapshot_revision = revision.stdout.strip() if revision.returncode == 0 else None
    except FileNotFoundError:
        snapshot_revision = None
    manifest = {'schema_version': 1, 'snapshot_revision': snapshot_revision,
                'execution_revision': None, 'spec': spec_relative,
                'scope': 'Saved JSON transcription and input hashes; no aggregate recomputation, inference or claim validation',
                'inputs': {name: {'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)}
                           for name, data in sorted(raw_inputs.items())}}
    measurements = {'schema_version': 1, 'measurements': rows,
                    'denominator_provenance': 'Specified by the caller; not independently validated'}
    table = ['| Measurement | Value | Unit | Denominator |', '| --- | --- | --- | --- |']
    for row in rows:
        value = 'unavailable' if row['value'] is None else str(row['value'])
        n = 'unknown' if row['denominator'] is None else str(row['denominator'])
        table.append(f"| {row['id']} | {value} | {row['unit']} | {n} |")
    if out.exists():
        raise ValueError('Output already exists; inspect it and choose a fresh output directory')
    # Validate everything before publishing a complete, new output directory.
    out.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix='.evidence-export-', dir=out.parent))
    try:
        (stage / 'evidence').mkdir()
        (stage / 'tables').mkdir()
        for name, data in [('manifest', manifest), ('measurements', measurements)]:
            (stage / 'evidence' / f'{name}.json').write_text(json.dumps(data, indent=2, ensure_ascii=False, allow_nan=False) + '\n', encoding='utf-8')
        (stage / 'tables/measurements.md').write_text('\n'.join(table) + '\n', encoding='utf-8')
        stage.rename(out)
    finally:
        if stage.exists():
            shutil.rmtree(stage)
    return {'output': str(out), 'measurements': len(rows), 'input_files': len(raw_inputs), 'scope': manifest['scope']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--spec', required=True, help='JSON specification relative to --root')
    parser.add_argument('--out', type=Path, required=True, help='A new output directory')
    args = parser.parse_args()
    try:
        print(json.dumps(export(args.root, args.spec, args.out), ensure_ascii=False))
    except (ValueError, KeyError, IndexError, TypeError, OSError) as exc:
        parser.exit(1, f'Evidence export failed: {exc}\n')


if __name__ == '__main__':
    main()
