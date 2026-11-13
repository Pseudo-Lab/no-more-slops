"""Download MMLU-Redux 2.0 and per-item MMLU predictions of open models from the
Open LLM Leaderboard (v1) details datasets. Writes compact parquet to ../data/."""
import json, re, sys, urllib.request
from pathlib import Path
import numpy as np, pandas as pd, pyarrow.ipc as ipc
from huggingface_hub import hf_hub_download

DATA = Path(__file__).resolve().parent.parent / "data"
MODELS = """meta-llama/Llama-2-7b-hf meta-llama/Llama-2-13b-hf meta-llama/Llama-2-70b-hf
meta-llama/Llama-2-7b-chat-hf meta-llama/Llama-2-13b-chat-hf meta-llama/Llama-2-70b-chat-hf
meta-llama/Meta-Llama-3-8B meta-llama/Meta-Llama-3-8B-Instruct mistralai/Mistral-7B-v0.1
mistralai/Mistral-7B-Instruct-v0.2 mistralai/Mixtral-8x7B-v0.1 mistralai/Mixtral-8x7B-Instruct-v0.1
tiiuae/falcon-7b tiiuae/falcon-40b Qwen/Qwen-7B Qwen/Qwen-14B Qwen/Qwen1.5-7B Qwen/Qwen1.5-14B Qwen/Qwen1.5-72B
google/gemma-7b google/gemma-2b microsoft/phi-2 01-ai/Yi-6B 01-ai/Yi-34B EleutherAI/pythia-12b
mosaicml/mpt-7b mosaicml/mpt-30b huggyllama/llama-7b huggyllama/llama-13b huggyllama/llama-30b huggyllama/llama-65b
deepseek-ai/deepseek-llm-7b-base deepseek-ai/deepseek-llm-67b-base internlm/internlm2-7b
upstage/SOLAR-10.7B-v1.0 HuggingFaceH4/zephyr-7b-beta teknium/OpenHermes-2.5-Mistral-7B openchat/openchat_3.5
allenai/OLMo-7B-hf allenai/OLMo-1.7-7B-hf stabilityai/stablelm-3b-4e1t tiiuae/falcon-180B Intel/neural-chat-7b-v3-1
lmsys/vicuna-13b-v1.5 lmsys/vicuna-7b-v1.5 WizardLM/WizardLM-70B-V1.0 NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO""".split()

def norm(s): return re.sub(r"\s+", " ", s).strip()

def tree(repo, path=""):
    url = f"https://huggingface.co/api/datasets/{repo}/tree/main/{path}"
    return json.loads(urllib.request.urlopen(url, timeout=60).read())

def redux():
    out = DATA / "redux.parquet"
    if out.exists(): return pd.read_parquet(out)
    subjects = [x["path"] for x in tree("edinburgh-dawg/mmlu-redux-2.0") if x["type"] == "directory"]
    rows = []
    for s in subjects:
        p = hf_hub_download("edinburgh-dawg/mmlu-redux-2.0", f"{s}/data-00000-of-00001.arrow", repo_type="dataset")
        t = ipc.open_stream(open(p, "rb")).read_all().to_pandas()
        t["subject"] = s; t["idx"] = range(len(t)); rows.append(t)
    d = pd.concat(rows, ignore_index=True)
    d["choices"] = d["choices"].map(list)
    for c in ("correct_answer", "potential_reason", "source"): d[c] = d[c].map(lambda v: None if v is None or (isinstance(v, float) and np.isnan(v)) else str(v))
    d.to_parquet(out); return d

def model(name):
    out = DATA / "preds" / (name.replace("/", "__") + ".parquet")
    if out.exists(): return
    repo = "open-llm-leaderboard-old/details_" + name.replace("/", "__")
    runs = sorted(x["path"] for x in tree(repo) if x["type"] == "directory")
    best = None  # the full MMLU run: largest professional_law file, latest on ties
    for run in runs:
        files = [x for x in tree(repo, run) if "hendrycksTest-" in x["path"]]
        if len(files) < 57: continue
        size = max(x["size"] for x in files if "professional_law" in x["path"])
        if best is None or size >= best[0]: best = (size, run, [x["path"] for x in files])
    if best is None: raise RuntimeError("no MMLU run")
    _, run, files = best
    rows = []
    for f in files:
        subj = re.search(r"hendrycksTest-(.+?)\|", f).group(1)
        d = pd.read_parquet(hf_hub_download(repo, f, repo_type="dataset"), columns=["example", "gold", "predictions"])
        d["subject"] = subj
        d["pred"] = d["predictions"].map(lambda v: int(np.argmax(v)))
        rows.append(d[["subject", "example", "gold", "pred"]])
    d = pd.concat(rows, ignore_index=True); d["run"] = run
    if len(d) < 14000: raise RuntimeError(f"partial run {len(d)} rows")
    out.parent.mkdir(parents=True, exist_ok=True); d.to_parquet(out)

if __name__ == "__main__":
    redux(); print("redux ok", flush=True)
    for m in (sys.argv[1:] or MODELS):
        try: model(m); print("ok", m, flush=True)
        except Exception as e: print("FAIL", m, repr(e)[:200], flush=True)
