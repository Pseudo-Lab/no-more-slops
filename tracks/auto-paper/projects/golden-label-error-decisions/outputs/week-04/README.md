# Week 04 결과물

| 결과물 | 파일 | 설명 |
| --- | --- | --- |
| 논문 PDF | [paper.pdf](paper.pdf) | ACL 공식 스타일, 심사용 익명 원고(줄 번호 포함). 본문 8쪽 이내, 이어서 한계, 참고문헌, 부록 |
| LaTeX 원본 | [paper.tex](paper.tex), [references.bib](references.bib), [tables/](tables/), [fig/](fig/) | 표 본문은 `app/tables.py`, 그림은 `app/figures.py`가 `results/`에서 생성 |
| Markdown 판 | [paper.md](paper.md) | GitHub에서 바로 읽기 위한 본문 사본. 빌드할 때 `app/tex2md.py`가 paper.tex에서 생성 |

심사 1라운드(Major, 필수 12건) 반영 내역은 [reviews/round1/](../../reviews/round1/)에 있습니다.

## 빌드

```bash
app/build_paper.sh            # 프로젝트 폴더에서 실행. 그림과 표를 다시 만든 뒤 PDF 빌드
app/build_paper.sh --no-figures   # TeX만 다시 컴파일
```

- 필요 도구: Tectonic(`brew install tectonic`), uv, curl. Tectonic이 XeLaTeX 엔진과 TeX 패키지를 처음 실행할 때 내려받습니다.
- ACL 스타일 파일(`acl.sty`, `acl_natbib.bst`)은 `acl-org/acl-style-files`의 고정 커밋에서 내려받아 수정 없이 씁니다. 재배포를 허락하는 라이선스 표기가 없어 저장소에 넣지 않습니다.
- 글꼴: 라틴 문자와 수식은 TeX Gyre Termes(Times 계열), 한글은 Noto Serif KR(SIL OFL, 빌드 때 내려받음)입니다.
- 저자 정보를 넣을 때는 `paper.tex`의 `\usepackage[review]{acl}`을 `preprint`로 바꾸고 `\author{...}`를 채웁니다.

## 검증

- 수치는 `app/analyze.py`, `app/compare.py`, `app/rerun_local.py`의 실행 결과(`results/`)에서 가져왔고, 표 본문은 스크립트가 결과 파일에서 직접 생성합니다.
- 5절의 비교에 쓴 선행 연구의 보고값은 `app/reference_numbers.py`에 출처 쪽수와 함께 있으며, 각 값은 arXiv 원문 텍스트에서 문자열 검색으로 확인했습니다.
- 이 브랜치에서 빌드를 다시 실행하고 [paper-readability-pass](../../../../skills/paper-readability-pass/)의 `check_build.py`로 점검했습니다. Overfull 경고 0건, 정의되지 않은 참조와 인용 0건, 본문 끝 6쪽입니다. 남은 경고는 참고문헌과 플로트 쪽의 Underfull(줄 간격 늘림)뿐입니다.
- 문항 결합: 5,690/5,700문항. 리더보드에 정답이 기록된 문항에서 리더보드 정답과 Redux 원래 정답이 모두 일치합니다.
- 모델 42종 포함(OLMo 2종은 실제 저장소 이름으로 대체), 후보 6종 제외. 원인과 40종 대비 비교는 [docs/excluded-models.md](../../docs/excluded-models.md)에 있습니다.

## 데이터 출처와 라이선스

- MMLU-Redux 2.0: `edinburgh-dawg/mmlu-redux-2.0` (CC BY 4.0). 저장소에는 복사하지 않고 스크립트로 내려받습니다.
- Open LLM Leaderboard v1 details: `open-llm-leaderboard-old/details_*`. 저장소에는 복사하지 않습니다.
