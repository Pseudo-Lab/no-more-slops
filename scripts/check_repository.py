#!/usr/bin/env python3
"""Check contribution paths and unique skill IDs without third-party packages."""

import argparse
from collections import defaultdict
from pathlib import Path, PurePosixPath
import re
import subprocess

TRACKS = {"auto-paper", "auto-application", "auto-post"}
SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
WEEK = re.compile(r"week-(?:0[1-9]|[1-9][0-9])\Z")
LEGACY_ROOTS = {"auto-paper", "auto-application", "auto-post", "skills", "artifacts", "research", "examples"}
ROOT_DIRS = {".github", "docs", "scripts", "tracks"}
RESULT_SUFFIXES = {".pdf", ".ppt", ".pptx", ".docx", ".mp4", ".mov"}
SOURCE_ASSET_DIRS = {"assets", "fixtures", "testdata", "templates"}


def inspect(root, files):
    errors, catalog = [], []
    names = defaultdict(list)
    projects, weeks = set(), set()
    files = set(files)
    for filename in sorted(files):
        path = PurePosixPath(filename)
        parts = path.parts
        if not parts:
            continue
        if parts[0].lower() in LEGACY_ROOTS:
            errors.append(f"{filename}: move contributions under tracks/<track>/skills or projects")
        elif len(parts) > 1 and parts[0] not in ROOT_DIRS:
            errors.append(f"{filename}: project directories belong under tracks/<track>/projects")
        if path.name == "SKILL.md":
            canonical = (len(parts) == 5 and parts[0] == "tracks" and
                         parts[1] in TRACKS and parts[2] == "skills" and SLUG.fullmatch(parts[3]))
            if not canonical:
                errors.append(f"{filename}: SKILL.md must use tracks/<track>/skills/<name>/SKILL.md")
            local = root / filename
            if local.is_symlink():
                errors.append(f"{filename}: commit one canonical skill, not a symlink copy")
                continue
            if not local.is_file():
                errors.append(f"{filename}: tracked skill is missing; stage its deletion or restore it")
                continue
            text = local.read_text(encoding="utf-8-sig")
            header = re.match(r"\A---\s*\n(.*?)\n---(?:\s*\n|\Z)", text, re.S)
            name = re.search(r"^name:\s*([^\n]+)$", header[1], re.M) if header else None
            if not name:
                errors.append(f"{filename}: missing frontmatter name")
                continue
            name = name[1].strip().strip("\"'")
            names[name].append(filename)
            if not SLUG.fullmatch(name) or name != path.parent.name:
                errors.append(f"{filename}: frontmatter name {name!r} must match its kebab-case folder")
            if not re.search(r"^description:\s*\S", header[1], re.M):
                errors.append(f"{filename}: missing frontmatter description")
            catalog.append((name, filename))
        if parts[0] != "tracks":
            if path.suffix.lower() in RESULT_SUFFIXES:
                errors.append(f"{filename}: final documents/media belong in project outputs/week-NN")
            continue
        if len(parts) < 3 or parts[1] not in TRACKS:
            errors.append(f"{filename}: unknown track")
            continue
        if parts[2] == "README.md" and len(parts) == 3:
            continue
        if parts[2] not in {"skills", "projects"} or len(parts) < 5:
            errors.append(f"{filename}: expected skills/<name> or projects/<name>")
            continue
        if not SLUG.fullmatch(parts[3]):
            errors.append(f"{filename}: folder name must use lowercase kebab-case")
        if parts[2] == "skills":
            skill = "/".join(parts[:4]) + "/SKILL.md"
            if skill not in files:
                errors.append(f"{filename}: skill folder has no SKILL.md")
        else:
            project = "/".join(parts[:4])
            projects.add(project)
            if parts[4] == "outputs":
                if len(parts) < 7 or not WEEK.fullmatch(parts[5]):
                    errors.append(f"{filename}: use outputs/week-NN/<file> (NN starts at 01)")
                else:
                    weeks.add("/".join(parts[:6]))
            elif path.suffix.lower() in RESULT_SUFFIXES and not SOURCE_ASSET_DIRS.intersection(parts[4:-1]):
                errors.append(f"{filename}: final documents/media belong in outputs/week-NN")
    for name, paths in names.items():
        if len(paths) > 1:
            errors.append(f"duplicate skill name {name!r}: {', '.join(paths)}")
    for directory in sorted(projects | weeks):
        if directory + "/README.md" not in files:
            errors.append(f"{directory}: missing README.md index")
    return errors, catalog


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--catalog", action="store_true", help="print skills in this checkout")
    args = parser.parse_args()
    result = subprocess.run(["git", "-C", str(args.root), "ls-files", "-z", "--cached", "--others", "--exclude-standard"],
                            check=True, capture_output=True)
    files = result.stdout.decode().rstrip("\0").split("\0") if result.stdout else []
    errors, catalog = inspect(args.root, files)
    if args.catalog:
        print("| Skill | Path |\n| --- | --- |")
        for name, path in catalog:
            print(f"| {name} | {path} |")
    for error in errors:
        print(f"ERROR: {error}")
    print(f"Checked {len(set(files))} files and {len(catalog)} skills: {len(errors)} error(s)")
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
