# lilleelab

auto-post 트랙의 [@xiyoon](https://github.com/xiyoon) 기여입니다. 원 PR: [#23](https://github.com/Pseudo-Lab/no-more-slops/pull/23).

사람 없이 제품만 나오는 화장품 3D 광고를 만들어 인스타그램 [@lilleelab.kr](https://www.instagram.com/lilleelab.kr/)에 올리는 프로젝트입니다. 역할별 AI 에이전트가 기획·콘티·렌더·캡션을 만들고, 제품 선정과 콘티 확정, 게시는 사람이 합니다.

## 재사용 스킬

| 스킬 | 적용 범위 |
| --- | --- |
| [ad-planning](../../skills/ad-planning/SKILL.md) | 제품 분석부터 스토리라인, 컷별 콘티, 검토까지 광고 기획 단계와 기준 |
| [product-cgi-render](../../skills/product-cgi-render/SKILL.md) | 확정 콘티로 용기 제품을 Blender로 렌더하고, 글자·효과음을 얹어 조립한 뒤 화면 품질을 수치로 검사 |

## 주차별 결과물

- [Week 02](outputs/week-02/README.md): 토리든 다이브인 세럼 릴스

## 실행 방법

- 에이전트 구성과 승인 게이트: [docs/pipeline.md](docs/pipeline.md), 역할별 지시문: [agents/](agents/)
- 렌더 스킬 테스트(Blender 없이): `sh skills/product-cgi-render/tests/run_tests.sh`
- 영상·사진 원본과 브랜드 라벨 이미지는 저장소에 올리지 않습니다.
