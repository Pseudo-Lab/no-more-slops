"""Figures for the paper from ../results CSVs."""
from pathlib import Path
import pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
R = Path(__file__).resolve().parent.parent / "results"
e = pd.read_csv(R / "e2_injection.csv"); e = e[e.delta == 0.03]
fig, axs = plt.subplots(1, 2, figsize=(9, 3.4), sharey=True)
colors = {100: "#9aa5b1", 300: "#5b7a99", 870: "#2a4d73", e.n.max(): "#0b1f3a"}
for ax, mech, title in zip(axs, ["random", "systematic"], ["Random errors", "Systematic (modal distractor) errors"]):
    for n, g in e[e.mech == mech].groupby("n"):
        ax.plot(100 * g.rate, 100 * g.flip_rate, marker="o", ms=3, color=colors[n], label=f"n={n}")
    ax.axvline(0.75, ls="--", color="#c0392b", lw=1); ax.text(0.85, ax.get_ylim()[1]*0.9 if ax.get_ylim()[1] else 1, "δ/4", color="#c0392b", fontsize=8)
    ax.set_xscale("log"); ax.set_title(title, fontsize=10); ax.set_xlabel("Injected label-error rate (%)")
axs[0].set_ylabel("Pairwise decision flips (%)"); axs[0].legend(fontsize=8, frameon=False)
fig.tight_layout(); fig.savefig(R / "fig" / "fig1_flip_vs_error.png", dpi=200)

f = pd.read_csv(R / "e1_flips.csv"); s = f[(f.level == "subject") & (f.delta == 0.03)]
fig, ax = plt.subplots(figsize=(4.5, 3.4))
ax.scatter(100 * s.err_rate, 100 * s.flips / s.pairs, s=12, color="#2a4d73")
for _, r in s[s.err_rate > 0.1].iterrows(): ax.annotate(r.unit, (100 * r.err_rate, 100 * r.flips / r.pairs), fontsize=7)
ax.set_xlabel("Real label-error rate in subject (%)"); ax.set_ylabel("Decision flips after correction (%)")
ax.set_title("MMLU-Redux, 57 subjects × 861 model pairs", fontsize=9)
fig.tight_layout(); fig.savefig(R / "fig" / "fig2_subject_flips.png", dpi=200)
print("ok")
