#!/usr/bin/env python3
"""Builds the about, support and privacy pages for every store locale, and checks the live copies.

usage:
  python3 build_support_site.py build  path/to/kit.json   writes <site.out>/[<folder>/]{index,support,privacy}.html
  python3 build_support_site.py verify path/to/kit.json   fetches every page from site.baseUrl

The primary locale usually lives at the site root and every other locale in its own folder, so each
App Store localisation can link to a page in its own language. Copy comes from the JSON file named by
site.strings (one object per locale code, see references/kit.md). `{email}` becomes a mailto link and
`{refund}` a link to Apple's refund page wherever it appears in FAQ answers or the contact line.
"""
import argparse
import html
import importlib.util
import json
import pathlib
import re
import sys
import urllib.error
import urllib.request

sys.dont_write_bytecode = True  # keep the installed skill folder clean
spec = importlib.util.spec_from_file_location("kit", pathlib.Path(__file__).with_name("kit.py"))
kit_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kit_module)

REFUND = "https://reportaproblem.apple.com"
NEEDED = ["native", "languages", "indexDesc", "headline", "lead", "supportTitle", "supportDocTitle", "supportDesc",
          "faq", "contactTitle", "contact", "privacyTitle", "privacyDocTitle", "privacyDesc", "privacyUpdated",
          "privacy", "footer"]

CSS = """:root{--paper:#fff;--ink:#000;--graphite:#62656d;--quiet:#9a9da5;--mist:#eeeff1;--body:#2a2c31;color-scheme:light}
@media (prefers-color-scheme:dark){:root{--paper:#000;--ink:#fff;--graphite:#a3a6ad;--quiet:#6d7078;--mist:#1a1b1e;--body:#d9dade;color-scheme:dark}}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.6 -apple-system,BlinkMacSystemFont,"SF Pro Text","Apple SD Gothic Neo","Hiragino Sans","PingFang SC","PingFang TC","Noto Sans KR","Noto Sans JP","Noto Sans SC","Noto Sans Thai","Helvetica Neue",Arial,sans-serif;-webkit-font-smoothing:antialiased}
.page{max-width:680px;margin:0 auto;padding:40px 24px 72px}
.mark{font-weight:800;font-size:22px;letter-spacing:-.03em;color:var(--ink);text-decoration:none}
nav.langs{display:flex;gap:6px 16px;flex-wrap:wrap;font-size:14px;margin:28px 0 36px}
nav.langs a{color:var(--graphite);text-decoration:none}
nav.langs a:hover{text-decoration:underline}
nav.langs a[aria-current="page"]{color:var(--ink);font-weight:600}
h1{font-size:34px;line-height:1.2;letter-spacing:-.03em;margin:0 0 6px;text-wrap:balance}
.meta{color:var(--graphite);font-size:14px;margin:0 0 28px}
h2{font-size:18px;letter-spacing:-.01em;margin:28px 0 4px}
p{margin:0 0 12px;color:var(--body)}
a{color:var(--ink)}
.lead{font-size:18px;color:var(--ink)}
.links{display:flex;gap:20px;flex-wrap:wrap;margin-top:28px;font-size:15px}
.contact{background:var(--mist);border-radius:14px;padding:18px 20px;margin-top:28px}
.contact h2{margin-top:0}
.contact p{margin:0}
footer{margin-top:64px;color:var(--quiet);font-size:13px}
:focus-visible{outline:2px solid var(--ink);outline-offset:2px}
@media (max-width:480px){h1{font-size:28px}}"""


def load_strings(kit):
    path = kit.file(kit.site.get("strings", "site-strings.json"))
    strings = json.loads(path.read_text(encoding="utf-8"))
    for loc in kit.locales:
        s = strings.get(loc["code"])
        if s is None:
            raise SystemExit(f"{path.name}: no copy for {loc['code']}")
        missing = [k for k in NEEDED if k not in s]
        if missing:
            raise SystemExit(f"{path.name} {loc['code']}: missing {', '.join(missing)}")
        if "{email}" not in s["contact"]:
            raise SystemExit(f"{path.name} {loc['code']}: contact must contain {{email}}")
    return strings


def relative(kit, from_code, to_code, page):
    up = "../" if kit.folder(from_code) else ""
    folder = kit.folder(to_code)
    return f"{up}{folder + '/' if folder else ''}{page}"


def render(kit, strings, code, page, title, description, body):
    e = html.escape
    loc = kit.locale(code)
    lang_links = []
    for other in kit.locales:
        current = ' aria-current="page"' if other["code"] == code else ""
        lang_links.append(
            f'<a href="{relative(kit, code, other["code"], page)}" lang="{other["lang"]}" hreflang="{other["lang"]}"'
            f'{current}>{e(strings[other["code"]]["native"])}</a>')
    langs = "".join(lang_links)
    alternates = ""
    if kit.site.get("baseUrl"):
        primary = kit.app.get("primaryLocale", kit.locales[0]["code"])
        links = [f'<link rel="alternate" hreflang="{o["lang"]}" href="{kit.site_url(o["code"], page)}">' for o in kit.locales]
        links.append(f'<link rel="alternate" hreflang="x-default" href="{kit.site_url(primary, page)}">')
        alternates = "\n".join(links)
    mark = e(kit.site.get("mark", kit.app.get("name", "")))
    s = strings[code]
    return f"""<!doctype html>
<html lang="{loc['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
{alternates}
<style>
{kit.site.get('css', CSS)}
</style>
</head>
<body>
<div class="page">
<a class="mark" href="index.html">{mark}</a>
<nav class="langs" aria-label="{e(s['languages'])}">{langs}</nav>
{body}
<footer>{e(s['footer'])}</footer>
</div>
</body>
</html>
"""


def fill(text, email):
    out = html.escape(text)
    out = out.replace("{email}", f'<a href="mailto:{email}">{email}</a>')
    return out.replace("{refund}", f'<a href="{REFUND}">reportaproblem.apple.com</a>')


def build(kit):
    strings = load_strings(kit)
    email = kit.site.get("email")
    if not email:
        raise SystemExit("kit.json: site.email is required (App Review opens the support page to find a contact)")
    out_root = kit.file(kit.site.get("out", "site"))
    e = html.escape
    written = []
    for loc in kit.locales:
        code, s = loc["code"], strings[loc["code"]]
        out = out_root / kit.folder(code) if kit.folder(code) else out_root
        out.mkdir(parents=True, exist_ok=True)
        meta = kit.metadata(code) or {}
        links = (f'<p class="links"><a href="support.html">{e(s["supportTitle"])}</a>'
                 f'<a href="privacy.html">{e(s["privacyTitle"])}</a></p>')
        index = f'<section>\n<h1>{e(s["headline"])}</h1>\n<p class="lead">{e(s["lead"])}</p>\n{links}\n</section>'
        faq = "\n".join(f"<h2>{e(q)}</h2>\n<p>{fill(a, email)}</p>" for q, a in s["faq"])
        meta_line = f'<p class="meta">{e(s["supportMeta"])}</p>\n' if s.get("supportMeta") else ""
        support = (f'<section>\n<h1>{e(s["supportTitle"])}</h1>\n{meta_line}{faq}\n'
                   f'<div class="contact"><h2>{e(s["contactTitle"])}</h2><p>{fill(s["contact"], email)}</p></div>\n'
                   f'<p class="links"><a href="privacy.html">{e(s["privacyTitle"])}</a></p>\n</section>')
        sections = "\n".join(f"<h2>{e(h)}</h2>\n<p>{fill(p, email)}</p>" for h, p in s["privacy"])
        privacy = (f'<section>\n<h1>{e(s["privacyTitle"])}</h1>\n<p class="meta">{e(s["privacyUpdated"])}</p>\n'
                   f'{sections}\n<p class="links"><a href="support.html">{e(s["supportTitle"])}</a></p>\n</section>')
        index_title = s.get("indexTitle") or meta.get("name") or kit.app.get("name", "")
        for page, title, desc, body in [("index.html", index_title, s["indexDesc"], index),
                                        ("support.html", s["supportDocTitle"], s["supportDesc"], support),
                                        ("privacy.html", s["privacyDocTitle"], s["privacyDesc"], privacy)]:
            (out / page).write_text(render(kit, strings, code, page, title, desc, body), encoding="utf-8")
            written.append((out / page).relative_to(out_root).as_posix())
    print(f"{len(written)} pages in {out_root}")
    for loc in kit.locales:
        print(f"  {loc['code']:8} {kit.site_url(loc['code'], 'support.html') or relative(kit, kit.locales[0]['code'], loc['code'], 'support.html')}")


def verify(kit):
    if not kit.site.get("baseUrl"):
        raise SystemExit("kit.json: site.baseUrl is required to verify the live pages")
    email = kit.site.get("email", "")
    failed = 0
    for loc in kit.locales:
        for page in kit_module.SITE_PAGES:
            url = kit.site_url(loc["code"], page)
            request = urllib.request.Request(url, headers={"User-Agent": "app-store-release-verify"})
            problems = []
            try:
                with urllib.request.urlopen(request, timeout=20) as response:
                    status, text = response.status, response.read().decode("utf-8", "replace")
            except urllib.error.HTTPError as error:
                status, text = error.code, ""
            except urllib.error.URLError as error:
                status, text = f"error ({error.reason})", ""
            if status != 200:
                problems.append(f"HTTP {status}")
            else:
                lang = re.search(r'<html[^>]*\blang="([^"]+)"', text)
                if not lang or lang.group(1) != loc["lang"]:
                    problems.append(f"lang={lang.group(1) if lang else 'none'}, expected {loc['lang']}")
                if page == "support.html" and email and email not in text:
                    problems.append("support email missing")
            failed += bool(problems)
            print(f"{'FAIL' if problems else 'PASS'} {url}" + (f" -- {'; '.join(problems)}" if problems else ""))
    total = len(kit.locales) * len(kit_module.SITE_PAGES)
    print(f"{total - failed}/{total} pages live")
    sys.exit(1 if failed else 0)


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("command", choices=["build", "verify"])
    parser.add_argument("kit", help="kit.json")
    args = parser.parse_args()
    kit = kit_module.Kit(args.kit)
    build(kit) if args.command == "build" else verify(kit)


if __name__ == "__main__":
    main()
