"""Shared helpers: HTTP with backoff, record normalization, search log."""

import csv
import datetime as dt
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
DATA = PROJECT / "data"
RAW = DATA / "raw"
LOG = DATA / "search_log.csv"
USER_AGENT = "llm-as-judge-survey/0.1 (literature review tooling)"

ARXIV_ID = re.compile(r"(\d{4}\.\d{4,5})(?:v\d+)?")


def request(url, params=None, data=None, headers=None, retries=12):
    if params:
        url += "?" + urllib.parse.urlencode(params)
    body = json.dumps(data).encode() if data is not None else None
    headers = {"User-Agent": USER_AGENT, **(headers or {})}
    if body is not None:
        headers["Content-Type"] = "application/json"
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, body, headers), timeout=60) as resp:
                return resp.read()
        except urllib.error.HTTPError as err:
            if err.code not in {429, 500, 502, 503, 504} or attempt == retries - 1:
                raise
        except (urllib.error.URLError, TimeoutError):
            if attempt == retries - 1:
                raise
        time.sleep(min(2 ** attempt * 2, 90))


def get_json(url, params=None, data=None, headers=None):
    return json.loads(request(url, params, data, headers))


def arxiv_id(*values):
    for value in values:
        if value and (m := ARXIV_ID.search(str(value))):
            return m[1]
    return ""


def norm_title(title):
    return re.sub(r"[^a-z0-9]+", " ", (title or "").lower()).strip()


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:60]


def record(source, query, **fields):
    keys = ["title", "year", "date", "venue", "doi", "arxiv", "s2_id", "openalex_id",
            "authors", "cited_by", "abstract"]
    rec = {"source": source, "query": query}
    rec.update({k: fields.get(k) or "" for k in keys})
    rec["doi"] = rec["doi"].lower().removeprefix("https://doi.org/")
    rec["arxiv"] = rec["arxiv"] or arxiv_id(rec["doi"] if "arxiv" in rec["doi"] else "")
    return rec


def save(step, source, query, records):
    path = RAW / step / source / f"{slug(query)}.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    new = not LOG.exists()
    with LOG.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if new:
            writer.writerow(["run_at", "step", "source", "query", "records", "file"])
        writer.writerow([dt.datetime.now().isoformat(timespec="seconds"), step, source, query,
                         len(records), path.relative_to(PROJECT).as_posix()])
    print(f"[{step}/{source}] {query}: {len(records)}")


def s2_headers():
    key = os.environ.get("SEMANTIC_SCHOLAR_API_KEY")
    return {"x-api-key": key} if key else {}
