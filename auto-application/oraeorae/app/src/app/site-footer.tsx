import Link from "next/link";
import { SERVICE } from "@/lib/service";

export function SiteFooter() {
  return (
    <footer className="border-t border-line">
      <div className="mx-auto max-w-5xl space-y-3 px-5 py-10 text-xs leading-relaxed text-muted">
        <nav className="flex flex-wrap gap-x-4 gap-y-2 text-sm">
          <Link href="/terms" className="hover:text-foreground">이용약관</Link>
          <Link href="/privacy" className="font-semibold text-foreground">개인정보처리방침</Link>
          <a href={`mailto:${SERVICE.contact}`} className="hover:text-foreground">문의하기</a>
        </nav>
        <p>{SERVICE.name}는 건강검진 결과를 기록하고 가족과 나누는 서비스예요. 의료 진단이나 치료를 대신하지 않으며, 판정은 결과지에 적힌 내용을 그대로 보여 줘요.</p>
        <p>개인정보 문의 {SERVICE.officer} · {SERVICE.contact}</p>
        {/* Constraint: Pseudo Lab No-More-Slops requires this acknowledgement on services built in the cohort (README "소유권과 Acknowledgement"). */}
        <p>이 결과물은 가짜연구소(Pseudo Lab) No-More-Slops 그룹 활동의 일환으로 제작되었습니다.</p>
        <p>© 2026 {SERVICE.name}</p>
      </div>
    </footer>
  );
}
