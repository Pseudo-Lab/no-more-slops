"use client";

import Link from "next/link";
import { useState } from "react";
import { type FunnelEvent, track } from "@/lib/analytics";
import { CONSENTS } from "@/lib/consents";


export function ConsentForm({ action, submitLabel, event, defaultName }: {
  action: (formData: FormData) => Promise<void>; submitLabel: string; event: FunnelEvent; defaultName?: string | null;
}) {
  const [checked, setChecked] = useState<Set<string>>(new Set());
  const [open, setOpen] = useState<string | null>(null);
  const all = checked.size === CONSENTS.length;
  const toggle = (id: string) =>
    setChecked((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });

  return (
    <form action={action} onSubmit={() => track(event)} className="space-y-3">
      <section className="rounded-3xl bg-card p-5">
        <label className="block text-sm text-muted" htmlFor="name">가족에게 보일 이름</label>
        <input id="name" name="name" required maxLength={20} defaultValue={defaultName ?? ""} placeholder="예: 엄마, 첫째" className="mt-2 w-full rounded-xl bg-background px-4 py-3 text-[17px] outline-none focus:ring-2 focus:ring-primary" />
      </section>

      <section className="rounded-3xl bg-card p-5">
        {[...checked].map((id) => <input key={id} type="hidden" name="consent" value={id} />)}
        <button
          type="button"
          onClick={() => setChecked(all ? new Set() : new Set(CONSENTS.map((c) => c.id)))}
          className="flex w-full items-center gap-3 text-left text-[17px] font-semibold"
        >
          <Check on={all} /> 모두 동의해요
        </button>
        <ul className="mt-3 space-y-4 border-t border-line pt-4">
          {CONSENTS.map((c) => (
            <li key={c.id}>
              <div className="flex items-start gap-3">
                <button type="button" onClick={() => toggle(c.id)} className="flex flex-1 items-start gap-3 text-left">
                  <Check on={checked.has(c.id)} small />
                  <span>
                    <span className="block text-[15px]">[필수] {c.title} 동의</span>
                    <span className="mt-0.5 block text-xs text-muted">{c.summary}</span>
                  </span>
                </button>
                <button type="button" onClick={() => setOpen(open === c.id ? null : c.id)} className="shrink-0 pt-0.5 text-xs text-muted underline">
                  {open === c.id ? "닫기" : "보기"}
                </button>
              </div>
              {open === c.id && (
                <dl className="mt-3 ml-8 space-y-2 rounded-xl bg-background p-3 text-xs">
                  {c.rows.map(([k, v]) => (
                    <div key={k}>
                      <dt className="font-semibold">{k}</dt>
                      <dd className="mt-0.5 text-muted">{v}</dd>
                    </div>
                  ))}
                </dl>
              )}
            </li>
          ))}
        </ul>
      </section>

      <p className="px-1 text-xs leading-relaxed text-muted">
        만 14세 이상만 가입할 수 있어요. 시작하면 <Link href="/terms" className="underline">이용약관</Link>과{" "}
        <Link href="/privacy" className="underline">개인정보처리방침</Link>에 동의한 것으로 봐요.
      </p>

      <button
        disabled={!all}
        className="w-full rounded-2xl bg-primary py-4 text-[17px] font-semibold text-white disabled:bg-line disabled:text-muted"
      >
        {submitLabel}
      </button>
    </form>
  );
}

function Check({ on, small = false }: { on: boolean; small?: boolean }) {
  const size = small ? "h-5 w-5 text-xs" : "h-6 w-6 text-sm";
  return (
    <span className={`flex shrink-0 items-center justify-center rounded-full ${size} ${on ? "bg-primary text-white" : "bg-line text-white"}`}>✓</span>
  );
}
