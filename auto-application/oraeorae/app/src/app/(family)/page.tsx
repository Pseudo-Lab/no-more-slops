import Link from "next/link";
import { Suspense } from "react";
import { requireFamily } from "@/lib/family";
import { flagged, formatDate, glance, latest } from "@/lib/health";
import { Skeleton } from "./skeleton";
import { BottomButton, Card, StatusDot } from "./ui";

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
      {/* One line per person (UI reference 2026-10-12): the dot colour says who to look at first, the counts say why. */}
      <Card className="py-1">
        <ul className="divide-y divide-line">
          {members.map((m) => {
            const exam = latest(m);
            const { level, counts } = glance(exam);
            return (
              <li key={m.id}>
                <Link href={`/member/${m.id}`} className="flex items-center gap-3 py-3.5">
                  <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-full bg-primary-soft text-lg font-bold text-primary">{m.name[0]}</div>
                  <div className="min-w-0 flex-1">
                    <p className="flex items-center gap-2 text-[17px] font-semibold"><StatusDot level={level} />{m.name} {m.age && <span className="text-sm font-normal text-muted">{m.age}세</span>}</p>
                    <p className="truncate text-sm text-muted">{counts}{!exam && m.nextExam ? ` · 다음 검진 ${m.nextExam}` : ""}</p>
                  </div>
                  <span className="shrink-0 text-sm text-muted">{exam ? formatDate(exam.date) : "›"}</span>
                </Link>
              </li>
            );
          })}
        </ul>
      </Card>

      <BottomButton href="/upload">결과지 올리기</BottomButton>
    </main>
  );
}
