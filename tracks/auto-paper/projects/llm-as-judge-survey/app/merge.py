"""Deduplicate raw records into data/candidates.csv.

Records match on arXiv ID, DOI, or normalized title. Records dated before
queries.json date_from are dropped and counted.

Usage: uv run merge.py
"""

import csv
import json
import re
from collections import Counter

from common import DATA, RAW, arxiv_id, norm_title
from search import QUERIES

FIELDS = ["key", "title", "year", "date", "venue", "doi", "arxiv", "s2_id", "openalex_id",
          "authors", "cited_by", "title_hit", "sources", "queries", "abstract"]
TITLE_HIT = re.compile(r"judg|jury|evaluator|as-a-|meta-evaluat|reward model", re.I)


def keys(rec):
    out = []
    if rec["arxiv"]:
        out.append("arxiv:" + rec["arxiv"])
    if rec["doi"] and "arxiv" not in rec["doi"]:
        out.append("doi:" + rec["doi"])
    if len(title := norm_title(rec["title"])) > 20:
        out.append("title:" + title)
    return out


def main():
    groups, index = [], {}
    for path in sorted(RAW.rglob("*.jsonl")):
        for line in path.open(encoding="utf-8"):
            rec = json.loads(line)
            # Raw OpenAlex records from before 2026-10-19 took arXiv IDs from DOI landing URLs; re-derive.
            rec["arxiv"] = arxiv_id(rec["doi"]) if rec["source"] == "openalex" else arxiv_id(rec["arxiv"])
            ks = keys(rec)
            if not ks:
                continue
            hits = {index[k] for k in ks if k in index}
            if hits:
                gid = min(hits)
                for other in hits - {gid}:
                    groups[gid] += groups[other]
                    groups[other] = []
                    for k, v in index.items():
                        if v == other:
                            index[k] = gid
            else:
                gid = len(groups)
                groups.append([])
            groups[gid].append(rec)
            for k in ks:
                index[k] = gid

    rows, dropped = [], 0
    for recs in filter(None, groups):
        row = {f: "" for f in FIELDS}
        for rec in sorted(recs, key=lambda r: r["source"] != "arxiv"):
            for f in FIELDS:
                if not row[f] and rec.get(f):
                    row[f] = rec[f]
        dates = [str(r["date"] or r["year"]) for r in recs if r["date"] or r["year"]]
        if dates and min(dates)[:4] < QUERIES["date_from"][:4]:
            dropped += 1
            continue
        for f in ("title", "venue", "authors", "abstract"):
            row[f] = " ".join(str(row[f]).split())
        row["key"] = keys(row)[0]
        row["sources"] = ";".join(sorted({r["source"] for r in recs}))
        row["queries"] = " | ".join(sorted({r["query"] for r in recs}))
        row["title_hit"] = int(bool(TITLE_HIT.search(row["title"])))
        rows.append(row)

    rows.sort(key=lambda r: (-r["title_hit"], -int(r["cited_by"] or 0)))
    with (DATA / "candidates.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    print(f"candidates: {len(rows)} (dropped {dropped} before {QUERIES['date_from'][:4]})")
    print(f"title_hit: {sum(r['title_hit'] for r in rows)}")
    for source, n in Counter(s for r in rows for s in r["sources"].split(";")).most_common():
        print(f"  {source}: {n}")


if __name__ == "__main__":
    main()
