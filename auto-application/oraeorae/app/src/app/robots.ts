import type { MetadataRoute } from "next";

// Only the public pages are worth indexing; everything else is behind login and holds health data.
export default function robots(): MetadataRoute.Robots {
  return { rules: { userAgent: "*", allow: ["/login", "/terms", "/privacy"], disallow: "/" } };
}
