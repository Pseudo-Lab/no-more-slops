"use client";

import { usePathname } from "next/navigation";
import Script from "next/script";
import { Suspense, useEffect } from "react";
import { GA_ID, gtag, normalizePath } from "@/lib/analytics";

// Renders nothing until NEXT_PUBLIC_GA_ID is set, so local dev and previews send no data.
export function Analytics() {
  if (!GA_ID) return null;
  return (
    <>
      <Script src={`https://www.googletagmanager.com/gtag/js?id=${GA_ID}`} strategy="afterInteractive" />
      {/* Constraint: with cacheComponents, usePathname must sit inside Suspense. */}
      <Suspense>
        <PageViews />
      </Suspense>
    </>
  );
}

function PageViews() {
  const pathname = usePathname();
  useEffect(() => {
    gtag("js", new Date());
    // Automatic page views would send raw URLs (member ids, invite codes); page_view below sends normalized paths.
    // History: enhanced measurement can fire scroll right after config, before the effect below runs, so config carries the normalized URL too.
    gtag("config", GA_ID, { send_page_view: false, page_location: location.origin + normalizePath(location.pathname) });
  }, []);
  useEffect(() => {
    // History: passing page_location only on page_view let enhanced-measurement events (scroll, click) send the raw URL; "set" covers every event.
    gtag("set", { page_location: location.origin + normalizePath(pathname) });
    gtag("event", "page_view");
  }, [pathname]);
  return null;
}
