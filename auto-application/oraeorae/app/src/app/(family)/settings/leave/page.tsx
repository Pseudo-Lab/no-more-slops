import type { Metadata } from "next";
import Link from "next/link";
import { Suspense } from "react";
import { deleteAccount } from "@/app/actions";
import { requireFamily } from "@/lib/family";
import { Skeleton } from "../../skeleton";
import { ConfirmButton } from "../../confirm-button";
import { Card } from "../../ui";

export const metadata: Metadata = { title: "회원 탈퇴" };

export default function LeavePage() {
  return (
    <Suspense fallback={<Skeleton />}>
      <LeaveContent />
    </Suspense>
  );
}

async function LeaveContent() {
  const { members, meId } = await requireFamily();
  const others = members.filter((m) => m.id !== meId && m.hasLogin).length;
  const proxies = members.filter((m) => !m.hasLogin).length;

  return (
    <main className="space-y-3 px-5 pt-6 md:max-w-xl md:px-0 md:pt-10">
      <Link href="/settings" className="inline-block px-1 py-2 text-[15px] text-muted">‹ 설정</Link>
      <header className="mb-5 px-1">
        <h1 className="text-[26px] font-bold leading-tight">정말 탈퇴할까요?</h1>
        <p className="mt-2 text-sm text-muted">탈퇴하면 되돌릴 수 없어요</p>
      </header>

      <Card>
        <p className="text-[17px] font-semibold">바로 삭제돼요</p>
        <ul className="mt-3 list-disc space-y-1.5 pl-5 text-[15px]">
          <li>내 계정과 동의 내역</li>
          <li>내 프로필과 내 검진 기록</li>
          {others === 0 && <li className="text-danger">가족 그룹 전체 ({proxies > 0 ? `대신 기록한 ${proxies}명 포함` : "다른 가족 없음"})</li>}
        </ul>
        {others > 0 && proxies > 0 && (
          <>
            <p className="mt-5 text-[17px] font-semibold">가족에게 남아요</p>
            <p className="mt-2 text-[15px] text-muted">대신 기록한 가족 {proxies}명의 기록은 남은 가족 {others}명이 계속 볼 수 있어요.</p>
          </>
        )}
      </Card>

      <form action={deleteAccount} className="space-y-3">
        <label className="flex items-center gap-2 px-1 py-2 text-[15px]">
          <input type="checkbox" required className="h-4 w-4 accent-[var(--danger)]" /> 위 내용을 확인했고, 탈퇴할게요
        </label>
        <ConfirmButton label="탈퇴하기" title="정말 탈퇴할까요?" description="계정과 내 검진 기록이 바로 삭제되고 되돌릴 수 없어요" confirmLabel="탈퇴하기" className="w-full rounded-2xl bg-danger py-4 text-[17px] font-semibold text-white" />
      </form>
    </main>
  );
}
