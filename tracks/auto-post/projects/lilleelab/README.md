# lilleelab

auto-post 트랙의 [@xiyoon](https://github.com/xiyoon) 기여입니다. 원 PR: [#23](https://github.com/Pseudo-Lab/no-more-slops/pull/23).

사람 없이 제품만 나오는 화장품 3D 광고를 인스타그램 [@lilleelab.kr](https://www.instagram.com/lilleelab.kr/)에 올리는 프로젝트입니다.
실제 제품을 쓰고 올리브영 쇼핑 큐레이터 제휴 링크를 답니다. 제품, 스토리라인, 콘티, 게시 여부는 사람이 정하고, 에이전트가 기획·콘티·렌더·캡션 초안을 만듭니다. 게시는 사람이 합니다.

- 목표: 주 3개 제품 × (릴스 1개 30초 이내 + 사진 10장)
- 영상과 사진 원본은 저장소에 올리지 않습니다. 결과물은 인스타그램 링크로 남깁니다
- 브랜드 로고·라벨 이미지, 제품 참고 사진, 효과음 원본은 공개하지 않습니다

## 재사용 스킬

| 스킬 | 적용 범위 |
| --- | --- |
| [ad-planning](../../skills/ad-planning/SKILL.md) | 사람 없는 숏폼 제품 광고의 기획과 콘티. 제품 분석 → 특징 추출 → 트렌드·레퍼런스 → 아이디어 발산 → 스토리라인 → 컷별 그림 콘티 → 검토 |
| [product-cgi-render](../../skills/product-cgi-render/SKILL.md) | 확정 콘티에서 회전체 용기(유리병·스포이트·뚜껑) CGI 컷을 Blender로 렌더하고, 마감·글자 오버레이·효과음·조립·수치 QC까지. 제품은 설정 JSON으로 바꾼다 |

## 파이프라인

[docs/pipeline.md](docs/pipeline.md): 역할 8개(기획, 콘티 작가, 에이전시 PM, 제작, QC, 사진, 카피, 점검)와 사람 승인 게이트 3개(G1 스토리라인, G2 콘티, G3 게시). 역할별 지시문은 [agents/](agents/)에 있습니다.

## 주차별 결과물

- [Week 02](outputs/week-02/README.md): 토리든 다이브인 세럼 릴스(19.0초, 12컷) + 제작 노트 캐러셀 + 캡션

## 실행 방법

필요한 도구: Blender 5.x (Cycles), Python 3, ffmpeg, Chrome(글자 오버레이, 선택), Node.js(`puppeteer-core`, 선택).

```sh
# 스킬 시험 (Blender 없이)
sh skills/product-cgi-render/tests/run_tests.sh
# Blender까지 포함
BLENDER_SMOKE=1 sh skills/product-cgi-render/tests/run_tests.sh
```

렌더·조립·QC 명령은 [product-cgi-render/SKILL.md](../../skills/product-cgi-render/SKILL.md)를 따릅니다. 실제 제품 라벨 PNG는 사람이 공식 정면 사진을 보고 직접 조판해 준비합니다(스킬에는 시험용 라벨만 들어 있습니다).
