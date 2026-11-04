"""슬라이드 HTML을 인스타 캐러셀 PNG(1080x1350)로 뽑는다.

python3 scripts/render.py design/file-01.html outputs/week-01/file-01
"""
import pathlib
import sys

from playwright.sync_api import sync_playwright


def main(html, out_dir):
    out = pathlib.Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1200, "height": 1500})
        pg.goto(pathlib.Path(html).resolve().as_uri(), wait_until="networkidle")
        pg.add_style_tag(content=".grid{grid-template-columns:1080px!important}.cell small{display:none}")
        pg.evaluate("document.fonts.ready")
        # 슬라이드 안 글이 아래로 넘친 px (0이면 정상)
        # 슬라이드(.s)마다 하나씩. .in이 없는 장(표지 증거 보드 등)은 0으로 쳐서 장 번호가 밀리지 않게 한다
        spill = pg.evaluate("[...document.querySelectorAll('.s')].map(s => { const e = s.querySelector('.in'); return e ? e.scrollHeight - e.clientHeight : 0 })")
        for i, el in enumerate(pg.query_selector_all(".s"), 1):
            box = el.bounding_box()
            clip = {"x": box["x"], "y": box["y"], "width": 1080, "height": 1350}
            pg.screenshot(path=str(out / f"{i:02d}.png"), clip=clip, full_page=True)
            print("ok", out / f"{i:02d}.png")
        b.close()
    bad = [(i, px) for i, px in enumerate(spill, 1) if px > 0]
    for i, px in bad:
        print(f"WARN {i:02d}장 글이 {px}px 넘쳐서 아래가 잘림. 문구를 줄이세요.")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main(*sys.argv[1:3])
