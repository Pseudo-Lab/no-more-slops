"use server";

import { redirect } from "next/navigation";
import { CHECKUP_ITEMS } from "@/lib/checkup-items";
import type { Finding, Item, Judgement } from "@/lib/health";
import { SAMPLE_EXTRACTED } from "@/lib/mock";
import { createClient } from "@/lib/supabase/server";

export type Extracted = Item & { uncertain?: boolean };
export type ExtractResult = { items: Extracted[]; examDate: string | null; findings: Finding[]; sample: boolean } | { error: string };

// Business: on a 36-page report (3 runs, 2026-10-12) luna read 17/17 values and judgements at ~5 KRW per sheet;
// gpt-5.4-mini-2026-03-17 missed a judgement in 2 of 3 runs at ~19 KRW.
// Future: luna has no dated snapshot yet, so accuracy can shift when OpenAI updates it; pin one once published.
const MODEL = "gpt-5.6-luna";

// Kept identical across requests (no per-user text) so OpenAI can cache it as the prompt prefix.
const INSTRUCTIONS = `한국 건강검진 결과지에 적힌 검사 결과를 빠짐없이 옮겨요.
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

const SCHEMA = {
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

type RawItem = {
  section: string | null; key: string; label: string; value: number | null; text_value: string | null;
  unit: string; reference: string | null; flag: "H" | "L" | null; judgement: Judgement | null; uncertain: boolean;
};

const FAILED = { error: "지금은 결과지를 읽을 수 없어요. 잠시 후 다시 눌러 주세요" };

const clean = (s: string | null | undefined) => s?.trim() || null;

// Constraint: the sheet lives only in this request's memory — never stored or logged (privacy policy, constitution I).
export async function extractSheet(formData: FormData): Promise<ExtractResult> {
  // PDFs arrive already parsed on the device: the report text plus one image per page that must be read as pixels.
  const files = formData.getAll("file").filter((f): f is File => f instanceof File && f.type.startsWith("image/"));
  if (files.length === 0) return { error: "사진이나 PDF 파일을 골라 주세요" };
  const reportText = formData.get("text");

  const supabase = await createClient();
  const { data } = await supabase.auth.getClaims();
  const uid = data?.claims.sub;
  if (!uid) redirect("/login");
  // Constraint: sending the sheet to OpenAI (US) is a cross-border transfer; PIPA art. 28-8 needs this consent first.
  const { data: consent } = await supabase.from("consents").select("kind").eq("user_id", uid).eq("kind", "transfer").maybeSingle();
  if (!consent) return { error: "국외 이전 동의 후에 결과지를 읽을 수 있어요" };

  // Future: local dev and previews have no key; the review step shows sample values with a warning instead.
  if (!process.env.OPENAI_API_KEY) return { items: SAMPLE_EXTRACTED, examDate: null, findings: [], sample: true };

  // One credit per read, taken before the paid call so a re-tap can't run up the bill. Future: no refund on failure
  // until credits are sold (#26); the owner accepted the occasional lost free credit.
  const { data: spend, error: spendError } = await supabase.rpc("spend_credit");
  if (spendError) return FAILED;
  if (spend === null) return { error: "판독 크레딧을 모두 썼어요. 충전 기능은 준비 중이에요" };

  const sheet = [
    ...(typeof reportText === "string" && reportText ? [{ type: "input_text", text: reportText }] : []),
    ...(await Promise.all(files.map(async (f) => ({
      type: "input_image",
      image_url: `data:${f.type};base64,${Buffer.from(await f.arrayBuffer()).toString("base64")}`,
      detail: "high",
    })))),
  ];

  const request = () => fetch("https://api.openai.com/v1/responses", {
    method: "POST",
    headers: { Authorization: `Bearer ${process.env.OPENAI_API_KEY}`, "Content-Type": "application/json" },
    body: JSON.stringify({
      model: MODEL,
      // Constraint: keep the sheet out of OpenAI's stored responses; only their abuse-monitoring retention applies.
      store: false,
      instructions: INSTRUCTIONS,
      // Copying printed numbers needs no reasoning; reasoning tokens would only add cost and latency.
      reasoning: { effort: "none" },
      input: [{ role: "user", content: sheet }],
      text: { format: { type: "json_schema", name: "checkup_sheet", strict: true, schema: SCHEMA } },
    }),
  }).catch(() => null);
  // Rate limits and 5xx are usually momentary; one retry spares the user a manual re-tap.
  let res = await request();
  if (!res || res.status === 429 || res.status >= 500) res = await request();
  if (!res?.ok) {
    console.error("extractSheet: OpenAI request failed", res?.status);
    return FAILED;
  }

  const body = await res.json();
  // An incomplete or refused response has no usable JSON; treat it like a failed request.
  if (body.status !== "completed") return FAILED;
  const text = body.output?.flatMap((o: { content?: { type: string; text?: string }[] }) => o.content ?? [])
    .find((c: { type: string }) => c.type === "output_text")?.text;
  let out: { exam_date: string | null; items: RawItem[]; findings: Finding[] };
  try {
    out = JSON.parse(text);
  } catch {
    return FAILED;
  }
  const extracted: Extracted[] = out.items.flatMap((i) => {
    // Catalog items keep the catalog's label and unit so trends across years and labs line up.
    const catalog = CHECKUP_ITEMS.find((c) => c.key === i.key);
    const label = catalog?.label ?? clean(i.label);
    const value = typeof i.value === "number" && Number.isFinite(i.value) ? i.value : null;
    const textValue = value === null ? clean(i.text_value) : null;
    if (!label || (value === null && !textValue)) return [];
    return [{
      key: catalog?.key ?? label, label, unit: catalog?.unit ?? i.unit.trim(), section: clean(i.section),
      value, textValue, reference: clean(i.reference), flag: i.flag, judgement: i.judgement, uncertain: i.uncertain,
    }];
  });
  // The same finding is printed differently across pages ("융합척추" on the CT page, "융합척추 의심" in the summary); keep the longer one.
  const findings = out.findings
    .map((f) => ({ category: clean(f.category), finding: f.finding.trim() }))
    // Normal-range lines are not findings (the rule says so, but the model sometimes keeps a qualified "정상범위(...)").
    .filter((f, n, all) => f.finding && !/^정상/.test(f.finding) && !all.some((g, k) => k !== n && g.finding !== f.finding && g.finding.startsWith(f.finding)))
    .filter((f, n, all) => all.findIndex((g) => g.finding === f.finding) === n);
  if (extracted.length === 0 && findings.length === 0) return { error: "결과지에서 수치를 찾지 못했어요. 결과지 전체가 선명하게 나오게 다시 찍어 주세요" };
  // The date pre-fills an editable field, so anything that isn't a real YYYY-MM-DD just falls back to today.
  const examDate = /^\d{4}-\d{2}-\d{2}$/.test(out.exam_date ?? "") && !isNaN(Date.parse(out.exam_date!)) ? out.exam_date : null;
  return { items: extracted, examDate, findings, sample: false };
}
