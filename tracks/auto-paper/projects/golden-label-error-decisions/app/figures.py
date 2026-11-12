"""Figures for the paper from ../results CSVs."""
from pathlib import Path
import pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt

R = Path(__file__).resolve().parent.parent / "results"
e = pd.read_csv(R / "e2_injection.csv"); e = e[e.delta == 0.03]
NMAX = e.n.max()
colors = {100: "#9aa5b1", 300: "#5b7a99", 870: "#2a4d73", NMAX: "#0b1f3a"}

# Fig 1: flip rate vs injected error rate, random vs systematic, with 95% CI over repetitions.
fig, axs = plt.subplots(1, 2, figsize=(9, 3.4), sharey=True)
for ax, mech, title in zip(axs, ["random", "systematic"],
                           ["Random errors", "Systematic errors (hard items → modal distractor)"]):
    for n, g in e[e.mech == mech].groupby("n"):
        x = 100 * g.rate
        ax.plot(x, 100 * g.flip_rate, marker="o", ms=3, color=colors[n], label=f"n={n}")
        ax.fill_between(x, 100 * g.flip_ci_lo, 100 * g.flip_ci_hi, color=colors[n], alpha=0.15, lw=0)
        low = g[g.rate * n < 1]  # expected number of corrupted items below one
        ax.scatter(100 * low.rate, 100 * low.flip_rate, s=22, facecolors="white", edgecolors=colors[n], zorder=3)
    ax.axvline(0.75, ls="--", color="#c0392b", lw=1)
    ax.text(0.78, 0.97, "δ/4", color="#c0392b", fontsize=8, transform=ax.get_xaxis_transform(), va="top")
    ax.set_xscale("log"); ax.set_title(title, fontsize=10); ax.set_xlabel("Injected label-error rate (%)")
axs[0].set_ylabel("Pairwise decision flips (%)"); axs[0].legend(fontsize=8, frameon=False)
fig.text(0.01, 0.01, "Open markers: expected corrupted items < 1. Bands: 95% CI over repetitions. δ = 3 pp.",
         fontsize=7, color="#555")
fig.tight_layout(rect=(0, 0.03, 1, 1)); fig.savefig(R / "fig" / "fig1_flip_vs_error.png", dpi=200)

# Fig 2: real subject error rate vs flips after correction.
f = pd.read_csv(R / "e1_flips.csv"); s = f[(f.level == "subject") & (f.delta == 0.03)]
pairs = int(s.pairs.iloc[0])
fig, ax = plt.subplots(figsize=(4.5, 3.4))
ax.scatter(100 * s.err_rate, 100 * s.flips / s.pairs, s=12, color="#2a4d73")
for _, r in s[s.err_rate > 0.1].iterrows():
    ax.annotate(r.unit, (100 * r.err_rate, 100 * r.flips / r.pairs), fontsize=7)
ax.set_xlabel("Corrected-label share in subject (%)"); ax.set_ylabel("Decision flips after correction (%)")
ax.set_title(f"MMLU-Redux, 57 subjects × {pairs} model pairs", fontsize=9)
fig.tight_layout(); fig.savefig(R / "fig" / "fig2_subject_flips.png", dpi=200)

# Fig 3: 2x2 ablation and no-label-error baselines at n=870.
order = [("swap", "Swap items (no label error)"), ("drop", "Drop items (no label error)"),
         ("random", "Uniform items, random label"), ("hard_random", "Hard items, random label"),
         ("uniform_modal", "Uniform items, modal label"), ("systematic", "Hard items, modal label")]
g = e[(e.n == 870) & (e.rate == 0.03)].set_index("mech")
fig, ax = plt.subplots(figsize=(5.2, 3.0))
names = [lab for m, lab in order if m in g.index]
vals = [100 * g.loc[m, "flip_rate"] for m, _ in order if m in g.index]
err = [[100 * (g.loc[m, "flip_rate"] - g.loc[m, "flip_ci_lo"]) for m, _ in order if m in g.index],
       [100 * (g.loc[m, "flip_ci_hi"] - g.loc[m, "flip_rate"]) for m, _ in order if m in g.index]]
cols = ["#b8c2cc", "#b8c2cc", "#5b7a99", "#5b7a99", "#2a4d73", "#2a4d73"][: len(names)]
ax.barh(names, vals, xerr=err, color=cols, capsize=2)
ax.invert_yaxis(); ax.set_xlabel("Pairwise decision flips (%)")
ax.set_title("n = 870, perturbed share 3%, δ = 3 pp", fontsize=9); ax.tick_params(axis="y", labelsize=8)
fig.tight_layout(); fig.savefig(R / "fig" / "fig3_ablation.png", dpi=200)
print("ok")
