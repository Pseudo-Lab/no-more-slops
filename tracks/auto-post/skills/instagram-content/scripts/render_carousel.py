#!/usr/bin/env python3
"""Render a reviewed Instagram manifest using its own brand and local media."""
from __future__ import annotations

import argparse
from datetime import date
import json
import os
from pathlib import Path
import re
import sys
from urllib.parse import urlparse
import zipfile

from PIL import Image, ImageCms, ImageDraw, ImageFont, ImageOps

W, H, SCALE = 1080, 1350, 2
ICC = ImageCms.ImageCmsProfile(ImageCms.createProfile('sRGB')).tobytes()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def lines(value):
    if isinstance(value, str):
        return value.split('\n')
    require(isinstance(value, list) and all(isinstance(s, str) for s in value), 'Text must be a string or a list of lines.')
    return value


def valid_url(value):
    parsed = urlparse(str(value))
    return parsed.scheme in ('https', 'http') and bool(parsed.netloc)


def resolve_image(manifest_path, image):
    path = Path(image['path']).expanduser()
    return (manifest_path.parent / path).resolve() if not path.is_absolute() else path.resolve()


def read_manifest(path, brand_defaults=None):
    post = json.loads(path.read_text(encoding='utf-8'))
    require(isinstance(post, dict), 'The manifest must be an object.')
    if brand_defaults is not None:
        require(isinstance(post.get('brand', {}), dict), 'brand must be an object.')
        post['brand'] = {**brand_defaults, **post.get('brand', {})}
    require(isinstance(post.get('demo', False), bool), 'demo must be true or false.')
    if post.get('edition_date') is not None:
        require(isinstance(post['edition_date'], str), 'edition_date must be an ISO date.')
        date.fromisoformat(post['edition_date'])
    require(post.get('content_type') in ('news', 'evergreen', 'promotion'), 'content_type must be news, evergreen or promotion.')
    require(isinstance(post.get('topic'), str) and post['topic'].strip(), 'topic is required.')
    require(isinstance(post.get('caption'), str) and post['caption'].strip(), 'A finished caption is required.')
    require(isinstance(post.get('slides'), list) and post['slides'], 'At least one slide is required.')
    require(len(post['slides']) <= 99, 'At most 99 numbered files can be rendered; check current Instagram limits before publishing.')
    sources = post.get('sources', [])
    require(isinstance(sources, list), 'sources must be a list.')
    require(post.get('demo') or post['content_type'] != 'news' or sources, 'A real news post needs verified primary sources.')
    ids = set()
    for source in sources:
        require(isinstance(source, dict), 'A source must be an object.')
        for key in ('id', 'publisher', 'title', 'url', 'checked_at'):
            require(isinstance(source.get(key), str) and source[key].strip(), f'A source is missing {key}.')
        require(valid_url(source['url']), 'Source URLs must be http(s) URLs.')
        require(source['id'] not in ids, f'Duplicate source id: {source["id"]}')
        ids.add(source['id'])
    for number, slide in enumerate(post['slides'], 1):
        require(isinstance(slide, dict), f'Slide {number}: must be an object.')
        require(slide.get('layout') in ('cover', 'photo', 'facts', 'closing'), f'Slide {number}: unknown layout.')
        require(lines(slide.get('title', [])), f'Slide {number}: title is required.')
        account_intro = slide.get('account_intro', False)
        require(isinstance(account_intro, bool), f'Slide {number}: account_intro must be true or false.')
        if account_intro:
            require(slide['layout'] == 'closing' and number == len(post['slides']), f'Slide {number}: account_intro belongs on the final closing slide.')
            require(len(lines(slide['title'])) <= 2, f'Slide {number}: account intro titles may use at most two lines.')
            for key in ('intro_line', 'follow_line'):
                require(isinstance(slide.get(key), str) and slide[key].strip() and '\n' not in slide[key], f'Slide {number}: {key} must be one nonempty line.')
        references = slide.get('source_ids', [])
        require(isinstance(references, list), f'Slide {number}: source_ids must be a list.')
        needs_sources = slide.get('requires_sources', post['content_type'] == 'news' and slide['layout'] != 'closing')
        require(isinstance(needs_sources, bool), f'Slide {number}: requires_sources must be true or false.')
        require(post.get('demo') or not needs_sources or references, f'Slide {number}: connect its claims to source_ids.')
        require(all(isinstance(ref, str) and ref in ids for ref in references), f'Slide {number}: unknown source id.')
        if slide['layout'] in ('cover', 'photo', 'closing'):
            image = slide.get('image')
            require(isinstance(image, dict), f'Slide {number}: this layout needs an image.')
            require(image.get('kind') in ('official_photo', 'official_screenshot', 'provided', 'owned', 'licensed', 'illustration'), f'Slide {number}: image kind is required.')
            require(isinstance(image.get('credit'), str) and image['credit'].strip(), f'Slide {number}: image credit is required.')
            require(isinstance(image.get('path'), str), f'Slide {number}: image path is required.')
            if image['kind'].startswith('official_') or image['kind'] == 'licensed':
                require(valid_url(image.get('source_url', '')), f'Slide {number}: official or licensed media needs a source URL.')
            require(image.get('fit', 'contain') in ('contain', 'cover'), f'Slide {number}: invalid image fit.')
            if account_intro:
                require(image.get('fit', 'contain') == 'contain', f'Slide {number}: account intro image fit must be contain.')
            require(resolve_image(path, image).is_file(), f'Slide {number}: image file does not exist.')
        else:
            rows = slide.get('rows')
            require(isinstance(rows, list) and 1 <= len(rows) <= 3, f'Slide {number}: facts needs 1–3 rows.')
            for row in rows:
                require(isinstance(row, dict) and isinstance(row.get('label'), str) and isinstance(row.get('heading'), str), f'Slide {number}: fact rows need label and heading.')
                require(len(lines(row.get('detail', []))) <= 2, f'Slide {number}: use at most two detail lines per fact.')
    require(isinstance(post.get('brand'), dict), 'brand is required; supply this project\'s colors instead of inheriting another account.')
    brand = dict(post['brand'])
    require((brand.get('width', W), brand.get('height', H)) == (W, H), 'These layouts are 1080×1350. Use another layout for a different format.')
    for name in ('background', 'text'):
        require(isinstance(brand.get(name), str) and re.fullmatch(r'#[0-9a-fA-F]{6}', brand[name]) is not None, f'Invalid or missing {name} color.')
    for name in ('display_name', 'handle', 'acknowledgement'):
        require(isinstance(brand.get(name, ''), str), f'brand.{name} must be a string.')
    if any(slide.get('account_intro') for slide in post['slides']):
        for name in ('display_name', 'handle'):
            require(brand.get(name, '').strip().lstrip('@').strip(), f'brand.{name} is required for an account intro.')
    return post, brand


def find_fonts(args, post=None):
    if args.font_regular or args.font_bold:
        require(args.font_regular and args.font_bold, 'Specify both --font-regular and --font-bold.')
        regular, bold = Path(args.font_regular), Path(args.font_bold)
        require(regular.is_file() and bold.is_file(), 'A specified font file does not exist.')
        return {'regular': regular, 'bold': bold, 'heavy': bold}
    explicit = args.font_dir or os.environ.get('INSTAGRAM_FONT_DIR')
    roots = [Path(explicit).expanduser()] if explicit else [
        Path.home() / 'Library/Fonts', Path('/Library/Fonts'),
        Path('/System/Library/Fonts'), Path.home() / '.local/share/fonts',
        Path('/usr/share/fonts'), Path('C:/Windows/Fonts'),
    ]
    files = sorted(p for root in roots if root.is_dir() for p in root.rglob('*') if p.suffix.lower() in ('.otf', '.ttf', '.ttc'))
    korean = bool(re.search(r'[\uac00-\ud7af]', json.dumps(post or {}, ensure_ascii=False)))
    visible = ['LAYOUT DEMO / NOT FOR PUBLICATION', '0123456789.@-']
    if post:
        visible.extend(post.get('brand', {}).get(key, '') for key in ('display_name', 'handle'))
        for slide in post['slides']:
            for key in ('title', 'kicker', 'body', 'stat', 'stat_label', 'note', 'intro_line', 'follow_line'):
                visible.extend(lines(slide.get(key, '')))
            visible.append(slide.get('image', {}).get('credit', ''))
            for row in slide.get('rows', []):
                visible.extend([row['label'], row['heading'], *lines(row.get('detail', ''))])
    characters = set(''.join(visible)) - set(' \t\r\n')

    def supports_text(path):
        try:
            font = ImageFont.truetype(str(path), 32)
            absent = font.getmask('\U0010ffff')
            missing = (absent.size, bytes(absent))
            for char in characters:
                glyph = font.getmask(char)
                if (glyph.size, bytes(glyph)) == missing:
                    return False
            return True
        except (OSError, ValueError):
            return False

    cjk = ('pretendard', 'notosanskr', 'notosanscjk', 'applesdgothicneo')
    latin = ('notosans', 'dejavusans', 'arial', 'helvetica')
    for family in (cjk + latin if korean else latin + cjk):
        matching = [p for p in files if family in re.sub(r'[^a-z]', '', p.stem.lower()) and supports_text(p)]
        if not matching:
            continue
        regular = next((p for p in matching if 'regular' in p.stem.lower()), matching[0])
        bold = next((p for p in matching if re.search(r'[-_ ]bold$', p.stem, re.I)), regular)
        heavy = next((p for p in matching if 'black' in p.stem.lower() or 'extrabold' in p.stem.lower()), bold)
        return {'regular': regular, 'bold': bold, 'heavy': heavy}
    raise ValueError('No suitable font found. Provide --font-dir or --font-regular and --font-bold with fonts supporting your text.')


class Renderer:
    def __init__(self, post, brand, manifest, fonts):
        self.post, self.brand, self.manifest, self.fonts = post, brand, manifest, fonts
        self.font_cache, self.glyph_cache = {}, set()

    def font(self, size, weight):
        key = (size, weight)
        if key not in self.font_cache:
            self.font_cache[key] = ImageFont.truetype(str(self.fonts[weight]), round(size * SCALE))
        return self.font_cache[key]

    def text(self, x, y, value, size=36, weight='regular', width=928, bottom=1220, leading=None, align='left'):
        f = self.font(size, weight)
        for j, row in enumerate(lines(value)):
            for char in set(row):
                if char.isspace() or (weight, char) in self.glyph_cache:
                    continue
                glyph, absent = f.getmask(char), f.getmask('\U0010ffff')
                require((glyph.size, bytes(glyph)) != (absent.size, bytes(absent)), f'Font is missing {char!r}; choose a font that supports the text.')
                self.glyph_cache.add((weight, char))
            length = self.draw.textlength(row, font=f) / SCALE
            require(length <= width, f'Slide {self.number}, text too wide: {row!r}. Shorten or break the line.')
            xx = x - length if align == 'right' else x - length / 2 if align == 'center' else x
            yy = y + j * (leading or size * 1.28)
            box = self.draw.textbbox((xx * SCALE, yy * SCALE), row, font=f, anchor='lt')
            require(box[0] >= 0 and box[2] <= W * SCALE and box[1] >= 0 and box[3] <= bottom * SCALE, f'Slide {self.number}, text exceeds its region: {row!r}.')
            self.draw.text((xx * SCALE, yy * SCALE), row, font=f, fill=self.brand['text'], anchor='lt')

    def rule(self, y, width=2):
        self.draw.line((76 * SCALE, y * SCALE, 1004 * SCALE, y * SCALE), fill=self.brand['text'], width=width * SCALE)

    def picture(self, image, y, height):
        with Image.open(resolve_image(self.manifest, image)) as original:
            source = ImageOps.exif_transpose(original).convert('RGBA')
        if 'crop' in image:
            box = image['crop']
            require(isinstance(box, list) and len(box) == 4 and all(isinstance(v, (int, float)) for v in box), 'crop must contain four pixel coordinates.')
            left, top, right, lower = box
            require(0 <= left < right <= source.width and 0 <= top < lower <= source.height, 'Image crop lies outside the source.')
            source = source.crop(tuple(box))
        target = (W * SCALE, round(height * SCALE))
        require(height > 0 and y >= 0 and y + height < 1210, 'Image region is out of bounds.')
        if image.get('fit', 'contain') == 'cover':
            tile = ImageOps.fit(source, target, method=Image.Resampling.LANCZOS)
        else:
            contained = ImageOps.contain(source, target, method=Image.Resampling.LANCZOS)
            tile = Image.new('RGBA', target, self.brand['background'])
            tile.alpha_composite(contained, ((target[0] - contained.width) // 2, (target[1] - contained.height) // 2))
        self.canvas.paste(tile, (0, round(y * SCALE)), tile)

    def render(self, slide, number):
        self.number = number
        self.canvas = Image.new('RGB', (W * SCALE, H * SCALE), self.brand['background'])
        self.draw = ImageDraw.Draw(self.canvas)
        heading = 'LAYOUT DEMO' if self.post.get('demo') else self.brand.get('display_name', '')
        self.text(76, 61, heading, 34, 'heavy', width=590, bottom=110)
        self.text(1004, 67, (self.post.get('edition_date') or '').replace('-', '.'), 26, width=330, bottom=110, align='right')
        self.rule(120)
        self.rule(1244)
        handle = self.brand.get('handle', '').lstrip('@')
        footer = 'DEMO / NOT FOR PUBLICATION' if self.post.get('demo') else ('@' + handle if handle else '')
        self.text(76, 1277, footer, 23, 'bold', width=700, bottom=1320)
        self.text(1004, 1277, f'{number:02d} / {len(self.post["slides"]):02d}', 24, 'bold', width=160, bottom=1320, align='right')
        self.text(76, 166, slide.get('kicker', ''), 27, 'bold', bottom=216)
        layout = slide['layout']
        if layout == 'closing' and slide.get('account_intro'):
            self.text(76, 241, slide['title'], 78, 'heavy', leading=104, bottom=461)
            self.picture(slide['image'], 515, 430)
            self.text(540, 990, slide['intro_line'], 32, width=928, align='center')
            self.text(540, 1054, slide['follow_line'], 34, 'bold', width=928, align='center')
            self.text(540, 1130, '@' + handle, 44, 'heavy', width=928, align='center')
            self.text(76, 1198, slide['image']['credit'], 22, bottom=1234)
        elif layout in ('cover', 'photo'):
            require(len(lines(slide['title'])) <= 2, f'Slide {number}: use at most two title lines.')
            self.text(76, 241, slide['title'], 96 if layout == 'cover' else 100, 'heavy', leading=117, bottom=461)
            height = slide.get('image_height', 590 if layout == 'cover' else 520)
            require(isinstance(height, int) and 250 <= height <= 600, 'image_height must be an integer from 250 to 600.')
            y = 491 if layout == 'cover' else 470
            self.picture(slide['image'], y, height)
            self.text(76, y + height + 20, slide['image']['credit'], 23, bottom=y + height + 58)
            self.text(76, y + height + 78, slide.get('body', []), 36 if layout == 'cover' else 39, 'bold', leading=52)
        elif layout == 'facts':
            has_stat = bool(slide.get('stat'))
            self.text(76, 258, slide['title'], 106 if has_stat else 100, 'heavy', leading=123, width=590 if has_stat else 928, bottom=555)
            if has_stat:
                self.text(1004, 327, slide['stat'], 155, 'heavy', width=355, bottom=508, align='right')
                self.text(1004, 527, slide.get('stat_label', ''), 28, 'bold', width=355, bottom=575, align='right')
            self.text(76, 576, slide.get('note', ''), 24, bottom=618)
            for i, row in enumerate(slide['rows']):
                yy = 638 + i * 193
                self.rule(yy)
                self.text(76, yy + 33, row['label'], 27, 'bold', width=215, bottom=yy + 81)
                self.text(307, yy + 31, row['heading'], 39, 'bold', width=697, bottom=yy + 83)
                self.text(307, yy + 94, row.get('detail', []), 33, width=697, leading=44, bottom=yy + 184)
        else:
            require(len(lines(slide['title'])) <= 3, 'Closing titles may use at most three lines.')
            self.picture(slide['image'], 234, 570)
            self.text(76, 824, slide['image']['credit'], 23, bottom=870)
            self.text(76, 905, slide['title'], 82, 'heavy', leading=103)
        return self.canvas.resize((W, H), Image.Resampling.LANCZOS)


def output_guard(out, inputs, overwrite):
    require(all(not p.is_relative_to(out) for p in inputs), 'Keep input manifests, images and fonts outside the output directory.')
    require(not out.exists() or out.is_dir(), 'The output path is not a directory.')
    require(overwrite or not out.exists() or not any(out.iterdir()), 'Output directory is not empty; use a new directory or --overwrite.')


def source_document(post):
    parts = [f'# {post["topic"]}']
    if post.get('edition_date'):
        parts.append(f'Edition date: {post["edition_date"]}')
    if post.get('demo'):
        parts.append('LAYOUT DEMO / NOT FOR PUBLICATION')
    parts.append('## Sources')
    for source in post.get('sources', []):
        parts.append(f'- [{source["id"]}] {source["publisher"]}: {source["title"]}\n  {source["url"]}\n  Published: {source.get("published_at") or "undated"} / Checked: {source["checked_at"]}')
    parts.append('## Slide references and media')
    for n, slide in enumerate(post['slides'], 1):
        parts.append(f'### {n:02d}\nReferences: {", ".join(slide.get("source_ids", [])) or "none supplied"}')
        if image := slide.get('image'):
            parts.append(f'- Media kind: {image["kind"]}\n- Credit: {image["credit"]}\n- Filename: {Path(image["path"]).name}')
            for key in ('source_url', 'asset_url', 'timestamp', 'crop', 'fit', 'license', 'license_url', 'modifications', 'usage_note'):
                if key in image:
                    parts.append(f'- {key}: {image[key]}')
        if slide.get('evidence_note'):
            parts.append(f'Evidence/context: {slide["evidence_note"]}')
    return '\n\n'.join(parts) + '\n'


def caption_text(post, brand):
    """The exact exported caption, including credits and the final newline."""
    caption = post['caption'].strip()
    if post.get('demo'):
        caption = 'LAYOUT DEMO / NOT FOR PUBLICATION\n\n' + caption
    acknowledgement = brand.get('acknowledgement', '').strip()
    if acknowledgement and acknowledgement not in caption:
        caption += '\n\n' + acknowledgement
    return caption + '\n'


def write_outputs(out, post, brand, images, overwrite, preview_columns=3):
    require(len(images) == len(post['slides']), 'Rendered image count does not match the manifest.')
    require(type(preview_columns) is int and 1 <= preview_columns <= 4, 'preview_columns must be 1–4.')
    out.mkdir(parents=True, exist_ok=True)
    if overwrite:
        for path in out.glob('[0-9][0-9].png'):
            path.unlink()
    paths = []
    for n, image in enumerate(images, 1):
        path = out / f'{n:02d}.png'
        image.save(path, icc_profile=ICC, optimize=True)
        paths.append(path)
    columns = min(preview_columns, len(images))
    tw, th, gap = 432, 540, 18
    rows = (len(images) + columns - 1) // columns
    preview = Image.new('RGB', (columns * tw + (columns + 1) * gap, rows * th + (rows + 1) * gap), '#171717')
    for i, image in enumerate(images):
        preview.paste(image.resize((tw, th), Image.Resampling.LANCZOS), (gap + (i % columns) * (tw + gap), gap + (i // columns) * (th + gap)))
    preview.save(out / 'preview.jpg', quality=95, subsampling=0)
    (out / 'caption.txt').write_text(caption_text(post, brand), encoding='utf-8', newline='\n')
    (out / 'sources.md').write_text(source_document(post), encoding='utf-8', newline='\n')
    with zipfile.ZipFile(out / 'carousel.zip', 'w', zipfile.ZIP_DEFLATED) as archive:
        for path in paths + [out / 'caption.txt', out / 'sources.md']:
            archive.write(path, path.name)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--font-dir')
    parser.add_argument('--font-regular')
    parser.add_argument('--font-bold')
    parser.add_argument('--overwrite', action='store_true')
    args = parser.parse_args()
    path, out = args.manifest.resolve(), args.out.resolve()
    post, brand = read_manifest(path)
    fonts = find_fonts(args, post)
    inputs = [path, *fonts.values()] + [resolve_image(path, slide['image']) for slide in post['slides'] if slide.get('image')]
    output_guard(out, inputs, args.overwrite)
    renderer = Renderer(post, brand, path, fonts)
    images = [renderer.render(slide, n) for n, slide in enumerate(post['slides'], 1)]
    write_outputs(out, post, brand, images, args.overwrite)
    print(json.dumps({'output': str(out), 'slides': len(images), 'size': [W, H], 'demo': post.get('demo', False)}, ensure_ascii=False))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        raise SystemExit(1)
