import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { Suspense } from "react";
import { deleteMember, updateMember } from "@/app/actions";
import { requireFamily } from "@/lib/family";
import { ConfirmButton } from "../../../confirm-button";
import { Skeleton } from "../../../skeleton";
import { Card } from "../../../ui";

export const metadata: Metadata = { title: "정보 수정" };

export default function EditMemberPage({ params }: PageProps<"/member/[id]/edit">) {
  return (
    <Suspense fallback={<Skeleton />}>
      <EditContent params={params} />
    </Suspense>
  );
}

const field = "mt-2 w-full rounded-xl bg-background px-4 py-3 text-[17px] outline-none focus:ring-2 focus:ring-primary";

async function EditContent({ params }: Pick<PageProps<"/member/[id]/edit">, "params">) {
  const { id } = await params;
  const { members, meId } = await requireFamily();
  const member = members.find((m) => m.id === id);
  // Only your own profile and proxy members are editable; other logged-in members manage their own.
  if (!member || (member.id !== meId && member.hasLogin)) notFound();

  return (
    <main className="space-y-3 px-5 pt-6 md:max-w-xl md:px-0 md:pt-10">
      <Link href={`/member/${member.id}`} className="inline-block px-1 py-2 text-[15px] text-muted">‹ {member.name}</Link>
      <h1 className="mb-5 px-1 text-[26px] font-bold">정보 수정</h1>

      <form action={updateMember.bind(null, member.id)} className="space-y-3">
        <Card className="space-y-5">
          <label className="block text-sm text-muted">이름
            <input name="name" required maxLength={20} defaultValue={member.name} className={field} />
          </label>
          <label className="block text-sm text-muted">관계
            <input name="relation" maxLength={20} defaultValue={member.relation} placeholder="예: 어머니" className={field} />
          </label>
          <label className="block text-sm text-muted">출생연도
            <input name="birthYear" inputMode="numeric" pattern="(19|20)[0-9]{2}" defaultValue={member.birthYear ?? ""} placeholder="예: 1962" className={field} />
          </label>
          <label className="block text-sm text-muted">다음 검진
            <input name="nextExam" maxLength={20} defaultValue={member.nextExam ?? ""} placeholder="예: 2027년 3월" className={field} />
          </label>
        </Card>
        <button className="w-full rounded-2xl bg-primary py-4 text-[17px] font-semibold text-white">저장하기</button>
      </form>

      {!member.hasLogin && (
        <form action={deleteMember.bind(null, member.id)} className="pt-4 text-center">
          <ConfirmButton label={`${member.name} 삭제하기`} title={`${member.name} 정보를 삭제할까요?`} description="검진 기록까지 모두 삭제되고 되돌릴 수 없어요" confirmLabel="삭제" className="px-4 py-3 text-sm text-muted" />
        </form>
      )}
    </main>
  );
}
