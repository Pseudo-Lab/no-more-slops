# Optional 4:5 renderer

This deterministic helper renders reviewed local content into four editorial layouts. It is not a news researcher, an image generator or the mandatory appearance of every account. It has no network access or repository configuration dependency.

For repeatable production from a saved brief, use the [harness](harness.md), which calls this renderer and checks account policies and the finished package.

## Run from any directory

Use Python 3.10+ and Pillow (`scripts/requirements.txt`). Select installed font files supporting the output language; fonts are not bundled. The helper accepts `--font-regular` and `--font-bold`, or searches `--font-dir`, `INSTAGRAM_FONT_DIR` and common system font folders. Discovery is a convenience, not a guarantee of language support. Missing glyphs fail the render. For complex-script shaping or another typographic style, use a suitable font and rendering tool and visually review it.

```sh
python -B /path/to/instagram-content/scripts/render_carousel.py /path/to/post.json \
  --out /path/to/output/carousel \
  --font-regular /path/to/Regular.ttf --font-bold /path/to/Bold.ttf
```

Paths to images are relative to the input JSON, never to the shell's current directory. The skill itself can be copied anywhere. It does not read a brand file from the installation or an enclosing repository. Nonempty output directories are refused unless `--overwrite` is explicit; keep all inputs and fonts outside the output directory. Overwrite replaces numbered slide PNGs and generated caption/preview/source/ZIP files; use a dedicated output directory.

## Manifest

[post.example.json](post.example.json) is a complete runnable **layout demo** with a neutral graphic fixture. Its names, colors and copy are illustrative, never defaults. For actual content, supply real media and reviewed text and remove `demo: true`; do not publish the fixture as a real post.

Required fields:

- `content_type`: `news`, `evergreen` or `promotion`.
- `topic`, `caption`: nonempty strings.
- `brand`: `background` and `text` hex colors. Optional `display_name`, `handle` (with or without @) and `acknowledgement`. All identity fields can be omitted. No organization credit is added unless supplied.
- `slides`: nonempty array. Numbered filenames support at most 99 slides; this is a helper limit, **not** a statement about Instagram's upload limit.

Optional `edition_date` is an ISO date displayed in the header, not an assumed latest-news date. Optional `demo: true` prints a conspicuous demonstration label. `brand.width` and `brand.height`, if provided, must be 1080 and 1350. For another format use a different layout/tool.

`sources` is a list of `{id, publisher, title, url, checked_at, published_at?}`. Use actual opened originals. URL must be http(s). Store exact check time with timezone when freshness matters. Use the original publication date where known; omit it for genuinely undated material and explain uncertainty in the copy.

Each slide may reference known IDs with `source_ids`. News requires sources and references on non-closing slides by default. `requires_sources` explicitly controls a slide's evidence requirement: use true for factual claims in evergreen, promotional or closing slides; false only for genuinely source-free personal opinion, editorial framing or calls to action. This flag does not exempt factual content from verification. Sources are not required merely to render original creative copy. Demo mode bypasses source requirements because it is visibly non-publishable.

## Layouts and images

All layouts support `kicker`, `title` (string or list of lines) and `source_ids`.

- `cover`: at most two title lines, large `image`, and short `body` lines.
- `photo`: at most two title lines, `image`, and short `body`. Cover and photo allow `image_height` from 250 to 600 pixels.
- `facts`: `rows` containing one to three `{label, heading, detail}` objects. `detail` has at most two lines. Optional `stat`, `stat_label`, `note` support a numeric callout.
- `closing`: image and a title of at most three short lines. Put longer follow-up copy in the caption.

An account-introduction variant uses `layout: "closing"` and `account_intro: true` on the final page. Supply at most two title lines, one-line nonempty `intro_line` and `follow_line`, and `brand.display_name`/`brand.handle` (or their selected brief values). The renderer places the title above a contained character image, then the account description, follow invitation and handle. It displays the image credit below. `image.fit` must be `contain` to preserve the character. All text still fails on overflow rather than shrinking. Existing closing slides without this flag keep their original layout; no account or mascot is built into the renderer.

Images require `path`, `kind` and nonempty `credit`. Kinds: `official_photo`, `official_screenshot`, `provided`, `owned`, `licensed`, `illustration`. Official/ licensed media also requires `source_url`; optionally record `asset_url`, video `timestamp`, pixel `crop: [left, top, right, bottom]` and `fit`.

Optional image `license`, `license_url`, `modifications` and `usage_note` are preserved in the source ledger. Optional slide `evidence_note` records the supporting passage or context. These records do not grant rights or replace any credit required in the image or public caption.

Default `fit: contain` preserves the whole picture on the supplied background. Use `cover` only when a reviewed central crop suits the content. Text is placed outside the picture. Source credit text is drawn on the slide, so make it concise; full URLs go in source metadata. Overlong copy or out-of-bounds crops fail rather than shrinking silently. Adjust copy/line breaks or choose another layout.

## Exports and checks

Outputs: numbered PNGs, `preview.jpg`, `caption.txt`, `sources.md`, `carousel.zip`. PNGs are RGB with an sRGB profile. The ZIP contains upload PNGs and caption/source text, excluding original media and fonts. The source ledger has neutral English field labels; translate them in the final handoff when useful. Post copy and captions stay in the supplied language.

Run the behavioral checks after changing a helper:

```sh
python -B -m unittest discover -s /path/to/instagram-content/tests -v
```

They cover different brands and content types, source requirements, overflow, original preservation, optional acknowledgement and avatar cropping. Font-dependent tests need a suitable installed font. Tests do not replace viewing the generated images.
