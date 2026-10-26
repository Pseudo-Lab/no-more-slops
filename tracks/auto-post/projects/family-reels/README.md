# Family Reels

작성자: [임경태 · darkwingduck-code](https://github.com/darkwingduck-code)

로컬 가족 영상을 세로 Instagram 릴스로 편집하고, 제작 과정과 검증 기록을 공유하는 Auto-Post 프로젝트입니다. 재사용 가능한 편집 절차는 [instagram-reel 스킬](../../skills/instagram-reel/SKILL.md)에 한 번만 보관합니다. 이 스킬은 영상 편집을 담당하며 정지 이미지 캐러셀을 만드는 `instagram-content`와 구분합니다.

- [1주차 · 편집 스킬과 완성 릴스](outputs/week-01/README.md), 원본 [PR #15](https://github.com/Pseudo-Lab/no-more-slops/pull/15)
- [2주차 · 밈 사전 기획과 파이프라인 화면 · PR #9](https://github.com/Pseudo-Lab/no-more-slops/pull/9)
- 현재 저장소에 포함된 자료는 [주차별 결과물 폴더](outputs/)에서 확인합니다.

공유하는 결과물과 근거는 `outputs/week-NN/README.md`에 기록합니다. 가족 영상의 원본·완성본·얼굴 이미지·위치 정보는 코드 저장소에 넣지 않고, 원본 기여자가 공유한 외부 결과물 링크를 사용합니다. 스킬을 설치할 때는 필요한 트랙 스킬 폴더만 복사하고 프로젝트 결과물을 함께 설치하지 않습니다.

[family-reel-meme-preflight](../../skills/family-reel-meme-preflight/SKILL.md)는 편집 전 트렌드·시장별 근거·아기 안전을 검토해 기획안을 준비합니다. 영상 편집은 기존 `instagram-reel` 스킬로 이어집니다. 두 스킬의 단계와 출력이 다르므로 같은 기능을 복사해 관리하지 않습니다.

## 2026-10-26 스킬 공유판

작성자 임경태 · @darkwingduck-code의 로컬 제작 작업실에서 사용하는 두 스킬의 최신 절차를 기존 canonical 경로에 반영했습니다. 공개판은 독립적으로 읽을 수 있도록 제작 앱의 상대 링크를 정리했으며 원본 파일의 바이트 단위 복사본은 아닙니다. 앱에 종속된 파일명·화면·API 설정과 작가 역할은 [작업실 연동 참고](../../skills/instagram-reel/references/local-workbench.md)에 분리했습니다. 앱 구현, 개인 미디어, 인증 정보와 새 주차 결과물은 포함하지 않습니다.

기준 원본은 2026-10-26의 `wonderland-automation-status` 작업 사본 `.agents/skills/`이며 같은 날 `wonderland-photos`, `wonderland-oneclick-input`, `wonderland-minimax-quality` 사본과 두 파일의 해시가 일치했습니다.

| 원본 스킬 | 원본 SHA-256 |
| --- | --- |
| `instagram-reel/SKILL.md` | `c20ec875e2feeca2d16ebde8fc7c81ee346e2dedd1dbc520489c57c38820003e` |
| `family-reel-meme-preflight/SKILL.md` | `d51a44e706c44b4607ffd3e3d45dc3b0baa446de5a2b7c2939331097c3b61b61` |

공유 범위는 제작·밈 조사·검수·복구 절차입니다. 사진 중심 `instagram-content`와 구분하며, 열린 [PR #27의 `ig-publish`](https://github.com/Pseudo-Lab/no-more-slops/pull/27)는 완성물을 웹으로 Instagram·Threads에 게시하는 단계여서 복사하지 않았습니다. 이번 스킬 갱신은 유료 생성·계정 연결·실제 게시 또는 작품 품질 개선을 실행·검증했다는 뜻이 아닙니다. 기존 #9·#15의 저작자와 제작 당시 검증 기록은 보존합니다.

이번 문서 제출에서 다시 실행한 검사: `python scripts/check_repository.py`는 370개 파일·36개 스킬에서 오류 0건, `python -B -m unittest discover -s scripts -p test_check_repository.py`는 8개 통과, 두 스킬의 `quick_validate.py`와 `git diff --check` 통과입니다. 변경 문서의 관련 상대 링크 15개, 개인 경로·인증키 패턴과 네 작업 사본의 원본 해시 일치도 확인했습니다. 실제 영상 제작·유료 API·Instagram 게시는 다시 실행하지 않았습니다.
