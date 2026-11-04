# Phantom Report

AI 사건사고를 매주 모아 일반인에게 보고하는 인스타그램 캐러셀 채널.

## 운영 원칙
- 타깃: 일반인. 쉽게 풀어서.
- 언어: 한국어 본문 + 영어 키워드·제목 병기.
- 발행: 매주 **토요일**. 수집 기간은 직전 토요일~금요일.
- 호 번호: `FILE 01`(2026-10-10)부터 매주 1씩. 파일 이름은 `file-01`. 사건 번호는 채널 전체 누적(`CASE #001`부터).
- 범위: AI 오작동·실수 / AI 악용 범죄 / 보안·개인정보가 메인. 법·규제와 사회 논란은 큰 건만.
- 사실: 1차 출처(당사자 발표, 기관 자료, 법원·수사기관 문서)로 확인한 것만 싣는다.
- 형식: 주간 묶음 포스트 하나. 단독 포스트는 나중에 검토.

## 슬라이드
- 톤: 기밀 문서 / 수사 보고서. 기준 템플릿은 `design/file-01.html`.
- 구성: 표지 → 사건 목록 → 사건당 1장 → 마무리.
- 사건 장: 설명형 이미지(크게) + 헤드라인 + 요약 1문장 + `→` 행동 1줄 + `SRC:` 줄.
- 슬라이드에 못 넣은 세부 사실과 1차 출처 링크는 캡션에 쓴다.
- 출력: 1080×1350 PNG(인스타 4:5).

## 만드는 법
저장소 루트에서 `cd tracks/auto-post/projects/phantom-report`로 이동합니다. 이 폴더가 아래 명령과 스킬의 작업 기준 경로입니다. `week-NN`은 활동 주차이며 호 번호 `file-NN`과 별도로 기록합니다.

Claude Code에서 이 폴더를 열고 "다음 호 만들자"라고 하면 하네스(`phantom-weekly`)가 진행한다.

```
수집(scout) → ✋ 채택 → 1차 출처 확인(fact-checker) → 원고·캡션(writer) → ✋ 원고 승인
→ 이미지·슬라이드·PNG(phantom-images) → 최종 대조(fact-checker)
```

필요한 것
- Codex CLI에 ChatGPT 계정으로 로그인(이미지 생성). 풀리면 `codex logout && codex login --device-auth`.
- Python + Playwright(Chromium): PNG 렌더링.

스크립트만 따로 돌릴 때
```
python3 scripts/gen_images.py issues/file-NN.prompts.json design/img/file-NN   # 이미지 생성
python3 scripts/render.py design/file-NN.html outputs/week-NN/file-NN                        # PNG + 글 넘침 검사
```

## 폴더
| 경로 | 내용 |
|---|---|
| `issues/file-NN.md` | 호별 작업 기록: 후보, 채택, 1차 출처, 원고, 발행본, 최종 대조 |
| `issues/file-NN.prompts.json` | 장별 이미지 프롬프트 |
| `design/file-NN.html`, `design/img/file-NN/` | 슬라이드와 이미지 원본 |
| `outputs/week-NN/file-NN/` | 업로드할 PNG(커밋 안 함, 다시 뽑을 수 있음)와 `caption.txt` |
| `cases.csv` | 채택한 사건의 누적 CASE 목록 |
| `scripts/` | 이미지 생성, PNG 렌더링 |
| `.claude/agents/` | 프로젝트 전용 에이전트(scout, fact-checker, writer) |
| `../../skills/phantom-weekly/`, `../../skills/phantom-images/` | 트랙에 한 번만 보관하는 하네스 스킬 |
| `devlog/` | 주간 하네스 개선 기록. 매주 발표 자료로 쓴다 |

## 로드맵
수동 제작(FILE 01) → 하네스로 반자동(지금) → 수집·제작 자동화, 사람은 채택·승인만.

## 공통 스킬과 결과물

[phantom-weekly](../../skills/phantom-weekly/SKILL.md)는 이 채널의 주간 제작 흐름을, [phantom-images](../../skills/phantom-images/SKILL.md)는 이미지·PNG 단계를 담당합니다. 범용 Instagram 캐러셀 제작 스킬과 별도로 이 프로젝트의 사건 기록·에이전트·디자인을 사용합니다. 스킬 본문을 프로젝트 안에 복사해 중복 관리하지 않습니다.

Claude Code에서 자동 탐색이 필요하면 프로젝트 폴더에서 다음 로컬 연결을 만듭니다. 연결 폴더는 커밋하지 않습니다.

```sh
mkdir -p .claude/skills
ln -s ../../../../skills/phantom-weekly .claude/skills/phantom-weekly
ln -s ../../../../skills/phantom-images .claude/skills/phantom-images
```

공유하는 결과물은 `outputs/week-NN/`에 놓고 주차별 README에 출처·재현 방법·검증 상태를 기록합니다. [1주차 FILE 01 결과물](outputs/week-01/README.md)을 시작점으로 사용합니다.
