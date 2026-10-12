import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  cacheComponents: true,
  // The Codex SDK spawns a local CLI binary; it is only loaded on the local-dev extraction path, never bundled.
  serverExternalPackages: ["@openai/codex-sdk"],
  partialPrefetching: true,
  experimental: {
    // Constraint: Vercel rejects request bodies over 4.5MB; result-sheet PDFs are sent as-is, so allow just under it.
    serverActions: { bodySizeLimit: "4mb" },
  },
  turbopack: {
    rules: {
      "*.css": {
        loaders: ["@tailwindcss/turbopack"],
        as: "*.css",
      },
    },
  },
};

export default nextConfig;
