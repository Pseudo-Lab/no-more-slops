"""Join MMLU-Redux annotations with per-item model predictions."""
import re
from pathlib import Path
import numpy as np, pandas as pd

DATA = Path(__file__).resolve().parent.parent / "data"
norm = lambda s: re.sub(r"\s+", " ", str(s)).strip()

def parse_correct(v):
    if v is None: return None
    v = str(v).strip()
    if v in "ABCD" and len(v) == 1: return "ABCD".index(v)
    m = re.fullmatch(r"(\d)(\.0)?", v)
    return int(m.group(1)) if m and int(m.group(1)) < 4 else None

def key(subject, q, choices):
    return subject + "||" + norm(q + "\n" + "\n".join(f"{l}. {c}" for l, c in zip("ABCD", choices)) + "\nAnswer:")

def load():
    r = pd.read_parquet(DATA / "redux.parquet")
    r["key"] = [key(s, q, c) for s, q, c in zip(r.subject, r.question, r.choices)]
    r["fixed"] = r.correct_answer.map(parse_correct).astype("float")
    # label status: ok, corrected (wrong ground truth with a resolvable answer), unresolved (other errors)
    r["status"] = np.where(r.error_type == "ok", "ok",
                  np.where((r.error_type == "wrong_groundtruth") & r.fixed.notna() & (r.fixed != r.answer), "corrected", "unresolved"))
    r["clean"] = np.where(r.status == "corrected", r.fixed, r.answer).astype(int)
    preds, golds = {}, {}
    for f in sorted((DATA / "preds").glob("*.parquet")):
        d = pd.read_parquet(f)
        d["key"] = d.subject + "||" + d.example.map(norm)
        d["gold"] = d.gold.map(lambda g: int(np.ravel(g)[0]) if np.size(g) else -1)
        d = d.drop_duplicates("key").set_index("key")
        name = f.stem.replace("__", "/")
        preds[name] = d.pred; golds[name] = d.gold
    P = pd.DataFrame(preds).reindex(r.key)
    G = pd.DataFrame(golds).reindex(r.key)
    keep = P.notna().all(axis=1).values
    r = r[keep].reset_index(drop=True); P = P[keep].astype(int).reset_index(drop=True)
    gm = G[keep].max(axis=1).astype(int).values  # newer runs store empty gold (-1)
    ok = gm >= 0; print("gold agreement", (gm[ok] == r.answer.values[ok]).mean(), "n", ok.sum())
    assert (gm[ok] == r.answer.values[ok]).mean() > 0.99, "gold mismatch"
    return r, P
