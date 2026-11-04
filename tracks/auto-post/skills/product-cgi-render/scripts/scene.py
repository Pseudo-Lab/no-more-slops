# 제품 CGI 장면 모듈 (Blender headless). 제품 프로필(JSON)과 설정의 look으로 장면을 만든다.
# 컷 스크립트(render_cut.py 또는 직접 쓴 스크립트)가 import 해서 쓴다. 이 파일만 실행하면 확인용 정지 이미지를 한 장 렌더한다.
#
# 들어 있는 것
#   - 연한 스튜디오: 바닥과 벽이 이어진 사이클로라마. 바닥은 확산(그림자를 받는다), 벽은 위로 갈수록 하늘빛 발광 + 흐린 소프트박스 하나.
#     수평선이 생기지 않게 곡면이 넓다. 루프 이음매용 배경 곱(BG_TINT, BG_TINT_FLOOR) 노드
#   - 병: 단면 점(r, z)을 돌린 회전체. 굴절 경계면 셋 = 바깥 유리(유리↔공기), 유리↔액체, 액체 윗면(액체↔공기)
#   - 라벨: 사용자가 준 투명 PNG를 바깥 유리면에 붙은 얇은 막에 정면 투영(또는 감싸기). 인쇄 잉크처럼 카메라 광선에만 보이고,
#     반사 없이 투과한 광선에는 back_ink만큼(뒷면 거울 글자). 반사 광선에는 안 보여 유리 속 반사로 글자가 겹치지 않는다
#   - 뚜껑·스포이트: 단면 점으로 만든 부품 묶음(rig). 병과 따로 움직인다(lift). 유리관(pipette)은 액체 높이 위·아래에서 IOR이 바뀐다
#   - 조명: 뒤쪽 옆 가는 세로 띠(라벨 밖 가장자리에만 반사), 높은 앞 소프트박스, 뒤에서 오는 해(접지 그림자 + 액체 색 투과 그림자),
#     좌우 회색 판과 카메라 기준 ±az 가장자리 장치(어두운 판 + 가는 밝은 띠) → 투명 병 윤곽, 라이트 링킹으로 제품에만
#   - 렌더 뒤 보정(grade): 하이라이트 어깨(255 픽셀 방지) + 선택 그레인. 원본은 raw/에 남긴다
#
# 좌표: 병 바닥 중심이 원점, 정면(라벨)이 -y, 위가 +z. 단위는 제품 프로필이 정한다(예: 1 ≈ 3.6cm).
#
# 확인용 실행 (정지 한 장):
#   blender -b --factory-startup -P scripts/scene.py -- --config project.json --out still.png [--samples 16] [--size 540x960]
#           [--yaw 0] [--lift 0] [--cam-yaw 0] [--cam-pitch 8] [--cam-dist 12] [--target 0,0,1.4] [--fov 26]
import argparse
import math
import os
import random
import sys

import bpy
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from cgi_config import Config, bottle_surfaces, r_at  # noqa: E402


def scene():
    return bpy.context.scene


def link(obj):
    scene().collection.objects.link(obj)
    return obj


# ───────────────────────── 재질 도구 ─────────────────────────
def principled(name, **inputs):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    for key, val in inputs.items():
        if key in bsdf.inputs:
            bsdf.inputs[key].default_value = val
    return mat


def sock(sockets, name):
    """이름이 같은 소켓이 여럿인 노드(Mix 등)에서 지금 켜져 있는 소켓을 고른다 (Blender 4·5 공통)."""
    for x in sockets:
        if x.name == name and getattr(x, "enabled", True):
            return x
    return sockets[name]


def _out_src(mat):
    nt = mat.node_tree
    out = [n for n in nt.nodes if n.type == "OUTPUT_MATERIAL"][0]
    return nt, out, out.inputs["Surface"].links[0].from_socket


def shadow_tint(mat, color, amount):
    """그림자 광선에는 색 있는 투명으로: 바닥 그림자 속에 액체를 통과한 색 빛이 맺힌 것처럼 (가짜 커스틱).
    amount 0 = 그림자 그대로, 1 = 그림자 없음."""
    nt, out, src = _out_src(mat)
    tr, mix, lp = nt.nodes.new("ShaderNodeBsdfTransparent"), nt.nodes.new("ShaderNodeMixShader"), nt.nodes.new("ShaderNodeLightPath")
    tr.inputs["Color"].default_value = (color[0] * amount, color[1] * amount, color[2] * amount, 1)
    nt.links.new(lp.outputs["Is Shadow Ray"], mix.inputs["Fac"])
    nt.links.new(src, mix.inputs[1])
    nt.links.new(tr.outputs["BSDF"], mix.inputs[2])
    nt.links.new(mix.outputs["Shader"], out.inputs["Surface"])


def shadow_fade(mat):
    """오브젝트 속성 sfade(0~1, 키프레임 가능)만큼 그림자 광선에 투명. 높이 떠 있는 뚜껑의 떠다니는 그림자를 없앤다."""
    nt, out, src = _out_src(mat)
    attr = nt.nodes.new("ShaderNodeAttribute")
    attr.attribute_type = "OBJECT"
    attr.attribute_name = "sfade"
    lp, mul = nt.nodes.new("ShaderNodeLightPath"), nt.nodes.new("ShaderNodeMath")
    mul.operation = "MULTIPLY"
    nt.links.new(lp.outputs["Is Shadow Ray"], mul.inputs[0])
    nt.links.new(attr.outputs["Fac"], mul.inputs[1])
    tr, mix = nt.nodes.new("ShaderNodeBsdfTransparent"), nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(mul.outputs["Value"], mix.inputs["Fac"])
    nt.links.new(src, mix.inputs[1])
    nt.links.new(tr.outputs["BSDF"], mix.inputs[2])
    nt.links.new(mix.outputs["Shader"], out.inputs["Surface"])


def edge_dark_material(mat, strength=0.5):
    """가장자리 어두운 판: 반사 광선에만, 세기 strength, 판의 위·아래 끝 30%와 좌우를 부드럽게 흐려
    '인쇄된 테두리'가 아니라 유리 가장자리 그늘로 읽히게 한다. 유리 겉면의 직접 반사(투과 깊이 0)에만 비친다
    (액체 수면·내부 반사에 비치면 라벨 위에 막대가 생긴다)."""
    nt, out, src = _out_src(mat)
    tc, sep = nt.nodes.new("ShaderNodeTexCoord"), nt.nodes.new("ShaderNodeSeparateXYZ")
    nt.links.new(tc.outputs["UV"], sep.inputs[0])

    def bell(sock, edge):
        a1, a2, m = nt.nodes.new("ShaderNodeMapRange"), nt.nodes.new("ShaderNodeMapRange"), nt.nodes.new("ShaderNodeMath")
        for node, lo, hi in ((a1, 0.0, edge), (a2, 1.0, 1.0 - edge)):
            node.interpolation_type = "SMOOTHSTEP"
            node.inputs["From Min"].default_value, node.inputs["From Max"].default_value = lo, hi
            nt.links.new(sock, node.inputs["Value"])
        m.operation = "MULTIPLY"
        nt.links.new(a1.outputs["Result"], m.inputs[0])
        nt.links.new(a2.outputs["Result"], m.inputs[1])
        return m.outputs["Value"]
    fv, fu = bell(sep.outputs["Y"], 0.30), bell(sep.outputs["X"], 0.5)
    lp = nt.nodes.new("ShaderNodeLightPath")
    f1, f2, f3, f4, td = (nt.nodes.new("ShaderNodeMath") for _ in range(5))
    for f in (f1, f2, f3, f4):
        f.operation = "MULTIPLY"
    td.operation = "LESS_THAN"
    td.inputs[1].default_value = 0.5
    nt.links.new(fv, f1.inputs[0])
    nt.links.new(fu, f1.inputs[1])
    nt.links.new(f1.outputs["Value"], f2.inputs[0])
    nt.links.new(lp.outputs["Is Glossy Ray"], f2.inputs[1])
    nt.links.new(lp.outputs["Transmission Depth"], td.inputs[0])
    nt.links.new(f2.outputs["Value"], f4.inputs[0])
    nt.links.new(td.outputs["Value"], f4.inputs[1])
    nt.links.new(f4.outputs["Value"], f3.inputs[0])
    f3.inputs[1].default_value = strength
    tr, mix = nt.nodes.new("ShaderNodeBsdfTransparent"), nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(f3.outputs["Value"], mix.inputs["Fac"])
    nt.links.new(tr.outputs["BSDF"], mix.inputs[1])
    nt.links.new(src, mix.inputs[2])
    nt.links.new(mix.outputs["Shader"], out.inputs["Surface"])


# ───────────────────────── 형상 도구 ─────────────────────────
def lathe(name, profile, mat, steps=256):
    """단면 [(r, z), ...]을 z축으로 돌린다 (스크루 모디파이어, 부드러운 셰이딩)."""
    mesh = bpy.data.meshes.new(name)
    verts = [(r, 0, z) for r, z in profile]
    mesh.from_pydata(verts, [(i, i + 1) for i in range(len(verts) - 1)], [])
    obj = link(bpy.data.objects.new(name, mesh))
    scr = obj.modifiers.new("screw", "SCREW")
    scr.steps = scr.render_steps = steps
    scr.use_merge_vertices = True
    scr.use_smooth_shade = True
    obj.data.materials.append(mat)
    return obj


def surface(name, profile, mat, outward=True, steps=256):
    """굴절 경계면용 회전면. 법선이 바깥(축에서 멀어지는 쪽)을 보게 맞춘다.
    경계면 재질의 IOR = (법선 반대쪽 매질) / (법선 쪽 매질). 예: 유리↔액체 면은 법선이 유리 쪽 → IOR 액체/유리."""
    obj = lathe(name, profile, mat, steps=steps)
    for o in bpy.context.view_layer.objects:
        o.select_set(False)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.modifier_apply(modifier="screw")
    me = obj.data
    score = 0.0
    for poly in me.polygons:
        c = poly.center
        radial = Vector((c.x, c.y, 0))
        ref = radial.normalized() if radial.length > 1e-4 else Vector((0, 0, 1))
        score += poly.normal.dot(ref) * poly.area
    if (score > 0) != outward:
        bpy.ops.object.mode_set(mode="EDIT")
        bpy.ops.mesh.select_all(action="SELECT")
        bpy.ops.mesh.flip_normals()
        bpy.ops.object.mode_set(mode="OBJECT")
    obj.select_set(False)
    return obj


def empty(name, parent=None):
    e = link(bpy.data.objects.new(name, None))
    e.empty_display_size = 0.3
    if parent:
        e.parent = parent
    return e


def area(name, loc, size, energy, color=(1, 1, 1), target=(0, 0, 1.0)):
    light = bpy.data.lights.new(name, "AREA")
    light.shape = "RECTANGLE"
    light.size, light.size_y = size
    light.energy = energy
    light.color = color
    obj = link(bpy.data.objects.new(name, light))
    obj.location = loc
    obj.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    return obj


def flag(name, loc, size, gray=0.35, target=(0, 0, 1.2)):
    """회색 판(빛을 막는 깃발): 유리 가장자리에 어두운 선. 카메라·그림자에는 안 보인다."""
    bpy.ops.mesh.primitive_plane_add(size=1, location=loc)
    o = bpy.context.active_object
    o.name = name
    o.scale = (size[0], size[1], 1)
    o.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat("Z", "Y").to_euler()
    o.data.materials.append(principled(name, **{"Base Color": (gray, gray, gray * 1.03, 1), "Roughness": 0.9}))
    o.visible_camera = False
    o.visible_shadow = False
    return o


def linear_keys(obj_or_data):
    """키프레임을 직선 보간으로 (매 프레임 키를 넣을 때 곡선이 넘치지 않게). Blender 4·5 액션 모두."""
    ad = getattr(obj_or_data, "animation_data", None)
    if not ad or not ad.action:
        return
    fcs = getattr(ad.action, "fcurves", None)
    if fcs is None:  # Blender 5 레이어드 액션
        fcs = []
        for layer in ad.action.layers:
            for strip in layer.strips:
                for bag in strip.channelbags:
                    fcs.extend(bag.fcurves)
    for fc in fcs:
        for k in fc.keyframe_points:
            k.interpolation = "LINEAR"


# ───────────────────────── 장면 ─────────────────────────
class Stage:
    """장면 하나. build()가 공장 초기화부터 전부 새로 만든다.
    주요 속성: bottle(rig), closure(rig|None), cam, edge_rig, look, product, mats"""

    def __init__(self, cfg: Config):
        self.cfg, self.look, self.product = cfg, cfg.look, cfg.product
        self.mats = {}
        self.bottle = self.closure = self.cam = self.edge_rig = None
        self.level = None
        self.pipette_level_nodes = []
        self.surfaces = None

    # ── 재질 ──
    def make_materials(self):
        L = self.look
        liq, gl = L["liquid"], L["glass"]
        rgb = tuple(liq["rgb"])
        m = self.mats
        m["glass"] = principled("glass", **{"Base Color": (1, 1, 1, 1), "Roughness": 0.0, "IOR": gl["ior"], "Transmission Weight": 1.0})
        m["liquid"] = principled("liquid", **{"Base Color": rgb + (1,), "Roughness": 0.0, "IOR": liq["ior"], "Transmission Weight": 1.0})
        m["glass_liquid"] = principled("glass_to_liquid", **{"Base Color": rgb + (1,), "Roughness": 0.0, "IOR": liq["ior"] / gl["ior"], "Transmission Weight": 1.0})
        m["air"] = principled("air_bubble", **{"Base Color": (1, 1, 1, 1), "Roughness": 0.0, "IOR": 1.0 / liq["ior"], "Transmission Weight": 1.0})
        sh = liq.get("shadow_rgb", rgb)
        shadow_tint(m["glass"], (1, 1, 1), gl.get("shadow_amount", 0.55))
        shadow_tint(m["glass_liquid"], tuple(c * 0.85 for c in sh), 0.85)
        shadow_tint(m["liquid"], sh, 0.95)
        shadow_tint(m["air"], (1, 1, 1), 1.0)

    def part_material(self, name, spec):
        """뚜껑·스포이트 부품 재질 (부품마다 따로 만들어 그림자 페이드를 병과 나눈다).
        spec: "matte_white" | "inner_white" | "gloss_white" | "matte_black" | "gloss_black" | "glass" | "pipette" | {base_color, roughness, metallic}"""
        L = self.look
        if spec == "pipette":
            return self.pipette_material(name)
        presets = {
            "matte_white": {"Base Color": (0.92, 0.93, 0.94, 1), "Roughness": 0.58, "Specular IOR Level": 0.35, "Subsurface Weight": 0.05},
            "inner_white": {"Base Color": (0.92, 0.93, 0.94, 1), "Roughness": 0.6, "Emission Color": (1, 1, 1, 1), "Emission Strength": 0.55},
            "gloss_white": {"Base Color": (0.92, 0.93, 0.94, 1), "Roughness": 0.15},
            "matte_black": {"Base Color": (0.02, 0.02, 0.025, 1), "Roughness": 0.55},
            "gloss_black": {"Base Color": (0.02, 0.02, 0.025, 1), "Roughness": 0.12},
            "glass": {"Base Color": (1, 1, 1, 1), "Roughness": 0.0, "IOR": L["glass"]["ior"], "Transmission Weight": 1.0},
        }
        if isinstance(spec, dict):
            inputs = {"Base Color": tuple(spec.get("base_color", (0.8, 0.8, 0.8))) + (1,), "Roughness": spec.get("roughness", 0.5),
                      "Metallic": spec.get("metallic", 0.0)}
        else:
            inputs = presets[spec]
        mat = principled(f"part_{name}", **inputs)
        shadow_fade(mat)
        return mat

    def pipette_material(self, name):
        """유리관: 액체 윗면(월드 z) 아래에서는 액체 속 유리(유리/액체), 위에서는 공기 속 유리.
        스포이트가 병 밖에서 안으로 들어가는 동안 굴절이 맞게 바뀐다. 기준 높이는 set_bottle_z()가 따라 움직인다."""
        L = self.look
        mat = bpy.data.materials.new(f"part_{name}")
        mat.use_nodes = True
        nt = mat.node_tree
        nt.nodes.clear()
        out = nt.nodes.new("ShaderNodeOutputMaterial")
        wet, dry = nt.nodes.new("ShaderNodeBsdfPrincipled"), nt.nodes.new("ShaderNodeBsdfPrincipled")
        for b, ior in ((wet, L["glass"]["ior"] / L["liquid"]["ior"]), (dry, L["glass"]["ior"])):
            b.inputs["Base Color"].default_value = (1, 1, 1, 1)
            b.inputs["Roughness"].default_value = 0.0
            b.inputs["IOR"].default_value = ior
            b.inputs["Transmission Weight"].default_value = 1.0
        geo, sep, cmp_, mix = (nt.nodes.new(t) for t in ("ShaderNodeNewGeometry", "ShaderNodeSeparateXYZ", "ShaderNodeMath", "ShaderNodeMixShader"))
        cmp_.operation = "GREATER_THAN"
        cmp_.inputs[1].default_value = self.level if self.level is not None else -1e6
        self.pipette_level_nodes.append(cmp_)
        nt.links.new(geo.outputs["Position"], sep.inputs[0])
        nt.links.new(sep.outputs["Z"], cmp_.inputs[0])
        nt.links.new(cmp_.outputs["Value"], mix.inputs["Fac"])
        nt.links.new(wet.outputs["BSDF"], mix.inputs[1])
        nt.links.new(dry.outputs["BSDF"], mix.inputs[2])
        nt.links.new(mix.outputs["Shader"], out.inputs["Surface"])
        shadow_fade(mat)
        return mat

    def ink_material(self, png, ink_rgb, back_ink):
        """인쇄 잉크: 텍스처 알파로 투명과 섞고, 카메라 광선(1.0) + 반사 없이 투과한 광선(back_ink)에만 보인다."""
        mat = bpy.data.materials.new("ink")
        mat.use_nodes = True
        nt = mat.node_tree
        nt.nodes.clear()
        out = nt.nodes.new("ShaderNodeOutputMaterial")
        tex = nt.nodes.new("ShaderNodeTexImage")
        tex.image = bpy.data.images.load(png, check_existing=True)
        tex.interpolation = "Cubic"
        tex.extension = "CLIP"
        ink = nt.nodes.new("ShaderNodeBsdfPrincipled")
        ink.inputs["Base Color"].default_value = tuple(ink_rgb) + (1,)
        ink.inputs["Roughness"].default_value = 0.35
        # 잉크 색을 PNG에서 가져오고 싶으면 (컬러 라벨) 텍스처 색을 Base Color에 잇는다
        if self.product.get("label", {}).get("use_png_color"):
            nt.links.new(tex.outputs["Color"], ink.inputs["Base Color"])
        clear, mix, lp = nt.nodes.new("ShaderNodeBsdfTransparent"), nt.nodes.new("ShaderNodeMixShader"), nt.nodes.new("ShaderNodeLightPath")
        vis, no_gloss, tr_ok, back, only = (nt.nodes.new("ShaderNodeMath") for _ in range(5))
        vis.operation = "MAXIMUM"
        no_gloss.operation = "LESS_THAN"
        no_gloss.inputs[1].default_value = 0.5
        tr_ok.operation = back.operation = only.operation = "MULTIPLY"
        back.inputs[1].default_value = back_ink
        nt.links.new(lp.outputs["Glossy Depth"], no_gloss.inputs[0])
        nt.links.new(lp.outputs["Is Transmission Ray"], tr_ok.inputs[0])
        nt.links.new(no_gloss.outputs["Value"], tr_ok.inputs[1])
        nt.links.new(tr_ok.outputs["Value"], back.inputs[0])
        nt.links.new(lp.outputs["Is Camera Ray"], vis.inputs[0])
        nt.links.new(back.outputs["Value"], vis.inputs[1])
        nt.links.new(tex.outputs["Alpha"], only.inputs[0])
        nt.links.new(vis.outputs["Value"], only.inputs[1])
        nt.links.new(only.outputs["Value"], mix.inputs["Fac"])
        nt.links.new(clear.outputs["BSDF"], mix.inputs[1])
        nt.links.new(ink.outputs["BSDF"], mix.inputs[2])
        nt.links.new(mix.outputs["Shader"], out.inputs["Surface"])
        if hasattr(mat, "surface_render_method"):
            mat.surface_render_method = "DITHERED"
        return mat

    # ── 병 ──
    def build_bottle(self):
        """병 rig(empty). rig.rotation_euler.z 로 돌린다 (0 = 라벨 정면이 -y)."""
        b = self.product["bottle"]
        s = bottle_surfaces(b)
        self.surfaces, self.level = s, s["level"]
        rig = empty("bottle_rig")
        parts = [surface("glass", s["glass"], self.mats["glass"], outward=True)]
        if s["wet"]:
            parts.append(surface("glass_liquid", s["wet"], self.mats["glass_liquid"], outward=True))
            parts.append(surface("liquid_top", s["top"], self.mats["liquid"], outward=True))
        for o in parts:
            o.parent = rig
        if b.get("threads"):
            self.threads(rig, b["threads"])
        lab = self.product.get("label")
        if lab and lab.get("png"):
            self.label_print(rig, lab)
        if self.product.get("bubbles") and s["wet"]:
            self.bubbles(rig, self.product["bubbles"], lab)
        self.bottle = rig
        return rig

    def threads(self, parent, t):
        """병 목 나사산: 나선 곡선 + 둥근 단면, 양 끝은 반지름을 줄여 목으로 녹아들게."""
        cu = bpy.data.curves.new("threads", "CURVE")
        cu.dimensions = "3D"
        cu.bevel_depth = t.get("thickness", 0.016)
        cu.bevel_resolution = 4
        cu.use_fill_caps = True
        sp = cu.splines.new("POLY")
        n, turns = 160, t.get("turns", 1.3)
        sp.points.add(n - 1)
        for i in range(n):
            u = i / (n - 1)
            a = u * turns * math.tau
            sp.points[i].co = (t["r"] * math.cos(a), t["r"] * math.sin(a), t["z0"] + (t["z1"] - t["z0"]) * u, 1)
            sp.points[i].radius = min(1.0, u / 0.08, (1 - u) / 0.08)
        obj = link(bpy.data.objects.new("threads", cu))
        obj.data.materials.append(self.mats["glass"])
        obj.parent = parent
        return obj

    def label_png_path(self, lab):
        return self.cfg.resolve(lab["png"], self.cfg.product_dir)

    def label_print(self, parent, lab):
        """인쇄 라벨: 바깥 유리면에 붙은 얇은 막 (행마다 그 높이의 바깥 반지름 + offset).
        projection "front" = 정면 투영(정면에서 PNG가 그대로 보인다), "wrap" = 각도로 감싸기(둘레 인쇄)."""
        outer = self.product["bottle"]["outer"]
        z0, z1 = lab["z0"], lab["z1"]
        arc = math.radians(lab.get("arc_deg", 160))
        off = lab.get("offset", 0.0015)
        proj = lab.get("projection", "front")
        seg, rows = 64, max(2, int(lab.get("rows", 24)))
        verts, faces, uvs = [], [], []
        for j in range(rows + 1):
            z = z0 + (z1 - z0) * j / rows
            r = (r_at(outer, z) or outer[-1][0]) + off
            for i in range(seg + 1):
                a = -math.pi / 2 - arc / 2 + arc * i / seg
                x, y = r * math.cos(a), r * math.sin(a)
                verts.append((x, y, z))
                u = (x / r + 1) / 2 if proj == "front" else (a + math.pi / 2) / arc + 0.5
                uvs.append((u, j / rows))
        for j in range(rows):
            for i in range(seg):
                k = j * (seg + 1) + i
                faces.append((k, k + 1, k + seg + 2, k + seg + 1))
        me = bpy.data.meshes.new("label")
        me.from_pydata(verts, [], faces)
        uv = me.uv_layers.new(name="UV")
        for poly in me.polygons:
            poly.use_smooth = True
            for li in poly.loop_indices:
                uv.data[li].uv = uvs[me.loops[li].vertex_index]
        obj = link(bpy.data.objects.new("label", me))
        obj.data.materials.append(self.ink_material(self.label_png_path(lab), lab.get("ink_rgb", (0.02, 0.02, 0.025)), lab.get("back_ink", 0.38)))
        obj.parent = parent
        return obj

    def label_hit_fn(self, lab):
        """정면에서 본 (x, z) 둘레 r 안에 인쇄 글자가 있는지. 액체 속 물체는 원통 렌즈로 가로 약 lens배 커 보인다.
        기포가 글자에 겹치면 글자가 달라 보인다(예: 철자 끝에 '-'가 붙어 보임) → 겹치는 자리는 다시 뽑는다."""
        if not lab or not lab.get("png"):
            return lambda x, z, r: False
        import numpy as np  # Blender에 들어 있다
        img = bpy.data.images.load(self.label_png_path(lab), check_existing=True)
        w, h = img.size
        px = np.empty(w * h * 4, dtype=np.float32)
        img.pixels.foreach_get(px)
        alpha = px.reshape(h, w, 4)[::4, ::4, 3]  # 아래가 0행
        ah, aw = alpha.shape
        z0, z1 = lab["z0"], lab["z1"]
        lens = lab.get("lens", 1.3)
        outer = self.product["bottle"]["outer"]

        def hit(x, z, r):
            R = r_at(outer, z) or outer[-1][0]
            m = r + 0.03
            u0, u1 = ((x - m) * lens / R + 1) / 2, ((x + m) * lens / R + 1) / 2
            v0, v1 = (z - m - z0) / (z1 - z0), (z + m - z0) / (z1 - z0)
            if v1 < 0 or v0 > 1 or u1 < 0 or u0 > 1:
                return False
            c0, c1 = max(0, int(u0 * aw)), min(aw, int(u1 * aw) + 1)
            r0, r1 = max(0, int(v0 * ah)), min(ah, int(v1 * ah) + 1)
            return bool(c1 > c0 and r1 > r0 and alpha[r0:r1, c0:c1].max() > 0.05)
        return hit

    def bubbles(self, parent, bc, lab):
        """액체 속 기포: 윗면 바로 아래 큰 기포 띠(top) + 몸통 작은 기포(body). 정면에서 라벨 글자에 겹치지 않게."""
        random.seed(bc.get("seed", 5))
        hit = self.label_hit_fn(lab) if bc.get("avoid_label", True) else (lambda *a: False)
        inner = self.surfaces["inner"]
        lvl = self.level
        n_top, n_body = int(bc.get("top", 40)), int(bc.get("body", 30))
        rt, rb = bc.get("r_top", [0.025, 0.07]), bc.get("r_body", [0.008, 0.026])
        zb = bc.get("body_z", [0.3, lvl - 0.25])
        made = []
        for i in range(n_top + n_body):
            top = i < n_top
            for _try in range(60):
                a = random.random() * math.tau
                rr = rt[0] + random.random() * (rt[1] - rt[0]) if top else rb[0] + random.random() * (rb[1] - rb[0])
                z = (lvl - rr - 0.004 - random.random() * 0.05) if top else (zb[0] + random.random() * (zb[1] - zb[0]))
                ri = (r_at(inner, z) or 0.1) - 0.04
                d = random.random() ** 0.5 * max(0.0, ri - rr)
                if not hit(math.cos(a) * d, z, rr):
                    break
            bpy.ops.mesh.primitive_uv_sphere_add(radius=rr, segments=24, ring_count=12, location=(math.cos(a) * d, math.sin(a) * d, z))
            s = bpy.context.active_object
            s.name = f"bubble_{'top' if top else 'body'}_{i:02d}"
            s.data.materials.append(self.mats["air"])
            bpy.ops.object.shade_smooth()
            s.parent = parent
            s["z0"] = z
            made.append(s)
        return made

    # ── 뚜껑·스포이트 ──
    def build_closure(self):
        """제품 프로필 "closure.parts"의 부품을 rig 하나로. rig.location.z = seat_z + lift (0 = 꽂힘/닫힘)."""
        c = self.product.get("closure")
        if not c:
            return None
        rig = empty("closure_rig", self.bottle)
        rig["seat_z"] = c.get("seat_z", 0.0)
        rig.location.z = rig["seat_z"]
        for p in c["parts"]:
            mat = self.part_material(p["name"], p.get("material", "matte_white"))
            prof = [tuple(v) for v in p["profile"]]
            if p.get("refractive") or p.get("material") in ("pipette", "glass"):
                o = surface(p["name"], prof, mat, outward=True, steps=p.get("steps", 96))
            else:
                o = lathe(p["name"], prof, mat, steps=p.get("steps", 256))
            o.parent = rig
            o["sfade"] = 0.0
            o["key_lit"] = p.get("material", "matte_white") not in ("pipette", "glass")
        self.closure = rig
        return rig

    def set_lift(self, lift):
        """뚜껑을 lift만큼 들어 올리고, 그림자 페이드를 높이에 맞춘다 (높이 떠 있으면 그림자 없음)."""
        if not self.closure:
            return
        self.closure.location.z = self.closure["seat_z"] + lift
        lo, hi = self.look.get("closure_shadow_fade", [0.6, 1.6])
        for o in self.closure.children:
            o["sfade"] = fade_val(lift, lo, hi)

    def set_bottle_z(self, z):
        """병 높이를 바꾸면 유리관 IOR 전환 높이도 따라간다."""
        self.bottle.location.z = z
        if self.level is not None:
            for n in self.pipette_level_nodes:
                n.inputs[1].default_value = self.level + z

    # ── 스튜디오·조명 ──
    def studio(self):
        """바닥과 벽이 이어진 사이클로라마. 바닥은 확산면(그림자를 받는다), 벽은 위로 갈수록 하늘빛 발광."""
        st = self.look["studio"]
        floor_white, wall_glow = st["floor_white"], st["wall_glow"]
        mat = bpy.data.materials.new("cyc")
        mat.use_nodes = True
        nt = mat.node_tree
        nt.nodes.clear()
        out = nt.nodes.new("ShaderNodeOutputMaterial")
        diff = nt.nodes.new("ShaderNodeBsdfDiffuse")
        tc, sep = nt.nodes.new("ShaderNodeTexCoord"), nt.nodes.new("ShaderNodeSeparateXYZ")
        nt.links.new(tc.outputs["Object"], sep.inputs[0])
        mr_c = nt.nodes.new("ShaderNodeMapRange")    # 높이 → 색 (아래 base → 위 sky)
        mr_c.inputs["From Min"].default_value, mr_c.inputs["From Max"].default_value = 2.5, 9.0
        ramp = nt.nodes.new("ShaderNodeValToRGB")
        ramp.color_ramp.interpolation = "EASE"
        ramp.color_ramp.elements[0].color = (*st["base"], 1)
        ramp.color_ramp.elements[1].color = (*st["sky"], 1)
        mr_s = nt.nodes.new("ShaderNodeMapRange")    # 깊이 → 발광 세기 (앞 바닥 0 → 벽 wall_glow)
        mr_s.inputs["From Min"].default_value, mr_s.inputs["From Max"].default_value = 0.0, 4.5
        mr_s.interpolation_type = "SMOOTHSTEP"
        mr_s.inputs["To Min"].default_value, mr_s.inputs["To Max"].default_value = 0.0, wall_glow
        emit, add = nt.nodes.new("ShaderNodeEmission"), nt.nodes.new("ShaderNodeAddShader")
        nt.links.new(sep.outputs["Z"], mr_c.inputs["Value"])
        nt.links.new(mr_c.outputs["Result"], ramp.inputs["Fac"])
        bgt = nt.nodes.new("ShaderNodeMix")          # 루프 이음매: Factor 0→1이면 배경이 loop_mul만큼 곱해진다
        bgt.name = "BG_TINT"
        bgt.data_type, bgt.blend_type = "RGBA", "MULTIPLY"
        sock(bgt.inputs, "Factor").default_value = 0.0
        sock(bgt.inputs, "B").default_value = (*st["loop_mul"], 1)
        nt.links.new(ramp.outputs["Color"], sock(bgt.inputs, "A"))
        nt.links.new(sock(bgt.outputs, "Result"), emit.inputs["Color"])
        mr_d = nt.nodes.new("ShaderNodeMapRange")    # 확산은 앞쪽 바닥에만 (곡면·벽은 발광만 → 수평선 없음)
        mr_d.inputs["From Min"].default_value, mr_d.inputs["From Max"].default_value = 0.0, 4.5
        mr_d.inputs["To Min"].default_value, mr_d.inputs["To Max"].default_value = floor_white, 0.0
        mr_d.interpolation_type = "SMOOTHSTEP"
        nt.links.new(sep.outputs["Y"], mr_d.inputs["Value"])
        tint = nt.nodes.new("ShaderNodeVectorMath")
        tint.operation = "SCALE"
        tint.inputs[0].default_value = tuple(st["floor_tint"])
        nt.links.new(mr_d.outputs["Result"], tint.inputs["Scale"])
        bgf = nt.nodes.new("ShaderNodeMix")
        bgf.name = "BG_TINT_FLOOR"
        bgf.data_type, bgf.blend_type = "RGBA", "MULTIPLY"
        sock(bgf.inputs, "Factor").default_value = 0.0
        sock(bgf.inputs, "B").default_value = (*st["loop_floor_mul"], 1)
        nt.links.new(tint.outputs["Vector"], sock(bgf.inputs, "A"))
        nt.links.new(sock(bgf.outputs, "Result"), diff.inputs["Color"])
        nt.links.new(sep.outputs["Y"], mr_s.inputs["Value"])
        # 벽 위 아주 흐린 소프트박스 하나 (배경이 완전히 고르지 않게)
        sbx = st["softbox"]
        mp = nt.nodes.new("ShaderNodeMapping")
        mp.inputs["Location"].default_value = tuple(sbx["location"])
        mp.inputs["Scale"].default_value = tuple(1 / v for v in sbx["scale"])
        nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
        gr = nt.nodes.new("ShaderNodeTexGradient")
        gr.gradient_type = "SPHERICAL"
        nt.links.new(mp.outputs["Vector"], gr.inputs["Vector"])
        pw, sb, sb2 = (nt.nodes.new("ShaderNodeMath") for _ in range(3))
        pw.operation, sb.operation, sb2.operation = "POWER", "MULTIPLY_ADD", "MULTIPLY"
        pw.inputs[1].default_value = 2.0
        nt.links.new(gr.outputs["Fac"], pw.inputs[0])
        sb.inputs[1].default_value = sbx["add"]
        nt.links.new(pw.outputs["Value"], sb.inputs[0])
        nt.links.new(mr_s.outputs["Result"], sb.inputs[2])
        nt.links.new(mr_s.outputs["Result"], sb2.inputs[0])
        sb2.inputs[1].default_value = 1.0 / max(wall_glow, 1e-3)
        sb3 = nt.nodes.new("ShaderNodeMix")          # 벽 쪽에만 소프트박스 (바닥 발광 0 유지)
        sb3.data_type = "FLOAT"
        nt.links.new(sb2.outputs["Value"], sock(sb3.inputs, "Factor"))
        nt.links.new(mr_s.outputs["Result"], sock(sb3.inputs, "A"))
        nt.links.new(sb.outputs["Value"], sock(sb3.inputs, "B"))
        nt.links.new(sock(sb3.outputs, "Result"), emit.inputs["Strength"])
        nt.links.new(diff.outputs["BSDF"], add.inputs[0])
        nt.links.new(emit.outputs["Emission"], add.inputs[1])
        nt.links.new(add.outputs["Shader"], out.inputs["Surface"])
        # 단면: 바닥(y -16→4) → 반지름 6 곡면 → 벽(y 10, z 6→30)
        rad = 6.0
        prof = [(-16, 0.0), (4, 0.0)] + [(4 + rad * math.sin(a / 16 * math.pi / 2), rad - rad * math.cos(a / 16 * math.pi / 2)) for a in range(1, 17)] + [(4 + rad, 30)]
        verts, faces = [], []
        for x in (-30, 30):
            for d, z in prof:
                verts.append((x, d, z))
        n = len(prof)
        for i in range(n - 1):
            faces.append((i, i + 1, n + i + 1, n + i))
        mesh = bpy.data.meshes.new("cyc")
        mesh.from_pydata(verts, [], faces)
        for p in mesh.polygons:
            p.use_smooth = True
        obj = link(bpy.data.objects.new("cyc", mesh))
        obj.data.materials.append(mat)
        obj.visible_shadow = False  # 뒤에서 오는 해를 벽이 가리지 않게
        return obj

    def world(self):
        wl = self.look["world"]
        w = bpy.data.worlds.new("world")
        scene().world = w
        w.use_nodes = True
        wn = w.node_tree
        bl = wn.nodes["Background"]
        bl.inputs["Color"].default_value = (*wl["light_color"], 1)
        bl.inputs["Strength"].default_value = wl["light_strength"]
        bc = wn.nodes.new("ShaderNodeBackground")
        bc.inputs["Color"].default_value = (*wl["cam_color"], 1)
        bc.inputs["Strength"].default_value = wl["cam_strength"]
        lp, mix = wn.nodes.new("ShaderNodeLightPath"), wn.nodes.new("ShaderNodeMixShader")
        wn.links.new(lp.outputs["Is Camera Ray"], mix.inputs["Fac"])
        wn.links.new(bl.outputs["Background"], mix.inputs[1])
        wn.links.new(bc.outputs["Background"], mix.inputs[2])
        wn.links.new(mix.outputs["Shader"], wn.nodes["World Output"].inputs["Surface"])

    def lights(self, height):
        """라벨 위에 하이라이트가 생기지 않는 조명 키.
        병은 회전면이라 z축으로 돌아도 반사 위치가 그대로다. 반사는 카메라 기준 방위각의 절반 지점(법선)에 생기므로
        빛을 카메라에서 ±125° 넘게(뒤쪽 옆) 두면 반사가 라벨(보통 ±50~55°) 밖 가장자리에 선다."""
        L = self.look["lights"]
        cz = height * 0.55   # 조명이 겨누는 높이
        rim = L["rim"]
        area("rim_l", (-rim["x"], rim["y"], rim["z"]), tuple(rim["size"]), rim["energy"][0], tuple(rim["color_l"]), target=(0, 0, cz))
        area("rim_r", (rim["x"], rim["y"], rim["z"]), tuple(rim["size"]), rim["energy"][1], target=(0, 0, cz))
        fr = L["front"]
        area("front", tuple(fr["location"]), (fr["size"], fr["size"]), fr["energy"], target=(0, 0, cz * 1.2))
        su = L["sun"]
        sun = bpy.data.lights.new("sun", "SUN")
        sun.energy = su["energy"]
        sun.angle = math.radians(su["angle_deg"])
        so = link(bpy.data.objects.new("sun", sun))
        so.rotation_euler = tuple(math.radians(v) for v in su["rotation_deg"])
        fl = L["flags"]
        flag("flag_l", (-fl["x"], fl["y"], cz), tuple(fl["size"]), fl["gray"], target=(0, 0, cz))
        flag("flag_r", (fl["x"], fl["y"], cz), tuple(fl["size"]), fl["gray"] + 0.02, target=(0, 0, cz))
        bf = L.get("back_flags")
        if bf:
            flag("flag_bl", (-bf["x"], 2.0, cz * 1.25), (0.6, 8.0), bf["gray"], target=(0, 0, cz * 1.25))
            flag("flag_br", (bf["x"], 2.0, cz * 1.25), (0.6, 8.0), bf["gray"], target=(0, 0, cz * 1.25))
        # 유리 가장자리 선: 카메라 기준 ±az에 가는 어두운 판 + 가는 밝은 띠. edge_rig를 카메라 방위각만큼 돌려 따라가게 한다.
        # az 160° 이상은 액체 속 내부 반사로 라벨 위에 막대가 생겼다 → 150° 근처
        ed = L["edges"]
        self.edge_rig = empty("edge_rig")
        if ed.get("az_deg"):
            for sx in (-1, 1):
                a = math.radians(ed["az_deg"]) * sx
                for da, kind in ((0.0, "dark"), (ed["gap_deg"] * sx, "bright")):
                    aa = a + math.radians(da)
                    loc = (math.sin(aa) * ed["radius"], -math.cos(aa) * ed["radius"], cz)
                    if kind == "dark":
                        fo = flag(f"edge_dark_{sx}", loc, (ed["width"], height * 3.0), 0.01, target=(0, 0, cz))
                        edge_dark_material(fo.data.materials[0], ed["strength"])
                    else:
                        fo = area(f"edge_bright_{sx}", loc, (0.08, height * 3.0), ed["bright_energy"], target=(0, 0, cz))
                    fo.parent = self.edge_rig
        self.world()

    def link_lights(self):
        """라이트 링킹: 가는 세로 띠·가장자리 밝은 띠는 제품에만(벽에 번지면 배경에 밝은 가로 띠), 뚜껑 키는 불투명 부품에만."""
        prod = bpy.data.collections.new("product_receivers")
        stack = [self.bottle]
        while stack:
            o = stack.pop()
            stack.extend(o.children)
            if o.type in ("MESH", "CURVE"):
                prod.objects.link(o)
        for o in bpy.data.objects:
            if o.name in ("rim_l", "rim_r") or o.name.startswith("edge_bright"):
                o.light_linking.receiver_collection = prod
        if self.closure:
            col = bpy.data.collections.new("closure_receivers")
            for o in self.closure.children:
                if o.get("key_lit"):
                    col.objects.link(o)
            ck = self.look["lights"]["closure_key"]
            top = max(z for _, z in self.product["bottle"]["outer"])
            key = area("closure_key", tuple(ck["location"]), (ck["size"], ck["size"]), ck["energy"], target=(0, 0, top + 0.3))
            key.light_linking.receiver_collection = col

    # ── 카메라·렌더 ──
    def camera(self, fov_deg=26):
        cd = bpy.data.cameras.new("cam")
        cd.sensor_fit = "VERTICAL"
        cd.lens_unit = "FOV"
        cd.angle = math.radians(fov_deg)
        cd.clip_start = 0.01
        cam = link(bpy.data.objects.new("cam", cd))
        cd.dof.use_dof = True
        cd.dof.aperture_fstop = 8.0
        scene().camera = cam
        self.cam = cam
        return cam

    def aim(self, target, yaw_deg, pitch_deg, dist, focus=None):
        """target을 중심으로 방위각 yaw(0 = 정면 -y), 위로 pitch, 거리 dist. 가장자리 장치도 yaw를 따라 돈다."""
        yaw, pitch = math.radians(yaw_deg), math.radians(pitch_deg)
        target = Vector(target)
        cam = self.cam
        cam.location = target + Vector((math.sin(yaw) * math.cos(pitch), -math.cos(yaw) * math.cos(pitch), math.sin(pitch))) * dist
        cam.rotation_euler = (target - cam.location).to_track_quat("-Z", "Y").to_euler()
        cam.data.dof.focus_distance = focus if focus is not None else dist
        if self.edge_rig is not None:
            self.edge_rig.rotation_euler.z = yaw

    def render_setup(self, samples=None, size=(1080, 1920), device="AUTO"):
        R = self.look["render"]
        sc = scene()
        sc.render.resolution_x, sc.render.resolution_y = size
        sc.render.resolution_percentage = 100
        sc.render.fps = self.cfg.fps
        sc.view_settings.view_transform = "Standard"
        sc.view_settings.look = "None"
        sc.render.engine = "CYCLES"
        sc.render.use_persistent_data = bool(R.get("persistent_data", False))
        use_gpu = False
        prefs = bpy.context.preferences.addons["cycles"].preferences
        kinds = ["METAL", "OPTIX", "CUDA", "HIP", "ONEAPI"] if device == "AUTO" else ([] if device == "CPU" else [device])
        for kind in kinds:
            try:
                prefs.compute_device_type = kind
                prefs.get_devices()
                devs = [d for d in prefs.devices if d.type == kind]
                if devs:
                    for d in prefs.devices:
                        d.use = d.type == kind
                    use_gpu = True
                    break
            except TypeError:
                continue
        sc.cycles.device = "GPU" if use_gpu else "CPU"
        sc.cycles.samples = int(samples or R["samples"])
        sc.cycles.use_adaptive_sampling = True
        sc.cycles.use_denoising = bool(R.get("denoise", True))
        for k in ("max_bounces", "transmission_bounces", "transparent_max_bounces", "glossy_bounces"):
            setattr(sc.cycles, k, int(R["bounces"]))
        sc.cycles.diffuse_bounces = int(R["diffuse_bounces"])
        sc.cycles.caustics_refractive = True
        sc.cycles.caustics_reflective = True
        sc.cycles.blur_glossy = 0.5
        sc.render.image_settings.file_format = "PNG"
        sc.render.image_settings.color_mode = "RGB"
        return sc.cycles.device

    def build(self, fov=26):
        """장면 전체를 새로 만든다."""
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.make_materials()
        self.studio()
        self.build_bottle()
        height = max(z for _, z in self.product["bottle"]["outer"])
        self.lights(height)
        self.build_closure()
        self.link_lights()
        self.camera(fov)
        return self


def fade_val(lift, lo, hi):
    """sfade(그림자 광선 투명도): lift가 lo 이하면 0(그림자 그대로), hi 이상이면 1(그림자 없음)."""
    return min(1.0, max(0.0, (lift - lo) / max(1e-6, hi - lo)))


# ───────────────────────── 렌더 뒤 보정 ─────────────────────────
def grade(path_raw, path_out, g, seed=0):
    """하이라이트 어깨(무릎 white_knee부터 부드럽게 눌러 최대 white_max) + 단색 그레인. raw는 그대로 둔다.
    255 픽셀(완전한 흰색)은 고급 광고에서 '번진 흰 덩어리'로 보인다 → 렌더 단계에서 막는다."""
    import numpy as np
    img = bpy.data.images.load(path_raw)
    w, h = img.size
    px = np.empty(w * h * 4, dtype=np.float32)
    img.pixels.foreach_get(px)
    px = px.reshape(h, w, 4)
    kn, wm, gr = g["white_knee"], g["white_max"], g.get("grain", 0.0)
    noise = np.random.default_rng(seed).normal(0, gr, size=(h, w)).astype(np.float32) if gr > 0 else 0.0

    def shoulder(x):
        over = np.maximum(x - kn, 0)
        return np.where(x > kn, kn + (wm - kn) * (1 - np.exp(-over / (wm - kn))), x)

    for c in range(3):
        px[:, :, c] = np.clip(shoulder(px[:, :, c]) + noise, 0, wm)
    img.pixels.foreach_set(px.ravel())
    img.filepath_raw = path_out
    img.file_format = "PNG"
    img.save()
    bpy.data.images.remove(img)


def render_still(path, look_grade, seed=0):
    """raw/에 원본, path에 보정본."""
    d = os.path.dirname(os.path.abspath(path))
    raw = os.path.join(d, "raw", os.path.basename(path))
    os.makedirs(os.path.dirname(raw), exist_ok=True)
    scene().render.filepath = raw
    bpy.ops.render.render(write_still=True)
    grade(raw, path, look_grade, seed)


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    ap = argparse.ArgumentParser(prog="scene.py")
    ap.add_argument("--config", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--samples", type=int, default=16)
    ap.add_argument("--size", default="540x960")
    ap.add_argument("--device", default="AUTO")
    ap.add_argument("--yaw", type=float, default=0.0)
    ap.add_argument("--lift", type=float, default=0.0)
    ap.add_argument("--cam-yaw", type=float, default=0.0)
    ap.add_argument("--cam-pitch", type=float, default=8.0)
    ap.add_argument("--cam-dist", type=float, default=12.0)
    ap.add_argument("--target", default="")
    ap.add_argument("--fov", type=float, default=26.0)
    a = ap.parse_args(argv)
    st = Stage(Config(a.config)).build(a.fov)
    st.bottle.rotation_euler.z = math.radians(a.yaw)
    st.set_lift(a.lift)
    h = max(z for _, z in st.product["bottle"]["outer"])
    tgt = [float(v) for v in a.target.split(",")] if a.target else (0, 0, h * 0.6)
    st.aim(tgt, a.cam_yaw, a.cam_pitch, a.cam_dist)
    dev = st.render_setup(a.samples, tuple(int(v) for v in a.size.split("x")), a.device)
    render_still(a.out, st.look["grade"])
    print("SCENE_STILL_DONE", a.out, "device", dev)
