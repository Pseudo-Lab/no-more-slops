export function Skeleton() {
  return (
    <main className="space-y-3 px-5 pt-10 md:px-0">
      <div className="h-10 w-48 animate-pulse rounded-xl bg-card" />
      <div className="h-40 animate-pulse rounded-3xl bg-card" />
      <div className="h-40 animate-pulse rounded-3xl bg-card" />
    </main>
  );
}
