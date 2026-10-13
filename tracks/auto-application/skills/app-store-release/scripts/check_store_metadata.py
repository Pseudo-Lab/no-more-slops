#!/usr/bin/env python3
"""Checks every locale's store metadata against App Store Connect limits before you paste it.

usage: python3 check_store_metadata.py path/to/kit.json [--strict]

FAIL (exit 1): a required field is missing, a field is over its limit, keywords have a space after
a comma or repeat a keyword, or a kit locale has no metadata file.
WARN: no subtitle or promotional text, a keyword that only repeats a word from the name or subtitle
(App Store search already indexes those), a name that doesn't start with the brand, or emoji,
exclamation marks, middle dots and ranking/price words. --strict turns warnings into failures.
"""
import argparse
import importlib.util
import pathlib
import re
import sys

sys.dont_write_bytecode = True  # keep the installed skill folder clean
spec = importlib.util.spec_from_file_location("kit", pathlib.Path(__file__).with_name("kit.py"))
kit_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kit_module)

EMOJI = re.compile(r"[\U0001F000-\U0001FAFF☀-➿️]")
STYLE = re.compile(r"[!！·・]")
CLAIMS = re.compile(r"\b(?:free|best|no\.?\s?1|#1|top[- ]rated)\b|무료|최고|1위|無料|免费|免費|gratis|gratuit|kostenlos", re.I)


def words(text):
    return {w for w in re.split(r"[\s:：,，、/|()（）\-–—]+", text.lower()) if w}


def check(fields, brands):
    fails, warns = [], []
    for key in kit_module.REQUIRED:
        if not fields.get(key):
            fails.append(f"{key} missing")
    for key in ("subtitle", "promo"):
        if not fields.get(key):
            warns.append(f"no {key}")
    for key, limit in kit_module.LIMITS.items():
        value = fields.get(key, "")
        if len(value) > limit:
            fails.append(f"{key} {len(value)}/{limit}")
    keywords = fields.get("keywords", "")
    if keywords:
        if re.search(r",\s", keywords):
            fails.append("keywords have a space after a comma")
        items = [k.strip().lower() for k in keywords.split(",") if k.strip()]
        repeated = sorted({k for k in items if items.count(k) > 1})
        if repeated:
            fails.append(f"keywords repeat {', '.join(repeated)}")
        shown = words(fields.get("name", "") + " " + fields.get("subtitle", ""))
        wasted = [k for k in items if k in shown]
        if wasted:
            warns.append(f"keywords repeat the name or subtitle: {', '.join(wasted)}")
    if brands and fields.get("name") and not fields["name"].startswith(tuple(brands)):
        warns.append("name doesn't start with the brand")
    short = " ".join(fields.get(k, "") for k in ("name", "subtitle", "keywords", "promo"))
    if EMOJI.search(short) or STYLE.search(short):
        warns.append("emoji, exclamation mark or middle dot in name, subtitle, keywords or promo")
    claim = CLAIMS.search(" ".join(fields.values()))
    if claim:
        warns.append(f"price or ranking word '{claim.group(0)}' (App Review guideline 2.3.7)")
    return fails, warns


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("kit", help="kit.json")
    parser.add_argument("--strict", action="store_true", help="treat warnings as failures")
    args = parser.parse_args()
    kit = kit_module.Kit(args.kit)
    brands = kit.app.get("brandPrefixes", [])
    failed = False
    for loc in kit.locales:
        code = loc["code"]
        fields = kit.metadata(code)
        if fields is None:
            print(f"FAIL {code}: no {kit.metadata_dir.name}/{code}.md")
            failed = True
            continue
        fails, warns = check(fields, brands)
        counts = ", ".join(f"{k} {len(fields.get(k, ''))}" for k in ("name", "subtitle", "promo", "keywords", "description"))
        status = "FAIL" if fails or (args.strict and warns) else ("WARN" if warns else "PASS")
        notes = "; ".join(fails + warns)
        print(f"{status} {code}: {counts}" + (f" -- {notes}" if notes else ""))
        failed |= status == "FAIL"
    extra = sorted(p.stem for p in kit.metadata_dir.glob("*.md")) if kit.metadata_dir.exists() else []
    unknown = [c for c in extra if c not in {loc["code"] for loc in kit.locales}]
    if unknown:
        print(f"WARN metadata files not listed in kit.json: {', '.join(unknown)}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
