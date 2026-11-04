"""Offline input/escaping/ack-only regression checks; no model or PDF rebuild."""
import copy
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

import typeset as t


class DocumentContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inputs, cls.bindings, cls.data = t.inputs_for(t.DEFAULT_INPUTS)

    def test_ack_only_change_to_all_three_original_generated_sources(self):
        for key, data in self.data.items():
            rendered = t.render(data)
            self.assertEqual(rendered.count(t.ACK_BLOCK), 1)
            self.assertIn(t.ACK_BLOCK + '#heading(numbering: none)[References]', rendered)
            original = rendered.replace(t.ACK_BLOCK, "", 1).encode("utf8")
            self.assertEqual(hashlib.sha256(original).hexdigest(), self.bindings['projects'][key]['original_typst_normalized_sha256'])

    def test_native_math_rejects_executable_or_latex_input(self):
        for equation in ('#read("secret")', '$ a $', r'\frac{a}{b}'):
            with self.assertRaises(ValueError):
                t.math(equation)
        self.assertEqual(t.math('frac(a,b)'), '$ frac(a,b) $')

    def test_prose_is_literal_and_citation_links_are_preserved(self):
        value = '#read("secret") [1–3] _not-code_'
        rendered = t.content(value)
        self.assertIn(json.dumps('#read("secret") ', ensure_ascii=False), rendered)
        self.assertIn('#link(<bib1>)', rendered)
        self.assertIn('[1–3]', rendered)

    def test_duplicate_and_unresolved_reference_rejected(self):
        data = copy.deepcopy(self.data['skillmerge'])
        data['references'].append(copy.deepcopy(data['references'][0]))
        with self.assertRaises(ValueError):
            t.validate(data, 'skillmerge')
        data = copy.deepcopy(self.data['skillmerge']); data['abstract'] += ' [99].'
        with self.assertRaises(ValueError):
            t.validate(data, 'skillmerge')

    def test_ragged_table_and_figure_traversal_rejected(self):
        data = copy.deepcopy(self.data['skillmerge'])
        data['sections'][0]['table'] = {'headers': ['A', 'B'], 'rows': [['A']], 'caption': 'bad'}
        with self.assertRaises(ValueError):
            t.validate(data, 'skillmerge')
        data = copy.deepcopy(self.data['skillmerge'])
        section = next(s for s in data['sections'] if s.get('figures'))
        section['figures'][0]['id'] = '../private'
        with self.assertRaises(ValueError):
            t.validate(data, 'skillmerge')

    def test_existing_output_rejected_without_mutation(self):
        with tempfile.TemporaryDirectory(dir=t.APP) as folder:
            sentinel = Path(folder) / 'keep'; sentinel.write_bytes(b'original evidence')
            with self.assertRaises(ValueError):
                t.fresh_output(Path(folder), self.inputs)
            self.assertEqual(sentinel.read_bytes(), b'original evidence')

    def test_repository_path_escape_rejected(self):
        for value in ('../outside', 'C:/private', '/outside', 'a/../b', 'a\\b'):
            with self.assertRaises(ValueError):
                t.recorded_path(value)


if __name__ == '__main__':
    unittest.main(verbosity=2)
