# Repeatable silent Reel production

`scripts/run_reel.py` turns a reviewed JSON episode plus an explicit account brief into a video package. Python 3.10+, Pillow (in `scripts/requirements.txt`), FFmpeg with libx264, ffprobe, and fonts supporting the copy are required. No repository checkout, OpenCV, cloud account, TTS provider or credential is needed after copying the skill.

```sh
python -B /path/to/instagram-content/scripts/run_reel.py /path/to/episode.json \
  --brief /path/to/reel-brief.json --out /path/to/output/reel \
  --font-regular /path/to/Regular.ttf --font-bold /path/to/Bold.ttf
```

`--validate-only` checks manifests, source links, date windows, duration math and caption policies without writing files, invoking FFmpeg or loading fonts. It does not inspect media codecs, glyphs, layout or visuals. Full runs can select executable paths with `--ffmpeg` and `--ffprobe`. Font discovery also supports `--font-dir` and `INSTAGRAM_FONT_DIR`; explicit font files are preferred for reproduction.

## Inputs

Copy [reel.example.json](reel.example.json) and [reel-brief.example.json](reel-brief.example.json). Together they run a 60-second, 2160×3840, seven-scene **design exercise**, using only original diagrams and a bundled illustration. Their demo labels are intentional. Select an account-specific brief explicitly; there is no automatic lookup or account fallback.

Brief fields:

| Field | Meaning |
| --- | --- |
| `account.display_name`, `brand.background`, `brand.text` | Required account identity and two hex colors |
| `deliverable.type`, `audio` | `reel` and `none` for this harness |
| `width`, `height`, `fps`, `duration_seconds` | Exact output; dimensions must be even and 9:16 |
| `min_short_side` | Optional enforceable pixel floor, independent of vague “2K” labels |
| `min_scene_seconds` | Optional account reading-time floor |
| `safe_area.left/top/right/bottom` | Fractional **edge insets**, not coordinates; at least half the canvas width and height must remain for these layouts |
| `caption_policy` | Same count/hashtag rules as [the carousel harness](harness.md#brief-as-the-account-input) |
| `punctuation_policy`, `acknowledgement` | Task-specific preferences, never global organization defaults |
| `motion_policy` | Optional account production/review requirements; continuous motion is **not** automatically validated by this harness |
| `recompression_policy` | Optional white body panel, minimum body/graphic type and line widths, plus a pending review requirement; see [legibility after recompression](recompression.md) |

An episode declares `schema_version: 1`, `content_type`, `edition_date`, `topic`, `caption`, `sources` and `scenes`. Account/brand overrides in the episode are rejected to prevent accidental drift. The output caption includes the optional acknowledgement, demo marker and final newline before counts are checked.

Each scene supplies a unique `id`, `layout`, `duration`, 1–2 `title` lines, 1–2 complete `body` lines, an optional `kicker`, and an on-screen `credit`. Scene durations must resolve to whole frames and add up exactly. No copy is silently truncated or shrunk to fit; overflow and missing glyphs fail the run.

| Layout | `visual` fields | Motion |
| --- | --- | --- |
| `flow` | 2–5 `nodes`, each `{symbol, label}`; 1–2 `center` lines | Signals converge, nodes pulse |
| `steps` | 2–3 `items`, each `{symbol, label}`; optional `token`, `note` | A token travels in sequence |
| `occlusion` | `cover_label`, `memory_label`, optional `note` | Hide, retain a location cue, reveal |
| `cards` | 1–3 `items`, each `{symbol, label, detail}` | Staggered explanation and data markers |
| `metric` | `value`, `label`, `note` | Value entrance and emphasis, no misleading count-up |
| `media` | Optional `label`; scene also needs `media` below | Original image or source-video motion |

When `motion_policy.mode` is `continuous`, follow [the uninterrupted-motion acceptance rules](reels.md#when-uninterrupted-motion-is-required). The stock layouts and example exports do not guarantee prominent motion throughout a scene; entrances that settle, tiny moving symbols, progress bars and held media frames cannot satisfy that requirement by themselves. Adapt the primary graphic animation and inspect the encoded video. A successful technical report does not certify continuous motion.

Symbols are short text glyphs supported by the selected fonts; letters/numbers work without platform emoji differences. Templates target concise copy. Change the copy or the renderer if a topic needs a different composition rather than forcing all stories into these examples.

## Sources, time and local media

Sources use `{id, publisher, title, url, checked_at}` and optional `published_at`. News scenes require valid `source_ids` and an `evidence_note`, unless the episode is explicitly a design demo. Set `requires_sources: false` for an editorial question, not to hide factual claims. Source existence is validated; source truth and usage rights are not automated.

For an optional recency check, supply `freshness: {reference_time: "2026-10-15T12:00:00+09:00", max_age_hours: 48}`. At least one timestamped source must be in that window, and no supplied publication can be in the future relative to it. Timestamps need timezone offsets. Choose the audience's current time when authoring; the harness does not reinterpret a saved episode using its host clock.

Media scenes accept `{kind: "image" | "video", path, credit, usage_note}` plus optional source/license URLs and text. Paths resolve relative to the episode, including when the skill is installed elsewhere. Only local files are opened. Video may specify `start` and `duration`; ranges are checked against the source. A shorter selected range holds its final frame for the rest of the scene. The source is contained in a 16:9 graphic window without stretching. Audio is never decoded into the export. Source dimensions are recorded so an output labeled 4K is not confused with native-4K footage.

## Exports and verification

The package contains `reel.mp4`, `cover.jpg`, `preview.jpg`, `safe-area-preview.jpg`, `caption.txt`, `subtitles.srt`, `sources.md`, `brand-brief.json` and `production-report.json`. The review masks appear only in the separate safe-area preview. Source media and local input paths are not bundled into the package.

The report checks the encoded dimensions, whole-frame count, duration, H.264/yuv420p, BT.709 tags, exactly one video stream, zero audio streams and a full decoder pass. Text and geometry are rasterized directly at the requested resolution. Text and bounded shapes are checked throughout rendering, with their measured region bounds recorded. Body copy stays fixed throughout each scene. The report also contains caption counts and punctuation **review candidates**, which do not rewrite the input.

The renderer checks type regions as well as outer safety margins, but it is not a general collision detector for arbitrary custom drawings. Inspect the encoded contact sheet, masked preview and moving MP4. The report is not factual, legal, aesthetic or platform-upload approval. Instagram may transcode a file after upload.

For selected briefs with `recompression_policy.require_review`, the report explicitly leaves that review pending. Run [preview_recompression.py](../scripts/preview_recompression.py) on the master, then follow the [manual review steps](recompression.md#complete-the-review). It creates separate review-only videos and verifies their technical properties; it cannot pass visual review or simulate Instagram exactly.

Rendering occurs in a temporary staging directory. Input, font, source, layout and encode failures leave the previous delivery intact. Use a new output directory, or `--overwrite` to replace the generated package while retaining unrelated files. Keep all input files outside the output directory. The final file replacement is per file, not a filesystem-wide atomic transaction.

Run the existing and Reel regression checks together:

```sh
python -B -m unittest discover -s /path/to/instagram-content/tests -v
```

The tests exercise native 4K output, actual decoding and source-audio removal, fixed explanations with moving graphics, safe-area bounds, input failure preservation, date windows, caption limits, and a copied skill launched from an unrelated working directory.
