"use client";

import { useEffect, useState, useTransition } from "react";
import { track } from "@/lib/analytics";
import type { Member } from "@/lib/health";
import { extractSheet, type ExtractResult } from "./extract";
import { ReviewForm } from "./review-form";
import { readPdf, shrinkPhoto } from "./sheet-image";

// Constraint: matches serverActions.bodySizeLimit in next.config.ts (Vercel's 4.5MB request limit).
const MAX_BYTES = 4 * 1024 * 1024;

export function UploadForm({ members, initialMemberId, credits }: { members: Pick<Member, "id" | "name">[]; initialMemberId: string; credits: number }) {
  const [memberId, setMemberId] = useState(initialMemberId);
  const [file, setFile] = useState<File | null>(null);
  const [error, setError] = useState("");
  const [result, setResult] = useState<Extract<ExtractResult, { items: unknown }> | null>(null);
  const [reading, startReading] = useTransition();
  const [stage, setStage] = useState<"file" | "ai">("file");
  const [seconds, setSeconds] = useState(0);
  // A long PDF takes about a minute to read; a ticking counter shows the wait is alive, not stuck.
  useEffect(() => {
    if (!reading) return;
    const t = setInterval(() => setSeconds((s) => s + 1), 1000);
    return () => clearInterval(t);
  }, [reading]);

  function read() {
    if (!file) return;
    track("upload_submit");
    setError("");
    setStage("file");
    setSeconds(0);
    startReading(async () => {
      const out = await readSheet(file, setStage);
      if ("error" in out) {
        track("extract_error");
        setError(out.error);
      } else {
        setResult(out);
        scrollTo(0, 0);
      }
    });
  }

  if (reading) {
    return (
      <>
        <header className="mb-5 px-1">
          <h1 className="text-[26px] font-bold leading-tight">결과지를<br />읽고 있어요</h1>
          <p className="mt-2 text-sm text-muted">
            {stage === "file" ? "파일을 준비하고 있어요" : "AI가 결과지를 읽고 있어요 · 사진은 10초, 긴 PDF는 1분쯤 걸려요"} · {seconds}초
          </p>
        </header>
        <section aria-busy="true" aria-label="판독 중" className="space-y-4 rounded-3xl bg-card p-5">
          {Array.from({ length: 6 }, (_, n) => (
            <div key={n} className="flex items-center gap-3">
              <div className="h-4 flex-1 animate-pulse rounded-lg bg-background" />
              <div className="h-9 w-24 animate-pulse rounded-xl bg-background" />
            </div>
          ))}
        </section>
        <p className="px-1 text-xs leading-relaxed text-muted">이 화면을 닫지 말고 기다려 주세요. 결과지 원본은 저장하지 않아요.</p>
      </>
    );
  }

  if (result) {
    const member = members.find((m) => m.id === memberId)!;
    return (
      <>
        <header className="mb-5 px-1">
          <h1 className="text-[26px] font-bold leading-tight">읽은 값이 맞는지<br />확인해 주세요</h1>
          <p className="mt-2 text-sm text-muted">{member.name}님의 결과지 · 틀린 값은 눌러서 고칠 수 있어요</p>
        </header>
        <button onClick={() => setResult(null)} className="px-1 text-sm font-semibold text-primary">‹ 다른 결과지 올리기</button>
        {result.sample && (
          <p className="rounded-2xl bg-warn-soft px-4 py-3 text-sm text-warn">AI 판독 연결 전이라 예시 값이 채워져 있어요. 실제 결과지 값으로 고쳐 주세요.</p>
        )}
        <ReviewForm memberId={memberId} extracted={result.items} examDate={result.examDate} findings={result.findings} />
      </>
    );
  }

  return (
    <>
      <header className="mb-5 px-1">
        <h1 className="text-[26px] font-bold leading-tight">건강검진 결과지를<br />올려 주세요</h1>
        <p className="mt-2 text-sm text-muted">AI가 수치를 읽고, 저장 전에 한 번 더 확인해요</p>
        <p className={`mt-2 inline-block rounded-md px-2 py-0.5 text-xs font-semibold ${credits > 0 ? "bg-primary-soft text-primary" : "bg-danger-soft text-danger"}`}>남은 판독 {credits}회</p>
      </header>

      <section className="rounded-3xl bg-card p-5">
        <p className="text-sm text-muted">누구의 결과지인가요?</p>
        <div className="mt-3 flex flex-wrap gap-2">
          {members.map((m) => (
            <button
              key={m.id}
              onClick={() => setMemberId(m.id)}
              className={`rounded-xl px-4 py-2.5 text-[15px] ${memberId === m.id ? "bg-primary font-semibold text-white" : "bg-background"}`}
            >
              {m.name}
            </button>
          ))}
        </div>
      </section>

      <label className="flex cursor-pointer flex-col items-center justify-center rounded-3xl border-2 border-dashed border-line bg-card px-5 py-12 text-center">
        <input type="file" accept="image/*,application/pdf" capture="environment" className="hidden" onChange={(e) => {
          setFile(e.target.files?.[0] ?? null);
          setError("");
          if (e.target.files?.[0]) track("upload_file_selected");
        }} />
        {file ? (
          <>
            <p className="text-3xl">📄</p>
            <p className="mt-3 break-all text-[17px] font-semibold">{file.name}</p>
            <p className="mt-1 text-sm text-primary">다른 파일로 바꾸기</p>
          </>
        ) : (
          <>
            <p className="text-3xl">📷</p>
            <p className="mt-3 text-[17px] font-semibold">결과지 사진 찍기 또는 파일 선택</p>
            <p className="mt-1 text-sm text-muted">사진(JPG, PNG)이나 PDF · 여러 쪽짜리 PDF도 그대로 올려요</p>
          </>
        )}
      </label>

      <p className="px-1 text-xs leading-relaxed text-muted">
        결과지는 수치를 읽는 데만 쓰고 바로 지워요. 주민번호나 주소는 저장하지 않아요.
      </p>

      <div className="fixed inset-x-0 bottom-0 bg-gradient-to-t from-background via-background to-transparent pt-6 md:static md:bg-none md:pt-2">
        <div className="mx-auto max-w-md px-5 pb-6 md:max-w-none md:px-0">
          {(error || credits === 0) && <p role="alert" className="mb-3 text-center text-sm text-danger">{error || "판독 크레딧을 모두 썼어요. 충전 기능은 준비 중이에요"}</p>}
          <button
            disabled={!file || reading || credits === 0}
            onClick={read}
            className="w-full rounded-2xl bg-primary py-4 text-[17px] font-semibold text-white disabled:bg-line disabled:text-muted"
          >
            {reading ? "결과지를 읽고 있어요…" : "결과지 읽기"}
          </button>
        </div>
      </div>
    </>
  );
}

// PDFs become the whole report's text plus page images; photos are just shrunk.
async function readSheet(file: File, onStage: (s: "file" | "ai") => void): Promise<ExtractResult> {
  const form = new FormData();
  try {
    if (file.type === "application/pdf") {
      const pdf = await readPdf(file);
      if (!pdf) return { error: "파일을 열지 못했어요. 다른 파일이나 사진으로 올려 주세요" };
      // The first image (result page) always goes; later image-only pages are dropped once the request limit is near.
      let bytes = new Blob([pdf.text]).size;
      pdf.images.forEach((image, n) => {
        if (n > 0 && bytes + image.size > MAX_BYTES) return;
        bytes += image.size;
        form.append("file", image, `page${n}.jpg`);
      });
      if (pdf.text) form.append("text", pdf.text);
    } else {
      form.append("file", await shrinkPhoto(file), "sheet");
    }
  } catch {
    return { error: "파일을 열지 못했어요. 다른 파일이나 사진으로 올려 주세요" };
  }
  const bytes = form.getAll("file").reduce((sum, f) => sum + (f as Blob).size, 0) + new Blob([String(form.get("text") ?? "")]).size;
  if (bytes > MAX_BYTES) return { error: "파일이 너무 커요. 결과지를 사진으로 찍어 올려 주세요" };
  onStage("ai");
  return extractSheet(form).catch(() => ({ error: "연결이 끊겼어요. 잠시 후 다시 눌러 주세요" }));
}
