import { redirect } from "next/navigation";
import { Suspense } from "react";
import { startFamily } from "@/app/actions";
import { ConsentForm } from "@/app/consent/consent-form";
import { getFamily } from "@/lib/family";
import { kakaoProfile } from "@/lib/kakao-profile";

export default function StartPage() {
  return (
    <main className="mx-auto max-w-md space-y-3 px-5 pt-16 pb-10">
      <header className="mb-8 px-1">
        <h1 className="text-[26px] font-bold leading-tight">우리 가족 기록을<br />시작해요</h1>
        <p className="mt-2 text-sm text-muted">시작한 뒤 가족을 초대하거나, 부모님을 직접 추가할 수 있어요</p>
      </header>
      <Suspense>
        <Start />
      </Suspense>
    </main>
  );
}

async function Start() {
  if (await getFamily()) redirect("/");
  // The Kakao nickname is only a starting point; parents are usually entered as "엄마", "아빠".
  return <ConsentForm action={startFamily} submitLabel="시작하기" event="family_create" defaultName={(await kakaoProfile())?.nickname} />;
}
