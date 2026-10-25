"""Normalize author lists in manuscript/references.md to the ICMJE/Vancouver rule.

For each entry with an arXiv id or DOI, fetch the author list from the arXiv API or Crossref and
rewrite the author segment (text before the first ". ") as "Family AB, Family C, ..." with up to
six authors, followed by "et al." when there are seven or more. Entries authored by organizations
or without identifiers are left unchanged. Long proceedings names are shortened to "Proc <venue>".
Fetched author lists are cached in data/authors.json so reruns need no network.

Usage:
    uv run normalize_refs.py [--dry-run]
"""
import argparse
import json
import re
import time
import unicodedata
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REFS = ROOT / "manuscript" / "references.md"
CACHE = ROOT / "data" / "authors.json"
UA = {"User-Agent": "golden-dataset-review/0.1 (reference normalization)"}

VENUES = [  # long proceedings names -> short form
    (r"In: Proceedings of the \d+\w* Annual Meeting of the Association for Computational Linguistics(?: and the \d+\w* International Joint Conference on Natural Language Processing)? \(Volume 1: Long Papers\)", "In: Proc ACL"),
    (r"In: Proceedings of the \d+ Conference of the (?:North American Chapter|Nations of the Americas Chapter) of the Association for Computational Linguistics: Human Language Technologies \(Volume 1: Long Papers\)", "In: Proc NAACL"),
    (r"In: Proceedings of the \d+ Conference on Empirical Methods in Natural Language Processing: System Demonstrations", "In: Proc EMNLP System Demonstrations"),
    (r"In: Proceedings of the \d+ Conference on Empirical Methods in Natural Language Processing", "In: Proc EMNLP"),
    (r"In: Proceedings of the \d+ Joint International Conference on Computational Linguistics, Language Resources and Evaluation \(LREC-COLING \d+\)", "In: Proc LREC-COLING"),
    (r"In: Proceedings of the \d+\w* International Conference on Machine Learning \(ICML \d+\), (PMLR \d+)", r"In: Proc ICML (\1)"),
    (r"In: Proceedings of the Fourth Workshop on Generation, Evaluation and Metrics \(GEM²\)", "In: Proc GEM² Workshop"),
    (r"In: Advances in Neural Information Processing Systems 38 \(NeurIPS 2025\)", "In: Proc NeurIPS"),
    (r"In: Thirty-fifth Conference on Neural Information Processing Systems \(NeurIPS 2021\) Datasets and Benchmarks Track", "In: Proc NeurIPS Datasets and Benchmarks Track"),
    (r"In: NeurIPS Datasets and Benchmarks Track", "In: Proc NeurIPS Datasets and Benchmarks Track"),
    (r"Proceedings of the National Academy of Sciences of the United States of America; (\d{4})\. (\d+)\((\d+)\) (e\d+)", r"Proc Natl Acad Sci U S A. \1;\2(\3):\4"),
    (r"Computational Linguistics; (\d{4})\. (\d+)\((\d+)\) p\. ([\d-]+)", r"Comput Linguist. \1;\2(\3):\4"),
    (r"Science; (\d{4})\. (\d+)\((\d+)\) p\. ([\d-]+)", r"Science. \1;\2(\3):\4"),
    (r"Nature; (\d{4})\. (\d+)\((\d+)\) p\. ([\d-]+)", r"Nature. \1;\2(\3):\4"),
    (r"arXiv preprint; (\d{4})\. (arXiv:\d{4}\.\d{4,5})\.?", r"\2. \1."),
    (r"In: Proc AAAI; (\d{4});(\d+)\((\d+)\):", r"Proc AAAI Conf Artif Intell. \1;\2(\3):"),
]

OVERRIDES = {  # names that initials logic or the metadata source gets wrong
    "gebru2021": "Gebru T, Morgenstern J, Vecchione B, Vaughan JW, Wallach H, Daumé III H, et al.",
    "polo2024": "Maia Polo F, Weber L, Choshen L, Sun Y, Xu G, Yurochkin M",
    "sainz2023": "Sainz O, Campos JA, García-Ferrero I, Etxaniz J, Lopez de Lacalle O, Agirre E",
    "boyeau2024": "Boyeau P, Angelopoulos AN, Li T, Yosef N, Malik J, Jordan MI",
    "hle": "Center for AI Safety, Scale AI, HLE Contributors Consortium.",
    "rebholz2010": "Rebholz-Schuhmann D, Jimeno Yepes AJ, van Mulligen EM, Kang N, Kors J, Milward D, et al.",
}


def pages(body):
    """Write page ranges after "p. " or a volume colon in full with an en dash (4843–55 -> 4843–4855)."""
    def full(m):
        a, b = m[2], m[3]
        return f"{m[1]}{a}–{a[:len(a) - len(b)] + b if len(b) < len(a) else b}"
    return re.sub(r"(p\. |\):|;\d+:)(\d+)[-–](\d+)", full, body)


def initials(given):
    parts = re.split(r"[\s.\-]+", given.strip())
    return "".join(p[0].upper() for p in parts if p and p[0].isalpha())


def fmt(people):
    names = [f"{fam} {initials(giv)}".strip() for fam, giv in people]
    return ", ".join(names[:6]) + (", et al." if len(names) > 6 else "")


def fetch_arxiv(aid):
    url = f"http://export.arxiv.org/api/query?id_list={aid}"
    xml = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read()
    ns = {"a": "http://www.w3.org/2005/Atom"}
    entry = ET.fromstring(xml).find("a:entry", ns)
    people = []
    for a in entry.findall("a:author/a:name", ns):
        toks = a.text.strip().split()
        people.append((toks[-1], " ".join(toks[:-1])))
    return people


def fetch_doi(doi):
    url = f"https://api.crossref.org/works/{doi}"
    data = json.loads(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30).read())
    return [(a.get("family", ""), a.get("given", "")) for a in data["message"].get("author", []) if a.get("family")]


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    lines = REFS.read_text(encoding="utf-8").splitlines()
    out = []
    for line in lines:
        m = re.match(r"^- ([\w-]+): (.+)$", line)
        if not m:
            out.append(line)
            continue
        key, body = m[1], m[2]
        for pat, rep in VENUES:
            body = re.sub(pat, rep, body)
        authors, sep, rest = body.partition(". ")
        org = not re.search(r"[A-Z][a-z]+ [A-Z]{1,3}(,|$| et al)", authors)
        ident = re.search(r"arXiv:(\d{4}\.\d{4,5})", body)
        doi = re.search(r"doi:(10\.\S+?)\.?(?:\s|$)", body)
        if not org and (ident or doi):
            if key not in cache:
                try:
                    cache[key] = fetch_doi(doi[1]) if doi else fetch_arxiv(ident[1])
                except Exception as exc:  # keep the line as is when the lookup fails
                    print(f"{key}: lookup failed ({exc})")
                    cache[key] = []
                time.sleep(1)
            if cache[key]:
                authors = unicodedata.normalize("NFC", fmt(cache[key]))
        authors = OVERRIDES.get(key, authors)
        if authors.endswith("."):
            sep = " "
        out.append(f"- {key}: {authors}{sep}{pages(rest)}")
    CACHE.parent.mkdir(exist_ok=True)
    CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=1), encoding="utf-8")
    if args.dry_run:
        print("\n".join(out))
    else:
        REFS.write_text("\n".join(out) + "\n", encoding="utf-8")
        print(f"normalized {sum(1 for l in out if l.startswith('- '))} entries")


if __name__ == "__main__":
    main()
