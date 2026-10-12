import type { MetadataRoute } from "next";
import { SERVICE } from "@/lib/service";

// Lets parents add the app to their phone's home screen and open it like a native app.
export default function manifest(): MetadataRoute.Manifest {
  return {
    name: SERVICE.name,
    short_name: SERVICE.name,
    description: SERVICE.tagline,
    start_url: "/",
    display: "standalone",
    background_color: "#f2f4f6",
    theme_color: "#3182f6",
    lang: "ko",
    icons: [
      { src: "/icon-192.png", sizes: "192x192", type: "image/png" },
      { src: "/app-icon.png", sizes: "512x512", type: "image/png" },
    ],
  };
}
