import Link from "next/link";
import { Suspense } from "react";
import { creditBalance } from "@/lib/credits";
import { requireFamily } from "@/lib/family";
import { Skeleton } from "../skeleton";
import { UploadForm } from "./upload-form";

export default function UploadPage({ searchParams }: PageProps<"/upload">) {
  return (
    <main className="space-y-3 px-5 pt-6 md:max-w-xl md:px-0 md:pt-10">
      <Link href="/" className="inline-block px-1 py-2 text-[15px] text-muted md:hidden">‹ 가족</Link>
      {/* The header lives in UploadForm: it changes once the sheet is read and the review step begins. */}
      <Suspense fallback={<Skeleton />}>
        <Upload searchParams={searchParams} />
      </Suspense>
    </main>
  );
}

async function Upload({ searchParams }: Pick<PageProps<"/upload">, "searchParams">) {
  const [{ member }, { members, meId }, credits] = await Promise.all([searchParams, requireFamily(), creditBalance()]);
  const initial = typeof member === "string" && members.some((m) => m.id === member) ? member : meId;
  return <UploadForm members={members.map(({ id, name }) => ({ id, name }))} initialMemberId={initial} credits={credits} />;
}
