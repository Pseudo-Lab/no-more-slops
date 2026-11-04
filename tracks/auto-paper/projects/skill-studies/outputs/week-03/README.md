# Week 03 · ProbeFlow 작업 논문과 연구 스킬

- 작성자: 임경태 · @darkwingduck-code
- 트랙: Auto-Paper · Week 03
- 판본: 2026-11-02 a04 작업 원고. **최종 문서 검토 대기 초안**입니다.
- 결과: **no_gain / needs_evidence**. arXiv 제출·접수·외부 심사 완료를 뜻하지 않습니다.

| 결과물 | 내용 |
| --- | --- |
| [전체 논문 PDF](paper.pdf) | 22쪽. 이론·방법·실험·결과·한계를 통합한 작업 원고 |
| [전체 보충자료 PDF](supplement.pdf) | 253쪽. 상세 증명·조건·비교·실패·원전 대응 |
| [ProbeFlow SKILL.md](../../../../skills/probeflow-evidence-acquisition/SKILL.md) | 허용된 관측·비용·예산에서 다음 획득 또는 STOP/ABSTAIN을 선택하는 기존 스킬 |
| [판본 명세](manifest.json) | SHA-256·크기·실제 쪽수·검토 상태 |
| [제출 검사](validation.json) | 이번 공개 파일·링크·저장소 형식 검사 범위 |

## 이전 결과와 이번 결과

[Week 01](../week-01/README.md)과 이후 공개된 [v14 판본](https://github.com/Pseudo-Lab/no-more-slops/tree/3f70a914cb94dfb090c6b7b20fd02865e7a57a09/tracks/auto-paper/projects/skill-studies)은 보존합니다. 이번에는 최신 전체 원고를 별도 Week 03에 보관합니다. 이전 17쪽/239쪽 검토본 이후의 조건부 이력 제어 실험과 사후 진단이 포함됐으며, 이 22쪽/253쪽 판본의 최종 문서 검토는 진행 중입니다.

WISDM 개발 자료의 예측기 정확도 25.08%→33.39% 개선과 적응적 정보 수집 효과는 구분합니다. 최신 조건부 제어 실험의 adaptive-minus-static 손실차는 적합 TUNE 약 −0.008661, 사람별 교차검증 +0.033421, CAL +0.018873입니다. CAL 양쪽 전략은 평균 .50·사람별 .25의 예측 비율을 충족했지만 적응 전략은 더 나빴습니다. 사전 규칙은 static을 선택했고 핵심 실증 결론은 no_gain입니다.

CAL 정답을 사용한 사후 최적화는 잠재 class 차이와 전이 초과손실을 구분하는 진단입니다. 배포 정책의 성능이나 새 사람 일반화로 해석하지 않습니다. 원 방법 검토의 근거 공백과 정정된 산술 검토의 제한된 수락도 구분합니다.

## 스킬과 재사용

기존 공개 `probeflow-evidence-acquisition`의 이름·canonical 경로·한 번의 행동 선택 계약을 유지했습니다. 최신 원고 연결, 강한 고정 비교군·coverage·평가 노출·사후 oracle의 해석 기준을 보완했습니다. 프로젝트 안에 실행용 스킬 사본을 두지 않습니다.

`evidence-tracked-research`는 연구 전반의 근거 관리, `research-pipeline`은 연구 계획과 단계 조합, `evidence-driven-paper`는 경험적 논문의 주장 수정에 초점을 둡니다. ProbeFlow 스킬은 주어진 관측/도구 계약 안에서 다음 유료 관측 한 번을 결정합니다. 이번 제출에서 모델을 사용한 스킬 효과 평가는 하지 않았습니다.

## 검증과 재현 범위

PDF는 작업 파일을 바이트 그대로 복사했습니다. 이번 PR에서 과학 본문이나 조판을 바꾸지 않았습니다. 이 주차 폴더에서 다음 명령으로 원본 해시를 확인할 수 있습니다.

```sh
python -c "import hashlib,json,pathlib; p=pathlib.Path('.'); m=json.loads((p/'manifest.json').read_text()); [(print(f['path'],hashlib.sha256((p/f['path']).read_bytes()).hexdigest()==f['sha256'])) for f in m['files']]"
```

저장소 루트의 `python scripts/check_repository.py`와 `python -m unittest discover -s scripts -p test_check_repository.py`는 제출 구조를 검사합니다. 실제 결과는 `validation.json`에 있습니다.

이 제출에는 원 데이터·예측 cache·학습 모델·실험 실행 도구·전체 조판 소스가 없습니다. 문서 열람과 해시 검사는 가능하지만 과학 실험이나 PDF 조판 전체를 이 저장소만으로 재현할 수는 없습니다. 보충자료의 과거 Task/Run 식별자와 상대 경로는 출처 서술이며 내부 원본을 공개한 것은 아닙니다. 새 사람 독립 평가·물리 비용·현대 AFA 방법 재현은 이번 제출에서 수행하지 않았습니다.

## 후속 연구와 리뷰 요청

다음 질문은 신뢰도 구간을 제거하고 구매된 label 전체 이력을 유지했을 때 전이 손실이 줄어드는지입니다. adaptive와 full-six-order static을 같은 조건으로 비교하고 원 full_static도 강한 기준으로 유지합니다. 준비 과제가 실행 중이며 최대18LP의 새 실증 실행은 아직 시작 전입니다. 예측 비율·교차검증·평가 손실·해로운 변화·비용을 함께 보고하며 실패하면 no_gain을 유지합니다.

고정 비교군의 정보·정지 권한, 조건부 이론과 개발 결과의 주장 구분, 후속 질문의 설득력을 검토해 주세요. 쪽수·검사 수·AI의 동의를 연구 효과로 세지 않습니다.

## Acknowledgement

This work was created as part of the No-More-Slops group activities at Pseudo Lab.

이 문구는 이번 공개 제출의 소개에 추가했습니다. 원 PDF에는 별도 삽입하지 않았습니다. 기존 저술과 기여를 보존하며 저장소 MIT License를 따릅니다.
