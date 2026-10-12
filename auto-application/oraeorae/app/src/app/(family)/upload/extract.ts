"use server";

import { redirect } from "next/navigation";
import { CHECKUP_ITEMS } from "@/lib/checkup-items";
import { INSTRUCTIONS, SCHEMA } from "./extract-prompt";
import type { Finding, Item, Judgement } from "@/lib/health";
import { SAMPLE_EXTRACTED } from "@/lib/mock";
import { createClient } from "@/lib/supabase/server";

export type Extracted = Item & { uncertain?: boolean };
export type ExtractResult = { items: Extracted[]; examDate: string | null; findings: Finding[]; sample: boolean } | { error: string };

// Business: on a 36-page report (3 runs, 2026-10-12) luna read 17/17 values and judgements at ~5 KRW per sheet;
// gpt-5.4-mini-2026-03-17 missed a judgement in 2 of 3 runs at ~19 KRW.
// Future: luna has no dated snapshot yet, so accuracy can shift when OpenAI updates it; pin one once published.
const MODEL = "gpt-5.6-luna";

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

  const supabase = await createClient();
  const { data } = await supabase.auth.getClaims();
  const uid = data?.claims.sub;
  if (!uid) redirect("/login");
  // Constraint: sending the sheet to OpenAI (US) is a cross-border transfer; PIPA art. 28-8 needs this consent first.
  const { data: consent } = await supabase.from("consents").select("kind").eq("user_id", uid).eq("kind", "transfer").maybeSingle();
  if (!consent) return { error: "국외 이전 동의 후에 결과지를 읽을 수 있어요" };

  // Local dev reads through the Codex SDK (ChatGPT login, no key) when EXTRACT_VIA=codex; previews and a dev box
  // without either show sample values with a warning instead.
  const viaCodex = process.env.EXTRACT_VIA === "codex";
  if (!viaCodex && !process.env.OPENAI_API_KEY) return { items: SAMPLE_EXTRACTED, examDate: null, findings: [], sample: true };

  // One credit per read, taken before the paid call so a re-tap can't run up the bill. Future: no refund on failure
  // until credits are sold (#26); the owner accepted the occasional lost free credit.
  const { data: spend, error: spendError } = await supabase.rpc("spend_credit");
  if (spendError) return FAILED;
  if (spend === null) return { error: "판독 크레딧을 모두 썼어요. 충전 기능은 준비 중이에요" };

  const raw = formData.get("text");
  const reportText = typeof raw === "string" && raw ? raw : null;
  const text = viaCodex ? await (await import("./extract-codex")).askCodex(reportText, files) : await askOpenAI(reportText, files);
  if (!text) return FAILED;
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

// The production path: one Responses API call with the sheet text and page images.
async function askOpenAI(reportText: string | null, files: File[]): Promise<string | null> {
  const sheet = [
    ...(reportText ? [{ type: "input_text", text: reportText }] : []),
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
    return null;
  }

  const body = await res.json();
  // An incomplete or refused response has no usable JSON; treat it like a failed request.
  if (body.status !== "completed") return null;
  return body.output?.flatMap((o: { content?: { type: string; text?: string }[] }) => o.content ?? [])
    .find((c: { type: string }) => c.type === "output_text")?.text ?? null;
}
