"use client";

import { useRef } from "react";

// Irreversible actions (delete, sign out, leave) ask once more in a modal. A native <dialog> instead of confirm():
// confirm() is easy to miss on phones and can't say what exactly will be lost.
export function ConfirmButton({ label, title, description, confirmLabel, className = "", danger = true }: {
  label: string; title: string; description?: string; confirmLabel: string; className?: string; danger?: boolean;
}) {
  const dialog = useRef<HTMLDialogElement>(null);
  return (
    <>
      <button
        type="button"
        className={className}
        onClick={(e) => {
          // Required fields (e.g. the leave page's checkbox) are checked before asking, so the question is never moot.
          if (e.currentTarget.form?.reportValidity() === false) return;
          dialog.current?.showModal();
        }}
      >
        {label}
      </button>
      <dialog
        ref={dialog}
        onClick={(e) => e.target === dialog.current && dialog.current.close()}
        className="m-auto w-[calc(100%-40px)] max-w-sm rounded-3xl bg-card p-6 text-foreground shadow-xl backdrop:bg-black/40"
      >
        <p className="text-[19px] font-bold leading-snug">{title}</p>
        {description && <p className="mt-2 text-sm leading-relaxed text-muted">{description}</p>}
        <div className="mt-6 grid grid-cols-2 gap-2">
          <button type="button" onClick={() => dialog.current?.close()} className="rounded-2xl bg-background py-3.5 text-[15px] font-semibold">취소</button>
          <button type="submit" className={`rounded-2xl py-3.5 text-[15px] font-semibold text-white ${danger ? "bg-danger" : "bg-primary"}`}>{confirmLabel}</button>
        </div>
      </dialog>
    </>
  );
}
