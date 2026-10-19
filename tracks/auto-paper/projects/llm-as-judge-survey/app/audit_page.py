"""Build the human audit page from data/screening/audit.csv.

Embeds the include/exclude audit rows (not the maybe rows) with their
abstracts and links into templates/audit.html. Human decisions are stored
in the published page's db collection `audit`, not in this file.

Usage: uv run audit_page.py OUT.html [--include-maybe]
"""

import argparse
import csv
import json
from pathlib import Path

from common import DATA

TEMPLATE = Path(__file__).parent / "templates" / "audit.html"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("out", type=Path)
    parser.add_argument("--include-maybe", action="store_true")
    args = parser.parse_args()

    with (DATA / "candidates.csv").open(encoding="utf-8") as f:
        papers = {r["key"]: r for r in csv.DictReader(f)}
    with (DATA / "screening" / "audit.csv").open(encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if args.include_maybe or r["llm_decision"] != "maybe"]

    data = [{"key": r["key"], "title": r["title"], "year": papers[r["key"]]["year"],
             "venue": papers[r["key"]]["venue"], "doi": papers[r["key"]]["doi"],
             "arxiv": papers[r["key"]]["arxiv"], "abstract": papers[r["key"]]["abstract"],
             "llm_decision": r["llm_decision"], "llm_code": r["llm_code"], "llm_reason": r["llm_reason"]}
            for r in rows]
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    args.out.write_text(TEMPLATE.read_text(encoding="utf-8").replace("/*DATA*/[]", payload), encoding="utf-8")
    print(f"{len(data)} papers -> {args.out}")


if __name__ == "__main__":
    main()
