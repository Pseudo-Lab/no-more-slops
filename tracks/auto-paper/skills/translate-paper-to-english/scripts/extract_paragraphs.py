#!/usr/bin/env python3
"""List every paragraph of a .docx with a stable key so it can be translated in place.

Usage: extract_paragraphs.py INPUT.docx OUT.json [--media-dir DIR]

Writes OUT.json and prints a compact listing. Keys look like "document#12" or
"header1#0"; feed them back to apply_translation.py.
"""
import argparse
import json
import os
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from docx_common import (HANGUL_RE, MATH_T_RE, PARA_RE, part_label, plain,  # noqa: E402
                         read_docx, table_spans, text_runs)
import re  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('docx')
    ap.add_argument('out_json')
    ap.add_argument('--media-dir', help='also save embedded images here for viewing')
    a = ap.parse_args()

    paragraphs = []
    for name, xml in read_docx(a.docx).items():
        tables = table_spans(xml)
        for i, m in enumerate(PARA_RE.finditer(xml)):
            par = m.group(0)
            runs = text_runs(par)
            text = ''.join(t for _, t, _, _ in runs)
            math = ''.join(plain(x) for x in MATH_T_RE.findall(par))
            entry = {'key': f'{part_label(name)}#{i}', 'text': text}
            style = re.search(r'<w:pStyle w:val="([^"]+)"', par)
            if style:
                entry['style'] = style.group(1)
            if any(s <= m.start() < e for s, e in tables):
                entry['in_table'] = True
            if '<w:drawing' in par or '<w:pict' in par:
                entry['has_drawing'] = True
            if math:
                entry['math'] = math
            if '<w:sectPr' in par:
                entry['has_section_break'] = True
            if '<w:ins ' in par or '<w:del ' in par:
                entry['tracked_changes'] = True
            formats = {f for _, t, f, link in runs if t.strip() and not link}
            if len(formats) > 1 or any(link for *_, link in runs):
                entry['runs'] = [{'text': t, 'format': f, **({'link': True} if link else {})}
                                 for _, t, f, link in runs]
            if HANGUL_RE.search(text) or HANGUL_RE.search(math):
                entry['korean'] = True
            if text or len(entry) > 2:
                paragraphs.append(entry)

    with zipfile.ZipFile(a.docx) as zf:
        media = [n for n in zf.namelist() if n.startswith('word/media/')]
        core = zf.read('docProps/core.xml').decode('utf8') if 'docProps/core.xml' in zf.namelist() else ''
        if a.media_dir:
            os.makedirs(a.media_dir, exist_ok=True)
            for n in media:
                with open(os.path.join(a.media_dir, os.path.basename(n)), 'wb') as f:
                    f.write(zf.read(n))
    title = re.search(r'<dc:title>(.*?)</dc:title>', core, re.S)
    result = {'source': os.path.abspath(a.docx), 'title_property': plain(title.group(1)) if title else '',
              'media': media, 'paragraphs': paragraphs}
    with open(a.out_json, 'w', encoding='utf8') as f:
        json.dump(result, f, ensure_ascii=False, indent=1)

    for e in paragraphs:
        flags = [k for k in ('in_table', 'has_drawing', 'math', 'has_section_break', 'tracked_changes') if k in e]
        if 'runs' in e:
            flags.append(f"runs={len(e['runs'])}")
        mark = 'KO' if e.get('korean') else '  '
        print(f"{mark} {e['key']} [{e.get('style', '-')}]{' {' + ','.join(flags) + '}' if flags else ''} {e['text']}")
    n_ko = sum(1 for e in paragraphs if e.get('korean'))
    print(f"\n{len(paragraphs)} paragraphs listed, {n_ko} contain Korean. Images: {', '.join(media) or 'none'}")
    if result['title_property']:
        print(f"Document title property: {result['title_property']}")


if __name__ == '__main__':
    main()
