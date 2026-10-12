import Link from "next/link";
import { Suspense } from "react";
import { requireFamily } from "@/lib/family";
import { SERVICE } from "@/lib/service";
import { navClass } from "./nav-class";
import { NavLink } from "./nav-link";

// Constraint: with cacheComponents, usePathname under a dynamic route must sit inside Suspense, so only the leaf link suspends.
function Nav({ href, children }: { href: string; children: React.ReactNode }) {
  return (
    <Suspense fallback={<Link href={href} className={navClass(false)}>{children}</Link>}>
      <NavLink href={href}>{children}</NavLink>
    </Suspense>
  );
}

export async function Sidebar() {
  const { members } = await requireFamily();
  return (
    <aside className="sticky top-0 hidden h-screen w-60 shrink-0 flex-col gap-1 py-10 md:flex">
      <p className="mb-6 px-4 text-[19px] font-bold">{SERVICE.name}</p>
      <Nav href="/">홈</Nav>
      <p className="mt-6 mb-1 px-4 text-xs text-muted">가족</p>
      {members.map((m) => (
        <Nav key={m.id} href={`/member/${m.id}`}>
          <span className="flex h-7 w-7 items-center justify-center rounded-full bg-primary-soft text-xs font-bold text-primary">{m.name[0]}</span>
          {m.name}
        </Nav>
      ))}
      <Nav href="/invite"><span className="flex h-7 w-7 items-center justify-center rounded-full bg-primary-soft text-xs font-bold text-primary">+</span>가족 초대</Nav>
      <div className="mt-auto pb-3">
        <Nav href="/settings">설정</Nav>
      </div>
      <Link href="/upload" className=" rounded-2xl bg-primary py-3.5 text-center text-[15px] font-semibold text-white">결과지 올리기</Link>
    </aside>
  );
}
