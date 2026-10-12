import { Suspense } from "react";
import { Sidebar } from "./sidebar";

export default function FamilyLayout({ children }: LayoutProps<"/">) {
  return (
    <div className="mx-auto flex min-h-full max-w-md gap-10 md:max-w-6xl md:px-8">
      <Suspense fallback={<aside className="hidden w-60 shrink-0 md:block" />}>
        <Sidebar />
      </Suspense>
      <div className="min-w-0 flex-1 pb-28 md:pb-12">{children}</div>
    </div>
  );
}
