# Instagram production

[한국어](README.ko.md)

Owner: [유민형 · gogoymh](https://github.com/gogoymh). Original contribution: [PR #5](https://github.com/Pseudo-Lab/no-more-slops/pull/5).

All repository commands below run from the repository root. The canonical skills live in `tracks/auto-post/skills/`; account inputs live in `examples/` and shared production results in [outputs/week-01/](outputs/week-01/README.md).

## Production skills

The reusable skills in `tracks/auto-post/skills/` can be installed for use across all your projects. They do not require this repository as the working directory.

| Skill | Purpose |
| --- | --- |
| [instagram-content](../../skills/instagram-content/SKILL.md) | Create Instagram brand identities, photo-led carousels and reference-based profile images or characters. Supply the account, topic, language, colors and media for each task. Includes optional local renderers. |
| [design-punctuation](../../skills/design-punctuation/SKILL.md) | Omit unnecessary terminal periods in headings, short captions and large display copy across content and web design, while preserving punctuation needed for meaning and data. |

For a first local installation, run from this repository:

```sh
mkdir -p "$HOME/.agents/skills"
cp -R tracks/auto-post/skills/instagram-content "$HOME/.agents/skills/"
cp -R tracks/auto-post/skills/design-punctuation "$HOME/.agents/skills/"
```

This copies a self-contained skill into Codex's user-wide discovery directory. It works outside the repository, even if the original checkout is moved. When updating, back up any changes to the installed copy before replacing it from this repository. Codex detects local skill changes automatically; if the skill does not appear, restart Codex. See the [official local-skills documentation](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills).

Example: `Use $instagram-content to make a photo-led Instagram carousel for a bookshop, using its existing brand brief.`

Colors, mascot, language and acknowledgements are task inputs, not global defaults. The earlier [Chihuahua AI example](examples/chihuahua-ai/README.md) is stored separately and loaded only when explicitly selected; it is not included in the global installation. Keep each account's brief and generated media with that account's work. The [renderer guide](../../skills/instagram-content/references/renderer.md) covers portable inputs and validation. Creating assets does not automatically publish them.

For recurring carousel production, the [local harness](../../skills/instagram-content/references/harness.md) reads the selected brief, checks the final caption and slide count, renders a contact sheet and numbered PNGs, and verifies their upload ZIP. It also exports the brief and a production report for the next run. Use `--validate-only` to check inputs before rendering:

```sh
python -m pip install -r "$HOME/.agents/skills/instagram-content/scripts/requirements.txt"
python -B "$HOME/.agents/skills/instagram-content/scripts/run_carousel.py" /path/to/post.json \
  --brief /path/to/brand-brief.json --out /path/to/output/carousel \
  --font-regular /path/to/Regular.ttf --font-bold /path/to/Bold.ttf
```

Caption limits, hashtag counts, slide counts and punctuation preferences are configurable per account. Source verification and visual review remain part of the skill workflow. The [behavioral tests](../../skills/instagram-content/tests) run in CI on Python 3.10 and 3.12, including a copied installation used outside this checkout. See the [reproduction example](examples/layout-demo/README.md).
