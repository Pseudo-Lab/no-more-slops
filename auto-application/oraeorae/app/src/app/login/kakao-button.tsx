"use client";

import { track } from "@/lib/analytics";
import { createClient } from "@/lib/supabase/client";

export function KakaoButton({ next }: { next: string }) {
  async function signIn() {
    track("login_click");
    await createClient().auth.signInWithOAuth({
      provider: "kakao",
      options: { redirectTo: `${location.origin}/auth/callback?next=${encodeURIComponent(next)}` },
    });
  }
  return (
    <button onClick={signIn} className="w-full rounded-2xl bg-[#fee500] py-4 text-[17px] font-semibold text-[#191919]">
      카카오로 시작하기
    </button>
  );
}
