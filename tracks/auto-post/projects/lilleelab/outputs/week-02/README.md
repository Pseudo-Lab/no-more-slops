# Week 02 결과물

- 작성자: @xiyoon
- 트랙: auto-post
- 원본 PR: [#23](https://github.com/Pseudo-Lab/no-more-slops/pull/23)
- 결과물: 토리든 다이브인 저분자 히알루론산 세럼 50ml
  - 릴스 (19.0초, 12컷, 9:16 1080×1920): https://www.instagram.com/lilleelab.kr/reel/Dep-DD3IBy9/
  - 사진 10장 캐러셀: 콘티 v8 장면으로 다시 만드는 중이라 이번 주에는 올리지 않았습니다
  - 제작 노트 캐러셀 10장: https://www.instagram.com/p/Dep1c03kwMU/
  - 영상·사진 원본은 저장소에 없습니다. 인스타그램 공개 게시물로 봅니다
- 상태: 릴스 공개 2026-10-19, 제작 노트 캐러셀 공개 2026-10-19
- 사용한 스킬: [ad-planning](../../../../skills/ad-planning/SKILL.md), [product-cgi-render](../../../../skills/product-cgi-render/SKILL.md)
- 파이프라인: [docs/pipeline.md](../../docs/pipeline.md)

## 폴더

| 경로 | 내용 |
| --- | --- |
| [torriden-divein-serum/caption.md](torriden-divein-serum/caption.md) | 릴스·사진 캡션, 해시태그, 표기 확인, 게시할 때 사람이 할 일 |
| [torriden-divein-serum/sources.md](torriden-divein-serum/sources.md) | 효능 문구 출처(공식 상세), 레퍼런스, 미디어 권리, CC0 효과음 출처 |
| [torriden-divein-serum/storyboard.md](torriden-divein-serum/storyboard.md) | 확정 콘티 v8 (12컷, 컷별 제작 방식·실패 시 대체·통과 기준) |
| [torriden-divein-serum/planning/](torriden-divein-serum/planning/) | 제품 분석·특징 추출, 리서치, 스토리라인(`idea.md`, 스킬로 다시 쓴 `idea-skill.md`) |
| [torriden-divein-serum/report/agency-review.md](torriden-divein-serum/report/agency-review.md) | 에이전시 PM 검토 기록 (콘티 v4 → v8 라운드 5) |
| [torriden-divein-serum/report/qc.md](torriden-divein-serum/report/qc.md) | 제작 QC 라운드별 판정과 근거 |
| [torriden-divein-serum/report/production-log.md](torriden-divein-serum/report/production-log.md) | 제작 한 바퀴마다 바꾼 것과 렌더 시간 |
| [torriden-divein-serum/report/cost.md](torriden-divein-serum/report/cost.md) | 단계별 도구, 생성 건수, 비용, 소요 시간 |

## 재현 및 검증

- 스킬 시험: `sh skills/product-cgi-render/tests/run_tests.sh` → 23개 중 22개 통과, 1개 건너뜀(오버레이 시험, `puppeteer-core` 미설치). Blender 시험(`BLENDER_SMOKE=1`)은 이 실행에 포함하지 않았습니다
- 최종 조립 점검(조립 스크립트의 점검 단계):
  - 길이 570프레임 = 19.0초, 영상·소리 길이 일치, H.264 High 1080×1920 30fps + AAC 48kHz
  - 순백(255) 픽셀 0개
  - 루프 이음매(마지막 → 첫 프레임 평균색 차): 최대 4.9, 기준 10 이하 → 통과
  - 처음 점검에서는 이음매 10.7로 실패했습니다. 원인은 영상이 아니라 조립 스크립트 버그(프레임이 빠져 마지막 프레임이 바뀜)였고, 스크립트를 고친 뒤 다시 점검해 통과했습니다
- 확인하지 못한 범위: 실제 휴대폰 화면에서의 재생, 소리의 귀 확인은 사람 확인 대상. 원본 영상은 공개하지 않으므로 위 수치는 이 저장소에서 다시 잴 수 없습니다

## 지표와 레슨런

- 유료 API: OpenAI 이미지 생성 약 $0.22 (초기 콘티 v3 시험, 사람 승인 $2 한도 안). 최종 릴스에는 쓰지 않았습니다
- Google Flow(Veo): 사람 계정 크레딧으로 따로 사용. 액체 컷 3개(컷 6·7·9)에 사용 <!-- 사용 크레딧 사람 확인 -->
- 소요 시간: `cost.md` 기록 44행 합계 약 37.5시간(렌더 대기 포함). v8 본 제작 렌더 기록 합계 약 6.6시간 이상(일부 대기열 로그 미합산)으로, 콘티 추정 4시간 16분을 넘었습니다
- 토큰: 대부분 미계측. 서브에이전트 집계분만 약 87만 토큰
- 게시 지표: <!-- 게시 후 metrics.md에서 조회수, 저장, 공유, 제휴 클릭·수익 -->

레슨런 5개는 PR 본문과 같습니다.

1. 콘티를 v1 → v8까지 다시 짰고, 판마다 새 context의 에이전시 PM이 점수를 매겼습니다(6 → 9 / 10, v8 최종 8.5 / 10)
2. QC는 수치 기준(255 픽셀 0개, 세계 평균색 채널당 10 이하, 루프 이음매 10 이하)으로 통과시켰습니다
3. Flow는 라벨 글자를 약 0.5초 안에 바꿉니다. 라벨이 보이는 컷은 Blender로만 만들고, 액체 컷 6·7·9만 Flow로 만들었습니다
4. 한 대의 Mac에서 렌더를 동시에 돌리면 2~3배 느렸습니다. 한 번에 하나씩 돌립니다
5. 렌더 스킬은 룩 상수 블록과 Blender 없이 도는 시험으로 다른 제품에도 쓸 수 있게 일반화했습니다
