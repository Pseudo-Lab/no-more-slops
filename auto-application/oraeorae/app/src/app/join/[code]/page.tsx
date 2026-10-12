import { redirect } from "next/navigation";
import { Suspense } from "react";
import { joinFamily } from "@/app/actions";
import { ConsentForm } from "@/app/consent/consent-form";
import { KakaoButton } from "@/app/login/kakao-button";
import { getFamily } from "@/lib/family";
import { kakaoProfile } from "@/lib/kakao-profile";
import { createClient } from "@/lib/supabase/server";

export default function JoinPage({ params }: PageProps<"/join/[code]">) {
  return (
    <main className="mx-auto max-w-md space-y-3 px-5 pt-16 pb-10">
      <header className="mb-8 px-1">
        <p className="text-4xl">👨‍👩‍👧‍👦</p>
        <h1 className="mt-4 text-[26px] font-bold leading-tight">가족 건강 기록에<br />초대받았어요</h1>
        <p className="mt-2 text-sm text-muted">가족이 함께 건강검진 결과를 모아 보고 있어요</p>
      </header>
      <Suspense>
        <Join params={params} />
      </Suspense>
    </main>
  );
}

async function Join({ params }: Pick<PageProps<"/join/[code]">, "params">) {
  const { code } = await params;
  const supabase = await createClient();
  const { data } = await supabase.auth.getClaims();
  if (!data?.claims) return <KakaoButton next={`/join/${code}`} />;
  if (await getFamily()) redirect("/");
  return <ConsentForm action={joinFamily.bind(null, code)} submitLabel="가족에 참여하기" event="family_join" defaultName={(await kakaoProfile())?.nickname} />;
}
