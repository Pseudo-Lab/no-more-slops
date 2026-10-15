"""Observable production invariants, including running a copied skill elsewhere."""
import argparse
from copy import deepcopy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from zipfile import ZipFile

from PIL import Image

SKILL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL / 'scripts'))
import run_carousel as harness


class HarnessTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix='carousel-harness-test-')
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.manifest, self.brief_path = self.root / 'post.json', self.root / 'brand-brief.json'
        self.post = json.loads((SKILL / 'references/post.example.json').read_text())
        self.post.pop('brand')
        self.post['demo'] = False
        for slide in self.post['slides']:
            if image := slide.get('image'):
                image['path'] = str(SKILL / 'assets/layout-sample.png')
        self.brief = {'brand': {'background': '#2457FF', 'text': '#FFFFFF'}}
        self.args = argparse.Namespace(manifest=self.manifest, brief=self.brief_path,
                                       out=self.root / 'out', validate_only=False, overwrite=False,
                                       font_dir=None, font_regular=None, font_bold=None)

    def save(self):
        self.manifest.write_text(json.dumps(self.post, ensure_ascii=False), encoding='utf-8')
        self.brief_path.write_text(json.dumps(self.brief, ensure_ascii=False), encoding='utf-8')

    def test_caption_boundary_counts_final_newline_and_acknowledgement(self):
        self.brief['acknowledgement'] = 'Credit'
        self.brief['caption_policy'] = {'max_characters': 499}
        self.post['caption'] = '가' * 490
        self.save()
        post, brand, _, report = harness.preflight(self.manifest, self.brief_path)
        self.assertEqual(report['caption_characters'], 499)
        self.assertEqual(harness.render.caption_text(post, brand), '가' * 490 + '\n\nCredit\n')
        self.post['caption'] += '나'
        self.save()
        with self.assertRaisesRegex(ValueError, '500 characters'):
            harness.run(self.args)
        self.assertFalse(self.args.out.exists())

    def test_hashtag_policy_counts_korean_and_ignores_url_fragments(self):
        self.post['caption'] = '본문 #AI뉴스 #Microsoft #치와와AILab\nhttps://example.com/#anchor'
        self.brief['caption_policy'] = {'hashtag_count': 3, 'max_hashtags': 3}
        self.save()
        self.assertEqual(harness.preflight(self.manifest, self.brief_path)[3]['hashtags'], 3)
        self.post['caption'] += ' #추가'
        self.save()
        with self.assertRaisesRegex(ValueError, 'exactly 3'):
            harness.preflight(self.manifest, self.brief_path)
        del self.brief['caption_policy']['hashtag_count']
        self.save()
        with self.assertRaisesRegex(ValueError, 'maximum is 3'):
            harness.preflight(self.manifest, self.brief_path)

    def test_selected_brief_prevents_brand_drift_and_wrong_slide_count(self):
        self.brief['account'] = {'display_name': 'Harbor Books', 'handle': 'harbor_books'}
        self.post['brand'] = {'handle': '@harbor_books'}
        self.save()
        _, brand, _, _ = harness.preflight(self.manifest, self.brief_path)
        self.assertEqual(brand['display_name'], 'Harbor Books')
        self.post['brand']['display_name'] = 'Another account'
        self.save()
        with self.assertRaisesRegex(ValueError, 'differs from the selected brief'):
            harness.preflight(self.manifest, self.brief_path)
        self.post.pop('brand')
        self.brief['deliverable'] = {'slides': 10}
        self.save()
        with self.assertRaisesRegex(ValueError, 'requests 10 slides'):
            harness.preflight(self.manifest, self.brief_path)

    def test_punctuation_candidates_never_rewrite_meaning_or_prose(self):
        self.brief['punctuation_policy'] = {'headlines': 'omit_terminal_period', 'large_display_copy': 'omit_terminal_period', 'short_captions': 'omit_terminal_period'}
        self.post['slides'][0]['title'] = ['오늘의 소식.']
        self.post['slides'][0]['body'] = ['v2.1 · 3.5% · example.com']
        self.post['slides'][1]['title'] = ['U.S.']
        self.post['caption'] = '새로운 소식\n\n첫 문장입니다. 두 번째 문장입니다.'
        self.save()
        before = self.manifest.read_bytes()
        post, _, _, report = harness.preflight(self.manifest, self.brief_path)
        fields = [f['field'] for f in report['punctuation_review']]
        self.assertIn('slide 1.title', fields)
        self.assertIn('slide 2.title', fields)  # Reviewable abbreviation, never deleted.
        self.assertNotIn('slide 1.body', fields)
        self.assertNotIn('caption opening', fields)
        self.assertEqual(self.manifest.read_bytes(), before)
        self.assertEqual(post['caption'], self.post['caption'])

    def test_validate_only_writes_nothing_and_does_not_claim_visual_checks(self):
        self.save()
        self.args.validate_only = True
        report = harness.run(self.args)
        self.assertFalse(report['exports_verified'])
        self.assertFalse(self.args.out.exists())
        self.assertEqual(sorted(p.name for p in self.root.iterdir()), ['brand-brief.json', 'post.json'])

    def test_failed_render_preserves_prior_delivery(self):
        self.save()
        self.args.out.mkdir()
        previous = self.args.out / '01.png'
        previous.write_bytes(b'previous delivery')
        self.args.overwrite = True
        self.post['slides'][0]['title'] = 'Overflow ' * 30
        self.save()
        with self.assertRaisesRegex(ValueError, 'too wide'):
            harness.run(self.args)
        self.assertEqual(previous.read_bytes(), b'previous delivery')
        self.assertEqual(list(self.root.glob('.carousel-*')), [])

    def test_copied_skill_runs_from_an_unrelated_working_directory(self):
        copied = self.root / 'installed' / 'instagram-content'
        shutil.copytree(SKILL, copied)
        fonts = harness.render.find_fonts(self.args, self.post)
        fixture = copied / 'references/post.example.json'
        before = (copied / 'assets/layout-sample.png').read_bytes()
        other = self.root / 'unrelated-project'
        other.mkdir()
        self.brief['deliverable'] = {'slides': 4, 'preview_columns': 2}
        self.save()
        result = subprocess.run([sys.executable, '-B', str(copied / 'scripts/run_carousel.py'), str(fixture), '--brief', str(self.brief_path), '--out', str(self.args.out), '--font-regular', str(fonts['regular']), '--font-bold', str(fonts['bold'])], cwd=other, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertTrue(report['exports_verified'])
        self.assertEqual(report['zip_entries'], 6)
        self.assertTrue(report['demo'])
        self.assertEqual((copied / 'assets/layout-sample.png').read_bytes(), before)
        with Image.open(self.args.out / 'preview.jpg') as preview:
            self.assertEqual(preview.size, (918, 1134))
        with ZipFile(self.args.out / 'carousel.zip') as archive:
            self.assertNotIn('brand-brief.json', archive.namelist())
            self.assertNotIn('production-report.json', archive.namelist())
            self.assertIn(b'NOT FOR PUBLICATION', archive.read('caption.txt'))

    def test_successful_rerun_verifies_ledger_zip_and_removes_stale_pages(self):
        self.brief['brand'] = {'background': '#132A24', 'text': '#FFFFFF'}
        self.brief['account'] = {'display_name': 'Harbor Books', 'handle': 'harbor_books'}
        self.post['slides'] = self.post['slides'][:1]
        self.post['slides'][0]['image'].update(kind='licensed', source_url='https://example.com/photo', license='CC BY 4.0', license_url='https://creativecommons.org/licenses/by/4.0/', modifications='Cropped', usage_note='Credit retained')
        self.post['slides'][0]['evidence_note'] = 'Original editorial copy, not a news claim'
        self.save()
        self.args.out.mkdir()
        (self.args.out / '09.png').write_bytes(b'stale')
        (self.args.out / 'keep.txt').write_text('unrelated file')
        self.args.overwrite = True
        report = harness.run(self.args)
        self.assertTrue(report['exports_verified'])
        self.assertFalse((self.args.out / '09.png').exists())
        self.assertEqual((self.args.out / 'keep.txt').read_text(), 'unrelated file')
        ledger = (self.args.out / 'sources.md').read_text()
        self.assertIn('CC BY 4.0', ledger)
        self.assertIn('modifications: Cropped', ledger)
        self.assertIn('Original editorial copy', ledger)
        with Image.open(self.args.out / '01.png') as image:
            self.assertEqual(image.getpixel((0, 0)), (19, 42, 36))
        post, brand = harness.render.read_manifest(self.manifest, self.brief['brand'])
        # Verification catches edits made after packaging.
        (self.args.out / 'sources.md').write_text('stale package')
        with self.assertRaisesRegex(ValueError, 'stale sources.md'):
            harness.verify_exports(self.args.out, post, brand)

    def test_malformed_policies_fail_instead_of_silently_disabling_checks(self):
        for policy in ({'max_characters': '499'}, {'hashtag_count': True}, {'max_hashtags': -1}):
            with self.subTest(policy=policy):
                self.brief['caption_policy'] = policy
                self.save()
                with self.assertRaises(ValueError):
                    harness.preflight(self.manifest, self.brief_path)


if __name__ == '__main__':
    unittest.main()
