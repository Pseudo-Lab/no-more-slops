"""Report page count of the built PDF and render each page to PNG for visual inspection.

Usage:
    uv run check_pdf.py [--pdf ../outputs/week-03/paper.pdf] [--png-dir DIR] [--max-pages 4]
"""
import argparse
from pathlib import Path

import pypdfium2 as pdfium

ROOT = Path(__file__).resolve().parent.parent


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--pdf", type=Path, default=ROOT / "outputs" / "week-03" / "paper.pdf")
    parser.add_argument("--png-dir", type=Path)
    parser.add_argument("--max-pages", type=int, default=4)
    args = parser.parse_args()

    doc = pdfium.PdfDocument(args.pdf)
    n = len(doc)
    print(f"pages: {n} (limit {args.max_pages}) -> {'OK' if n <= args.max_pages else 'OVER'}")
    last = doc[n - 1].get_textpage().get_text_range()
    print(f"last page characters: {len(last)}")
    if args.png_dir:
        args.png_dir.mkdir(parents=True, exist_ok=True)
        for old in args.png_dir.glob("page-*.png"):  # drop pages from earlier, longer renders
            old.unlink()
        for i in range(n):
            doc[i].render(scale=1.6).to_pil().save(args.png_dir / f"page-{i + 1}.png")
        print(f"rendered to {args.png_dir}")


if __name__ == "__main__":
    main()
