import type { Metadata } from "next";
import Image from "next/image";
import { redirect } from "next/navigation";
import { Suspense } from "react";
import { Badge, Sparkline } from "@/app/(family)/ui";
import { SiteFooter } from "@/app/site-footer";
import { SERVICE } from "@/lib/service";
import { createClient } from "@/lib/supabase/server";
import { KakaoButton } from "./kakao-button";

export const metadata: Metadata = { title: { absolute: `${SERVICE.name} · ${SERVICE.tagline}` } };

const WORRIES = ["엄마 작년 혈당이 얼마였더라?", "아빠 대장내시경은 언제 했지?", "결과지를 어디 뒀더라…"];

const FEATURES = [
  { icon: "📷", title: "사진 한 장으로 기록", body: "결과지를 찍어 올리면 AI가 수치를 읽어요. 저장하기 전에 결과지와 한 번 더 확인해요." },
  { icon: "👨‍👩‍👧", title: "가족이 함께 봐요", body: "초대 링크로 가족을 모아요. 스마트폰이 어려운 부모님은 자녀가 대신 기록할 수 있어요." },
  { icon: "📈", title: "해마다 변화를 한눈에", body: "주의가 필요한 항목을 먼저 보여 주고, 해마다 수치가 어떻게 변했는지 그래프로 보여 줘요." },
];

const STEPS = [
  { title: "카카오로 시작", body: "가입은 카카오 계정 하나면 돼요" },
  { title: "가족 초대", body: "링크를 보내거나 부모님을 직접 추가해요" },
  { title: "결과지 올리기", body: "사진이나 PDF를 올리고 수치를 확인해요" },
];

const TRUST = [
  { title: "원본은 저장하지 않아요", body: "결과지 사진은 수치를 읽는 데에만 쓰고 바로 지워요." },
  { title: "우리 가족만 볼 수 있어요", body: "같은 가족 그룹에 참여한 사람만 기록을 볼 수 있어요." },
  { title: "판정을 지어내지 않아요", body: "결과지에 적힌 판정을 그대로 보여 주고, 의료 판단은 하지 않아요." },
  { title: "언제든 지울 수 있어요", body: "탈퇴하면 내 정보와 기록을 바로 삭제해요." },
];

const FAQ = [
  { q: "부모님이 스마트폰을 잘 못 쓰셔도 되나요?", a: "네. 자녀가 부모님을 가족으로 추가하고 대신 결과지를 올릴 수 있어요. 이때는 부모님께 미리 동의를 받아 주세요." },
  { q: "어떤 결과지를 올릴 수 있나요?", a: "국가건강검진 결과통보서나 병원 종합검진 결과지를 사진 또는 PDF로 올릴 수 있어요." },
  { q: "AI가 읽은 수치가 틀리면요?", a: "저장하기 전에 모든 수치와 판정을 직접 고칠 수 있어요. 결과지와 꼭 대조해 주세요." },
  { q: "건강 상태를 판단해 주나요?", a: "아니요. 결과지에 적힌 정상·경계·질환의심 판정만 보여 줘요. 건강에 관한 판단은 의사와 상담해 주세요." },
  { q: "탈퇴하면 기록은 어떻게 되나요?", a: "내 정보와 내 검진 기록은 바로 삭제해요. 부모님처럼 대신 기록한 가족의 정보는 남은 가족을 위해 그대로 남아요." },
];

export default function LandingPage({ searchParams }: PageProps<"/login">) {
  return (
    <>
      <header className="mx-auto flex max-w-5xl items-center gap-2 px-5 py-5">
        <Image src="/icon-192.png" alt="" width={28} height={28} className="rounded-lg" />
        <span className="text-[17px] font-bold">{SERVICE.name}</span>
      </header>

      <main>
        <section className="mx-auto grid max-w-5xl items-center gap-12 px-5 pt-10 pb-20 md:grid-cols-2 md:pt-20">
          <div>
            <p className="text-sm font-semibold text-primary">{SERVICE.tagline}</p>
            <h1 className="mt-3 text-[34px] font-bold leading-[1.25] md:text-[44px]">
              부모님 건강검진 결과,<br />이제 기억하지<br className="md:hidden" /> 않아도 돼요
            </h1>
            <p className="mt-5 text-[17px] leading-relaxed text-muted">
              결과지 사진 한 장이면 수치가 정리되고,<br />가족이 함께 보면서 해마다 변화를 챙길 수 있어요.
            </p>
            <div className="mt-8 max-w-sm">
              <Suspense fallback={<KakaoButton next="/" />}>
                <LoginAction searchParams={searchParams} />
              </Suspense>
              <p className="mt-3 text-center text-xs text-muted">카카오 계정으로 바로 시작해요</p>
            </div>
          </div>
          <Preview />
        </section>

        <section className="bg-card py-20">
          <div className="mx-auto max-w-5xl px-5">
            <h2 className="text-[26px] font-bold leading-snug">이런 적, 있지 않나요?</h2>
            <ul className="mt-8 grid gap-3 md:grid-cols-3">
              {WORRIES.map((w) => (
                <li key={w} className="rounded-2xl bg-background px-5 py-4 text-[17px]">“{w}”</li>
              ))}
            </ul>
            <p className="mt-8 text-[17px] leading-relaxed text-muted">
              가족의 검진 결과는 집집마다 흩어져 있어요. 한곳에 모아 두면 다음 검진도, 병원 상담도 훨씬 쉬워져요.
            </p>
          </div>
        </section>

        <section className="mx-auto max-w-5xl px-5 py-20">
          <h2 className="text-[26px] font-bold">가족 건강을 챙기는 가장 쉬운 방법</h2>
          <div className="mt-8 grid gap-3 md:grid-cols-3">
            {FEATURES.map((f) => (
              <div key={f.title} className="rounded-3xl bg-card p-6">
                <p className="text-3xl">{f.icon}</p>
                <h3 className="mt-4 text-[19px] font-bold">{f.title}</h3>
                <p className="mt-2 text-[15px] leading-relaxed text-muted">{f.body}</p>
              </div>
            ))}
          </div>
        </section>

        <section className="bg-card py-20">
          <div className="mx-auto max-w-5xl px-5">
            <h2 className="text-[26px] font-bold">세 단계면 시작해요</h2>
            <ol className="mt-8 grid gap-6 md:grid-cols-3">
              {STEPS.map((s, i) => (
                <li key={s.title} className="flex gap-4">
                  <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-primary text-[15px] font-bold text-white">{i + 1}</span>
                  <div>
                    <p className="text-[17px] font-semibold">{s.title}</p>
                    <p className="mt-1 text-[15px] text-muted">{s.body}</p>
                  </div>
                </li>
              ))}
            </ol>
          </div>
        </section>

        <section className="mx-auto max-w-5xl px-5 py-20">
          <h2 className="text-[26px] font-bold leading-snug">민감한 건강정보,<br className="md:hidden" /> 이렇게 지켜요</h2>
          <div className="mt-8 grid gap-3 md:grid-cols-2">
            {TRUST.map((t) => (
              <div key={t.title} className="flex gap-4 rounded-3xl bg-card p-6">
                <span className="mt-0.5 flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-primary-soft text-sm font-bold text-primary">✓</span>
                <div>
                  <p className="text-[17px] font-semibold">{t.title}</p>
                  <p className="mt-1 text-[15px] leading-relaxed text-muted">{t.body}</p>
                </div>
              </div>
            ))}
          </div>
        </section>

        <section className="bg-card py-20">
          <div className="mx-auto max-w-3xl px-5">
            <h2 className="text-[26px] font-bold">자주 묻는 질문</h2>
            <div className="mt-8 divide-y divide-line">
              {FAQ.map((f) => (
                <details key={f.q} className="group py-5">
                  <summary className="flex cursor-pointer list-none items-center justify-between gap-4 text-[17px] font-semibold">
                    {f.q}
                    <span className="text-muted transition group-open:rotate-180">⌄</span>
                  </summary>
                  <p className="mt-3 text-[15px] leading-relaxed text-muted">{f.a}</p>
                </details>
              ))}
            </div>
          </div>
        </section>

        <section className="mx-auto max-w-5xl px-5 py-20 text-center">
          <h2 className="text-[26px] font-bold leading-snug">올해 부모님 검진 결과부터<br />모아 볼까요?</h2>
          <div className="mx-auto mt-8 max-w-sm">
            <Suspense fallback={<KakaoButton next="/" />}>
              <LoginAction searchParams={searchParams} quiet />
            </Suspense>
          </div>
        </section>
      </main>

      <SiteFooter />
    </>
  );
}

async function LoginAction({ searchParams, quiet = false }: Pick<PageProps<"/login">, "searchParams"> & { quiet?: boolean }) {
  const { next, error, deleted } = await searchParams;
  const target = typeof next === "string" && next.startsWith("/") ? next : "/";
  const supabase = await createClient();
  const { data } = await supabase.auth.getClaims();
  if (data?.claims) redirect(target);
  return (
    <>
      {!quiet && error && <p className="mb-3 text-center text-sm text-danger">로그인에 실패했어요. 다시 시도해 주세요.</p>}
      {!quiet && deleted && <p className="mb-3 text-center text-sm text-muted">탈퇴가 완료됐어요. 그동안 고마웠어요.</p>}
      <KakaoButton next={target} />
    </>
  );
}

// A static example of the home card so visitors see what they get before signing in.
function Preview() {
  return (
    <div aria-label="예시 화면" className="relative mx-auto w-full max-w-sm">
      <div className="space-y-3 rounded-[32px] bg-background p-4 shadow-[0_20px_60px_-20px_rgba(0,0,0,0.25)] ring-1 ring-line">
        <div className="rounded-3xl bg-card p-5">
          <p className="text-sm text-muted">지금 확인이 필요해요</p>
          <p className="mt-1 text-[20px] font-bold"><span className="text-danger">1개</span> 항목이 질환의심이에요</p>
          <div className="mt-3 flex items-center justify-between text-[15px]">
            <span>엄마 · LDL 콜레스테롤</span>
            <span className="font-semibold">168 <span className="text-xs font-normal text-muted">mg/dL</span></span>
          </div>
        </div>
        <div className="rounded-3xl bg-card p-5">
          <div className="flex items-center gap-3">
            <div className="flex h-11 w-11 items-center justify-center rounded-full bg-primary-soft text-lg font-bold text-primary">엄</div>
            <div className="flex-1">
              <p className="text-[17px] font-semibold">엄마 <span className="text-sm font-normal text-muted">64세</span></p>
              <p className="text-sm text-muted">최근 검진 2026.03.14</p>
            </div>
          </div>
          <ul className="mt-4 divide-y divide-line">
            {[
              { label: "공복혈당", value: 108, unit: "mg/dL", j: "경계" as const, h: [96, 101, 108] },
              { label: "LDL 콜레스테롤", value: 168, unit: "mg/dL", j: "질환의심" as const, h: [138, 151, 168] },
              { label: "수축기 혈압", value: 124, unit: "mmHg", j: "정상" as const, h: [131, 127, 124] },
            ].map((i) => (
              <li key={i.label} className="flex items-center gap-3 py-3">
                <div className="flex-1">
                  <p className="text-sm">{i.label}</p>
                  <p className="text-[17px] font-bold">{i.value} <span className="text-xs font-normal text-muted">{i.unit}</span></p>
                </div>
                <Sparkline values={i.h} />
                <Badge judgement={i.j} />
              </li>
            ))}
          </ul>
        </div>
      </div>
      <p className="mt-3 text-center text-xs text-muted">예시 화면이에요</p>
    </div>
  );
}
