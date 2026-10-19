# v21 문서 재현 도구

[2주차 결과물](../../outputs/week-02/README.md)의 Typst·SVG·PDF를 검증하거나 새 디렉터리에 다시 조판합니다. 기존 v20 도구의 경로·판본만 갱신했으며 과학 실험 실행기는 아닙니다.

저장소 루트에서 실행합니다.

```sh
python -B tracks/auto-paper/projects/skill-studies/app/v21/test_build_documents.py
python -B tracks/auto-paper/projects/skill-studies/app/v21/build_documents.py verify
python -B tracks/auto-paper/projects/skill-studies/app/v21/build_documents.py rebuild --out /absolute/new/v21-rebuild
```

Python 3.11+, 설치된 PyMuPDF와 Typst 0.15.1을 사용합니다. Arial·Malgun Gothic·DejaVu Sans 등 설치된 폰트에 따라 결과가 달라질 수 있으며 폰트를 배포하거나 의존성을 자동 설치하지 않습니다. Windows에서는 `--out C:/Temp/skill-studies-v21-rebuild`처럼 아직 없는 절대 경로를 사용합니다.

검증은 파일 목록·SHA-256·PDF 쪽수·필수 감사 문구를 검사합니다. 출력 경로·변조·심볼릭 링크·PDF 검사 경계의 회귀 테스트는 모의 PDF 판독이며, 실제 재조판 검증과 구별합니다. 원자료·모델·예측 캐시가 없으므로 연구 결과의 재실행이나 독립 재현을 수행하지 않습니다.
