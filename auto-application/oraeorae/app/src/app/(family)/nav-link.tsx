"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { navClass } from "./nav-class";

export function NavLink({ href, children }: { href: string; children: React.ReactNode }) {
  return <Link href={href} className={navClass(usePathname() === href)}>{children}</Link>;
}
