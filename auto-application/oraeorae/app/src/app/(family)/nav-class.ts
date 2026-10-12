export const navClass = (active: boolean) =>
  `flex items-center gap-3 rounded-2xl px-4 py-3 text-[15px] ${active ? "bg-card font-semibold" : "text-muted hover:bg-card/60"}`;
