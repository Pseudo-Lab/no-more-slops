# /// script
# requires-python = ">=3.10"
# dependencies = ["torch>=2.4", "transformers>=4.46", "pandas", "pyarrow", "numpy", "scipy", "huggingface_hub"]
# ///
"""E0: re-run models on this machine with the leaderboard's own MMLU prompts and compare the
per-item results with those the Open LLM Leaderboard v1 published.

The leaderboard details store, per item, the tokenized 5-shot prompt (input_tokens, right-padded;
`padded` counts the pad ids), the four single-token continuations " A".." D" (cont_tokens) and the
log-likelihoods it computed for them (predictions). We feed the same token ids to the model and
recompute the four log-likelihoods, so prompt construction and tokenization are identical and only
the weights revision, precision and hardware differ. Only items of the joined MMLU-Redux set are run.

Usage (from the project folder):
  uv run app/rerun_local.py run microsoft/phi-2 --revision <sha> --dtype float16
  uv run app/rerun_local.py summarize        # writes results/e0_rerun.csv and results/e0_rerun.json
Raw per-item outputs go to data/rerun/ (git-ignored, like the downloaded predictions).
"""
import argparse, json, re, sys, time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA, OUT = ROOT / "data", ROOT / "results"
sys.path.insert(0, str(Path(__file__).resolve().parent))
from load import key, load  # noqa: E402


def board_rows(name):
    """Leaderboard rows (prompt tokens, continuation tokens, log-likelihoods) of the run fetch.py used."""
    from huggingface_hub import hf_hub_download
    from fetch import tree
    run = pd.read_parquet(DATA / "preds" / (name.replace("/", "__") + ".parquet"), columns=["run"]).run.iloc[0]
    repo = "open-llm-leaderboard-old/details_" + name.replace("/", "__")
    files = [x["path"] for x in tree(repo, run) if "hendrycksTest-" in x["path"]]
    rows = []
    for f in files:
        subj = re.search(r"hendrycksTest-(.+?)\|", f).group(1)
        d = pd.read_parquet(hf_hub_download(repo, f, repo_type="dataset"),
                            columns=["example", "input_tokens", "cont_tokens", "padded", "truncated", "predictions"])
        d["subject"] = subj
        rows.append(d)
    d = pd.concat(rows, ignore_index=True)
    d["key"] = d.subject + "||" + d.example.map(lambda s: re.sub(r"\s+", " ", s).strip())
    return d.drop_duplicates("key"), run


def run(args):
    import torch
    from transformers import AutoModelForCausalLM
    redux = pd.read_parquet(DATA / "redux.parquet")
    keys = {key(s, q, c) for s, q, c in zip(redux.subject, redux.question, redux.choices)}
    d, board_run = board_rows(args.model)
    d = d[d.key.isin(keys)].reset_index(drop=True)
    if args.limit:
        d = d.sample(args.limit, random_state=0).reset_index(drop=True)
    dev = "mps" if torch.backends.mps.is_available() else "cpu"
    model = AutoModelForCausalLM.from_pretrained(args.model, revision=args.revision,
                                                 torch_dtype=getattr(torch, args.dtype)).to(dev).eval()
    ctx = []
    for r in d.itertuples():
        ctxs = [np.asarray(x)[: len(x) - int(p)] for x, p in zip(r.input_tokens, r.padded)]
        assert all(len(c) == 1 for c in r.cont_tokens) and all((c == ctxs[0]).all() for c in ctxs[1:]), "multi-token item"
        ctx.append(ctxs[0])
    conts = [[int(np.asarray(c)[0]) for c in r] for r in d.cont_tokens]
    out_ll, t0 = [None] * len(d), time.time()

    def last_logprobs(logits, i):
        return torch.log_softmax(logits[0, -1].float(), -1)[conts[i]].cpu().numpy()

    done = 0
    for subj, idx in d.groupby("subject").indices.items():
        # The 5-shot examples are the same for every item of a subject: run that shared prefix once and
        # reuse its key-value cache (cropped back after each item). Items whose prompt was truncated on the
        # left do not share the prefix and run in full. --no-prefix-cache runs every item in full.
        prefix = ctx[idx[0]]
        for i in idx[1:]:
            n = min(len(prefix), len(ctx[i]))
            k = int(np.argmax(prefix[:n] != ctx[i][:n])) if (prefix[:n] != ctx[i][:n]).any() else n
            prefix = prefix[:k]
        cache = None
        if args.prefix_cache and len(prefix) > 1:
            with torch.no_grad():
                cache = model(torch.tensor(prefix[None, :], device=dev), use_cache=True).past_key_values
        for i in idx:
            with torch.no_grad():
                shared = cache is not None and len(ctx[i]) > len(prefix) and (ctx[i][: len(prefix)] == prefix).all()
                if shared:
                    o = model(torch.tensor(ctx[i][None, len(prefix):], device=dev), past_key_values=cache, use_cache=True)
                    cache.crop(len(prefix) - cache.get_seq_length())  # negative: number of tokens to drop
                else:
                    o = model(torch.tensor(ctx[i][None, :], device=dev))
            out_ll[i] = last_logprobs(o.logits, i)
            done += 1
        print(f"{done}/{len(d)} {subj} {time.time() - t0:.0f}s", flush=True)
    d["ll_local"] = out_ll
    d["truncated"] = d.truncated.map(lambda v: bool(np.any(v)))  # stored ids are already the truncated input
    d["ll_board"] = d.predictions.map(lambda v: np.asarray(v, dtype=float))
    d["model"], d["board_run"], d["revision"], d["dtype"], d["device"] = args.model, board_run, args.revision, args.dtype, dev
    d["prefix_cache"] = args.prefix_cache
    out = DATA / "rerun" / (args.model.replace("/", "__") + ("" if args.prefix_cache else ".nocache") + ".parquet")
    out.parent.mkdir(parents=True, exist_ok=True)
    d[["key", "subject", "truncated", "ll_local", "ll_board", "model", "board_run", "revision", "dtype", "device",
       "prefix_cache"]].to_parquet(out)
    print("wrote", out, f"{time.time() - t0:.0f}s")


def summarize(_):
    r, P = load()
    S = r.status.isin(["ok", "corrected"]).values
    files = sorted(f for f in (DATA / "rerun").glob("*.parquet") if ".nocache" not in f.name)
    rows, preds_local, preds_board = [], {}, {}
    for f in files:
        d = pd.read_parquet(f).set_index("key").reindex(r.key)
        have = d.ll_local.notna().values
        L = np.stack(d.ll_local[have].values); B = np.stack(d.ll_board[have].values)
        pl, pb = L.argmax(1), B.argmax(1)
        name = d.model.dropna().iloc[0]
        assert (pb == P[name].values[have]).all(), "leaderboard argmax differs from fetched predictions"
        ans, clean, st = r.answer.values[have], r.clean.values[have], r.status.values[have]
        s = np.isin(st, ["ok", "corrected"]); c = st == "corrected"
        rows.append(dict(
            model=name, revision=d.revision.dropna().iloc[0], dtype=d.dtype.dropna().iloc[0],
            board_run=d.board_run.dropna().iloc[0], items=int(have.sum()),
            pred_agreement=float((pl == pb).mean()),
            ll_max_abs_diff=float(np.abs(L - B).max()), ll_median_abs_diff=float(np.median(np.abs(L - B))),
            acc_board_published=float((pb == ans).mean()), acc_local_published=float((pl == ans).mean()),
            acc_board_orig_S=float((pb[s] == ans[s]).mean()), acc_local_orig_S=float((pl[s] == ans[s]).mean()),
            acc_board_clean_S=float((pb[s] == clean[s]).mean()), acc_local_clean_S=float((pl[s] == clean[s]).mean()),
            corrected_items=int(c.sum()),
            corrected_pred_agreement=float((pl[c] == pb[c]).mean()),
            corrected_local_on_orig=float((pl[c] == ans[c]).mean()), corrected_board_on_orig=float((pb[c] == ans[c]).mean()),
            # how close were the top two options (leaderboard log-likelihoods) where the two predictions differ?
            disagree_margin_median=float(np.median(np.diff(np.sort(B[pl != pb], 1)[:, -2:], axis=1))) if (pl != pb).any() else None,
            all_margin_median=float(np.median(np.diff(np.sort(B, 1)[:, -2:], axis=1))),
        ))
        preds_local[name], preds_board[name] = np.full(len(r), -1), np.full(len(r), -1)
        preds_local[name][have], preds_board[name][have] = pl, pb
    tab = pd.DataFrame(rows)
    # pairwise decisions among the re-run models (delta = 3 pp) from local vs leaderboard predictions
    from analyze import decide
    names = list(preds_local)
    if len(names) > 1:
        Sm = S & np.all([preds_local[n] >= 0 for n in names], axis=0)
        iu = np.triu_indices(len(names), 1)
        agree = {}
        for lab_name, lab in [("orig", r.answer.values), ("clean", r.clean.values)]:
            dec = {}
            for src, pr in [("local", preds_local), ("board", preds_board)]:
                Y = np.stack([pr[n] for n in names], 1)
                dec[src] = decide((Y[Sm] == lab[Sm][:, None]).astype(float), 0.03)[iu]
            agree[lab_name] = int((dec["local"] == dec["board"]).sum())
        tab["pair_decisions_equal"] = f"{agree['orig']}/{len(iu[0])} (orig), {agree['clean']}/{len(iu[0])} (clean)"
    tab["shift_pp_board"] = 100 * (tab.acc_board_clean_S - tab.acc_board_orig_S)
    tab["shift_pp_local"] = 100 * (tab.acc_local_clean_S - tab.acc_local_orig_S)
    # the shared-prefix cache must not change results: compare with full-prompt runs where both exist
    for f in (DATA / "rerun").glob("*.nocache.parquet"):
        a = pd.read_parquet(f).set_index("key")
        name = a.model.iloc[0]
        b = pd.read_parquet(DATA / "rerun" / f.name.replace(".nocache", "")).set_index("key").loc[a.index]
        A, Bc = np.stack(a.ll_local.values), np.stack(b.ll_local.values)
        k = tab.model == name
        tab.loc[k, "nocache_items"] = len(a)
        tab.loc[k, "nocache_max_abs_diff"] = float(np.abs(A - Bc).max())
        tab.loc[k, "nocache_pred_agreement"] = float((A.argmax(1) == Bc.argmax(1)).mean())
    tab.to_csv(OUT / "e0_rerun.csv", index=False)
    print(tab.T.to_string())


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("run"); a.add_argument("model"); a.add_argument("--revision", default="main")
    a.add_argument("--dtype", default="float16"); a.add_argument("--limit", type=int, default=0)
    a.add_argument("--no-prefix-cache", dest="prefix_cache", action="store_false")
    sub.add_parser("summarize")
    args = ap.parse_args()
    {"run": run, "summarize": summarize}[args.cmd](args)
