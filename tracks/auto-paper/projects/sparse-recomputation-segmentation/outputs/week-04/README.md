# Week 04 · sparse-recomputation-segmentation

- 트랙: Auto-Paper
- 작성자: [YOOHYOJEONG](https://github.com/YOOHYOJEONG)
- 원 PR: #번호
- 프로젝트 안내: [README](../../README.md)

## 제출물

- [논문 PDF](Sparse%20Recomputation%20and%20Boundary%20Placement%20in%20Transcript%20Segmentation%20-%20Exploratory%20Negative%20Results%20on%20YTSeg%20and%20a%20Preregistered%20Test%20on%20VT-SSum.pdf): *Sparse Recomputation and Boundary Placement in Transcript Segmentation: Exploratory Negative Results on YTSeg and a Preregistered Test on VT-SSum*
- SHA256: `db834377321952e1a445637f3b4325773700e57f831cb738969f8a30c5c87150`
- 코드: [AutoResearchLab 소스 사본](../../app/)

## 상태

프리프린트 초안이며 동료 심사를 받지 않았습니다. 논문의 Limitations에는 사람이 검토하지 않았다고 적혀 있지만, 작성자가 직접 검토했습니다. AutoResearchLab 사이클의 게이트는 통과하지 못했습니다(마지막 점수 58, reject).

## 제작 과정

1. **주제 선정:** AutoResearchLab이 문헌을 조사해 분야 지도를 만들고 후보 9개를 생성했습니다. 전문가 패널 에이전트 4명의 평가와 신규성·실행 가능성 점검을 거쳐, 상위 후보를 자동 선택하는 설정으로 `event_triggered_semantic_memory`가 선정됐습니다.
2. **실험:** VT-SSum 사전등록 검증까지 AutoResearchLab에서 가설 확정, 사전등록, 실험, 심사를 진행했습니다. 런타임은 Codex로 시작해 사용 한도 소진 후 Claude로 전환했습니다. 기준 모델 MiniSeg는 에이전트 레인의 시간 예산을 넘어, 레인 밖에서 직접 재구현해 학습했습니다.
3. **논문 작성:** AutoResearchLab의 논문 초안은 Markdown으로 작성됩니다. 제출한 PDF는 이 초안을 별도로 변환해 만들었습니다.

## 논문 요약

**연구 질문**

- 값싼 트리거로 고정된 호출 예산 안에서 전사 분할 모델의 재계산 시점을 정할 수 있는가?
- 모델의 경계 배치 이점이 학습 벤치마크 밖에서도 유지되는가?

**데이터와 모델**

- 영어 YouTube 전사 YTSeg와 강의 전사 VT-SSum을 텍스트만으로 사용했습니다.
- MiniSeg를 공식 구현 없이 논문을 바탕으로 재구현했습니다.

**결과 1: 희소 재계산 (YTSeg, 탐색적, 호출 예산 12.5%)**

| 지표 (collar 1) | 결과 | 목표 | 판정 |
| --- | --- | --- | --- |
| 학습 트리거 recall | 0.171 (전체 재계산 0.472) | - | - |
| 전체 재계산 대비 recall 비율 | 구간 0.347–0.377 | 0.90 이상 | 미달 |
| 무작위 호출 대비 recall 이득 | 구간 0.051–0.075 | 0.08 이상 | 미달 |

사후 진단에서는 라벨과 모델 적중 위치를 모두 미리 알아도 비율이 0.91이었고, 사용한 호출 조절 방식에서는 완벽한 제안자도 0.54에 그쳤습니다. 따라서 0.90 목표 미달은 신호의 품질보다 목표와 설계의 한계를 더 많이 보여 줍니다.

**결과 2: 경계 배치 (경계 수를 같게 고정)**

YTSeg에서 MiniSeg는 문장 균등 배치보다 collar 1 F1이 0.295 높았습니다(탐색적). 이를 VT-SSum 테스트 958편에서 재학습과 튜닝 없이 사전등록 검증한 결과는 다음과 같습니다.

| 주장 | 추정값 | 시드별 구간 범위 | 기준 | 판정 |
| --- | --- | --- | --- | --- |
| P1: 균등 배치 대비 이점 (collar 1) | 0.056 | 0.044–0.067 | 0.05 | 결론 불가 |
| P2: 무작위 배치 대비 이점 (collar 1) | 0.100 | 0.088–0.109 | 0.05 | 지지 |
| P3: 균등 대비 이점이 collar 0에서 3으로 가며 줄어든 폭 | 0.209 | 0.199–0.218 | 0 | 지지 |
| P4: 배치 효과가 경계 수 효과보다 큼 | -0.280 | -0.298 – -0.262 | 0 | 반증 |

균등 배치 대비 이점은 collar 2와 3에서 역전됐습니다. P4가 반증된 것은 보정하지 않은 모델이 경계 수를 직접 정할 때 32,600개 중 2,429개만 예측했기 때문입니다. 사후 분석에서 peak suppression을 적용하면 collar 1 이점이 0.119까지 올랐고, 더 넓은 설정에서는 역전도 사라졌습니다.

**결론:** 모델 순위는 경계 선택 규칙, 허용 오차, 보정에 따라 달라지므로, 정의가 다른 구간으로 그대로 옮겨진다고 가정하면 안 됩니다.

## 재현과 검증

**이번 제출에서 확인:** 원본과 PDF 사본의 SHA256 일치, `app/`와 원본 커밋의 파일 내용·권한·목록 일치, `python3 scripts/check_repository.py` 오류 0건. `git diff --check`는 `app/` 원본 코드에서 공백 경고 15건을 보고했으며, 원본 보존을 위해 수정하지 않았습니다. README와 PDF에서는 경고가 없었습니다.

**다시 실행하지 않은 것:** 논문의 실험과 수치, 인용, AutoResearchLab 설치와 실행.

**포함하지 않은 것:** 실험 스크립트, 학습 체크포인트, 실행 기록, Markdown 원고, 데이터셋. 따라서 이 폴더만으로 논문 수치를 재현할 수는 없습니다. VT-SSum(CC BY-NC-ND 4.0)과 YTSeg(CC BY-NC-SA 4.0) 데이터는 재배포하지 않습니다.

## 한계

- YTSeg 테스트 분할을 반복해서 열어 보았으므로 YTSeg 결과는 모두 탐색적입니다.
- VT-SSum 가설과 기준은 이미 열어 본 YTSeg 결과에서 나왔고, 라벨은 슬라이드에서 파생된 약한 라벨입니다.
- 모델 학습 시드는 하나이고, 음성·영상 단서와 한국어, 30분 초과 영상에 대한 근거는 없습니다.

## 지표와 레슨런

- 측정 도구 오류가 결론을 바꿀 뻔했습니다. 예를 들어 인과성을 어긴 실행은 C1을 0.830으로 보고했지만, 인과적으로 다시 실행하니 0.347–0.377이었습니다.
- 목표를 정하기 전에 그 목표가 도달 가능한지 먼저 확인해야 합니다.
- 경계 평가는 허용 오차별로 보고하고, 경계 수와 배치를 분리하며, 선택 규칙을 함께 밝혀야 합니다.

---

This work was created as part of the No-More-Slops group activities at Pseudo Lab.

이 결과물은 가짜연구소(Pseudo Lab) No-More-Slops 그룹 활동의 일환으로 제작되었습니다.
