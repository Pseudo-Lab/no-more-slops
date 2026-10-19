"""Data extraction (PMDRL summary + taxonomy codes) for included papers.

prepare: split included papers without results into data/extraction/batches/<round>-NN.jsonl
fill: fetch missing or short abstracts of included papers (arXiv, OpenAlex, Semantic Scholar)
      into data/extraction/abstracts.json (used by prepare)
collect: validate data/extraction/results/*.jsonl, add `who` from candidates.csv,
         and write data/extraction.jsonl

Fields are defined in docs/extraction.md.

Usage:
  uv run extract.py fill
  uv run extract.py prepare --round e1 --size 70
  uv run extract.py prepare --round e1-fix --redo-filled   # re-extract title-only records
  uv run extract.py collect
"""

import argparse
import json
import time
import urllib.error
import xml.etree.ElementTree as ET
from collections import Counter

from common import DATA, get_json, norm_title, request, s2_headers
from screen import candidates, results as screening

EXTRACT = DATA / "extraction"
BATCHES, RESULTS = EXTRACT / "batches", EXTRACT / "results"
ABSTRACTS = EXTRACT / "abstracts.json"  # abstracts fetched by `fill`, keyed by candidate key
SHORT = 300  # abstracts shorter than this are treated as missing or truncated
PMDRL = ("problem", "method", "data", "result", "limitation", "gap")
REQUIRED = ("problem", "method", "data", "result")
CODES = {
    "contribution": {"method", "analysis", "training", "benchmark", "application", "security", "survey"},
    "judge_format": {"pointwise", "pairwise", "listwise", "binary", "rubric", "reference", "critique"},
    "judge_setup": {"single", "ensemble", "debate", "reasoning", "agent", "finetuned"},
    "domain": {"general", "code", "math", "medical", "legal", "education", "science", "finance", "ir_rag",
               "dialogue", "summarization", "translation", "safety", "agent", "multimodal", "creative", "other"},
    "biases": {"position", "verbosity", "self_preference", "authority", "sycophancy", "inconsistency",
               "prompt_sensitivity", "leakage", "adversarial", "other"},
    "mitigation": {"swap", "calibration", "ensemble", "fine_tuning", "rubric", "cot", "reference", "other"},
}


def included():
    done = screening()
    fetched = json.loads(ABSTRACTS.read_text(encoding="utf-8")) if ABSTRACTS.exists() else {}
    rows = [r for r in candidates() if done.get(r["key"], {}).get("decision") == "include"]
    for r in rows:
        if len(fetched.get(r["key"], "")) > len(r["abstract"]):
            r["abstract"], r["abstract_fetched"] = fetched[r["key"]], True
    return rows


def results():
    out = {}
    for path in sorted(RESULTS.glob("*.jsonl")):
        for line in path.open(encoding="utf-8"):
            if line.strip():
                rec = json.loads(line)
                rec["batch"] = path.stem
                out[rec["key"]] = rec
    return out


def who(r):
    authors = [a.strip() for a in r["authors"].split(";") if a.strip()]
    first = (authors[0] + (" 외" if len(authors) > 1 else "")) if authors else "저자 미상"
    return ", ".join(x for x in (first, r["year"], r["venue"]) if x)


def problems(rec):
    """Return a list of schema violations for one result record."""
    out = []
    p, c = rec.get("pmdrl") or {}, rec.get("codes") or {}
    out += [f"pmdrl.{k} missing" for k in PMDRL if k not in p]
    out += [f"pmdrl.{k} empty" for k in REQUIRED if not p.get(k)]
    for field, allowed in CODES.items():
        values = c.get(field)
        if not isinstance(values, list):
            out.append(f"codes.{field} not a list")
        elif set(values) - allowed:
            out.append(f"codes.{field} unknown {sorted(set(values) - allowed)}")
    if not isinstance(c.get("judge_models"), list):
        out.append("codes.judge_models not a list")
    if not isinstance(c.get("language"), list):
        out.append("codes.language not a list")
    if not isinstance(c.get("human_comparison"), dict) or "done" not in c["human_comparison"]:
        out.append("codes.human_comparison malformed")
    return out


def fetch_abstract(r):
    """Try arXiv, OpenAlex, then one Semantic Scholar title search; return "" if none has it."""
    if r["arxiv"]:
        feed = ET.fromstring(request("http://export.arxiv.org/api/query", {"id_list": r["arxiv"]}))
        summary = feed.find("{http://www.w3.org/2005/Atom}entry/{http://www.w3.org/2005/Atom}summary")
        if summary is not None and summary.text:
            return " ".join(summary.text.split())
    if r["doi"]:
        try:
            work = get_json(f"https://api.openalex.org/works/doi:{r['doi']}", {"select": "abstract_inverted_index"})
        except urllib.error.HTTPError:
            work = {}
        if index := work.get("abstract_inverted_index"):
            words = sorted((i, w) for w, positions in index.items() for i in positions)
            return " ".join(w for _, w in words)
    try:
        hits = json.loads(request("https://api.semanticscholar.org/graph/v1/paper/search",
                                  {"query": r["title"], "fields": "title,abstract", "limit": 3},
                                  headers=s2_headers(), retries=2))
    except urllib.error.HTTPError:
        return ""
    for paper in hits.get("data", []):
        if norm_title(paper["title"]) == norm_title(r["title"]) and paper.get("abstract"):
            return paper["abstract"]
    return ""


def fill(args):
    """Fetch abstracts for included papers whose abstract is missing or short."""
    fetched = json.loads(ABSTRACTS.read_text(encoding="utf-8")) if ABSTRACTS.exists() else {}
    rows = [r for r in included() if len(r["abstract"]) < SHORT and r["key"] not in fetched]
    found = 0
    for r in rows:
        abstract = fetch_abstract(r)
        if len(abstract) > len(r["abstract"]):
            fetched[r["key"]] = abstract
            found += 1
            ABSTRACTS.parent.mkdir(parents=True, exist_ok=True)
            ABSTRACTS.write_text(json.dumps(fetched, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        time.sleep(3)
    print(f"short or missing abstracts: {len(rows)}; fetched {found} -> {ABSTRACTS.relative_to(DATA.parent)}")


def prepare(args):
    done = results()
    pending = {p.stem for p in BATCHES.glob("*.jsonl")} - {p.stem for p in RESULTS.glob("*.jsonl")}
    queued = {json.loads(line)["key"] for name in pending for line in (BATCHES / f"{name}.jsonl").open()}
    if args.redo_filled:
        # Records first written from a missing or truncated abstract, now that `fill` found a full one.
        rows = [r for r in included() if r.get("abstract_fetched") and r["key"] in done and r["key"] not in queued]
    else:
        rows = [r for r in included() if r["key"] not in done and r["key"] not in queued]
    BATCHES.mkdir(parents=True, exist_ok=True)
    for n, i in enumerate(range(0, len(rows), args.size), 1):
        with (BATCHES / f"{args.round}-{n:02d}.jsonl").open("w", encoding="utf-8") as f:
            for r in rows[i:i + args.size]:
                f.write(json.dumps({k: r[k] for k in ("key", "title", "year", "venue")} |
                                   {"abstract": r["abstract"][:3000]}, ensure_ascii=False) + "\n")
    print(f"{len(rows)} papers -> {-(-len(rows) // args.size)} batches ({args.round}-NN)")


def collect(args):
    papers = {r["key"]: r for r in included()}
    done = results()
    stray = sorted(set(done) - set(papers))
    for batch in sorted(p.stem for p in BATCHES.glob("*.jsonl")):
        keys = [json.loads(line)["key"] for line in (BATCHES / f"{batch}.jsonl").open()]
        missing = [k for k in keys if k not in done]
        if (RESULTS / f"{batch}.jsonl").exists() and missing:
            print(f"WARNING {batch}: {len(missing)} keys without results, e.g. {missing[:2]}")

    bad = {k: problems(r) for k, r in done.items() if k in papers}
    bad = {k: v for k, v in bad.items() if v}
    for batch, n in sorted(Counter(done[k]["batch"] for k in bad).items()):
        example = next(k for k in bad if done[k]["batch"] == batch)
        print(f"WARNING {batch}: {n} invalid records, e.g. {example}: {bad[example][:3]}")
    if stray:
        # Papers later moved to maybe/exclude (r5 re-screening, duplicates) keep their records but are dropped here.
        print(f"note: {len(stray)} results for papers no longer included, e.g. {stray[:3]}")
    # Subagents sometimes skim and reuse template text; flag batches where >10% of summaries repeat.
    for batch in sorted({r["batch"] for r in done.values()}):
        texts = Counter((r.get("pmdrl") or {}).get("result") for r in done.values() if r["batch"] == batch)
        repeated, total = sum(n for n in texts.values() if n > 1), sum(texts.values())
        if repeated > total * 0.1:
            print(f"WARNING {batch}: {repeated}/{total} results are repeated sentences; re-extract this batch")
    # Parallel subagents once shared scratch files, attaching one batch's text to another's keys.
    seen = {}
    for r in done.values():
        text = (r.get("pmdrl") or {}).get("problem") or ""
        if len(text) > 30:
            seen.setdefault(text, set()).add(r["batch"])
    shared = Counter(b for batches in seen.values() if len(batches) > 1 for b in batches)
    for batch, n in sorted(shared.items()):
        if n > 3:
            print(f"WARNING {batch}: {n} problems also appear in other batches; check for mixed-up results")

    with (DATA / "extraction.jsonl").open("w", encoding="utf-8") as f:
        for key, r in papers.items():
            if key in done and key not in bad:
                rec = {k: v for k, v in done[key].items() if k != "batch"}
                rec["pmdrl"] = {"who": who(r), **rec["pmdrl"]}
                f.write(json.dumps(rec | {"title": r["title"], "batch": done[key]["batch"]},
                                   ensure_ascii=False) + "\n")
    valid = [done[k] for k in papers if k in done and k not in bad]
    print(f"extracted {len(valid)}/{len(papers)} (invalid {len(bad)})")
    for field in CODES:
        counts = Counter(v for r in valid for v in r["codes"][field])
        print(f"{field}: " + ", ".join(f"{k} {n}" for k, n in counts.most_common()))
    human = sum(bool(r["codes"]["human_comparison"].get("done")) for r in valid)
    print(f"human_comparison done: {human}/{len(valid)}; "
          f"limitation stated: {sum(bool(r['pmdrl'].get('limitation')) for r in valid)}; "
          f"gap stated: {sum(bool(r['pmdrl'].get('gap')) for r in valid)}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("prepare")
    p.add_argument("--round", required=True)
    p.add_argument("--size", type=int, default=70)
    p.add_argument("--redo-filled", action="store_true", help="re-extract papers whose abstract `fill` fetched")
    sub.add_parser("fill")
    sub.add_parser("collect")
    args = parser.parse_args()
    {"prepare": prepare, "fill": fill, "collect": collect}[args.cmd](args)


if __name__ == "__main__":
    main()
