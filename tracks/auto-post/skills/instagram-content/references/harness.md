# Repeatable carousel production

Use `scripts/run_carousel.py` when an account has a saved brief and needs repeatable checks and exports. It runs entirely locally with Python 3.10+ and `scripts/requirements.txt`. Research, selection of licensed images and copywriting happen before this step; the harness does not browse, generate images or publish posts.

## Run from any project

```sh
python -B /path/to/instagram-content/scripts/run_carousel.py /path/to/post.json \
  --brief /path/to/brand-brief.json --out /path/to/output/carousel \
  --font-regular /path/to/Regular.ttf --font-bold /path/to/Bold.ttf
```

Use `--validate-only` to check inputs and caption policies without writing files or loading fonts. It does not check glyphs, overflow or visual quality. For a full run, select language-compatible fonts as described in [renderer.md](renderer.md).

The [example manifest](post.example.json) and [example brief](brief.example.json) provide a runnable four-slide layout demo. They are not a real news item or a default account. Copy them and replace the inputs for real work. Image paths resolve relative to `post.json`, so a copied installation works from another working directory without this repository.

## Brief as the account input

The brief supplies `brand.background`, `brand.text`, `account.display_name`, `account.handle`, `acknowledgement`, and `deliverable.width`/`height`. `post.json` may omit `brand` entirely. If it repeats a supplied setting, that value must agree with the brief; update the intended input explicitly instead of silently reverting an accepted identity. Hex color case and a leading `@` do not count as a change. Fields absent from the brief can still be supplied in the post.

Optional policies are task-specific:

```json
{
  "deliverable": {"type": "carousel", "width": 1080, "height": 1350, "slides": 10, "preview_columns": 2},
  "caption_policy": {"max_characters": 499, "hashtag_count": 3},
  "punctuation_policy": {
    "headlines": "omit_terminal_period",
    "short_captions": "omit_terminal_period",
    "large_display_copy": "omit_terminal_period"
  }
}
```

These values illustrate the Chihuahua AI Lab brief, not platform-wide rules. Omit a policy when the account has no such constraint. `slides` is an exact count. `preview_columns` allows 1–4 (harness default: 2). `hashtag_count` is exact; use `max_hashtags` for a ceiling instead. Set `max_characters: 499` to require fewer than 500 characters.

Caption checks run on the exact export after any acknowledgement and demo label are added. The count includes spaces, line breaks, source links, hashtags, credits and the final newline, using Unicode code points. This is a documented local counting convention, not a guarantee about every platform's treatment of emoji or URLs. Hashtag counting recognizes Unicode word tags such as `#AI뉴스` and ignores URL fragments. Source and license text that belongs in the public caption must already be included by the author; the tool never invents or truncates it to pass a limit.

Punctuation findings are **review candidates**, not auto-corrections or blocking errors. The harness scans the ends of title/kicker blocks, row headings and configured display-copy fields. It also flags a single-line caption opening of up to 100 characters when separated from the rest by a blank line. It cannot infer the role of every caption or text already embedded in a picture. Preserve meaningful periods in numbers, versions, URLs, abbreviations and verbatim quotes. Review all large display copy using the [design-punctuation skill](../../design-punctuation/SKILL.md) when installed; the harness works without that optional skill.

## Sources and media

Use the renderer's `sources` and per-slide `source_ids`. Optional `evidence_note` records which passage or context supports a slide. Images may record `license`, `license_url`, `modifications` and `usage_note` in addition to source/asset URLs and crop coordinates. These fields are preserved in `sources.md` and its ZIP copy. A source link or `official_photo` label is not proof of permission; check the original terms and include any required public credit or license notice.

## Outputs and failure behavior

The harness stages a full render, then reopens the PNGs, checks RGB/sRGB and dimensions, and verifies ZIP order and byte-for-byte agreement with the caption, sources and slides. Only after those checks pass does it replace generated files in the destination. Validation, font and render failures leave an earlier delivery intact. A nonempty destination requires `--overwrite`; unrelated files are retained, stale numbered pages are removed. Keep input files and fonts outside the output directory.

Outputs:

- `01.png` onward, `preview.jpg`, `caption.txt`, `sources.md`, `carousel.zip`
- `brand-brief.json`, the selected brief for the next edition
- `production-report.json`, measured counts, punctuation candidates and export-check status

The upload ZIP contains only numbered slides, caption and sources. It excludes the brief, working images, fonts and report. Keep the original manifest and working assets in the task workspace for reproduction. `--validate-only` returns `exports_verified: false`; successful exports still require checking the actual images and source claims. Never represent the automated report as factual, legal or visual approval.

Run regression checks with:

```sh
python -B -m unittest discover -s /path/to/instagram-content/tests -v
```

The suite covers caption boundaries including credits, Korean hashtags, account changes, failed reruns, ordered ZIPs, license metadata, source links, overflow, profile crops and a copied skill executed from an unrelated project.
