"""Isolated offline checks; PDF parsing is mocked, scientific results are not rerun."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import build_documents as documents


class DocumentPackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.package = self.root / 'package'
        self.package.mkdir()
        for name in documents.DOCUMENTS:
            path = self.package / (name + '.pdf')
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(b'%PDF fixture')
        self.manifest()

    def manifest(self):
        assets = [dict(path=p.relative_to(self.package).as_posix(), bytes=p.stat().st_size,
                       sha256=hashlib.sha256(p.read_bytes()).hexdigest(), pages=2)
                  for p in self.package.rglob('*.pdf')]
        value = dict(schema='nms_week02_document_package_v1', version='v21.1-20261019', assets=assets)
        (self.package / 'MANIFEST.json').write_text(json.dumps(value), encoding='utf-8')

    def test_existing_and_relative_output_are_refused(self):
        marker = self.root / 'keep.txt'
        marker.write_text('preserve', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'existing output'):
            documents.rebuild(self.package, self.root)
        with self.assertRaisesRegex(ValueError, 'absolute'):
            documents.rebuild(self.package, Path('relative-output'))
        self.assertEqual(marker.read_text(encoding='utf-8'), 'preserve')

    def test_unsafe_paths_links_and_tampering_are_refused(self):
        for name in ['../outside', '/absolute', 'build/../escape', 'C:/escape', 'build\\escape']:
            with self.assertRaisesRegex(ValueError, 'unsafe'):
                documents.file_at(self.package, name)
        path = self.package / (documents.DOCUMENTS[0] + '.pdf')
        path.write_bytes(b'changed')
        with patch.object(documents, 'read_pdf', return_value=(2, documents.ACK)), self.assertRaisesRegex(ValueError, 'changed asset'):
            documents.verify(self.package)
        with patch.object(Path, 'is_symlink', return_value=True):
            with self.assertRaisesRegex(ValueError, 'symlink'):
                documents.file_at(self.package, documents.DOCUMENTS[0] + '.pdf')

    def test_pdf_pages_acknowledgement_and_exact_inventory(self):
        with patch.object(documents, 'read_pdf', return_value=(2, documents.ACK)) as parser:
            self.assertEqual(len(documents.verify(self.package)['pdfs']), 9)
            self.assertEqual(parser.call_count, 9)
        for value, error in [((3, documents.ACK), 'page count'), ((2, 'No acknowledgement'), 'Acknowledgement')]:
            with patch.object(documents, 'read_pdf', return_value=value):
                with self.assertRaisesRegex(ValueError, error):
                    documents.verify(self.package)
        (self.package / 'extra.txt').write_text('unlisted', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'exact package inventory'):
            documents.verify(self.package)


if __name__ == '__main__':
    unittest.main()
