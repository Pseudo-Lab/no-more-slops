import Link from "next/link";
import { notFound } from "next/navigation";
import { Suspense } from "react";
import { deleteExam } from "@/app/actions";
import { requireFamily } from "@/lib/family";
import { flagged, formatDate, latest } from "@/lib/health";
import { ConfirmButton } from "../../confirm-button";
import { Skeleton } from "../../skeleton";
import { BottomButton, Card } from "../../ui";
import { ExamView } from "./exam-view";

// Constraint: with cacheComponents, params must be awaited inside Suspense so the shell can prerender.
export default function MemberPage({ params }: PageProps<"/member/[id]">) {
  return (
    <Suspense fallback={<Skeleton />}>
      <MemberContent params={params} />
    </Suspense>
  );
}

async function MemberContent({ params }: Pick<PageProps<"/member/[id]">, "params">) {
  const { id } = await params;
  const { members, meId } = await requireFamily();
  const member = members.find((m) => m.id === id);
  if (!member) notFound();
  const exam = latest(member);

  return (
    <main className="space-y-3 px-5 pt-6 md:px-0 md:pt-10">
      <Link href="/" className="inline-block px-1 py-2 text-[15px] text-muted md:hidden">‹ 가족</Link>
      <header className="mb-5 flex items-start justify-between gap-3 px-1">
        <div>
          <h1 className="text-[26px] font-bold">{member.name}의 건강</h1>
          <p className="mt-1 text-sm text-muted">{[member.relation, member.age && `${member.age}세`, `검진 ${member.exams.length}회`].filter(Boolean).join(" · ")}</p>
        </div>
        {(member.id === meId || !member.hasLogin) && (
          <Link href={`/member/${member.id}/edit`} className="shrink-0 rounded-xl bg-card px-3 py-2 text-sm font-semibold">정보 수정</Link>
        )}
      </header>

      {exam ? (
        <div className="grid items-start gap-3 md:grid-cols-[1fr_300px]">
          <div className="space-y-3">
            <ExamView member={member} exam={exam} />
          </div>
          <Card>
            <p className="text-[17px] font-semibold">지난 검진</p>
            <ul className="mt-2 divide-y divide-line">
              {[...member.exams].reverse().map((e) => (
                <li key={e.id} className="flex items-center gap-3 py-3 text-[15px]">
                  <span className="flex-1">{formatDate(e.date)}</span>
                  <span className="text-muted">주의 {flagged(e).length}개</span>
                  <form action={deleteExam.bind(null, member.id, e.id)}>
                    <ConfirmButton label="삭제" title={`${formatDate(e.date)} 검진 기록을 삭제할까요?`} description="삭제하면 되돌릴 수 없어요" confirmLabel="삭제" className="text-xs text-muted" />
                  </form>
                </li>
              ))}
            </ul>
          </Card>
        </div>
      ) : (
        <Card><p className="text-[15px] text-muted">아직 올린 결과지가 없어요</p></Card>
      )}

      <BottomButton href={`/upload?member=${member.id}`}>{member.name} 결과지 올리기</BottomButton>
    </main>
  );
}
