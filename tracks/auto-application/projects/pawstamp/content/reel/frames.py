# usage: python3 frames.py <outdir> <bg hex> <slide.png:seconds> ...
# 4:5 슬라이드를 9:16 캔버스(위쪽 여백 작게, 아래는 릴스 캡션 자리)에 얹고, 장 사이를 0.4초 크로스페이드
import sys, os
from PIL import Image

out, bg = sys.argv[1], sys.argv[2]
items = [(a.rsplit(':', 1)[0], float(a.rsplit(':', 1)[1])) for a in sys.argv[3:]]
os.makedirs(out, exist_ok=True)
FPS, FADE = 30, 12
TOP = 170

def canvas(p):
    c = Image.new('RGB', (1080, 1920), bg)
    c.paste(Image.open(p).convert('RGB').resize((1080, 1350)), (0, TOP))
    return c

frames = [canvas(p) for p, _ in items]
manifest = []
for i, (im, (_, sec)) in enumerate(zip(frames, items)):
    f = f'{out}/s{i}.png'; im.save(f)
    manifest.append(f'{f}\t{int(sec * FPS)}')
    if i + 1 < len(frames):
        for k in range(1, FADE):
            t = f'{out}/s{i}_{k}.png'
            Image.blend(im, frames[i + 1], k / FADE).save(t)
            manifest.append(f'{t}\t1')
open(f'{out}/manifest.txt', 'w').write('\n'.join(manifest))
print(len(manifest))
