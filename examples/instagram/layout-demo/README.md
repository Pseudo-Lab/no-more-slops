# Portable carousel reproduction

This four-slide demo uses an original neutral graphic and fictional copy. It is visibly marked **LAYOUT DEMO / NOT FOR PUBLICATION**. Real news photos, account credentials and working media are not needed or bundled.

Install Python 3.10+, Pillow from `skills/instagram-content/scripts/requirements.txt`, and fonts supporting the supplied language. From the repository root:

```sh
python -B skills/instagram-content/scripts/run_carousel.py \
  skills/instagram-content/references/post.example.json \
  --brief skills/instagram-content/references/brief.example.json \
  --out /tmp/instagram-layout-demo \
  --font-regular /path/to/Regular.ttf --font-bold /path/to/Bold.ttf
```

Use a fresh output folder or add `--overwrite` for an intentional rerun. For another working directory, pass absolute paths to the copied skill and inputs. No path in the skill points to a developer's machine or a specific repository checkout.

The [committed contact sheet](preview.jpg) demonstrates the four layouts. The [production report](production-report.json) records the measured caption and hashtag counts, slide dimensions, export checks and remaining review work. Review the actual full-size PNGs from your run; a successful automated report does not certify visual design or source truth.

Expected outputs: 4 RGB/sRGB PNGs at 1080×1350, a two-column preview, caption, source ledger, brief, production report, and a ZIP containing exactly 6 entries (4 PNGs + caption + sources). Rendering may vary with the supplied font; fonts are not bundled.

Run the behavioral suite:

```sh
python -B -m unittest discover -s skills/instagram-content/tests -v
```
