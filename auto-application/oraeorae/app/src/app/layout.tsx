import type { Metadata, Viewport } from "next";
import { SERVICE } from "@/lib/service";
import { Analytics } from "./analytics";
import "./globals.css";

export const metadata: Metadata = {
  // Business: free kro.kr domain for the experiment (#18); share previews and icons resolve against it.
  // Future: move to oraeorae.kr once bought; the old vercel.app URL keeps working until Kakao/Supabase point here.
  metadataBase: new URL("https://oraeorae.kro.kr"),
  title: { default: `${SERVICE.name} · ${SERVICE.tagline}`, template: `%s · ${SERVICE.name}` },
  description: "부모님, 배우자, 아이의 건강검진 결과를 사진 한 장으로 기록하고 가족이 함께 봐요.",
  applicationName: SERVICE.name,
  openGraph: { siteName: SERVICE.name, locale: "ko_KR", type: "website" },
  appleWebApp: { title: SERVICE.name, statusBarStyle: "default" },
};

// Matches --background in each scheme so the mobile browser bar blends into the page.
export const viewport: Viewport = {
  themeColor: [
    { media: "(prefers-color-scheme: light)", color: "#f2f4f6" },
    { media: "(prefers-color-scheme: dark)", color: "#17171c" },
  ],
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="ko" className="h-full antialiased">
      <body className="min-h-full">
        {children}
        <Analytics />
      </body>
    </html>
  );
}
