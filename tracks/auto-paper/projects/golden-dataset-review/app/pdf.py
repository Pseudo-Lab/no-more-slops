"""Build a two-column A4 PDF of the mini review from manuscript/paper.md.

Converts the Markdown subset the manuscript uses (front matter, headings, paragraphs, lists,
tables, figures, bold, italic, inline code) to HTML with the standard library, then prints it
with headless Chromium. The front matter and both abstracts span the full width; the body and
references flow in two columns.

Front matter (between the first two `---` lines): `key: value` lines for title, title_en,
authors, affiliation, type, date. A line `<!-- wide -->` before a table or figure makes it
span both columns. With --float-wide, a script paginates the body in the browser and places
each wide block at the top or bottom of a page (page 1: bottom only) instead of mid-page.

Usage:
    uv run pdf.py [--src ../manuscript/paper.md] [--out ../outputs/week-03/paper-extended.pdf] [--float-wide]
"""
import argparse
import html
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BROWSERS = ("chromium", "chromium-browser", "google-chrome", "google-chrome-stable")

FONTS = {  # family -> candidate font files (Noto fonts are SIL OFL; copied locally, not committed)
    "Noto Serif KR": [Path("/mnt/c/Windows/Fonts/NotoSerifKR-VF.ttf"), Path.home() / ".local/share/fonts/NotoSerifKR.ttf"],
    "Noto Sans KR": [Path.home() / ".local/share/fonts/NotoSansKR.ttf", Path("/mnt/c/Windows/Fonts/NotoSansKR-VF.ttf")],
}

CSS = """
@page { size: A4; margin: 13mm 14mm 12mm 14mm;
        @bottom-center { content: counter(page); font-size: 8pt; color: #555; } }
html { -webkit-print-color-adjust: exact; }
body { font-family: 'Paper Serif', 'Noto Serif KR', serif; font-size: 8.5pt;
       line-height: 1.42; color: #111; word-break: normal; line-break: strict; hyphens: manual;
       overflow-wrap: break-word; margin: 0; }
.front { border-bottom: 0.6pt solid #333; padding-bottom: 6pt; margin-bottom: 8pt; }
.type { font-family: 'Paper Sans', 'Noto Sans KR', sans-serif; font-size: 7.5pt; letter-spacing: 0.08em;
        text-transform: uppercase; color: #555; margin: 0 0 4pt; }
h1.title { font-family: 'Paper Sans', 'Noto Sans KR', sans-serif; font-size: 15pt; line-height: 1.3;
           margin: 0 0 3pt; font-weight: 700; }
p.title-en { font-family: 'Paper Sans', 'Noto Sans KR', sans-serif; font-size: 10pt; margin: 0 0 6pt; color: #333; }
p.authors { font-family: 'Paper Sans', 'Noto Sans KR', sans-serif; font-size: 9pt; margin: 0; }
p.affil { font-size: 7.8pt; color: #444; margin: 1pt 0 0; }
.abstract { margin: 5pt 0 0; font-size: 8.1pt; line-height: 1.4; }
.abstract h2 { font-size: 9pt; margin: 0 0 2pt; }
.abstract p { margin: 0 0 3pt; }
.body { column-count: 2; column-gap: 7mm; column-fill: auto; }
h2, h3 { font-family: 'Paper Sans', 'Noto Sans KR', sans-serif; line-height: 1.35; break-after: avoid; }
h2 { font-size: 10pt; margin: 8pt 0 3pt; }
h3 { font-size: 9pt; margin: 6pt 0 2pt; }
p { margin: 0 0 4pt; text-align: justify; text-indent: 0; }
code { font-family: 'Noto Sans Mono', monospace; font-size: 8pt; }
ul, ol { margin: 0 0 4pt; padding-left: 13pt; }
li { margin-bottom: 1.5pt; }
table { border-collapse: collapse; margin: 3pt 0 6pt; font-size: 6.9pt; line-height: 1.32;
        width: 100%; break-inside: avoid; }
thead th { border-top: 0.8pt solid #222; border-bottom: 0.5pt solid #222; }
tbody tr:last-child td { border-bottom: 0.8pt solid #222; }
th, td { padding: 2pt 3pt; vertical-align: top; text-align: left; word-break: keep-all; }
sub, sup { line-height: 0; font-size: 72%; }
p.left { text-align: left; }
p.eq { text-align: center; margin: 3pt 0 5pt; }
th { font-family: 'Paper Sans', 'Noto Sans KR', sans-serif; font-weight: 700; }
.wide { column-span: all; margin: 4pt 0 6pt; }
p.caption { font-family: 'Paper Sans', 'Noto Sans KR', sans-serif; font-size: 7.8pt; line-height: 1.35;
            margin: 4pt 0 2pt; text-align: left; break-after: avoid; }
figure { margin: 3pt 0 6pt; break-inside: avoid; }
figure img { width: 100%; }
.refs { font-size: 6.4pt; line-height: 1.2; padding-left: 15pt; overflow-wrap: anywhere; }
.refs li { break-inside: avoid; margin-bottom: 0.6pt; text-align: left; }
.note { font-size: 7.6pt; color: #333; }
"""


COLS = {4: (11, 15, 32, 42), 5: (10, 20, 27, 28, 15)}  # column widths (%) of the two manuscript tables


PAGED_CSS = """
.page { width: 182mm; height: 271.8mm; overflow: hidden; break-after: page; }
.page:last-child { break-after: auto; }
.page .body { column-fill: auto; }
.page.last .body { column-fill: balance; }
.slot-top, .slot-bottom { display: flow-root; }
.slot-top > .wide { margin: 0 0 6pt; }
.slot-bottom > .wide { margin: 6pt 0 0; }
.slot-top figure, .slot-bottom figure { margin: 0; }
p.split-head { margin-bottom: 0; }
p.split-head:not(.left) { text-align-last: justify; }
"""

# Page floats for wide blocks: Chromium has no `float: top/bottom`, so lay the body out page by
# page. Blocks fill a fixed-height two-column box; a wide block goes to the bottom of the page
# where it is anchored if the text placed so far still fits, otherwise to the top of the next
# page. Paragraphs split at spaces and lists split between items to fill each page.
PAGINATE = r"""
(async () => {
  await document.fonts.ready;
  const src = document.getElementById("src"), out = document.getElementById("pages");
  const front = src.querySelector(".front"), flow = [...src.querySelector(".body").children];
  const pages = [];
  const newPage = () => {
    const page = document.createElement("div");
    page.className = "page";
    if (!pages.length) page.append(front);
    page.top = page.appendChild(Object.assign(document.createElement("div"), {className: "slot-top"}));
    page.body = page.appendChild(Object.assign(document.createElement("div"), {className: "body"}));
    page.bottom = page.appendChild(Object.assign(document.createElement("div"), {className: "slot-bottom"}));
    out.append(page);
    pages.push(page);
    return page;
  };
  const fits = (page) => {
    const head = page.firstChild === front ? front.offsetHeight + parseFloat(getComputedStyle(front).marginBottom) : 0;
    const rest = page.clientHeight - head
      - page.top.offsetHeight - page.bottom.offsetHeight;
    page.body.style.height = rest + "px";
    return rest > 0 && page.body.scrollWidth <= page.body.clientWidth + 1;
  };
  const isWide = (el) => el.classList.contains("wide");
  const isHeading = (el) => /^H[23]$/.test(el.tagName);

  // Put the longest head of `el` that fits on `page`; return the remainder (or el if nothing fits).
  const split = (page, el) => {
    if (el.tagName === "P" && !el.classList.contains("eq")) {
      const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT), nodes = [], cuts = [];
      while (walker.nextNode()) nodes.push(walker.currentNode);
      nodes.forEach((n, i) => { for (const m of n.data.matchAll(/ +/g)) cuts.push([i, m.index + m[0].length]); });
      const cut = (k, keepHead) => {
        const copy = el.cloneNode(true), w = document.createTreeWalker(copy, NodeFilter.SHOW_TEXT), cn = [];
        while (w.nextNode()) cn.push(w.currentNode);
        const r = document.createRange();
        const [i, off] = cuts[k];
        if (keepHead) { r.setStart(cn[i], off); r.setEndAfter(copy.lastChild); }
        else { r.setStartBefore(copy.firstChild); r.setEnd(cn[i], off); }
        r.deleteContents();
        copy.classList.add(keepHead ? "split-head" : "split-tail");
        return copy;
      };
      let lo = -1, hi = cuts.length - 1;
      while (lo < hi) {
        const mid = Math.ceil((lo + hi + 1) / 2), head = cut(mid, true);
        page.body.append(head);
        const ok = fits(page);
        head.remove();
        if (ok) lo = mid; else hi = mid - 1;
      }
      if (lo < 0) return el;
      page.body.append(cut(lo, true));
      return cut(lo, false);
    }
    if (el.tagName === "OL" || el.tagName === "UL") {
      const head = el.cloneNode(false), items = [...el.children];
      page.body.append(head);
      let n = 0;
      for (const li of items) {
        head.append(li);
        if (!fits(page)) { li.remove(); break; }
        n++;
      }
      if (!n) { head.remove(); return el; }
      const tail = el.cloneNode(false);
      tail.append(...items.slice(n));
      if (el.tagName === "OL") tail.start = (el.start || 1) + n;
      return tail.children.length ? tail : null;
    }
    return el;
  };

  let page = newPage(), pending = [];
  const turn = () => {
    const carry = [];  // keep headings with the text that follows them
    while (page.body.lastElementChild && isHeading(page.body.lastElementChild)) carry.unshift(page.body.lastElementChild);
    page = newPage();
    page.top.append(...pending);
    pending = [];
    page.body.append(...carry);
  };
  const queue = flow.slice();
  while (queue.length) {
    const el = queue.shift();
    if (isWide(el)) {
      if (pages.length > 1 && !page.body.children.length && !page.top.children.length) { page.top.append(el); continue; }
      if (!page.bottom.children.length) {
        page.bottom.append(el);
        if (fits(page)) continue;
        el.remove();
      }
      pending.push(el);
      continue;
    }
    page.body.append(el);
    if (fits(page)) continue;
    el.remove();
    const rest = split(page, el);
    turn();
    if (rest) queue.unshift(rest);
  }
  if (pending.length) { turn(); }
  page.classList.add("last");
  fits(page);
  src.remove();
})();
"""


KEEP_ALL = "body { word-break: keep-all; overflow-wrap: anywhere; } .refs { word-break: normal; }"


def inline(text):
    out = html.escape(text, quote=False)
    out = re.sub(r"&lt;(/?)(sub|sup)&gt;", r"<\1\2>", out)  # allow sub/superscripts in formulas
    out = re.sub(r"`([^`]+)`", r"<code>\1</code>", out)
    out = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", out)
    return out


def table(rows, widths=None):
    cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
    head, body = cells[0], cells[2:]

    def row(tag, values):
        return "<tr>" + "".join(f"<{tag}>{inline(v)}</{tag}>" for v in values) + "</tr>"

    widths = widths or COLS.get(len(head))
    cols = "<colgroup>" + "".join(f'<col style="width:{w}%">' for w in widths) + "</colgroup>" if widths else ""
    return (f'<table style="table-layout:{"fixed" if widths else "auto"}">{cols}<thead>' + row("th", head) + "</thead><tbody>"
            + "".join(row("td", r) for r in body) + "</tbody></table>")


def convert(lines):
    out, i, wide, cols = [], 0, False, None
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line.strip() == "<!-- wide -->":
            wide = True
            i += 1
            continue
        if m := re.fullmatch(r"<!-- cols: ([\d, ]+) -->", line.strip()):
            cols = tuple(int(x) for x in m[1].split(","))
            i += 1
            continue
        if m := re.match(r"^(#{2,3})\s+(.*)$", line):
            level, text = len(m[1]), m[2]
            out.append(f"<h{level}>{inline(text)}</h{level}>")
            i += 1
            continue
        block = None
        if re.fullmatch(r"\*\*(표|그림) .+", line.strip()):
            # caption followed by a table or figure: keep them together
            caption = f'<p class="caption">{inline(line.strip())}</p>'
            i += 1
            while i < len(lines) and not lines[i].strip():
                i += 1
            inner = ""
            if i < len(lines) and lines[i].startswith("|"):
                rows = []
                while i < len(lines) and lines[i].startswith("|"):
                    rows.append(lines[i])
                    i += 1
                inner = table(rows, cols)
                cols = None
            elif i < len(lines) and (m := re.match(r"^!\[[^\]]*\]\(([^)]+)\)", lines[i])):
                inner = f'<img src="{html.escape(m[1])}" alt="">'
                i += 1
            note = ""
            if i < len(lines) and lines[i].startswith("주: "):
                note = f'<p class="note">{inline(lines[i])}</p>'
                i += 1
            block = f"<figure>{caption}{inner}{note}</figure>"
        elif line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append(lines[i])
                i += 1
            block = table(rows)
        elif re.match(r"^\s*[-*] ", line):
            items = []
            while i < len(lines) and re.match(r"^\s*[-*] ", lines[i]):
                items.append(re.sub(r"^\s*[-*] ", "", lines[i]))
                i += 1
            block = "<ul>" + "".join(f"<li>{inline(t)}</li>" for t in items) + "</ul>"
        elif re.match(r"^\[?\d+\]?\.? ", line) and out and out[-1].startswith("<h2>참고문헌"):
            items = []
            while i < len(lines) and re.match(r"^\[?\d+\]?\.? ", lines[i]):
                items.append(re.sub(r"^\[?\d+\]?\.? ", "", lines[i]))
                i += 1
            block = '<ol class="refs">' + "".join(f"<li>{inline(t)}</li>" for t in items) + "</ol>"
        elif re.match(r"^\d+\. ", line):
            items = []
            while i < len(lines) and re.match(r"^\d+\. ", lines[i]):
                items.append(re.sub(r"^\d+\. ", "", lines[i]))
                i += 1
            block = "<ol>" + "".join(f"<li>{inline(t)}</li>" for t in items) + "</ol>"
        elif line.startswith("=: "):  # display formula
            block = f'<p class="eq">{inline(line[3:].strip())}</p>'
            i += 1
        else:
            cls = ' class="left"' if re.search(r"(?:github|https?)\S*\.\w", line) else ""  # long URLs widen justified gaps
            block = f"<p{cls}>{inline(line.strip())}</p>"
            i += 1
        if wide:
            block = f'<div class="wide">{block}</div>'
            wide = False
        out.append(block)
    return "\n".join(out)


def split(md):
    """Return (meta dict, abstract lines, body lines)."""
    lines = md.splitlines()
    meta = {}
    if lines and lines[0].strip() == "---":
        end = lines.index("---", 1)
        for line in lines[1:end]:
            key, _, value = line.partition(":")
            meta[key.strip()] = value.strip()
        lines = lines[end + 1:]
    # abstracts run until the first numbered section heading
    first = next(i for i, l in enumerate(lines) if re.match(r"^## \d", l))
    return meta, lines[:first], lines[first:]


def front(meta, abstract_lines):
    parts = ['<div class="front">']
    if meta.get("type"):
        parts.append(f'<p class="type">{inline(meta["type"])}</p>')
    parts.append(f'<h1 class="title">{inline(meta.get("title", ""))}</h1>')
    if meta.get("title_en"):
        parts.append(f'<p class="title-en">{inline(meta["title_en"])}</p>')
    if meta.get("authors"):
        parts.append(f'<p class="authors">{inline(meta["authors"])}</p>')
    if meta.get("affiliation"):
        parts.append(f'<p class="affil">{inline(meta["affiliation"])}</p>')
    parts.append(f'<div class="abstract">{convert(abstract_lines)}</div></div>')
    return "".join(parts)


def font_faces(out_dir):
    """Copy available Korean fonts next to the HTML and declare them, so Latin and Hangul share one family."""
    faces = []
    for alias, family in (("Paper Serif", "Noto Serif KR"), ("Paper Sans", "Noto Sans KR")):
        src = next((f for f in FONTS[family] if f.exists()), None)
        if src is None:
            continue
        dst = out_dir / ".fonts" / src.name
        if not dst.exists():
            dst.parent.mkdir(exist_ok=True)
            shutil.copyfile(src, dst)
        faces.append(f"@font-face {{ font-family: '{alias}'; src: url('.fonts/{src.name}'); font-weight: 100 900; }}")
    return "\n".join(faces)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--src", type=Path, default=ROOT / "manuscript" / "paper.md")
    parser.add_argument("--out", type=Path, default=ROOT / "outputs" / "week-03" / "paper-extended.pdf")
    parser.add_argument("--keep-all", action="store_true", help="break Korean text only between words (eojeol)")
    parser.add_argument("--float-wide", action="store_true", help="place wide tables and figures at page top or bottom")
    args = parser.parse_args()

    meta, abstract_lines, body_lines = split(args.src.read_text(encoding="utf-8"))
    content = f'{front(meta, abstract_lines)}<div class="body">{convert(body_lines)}</div>'
    if args.float_wide:
        content = f'<div id="src">{content}</div><div id="pages"></div><script>{PAGINATE}</script>'
    page = (f'<!doctype html><html lang="ko"><head><meta charset="utf-8">'
            f'<title>{html.escape(meta.get("title", "paper"))}</title><style>{font_faces(args.src.parent)}{CSS}'
            f'{KEEP_ALL if args.keep_all else ""}{PAGED_CSS if args.float_wide else ""}</style></head>'
            f'<body>{content}</body></html>')
    page_path = args.src.with_suffix(".html")
    page_path.write_text(page, encoding="utf-8")

    browser = next((b for b in BROWSERS if shutil.which(b)), None)
    if not browser:
        raise SystemExit(f"no Chromium found; open {page_path} and print to PDF")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([browser, "--headless", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=20000",
                    f"--print-to-pdf={args.out.resolve()}", page_path.resolve().as_uri()],
                   check=True, capture_output=True)
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
