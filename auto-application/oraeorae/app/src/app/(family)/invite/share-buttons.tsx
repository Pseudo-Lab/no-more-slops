"use client";

import { useState } from "react";
import { track } from "@/lib/analytics";
import { SERVICE } from "@/lib/service";

export function ShareButtons({ url }: { url: string }) {
  const [copied, setCopied] = useState(false);
  async function copy() {
    track("invite_copy");
    await navigator.clipboard.writeText(url);
    setCopied(true);
  }
  // Future: Web Share opens the OS share sheet (KakaoTalk included on phones); a Kakao SDK share needs a registered JS key.
  async function share() {
    track("invite_share");
    if (navigator.share) await navigator.share({ title: SERVICE.name, text: `${SERVICE.name}에서 우리 가족 건강검진 기록을 함께 봐요`, url });
    else await copy();
  }
  return (
    <div className="mt-4 grid grid-cols-2 gap-2">
      <button onClick={share} className="rounded-2xl bg-primary py-4 text-[17px] font-semibold text-white">공유하기</button>
      <button onClick={copy} className="rounded-2xl bg-background py-4 text-[17px] font-semibold">{copied ? "복사했어요" : "링크 복사"}</button>
    </div>
  );
}
