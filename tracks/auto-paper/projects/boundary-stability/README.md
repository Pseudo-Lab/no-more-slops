# boundary-stability

Auto-Paper 트랙의 [YOOHYOJEONG](https://github.com/YOOHYOJEONG) 기여입니다. 원 PR: [#4](https://github.com/Pseudo-Lab/no-more-slops/pull/4).

[1주차 결과물과 검증 범위](outputs/week-01/README.md)를 확인하세요.

## 재사용 스킬

| 스킬 | 적용 범위 |
| --- | --- |
| [audit-paper-citations](../../skills/audit-paper-citations/SKILL.md) | Word 논문의 인용·서지 정보와 원문 부합성 검수 |
| [draft-conference-paper](../../skills/draft-conference-paper/SKILL.md) | 실험 전 선행연구 자료에서 학회 초안 작성 |
| [experiment-report-to-paper](../../skills/experiment-report-to-paper/SKILL.md) | 완료된 실험 리포트를 학회 형식 Word 논문으로 작성 |
| [research-related-work](../../skills/research-related-work/SKILL.md) | 연구 주제의 문헌 검색과 원문·BibTeX 근거 정리 |
| [translate-paper-to-english](../../skills/translate-paper-to-english/SKILL.md) | 국문 Word 논문의 서식을 유지하는 영문 번역 |

같은 이름의 스킬을 주차별로 복사하지 않고 `tracks/auto-paper/skills/`의 기존 스킬을 개선합니다. 비슷한 스킬은 위 입력·역할 범위를 기준으로 선택합니다.

## 원 기여 소개

# Auto-Paper · Week 01

논문 한 편을 선행연구 조사부터 영문 투고본까지 만드는 데 쓴 스킬 5개와, 그 결과물인 논문을 담았습니다.

스킬은 `../../skills/`에, 논문은 `outputs/week-01/`에 모았습니다.

## Skills

논문 작성 흐름에 맞춰 아래 순서로 이어서 쓸 수 있고, 각 스킬은 단독으로도 호출할 수 있습니다.

| 순서 | 스킬 | 입력 | 출력 |
| --- | --- | --- | --- |
| 1 | [`research-related-work`](../../skills/research-related-work/SKILL.md) | 연구 주제 또는 연구계획서 | 선행연구 조사 보고서, 출처·BibTeX |
| 2 | [`draft-conference-paper`](../../skills/draft-conference-paper/SKILL.md) | 선행연구 조사 결과, 목표 학회명 | 실험 전 초안(Abstract·Introduction·Related Work)의 Word·LaTeX |
| 3 | [`experiment-report-to-paper`](../../skills/experiment-report-to-paper/SKILL.md) | 실험 결과 리포트(Markdown), 목표 학회명 | 학회 형식의 완성 논문 Word |
| 4 | [`audit-paper-citations`](../../skills/audit-paper-citations/SKILL.md) | 논문 Word | 인용 검수 보고서(Markdown) 또는 수정 반영 Word |
| 5 | [`translate-paper-to-english`](../../skills/translate-paper-to-english/SKILL.md) | 한글 논문 Word | 서식을 유지한 영문 Word |

### 전체 사용 예시

아래는 GEBD 조기 종료 연구를 준비할 때 다섯 스킬의 입력과 출력을 연결하는 **호출 예시**입니다. 이 예시를 새로 실행한 기록은 아니며, 1주차 논문의 재현 명령도 아닙니다. 이 PR에는 실험 리포트와 편집 가능한 Word 원본이 포함되어 있지 않으므로, 실험 후 단계에는 사용자가 실제로 확보한 자료가 필요합니다.

스킬이 등록된 환경에서는 `$스킬이름`으로 호출합니다. 등록되지 않았다면 위 표의 `SKILL.md`를 열고, 에이전트에게 해당 파일의 실제 경로와 아래 입력을 주면서 "이 스킬을 읽고 실행해 줘"라고 요청합니다. 저장소를 내려받은 것만으로 스킬이 등록되지는 않습니다.

실행 전에 연구 주제, 목표 학회·연도·트랙, 새 출력 폴더를 정합니다. 아래의 `work/boundary-example/`은 사용자가 선택할 작업 폴더의 예시이며, 각 호출 전에 실제 경로로 바꿉니다. `ICML`도 호출 형식을 보여주기 위한 예시 학회명입니다. 공식 규정과 양식의 적용 상태는 실행할 때 확인합니다.

1. 선행연구를 조사하고 이후 초안의 근거로 사용할 파일을 만듭니다.

   ```text
   $research-related-work
   주제: GEBD에서 디노이징 단계 사이의 경계 안정성을 이용한 영상별 조기 종료
   조사 범위: 실행일 기준 최근 5년, 기반 문헌은 별도 표시
   언어: 한국어
   저장 위치: work/boundary-example/literature/
   report.md, references.bib, search-log.md에 실제 확인한 원문과 근거 위치를 남겨 줘.
   ```

2. 생성된 조사 파일을 읽어 실험 전 초안을 작성합니다.

   ```text
   $draft-conference-paper
   선행연구 파일: work/boundary-example/literature/report.md,
                  work/boundary-example/literature/references.bib,
                  work/boundary-example/literature/search-log.md
   목표 학회: ICML, 연도·트랙은 내가 확정한 값을 적용
   언어: 국문 검토본
   저장 위치: work/boundary-example/draft/
   Abstract, Introduction, Related Work의 Word·LaTeX 초안과 draft-notes.md를 만들어 줘.
   실험 전 가설과 이미 확인한 기존 연구 결과를 구분해 줘.
   ```

3. 사용자가 별도로 실험을 완료한 뒤, 실제 실험 리포트를 근거로 완성 원고를 작성합니다. 이 다섯 스킬은 실험 실행을 담당하지 않습니다. `experiment-report.md`에는 데이터 분할, 선택·튜닝 이력, 모델·체크포인트, 비교 방법, 지표·단위, 시간 측정 조건과 완료·미완료 실험을 적고 실제 결과 파일을 연결합니다.

   ```text
   $experiment-report-to-paper
   실험 리포트: work/boundary-example/experiment-report.md
   기존 초안과 서지: 2단계에서 실제 생성된 파일
   목표 학회·연도·트랙: 2단계와 동일
   언어: 국문 검토본
   저장 위치: work/boundary-example/manuscript/paper_ko.docx
   보고서에 근거한 수치·표·그림만 사용하고 비교 조건과 한계를 보존해 줘.
   편집 가능한 Word를 저장하고 실제 수행한 내용·인용·렌더링 검사를 보고해 줘.
   ```

4. 완성된 국문 Word의 인용을 검수하고, 확인된 오류를 반영한 별도 원고를 만듭니다.

   ```text
   $audit-paper-citations
   원고: work/boundary-example/manuscript/paper_ko.docx
   참고자료: 1단계 references.bib와 실제 확보한 논문 원문·공식 링크
   저장 위치: work/boundary-example/audit/
   인용·서지를 검수하고 확인된 오류를 수정해 줘.
   원본을 보존하고 paper_ko_citation_reviewed.docx와 검수 Markdown을 함께 저장해 줘.
   원문 접근 실패와 미확인 항목을 검수 결과에 남겨 줘.
   ```

5. 검수한 국문 Word를 번역합니다. 4단계에서 실제 생성된 파일을 입력으로 사용합니다.

   ```text
   $translate-paper-to-english
   논문 파일: work/boundary-example/audit/paper_ko_citation_reviewed.docx
   목표 분야: 영상 이벤트 경계 검출
   저장 위치: work/boundary-example/english/
   원본의 수치·수식·표·그림·서지를 유지하며 영문 Word로 번역해 줘.
   용어 대응표, 숫자 대조 결과, 실제 렌더링 범위와 남은 미확인 항목을 보고해 줘.
   ```

번역의 기본 출력명은 `paper_ko_citation_reviewed_en.docx`입니다. 다음 단계에는 각 스킬이 실제 반환한 파일 경로를 전달합니다. 원문 접근, 문서 렌더링 또는 LaTeX 컴파일이 실패하면 그 단계를 완료로 표시하지 않습니다. 최종 PDF가 필요하면 확인한 영문 Word를 별도로 렌더링하고 배치를 확인합니다. 번역 결과만으로 투고 준비가 끝났다고 표시하지 않습니다.

### 문헌과 작성 안내를 확인할 수 있는 사이트

| 사이트 | 사용 목적과 확인할 범위 |
| --- | --- |
| [arXiv](https://arxiv.org/) | 저자 공개 원문과 버전·최초 공개일 확인. 사전공개 상태와 정식 출판 상태를 구분합니다. |
| [CVF Open Access](https://openaccess.thecvf.com/) | 컴퓨터 비전 학회 논문 원문과 보충자료 확인. 찾는 논문의 실제 공개 범위를 기록합니다. |
| [Proceedings of Machine Learning Research](https://proceedings.mlr.press/) | ICML 등 머신러닝 학회 논문 원문과 서지 확인. 투고 양식은 목표 회차의 공식 저자 안내에서 따로 확인합니다. |
| [How to Read a Paper](https://web.stanford.edu/class/ee384m/Handouts/HowtoReadPaper.pdf) | 리뷰에서 추천한 논문 읽기 안내의 공개 사본입니다. 스킬의 실제 인용 검수 기록을 대신하지 않습니다. |

위 링크는 공개 열람 경로이며 실행 시 다시 접근 여부를 확인합니다. 개별 원문·코드·가중치·데이터의 접근 조건은 다를 수 있습니다. 이 안내 추가 과정에서는 링크 응답과 저장소 내 참조 경로만 확인했고, 문헌 조사·실험·원고 작성·인용 검수·번역을 다시 실행하지 않았습니다.

### research-related-work

주제를 검색 가능한 요소로 나눠 최신 학술 선행연구를 찾고, 원문과 서지정보를 직접 확인합니다. 방법 중복, 필요한 비교 실험, 재현 가능성을 정리해 연구의 차별성을 검토합니다.

### draft-conference-paper

조사 결과를 "확인된 근거"와 "연구 계획"으로 구분한 뒤, 목표 학회의 공식 양식을 확인해 실험 전 단계의 Abstract, Introduction, Related Work를 국문 또는 영문으로 작성합니다.

### experiment-report-to-paper

실험 리포트에서 주장할 수 있는 결과의 범위를 먼저 확정하고, 그 수치만으로 본문·표·그림·캡션을 작성합니다. 참고문헌 확인과 문서 렌더링 검수까지 포함합니다. 새 실험을 실행하지는 않습니다.

### audit-paper-citations

본문 인용과 참고문헌의 연결, 논문의 실재 여부와 서지 정보, 인용한 주장이 원문과 맞는지를 검수합니다. 검수만 요청하면 원본을 그대로 두고 결과 표를 저장하고, 수정을 요청하면 확인된 사항을 반영한 Word를 새로 만듭니다.

### translate-paper-to-english

문단을 추출해 용어집을 먼저 확정한 뒤, 해당 분야 영어 논문의 용어와 문체로 번역합니다. 원본의 서식·수식·표·그림·참고문헌은 유지하며, 추출과 적용에는 `scripts/`의 Python 스크립트를 씁니다.

### 스킬 폴더 구성

- `SKILL.md`: 스킬 정의와 작업 절차
- `references/`: 보고서 형식, 검증 기준 등 스킬이 참조하는 문서
- `agents/openai.yaml`: Codex용 표시 이름과 기본 프롬프트
- `scripts/`: 스킬이 실행하는 스크립트 (`translate-paper-to-english`에만 있음)

## Paper

[**Boundary Stability for Adaptive Stopping in Diffusion-Based Event Boundary Detection**](outputs/week-01/Boundary%20Stability%20for%20Adaptive%20Stopping%20in%20Diffusion-Based%20Event%20Boundary%20Detection.pdf)

확산 모델 기반 이벤트 경계 검출(DiffGEBD)에서, 디노이징 단계 사이의 평균 점수 변화가 작아도 검출된 경계는 계속 바뀔 수 있다는 점을 분석한 논문입니다. Kinetics-GEBD 검증 영상 18,797개 중 55.97%에서 이런 불일치가 나타났습니다. 이를 바탕으로 인접한 두 단계의 경계 개수와 위치가 같아지면 추론을 멈추는, 추가 학습이 필요 없는 영상별 조기 종료 규칙을 제안합니다. 확인용 영상 12,900개에서 고정 4-step DDIM 대비 F1@0.05가 0.635%p 오르고 추론 시간은 5.23% 줄었으나, 단일 공개 체크포인트와 이미 관측한 검증 세트에 한정된 결과입니다.

---

This work was created as part of the No-More-Slops group activities at Pseudo Lab.

이 결과물은 가짜연구소(Pseudo Lab) No-More-Slops 그룹 활동의 일환으로 제작되었습니다.
