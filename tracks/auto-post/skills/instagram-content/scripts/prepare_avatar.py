#!/usr/bin/env python3
"""Prepare a finished square image for profile upload; does not generate art."""
import argparse
import json
from pathlib import Path
import sys
from PIL import Image, ImageCms, ImageDraw, ImageOps


def prepare(source, out, background, overwrite=False):
    source, out = source.resolve(), out.resolve()
    if source.is_relative_to(out):
        raise ValueError('Keep the source image outside the output directory.')
    if out.exists() and (not out.is_dir() or (any(out.iterdir()) and not overwrite)):
        raise ValueError('Output directory is not empty; use another directory or --overwrite.')
    with Image.open(source) as original:
        image = ImageOps.exif_transpose(original).convert('RGBA')
    if image.width != image.height:
        raise ValueError('Provide a reviewed square image; this helper does not crop faces automatically.')
    base = Image.new('RGBA', image.size, background)
    base.alpha_composite(image)
    rgb = base.convert('RGB').resize((1080, 1080), Image.Resampling.LANCZOS)
    icc = ImageCms.ImageCmsProfile(ImageCms.createProfile('sRGB')).tobytes()
    mask = Image.new('L', (2160, 2160))
    ImageDraw.Draw(mask).ellipse((0, 0, 2159, 2159), fill=255)
    rounded = rgb.convert('RGBA')
    rounded.putalpha(mask.resize((1080, 1080), Image.Resampling.LANCZOS))
    preview = Image.new('RGB', (640, 250), '#202020')
    x = 32
    for size in (180, 110, 64, 40):
        icon = rounded.resize((size, size), Image.Resampling.LANCZOS)
        preview.paste(icon, (x, (250 - size) // 2), icon)
        x += size + 28
    out.mkdir(parents=True, exist_ok=True)
    rgb.save(out / 'profile-1080.png', icc_profile=icc, optimize=True)
    rounded.resize((640, 640), Image.Resampling.LANCZOS).save(out / 'circle-preview.png', icc_profile=icc, optimize=True)
    preview.save(out / 'size-check.jpg', quality=94)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--background', required=True, help='Background chosen for this project, such as #2457FF.')
    parser.add_argument('--overwrite', action='store_true')
    args = parser.parse_args()
    prepare(args.source, args.out, args.background, args.overwrite)
    print(json.dumps({'output': str(args.out.resolve()), 'size': [1080, 1080]}))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        raise SystemExit(1)
