<p align="center">
  <img src="no-more-slops.png" alt="No-More-Slops — turning ideas into papers, applications, and posts" width="100%">
</p>

# No-More-Slops

**English** | [한국어](README.ko.md)

**The No-More-Slops project in Pseudo Lab's 13th cohort focuses on getting more value from tokens.**

Two outputs can cost the same in tokens yet differ in value: one goes unused, while the other solves someone's problem.

AI-generated work becomes part of culture as people use and share it.
It supports research and development and becomes material for new creations.

No-More-Slops creates and publishes work that people actually use.
It improves that work and the systems that produce it to get more value from the tokens invested.

## Schedule and team

- **Duration:** 12 weeks: onboarding in Week 1, production in Weeks 2–11, retrospective in Week 12
- **Team:** 1 builder and 11 participants. Target: 4 per track, adjusted based on applications
- **Weekly meeting:** Mondays, 21:00–23:00
- **In person:** Once a month on Monday, 20:00–22:00, replacing that week's regular meeting. Date, time, and location may change

All times are in Korea Standard Time (KST).

## Weekly targets

There are three tracks: Auto-Paper, Auto-Application, and Auto-Post.
Choose one track and complete the following during **Weeks 2–11**.

| Track | Weekly deliverables | Weekly GitHub PR | Weekly PR reviews | Total (10 production weeks) |
| --- | --- | --- | --- | --- |
| **Auto-Paper** | Write at least 1 paper | Submit and merge 1 PR | Review peers' PRs | At least 10 papers |
| **Auto-Application** | Launch at least 1 service | Submit and merge 1 PR | Review peers' PRs | At least 10 services |
| **Auto-Post** | Publish at least 3 pieces of content | Submit and merge 1 PR | Review peers' PRs | At least 30 pieces of content |

With 4 people per track, the total is **at least 200 deliverables**: 40 papers, 40 services, and 120 pieces of content.

The pace is designed to require automation and continual improvements to its quality. Assess those improvements using metrics you define for actual use.

Include deliverables, production code, reproduction instructions, metrics, and peer reviews in your PR. **Complete review, revisions, and merging within the week the PR is opened.**

## Production skills

The reusable skills in `skills/` can be installed for use across all your projects. They do not require this repository as the working directory.

| Skill | Purpose |
| --- | --- |
| [instagram-content](skills/instagram-content/SKILL.md) | Create Instagram brand identities, photo-led carousels and reference-based profile images or characters. Supply the account, topic, language, colors and media for each task. Includes optional local renderers. |
| [design-punctuation](skills/design-punctuation/SKILL.md) | Omit unnecessary terminal periods in headings, short captions and large display copy across content and web design, while preserving punctuation needed for meaning and data. |

For a first local installation, run from this repository:

```sh
mkdir -p "$HOME/.agents/skills"
cp -R skills/instagram-content "$HOME/.agents/skills/"
cp -R skills/design-punctuation "$HOME/.agents/skills/"
```

This copies a self-contained skill into Codex's user-wide discovery directory. It works outside the repository, even if the original checkout is moved. When updating, back up any changes to the installed copy before replacing it from this repository. Codex detects local skill changes automatically; if the skill does not appear, restart Codex. See the [official local-skills documentation](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills).

Example: `Use $instagram-content to make a photo-led Instagram carousel for a bookshop, using its existing brand brief.`

Colors, mascot, language and acknowledgements are task inputs, not global defaults. The earlier [Chihuahua AI example](examples/instagram/chihuahua-ai/README.md) is stored separately and loaded only when explicitly selected; it is not included in the global installation. Keep each account's brief and generated media with that account's work. The [renderer guide](skills/instagram-content/references/renderer.md) covers portable inputs and validation. Creating assets does not automatically publish them.

For recurring carousel production, the [local harness](skills/instagram-content/references/harness.md) reads the selected brief, checks the final caption and slide count, renders a contact sheet and numbered PNGs, and verifies their upload ZIP. It also exports the brief and a production report for the next run. Use `--validate-only` to check inputs before rendering:

```sh
python -m pip install -r "$HOME/.agents/skills/instagram-content/scripts/requirements.txt"
python -B "$HOME/.agents/skills/instagram-content/scripts/run_carousel.py" /path/to/post.json \
  --brief /path/to/brand-brief.json --out /path/to/output/carousel \
  --font-regular /path/to/Regular.ttf --font-bold /path/to/Bold.ttf
```

Caption limits, hashtag counts, slide counts and punctuation preferences are configurable per account. Source verification and visual review remain part of the skill workflow. The [behavioral tests](skills/instagram-content/tests/) run in CI on Python 3.10 and 3.12, including a copied installation used outside this checkout. See the [reproduction example](examples/instagram/layout-demo/README.md).

## Who should join

1. **People who can stay committed throughout the 12 weeks** (top priority)
2. People who have the AI tools needed for the project, such as Codex or Claude
3. People who are comfortable with this pace
4. People who keep trying new approaches even after failure
5. People who motivate themselves and take initiative

## What you gain

- **Hands-on automation experience:** Gain experience contributing to automation systems that turn ideas into real deliverables.
- **A personal portfolio:** Own the papers, services, or content you create during the project.
- **Peer feedback:** Review each other's work, find ways to improve, and share production know-how.

## Ownership and acknowledgement

Participants may retain their work and be paper authors, app or service owners, or owners of the accounts where they publish content.

When publishing or operating the work under your own name, **you must still include an acknowledgement** in the paper's acknowledgements, an about page or credits, or the post itself:

> This work was created as part of the No-More-Slops group activities at Pseudo Lab.

**The GitHub repository for the production systems belongs to Pseudo Lab.** Contributed code, skills, prompts, and documentation are published under the [MIT License](LICENSE), which continues to apply when participants use their deliverables under their own names.
