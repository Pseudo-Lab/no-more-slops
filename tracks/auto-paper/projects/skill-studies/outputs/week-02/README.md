# Week 02 최종 결과물 · SkillMerge / SecondChance / ProbeFlow v21.1

- 작성자: [@darkwingduck-code](https://github.com/darkwingduck-code)
- 트랙·프로젝트: Auto-Paper · `tracks/auto-paper/projects/skill-studies`
- 사용한 연구 자동화 스킬: [evidence-tracked-research/SKILL.md](../../../../skills/evidence-tracked-research/SKILL.md)
- 상태: 기존 저장 근거의 유한 후속 분석과 연구 원고. 학회 채택·외부 동료심사·독립 실험 완료가 아닙니다.
- 판본: 과학 원고·PDF는 v21, 한국어 요약·후보 문자의 표시 수정판은 v21.1입니다.

## 결과물

최종 9개 PDF와 실제 쪽수·SHA-256은 [MANIFEST](v21/MANIFEST.json)에 기록합니다.

| 연구 | 본문 | Supplement | 한국어 해설서 |
|---|---|---|---|
| SkillMerge | [5쪽](v21/build/skillmerge/SkillMerge_v21.pdf) | [45쪽](v21/build/skillmerge/SkillMerge_SUPPLEMENT_v21.pdf) | [25쪽](v21/build/skillmerge/SkillMerge_EXPLAINER_KO_v21.pdf) |
| SecondChance | [5쪽](v21/build/second-chance/SecondChance_v21.pdf) | [43쪽](v21/build/second-chance/SecondChance_SUPPLEMENT_v21.pdf) | [23쪽](v21/build/second-chance/SecondChance_EXPLAINER_KO_v21.pdf) |
| ProbeFlow | [5쪽](v21/build/probeflow/ProbeFlow_v21.pdf) | [38쪽](v21/build/probeflow/ProbeFlow_SUPPLEMENT_v21.pdf) | [43쪽](v21/build/probeflow/ProbeFlow_EXPLAINER_KO_v21.pdf) |

본문은 핵심 질문·방법·결과·한계를 짧게 유지합니다. Supplement에는 증명·전체 비교·반례·실행 조건을, 해설에는 당위성·절차·수식의 쉬운 풀이를 담았습니다. 제출용 Typst/PDF 사본에만 저장소 필수 Acknowledgement를 추가하며 Research Forge 원본은 보존합니다. 제출본의 쪽수 변화와 원본·제출본의 해시는 [ORIGINAL_BINDINGS](v21/ORIGINAL_BINDINGS.json)와 [검증 기록](v21/validation)에 남깁니다.

감사 문구 때문에 ProbeFlow Supplement만 원본37쪽에서 제출본38쪽으로 늘었습니다. 공개 해설 Markdown의 그림 링크23개는 이 패키지의 SVG 경로로 연결했고, 포함하지 않은 과거 작업본 링크2개는 원출처 경로 설명으로 바꿨습니다. 다른 과학적 원문은 유지하며 이 링크 변환도 별도 기록에 남깁니다.

## 이번 연구의 진전과 범위

- **SkillMerge:** 정답을 읽지 않는 prefix 가드의 조건부 필요충분성을 논증했습니다. 두 완전 입력이 각각 주석상 충분한 12,067쌍에서 cap1/2/3 이득·손실은 563/0·95/0·0/0입니다. 전체 22,794쌍의 cap1에는 487손실과 포기한 2이득이 남습니다. 실제 Q자격·독립 스킬 실행 효과와 구별합니다.
- **SecondChance:** 33,658개 일정–계약 조합, 고유(B,일정)25,904개를 비교했습니다. 기존 72정책 행 중 44개는 전체 오프라인 frontier에 지배됩니다. B8/q3의 최종 폭·면적(1/24,73/64)은 FIFO·late보다 좋지만 미래 구조를 읽는 특권과 즉시 quote에 조건부이며 온라인 달성 효과가 아닙니다.
- **ProbeFlow:** 같은 421cycle에서 k1의 두 leaf는 각 cycle의 component/vector 오류 점수가 같고 비용만 다릅니다. 고정 g129는 quote22개를 더 씁니다. Secondary의 고정 정책 차이는 `(-63+103α−432λ)/1684`이며 원래 λ0에서 선택한 정책의 사후 민감도입니다. 새 선호의 정책 재선택 비교나 물리 에너지 실측이 아닙니다.

[원고·해설·장부](v21/sources), [새 분석 계획·결과·검산 영수증](v21/evidence), [참고자료 읽기 지도](v21/sources/learning/research-reading.json)를 함께 보관합니다. 핵심 자료10개의 방법·비교 조건·분할·권한·한계는 각 연구의 `literature/RESOURCES.json`에 있습니다. 외부 자료의 원문 전체·데이터셋·예측 캐시는 배포하지 않습니다.

저장 근거의 새 분석은 3건입니다. 새 독립 표본, 새 모델/API 실험, 외부 방법의 native 재현, 실제 교수 자문, 전역 스킬 승격은 모두 0입니다. 별도 구현 검산과 Codex lane의 제한 검토는 외부 독립 과학 재현이 아닙니다.

## 연구 자동화 스킬

[기존 canonical 스킬](../../../../skills/evidence-tracked-research/SKILL.md)의 v13 전체 원문을 보존하고 v21의 세 판단 경계를 추가했습니다. 다른 이름의 중복 연구 스킬을 만들지 않았습니다. 스킬은 질문·근거·대조 설계·실행 보존·주장 검토·원고/해설 동기화·후보 평가를 다루며, PDF 포장만 수행하는 아래 조판 도구와 다릅니다.

[출처와 후보 상태](../../../../skills/evidence-tracked-research/references/v21-provenance.json)에 원 공개본·로컬 후보·활성본의 서로 다른 해시를 기록합니다. 절차 개정은 미평가 후보이며 로컬 활성 스킬을 교체하지 않았고 개선 효과를 측정하지 않았습니다.

## 재현 및 실제 검증 범위

저장소 루트에서 실행합니다. Python 3.11+, 이미 설치된 PyMuPDF와 Typst 0.15.1 및 폰트를 사용하며 자동 설치·네트워크·모델 호출을 수행하지 않습니다.

```sh
python -B scripts/check_repository.py
python -B -m unittest discover -s scripts -p 'test_check_repository.py' -v
python -B tracks/auto-paper/projects/skill-studies/app/v21/test_build_documents.py
python -B tracks/auto-paper/projects/skill-studies/app/v21/build_documents.py verify
git diff --check
```

새 디렉터리에 문서를 다시 조판하려면 다음 명령을 사용합니다.

```sh
python -B tracks/auto-paper/projects/skill-studies/app/v21/build_documents.py rebuild --out /absolute/new/v21-rebuild
```

Windows 예시는 `--out C:/Temp/skill-studies-v21-rebuild`입니다. 기존 출력은 거절합니다. 폰트와 PDF metadata에 따라 재컴파일 바이트는 달라질 수 있습니다. [문서 도구 안내](../../app/v21/README.md)와 검증 영수증에서 모의 경계 검사·실제 재조판·원문 보존·선택 페이지 시각 검토를 구별합니다.

여기서 재현 가능한 것은 포함된 Typst/SVG의 문서 조판과 제출 파일 무결성입니다. 저장 결과·계획·입력 해시는 연구 기록이며, 원자료·예측 캐시를 포함하지 않아 과학 실험을 재실행하지 않습니다. 원문의 `source_path`는 원래 작업본의 출처 식별자이며 이 체크아웃의 실행 경로가 아닙니다.

## 이력·검토 요청

기존 2주차 v20 대신 현재 결과물을 기본 진입점으로 교체했습니다. [이전 제출물·바이너리](https://github.com/Pseudo-Lab/no-more-slops/tree/a400814fef58a7ffa7246dc6c69d4a70c4f65922/tracks/auto-paper/projects/skill-studies/outputs/week-02)는 Git 커밋에 보존합니다. 1주차 자료를 변경하지 않습니다.

동료에게는 조건부 보장과 실제 행동 효과, 오프라인 기준과 온라인 권한, 오류·비용의 교환 관계가 충분히 구분되는지 검토를 요청합니다. 이번 업로드는 기존 2주차 브랜치 업데이트이며 새 PR 생성·기존 PR11/14 수정·원격 CI·병합 완료를 뜻하지 않습니다. 향후 PR 제출에는 공유 README·스킬의 조율과 양방향 병합 검증이 필요합니다.

이 결과물은 가짜연구소(Pseudo Lab) No-More-Slops 그룹 활동의 일환으로 제작되었습니다.

This work was created as part of the No-More-Slops group activities at Pseudo Lab.
