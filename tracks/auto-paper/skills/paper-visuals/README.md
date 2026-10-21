# paper-visuals

Adds the **smallest set of scientifically justified visuals** to one paper
(`.md` or `.tex`): tables, statistical plots, and workflow, methodology,
architecture, pipeline or algorithm diagrams. **Every value and every
arrow** is checked against the manuscript and any evidence files. It
renders each figure reproducibly, inspects every render visually, and
inserts the figures into a *copy* of the paper.

It is a communication skill, not a research skill. It never invents
results, steps or feedback loops, never runs experiments, and never
overwrites your paper. "No new visuals needed" is an acceptable outcome.

## How to use it

```
/paper-visuals <paper_file> [format:<venue/page limit>] [evidence:<dir>] [free-text instructions]
```

Examples:

```
/paper-visuals paper_RQ1_v2.md
/paper-visuals paper.tex format:"4-page two-column, refs excluded" evidence:experiments_RQ1/outputs
/paper-visuals paper.md tables only, no architecture figure
```

| Argument | Meaning |
| --- | --- |
| `paper_file` | Required. `.md`, `.markdown` or `.tex` |
| `format:` | Venue, column layout or page limit. Overrides what is inferred from the paper. |
| `evidence:` | Extra folder(s) to search for CSV/JSON results, scripts, configs and logs (can be repeated) |
| free text | Preferences such as "tables only" or "appendix allowed". These never override the skill's restrictions. |

## How it decides

It reads the whole paper, finds and verifies the evidence, reviews the
existing visuals, generates candidate visuals, and scores each one against
the page budget. For diagrams it first builds a step table and draws only
the steps that are listed. Tools used: Matplotlib, Graphviz, Mermaid or
hand-written SVG.

## Output (next to the paper)

```
<stem>_visuals.<ext>          # paper copy with the visuals inserted
<stem>_figures/
    figN_<slug>.pdf / .svg / .png
    src/figN_<slug>.py|.dot|.mmd|.svg   # editable sources
    src/README.md                        # how to regenerate each figure
<stem>_visuals_audit.md       # selected and rejected visuals, data provenance, discrepancies, QC
```

## Next step

`<stem>_figures/` can be passed directly to paper-to-latex:

```
/paper-to-latex <stem>_visuals.md --visuals <stem>_figures/
```
