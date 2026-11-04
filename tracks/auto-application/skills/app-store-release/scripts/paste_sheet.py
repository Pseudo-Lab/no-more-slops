#!/usr/bin/env python3
"""Builds a one-file HTML sheet of everything to paste into App Store Connect, per locale.

usage: python3 paste_sheet.py path/to/kit.json [-o paste-sheet.html]

The sheet follows the App Store Connect pages top to bottom (version page, App Information, App
Privacy, then kit.json `common` answers grouped by page). A language bar switches every
per-language field (name, subtitle, promotional text, description, keywords, what's new, support,
marketing and privacy URLs, screenshot folder) at once; each value has a copy button and a live
character count. Open it in a browser next to App Store Connect, or publish it as a private page.
"""
import argparse
import importlib.util
import json
import pathlib
import sys

sys.dont_write_bytecode = True  # keep the installed skill folder clean
spec = importlib.util.spec_from_file_location("kit", pathlib.Path(__file__).with_name("kit.py"))
kit_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kit_module)

TEMPLATE = pathlib.Path(__file__).resolve().parent.parent / "assets" / "paste-sheet.html"


def sheet_data(kit):
    shots_dir = kit.screenshots.get("dir", "screenshots")
    locales = []
    for loc in kit.locales:
        fields = kit.metadata(loc["code"])
        if fields is None:
            raise SystemExit(f"no metadata file for {loc['code']} in {kit.metadata_dir}")
        urls = {}
        if kit.site.get("baseUrl"):
            urls = {"support": kit.site_url(loc["code"], "support.html"),
                    "marketing": kit.site_url(loc["code"]),
                    "privacy": kit.site_url(loc["code"], "privacy.html")}
        locales.append({"code": loc["code"], "label": loc.get("label", loc["code"]), "fields": fields,
                        "urls": urls, "shotsDir": f"{shots_dir.rstrip('/')}/{loc['code']}"})
    review = dict(kit.data.get("review", {}))
    notes = ""
    if review.get("notes"):
        notes = kit.file(review.pop("notes")).read_text(encoding="utf-8").strip()
    return {
        "app": {k: kit.app.get(k, "") for k in ("name", "bundleId", "version", "build", "primaryLocale")},
        "locales": locales,
        "siteLive": bool(kit.site.get("live")),
        "screenshots": {k: kit.screenshots.get(k) for k in ("slot", "size")} | {
            "files": [f"{s['name']}.jpg" for s in kit.screenshots.get("shots", [])] or kit.screenshots.get("files", [])},
        "review": review,
        "notes": notes,
        "common": kit.data.get("common", []),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("kit", help="kit.json")
    parser.add_argument("-o", "--out", default=None, help="output HTML (default: paste-sheet.html beside kit.json)")
    args = parser.parse_args()
    kit = kit_module.Kit(args.kit)
    data = sheet_data(kit)
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    html = TEMPLATE.read_text(encoding="utf-8")
    html = html.replace("/*DATA*/null", payload).replace("__TITLE__", f"{kit.app.get('name', 'App')} 제출 시트")
    out = pathlib.Path(args.out) if args.out else kit.root / "paste-sheet.html"
    out.write_text(html, encoding="utf-8")
    print(f"{out} ({len(data['locales'])} locales)")


if __name__ == "__main__":
    main()
