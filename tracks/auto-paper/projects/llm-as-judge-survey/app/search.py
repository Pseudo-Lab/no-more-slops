"""Keyword search over OpenAlex, arXiv, and Semantic Scholar.

Usage: uv run search.py [--sources openalex arxiv s2]
Optional env: OPENALEX_API_KEY, SEMANTIC_SCHOLAR_API_KEY.
"""

import argparse
import json
import os
import time
import xml.etree.ElementTree as ET
from pathlib import Path

from common import arxiv_id, get_json, record, request, s2_headers, save

QUERIES = json.loads((Path(__file__).parent / "queries.json").read_text())
ATOM = {"a": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}


def openalex_abstract(index):
    if not index:
        return ""
    words = sorted((pos, word) for word, positions in index.items() for pos in positions)
    return " ".join(word for _, word in words)


def openalex(phrase):
    params = {
        "filter": f"from_publication_date:{QUERIES['date_from']},to_publication_date:{QUERIES['date_to']},"
                  f'title_and_abstract.search:"{phrase}"',
        "per-page": 200,
        "cursor": "*",
        "select": "id,doi,title,publication_year,publication_date,primary_location,ids,"
                  "authorships,cited_by_count,abstract_inverted_index",
    }
    if key := os.environ.get("OPENALEX_API_KEY"):
        params["api_key"] = key
    out = []
    while params["cursor"]:
        page = get_json("https://api.openalex.org/works", params)
        for w in page["results"]:
            source = (w.get("primary_location") or {}).get("source") or {}
            out.append(record(
                "openalex", phrase, title=w.get("title"), year=w.get("publication_year"),
                date=w.get("publication_date"), venue=source.get("display_name"), doi=w.get("doi"),
                openalex_id=w["id"].rsplit("/", 1)[-1],
                authors="; ".join(a["author"]["display_name"] for a in w.get("authorships", [])[:10]),
                cited_by=w.get("cited_by_count"), abstract=openalex_abstract(w.get("abstract_inverted_index"))))
        params["cursor"] = page["meta"].get("next_cursor")
    return out


def arxiv(phrase):
    start, out, size = 0, [], 500
    lo, hi = (QUERIES[k].replace("-", "") for k in ("date_from", "date_to"))
    query = f'(ti:"{phrase}" OR abs:"{phrase}") AND submittedDate:[{lo}0000 TO {hi}2359]'
    while True:
        xml = request("https://export.arxiv.org/api/query",
                      {"search_query": query, "start": start, "max_results": size})
        entries = ET.fromstring(xml).findall("a:entry", ATOM)
        for e in entries:
            doi = e.findtext("arxiv:doi", "", ATOM)
            out.append(record(
                "arxiv", phrase, title=" ".join(e.findtext("a:title", "", ATOM).split()),
                date=e.findtext("a:published", "", ATOM)[:10], year=e.findtext("a:published", "", ATOM)[:4],
                venue=e.findtext("arxiv:journal_ref", "", ATOM) or "arXiv", doi=doi,
                arxiv=arxiv_id(e.findtext("a:id", "", ATOM)),
                authors="; ".join(a.findtext("a:name", "", ATOM) for a in e.findall("a:author", ATOM)[:10]),
                abstract=" ".join(e.findtext("a:summary", "", ATOM).split())))
        if len(entries) < size:
            return out
        start += size
        time.sleep(3)


S2_FIELDS = "paperId,title,year,publicationDate,venue,externalIds,authors,citationCount,abstract"


def s2_record(p, source, query):
    ext = p.get("externalIds") or {}
    return record(
        source, query, title=p.get("title"), year=p.get("year"), date=p.get("publicationDate"),
        venue=p.get("venue"), doi=ext.get("DOI"), arxiv=ext.get("ArXiv"), s2_id=p.get("paperId"),
        authors="; ".join(a.get("name", "") for a in (p.get("authors") or [])[:10]),
        cited_by=p.get("citationCount"), abstract=p.get("abstract"))


def s2(phrase):
    params = {"query": f'"{phrase}"', "fields": S2_FIELDS,
              "publicationDateOrYear": f"{QUERIES['date_from']}:{QUERIES['date_to']}"}
    out = []
    while True:
        page = get_json("https://api.semanticscholar.org/graph/v1/paper/search/bulk", params, headers=s2_headers())
        out += [s2_record(p, "s2", phrase) for p in page.get("data") or []]
        if not page.get("token"):
            return out
        params["token"] = page["token"]
        time.sleep(1.5)


SOURCES = {"openalex": openalex, "arxiv": arxiv, "s2": s2}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sources", nargs="+", choices=SOURCES, default=list(SOURCES))
    parser.add_argument("--phrases", nargs="+", default=QUERIES["phrases"])
    args = parser.parse_args()
    for name in args.sources:
        for phrase in args.phrases:
            try:
                save("search", name, phrase, SOURCES[name](phrase))
            except Exception as err:
                print(f"[search/{name}] {phrase}: FAILED {err!r}")
            time.sleep(3 if name == "arxiv" else 1.5)


if __name__ == "__main__":
    main()
