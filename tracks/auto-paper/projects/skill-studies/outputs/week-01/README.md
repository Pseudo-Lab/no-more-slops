# Auto-Paper: 1주차 스킬 연구 논문과 해설서

**2026-10-18 수정:** [v13 논문 PDF 3편과 재현 안내](revisions/v13-20261018/README.md)를 추가했습니다. 아래는 기존 v5 배포·검증 기록으로 보존합니다. 최신 제출본의 결과 범위와 파일 해시는 새 revision의 안내를 따릅니다. 새 연구 자동화 지침은 [canonical SKILL.md](../../../../skills/evidence-tracked-research/SKILL.md)에서 읽습니다.

- 작성자: @darkwingduck-code
- 트랙: Auto-Paper
- 원본 PR: [#14](https://github.com/Pseudo-Lab/no-more-slops/pull/14)
- 사용한 연구 자동화 스킬: [별도 기여 PR #11](https://github.com/Pseudo-Lab/no-more-slops/pull/11)

2026-10-12에 작성·검증한 연구 설계 원고 3편과 한국어 해설서 3권이다. 논문은 각각 정확히 4페이지이며, 실제 모델 성능은 아직 NR(미실측)이다. 논문의 상태는 **첫 주 연구 설계**이고 사전등록·산업 성능 평가·arXiv 제출은 완료하지 않았다.

| 프로젝트 | 연구 설계 논문 | 별도 한국어 해설서 | 중심 질문 |
| --- | --- | --- | --- |
| SkillMerge | [4페이지 PDF](papers/SkillMerge_Week1_4p.pdf) | [16페이지 PDF](explainers/skillmerge_EXPLAINER_KO.pdf) | 각각 개선 자격을 얻은 스킬 업데이트를 합쳤을 때 성공이 보존되는가 |
| Second-Chance | [4페이지 PDF](papers/SecondChance_Week1_4p.pdf) | [13페이지 PDF](explainers/second_chance_EXPLAINER_KO.pdf) | 잘못된 평가가 만든 선택과 부정적 교훈을 고쳐 현재 능력을 복구할 수 있는가 |
| ProbeFlow | [4페이지 PDF](papers/ProbeFlow_Week1_4p.pdf) | [17페이지 PDF](explainers/probeflow_EXPLAINER_KO.pdf) | 공유 분석 비용·캐시와 실제 공개 증거가 제한된 분석 선택을 어떻게 바꾸는가 |

해설서는 개념과 기호, 계산 예제, 구현 파이프라인, 데이터 분할, 대조군, 비용·분모·선택 편향, 반증 기준과 예상 Q&A를 다룬다. 선행연구와 중복되는 기여 주장을 정리하고, 설명용 모형·직접 데이터 준비·기존 소프트웨어 검증·실측이 필요한 가설을 구분했다.

## 편집 원문과 검토 근거

- [SkillMerge](skillmerge/): paper.json, EXPLAINER_KO.md, METHODS_CONTRACT.json, SOURCES.json.
- [Second-Chance](second_chance/): 같은 네 종류의 원문·설계 계약·출처 연결.
- [ProbeFlow](probeflow/): 같은 네 종류의 원문·설계 계약·출처 연결.
- [독립 검토 기록](REVIEW_NOTES.md), [PDF 검증](validation/paper_verification.json), [해설서 검증](explainers/verification.json).
- [계산 예제 검사](validation/formal_examples.json), [조판 입력 검사](validation/typesetting_checks.json), [배포 파일 해시](ARTIFACTS.json).

PDF 6개는 검증된 v5 배포본과 동일한 바이트다. 논문 12쪽과 해설서 46쪽이며, 원문 본문·인용·수식 폰트·페이지 경계와 source/PDF 해시를 검사했다. 설명용 계산 15개와 조판 경계 7개 검사를 통과했다. 이 수치는 모델 성능이 아니다.

해설서·SOURCES.json에 나오는 이전 v3/v4 경로는 원 연구 환경의 기록을 식별하는 참조다. 그 로컬 실험 프로젝트와 원시 데이터는 이 PR에 포함하지 않았다. 이전 소프트웨어 검증이나 데이터 준비를 재실행한 것으로 표시하지 않으며, 이 폴더에서 재현하는 범위는 동봉한 계산 예제와 문서 조판이다. 기존 연구 자동화 SKILL.md 기여와 별도 자료다.

## 문서 재조판

검증 환경은 Python 3.11, Typst 0.15.1과 설치된 PyMuPDF/Pillow다. 영문 논문은 New Computer Modern, 한국어 해설서는 Malgun Gothic을 사용했다. 한국어 폰트가 없는 환경에서는 동일 폰트를 제공해야 같은 조판을 비교할 수 있다. 이 PR 작성 중 새 dependency를 설치하지 않았다.

이 디렉터리에서 실행한다. 아래 명령은 문서와 저자 계산만 처리하고 실제 연구 모델을 호출하지 않는다.

```powershell
python -X utf8 -B tools/formal_checks.py
python -X utf8 -B tools/test_typesetting.py
python -X utf8 -B tools/build_papers.py
python -X utf8 -B tools/verify_papers.py
python -X utf8 -B tools/build_explainers.py
python -X utf8 -B tools/check_explainers.py
```

재조판 후에는 PDF와 검증 파일이 갱신되므로 ARTIFACTS.json의 과거 배포 바이트 해시와 새 출력은 구분한다. 출력 source/PDF 해시와 문장 보존은 새 검증 영수증으로 확인한다. 도구가 자동으로 원고 문장을 잘라 4페이지에 맞추지 않는다.

실제 모델 비교는 모델 ID·입력 전송 범위·요청/토큰/비용 한도, 독립 데이터 그룹, 평가기 교정 검토, benchmark 환경과 활성화 기록을 먼저 고정해야 한다. 공개 데이터의 사전학습 노출, 미확정 독립 운전 블록, 미구현 외부 benchmark adapter는 남아 있다. 실제 조합 실패율·회복 효과·산업 정책 이득은 NR이다.

## Acknowledgement와 라이선스

이 결과물은 가짜연구소(Pseudo Lab) No-More-Slops 그룹 활동의 일환으로 제작되었습니다.

동봉한 저자 작성 문서·코드는 저장소의 [MIT License](../../../../../../LICENSE)를 따른다. 인용한 외부 논문, 원시 데이터와 개별 스킬 자산의 조건을 이 라이선스로 대체하지 않는다. 데이터셋 원문, 미확인 bundled skill, 원 연구 환경의 credentials·운영 상태는 포함하지 않았다.
