# Auto-Paper: 논문 작성·검토 스킬

완료된 실험 결과를 논문으로 정리하면서 만든 두 스킬과 [논문 PDF](../outputs/week-01/paper.pdf)를 공유합니다. PDF는 본문 4쪽과 참고문헌 1쪽으로 구성된 연구 초안입니다.

| 스킬 | 사용하는 때 |
| --- | --- |
| [experiment-to-paper](../../../skills/experiment-to-paper/SKILL.md) | 저장된 실험 결과에서 수치와 근거를 정리하고 원고를 작성할 때 |
| [paper-review-local](../../../skills/paper-review-local/SKILL.md) | 원고·인용 키·그림·PDF를 확인하고 수정 전후의 검토 기록을 남길 때 |

## 설치

각 `tracks/auto-paper/skills/<스킬 이름>/` 폴더 전체를 사용하는 에이전트의 스킬 디렉터리에 복사합니다. Hermes에서는 공개된 제출 브랜치의 URL로 설치할 수도 있습니다.

```sh
hermes skills install https://raw.githubusercontent.com/11kkw/no-more-slops/feat/auto-paper-evidence-review/tracks/auto-paper/skills/experiment-to-paper/SKILL.md
hermes skills install https://raw.githubusercontent.com/11kkw/no-more-slops/feat/auto-paper-evidence-review/tracks/auto-paper/skills/paper-review-local/SKILL.md
hermes skills list
```

실행 도구에는 Python 3.10 이상이 필요합니다. 원고 검토용 의존성은 설치한 `paper-review-local` 폴더의 `scripts/requirements.txt`로 설치하고, LaTeX 검사에는 ChkTeX를 별도로 설치합니다. [검토 도구 실행 안내](../../../skills/paper-review-local/references/local-tools.md)에 CLI와 선택적 MCP 사용법이 있습니다. API 키는 필요하지 않습니다.

## 사용 요청 예시

> experiment-to-paper 스킬로 내 실험 결과를 읽고, 지표·단위·분모와 원본 파일을 근거표로 연결해줘. 확인된 결과를 바탕으로 원고를 작성하고 미확인 주장은 표시해줘.

> paper-review-local 스킬로 내 원고와 PDF를 검토해줘. 인용 키, 그림, PDF와 LaTeX 검사 결과를 확인하고, 수정한 원고에는 새 검토 기록을 남겨줘.

논문 형식과 쪽수는 각 프로젝트에 맞춰 지정합니다.

## 실행 예제

저장소 루트에서 가상 결과로 근거 추출을 실행합니다. 추가 Python 패키지는 필요 없습니다.

```sh
python3 tracks/auto-paper/skills/experiment-to-paper/scripts/export_evidence.py \
  --root tracks/auto-paper/skills/experiment-to-paper/assets/example --spec export-spec.json \
  --out /tmp/paper-evidence-demo-new
```

수치 3개와 입력 파일 해시·표가 생성됩니다. 다시 실행할 때는 새 출력 경로를 사용합니다. 실제 프로젝트에서는 [설정 규약](../../../skills/experiment-to-paper/references/evidence-schema.md)에 따라 입력 파일과 JSON pointer를 바꿉니다.

원고 검토는 자신의 프로젝트 경로와 원고 폴더를 지정합니다.

```sh
python3 -m pip install -r tracks/auto-paper/skills/paper-review-local/scripts/requirements.txt
python3 tracks/auto-paper/skills/paper-review-local/scripts/review_mcp.py \
  --root /path/to/project --package paper --review-id initial-01
```

검토 보고서는 원고 폴더의 `reviews/initial-01/`에 저장됩니다. 원고가 바뀌면 새 review ID를 사용합니다. 자동 검사는 원고 내용과 실제 PDF 화면의 검토를 보조합니다.

## 스킬 개발 시 확인

```sh
python3 -m pip install -r tracks/auto-paper/skills/paper-review-local/scripts/requirements-mcp.txt
python3 -B -m unittest discover -s tracks/auto-paper/projects/dcsm-spatial/tests -v
```

스킬 테스트는 포함된 가상 데이터와 임시 원고를 사용하므로 연구 실험 데이터가 필요하지 않습니다.

이 결과물은 가짜연구소(Pseudo Lab) No-More-Slops 그룹 활동의 일환으로 제작되었습니다.
