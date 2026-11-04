#!/bin/sh
# 선택 시험: 아주 작은 Blender 렌더 한 장 (270×480, 4샘플, 1프레임, nice 19) → 255 픽셀 QC.
# 건너뛰는 경우: Blender가 없을 때, 다른 Blender 프로세스가 돌고 있을 때 (GPU를 나눠 쓰면 다른 사람 렌더가 느려지고 오류가 난 적이 있다).
# 사용법: sh tests/blender_smoke.sh    (BLENDER=<실행 파일>로 경로 지정)
set -e
HERE=$(cd "$(dirname "$0")/.." && pwd)
B=${BLENDER:-$(command -v blender || true)}
[ -z "$B" ] && [ -x /Applications/Blender.app/Contents/MacOS/Blender ] && B=/Applications/Blender.app/Contents/MacOS/Blender
if [ -z "$B" ]; then echo "SKIP: Blender 없음"; exit 0; fi
if pgrep -ix blender >/dev/null 2>&1; then
  echo "SKIP: 다른 Blender 프로세스가 돌고 있다 (한 번에 하나만):"; pgrep -ixl blender; exit 0
fi
T=$(mktemp -d)
cat > "$T/smoke.json" <<JSON
{"fps": 30, "size": [1080, 1920], "product": "$HERE/assets/test-bottle.json",
 "cuts": [{"id": "smoke", "duration": 0.1, "blender": {"frames": 3,
   "camera": [{"f": 0, "target": [0, 0, 1.4], "yaw": 0, "pitch": 6, "dist": 11, "fov": 26}],
   "bottle": [{"f": 0, "yaw": 0}], "closure": [{"f": 0, "lift": 0.8}]}}]}
JSON
nice -n 19 "$B" -b --factory-startup -P "$HERE/scripts/render_cut.py" -- --config "$T/smoke.json" --cut smoke --out "$T/frames" \
  --samples 4 --size 270x480 --frames 0 2>&1 | grep -E "FRAME|RENDER_DONE|Error|error" || true
[ -f "$T/frames/f0000.png" ] || { echo "FAIL: 프레임이 없다"; exit 1; }
python3 "$HERE/scripts/qc.py" white "$T/frames/f0000.png"
grep -q '"preview": true' "$T/frames/render.json" && echo "OK: 작은 렌더는 미리보기로 표시됨"
echo "결과: $T/frames/f0000.png"
