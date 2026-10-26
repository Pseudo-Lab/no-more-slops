#!/usr/bin/env python3
"""Validate a task brief, render a carousel, and verify its upload package locally."""
from __future__ import annotations

import argparse
import io
import json
from pathlib import Path
import re
import sys
import tempfile
from zipfile import ZipFile

from PIL import Image, ImageCms

import render_carousel as render


def object_field(parent, key):
    value = parent.get(key, {})
    render.require(isinstance(value, dict), f'{key} must be an object.')
    return value


def integer_field(parent, key, minimum=0):
    value = parent.get(key)
    if key in parent:
        render.require(type(value) is int and value >= minimum, f'{key} must be an integer >= {minimum}.')
    return value


def read_brief(path):
    brief = json.loads(path.read_text(encoding='utf-8'))
    render.require(isinstance(brief, dict), 'The brief must be an object.')
    account = object_field(brief, 'account')
    brand = object_field(brief, 'brand')
    delivery = object_field(brief, 'deliverable')
    caption = object_field(brief, 'caption_policy')
    object_field(brief, 'punctuation_policy')
    render.require(delivery.get('type', 'carousel') == 'carousel', 'This harness supports carousel deliverables.')
    integer_field(delivery, 'slides', 1)
    columns = integer_field(delivery, 'preview_columns', 1)
    render.require(columns is None or columns <= 4, 'preview_columns must be 1–4.')
    integer_field(caption, 'max_characters', 1)
    integer_field(caption, 'hashtag_count')
    integer_field(caption, 'max_hashtags')
    # Only the selected brief supplies identity. No repository/global brand lookup.
    expected = {key: brand[key] for key in ('background', 'text') if key in brand}
    render.require(len(expected) == 2, 'The brief needs brand.background and brand.text.')
    for key in ('display_name', 'handle'):
        if key in account:
            render.require(isinstance(account[key], str), f'account.{key} must be a string.')
            expected[key] = account[key]
    for key in ('width', 'height'):
        if key in delivery:
            expected[key] = delivery[key]
    if 'acknowledgement' in brief:
        expected['acknowledgement'] = brief['acknowledgement']
    return brief, expected


def hashtag_count(caption):
    # URL fragments are not social hashtags. Unicode \w includes Korean tags.
    without_urls = re.sub(r'https?://\S+', '', caption)
    return len(re.findall(r'(?<![\w/#])#\w+', without_urls))


def punctuation_findings(post, policy):
    """Review candidates only: never rewrite copy, abbreviations, URLs or quotes."""
    findings = []

    def inspect(field, value):
        text = '\n'.join(render.lines(value)).rstrip()
        if text.endswith(('.', '。', '．')):
            findings.append({'field': field, 'text': text, 'reason': 'Review the terminal period in display copy; preserve meaningful punctuation and verbatim quotations.'})

    for i, slide in enumerate(post['slides'], 1):
        prefix = f'slide {i}'
        if policy.get('headlines') == 'omit_terminal_period':
            for key in ('title', 'kicker'):
                inspect(f'{prefix}.{key}', slide.get(key, ''))
            for j, row in enumerate(slide.get('rows', []), 1):
                inspect(f'{prefix}.row {j}.heading', row['heading'])
        if policy.get('large_display_copy') == 'omit_terminal_period':
            for key in ('body', 'stat', 'stat_label', 'note', 'intro_line', 'follow_line'):
                inspect(f'{prefix}.{key}', slide.get(key, ''))
    if policy.get('short_captions') == 'omit_terminal_period':
        # A short standalone opening is a candidate, not the whole prose caption.
        parts = post['caption'].strip().split('\n\n', 1)
        if len(parts) == 2 and '\n' not in parts[0] and len(parts[0]) <= 100:
            inspect('caption opening', parts[0])
    return findings


def preflight(manifest, brief_path):
    brief, expected = read_brief(brief_path)
    post, brand = render.read_manifest(manifest, brand_defaults=expected)
    for key, value in expected.items():
        actual = brand[key]
        if key in ('background', 'text'):
            actual, value = actual.upper(), value.upper()
        if key == 'handle':
            actual, value = actual.lstrip('@'), value.lstrip('@')
        render.require(actual == value, f'brand.{key} differs from the selected brief. Update the intended input explicitly.')
    delivery = brief.get('deliverable', {})
    count = len(post['slides'])
    if 'slides' in delivery:
        render.require(count == delivery['slides'], f'The brief requests {delivery["slides"]} slides; the manifest has {count}.')
    caption = render.caption_text(post, brand)
    tags = hashtag_count(caption)
    policy = brief.get('caption_policy', {})
    if 'max_characters' in policy:
        render.require(len(caption) <= policy['max_characters'], f'Final caption has {len(caption)} characters; maximum is {policy["max_characters"]}, including credits, spaces and newlines.')
    if 'hashtag_count' in policy:
        render.require(tags == policy['hashtag_count'], f'Final caption has {tags} hashtags; the brief requests exactly {policy["hashtag_count"]}.')
    if 'max_hashtags' in policy:
        render.require(tags <= policy['max_hashtags'], f'Final caption has {tags} hashtags; maximum is {policy["max_hashtags"]}.')
    report = {
        'schema_version': 1,
        'demo': post.get('demo', False),
        'slides': count,
        'dimensions': [render.W, render.H],
        'caption_characters': len(caption),
        'character_count_method': 'Unicode code points, including final newline',
        'hashtags': tags,
        'sources': len(post.get('sources', [])),
        'punctuation_review': punctuation_findings(post, brief.get('punctuation_policy', {})),
        'exports_verified': False,
        'manual_review': ['Open the exported slides and contact sheet to review crops, typography and phone-size readability.',
                          'Check that originals support each claim, dates are accurate and media rights/credits are satisfied. The harness does not research or certify these.'],
    }
    return post, brand, brief, report


def verify_exports(out, post, brand):
    names = [f'{n:02d}.png' for n in range(1, len(post['slides']) + 1)]
    render.require(sorted(p.name for p in out.glob('[0-9][0-9].png')) == names, 'Unexpected numbered slide files.')
    for name in names:
        with Image.open(out / name) as image:
            image.load()
            render.require(image.size == (render.W, render.H) and image.mode == 'RGB', f'{name}: expected RGB 1080×1350.')
            profile = image.info.get('icc_profile')
            render.require(profile, f'{name}: missing color profile.')
            profile_name = ImageCms.getProfileName(ImageCms.ImageCmsProfile(io.BytesIO(profile)))
            render.require('srgb' in profile_name.lower(), f'{name}: expected sRGB.')
    expected_caption = render.caption_text(post, brand).encode('utf-8')
    render.require((out / 'caption.txt').read_bytes() == expected_caption, 'Exported caption differs from the checked caption.')
    with Image.open(out / 'preview.jpg') as preview:
        preview.verify()
    with ZipFile(out / 'carousel.zip') as archive:
        render.require(archive.testzip() is None, 'Upload ZIP is corrupt.')
        render.require(archive.namelist() == names + ['caption.txt', 'sources.md'], 'Upload ZIP contains unexpected or missing files.')
        for name in archive.namelist():
            render.require(archive.read(name) == (out / name).read_bytes(), f'Upload ZIP has a stale {name}.')


def run(args):
    manifest, brief_path = args.manifest.resolve(), args.brief.resolve()
    post, brand, brief, report = preflight(manifest, brief_path)
    if args.validate_only:
        return report
    render.require(args.out is not None, '--out is required unless --validate-only is used.')
    out = args.out.resolve()
    fonts = render.find_fonts(args, post)
    inputs = [manifest, brief_path, *[p.resolve() for p in fonts.values()]]
    inputs += [render.resolve_image(manifest, s['image']) for s in post['slides'] if s.get('image')]
    render.output_guard(out, inputs, args.overwrite)
    out.parent.mkdir(parents=True, exist_ok=True)
    # Failed validation/rendering does not replace an earlier successful delivery.
    with tempfile.TemporaryDirectory(prefix='.carousel-', dir=out.parent) as temporary:
        stage = Path(temporary)
        renderer = render.Renderer(post, brand, manifest, fonts)
        images = [renderer.render(slide, n) for n, slide in enumerate(post['slides'], 1)]
        columns = brief.get('deliverable', {}).get('preview_columns', 2)
        render.write_outputs(stage, post, brand, images, False, columns)
        verify_exports(stage, post, brand)
        report['exports_verified'] = True
        report['zip_entries'] = len(images) + 2
        (stage / 'production-report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        (stage / 'brand-brief.json').write_text(json.dumps(brief, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        render.output_guard(out, inputs, args.overwrite)
        out.mkdir(parents=True, exist_ok=True)
        for path in sorted(stage.iterdir()):
            path.replace(out / path.name)
        for path in out.glob('[0-9][0-9].png'):
            if int(path.stem) > len(images) or path.stem == '00':
                path.unlink()
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path)
    parser.add_argument('--brief', type=Path, required=True)
    parser.add_argument('--out', type=Path)
    parser.add_argument('--validate-only', action='store_true', help='Check inputs and caption policies without rendering or writing files.')
    parser.add_argument('--font-dir')
    parser.add_argument('--font-regular')
    parser.add_argument('--font-bold')
    parser.add_argument('--overwrite', action='store_true')
    args = parser.parse_args()
    print(json.dumps(run(args), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        raise SystemExit(1)
