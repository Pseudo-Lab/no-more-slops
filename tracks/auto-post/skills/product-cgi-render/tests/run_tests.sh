#!/bin/sh
# 전체 시험: 단위 시험(Blender 없이) + 선택 시험(오버레이: Chrome·puppeteer-core 있을 때, Blender: 따로 BLENDER_SMOKE=1)
# 사용법: sh tests/run_tests.sh
set -e
HERE=$(cd "$(dirname "$0")/.." && pwd)
cd "$HERE/tests"
python3 -m unittest -v test_config test_qc test_compose test_assemble test_audio test_hygiene test_overlay
if [ "${BLENDER_SMOKE:-0}" = "1" ]; then sh "$HERE/tests/blender_smoke.sh"; else echo "Blender 시험 건너뜀 (BLENDER_SMOKE=1 sh tests/run_tests.sh)"; fi
