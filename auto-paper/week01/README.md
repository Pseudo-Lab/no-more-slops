# Auto-Paper · Week 01

논문 한 편을 선행연구 조사부터 영문 투고본까지 만드는 데 쓴 스킬 5개와, 그 결과물인 논문을 담았습니다.

```
week01/
├── skills/   # 논문 작성 단계별 스킬
└── paper/    # 스킬로 작성한 논문 (PDF)
```

## Skills

논문 작성 흐름에 맞춰 아래 순서로 이어서 쓸 수 있고, 각 스킬은 단독으로도 호출할 수 있습니다.

| 순서 | 스킬 | 입력 | 출력 |
| --- | --- | --- | --- |
| 1 | [`research-related-work`](skills/research-related-work/SKILL.md) | 연구 주제 또는 연구계획서 | 선행연구 조사 보고서, 출처·BibTeX |
| 2 | [`draft-conference-paper`](skills/draft-conference-paper/SKILL.md) | 선행연구 조사 결과, 목표 학회명 | 실험 전 초안(Abstract·Introduction·Related Work)의 Word·LaTeX |
| 3 | [`experiment-report-to-paper`](skills/experiment-report-to-paper/SKILL.md) | 실험 결과 리포트(Markdown), 목표 학회명 | 학회 형식의 완성 논문 Word |
| 4 | [`audit-paper-citations`](skills/audit-paper-citations/SKILL.md) | 논문 Word | 인용 검수 보고서(Markdown) 또는 수정 반영 Word |
| 5 | [`translate-paper-to-english`](skills/translate-paper-to-english/SKILL.md) | 한글 논문 Word | 서식을 유지한 영문 Word |

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

[**Boundary Stability for Adaptive Stopping in Diffusion-Based Event Boundary Detection**](paper/Boundary%20Stability%20for%20Adaptive%20Stopping%20in%20Diffusion-Based%20Event%20Boundary%20Detection.pdf)

확산 모델 기반 이벤트 경계 검출(DiffGEBD)에서, 디노이징 단계 사이의 평균 점수 변화가 작아도 검출된 경계는 계속 바뀔 수 있다는 점을 분석한 논문입니다. Kinetics-GEBD 검증 영상 18,797개 중 55.97%에서 이런 불일치가 나타났습니다. 이를 바탕으로 인접한 두 단계의 경계 개수와 위치가 같아지면 추론을 멈추는, 추가 학습이 필요 없는 영상별 조기 종료 규칙을 제안합니다. 확인용 영상 12,900개에서 고정 4-step DDIM 대비 F1@0.05가 0.635%p 오르고 추론 시간은 5.23% 줄었으나, 단일 공개 체크포인트와 이미 관측한 검증 세트에 한정된 결과입니다.

---

This work was created as part of the No-More-Slops group activities at Pseudo Lab.

이 결과물은 가짜연구소(Pseudo Lab) No-More-Slops 그룹 활동의 일환으로 제작되었습니다.
