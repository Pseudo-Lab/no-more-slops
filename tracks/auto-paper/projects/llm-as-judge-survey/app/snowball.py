"""Seed lists and citation snowballing via Semantic Scholar.

seeds:   arXiv IDs listed in curated awesome lists, resolved to metadata.
snowball: references and citations of the seed surveys (one hop).
bib:      arXiv IDs in the seed surveys' HTML bibliographies.

Usage: uv run snowball.py [seeds|snowball|bib ...]
Optional env: SEMANTIC_SCHOLAR_API_KEY.
"""

import argparse
import re
import time

from common import get_json, request, s2_headers, save
from search import S2_FIELDS, s2_record

SURVEYS = {
    "2411.15594": "A Survey on LLM-as-a-Judge",
    "2411.16594": "From Generation to Judgment",
    "2412.05579": "LLMs-as-Judges: A Comprehensive Survey",
    "2603.29403": "Security in LLM-as-a-Judge: SoK",
    "2605.25273": "LLM-as-a-Judge in Healthcare",
    "2510.24367": "From Code to Courtroom",
}

AWESOME_LISTS = {
    "llm-as-a-judge/Awesome-LLM-as-a-judge": "https://raw.githubusercontent.com/llm-as-a-judge/Awesome-LLM-as-a-judge/main/README.md",
    "CSHaitao/Awesome-LLMs-as-Judges": "https://raw.githubusercontent.com/CSHaitao/Awesome-LLMs-as-Judges/main/README.md",
}

ARXIV_LINK = re.compile(r"arxiv\.org/(?:abs|pdf|html)/(\d{4}\.\d{4,5})")
BIB_ID = re.compile(r"(?:arxiv\.org/(?:abs|pdf)/|arXiv:|abs/)(\d{4}\.\d{4,5})")


def batch(ids, source, query):
    out = []
    for i in range(0, len(ids), 400):
        papers = get_json("https://api.semanticscholar.org/graph/v1/paper/batch", {"fields": S2_FIELDS},
                          data={"ids": ids[i:i + 400]}, headers=s2_headers())
        out += [s2_record(p, source, query) for p in papers if p]
        time.sleep(1.5)
    return out


def seeds():
    for name, url in AWESOME_LISTS.items():
        text = request(url).decode("utf-8", "replace")
        ids = sorted(set(ARXIV_LINK.findall(text)))
        save("seeds", "awesome", name, batch([f"arXiv:{i}" for i in ids], "awesome", name))


def edges(paper, direction):
    key = "citingPaper" if direction == "citations" else "citedPaper"
    params = {"fields": S2_FIELDS, "limit": 1000, "offset": 0}
    out = []
    while True:
        page = get_json(f"https://api.semanticscholar.org/graph/v1/paper/arXiv:{paper}/{direction}",
                        params, headers=s2_headers())
        out += [s2_record(e[key], f"s2-{direction}", f"{direction}:{paper}")
                for e in page.get("data") or [] if e.get(key, {}).get("paperId")]
        if "next" not in page:
            return out
        params["offset"] = page["next"]
        time.sleep(1.5)


def snowball():
    try:
        save("seeds", "survey", "surveys", batch([f"arXiv:{i}" for i in SURVEYS], "seed-survey", "surveys"))
    except Exception as err:
        print(f"[seeds/survey] surveys: FAILED {err!r}")
    for paper in SURVEYS:
        for direction in ("references", "citations"):
            try:
                save("snowball", direction, f"{direction}:{paper}", edges(paper, direction))
            except Exception as err:
                print(f"[snowball/{direction}] {paper}: FAILED {err!r}")
            time.sleep(1.5)


def bib():
    """Fallback for surveys whose references Semantic Scholar withholds: arXiv IDs in the HTML bibliography."""
    for paper in SURVEYS:
        try:
            text = request(f"https://arxiv.org/html/{paper}").decode("utf-8", "replace")
            ids = sorted(set(BIB_ID.findall(text)) - {paper})
            save("snowball", "bib", f"bib:{paper}", batch([f"arXiv:{i}" for i in ids], "arxiv-bib", f"bib:{paper}"))
        except Exception as err:
            print(f"[snowball/bib] {paper}: FAILED {err!r}")


STEPS = {"seeds": seeds, "snowball": snowball, "bib": bib}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("steps", nargs="*", choices=STEPS)
    for step in parser.parse_args().steps or STEPS:
        STEPS[step]()


if __name__ == "__main__":
    main()
