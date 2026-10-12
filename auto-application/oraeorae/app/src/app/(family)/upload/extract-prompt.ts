import { CHECKUP_ITEMS } from "@/lib/checkup-items";

// The extraction prompt and output schema, shared by the production call (OpenAI Responses API) and the local-dev
// path (Codex SDK). A "use server" file can only export functions, so they live here.

// Kept identical across requests (no per-user text) so OpenAI can cache it as the prompt prefix.
export const INSTRUCTIONS = `한국 건강검진 결과지에 적힌 검사 결과를 빠짐없이 옮겨요.
PDF였다면 문서 전체 텍스트가 쪽 번호와 함께 먼저 오고, 그 뒤에 결과지 이미지가 한 장 이상 와요. 글자가 없는 쪽(체성분, 골밀도, 스캔본)은 이미지로만 와요.
텍스트가 있으면 수치는 텍스트에서 정확히 옮기고, 판정은 이미지의 체크(■/☑/V) 위치로 확인해요.

items 규칙:
- 결과지에 결과가 적힌 검사 항목은 모두 넣어요: 신체계측, 혈압, 시력·안압·청력, 혈액·소변 검사, 종양표지, 갑상선, 체성분(InBody), 골밀도(T-score 등), 영양지수 점수, 위험평가 점수 등.
  같은 항목이 여러 쪽에 나오면 이번 검진 값으로 한 번만 넣어요.
- section: 그 항목이 실린 쪽의 분류 제목 그대로(예: "간기능검사 및 간염검사", "체성분분석", "골밀도 검사", "영양지수"). 목차 제목이 아니라 그 쪽에 적힌 제목이에요. 없으면 null이에요.
- label: 결과지에 적힌 항목 이름이에요. 한글 검사명과 영문 약어가 함께 적혀 있으면("T.Bilirubin 총빌리루빈", "WBC 백혈구수") 한글 검사명을 써요.
  한글 부분이 검사명이 아니라 설명이면("CRP 세균,심근질환") 영문 이름(CRP)을 써요. 한글 이름이 없으면 적힌 그대로예요.
  아래 표준 항목에 해당하면 key에 표준 key를, 아니면 key에 label을 그대로 넣어요.
  표준 항목 (key: 이름 · 결과지 표기 · 단위):
${CHECKUP_ITEMS.map((i) => `  - ${i.key}: ${i.label} · ${i.find} · ${i.unit}`).join("\n")}
- value는 숫자 결과(단위 제외)예요. "Negative", "정상범위", "Yellow"처럼 글자로 적힌 결과와 "3-5", "0-3"처럼 범위로 적힌 결과는 text_value에 그대로 넣고 value는 null이에요. 둘 다 없는 항목은 빼요.
- "117/70"(수축기/이완기), "16 / 16"(좌/우)처럼 한 칸에 두 값이 있으면 나눠서 각각 넣어요.
- 한 칸에 "간초음파: 지방간(경도) 담낭초음파: 정상범위 …"처럼 검사 여러 개의 결과가 적혀 있으면 검사마다 항목을 나눠요(label "간초음파", text_value "지방간(경도)").
- reference: 결과지에 적힌 참고치 그대로(예: "0.1-1.2", "<200", "Negative"). 여러 줄로 적혀 있으면 정상 기준 한 줄만(예: "Negative <0.90"). 없으면 null이에요.
- flag: 결과지가 그 항목에 H 또는 L을 표시한 경우만 "H"/"L"이고, 아니면 null이에요. 참고치와 비교해 직접 표시하지 마세요.
- "***"·"비대상"·빈칸뿐이고 이번 검진의 실제 수치가 다른 쪽에도 없는 항목은 넣지 마세요.
- 결과 쪽 칸이 "***"이어도 같은 검진의 다른 쪽 검사표에 실제 수치가 있으면 그 수치를 넣어요. 이전 검진 수치와 참고치를 value로 옮기지 마세요.
- judgement는 국가건강검진 결과통보서의 판정 칸에 적히거나 체크된 판정만 옮겨요. 영양지수·체성분·유전자검사 등의 등급(개선시급·양호·표준 등)은 judgement가 아니에요:
  정상A·정상 → "정상" / 정상B·경계·전단계·공복혈당장애 의심 → "경계" / 질환의심·○○ 의심·유질환자 → "질환의심".
  판정 칸이 없거나 체크가 보이지 않으면 null이에요. 참고치와 비교해 직접 판단하지 마세요.
- 단위 IU/L은 U/L과 같아요.
- uncertain: 글자가 흐리거나 잘려 결과가 확실하지 않으면 true예요.
- exam_date: 결과지에 적힌 이번 검진일(검진일자·수검일)을 YYYY-MM-DD로 줘요. 발행일·출력일·이전 검진일은 아니에요. 없으면 null이에요.
- findings: 수치가 아닌 소견(장기별 소견, 종합소견, 영상·내시경 결과 등)에서 정상이 아닌 것만 결과지 표현 그대로 옮겨요.
  예: "경증 지방간", "비장비대(종대)", "만성표재성위염", "역류성식도염". 한 줄에 여러 소견이 있으면 하나씩 나눠요.
  "의심", "경도", "경증" 같은 말은 빼지 말고 결과지 글자 그대로 옮겨요(예: "융합척추 의심"). 문장으로 적힌 소견은 첫 문장만 옮겨요.
  "정상", "정상범위"로 시작하는 것, 설명·권고·"별지 참조" 안내, items에 이미 넣은 수치 판정과 같은 내용은 넣지 마세요.
  같은 소견이 여러 쪽에 나오면 한 번만 넣어요. category는 결과지의 분류(예: "소화기계", "간")이고 없으면 null이에요.
- 건강검진 결과지가 아니면 items와 findings를 빈 배열로 주세요.`;

export const SCHEMA = {
  type: "object",
  additionalProperties: false,
  required: ["exam_date", "items", "findings"],
  properties: {
    exam_date: { type: ["string", "null"] },
    findings: {
      type: "array",
      items: {
        type: "object",
        additionalProperties: false,
        required: ["category", "finding"],
        properties: { category: { type: ["string", "null"] }, finding: { type: "string" } },
      },
    },
    items: {
      type: "array",
      items: {
        type: "object",
        additionalProperties: false,
        required: ["section", "key", "label", "value", "text_value", "unit", "reference", "flag", "judgement", "uncertain"],
        properties: {
          section: { type: ["string", "null"] },
          key: { type: "string" },
          label: { type: "string" },
          value: { type: ["number", "null"] },
          text_value: { type: ["string", "null"] },
          unit: { type: "string" },
          reference: { type: ["string", "null"] },
          flag: { type: ["string", "null"], enum: ["H", "L", null] },
          judgement: { type: ["string", "null"], enum: ["정상", "경계", "질환의심", null] },
          uncertain: { type: "boolean" },
        },
      },
    },
  },
};
