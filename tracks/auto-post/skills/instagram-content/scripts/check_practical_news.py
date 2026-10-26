#!/usr/bin/env python3
"""Check declared freshness and usable companion files; does not verify source truth."""

import argparse
from datetime import date
import json
from pathlib import Path
import re
from urllib.parse import urlsplit


def inspect(manifest, base):
    errors, results = [], []
    try:
        edition = date.fromisoformat(manifest["edition_date"])
        window = manifest["freshness_window_days"]
        if isinstance(window, bool) or not isinstance(window, int) or window < 0:
            raise ValueError("freshness_window_days must be a nonnegative integer")
        stories = manifest["stories"]
        if not isinstance(stories, list) or not stories:
            raise ValueError("stories must be a nonempty list")
    except (KeyError, TypeError, ValueError) as exc:
        return [f"manifest: {exc}"], []

    base = Path(base).resolve()
    for index, story in enumerate(stories, 1):
        label = f"story {index}"
        before = len(errors)
        if not isinstance(story, dict):
            errors.append(f"{label}: expected an object")
            continue
        for field in ("title", "change_summary", "access_conditions", "evidence_status"):
            if not isinstance(story.get(field), str) or not story[field].strip():
                errors.append(f"{label}: missing {field}")
        for field in ("announcement_url", "entry_url"):
            parsed = urlsplit(story.get(field, "")) if isinstance(story.get(field, ""), str) else None
            if not parsed or parsed.scheme != "https" or not parsed.netloc:
                errors.append(f"{label}: {field} must be an HTTPS address")
        age = None
        try:
            age = (edition - date.fromisoformat(story["announcement_date"])).days
            if age < 0 or age > window:
                errors.append(f"{label}: original announcement is {age} days from edition; allowed 0–{window}")
        except (KeyError, TypeError, ValueError):
            errors.append(f"{label}: invalid original announcement_date")

        companions = {}
        for field in ("prompt_file", "caption_file"):
            try:
                relative = Path(story[field])
                path = (base / relative).resolve()
                if relative.is_absolute() or not path.is_relative_to(base):
                    raise ValueError("companion must stay inside the manifest directory")
                content = path.read_text(encoding="utf-8")
                if not content.strip():
                    raise ValueError("companion is empty")
                companions[field] = content
            except (KeyError, TypeError, ValueError, OSError) as exc:
                errors.append(f"{label}: {field}: {exc}")
        caption = companions.get("caption_file", "")
        limit = story.get("caption_max_characters", 499)
        hashtag_limit = story.get("max_hashtags", 3)
        for field, value in (("caption_max_characters", limit), ("max_hashtags", hashtag_limit)):
            if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                errors.append(f"{label}: invalid {field}")
        if isinstance(limit, int) and len(caption) > limit:
            errors.append(f"{label}: caption has {len(caption)} characters, limit {limit}")
        hashtags = len(re.findall(r"(?<!\w)#[\w]+", caption))
        if isinstance(hashtag_limit, int) and hashtags > hashtag_limit:
            errors.append(f"{label}: caption has {hashtags} hashtags, limit {hashtag_limit}")
        results.append({"title": story.get("title"), "announcement_age_days": age,
                        "caption_characters": len(caption), "hashtags": hashtags,
                        "passed": before == len(errors)})
    return errors, results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()
    try:
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        if not isinstance(manifest, dict):
            raise ValueError("manifest must be an object")
        errors, stories = inspect(manifest, args.manifest.parent)
    except (OSError, ValueError) as exc:
        errors, stories = [str(exc)], []
    print(json.dumps({"passed": not errors, "scope": "declared metadata and companion files; manual source/media review required",
                      "stories": stories, "errors": errors}, ensure_ascii=False, indent=2))
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
