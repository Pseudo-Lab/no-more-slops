import Link from "next/link";
import { Suspense } from "react";
import { requireFamily } from "@/lib/family";
import { flagged, formatDate, latest, printed, severity } from "@/lib/health";
import { Skeleton } from "./skeleton";
import { Badge, BottomButton, Card } from "./ui";

export default function Home() {
  return (
    <Suspense fallback={<Skeleton />}>
      <HomeContent />
    </Suspense>
  );
}

async function HomeContent() {
  const { members } = await requireFamily();
  const attention = members.flatMap((m) => flagged(latest(m)).filter((i) => i.judgement === "질환의심").map((i) => ({ m, i })));
  const upcoming = members.filter((m) => m.nextExam).sort((a, b) => a.nextExam!.localeCompare(b.nextExam!))[0];
  const hasExams = members.some((m) => m.exams.length > 0);

  return (
    <main className="space-y-3 px-5 pt-8 md:px-0 md:pt-10">
      <header className="mb-5 flex items-start justify-between px-1">
        <div>
          <p className="text-sm text-muted">우리 가족 · {members.length}명</p>
          <h1 className="mt-1 text-[26px] font-bold leading-tight">가족 건강, 함께 챙겨요</h1>
        </div>
        <Link href="/settings" aria-label="설정" className="rounded-xl px-2 py-1 text-[22px] text-muted md:hidden">⚙︎</Link>
      </header>

      {hasExams ? (
        <div className="grid gap-3 md:grid-cols-[2fr_1fr]">
          <Card>
            <p className="text-sm text-muted">지금 확인이 필요해요</p>
            {attention.length > 0 ? (
              <>
                <p className="mt-1 text-[22px] font-bold"><span className="text-danger">{attention.length}개</span> 항목이 질환의심이에요</p>
                <ul className="mt-4 space-y-3">
                  {attention.map(({ m, i }) => (
                    <li key={m.id + i.key} className="flex items-center justify-between">
                      <span className="text-[15px]">{m.name} · {i.label}</span>
                      <span className="text-[15px] font-semibold">{i.value} <span className="text-xs font-normal text-muted">{i.unit}</span></span>
                    </li>
                  ))}
                </ul>
              </>
            ) : (
              <p className="mt-1 text-[22px] font-bold">질환의심 항목이 없어요</p>
            )}
            <p className="mt-4 text-xs text-muted">결과지에 적힌 판정이에요. 자세한 건 의사와 상담해 주세요.</p>
          </Card>
          <Card className="flex items-center justify-between md:flex-col md:items-start md:justify-between md:gap-6">
            <div>
              <p className="text-sm text-muted">다음 검진</p>
              <p className="mt-1 text-[17px] font-semibold">{upcoming ? `${upcoming.name} · ${upcoming.nextExam}` : "아직 정하지 않았어요"}</p>
            </div>
          </Card>
        </div>
      ) : (
        <Card>
          <p className="text-[22px] font-bold leading-snug">첫 결과지를 올려 볼까요?</p>
          <p className="mt-2 text-[15px] text-muted">건강검진 결과지 사진을 올리면 AI가 수치를 읽어 정리해요</p>
        </Card>
      )}

      <div className="flex items-baseline justify-between px-1 pt-4">
        <h2 className="text-[17px] font-bold">가족</h2>
        <Link href="/invite" className="text-sm font-semibold text-primary">+ 초대하기</Link>
      </div>
      <div className="grid gap-3 md:grid-cols-2">
        {members.map((m) => {
          const exam = latest(m);
          const flags = flagged(exam);
          return (
            <Link key={m.id} href={`/member/${m.id}`} className="block">
              <Card className="h-full transition hover:shadow-sm active:scale-[0.98]">
                <div className="flex items-center gap-3">
                  <div className="flex h-11 w-11 items-center justify-center rounded-full bg-primary-soft text-lg font-bold text-primary">{m.name[0]}</div>
                  <div className="flex-1">
                    <p className="flex items-center gap-2 text-[17px] font-semibold">
                      {m.name} {m.age && <span className="text-sm font-normal text-muted">{m.age}세</span>}
                      {flags.length > 0 && <span className={`rounded-md px-1.5 py-0.5 text-xs font-semibold ${flags.some((i) => severity(i) === "danger") ? "bg-danger-soft text-danger" : "bg-warn-soft text-warn"}`}>주의 {flags.length}</span>}
                    </p>
                    <p className="text-sm text-muted">{exam ? `최근 검진 ${formatDate(exam.date)}` : "아직 기록이 없어요"}</p>
                  </div>
                  <span className="text-muted">›</span>
                </div>
                {exam && (flags.length > 0 ? (
                  <div className="mt-4 flex flex-wrap gap-2">
                    {/* Four chips keep the card one glance; the member page lists the rest. */}
                    {flags.slice(0, 4).map((i, n) => (
                      <span key={n} className="flex items-center gap-1.5 rounded-xl bg-background px-3 py-1.5 text-sm">
                        {printed(i.label)} <Badge judgement={i.judgement} flag={i.flag} />
                      </span>
                    ))}
                    {flags.length > 4 && <span className="rounded-xl bg-background px-3 py-1.5 text-sm text-muted">+{flags.length - 4}</span>}
                  </div>
                ) : exam.findings.length === 0 && (
                  <p className="mt-4 text-sm text-muted">결과지에 표시된 주의 항목이 없어요</p>
                ))}
                {exam && exam.findings.length > 0 && <p className="mt-3 text-sm text-muted">결과지 소견 {exam.findings.length}개</p>}
              </Card>
            </Link>
          );
        })}
      </div>

      <BottomButton href="/upload">결과지 올리기</BottomButton>
    </main>
  );
}
