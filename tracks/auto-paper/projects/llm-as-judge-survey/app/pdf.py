"""Build a PDF of the manuscript from manuscript/build/paper.md.

Converts the small Markdown subset the manuscript uses (headings, paragraphs, lists, tables,
bold, inline code) to HTML with the standard library, then prints it with headless Chromium.
Run `uv run manuscript.py render` first.

Usage:
    uv run pdf.py [--out PATH] [--status 초안]
"""
import argparse
import html
import re
import shutil
import subprocess
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "manuscript" / "build"
BROWSERS = ("chromium", "chromium-browser", "google-chrome", "google-chrome-stable")

CSS = """
@page { size: A4; margin: 22mm 20mm 22mm 20mm;
        @bottom-center { content: counter(page); font-size: 9pt; } }
body { font-family: 'Noto Serif KR', 'Batang', serif; font-size: 10.5pt; line-height: 1.75;
       color: #111; word-break: keep-all; overflow-wrap: break-word; }
h1, h2, h3, h4 { font-family: 'Noto Sans KR', 'Malgun Gothic', sans-serif; line-height: 1.4;
                 break-after: avoid; }
h1 { font-size: 17pt; margin: 0 0 14pt; break-before: page; }
h1.title { font-size: 20pt; break-before: auto; margin-top: 30mm; }
h2 { font-size: 13pt; margin: 18pt 0 8pt; }
h3 { font-size: 11.5pt; margin: 14pt 0 6pt; }
p { margin: 0 0 8pt; text-align: justify; }
.meta { font-family: 'Noto Sans KR', sans-serif; font-size: 9.5pt; color: #444; margin-bottom: 18mm; }
code { font-family: 'Noto Sans Mono', 'Consolas', monospace; font-size: 9pt; }
ul, ol { margin: 0 0 8pt; padding-left: 18pt; }
li { margin-bottom: 3pt; }
table { border-collapse: collapse; margin: 6pt 0 12pt; font-size: 8.8pt; line-height: 1.45;
        width: 100%; break-inside: auto; }
th, td { border-top: 0.5pt solid #999; border-bottom: 0.5pt solid #999; padding: 3pt 5pt;
         vertical-align: top; text-align: left; }
th { background: #f0f0f0; font-family: 'Noto Sans KR', sans-serif; }
td.num, th.num { text-align: right; }
tr { break-inside: avoid; }
p.caption { font-family: 'Noto Sans KR', sans-serif; font-size: 9.5pt; margin: 10pt 0 2pt;
            break-after: avoid; }
ol.refs { font-size: 8.8pt; line-height: 1.5; padding-left: 26pt; }
"""


def inline(text):
    out = html.escape(text, quote=False)
    out = re.sub(r"`([^`]+)`", r"<code>\1</code>", out)
    out = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", out)
    return out


def table(rows):
    cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
    head, align, body = cells[0], cells[1], cells[2:]
    num = [a.endswith(":") and not a.startswith(":") for a in align]

    def row(tag, values):
        return "<tr>" + "".join(f'<{tag}{" class=num" if num[i] else ""}>{inline(v)}</{tag}>'
                                for i, v in enumerate(values)) + "</tr>"

    return ("<table><thead>" + row("th", head) + "</thead><tbody>"
            + "".join(row("td", r) for r in body) + "</tbody></table>")


def convert(md):
    lines, out, i = md.splitlines(), [], 0
    first_h1 = True
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if m := re.match(r"^(#{1,4})\s+(.*)$", line):
            level, text = len(m[1]), m[2]
            cls = ' class="title"' if level == 1 and first_h1 else ""
            first_h1 = first_h1 and level != 1
            out.append(f"<h{level}{cls}>{inline(text)}</h{level}>")
            i += 1
            continue
        if line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append(lines[i])
                i += 1
            out.append(table(rows))
            continue
        if re.match(r"^\s*[-*] ", line):
            items = []
            while i < len(lines) and re.match(r"^\s*[-*] ", lines[i]):
                items.append(re.sub(r"^\s*[-*] ", "", lines[i]))
                i += 1
            out.append("<ul>" + "".join(f"<li>{inline(t)}</li>" for t in items) + "</ul>")
            continue
        if re.match(r"^\d+\. ", line):
            items, start = [], int(line.split(".")[0])
            while i < len(lines) and re.match(r"^\d+\. ", lines[i]):
                items.append(re.sub(r"^\d+\. ", "", lines[i]))
                i += 1
            refs = ' class="refs"' if len(items) > 50 else ""
            out.append(f'<ol start="{start}"{refs}>' + "".join(f"<li>{inline(t)}</li>" for t in items) + "</ol>")
            continue
        if re.fullmatch(r"\*\*(표|그림) .+\*\*", line.strip()):
            out.append(f'<p class="caption">{inline(line.strip())}</p>')
            i += 1
            continue
        out.append(f"<p>{inline(line.strip())}</p>")
        i += 1
    return "\n".join(out)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out", type=Path, default=BUILD / "paper.pdf")
    parser.add_argument("--status", default="초안")
    args = parser.parse_args()

    body = convert((BUILD / "paper.md").read_text(encoding="utf-8"))
    meta = f'<p class="meta">{html.escape(args.status)} · {date.today().isoformat()}</p>'
    body = body.replace("</h1>", "</h1>\n" + meta, 1)
    page = (f'<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>paper</title>'
            f"<style>{CSS}</style></head><body>{body}</body></html>")
    page_path = BUILD / "paper.html"
    page_path.write_text(page, encoding="utf-8")

    browser = next((b for b in BROWSERS if shutil.which(b)), None)
    if not browser:
        raise SystemExit("no Chromium found; open manuscript/build/paper.html and print to PDF")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([browser, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={args.out.resolve()}", page_path.resolve().as_uri()],
                   check=True, capture_output=True)
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
