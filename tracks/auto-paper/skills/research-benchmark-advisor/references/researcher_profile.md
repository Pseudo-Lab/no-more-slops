# Researcher Profile (default) and Override Syntax

The skill evaluates every candidate against the *effective profile*: the
default below with any user overrides applied. Print the effective profile
in section A of the report, marking overridden fields.

## Default profile

### Education
- B.S. in Statistics
- Currently pursuing a post-baccalaureate B.S. in Computer Science

### Programming
- Intermediate-to-beginner proficiency
- Familiar with Python and basic ML libraries (NumPy, pandas, scikit-learn,
  PyTorch basics)
- Can read and modify code; may struggle to implement complex algorithms
  independently
- Uses AI coding agents extensively for implementation

### Mathematics
- Undergraduate statistics: probability, statistical inference,
  hypothesis testing, regression, basic linear algebra
- Limited experience with advanced deep-learning mathematics (e.g.
  variational bounds, measure-theoretic arguments, advanced optimization
  theory)

### Machine learning
- Basic understanding of supervised learning
- Familiar with fundamental ML concepts (overfitting, cross-validation,
  loss functions, gradient descent)
- Shallow understanding of deep-learning architectures and optimization
- Limited experience implementing research papers

### Research experience
- Beginner researcher
- Limited experience reproducing published research
- Uses AI tools for coding, literature review and experimentation

### Computational resources
- Access to university HPC resources
- GPU experimentation allowed
- Potential access to A40, H100, H200 and other GPUs
- **GPU availability must be verified, not assumed.** Plan for a single
  mid-range GPU (A40-class, 48 GB) as the baseline assumption; treat H100/H200
  as upside, not the plan.

### Research interests (preferences, not constraints)
- Subliminal learning
- Mechanistic interpretability
- Hidden interactions between AI models
- Multi-agent systems
- AI safety
- Unexpected or implicit model behaviors

The skill must remain open to unrelated areas when they offer significantly
better opportunities. Interest alignment is criterion 7 in the rubric
(Important), below SOTA opportunity and the four gates.

### Default constraints
This is the single global home of these defaults, shared by all research
and paper skills (shared definitions §10). Override them per project;
never hard-code them into a project.
- Time budget: **4 working days** (about 32 focused hours, including
  debugging)
- Paper target: **4-page workshop-style paper** (plus references).
  Venue profile `default-4`
  (`~/.claude/skills/paper-writer/references/venue_profiles.json`).
  Enforced on the compiled PDF by the page-limit gate.
- Priority: **defensible overall SOTA over novelty** (shared definitions
  §4f levels 1–2 targeted; §8 ranking)
- Meaningful technical depth required (shared definitions §3)
- Compute: OSU HPC GPU access (global `compute.md`)
- Prefer public code and pretrained checkpoints

### Preferences (tie-breakers, not gates)
- Interests: underlying AI mechanisms, interactions between models,
  anomaly detection (plus the research interests listed above)
- Extensibility: a topic that extends to **either** multi-agent systems
  **or** multimodal learning/robotics is preferred. Either one suffices,
  and neither is mandatory.

## Override syntax

Users override any field inline:

```
/research-benchmark-advisor profile: programming=advanced; math=graduate ML; gpu=none; interests=tabular learning, time series
```

Or point to a file:

```
/research-benchmark-advisor profile: ./my_profile.md
```

Recognized field keys (case-insensitive, synonyms accepted):

| Key | Meaning | Example values |
| --- | --- | --- |
| `education` | degrees / background | `MS CS`, `BS physics` |
| `programming` | coding level | `beginner`, `intermediate`, `advanced` |
| `math` | math background | `undergrad stats`, `graduate ML`, `minimal` |
| `ml` | ML/DL depth | `basic`, `intermediate`, `strong DL` |
| `research` | research experience | `none`, `beginner`, `1 paper`, `PhD` |
| `gpu` | compute | `none`, `single A40`, `8xH100`, `laptop only` |
| `interests` | comma-separated list | `OOD detection, calibration` |
| `days` | time budget | `4`, `6`, `10` |
| `pages` | paper length | `4`, `8` |
| `venue` | target venue profile (venue_profiles.json) | `default-4`, `neurips-workshop-4`, `cvpr`, `aaai` |
| `priority` | ranking priority | `sota` (default), `diagnostic` (waives gate 9 for a scientific-diagnostic goal) |
| `extensibility` | preferred extension direction | `multi-agent or multimodal/robotics` (default), `none` |
| `exclude` | areas or benchmarks to skip | `LLM agents, robotics` |
| `require` | hard inclusion constraints | `must use open-weight LLMs` |

Unknown keys: record them verbatim in section A under "Unrecognized
overrides" and ignore them for scoring.

## How the profile drives evaluation

| Profile fact | Effect on scoring |
| --- | --- |
| Statistics background | Favor methods whose core idea is statistical (calibration, uncertainty, selection, weighting, reweighting, robust estimation, conformal methods, mixture models); these count toward criterion 6 and lower H1 difficulty. |
| Shallow DL theory | Penalize H1 when the baseline's correctness depends on advanced DL theory the researcher cannot check. |
| Beginner reproduction experience | Require public, recently maintained code for the strongest baseline, or a benchmark with a maintained evaluation harness. |
| AI coding agents available | Reduces *implementation time* estimates modestly (not more than about 30 %) but never changes H1 (understanding) assessments. |
| Unverified GPU | Schedule must fit on one 48 GB GPU or less; multi-GPU plans are VERY LOW on feasibility until the user confirms availability. |
| Interests | Tie-breaker and criterion 7 only. |
