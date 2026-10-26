# Scholar Monster

LaTeX 논문을 공동으로 작성하고, AI가 제안한 수정안을 컴파일된 PDF와 비교해 검토하는 웹 서비스입니다. 원고에 곧바로 덮어쓰지 않고 Proposal(수정안)을 만든 뒤, 공동저자가 변경 내용과 결과를 확인하고 병합합니다.

- 작성자: [@gogoymh](https://github.com/gogoymh)
- 트랙: Auto-Application
- 서비스: [scholarmonster.com](https://scholarmonster.com/)
- 상태: 운영 배포 완료. 광고와 유료 결제는 아직 비활성입니다.
- 접근 조건: 서비스 소개는 공개되어 있습니다. 원고와 Proposal은 로그인과 프로젝트 접근 권한이 필요합니다.
- 원본 서비스 소스: 비공개. 이 제출에는 서비스 코드, 실제 논문, 계정 정보가 포함되지 않습니다.

## 사용 흐름

1. 로그인한 뒤 본인 프로젝트에 LaTeX 원고와 참고문헌을 준비합니다.
2. 웹 또는 MCP(Model Context Protocol)로 수정안을 제출합니다.
3. 자동 컴파일 결과를 보면서 왼쪽 변경 내용과 오른쪽 전체 PDF를 비교합니다.
4. 공동저자와 댓글로 검토하고, 승인한 변경을 병합합니다.
5. 특정 Proposal을 전달하려면 Share → Copy link를 사용합니다. 새 공동저자는 먼저 프로젝트에 초대해야 합니다.

## 주차별 결과

| 주차 | 결과물 | 공개 범위 |
| --- | --- | --- |
| [Week 03](outputs/week-03/README.md) | Proposal 자동 컴파일, PDF 검토 화면, 알림, arXiv 패키징, 공유와 운영 배포 기록 | 서비스 링크, 제작 절차, 검증 요약, 합성 데이터로 찍은 로컬 UI 화면 |

## 제작 도구와 공개 범위

Codex와 협업 에이전트로 원인 조사, 구현, 독립 코드 리뷰와 브라우저 검증을 나눠 진행했습니다. Git/GitHub CLI로 커밋과 squash 병합을 관리하고, pnpm, TypeScript, Vitest, Chromium, Docker Compose로 검사와 배포를 진행했습니다.

이번 제출에서 추가하거나 수정한 저장소 스킬은 없습니다. 기존 카탈로그의 스킬을 실행했다고 주장하거나 동일한 스킬 사본을 만들지 않았습니다. 개발 중 반복한 절차와 검증 한계는 [주차 결과 문서](outputs/week-03/README.md)에 기록했습니다. 문서와 제출 이미지에는 이 저장소의 [MIT License](../../../../LICENSE)가 적용됩니다. 외부 서비스의 비공개 소스는 이 기여에 포함되지 않습니다.

## Acknowledgement

이 결과물은 가짜연구소(Pseudo Lab) No-More-Slops 그룹 활동의 일환으로 제작되었습니다.
