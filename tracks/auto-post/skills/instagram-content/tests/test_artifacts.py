"""Behavioral checks for file generation, source requirements and safe reruns."""
import argparse
from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from zipfile import ZipFile

from PIL import Image

SKILL = Path(__file__).resolve().parents[1]


def load(name):
    spec = importlib.util.spec_from_file_location(name, SKILL / 'scripts' / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


carousel = load('render_carousel')
avatar = load('prepare_avatar')


class ArtifactTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='instagram-content-test-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.manifest = self.root / 'post.json'
        self.post = json.loads((SKILL / 'references/post.example.json').read_text())
        for slide in self.post['slides']:
            if image := slide.get('image'):
                image['path'] = str(SKILL / 'assets/layout-sample.png')

    def read(self, post=None):
        self.manifest.write_text(json.dumps(post or self.post, ensure_ascii=False))
        return carousel.read_manifest(self.manifest)

    def fonts(self):
        try:
            return carousel.find_fonts(argparse.Namespace(font_dir=None, font_regular=None, font_bold=None), self.post)
        except ValueError as error:
            self.skipTest(str(error))

    def test_all_layouts_produce_ordered_upload_package(self):
        post, brand = self.read()
        renderer = carousel.Renderer(post, brand, self.manifest, self.fonts())
        images = [renderer.render(slide, n) for n, slide in enumerate(post['slides'], 1)]
        out = self.root / 'rendered'
        carousel.write_outputs(out, post, brand, images, False)
        for path in sorted(out.glob('[0-9][0-9].png')):
            with Image.open(path) as image:
                self.assertEqual(image.size, (1080, 1350))
                self.assertEqual(image.mode, 'RGB')
                self.assertEqual(image.getpixel((0, 0)), (36, 87, 255))
                self.assertTrue(image.info.get('icc_profile'))
        with ZipFile(out / 'carousel.zip') as archive:
            self.assertIsNone(archive.testzip())
            self.assertEqual(archive.namelist(), ['01.png', '02.png', '03.png', '04.png', 'caption.txt', 'sources.md'])
        self.assertEqual((out / 'caption.txt').read_text(), 'LAYOUT DEMO / NOT FOR PUBLICATION\n\n' + post['caption'] + '\n')
        self.assertNotIn(str(self.root), (out / 'sources.md').read_text())
        self.assertIn('NOT FOR PUBLICATION', (out / 'caption.txt').read_text())

    def test_real_news_requires_sources_and_connected_claims(self):
        self.post['demo'] = False
        self.post['content_type'] = 'news'
        with self.assertRaisesRegex(ValueError, 'primary sources'):
            self.read()
        self.post['sources'] = [{'id': 'primary', 'publisher': 'Example', 'title': 'Fixture source', 'url': 'https://example.com/release', 'published_at': '2026-10-07', 'checked_at': '2026-10-08'}]
        with self.assertRaisesRegex(ValueError, 'source_ids'):
            self.read()
        for slide in self.post['slides']:
            slide['source_ids'] = ['primary']
        post, _ = self.read()
        self.assertFalse(post['demo'])
        self.post['slides'][0]['source_ids'] = ['unknown']
        with self.assertRaisesRegex(ValueError, 'unknown source'):
            self.read()

    def test_official_media_requires_attribution(self):
        image = self.post['slides'][0]['image']
        image['kind'] = 'official_photo'
        with self.assertRaisesRegex(ValueError, 'source URL'):
            self.read()
        image['source_url'] = 'https://example.com/official'
        image['credit'] = ''
        with self.assertRaisesRegex(ValueError, 'credit'):
            self.read()

    def test_overflow_and_invalid_crops_fail_before_export(self):
        post, brand = self.read()
        renderer = carousel.Renderer(post, brand, self.manifest, self.fonts())
        slide = deepcopy(post['slides'][0])
        slide['title'] = ['An unreadably long title ' * 15]
        with self.assertRaisesRegex(ValueError, 'too wide'):
            renderer.render(slide, 1)
        slide = deepcopy(post['slides'][0])
        slide['image']['crop'] = [0, 0, 99999, 100]
        with self.assertRaisesRegex(ValueError, 'outside the source'):
            renderer.render(slide, 1)

    def test_output_guard_preserves_existing_work(self):
        out = self.root / 'existing'
        out.mkdir()
        marker = out / 'keep.txt'
        marker.write_text('do not alter')
        with self.assertRaisesRegex(ValueError, 'not empty'):
            carousel.output_guard(out, [self.manifest], False)
        with self.assertRaisesRegex(ValueError, 'outside the output'):
            carousel.output_guard(out, [marker], True)
        self.assertEqual(marker.read_text(), 'do not alter')

    def test_acknowledgement_not_duplicated_and_stale_pages_not_zipped(self):
        self.post['brand']['acknowledgement'] = 'Photos courtesy of Harbor Studio.'
        post, brand = self.read()
        post['slides'] = post['slides'][:1]
        post['caption'] += '\n' + brand['acknowledgement']
        out = self.root / 'rerun'
        out.mkdir()
        (out / '09.png').write_bytes(b'stale')
        (out / 'keep.txt').write_text('keep')
        carousel.write_outputs(out, post, brand, [Image.new('RGB', (1080, 1350), brand['background'])], True)
        self.assertFalse((out / '09.png').exists())
        self.assertEqual((out / 'keep.txt').read_text(), 'keep')
        self.assertEqual((out / 'caption.txt').read_text().count(brand['acknowledgement']), 1)
        with ZipFile(out / 'carousel.zip') as archive:
            self.assertEqual(archive.namelist(), ['01.png', 'caption.txt', 'sources.md'])

    def test_avatar_alpha_background_and_circle(self):
        source = self.root / 'square.png'
        Image.new('RGBA', (128, 128), (0, 0, 0, 0)).save(source)
        out = self.root / 'avatar'
        avatar.prepare(source, out, '#2457FF')
        with Image.open(out / 'profile-1080.png') as image:
            self.assertEqual(image.size, (1080, 1080))
            self.assertEqual(image.getpixel((20, 20)), (36, 87, 255))
            self.assertTrue(image.info.get('icc_profile'))
        with Image.open(out / 'circle-preview.png') as image:
            self.assertEqual(image.getpixel((0, 0))[3], 0)
            self.assertEqual(image.getpixel((320, 320))[3], 255)

    def test_avatar_rejects_unreviewed_crop_and_source_overwrite(self):
        source = self.root / 'portrait.png'
        Image.new('RGB', (100, 160)).save(source)
        with self.assertRaisesRegex(ValueError, 'square image'):
            avatar.prepare(source, self.root / 'avatar', '#2457FF')
        with self.assertRaisesRegex(ValueError, 'outside the output'):
            avatar.prepare(source, self.root, '#2457FF', True)

    def test_brand_is_explicit_and_identity_fields_are_optional(self):
        self.post.pop('brand')
        with self.assertRaisesRegex(ValueError, 'brand is required'):
            self.read()
        self.post['brand'] = {'text': '#FFFFFF'}
        with self.assertRaisesRegex(ValueError, 'background'):
            self.read()
        self.post['brand']['background'] = '#121212'
        self.post['demo'] = False
        post, brand = self.read()
        renderer = carousel.Renderer(post, brand, self.manifest, self.fonts())
        images = [renderer.render(post['slides'][0], 1)]
        post['slides'] = post['slides'][:1]
        out = self.root / 'unbranded'
        carousel.write_outputs(out, post, brand, images, False)
        self.assertEqual((out / 'caption.txt').read_text(), post['caption'] + '\n')
        self.assertEqual(set(brand), {'background', 'text'})

    def test_non_news_claims_can_require_evidence(self):
        self.post['demo'] = False
        self.read()  # Original editorial copy needs no fabricated news references.
        self.post['slides'][0]['requires_sources'] = True
        with self.assertRaisesRegex(ValueError, 'source_ids'):
            self.read()

    def test_distinct_account_can_use_korean_copy_and_dark_palette(self):
        self.post['demo'] = False
        self.post['content_type'] = 'promotion'
        self.post['brand'] = {'background': '#132A24', 'text': '#FFFFFF', 'display_name': '숲의 서점', 'handle': '@forest_books'}
        self.post['caption'] = '좋아하는 문장을 오래 읽는 공간, 숲의 서점을 소개합니다.'
        self.post['slides'] = [self.post['slides'][0]]
        self.post['slides'][0].update(kicker='책과 함께 보내는 오후', title=['천천히 읽는', '우리의 공간.'], body=['좋아하는 책 한 권을 만나보세요.'])
        post, brand = self.read()
        renderer = carousel.Renderer(post, brand, self.manifest, self.fonts())
        out = self.root / 'bookshop'
        carousel.write_outputs(out, post, brand, [renderer.render(post['slides'][0], 1)], False)
        with Image.open(out / '01.png') as image:
            self.assertEqual(image.getpixel((0, 0)), (19, 42, 36))
        self.assertEqual((out / 'caption.txt').read_text(), post['caption'] + '\n')


if __name__ == '__main__':
    unittest.main()
