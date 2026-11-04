"""시험 공통 도구: 스크립트 경로, 합성 이미지·영상·소리 만들기."""
import os
import subprocess
import sys

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(SKILL, "scripts")
ASSETS = os.path.join(SKILL, "assets")
sys.path.insert(0, SCRIPTS)

from pngio import Canvas  # noqa: E402,F401


def run_py(script, *args, check=True):
    """scripts/<script>를 시스템 파이썬으로 돌린다. (종료 코드, 표준 출력+오류)."""
    r = subprocess.run([sys.executable, os.path.join(SCRIPTS, script), *map(str, args)], capture_output=True, text=True)
    if check and r.returncode:
        raise AssertionError(f"{script} {' '.join(map(str, args))} 실패 ({r.returncode})\n{r.stdout}\n{r.stderr}")
    return r.returncode, r.stdout + r.stderr


def ff(*args):
    subprocess.run(["ffmpeg", "-y", "-v", "error", *map(str, args)], check=True)


def solid_png(path, w, h, color):
    Canvas(w, h, color).save(path)


def color_clip(path, w, h, seconds, color="0x8090a0", tone=None):
    """단색 영상 (선택: 사인파 소리)."""
    a = ["-f", "lavfi", "-i", f"color=c={color}:s={w}x{h}:r=30:d={seconds}"]
    if tone:
        a += ["-f", "lavfi", "-i", f"sine=frequency={tone}:sample_rate=48000:duration={seconds}"]
    ff(*a, "-c:v", "libx264", "-pix_fmt", "yuv420p", *(["-c:a", "aac", "-shortest"] if tone else []), path)


def probe(path, entries="format=duration"):
    return subprocess.run(["ffprobe", "-v", "error", "-show_entries", entries, "-of", "csv=p=0", path],
                          capture_output=True, text=True).stdout.strip()
