#!/usr/bin/env python3
"""App Store에 같은 이름을 쓰는 앱이 있는지 공개 검색 API로 확인한다.

이름이 앱 제목 **어디에든** 단어로 들어 있으면 겹친다고 본다.
("Swipe Photo Sorting - Albumate"처럼 부제 뒤에 이름을 붙이는 앱이 많다.)
App Store Connect에서 이름을 실제로 잡기 전의 1차 확인이다. 상표 검토를 대신하지 않는다.

사용: python3 -I app_name_check.py Fewshot Albumate --countries us kr jp
"""
import argparse
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request


def search(term, country):
    query = urllib.parse.urlencode({"term": term, "entity": "software", "country": country, "limit": 50})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(f"https://itunes.apple.com/search?{query}", timeout=20) as response:
                return [r["trackName"] for r in json.load(response).get("results", [])]
        except urllib.error.HTTPError as error:
            if error.code != 429:
                raise
            time.sleep(5 * (attempt + 1))
    raise RuntimeError(f"검색이 계속 막힌다 (429): {term} {country}")


def classify(term, names):
    """같은 단어로 쓰는 앱(taken)과 이름 안에 글자로만 들어 있는 앱(similar)으로 나눈다."""
    word = re.compile(rf"(?<![0-9a-z]){re.escape(term.lower())}(?![0-9a-z])")
    taken = [n for n in names if word.search(n.lower())]
    similar = [n for n in names if n not in taken and term.lower() in n.lower()]
    return taken, similar


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("names", nargs="+")
    parser.add_argument("--countries", nargs="+", default=["us", "kr", "jp", "de", "gb"])
    args = parser.parse_args()
    for name in args.names:
        taken, similar = {}, {}
        for country in args.countries:
            t, s = classify(name, search(name, country))
            if t: taken[country] = t
            if s: similar[country] = s
            time.sleep(0.5)
        status = "taken" if taken else ("similar" if similar else "free")
        detail = taken or similar
        print(f"{name}: {status}" + (f"  {json.dumps(detail, ensure_ascii=False)}" if detail else ""))


if __name__ == "__main__":
    main()
