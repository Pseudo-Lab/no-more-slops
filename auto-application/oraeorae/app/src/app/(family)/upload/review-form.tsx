"use client";

import { useState, useTransition } from "react";
import { saveExam } from "@/app/actions";
import { track } from "@/lib/analytics";
import { CHECKUP_ITEMS } from "@/lib/checkup-items";
import { printed, severity, type Finding, type Judgement } from "@/lib/health";
import type { Extracted } from "./extract";

const JUDGEMENTS: { value: Judgement | null; label: string; on: string }[] = [
  { value: "정상", label: "정상", on: "bg-primary-soft text-primary" },
  { value: "경계", label: "경계", on: "bg-warn-soft text-warn" },
  { value: "질환의심", label: "질환의심", on: "bg-danger-soft text-danger" },
  { value: null, label: "판정 없음", on: "bg-background text-foreground ring-1 ring-line" },
];
// Only the national-checkup items have a judgement box on the sheet; other labs print H/L instead.
const CATALOG_KEYS = new Set<string>(CHECKUP_ITEMS.map((c) => c.key));

// Values stay as typed text while editing, so a field can be cleared and decimals like "1." survive until save.
// `id` is positional: printed names can repeat across sections, so `key` isn't unique.
type Draft = Omit<Extracted, "value" | "textValue"> & { id: number; value: string; isText: boolean };
const isNumber = (v: string) => v.trim() !== "" && Number.isFinite(Number(v));
// Constraint: same cap as saveExam's MAX_TEXT, checked here so the offending row is shown instead of a server error.
const MAX_TEXT = 100;
// Constraint: a judgement absent from the sheet stays absent when saved (constitution III).
const isValid = (i: Draft) => (i.isText ? i.value.trim() !== "" && i.value.length <= MAX_TEXT : isNumber(i.value));
const marked = (i: Draft) => severity(i) !== null || !!i.uncertain;
const TINT = { danger: "border-danger bg-danger-soft/60", warn: "border-warn bg-warn-soft/60" };

export function ReviewForm({ memberId, extracted, examDate, findings: extractedFindings }: {
  memberId: string; extracted: Extracted[]; examDate: string | null; findings: Finding[];
}) {
  const [items, setItems] = useState<Draft[]>(() => extracted.map((i, id) => ({
    ...i, id, isText: i.value === null, value: i.value === null ? (i.textValue ?? "") : String(i.value),
  })));
  // History: toISOString() is UTC, so before 9am in Korea the default showed yesterday. sv-SE formats the local date as YYYY-MM-DD.
  const [date, setDate] = useState(() => examDate ?? new Date().toLocaleDateString("sv-SE"));
  const [findings, setFindings] = useState(extractedFindings);
  const [error, setError] = useState("");
  const [pending, startTransition] = useTransition();
  const update = (id: number, patch: Partial<Draft>) => setItems((prev) => prev.map((i) => (i.id === id ? { ...i, ...patch } : i)));
  const invalid = items.filter((i) => !isValid(i)).length;
  // Sections in the sheet's own order, merged by display name; items the sheet didn't group go under "기타".
  const name = (i: Draft) => printed(i.section ?? "기타");
  const sections = [...new Map(items.map((i) => [name(i), [] as Draft[]]))];
  items.forEach((i) => sections.find(([s]) => s === name(i))![1].push(i));

  function save() {
    setError("");
    track("exam_save");
    startTransition(async () => {
      const result = await saveExam(
        memberId,
        date,
        items.map((i) => ({
          key: i.key, label: i.label, unit: i.unit, section: i.section, reference: i.reference, flag: i.flag, judgement: i.judgement,
          value: i.isText ? null : Number(i.value), textValue: i.isText ? i.value.trim() : null,
        })),
        findings.filter((f) => f.finding.trim()),
      );
      if (result?.error) {
        track("exam_save_error");
        setError(result.error);
      }
    });
  }

  return (
    <>
      <section className="rounded-3xl bg-card p-5">
        <label className="flex items-center justify-between text-[15px]">
          검진일
          <input type="date" required value={date} onChange={(e) => setDate(e.target.value)} className="rounded-xl bg-background px-3 py-2 text-[15px] outline-none focus:ring-2 focus:ring-primary" />
        </label>
        <p className="mt-2 text-xs text-muted">{examDate ? "결과지에 적힌 검진일이에요" : "결과지에서 검진일을 찾지 못했어요. 실제 검진일로 바꿔 주세요"}</p>
        {/* What to look at first: the counts the sheet itself marked, before the 100-item list. */}
        <div className="mt-4 flex flex-wrap gap-2 text-sm">
          <span className="rounded-xl bg-background px-3 py-1.5">항목 <b>{items.length}</b></span>
          <span className={`rounded-xl px-3 py-1.5 ${items.some((i) => severity(i) === "danger") ? "bg-danger-soft text-danger" : items.some(marked) ? "bg-warn-soft text-warn" : "bg-background text-muted"}`}>주의 <b>{items.filter((i) => severity(i)).length}</b></span>
          <span className="rounded-xl bg-background px-3 py-1.5">소견 <b>{findings.length}</b></span>
          {items.some((i) => i.uncertain) && <span className="rounded-xl bg-warn-soft px-3 py-1.5 text-warn">확인 필요 <b>{items.filter((i) => i.uncertain).length}</b></span>}
        </div>
      </section>

      <section className="rounded-3xl bg-card px-5 py-1">
        <div className="divide-y divide-line">
          {sections.map(([section, list]) => (
            // Sections the sheet marked (H/L, 경계·질환의심, unsure reads) start open; the rest fold so 100+ items stay scannable.
            <details key={section} open={list.some(marked) || list.some((i) => !isValid(i))} className="group -mx-5 px-5 py-3 open:bg-background/60">
              <summary className="flex cursor-pointer list-none items-center justify-between gap-3 py-1 text-[17px] font-bold">
                <span className="break-keep">{section} <span className="ml-1 text-xs font-normal text-muted">{list.length}개</span></span>
                <span className="shrink-0 text-xs font-normal text-muted">
                  {list.filter(marked).length > 0 && <span className={`mr-2 rounded-md px-1.5 py-0.5 text-[11px] font-semibold ${list.some((i) => severity(i) === "danger") ? "bg-danger-soft text-danger" : "bg-warn-soft text-warn"}`}>주의 {list.filter(marked).length}</span>}
                  <span className="inline-block transition group-open:rotate-180">⌄</span>
                </span>
              </summary>
              <ul className="divide-y divide-line">
                {list.map((i) => (
                  <li key={i.id} className={`py-4 ${severity(i) ? `-mx-3 my-1 rounded-2xl border-l-4 px-3 ${TINT[severity(i)!]}` : ""}`}>
                    <div className="flex items-center gap-3">
                      <label htmlFor={`v-${i.id}`} className={`min-w-0 flex-1 break-keep text-[15px] ${marked(i) ? "font-semibold" : ""}`}>
                        {printed(i.label)}
                        {i.uncertain && <span className="ml-1.5 rounded-md bg-warn-soft px-1.5 py-0.5 text-[11px] font-semibold text-warn">확인 필요</span>}
                        {i.flag && <span className="ml-1.5 rounded-md bg-warn-soft px-1.5 py-0.5 text-[11px] font-semibold text-warn">{i.flag}</span>}
                        {i.reference && <span className="mt-0.5 block truncate text-xs text-muted">참고치 {i.reference}</span>}
                      </label>
                      <input
                        id={`v-${i.id}`}
                        value={i.value}
                        onChange={(e) => update(i.id, { value: i.isText ? e.target.value : e.target.value.replace(/[^0-9.-]/g, "") })}
                        inputMode={i.isText ? "text" : "decimal"}
                        aria-invalid={!isValid(i)}
                        className={`rounded-xl bg-card px-3 py-2 text-right font-semibold outline-none ring-1 ring-line focus:ring-2 ${i.isText ? "w-40 text-[15px]" : "w-24 text-[17px]"} ${isValid(i) ? "focus:ring-primary" : "ring-2 ring-danger"}`}
                      />
                      <span className="w-11 shrink-0 text-xs text-muted">{i.unit}</span>
                      <button type="button" aria-label={`${i.label} 삭제`} onClick={() => setItems((prev) => prev.filter((p) => p.id !== i.id))} className="shrink-0 px-1 text-sm text-muted">✕</button>
                    </div>
                    {CATALOG_KEYS.has(i.key) && (
                      <>
                        <div role="radiogroup" aria-label={`${i.label} 판정`} className="mt-3 grid grid-cols-4 gap-1.5 rounded-xl">
                          {JUDGEMENTS.map((j) => (
                            <button
                              key={j.label}
                              type="button"
                              role="radio"
                              aria-checked={i.judgement === j.value}
                              onClick={() => update(i.id, { judgement: j.value })}
                              className={`rounded-lg py-1.5 text-[13px] font-semibold ${i.judgement === j.value ? j.on : "bg-background text-muted"}`}
                            >
                              {j.label}
                            </button>
                          ))}
                        </div>
                        {i.judgement === null && <p className="mt-2 text-xs text-muted">결과지에 체크된 판정이 없어요. 있다면 골라 주세요.</p>}
                      </>
                    )}
                  </li>
                ))}
              </ul>
            </details>
          ))}
        </div>
      </section>

      {findings.length > 0 && (
        <section className="rounded-3xl bg-card p-5">
          <p className="text-[15px] font-semibold">결과지 소견</p>
          <p className="mt-1 text-xs text-muted">결과지에 적힌 그대로예요. 틀리거나 필요 없는 소견은 고치거나 지워 주세요</p>
          <ul className="mt-3 space-y-2">
            {findings.map((f, n) => (
              <li key={n} className="flex items-center gap-2">
                {f.category && <span className="shrink-0 text-xs text-muted">{printed(f.category)}</span>}
                <input
                  aria-label={`소견 ${n + 1}`}
                  value={f.finding}
                  onChange={(e) => setFindings((prev) => prev.map((p, k) => (k === n ? { ...p, finding: e.target.value } : p)))}
                  className="min-w-0 flex-1 rounded-xl bg-background px-3 py-2 text-[15px] outline-none focus:ring-2 focus:ring-primary"
                />
                <button type="button" onClick={() => setFindings((prev) => prev.filter((_, k) => k !== n))} className="shrink-0 px-2 text-sm text-muted">삭제</button>
              </li>
            ))}
          </ul>
        </section>
      )}

      <p className="px-1 text-xs leading-relaxed text-muted">
        수치·참고치·H/L 표시는 결과지에 적힌 그대로예요. 결과지 원본은 저장하지 않고, 확인한 내용만 가족에게 보여드려요.
      </p>

      {/* Sticky, not fixed: on phones it rides the bottom while scrolling but never covers the last item. */}
      <div className="sticky bottom-0 -mx-5 bg-gradient-to-t from-background via-background to-transparent px-5 pt-6 pb-6 md:static md:mx-0 md:bg-none md:px-0 md:pt-2">
        {(error || invalid > 0) && (
          <p role="alert" className="mb-3 text-center text-sm text-danger">{error || `값을 확인해 주세요 (${invalid}개 항목${items.some((i) => i.isText && i.value.length > MAX_TEXT) ? ` · 글자 결과는 ${MAX_TEXT}자까지` : ""})`}</p>
        )}
        <button
          type="button"
          disabled={pending || invalid > 0 || !date || (items.length === 0 && findings.length === 0)}
          onClick={save}
          className="w-full rounded-2xl bg-primary py-4 text-[17px] font-semibold text-white disabled:bg-line disabled:text-muted"
        >
          {pending ? "저장하고 있어요…" : `${items.length}개 항목${findings.length ? ` · 소견 ${findings.length}개` : ""} 저장하기`}
        </button>
      </div>
    </>
  );
}
