import Link from "next/link";

export default function NotFound() {
  return (
    <main className="mx-auto flex min-h-screen max-w-md flex-col items-center justify-center px-5 text-center">
      <p className="text-5xl">🔍</p>
      <h1 className="mt-6 text-[22px] font-bold">페이지를 찾을 수 없어요</h1>
      <p className="mt-2 text-[15px] text-muted">주소가 바뀌었거나, 볼 수 없는 가족의 기록이에요.</p>
      <Link href="/" className="mt-8 rounded-2xl bg-primary px-8 py-3.5 text-[15px] font-semibold text-white">홈으로</Link>
    </main>
  );
}
