# 골든셋 라벨 오류와 모델 선택 결정

- 작성자: @sooyoung-wind
- 트랙: Auto-Paper
- 상태: Week 04 실험 초안. 선행 리뷰 [golden-dataset-review](../golden-dataset-review/)의 연구 공백(5.2절의 첫째와 넷째)을 실험으로 검증. 논문은 ACL 형식(심사용 익명 원고)
- 원고 언어: 한국어 (영문 초록 병기)

골든셋의 라벨 오류가 모델 쌍 비교 결정(배포 결정)을 얼마나 바꾸는지 측정합니다. MMLU-Redux 2.0의 전문가 수정 라벨과 Open LLM Leaderboard에 공개된 모델 42종의 문항별 예측을 사용하며, API 비용은 들지 않습니다.

## 핵심 결과 (v2, 심사 1라운드 반영)

- 전체 셋(5,421문항)에서 라벨을 수정해도 순위는 거의 그대로였고(Kendall τ 0.99), δ=3%p 결정 반전은 861쌍 중 8건이었습니다.
- 과목 단위 소형 셋(76–100문항)에서는 반전율이 과목의 수정 문항 비율과 함께 증가했고(Spearman ρ=0.97), virology에서는 36%에 달했습니다.
- 모든 조건에서 승자 역전은 0건이었습니다. 라벨 오류는 모델 간 격차를 압축해 결정을 "보류"로 바꿉니다.
- 무작위 라벨 오류의 반전율은 라벨 오류 없이 같은 수의 문항을 교체한 기준선의 1.0–1.2배였습니다. 반면 어려운 문항을 대표 오답으로 잘못 표시하는 체계적 오류는 무작위 오류의 1.4–1.6배였습니다(교차 적합, 2×2 소거).
- 실제 오류의 43%가 모델들의 대표 오답과 같았습니다(우연 33%, p=0.028).
- 리뷰의 감사 기준(509문항 오류 0건)은 Wilson 상한 ≤ δ/4와 동치입니다. 그 경계 오류율에서 870문항 셋의 반전율은 0.8–1.1%였습니다.

## 구조

| 경로 | 내용 |
| --- | --- |
| [docs/design.md](docs/design.md) | 연구 질문, 데이터, 결정 규칙, 실험 설계 |
| `app/fetch.py` | MMLU-Redux와 리더보드 문항별 예측 다운로드(→ `data/`, git 제외, 약 130MB) |
| `app/load.py` | 문항 결합과 라벨 조건(ok, 수정 가능, 미해결) |
| `app/analyze.py` | E1 자연 실험, E2 오류 주입, E3 감사 작동 특성 |
| `app/figures.py`, `app/tables.py` | 그림(PDF, PNG)과 논문 표 생성(결과 파일에서 직접 생성) |
| `app/build_paper.sh` | 논문 PDF 빌드(ACL 공식 스타일, XeLaTeX) |
| [results/](results/) | 실험 결과(CSV, JSON)와 그림 |
| [reviews/](reviews/) | 심사 보고서와 반영 내역 |
| [outputs/week-04/](outputs/week-04/) | 논문 초안(LaTeX 원본, PDF, Markdown 판) |

## 실행

```bash
cd app
uv run python fetch.py      # 데이터 다운로드(인증 없이 약 1시간)
uv run python analyze.py    # 결과 CSV(약 1–2분)
cd ..
app/build_paper.sh          # 그림과 표를 다시 만들고 outputs/week-04/paper.pdf 빌드
```

PDF 빌드에는 [Tectonic](https://tectonic-typesetting.github.io/)(`brew install tectonic`)이 필요합니다. ACL 공식 스타일 파일(`acl-org/acl-style-files`)은 재배포를 허락하는 라이선스 표기가 없고 수정이 금지되어 있어 저장소에 넣지 않았습니다. 빌드 스크립트가 고정 커밋에서 내려받아 `outputs/week-04/.build/`(git 제외)에 둡니다. 한글 글꼴 Noto Serif KR(SIL OFL)도 같은 방식으로 내려받습니다.

## 사용한 스킬과 도구

Claude Code(Opus 5.5)로 주제 선정, 설계, 코드, 분석, 원고를 작성했습니다. 주제는 선행 리뷰의 연구 공백 네 가지 중 사용자가 선택했습니다.
