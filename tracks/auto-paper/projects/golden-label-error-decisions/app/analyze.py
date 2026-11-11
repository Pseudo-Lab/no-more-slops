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


def inject(y, Y, rate, mech, rng, modal, hard):
    yn = y.copy()
    n = len(y)
    k = int(round(rate * n))
    if k == 0:
        return yn
    if mech == "random":
        idx = rng.choice(n, k, replace=False)
        yn[idx] = (y[idx] + rng.integers(1, 4, k)) % 4
    else:  # systematic: harder items more likely, label set to the models' favourite distractor
        p = hard + 1e-3
        idx = rng.choice(n, k, replace=False, p=p / p.sum())
        yn[idx] = modal[idx]
    return yn


def e2(Y, y, reps=int(__import__("os").environ.get("REPS", 300))):
    rng = np.random.default_rng(42)
    modal = modal_wrong_answer(Y, y)
    hard = 1 - (Y == y[:, None]).mean(1)
    rates = [0.0025, 0.005, 0.01, 0.02, 0.03, 0.05, 0.08, 0.12]
    sizes = [100, 300, 870, len(y)]
    M = Y.shape[1]
    iu = np.triu_indices(M, 1)
    rows = []
    for n in sizes:
        for rep in range(reps if n < len(y) else max(reps // 5, 20)):
            idx = rng.choice(len(y), n, replace=False) if n < len(y) else np.arange(len(y))
            Ys, ys = Y[idx], y[idx]
            Cc = (Ys == ys[:, None]).astype(float)
            ref = {d: decide(Cc, d)[iu] for d in DELTAS}
            gap = np.abs(Cc.mean(0)[None, :] - Cc.mean(0)[:, None])[iu]
            for mech in ["random", "systematic"]:
                for e in rates:
                    yn = inject(ys, Ys, e, mech, rng, modal[idx], hard[idx])
                    Cn = (Ys == yn[:, None]).astype(float)
                    bias = ((Cn.mean(0)[None, :] - Cn.mean(0)[:, None]) - (Cc.mean(0)[None, :] - Cc.mean(0)[:, None]))[iu]
                    for d in DELTAS:
                        obs = decide(Cn, d)[iu]
                        f = ref[d] != obs
                        rows.append(dict(n=n, rep=rep, mech=mech, rate=e, delta=d,
                                         flip_rate=f.mean(), reversal_rate=(ref[d] * obs == -1).mean(),
                                         lost_rate=((ref[d] != 0) & (obs == 0)).mean(), spurious_rate=((ref[d] == 0) & (obs != 0)).mean(),
                                         flip_rate_close=f[gap < 0.03].mean() if (gap < 0.03).any() else np.nan,
                                         acc_drop=float((Cc.mean() - Cn.mean())),
                                         mean_abs_bias=float(np.abs(bias).mean()), max_abs_bias=float(np.abs(bias).max()),
                                         compress=float(np.corrcoef(bias, (Cc.mean(0)[None, :] - Cc.mean(0)[:, None])[iu])[0, 1])))
    df = pd.DataFrame(rows)
    agg = df.groupby(["n", "mech", "rate", "delta"]).mean(numeric_only=True).drop(columns="rep").reset_index()
    agg.to_csv(OUT / "e2_injection.csv", index=False)
    return agg


def e3():
    rows = []
    for e in [0.001, 0.0025, 0.005, 0.0075, 0.01, 0.02, 0.03]:
        for n in [100, 300, 509, 1000]:
            rows.append(dict(rate=e, audit_n=n, p_pass_zero_error=(1 - e) ** n))
    pd.DataFrame(rows).to_csv(OUT / "e3_audit_oc.csv", index=False)


if __name__ == "__main__":
    r, P = load()
    print("items", len(r), "models", P.shape[1])
    C, Y, y = e1(r, P)
    e2(Y, y)
    e3()
    print("done")
