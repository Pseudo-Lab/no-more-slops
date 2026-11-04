#!/usr/bin/env python3
"""Finds tools that don't visibly change their output.

usage: python3 noop_audit.py RENDERS_DIR [--baseline baseline.png] [--sheet audit-sheet.jpg] [--strict]

RENDERS_DIR holds the untouched output (baseline.png) and one image per tool at full strength
(<tool>.png, same size), rendered by the app from the same input. For each tool it reports the share
of pixels that changed visibly (any channel by more than --threshold of 255), the peak change (the
99.99th percentile, so a few stray pixels don't count) and the box where the change happened, so you
can see that e.g. an arm tool changed the arm and not the face.

NO-OP (exit 1): the peak change is under --noop-peak, i.e. no more than compression noise.
WEAK (fails only with --strict): the peak stays under --min-peak or under --min-changed of the pixels
changed visibly; it is there but hard to see on a phone. Check it on the contact sheet.
The contact sheet shows baseline, render and the change amplified x4 with its box, one row per tool.
Needs Pillow (pip install Pillow).
"""
import argparse
import pathlib
import sys

from PIL import Image, ImageChops, ImageDraw


def measure(base, render, threshold):
    diff = ImageChops.difference(base, render)
    r, g, b = diff.split()
    peak = ImageChops.lighter(ImageChops.lighter(r, g), b)
    hist = peak.histogram()
    total = base.width * base.height
    changed = sum(hist[threshold + 1:]) / total
    running, top = 0, 0
    for value in range(255, -1, -1):
        running += hist[value]
        if running >= total * 0.0001:
            top = value
            break
    box = peak.point(lambda v: 255 if v > threshold else 0).getbbox()
    return diff, changed, top, box


def thumb(image, height):
    return image.resize((max(1, round(image.width * height / image.height)), height), Image.LANCZOS)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("renders", type=pathlib.Path)
    parser.add_argument("--baseline", default="baseline.png")
    parser.add_argument("--threshold", type=int, default=8, help="per-channel change (0-255) that counts as visible")
    parser.add_argument("--noop-peak", type=int, default=4, help="peak change below which a tool is a no-op")
    parser.add_argument("--min-peak", type=int, default=16, help="peak change below which a tool is weak")
    parser.add_argument("--min-changed", type=float, default=0.0005, help="share of visibly changed pixels below which a tool is weak")
    parser.add_argument("--sheet", default="audit-sheet.jpg", help="contact sheet written into RENDERS_DIR ('' to skip)")
    parser.add_argument("--strict", action="store_true", help="WEAK fails too")
    args = parser.parse_args()

    base_path = args.renders / args.baseline
    base = Image.open(base_path).convert("RGB")
    tools = sorted(p for p in args.renders.iterdir()
                   if p.suffix.lower() in {".png", ".jpg", ".jpeg"} and p.name != args.baseline and p.name != args.sheet)
    if not tools:
        sys.exit(f"no tool renders next to {base_path}")
    rows, failed = [], False
    for path in tools:
        render = Image.open(path).convert("RGB")
        if render.size != base.size:
            print(f"FAIL {path.stem}: size {render.size} differs from baseline {base.size}")
            failed = True
            continue
        diff, changed, peak, box = measure(base, render, args.threshold)
        if peak < args.noop_peak:
            status = "NO-OP"
        elif peak < args.min_peak or changed < args.min_changed:
            status = "WEAK"
        else:
            status = "OK"
        failed |= status == "NO-OP" or (args.strict and status == "WEAK")
        where = f"box {box}" if box else "no visible change"
        print(f"{status:5} {path.stem}: {changed:.2%} pixels changed, peak {peak}, {where}")
        rows.append((path.stem, status, render, diff, box))

    if args.sheet and rows:
        height, gap, label = 320, 8, 22
        cells = []
        for name, status, render, diff, box in rows:
            amplified = diff.point(lambda v: min(255, v * 4))
            if box:
                ImageDraw.Draw(amplified).rectangle(box, outline=(255, 64, 64), width=max(2, base.width // 200))
            cells.append((f"{name}  {status}", [thumb(base, height), thumb(render, height), thumb(amplified, height)]))
        width = max(sum(t.width for t in imgs) + gap * 2 for _, imgs in cells)
        sheet = Image.new("RGB", (width, len(cells) * (height + label + gap)), "white")
        draw = ImageDraw.Draw(sheet)
        y = 0
        for title, imgs in cells:
            draw.text((4, y + 4), title, fill="black")
            x = 0
            for t in imgs:
                sheet.paste(t, (x, y + label))
                x += t.width + gap
            y += height + label + gap
        out = args.renders / args.sheet
        sheet.save(out, quality=88)
        print(f"sheet: {out} (baseline | render | change x4)")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
