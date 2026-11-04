# CAD-JEV: Decision Model로 도면 그래프 추출하기

Auto-Paper 트랙의 [@gogoymh](https://github.com/gogoymh) 3주차 기여입니다. 도면 이미지에서 객체, 연결, 글자 영역의 포함 관계를 추출하고, 판단에 사용한 원본 경로와 모델 응답을 보관합니다. Jev는 사용한 모델의 이름이며, 방법을 설명할 때는 ‘Decision Model’이라는 용어를 사용합니다.

논문 저자는 Minhyeong Yu (minhyeong@enhans.ai, Enhans)와 Seunghyun Lee (seunghyun@enhans.ai, Enhans)입니다. 논문 제목은 *Preserving Visual Evidence While Repairing Industrial Diagram Graphs*입니다.

[3주차 결과물](outputs/week-03/README.md)에서 논문 PDF, 공개 벤치마크 결과, API 소스, 연결 누락 분석을 확인할 수 있습니다. 논문은 v11/v12의 공개 평가를 다루는 투고 전 초안입니다. API 기본 구현인 v15의 후속 검사는 별도로 기록했습니다.

## 실행과 검토

- [추출 API 실행과 모델 연결 설정](app/README.md): 이미지 업로드, 작업 조회, JSON 그래프와 판단 기록 반환.
- [실패 사례의 특징과 다음 검증](docs/failure-analysis.md): 부분 검수에서 남은 연결 누락을 원인별로 분석.
- [논문 원문](outputs/week-03/paper-source/main.tex): 그림의 (a)–(f)와 Method의 동명 소절을 연결.
- [데이터 출처와 라이선스](outputs/week-03/DATA_ATTRIBUTION.md): PID2Graph/OPEN100 및 공개 범례 이미지의 출처.

새로운 스킬을 추가하거나 기존 스킬을 수정하지 않았습니다. 이 프로젝트의 API, 실험 기록과 분석 자료를 한 프로젝트의 주차 결과물로 제출합니다. 다른 미병합 PR의 파일을 설치하거나 병합할 필요가 없습니다.

## 공개 범위

이 제출물에는 공개 벤치마크 그림과 사용자 제작 코드, 원고, 합계 검증 기록을 포함합니다. 후속 부분 검수에 사용한 비공개 도면, 개별 객체 식별자, 원본 실행 캐시와 인증 정보는 포함하지 않습니다. 코드와 문서는 저장소의 MIT License를 따르며, 공개 데이터 이미지와 ACM 템플릿의 별도 라이선스는 출처 문서에 명시합니다.

이 결과물은 가짜연구소(Pseudo Lab) No-More-Slops 그룹 활동의 일환으로 제작되었습니다.
