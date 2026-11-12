"""Experiments: do golden-set label errors flip model-selection decisions?

E1  natural experiment: original MMLU labels vs MMLU-Redux corrected labels.
E2  controlled injection: random vs systematic (plausible-distractor) label errors,
    at several error rates and golden-set sizes; decision flips vs clean labels.
E3  audit operating characteristic for the review's zero-error audit rule.
Outputs CSV/JSON to ../results and figures to ../results/fig.
"""
import json, itertools
from pathlib import Path
import numpy as np, pandas as pd
from scipy import stats
from load import load

OUT = Path(__file__).resolve().parent.parent / "results"
(OUT / "fig").mkdir(parents=True, exist_ok=True)
DELTAS = [0.0, 0.01, 0.02, 0.03, 0.05]
Z = 1.96


def decide(C, delta):
    """C: items x models correctness (0/1). Returns models x models decision matrix:
    +1 if column model j beats row model i (diff >= delta and paired 95% CI excludes 0),
    -1 if i beats j, 0 inconclusive."""
    n = C.shape[0]
    m = C.mean(0)
    D = m[None, :] - m[:, None]
    # paired variance of (c_j - c_i)
    cov = (C.T @ C) / n - np.outer(m, m)
    var = np.diag(cov)[None, :] + np.diag(cov)[:, None] - 2 * cov
    se = np.sqrt(np.maximum(var, 0) / n)
    lo, hi = D - Z * se, D + Z * se
    out = np.zeros_like(D, dtype=int)
    out[(D >= delta) & (lo > 0)] = 1
    out[(D <= -delta) & (hi < 0)] = -1
    return out


def flip_stats(Cref, Cobs, delta):
    a, b = decide(Cref, delta), decide(Cobs, delta)
    iu = np.triu_indices(Cref.shape[1], 1)
    a, b = a[iu], b[iu]
    return dict(pairs=len(a), flips=int((a != b).sum()), reversals=int((a * b == -1).sum()),
                lost=int(((a != 0) & (b == 0)).sum()), spurious=int(((a == 0) & (b != 0)).sum()),
                ref_decided=int((a != 0).sum()))


def kendall(Cref, Cobs):
    return stats.kendalltau(Cref.mean(0), Cobs.mean(0)).statistic


def e1(r, P):
    S = r.status.isin(["ok", "corrected"]).values
    Y = P.values
    C_all = (Y == r.answer.values[:, None]).astype(float)
    C_orig = C_all[S]
    C_clean = (Y[S] == r.clean.values[S][:, None]).astype(float)
    acc = pd.DataFrame({"model": P.columns, "acc_published": C_all.mean(0), "acc_orig_S": C_orig.mean(0),
                        "acc_clean_S": C_clean.mean(0)})
    acc["shift_pp"] = 100 * (acc.acc_clean_S - acc.acc_orig_S)
    acc = acc.sort_values("acc_clean_S", ascending=False)
    acc.to_csv(OUT / "e1_model_accuracy.csv", index=False)
    # where do real errors point? fraction of corrected items whose original (wrong) label equals
    # the modal wrong answer among models, vs chance (1/3)
    corr = (r.status == "corrected").values
    modal_wrong = modal_wrong_answer(Y, r.clean.values)
    real = dict(n_items=int(len(r)), n_S=int(S.sum()), n_corrected=int(corr.sum()),
                n_unresolved=int((r.status == "unresolved").sum()),
                err_rate_S=float(corr.sum() / S.sum()),
                orig_label_is_modal_distractor=float((r.answer.values[corr] == modal_wrong[corr]).mean()),
                model_acc_on_orig_label_corrected_items=float((Y[corr] == r.answer.values[corr][:, None]).mean()),
                model_acc_on_fixed_label_corrected_items=float((Y[corr] == r.clean.values[corr][:, None]).mean()),
                model_acc_on_ok_items=float((Y[r.status.values == "ok"] == r.answer.values[r.status.values == "ok"][:, None]).mean()))
    rows = []
    for d in DELTAS:
        for scope, ref, obs in [("orig_S", C_clean, C_orig), ("published_all", C_clean, None)]:
            if obs is None:  # published score on all items vs clean score on S: different item sets
                a, b = decide(C_clean, d), decide(C_all, d)
                iu = np.triu_indices(len(P.columns), 1)
                a, b = a[iu], b[iu]
                st = dict(pairs=len(a), flips=int((a != b).sum()), reversals=int((a * b == -1).sum()),
                          lost=int(((a != 0) & (b == 0)).sum()), spurious=int(((a == 0) & (b != 0)).sum()),
                          ref_decided=int((a != 0).sum()))
            else:
                st = flip_stats(ref, obs, d)
            rows.append(dict(level="full", unit="all", scope=scope, delta=d, **st))
    tau = dict(orig_S=kendall(C_clean, C_orig), published_all=kendall(C_clean, C_all))
    # per-subject golden sets (~100 items each)
    sub = r.subject.values[S]
    for s in np.unique(sub):
        k = sub == s
        er = float((r.status.values[S][k] == "corrected").mean())
        for d in DELTAS:
            st = flip_stats(C_clean[k], C_orig[k], d)
            rows.append(dict(level="subject", unit=s, scope="orig_S", delta=d, err_rate=er, n=int(k.sum()), **st))
    fl = pd.DataFrame(rows)
    fl.to_csv(OUT / "e1_flips.csv", index=False)
    json.dump(dict(real_errors=real, kendall_tau=tau), open(OUT / "e1_summary.json", "w"), indent=2)
    return C_clean, Y[S], r.clean.values[S]


def decide_mcnemar(C, delta, alpha=0.05):
    """Exact McNemar (binomial on discordant items) with Holm correction over all pairs."""
    M = C.shape[1]; iu = np.triu_indices(M, 1)
    m = C.mean(0); D = (m[None, :] - m[:, None])[iu]
    b = ((C[:, :, None] == 1) & (C[:, None, :] == 0)).sum(0)[iu]  # row model right, column wrong
    c = ((C[:, :, None] == 0) & (C[:, None, :] == 1)).sum(0)[iu]
    p = np.array([stats.binomtest(int(ci), int(bi + ci)).pvalue if bi + ci else 1.0 for bi, ci in zip(b, c)])
    order = np.argsort(p); adj = np.empty_like(p); running = 0
    for rank, i in enumerate(order):
        running = max(running, min(1, (len(p) - rank) * p[i])); adj[i] = running
    out = np.zeros(len(p), dtype=int)
    out[(adj < alpha) & (D >= delta)] = 1; out[(adj < alpha) & (D <= -delta)] = -1
    return out


def e1_extra(r, P):
    S = r.status.isin(["ok", "corrected"]).values
    Y = P.values
    C_orig = (Y[S] == r.answer.values[S][:, None]).astype(float)
    C_clean = (Y[S] == r.clean.values[S][:, None]).astype(float)
    corr = (r.status == "corrected").values
    modal = modal_wrong_answer(Y, r.clean.values)
    hits = int((r.answer.values[corr] == modal[corr]).sum()); n = int(corr.sum())
    bt = stats.binomtest(hits, n, 1 / 3, alternative="greater")
    ci = stats.binomtest(hits, n).proportion_ci(0.95, method="wilson")  # two-sided CI
    f = pd.read_csv(OUT / "e1_flips.csv"); s = f[(f.level == "subject") & (f.delta == 0.03)]
    rate = s.flips / s.pairs
    excl = lambda units: np.corrcoef(s.err_rate[~s.unit.isin(units)], rate[~s.unit.isin(units)])[0, 1]
    sens = []
    for d in DELTAS:
        a, b = decide_mcnemar(C_clean, d), decide_mcnemar(C_orig, d)
        sens.append(dict(delta=d, rule="mcnemar_holm", flips=int((a != b).sum()), reversals=int((a * b == -1).sum()),
                         lost=int(((a != 0) & (b == 0)).sum()), spurious=int(((a == 0) & (b != 0)).sum()), decided=int((a != 0).sum())))
    sub_rows = []
    sub = r.subject.values[S]
    for u in np.unique(sub):
        k = sub == u
        a, b = decide_mcnemar(C_clean[k], 0.03), decide_mcnemar(C_orig[k], 0.03)
        sub_rows.append(dict(unit=u, flips=int((a != b).sum()), reversals=int((a * b == -1).sum()), decided=int((a != 0).sum())))
    sr = pd.DataFrame(sub_rows)
    by_delta = f[f.level == "subject"].groupby("delta").flips.sum().to_dict()
    res = dict(
        modal_distractor=dict(hits=hits, n=n, rate=hits / n, chance=1 / 3, p_one_sided=bt.pvalue,
                              wilson95=[ci.low, ci.high], tie_rule="lowest option index among most-chosen wrong options"),
        subject_flip_correlation=dict(pearson=float(np.corrcoef(s.err_rate, rate)[0, 1]),
                                      spearman=float(stats.spearmanr(s.err_rate, rate).statistic),
                                      pearson_excl_virology=float(excl(["virology"])),
                                      pearson_excl_virology_college_chemistry=float(excl(["virology", "college_chemistry"])),
                                      subjects_with_zero_flips=int((s.flips == 0).sum()), n_subjects=int(len(s)),
                                      subject_size_mean=float(s.n.mean()), subject_size_min=int(s.n.min()), subject_size_max=int(s.n.max())),
        subject_flips_by_delta=by_delta,
        full_mcnemar_holm=sens,
        subject_mcnemar_holm_delta3=dict(flips=int(sr.flips.sum()), reversals=int(sr.reversals.sum()),
                                         pairs=int(len(sr) * P.shape[1] * (P.shape[1] - 1) // 2)),
        full_lost_of_decided_delta3=None,
    )
    fl = f[(f.level == "full") & (f.scope == "orig_S") & (f.delta == 0.03)].iloc[0]
    res["full_lost_of_decided_delta3"] = dict(lost=int(fl.lost), decided=int(fl.ref_decided))
    json.dump(res, open(OUT / "e1_extra.json", "w"), indent=2, default=float)


def modal_wrong_answer(Y, y):
    """Most frequent wrong option chosen by models for each item (ties: lowest index; if no model
    is wrong, a random wrong option)."""
    rng = np.random.default_rng(0)
    out = np.empty(len(y), dtype=int)
    for i in range(len(y)):
        cnt = np.bincount(Y[i], minlength=4).astype(float)
        cnt[y[i]] = -1
        if cnt.max() <= 0:
            out[i] = rng.choice([o for o in range(4) if o != y[i]])
        else:
            out[i] = int(np.argmax(cnt))
    return out


MECHS = {  # name: (item selection, new label)
    "random": ("uniform", "random"),
    "uniform_modal": ("uniform", "modal"),
    "hard_random": ("hard", "random"),
    "systematic": ("hard", "modal"),
}
BASELINES = ["swap", "drop"]  # no label error: replace / remove the same number of items


def inject(y, k, mech, rng, modal, hard):
    yn = y.copy()
    if k == 0:
        return yn
    sel, lab = MECHS[mech]
    n = len(y)
    if sel == "uniform":
        idx = rng.choice(n, k, replace=False)
    else:
        p = hard + 1e-3
        idx = rng.choice(n, k, replace=False, p=p / p.sum())
    yn[idx] = (y[idx] + rng.integers(1, 4, k)) % 4 if lab == "random" else modal[idx]
    return yn


def e2(Y, y, reps=int(__import__("os").environ.get("REPS", 300))):
    """Cross-fitted injection: models are split into two halves; the modal distractor and item
    hardness used to inject errors for one half are computed from the other half only, and
    decisions are evaluated on pairs within a half. The number of corrupted items is
    k ~ Binomial(n, e), so small sets also receive low error rates in expectation."""
    rng = np.random.default_rng(42)
    M = Y.shape[1]
    perm = np.random.default_rng(7).permutation(M)
    halves = [np.sort(perm[: M // 2]), np.sort(perm[M // 2:])]
    stats_for = []
    for h in range(2):
        other = halves[1 - h]
        stats_for.append((modal_wrong_answer(Y[:, other], y), 1 - (Y[:, other] == y[:, None]).mean(1)))
    rates = [0.0025, 0.005, 0.0075, 0.01, 0.02, 0.03, 0.05, 0.08, 0.12]
    sizes = [100, 300, 870, len(y)]
    rows = []
    for n in sizes:
        R = reps if n < len(y) else max(reps // 5, 20)
        for rep in range(R):
            full = n >= len(y)
            idx = np.arange(len(y)) if full else rng.choice(len(y), n, replace=False)
            for e in rates:
                k = int(rng.binomial(n, e))
                conds = {}
                for h, cols in enumerate(halves):
                    modal, hard = stats_for[h]
                    Ys, ys = Y[idx][:, cols], y[idx]
                    for mech in MECHS:
                        yn = inject(ys, k, mech, rng, modal[idx], hard[idx])
                        conds.setdefault(mech, []).append((Ys, ys, Ys, yn))
                    # baselines: same k items replaced by fresh clean items, or removed
                    if not full:
                        pool = np.setdiff1d(np.arange(len(y)), idx)
                        out = rng.choice(n, k, replace=False); new = rng.choice(pool, k, replace=False)
                        idx2 = idx.copy(); idx2[out] = new
                        conds.setdefault("swap", []).append((Ys, ys, Y[idx2][:, cols], y[idx2]))
                    keep = np.delete(np.arange(n), rng.choice(n, k, replace=False))
                    conds.setdefault("drop", []).append((Ys, ys, Ys[keep], ys[keep]))
                for mech, parts in conds.items():
                    for d in DELTAS:
                        acc = dict(pairs=0, flip=0, rev=0, lost=0, spur=0, decided=0, bias=[], gap=[])
                        for Ya, ya, Yb, yb in parts:
                            Ca = (Ya == ya[:, None]).astype(float); Cb = (Yb == yb[:, None]).astype(float)
                            iu = np.triu_indices(Ca.shape[1], 1)
                            a, b = decide(Ca, d)[iu], decide(Cb, d)[iu]
                            acc["pairs"] += len(a); acc["flip"] += (a != b).sum(); acc["rev"] += (a * b == -1).sum()
                            acc["lost"] += ((a != 0) & (b == 0)).sum(); acc["spur"] += ((a == 0) & (b != 0)).sum()
                            acc["decided"] += (a != 0).sum()
                            if d == DELTAS[0]:
                                ga = (Ca.mean(0)[None, :] - Ca.mean(0)[:, None])[iu]
                                gb = (Cb.mean(0)[None, :] - Cb.mean(0)[:, None])[iu]
                                acc["bias"].append(gb - ga); acc["gap"].append(ga)
                        row = dict(n=n, rep=rep, mech=mech, rate=e, k=k, delta=d,
                                   flip_rate=acc["flip"] / acc["pairs"], reversal_rate=acc["rev"] / acc["pairs"],
                                   lost_rate=acc["lost"] / acc["pairs"], spurious_rate=acc["spur"] / acc["pairs"],
                                   lost_of_decided=acc["lost"] / max(acc["decided"], 1))
                        if acc["bias"]:
                            bb, gg = np.concatenate(acc["bias"]), np.concatenate(acc["gap"])
                            row["mean_abs_bias"] = float(np.abs(bb).mean())
                            row["compress"] = float(np.corrcoef(bb, gg)[0, 1]) if bb.std() > 0 else np.nan
                        rows.append(row)
    df = pd.DataFrame(rows)
    df[df.delta == 0.03].to_csv(OUT / "e2_injection_reps_delta3.csv.gz", index=False)
    g = df.groupby(["n", "mech", "rate", "delta"])
    agg = g.mean(numeric_only=True).drop(columns="rep").reset_index()
    se = g.flip_rate.std().values / np.sqrt(g.size().values)
    agg["flip_ci_lo"] = agg.flip_rate - Z * se; agg["flip_ci_hi"] = agg.flip_rate + Z * se
    agg["reps"] = g.size().values
    agg.to_csv(OUT / "e2_injection.csv", index=False)
    # paired ratio systematic / random with bootstrap CI over reps (delta = 3pp)
    d3 = df[df.delta == 0.03].pivot_table(index=["n", "rate", "rep"], columns="mech", values="flip_rate").reset_index()
    brng = np.random.default_rng(1); out = []
    for (n, e), g2 in d3.groupby(["n", "rate"]):
        for m in ["uniform_modal", "hard_random", "systematic", "swap", "drop"]:
            if m not in g2 or g2[m].isna().all():
                continue
            a, b = g2[m].values, g2["random"].values
            if b.mean() == 0:
                continue
            bs = [a[i].mean() / max(b[i].mean(), 1e-12) for i in (brng.integers(0, len(a), len(a)) for _ in range(1000))]
            out.append(dict(n=n, rate=e, mech=m, ratio_to_random=a.mean() / b.mean(),
                            ci_lo=np.percentile(bs, 2.5), ci_hi=np.percentile(bs, 97.5)))
    pd.DataFrame(out).to_csv(OUT / "e2_ratio_to_random.csv", index=False)
    return agg


def e3():
    rows = []
    for e in [0.001, 0.0025, 0.005, 0.0075, 0.01, 0.02, 0.03]:
        for n in [100, 300, 509, 1000]:
            rows.append(dict(rate=e, audit_n=n, p_pass_zero_error=(1 - e) ** n,
                             wilson_upper_0_errors=Z ** 2 / (n + Z ** 2)))
    pd.DataFrame(rows).to_csv(OUT / "e3_audit_oc.csv", index=False)
    # smallest zero-error audit whose 95% Wilson upper bound is <= delta/4
    json.dump({f"delta={d}": int(np.ceil(Z ** 2 / (d / 4) - Z ** 2)) for d in [0.01, 0.02, 0.03, 0.05]},
              open(OUT / "e3_wilson_min_n.json", "w"), indent=2)


if __name__ == "__main__":
    r, P = load()
    print("items", len(r), "models", P.shape[1])
    C, Y, y = e1(r, P)
    e1_extra(r, P)
    e2(Y, y)
    e3()
    print("done")
