import { CHECKUP_ITEMS } from "@/lib/checkup-items";
import { flagged, formatDate, glance, history, printed, severity, trends, type Exam, type Item, type Member } from "@/lib/health";
import { Badge, Card, RangeBar, Sparkline, StatusDot } from "../../ui";

const TINT = { danger: "bg-danger-soft", warn: "bg-warn-soft" };
// Business: a glance shows at most this many marked items and findings before "N개 더 보기" (UI reference 2026-10-12);
// more than that and the summary card turns back into the list it was meant to replace.
const SHOW = 3;

// The latest exam, read top-down: a dot and one sentence, the counts, the first marked items with a range bar, the
// findings, then every result folded away by section. The app adds no judgement of its own (constitution III).
export function ExamView({ member, exam }: { member: Member; exam: Exam }) {
  const flags = flagged(exam);
  const { level, sentence } = glance(exam);
  const count = (f: (i: Item) => boolean) => exam.items.filter(f).length;
  const chips = [
    [count((i) => severity(i) === "danger"), "질환의심", "bg-danger-soft text-danger"],
    [count((i) => i.judgement === "경계"), "경계", "bg-warn-soft text-warn"],
    [count((i) => !i.judgement && i.flag === "H"), "높음 H", "bg-warn-soft text-warn"],
    [count((i) => !i.judgement && i.flag === "L"), "낮음 L", "bg-warn-soft text-warn"],
    [count((i) => i.judgement === "정상"), "정상", "bg-ok-soft text-ok"],
    [exam.findings.length, "소견", "bg-background text-muted"],
  ] as const;
  // Sections in the sheet's own order, merged by their display name ("골밀도 검사 (B.M.D)" and "골밀도 검사" are one);
  // items the sheet didn't group go under "기타".
  const name = (i: Item) => printed(i.section ?? "기타");
  const sections = [...new Map(exam.items.map((i) => [name(i), [] as Item[]]))];
  exam.items.forEach((i) => sections.find(([s]) => s === name(i))![1].push(i));

  const row = (i: Item, n: number) => {
    const s = severity(i)!;
    return (
      <li key={n} className={`rounded-2xl px-4 py-3 ${TINT[s]}`}>
        <div className="flex items-center gap-3">
          <div className="min-w-0 flex-1">
            <p className="text-[15px] font-semibold">{printed(i.label)}</p>
            <p className="mt-0.5 text-[22px] font-bold leading-tight">{i.value ?? i.textValue} <span className="text-xs font-normal text-muted">{i.unit}</span></p>
          </div>
          <Badge judgement={i.judgement} flag={i.flag} />
        </div>
        {i.reference && (
          <div className="mt-2 flex items-center gap-3">
            <RangeBar value={i.value} reference={i.reference} level={s} />
            <span className="shrink-0 text-xs text-muted">참고 {i.reference}</span>
          </div>
        )}
      </li>
    );
  };

  const lines = trends(member, exam);
  const trendRow = ({ item, points }: (typeof lines)[number]) => (
    <li key={item.key} className="flex items-center gap-3 py-3">
      <div className="min-w-0 flex-1">
        <p className="text-[15px] font-semibold">{printed(item.label)}</p>
        <p className="mt-0.5 text-xs text-muted">{points.map((p) => `${p.year} ${p.value}`).join(" · ")} {item.unit}</p>
      </div>
      <Sparkline values={points.map((p) => p.value)} />
    </li>
  );

  return (
    <>
      <Card>
        <div className="flex items-center gap-3">
          <StatusDot level={level} />
          <p className="flex-1 text-[19px] font-bold leading-snug break-keep">{sentence}</p>
          <p className="shrink-0 text-sm text-muted">{formatDate(exam.date)}</p>
        </div>
        <div className="mt-3 flex flex-wrap gap-1.5">
          {chips.filter(([n]) => n > 0).map(([n, label, cls]) => (
            <span key={label} className={`rounded-lg px-2 py-1 text-xs font-semibold ${cls}`}>{label} {n}</span>
          ))}
        </div>

        {flags.length > 0 && (
          <>
            <ul className="mt-4 space-y-2">{flags.slice(0, SHOW).map(row)}</ul>
            {flags.length > SHOW && (
              <details className="group">
                <summary className="flex cursor-pointer list-none items-center justify-between py-3 text-sm text-muted">
                  주의 {flags.length - SHOW}개 더 보기 <span className="inline-block transition group-open:rotate-180">⌄</span>
                </summary>
                <ul className="space-y-2">{flags.slice(SHOW).map((i, n) => row(i, n + SHOW))}</ul>
              </details>
            )}
          </>
        )}

        {exam.findings.length > 0 && (
          <div className="mt-4">
            <p className="text-sm font-semibold text-muted">결과지 소견 {exam.findings.length}개</p>
            <ul className="mt-2 space-y-1.5">
              {exam.findings.slice(0, SHOW).map((f, n) => (
                <li key={n} className="flex items-baseline gap-2 text-[15px]">
                  <span className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-warn" />
                  <span>{f.finding}{f.category && <span className="ml-2 text-xs text-muted">{printed(f.category)}</span>}</span>
                </li>
              ))}
            </ul>
            {exam.findings.length > SHOW && (
              <details className="group">
                <summary className="flex cursor-pointer list-none items-center justify-between py-3 text-sm text-muted">
                  소견 {exam.findings.length - SHOW}개 더 보기 <span className="inline-block transition group-open:rotate-180">⌄</span>
                </summary>
                <ul className="space-y-1.5">
                  {exam.findings.slice(SHOW).map((f, n) => (
                    <li key={n} className="flex items-baseline gap-2 text-[15px]">
                      <span className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-warn" />
                      <span>{f.finding}{f.category && <span className="ml-2 text-xs text-muted">{printed(f.category)}</span>}</span>
                    </li>
                  ))}
                </ul>
              </details>
            )}
          </div>
        )}
        <p className="mt-4 text-xs text-muted">결과지에 적힌 판정·표시 그대로예요. 자세한 내용은 담당 의사와 상담하세요</p>
      </Card>

      {lines.length > 0 && (
        <Card>
          <p className="text-[17px] font-semibold">추이 <span className="text-sm font-normal text-muted">{lines.length}개 항목 · 검진 {member.exams.length}회</span></p>
          <ul className="mt-2 divide-y divide-line">{lines.slice(0, SHOW).map(trendRow)}</ul>
          {lines.length > SHOW && (
            <details className="group">
              <summary className="flex cursor-pointer list-none items-center justify-between py-3 text-sm text-muted">
                추이 {lines.length - SHOW}개 더 보기 <span className="inline-block transition group-open:rotate-180">⌄</span>
              </summary>
              <ul className="divide-y divide-line">{lines.slice(SHOW).map(trendRow)}</ul>
            </details>
          )}
        </Card>
      )}

      <Card className="py-2">
        <details className="group">
          <summary className="flex cursor-pointer list-none items-center justify-between py-2 text-[15px] font-semibold">
            모든 항목 {exam.items.length}개 보기 <span className="inline-block text-muted transition group-open:rotate-180">⌄</span>
          </summary>
          <div className="divide-y divide-line">
            {sections.map(([section, list]) => {
              const marks = list.filter((i) => severity(i));
              return (
                <details key={section} className="group/s -mx-5 px-5 py-2 open:bg-background/60">
                  <summary className="flex cursor-pointer list-none items-center justify-between gap-3 py-2 text-[15px] font-semibold">
                    <span className="break-keep">{section}</span>
                    <span className="flex shrink-0 items-center gap-2 text-xs font-normal text-muted">
                      {marks.length > 0 && <span className={`rounded-md px-1.5 py-0.5 font-semibold ${marks.some((i) => severity(i) === "danger") ? "bg-danger-soft text-danger" : "bg-warn-soft text-warn"}`}>주의 {marks.length}</span>}
                      {list.length}개 <span className="inline-block transition group-open/s:rotate-180">⌄</span>
                    </span>
                  </summary>
                  <ul className="divide-y divide-line">
                    {list.map((i, n) => {
                      const s = severity(i);
                      return (
                        <li key={n} className={`flex items-center gap-3 py-3 ${s ? "" : "text-muted"}`}>
                          <div className="min-w-0 flex-1">
                            <p className="text-[15px]">{printed(i.label)}</p>
                            <p className={`mt-0.5 text-[17px] font-bold ${s ? "text-foreground" : ""}`}>{i.value ?? i.textValue} <span className="text-xs font-normal text-muted">{i.unit}</span></p>
                            {i.reference && <p className="truncate text-xs text-muted">참고치 {i.reference}</p>}
                          </div>
                          {CHECKUP_ITEMS.some((c) => c.key === i.key) && <Sparkline values={history(member, i.key).map((h) => h.value)} />}
                          {(i.judgement || i.flag) && <Badge judgement={i.judgement} flag={i.flag} />}
                        </li>
                      );
                    })}
                  </ul>
                </details>
              );
            })}
          </div>
        </details>
      </Card>
    </>
  );
}
