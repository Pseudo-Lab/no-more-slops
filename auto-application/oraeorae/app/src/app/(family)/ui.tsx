import Link from "next/link";
import type { Judgement } from "@/lib/health";

const BADGE: Record<Judgement, string> = {
  정상: "bg-primary-soft text-primary",
  경계: "bg-warn-soft text-warn",
  질환의심: "bg-danger-soft text-danger",
};

// Shows the sheet's own mark: a national-checkup judgement, else a lab H/L flag, else nothing was marked.
export function Badge({ judgement, flag = null }: { judgement: Judgement | null; flag?: "H" | "L" | null }) {
  if (!judgement && flag) return <span className="rounded-md bg-warn-soft px-2 py-0.5 text-xs font-semibold text-warn">{flag === "H" ? "높음 H" : "낮음 L"}</span>;
  return <span className={`rounded-md px-2 py-0.5 text-xs font-semibold ${judgement ? BADGE[judgement] : "bg-background text-muted"}`}>{judgement ?? "판정 없음"}</span>;
}

export function Card({ children, className = "" }: { children: React.ReactNode; className?: string }) {
  return <section className={`rounded-3xl bg-card p-5 ${className}`}>{children}</section>;
}

export function Sparkline({ values }: { values: number[] }) {
  if (values.length < 2) return <span className="text-xs text-muted">기록 1회</span>;
  const min = Math.min(...values), max = Math.max(...values), span = max - min || 1;
  const points = values.map((v, i) => `${(i / (values.length - 1)) * 64},${20 - ((v - min) / span) * 16 - 2}`).join(" ");
  return (
    <svg width="64" height="20" viewBox="0 0 64 20" aria-hidden>
      <polyline points={points} fill="none" stroke="var(--primary)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

export function BottomButton({ href, children }: { href: string; children: React.ReactNode }) {
  return (
    <div className="fixed inset-x-0 bottom-0 bg-gradient-to-t from-background via-background to-transparent pt-6 md:hidden">
      <div className="mx-auto max-w-md px-5 pb-6">
        <Link href={href} className="block rounded-2xl bg-primary py-4 text-center text-[17px] font-semibold text-white">{children}</Link>
      </div>
    </div>
  );
}
