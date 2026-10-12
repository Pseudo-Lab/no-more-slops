"use client";

import Link from "next/link";

export default function Error({ reset }: { error: Error & { digest?: string }; reset: () => void }) {
  return (
    <main className="mx-auto flex min-h-screen max-w-md flex-col items-center justify-center px-5 text-center">
      <p className="text-5xl">😵</p>
      <h1 className="mt-6 text-[22px] font-bold">잠시 문제가 생겼어요</h1>
      <p className="mt-2 text-[15px] text-muted">입력한 내용은 저장되지 않았을 수 있어요. 다시 시도해 주세요.</p>
      <div className="mt-8 flex gap-2">
        <button onClick={reset} className="rounded-2xl bg-primary px-6 py-3.5 text-[15px] font-semibold text-white">다시 시도</button>
        <Link href="/" className="rounded-2xl bg-card px-6 py-3.5 text-[15px] font-semibold">홈으로</Link>
      </div>
    </main>
  );
}
