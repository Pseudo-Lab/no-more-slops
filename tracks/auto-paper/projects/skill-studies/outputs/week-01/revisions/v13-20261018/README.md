# Week 01 원고 수정본 · v13-20261018

- 작성자: @darkwingduck-code
- 트랙: Auto-Paper
- 기존 기여: [PR #14](https://github.com/Pseudo-Lab/no-more-slops/pull/14)의 Week 01 수정본. 새 주차를 뜻하지 않는다.
- 상태: Research Forge v13의 학술 논문 구조를 유지한 개발 중 working paper 3편. 문헌 검토와 기존 v11/v12 근거를 정리한 원고 개정이며 새 실험·학회 제출·외부 심사·채택 기록이 아니다.
- 사용한 연구 자동화 스킬: [evidence-tracked-research](../../../../../../skills/evidence-tracked-research/SKILL.md). 아래 도구는 문서 조판·검증용이며 연구 pipeline이나 모델 실행기를 동봉한 것이 아니다.

| 논문 | 제출용 PDF | 쪽수 | 참고문헌 | SVG 그림 | 원문과 학습 자료 |
| --- | --- | ---: | ---: | ---: | --- |
| SkillMerge | [SkillMerge_v13_nms.pdf](build/skillmerge/SkillMerge_v13_nms.pdf) | 13 | 19 | 3 | [paper.json](sources/skillmerge/paper.json) · [한국어 해설](sources/skillmerge/EXPLAINER_KO.md) · [출처](sources/skillmerge/SOURCES.json) · [주장](sources/skillmerge/CLAIMS.json) |
| SecondChance | [SecondChance_v13_nms.pdf](build/second_chance/SecondChance_v13_nms.pdf) | 14 | 19 | 3 | [paper.json](sources/second_chance/paper.json) · [한국어 해설](sources/second_chance/EXPLAINER_KO.md) · [출처](sources/second_chance/SOURCES.json) · [주장](sources/second_chance/CLAIMS.json) |
| ProbeFlow | [ProbeFlow_v13_nms.pdf](build/probeflow/ProbeFlow_v13_nms.pdf) | 12 | 18 | 3 | [paper.json](sources/probeflow/paper.json) · [한국어 해설](sources/probeflow/EXPLAINER_KO.md) · [출처](sources/probeflow/SOURCES.json) · [주장](sources/probeflow/CLAIMS.json) |

원본 paper.json·SOURCES.json·CLAIMS.json·EXPLAINER_KO.md와 그림 9개는 보존한 Research Forge v13 원문과 **같은 바이트**다. 제출용 파생 PDF에서만 References 바로 앞에 번호 없는 Acknowledgements 절과 아래 문장 한 개를 추가했다. 기존 원본 PDF와 첫 Week 01의 4페이지 논문·해설 PDF 6개는 수정하지 않았다. 감사 절로 SkillMerge의 조판 쪽수가 원본 12쪽에서 제출본 13쪽으로 바뀌었고, 다른 두 원고는 원본과 같은 14·12쪽이다. 본문·수식·표·그림·참고문헌·부록·출처 검토 범위는 줄이거나 바꾸지 않았다.

> This work was created as part of the No-More-Slops group activities at Pseudo Lab.

## 원고의 근거와 남은 과학적 문턱

SkillMerge는 531개 노출 SciFact 과제에서 548개 annotation 대안, 4,186개 채점 진단 행과 66,431개 제한 크기 집합을 점검한다. 이는 채점·정답 표현 가능성 진단이며 실제 스킬 A/B/A+B 조합 이력은 0개다. 자격을 얻은 조합 분모는 0, 조합 효과는 null로 남긴다.

SecondChance는 저자 작성 이력 12개에서 나온 중첩 궤적 168개와 이미 보존한 292회 로컬 상태 감사·876개 panel 출력을 분석한다. 저장 답의 재채점, 새 후보, 현재 통합 상태의 복구를 분리하고, 강한 neutral 기준의 동률·비용 우위를 보존한다. 자연 LLM 이력과 장기 재발·복구 효과는 아직 평가하지 않았다.

ProbeFlow는 이미 노출된 유압 장치 한 대의 분할과 3개 예측기×8개 입력 mask, 고정 정책 36개 cache replay를 분석한다. 더 적은 채널과의 동률·더 나은 저비용 기준, 학습에 없던 결합 조건, 논리적 quote와 물리적 취득 비용의 차이를 유지한다. 새 적응형 정책·독립 현장 효과·실제 취득 비용의 개선으로 해석하지 않는다.

유사 선행 방법은 원문 검토와 방법·측정 계약을 비교한 것이며, 해당 논문들의 native 구현과 같은 조건의 성능 benchmark를 실행한 것은 아니다. 독립 평가 자료·자격을 얻은 실제 조합 이력·자연 오류 이력·장치/세션 식별·실제 정보 권한과 비용을 갖춘 후속 평가 등 과학적 gate가 열려 있다. SOURCES/CLAIMS/해설서의 `runs/...`, `projects/...` 경로는 원 연구 환경의 보존 근거를 식별하는 기록으로, 이 제출 패키지 안에 원시 실행이나 전체 Research Forge 웹을 동봉했다는 뜻이 아니다.

해설서 원문의 상대 그림 링크도 원래 Research Forge의 폴더 배치를 유지한다. 이번 제출의 [그림 원본](figures/)은 별도 경로에 있으므로 GitHub에서 해설서의 이미지가 바로 보이지 않으면 이 디렉터리에서 같은 이름의 SVG를 열어볼 수 있다. 원문 바이트를 보존하기 위해 해설서 링크를 재작성하지 않았다.

## 조판과 검증 재현

저장소 루트에서 실행한다. Python 3.11, 이미 설치된 Typst 0.15.1와 PyMuPDF 1.26.4 환경에서 새 dependency 설치 없이 확인했다. [독립 조판 도구 안내](../../../../app/v13/README.md)에 입력·출력 경계와 검증 한계를 정리했다.

```sh
python -X utf8 -B tracks/auto-paper/projects/skill-studies/app/v13/test_typeset.py
python -X utf8 -B tracks/auto-paper/projects/skill-studies/app/v13/typeset.py verify --out tracks/auto-paper/projects/skill-studies/outputs/week-01/revisions/v13-20261018/build
python -X utf8 -B tracks/auto-paper/projects/skill-studies/app/v13/check_evidence.py --out tracks/auto-paper/projects/skill-studies/outputs/week-01/revisions/v13-20261018/build
python -X utf8 -B tracks/auto-paper/projects/skill-studies/app/v13/typeset.py build --out tracks/auto-paper/projects/skill-studies/outputs/week-01/revisions/v13-20261018/rebuild-local-01
```

`build`의 `--out`은 새 폴더여야 한다. `verify`는 출력 없는 읽기 전용 검사다. 이 명령의 재현 범위는 **문서 조판·인용 연결·PDF 파일 검증**이며 실제 연구 모델 효과의 재현이 아니다. 모델/API 호출·새 과학 실험은 0회다.

실제 수행한 작은 회귀검사 7개가 통과했다. 새 PDF 전체 39쪽에서 원문 대조 블록 847개(195·342·310), 인용 URL 56개, 감사 문구 각 1회, 수식 폰트와 페이지 밖 문자 0개를 확인했다. 정확한 방정식·그림 입력은 해시로 고정하고 추출 텍스트 검사는 구두점·조판 하이픈을 정규화한다. 이 검사가 수학적 타당성·원 논문의 모든 주장·연구 성능을 인증하지 않는다.

- [PUBLICATION.json](build/PUBLICATION.json): 원본 source/PDF 해시 → 제출 PDF 해시, 조판기·스타일·테스트 해시, 쪽수와 개정 범위.
- [VALIDATION.json](build/VALIDATION.json): 원문 블록·그림 입력·URL·폰트·페이지 경계 검사와 모델 호출 0회.
- [ORIGINAL_BINDINGS.json](ORIGINAL_BINDINGS.json): 동봉 원문/SVG의 원본 식별 해시와 이전 Week 01 바이너리 6개의 보존 해시. 원본 v13 PDF는 해시만 기록하고 파일 자체는 중복 첨부하지 않았다.
- [EVIDENCE_BINDINGS.json](EVIDENCE_BINDINGS.json): 위 publication receipt와 [원본 그림 영수증](evidence/figure-receipt.json), [SkillMerge 요약](evidence/skillmerge-results.json), [SecondChance 요약](evidence/second_chance-results.json), [ProbeFlow 요약](evidence/probeflow-results.json)의 바이트·해시 연결. 이 JSON 4개는 보존 자료의 동일 바이트 사본이다. 원 그림 영수증에 있는 전체 source 5개 중 3개 요약만 동봉했고, 앞선 v11 요약과 ProbeFlow validation은 해시 식별만 남았다. 원시 행·과거 실행 코드·데이터셋·원문 웹 전문은 포함하지 않으므로 그림 생성이나 실험 실행을 완전히 재현한다고 표시하지 않는다.

## 라이선스와 감사 표시

동봉 저자 작성 원고·그림·해설·코드는 저장소의 [MIT License](../../../../../../../../LICENSE)를 따른다. 외부 참고문헌과 데이터셋의 권리를 이 라이선스로 바꾸지 않는다. 원문 논문 PDF, 원시 데이터, 운영 상태, 개인 사진, 형광펜 PDF와 해설 PDF는 이번 패키지 범위 밖이다.

이 결과물은 가짜연구소(Pseudo Lab) No-More-Slops 그룹 활동의 일환으로 제작되었다. 세 제출 PDF에도 위 영문 감사 문구를 동일하게 넣었다.
