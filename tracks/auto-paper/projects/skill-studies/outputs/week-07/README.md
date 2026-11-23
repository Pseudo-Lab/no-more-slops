# Week 07 연구 초안 두 편

ProbeFlow에서 강한 비교법과 실패 진단이 연구 질문을 어떻게 바꾸었는지 정리한 논문과, 관계가 있는 불확실한 정답에서 비교 오차를 정확히 최적화하는 별도 STN 논문을 공유합니다. 두 연구의 자료와 성과를 합산하지 않습니다.

- 제출자: 임경태 · [@darkwingduck-code](https://github.com/darkwingduck-code)
- 트랙과 프로젝트: Auto-Paper · skill-studies
- 주차: Week 07 · 2026-11-23~29
- 상태: 동료 검토를 위한 연구 초안. 학회·저널 접수나 채택을 뜻하지 않습니다.
- 이전 제출: [Week 03](../week-03/README.md) · [PR #35](https://github.com/Pseudo-Lab/no-more-slops/pull/35)

| 논문 | PDF | LaTeX 원본 | 현재 범위 |
| --- | --- | --- | --- |
| From Verification Savings to Repair Limits: A Retrospective Methodological Evaluation of ProbeFlow | [12쪽](probeflow/paper.pdf) | [main.tex](probeflow/main.tex) · [참고문헌](probeflow/references.bib) | 기존 연구의 방법론적 선회와 증거 한계를 정리한 후향 연구 |
| Rigid-Block Aggregation for Exact Comparative Absolute-Error Optimization on Temporal Networks | [7쪽](stn/paper.pdf) | [main.tex](stn/main.tex) · [이론](stn/theory.tex) · [결과](stn/results.tex) | 고정 차이 묶음과 합산 손실을 이용한 정확 차원 축소. 익명 기술 초안 표기 유지 |

## 연구에서 확인한 것

ProbeFlow는 가상 확인 비용, 실제 실행 시간, 행동에 필요한 도구 조회, 규칙 수리와 표현 한계, 외부 보안 로그 순서로 질문을 좁혔습니다. 확인 횟수를 줄인 결과가 강한 기준법 우위나 전체 비용 절감으로 이어지지 않은 이유를 설명합니다. 외부 FoRGe의 첫 17과제 확인에서 설명 선호 방법은 macro F1 0.537이었지만 pooled F1은 0.075였고 오탐은 2,409건이었습니다. 같은 17과제를 다시 쓴 반례 후속 탐색에서 pooled F1은 설명 선호 0.598, 같은 후보 집합의 길이 선택 0.260이었습니다. 이는 새로운 자료의 독립 확인이나 기존 자연어 기반 합성법에 대한 우위가 아닙니다. 반환한 반례 22개를 찾는 데 개발 라벨 4,390개를 대조한 비용도 보고합니다.

STN 연구는 모든 가능한 정답에서 차이가 고정된 좌표를 묶고, 원래 가중치와 상수항을 보존한 합산 손실을 탐색합니다. 내부 기울기를 모두 확인해 양 끝값만 같아도 중간 최대가 생기는 오류를 피합니다. 기존 224개와 새 156개를 합친 380개 개발 사례가 원좌표 oracle과 일치했고, 탐색 차원은 52개에서 줄고 증가한 사례는 없었습니다. 별도 16개 설정은 최대 1,024좌표의 입력을 검사했습니다. 새 물리 측정, 독립 holdout, 범용 최적화기 속도 우위는 확인하지 않았습니다.

## 공개 판본과 저자 표시

2026-11-23 로컬 검토본을 보존하고, 두 main.tex에 저장소 필수 Acknowledgements 한 절만 추가한 별도 공개용 PDF를 재조판했습니다. 과학 본문과 수치, 인용, 그림은 유지했습니다. [manifest.json](manifest.json)은 공개 파일의 SHA-256·크기·쪽수와 판본 관계를 기록합니다.

ProbeFlow 원고의 저자는 Gyeongtae Im, Independent Researcher이며 사용자가 제공한 이메일을 유지했습니다. STN은 원본의 `Anonymous technical working draft`를 유지합니다. STN의 책임 저자·저자 순서·소속·연락처·AI 버전·최종 인간 승인은 미확정이며 이번 공유로 확정하지 않습니다.

원자료, 모델 응답, 실험 실행 코드, 내부 검토 로그와 전체 연구 묶음은 포함하지 않습니다. ProbeFlow 부록의 지역 기록 경로와 STN의 source package 서술은 출처 설명이며, 이 공개 폴더에서 접근 가능한 링크가 아닙니다. 여기서는 문서 열람·해시 확인·LaTeX 조판을 재현할 수 있고 과학 실험 전체는 재현할 수 없습니다.

## 조판과 검증

Tectonic 0.17.0으로 두 main.tex를 실제 컴파일했습니다. 각 논문 폴더에서 새 출력 폴더를 만들어 실행합니다.

```sh
mkdir build
tectonic --untrusted --keep-logs --outdir build main.tex
```

동일한 폰트·패키지 자원이 필요하며 첫 실행에는 Tectonic 자원 다운로드가 필요할 수 있습니다. 그림의 상대 경로는 원고와 함께 보존했습니다. 재조판한 PDF의 SHA-256은 생성 시각 등으로 제공본과 달라질 수 있습니다.

이번 공개본 검사에서 필수 문구만의 변경, 원고 텍스트 보존, 실제 PDF의 쪽수·참조·글꼴·페이지 경계와 레이아웃을 확인했습니다. `python -X utf8 scripts/check_repository.py`는 1,187개 파일·60개 스킬에서 오류 0건, `python -X utf8 scripts/test_check_repository.py`는 기존 테스트 9개 통과였습니다. 공개 파일 10개의 스테이징 바이트·해시, 문서 상대 링크 16개, `git diff --cached --check`도 확인했습니다. 새 과학 실험·대상 모델 호출은 0회입니다. 이 검사로 사람 전문가 검토나 연구 우위를 인증하지 않습니다.

## 관련 스킬과 리뷰 요청

기존 [evidence-tracked-research](../../../../skills/evidence-tracked-research/SKILL.md)는 연구 근거와 주장 관리, [probeflow-evidence-acquisition](../../../../skills/probeflow-evidence-acquisition/SKILL.md)는 허용된 정보 획득 선택을 다룹니다. 이번 PR은 결과물 공유이며 스킬을 추가·수정하거나 사본을 만들지 않습니다. 스킬 효과를 새로 평가하지 않았습니다.

ProbeFlow에서는 선회 근거, 동일 정보·후보 집합 비교의 타당성, 다음 독립 확인의 설계를 검토해 주세요. STN에서는 합산 손실 보존, 단조성 판정, 원좌표 검산 범위와 기존 연구 대비 기여를 검토해 주세요. 이전 Week 01·03 파일은 유지하고 다른 열린 PR의 선행 병합을 요구하지 않습니다.

## Acknowledgement

This work was created as part of the No-More-Slops group activities at Pseudo Lab.

기존 저술과 기여를 보존하며 저장소의 MIT License를 따릅니다.
