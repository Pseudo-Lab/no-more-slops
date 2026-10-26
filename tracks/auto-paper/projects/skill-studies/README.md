# skill-studies

SkillMerge, Second-Chance, ProbeFlow 연구 설계 논문과 한국어 해설, 원문·조판 도구·검증 기록을 보관합니다.

**최신 ProbeFlow 교정판:** [v14-20261027 논문·부록·한국어 해설·공개 원문](outputs/week-01/revisions/v14-20261027/README.md). 2026-10-26 완료 원고의 공개 조판 교정판으로, 기존 Week 01 원고의 수정이며 새 주차를 추정하지 않습니다. SkillMerge·Second-Chance의 [v13 제출본](outputs/week-01/revisions/v13-20261018/README.md)과 이전 ProbeFlow 판본, 4페이지 논문·해설·검증 기록은 보존했습니다.

- 작성자: @darkwingduck-code
- 트랙: Auto-Paper
- [1주차 결과물과 재현 안내](outputs/week-01/README.md)
- 원본 PR: [#14](https://github.com/Pseudo-Lab/no-more-slops/pull/14)

## 사용한 연구 자동화 스킬

[evidence-tracked-research](../../skills/evidence-tracked-research/SKILL.md)는 질문·출처·실험·비평·원고·해설·스킬 후보 평가를 연결합니다. 기존 [#14](https://github.com/Pseudo-Lab/no-more-slops/pull/14)와 스킬 PR [#11](https://github.com/Pseudo-Lab/no-more-slops/pull/11)은 이 canonical 파일을 동일한 내용으로 공유했습니다. #11의 프로젝트 설명·스킬 검증 기록과 #14의 논문 결과물은 서로 다른 고유 기여입니다. 이번 교정판은 기존 스킬과 #11을 변경하지 않습니다.

[probeflow-evidence-acquisition](../../skills/probeflow-evidence-acquisition/SKILL.md)은 별도의 연구 참고 후보입니다. 고정된 typed 도구 목록·이미 지불한 공개 관측·공개 권한·남은 예산을 입력받아 다음 획득 행동 하나 또는 허용된 STOP/ABSTAIN과 견적·근거를 반환합니다. 일반 연구 계획을 조합하는 `research-pipeline`, 전체 연구 기록을 잇는 `evidence-tracked-research`, 결과와 원고를 검토하는 `evidence-driven-paper`와 입력·출력·적용 단계가 다릅니다. 모델·사용자 이득이나 전역 설치·활성화는 검증하지 않았습니다.

## ProbeFlow 현재 판본과 검토 범위

[논문](outputs/week-01/revisions/v14-20261027/paper.pdf) · [부록](outputs/week-01/revisions/v14-20261027/supplement.pdf) · [한국어 해설](outputs/week-01/revisions/v14-20261027/explainer.pdf) · [오프라인 HTML](outputs/week-01/revisions/v14-20261027/study.html) · [공개 파일 목록](outputs/week-01/revisions/v14-20261027/PUBLIC_MANIFEST.json) · [판본 출처 연결](outputs/week-01/revisions/v14-20261027/PUBLIC_SOURCE_PROVENANCE.json)

현재 공개 원문의 SHA256은 `c06138d1746b0c982e0550f869e221fa13941390c199f7d957f02cec8e8948e6`, 공개 manifest의 SHA256은 `4a289ebc0cfaaec0ed76716aa32535da5294452a04013d2a24a87c16993d0356`입니다. 논문 묶음 93개와 스킬 후보 2개는 검토 대상으로 고정된 바이트를 보존합니다. 내부 README와 스킬의 [paper-scope.md](../../skills/probeflow-evidence-acquisition/references/paper-scope.md)에 남은 pending·ongoing 문구와 이전 원문·PDF 해시는 당시 작성 기록입니다. 이후 교정판과 별도 검토의 연결은 이 바깥 README와 판본 출처 연결을 기준으로 읽습니다.

아래는 수락된 저자 산출물과 별도 검토 결과의 내용 식별자입니다. 검토 기록 원문과 비공개 실행·조정 기록은 공개하지 않습니다.

| 구분 | 결과 SHA256 | 범위 |
| --- | --- | --- |
| 공개 교정판 작성 | `d48cae4a2b903217adf2b51413fb9c1819c8e59eec710bbf30c9dae0d0fa3b86` | 현재 문서와 표현 교정 |
| 공개 교정판 별도 검토 | `82649b125e81cd0b7bb60cb30ba2062b655c17e4eec71a88d13d865607fe5cdf` | 정확한 문서·보존·가독성·명시적 공개 파일 목록 |
| 스킬 후보 작성 | `8f48380d574c5489dda1341d8267759c6998fc182bc52eabe93cdf27dd5ba6bf` | canonical 후보 2개 파일 |
| 스킬 후보 별도 검토 | `5a9805dc320e81fe806b95e4b86b3ccc745c1ae101e627c481623f6bf33ae3a6` | 정확한 2개 파일과 제한된 관측 행동 |

이 수락은 과학적 사실 인증·스킬 또는 모델 성능 향상 인증이 아닙니다. PDF는 조판 시각 metadata로 바이트 재현성이 보장되지 않으며, 역사적 출처 참조가 있어 단순 문자열 검색의 무일치도 보증하지 않습니다. 공개 범위는 위의 정확한 파일 목록으로 한정합니다.

별도 9회 fit 후속 연구의 원래 실행은 **693 epoch에서 FAILED**이며, H 수치·최종 호출은 **0회**입니다. 이를 완료한 9회 fit이나 독립 최종 성능으로 세지 않습니다. 여섯 과학 영역은 모두 **partial/needs_evidence**이고 과거의 `no_gain`·회귀·동률을 유지합니다. SEFA 및 외부 참조 대비 우월성이나 독립 final 결과는 없습니다. 문서 안의 완료된 finite-model R 결과와 미완료 후속 연구를 구분합니다.

이 결과물은 가짜연구소(Pseudo Lab) No-More-Slops 그룹 활동의 일환으로 제작되었습니다. 저자 기여에는 저장소 [MIT License](../../../../LICENSE)를 적용하고, 인용한 외부 연구·데이터의 권리는 [공개 판본 라이선스 범위](outputs/week-01/revisions/v14-20261027/LICENSE_SCOPE.md)대로 구분합니다.

원고 개정과 조판 검증은 새 모델 효과·학회 채택·스킬 행동 개선을 뜻하지 않습니다. 새 독립 연구 주차가 생기면 같은 프로젝트의 `outputs/week-NN/`에 추가합니다.
