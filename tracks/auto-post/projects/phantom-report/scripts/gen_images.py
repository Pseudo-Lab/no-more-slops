"""슬라이드 이미지 생성. Codex CLI의 이미지 생성(ChatGPT 계정 로그인)을 쓴다.

python3 scripts/gen_images.py issues/file-01.prompts.json design/img/file-01
이미 있는 파일은 건너뛴다. 다시 만들려면 해당 png를 지우고 돌린다.
로그인이 풀렸으면: codex logout && codex login --device-auth
"""
import json
import pathlib
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

STYLE = (
    "Grainy black-and-white evidence photograph from a classified police case file, "
    "high contrast film noir lighting, subtle deep red accent, documentary realism. "
    "No text, no letters, no logos, no brand names. "
    "No identifiable real people: faces out of frame, in shadow or from behind. Scene: "
)

ROOT = pathlib.Path(__file__).resolve().parent.parent


def gen(path, prompt):
    rel = path.resolve().relative_to(ROOT)
    task = (
        "Use your image generation tool to create ONE landscape (1536x1024) image from the prompt below, "
        f"then save it as {rel} in the current directory. Do not write any other files. "
        f"Reply with the saved path only.\n\nPROMPT: {STYLE}{prompt}"
    )
    r = subprocess.run(
        # effort를 low로 고정: 기본값(xhigh)이면 한 장이 600초를 넘겨 타임아웃된다
        ["codex", "exec", "-c", "model_reasoning_effort=low", "-s", "workspace-write", "--skip-git-repo-check", task],
        cwd=ROOT, capture_output=True, text=True, timeout=600,
    )
    print("ok" if path.exists() else f"fail ({r.stderr.strip()[-300:]})", path)


def main(prompts_path, out_dir):
    prompts = json.loads(pathlib.Path(prompts_path).read_text())
    out = pathlib.Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    todo = [(out / f"{n}.png", p) for n, p in prompts.items() if not (out / f"{n}.png").exists()]
    with ThreadPoolExecutor(4) as ex:  # ponytail: 동시 4개, 사용량 제한 걸리면 줄인다
        list(ex.map(lambda a: gen(*a), todo))


if __name__ == "__main__":
    main(*sys.argv[1:3])
