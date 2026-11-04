"""설정(JSON) 읽기와 bpy 없이 계산할 수 있는 도구: 기본 룩, 회전체 단면 계산, 키프레임 보간, 프레임 범위.

scene.py·render_cut.py(Blender 안)와 assemble.py·audio.py·qc.py(시스템 파이썬)가 함께 쓴다.
그래서 이 파일은 표준 라이브러리만 쓴다.
"""
import copy
import json
import math
import os

# ───────────────────────── 기본 룩 (제품과 무관한 연한 스튜디오) ─────────────────────────
# 값은 설정 파일의 "look"으로 덮어쓴다. 모든 컷이 같은 look을 써야 한 세계로 보인다.
DEFAULT_LOOK = {
    "studio": {
        "base": [0.86, 0.93, 1.0],        # 벽 아래(지평선 쪽) 색
        "sky": [0.70, 0.84, 0.98],        # 벽 위 색
        "wall_glow": 0.88,                # 벽 발광 세기 (화면 밝기 ≈ 색 × 세기)
        "floor_white": 0.70,              # 앞쪽 바닥 확산 반사율 (그림자를 받는다)
        "floor_tint": [0.90, 0.95, 1.0],  # 바닥 색 기울기
        "softbox": {"location": [2.5, -9.5, -6.5], "scale": [5.0, 5.0, 4.0], "add": 0.16},  # 벽 위 흐린 소프트박스 하나
        "loop_mul": [1.0, 1.0, 1.0],      # 루프 이음매용 배경 곱 (bg_tint 키 0→1)
        "loop_floor_mul": [1.0, 1.0, 1.0],
    },
    "world": {"cam_color": [0.86, 0.93, 1.0], "cam_strength": 1.0, "light_color": [0.88, 0.94, 1.0], "light_strength": 0.35},
    "liquid": {"rgb": [0.88, 0.955, 1.0], "ior": 1.34, "shadow_rgb": [0.80, 0.91, 1.0]},  # 경계면마다 곱해진다 (병 한 번 통과 ≈ rgb²)
    "glass": {"ior": 1.5, "shadow_amount": 0.55},
    "lights": {
        "rim": {"energy": [230, 200], "size": [0.3, 5.0], "x": 2.6, "y": 3.0, "z": 2.2, "color_l": [0.85, 0.93, 1.0]},
        "front": {"energy": 140, "location": [-3.2, -6.0, 9.0], "size": 4.0},
        "sun": {"energy": 3.2, "angle_deg": 4.0, "rotation_deg": [40, 0, 200]},  # 뒤에서 오는 해: 접지 그림자 + 투과 그림자
        "flags": {"gray": 0.18, "x": 2.1, "y": 0.6, "size": [1.6, 5.0]},          # 좌우 회색 판: 유리 가장자리 진한 선
        "back_flags": {"gray": 0.20, "x": 2.6},
        "edges": {"az_deg": 150, "gap_deg": 6, "width": 0.14, "strength": 0.5, "bright_energy": 320, "radius": 3.0},
        "closure_key": {"energy": 120, "location": [-2.5, -4.0, 6.5], "size": 2.5},  # 뚜껑·스포이트만 비추는 키 (라이트 링킹)
    },
    "grade": {
        "white_knee": 0.85,   # 하이라이트 어깨 시작 (0~1)
        "white_max": 0.975,   # 어깨 최대값 ≈ 249/255 → R=G=B=255 픽셀이 생기지 않는다
        "grain": 0.0,         # Blender 단계 그레인 (0이면 compose_cut.py에서 공통으로 얹는다)
    },
    "render": {"samples": 64, "bounces": 24, "diffuse_bounces": 3, "denoise": True, "min_final_samples": 32,
               "persistent_data": False},  # persistent data는 끈다 (켜면 GPU 공유 중 액체가 검게 렌더된 적이 있다)
    "closure_shadow_fade": [0.6, 1.6],  # 뚜껑·스포이트가 이 높이(lift) 사이에서 그림자를 서서히 얻는다
}

EASES = {
    "linear": lambda u: u,
    "in": lambda u: u * u * u,
    "out": lambda u: 1 - (1 - u) ** 3,
    "inout": lambda u: 4 * u ** 3 if u < 0.5 else 1 - (-2 * u + 2) ** 3 / 2,
    "smooth": lambda u: u * u * (3 - 2 * u),
}


def deep_update(base, extra):
    """base(dict)에 extra를 재귀로 덮어쓴 새 dict."""
    out = copy.deepcopy(base)
    for k, v in (extra or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = deep_update(out[k], v)
        else:
            out[k] = copy.deepcopy(v)
    return out


class Config:
    """프로젝트 설정. 상대 경로는 설정 파일이 있는 폴더 기준."""

    def __init__(self, path):
        self.path = os.path.abspath(path)
        self.dir = os.path.dirname(self.path)
        with open(self.path, encoding="utf-8") as f:
            self.data = json.load(f)
        self.fps = int(self.data.get("fps", 30))
        self.size = tuple(self.data.get("size", [1080, 1920]))
        self.look = deep_update(DEFAULT_LOOK, self.data.get("look"))
        self.cuts = self.data.get("cuts", [])
        prod = self.data.get("product")
        if isinstance(prod, str):  # 제품 프로필 파일 경로
            with open(self.resolve(prod), encoding="utf-8") as f:
                self.product = json.load(f)
            self.product_dir = os.path.dirname(self.resolve(prod))
        else:
            self.product = prod or {}
            self.product_dir = self.dir

    def resolve(self, p, base=None):
        if p is None:
            return None
        p = os.path.expanduser(p)
        return p if os.path.isabs(p) else os.path.normpath(os.path.join(base or self.dir, p))

    def cut(self, cid):
        for c in self.cuts:
            if str(c.get("id")) == str(cid):
                return c
        raise KeyError(f"컷 '{cid}'이 설정에 없다. 있는 컷: {', '.join(str(c.get('id')) for c in self.cuts)}")


# ───────────────────────── 회전체 단면 ─────────────────────────
def r_at(profile, z):
    """단면 [(r, z), ...]에서 높이 z의 반지름 (z가 처음 걸리는 구간에서 선형 보간). 없으면 None."""
    for (r0, z0), (r1, z1) in zip(profile, profile[1:]):
        if min(z0, z1) <= z <= max(z0, z1) and z1 != z0:
            return r0 + (r1 - r0) * (z - z0) / (z1 - z0)
    return None


def inner_offset(outer, wall, base):
    """바깥 단면에서 안쪽 단면을 만든다: 각 점을 법선 방향(병 안쪽)으로 wall만큼, 바닥은 base 두께.
    결과는 위(입술)에서 아래(축)로 내려가는 순서. 축 위의 점(r=0)은 r=0을 유지한다.
    모서리가 많은 단면은 직접 "inner"를 주는 편이 정확하다."""
    pts = [(float(r), float(z)) for r, z in outer]
    out = []
    n = len(pts)
    def left_normal(p, q):               # 진행 방향(축→바깥, 아래→위)의 왼쪽 법선 = 병 안쪽
        tr, tz = q[0] - p[0], q[1] - p[1]
        L = math.hypot(tr, tz) or 1.0
        return -tz / L, tr / L

    for i, (r, z) in enumerate(pts):
        n1 = left_normal(pts[max(0, i - 1)], pts[max(1, i)]) if i > 0 else None
        n2 = left_normal(pts[i], pts[i + 1]) if i < n - 1 else None
        n1, n2 = n1 or n2, n2 or n1
        mr, mz = n1[0] + n2[0], n1[1] + n2[1]   # 모서리는 이등분선 방향으로 (마이터), 길이는 최대 3배
        L = math.hypot(mr, mz) or 1.0
        mr, mz = mr / L, mz / L
        k = min(3.0, 1.0 / max(1e-6, mr * n1[0] + mz * n1[1]))
        rr, zz = r + mr * wall * k, z + mz * wall * k
        if z <= 1e-9:                     # 바닥면은 base 두께
            zz = base
        out.append((max(0.0, rr) if r > 1e-9 else 0.0, max(zz, base)))
    return list(reversed(out))


def split_inner(inner_top_down, level):
    """안쪽 단면(위→아래)을 액체 높이에서 나눈다.
    돌려줌: (above, wet, r_level)
      above = 위→level 점까지 (유리↔공기 안쪽면, 유리 본체 면에 이어 붙인다)
      wet   = 축 바닥 → level 점 (아래→위, 유리↔액체 경계면)
      r_level = 액체 윗면 반지름"""
    pts = inner_top_down
    for i in range(len(pts) - 1):
        (r0, z0), (r1, z1) = pts[i], pts[i + 1]
        if z0 >= level >= z1 and z0 != z1:
            t = (z0 - level) / (z0 - z1)
            p = (r0 + (r1 - r0) * t, level)
            above = pts[:i + 1] + [p]
            wet = list(reversed([p] + pts[i + 1:]))
            return above, wet, p[0]
    raise ValueError(f"액체 높이 {level}가 안쪽 단면 높이 범위 밖이다")


def bottle_surfaces(bottle):
    """제품 프로필의 "bottle"에서 세 굴절 경계면 단면을 만든다.
    돌려줌: dict(glass=[...], wet=[...] | None, top=[(0, L), (rL, L)] | None, inner=[...], level=L|None)"""
    outer = [tuple(p) for p in bottle["outer"]]
    inner = [tuple(p) for p in bottle["inner"]] if bottle.get("inner") else inner_offset(outer, bottle.get("wall", 0.03), bottle.get("base", 0.04))
    level = bottle.get("fill_level")
    if level is None:   # 빈 병: 바깥면 + 안쪽면 전체가 유리↔공기
        return {"glass": outer + inner, "wet": None, "top": None, "inner": inner, "level": None}
    above, wet, rl = split_inner(inner, level)
    return {"glass": outer + above, "wet": wet, "top": [(0.0, level), (rl, level)], "inner": inner, "level": level}


# ───────────────────────── 키프레임 ─────────────────────────
def interp(keys, f, field, default=None):
    """keys = [{"f": 0, "yaw": 0, ...}, {"f": 29, "yaw": 90, "ease": "out"}, ...]
    field가 있는 키들 사이를 보간한다. 구간의 이징은 뒤쪽 키의 "ease" (기본 smooth).
    리스트 값(예: target [x,y,z])은 성분별로 보간한다."""
    ks = sorted((k for k in keys or [] if field in k), key=lambda k: k["f"])
    if not ks:
        return default
    if f <= ks[0]["f"]:
        return ks[0][field]
    if f >= ks[-1]["f"]:
        return ks[-1][field]
    for k0, k1 in zip(ks, ks[1:]):
        if k0["f"] <= f <= k1["f"]:
            span = k1["f"] - k0["f"]
            u = 0.0 if span == 0 else (f - k0["f"]) / span
            u = EASES[k1.get("ease", "smooth")](u)
            a, b = k0[field], k1[field]
            if isinstance(a, (list, tuple)):
                return [x + (y - x) * u for x, y in zip(a, b)]
            if isinstance(a, bool) or isinstance(a, str):
                return a
            return a + (b - a) * u
    return ks[-1][field]


def parse_frames(arg, n):
    """"" → 0..n-1, "0-29" → 범위, "0,15,29" → 목록."""
    if not arg:
        return list(range(n))
    out = []
    for part in str(arg).split(","):
        if "-" in part:
            a, b = part.split("-")
            out.extend(range(int(a), int(b) + 1))
        elif part.strip():
            out.append(int(part))
    return [f for f in out if 0 <= f < n]


def cut_frames(cut, fps):
    """컷의 프레임 수: blender.frames가 있으면 그것, 없으면 길이 × fps."""
    b = cut.get("blender") or {}
    return int(b.get("frames") or round(float(cut["duration"]) * fps))
