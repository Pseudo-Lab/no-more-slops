import { headers } from "next/headers";
import Link from "next/link";
import { Suspense } from "react";
import { addMember, renewInvite } from "@/app/actions";
import { requireFamily } from "@/lib/family";
import { Skeleton } from "../skeleton";
import { Card } from "../ui";
import { ShareButtons } from "./share-buttons";

export default function InvitePage() {
  return (
    <Suspense fallback={<Skeleton />}>
      <InviteContent />
    </Suspense>
  );
}

async function InviteContent() {
  const family = await requireFamily();
  const h = await headers();
  const url = `${h.get("x-forwarded-proto") ?? "http"}://${h.get("host")}/join/${family.inviteCode}`;
  const expired = new Date(family.inviteExpiresAt) < new Date();
  const until = family.inviteExpiresAt.slice(0, 10).replaceAll("-", ".");

  return (
    <main className="space-y-3 px-5 pt-6 md:max-w-xl md:px-0 md:pt-10">
      <Link href="/" className="inline-block px-1 py-2 text-[15px] text-muted md:hidden">‹ 가족</Link>
      <header className="mb-5 px-1">
        <h1 className="text-[26px] font-bold leading-tight">가족을 초대해 주세요</h1>
        <p className="mt-2 text-sm text-muted">초대받은 가족은 자기 결과를 직접 올리고, 우리 가족의 기록을 함께 볼 수 있어요</p>
      </header>

      <Card>
        <div className="flex items-baseline justify-between">
          <p className="text-sm text-muted">{expired ? "초대 링크가 만료됐어요" : `초대 링크 · ${until}까지`}</p>
          <form action={renewInvite.bind(null, family.id)}>
            <button className="text-sm font-semibold text-primary">새 링크 만들기</button>
          </form>
        </div>
        {!expired && (
          <>
            <p className="mt-2 break-all rounded-2xl bg-background px-4 py-3 text-[15px]">{url}</p>
            <ShareButtons url={url} />
          </>
        )}
      </Card>

      <Card>
        <p className="text-[17px] font-semibold">우리 가족 {family.members.length}명</p>
        <ul className="mt-2 divide-y divide-line">
          {family.members.map((m) => (
            <li key={m.id} className="flex items-center gap-3 py-3">
              <span className="flex h-10 w-10 items-center justify-center rounded-full bg-background font-bold">{m.name[0]}</span>
              <span className="flex-1 text-[15px]">{m.name}{m.id === family.meId && <span className="text-muted"> (나)</span>}</span>
              <span className={`text-sm ${m.hasLogin ? "text-primary" : "text-muted"}`}>{m.hasLogin ? "참여 중" : "대신 기록"}</span>
            </li>
          ))}
        </ul>
      </Card>

      <Card>
        <p className="text-[17px] font-semibold">직접 추가하기</p>
        <p className="mt-1 text-sm text-muted">부모님이 앱을 쓰기 어려우시면, 동의를 받은 뒤 대신 기록할 수 있어요</p>
        <form action={addMember.bind(null, family.id)} className="mt-4 grid grid-cols-[1fr_1fr_88px] gap-2">
          <input name="name" required maxLength={20} placeholder="이름" className="min-w-0 rounded-xl bg-background px-3 py-3 text-[15px] outline-none focus:ring-2 focus:ring-primary" />
          <input name="relation" maxLength={20} placeholder="관계 (예: 엄마)" className="min-w-0 rounded-xl bg-background px-3 py-3 text-[15px] outline-none focus:ring-2 focus:ring-primary" />
          <input name="birthYear" inputMode="numeric" pattern="[0-9]{4}" placeholder="출생연도" className="min-w-0 rounded-xl bg-background px-3 py-3 text-[15px] outline-none focus:ring-2 focus:ring-primary" />
          <label className="col-span-3 flex items-center gap-2 px-1 py-1 text-sm text-muted">
            <input type="checkbox" required className="accent-[var(--primary)]" /> 본인에게 건강정보 기록과 가족 공유에 대한 동의를 받았어요
          </label>
          <button className="col-span-3 rounded-2xl bg-background py-3.5 text-[15px] font-semibold">추가하기</button>
        </form>
      </Card>
    </main>
  );
}
