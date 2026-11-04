# v13 제출본 문서 조판 도구

Python 표준 라이브러리, 이미 설치된 Typst와 PyMuPDF로 원고 3편을 조판하고 검증한다. 저장소 루트에서 실행하며, 외부 모델·네트워크·Research Forge 설치·개인 드라이브·과거 v5 helper를 사용하지 않는다. 기존 v13 조판기의 literal/content/math 처리를 내장하고 같은 conference.typ을 보존했다. 동봉 코드·스타일은 저장소 MIT License를 따른다.

기본 입력은 [같은 Week 01의 v13 수정본](../../outputs/week-01/revisions/v13-20261018/)이다. 원본 JSON/SVG의 바이트 해시와 원본 PDF 식별 해시를 ORIGINAL_BINDINGS.json으로 고정했다. 원본 Typst는 개행 정규화 후 비교하며, 생성된 소스에서 감사 절을 제거하면 원본 v13의 내용과 정확히 같아야 한다. 원고 JSON은 수정하지 않는다.

```sh
python -X utf8 -B tracks/auto-paper/projects/skill-studies/app/v13/test_typeset.py
python -X utf8 -B tracks/auto-paper/projects/skill-studies/app/v13/typeset.py verify --out tracks/auto-paper/projects/skill-studies/outputs/week-01/revisions/v13-20261018/build
python -X utf8 -B tracks/auto-paper/projects/skill-studies/app/v13/check_evidence.py --out tracks/auto-paper/projects/skill-studies/outputs/week-01/revisions/v13-20261018/build
python -X utf8 -B tracks/auto-paper/projects/skill-studies/app/v13/typeset.py build --out tracks/auto-paper/projects/skill-studies/outputs/week-01/revisions/v13-20261018/rebuild-local-01
```

`build --out`은 필수이며 **저장소 안의 새 디렉터리**만 받는다. 이미 존재하는 디렉터리는 덮어쓰지 않는다. 다른 입력 패키지를 쓰려면 `--inputs <패키지 디렉터리>`를 지정한다. `verify`는 기존 build의 receipt·원문·SVG·Typst·PDF·과거 바이너리를 읽기만 하며 조판이나 출력 쓰기를 수행하지 않는다. 폰트는 Typst에 포함된 New Computer Modern을 쓰고 시스템 폰트는 검색하지 않는다. 정확한 PDF 바이트는 동봉 PUBLICATION.json의 환경·해시를 기준으로 하며 다른 Typst 버전의 출력은 새 build로 구분한다.

`check_evidence.py`도 읽기 전용이다. 동봉한 기존 v12 결과 요약 3개와 원 v13 그림 영수증을 EVIDENCE_BINDINGS.json을 통해 기존 build의 PUBLICATION.json에 결박하고 SVG 9개의 해시를 대조한다. 원 영수증의 source 5개 중 2개는 미동봉 상태로 명시한다. 이 추가 검사는 기존 build를 바꾸지 않고, 원시 행 재생이나 실험·그림 생성 재현을 수행하지 않는다. 새 build는 자체 PUBLICATION/VALIDATION으로 검증하며, 동봉 EVIDENCE_BINDINGS는 제출 build에만 연결된다.

작은 회귀검사는 감사 절만 추가됐는지, 문자 이스케이프·수식 경계·인용 번호·표/그림 경로·기존 출력 거절을 확인한다. PDF 검사는 본문·표·알고리즘·그림 설명·참고문헌·출처 검토 범위를 대조하고 URL 링크·빈 페이지·페이지 밖 문자·수식 폰트를 확인한다. PDF 추출 대조는 구두점과 조판 하이픈을 정규화하므로 수식의 의미 검증을 대신하지 않는다. 수식·단위의 정확한 원문은 JSON/SVG/생성 Typst 해시로 함께 고정한다. 실험·모델 효과·선행 방법의 재현, 외부 심사, 학회 규격 준수나 채택을 검증하는 도구가 아니다.
