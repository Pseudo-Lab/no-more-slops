# Silent Reels

Use this workflow for silent explanations built from copy and selected photos, footage or diagrams. Choose the visual medium from the latest brief; do not force an infographic layout onto a requested photo-led edit. Editing a person's recorded footage around its actions may need a dedicated editing workflow. Do not add narration just because TTS is available.

## Continue the account's accepted choices

Read the current task's latest brief. Preserve the display name, colors, caption policy, punctuation, motion policy and latest format choices. Record the latest motion choice in the account brief. An explicit request for uninterrupted movement uses `motion_policy.mode: "continuous"`; approval of large editorial explanations with reading time uses `"information_linked"` and supersedes older continuous-motion instructions. A request to apply this to future editions does not ask you to regenerate already accepted videos. Keep these preferences with the task; an example account is never the global default. A new request for movement does not reopen the account identity or re-enable audio.

Translate ambiguous quality labels into concrete output dimensions. For example, 2160×3840 is a 9:16 vertical 4K delivery that satisfies a minimum-2K request. Record exact dimensions rather than promising “high resolution.” Render typography and diagrams at that resolution; increasing an old 1080p video's dimensions does not restore detail. Record source footage dimensions separately. Use the user's requested length; an approximately one-minute explanation needs enough reading time, not a fixed count of scenes.

For a silent version, remove the audio stream entirely. A mute flag or a zero-volume narration track is insufficient. Do not add TTS, music, effects or a silent AAC track. Standalone scene explanations must make sense without narration and stay long enough to read.

## Select and explain one story

For news, use the source workflow in [carousel.md](carousel.md#content-and-evidence): establish the audience's date/timezone, open the original announcement, and distinguish announced plans from released features or observed results. If the request says “today or yesterday,” use that window, inspect previous editions to avoid repeating a story, and record publication and check times. A replay example retains its historical date and is never silently relabeled today's news.

Build a sequence around what changed, how it works, a concrete example, its limits and why it matters. Link each factual scene to its sources and evidence notes. Keep necessary qualifications visible beside the claim. For instance, an eleven-minute *laundry-handling demonstration* must not imply an eleven-minute wash-and-dry cycle.

Use relevant official or authorized footage when it helps. Keep its geometry and natural colors, credit it, and record the selected time range and usage basis. An explanatory animation is not a measured benchmark or an actual product interface. Personal screenshots, editorial source videos and credentials do not belong in a reusable skill or public code contribution.

## When actual demonstrations lead the Reel

Read [demo-led-reels.md](demo-led-reels.md). Use relevant moving source footage in a large viewing area, with short, stable explanations matched to what the viewer can see. This selected treatment takes precedence over photo-motion examples and older fixed-photo defaults. Keep the account’s existing audio, UI margins, progress and caption choices.

## When the account prefers real photography

Make the relevant real subject the dominant visual. Use the account's preferred background and accent roles; a selected brand color does not require a large color field or a tint over the photo. Respect a rejected video mascot even when that character remains the profile identity.

Build variety through meaningful crops, different source images, layered depth and timed cuts. If uninterrupted motion is required, keep clearly visible subject or camera movement through reading time and transitions, such as a continuing reframe that reveals a relevant detail. A photo-led edit need not add a diagram to qualify, but an imperceptible pan or an unrelated decorative overlay is still insufficient. Keep the explanatory copy stable and verify the actual encoded video at phone size.

## When fixed-photo editorial explanations are selected

Read [editorial-reels.md](editorial-reels.md). Keep photography fixed and place large information directly across the protected screen area. Follow the selected motion style: `multi_stage_editorial` uses varied large compositions and meaningful transformations after the entrance, with brief reading holds. Use source-grounded selection, connection, grouping or branching when it helps explain the story. This selected treatment takes precedence over the moving-photo examples above, continuous-motion rules below, and an earlier light-panel choice. A small explanation box or a decorative diagram is not required.

## Compose for the actual Reels view

Instagram places controls at the top, bottom and right; their locations vary with device, crop and viewing mode. Use the user's screenshot when supplied, and treat safe-area coordinates as task-specific settings rather than a universal platform specification.

The bundled demo's older rectangle x=120–890, y=280–1440 on a 1080×1920 canvas is only a historical example. For Chihuahua AI Lab, use the approved expanded margins in its saved account brief and [editorial guide](editorial-reels.md#calibrate-space-against-the-actual-reels-screen), which leave more usable lower-screen space. Adjust other accounts' margins to their intended view. Safe-area fractions are edge insets, not coordinates.

Recompose the title, graphic, explanation and credit into that rectangle. Keep key nodes and their labels away from the right-hand action buttons. Leave only optional decoration in covered regions. Avoid burning a second handle or caption into the bottom account area. Uniformly shrinking a previous card is often less readable than simplifying copy and rearranging the graphic.

## Make motion explain the information

Use movement with a purpose: inputs converge, a value is emphasized, an object is hidden and revealed, a token moves through a process, or data arrives from multiple sources. Vary the scene structure while retaining a coherent brand. An animated number must not pass through misleading values that could be mistaken for the result.

Keep explanatory text stable during its reading interval; a staged editorial treatment can resize or reposition it between meaningful states. Use soft transitions and avoid flashing or moving all the text at once. For a complex scene, compare early, middle and late frames and watch the actual segment. Mere frame differences do not prove the animation is useful.

## When uninterrupted motion is required

Apply these acceptance rules only when the latest user instruction or selected brief still requires continuous motion. Do not apply them to an approved information-linked editorial treatment with reading holds. This is an account preference, not a requirement for unrelated accounts that ask for calmer or static content.

- Keep the primary explanatory graphic visibly active from the first frame through the last, including opening, reading time, scene transitions and the closing call to action. There is no permitted frozen hold. Before one action settles, start the next or overlap their motion so the scene stays alive.
- Make motion substantial enough to read on a phone: unfold or reorganize layers, assemble and separate objects, trace meaningful paths, move data through a process, or continuously transform the diagram. A static slide with an entrance animation, a progress bar, tiny decorative dots, subtle bobbing, camera micro-jitter or encoder noise does not satisfy this requirement by itself.
- Plan an entrance, continuing action and moving handoff for each scene. After the entrance, the primary visual must continue doing something that explains the story. Do not stretch a short animation by freezing its final frame. A still image or held source-video frame needs continuing, prominent motion, using the photo-led treatment above when selected.
- Keep explanatory copy stable for reading while graphics remain active. Continuous motion does not require shaking every label, flashing, unreadable camera moves, or animating a measured number through false values. Preserve the selected safe areas throughout the movement.
- Review the **entire encoded MP4** at normal speed and phone size, including the first/last frames and both sides of every cut. Inspect the main graphic region separately from captions, credits and progress indicators. Use frame-difference or freeze detection to locate suspect intervals, then judge whether the visible motion actually communicates; changing pixels alone cannot pass the review. Fix every stationary or merely decorative interval before delivery and record what was checked.

Save the choice in the selected account brief, for example:

```json
"motion_policy": {
  "mode": "continuous",
  "max_static_seconds": 0,
  "scope": "primary_explanatory_graphic",
  "visibility": "clearly_visible_at_phone_size",
  "explanatory_text": "stable_while_graphics_move",
  "reject_sole_motion": ["entrance_then_hold", "progress_bar", "tiny_decorative_dots", "micro_jitter"],
  "review": "full_encoded_video_and_primary_graphic_region"
}
```

These fields record production and review requirements. The current harness preserves them as brief metadata but **does not enforce continuous motion automatically**. Its existing layout demos predate this stricter requirement and are not proof of compliance. Adapt the renderer and review the resulting motion; neither `exports_verified: true` nor `--validate-only` establishes this visual criterion.

## Produce and inspect

The [local harness](reel-harness.md) can render six configurable layouts. A custom design may use another renderer, but keep the same delivery checks: exact 9:16 dimensions, requested duration/frame rate, no audio, complete decode, supported glyphs, safe-area bounds and encoded-frame previews.

Review the whole exported video at phone size, especially transitions, late-stage diagrams, credits and the bottom explanation. A preview mask is a separate review artifact, never burned into the upload. Check title punctuation and large copy using the user's style; preserve meaningful dates, decimals, abbreviations and genuine questions.

When the selected brief requires recompression review, follow [the legibility workflow](recompression.md): preserve the master, make separate 1080p/720p stress previews, and inspect text, line clarity and the selected motion policy in those files. The optional light-panel and minimum-type settings support the chosen brand; they do not certify Instagram's eventual encoding quality.

Measure the final public caption after links, media credits, hashtags and acknowledgement are included. The Chihuahua AI Lab example uses fewer than 500 characters and exactly three hashtags as account preferences. Do not turn these into universal Instagram limits. Do not truncate attribution merely to pass a count.

Deliver the actual files and record the updated brief for the next edition. Creating files, naming a branch `auto-post`, or invoking this production workflow does not authorize posting to a social account or scheduling a run. Continue external publishing only when it is actually requested through an available, authorized workflow.
