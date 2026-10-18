# PR #18 시각 설명과 실제 제작 예시

작성자 @gogoymh · Auto-Post · 시각 설명 작성일 2026-10-18

| 그림 | 읽을 내용 | 종류 |
| --- | --- | --- |
| [릴스 전후 비교](editorial-before-after.jpg) | 작은 설명 패널을 없애고 큰 설명·하단 공간을 적용한 변화 | 10월 17일 실제 MP4의 23초 프레임을 나란히 배치 |
| [제작물 미리보기](production-examples.jpg) | CLaC 카드뉴스와 벤츠·NVIDIA 릴스의 내용·규격 | 실제 PNG·MP4 프레임 발췌 |
| [제작 흐름](production-flow.png) | 원문 확인 → 카피 검토 → 계정 입력 → 출력 → 검수 | 스킬과 제작 도구를 설명하는 도식 |

## 제작한 콘텐츠

- **CLaC 소재 탐색 AI 카드뉴스:** 2026-10-18 제작, 총 10장·1080×1350. 결정 구조와 언어를 연결하는 방식, 배터리 소재 후보 검색과 평가 범위를 설명했습니다. 이 PR에는 자체 문구로 구성한 [02장](carousel-02.png)·[08장](carousel-08.png)을 발췌하고 [당시 출력 측정 기록](carousel-production-report.json)을 보존했습니다.
- **벤츠·NVIDIA 협력 확대 릴스:** 2026-10-17 개정, 60초·2160×3840·30fps·무음·8개 장면. 회사별 담당 기술, MB.OS·Hyperion·Alpamayo Stack·Halos의 역할과 개발 범위를 고정 사진 위의 큰 설명으로 전달했습니다. [실제 영상과 보존 파일](../editorial-reel/README.md)을 함께 추가했습니다.
- **Neuron AI 도식 데모:** 기존 [60초 하네스 재현 영상](../neuron-reel-demo/reel.mp4)은 원래 입력·출력·검증 기록으로 보존했습니다.

카드뉴스와 릴스는 `direct-news-copy`를 추가하기 전에 만든 결과입니다. 카피 수정의 효과는 [문구 전후 예시](../copy-review.md)로 따로 설명합니다. 그림에 완성본, 과거 개정본, 제작 흐름을 각각 표시했습니다.

## 어떻게 만들었나

공식 기사와 논문의 주장·날짜를 확인한 뒤 계정 설정과 콘텐츠 입력을 분리했습니다. 카드뉴스는 Python/Pillow 기반의 캐러셀 하네스로 출력하고, 고정 사진 위에 설명을 크게 배치한 릴스는 React/Remotion으로 렌더링했습니다. 도식용 Python 릴스 하네스는 별도의 선택 경로입니다.

이번에 추가한 `direct-news-copy`는 출력 전에 반복 해명을 줄이고 사실·계획·검증 범위를 직접 쓰는 단계입니다. `design-punctuation`은 큰 제목의 끝마침표를 검토하고, `instagram-content`는 제작과 검수를 연결합니다. 기술 검사는 해상도·길이·프레임·무음·전체 디코딩·캡션 길이 등을 확인하고, 전체 영상의 가독성과 움직임은 휴대폰 크기로 직접 확인합니다.

## 이미지 출처와 검증 범위

- 카드 발췌의 문구와 레이아웃은 자체 제작입니다. 원문은 [MIT News](https://news.mit.edu/2026/giving-ai-crystal-clear-view-of-materials-world-1018)와 [CLaC 논문](https://www.nature.com/articles/s41467-026-76378-7)입니다. 원본 연구 일러스트와 논문 도표는 이 발췌에 포함하지 않았습니다.
- 릴스 사진: **OWS Photography · [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)** · [원본 자료사진](https://commons.wikimedia.org/w/index.php?curid=163895996). 기존 영상은 고정 크롭·리사이즈·명암 오버레이·설명 합성을 적용했습니다. PR 그림에서는 기존 영상 프레임의 크기만 조정해 배치했습니다.
- 제작 흐름 도식과 이미지 합성은 이번에 직접 제작했습니다. 새로운 영상 렌더링, 카피 수정 영상, 새 Instagram 업로드 검증은 이번 설명 보완의 범위에 포함하지 않았습니다.
- 이번 확인: 세 그림의 글자와 배치, 링크, 발췌 PNG, 복사한 영상의 원본 해시 일치, 저장소 구조를 확인했습니다. 과거 제작 테스트는 [기존 검증 기록](../skill-validation.md)으로 구분합니다.
