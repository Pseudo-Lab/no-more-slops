import Link from "next/link";
import { SERVICE } from "@/lib/service";
import { SiteFooter } from "./site-footer";

export type Section = { title: string; body: React.ReactNode };

export function LegalPage({ title, sections }: { title: string; sections: Section[] }) {
  return (
    <>
      <main className="mx-auto max-w-2xl px-5 pt-8 pb-16">
        <Link href="/" className="inline-block py-2 text-[15px] text-muted">‹ {SERVICE.name}</Link>
        <h1 className="mt-4 text-[28px] font-bold">{title}</h1>
        <p className="mt-2 text-sm text-muted">시행일 {SERVICE.policyDate.replaceAll("-", ".")}</p>
        <div className="mt-8 space-y-3">
          {sections.map((s, i) => (
            <section key={s.title} className="rounded-3xl bg-card p-6">
              <h2 className="text-[17px] font-bold">{i + 1}. {s.title}</h2>
              <div className="legal mt-3 space-y-2 text-[15px] leading-relaxed text-foreground/85">{s.body}</div>
            </section>
          ))}
        </div>
      </main>
      <SiteFooter />
    </>
  );
}
