# /// script
# requires-python = ">=3.10"
# dependencies = ["typesafe-sdk[pil]==0.7.5", "numpy>=1.24", "opencv-python-headless>=4.8"]
# ///
"""도면 한 장 → 모든 심볼의 bbox·클래스 + 심볼 사이 연결 + 텍스트 박스. 결과를 도면 위에 그린다.
로직 다이어그램(CLD)과 P&ID를 모두 다룬다: 글자 높이를 재서 모든 크기 기준을 도면 해상도에 맞추고(page_cv.set_scale),
도면 종류는 Jev S0가 정한다 (--kind 로 지정 가능). 종류에 따라 질문 문구·범례(legend_cld.json / legend_pid.json)·점선 처리가 바뀐다.

순서 (코드가 후보를 만들고 Jev가 고른다. Jev 질문은 Choice/Noul만 쓰고, Choice는 옵션 순서를 바꿔 두 번 묻는다):
  0. 종류      Jev S0 (Choice, 도면 전체 축소 이미지): 로직 다이어그램 / P&ID / 기타.  코드: 표(표제란·개정란 등 괘선 표) 찾기 → 이후 단계에서 제외
  1. 영역      코드: 잉크 덩어리로 큰 영역 나누기          → Jev S1 (Choice): 로직 다이어그램 / 표 / 표제란 / 노트 / 모듈 박스 …
  2. 후보      코드: 닫힌 도형 내부, 채운 도형, 열린 밸브, 탱크의 전체 윤곽과 서로 붙은 밸브/축소부 분리      → Jev S2 (Choice): 심볼 / 심볼 일부 / 글자 / 표 칸 / 선으로 둘러싸인 빈 곳 …
  3. bbox 맞춤 코드: 윤곽선 박스 + 붙어 있는 획(게이트 입력 바, 램프 방사선)까지 넓힌 박스 → Jev B6 (Choice): 어느 박스가 심볼 전체에 맞나
               (--refine edges 로 바꾸면 예전 방식: Jev B1 변 방향 판단을 반복하는 p0_refine 루프)
  4. 중복 제거 코드: IoU 0.5 이상이면 확신도 높은 쪽만
  5. 분류      Jev C1 (Choice, 범례 예시 이미지 포함), 작은 모호한 P&ID 도형은 확대 C2 재검토: OR / AND / S-R / 램프 / 연속표시 … (experiments/legend_cld.json)
  6. 연결      코드: 박스를 지운 선을 따라가 net 만들기(교차점 끊긴 선은 건너뜀, P&ID는 점선 신호선·플랜지 틈도 잇는다) → 같은 net의 심볼 쌍마다
               Jev K3 (Noul, 빨강/파랑 바꿔 2회): 두 심볼이 선으로 이어져 있나. P&ID는 K5로 원본 경로를 확대해 검토하고, 거절된 연결의 복원에는 K6 끝점 검증도 요구한다. 심볼이 많은 net은 최소 신장 트리만 묻는다
  7. 텍스트    코드: 다이어그램 안 글자를 줄 → 덩어리로 묶기(심볼 선을 넘지 않음, 90도 돌린 글자도) → Jev T1 (Choice): 글자 덩어리 / 일부 /
               여러 덩어리 / 글자 아님 (P&ID는 '노트·표 글자'도 골라 뺀다).  P&ID에서 두 줄 이상인 덩어리는
               Jev T2 (Noul, 색 바꿔 2회): 이웃한 두 줄이 한 라벨인가 → 아니면 나눈다 (밸브 번호 아래 배관 번호 등)
               심볼 안 글자(S/R, 램프 W, 연속표시 번호, 시스템 이름, 계기 태그)는 따로 텍스트 박스가 되고 'inside' 관계로 그 심볼과 묶인다
  8. 출력      docs/PLAN.md §6 형식 JSON + 시각화(HTML 뷰어, 결과 PNG, 단계별 PNG)

실행 (cad-jev 루트에서):
    uv run experiments/run_page.py image/page-016.png --model jev-1.14.0
    uv run experiments/run_page.py image/page-022.png --model jev-1.14.0   # P&ID (종류는 S0가 판단, --kind pid 로 지정해도 됨)
    uv run experiments/run_page.py image/page-016.png --dry-run        # Jev 호출 없이 코드 단계만 보고 예상 비용 확인
결과: runs/page/<페이지>-<시각>/
    page-016.html          도면 위 결과 뷰어 (브라우저로 열기)
    page-016_overlay.png   전체 결과 이미지,  page-016_steps.png  단계별 이미지,  page-016_objects.png  객체별 확대
    page-016_output.json   최종 출력 (objects + relations),  page-016_trace.json  단계별 Jev 확률 기록
    summary.md             요약 (요청 수, 비용, 정답 파일이 있으면 정답 대비 점수)
같은 질문은 .cache/jev/ 에 저장돼 다시 돌리면 비용 없이 재사용된다 (--no-cache 로 끔).
"""
from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import math
import os
import statistics
import sys
import time
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
import cv2  # noqa: E402
import numpy as np  # noqa: E402

import p0_refine as R  # noqa: E402
import page_cv as CV  # noqa: E402
import views as V  # noqa: E402
import visualize as VZ  # noqa: E402
import connection_geometry as CG  # noqa: E402
import classification_detail as CD  # noqa: E402
import frame_geometry as FG  # noqa: E402
import text_geometry as TG  # noqa: E402
import symbol_geometry as SG  # noqa: E402
import logic_geometry as LG  # noqa: E402
import equipment_geometry as EG  # noqa: E402
import arrow_geometry as AG  # noqa: E402
import port_geometry as PG  # noqa: E402
import drawing_kind as DK  # noqa: E402
import signal_geometry as SIG  # noqa: E402
import crossing_geometry as XG  # noqa: E402
from p0_bench import FATAL, IMAGES_ON, PX_PER_TOKEN, TASK, USD_PER_TOKEN, WORDS, Fatal, load_env  # noqa: E402

DEFAULT_MODEL = "jev-1.14.0"
REQ_TOKENS = 24_000          # 요청 한 번의 추정 토큰 상한. 실측: jev-1.14.0은 약 4만 토큰 요청을 max_tokens_exceeded로 거부
                             # (요청당 한도가 32k로 보임). 넘치면 요청을 반으로 나눠 다시 보낸다 (Jev.ask_chunked)
MIN_REGION_SIDE = 120                        # 이보다 작은 영역(테두리 화살표 등)은 묻지 않고 '기타'
KEEP_SYMBOL = 0.4                            # S2: P(심볼) + P(심볼 일부)가 이 값 이상이면 후보 유지 (놓치는 쪽이 더 나빠서 낮게)
CONTAINER_SYMBOL = 0.8                       # S2: 다른 후보를 통째로 품은 후보(선으로 둘러싸인 영역 등)는 P(심볼)이 이 값 이상일 때만 유지
ACCEPT_LINK = 0.5                            # K3: 평균 P(연결)이 이 값 이상이면 관계로 출력
LOCAL_RECOVER = 0.60                        # every bounded route view must support a global-pair recovery
LOCAL_REJECT = 0.15                         # an unequivocally broken local span vetoes a global pair
DROP_OTHER = 0.5                             # C1: P(기타)가 이 값 이상이고
S2_TRUST = 0.7                               #     S2의 P(심볼)+P(심볼 일부)가 이 값보다 낮을 때만(두 판단이 모두 심볼이 아니라고 볼 때만) 뺀다
DUP_IOU = 0.5
TEXT_DROP = 0.5                              # T1: P(글자 아님)이 이 값 이상이면 텍스트 후보를 버린다
SEARCH_KINDS = ("diagram", "unknown")       # 이 영역들에서 심볼 후보를 찾는다

BOX_RULE = ("Inside the box: every stroke of the symbol body, including a gate's vertical input bar, the short rays "
            "around a lamp, and any letters or digits drawn inside the symbol. Outside the box: wires (connecting lines) "
            "leaving the symbol, and text labels next to it.")

S1_Q = ("In `page`, a red rectangle marks one region of an engineering drawing sheet, and `region` shows that region "
        "enlarged. What does the region contain?")
S1_CRITERIA = {
    "diagram": "A logic diagram: symbols such as gates, small boxes, circles, lamps and arrow-shaped connectors, joined by wire lines.",
    "table": "A table: ruled rows and columns of text, such as an equipment list.",
    "title_block": "The title block or revision block of the sheet: company names, drawing number, revision rows, signatures.",
    "notes": "Notes: lines of text such as numbered notes, with no symbols.",
    "module_box": "A switch or panel module drawn as stacked labelled boxes, not wired to the logic.",
    "title_text": "A single short title or heading line.",
    "other": "Something else: border marks, zone numbers, arrows, or an empty area.",
}
S2_Q = "`view` shows part of an engineering logic diagram. What is inside the red box?"
S2_CRITERIA = {
    "symbol": "Exactly one complete drawing symbol, for example a logic gate, a memory or timer box, an arrow-shaped connector, "
              "a lamp, a small input circle, a filled marker, or a large system block with a name inside.",
    "several_symbols": "Several separate symbols, or symbols together with the wires running between them.",
    "symbol_part": "Only part of one drawing symbol: the same symbol continues outside the red box.",
    "text": "Only text (letters or digits) that is not inside a symbol.",
    "table_cell": "A cell of a table (a ruled grid).",
    "wire_loop": "An empty area enclosed by wire lines and the sides of different symbols; it is not a symbol itself.",
    "other": "Something else, such as a junction dot, an arrow head, or a frame mark.",
}
C1_Q = ("`symbol` shows part of a control logic diagram. Which type is the drawing symbol inside the red box? "
        "Each option has a description and, when available, an example from the drawing legend.")
K3_Q = ("`pair_view` shows part of a control logic diagram with two symbols outlined: one in a red box and one in a blue box. "
        "Are these two symbols wired to each other? Follow the drawn lines from one box to the other without passing through "
        "any other symbol. Lines that meet at a dot are joined. Where two lines cross and one of them is broken by a small gap, "
        "they are not joined: the broken line just continues across.")
K3_TRUE = "A continuous path of drawn lines leads from the red box to the blue box."
K3_FALSE = ("There is no such path: the lines leaving one box end, lead to other symbols, or only cross the other box's lines "
            "at a broken crossing.")
B6_Q = ("`box_1` and `box_2` show the same part of a control logic diagram, each with a different red box around one drawing "
        "symbol. Which red box encloses the whole symbol body more exactly? The symbol body includes a gate's vertical input "
        "bar (also where it sticks out above or below the gate), the short rays around a lamp, and letters inside the symbol. "
        "It does not include wires leaving the symbol or text labels next to it.")
B6_CRITERIA = {"1": "The red box in `box_1` fits the whole symbol body more exactly.",
               "2": "The red box in `box_2` fits the whole symbol body more exactly."}
T1_Q = "`view` shows part of a control logic diagram. What is inside the red box?"
T1_CRITERIA = {
    "text": "One block of text: a word, a number, a tag, or several lines that belong together. Letters or digits written "
            "inside a symbol (such as S and R in memory cells, the number in an arrow-shaped connector, or a system name) count as text.",
    "text_part": "Only part of a text block: the same word or line continues outside the red box.",
    "several_texts": "Several separate pieces of text that do not belong together.",
    "not_text": "Not text: a piece of a line, a dot, part of a symbol outline, or another mark that is not a letter or digit.",
}

# ---- S0: what kind of drawing (decides the question set, the legend and the line handling below)
S0_Q = "`page` shows a whole engineering drawing sheet, shrunk to fit. What kind of drawing is it?"
S0_CRITERIA = {
    "logic": "A control logic diagram: logic gates, timers, memory boxes, lamps and arrow-shaped connectors joined by thin signal lines.",
    "pid": "A piping and instrumentation diagram (P&ID): pipes with valves, instrument bubbles, pumps, tanks and other equipment.",
    "other": "Something else, such as a symbol legend, a cover sheet, a list or a page of text.",
}

# ---- P&ID question set (the logic-diagram questions above stay word for word, so their cached answers stay valid)
S1_CRITERIA_PID = {
    "diagram": "A piping and instrumentation diagram: pipes and signal lines with valves, instrument bubbles, switches, pumps, "
               "tanks or other equipment.",
    "table": S1_CRITERIA["table"],
    "title_block": S1_CRITERIA["title_block"],
    "notes": S1_CRITERIA["notes"],
    "title_text": S1_CRITERIA["title_text"],
    "other": S1_CRITERIA["other"],
}
S2_Q_PID = "`view` shows part of a piping and instrumentation diagram (P&ID). What is inside the red box?"
S2_CRITERIA_PID = {
    "symbol": "Exactly one complete drawing symbol, for example a valve (two triangles tip to tip), a valve actuator (a small circle "
              "with M, a filled dome or a spring), an instrument bubble, a hand switch, a tag circle or tag box, an arrow-shaped "
              "off-page connector, a diamond, a reducer, a flow arrow head, a pump, a tank or another piece of equipment.",
    "several_symbols": "Several separate symbols, or symbols together with the lines running between them.",
    "symbol_part": "Only part of one drawing symbol: the same symbol continues outside the red box (for example one triangle of a valve).",
    "text": "Only text (letters or digits) that is not inside a symbol.",
    "table_cell": "A cell of a table (a ruled grid).",
    "wire_loop": "An empty area enclosed by pipes or other lines and the sides of different symbols; it is not a symbol itself.",
    "other": "Something else, such as a junction dot, a pipe fitting mark, a revision cloud or a frame mark.",
}
B6_Q_PID = ("`box_1` and `box_2` show the same part of a piping and instrumentation diagram (P&ID), each with a different red box "
            "around one drawing symbol. Which red box encloses the whole symbol more exactly? The symbol includes all of its outline "
            "and the letters inside it. It does not include pipes or other lines leaving it, leader lines, other symbols attached to "
            "it (such as a valve's actuator on its stem), or text labels next to it.")
C1_Q_PID = ("`symbol` shows part of a piping and instrumentation diagram (P&ID). Which type is the drawing symbol inside the red box? "
            "Each option has a description and, when available, an example from another sheet of the same drawing set.")
K3_Q_PID = ("`pair_view` shows part of a piping and instrumentation diagram (P&ID) with two symbols outlined: one in a red box and one "
            "in a blue box. Are these two symbols joined by drawn lines? Follow the lines (solid pipes, dashed signal lines, or the "
            "leader line of a tag) from one box to the other without passing through any other symbol. Lines that meet at a dot or a "
            "corner are joined, and a pair of short bars across a pipe (a flange) does not break it. Where two lines cross and one of "
            "them is broken by a small gap, they are not joined: the broken line just continues across.")
# (2026-10-21, 2nd run) A longer wording that also named scope-boundary marks did not make Jev accept the pipes running past
# those marks, and it made two clear pairs inconsistent between the colour-swapped questions (0.94 / 0.21), so the first
# wording above is kept.
T2_Q_PID = ("`view` shows text in a piping and instrumentation diagram (P&ID). One line of text is in a red box and the line next to "
            "it is in a blue box. Do the two lines belong to one label?")
T2_TRUE_PID = ("They are one label: the two lines are read together as one tag or one name (for example the letters and the number of "
               "an instrument tag, the two lines written inside one symbol, or a destination name written on two lines).")
T2_FALSE_PID = ("They are two separate labels that only sit close together, each naming something different (for example a valve "
                "number and a pipe line number, a note reference and a line number, or a small marker next to a tag).")
K3_TRUE_PID = "A continuous path of drawn lines (solid or dashed) leads from the red box to the blue box."
K3_FALSE_PID = ("There is no such path: the lines leaving one box end, lead to other symbols, or only cross the other box's lines "
                "at a broken crossing.")
T1_Q_PID = "`view` shows part of a piping and instrumentation diagram (P&ID). What is inside the red box?"
T1_CRITERIA_PID = {
    "text": "One block of text: a word, a number, a tag (such as V0421, 042AC-1 or 9451-005), or several lines that belong together. "
            "Letters or digits written inside a symbol (such as HS 0421 in a switch, FT 33B in an instrument bubble, or the drawing "
            "number in an off-page connector) count as text.",
    "text_part": "Only part of a text block: the same word or line continues outside the red box.",
    "several_texts": "Several separate pieces of text that do not belong together.",
    "not_text": "Not text: a piece of a line, a dash of a dashed line, a dot, part of a symbol outline, or another mark that is not "
                "a letter or digit.",
    "notes_or_table": "Text of the sheet's notes, a table, the title block or the revision block, not a label in the diagram itself.",
}

# ---- per-kind settings. 'logic' is the original pipeline unchanged.
PROFILES = {
    "logic": {
        "label": "로직 다이어그램", "legend": "legend_cld.json",
        "s1": S1_CRITERIA, "s1_task": "Find the logic diagram on an engineering drawing sheet.",
        "s2_q": S2_Q, "s2": S2_CRITERIA, "s2_task": "Find the drawing symbols in a control logic diagram.",
        "b6_q": B6_Q, "b6_task": "Pick the box that encloses the whole drawing symbol.",
        "c1_q": C1_Q, "c1_task": "Classify drawing symbols using the drawing legend.",
        "k3_q": K3_Q, "k3_true": K3_TRUE, "k3_false": K3_FALSE,
        "k3_task": "Decide which symbols in a control logic diagram are wired together.",
        "t1_q": T1_Q, "t1": T1_CRITERIA, "t1_task": "Find the text in a control logic diagram.",
        "t2": None,
        "dashes": False,          # chain dashed lines into nets
        "mst_over": None,         # nets with more symbols than this ask K3 only about minimum-spanning-tree pairs
        "pair_up": 2.0,           # max upscale of the K3 view
        "container": "strict",    # S2: a candidate holding other candidates needs P(symbol) >= CONTAINER_SYMBOL
        "blob": None,             # solid_blobs limits (None: page_cv defaults)
        "text_loose": False,      # text_candidates in low-resolution mode (P&ID lettering)
        "erase_ext": True,        # wires: also erase the attached strokes found for B6 (a gate's input bar) even if B6 kept the outline
        "faint_wires": True,      # both sheet types can contain long light-gray wire branches
    },
    "pid": {
        "label": "P&ID", "legend": "legend_pid.json",
        "s1": S1_CRITERIA_PID, "s1_task": "Find the piping and instrumentation diagram on an engineering drawing sheet.",
        "s2_q": S2_Q_PID, "s2": S2_CRITERIA_PID, "s2_task": "Find the drawing symbols in a piping and instrumentation diagram.",
        "b6_q": B6_Q_PID, "b6_task": "Pick the box that encloses the whole drawing symbol.",
        "c1_q": C1_Q_PID, "c1_task": "Classify the drawing symbols of a piping and instrumentation diagram.",
        "k3_q": K3_Q_PID, "k3_true": K3_TRUE_PID, "k3_false": K3_FALSE_PID,
        "k3_task": "Decide which symbols in a piping and instrumentation diagram are joined by lines.",
        "t1_q": T1_Q_PID, "t1": T1_CRITERIA_PID, "t1_task": "Find the text labels in a piping and instrumentation diagram.",
        "t2": (T2_Q_PID, T2_TRUE_PID, T2_FALSE_PID),   # T2: do two stacked lines of a text block form one label (Noul)
        "dashes": True,
        "mst_over": 4,
        "pair_up": 3.0,
        "container": "top",       # S2: a candidate holding other candidates (a vessel, a pump) is kept when 'symbol' is the top answer
        "blob": (0.45, 3.2, 0.45),  # filled valves and arrow heads: min side, max side (x letter height), share of the box filled
        "text_loose": True,
        "erase_ext": False,       # (P&ID: the attached strokes are stems, leaders and pipe stubs, i.e. the connections themselves)
        "faint_wires": True,      # (P&ID: dashed signal lines are often drawn light gray)
    },
}
BLUE = (230, 80, 0)  # BGR
PURPLE = (190, 40, 150)  # BGR, text boxes


# ----------------------------------------------------------------------------- Jev wrapper (cache, chunking, log)

class Img:
    """PNG + content digest. The digest keys the response cache; one SDK Image per Img so a repeated image is sent once."""

    def __init__(self, arr):
        self.png = V.png_bytes(arr)
        self.sha = hashlib.sha256(self.png).hexdigest()[:24]
        self.h, self.w = arr.shape[:2]
        self.arr = arr
        self._sdk = None

    def sdk(self):
        if self._sdk is None:
            from typesafe_sdk import Image
            self._sdk = Image(self.png)
        return self._sdk

    @property
    def tokens(self):
        return self.w * self.h / PX_PER_TOKEN


def choice(instructions, criteria):
    return {"type": "choice", "instructions": instructions, "criteria": criteria}


def noul(instructions, true, false):
    return {"type": "noul", "instructions": instructions, "criteria": {"true": true, "false": false}}


def ordered(criteria, reverse):
    return dict(reversed(list(criteria.items()))) if reverse else dict(criteria)


def _img_tokens(obj):
    """Image tokens counted per reference: an image used by two questions is counted twice."""
    if isinstance(obj, Img):
        return obj.tokens
    if isinstance(obj, dict):
        return sum(_img_tokens(v) for v in obj.values())
    if isinstance(obj, (list, tuple)):
        return sum(_img_tokens(v) for v in obj)
    return 0.0


def est_tokens(obj):
    text = len(json.dumps(obj, default=lambda o: "", ensure_ascii=False)) / 4
    return 1.06 * _img_tokens(obj) + text          # 실측 대비 약 5% 낮게 나와 보정


def est_request(state, questions):
    """보수적으로: state(공통 이미지 포함)는 질문마다 다시 센다 (실측상 질문 수만큼 드는 것으로 보임)."""
    return len(questions) * est_tokens(state) + sum(est_tokens(q) for q in questions.values())


class TooBig(Exception):
    """Jev rejected the request as too long (400 max_tokens_exceeded)."""


def _to_sdk(obj):
    if isinstance(obj, Img):
        return obj.sdk()
    if isinstance(obj, dict):
        return {k: _to_sdk(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_to_sdk(v) for v in obj]
    return obj


def _sdk_question(q):
    from typesafe_sdk import Choice, Noul
    if q["type"] == "choice":
        return Choice(instructions=_to_sdk(q.get("instructions")), criteria=_to_sdk(q["criteria"]))
    return Noul(instructions=_to_sdk(q.get("instructions")), criteria=_to_sdk(q.get("criteria")))


def mean_dist(*ds):
    ds = [d for d in ds if d]
    if not ds:
        return None
    keys = sorted({k for d in ds for k in d})
    return {k: sum(d.get(k, 0.0) for d in ds) / len(ds) for k in keys}


def top(d):
    # Equal model probabilities must not change a label with Python hash seeds
    # or the option order in an independently cached A/B answer.
    return min(d, key=lambda key: (-d[key], key)) if d else None


def choice_conf(d):
    """TypeSafe's Choice confidence: (p_max - 1/n) / (1 - 1/n)."""
    if not d:
        return 0.0
    n = len(d)
    return max(0.0, (max(d.values()) - 1 / n) / (1 - 1 / n)) if n > 1 else 1.0


def rounded(d, k=4):
    return {key: round(v, k) for key, v in sorted(d.items(), key=lambda kv: -kv[1])} if d else None


class Jev:
    """One place for every Jev call: per-question response cache, token-limit chunking (split again on
    max_tokens_exceeded), concurrency limit, JSONL log, cost."""

    def __init__(self, model, concurrency=8, client=None, fake=None, cache_dir=None, log_path=None):
        self.model, self.client, self.fake = model, client, fake
        self.sem = asyncio.Semaphore(concurrency)
        self.cache_dir = None if fake is not None else cache_dir    # fake answers never go into the real cache
        self.log_path = log_path
        self.fatal = None
        self.served = None
        self.stats = {}                                              # tool -> counters
        self.ms = []

    def _count(self, tool, **kw):
        s = self.stats.setdefault(tool, {"requests": 0, "cached": 0, "errors": 0, "questions": 0, "tokens": 0})
        for k, v in kw.items():
            s[k] += v

    def total(self, key):
        return sum(s[key] for s in self.stats.values())

    def _qkey(self, state, question):
        """Questions are judged independently, so each answer is cached on its own (state + that question).
        Key order is kept (no sort_keys): the A and B questions differ only in the order of their options, and each must
        keep its own answer (with sorted keys both shared one cache entry, so a re-run averaged one answer with itself)."""
        blob = json.dumps({"v": 2, "model": self.model, "state": state, "question": question}, ensure_ascii=False,
                          default=lambda o: "img:" + o.sha if isinstance(o, Img) else str(o))
        return hashlib.sha256(blob.encode()).hexdigest()

    def _cache_path(self, key):
        return self.cache_dir / self.model / key[:2] / f"{key}.json"

    def _log(self, rec):
        if self.log_path:
            with open(self.log_path, "a") as f:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    async def ask(self, tool, state, questions, meta=None):
        """All uncached questions in one request. Returns {name: probabilities (choice) | P(yes) (noul)} (cached
        answers included), or None on failure. Raises TooBig when Jev says the request is too long."""
        if self.fatal:
            raise Fatal(self.fatal)
        answers, todo = {}, {}
        for name, q in questions.items():
            k = self._qkey(state, q) if self.cache_dir else None
            if k and self._cache_path(k).exists():
                answers[name] = json.loads(self._cache_path(k).read_text())["answer"]
            else:
                todo[name] = (q, k)
        if answers:
            self._count(tool, cached=len(answers))
        if not todo:
            return answers
        qs_plain = {n: q for n, (q, _) in todo.items()}
        est = round(est_request(state, qs_plain))
        if self.fake is not None:
            got = await self.fake.ask(tool, state, qs_plain, meta or {})
            self._count(tool, requests=1, questions=len(todo), tokens=est)
            return {**answers, **got}
        from typesafe_sdk import TypeSafeAPIError, TypeSafeError
        async with self.sem:
            if self.fatal:
                raise Fatal(self.fatal)
            st = _to_sdk(state)
            qs = {n: _sdk_question(q) for n, q in qs_plain.items()}
            t0 = time.perf_counter()
            try:
                resp = await self.client.system_one(state=st, questions=qs, model=self.model, extra_headers=IMAGES_ON)
            except TypeSafeAPIError as error:
                if error.status in FATAL:
                    self.fatal = f"{error.status} — {FATAL[error.status]} (request_id={error.request_id})"
                    raise Fatal(self.fatal) from error
                if error.status == 400 and "max_tokens" in str(error):
                    self._log({"tool": tool, "questions": len(todo), "est": est, "too_big": True})
                    raise TooBig(str(error)) from error
                self._count(tool, errors=1)
                self._log({"tool": tool, "questions": len(todo), "est": est, "error": f"{error.status} {error}"[:300]})
                return answers or None
            except TypeSafeError as error:
                self._count(tool, errors=1)
                self._log({"tool": tool, "questions": len(todo), "est": est, "error": str(error)[:300]})
                return answers or None
            ms = round((time.perf_counter() - t0) * 1000)
        self.served = self.served or resp.model
        got = {}
        for name, a in resp.choices.items():
            got[name] = dict(a.probabilities)
        for name, a in resp.nouls.items():
            got[name] = float(a.noul)
        tokens = resp.usage.input_tokens or 0
        self.ms.append(ms)
        self._count(tool, requests=1, questions=len(todo), tokens=tokens)
        self._log({"tool": tool, "questions": len(todo), "tokens": tokens, "est": est, "ms": ms, "model": resp.model})
        if self.cache_dir:
            for name, (q, k) in todo.items():
                if name in got:
                    p = self._cache_path(k)
                    p.parent.mkdir(parents=True, exist_ok=True)
                    p.write_text(json.dumps({"model": resp.model, "answer": got[name]}))
        return {**answers, **got}

    async def _ask_split(self, tool, state, questions, meta):
        try:
            return await self.ask(tool, state, questions, meta) or {}
        except TooBig:
            names = list(questions)
            if len(names) == 1:
                self._count(tool, errors=1)
                self._log({"tool": tool, "question": names[0], "error": "single question exceeds Jev's token limit"})
                return {}
            pairs = {}
            for n in names:
                pairs.setdefault(n.rsplit("_", 1)[0], []).append(n)
            groups = list(pairs.values())
            if len(groups) > 1:                                      # split between A/B pairs first
                half = len(groups) // 2
                first = [n for g in groups[:half] for n in g]
            else:
                first = names[: len(names) // 2]
            second = [n for n in names if n not in first]
            a, b = await asyncio.gather(self._ask_split(tool, state, {n: questions[n] for n in first}, meta),
                                        self._ask_split(tool, state, {n: questions[n] for n in second}, meta))
            return {**a, **b}

    async def ask_chunked(self, tool, state, questions, meta=None):
        """Split into requests under REQ_TOKENS (estimated). Questions sharing a prefix before the last '_'
        (an A/B pair) stay together. A request Jev still finds too long is halved and sent again."""
        groups = {}
        for name, q in questions.items():
            groups.setdefault(name.rsplit("_", 1)[0], {})[name] = q
        chunks, cur = [], {}
        for g in groups.values():
            if cur and est_request(state, {**cur, **g}) > REQ_TOKENS:
                chunks.append(cur)
                cur = {}
            cur.update(g)
        if cur:
            chunks.append(cur)
        meta = meta or {}
        results = await asyncio.gather(*(self._ask_split(tool, state, c, {k: meta.get(k) for k in c}) for c in chunks))
        out = {}
        for r in results:
            out.update(r or {})
        return out


# ----------------------------------------------------------------------------- views

class ScaledView(V.View):
    """View at an explicit scale. When shrinking, dark lines are thickened first so 1-px wires survive the downscale."""

    def __init__(self, page, rect, s):
        self.rect = tuple(int(round(v)) for v in rect)
        x0, y0, x1, y1 = self.rect
        g = V.crop(page, x0, y0, x1, y1)
        if s < 0.75:
            k = max(2, int(round(1 / s)))
            g = cv2.erode(g, np.ones((k, k), np.uint8))
        self.s = s
        size = (max(1, round((x1 - x0) * s)), max(1, round((y1 - y0) * s)))
        g = cv2.resize(g, size, interpolation=cv2.INTER_AREA if s < 1 else cv2.INTER_CUBIC)
        self.img = cv2.cvtColor(g, cv2.COLOR_GRAY2BGR)


def fit_scale(w, h, max_side, min_side=V.JEV_MIN_SIDE, up=3.0):
    s = min(max_side / max(w, h), up)
    if min(w, h) * s < min_side:
        s = min(min_side / min(w, h), V.JEV_MAX_SIDE / max(w, h), up * 2)
    return min(s, (V.JEV_MAX_PIXELS * 0.95 / (w * h)) ** 0.5)


def region_views(page, b):
    H, W = page.shape[:2]
    s = 1024 / max(W, H)
    ov = cv2.resize(page, (round(W * s), round(H * s)), interpolation=cv2.INTER_AREA)
    ov = cv2.cvtColor(ov, cv2.COLOR_GRAY2BGR)
    cv2.rectangle(ov, (int(b[0] * s) - 4, int(b[1] * s) - 4), (int(b[2] * s) + 4, int(b[3] * s) + 4), V.RED, 3)
    m = 24
    rect = (b[0] - m, b[1] - m, b[2] + m + 1, b[3] + m + 1)
    v = ScaledView(page, rect, fit_scale(rect[2] - rect[0], rect[3] - rect[1], 1024))
    return ov, v.finish()


def candidate_view(page, b):
    w, h = V.wh(b)
    m = int(V.clamp(0.6 * max(w, h), 30, 200))
    v = V.View(page, (b[0] - m, b[1] - m, b[2] + m + 1, b[3] + m + 1))
    v.box(b, V.RED, 3)
    return v.finish()


def symbol_view(page, b):
    w, h = V.wh(b)
    m = int(V.clamp(0.35 * max(w, h), 40, 120))                     # 작은 심볼은 주변(선, 태그 글자)도 보이게
    v = V.View(page, (b[0] - m, b[1] - m, b[2] + m + 1, b[3] + m + 1))
    v.box(padded(b), V.RED, 2)
    return v.finish()


def padded(b, p=3):
    """Draw boxes a few pixels outside the symbol so the red line never hides a stroke (e.g. a gate's input bar)."""
    return (b[0] - p, b[1] - p, b[2] + p, b[3] + p)


def text_view(page, b):
    w, h = V.wh(b)
    m = int(V.clamp(0.6 * max(w, h), 24, 120))
    v = V.View(page, (b[0] - m, b[1] - m, b[2] + m + 1, b[3] + m + 1))
    v.box(padded(b, 2), V.RED, 2)
    return v.finish()


def compare_views(page, boxes):
    """Same crop for every box (so the only difference is the red box): one image per box."""
    x0, y0 = min(b[0] for b in boxes), min(b[1] for b in boxes)
    x1, y1 = max(b[2] for b in boxes), max(b[3] for b in boxes)
    m = int(V.clamp(0.5 * max(x1 - x0 + 1, y1 - y0 + 1), 20, 120))
    out = []
    for b in boxes:
        v = V.View(page, (x0 - m, y0 - m, x1 + m + 1, y1 + m + 1))
        v.box(padded(b), V.RED, 2)
        out.append(v.finish())
    return out


def pair_view(page, a, b, path, a_color, b_color, up=2.0):
    xs = [a[0], a[2], b[0], b[2]] + [p[0] for p in path or []]
    ys = [a[1], a[3], b[1], b[3]] + [p[1] for p in path or []]
    m = 36
    rect = (min(xs) - m, min(ys) - m, max(xs) + m + 1, max(ys) + m + 1)
    v = ScaledView(page, rect, fit_scale(rect[2] - rect[0], rect[3] - rect[1], 1280, up=up))
    t = max(2, int(round(3 / max(v.s, 0.5))))
    v.box(padded(a), a_color, t)
    v.box(padded(b), b_color, t)
    return v.finish()


def exemplar_view(page, crop, max_side=448):
    x0, y0, x1, y1 = crop
    c = page[y0:y1 + 1, x0:x1 + 1]
    h, w = c.shape[:2]
    s = min(max_side / max(w, h), 4.0)
    c = cv2.resize(c, (round(w * s), round(h * s)), interpolation=cv2.INTER_CUBIC if s > 1 else cv2.INTER_AREA)
    h, w = c.shape[:2]
    H, W = max(h, V.JEV_MIN_SIDE), max(w, V.JEV_MIN_SIDE)
    out = np.full((H, W), 255, np.uint8)
    out[(H - h) // 2:(H - h) // 2 + h, (W - w) // 2:(W - w) // 2 + w] = c
    return cv2.cvtColor(out, cv2.COLOR_GRAY2BGR)


def direction_q(edge, img, reverse, key):
    """Same wording as p0_bench.direction_q (framing='candidate'), as a cacheable dict."""
    out, inward, side, beyond, orient = WORDS[edge]
    criteria = {
        out: f"Some stroke of the symbol body (not a wire) is {beyond} the red line, or the red line cuts through the symbol.",
        "keep": f"The red line touches the {side} stroke of the symbol body or leaves only a hair-thin gap; "
                f"no part of the symbol body is {beyond} it.",
        inward: f"There is clear space (white, or only wires) between the red line and the {side} stroke of the symbol body.",
    }
    lead = f"In `{key}`, the thick red {orient} line is a possible {edge.upper()} edge of the box around the symbol in `context`."
    return choice({key: img, "question": f"{lead} Compare it with the {side} stroke of the symbol body. Ignore wires and text labels."},
                  ordered(criteria, reverse))


# ----------------------------------------------------------------------------- stages

class Ctx:
    def __init__(self, page, bw, jev, kind="logic", tables=(), text_h=18, frame_box=None):
        self.page, self.bw, self.jev = page, bw, jev
        self.tables = [tuple(t) for t in tables]                   # ruled tables: never searched for symbols, text or wires
        self.text_h = text_h
        self.frame_box = frame_box
        self.set_kind(kind)

    def set_kind(self, kind):
        self.kind = kind
        self.k = PROFILES[kind]
        self.bw_wire = (self.bw | CV.faint_lines(self.page)) if self.k["faint_wires"] else self.bw
        if self.frame_box is not None and self.k["faint_wires"]:
            x0, y0, x1, y1 = self.frame_box
            allowed = np.zeros_like(self.bw)
            allowed[y0:y1+1, x0:x1+1] = 1
            self.bw_wire &= allowed
        b = self.k["blob"]
        self.blob = None if b is None else {"min_side": max(4, round(b[0] * self.text_h)), "max_side": round(b[1] * self.text_h),
                                            "fill": b[2]}
        self.equipment_proposals = []


def page_view(page, max_side=1024):
    """The whole sheet shrunk to `max_side` (lines thickened first so they survive the shrink)."""
    H, W = page.shape[:2]
    return ScaledView(page, (0, 0, W, H), max_side / max(W, H)).finish()


def guess_kind(text_h):
    """Fallback only (S0 unanswered, or --dry-run): P&ID sheets in this set are drawn at half the letter height of the logic sheets."""
    return "pid" if text_h <= 12 else "logic"


async def stage_kind(ctx, text_h):
    """0. 도면 종류 → S0. 'other'(범례·표지 등)는 로직 다이어그램 방식으로 처리한다."""
    img = Img(page_view(ctx.page))
    qs = {f"k_{tag}": choice({"page": img, "question": S0_Q}, ordered(S0_CRITERIA, rev)) for tag, rev in (("A", False), ("B", True))}
    ans = await ctx.jev.ask_chunked("S0_kind", {"task": "Tell what kind of engineering drawing a sheet is."}, qs)
    probs = mean_dist(ans.get("k_A"), ans.get("k_B"))
    info = {"probs": rounded(probs), "text_height": text_h}
    if probs is None:
        info["kind"], info["note"] = guess_kind(text_h), "S0 gave no answer; guessed from the letter height"
    else:
        info["answer"] = top(probs)
        info["kind"] = "pid" if info["answer"] == "pid" else "logic"
        if info["answer"] == "other":
            info["note"] = "S0 said neither; using the logic-diagram questions"
    if DK.needs_review(probs):
        regions = DK.select_review_crops(ctx.bw, exclude=ctx.tables, frame=ctx.frame_box)
        review_qs, review_meta = {}, {}
        for r in regions:
            ov, cr = region_views(ctx.page, r["bbox"])
            state = {"page": Img(ov), "region": Img(cr), "question": DK.REVIEW_QUESTION}
            for tag, rev in (("A", False), ("B", True)):
                name = f"{r['id']}_{tag}"
                review_qs[name] = choice(state, ordered(S0_CRITERIA, rev))
                review_meta[name] = {"bbox": r["bbox"]}
        got = await ctx.jev.ask_chunked("S0_content_review", {"task": "Identify the drawing kind from broad original content."},
                                        review_qs, review_meta) if review_qs else {}
        reviews = [{**r, "A": got.get(f"{r['id']}_A"), "B": got.get(f"{r['id']}_B")} for r in regions]
        decision = DK.resolve_review(probs, reviews)
        info["content_review"] = {**decision, "regions": reviews}
        if decision["answer"] in ("logic", "pid") and (decision["changed"] or probs is None):
            info["answer_before_review"] = info.get("answer")
            info["answer"], info["kind"] = decision["answer"], decision["answer"]
            info["note"] = decision["reason"]
    return info


async def stage_regions(ctx):
    """1. 영역 (코드) → S1."""
    boxes = CV.layout_regions(ctx.bw)
    info, qs, meta = [], {}, {}
    for i, b in enumerate(boxes):
        r = {"id": f"R{i + 1}", "bbox": list(b), "kind": None, "probs": None}
        info.append(r)
        if max(b[2] - b[0], b[3] - b[1]) + 1 < MIN_REGION_SIDE:
            r["kind"], r["note"] = "other", "small region, not asked"
            continue
        if any(CV.contains(t, b, 4) for t in ctx.tables):
            r["kind"], r["note"] = "table", "ruled table found by code, not asked"
            continue
        ov, cr = region_views(ctx.page, b)
        i_ov, i_cr = Img(ov), Img(cr)
        for tag, rev in (("A", False), ("B", True)):
            qs[f"{r['id']}_{tag}"] = choice({"page": i_ov, "region": i_cr, "question": S1_Q}, ordered(ctx.k["s1"], rev))
            meta[f"{r['id']}_{tag}"] = {"bbox": b}
    ans = await ctx.jev.ask_chunked("S1_region", {"task": ctx.k["s1_task"]}, qs, meta) if qs else {}
    for r in info:
        if r["kind"]:
            continue
        probs = mean_dist(ans.get(f"{r['id']}_A"), ans.get(f"{r['id']}_B"))
        r["probs"] = rounded(probs)
        if probs:
            r["kind"] = top(probs)
        else:
            r["kind"], r["note"] = "unknown", "S1 gave no answer; searched anyway (S2 filters the candidates)"
    if info and not any(r["kind"] in SEARCH_KINDS for r in info):
        best = max(info, key=lambda r: CV.area(r["bbox"]))        # 판정이 모두 다이어그램이 아니면 가장 큰 영역
        best["note"] = f"no region was judged a diagram; searching the largest one (S1 said {best['kind']})"
        best["kind"] = "diagram"
    return info


def geometry_candidates(ctx, diag_boxes):
    """One raw-geometry path for live evaluation and offline cost previews."""
    boxes = SG.propose(ctx.bw, diag_boxes, exclude=ctx.tables, profile_kind=ctx.kind, blob=ctx.blob)
    boxes = LG.propose(ctx.bw, diag_boxes, exclude=ctx.tables, boxes=boxes, profile_kind=ctx.kind)
    boxes, arrow_metadata = AG.propose(ctx.bw, diag_boxes, exclude=ctx.tables, boxes=boxes, profile_kind=ctx.kind)
    if ctx.kind == "logic":
        arrow_metadata = {tuple(shape["bbox"]): shape for shape in
                          AG.detect(ctx.bw, diag_boxes, exclude=ctx.tables, profile_kind="pid")
                          if tuple(shape["bbox"]) in boxes}
    ctx.equipment_proposals = EG.detect(ctx.bw, diag_boxes, exclude=ctx.tables, profile_kind=ctx.kind)
    geometry = {tuple(item["bbox"]): item for item in ctx.equipment_proposals}
    boxes = sorted(set(tuple(b) for b in boxes) | set(geometry), key=lambda b: (b[1], b[0], b[3], b[2]))
    return boxes, geometry, arrow_metadata


async def stage_candidates(ctx, diag_boxes):
    """2. 후보 (코드) → S2."""
    boxes, geometry, arrow_metadata = geometry_candidates(ctx, diag_boxes)
    cands, qs, meta = [], {}, {}
    for i, b in enumerate(boxes):
        c = {"id": f"c{i + 1}", "bbox": list(b)}
        if b in geometry:
            c["equipment_geometry"] = geometry[b]
        if b in arrow_metadata:
            c["shape_proposal"] = arrow_metadata[b]
        cands.append(c)
        img = Img(candidate_view(ctx.page, b))
        for tag, rev in (("A", False), ("B", True)):
            qs[f"{c['id']}_{tag}"] = choice({"view": img, "question": ctx.k["s2_q"]}, ordered(ctx.k["s2"], rev))
            meta[f"{c['id']}_{tag}"] = {"bbox": b}
    ans = await ctx.jev.ask_chunked("S2_candidate", {"task": ctx.k["s2_task"]}, qs, meta) if qs else {}
    for c in cands:
        probs = mean_dist(ans.get(f"{c['id']}_A"), ans.get(f"{c['id']}_B"))
        c["probs"] = rounded(probs)
        inner = [d["id"] for d in cands if d is not c and CV.contains(c["bbox"], d["bbox"])]
        if inner:
            c["contains"] = inner
        if probs is None:
            c["kind"], c["keep"] = "unknown", not inner              # 답이 없으면 버리지 않고 다음 단계로 (다른 후보를 품은 것은 제외)
        else:
            c["kind"] = top(probs)
            c["keep"] = probs.get("symbol", 0) + probs.get("symbol_part", 0) >= KEEP_SYMBOL
            sure = probs.get("symbol", 0) >= CONTAINER_SYMBOL or (ctx.k["container"] == "top" and c["kind"] == "symbol")
            if inner and not sure:
                c["keep"], c["note"] = False, "contains other candidates and S2 is not sure it is one symbol"
    return cands


async def stage_fit(ctx, cands):
    """3. bbox 맞춤: 코드가 윤곽선 박스와 붙은 획까지 넓힌 박스를 만들고, 둘이 다르면 Jev B6가 고른다
    (두 이미지의 순서를 바꿔 두 번 묻고 평균). 넓힌 박스는 고르지 않더라도 선 추적에서 지울 영역으로 쓴다."""
    keep = [c for c in cands if c["keep"]]
    boxes = [tuple(c["bbox"]) for c in keep]
    objs, qs, meta = [], {}, {}
    for k, c in enumerate(keep):
        start = tuple(c["bbox"])
        ext, _ = CV.attached_extent(ctx.bw, start, boxes)
        ext = SG.protected_extent(ctx.bw, start, ext, boxes, profile_kind=ctx.kind)
        ext = LG.attached_extent(ctx.bw, start, ext, boxes, profile_kind=ctx.kind)
        if c.get("equipment_geometry") or c.get("shape_proposal"):
            ext = start       # the verified closed silhouette already contains its attached body cells
        o = {"cand": c["id"], "start_bbox": list(start), "ext_bbox": list(ext), "bbox": list(start), "rounds": [],
             "confidence": (c.get("probs") or {}).get("symbol"), "s2": c.get("probs")}
        if c.get("equipment_geometry"):
            o["equipment_geometry"] = c["equipment_geometry"]
        if c.get("shape_proposal"):
            o["shape_proposal"] = c["shape_proposal"]
        objs.append(o)
        if max(abs(a - b) for a, b in zip(start, ext)) < 2:
            continue                                                 # 붙은 획이 없음: 물을 것이 없다
        i_start, i_ext = (Img(v) for v in compare_views(ctx.page, [start, ext]))
        qs[f"f{k}_A"] = choice({"box_1": i_start, "box_2": i_ext, "question": ctx.k["b6_q"]}, B6_CRITERIA)
        qs[f"f{k}_B"] = choice({"box_1": i_ext, "box_2": i_start, "question": ctx.k["b6_q"]}, B6_CRITERIA)
        meta[f"f{k}_A"] = {"boxes": [start, ext]}
        meta[f"f{k}_B"] = {"boxes": [ext, start]}
    ans = await ctx.jev.ask_chunked("B6_fit", {"task": ctx.k["b6_task"]}, qs, meta) if qs else {}
    for k, o in enumerate(objs):
        a, b = ans.get(f"f{k}_A"), ans.get(f"f{k}_B")
        if f"f{k}_A" not in qs:
            continue
        ps = ([a.get("2", 0.0)] if a else []) + ([b.get("1", 0.0)] if b else [])
        if not ps:
            o["note"] = "B6 gave no answer; keeping the outline box"
            continue
        p_ext = sum(ps) / len(ps)
        o["p_ext"] = round(p_ext, 4)
        o["bbox"] = list(o["ext_bbox"]) if p_ext >= 0.5 else list(o["start_bbox"])
        o["confidence"] = round(max(p_ext, 1 - p_ext), 4)
    return objs


def make_judge(ctx):
    """3. bbox 조정: p0_refine.refine 이 부르는 judge. 후보 위치마다 변 하나짜리 뷰로 방향 질문(옵션 순서 2가지)."""
    async def judge(page, box, edge, positions):
        state = {"task": TASK, "box_rule": BOX_RULE, "context": Img(V.context_view(page, box))}
        qs, meta = {}, {}
        for i, p in enumerate(positions):
            key = f"cand{i + 1}_view"
            img = Img(V.edge_view(page, V.with_edge(box, edge, p), edge))
            for tag, rev in (("A", False), ("B", True)):
                qs[f"c{i + 1}_{tag}"] = direction_q(edge, img, rev, key)
                meta[f"c{i + 1}_{tag}"] = {"box": box, "edge": edge, "pos": p}
        ans = await ctx.jev.ask_chunked("B1_edge", state, qs, meta)
        if not ans:
            return None
        return [mean_dist(ans.get(f"c{i + 1}_A"), ans.get(f"c{i + 1}_B")) or {} for i in range(len(positions))]
    return judge


async def stage_refine(ctx, cands, refine=True):
    judge = make_judge(ctx)
    keep = [c for c in cands if c["keep"]]

    boxes = [tuple(c["bbox"]) for c in keep]

    async def one(c):
        start = tuple(c["bbox"])
        ext = CV.attached_extent(ctx.bw, start, boxes)[0]
        ext = SG.protected_extent(ctx.bw, start, ext, boxes, profile_kind=ctx.kind)
        ext = list(LG.attached_extent(ctx.bw, start, ext, boxes, profile_kind=ctx.kind))
        if c.get("equipment_geometry") or c.get("shape_proposal"):
            ext = list(start)
        evidence = {key: c[key] for key in ("equipment_geometry", "shape_proposal") if c.get(key)}
        if not refine:
            return {"cand": c["id"], "start_bbox": list(start), "ext_bbox": ext, "bbox": list(start), "confidence": None, "rounds": [], **evidence}
        box, conf, rounds = await R.refine(ctx.page, start, judge)
        return {"cand": c["id"], "start_bbox": list(start), "ext_bbox": ext, "bbox": [int(v) for v in box], "confidence": conf,
                "rounds": rounds, **evidence}
    return await asyncio.gather(*(one(c) for c in keep))


def iou(a, b):
    i = CV.inter(a, b)
    return i / float(CV.area(a) + CV.area(b) - i) if i else 0.0


def dedupe(objs, cands, bw=None):
    """4. 같은 심볼로 수렴한 박스는 하나만 (확신도 높은 쪽). '심볼 일부' 후보가 다른 박스 안에 들어가면 그것도 정리."""
    kind = {c["id"]: c.get("kind") for c in cands}
    order = sorted(objs, key=lambda o: -(o["confidence"] if o["confidence"] is not None else 1.0))
    kept = []
    for o in order:
        hit = None
        for k in kept:
            inside = CV.inter(o["bbox"], k["bbox"]) / max(1, CV.area(o["bbox"]))
            if AG.preserve_distinct_shape(o, k) or (bw is not None and
                    (AG.separates_existing_ink(bw, o, k) or AG.separates_existing_ink(bw, k, o))):
                continue
            # A newly proposed whole vessel and its old partial need their own
            # C1 judgment before same-class fragment removal. Small internal
            # instruments and coils must never disappear in this pre-class pass.
            if (bool(o.get("equipment_geometry", {}).get("routing_obstacle"))
                    != bool(k.get("equipment_geometry", {}).get("routing_obstacle"))):
                continue
            if iou(o["bbox"], k["bbox"]) >= DUP_IOU or (inside >= 0.9 and kind.get(o["cand"]) == "symbol_part"):
                hit = k
                break
        if hit:
            o["merged_into"] = hit["cand"]
        else:
            kept.append(o)
    return kept, [o for o in objs if "merged_into" in o]


def load_legend(name="legend_cld.json"):
    """C1 options: {class key: description, or {description, example image}}. Each example is cropped from the page named by
    the class ("page") or by the file ("legend_page")."""
    data = json.loads((HERE / name).read_text())
    pages, options = {}, {}
    for c in data["classes"]:
        if c.get("crop"):
            pname = c.get("page") or data["legend_page"]
            if pname not in pages:
                pages[pname] = V.load_page(ROOT / "image" / pname)
            options[c["key"]] = {"description": c["text"], "example": Img(exemplar_view(pages[pname], c["crop"]))}
        else:
            options[c["key"]] = c["text"]
    return options


async def stage_classify(ctx, objs, legend):
    """5. 분류 → C1."""
    qs, meta = {}, {}
    for k, o in enumerate(objs):
        img = Img(symbol_view(ctx.page, o["bbox"]))
        for tag, rev in (("A", False), ("B", True)):
            qs[f"o{k}_{tag}"] = choice({"symbol": img, "question": ctx.k["c1_q"]}, ordered(legend, rev))
            meta[f"o{k}_{tag}"] = {"bbox": o["bbox"]}
    ans = await ctx.jev.ask_chunked("C1_class", {"task": ctx.k["c1_task"]}, qs, meta) if qs else {}
    for k, o in enumerate(objs):
        probs = mean_dist(ans.get(f"o{k}_A"), ans.get(f"o{k}_B"))
        o["class_probs"] = rounded(probs)
        if not probs:
            o["class"], o["class_confidence"] = None, None
            continue
        sym = {key: v for key, v in probs.items() if key != "other"}
        s2 = o.get("s2") or {}
        # A high "symbol_part" probability establishes only a fragment. It must
        # not overrule C1's explicit "other" judgment as if it proved a whole
        # equipment body (repeated section hatching exposed this on a new page).
        s2_symbol = (s2.get("symbol", 0) if ctx.kind == "pid" else
                     s2.get("symbol", 0) + s2.get("symbol_part", 0)) if s2 else 0.0
        trust = KEEP_SYMBOL if ctx.kind == "pid" else S2_TRUST
        o["class"] = "other" if probs.get("other", 0) >= DROP_OTHER and s2_symbol < trust else top(sym)
        n = len(probs)
        selected_probability = probs.get(o["class"], 0)
        o["class_confidence"] = round(max(0., (selected_probability - 1/n) / (1 - 1/n)), 4) if n > 1 else 1.


def focused_symbol_view(page, box):
    """Enlarge only the selected body; surrounding context is shown separately."""
    x0, y0, x1, y1 = box
    crop = page[y0:y1+1, x0:x1+1]
    h, w = crop.shape[:2]
    scale = min(12., 448 / max(w, h))
    crop = cv2.resize(crop, (round(w*scale), round(h*scale)), interpolation=cv2.INTER_NEAREST)
    h, w = crop.shape[:2]
    out = np.full((max(280, h+24), max(280, w+24)), 255, np.uint8)
    out[(out.shape[0]-h)//2:(out.shape[0]-h)//2+h, (out.shape[1]-w)//2:(out.shape[1]-w)//2+w] = crop
    return cv2.cvtColor(out, cv2.COLOR_GRAY2BGR)


def paired_symbol_view(page, box, context_box, text_h):
    """Keep tiny ink unpainted; mark the selection with external corner brackets."""
    mx, my = max(5, round(.6*text_h)), max(8, round(1.3*text_h))
    rect = (context_box[0]-mx, context_box[1]-my,
            context_box[2]+mx+1, context_box[3]+my+1)
    v = ScaledView(page, rect, 10.0)
    # Nearest-neighbour enlargement preserves the taper of five-pixel bodies.
    raw = V.crop(page, *rect)
    v.img = cv2.cvtColor(cv2.resize(raw, (raw.shape[1]*10, raw.shape[0]*10),
                                  interpolation=cv2.INTER_NEAREST), cv2.COLOR_GRAY2BGR)
    x0, y0, x1, y1 = box[0]-2, box[1]-2, box[2]+2, box[3]+2
    for x, y, dx, dy in ((x0, y0, -1, -1), (x1, y0, 1, -1),
                         (x0, y1, -1, 1), (x1, y1, 1, 1)):
        cv2.line(v.img, v.p(x, y), v.p(x+dx*2, y), V.RED, 2)
        cv2.line(v.img, v.p(x, y), v.p(x, y+dy*2), V.RED, 2)
    return v.finish()


async def stage_recheck_classes(ctx, objs, legend):
    """Recheck ambiguous tiny bodies in an enlarged isolated view, keeping context.

    This is a second visual judgment, not a class assigned from geometry. Replace
    C1 only with a stronger paired answer; retain both distributions in the trace.
    """
    if ctx.kind == "pid":
        selected = [o for o in objs if (o.get("class") in {"reducer", "actuator/diaphragm", "letter_marker"}
                    or (o.get("shape_proposal") or {}).get("geometry") == "filled-taper-on-shaft")
                    and max(V.wh(o["bbox"])) <= 6*ctx.text_h
                    and (o.get("class_confidence") or 0) < .80]
    else:
        selected = [o for o in objs if o.get("start_bbox")
                    and CV.area(o["bbox"]) > 3*CV.area(o["start_bbox"])
                    and max(V.wh(o["start_bbox"])) <= 6*ctx.text_h
                    and (o.get("class_confidence") or 0) < .65]
    qs, meta = {}, {}
    for k, o in enumerate(selected):
        body_box = o["bbox"] if ctx.kind == "pid" else o["start_bbox"]
        state = {"body_detail": Img(focused_symbol_view(ctx.page, body_box)),
                 "context": Img(symbol_view(ctx.page, o["bbox"])),
                 "question": "Which legend class matches the selected symbol BODY in `body_detail`? "
                             "The detail contains only the selected body pixels enlarged. `context` shows its "
                             "location in the drawing; ignore other shapes outside the selected box. A reducer "
                             "is an outlined tapered pipe section with unequal ends; a diaphragm is a filled dome "
                             "on a valve stem; a letter marker is a small circle containing one letter. "
                             "Choose other if the selection contains only a fragment or several separate bodies."}
        if (o.get("shape_proposal") or {}).get("geometry") == "filled-taper-on-shaft":
            state["question"] += (" A flow arrow is a filled triangular tip on a thin shaft and may point in "
                                   "any direction. An outline valve has two opposed outline flanks meeting on "
                                   "its pipe, rather than a single filled tip.")
        if ctx.kind == "logic":
            b = tuple(body_box)
            near = (b[0]-ctx.text_h, b[1]-ctx.text_h, b[2]+ctx.text_h, b[3]+ctx.text_h)
            state["body_context"] = Img(paired_symbol_view(ctx.page, b, near, ctx.text_h))
            state["question"] = ("Which legend class matches the selected logic symbol BODY in body_detail? "
                                  "All views show the SAME selected symbol. context includes its complete finite input "
                                  "bars; body_detail enlarges the compact central body; body_context uses external red "
                                  "corner brackets to mark that compact body without painting over its internal marks. "
                                  "The attached finite bar belongs to the selected symbol even where body_detail crops "
                                  "it out. Use the compact body's outline and internal marks, together with the full "
                                  "context, to select one legend class. Classify one complete symbol including its "
                                  "bar, rather than the entire connected group.")
        pair = (o.get("shape_proposal") or {}).get("pair_geometry")
        if pair:
            pair_box = tuple(pair["context_bbox"])
            state["pair_context"] = Img(paired_symbol_view(ctx.page, o["bbox"], pair_box, ctx.text_h))
            state["question"] += (" In pair_context four red corner brackets OUTSIDE the ink mark the SAME "
                                   "selected body as body_detail. The dark body across the horizontal line is outside "
                                   "this selection. Classify only the selected body using its fill, taper and adjacent "
                                   "shaft. Decide whether it is one filled directional tip, an outlined valve with two "
                                   "flanks, a pipe mark, or other. Do not classify the two bodies together.")
        for tag, rev in (("A", False), ("B", True)):
            qs[f"u{k}_{tag}"] = choice(state, ordered(legend, rev))
            meta[f"u{k}_{tag}"] = {"bbox": o["bbox"]}
    ans = await ctx.jev.ask_chunked("C2_body_detail", {"task": "Classify one small engineering drawing symbol body."},
                                  qs, meta) if qs else {}
    for k, o in enumerate(selected):
        a, b = ans.get(f"u{k}_A"), ans.get(f"u{k}_B")
        probs = mean_dist(a, b) if valid_choice_distribution(a, legend) and valid_choice_distribution(b, legend) else None
        o["detail_class_probs"] = rounded(probs)
        o["detail_class_accepted"] = False
        if not probs:
            continue
        conf = choice_conf(probs)
        winner = top(probs)
        if top(a) == top(b) == winner and winner != "other" and conf >= .65 and conf >= (o.get("class_confidence") or 0) + .10:
            o["class_before_detail"] = o.get("class")
            o["class_probs_before_detail"] = o.get("class_probs")
            o["class"], o["class_probs"], o["class_confidence"] = winner, rounded(probs), round(conf, 4)
            o["detail_class_accepted"] = True


def valid_choice_distribution(value, options):
    """A detail recheck must contain normalized finite probabilities for the whole legend."""
    return isinstance(value, dict) and set(value) == set(options) and \
        all(type(p) in (int, float) and math.isfinite(p) and 0 <= p <= 1 for p in value.values()) and \
        abs(sum(value.values()) - 1) <= .02


async def stage_closed_box_classes(ctx, objs, legend):
    """Ask one additional full-legend question for ambiguous intact small boxes."""
    qs, meta, selected = {}, {}, []
    for o in objs:
        evidence = CD.recheck_evidence(ctx.page, ctx.bw, o, ctx.kind, ctx.text_h)
        if evidence is None:
            continue
        view = CD.detail_view(ctx.page, evidence)
        if view is None:
            continue
        k = len(selected)
        selected.append((o, evidence))
        state = {"detail": Img(view),
                 "context": Img(paired_symbol_view(ctx.page, evidence["body_bbox"], evidence["context_bbox"], ctx.text_h)),
                 "question": CD.BOX_QUESTION}
        for tag, rev in (("A", False), ("B", True)):
            qs[f"b{k}_{tag}"] = choice(state, ordered(legend, rev))
            meta[f"b{k}_{tag}"] = evidence
    ans = await ctx.jev.ask_chunked("C2_closed_box_detail", {"task": "Classify one small engineering drawing symbol body."},
                                  qs, meta) if qs else {}
    for k, (o, evidence) in enumerate(selected):
        a, b = ans.get(f"b{k}_A"), ans.get(f"b{k}_B")
        probs = mean_dist(a, b) if valid_choice_distribution(a, legend) and valid_choice_distribution(b, legend) else None
        o["closed_box_review"] = {"evidence": evidence, "class_probs": rounded(probs), "accepted": False}
        if not probs:
            continue
        conf, winner = choice_conf(probs), top(probs)
        if top(a) == top(b) == winner and winner != "other" and conf >= .65 and conf >= (o.get("class_confidence") or 0)+.10:
            o["closed_box_review"].update({"accepted": True, "previous_class": o.get("class"),
                                           "previous_probs": o.get("class_probs")})
            o["class"], o["class_probs"], o["class_confidence"] = winner, rounded(probs), round(conf, 4)


def erase_box(o, with_ext=True):
    """선 추적에서 지울 박스: 출력 bbox와 코드가 찾은 붙은 획 범위(ext_bbox)를 합친 박스 (with_ext=False면 출력 bbox만)."""
    b = o["bbox"]
    if not with_ext:
        return tuple(b)
    e = o.get("ext_bbox") or b
    return (min(b[0], e[0]), min(b[1], e[1]), max(b[2], e[2]), max(b[3], e[3]))


def mst_port_pairs(ports, lab=None, net=None, neighbours=0):
    """Minimum spanning tree over the symbols of one net, distance = length of the drawn route between their closest
    ports (straight-line distance if no route is found), so tree edges join neighbours along the pipe. Returns the port
    pairs of the tree edges. Used for big P&ID nets (a header with many branches) instead of every pair."""
    by_obj = {}
    for p in ports:
        by_obj.setdefault(p["obj"], []).append(p)
    objs = sorted(by_obj)
    route = {}
    if lab is not None and net is not None:
        D = CV.wire_dists(lab, net, [p["anchor"] for p in ports])
        for i, p in enumerate(ports):
            for j, q in enumerate(ports):
                if D[i][j] is not None:
                    route[(id(p), id(q))] = D[i][j]

    def dist(pq):
        p, q = pq
        r = route.get((id(p), id(q)))
        if r is not None:
            return r
        return 10 * ((p["anchor"][0] - q["anchor"][0]) ** 2 + (p["anchor"][1] - q["anchor"][1]) ** 2) ** 0.5

    def best(a, b):
        return min(((pa, pb) for pa in by_obj[a] for pb in by_obj[b]), key=dist)
    inside, edges = {objs[0]}, []
    while len(inside) < len(objs):
        a, b, pq = min(((a, b, best(a, b)) for a in inside for b in objs if b not in inside), key=lambda t: dist(t[2]))
        inside.add(b)
        edges.append(pq)
    # An inferred signal net may contain a spurious detected endpoint. A
    # rejected tree edge must not hide every alternate route to a real port.
    # These bounded nearest-neighbour pairs are questions, never acceptance.
    seen = {tuple(sorted((p['obj'], q['obj']))) for p,q in edges}
    for a in objs if neighbours else ():
        options = sorted(((dist(best(a,b)), b, best(a,b)) for b in objs if b != a),
                         key=lambda item: item[:2])
        for _, b, pq in options[:neighbours]:
            key = tuple(sorted((a,b)))
            if key not in seen:
                seen.add(key)
                edges.append(pq)
    return edges


def relation_candidates(ctx, objs, diag_boxes):
    """6a. 연결 후보 (코드): 박스를 지운 선 → net → 같은 net 위 심볼 쌍. 같은 쌍이 여러 번 나오면 경로가 짧은 것 하나.
    P&ID: 점선 신호선도 잇고, 심볼이 mst_over 개보다 많은 net은 최소 신장 트리의 쌍만 후보로 낸다 (net 번호로 묶어 보면 나머지 쌍도 이어진 것)."""
    boxes = [erase_box(o, ctx.k["erase_ext"]) for o in objs]       # 붙은 획(입력 바 등)은 박스 판정과 상관없이 선에서 뺀다 (로직 다이어그램)
    # Keep every original candidate and route. Inferred outlet tees only add
    # previously absent symbol pairs; they never replace a traced header path.
    def collect(nets, lab, tees):
        pairs = {}
        for net in nets:
            ps = net["ports"]
            n_obj = len({p["obj"] for p in ps})
            if ctx.k["mst_over"] and n_obj > ctx.k["mst_over"]:
                port_pairs = mst_port_pairs(ps, lab, net,
                                             neighbours=2 if net.get('signal_gap_proposals') else 0)
                net["mst"] = True
            else:
                port_pairs = [(ps[i], ps[j]) for i in range(len(ps)) for j in range(i + 1, len(ps))]
            for a, b in port_pairs:
                if a["obj"] == b["obj"]:
                    continue
                if a["obj"] > b["obj"]:
                    a, b = b, a
                path = CV.wire_path(lab, net, a["anchor"], b["anchor"])
                length = sum(abs(p[0] - q[0]) + abs(p[1] - q[1]) for p, q in zip(path, path[1:])) if path else 10 ** 9
                key = (a["obj"], b["obj"])
                cand = {"a": a["obj"], "a_side": a["side"], "a_point": a["point"], "b": b["obj"], "b_side": b["side"],
                        "b_point": b["point"], "net": net["id"], "path": path, "length": length, "bridges": len(net["bridges"]),
                        "dashed": net.get("dashed", False), "mst": net.get("mst", False)}
                cand["tee_gaps"] = [tee for tee in tees if CG.uses_bridge(path, tee["path"], ctx.bw_wire)]
                if net.get("signal_gap_proposals"):
                    cand["signal_gaps"] = [SIG.route_used_gap(gap, path, ctx.bw_wire)
                                           for gap in net["signal_gap_proposals"]
                                           if CG.uses_bridge(path, gap["path"], ctx.bw_wire)
                                           or gap.get("symbol") in {objs[a["obj"]]["id"], objs[b["obj"]]["id"]}]
                    cand["endpoint_contacts"] = {p["obj"]: p["inferred_port_gap"] for p in (a, b)
                                                  if p.get("inferred_port_gap")}
                if key not in pairs or length < pairs[key]["length"]:
                    if key in pairs:
                        cand["other_nets"] = sorted(set(pairs[key].get("other_nets", []) + [pairs[key]["net"]]))
                    pairs[key] = cand
        return pairs

    obstacle = EG.obstacle_mask(ctx.bw, ctx.equipment_proposals) if ctx.equipment_proposals else None
    guarded_mask = None
    if obstacle is not None and obstacle.any():
        guarded_mask = CV.wire_mask(ctx.bw_wire, boxes, diag_boxes, CV.ERASE, ctx.tables)
        guarded_mask[obstacle != 0] = 0
    base_nets, base_lab = CV.wire_nets(ctx.bw_wire, boxes, diag_boxes, exclude=ctx.tables,
                                     dashes=ctx.k["dashes"], wire_override=guarded_mask)
    pairs = collect(base_nets, base_lab, [])
    ctx.port_tee_proposals = []
    ctx.port_tee_pruned = []
    ctx.signal_gap_proposals = []
    if ctx.kind != "pid":
        raw_mask = CV.wire_mask(ctx.bw_wire, boxes, diag_boxes, CV.ERASE, ctx.tables)
        crossings = CV.find_bridges(raw_mask, base_lab)
        for cand in pairs.values():
            net = next(n for n in base_nets if n["id"] == cand["net"])
            cand["crossing_details"] = XG.checkpoints(raw_mask, cand["path"], net["bridges"],
                                                       crossings=crossings, labels=base_lab, text_h=ctx.text_h)
        return list(pairs.values()), base_nets
    _, proposals = PG.outlet_tee_wire_mask(ctx.bw_wire, boxes, diag_boxes, objs,
                                                 erase=CV.ERASE, exclude=ctx.tables, text_h=ctx.text_h)
    tees, removed = PG.prune_redundant_tees(proposals, base_lab, base_nets)
    ctx.port_tee_proposals, ctx.port_tee_pruned = tees, removed
    original_mask = CV.wire_mask(ctx.bw_wire, boxes, diag_boxes, CV.ERASE, ctx.tables)
    if obstacle is not None:
        original_mask[obstacle != 0] = 0
    appended_nets, remap = [], {}
    if tees:
        enhanced_mask = PG.apply_outlet_tees(original_mask, tees)
        if obstacle is not None:
            enhanced_mask[obstacle != 0] = 0
        enhanced_nets, enhanced_lab = CV.wire_nets(ctx.bw_wire, boxes, diag_boxes, exclude=ctx.tables,
                                                 dashes=ctx.k["dashes"], wire_override=enhanced_mask)
        enhanced = collect(enhanced_nets, enhanced_lab, tees)
        for key, cand in enhanced.items():
            if key in pairs or not cand.get("tee_gaps"):
                continue
            old_net = cand["net"]
            if old_net not in remap:
                new_net = len(base_nets) + len(appended_nets)
                remap[old_net] = new_net
                net = dict(next(n for n in enhanced_nets if n["id"] == old_net))
                net["id"], net["inferred_outlet_tee"] = new_net, True
                appended_nets.append(net)
            cand["net"] = remap[old_net]
            pairs[key] = cand
    proposals = SIG.propose(ctx.page, original_mask, objs, erase=CV.ERASE,
                            text_h=ctx.text_h, obstacles=obstacle, exclude=ctx.tables)
    ctx.signal_gap_proposals = proposals
    signal_nets = SIG.augment_nets(base_nets, base_lab, proposals, objs, gray=ctx.page)
    signal_pairs = collect(signal_nets, base_lab, [])
    signal_remap = {}
    for key, cand in signal_pairs.items():
        if key in pairs or not cand.get("signal_gaps"):
            continue
        old_net = cand["net"]
        if old_net not in signal_remap:
            new_net = len(base_nets) + len(appended_nets)
            signal_remap[old_net] = new_net
            net = dict(next(n for n in signal_nets if n["id"] == old_net))
            net["id"] = new_net
            appended_nets.append(net)
        cand["net"] = signal_remap[old_net]
        pairs[key] = cand
    return list(pairs.values()), base_nets + appended_nets


LOCAL_LINE_Q = (
    "In `route_detail`, the two coloured rings mark point A and point B on the original engineering drawing. "
    "Within this crop, can you follow the SAME drawn pipe, signal line, or tag leader from the centre of one ring "
    "to the other without going through the body of another symbol? Only the black or grey strokes count as lines; "
    "the coloured rings and A/B labels are location markers, not connections. Lines meeting at a T junction, dot "
    "or elbow are connected. A solid branch joining a common header is connected through the header. A pair of "
    "short flange bars does not break the pipe. A dashed signal line continues through its regular dash gaps. "
    "A crossing with a gap joins the two opposite arms of the gapped line, not the crossing line."
)


def route_detail_view(page, item, ca, cb):
    x0, y0, x1, y1 = item["bbox"]
    # Preserve line pixels: enlarge a bounded local crop, leave the route itself unpainted.
    v = ScaledView(page, (x0, y0, x1 + 1, y1 + 1), fit_scale(x1-x0+1, y1-y0+1, 768, up=6.0))
    keep_ink = item.get('marker_style') == 'legacy_markers_keep_original_ink'
    if keep_ink:
        raw=V.crop(page,x0,y0,x1+1,y1+1)
        raw=cv2.resize(raw,(v.img.shape[1],v.img.shape[0]),interpolation=cv2.INTER_NEAREST)
        original=cv2.cvtColor(raw,cv2.COLOR_GRAY2BGR)
        v.img=original.copy()
    if item.get("marker_style") == "external_blank_brackets":
        raw = V.crop(page, x0, y0, x1 + 1, y1 + 1)
        v.img = cv2.cvtColor(cv2.resize(raw, (v.img.shape[1], v.img.shape[0]),
                                       interpolation=cv2.INTER_NEAREST), cv2.COLOR_GRAY2BGR)
        for name, color in (("a", ca), ("b", cb)):
            for a, b in item["marker_brackets"][name]:
                cv2.line(v.img, v.p(*a), v.p(*b), color, max(1, round(v.s/3)), cv2.LINE_8)
        return v.finish()
    for p, color, label in ((item["a"], ca, "A"), (item["b"], cb, "B")):
        point = v.p(*p)
        radius = max(5, round(3*v.s))
        if item.get("kind") == "signal_gap":
            # Close anchor rings hide one-pixel elbows. External brackets keep
            # their centres unpainted, with enough context to see repeated dashes.
            dx = max(8, round(2*v.s))
            for side in (-1, 1):
                cv2.line(v.img, (point[0]+side*dx, point[1]-dx),
                         (point[0]+side*(dx+6), point[1]-dx), color, 2)
                cv2.line(v.img, (point[0]+side*dx, point[1]+dx),
                         (point[0]+side*(dx+6), point[1]+dx), color, 2)
            cv2.putText(v.img, label, (point[0]+dx+8, point[1]-dx-3),
                        cv2.FONT_HERSHEY_SIMPLEX, .65, color, 1, cv2.LINE_AA)
            continue
        cv2.circle(v.img, point, radius, color, max(1, round(v.s/2)), cv2.LINE_AA)
        cv2.putText(v.img, label, (point[0] + radius + 3, point[1] - radius - 2),
                    cv2.FONT_HERSHEY_SIMPLEX, .65, color, 1, cv2.LINE_AA)
    if keep_ink:
        v.img[raw<255]=original[raw<255]
    return v.finish()


def valid_noul_values(answers, names):
    """Only finite probabilities from actual model answers count toward a paired judgment."""
    return [answers[n] for n in names if type(answers.get(n)) in (int, float)
            and math.isfinite(answers[n]) and 0 <= answers[n] <= 1]


ENDPOINT_Q = (
    "In `endpoint_detail`, the rectangular box marks exactly one target symbol and the coloured ring marks "
    "a point on a proposed connecting line. Does the original black or grey pipe, dashed signal line, stem "
    "or tag leader at the CENTRE of that ring actually enter or touch the boxed symbol body? Follow the ink "
    "between the ring and the target, allowing regular dash gaps and flange marks. Mere proximity to the box "
    "does not count. Reject if it ends nearby, passes beside the target, crosses a broken crossing or reaches "
    "another symbol first. Coloured outlines are only markers and do not create a connection."
)


def endpoint_detail_view(page, box, point, box_color, point_color):
    x0, y0 = min(box[0], point[0])-20, min(box[1], point[1])-20
    x1, y1 = max(box[2], point[0])+21, max(box[3], point[1])+21
    v = ScaledView(page, (x0, y0, x1, y1), fit_scale(x1-x0, y1-y0, 768, up=6.0))
    v.box(padded(box, 2), box_color, max(1, round(1/v.s)))
    cv2.circle(v.img, v.p(*point), max(5, round(3*v.s)), point_color,
               max(1, round(v.s/2)), cv2.LINE_AA)
    return v.finish()


def contact_detail_view(page, detail, box_color, point_color):
    """A fresh bounded attachment view with the short original neck unpainted."""
    box, point = detail["bbox"], detail["point"]
    rect = (box[0]-20, box[1]-20, box[2]+21, box[3]+21)
    v = ScaledView(page, rect, fit_scale(rect[2]-rect[0], rect[3]-rect[1], 768, up=8.0))
    markers = detail.get('blank_markers')
    if markers:
        raw=V.crop(page,*rect)
        v.img=cv2.cvtColor(cv2.resize(raw,(v.img.shape[1],v.img.shape[0]),
                                       interpolation=cv2.INTER_NEAREST),cv2.COLOR_GRAY2BGR)
        for name,color in [('body',box_color),('point',point_color)]:
            for a,b in markers[name]:
                cv2.line(v.img,v.p(*a),v.p(*b),color,max(1,round(v.s/3)),cv2.LINE_8)
        return v.finish()
    restore_ink=detail.get('restore_original_contact_ink',False)
    if restore_ink:
        raw=V.crop(page,*rect)
        original=cv2.cvtColor(cv2.resize(raw,(v.img.shape[1],v.img.shape[0]),
                                          interpolation=cv2.INTER_NEAREST),cv2.COLOR_GRAY2BGR)
        protected=cv2.resize((cv2.dilate((raw<255).astype(np.uint8),np.ones((3,3),np.uint8))!=0).astype(np.uint8),
                             (v.img.shape[1],v.img.shape[0]),interpolation=cv2.INTER_NEAREST)!=0
        v.img=original.copy()
    v.box(padded(box, 4), box_color, 2)
    px, py = v.p(*point)
    # Off-stroke brackets indicate the point without obscuring the tiny neck.
    for direction in (-1, 1):
        cv2.line(v.img, (px+direction*8, py-8), (px+direction*14, py-8), point_color, 2)
        cv2.line(v.img, (px+direction*8, py+8), (px+direction*14, py+8), point_color, 2)
    if restore_ink:
        v.img[protected]=original[protected]
    return v.finish()


async def stage_verify(ctx, objs, rels):
    """Judge global CLD pairs; P&ID also judges raw-ink route checkpoints, with no painted connecting path.

    Local checks can recover clearly connected common-header branches that the global view rejects.
    Paths through a detected third symbol are excluded before judging. Missing/ambiguous local
    responses preserve the global decision and are recorded; an unanswered global check is not accepted.
    """
    qs, meta = {}, {}
    for k, r in enumerate(rels):
        a, b = erase_box(objs[r["a"]], ctx.k["erase_ext"]), erase_box(objs[r["b"]], ctx.k["erase_ext"])
        for tag, (ca, cb) in (("A", (V.RED, BLUE)), ("B", (BLUE, V.RED))):
            img = Img(pair_view(ctx.page, a, b, r["path"], ca, cb, up=ctx.k["pair_up"]))
            qs[f"p{k}_{tag}"] = noul({"pair_view": img, "question": ctx.k["k3_q"]}, ctx.k["k3_true"], ctx.k["k3_false"])
            meta[f"p{k}_{tag}"] = {"a": a, "b": b}
    ans = await ctx.jev.ask_chunked("K3_pair", {"task": ctx.k["k3_task"]}, qs, meta) if qs else {}
    for k, r in enumerate(rels):
        ps = valid_noul_values(ans, [f"p{k}_{t}" for t in ("A", "B")])
        r["k3"] = [round(p, 4) for p in ps]
        r["confidence"] = round(sum(ps) / len(ps), 4) if len(ps) == 2 else None
        r["accepted"] = r["confidence"] is not None and r["confidence"] >= ACCEPT_LINK
        r["decision"] = "global_pair" if len(ps) == 2 else "unanswered"
    # A long finite input bar can shrink a short output neck in the whole-pair
    # view. Ask once at the unchanged gate body, then require the usual local
    # route and both endpoint judges. The full exported box/net/path stay put.
    compact_qs, compact_meta, compact_pending = {}, {}, []
    if ctx.kind == 'logic':
        for k, r in enumerate(rels):
            if r['accepted'] or len(r.get('k3', [])) != 2 or min(r['k3']) < LOCAL_REJECT:
                continue
            for gate_index, other_index, path, side in (
                    (r['a'], r['b'], r.get('path'), r['a_side']),
                    (r['b'], r['a'], list(reversed(r.get('path') or [])), r['b_side'])):
                detail = LG.compact_gate_output_pair(ctx.bw, objs[gate_index], objs[other_index],
                                                     path, side, objs)
                if detail is None:
                    continue
                boxes = {gate_index: detail['gate_bbox'], other_index: detail['other_bbox']}
                r['compact_output_review'] = {**detail, 'gate': objs[gate_index]['id'],
                                               'a_bbox': list(boxes[r['a']]), 'b_bbox': list(boxes[r['b']])}
                for tag, (ca, cb) in (('A', (V.RED, BLUE)), ('B', (BLUE, V.RED))):
                    key = f'o{k}_{tag}'
                    compact_qs[key] = noul({'pair_view': Img(pair_view(ctx.page, boxes[r['a']], boxes[r['b']],
                                                                      r['path'], ca, cb, up=ctx.k['pair_up'])),
                                            'question': ctx.k['k3_q']}, ctx.k['k3_true'], ctx.k['k3_false'])
                    compact_meta[key] = r['compact_output_review']
                compact_pending.append((k, r))
                break
    compact_ans = await ctx.jev.ask_chunked('K3_compact_output', {'task': ctx.k['k3_task']},
                                            compact_qs, compact_meta) if compact_qs else {}
    for k, r in compact_pending:
        ps = valid_noul_values(compact_ans, [f'o{k}_{tag}' for tag in ('A', 'B')])
        r['compact_output_review']['p_yes'] = [round(p, 4) for p in ps]
        r['compact_output_review']['confirmed'] = len(ps) == 2 and min(ps) >= LOCAL_RECOVER
    local_rels = rels if ctx.kind == "pid" else [r for r in rels if not r["accepted"] and
                    (r.get("crossing_details") or r.get('compact_output_review', {}).get('confirmed'))]
    if not local_rels:
        return
    local, views, loc_meta = {}, {}, {}
    for k, r in enumerate(local_rels):
        blockers = CG.intervening_symbols(r.get("path"), objs, {r["a"], r["b"]})
        if blockers:
            r["accepted"], r["decision"] = False, "intervening_symbol"
            r["blockers"] = [objs[i]["id"] for i in blockers]
            continue
        r["checkpoint_keys"] = []
        turns = [point for gap in r.get("signal_gaps", [])
                 if gap.get("reason") == "raw_supported_dashed_elbow"
                 for point in gap.get("path", [])[1:-1]]
        details = CG.checkpoints(r.get("path"), max_span=max(100, round(ctx.text_h*20)),
                                 protected_turns=turns)
        details = [SIG.junction_gap_detail(ctx.page, detail, r.get('signal_gaps',[]),
                                          ctx.text_h, symbols=objs) or detail for detail in details]
        details = CG.partition_crossing_spans(details, r.get("crossing_details", []))
        for tee in r.get("tee_gaps", []):
            details.append({"path": tee["path"], "a": tee["gap_points"][0], "b": tee["gap_points"][1],
                            "bbox": tee["bbox"], "kind": "outlet_tee_gap"})
        for gap in r.get("signal_gaps", []):
            detail = SIG.review_detail(ctx.page, gap, ctx.text_h, symbols=objs)
            if detail:
                details.append(detail)
        for detail in details:
            key = hashlib.sha256(json.dumps(detail, sort_keys=True).encode()).hexdigest()[:16]
            r["checkpoint_keys"].append(key)
            if key in views:
                continue
            views[key] = detail
            for tag, (ca, cb) in (("A", (V.RED, BLUE)), ("B", (BLUE, V.RED))):
                local[f"l{key}_{tag}"] = noul({"route_detail": Img(route_detail_view(ctx.page, detail, ca, cb)),
                                             "question": ("The two pairs of coloured brackets mark points A and B "
                                                          "at their CENTRES on the unpainted original drawing. "
                                                          "Can you follow the SAME original pipe or dashed signal "
                                                          "line from A to B, allowing regular dash gaps, a drawn "
                                                          "elbow or flange bars? The surrounding symbol bodies "
                                                          "provide context; neither brackets nor labels create a "
                                                          "connection. Reject a nearby unrelated line or crossing "
                                                          "through a symbol body.") if detail.get("kind") == "signal_gap" else LOCAL_LINE_Q},
                                            "The two marked points are joined by a drawn line path in this crop.",
                                            "No such line path joins the marked points in this crop.")
                loc_meta[f"l{key}_{tag}"] = detail
    got = await ctx.jev.ask_chunked("K5_local_route", {"task": "Check one small drawn-line route in an engineering diagram."},
                                      local, loc_meta) if local else {}
    checkpoints = {}
    for key, detail in views.items():
        ps = valid_noul_values(got, [f"l{key}_{tag}" for tag in ("A", "B")])
        checkpoints[key] = {**detail, "p_yes": [round(p, 4) for p in ps],
                            "confidence": round(sum(ps)/len(ps), 4) if len(ps) == 2 else None}
    ctx.route_checkpoints = checkpoints
    # A single additional view may correct a demonstrably misplaced/obscuring
    # marker. Keep the original answer, route and threshold. Strong rejection
    # with correctly placed centres remains a veto, not a prompt to retry.
    anchor_qs, anchor_meta, replacements = {}, {}, {}
    for r in local_rels:
        if (r.get("accepted") and not (r.get('signal_gaps') or r.get('tee_gaps'))) \
                or len(r.get("k3", [])) != 2 or r.get("blockers"):
            continue
        old_keys = r.get("checkpoint_keys", [])
        if not old_keys or any(checkpoints[k]["confidence"] is None for k in old_keys):
            continue
        pending = {}
        for key in old_keys:
            old = checkpoints[key]
            if old["confidence"] >= LOCAL_RECOVER:
                continue
            detail = CG.anchored_checkpoint(ctx.page, old, ctx.text_h, symbols=objs)
            if detail is None or (old["confidence"] < LOCAL_REJECT
                                  and "white_marker_centre" not in detail["retry_reasons"]):
                pending = {}
                break
            pending[key] = detail
        if not pending:
            continue
        replacements[id(r)] = {}
        for old_key, detail in pending.items():
            key = hashlib.sha256(json.dumps(detail, sort_keys=True).encode()).hexdigest()[:16]
            replacements[id(r)][old_key] = key
            for tag, (ca, cb) in (("A", (V.RED, BLUE)), ("B", (BLUE, V.RED))):
                name = f"r{key}_{tag}"
                anchor_qs[name] = noul({"route_detail": Img(route_detail_view(ctx.page, detail, ca, cb)),
                                       "question": LOCAL_LINE_Q.replace("coloured rings", "coloured corner brackets")
                                                             .replace("centre of one ring", "centre of one bracket group")},
                                      "The two marked points are joined by a drawn line path in this crop.",
                                      "No such line path joins the marked points in this crop.")
                anchor_meta[name] = detail
    anchored = await ctx.jev.ask_chunked("K5_anchor_review", {"task": "Check one small drawn-line route in an engineering diagram."},
                                       anchor_qs, anchor_meta) if anchor_qs else {}
    for r in local_rels:
        changed = replacements.get(id(r))
        if not changed:
            continue
        r["initial_checkpoint_keys"] = list(r["checkpoint_keys"])
        r["anchor_review_keys"] = changed
        for old_key, key in changed.items():
            ps = valid_noul_values(anchored, [f"r{key}_{tag}" for tag in ("A", "B")])
            checkpoints[key] = {**anchor_meta[f"r{key}_A"], "rechecks": old_key,
                                "p_yes": [round(p, 4) for p in ps],
                                "confidence": round(sum(ps)/2, 4) if len(ps) == 2 else None}
        # Missing or contradictory fresh evidence cannot replace an old check.
        if all(checkpoints[key]["confidence"] is not None and
               checkpoints[key]["confidence"] >= LOCAL_RECOVER for key in changed.values()):
            r["checkpoint_keys"] = [changed.get(key, key) for key in r["checkpoint_keys"]]
    recover = []
    for r in local_rels:
        if r.get("decision") == "intervening_symbol":
            continue
        if not r.get("path") or len(r["path"]) < 2:
            r["route_status"] = "no_path"
            if r.get("tee_gaps") or r.get("signal_gaps"):
                r["accepted"], r["decision"] = False, "outlet_tee_no_path"
            continue
        checks = [checkpoints[key] for key in r.get("checkpoint_keys", [])]
        if r.get("tee_gaps") or r.get("signal_gaps"):
            # Inserted ink is a candidate only. Neither a high global score nor
            # an unanswered local crop can confirm an inferred branch.
            r["accepted"], r["decision"] = False, "inferred_gap_unconfirmed"
        values = [c["confidence"] for c in checks if c["confidence"] is not None]
        if not values or len(values) != len(checks):
            r["route_status"] = "unanswered" if checks else "no_path"
            continue
        weakest = min(values)
        r["local_confidence"] = weakest
        r["route_status"] = "checked"
        # Require every observed span/turn to be supported; one high pair score cannot hide a broken span.
        if weakest >= LOCAL_RECOVER:
            if r["accepted"]:
                r["decision"] = "global_pair_local_supported"
            elif len(r.get("k3", [])) == 2:
                recover.append(r)
        elif weakest < LOCAL_REJECT:
            r["accepted"], r["decision"] = False, "local_route_rejected"
            r["confidence"] = weakest
        else:
            r["decision"] = "global_pair_local_uncertain"

    # Local spans prove a route exists, but proximity-based ports may have picked
    # the wrong nearby symbol. Recover a rejected pair only when both actual
    # endpoints are independently supported in their original-image context.
    endpoint_qs, endpoint_meta = {}, {}
    for r in recover:
        r["endpoint_keys"] = []
        for index, point in ((r["a"], r["path"][0]), (r["b"], r["path"][-1])):
            box = erase_box(objs[index], ctx.k["erase_ext"])
            if r.get('compact_output_review', {}).get('confirmed'):
                box = r['compact_output_review']['a_bbox' if index == r['a'] else 'b_bbox']
            attachment = r.get("endpoint_contacts", {}).get(index)
            if attachment and attachment.get("body_contact"):
                point = attachment["body_contact"]
            detail = {"bbox": list(box), "point": list(point)}
            key = hashlib.sha256(json.dumps(detail, sort_keys=True).encode()).hexdigest()[:16]
            r["endpoint_keys"].append(key)
            for tag, (bc, pc) in (("A", (V.RED, BLUE)), ("B", (BLUE, V.RED))):
                name = f"e{key}_{tag}"
                if name in endpoint_qs:
                    continue
                endpoint_qs[name] = noul({"endpoint_detail": Img(endpoint_detail_view(ctx.page, box, point, bc, pc)),
                                          "question": ENDPOINT_Q},
                                         "The marked drawn line enters the target symbol.",
                                         "The marked line does not enter that symbol.")
                endpoint_meta[name] = detail
    endpoint_got = await ctx.jev.ask_chunked("K6_endpoint", {"task": "Check the attachment of one line to one symbol."},
                                           endpoint_qs, endpoint_meta) if endpoint_qs else {}
    endpoint_checks = {}
    for r in recover:
        values = []
        for key in r["endpoint_keys"]:
            ps = valid_noul_values(endpoint_got, [f"e{key}_{tag}" for tag in ("A", "B")])
            endpoint_checks[key] = {**endpoint_meta[f"e{key}_A"], "p_yes": [round(p, 4) for p in ps],
                                    "confidence": round(sum(ps)/2, 4) if len(ps) == 2 else None}
            values.append(endpoint_checks[key]["confidence"])
        if all(p is not None and p >= LOCAL_RECOVER for p in values):
            r["accepted"], r["decision"] = True, "local_route_with_endpoints"
            r["endpoint_confidence"] = min(values)
            r["confidence"] = min(r["local_confidence"], min(values))
            if r.get('compact_output_review', {}).get('confirmed'):
                r['confidence'] = min(r['confidence'], min(r['compact_output_review']['p_yes']))
        else:
            r["decision"] = "local_route_endpoint_unconfirmed"
            r["endpoint_confidence"] = min(p for p in values if p is not None) if any(p is not None for p in values) else None
    ctx.endpoint_checks = endpoint_checks
    # A rejected coarse attachment can receive fresh evidence only when raw
    # central-side ink identifies a different, finite body contact. The previous
    # answer remains in the trace; metadata alone never accepts a pair.
    retry, retry_meta, pending = {}, {}, []
    for r in recover:
        if r.get("accepted"):
            continue
        if not r.get("signal_gaps") and not any(str(objs[i].get("class", "")).startswith("instrument/")
                                                for i in (r["a"], r["b"])):
            continue
        new_keys = []
        for position,(index, point) in enumerate(((r["a"], r["path"][0]), (r["b"], r["path"][-1]))):
            old = endpoint_checks[r['endpoint_keys'][position]]['confidence']
            if old is not None and old >= LOCAL_RECOVER:
                new_keys.append(None)
                continue
            box = erase_box(objs[index], ctx.k["erase_ext"])
            detail = SIG.endpoint_contact(ctx.page, box, point, ctx.text_h)
            if detail is None:
                new_keys.append(None)
                continue
            markers=SIG.contact_markers(ctx.page,detail)
            if markers is None:
                # Crowded instrument labels may leave no complete blank
                # bracket groups. A fresh view can still preserve every
                # original pixel and its clear margin by clipping markers.
                # It requires the same actual paired endpoint verdict.
                detail['restore_original_contact_ink']=True
            else:
                detail['blank_markers']=markers
            key = hashlib.sha256(json.dumps(detail, sort_keys=True).encode()).hexdigest()[:16]
            new_keys.append(key)
            for tag, (bc, pc) in (("A", (V.RED, BLUE)), ("B", (BLUE, V.RED))):
                name = f"c{key}_{tag}"
                retry[name] = noul({"contact_detail": Img(contact_detail_view(ctx.page, detail, bc, pc)),
                                    "target_body": Img(focused_symbol_view(ctx.page, detail['bbox'])),
                                    "question": "target_body shows exactly the selected symbol body from the original image. "
                                                "contact_detail shows its unchanged surrounding drawing. Two pairs of "
                                                "short brackets indicate a point at their centre on the original "
                                                "line beside that body. Follow only the original black or grey ink: "
                                                "does this line actually enter the selected body, allowing regular "
                                                "dash gaps and flange marks? The markers do not create a connection."},
                                   "The original line enters the selected body.", "The line does not enter that body.")
                retry_meta[name] = detail
        if any(new_keys):
            pending.append((r, new_keys))
    fresh = await ctx.jev.ask_chunked("K6_contact_review", {"task": "Recheck a finite raw line attachment."},
                                     retry, retry_meta) if retry else {}
    for r, keys in pending:
        vals = []
        for old_key, key in zip(r["endpoint_keys"], keys):
            if key is None:
                vals.append(endpoint_checks[old_key]["confidence"])
                continue
            ps = valid_noul_values(fresh, [f"c{key}_{tag}" for tag in ("A", "B")])
            endpoint_checks[key] = {**retry_meta[f"c{key}_A"], "p_yes": [round(p, 4) for p in ps],
                                    "confidence": round(sum(ps)/2, 4) if len(ps) == 2 else None}
            vals.append(endpoint_checks[key]["confidence"])
        r["contact_review_keys"] = keys
        if len(vals) == 2 and all(v is not None and v >= LOCAL_RECOVER for v in vals):
            r["accepted"], r["decision"] = True, "local_route_with_contact_review"
            r["endpoint_confidence"] = min(vals)
            r["confidence"] = min(r["local_confidence"], min(vals))


def text_blocks(ctx, diag_boxes, sym_boxes):
    """Code proposal of text blocks for this kind of drawing (P&ID: low-resolution lettering, letters freed from symbol outlines)."""
    loose = ctx.k["text_loose"]
    return CV.text_candidates(ctx.bw, diag_boxes, exclude=ctx.tables, skip_dashes=ctx.k["dashes"], loose=loose,
                              free_from=[tuple(b) for b in sym_boxes] if loose else ())


async def stage_text(ctx, diag_boxes, symbols):
    """7. 텍스트: 코드가 글자 덩어리를 제안하고 Jev T1이 판정한다 (옵션 순서 2가지). '여러 덩어리'로 판정되면 줄 단위로 나눈다."""
    sym_boxes = [o["bbox"] for o in symbols]
    blocks = []
    for k, t in enumerate(text_blocks(ctx, diag_boxes, sym_boxes)):
        b = list(t["bbox"])
        if any(iou(b, sb) > 0.5 for sb in sym_boxes):
            continue                                                 # 이미 심볼로 잡힌 것
        blocks.append({"id": f"x{k + 1}", "bbox": b, "lines": [list(ln) for ln in t["lines"]], "chars": t["chars"],
                       "words": [[list(w) for w in ws] for ws in t.get("words", [])], "orient": t.get("orient", "h")})
    qs, meta = {}, {}
    for t in blocks:
        img = Img(text_view(ctx.page, t["bbox"]))
        for tag, rev in (("A", False), ("B", True)):
            qs[f"{t['id']}_{tag}"] = choice({"view": img, "question": ctx.k["t1_q"]}, ordered(ctx.k["t1"], rev))
            meta[f"{t['id']}_{tag}"] = {"bbox": t["bbox"]}
    ans = await ctx.jev.ask_chunked("T1_text", {"task": ctx.k["t1_task"]}, qs, meta) if qs else {}
    for t in blocks:
        probs = mean_dist(ans.get(f"{t['id']}_A"), ans.get(f"{t['id']}_B"))
        t["probs"] = rounded(probs)
        if probs is None:
            t["kind"], t["keep"], t["confidence"] = "unknown", True, None
        else:
            t["kind"] = top(probs)
            t["keep"] = probs.get("not_text", 0) < TEXT_DROP and probs.get("notes_or_table", 0) < TEXT_DROP
            t["confidence"] = round(1 - probs.get("not_text", 0), 4)
    groups = await stage_line_groups(ctx, [t for t in blocks if t["keep"] and len(t["lines"]) > 1]) if ctx.k["t2"] else {}
    texts = []
    for t in blocks:
        if not t["keep"]:
            continue
        if t["id"] in groups:                                        # T2 decided which stacked lines form one label
            gs = groups[t["id"]]
            if len(gs) == 1:
                texts.append(dict(t))
            for j, g in enumerate(gs if len(gs) > 1 else []):
                lines = [t["lines"][i] for i in g]
                bb = [min(ln[0] for ln in lines), min(ln[1] for ln in lines), max(ln[2] for ln in lines), max(ln[3] for ln in lines)]
                texts.append({**t, "id": f"{t['id']}.{j + 1}", "bbox": bb, "lines": lines, "split_from": t["id"]})
        elif t["kind"] == "several_texts" and len(t["lines"]) > 1:
            for j, ln in enumerate(t["lines"]):
                texts.append({**t, "id": f"{t['id']}.{j + 1}", "bbox": list(ln), "lines": [list(ln)], "split_from": t["id"]})
        elif t["kind"] == "several_texts" and t.get("words") and len(t["words"][0]) > 1:
            for j, w in enumerate(t["words"][0]):                   # one line holding separate labels: split at the word gaps
                texts.append({**t, "id": f"{t['id']}.{j + 1}", "bbox": list(w), "lines": [list(w)], "split_from": t["id"]})
        else:
            texts.append(dict(t))
    texts, removed = TG.normalize_texts(ctx.bw, texts, symbols, diag_boxes, exclude=ctx.tables)
    ctx.text_geometry_removed = removed
    return blocks, texts


def line_pair_view(page, block, a, b, ca, cb):
    """The text block with one line in colour ca and the next line in colour cb."""
    bx = block["bbox"]
    w, h = V.wh(bx)
    m = int(V.clamp(0.6 * max(w, h), 24, 120))
    v = V.View(page, (bx[0] - m, bx[1] - m, bx[2] + m + 1, bx[3] + m + 1))
    v.box(padded(a, 2), ca, 2)
    v.box(padded(b, 2), cb, 2)
    return v.finish()


async def stage_line_groups(ctx, blocks):
    """7b. P&ID: T2 (Noul, colours swapped for the second question) for every two neighbouring lines of a multi-line block:
    do they belong to one label? Lines joined by a 'yes' (average P >= 0.5) stay together. -> {block id: [[line index, ...]]}."""
    q, ttf = ctx.k["t2"][0], ctx.k["t2"][1:]
    qs, meta = {}, {}
    def order(t):                                                    # neighbours: top to bottom, or left to right for rotated text
        key = (lambda i: (t["lines"][i][0], t["lines"][i][1])) if t.get("orient") == "v" else (lambda i: (t["lines"][i][1], t["lines"][i][0]))
        return sorted(range(len(t["lines"])), key=key)
    for t in blocks:
        o = order(t)
        for i in range(len(o) - 1):
            a, b = t["lines"][o[i]], t["lines"][o[i + 1]]
            for tag, (ca, cb) in (("A", (V.RED, BLUE)), ("B", (BLUE, V.RED))):
                qs[f"{t['id']}.{i}_{tag}"] = noul({"view": Img(line_pair_view(ctx.page, t, a, b, ca, cb)), "question": q}, *ttf)
                meta[f"{t['id']}.{i}_{tag}"] = {"a": a, "b": b, "bbox": t["bbox"]}
    ans = await ctx.jev.ask_chunked("T2_lines", {"task": "Group the lines of text in a piping and instrumentation diagram into labels."},
                                    qs, meta) if qs else {}
    out = {}
    for t in blocks:
        parent = list(range(len(t["lines"])))

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x
        pairs, answered, o = [], True, order(t)
        for i in range(len(o) - 1):
            ps = [ans[f"{t['id']}.{i}_{tg}"] for tg in ("A", "B") if isinstance(ans.get(f"{t['id']}.{i}_{tg}"), (int, float))]
            if not ps:
                answered = False
                continue
            p = sum(ps) / len(ps)
            pairs.append(round(p, 4))
            if p >= 0.5:
                parent[find(o[i + 1])] = find(o[i])
        t["t2"] = pairs
        if not answered and not pairs:
            continue                                                 # no answer: T1 decides as before
        gs = {}
        for i in range(len(t["lines"])):
            gs.setdefault(find(i), []).append(i)
        out[t["id"]] = sorted(gs.values())
    return out


def inside_relations(texts, symbols):
    """심볼 박스 안에 든 텍스트 → {"type": "inside", "a": 텍스트, "b": 심볼} (여럿이면 가장 작은 심볼)."""
    rels = []
    for t in texts:
        hosts = [o for o in symbols if CV.contains(o["bbox"], t["bbox"], 1)]
        if hosts:
            h = min(hosts, key=lambda o: CV.area(o["bbox"]))
            t["inside"] = h["id"]
            rels.append({"type": "inside", "a": t["id"], "b": h["id"]})
    return rels


# ----------------------------------------------------------------------------- output, evaluation, pictures

def reading_order(objs):
    """위에서 아래, 왼쪽에서 오른쪽 (세로 위치가 겹치는 것끼리 한 줄)."""
    rest = sorted(objs, key=lambda o: (o["bbox"][1], o["bbox"][0]))
    rows = []
    for o in rest:
        cy = (o["bbox"][1] + o["bbox"][3]) / 2
        for row in rows:
            if abs(row[0] - cy) <= 25:
                row[1].append(o)
                break
        else:
            rows.append([cy, [o]])
    rows.sort(key=lambda r: r[0])
    return [o for _, row in rows for o in sorted(row, key=lambda o: o["bbox"][0])]


def _match(outs, gts):
    """IoU 0.5 이상끼리 탐욕적으로 짝짓기 -> {출력 id: 정답 id}."""
    pairs = sorted(((iou(o["bbox"], g["bbox"]), o["id"], g["id"]) for o in outs for g in gts), reverse=True)
    o2g, used = {}, set()
    for v, oid, gid in pairs:
        if v >= 0.5 and oid not in o2g and gid not in used:
            o2g[oid] = gid
            used.add(gid)
    return o2g


def _box_stats(outs, gts, o2g, with_class):
    gby = {g["id"]: g for g in gts}
    oby = {o["id"]: o for o in outs}
    ious = [iou(oby[o]["bbox"], gby[g]["bbox"]) for o, g in o2g.items()]
    edges = [abs(oby[o]["bbox"][i] - gby[g]["bbox"][i]) for o, g in o2g.items() for i in range(4)]
    res = {"gt_objects": len(gts), "outputs": len(outs), "matched": len(o2g),
           "precision": len(o2g) / len(outs) if outs else 0.0, "recall": len(o2g) / len(gts) if gts else 0.0,
           "mean_iou": statistics.mean(ious) if ious else 0.0, "iou90": sum(v >= 0.9 for v in ious),
           "edge_le2": sum(e <= 2 for e in edges), "edges": len(edges),
           "missed": sorted(set(gby) - set(o2g.values())), "extra": sorted(set(oby) - set(o2g))}
    if with_class:
        ok = [oby[o].get("class") == gby[g].get("class") for o, g in o2g.items()]
        res["class_acc"] = sum(ok) / len(ok) if ok else 0.0
        res["wrong_class"] = [(o, oby[o].get("class"), gby[g].get("class")) for o, g in o2g.items()
                              if oby[o].get("class") != gby[g].get("class")]
    return res


def in_window(b, w):
    """Box centre inside the window (None = whole page)."""
    if not w:
        return True
    cx, cy = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
    return w[0] <= cx <= w[2] and w[1] <= cy <= w[3]


def evaluate(out, gt_path, page_name, starts=None, cand_rels=None, closure=False):
    """정답 파일(gt_page-XXX.json 형식: objects + relations, 또는 gt_p0.json 형식: symbols)과 비교. 심볼과 텍스트는 따로 채점.
    정답 파일에 "window"가 있으면 그 구역 안(박스 중심 기준)의 출력만 채점한다. "optional": true 인 정답 객체(플랜지 표시처럼 열린 모양이라
    코드가 후보로 내지 못하는 것)는 찾으면 맞은 것도 틀린 것도 아니고, 못 찾아도 놓친 것으로 세지 않는다.
    starts: 심볼 id -> 맞춤 전 박스, cand_rels: K3 이전 연결 후보 [{"a", "b", "net"}],
    closure: 같은 net 안에서 이어진 쌍을 모두 이어진 것으로 본다 (P&ID: 큰 net은 최소 신장 트리 쌍만 출력하므로)."""
    data = json.loads(Path(gt_path).read_text())
    if "objects" in data:
        gts, grels = data["objects"], data.get("relations", [])
    else:
        gts, grels = [s for s in data.get("symbols", []) if s["page"] == page_name], []
    if not gts:
        return None
    win = data.get("window")
    optional = {g["id"] for g in gts if g.get("optional")}
    objs = [o for o in out["objects"] if in_window(o["bbox"], win)]
    is_text = lambda o: o.get("class") == "text"  # noqa: E731
    sym_out, txt_out = [o for o in objs if not is_text(o)], [o for o in objs if is_text(o)]
    sym_gt, txt_gt = [g for g in gts if not is_text(g)], [g for g in gts if is_text(g)]
    o2g = _match(sym_out, sym_gt)
    neutral = {o for o, g in o2g.items() if g in optional}             # matched an optional GT object: not scored
    sym_out = [o for o in sym_out if o["id"] not in neutral]
    sym_gt = [g for g in sym_gt if g["id"] not in optional]
    o2g = {o: g for o, g in o2g.items() if g not in optional}
    res = _box_stats(sym_out, sym_gt, o2g, True)
    if win:
        res["window"] = win
    if neutral:
        res["optional_found"] = sorted(neutral)
    if starts:
        gby = {g["id"]: g for g in sym_gt}
        s_ious = [iou(starts[o], gby[g]["bbox"]) for o, g in o2g.items() if o in starts]
        res["start_mean_iou"] = statistics.mean(s_ious) if s_ious else None
        res["start_iou90"] = sum(v >= 0.9 for v in s_ious)
    if txt_gt:
        t2g = _match(txt_out, txt_gt)
        t_neutral = {o for o, g in t2g.items() if g in optional}
        neutral |= t_neutral
        txt_out = [o for o in txt_out if o["id"] not in t_neutral]
        txt_gt = [g for g in txt_gt if g["id"] not in optional]
        t2g = {o: g for o, g in t2g.items() if g not in optional}
        res["text"] = _box_stats(txt_out, txt_gt, t2g, False)
        o2g = {**o2g, **t2g}
        if neutral:
            res["optional_found"] = sorted(neutral)
    scored = {o["id"] for o in sym_out + txt_out}

    def pairs_of(rels):
        """Output pairs between scored objects; an output matched to an optional GT object (a flange tick found as a symbol)
        is passed through, so the two symbols on either side of it count as joined."""
        rels = [r for r in rels if r["a"] in scored | neutral and r["b"] in scored | neutral]
        if closure or neutral:
            return VZ.closure_pairs(rels, neutral, per_net=closure)
        return [(r["a"], r["b"]) for r in rels]

    def score(pairs_, gset):
        got = set()
        for a, b in pairs_:
            ga, gb = o2g.get(a), o2g.get(b)
            got.add(frozenset((ga, gb)) if ga and gb else frozenset((a + "?", b + "?")))
        return got, len(got & gset)
    conn = {frozenset((r["a"], r["b"])) for r in grels if r.get("type", "connected") == "connected"
            and r["a"] not in optional and r["b"] not in optional}
    if conn:
        got, tp = score(pairs_of([r for r in out["relations"] if r.get("type", "connected") == "connected"]), conn)
        res.update({"gt_relations": len(conn), "relations": len(got), "rel_tp": tp,
                    "rel_precision": tp / len(got) if got else 0.0, "rel_recall": tp / len(conn)})
        if closure:
            res["closure"] = True
        if cand_rels is not None:
            cgot, ctp = score(pairs_of(cand_rels), conn)
            res.update({"cand_relations": len(cgot), "cand_tp": ctp,
                        "cand_precision": ctp / len(cgot) if cgot else 0.0, "cand_recall": ctp / len(conn)})
    ins = {frozenset((r["a"], r["b"])) for r in grels if r.get("type") == "inside"}
    if ins:
        got, tp = score([(r["a"], r["b"]) for r in out["relations"] if r.get("type") == "inside"
                         and r["a"] in scored and r["b"] in scored], ins)
        res["inside"] = {"gt": len(ins), "out": len(got), "tp": tp}
    return res


def eval_lines(ev):
    if not ev:
        return []
    L = ["## 정답 대비", ""]
    if ev.get("window"):
        L.append(f"- 정답이 있는 구역 {ev['window']} 안(박스 중심 기준)의 출력만 채점"
                 + (f" · 정답에서 '선택'으로 표시한 객체(플랜지 표시 등)와 겹친 출력 {len(ev['optional_found'])}개는 채점에서 뺌"
                    if ev.get("optional_found") else ""))
    L += [f"- 심볼: 정답 {ev['gt_objects']}개 중 {ev['matched']}개 찾음 (재현율 {ev['recall']:.0%}), 출력 {ev['outputs']}개 중 "
         f"{ev['matched']}개 정답 (정밀도 {ev['precision']:.0%})",
         f"- 심볼 bbox: 평균 IoU {ev['mean_iou']:.3f} · IoU≥0.9 {ev['iou90']}/{ev['matched']} · 변 오차 ±2px 이내 {ev['edge_le2']}/{ev['edges']}"
         + (f" (맞춤 전 코드 후보: 평균 IoU {ev['start_mean_iou']:.3f} · IoU≥0.9 {ev['start_iou90']}/{ev['matched']})"
            if ev.get("start_mean_iou") is not None else ""),
         f"- 클래스 정확도: {ev['class_acc']:.0%}"]
    if ev.get("wrong_class"):
        L.append("  - 틀린 클래스: " + ", ".join(f"{o} {p} (정답 {g})" for o, p, g in ev["wrong_class"]))
    if ev["missed"]:
        L.append("- 놓친 심볼: " + ", ".join(ev["missed"]))
    if ev["extra"]:
        L.append("- 정답에 없는 심볼 출력: " + ", ".join(ev["extra"]))
    t = ev.get("text")
    if t:
        L.append(f"- 텍스트: 정답 {t['gt_objects']}개 중 {t['matched']}개 찾음 (재현율 {t['recall']:.0%}), 출력 {t['outputs']}개 중 "
                 f"{t['matched']}개 정답 (정밀도 {t['precision']:.0%}) · 평균 IoU {t['mean_iou']:.3f}")
        if t["missed"]:
            L.append("  - 놓친 텍스트: " + ", ".join(t["missed"]))
        if t["extra"]:
            L.append("  - 정답에 없는 텍스트 출력: " + ", ".join(t["extra"]))
    if "gt_relations" in ev:
        L.append(f"- 연결: 정답 {ev['gt_relations']}쌍 중 {ev['rel_tp']}쌍 찾음 (재현율 {ev['rel_recall']:.0%}), "
                 f"출력 {ev['relations']}쌍 중 {ev['rel_tp']}쌍 정답 (정밀도 {ev['rel_precision']:.0%})"
                 + (" — 같은 net 안에서 출력 연결로 이어지는 쌍은 모두 이어진 것으로 셈" if ev.get("closure") else ""))
        if "cand_relations" in ev:
            L.append(f"  - K3 검증 전 코드 후보: {ev['cand_relations']}쌍 중 {ev['cand_tp']}쌍 정답 "
                     f"(재현율 {ev['cand_recall']:.0%}, 정밀도 {ev['cand_precision']:.0%})")
    if ev.get("inside"):
        i = ev["inside"]
        L.append(f"- 심볼 안 글자(inside 관계): 정답 {i['gt']}개 중 {i['tp']}개, 출력 {i['out']}개")
    return L + [""]


def net_color(rank):
    return VZ.hex_bgr(VZ.NET_HEX[(rank - 1) % len(VZ.NET_HEX)])


def rank_nets(rels, objs):
    """net 번호를 1부터 다시 매긴다: 연결이 많은 net부터 (색이 겹치지 않게 큰 net에 앞쪽 색을 준다)."""
    size = {}
    for r in rels:
        size[r["net"]] = size.get(r["net"], 0) + 1
    top_y = {}
    for r in rels:
        y = min(objs[r["a"]]["bbox"][1], objs[r["b"]]["bbox"][1])
        top_y[r["net"]] = min(top_y.get(r["net"], y), y)
    order = sorted(size, key=lambda n: (-size[n], top_y[n]))
    rank = {n: i + 1 for i, n in enumerate(order)}
    for r in rels:
        r["net_rank"] = rank[r["net"]]


def _panel(img, title, width):
    s = width / img.shape[1]
    img = cv2.resize(img, (width, int(img.shape[0] * s)), interpolation=cv2.INTER_AREA)
    bar = np.full((44, width, 3), 255, np.uint8)
    cv2.putText(bar, title, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.85, (30, 30, 30), 2, cv2.LINE_AA)
    return np.concatenate([bar, img, np.full((12, width, 3), 255, np.uint8)], axis=0)


def _rect(img, b, color, t=2, dashed=False, pad=2):
    b = (int(b[0]) - pad, int(b[1]) - pad, int(b[2]) + pad, int(b[3]) + pad)
    if dashed:
        VZ.dashed_rect(img, b, color, t, 8)
    else:
        cv2.rectangle(img, b[:2], b[2:], color, t)


def render_steps(page, regions, cands, objs, merged, rels, out_path, tblocks=(), width=1800, tables=()):
    """단계별 그림: 영역(S1) → 후보(S2) → bbox 조정 → 분류 → 연결(K3)."""
    H, W = page.shape[:2]
    base = cv2.cvtColor(page, cv2.COLOR_GRAY2BGR)
    ov = base.copy()
    for t in tables:
        _rect(ov, t, (40, 40, 220), 5, dashed=True, pad=10)
        VZ.put_label(ov, "table (code, excluded)", (t[0], max(t[1] - 20, 40)), (40, 40, 220), 1.4)
    for r in regions:
        col = (0, 150, 0) if r["kind"] in SEARCH_KINDS else (150, 150, 150)
        _rect(ov, r["bbox"], col, 6, pad=6)
        VZ.put_label(ov, f"{r['id']} {r['kind']}", (r["bbox"][0], max(r["bbox"][1] - 14, 40)), col, 1.6)
    panels = [_panel(ov, "1) regions (code) -> S1: green = diagram, searched for symbols; red dashed = ruled table, excluded", width)]
    diag = [r["bbox"] for r in regions if r["kind"] in SEARCH_KINDS] or [regions[0]["bbox"]]
    x0 = max(min(b[0] for b in diag) - 40, 0)
    y0 = max(min(b[1] for b in diag) - 40, 0)
    x1 = min(max(b[2] for b in diag) + 40, W - 1)
    y1 = min(max(b[3] for b in diag) + 40, H - 1)

    def crop(img):
        return img[y0:y1 + 1, x0:x1 + 1].copy()
    im = base.copy()
    for c in cands:
        if c["keep"]:
            _rect(im, c["bbox"], (208, 91, 29), 2)
        else:
            _rect(im, c["bbox"], (40, 40, 220), 2, dashed=True)
            VZ.put_label(im, c.get("kind", ""), (c["bbox"][0] + 6, c["bbox"][1] + 26), (40, 40, 220), 0.8)
    panels.append(_panel(crop(im), "2) candidates (code) -> S2: blue = kept as symbol, red dashed = rejected", width))
    im = base.copy()
    for o in objs + merged:
        _rect(im, o["start_bbox"], (150, 150, 150), 1, dashed=True, pad=0)
    for o in objs:
        _rect(im, o["bbox"], (208, 91, 29), 2, pad=1)
    panels.append(_panel(crop(im), "3) box fit: gray dashed = outline box (code), blue = final (B6 picks outline or extended box)", width))
    im = base.copy()
    for o in objs:
        _rect(im, o["bbox"], (208, 91, 29), 2, pad=1)
        short = (o.get("class") or "-").split("/")[-1]
        VZ.put_label(im, f"{o['id']} {short}", (o["bbox"][0], max(o["bbox"][1] - 8, 20)), (208, 91, 29), 0.7)
    panels.append(_panel(crop(im), "4) classes (C1, legend examples)", width))
    im = base.copy()
    for r in rels:
        if not r.get("path"):
            continue
        pts = np.array(r["path"], np.int32).reshape(-1, 1, 2)
        if r.get("accepted", True):
            cv2.polylines(im, [pts], False, net_color(r.get("net_rank", r["net"] + 1)), 6, cv2.LINE_AA)
    for r in rels:
        if r.get("path") and not r.get("accepted", True):
            for p, q in zip(r["path"], r["path"][1:]):
                VZ.dashed_rect(im, (min(p[0], q[0]), min(p[1], q[1]), max(p[0], q[0]), max(p[1], q[1])), (40, 40, 220), 3, 10)
    for o in objs:
        _rect(im, o["bbox"], (208, 91, 29), 2, pad=1)
    panels.append(_panel(crop(im), "5) connections: wires traced by code, one color per net; K3-rejected pairs red dashed", width))
    if tblocks:
        im = base.copy()
        for o in objs:
            _rect(im, o["bbox"], (208, 91, 29), 1, pad=1)
        for t in tblocks:
            if t.get("keep", True):
                _rect(im, t["bbox"], PURPLE, 2, pad=3)
            else:
                _rect(im, t["bbox"], (40, 40, 220), 2, dashed=True, pad=3)
                VZ.put_label(im, t.get("kind", ""), (t["bbox"][0], t["bbox"][1] - 8), (40, 40, 220), 0.7)
        panels.append(_panel(crop(im), "6) text blocks (code) -> T1: purple = text, red dashed = rejected", width))
    cv2.imwrite(str(out_path), np.concatenate(panels, axis=0))


# ----------------------------------------------------------------------------- main

def show(p):
    p = Path(p)
    return p.relative_to(ROOT) if p.is_relative_to(ROOT) else p


def resolve_page(arg):
    p = Path(arg)
    for cand in (p, ROOT / p, ROOT / "image" / p.name):
        if cand.exists():
            return cand.resolve()
    raise FileNotFoundError(arg)


def est_cost_lines(ctx, regions, cands, rels=(), objs=(), diag=()):
    """--dry-run 용: 실제로 만들 뷰로 토큰을 추정한다 (기본 compare 방식 기준, edges 방식의 B1은 따로 표시).
    모든 후보를 심볼로 보고 세므로 실제보다 크게 나온다."""
    s0 = 2 * Img(page_view(ctx.page)).tokens
    s1 = sum(2 * (Img(v[0]).tokens + Img(v[1]).tokens) for v in (region_views(ctx.page, r["bbox"]) for r in regions
                                                                  if max(r["bbox"][2] - r["bbox"][0], r["bbox"][3] - r["bbox"][1]) + 1 >= MIN_REGION_SIDE))
    s2 = sum(2 * Img(candidate_view(ctx.page, c["bbox"])).tokens for c in cands)
    boxes = [tuple(c["bbox"]) for c in cands]
    b6, b1 = 0.0, 0.0
    for c in cands:
        box = tuple(c["bbox"])
        ext, _ = CV.attached_extent(ctx.bw, box, boxes)
        if max(abs(a - b) for a, b in zip(box, ext)) >= 2:
            b6 += 4 * sum(Img(v).tokens for v in compare_views(ctx.page, [box, ext])) / 2
        per_round = 0.0
        for e in V.EDGES:
            pos = R.candidate_positions(ctx.page, box, e)[0]
            per_round += Img(V.context_view(ctx.page, box)).tokens
            per_round += 2 * sum(Img(V.edge_view(ctx.page, V.with_edge(box, e, p), e)).tokens for p in pos)
        b1 += 2.5 * per_round
    legend = load_legend(ctx.k["legend"])
    c1 = sum(2 * est_tokens(choice({"symbol": Img(symbol_view(ctx.page, c["bbox"])), "question": ctx.k["c1_q"]}, legend))
             for c in cands)
    diag = list(diag) or [tuple(regions[0]["bbox"])]
    tb = text_blocks(ctx, diag, [c["bbox"] for c in cands])
    t1 = sum(2 * Img(text_view(ctx.page, t["bbox"])).tokens for t in tb)
    t2 = sum(2 * (len(t["lines"]) - 1) * Img(text_view(ctx.page, t["bbox"])).tokens for t in tb) if ctx.k["t2"] else 0
    k3 = sum(2 * Img(pair_view(ctx.page, erase_box(objs[r["a"]], ctx.k["erase_ext"]), erase_box(objs[r["b"]], ctx.k["erase_ext"]),
                               r["path"], V.RED, BLUE, up=ctx.k["pair_up"])).tokens for r in rels) if objs else 60 * 1800
    total = s0 + s1 + s2 + b6 + c1 + t1 + t2 + k3
    return [f"예상 입력 토큰 ≈ {total:,.0f} (≈ ${total * USD_PER_TOKEN:.3f})  [S0 {s0:,.0f} · S1 {s1:,.0f} · S2 {s2:,.0f} · "
            f"B6 {b6:,.0f} · C1 {c1:,.0f} · K3 {k3:,.0f} · T1 {t1:,.0f}" + (f" · T2 {t2:,.0f}" if t2 else "") + "]  (후보를 모두 심볼로 본 상한)",
            f"(--refine edges 로 돌리면 B1 조정 루프 ≈ {b1:,.0f} 토큰이 더 든다)"]


async def main(argv=None, transport=None, fake=None) -> int:
    load_env(ROOT / ".env")
    ap = argparse.ArgumentParser(description="도면 한 장의 모든 심볼과 연결을 Jev로 인식")
    ap.add_argument("page", help="도면 이미지 (예: image/page-016.png 또는 page-016.png)")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--kind", choices=("auto", "logic", "pid"), default="auto",
                    help="도면 종류. auto: Jev S0가 판단 (기본) · logic: 로직 다이어그램 · pid: P&ID")
    ap.add_argument("--gt", default=None, help="정답 파일 (기본: experiments/gt_<페이지>.json 이 있으면 자동 사용)")
    ap.add_argument("--concurrency", type=int, default=8)
    ap.add_argument("--refine", choices=("compare", "edges", "none"), default="compare",
                    help="bbox 맞춤 방식. compare: 코드가 붙은 획까지 넓힌 박스를 제안하고 Jev B6가 고름 (기본) · "
                         "edges: Jev B1 변 방향 판단 루프 (p0_refine) · none: 코드 후보 박스 그대로")
    ap.add_argument("--no-verify", action="store_true", help="연결 검증(K3)을 건너뛰고 코드가 찾은 연결을 그대로 쓴다")
    ap.add_argument("--no-cache", action="store_true")
    ap.add_argument("--dry-run", action="store_true", help="Jev 호출 없이 코드 단계만 실행하고 예상 비용을 보여 준다")
    ap.add_argument("--out", default=None, help="결과 폴더 (기본: runs/page/<페이지>-<시각>)")
    args = ap.parse_args(argv)

    page_path = resolve_page(args.page)
    stem = page_path.stem
    gt_path = Path(args.gt) if args.gt else (HERE / f"gt_{stem}.json")
    gt_path = gt_path if gt_path.exists() else None
    if not args.dry_run and fake is None and not os.environ.get("TYPESAFE_API_KEY"):
        print("TYPESAFE_API_KEY 가 없습니다. cad-jev/.env 를 확인하세요.")
        return 2
    out_dir = Path(args.out).resolve() if args.out else ROOT / "runs" / "page" / f"{stem}-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    out_dir.mkdir(parents=True, exist_ok=True)

    page = V.load_page(page_path)
    H, W = page.shape[:2]
    bw, frame_box = FG.remove_coordinate_strips(CV.binarize(page))
    bw, _ = CV.remove_frame(bw)
    text_h = CV.estimate_text_height(bw)
    CV.set_scale(text_h)                                             # 모든 크기 기준을 이 도면의 글자 높이에 맞춘다
    tables = CV.table_regions(bw)
    t0 = time.perf_counter()
    print(f"[{args.model}] {page_path.name} ({W}x{H}) · 글자 높이 {text_h}px · 괘선 표 {len(tables)}개"
          + (f" · 정답 파일 {gt_path.name}" if gt_path else "") + (" · DRY RUN" if args.dry_run else ""))

    client = None
    if not args.dry_run and fake is None:
        from typesafe_sdk import AsyncTypeSafeClient, RetryPolicy
        client = AsyncTypeSafeClient(api_key=os.environ["TYPESAFE_API_KEY"], model=args.model, timeout=90.0,
                                     retry=RetryPolicy(max_retries=4, timeout=180.0), transport=transport)
    jev = Jev(args.model, args.concurrency, client=client, fake=fake,
              cache_dir=None if args.no_cache else ROOT / ".cache" / "jev", log_path=out_dir / "jev_log.jsonl")
    ctx = Ctx(page, bw, jev, "logic", tables, text_h, frame_box=frame_box)
    trace = {"model": args.model, "page": page_path.name, "text_height": text_h, "tables": [list(t) for t in tables], "frame": frame_box}

    def step(msg):
        print(f"  {time.perf_counter() - t0:6.1f}s  {msg}", flush=True)

    if args.dry_run:
        ctx.set_kind(args.kind if args.kind != "auto" else guess_kind(text_h))
        if ctx.kind == "pid" and frame_box != [0, 0, W-1, H-1]:
            ctx.bw, _ = FG.remove_coordinate_strips(CV.binarize(page))
            ctx.set_kind(ctx.kind)
        step(f"0) 종류 {ctx.k['label']} (" + ("--kind 지정" if args.kind != "auto" else "글자 높이로 가정. 실제 실행에서는 Jev S0가 판단") + ")")
        regions = [{"id": f"R{i + 1}", "bbox": list(b), "kind": "diagram" if i == 0 else "?", "probs": None}
                   for i, b in enumerate(CV.layout_regions(bw))]
        diag = [tuple(regions[0]["bbox"])]
        boxes, equipment, arrows = geometry_candidates(ctx, diag)
        cands = [{"id": f"c{i + 1}", "bbox": list(b), "keep": True, "kind": "?",
                  **({"equipment_geometry": equipment[b]} if b in equipment else {}),
                  **({"shape_proposal": arrows[b]} if b in arrows else {})}
                 for i, b in enumerate(boxes)]
        step(f"영역 {len(regions)}개 (가장 큰 영역을 다이어그램으로 가정) · 후보 {len(cands)}개")
        objs = [{"id": f"s{i + 1}", "cand": c["id"], "start_bbox": c["bbox"], "bbox": c["bbox"], "confidence": None}
                for i, c in enumerate(cands)]
        rels, nets = relation_candidates(ctx, objs, diag)
        rank_nets(rels, objs)
        step(f"연결 후보 {len(rels)}쌍 (net {sum(1 for n in nets if len(n['ports']) >= 2)}개"
             + (f", 그중 점선 포함 {sum(1 for n in nets if n.get('dashed') and len(n['ports']) >= 2)}개" if ctx.k["dashes"] else "") + ")")
        tblocks = [{"id": f"x{i + 1}", "bbox": list(t["bbox"]), "keep": True, "kind": "?"}
                   for i, t in enumerate(text_blocks(ctx, diag, [c["bbox"] for c in cands]))]
        step(f"텍스트 덩어리 후보 {len(tblocks)}개")
        for line in est_cost_lines(ctx, regions, cands, rels, objs, diag):
            print("  " + line)
        render_steps(page, regions, cands, objs, [], rels, out_dir / f"{stem}_steps.png", tblocks, tables=ctx.tables)
        print(f"\n단계별 그림: open {show(out_dir / f'{stem}_steps.png')}")
        return 0

    fatal = None
    if client is not None:
        await client.__aenter__()
    try:
        if args.kind == "auto":
            kinfo = await stage_kind(ctx, text_h)
        else:
            kinfo = {"kind": args.kind, "note": "--kind", "text_height": text_h}
        ctx.set_kind(kinfo["kind"])
        # A coherent closed frame was already removed by its actual bounds.
        # P&ID's internal long pipes/shaft lines must not be swept away merely
        # because they span half the sheet. Keep the established CLD preprocessing.
        if ctx.kind == "pid" and frame_box != [0, 0, W-1, H-1]:
            ctx.bw, _ = FG.remove_coordinate_strips(CV.binarize(page))
            ctx.set_kind(ctx.kind)
            trace["long_internal_lines_preserved"] = True
        trace["kind"] = kinfo
        step(f"0) 종류 {ctx.k['label']}" + (f" (S0 {top(kinfo['probs'])} {max(kinfo['probs'].values()):.2f})" if kinfo.get("probs") else "")
             + (f" · {kinfo['note']}" if kinfo.get("note") else "") + f" · 글자 높이 {text_h}px")
        regions = await stage_regions(ctx)
        diag = [tuple(r["bbox"]) for r in regions if r["kind"] in SEARCH_KINDS]
        step("1) 영역 " + ", ".join(f"{r['id']}={r['kind']}" for r in regions))
        cands = await stage_candidates(ctx, diag)
        step(f"2) 후보 {len(cands)}개 → 심볼 {sum(c['keep'] for c in cands)}개 "
             f"(제외: " + ", ".join(f"{c['id']} {c['kind']}" for c in cands if not c["keep"]) + ")")
        if args.refine == "compare":
            refined = await stage_fit(ctx, cands)
            asked = [o for o in refined if "p_ext" in o]
            step(f"3) bbox 맞춤 {len(refined)}개: 붙은 획이 있어 B6에 물은 것 {len(asked)}개 → 넓힌 박스 채택 "
                 f"{sum(o['p_ext'] >= 0.5 for o in asked)}개")
        else:
            refined = await stage_refine(ctx, cands, refine=args.refine == "edges")
            step(f"3) bbox 조정 {len(refined)}개 (라운드 중앙값 {statistics.median([len(o['rounds']) for o in refined]) if refined else 0:.0f})")
        objs, merged = dedupe(refined, cands, ctx.bw)
        step(f"4) 중복 정리 → {len(objs)}개" + (f" (합침 {len(merged)})" if merged else ""))
        legend = load_legend(ctx.k["legend"])
        await stage_classify(ctx, objs, legend)
        await stage_recheck_classes(ctx, objs, legend)
        await stage_closed_box_classes(ctx, objs, legend)
        dropped = [o for o in objs if o.get("class") == "other"]
        objs = [o for o in objs if o.get("class") != "other"]
        objs, compound_dropped, compound_notes = AG.postclass_compounds(ctx.bw, objs)
        dropped.extend(compound_dropped)
        trace["arrow_geometry"] = compound_notes
        objs, geometry_dropped, geometry_notes = SG.refine(ctx.bw, objs, cands, profile_kind=ctx.kind, gray=ctx.page)
        dropped.extend(geometry_dropped)
        trace["symbol_geometry"] = geometry_notes
        objs, logic_dropped, logic_notes = LG.refine(ctx.bw, objs, cands, profile_kind=ctx.kind)
        dropped.extend(logic_dropped)
        trace["logic_geometry"] = logic_notes
        trace["equipment_geometry"] = ctx.equipment_proposals
        if ctx.k["container"] == "top":                             # P&ID: a box holding other symbols stays only as equipment
            for o in objs:
                if o.get("class") != "equipment" and any(p is not o and p.get("class") != o.get("class")
                                                        and CV.contains(o["bbox"], p["bbox"])
                                                        and CV.area(p["bbox"]) > .12 * CV.area(o["bbox"])
                                                        for p in objs):
                    o["note"] = "holds other symbols but C1 did not call it equipment (a pipe loop); removed"
                    dropped.append(o)
            objs = [o for o in objs if o not in dropped]
        step(f"5) 분류 완료" + (f" (기타 또는 배관 고리로 보고 제외 {len(dropped)}개)" if dropped else ""))
        objs = reading_order(objs)
        for i, o in enumerate(objs):
            o["id"] = f"s{i + 1}"
        rels, nets = relation_candidates(ctx, objs, diag)
        if not args.no_verify:
            await stage_verify(ctx, objs, rels)
        else:
            for r in rels:
                r["confidence"], r["accepted"] = None, True
        rank_nets(rels, objs)
        n_mst = sum(1 for n in nets if n.get("mst"))
        step(f"6) 연결 후보 {len(rels)}쌍 → 채택 {sum(r['accepted'] for r in rels)}쌍"
             + (f" (심볼이 많은 net {n_mst}개는 최소 신장 트리 쌍만 물음)" if n_mst else ""))
        tblocks, texts = await stage_text(ctx, diag, objs)
        texts = reading_order(texts)
        for i, t in enumerate(texts):
            t["id"] = f"t{i + 1}"
        inside = inside_relations(texts, objs)
        step(f"7) 텍스트 덩어리 후보 {len(tblocks)}개 → 텍스트 {len(texts)}개 (심볼 안 {len(inside)}개)"
             + (" · 제외: " + ", ".join(f"{t['id']} {t['kind']}" for t in tblocks if not t["keep"]) if any(not t["keep"] for t in tblocks) else ""))
    except Fatal as error:
        fatal = error
    finally:
        if client is not None:
            await client.__aexit__(None, None, None)
    if fatal:
        print(f"중단: {fatal}")
        return 1

    # ---- output (§6) + trace
    rel_out, k = [], 0
    for r in sorted(rels, key=lambda r: (r["net_rank"], r["a"], r["b"])):
        if not r["accepted"]:
            continue
        k += 1
        r["id"] = f"r{k}"
        rel_out.append({"id": r["id"], "type": "connected", "a": objs[r["a"]]["id"], "a_side": r["a_side"],
                        "b": objs[r["b"]]["id"], "b_side": r["b_side"], "confidence": r["confidence"],
                        "a_point": r["a_point"], "b_point": r["b_point"], "net": f"n{r['net_rank']}", "path": r["path"],
                        "evidence": {"code": "same wire net" + (f", {r['bridges']} crossing jump(s)/dash link(s)" if r["bridges"] else "")
                                     + (", net has dashed line pieces" if r.get("dashed") else "")
                                     + (", candidate pair of a big net" if r.get("mst") else ""),
                                     "k3_p_yes": r.get("k3"), "decision": r.get("decision"),
                                     "compact_output_review": r.get("compact_output_review"),
                                     "local_min_p": r.get("local_confidence"), "checkpoint_keys": r.get("checkpoint_keys"),
                                     "endpoint_min_p": r.get("endpoint_confidence"), "endpoint_keys": r.get("endpoint_keys")}})
    for r in inside:
        k += 1
        r["id"] = f"r{k}"
        rel_out.append({"id": r["id"], "type": "inside", "a": r["a"], "b": r["b"],
                        "evidence": {"code": "text box lies inside the symbol box"}})
    rel_path = (page_path.relative_to(ROOT) if page_path.is_relative_to(ROOT) else page_path).as_posix()
    output = {
        "image": {"file": page_path.name, "path": rel_path, "width": W, "height": H},
        "objects": [{"id": o["id"], "class": o.get("class"), "bbox": o["bbox"], "confidence": o["confidence"],
                     "class_confidence": o.get("class_confidence"), "evidence": {"trace": f"objects.{o['id']}"}} for o in objs]
                   + [{"id": t["id"], "class": "text", "bbox": t["bbox"], "confidence": t["confidence"],
                       "evidence": {"trace": f"texts.{t['id']}", "lines": len(t["lines"])}} for t in texts],
        "relations": rel_out,
        "meta": {"model": jev.served or args.model, "created": datetime.now().isoformat(timespec="seconds"),
                 "drawing_kind": ctx.kind, "text_height": text_h,
                 "relation_mode": "mst" if ctx.k["mst_over"] else "pairs",
                 "relation_note": ("connected = two symbols joined by lines with no other symbol between them. In a net with more than "
                                   f"{ctx.k['mst_over']} symbols spanning-tree pairs are listed, with bounded nearest-neighbour "
                                   "backup pairs for inferred signal routes; every two symbols linked through "
                                   "relations of the same net are connected too.") if ctx.k["mst_over"] else
                                  "connected = every pair of symbols on the same wire net.",
                 "pipeline": "run_page.py: frame → S0 → S1 → geometric proposals → S2 → B6 fit → C1/C2 body/closed-box detail → raw body extent → wire nets → K3/compact output detail/K5 partitioned route/anchor review/K6 endpoints → T1/T2 → text geometry",
                 "algorithm_revision": "geometry-local-route-v12"},
    }
    trace.update({
        "regions": regions,
        "candidates": cands,
        "objects": {o["id"]: {k2: o.get(k2) for k2 in ("cand", "start_bbox", "ext_bbox", "p_ext", "bbox", "confidence", "s2",
                                                        "class", "class_probs", "class_confidence", "rounds", "note", "geometry_reason",
                                                        "equipment_geometry", "shape_proposal", "logic_geometry_reason",
                                                        "detail_class_probs", "detail_class_accepted", "class_before_detail", "class_probs_before_detail",
                                                        "closed_box_review")} for o in objs},
        "merged": [{k2: o.get(k2) for k2 in ("cand", "bbox", "merged_into")} for o in merged],
        "dropped_as_other": [{k2: o.get(k2) for k2 in ("cand", "bbox", "class_probs", "s2")} for o in dropped],
        "nets": [{"id": n["id"], "bbox": n["bbox"], "bridges": n["bridges"],
                  "source": "signal_gap_hypothesis" if n.get("signal_gap_proposals") else
                            "enhanced_outlet_tee" if n.get("inferred_outlet_tee") else "original_ink",
                  "ports": [{"object": objs[p["obj"]]["id"], "side": p["side"], "point": p["point"]} for p in n["ports"]]}
                 for n in nets if n["ports"]],
        "route_checkpoints": getattr(ctx, "route_checkpoints", {}),
        "port_tee_proposals": getattr(ctx, "port_tee_proposals", []),
        "port_tee_pruned": getattr(ctx, "port_tee_pruned", []),
        "signal_gap_proposals": getattr(ctx, "signal_gap_proposals", []),
        "endpoint_checks": getattr(ctx, "endpoint_checks", {}),
        "relation_candidates": [{"a": objs[r["a"]]["id"], "b": objs[r["b"]]["id"], "net": f"n{r['net_rank']}", "k3_p_yes": r.get("k3"),
                                 "compact_output_review": r.get("compact_output_review"),
                                 "confidence": r.get("confidence"), "accepted": r["accepted"], "path": r["path"],
                                 "decision": r.get("decision"), "local_min_p": r.get("local_confidence"),
                                 "checkpoint_keys": r.get("checkpoint_keys"), "blockers": r.get("blockers"), "tee_gaps": r.get("tee_gaps"),
                                 "initial_checkpoint_keys": r.get("initial_checkpoint_keys"),
                                 "anchor_review_keys": r.get("anchor_review_keys"),
                                 "signal_gaps": r.get("signal_gaps"), "endpoint_contacts": r.get("endpoint_contacts"),
                                 "crossing_details": r.get("crossing_details"),
                                 "contact_review_keys": r.get("contact_review_keys"),
                                 "endpoint_min_p": r.get("endpoint_confidence"), "endpoint_keys": r.get("endpoint_keys")} for r in rels],
        "text_candidates": tblocks,
        "text_geometry_removed": getattr(ctx, "text_geometry_removed", []),
        "texts": {t["id"]: {k2: t.get(k2) for k2 in ("bbox", "lines", "chars", "probs", "kind", "confidence", "t2", "inside", "split_from", "geometry_before_bbox", "geometry_removed_lines")}
                  for t in texts},
        "jev": jev.stats,
    })
    (out_dir / f"{stem}_output.json").write_text(json.dumps(output, ensure_ascii=False, indent=1))
    (out_dir / f"{stem}_trace.json").write_text(json.dumps(trace, ensure_ascii=False, indent=1))

    elapsed = time.perf_counter() - t0
    ev = evaluate(output, gt_path, page_path.name, starts={o["id"]: o["start_bbox"] for o in objs},
                  cand_rels=[{"a": objs[r["a"]]["id"], "b": objs[r["b"]]["id"], "net": f"n{r['net_rank']}"} for r in rels],
                  closure=bool(ctx.k["mst_over"])) if gt_path else None
    tokens = jev.total("tokens")
    lines = [f"# {page_path.name} 인식 결과 ({jev.served or args.model})", "",
             f"도면 종류 {ctx.k['label']}" + (f" (S0: {kinfo['answer']})" if kinfo.get("answer") else f" ({kinfo.get('note', '')})")
             + f" · 글자 높이 {text_h}px · 괘선 표 {len(tables)}개 제외", "",
             f"심볼 {len(objs)}개 · 텍스트 {len(texts)}개 · 연결 {sum(r['type'] == 'connected' for r in rel_out)}쌍 · "
             f"심볼 안 글자 {len(inside)}개 · 소요 {elapsed:.0f}초", "",
             f"Jev 요청 {jev.total('requests')}회 (실패 {jev.total('errors')}, 캐시에서 답한 질문 {jev.total('cached')}개) · "
             f"입력 토큰 {tokens:,} (≈ ${tokens * USD_PER_TOKEN:.3f})"
             + (f" · 지연 중앙값 {int(statistics.median(jev.ms))} ms" if jev.ms else ""), "",
             "| 툴 | 요청 | 실패 | 보낸 질문 | 캐시에서 답한 질문 | 토큰 |", "|---|---|---|---|---|---|"]
    for tool, s in jev.stats.items():
        lines.append(f"| {tool} | {s['requests']} | {s['errors']} | {s['questions']} | {s['cached']} | {s['tokens']:,} |")
    lines += [""] + eval_lines(ev)
    lines += ["## 객체", "", "| id | class | bbox | 박스 확신도 | 클래스 확신도 |", "|---|---|---|---|---|"]
    for o in objs:
        conf = "-" if o["confidence"] is None else f"{o['confidence']:.2f}"
        cconf = "-" if o.get("class_confidence") is None else f"{o['class_confidence']:.2f}"
        lines.append(f"| {o['id']} | {o.get('class')} | {o['bbox']} | {conf} | {cconf} |")
    lines += ["", "## 텍스트", "", "| id | bbox | 줄 | 들어 있는 심볼 | T1 P(글자) |", "|---|---|---|---|---|"]
    for t in texts:
        lines.append(f"| {t['id']} | {t['bbox']} | {len(t['lines'])} | {t.get('inside') or '-'} | "
                     f"{'-' if t['confidence'] is None else format(t['confidence'], '.2f')} |")
    lines += ["", "## 연결", "", "| id | a | b | net | 채택한 판단의 확률 |", "|---|---|---|---|---|"]
    for r in rel_out:
        if r["type"] != "connected":
            continue
        lines.append(f"| {r['id']} | {r['a']} ({r['a_side']}) | {r['b']} ({r['b_side']}) | {r['net']} | "
                     f"{'-' if r['confidence'] is None else format(r['confidence'], '.2f')} |")
    rejected = [r for r in rels if not r["accepted"]]
    if rejected:
        lines += ["", "검증에서 채택하지 않은 후보: " + ", ".join(
            f"{objs[r['a']]['id']}–{objs[r['b']]['id']} "
            f"({'미응답' if r['confidence'] is None else format(r['confidence'], '.2f')}; {r.get('decision', 'unchecked')})"
            for r in rejected)]
    text = "\n".join(lines)
    (out_dir / "summary.md").write_text(text + "\n")
    if ev:
        (out_dir / "eval.json").write_text(json.dumps(ev, ensure_ascii=False, indent=1))

    render_steps(page, regions, cands, objs, merged, rels, out_dir / f"{stem}_steps.png", tblocks, tables=ctx.tables)
    made = VZ.visualize(out_dir / f"{stem}_output.json", gt_path)
    print("\n" + text)
    print("\n결과 (브라우저·미리보기로 열기):")
    for p in made + [out_dir / f"{stem}_steps.png"]:
        if p.suffix in (".html", ".png"):
            print(f"  open {show(p)}")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
