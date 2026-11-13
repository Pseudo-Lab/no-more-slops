#!/usr/bin/env bash
# Build outputs/week-04/paper.pdf from paper.tex with the official ACL style (XeLaTeX via Tectonic).
#
# The ACL style files carry no license that allows redistribution and must not be modified, so they
# are downloaded here from a pinned commit of acl-org/acl-style-files instead of being committed.
# Noto Serif KR (SIL OFL) is downloaded the same way. Both go to outputs/week-04/.build/ (git-ignored).
#
# Figures (figures.py) and table bodies (tables.py) are regenerated from results/ first; pass
# --no-figures to only recompile the TeX.
# Requirements: tectonic (brew install tectonic), uv, curl. Usage: app/build_paper.sh [--no-figures]
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
OUT="$HERE/../outputs/week-04"
BUILD="$OUT/.build"
ACL_SHA=d5adc823ff0f80f98c80405ca0ab66c68e684409   # acl-org/acl-style-files, master on 2026-11-13
NOTO_SHA=f8d157532fbfaeda587e826d4cd5b21a49186f7c  # notofonts/noto-cjk, main on 2026-11-13

fetch() {  # url dest
  [ -s "$2" ] || curl -sSfL --retry 3 -o "$2" "$1"
}

mkdir -p "$BUILD/fonts"
for f in acl.sty acl_natbib.bst; do
  fetch "https://raw.githubusercontent.com/acl-org/acl-style-files/$ACL_SHA/$f" "$BUILD/$f"
done
for w in Regular Bold; do
  fetch "https://raw.githubusercontent.com/notofonts/noto-cjk/$NOTO_SHA/Serif/SubsetOTF/KR/NotoSerifKR-$w.otf" \
    "$BUILD/fonts/NotoSerifKR-$w.otf"
done

if [ "${1:-}" != "--no-figures" ]; then
  (cd "$HERE" && FONT_DIR="$BUILD/fonts" uv run python figures.py && uv run python tables.py)
fi

cd "$OUT"
tectonic -X compile paper.tex -Z search-path="$BUILD" --keep-logs
rm -f paper.log
echo "wrote $OUT/paper.pdf"
