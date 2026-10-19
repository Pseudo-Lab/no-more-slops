# Week 02 · SkillMerge / SecondChance / ProbeFlow v20

- 작성자: [@darkwingduck-code](https://github.com/darkwingduck-code)
- 트랙·프로젝트: Auto-Paper · `tracks/auto-paper/projects/skill-studies`
- 주차: 사용자가 지정한 Week 02. 별도 독립 실험이 추가됐다는 뜻은 아닙니다.
- 상태: 본문·Supp·해설서로 분리한 문서 제출본. 학회 채택·과학적 성능 검증·외부 동료심사 완료가 아닙니다.

## 결과물

| 연구 | 본문 | Supplement | 한국어 해설서 |
|---|---|---|---|
| SkillMerge | [5쪽](v20/build/skillmerge/SkillMerge_v20.pdf) | [38쪽](v20/build/skillmerge/SkillMerge_SUPPLEMENT_v20.pdf) | [22쪽](v20/build/skillmerge/SkillMerge_EXPLAINER_KO_v20.pdf) |
| SecondChance | [5쪽](v20/build/second-chance/SecondChance_v20.pdf) | [39쪽](v20/build/second-chance/SecondChance_SUPPLEMENT_v20.pdf) | [20쪽](v20/build/second-chance/SecondChance_EXPLAINER_KO_v20.pdf) |
| ProbeFlow | [5쪽](v20/build/probeflow/ProbeFlow_v20.pdf) | [35쪽](v20/build/probeflow/ProbeFlow_SUPPLEMENT_v20.pdf) | [41쪽](v20/build/probeflow/ProbeFlow_EXPLAINER_KO_v20.pdf) |

본문은 핵심 주장·방법·결과·한계를 유지하면서 압축했습니다. Supplement는 정의·증명·가정·반례·전체 비교·실패 기록·재현 조건을 상세히 설명하고 v19 원고의 전체 과학적 내용을 보존합니다. 해설서는 수식 풀이·손계산·읽는 순서와 오해하기 쉬운 해석을 보강합니다. 필수 Acknowledgement 추가로 ProbeFlow의 제출용 Supplement만 원본 34쪽에서 35쪽이 됐으며 과학적 원문은 같습니다.

[편집 원문·해설 Markdown·읽기 지도](v20/sources), [Typst/SVG와 조판 결과](v20/build), [원본과 제출본의 해시 연결](v20/ORIGINAL_BINDINGS.json), [전체 파일 목록·해시·PDF 쪽수](v20/MANIFEST.json)를 함께 보관합니다. 제출용 Typst에는 저장소 필수 Acknowledgement만 추가했으며 로컬 Research Forge의 원본 원고와 9개 PDF는 덮어쓰지 않았습니다. 원문의 `source_path`는 원래 Research Forge 작업본의 출처 식별자이며, 이 체크아웃에서 실행할 경로가 아닙니다.

## 제작 절차와 스킬

Research Forge의 로컬 연구 지침과 Codex로 문서를 재구성했습니다. 공개 대응 지침은 기존 [evidence-tracked-research](https://github.com/Pseudo-Lab/no-more-slops/blob/bd80096c57aa0c8137e54769670845912f754165/tracks/auto-paper/skills/evidence-tracked-research/SKILL.md)입니다. 공개 지침의 파일 동일성이나 새 실행 성능을 주장하지 않으며, 이번 업로드에서 스킬을 추가·변경·승격하지 않았습니다.

## 재현 및 검증

다음 명령은 저장소 루트에서 실행합니다. Python 3.11+, 설치된 PyMuPDF, Typst 0.15.1을 사용했습니다. 재조판은 Arial·Malgun Gothic·설치된 Matplotlib의 DejaVu 폰트를 사용하며 폰트 파일은 배포하지 않습니다. 도구는 설치나 네트워크 요청을 수행하지 않습니다. 같은 폰트가 없으면 결과가 달라질 수 있으므로 원본 제출 PDF의 해시 검증과 구분합니다.

```sh
python -B scripts/check_repository.py
python -B -m unittest discover -s scripts -p 'test_check_repository.py' -v
python -B tracks/auto-paper/projects/skill-studies/app/v20/test_build_documents.py
python -B tracks/auto-paper/projects/skill-studies/app/v20/build_documents.py verify
git diff --check
```

문서를 다시 조판할 때는 다음처럼 **아직 없는 절대 출력 경로**를 지정합니다.

```sh
python -B tracks/auto-paper/projects/skill-studies/app/v20/build_documents.py rebuild --out /absolute/new/v20-rebuild
```

Windows 예시는 `--out C:/Temp/skill-studies-v20-rebuild`입니다. 기존 출력은 거절하며 원고·공개 PDF·원본 실행을 덮어쓰지 않습니다. 재조판은 포함된 Typst/SVG의 문서 재현입니다. 데이터 수집·모델 추론·정책 학습·논문 비교 실험의 재실행은 아닙니다. 재컴파일 PDF의 바이트 동일성을 보장하지 않습니다.

[검증 기록](v20/validation)은 이번에 실제 수행한 조판·원문 보존·경계·Acknowledgement 검사와 남은 한계를 기록합니다. 모델/API 호출·새 독립 표본·새 과학 실험은 0입니다. 기존의 한 장비 데이터, 노출된 평가 집합, 저자가 만든 경로 등 과학적 한계는 각 원고에 유지했습니다.

## 지표·레슨런·검토 요청

완성 결과물은 9 PDF입니다. 정확한 쪽수·용량·SHA-256은 MANIFEST와 검증 기록에 있습니다. 읽기 지도는 PDF 목차를 따라 본문·Supp·해설의 대응 절을 연결합니다.

본문의 길이를 줄일 때 부정적 결과나 한계를 함께 줄이지 않는 것이 핵심이었습니다. 자세한 유도와 전체 기록을 Supp로 옮기고, 해설에서는 같은 개념을 실제 숫자로 계산하도록 나눴습니다. 동료에게는 본문만 읽어도 주장과 한계가 분명한지, Supp가 증명에 필요한 가정을 모두 드러내는지, 예제·분모·비교 조건이 일치하는지 검토를 요청합니다. 실제 동료 검토는 아직 받지 않았습니다.

이 업로드는 기존 공개 PR #14·#11을 수정하지 않은 main 기반 별도 브랜치입니다. 관련 PR의 미병합 파일은 로컬 실행의 선행 조건으로 삼지 않습니다. 프로젝트 README 한 파일은 향후 #14와 조율이 필요하며, PR 생성·양방향 병합 검증·원격 CI·병합 완료를 주장하지 않습니다.

이 결과물은 가짜연구소(Pseudo Lab) No-More-Slops 그룹 활동의 일환으로 제작되었습니다.

This work was created as part of the No-More-Slops group activities at Pseudo Lab.
