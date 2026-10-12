import { CHECKUP_ITEMS } from "@/lib/checkup-items";

// Constraint: gpt-5.4-mini and gpt-5.6-luna read images as 32px patches and downsizes anything over 2,500 patches or 2048px at
// detail "high" (OpenAI vision docs, 2026-10). Sending exactly that budget avoids a second, blurrier resize
// on their side and keeps uploads small; tokens are capped at the budget either way.
const PATCH = 32;
const PATCH_BUDGET = 2500;
const MAX_SIDE = 2048;

// Largest scale (may be > 1) at which a w×h image still fits the patch budget and the max side.
function budgetScale(w: number, h: number) {
  let scale = Math.min(MAX_SIDE / Math.max(w, h), Math.sqrt((PATCH_BUDGET * PATCH * PATCH) / (w * h)));
  // ceil() per side can push the count just over budget; shave until it fits.
  while (Math.ceil((w * scale) / PATCH) * Math.ceil((h * scale) / PATCH) > PATCH_BUDGET) scale *= 0.99;
  return scale;
}

function toJpeg(canvas: HTMLCanvasElement): Promise<Blob | null> {
  return new Promise((resolve) => canvas.toBlob(resolve, "image/jpeg"));
}

// Phone photos are often 3–10MB; re-encode on the device so they fit the request limit.
export async function shrinkPhoto(file: File): Promise<Blob> {
  try {
    const bitmap = await createImageBitmap(file);
    const scale = Math.min(1, budgetScale(bitmap.width, bitmap.height));
    const canvas = document.createElement("canvas");
    canvas.width = Math.floor(bitmap.width * scale);
    canvas.height = Math.floor(bitmap.height * scale);
    canvas.getContext("2d")!.drawImage(bitmap, 0, 0, canvas.width, canvas.height);
    return (await toJpeg(canvas)) ?? file;
  } catch {
    // History: some browsers can't decode HEIC; send the original and let the size check decide.
    return file;
  }
}

// Masks resident registration numbers (e.g. 900101-1******) before any text leaves the device.
const maskRrn = (text: string) => text.replace(/\d{6}\s*-\s*[1-8][\d*]{6}/g, "******-*******");

// History: a 36-page, 7.6MB clinic report broke the 4MB upload limit and would cost ~20x a photo in tokens.
// The whole PDF is parsed on the device instead: every page's text goes up (numbers anywhere in the report), plus
// images of the pages that must be read as pixels — the page naming the most checkup items (its ■/□ judgement
// boxes) and every page without a text layer (InBody, bone density, scans). A fully scanned PDF sends all pages.
export async function readPdf(file: File): Promise<{ images: Blob[]; text: string } | null> {
  const pdfjs = await import("pdfjs-dist");
  const worker = new Worker(new URL("pdfjs-dist/build/pdf.worker.min.mjs", import.meta.url), { type: "module" });
  pdfjs.GlobalWorkerOptions.workerPort = worker;
  try {
    const pdf = await pdfjs.getDocument({ data: new Uint8Array(await file.arrayBuffer()) }).promise;
    if (pdf.numPages === 0) return null;
    const pages: string[] = [];
    for (let n = 1; n <= pdf.numPages; n++) {
      const content = await (await pdf.getPage(n)).getTextContent();
      pages.push(content.items.map((i) => ("str" in i ? i.str + (i.hasEOL ? "\n" : " ") : "")).join(""));
    }
    const score = (t: string) => CHECKUP_ITEMS.filter((c) => t.includes(c.find)).length;
    const best = pages.reduce((b, t, i) => (score(t) > score(pages[b]) ? i : b), 0);
    const textless = (i: number) => !pages[i].trim();
    const wanted = pages.some((t) => t.trim()) ? [best, ...pages.map((_, i) => i).filter((i) => i !== best && textless(i))] : pages.map((_, i) => i);

    const images: Blob[] = [];
    for (const i of wanted) {
      const page = await pdf.getPage(i + 1);
      const base = page.getViewport({ scale: 1 });
      const viewport = page.getViewport({ scale: budgetScale(base.width, base.height) });
      const canvas = document.createElement("canvas");
      canvas.width = Math.floor(viewport.width);
      canvas.height = Math.floor(viewport.height);
      await page.render({ canvas, viewport }).promise;
      const image = await toJpeg(canvas);
      if (image) images.push(image);
    }
    if (images.length === 0) return null;
    return { images, text: maskRrn(pages.map((t, i) => `[${i + 1}쪽]\n${t.trim()}`).join("\n\n")) };
  } finally {
    worker.terminate();
  }
}
