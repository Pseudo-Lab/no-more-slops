import type { Metadata } from "next";
import Link from "next/link";
import { Suspense } from "react";
import { signOut } from "@/app/actions";
import { ConfirmButton } from "../confirm-button";
import { CONSENTS } from "@/lib/consents";
import { requireFamily } from "@/lib/family";
import { SERVICE } from "@/lib/service";
import { kakaoProfile } from "@/lib/kakao-profile";
import { createClient } from "@/lib/supabase/server";
import { Skeleton } from "../skeleton";
import { Card } from "../ui";

export const metadata: Metadata = { title: "설정" };

export default function SettingsPage() {
  return (
    <Suspense fallback={<Skeleton />}>
      <SettingsContent />
    </Suspense>
  );
}

const row = "flex items-center justify-between py-4 text-[15px]";

async function SettingsContent() {
  const { members, meId } = await requireFamily();
  const me = members.find((m) => m.id === meId)!;
  const supabase = await createClient();
  const { data: consents } = await supabase.from("consents").select("kind, agreed_at");
  const agreedAt = new Map((consents ?? []).map((c) => [c.kind, c.agreed_at.slice(0, 10).replaceAll("-", ".")]));
  const kakao = await kakaoProfile();

  return (
    <main className="space-y-3 px-5 pt-6 md:max-w-xl md:px-0 md:pt-10">
      <Link href="/" className="inline-block px-1 py-2 text-[15px] text-muted md:hidden">‹ 홈</Link>
      <h1 className="mb-5 px-1 text-[26px] font-bold">설정</h1>

      <Card>
        <div className="flex items-center gap-3">
          <div className="flex h-11 w-11 items-center justify-center rounded-full bg-primary-soft text-lg font-bold text-primary">{me.name[0]}</div>
          <div className="flex-1">
            <p className="text-[17px] font-semibold">{me.name}</p>
            <p className="text-sm text-muted">가족에게 이렇게 보여요</p>
          </div>
          <Link href={`/member/${me.id}/edit`} className="text-sm font-semibold text-primary">수정</Link>
        </div>
      </Card>

      {kakao && (
        <Card>
          <p className="text-[17px] font-semibold">카카오 계정</p>
          <div className="mt-3 flex items-center gap-3">
            {kakao.avatarUrl ? (
              // One small avatar straight from Kakao's CDN; next/image would need a remote-host allowlist for it.
              // eslint-disable-next-line @next/next/no-img-element
              <img src={kakao.avatarUrl} alt="" width={44} height={44} className="h-11 w-11 rounded-full object-cover" />
            ) : (
              <div className="flex h-11 w-11 items-center justify-center rounded-full bg-[#fee500] text-lg font-bold text-[#191919]">{kakao.nickname?.[0] ?? "K"}</div>
            )}
            <div className="min-w-0 flex-1">
              <p className="truncate text-[15px] font-semibold">{kakao.nickname ?? "닉네임 없음"}</p>
              {kakao.email && <p className="truncate text-sm text-muted">{kakao.email}</p>}
            </div>
          </div>
          <p className="mt-3 text-xs text-muted">로그인할 때 카카오에서 받은 정보예요. 카카오에서 바꾸면 다음 로그인에 반영돼요.</p>
        </Card>
      )}

      <Card>
        <p className="text-[17px] font-semibold">동의 내역</p>
        <ul className="mt-2 divide-y divide-line">
          {CONSENTS.map((c) => (
            <li key={c.id} className={row}>
              <span>{c.title}</span>
              <span className="text-sm text-muted">{agreedAt.get(c.id) ? `${agreedAt.get(c.id)} 동의` : "동의 안 함"}</span>
            </li>
          ))}
        </ul>
        <p className="mt-2 text-xs text-muted">동의를 철회하려면 회원 탈퇴를 해 주세요. 건강정보 없이는 서비스를 쓸 수 없어요.</p>
      </Card>

      <Card className="py-1">
        <ul className="divide-y divide-line">
          <li><Link href="/terms" className={row}>이용약관 <span className="text-muted">›</span></Link></li>
          <li><Link href="/privacy" className={row}>개인정보처리방침 <span className="text-muted">›</span></Link></li>
          <li><a href={`mailto:${SERVICE.contact}`} className={row}>문의하기 <span className="text-sm text-muted">{SERVICE.contact}</span></a></li>
        </ul>
      </Card>

      <Card className="py-1">
        <form action={signOut}>
          <ConfirmButton label="로그아웃" title="로그아웃할까요?" description="다시 쓰려면 카카오로 다시 로그인하면 돼요" confirmLabel="로그아웃" danger={false} className={`${row} w-full text-left`} />
        </form>
      </Card>

      <Link href="/settings/leave" className="block px-1 py-3 text-sm text-muted underline">회원 탈퇴</Link>
    </main>
  );
}
