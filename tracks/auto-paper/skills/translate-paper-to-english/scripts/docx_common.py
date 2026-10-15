"""Shared helpers for reading and rewriting the text parts of a .docx (stdlib only)."""
import re
import zipfile
from xml.sax.saxutils import unescape

# Innermost paragraphs only: a paragraph that hosts a text box is not matched as a
# whole, but the paragraphs inside the text box are. Both scripts use this same
# pattern, so the paragraph indices they produce always agree.
PARA_RE = re.compile(r'<w:p(?: [^>]*)?>(?:(?!<w:p[ >]).)*?</w:p>', re.S)
T_RE = re.compile(r'<w:t(?: [^>]*[^/>])?>(.*?)</w:t>', re.S)
MATH_T_RE = re.compile(r'<m:t(?: [^>]*[^/>])?>(.*?)</m:t>', re.S)
LINK_RE = re.compile(r'<w:hyperlink[ >].*?</w:hyperlink>', re.S)
HANGUL_RE = re.compile(r'[ᄀ-ᇿ㄰-㆏가-힣]+')
PART_RE = re.compile(r'^word/(document|header\d*|footer\d*|footnotes|endnotes|comments)\.xml$')
IGNORED_RPR = {'rFonts', 'lang', 'noProof', 'szCs', 'bCs', 'iCs', 'kern', 'rStyle'}


def text_parts(zf):
    """Names of the XML parts that carry translatable text, document.xml first."""
    names = [n for n in zf.namelist() if PART_RE.match(n)]
    return sorted(names, key=lambda n: (n != 'word/document.xml', n))


def part_label(name):
    return name[len('word/'):-len('.xml')]


def plain(xml_text):
    return unescape(xml_text, {'&quot;': '"', '&apos;': "'"})


def run_format(par, pos):
    """Human-readable formatting of the run that contains the <w:t> at pos."""
    start = max(par.rfind('<w:r>', 0, pos), par.rfind('<w:r ', 0, pos))
    if start < 0:
        return ''
    rpr = re.search(r'<w:rPr>(.*?)</w:rPr>', par[start:pos], re.S)
    if not rpr:
        return ''
    out = []
    for tag, val in re.findall(r'<w:(\w+)(?: w:val="([^"]*)")?', rpr.group(1)):
        if tag not in IGNORED_RPR:
            out.append(f'{tag}={val}' if val else tag)
    return ','.join(out)


def text_runs(par):
    """Every <w:t> of a paragraph: (match, text, format, inside_hyperlink)."""
    links = [m.span() for m in LINK_RE.finditer(par)]
    runs = []
    for m in T_RE.finditer(par):
        in_link = any(a <= m.start() < b for a, b in links)
        runs.append((m, plain(m.group(1)), run_format(par, m.start()), in_link))
    return runs


def table_spans(xml):
    spans, depth, start = [], 0, 0
    for m in re.finditer(r'<w:tbl>|</w:tbl>', xml):
        if m.group(0) == '<w:tbl>':
            if depth == 0:
                start = m.start()
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                spans.append((start, m.end()))
    return spans


def read_docx(path):
    with zipfile.ZipFile(path) as zf:
        return {n: zf.read(n).decode('utf8') for n in text_parts(zf)}
