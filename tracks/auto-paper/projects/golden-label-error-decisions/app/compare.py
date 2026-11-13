"""E4: replicate the analyses of prior work on our data and put our numbers next to the reported ones.

C1  Gema et al.: recount the MMLU-Redux 2.0 error statistics from the released data (Table 5 of the paper).
C2  Gema et al.: rank changes when only correct instances are scored (their Table 2), on our fixed 42 models,
    split into the part due to item sampling and the part due to removing erroneous items.
C3  Gema et al.: per-model correlation between subject accuracy and the subject's share of correct items (Fig. 6).
C4  Vendrow et al.: share of model errors that are benchmark errors (their Table 4).
C5  Northcutt et al.: raise the prevalence of originally mislabeled items by removing correctly labeled ones
    and compare original-label and corrected-label orderings (their Sec. 5.2), plus their model-capacity effect.
C6  Madaan et al., Card et al., Alzahrani et al.: label correction next to other sources of evaluation noise.
Reported values come from reference_numbers.py; everything else is computed here. Writes results/e4_*.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

from analyze import decide
from load import load, norm
import reference_numbers as ref

ROOT = Path(__file__).resolve().parent.parent
DATA, OUT = ROOT / "data", ROOT / "results"
D3 = 0.03


def full_predictions(models):
    """Predictions and original gold labels for every MMLU test item (not only the Redux sample)."""
    preds, golds, sizes = {}, {}, None
    for f in sorted((DATA / "preds").glob("*.parquet")):
        d = pd.read_parquet(f, columns=["subject", "example", "gold", "pred"])
        if sizes is None:
            sizes = d.subject.value_counts()  # original MMLU subject sizes (with duplicate prompts)
        d["key"] = d.subject + "||" + d.example.map(norm)
        d["g"] = d.gold.map(lambda g: int(np.ravel(g)[0]) if np.size(g) else -1)
        d = d.drop_duplicates("key").set_index("key")
        name = f.stem.replace("__", "/")
        preds[name], golds[name] = d.pred, d.g
    P = pd.DataFrame(preds)[models]
    g = pd.DataFrame(golds).max(axis=1)
    assert (g >= 0).all()
    return P, g.values, np.array([k.split("||")[0] for k in P.index]), sizes


def ranks(acc):
    return stats.rankdata(-acc, method="min")


def order_swaps(a, b):
    """Share of model pairs whose point-estimate order differs (ties in either ordering are not swaps)."""
    iu = np.triu_indices(len(a), 1)
    da, db = (a[None, :] - a[:, None])[iu], (b[None, :] - b[:, None])[iu]
    return float((da * db < 0).mean())


def decision_flips(Ca, Cb, delta=D3):
    iu = np.triu_indices(Ca.shape[1], 1)
    a, b = decide(Ca, delta)[iu], decide(Cb, delta)[iu]
    return int((a != b).sum()), int((a * b == -1).sum())


def compare_rankings(acc_a, acc_b, Ca=None, Cb=None):
    ra, rb = ranks(acc_a), ranks(acc_b)
    out = dict(kendall_tau=float(stats.kendalltau(acc_a, acc_b).statistic), max_rank_shift=int(np.abs(ra - rb).max()),
               median_rank_shift=float(np.median(np.abs(ra - rb))), pair_order_swaps=order_swaps(acc_a, acc_b))
    if Ca is not None:
        out["decision_flips"], out["decision_reversals"] = decision_flips(Ca, Cb)
    return out


def c1_recount():
    red = pd.read_parquet(DATA / "redux.parquet")
    cnt = red.groupby("subject").error_type.value_counts().unstack(fill_value=0)
    cols = ["ok", "bad_question_clarity", "bad_options_clarity", "no_correct_answer", "multiple_correct_answers",
            "wrong_groundtruth"]
    rows = []
    for s, c in cnt.iterrows():
        size, ann, *paper = ref.GEMA_TABLE5[s.replace("_", " ")]
        ours = [int(c.get(k, 0)) for k in cols]
        rows.append(dict(subject=s, size=size, annotated=ann, ok_paper=paper[0], ok_data=ours[0], wgt_paper=paper[-1],
                         wgt_data=ours[-1], expert_data=int(c.get("expert", 0)), types_equal=paper == ours))
    t = pd.DataFrame(rows)
    w = t["size"] / t["size"].sum()
    t.to_csv(OUT / "e4_redux_recount.csv", index=False)
    return dict(
        subjects=len(t), subjects_identical=int(t.types_equal.sum()),
        ok_paper=int(t.ok_paper.sum()), ok_data=int(t.ok_data.sum()), wgt_paper=int(t.wgt_paper.sum()),
        wgt_data=int(t.wgt_data.sum()), expert_data=int(t.expert_data.sum()),
        subjects_with_expert=int((t.expert_data > 0).sum()),
        error_share_stratified_paper_table=float(1 - (w * t.ok_paper / t.annotated).sum()),
        error_share_stratified_data=float(1 - (w * t.ok_data / t.annotated).sum()),
        error_share_stratified_data_expert_as_ok=float(1 - (w * (t.ok_data + t.expert_data) / t.annotated).sum()),
        error_share_reported=ref.GEMA["error_share_stratified"],
        wgt_share_stratified_data=float((w * t.wgt_data / t.annotated).sum()),
        wgt_share_reported=ref.GEMA["wgt_share_stratified"],
        virology=t.set_index("subject").loc["virology", ["ok_paper", "ok_data", "wgt_paper", "wgt_data"]].astype(int).to_dict(),
        college_chemistry=t.set_index("subject").loc["college_chemistry", ["ok_paper", "ok_data", "wgt_paper", "wgt_data"]].astype(int).to_dict(),
    )


def c2_c3_gema(r, P):
    models = list(P.columns)
    PF, gF, subjF, sizes = full_predictions(models)
    CF = (PF.values == gF[:, None]).astype(float)
    Y = P.values
    C_orig = (Y == r.answer.values[:, None]).astype(float)
    C_clean = (Y == r.clean.values[:, None]).astype(float)
    st, sub = r.status.values, r.subject.values
    rows, fig6 = [], []
    for s in np.unique(sub):
        k = sub == s
        ok = k & (st == "ok")
        S = k & (st != "unresolved")
        full = subjF == s
        acc = dict(full=CF[full].mean(0), redux_all=C_orig[k].mean(0), redux_ok=C_orig[ok].mean(0),
                   S_orig=C_orig[S].mean(0), S_clean=C_clean[S].mean(0))
        comps = {"full_to_ok (Gema Table 2)": ("full", "redux_ok", CF[full], C_orig[ok]),
                 "full_to_redux (item sampling)": ("full", "redux_all", CF[full], C_orig[k]),
                 "redux_to_ok (removing errors)": ("redux_all", "redux_ok", C_orig[k], C_orig[ok]),
                 "relabel (this paper)": ("S_orig", "S_clean", C_orig[S], C_clean[S])}
        for name, (a, b, Ca, Cb) in comps.items():
            rows.append(dict(subject=s, comparison=name, n_a=len(Ca), n_b=len(Cb), ok_ratio=float(ok.sum() / k.sum()),
                             **compare_rankings(acc[a], acc[b], Ca, Cb)))
        # size-matched controls: random items of the same count as the ok items (Gema comparison minus error removal)
        rng = np.random.default_rng(11)
        n_ok, fidx, kidx = int(ok.sum()), np.flatnonzero(full), np.flatnonzero(k)
        ctl = {"full_to_random_nok": [], "redux_to_random_nok": []}
        for _ in range(200):
            a_f = CF[rng.choice(fidx, min(n_ok, len(fidx)), replace=False)].mean(0)
            a_r = C_orig[rng.choice(kidx, min(n_ok, len(kidx)), replace=False)].mean(0)
            ctl["full_to_random_nok"].append(compare_rankings(acc["full"], a_f))
            ctl["redux_to_random_nok"].append(compare_rankings(acc["redux_all"], a_r))
        for name, lst in ctl.items():
            rows.append(dict(subject=s, comparison=name, n_a=0, n_b=n_ok, ok_ratio=float(ok.sum() / k.sum()),
                             kendall_tau=float(np.median([x["kendall_tau"] for x in lst])),
                             max_rank_shift=int(np.median([x["max_rank_shift"] for x in lst])),
                             median_rank_shift=float(np.median([x["median_rank_shift"] for x in lst])),
                             pair_order_swaps=float(np.mean([x["pair_order_swaps"] for x in lst])),
                             decision_flips=0, decision_reversals=0))
        # largest single rank improvement in the Gema comparison, e.g. 16th -> 1st in their virology column
        ra, rb = ranks(acc["full"]), ranks(acc["redux_ok"])
        j = int(np.argmax(ra - rb))
        rows[-6]["largest_gain"] = f"{models[j]}: {ra[j]} -> {rb[j]}"
    t = pd.DataFrame(rows)
    t.to_csv(OUT / "e4_gema_ranks.csv", index=False)
    # Fig. 6: per model, Pearson r over subjects between subject accuracy (full test) and the ok ratio
    okr = t[t.comparison.str.startswith("full_to_ok")].set_index("subject").ok_ratio
    accs = pd.DataFrame({s: CF[subjF == s].mean(0) for s in okr.index}, index=models).T
    r6 = accs.apply(lambda col: np.corrcoef(col.values, okr.values)[0, 1])
    overall = CF.mean(0)
    top10 = np.argsort(-overall)[:10]
    five = ["virology", "logical_fallacies", "college_chemistry", "professional_law", "human_sexuality"]
    summ = {}
    for comp, g in t.groupby("comparison"):
        g5 = g[g.subject.isin(five)]
        summ[comp] = dict(
            mean_tau_all=float(g.kendall_tau.mean()), mean_pair_swaps_all=float(g.pair_order_swaps.mean()),
            mean_max_shift_all=float(g.max_rank_shift.mean()), mean_tau_five=float(g5.kendall_tau.mean()),
            mean_pair_swaps_five=float(g5.pair_order_swaps.mean()), decision_flips_all=int(g.decision_flips.sum()),
            decision_reversals_all=int(g.decision_reversals.sum()),
            virology=g.set_index("subject").loc["virology"].drop(["comparison"]).to_dict())
    top10b, bot10 = np.argsort(-overall)[:10], np.argsort(overall)[:10]
    return dict(per_comparison=summ, fig6=dict(
        pearson_top10_median=float(r6.iloc[top10b].median()), pearson_bottom10_median=float(r6.iloc[bot10].median()),
        spearman_overall_acc_vs_r=float(stats.spearmanr(overall, r6.values).statistic),
        pearson_min=float(r6.min()), pearson_median=float(r6.median()), pearson_max=float(r6.max()),
        pearson_top10_min=float(r6.iloc[top10].min()), pearson_top10_max=float(r6.iloc[top10].max()),
        reported_range=ref.GEMA["fig6_pearson_range"]))


def c4_vendrow(r, P):
    Y = P.values
    S = r.status.values != "unresolved"
    err_orig = (Y != r.answer.values[:, None])
    err_clean = (Y != r.clean.values[:, None]) & S[:, None]
    out = {}
    acc = 1 - err_orig.mean(0)
    for name, k in [("all", np.ones(len(r), bool)), ("high_school_mathematics", r.subject.values == "high_school_mathematics"),
                    ("virology", r.subject.values == "virology")]:
        eo, ec = err_orig[k].sum(0), err_clean[k].sum(0)
        top = np.argsort(-acc)[:5]
        out[name] = dict(items=int(k.sum()), avg_errors_original=float(eo.mean()), avg_errors_cleaned=float(ec.mean()),
                         benchmark_share=float(1 - ec.mean() / eo.mean()),
                         benchmark_share_top5_models=float(1 - ec[top].mean() / eo[top].mean()))
    out["reported_hs_math"] = ref.VENDROW["mmlu_hs_math_errors"]
    return out


def c5_northcutt(r, P, reps=200):
    Y = P.values
    st = r.status.values
    C, B = st == "corrected", st == "ok"
    A_Co = (Y[C] == r.answer.values[C][:, None]).mean(0)
    A_Cc = (Y[C] == r.clean.values[C][:, None]).mean(0)
    A_B = (Y[B] == r.answer.values[B][:, None]).mean(0)
    nC, nB = int(C.sum()), int(B.sum())
    n0 = nC / (nC + nB)
    curve = []
    for N in [n0, 0.03, n0 + 0.05, n0 + 0.06, 0.10, 0.15, 0.20, 0.30, 0.50]:
        ao, ac = N * A_Co + (1 - N) * A_B, N * A_Cc + (1 - N) * A_B
        a0 = n0 * A_Cc + (1 - n0) * A_B
        iu = np.triu_indices(len(A_B), 1)
        do, dc = (ao[None, :] - ao[:, None])[iu], (ac[None, :] - ac[:, None])[iu]
        dB = (A_B[None, :] - A_B[:, None])[iu]
        sw = do * dc < 0
        row = dict(N=N, N_increase=N - n0, set_size=int(round(nC / N)), swap_orig_vs_corrected=float(sw.mean()),
                   swap_corrected_vs_N0=order_swaps(a0, ac),
                   # among swaps, does the corrected-label winner have the lower accuracy on the benign items?
                   corrected_winner_is_weaker=float(((np.sign(dc[sw]) != np.sign(dB[sw])).mean()) if sw.any() else np.nan))
        # decisions with our rule on actual reduced sets (random removal of correctly labeled items)
        keep_B = int(round(nC * (1 - N) / N))
        if keep_B <= nB:
            rng = np.random.default_rng(3)
            fl = rv = 0
            for _ in range(reps if keep_B < nB else 1):
                idx = np.concatenate([np.flatnonzero(C), rng.choice(np.flatnonzero(B), keep_B, replace=False)])
                Co = (Y[idx] == r.answer.values[idx][:, None]).astype(float)
                Cc = (Y[idx] == r.clean.values[idx][:, None]).astype(float)
                f, v = decision_flips(Cc, Co)
                fl += f; rv += v
            n_rep = reps if keep_B < nB else 1
            row.update(decision_flip_rate=fl / n_rep / len(iu[0]), decision_reversal_rate=rv / n_rep / len(iu[0]))
        curve.append(row)
    pd.DataFrame(curve).to_csv(OUT / "e4_northcutt_curve.csv", index=False)
    # crossing prevalence for each pair whose corrected-label order changes as N grows from n0
    dB = A_B[None, :] - A_B[:, None]; dCc = A_Cc[None, :] - A_Cc[:, None]
    iu = np.triu_indices(len(A_B), 1)
    with np.errstate(divide="ignore", invalid="ignore"):
        Nstar = (dB / (dB - dCc))[iu]
    crossing = Nstar[(Nstar > n0) & (Nstar <= 1)]
    # Do strong models reproduce the original labels of erroneous items (memorisation, Gema et al. p4)?
    top, bottom = np.argsort(-A_B)[:10], np.argsort(A_B)[:10]
    U = st == "unresolved"
    A_U = (Y[U] == r.answer.values[U][:, None]).mean(0)
    memo = dict(top10_acc_ok=float(A_B[top].mean()), top10_on_original_label_corrected=float(A_Co[top].mean()),
                top10_on_corrected_label=float(A_Cc[top].mean()), top10_on_original_label_unresolved=float(A_U[top].mean()),
                bottom10_acc_ok=float(A_B[bottom].mean()), bottom10_on_original_label_corrected=float(A_Co[bottom].mean()),
                bottom10_on_corrected_label=float(A_Cc[bottom].mean()))
    for subj in ["professional_law", "formal_logic"]:
        ks = r.subject.values == subj
        err = ks & (st != "ok"); okk = ks & (st == "ok")
        memo[f"{subj}_top10_acc_err_original"] = float((Y[err][:, top] == r.answer.values[err][:, None]).mean())
        memo[f"{subj}_top10_acc_ok"] = float((Y[okk][:, top] == r.answer.values[okk][:, None]).mean())
        memo[f"{subj}_n_err"] = int(err.sum())
    wrong = (Y[C] != r.clean.values[C][:, None])
    share = (Y[C] == r.answer.values[C][:, None]).sum(0) / np.maximum(wrong.sum(0), 1)
    memo["top10_wrong_label_share_of_wrong"] = float(share[top].mean())
    memo["bottom10_wrong_label_share_of_wrong"] = float(share[bottom].mean())
    memo["spearman_AB_vs_share_of_wrong"] = float(stats.spearmanr(A_B, share).statistic)
    return dict(memorisation_check=memo,
        n_C=nC, n_B=nB, n_unresolved=int((st == "unresolved").sum()), N0=n0,
        spearman_AB_vs_AC_original=float(stats.spearmanr(A_B, A_Co).statistic),
        spearman_AB_vs_AC_corrected=float(stats.spearmanr(A_B, A_Cc).statistic),
        spearman_C_original_vs_corrected=float(stats.spearmanr(A_Co, A_Cc).statistic),
        pairs_crossing=int(len(crossing)), pairs=int(len(iu[0])),
        pairs_crossing_within_6pp=int((crossing <= n0 + 0.06).sum()),
        crossing_N_median=float(np.median(crossing)) if len(crossing) else None,
        crossing_increase_median=float(np.median(crossing - n0)) if len(crossing) else None,
        reported=ref.NORTHCUTT)


def c6_noise(r, P, reps=300):
    Y = P.values
    S = r.status.values != "unresolved"
    Co = (Y[S] == r.answer.values[S][:, None]).astype(float)
    Cc = (Y[S] == r.clean.values[S][:, None]).astype(float)
    n, M = Cc.shape
    iu = np.triu_indices(M, 1)
    mo, mc = Co.mean(0), Cc.mean(0)
    dd = ((mc[None, :] - mc[:, None]) - (mo[None, :] - mo[:, None]))[iu]  # change in pair differences
    # paired standard deviation of per-item differences, for SE and minimum detectable effect (80% power)
    cov = (Cc.T @ Cc) / n - np.outer(mc, mc)
    sd = np.sqrt(np.maximum(np.diag(cov)[None, :] + np.diag(cov)[:, None] - 2 * cov, 0))[iu]
    zz = stats.norm.ppf(0.975) + stats.norm.ppf(0.8)
    rng = np.random.default_rng(5)
    sub_swaps = [order_swaps(mc, Cc[rng.choice(n, 100, replace=False)].mean(0)) for _ in range(reps)]
    ro, rc = ranks(mo), ranks(mc)
    f = pd.read_csv(OUT / "e1_flips.csv")
    subj = r.subject.values[S]
    subj_swaps = [order_swaps(Co[subj == s].mean(0), Cc[subj == s].mean(0)) for s in np.unique(subj)]
    return dict(
        label_shift_pp_mean=float(100 * (mc - mo).mean()), label_shift_pp_min=float(100 * (mc - mo).min()),
        label_shift_pp_max=float(100 * (mc - mo).max()),
        pair_diff_change_pp_median=float(100 * np.median(np.abs(dd))), pair_diff_change_pp_max=float(100 * np.abs(dd).max()),
        pair_se_pp_median=float(100 * np.median(sd / np.sqrt(n))),
        discordance_median=float(np.median(((Cc[:, :, None] != Cc[:, None, :]).mean(0))[iu])),
        mde80_pp_median={str(k): float(100 * zz * np.median(sd) / np.sqrt(k)) for k in [100, 870, n]},
        single_model_ci95_pp_median=float(100 * 1.96 * np.median(np.sqrt(mc * (1 - mc) / n))),
        full_set_relabel=dict(kendall_tau=float(stats.kendalltau(mo, mc).statistic), pair_order_swaps=order_swaps(mo, mc),
                              models_rank_changed=int((ro != rc).sum()), max_rank_shift=int(np.abs(ro - rc).max())),
        subject_relabel_pair_order_swaps_mean=float(np.mean(subj_swaps)),
        random100_vs_full_pair_order_swaps_mean=float(np.mean(sub_swaps)),
        reported=dict(madaan=ref.MADAAN, card=ref.CARD, alzahrani=ref.ALZAHRANI),
    )


if __name__ == "__main__":
    r, P = load()
    res = dict(c1_redux_recount=c1_recount())
    res.update(c2_c3_gema(r, P))
    res["c4_vendrow"] = c4_vendrow(r, P)
    res["c5_northcutt"] = c5_northcutt(r, P)
    res["c6_noise"] = c6_noise(r, P)
    json.dump(res, open(OUT / "e4_compare.json", "w"), indent=2, default=lambda o: o.item() if hasattr(o, "item") else str(o))
    print(json.dumps(res, indent=1, default=str)[:6000])
