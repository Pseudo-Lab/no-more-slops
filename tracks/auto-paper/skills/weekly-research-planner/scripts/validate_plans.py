#!/usr/bin/env python3
"""Validate seven daily execution contracts without dependencies or file writes."""
import argparse
import json
import re
import sys
from pathlib import Path, PurePosixPath


def read_contract(path):
    text = path.read_text(encoding='utf-8')
    blocks = re.findall(r'^```research-plan[^\S\n]*\n(.*?)^```[^\S\n]*$', text, re.M | re.S)
    if len(blocks) != 1:
        raise ValueError('exactly one research-plan JSON block is required')
    obj = json.loads(blocks[0])
    if not isinstance(obj, dict):
        raise ValueError('contract must be a JSON object')
    return obj


def relative_artifact(value):
    if not isinstance(value, str) or not value or '\\' in value:
        return False
    p = PurePosixPath(value)
    return not p.is_absolute() and '..' not in p.parts and ':' not in value


def validate(folder, week):
    errors = []
    paths = [folder / f'{week}w{day}day.md' for day in range(1, 8)]
    actual, expected = set(folder.glob('*.md')), set(paths)
    if actual != expected:
        errors.append('expected exactly seven named MD files; missing=' +
                      str(sorted(p.name for p in expected - actual)) +
                      '; extra=' + str(sorted(p.name for p in actual - expected)))
    common_paths, earlier_outputs, root_missing = None, set(), False
    for day, path in enumerate(paths, 1):
        if not path.is_file():
            continue
        prefix = path.name + ': '
        try:
            obj = read_contract(path)
        except (OSError, UnicodeError, ValueError) as exc:
            errors.append(prefix + str(exc))
            continue
        if type(obj.get('week')) is not int or obj['week'] != week:
            errors.append(prefix + 'week must match the filename')
        if type(obj.get('day')) is not int or obj['day'] != day:
            errors.append(prefix + 'day must match the filename')
        root, previous = obj.get('work_root'), obj.get('previous_materials')
        if not isinstance(root, str):
            errors.append(prefix + 'work_root must be a string (empty if absent)')
        if not isinstance(previous, list) or any(not isinstance(x, str) or not x.strip() for x in previous):
            errors.append(prefix + 'previous_materials must be a list of nonempty path strings')
        this_paths = (root, previous)
        if common_paths is None:
            common_paths = this_paths
        elif this_paths != common_paths:
            errors.append(prefix + 'work_root and previous_materials differ between days')
        root_missing = root_missing or root == ''
        paper = obj.get('paper', {})
        if not isinstance(paper, dict) or type(paper.get('pages')) is not int or paper.get('pages') != 4 or any(
            paper.get(k) is not True for k in ('references_included', 'pdf', 'editable_source')
        ):
            errors.append(prefix + 'paper must require 4 pages including references, PDF and editable source')
        outputs, requires = obj.get('outputs'), obj.get('requires')
        good_outputs = isinstance(outputs, list) and all(relative_artifact(x) for x in outputs)
        good_requires = isinstance(requires, list) and all(relative_artifact(x) for x in requires)
        if not good_outputs:
            errors.append(prefix + 'outputs must list paths relative to work_root')
        if not good_requires:
            errors.append(prefix + 'requires must list paths relative to work_root')
        mandatory = {'progress.md', f'reports/{path.stem}_report.md', f'handoff/{path.stem}.md'}
        if good_outputs:
            missing = mandatory - set(outputs)
            if missing:
                errors.append(prefix + 'missing daily records: ' + ', '.join(sorted(missing)))
            if len(outputs) != len(set(outputs)):
                errors.append(prefix + 'duplicate outputs')
            if day >= 6:
                if not any(x.lower().endswith('.pdf') for x in outputs):
                    errors.append(prefix + 'draft/final PDF missing from outputs')
                if not any(x.startswith('paper/') and x.lower().endswith(('.md', '.tex', '.json', '.docx', '.html')) for x in outputs):
                    errors.append(prefix + 'editable paper source missing from outputs')
        if good_requires:
            if day > 1 and f'handoff/{week}w{day-1}day.md' not in requires:
                errors.append(prefix + 'previous day handoff missing from requires')
            unresolved = set(requires) - earlier_outputs
            if unresolved:
                errors.append(prefix + 'prerequisites not produced on earlier days: ' + ', '.join(sorted(unresolved)))
        if good_outputs:
            earlier_outputs.update(outputs)
    return errors, root_missing


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('folder', type=Path)
    parser.add_argument('--week', type=int, default=1)
    args = parser.parse_args()
    if args.week < 1:
        parser.error('--week must be positive')
    if not args.folder.is_dir():
        parser.error('folder must exist')
    errors, root_missing = validate(args.folder, args.week)
    if errors:
        for error in errors:
            print('ERROR: ' + error, file=sys.stderr)
        return 1
    print('PASS: seven ordered MDs; paths, dependencies, daily records and paper contract verified.')
    if root_missing:
        print('NOTE: work_root is empty; add the same work root to all seven files before execution.')
    print('Content, source-path fidelity and scientific validity still require review.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
