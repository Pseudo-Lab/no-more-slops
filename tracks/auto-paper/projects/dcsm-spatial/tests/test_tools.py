import hashlib
import asyncio
import importlib.util
import json
import os
import re
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[5]


def load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


exporter = load('evidence_export', 'tracks/auto-paper/skills/experiment-to-paper/scripts/export_evidence.py')
review = load('local_review', 'tracks/auto-paper/skills/paper-review-local/scripts/review_mcp.py')


class ExportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.result = self.root / 'results.json'
        self.result.write_text(json.dumps({'score': 0, 'missing': None, 'a/b': {'~key': [0.75]}}))
        self.spec = {'schema_version': 1, 'measurements': [
            {'id': 'score', 'file': 'results.json', 'pointer': '/score', 'unit': 'fraction', 'denominator': 4}]}

    def export(self):
        (self.root / 'spec.json').write_text(json.dumps(self.spec))
        return exporter.export(self.root, 'spec.json', self.root / 'output')

    def test_missing_and_zero_remain_distinct(self):
        self.spec['measurements'].append({'id': 'missing', 'file': 'results.json', 'pointer': '/missing', 'unit': 'fraction'})
        self.export()
        values = json.loads((self.root / 'output/evidence/measurements.json').read_text())['measurements']
        self.assertEqual(values[0]['value'], 0)
        self.assertEqual(values[1]['value'], None)
        self.assertEqual(values[1]['status'], 'unavailable')

    def test_manifest_hashes_exact_input_bytes(self):
        self.export()
        m = json.loads((self.root / 'output/evidence/manifest.json').read_text())
        self.assertEqual(m['inputs']['results.json']['sha256'], hashlib.sha256(self.result.read_bytes()).hexdigest())
        self.assertIsNone(m['execution_revision'])

    def test_escaped_pointer_and_array(self):
        self.spec['measurements'][0]['pointer'] = '/a~1b/~0key/0'
        self.export()
        m = json.loads((self.root / 'output/evidence/measurements.json').read_text())
        self.assertEqual(m['measurements'][0]['value'], 0.75)

    def test_invalid_measurement_creates_no_output(self):
        for value in [True, '0.5', float('nan'), float('inf')]:
            with self.subTest(value=value):
                self.result.write_text(json.dumps({'score': value}))
                with self.assertRaises(ValueError): self.export()
                self.assertFalse((self.root / 'output').exists())

    def test_duplicate_ids_rejected(self):
        self.spec['measurements'].append(dict(self.spec['measurements'][0]))
        with self.assertRaises(ValueError): self.export()

    def test_missing_selector_leaves_no_partial_output(self):
        self.spec['measurements'][0]['pointer'] = '/unknown'
        with self.assertRaises(KeyError): self.export()
        self.assertFalse((self.root / 'output').exists())

    def test_existing_output_is_preserved(self):
        self.export()
        original = (self.root / 'output/evidence/measurements.json').read_bytes()
        self.result.write_text('{"score": 1}')
        with self.assertRaises(ValueError): self.export()
        self.assertEqual((self.root / 'output/evidence/measurements.json').read_bytes(), original)

    def test_input_paths_and_symlinks_stay_in_root(self):
        with tempfile.TemporaryDirectory() as elsewhere:
            outside = Path(elsewhere) / 'outside.json'
            outside.write_text('{"score": 1}')
            (self.root / 'linked.json').symlink_to(outside)
            for name in [str(outside), '../outside.json', 'linked.json']:
                with self.subTest(name=name):
                    self.spec['measurements'][0]['file'] = name
                    with self.assertRaises(ValueError): self.export()

    def test_invalid_schema_denominator_and_pointer(self):
        for key, value in [('denominator', 0), ('denominator', True), ('pointer', '/a~2b'), ('unit', 'a|b')]:
            with self.subTest(key=key, value=value):
                entry = self.spec['measurements'][0]
                before = dict(entry)
                entry[key] = value
                with self.assertRaises(ValueError): self.export()
                self.spec['measurements'][0] = before


class ReviewTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.package = self.root / 'paper'
        self.package.mkdir()
        self.md = self.package / 'manuscript.md'
        self.md.write_text('# Demo\nAuthors and affiliations to be determined\n' +
                           '\n'.join('## ' + x for x in ['Abstract', 'Introduction', 'Methods', 'Results', 'Conclusion', 'References']))
        (self.package / 'manuscript.tex').write_text('\\documentclass{article}\n\\begin{document}\nDemo\\end{document}\n')
        self.linter = patch.object(review, 'latex_lint', return_value={'status': 'passed', 'diagnostics': []})
        self.linter.start()
        self.addCleanup(self.linter.stop)

    def test_check_preserves_originals_and_reports_missing_pdf(self):
        original = self.md.read_bytes()
        r = review.run_review('paper', 'one', self.root)
        self.assertEqual(self.md.read_bytes(), original)
        self.assertFalse(r['originals_modified'])
        self.assertTrue(any(f['id'] == 'author_placeholder' for f in r['findings']))
        self.assertEqual(next(c for c in r['checks'] if c['name'] == 'pdf_readable')['status'], 'needs_review')
        self.assertEqual(r['local_similarity']['status'], 'no_local_sources')

    def test_same_id_is_immutable(self):
        r = review.run_review('paper', 'one', self.root)
        self.assertEqual(review.run_review('paper', 'one', self.root), r)
        self.md.write_text(self.md.read_text() + '\nChanged')
        with self.assertRaises(ValueError): review.run_review('paper', 'one', self.root)

    def test_editorial_rejects_changed_inputs(self):
        r = review.run_review('paper', 'one', self.root)
        self.md.write_text(self.md.read_text() + '\nChanged')
        with self.assertRaises(ValueError): review.save_editorial('paper', 'one', r['input_digest'], [], 'review', self.root)

    def test_editorial_rejects_new_support_file(self):
        r = review.run_review('paper', 'one', self.root)
        (self.package / 'new-evidence.json').write_text('{}')
        with self.assertRaises(ValueError): review.save_editorial('paper', 'one', r['input_digest'], [], 'review', self.root)

    def test_editorial_requires_linter(self):
        with patch.object(review, 'latex_lint', return_value={'status': 'not_installed', 'diagnostics': []}):
            r = review.run_review('paper', 'one', self.root)
            with self.assertRaises(ValueError): review.save_editorial('paper', 'one', r['input_digest'], [], 'review', self.root)

    def test_editorial_save_is_idempotent_and_validated(self):
        r = review.run_review('paper', 'one', self.root)
        self.assertFalse(review.save_editorial('paper', 'one', r['input_digest'], [], 'review', self.root)['idempotent'])
        self.assertTrue(review.save_editorial('paper', 'one', r['input_digest'], [], 'review', self.root)['idempotent'])
        with self.assertRaises(ValueError): review.save_editorial('paper', 'one', 'wrong', [], 'review', self.root)

    def test_outside_package_and_review_id_rejected(self):
        with self.assertRaises(ValueError): review.run_review('../outside', 'one', self.root)
        with self.assertRaises(ValueError): review.run_review('paper', '../outside', self.root)
        with tempfile.TemporaryDirectory() as elsewhere:
            f = Path(elsewhere) / 'manuscript.md'
            f.write_text('external')
            self.md.unlink()
            self.md.symlink_to(f)
            with self.assertRaises(ValueError): review.audit('paper', self.root)

    def test_build_intermediates_do_not_change_digest(self):
        r = review.run_review('paper', 'one', self.root)
        (self.package / 'manuscript.aux').write_text('build temporary')
        self.assertEqual(review.run_review('paper', 'one', self.root)['input_digest'], r['input_digest'])

    def test_review_output_symlink_cannot_escape_package(self):
        sibling = self.root / 'sibling'
        sibling.mkdir()
        (self.package / 'reviews').symlink_to(sibling, target_is_directory=True)
        with self.assertRaises(ValueError): review.run_review('paper', 'one', self.root)
        self.assertEqual(list(sibling.iterdir()), [])

    def test_exact_source_matches_are_candidates(self):
        phrase = 'this is a sufficiently long shared technical phrase to inspect in context'
        (self.package / 'sources').mkdir()
        (self.package / 'sources/own-demo.txt').write_text(phrase)
        self.md.write_text(self.md.read_text().replace('## References', phrase + '\n## References'))
        r = review.audit('paper', self.root)
        self.assertEqual(r['local_similarity']['status'], 'candidates_found')
        self.assertIsNone(r['local_similarity']['plagiarism_percentage'])

    def test_linter_failure_never_passes(self):
        self.linter.stop()
        with patch.dict(os.environ, {'PAPER_REVIEW_CHKTEX': '/definitely-missing/chktex'}):
            self.assertEqual(review.latex_lint(self.package / 'manuscript.tex')['status'], 'tool_error')


class PortabilityTests(unittest.TestCase):
    def test_entrypoint_linked_bundle_runs_without_checkout(self):
        # URL installers fetch direct SKILL.md references, not every tree file.
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            for name in ['experiment-to-paper', 'paper-review-local']:
                source = ROOT / 'tracks/auto-paper/skills' / name
                installed = root / name
                installed.mkdir()
                entry = (source / 'SKILL.md').read_text()
                (installed / 'SKILL.md').write_text(entry)
                links = set(re.findall(r'\]\(((?:scripts|references|assets)/[^)]+)\)', entry))
                bundled = {p.relative_to(source).as_posix() for p in source.rglob('*')
                           if p.is_file() and p.parts[len(source.parts)] in {'scripts', 'references', 'assets'}
                           and '__pycache__' not in p.parts and p.suffix != '.pyc'}
                self.assertEqual(links, bundled, name)
                for relative in links:
                    target = installed / relative
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(source / relative, target)
            skill = root / 'experiment-to-paper'
            result = subprocess.run([sys.executable, '-S', str(skill / 'scripts/export_evidence.py'),
                '--root', str(skill / 'assets/example'), '--spec', 'export-spec.json', '--out', str(root / 'out')],
                cwd=root, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            values = json.loads((root / 'out/evidence/measurements.json').read_text())['measurements']
            self.assertEqual([v['value'] for v in values], [0.75, 0, None])
            package = root / 'project/paper'
            package.mkdir(parents=True)
            (package / 'manuscript.md').write_text('# Invented manuscript')
            result = subprocess.run([sys.executable, str(root / 'paper-review-local/scripts/review_mcp.py'),
                '--root', str(root / 'project'), '--package', 'paper', '--review-id', 'url-bundle'],
                cwd=root, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((package / 'reviews/url-bundle/local_checks.json').is_file())

    def test_installed_skills_run_outside_checkout(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            installed = root / 'installed'
            for name in ['experiment-to-paper', 'paper-review-local']:
                shutil.copytree(ROOT / 'tracks/auto-paper/skills' / name, installed / name)
            package = root / 'project/paper'
            shutil.copytree(ROOT / 'tracks/auto-paper/skills/experiment-to-paper/assets/example', package)
            (package / 'manuscript.md').write_text('# Invented manuscript')
            from pypdf import PdfWriter
            writer = PdfWriter()
            writer.add_blank_page(width=612, height=792)
            writer.write(package / 'manuscript.pdf')
            r = subprocess.run([sys.executable, str(installed / 'experiment-to-paper/scripts/export_evidence.py'),
                                '--root', str(package), '--spec', 'export-spec.json', '--out', str(root / 'export')],
                               cwd=root, capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertEqual(json.loads(r.stdout)['measurements'], 3)
            r = subprocess.run([sys.executable, str(installed / 'paper-review-local/scripts/review_mcp.py'),
                                '--root', str(root / 'project'), '--package', 'paper', '--review-id', 'portable'],
                               cwd=root, capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            report = json.loads((package / 'reviews/portable/local_checks.json').read_text())
            self.assertEqual(report['package'], 'paper')
            pdf_check = next(c for c in report['checks'] if c['name'] == 'pdf_readable')
            self.assertEqual(pdf_check['details']['pages'], 1)

    def test_mcp_tools_use_explicit_root(self):
        from mcp import ClientSession, StdioServerParameters
        from mcp.client.stdio import stdio_client

        async def exercise(root):
            params = StdioServerParameters(command=sys.executable,
                args=[str(ROOT / 'tracks/auto-paper/skills/paper-review-local/scripts/review_mcp.py'), '--serve', '--root', str(root)])
            async with stdio_client(params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    result = await session.call_tool('local_review_capabilities', {})
                    self.assertFalse(result.isError)
                    capabilities = json.loads(result.content[0].text)
                    self.assertEqual(capabilities['root'], str(root))
                    result = await session.call_tool('run_local_review', {'package_relative': 'paper', 'review_id': 'mcp-one'})
                    self.assertFalse(result.isError)
                    self.assertTrue((root / 'paper/reviews/mcp-one/local_checks.json').is_file())
                    denied = await session.call_tool('read_review_input', {'package_relative': 'paper', 'relative_file': '../outside.txt'})
                    self.assertTrue(denied.isError)

        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / 'paper').mkdir()
            (root / 'paper/manuscript.md').write_text('# Demo')
            asyncio.run(asyncio.wait_for(exercise(root), timeout=20))


if __name__ == '__main__':
    unittest.main()
