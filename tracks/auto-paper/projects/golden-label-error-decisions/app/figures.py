"""Figures for the paper from ../results CSVs.

Writes PNGs to ../results/fig/ and, for the paper, vector PDFs plus PNGs (paper.md) to
../outputs/week-04/fig/ (the repository keeps final PDFs under outputs/). Sizes match the
ACL two-column layout (column 7.7 cm, text width 16 cm) so the 8 pt labels print at 8 pt. Latin
glyphs use STIX (Times-like, bundled with matplotlib) and Hangul falls back to Noto Serif KR, the
same pair as the paper body. The font is downloaded by build_paper.sh into FONT_DIR.
"""
import os
from pathlib import Path

import matplotlib
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

ROOT = Path(__file__).resolve().parent.parent
R = ROOT / "results"
PAPER_FIG = ROOT / "outputs/week-04/fig"
PAPER_FIG.mkdir(parents=True, exist_ok=True)
FONT_DIR = Path(os.environ.get("FONT_DIR", ROOT / "outputs/week-04/.build/fonts"))
font = FONT_DIR / "NotoSerifKR-Regular.otf"
if not font.exists():
    raise SystemExit(f"{font} not found: run app/build_paper.sh (it downloads the font) or set FONT_DIR")
font_manager.fontManager.addfont(str(font))
plt.rcParams.update({
    "font.family": ["STIXGeneral", "Noto Serif KR"], "mathtext.fontset": "stix", "font.size": 8,
    "axes.titlesize": 8, "axes.labelsize": 8, "xtick.labelsize": 7, "ytick.labelsize": 7, "legend.fontsize": 7,
    "axes.linewidth": 0.6, "xtick.major.width": 0.6, "ytick.major.width": 0.6, "xtick.minor.width": 0.4,
    "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.color": "#e3e5e8",
    "grid.linewidth": 0.5, "axes.axisbelow": True, "pdf.fonttype": 42, "savefig.bbox": "tight",
    "savefig.pad_inches": 0.02,
})
COL, TEXT = 7.7 / 2.54, 16.0 / 2.54  # inches


def save(fig, name):
    fig.savefig(PAPER_FIG / f"{name}.pdf")
    for d in (R / "fig", PAPER_FIG):
        fig.savefig(d / f"{name}.png", dpi=220)
    plt.close(fig)


e = pd.read_csv(R / "e2_injection.csv")
e = e[e.delta == 0.03]
NMAX = e.n.max()
# One-hue sequential ramp for the ordered set sizes; markers repeat the encoding for print and CVD.
style = {100: ("#5b8fc9", "o"), 300: ("#2f6db0", "s"), 870: ("#1b4f8a", "^"), NMAX: ("#0b2e5c", "D")}

# Fig 1: flip rate vs injected error rate, random vs systematic, 95% CI over repetitions.
fig, axs = plt.subplots(1, 2, figsize=(TEXT, 2.25), sharey=True)
for ax, mech, title in zip(axs, ["random", "systematic"],
                           ["(a) 무작위 오류", "(b) 체계적 오류 (어려운 문항, 대표 오답)"]):
    for n, g in e[e.mech == mech].groupby("n"):
        c, m = style[n]
        x = 100 * g.rate
        ax.fill_between(x, 100 * g.flip_ci_lo, 100 * g.flip_ci_hi, color=c, alpha=0.15, lw=0)
        ax.plot(x, 100 * g.flip_rate, color=c, lw=1.2, label=f"n = {n:,}")
        hi = g[g.rate * n >= 1]
        lo = g[g.rate * n < 1]  # expected number of corrupted items below one
        ax.scatter(100 * hi.rate, 100 * hi.flip_rate, s=12, marker=m, color=c, zorder=3, lw=0)
        ax.scatter(100 * lo.rate, 100 * lo.flip_rate, s=12, marker=m, facecolors="white", edgecolors=c,
                   lw=0.8, zorder=3)
    ax.axvline(0.75, ls="--", color="#b03a2e", lw=0.8)
    ax.text(0.8, 0.97, r"$\delta/4$", color="#b03a2e", fontsize=7, transform=ax.get_xaxis_transform(), va="top")
    ax.set_xscale("log")
    ax.set_xticks([0.25, 0.5, 1, 2, 3, 5, 12], labels=["0.25", "0.5", "1", "2", "3", "5", "12"])
    ax.minorticks_off()
    ax.set_title(title, loc="left")
    ax.set_xlabel("주입 오류율 (%)")
axs[0].set_ylabel("결정 반전율 (%)")
handles = [plt.Line2D([], [], color=c, marker=m, ms=3.5, lw=1.2, label=f"n = {n:,}") for n, (c, m) in style.items()]
axs[0].legend(handles=handles, frameon=False, loc="upper left")
fig.tight_layout(w_pad=1.5)
save(fig, "fig1_flip_vs_error")

# Fig 2: real subject error rate vs flips after correction.
f = pd.read_csv(R / "e1_flips.csv")
s = f[(f.level == "subject") & (f.delta == 0.03)]
names = {"virology": "바이러스학", "college_chemistry": "대학 화학"}
fig, ax = plt.subplots(figsize=(COL, 2.1))
ax.scatter(100 * s.err_rate, 100 * s.flips / s.pairs, s=9, color="#1b4f8a", lw=0, alpha=0.85)
for _, r in s[s.unit.isin(names)].iterrows():
    ax.annotate(names[r.unit], (100 * r.err_rate, 100 * r.flips / r.pairs), xytext=(-4, 0),
                textcoords="offset points", ha="right", va="center", fontsize=7)
ax.set_xlabel("과목의 수정 문항 비율 (%)")
ax.set_ylabel("라벨 수정 후 결정 반전율 (%)")
fig.tight_layout()
save(fig, "fig2_subject_flips")

print("ok")
