#!/usr/bin/env python3
r"""Checks Xcode string catalogs (.xcstrings) for every language the app ships.

usage: python3 check_xcstrings.py Localizable.xcstrings [InfoPlist.xcstrings ...] [options]

FAIL (exit 1):
  - a key has no translation (or an empty one) in a language
  - format specifiers (%@, %lld, %1$@ ...) differ from the source text
  - a catalog repeats a JSON key
  - --titles: a listed title ends with . 。 ． ! or ！ in any language
  - --brand: a Korean particle doesn't fit the brand's last syllable (톤릿는 -> 톤릿은)
  - --forbid [LANGS:]REGEX: the pattern appears (old brand names, removed features)
  - --only-in LANGS:REGEX: the pattern appears outside those languages (a local unit or scale)
WARN (fails only with --strict): translations not marked translated, stale keys no longer in code.

Languages default to every language found in the catalogs except the source language; pass
--languages to require more. LANGS is a comma list such as ko or ja,zh-Hans, or * for all.
In patterns, \b counts Hangul and kana as letters, so \bHaze\b misses "Haze로"; use
(?<![A-Za-z])Haze(?![A-Za-z]) for Latin words inside Korean or Japanese text.
"""
import argparse
import json
import pathlib
import re
import sys

SPECIFIER = re.compile(r"%(?:\d+\$)?(?:#@\w+@|[-+ 0#]*\d*(?:\.\d+)?(?:hh|h|ll|l|q|z|t|j)?[@dDuUxXoOfeEgGcCsSaA])")
TITLE_END = re.compile(r"[.。．!！]\s*$")
LANG_PREFIX = re.compile(r"^([A-Za-z*][\w*,-]*):(.+)$", re.S)


def no_duplicates(pairs):
    seen = {}
    for key, value in pairs:
        if key in seen:
            raise SystemExit(f"FAIL duplicate JSON key: {key}")
        seen[key] = value
    return seen


def specifiers(text):
    return sorted(re.sub(r"^%\d+\$", "%", s) for s in SPECIFIER.findall(text.replace("%%", "")))


def values(localization):
    """Every string a localization can show: the plain value or each plural/device variation."""
    found = []
    unit = localization.get("stringUnit")
    if unit is not None:
        found.append((unit.get("value", ""), unit.get("state", "translated")))
    for variation in localization.get("variations", {}).values():
        for case in variation.values():
            found.extend(values(case))
    for substitution in localization.get("substitutions", {}).values():
        found.extend(values(substitution))
    return found


def hangul_ending(text):
    """(has final consonant, final consonant is ㄹ) of the last Hangul syllable, or None."""
    for ch in reversed(text):
        code = ord(ch) - 0xAC00
        if 0 <= code < 11172:
            final = code % 28
            return final != 0, final == 8
    return None


def wrong_particles(brand, reading):
    ending = hangul_ending(reading)
    if ending is None:
        return None
    batchim, rieul = ending
    if batchim and not rieul:
        bad = ["는", "를", "가", "와", "로", "랑"]
    elif rieul:
        bad = ["는", "를", "가", "와", "으로", "이랑"]
    else:
        bad = ["은", "을", "과", "으로", "이랑"]
    tail = r"(?:서|써|부터)?"
    pattern = "|".join(re.escape(p) + (tail if p.endswith("로") else "") for p in bad)
    return re.compile(re.escape(brand) + rf"(?:{pattern})(?![가-힣])")


def scoped(spec, option):
    match = LANG_PREFIX.match(spec)
    langs, regex = (match.group(1).split(","), match.group(2)) if match else (["*"], spec)
    try:
        return langs, re.compile(regex)
    except re.error as error:
        raise SystemExit(f"{option} {spec!r}: {error}")


def applies(langs, lang):
    return "*" in langs or lang in langs


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("catalogs", nargs="+", type=pathlib.Path)
    parser.add_argument("--languages", nargs="*", help="languages that must be complete (default: all in the catalogs)")
    parser.add_argument("--titles", type=pathlib.Path, help="file with one title key per line")
    parser.add_argument("--brand", action="append", default=[], help="brand as written in Korean text, or SPELLING=READING (Tonlit=톤릿)")
    parser.add_argument("--forbid", action="append", default=[], help="[LANGS:]REGEX that must not appear")
    parser.add_argument("--only-in", action="append", default=[], help="LANGS:REGEX allowed only in those languages")
    parser.add_argument("--strict", action="store_true", help="warnings fail too")
    args = parser.parse_args()

    titles = set()
    if args.titles:
        titles = {line.strip() for line in args.titles.read_text(encoding="utf-8").splitlines() if line.strip()}
    brands = []
    for spec in args.brand:
        spelling, _, reading = spec.partition("=")
        rule = wrong_particles(spelling, reading or spelling)
        if rule is None:
            raise SystemExit(f"--brand {spec!r}: give the Korean reading, e.g. --brand {spelling}=톤릿")
        brands.append(rule)
    forbid = [scoped(s, "--forbid") for s in args.forbid]
    only_in = [scoped(s, "--only-in") for s in args.only_in]

    fails, warns, counted, seen_titles = [], [], 0, set()
    for path in args.catalogs:
        catalog = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=no_duplicates)
        source = catalog.get("sourceLanguage", "en")
        strings = catalog.get("strings", {})
        languages = args.languages or sorted({lang for e in strings.values() for lang in e.get("localizations", {})} - {source})
        stale = 0
        for key, entry in strings.items():
            if entry.get("shouldTranslate") is False:
                continue
            if entry.get("extractionState") == "stale":
                stale += 1
            local = entry.get("localizations", {})
            source_values = values(local[source]) if source in local else [(key, "translated")]
            source_text = " ".join(v for v, _ in source_values)
            if not source_text.strip():
                continue
            counted += 1
            expected = specifiers(source_text)
            texts = {source: source_text}
            for lang in languages:
                found = values(local.get(lang, {}))
                if not found or any(not v.strip() for v, _ in found):
                    fails.append(f"{path.name} [{lang}] missing: {key}")
                    continue
                text = " ".join(v for v, _ in found)
                texts[lang] = text
                variations = "variations" in local.get(lang, {})
                got = specifiers(text)
                if (set(got) != set(expected)) if variations else (got != expected):
                    fails.append(f"{path.name} [{lang}] format specifiers {got} vs {expected}: {key}")
                if any(state != "translated" for _, state in found):
                    warns.append(f"{path.name} [{lang}] not marked translated: {key}")
            if key in titles:
                seen_titles.add(key)
                for lang, text in texts.items():
                    if TITLE_END.search(text):
                        fails.append(f"{path.name} [{lang}] title ends with punctuation: {text}")
            for lang, text in texts.items():
                if lang == "ko" or lang.startswith("ko-"):
                    for rule in brands:
                        for match in rule.finditer(text):
                            fails.append(f"{path.name} [{lang}] Korean particle after brand: {match.group(0)} in {text!r}")
                for langs, regex in forbid:
                    if applies(langs, lang) and regex.search(text):
                        fails.append(f"{path.name} [{lang}] forbidden {regex.pattern!r}: {text}")
                for langs, regex in only_in:
                    if not applies(langs, lang) and regex.search(text):
                        fails.append(f"{path.name} [{lang}] {regex.pattern!r} outside {','.join(langs)}: {text}")
        if stale:
            warns.append(f"{path.name}: {stale} stale keys (no longer in code; delete them in Xcode)")
        print(f"{path.name}: {len(strings)} keys, source {source}, checked {', '.join(languages) or 'no other languages'}")
    for missing in sorted(titles - seen_titles):
        fails.append(f"title key not in any catalog: {missing}")

    for label, items in (("FAIL", fails), ("WARN", warns)):
        for line in items[:40]:
            print(f"{label} {line}")
        if len(items) > 40:
            print(f"{label} ... {len(items) - 40} more")
    failed = bool(fails) or (args.strict and bool(warns))
    print(f"{'FAIL' if failed else 'PASS'} {counted} strings, {len(fails)} failures, {len(warns)} warnings")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
