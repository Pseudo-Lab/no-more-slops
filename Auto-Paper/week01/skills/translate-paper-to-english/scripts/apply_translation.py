#!/usr/bin/env python3
"""Write a translated copy of a .docx, keeping all formatting, equations, tables and images.

Usage: apply_translation.py INPUT.docx SPEC.json OUTPUT.docx

SPEC.json:
{
  "translations": {
    "document#5": "Whole paragraph in English.",          # text goes into the first run
    "document#16": ["Bold lead-in.", " Rest of text."]     # one string per <w:t>, keeps per-run formatting
  },
  "delete": ["document#1"],                                # optional: paragraphs to remove
  "title": "English title for the file properties"         # optional
}

The input file is never modified. Exit status is 1 when Korean text remains or the
spec does not fit the document; numeric mismatches are printed as warnings to review.
"""
import json
import os
import re
import sys
import zipfile
from collections import Counter
from xml.dom import minidom
from xml.sax.saxutils import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from docx_common import (HANGUL_RE, MATH_T_RE, PARA_RE, T_RE, part_label, plain,  # noqa: E402
                         read_docx, table_spans, text_runs)

NUM_RE = re.compile(r'\d+(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?')


def numbers(s):
    return Counter(n.replace(',', '') for n in NUM_RE.findall(s))


def t_element(text):
    return '<w:t xml:space="preserve">' + escape(text) + '</w:t>' if text else '<w:t></w:t>'


def main():
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    src, spec_path, dst = sys.argv[1:]
    if os.path.abspath(src) == os.path.abspath(dst):
        sys.exit('Refusing to overwrite the input file; choose a different output path.')
    with open(spec_path, encoding='utf8') as f:
        spec = json.load(f)
    trans = dict(spec.get('translations', {}))
    delete = set(spec.get('delete', []))
    errors, warnings, used = [], [], set()

    new_parts = {}
    for name, xml in read_docx(src).items():
        label = part_label(name)
        tables = table_spans(xml)
        counter = [-1]

        def rewrite(m):
            counter[0] += 1
            key = f'{label}#{counter[0]}'
            par = m.group(0)
            if key in delete:
                used.add(key)
                if '<w:sectPr' in par:
                    errors.append(f'{key}: holds a section break, so it cannot be deleted; translate or blank it instead')
                    return par
                if any(s <= m.start() < e for s, e in tables):
                    errors.append(f'{key}: is inside a table cell, so it cannot be deleted; set it to "" instead')
                    return par
                return ''
            if key not in trans:
                return par
            used.add(key)
            value = trans[key]
            runs = text_runs(par)
            source_text = ''.join(t for _, t, _, _ in runs)
            if isinstance(value, list):
                if len(value) != len(runs):
                    errors.append(f'{key}: list has {len(value)} items but the paragraph has {len(runs)} text runs')
                    return par
                new_texts = list(value)
            else:
                targets = [i for i, r in enumerate(runs) if not r[3]]
                if not targets:
                    errors.append(f'{key}: no text run outside hyperlinks; use the list form')
                    return par
                new_texts = [t for _, t, _, _ in runs]
                for i in targets:
                    new_texts[i] = ''
                new_texts[targets[0]] = value
            out, last = [], 0
            for (tm, *_), text in zip(runs, new_texts):
                out.append(par[last:tm.start()])
                out.append(t_element(text))
                last = tm.end()
            out.append(par[last:])
            new_par = re.sub(r'<w:proofErr [^>]*/>', '', ''.join(out))
            a, b = numbers(source_text), numbers(''.join(new_texts))
            if a != b:
                missing, extra = sorted((a - b).elements()), sorted((b - a).elements())
                warnings.append(f'{key}: numbers differ - only in source {missing}, only in translation {extra}')
            return new_par

        new_xml = PARA_RE.sub(rewrite, xml)
        try:
            minidom.parseString(new_xml.encode('utf8'))
        except Exception as e:  # malformed XML would make Word refuse the file
            errors.append(f'{name}: result is not well-formed XML ({e})')
        new_parts[name] = new_xml

    for key in sorted((set(trans) | delete) - used):
        errors.append(f'{key}: no such paragraph in the document')

    with zipfile.ZipFile(src) as zin:
        core = None
        if spec.get('title') and 'docProps/core.xml' in zin.namelist():
            core = zin.read('docProps/core.xml').decode('utf8')
            core = re.sub(r'<dc:title>.*?</dc:title>|<dc:title/>',
                          lambda _: '<dc:title>' + escape(spec['title']) + '</dc:title>', core, count=1, flags=re.S)
        if not errors:
            os.makedirs(os.path.dirname(os.path.abspath(dst)), exist_ok=True)
            with zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED) as zout:
                for item in zin.infolist():
                    if item.is_dir():
                        continue
                    if item.filename in new_parts:
                        data = new_parts[item.filename].encode('utf8')
                    elif item.filename == 'docProps/core.xml' and core is not None:
                        data = core.encode('utf8')
                    else:
                        data = zin.read(item.filename)
                    zout.writestr(item.filename, data)

    leftovers = []
    for name, xml in new_parts.items():
        label = part_label(name)
        for i, m in enumerate(PARA_RE.finditer(xml)):
            body = ''.join(plain(x) for x in T_RE.findall(m.group(0)) + MATH_T_RE.findall(m.group(0)))
            if HANGUL_RE.search(body):
                leftovers.append(f'{label}#{i}: {body[:80]}')
        outside = PARA_RE.sub('', xml)
        stray = HANGUL_RE.findall(''.join(T_RE.findall(outside) + MATH_T_RE.findall(outside)))
        if stray:
            leftovers.append(f'{label}: Korean text outside the indexed paragraphs (text box host or equation): {stray[:5]}')

    for w in warnings:
        print('WARNING', w)
    for e in errors:
        print('ERROR', e)
    for line in leftovers:
        print('KOREAN LEFT', line)
    if errors:
        sys.exit('\nNothing was written. Fix the spec and run again.')
    print(f'\nWrote {dst}: {len(used - delete)} paragraphs translated, {len(delete)} deleted, '
          f'{len(warnings)} number warnings, {len(leftovers)} places with Korean left.')
    if leftovers:
        print('Note: keys above are numbered in the OUTPUT; if paragraphs were deleted, '
              'match them to the source by their text.')
        sys.exit(1)


if __name__ == '__main__':
    main()
