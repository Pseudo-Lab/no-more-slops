"""Local manuscript checks over an explicitly scoped repository; no network calls."""
import argparse
from collections import defaultdict
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(os.environ.get('PAPER_REVIEW_ROOT', Path.cwd())).resolve()
VERSION = '0.4.0'


def safe(root, relative):
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError('Path must stay inside the configured repository')
    return path


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def words(text):
    return re.findall(r"[a-z]+(?:'[a-z]+)?", text.lower())


def body_text(text):
    return re.split(r'^#{1,3}\s+(?:\d+[.]?\s+)?(?:references|bibliography)\s*$', text, maxsplit=1, flags=re.I | re.M)[0]


def phrase_candidates(manuscript, sources, minimum=8):
    if not 8 <= minimum <= 30:
        raise ValueError('Phrase length must be between 8 and 30')
    tokens = words(body_text(manuscript))
    index = defaultdict(list)
    for i in range(len(tokens) - minimum + 1):
        index[tuple(tokens[i:i + minimum])].append(i)
    results = []
    for source in sources:
        source_tokens = words(source.read_text(encoding='utf-8', errors='replace'))
        matches = []
        for j in range(len(source_tokens) - minimum + 1):
            for i in index.get(tuple(source_tokens[j:j + minimum]), []):
                if i and j and tokens[i - 1] == source_tokens[j - 1]:
                    continue
                n = minimum
                while i + n < len(tokens) and j + n < len(source_tokens) and tokens[i + n] == source_tokens[j + n]:
                    n += 1
                matches.append({'manuscript_token_start': i, 'source_token_start': j,
                                'length_words': n, 'phrase': ' '.join(tokens[i:i + n]),
                                'classification': 'candidate_overlap', 'human_context_review': 'required'})
        results.append({'path': str(source), 'sha256': sha(source), 'source_tokens': len(source_tokens),
                        'candidate_count': len(matches), 'matches': matches[:100],
                        'matches_truncated': len(matches) > 100})
    return {'scope': 'Exact English word sequences in supplied local texts; references excluded',
            'minimum_words': minimum, 'plagiarism_percentage': None,
            'external_database_comparison': 'not_run', 'semantic_overlap_review': 'not_run',
            'sources': results, 'source_count': len(sources),
            'status': 'no_local_sources' if not sources else 'candidates_found' if any(x['candidate_count'] for x in results) else 'no_exact_candidates_in_supplied_sources',
            'interpretation': 'Neither a plagiarism verdict nor proof of originality'}


def near_candidates(manuscript, sources):
    """Screen sentence-like segments, not semantic equivalence or plagiarism."""
    try:
        from rapidfuzz import fuzz, process, __version__
    except ImportError:
        return {'status': 'dependency_unavailable', 'engine': 'RapidFuzz', 'plagiarism_percentage': None}
    def segments(text):
        return [' '.join(words(s)) for s in re.split(r'(?<=[.!?])\s+|\n\s*\n', text)
                if 12 <= len(words(s)) <= 150]
    manuscript_segments = segments(body_text(manuscript))
    results = []
    for source in sources:
        choices = segments(source.read_text(encoding='utf-8', errors='replace'))
        matches = []
        for i, segment in enumerate(manuscript_segments):
            match = process.extractOne(segment, choices, scorer=fuzz.ratio, score_cutoff=90)
            if match:
                matches.append({'manuscript_segment': i, 'manuscript_text': segment,
                                'source_segment': match[2], 'source_text': match[0],
                                'pair_string_similarity': round(match[1], 2),
                                'classification': 'candidate_overlap', 'human_context_review': 'required'})
        results.append({'path': str(source), 'candidate_count': len(matches), 'matches': matches[:100]})
    return {'engine': 'RapidFuzz', 'version': __version__, 'method': 'normalized sentence fuzz.ratio',
            'candidate_threshold': 90, 'segment_words': [12, 150], 'source_count': len(sources),
            'status': 'no_local_sources' if not sources else 'candidates_found' if any(r['candidate_count'] for r in results) else 'no_near_candidates_in_supplied_sources',
            'sources': results, 'plagiarism_percentage': None,
            'limitations': 'Pairwise string scores only. Sentence splitting and PDF extraction may miss overlap; no semantic or web/database comparison.'}


def latex_lint(tex):
    binary = os.environ.get('PAPER_REVIEW_CHKTEX') or shutil.which('chktex')
    config = os.environ.get('PAPER_REVIEW_CHKTEX_RC')
    if not binary:
        return {'engine': 'ChkTeX', 'status': 'not_installed', 'diagnostics': []}
    command = [binary, '-q', '-I0', '-f%l:%c:%n:%m\n']
    if config:
        command.extend(['-g0', '-l', str(Path(config).resolve())])
    command.append(str(tex))
    try:
        result = subprocess.run(command, cwd=tex.parent, text=True, capture_output=True, timeout=60)
        version = subprocess.run([binary, '--version'], text=True, capture_output=True, timeout=10)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {'engine': 'ChkTeX', 'status': 'tool_error', 'error': str(exc), 'diagnostics': []}
    diagnostics = []
    for line in result.stdout.splitlines():
        fields = line.split(':', 3)
        if len(fields) == 4 and all(f.isdigit() for f in fields[:3]):
            diagnostics.append(dict(zip(['line', 'column', 'rule', 'message'], fields)))
    status = 'tool_error' if result.returncode not in [0, 2, 3] else 'warnings_found' if diagnostics or result.returncode != 0 else 'passed'
    return {'engine': 'ChkTeX', 'version': (version.stdout + version.stderr).strip().splitlines()[:1], 'status': status,
            'exit_code': result.returncode, 'diagnostic_count': len(diagnostics), 'diagnostics': diagnostics,
            'stdout': result.stdout, 'stderr': result.stderr, 'command': command,
            'limitations': 'Static LaTeX typography only; no prose grammar, visual layout, arXiv compilation or acceptance judgment. Input-file traversal disabled.'}


def audit(package_relative, root=ROOT):
    root = Path(root).resolve()
    package = safe(root, package_relative)
    manuscript = package / 'shortpaper.md'
    if not manuscript.exists():
        manuscript = package / 'manuscript.md'
    if not manuscript.is_file():
        raise ValueError('Package needs shortpaper.md or manuscript.md')
    manuscript = safe(root, manuscript.relative_to(root))
    text = manuscript.read_text(encoding='utf-8')
    tex = package / (manuscript.stem + '.tex')
    pdf = package / (manuscript.stem + '.pdf')
    bib = package / 'references.bib'
    inputs = [manuscript]
    lint = {'engine': 'ChkTeX', 'status': 'no_latex_source', 'diagnostics': []}
    checks, findings = [], []

    def check(name, passed, details):
        checks.append({'name': name, 'status': 'passed' if passed else 'needs_review', 'details': details})

    headings = re.findall(r'^#{1,3}\s+(.+)', text, re.M)
    for section in ['abstract', 'introduction', 'methods', 'results', 'conclusion', 'references']:
        check('section_' + section, any(section in h.lower() for h in headings), 'Section presence only; content adequacy requires review')
    for pattern, label in [(r'Authors and affiliations.*?determined', 'author_placeholder'),
                           (r'Venue-neutral working short paper', 'working_draft_label'),
                           (r'Novelty, authorship, and venue compliance.*?pending', 'internal_status_in_body'),
                           (r'rather than submission readiness', 'internal_readiness_in_body')]:
        match = re.search(pattern, text, re.I)
        if match:
            findings.append({'id': label, 'priority': 'required' if label == 'author_placeholder' else 'recommended',
                             'evidence': match.group(), 'line': text[:match.start()].count('\n') + 1})
    if bib.is_file():
        inputs.append(safe(root, bib.relative_to(root)))
        keys = set(re.findall(r'@\w+\s*\{\s*([^,\s]+)', bib.read_text(encoding='utf-8')))
        cited = set(re.findall(r'@([\w:.-]+)', body_text(text)))
        check('bibliography_keys', bool(cited) and not cited - keys, {'cited': sorted(cited), 'missing': sorted(cited - keys)})
    else:
        check('bibliography_file', False, 'references.bib missing')
    if tex.is_file():
        inputs.append(safe(root, tex.relative_to(root)))
        source = tex.read_text(encoding='utf-8')
        lint = latex_lint(tex)
        figure_checks = []
        for name in re.findall(r'\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}', source):
            figure = safe(root, (package / name).relative_to(root))
            figure_checks.append({'reference': name, 'exists': figure.is_file()})
            if figure.is_file(): inputs.append(figure)
        check('figure_files', all(x['exists'] for x in figure_checks), figure_checks)
        check('latex_document', '\\documentclass' in source and '\\end{document}' in source, 'Source structure only; no arXiv-side compilation')
    else:
        check('latex_source', False, 'LaTeX source absent')
    if pdf.is_file():
        pdf = safe(root, pdf.relative_to(root)); inputs.append(pdf)
        try:
            from pypdf import PdfReader
            reader = PdfReader(pdf)
            page_text = [p.extract_text() or '' for p in reader.pages]
            check('pdf_readable', True, {'pages': len(reader.pages), 'text_chars_per_page': list(map(len, page_text))})
        except ImportError:
            check('pdf_readable', False, 'pypdf unavailable; file existence does not verify PDF')
        except Exception as exc:
            check('pdf_readable', False, type(exc).__name__)
    else:
        check('pdf_readable', False, 'PDF missing')
    validation = package / 'build_validation.json'
    if validation.exists():
        inputs.append(safe(root, validation.relative_to(root)))
        state = package / 'task_state.json'
        if state.exists(): inputs.append(safe(root, state.relative_to(root)))
        recorded = json.loads(validation.read_text(encoding='utf-8'))
        expected = json.loads(state.read_text(encoding='utf-8')).get('pdf_sha256') if state.exists() else None
        check('build_record_matches_pdf', bool(expected and pdf.exists() and expected == sha(pdf)),
              {'recorded_status': recorded.get('status'), 'recorded_pages': {k: v for k, v in recorded.get('pages', {}).items() if k != 'details'},
               'scope': 'PDF hash agreement only; manual rendering review still required'})
    sources = []
    source_dir = package / 'sources'
    if source_dir.is_dir():
        source_dir = safe(root, source_dir.relative_to(root))
        for file in sorted(source_dir.glob('*.txt')):
            file = safe(root, file.relative_to(root))
            if file.stat().st_size > 10_000_000: raise ValueError('Source text exceeds 10 MB')
            sources.append(file)
    inputs.extend(sources)
    if (package / 'renders').is_dir():
        for rendered in sorted((package / 'renders').glob('page-*.png')):
            inputs.append(safe(root, rendered.relative_to(root)))
    # Bind supporting metadata and page images as well as the checked manuscript.
    for file in sorted(package.rglob('*')):
        if (file.is_file() and 'reviews' not in file.relative_to(package).parts
                and '__pycache__' not in file.relative_to(package).parts
                and file.suffix not in {'.aux', '.bbl', '.blg', '.out', '.log', '.pyc', '.synctex'}):
            inputs.append(safe(root, file.relative_to(root)))
    report = {'schema_version': 1, 'tool_version': VERSION, 'checked_at': datetime.now(timezone.utc).isoformat(),
              'package': str(package.relative_to(root)), 'manuscript': str(manuscript.relative_to(root)),
              'input_files': [{'path': str(p.relative_to(root)), 'sha256': sha(p)} for p in dict.fromkeys(inputs)],
              'checks': checks, 'findings': findings, 'local_similarity': phrase_candidates(text, sources),
              'near_similarity': near_candidates(text, sources),
              'latex_lint': lint,
              'manual_checks_required': ['actual PDF layout', 'academic prose and claim support', 'figure provenance and representative selection', 'paraphrase/idea attribution', 'author and arXiv metadata decisions'],
              'arxiv_submission_status': 'not_ready_author_metadata_and_manual_review_pending' if any(f['id'] == 'author_placeholder' for f in findings) else 'manual_submission_review_pending',
              'external_similarity': {'status': 'not_connected', 'score': None, 'upload_performed': False},
              'originals_modified': False}
    for comparison in [report['local_similarity'], report['near_similarity']]:
        for entry in comparison.get('sources', []):
            entry['path'] = str(Path(entry['path']).relative_to(root))
    return report


def review_path(package_relative, review_id, root=ROOT):
    if not re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9_-]{0,79}', review_id): raise ValueError('Invalid review ID')
    root = Path(root).resolve()
    package = safe(root, package_relative)
    return safe(package, Path('reviews') / review_id)


def save_editorial(package_relative, review_id, input_digest, findings, summary, root=ROOT):
    directory = review_path(package_relative, review_id, root)
    checks_path = safe(Path(root).resolve(), (directory / 'local_checks.json').relative_to(Path(root).resolve()))
    checks = json.loads(checks_path.read_text(encoding='utf-8'))
    if checks['input_digest'] != input_digest: raise ValueError('Input digest mismatch')
    if checks['latex_lint']['status'] not in ['passed', 'warnings_found']: raise ValueError('Required ChkTeX run is missing or failed')
    for entry in checks['input_files']:
        if sha(safe(Path(root).resolve(), entry['path'])) != entry['sha256']: raise ValueError('Review inputs changed; start a fresh review')
    if audit(package_relative, root)['input_files'] != checks['input_files']:
        raise ValueError('Review input set changed; start a fresh review')
    if len(findings) > 100 or len(summary) > 10000: raise ValueError('Review exceeds limits')
    required = {'id', 'location', 'evidence', 'priority', 'explanation', 'confidence', 'suggested_correction'}
    for index, finding in enumerate(findings):
        if not required <= finding.keys(): raise ValueError('Missing required finding fields')
        if finding['priority'] not in ['required', 'recommended', 'minor']: raise ValueError('Invalid priority')
        confidence = finding['confidence']
        if isinstance(confidence, str) and confidence.split(':', 1)[0] in ['높음', '중간', '낮음']:
            finding = dict(finding)
            finding['confidence_note'] = confidence
            finding['confidence'] = {'높음': 'high', '중간': 'medium', '낮음': 'low'}[confidence.split(':', 1)[0]]
            findings[index] = finding
        if finding['confidence'] not in ['high', 'medium', 'low']: raise ValueError('Confidence must be high, medium or low (높음/중간/낮음 also accepted)')
        if not all(isinstance(v, str) and len(v) <= 10000 for v in finding.values()): raise ValueError('Finding values must be bounded strings')
    artifact = {'schema_version': 1, 'review_id': review_id, 'input_digest': input_digest,
                'summary': summary, 'findings': findings, 'originals_modified': False}
    output = safe(directory, 'editorial_review.json')
    if output.exists():
        if json.loads(output.read_text(encoding='utf-8')) != artifact: raise ValueError('Editorial report already saved; use a new review ID')
        return {'saved': str(output), 'idempotent': True}
    with output.open('x', encoding='utf-8') as handle: json.dump(artifact, handle, ensure_ascii=False, indent=2)
    return {'saved': str(output), 'idempotent': False}


def run_review(package_relative, review_id, root=ROOT):
    if not re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9_-]{0,79}', review_id):
        raise ValueError('Invalid review ID')
    report = audit(package_relative, root)
    root = Path(root).resolve(); package = safe(root, package_relative)
    destination = review_path(package_relative, review_id, root)
    output = safe(destination, 'local_checks.json')
    digest = hashlib.sha256(json.dumps({'version': VERSION, 'files': report['input_files']}, sort_keys=True).encode()).hexdigest()
    if output.exists():
        old = json.loads(output.read_text(encoding='utf-8'))
        if old.get('input_digest') != digest: raise ValueError('Review ID already used for different inputs; choose a fresh ID')
        return old
    report.update(review_id=review_id, input_digest=digest, review_directory=str(destination.relative_to(root)))
    destination.mkdir(parents=True, exist_ok=True)
    with output.open('x', encoding='utf-8') as handle:
        json.dump(report, handle, ensure_ascii=False, indent=2)
    return report


def serve(root=ROOT):
    from mcp.server.fastmcp import FastMCP, Image
    root = Path(root).resolve()
    server = FastMCP('paper_review_local')

    @server.tool()
    def run_local_review(package_relative: str, review_id: str) -> dict:
        """Save local manuscript checks under package/reviews; no upload or original edits."""
        return run_review(package_relative, review_id, root)

    @server.tool()
    def read_local_review(package_relative: str, review_id: str) -> dict:
        """Read a previously saved check report."""
        if not re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9_-]{0,79}', review_id): raise ValueError('Invalid review ID')
        path = safe(review_path(package_relative, review_id, root), 'local_checks.json')
        return json.loads(path.read_text(encoding='utf-8'))

    @server.tool()
    def read_review_input(package_relative: str, relative_file: str, offset: int = 0, limit: int = 20000) -> dict:
        """Read package text with pagination. No network or original writes."""
        package = safe(root, package_relative)
        path = safe(package, relative_file)
        if path.suffix not in ['.md', '.txt', '.tex', '.bib', '.json']: raise ValueError('Only text input formats are supported')
        if offset < 0 or not 1 <= limit <= 30000 or path.stat().st_size > 10_000_000: raise ValueError('Invalid read bounds')
        text = path.read_text(encoding='utf-8', errors='replace')
        return {'path': str(path), 'sha256': sha(path), 'offset': offset, 'total_chars': len(text), 'text': text[offset:offset+limit]}

    @server.tool()
    def read_rendered_page(package_relative: str, page_number: int) -> Image:
        """Return an existing PNG page rendering for visual inspection; no rendering job."""
        if not 1 <= page_number <= 100: raise ValueError('Invalid page number')
        package = safe(root, package_relative)
        path = safe(package, 'renders/page-' + str(page_number) + '.png')
        if path.stat().st_size > 10_000_000: raise ValueError('Image exceeds limit')
        return Image(path=str(path), format='png')

    @server.tool()
    def save_editorial_review(package_relative: str, review_id: str, input_digest: str, findings: list[dict], summary: str) -> dict:
        """Save findings only in the matching review directory. All finding values are strings. Fields: id, location, evidence, priority (required/recommended/minor), explanation, confidence (high/medium/low), suggested_correction. Originals unchanged."""
        return save_editorial(package_relative, review_id, input_digest, findings, summary, root)

    @server.tool()
    def local_review_capabilities() -> dict:
        """Explain current coverage and unavailable provider-backed comparisons."""
        return {'version': VERSION, 'root': str(root), 'network_access': False,
                'external_similarity_connected': False, 'global_plagiarism_percentage': False,
                'free_local_libraries': ['pypdf', 'RapidFuzz'],
                'tools': ['run_local_review', 'read_local_review', 'read_review_input', 'read_rendered_page', 'save_editorial_review', 'local_review_capabilities']}

    server.run(transport='stdio')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--serve', action='store_true')
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--package')
    parser.add_argument('--review-id')
    args = parser.parse_args()
    if args.serve: serve(args.root)
    elif args.package and args.review_id:
        result = run_review(args.package, args.review_id, args.root)
        print(json.dumps({'review_directory': result['review_directory'], 'findings': result['findings'], 'local_source_count': result['local_similarity']['source_count'], 'similarity_status': result['local_similarity']['status'], 'external_similarity': result['external_similarity']}, ensure_ascii=False))
    else: parser.error('Use --serve or both --package and --review-id')
