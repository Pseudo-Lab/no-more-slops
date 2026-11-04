#!/usr/bin/env python3
"""List, check, read and replace generated blocks between AUTO markers. Standard library only.

A generated block sits between a pair of markers, in LaTeX or Markdown/HTML form:

    % BEGIN AUTO RESULTS            <!-- BEGIN AUTO RESULTS -->
    ...generated...                 ...generated...
    % END AUTO RESULTS              <!-- END AUTO RESULTS -->

Every name appears exactly once, blocks do not nest, and only the text between the
markers is ever replaced. `replace` writes the file only when every check passes; `check`
compares a block with freshly generated content and exits 1 when they differ.

Exit status: 0 ok, 1 `check` found a difference, 2 malformed markers or unreadable files.
"""

import argparse
import difflib
import re
import sys
from pathlib import Path

MARKER = re.compile(r"^[ \t]*(?:%|<!--)[ \t]*(BEGIN|END) AUTO ([A-Za-z0-9_.-]+)[ \t]*(?:-->)?[ \t]*$", re.M)


def blocks(text):
    """{name: (start of content, end of content, begin line, end line)}; raises on malformed markers."""
    found, open_name, open_at, open_line = {}, None, None, None
    for match in MARKER.finditer(text):
        kind, name = match.group(1), match.group(2)
        line = text.count("\n", 0, match.start()) + 1
        if kind == "BEGIN":
            if open_name is not None:
                raise ValueError(f"line {line}: BEGIN AUTO {name} inside open block {open_name}")
            if name in found:
                raise ValueError(f"line {line}: block {name} appears twice")
            open_name, open_at, open_line = name, match.end(), line
        else:
            if open_name != name:
                raise ValueError(f"line {line}: END AUTO {name} without a matching BEGIN")
            content_end = match.start()
            content_start = open_at + 1 if text[open_at:open_at + 1] == "\n" else open_at
            found[name] = (content_start, max(content_start, content_end), open_line, line)
            open_name = None
    if open_name is not None:
        raise ValueError(f"line {open_line}: BEGIN AUTO {open_name} is never closed")
    return found


def replace(text, name, content):
    found = blocks(text)
    if name not in found:
        raise ValueError(f"no AUTO block named {name}")
    start, end, _, _ = found[name]
    if content and not content.endswith("\n"):
        content += "\n"
    return text[:start] + content + text[end:]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("list", help="names and line ranges of the blocks (also checks them)")
    p.add_argument("file")
    p = sub.add_parser("show", help="print one block's content")
    p.add_argument("file")
    p.add_argument("name")
    p = sub.add_parser("replace", help="replace one block's content with a file's (or stdin's)")
    p.add_argument("file")
    p.add_argument("name")
    p.add_argument("--from", dest="source", help="file with the new content; default stdin")
    p.add_argument("--require", nargs="*", default=[], help="names that must exist in the file")
    p = sub.add_parser("check", help="exit 1 and print a diff when a block differs from a file's content")
    p.add_argument("file")
    p.add_argument("name")
    p.add_argument("--from", dest="source", required=True, help="file with the expected content")
    args = parser.parse_args(argv)
    path = Path(args.file)
    text = path.read_text(encoding="utf-8")
    found = blocks(text)
    if args.command == "list":
        for name, (_, _, begin, end) in found.items():
            print(f"{name}\tlines {begin}-{end}")
        return 0
    if args.command in ("show", "check") and args.name not in found:
        raise ValueError(f"no AUTO block named {args.name}")
    if args.command == "show":
        start, end, _, _ = found[args.name]
        sys.stdout.write(text[start:end])
        return 0
    if args.command == "check":
        start, end, _, _ = found[args.name]
        expected = Path(args.source).read_text(encoding="utf-8")
        if expected and not expected.endswith("\n"):
            expected += "\n"
        if text[start:end] == expected:
            print(f"{args.name}: in sync", file=sys.stderr)
            return 0
        sys.stdout.writelines(difflib.unified_diff(text[start:end].splitlines(True), expected.splitlines(True),
                                                   f"{args.file} [{args.name}]", args.source))
        return 1
    missing = [name for name in args.require if name not in found]
    if missing:
        raise ValueError(f"missing AUTO blocks: {', '.join(missing)}")
    content = Path(args.source).read_text(encoding="utf-8") if args.source else sys.stdin.read()
    if MARKER.search(content):
        raise ValueError("the new content contains AUTO markers")
    new = replace(text, args.name, content)
    blocks(new)  # still well formed
    if new != text:
        path.write_text(new, encoding="utf-8")
    print(f"{args.name}: {'replaced' if new != text else 'unchanged'}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(2)
