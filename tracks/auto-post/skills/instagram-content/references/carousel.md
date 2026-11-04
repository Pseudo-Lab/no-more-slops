# Carousel production

## Content and evidence

Use the requested topic, audience and language. Choose a narrative suited to the content: a news update can lead with the change and then show its use and conditions; a guide can explain a problem, steps and examples; a product post can show a benefit and verifiable details. Each slide should communicate one useful point. Do not stretch a short story to fill a fixed page count.

For **latest news**, establish the current date and the audience's relevant region/timezone. If no time window is given, the past week is a useful initial search window, not a definition of latest. Open original announcements, release notes or other primary sources. Search snippets alone do not establish a claim. Record announcement dates, check dates, current versus planned behavior, rollout limits, region, subscription and the basis for numerical claims. Distinguish an unannounced region from a confirmed exclusion. Do not label old material as current or a preview as a released product. If current sources cannot be checked, explain the limit and offer a dated or visibly labeled design demo.

For **evergreen guides and promotions**, research externally verifiable assertions as needed. Personal advice, the user's own creative copy and a call to action do not require invented news sources. Never fabricate statistics, user testimonials, product capabilities or first-hand experience. Separate sourced facts, interpretation and speculation.

Maintain a compact source ledger linking claims to originals. In the helper manifest use `source_ids` per slide; set `requires_sources: true` for externally verifiable claims in non-news posts and in a closing slide. The renderer validates links exist, not whether they prove the claim.

## Photos and layout

Follow the selected brand's colors, typography, density and tone. Photo-led requests need actual relevant images or screenshots, not a typography-only substitute. Preserve the natural colors of photographs unless an intentional treatment is requested.

Choose material for the point each slide makes:

1. User-provided or owned media, or the announcement's official photos/screenshots.
2. Relevant frames from an official demonstration, recording timestamp and context.
3. Properly licensed editorial or stock photography where it suits the story.
4. Explanatory illustration or generated imagery when appropriate, clearly distinguished from real products, interfaces or events.

Use asset URLs observed on source pages. Record source page, credit, asset URL and any crop or video timestamp. Do not invent service screenshots or alter factual interface details to fill space. Observe stated rights conditions; public availability is not proof of unrestricted reuse. Never commit downloaded editorial photos or personal reference screenshots to the reusable skill.

Use a strong cover, a clear reading order and varied images. Do not repeat one image across the real carousel unless repetition serves the story. Tables or text-only slides can be appropriate for comparisons or conditions. Shorten copy, add a slide or change the layout when text does not fit; avoid shrinking type until it is illegible.

## Account-introduction closing

When the user or selected account brief asks for it, reserve the final page for the account: a short statement of what it publishes, the actual display name/handle, a relevant follow invitation and its existing approved character. Reuse the saved brand asset instead of inventing a mascot or redrawing it. Keep the account's main background and typography; a small orange character circle can carry the brand accent without filling the page. Do not invent a posting schedule, audience size or credentials.

For 치와와 AI Lab, the saved carousel brief selects this closing treatment while the news pages remain photo-led. The character belongs on the closing page only; this does not change the Reel's saved treatment. For other accounts, use their own explicit brief.

The optional renderer supports `layout: "closing"` with `account_intro: true`, a two-line `title`, `intro_line`, `follow_line` and a contained character image. Identity comes from the supplied brand/brief. Read [renderer.md](renderer.md) for the fields and limits. Use `requires_sources: false` for original account copy and a follow invitation; externally verifiable claims still require evidence. Keep any required image attribution visible.

## Produce and review

Write the finished slide copy and caption before rendering. Keep all slides the same requested size. Use the bundled renderer only when its four layouts suit the brief; a new brand does not have to inherit its typography, image positions or dimensions. Read [renderer.md](renderer.md) for its exact limits.

For repeated editions, use the [production harness](harness.md) with the account's saved brief. Put display name, caption length/hashtag constraints and punctuation preferences in that brief, not in the global skill. Measure the finished caption with source links, credits, acknowledgements, spaces and line breaks included. Recheck it after any edit and rebuild the ZIP so the packaged caption matches the final file.

Inspect actual PNGs and the contact sheet. Check title/body hierarchy, crop, contrast, font support, source labels, page order and readability at phone size. Confirm the caption matches the images and includes only relevant credits or explicitly applicable acknowledgements. Deliver the files rather than only the storyboard.
