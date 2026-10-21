# Available Compute Resources

## OSU College of Engineering HPC

### Cluster Overview

- ~130 servers
- >5,500 CPU cores
- >250 GPUs
- >50 TB total RAM
- 500 TB global fast scratch storage

### Known GPU Hardware

| GPU | VRAM per GPU | Example node configuration |
|---|---:|---:|
| NVIDIA H200 | 140 GB | 8 GPUs/node |
| NVIDIA H100 | 80 GB | 8 GPUs/node |
| NVIDIA L40S | 48 GB | 4–8 GPUs/node |
| NVIDIA A40 | 48 GB | 2–8 GPUs/node |
| NVIDIA V100 | 32 GB | 16 GPUs/node |
| NVIDIA RTX 8000 | 44 GB | 8 GPUs/node |
| NVIDIA RTX 6000 | 22–24 GB | 2–8 GPUs/node |
| NVIDIA T4 | 15 GB | 6 GPUs/node |
| NVIDIA M60 | 8 GB | 2 GPUs/node |

### User-Visible Slurm Partitions

- ampere
- dgx2
- dgxh
- eecs
- gpu
- preempt
- share

### Partition Access and Limits

| Partition | Account access | Max job duration | Max GPUs | GPU-time limit |
|---|---|---:|---:|---:|
| share | ALL | 14 days | 2 | 2 GPU-days |
| dgxh | ALL | 2 days | 8 | 2 GPU-days |
| dgx2 | ALL | 7 days | 16 | 8 GPU-days |
| gpu | eecs | 7 days | 8 | 8 GPU-days |
| ampere | ALL | 2 days | 2 | 2 GPU-days |
| eecs | eecs | 7 days | 8 | 8 GPU-days |
| preempt | ALL | 7 days | none specified | none specified |

GPU-time limits describe the amount of GPU allocation that may be
running at one time.

Examples:
- dgxh: 1 GPU × 2 days, 2 GPUs × 1 day, 4 GPUs × 12 hours,
  or 8 GPUs × 6 hours.
- dgx2: 1 GPU × 7 days, 2 GPUs × 4 days, 4 GPUs × 2 days,
  8 GPUs × 1 day, or 16 GPUs × 12 hours.
- ampere: 1 GPU × 2 days or 2 GPUs × 1 day.

### Confirmed Cluster-Wide GPU Availability

The following suitable configurations exist on the cluster:

- H200: 140 GB VRAM
- H100: 80 GB VRAM
- L40S: 48 GB VRAM
- A40: 48 GB VRAM
- V100: 32 GB VRAM
- RTX 8000: 44 GB VRAM

The cluster documentation explicitly supports requesting a GPU by
type using Slurm constraints, for example:

    srun -p preempt --gres=gpu:1 --constraint=a40 --pty bash

### User-Specific Availability

Documentation indicates that the following partitions accept ALL
accounts:

- share
- dgxh
- dgx2
- ampere
- preempt

The following require specific accounts:

- gpu: eecs account
- eecs: eecs account

However, documentation-level eligibility is not equivalent to a
personally confirmed successful allocation.

Exact GPU models successfully allocated by this user: UNKNOWN

Maximum GPUs personally confirmed in one job: UNKNOWN

Maximum simultaneous GPU allocation personally confirmed: UNKNOWN

Observed queue/wait-time constraints: UNKNOWN

### Confirmed User Access

No GPU configuration has yet been personally confirmed by a
successful user job.

For each successfully tested configuration, record:

- Partition:
- GPU type:
- GPU count:
- CPU count:
- Memory:
- Maximum confirmed job duration:
- Interactive or batch:
- Evidence/status: CONFIRMED

### Source of Truth

This file (global path
`C:\Users\<user>\.claude\skills\compute-planner\references\compute.md`,
i.e. `~/.claude/skills/compute-planner/references/compute.md`) is the
single authoritative source of research compute resources for every
pipeline stage.

- Any project-local `compute.md` is only a mirror of this file. It is
  never a required input and never a fallback source.
- If a local copy is missing, empty, a template, or differs from this
  file, ignore it and use this file. A missing or empty local copy never
  implies that GPUs are unavailable.
- If this global file itself cannot be read, report compute as UNKNOWN
  (not UNAVAILABLE) and ask the user; do not plan as if no GPU exists.
- Newer compute facts the user gives in the current conversation take
  precedence; record them here so every stage sees them.

### Feasibility Rules

Do not assume unrestricted access or guaranteed scheduling. Cluster
documentation establishes Hardware Fit and Documented Access; only a
successful job from the user's account establishes Confirmed Access.

For each proposed experiment, report these separately:

- Hardware Fit:
  Whether suitable hardware exists on the OSU HPC cluster
  (YES / NO).

- Documented Access:
  Whether the required partition is documented as open to the user's
  account category (YES for share, dgxh, dgx2, ampere, preempt;
  UNKNOWN for gpu and eecs, which need an eecs account).

- Allocation Status:
  CONFIRMED (a successful user job is recorded under Confirmed User
  Access) or UNVERIFIED (documented but not yet tested).

- Queue / Wait Time:
  KNOWN (observed) or UNKNOWN.

Status labels:

- DOCUMENTED-AVAILABLE: Hardware Fit YES and Documented Access YES,
  Allocation Status UNVERIFIED. This is the default status of the
  H200, H100, A40 and V100 configurations listed above when requested
  on an all-account partition (share, dgxh, dgx2, ampere, preempt)
  within that partition's documented GPU and GPU-time limits. Which GPU
  types each partition holds is not documented here; the day-0 test
  job confirms it.
- CONFIRMED-AVAILABLE: Allocation Status CONFIRMED.
- UNAVAILABLE: only with positive evidence: the hardware does not exist
  on the cluster, the requirement exceeds documented partition limits
  (GPU count, job duration, GPU-time), or the only suitable partition
  requires an account the user is known not to hold.
- UNKNOWN: an input needed to decide is missing (for example eecs-account
  partitions, or queue time).

Rules:

1. Unverified allocation is UNKNOWN, never UNAVAILABLE.
2. Unknown queue or wait time is UNKNOWN, never UNAVAILABLE.
3. GPU-based research is considered by default. Single-GPU experiments
   with 7B–8B models (inference, probing, activation analysis, steering,
   LoRA/QLoRA) fit one A40 (48 GB), H100 (80 GB) or H200 (140 GB),
   and 7B–8B fp16 inference fits one V100 (32 GB). These are
   DOCUMENTED-AVAILABLE and must be evaluated, not excluded.
4. A DOCUMENTED-AVAILABLE GPU design may be rated FEASIBLE or RISKY on
   its compute margin (EASY requires CONFIRMED-AVAILABLE). Record User
   Feasibility as UNKNOWN (allocation unverified) and treat it as a RISK
   with a concrete mitigation, not as a rejection or a downgrade by
   itself:
   - a day-0 test job on an all-account partition, e.g.
     `srun -p share --gres=gpu:1 -t 00:15:00 nvidia-smi` or
     `srun -p ampere --gres=gpu:1 --constraint=a40 -t 00:15:00 nvidia-smi`;
   - at least one alternative partition or GPU type (share, ampere,
     dgxh, dgx2, preempt);
   - pre-downloading weights while other work proceeds;
   - a named smaller or quantised fallback that keeps the question.
5. Do not prefer a CPU-only or API-only design over a GPU design solely
   because GPU allocation is unverified. Compare designs on research
   merit and duration fit.
6. Designs that exceed one all-account partition's documented limits
   (for example more than 2 GPUs on share/ampere, or more than 2
   GPU-days on dgxh) need Confirmed Access or a scope reduction before
   they count as fitting a short duration.
7. Once a configuration is confirmed, record it under Confirmed User
   Access so later runs use it.
