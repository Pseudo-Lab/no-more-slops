import { mkdtemp, readdir, rm, unlink, writeFile } from "node:fs/promises";
import { tmpdir, homedir } from "node:os";
import { join } from "node:path";
import { INSTRUCTIONS, SCHEMA } from "./extract-prompt";

// Business: local dev reads sheets through the owner's ChatGPT login instead of a paid API key (owner 2026-10-12);
// gpt-6-sol read 17/17 values and judgements in the model comparison. Production never takes this path.
const MODEL = "gpt-6-sol";

// Codex only takes images as files and keeps a transcript of every thread; the sheet lives in a temp dir for the
// length of the call and the transcript is deleted right after, so nothing of the sheet stays on disk (constitution I).
export async function askCodex(text: string | null, images: File[]): Promise<string | null> {
  const { Codex } = await import("@openai/codex-sdk");
  const dir = await mkdtemp(join(tmpdir(), "sheet-"));
  let threadId: string | null = null;
  try {
    const paths = await Promise.all(images.map(async (f, n) => {
      const p = join(dir, `page${n}.${f.type === "image/png" ? "png" : "jpg"}`);
      await writeFile(p, Buffer.from(await f.arrayBuffer()));
      return p;
    }));
    const thread = new Codex().startThread({ model: MODEL, modelReasoningEffort: "low", sandboxMode: "read-only", workingDirectory: dir, skipGitRepoCheck: true, webSearchMode: "disabled" });
    const turn = await thread.run(
      [{ type: "text", text: `${INSTRUCTIONS}\n\n${text ? `결과지 텍스트:\n${text}` : "결과지는 이미지로만 와요."}` }, ...paths.map((path) => ({ type: "local_image" as const, path }))],
      { outputSchema: SCHEMA },
    );
    threadId = thread.id;
    return turn.finalResponse || null;
  } catch (e) {
    console.error("askCodex failed", e instanceof Error ? e.message : e);
    return null;
  } finally {
    await rm(dir, { recursive: true, force: true });
    if (threadId) await forgetThread(threadId);
  }
}

// Session rollouts are `~/.codex/sessions/YYYY/MM/DD/rollout-<time>-<threadId>.jsonl`.
async function forgetThread(threadId: string) {
  const root = join(process.env.CODEX_HOME ?? join(homedir(), ".codex"), "sessions");
  const files = await readdir(root, { recursive: true }).catch(() => [] as string[]);
  await Promise.all(files.filter((f) => f.includes(threadId)).map((f) => unlink(join(root, f)).catch(() => {})));
}
