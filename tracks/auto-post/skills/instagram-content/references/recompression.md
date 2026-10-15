# Legibility after resizing and recompression

Use this workflow when revising Reels that look degraded after upload, or when the selected brief requires a recompression review. Keep the approved palette, resolution, silence, UI margins and motion requirements. An upload complaint alone does not identify the cause: distinguish the local master, an app preview and the delivered Instagram stream.

## Design for the smaller result

A uniform background usually compresses efficiently. Do not claim that a solid vivid color inherently causes poor quality, or that a small file / low average bitrate proves a bad encode. Saturated color boundaries, small text and thin lines can become less clear after downscaling, chroma subsampling and additional lossy encoding. Treat this as a mechanism to check, not a diagnosis of an unseen platform stream.

- Keep the selected accent color. For the Chihuahua AI Lab brief, retain vivid orange and place explanatory body copy on a white panel with bold black type. This is an account choice, not a rule for every brand.
- Increase body and diagram-label sizes and line thickness. Shorten or reflow crowded copy instead of shrinking it. Render text and diagrams at the master resolution; upscaling a finished low-resolution frame does not restore detail.
- Keep body copy stable while the primary explanatory graphic continues moving according to the [motion policy](reels.md#when-uninterrupted-motion-is-required). A readable panel does not justify holding the main graphic still.
- Do not add grain, noise or gradients merely to increase bitrate. They can consume encoding capacity and are not a proven fix. Preserve the clean brand unless a reviewed visual experiment supports a change.

The portable renderer supports an optional selected-brief policy:

```json
"recompression_policy": {
  "body_on_light_panel": true,
  "min_body_font_at_1080": 38,
  "min_graphic_font_at_1080": 30,
  "min_line_width_at_1080": 3,
  "require_review": true
}
```

The numbers are example design floors in a 1080-pixel-wide composition, multiplied by output width / 1080. Font sizes are font pixels, not measured glyph heights. The optional fields leave unrelated accounts unchanged when omitted. The renderer applies the floors to body text, graphic labels and its line/shape primitives; header and credit copy still need manual review. The body panel is white with black text. Oversized copy fails rather than silently shrinking. Custom renderers must implement the same selected policy explicitly.

`require_review` marks the production report's `recompression_review` as **pending**. It does not launch a preview, certify legibility or change the master resolution. An `exports_verified` result covers technical export checks only.

## Make local stress previews

Run [preview_recompression.py](../scripts/preview_recompression.py) on the final silent master, in a separate review directory:

```sh
python -B /path/to/instagram-content/scripts/preview_recompression.py /path/to/reel.mp4 \
  --out /path/to/recompression-review --at 3 12 25 40 55
```

Requires the same Python/Pillow/FFmpeg/ffprobe dependencies as the Reel harness. Accepted inputs have one video stream, no audio, square pixels, no rotation metadata, SDR BT.709 tags, exact 9:16, width at least 1080, and a constant integer frame rate of 1–60 fps. Use timestamps within the actual frame range. Without `--at`, it samples three positions across the video. Executable paths can be selected with `--ffmpeg` and `--ffprobe`.

| Output | Purpose |
| --- | --- |
| `review-only-1080p.mp4` | 1080×1920 H.264/yuv420p, CRF 26, scaled from the master |
| `review-only-720p.mp4` | 720×1280, CRF 30, recompressed from the 1080p preview |
| `comparison.jpg` | Master and both derivatives at the same sampled times, displayed at phone-like width |
| `review-report.json` | Source hash, encoding settings, measured decode/dimensions/duration, and pending manual review |
| `READ-ME.txt` | Explains the review-only purpose and limitations |

These are deliberately chosen **local stress conditions**, not Instagram's documented presets, algorithm or actual uploaded results. CRF is a quality setting, not a target bitrate. The second generation tests additional loss. There is no claim that either preview matches every device or account.

The master is read without modification and its SHA-256 is checked again before delivery. Outputs are staged; encoding failures leave prior review files intact. A nonempty output directory requires `--overwrite`, which replaces only the named generated files. Publication of those files is per file, not a filesystem-wide transaction. Keep all inputs outside the output directory. Never substitute the 720p/1080p review files for an explicitly requested 4K master.

## Complete the review

Watch both full preview MP4s at normal speed and phone size. Use the contact sheet to compare selected frames; it cannot prove motion quality or full-video legibility. Inspect small Korean characters, black/orange edges, light-panel body copy, diagram labels, lines, transitions and UI overlap. Review the primary graphic separately so a moving progress bar cannot hide a static explanation.

Record the source hash, reviewed files/times, legibility findings, motion findings and corrections in a separate visual-review note. The helper deliberately leaves manual review pending; do not interpret successful encoding or pixel-difference metrics as visual approval. Rework failed scenes and regenerate the master and previews before delivery. Mark actual Instagram quality as unverified unless the posted result was inspected. Local review does not authorize posting.
