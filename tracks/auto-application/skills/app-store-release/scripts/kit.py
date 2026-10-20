"""Reads the release kit shared by the app-store-release scripts.

A kit is one `kit.json` plus the files it points to (store metadata, site copy, review notes,
screenshots). Paths inside kit.json are relative to the kit.json file. See references/kit.md.
"""
import json
import pathlib
import re

# Store metadata headings -> field keys, and App Store Connect limits in characters.
FIELDS = {
    "name": "name",
    "subtitle": "subtitle",
    "promotional text": "promo",
    "keywords": "keywords",
    "description": "description",
    "what's new": "whatsNew",
}
LIMITS = {"name": 30, "subtitle": 30, "promo": 170, "keywords": 100, "description": 4000, "whatsNew": 4000}
REQUIRED = ("name", "keywords", "description")
SITE_PAGES = ("index.html", "support.html", "privacy.html")


def parse_metadata(text):
    """`## Heading` sections of a metadata file as {field key: value}; unknown headings are ignored."""
    fields = {}
    for match in re.finditer(r"^## (.+?)[ \t]*\n(.*?)(?=^## |\Z)", text, re.S | re.M):
        key = FIELDS.get(match.group(1).strip().lower())
        if key:
            fields[key] = match.group(2).strip()
    return fields


class Kit:
    def __init__(self, path):
        self.path = pathlib.Path(path).resolve()
        self.root = self.path.parent
        self.data = json.loads(self.path.read_text(encoding="utf-8"))
        self.app = self.data.get("app", {})
        self.locales = self.data.get("locales", [])
        if not self.locales:
            raise SystemExit(f"{self.path}: no locales")
        codes = [loc["code"] for loc in self.locales]
        if len(set(codes)) != len(codes):
            raise SystemExit(f"{self.path}: duplicate locale codes")
        self.site = self.data.get("site", {})
        self.screenshots = self.data.get("screenshots", {})

    def file(self, relative):
        return (self.root / relative).resolve()

    @property
    def metadata_dir(self):
        return self.file(self.data.get("metadataDir", "metadata"))

    def metadata(self, code):
        path = self.metadata_dir / f"{code}.md"
        return parse_metadata(path.read_text(encoding="utf-8")) if path.exists() else None

    def locale(self, code):
        for loc in self.locales:
            if loc["code"] == code:
                return loc
        raise KeyError(code)

    def folder(self, code):
        """Site folder of a locale ('' = site root)."""
        return self.locale(code).get("folder", "").strip("/")

    def site_url(self, code, page=""):
        base = self.site.get("baseUrl", "")
        if base and not base.endswith("/"):
            base += "/"
        folder = self.folder(code)
        return f"{base}{folder + '/' if folder else ''}{page}"
