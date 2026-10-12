import { CHECKUP_ITEMS } from "@/lib/checkup-items";
import { flagged, formatDate, history, printed, severity, type Exam, type Item, type Member } from "@/lib/health";
import { Badge, Card, Sparkline } from "../../ui";

const TINT = { danger: "bg-danger-soft", warn: "bg-warn-soft" };

// The latest exam, marked items first: what the sheet flagged (경계·질환의심·H/L) and its findings get the big
// treatment; the other ~100 results fold away by section. The app adds no judgement of its own (constitution III).
export function ExamView({ member, exam }: { member: Member; exam: Exam }) {
  const flags = flagged(exam);
  // Sections in the sheet's own order, merged by their display name ("골밀도 검사 (B.M.D)" and "골밀도 검사" are one);
  // items the sheet didn't group go under "기타".
  const name = (i: Item) => printed(i.section ?? "기타");
  const sections = [...new Map(exam.items.map((i) => [name(i), [] as Item[]]))];
  exam.items.forEach((i) => sections.find(([s]) => s === name(i))![1].push(i));

  return (
    <>
      <Card>
        <div className="flex items-baseline justify-between">
          <p className="text-[17px] font-bold">결과지가 표시한 것</p>
          <p className="text-sm text-muted">{formatDate(exam.date)}</p>
        </div>

        {flags.length === 0 && exam.findings.length === 0 && (
          <p className="mt-3 text-[15px] text-muted">결과지에 표시된 주의 항목이 없어요</p>
        )}

        {flags.length > 0 && (
          <ul className="mt-3 space-y-2">
            {flags.map((i, n) => (
              <li key={n} className={`flex items-center gap-3 rounded-2xl px-4 py-3 ${TINT[severity(i)!]}`}>
                <div className="min-w-0 flex-1">
                  <p className="text-[15px] font-semibold">{printed(i.label)}</p>
                  <p className="mt-0.5 text-[22px] font-bold leading-tight">{i.value ?? i.textValue} <span className="text-xs font-normal text-muted">{i.unit}</span></p>
                  {i.reference && <p className="mt-0.5 truncate text-xs text-muted">참고치 {i.reference}</p>}
                </div>
                <Badge judgement={i.judgement} flag={i.flag} />
              </li>
            ))}
          </ul>
        )}

        {exam.findings.length > 0 && (
          <div className="mt-4">
            <p className="text-sm font-semibold text-muted">소견 {exam.findings.length}개</p>
            <ul className="mt-2 space-y-1.5">
              {exam.findings.map((f, n) => (
                <li key={n} className="flex items-baseline gap-2 text-[15px]">
                  <span className="mt-2 h-1.5 w-1.5 shrink-0 rounded-full bg-warn" />
                  <span>{f.finding}{f.category && <span className="ml-2 text-xs text-muted">{printed(f.category)}</span>}</span>
                </li>
              ))}
            </ul>
          </div>
        )}
        <p className="mt-4 text-xs text-muted">결과지에 적힌 판정·표시 그대로예요. 자세한 내용은 담당 의사와 상담하세요</p>
      </Card>

      <Card className="py-2">
        <p className="px-0 py-2 text-sm font-semibold text-muted">모든 항목 {exam.items.length}개</p>
        <div className="divide-y divide-line">
          {sections.map(([section, list]) => {
            const marks = list.filter((i) => severity(i));
            return (
              <details key={section} className="group -mx-5 px-5 py-2 open:bg-background/60">
                <summary className="flex cursor-pointer list-none items-center justify-between gap-3 py-2 text-[15px] font-semibold">
                  <span className="break-keep">{section}</span>
                  <span className="flex shrink-0 items-center gap-2 text-xs font-normal text-muted">
                    {marks.length > 0 && <span className={`rounded-md px-1.5 py-0.5 font-semibold ${marks.some((i) => severity(i) === "danger") ? "bg-danger-soft text-danger" : "bg-warn-soft text-warn"}`}>주의 {marks.length}</span>}
                    {list.length}개 <span className="inline-block transition group-open:rotate-180">⌄</span>
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
      </Card>
    </>
  );
}
