<p align="center">
  <img src="no-more-slops.png" alt="No-More-Slops — 아이디어를 논문, 애플리케이션, 콘텐츠로 만드는 프로젝트" width="100%">
</p>

# No-More-Slops

[English](README.md) | **한국어**

**가짜연구소 13기 No-More-Slops 그룹의 프로젝트는 토큰의 가치를 높이는데 집중합니다.**

같은 토큰 비용을 들였어도, 아무도 쓰지 않는 결과물과 누군가의 문제를 해결하는 결과물은 가치가 다릅니다.

AI가 만든 결과물도 사람들이 쓰고 공유하면서 문화가 됩니다.
누군가의 연구와 개발을 돕고, 다음 창작의 재료가 됩니다.

No-More-Slops는 사람들이 실제로 쓰는 결과물을 만들고 공개합니다.
결과물과 제작 시스템을 개선해 토큰의 투자 가치를 높입니다.

## 활동 안내

- **기간:** 12주(1주차 온보딩, 2–11주차 제작, 12주차 회고)
- **인원:** 빌더 1명과 참여자 11명. 트랙별 4명을 목표로 하되 지원 현황에 따라 조정
- **정기 모임:** 매주 월요일 21:00–23:00
- **오프라인:** 월 1회 월요일 20:00–22:00에 해당 주 정기 모임 진행. 일시·장소는 조정 가능

모임 시간은 모두 한국시간 기준입니다.

## 주간 목표

Auto-Paper, Auto-Application, Auto-Post 3개의 트랙이 있습니다.
한 트랙을 선택해 **2–11주차**에 아래 활동을 수행합니다.

| 트랙 | 매주 결과물 | 매주 GitHub PR | 매주 PR 리뷰 | 총 결과물 (제작 10주) |
| --- | --- | --- | --- | --- |
| **Auto-Paper** | 논문 1편 이상 작성 | PR 1개 제출·머지 | 동료 PR 리뷰 | 10편 이상 |
| **Auto-Application** | 서비스 1개 이상 출시 | PR 1개 제출·머지 | 동료 PR 리뷰 | 10개 이상 |
| **Auto-Post** | 콘텐츠 3개 이상 포스팅 | PR 1개 제출·머지 | 동료 PR 리뷰 | 30개 이상 |

트랙별 4명 기준 **총 200건 이상**(논문 40편·서비스 40개·콘텐츠 120개)을 만듭니다.

자동화 없이는 지속하기 어려운 속도를 기준으로 삼아, 매주 자동화의 품질을 높이도록 설계했습니다. 개선 효과는 직접 정한 실사용 지표로 확인합니다.

결과물·제작 코드·재현 방법·지표·동료 리뷰를 PR에 남기고, **생성한 주 안에 리뷰·수정·머지를 완료**합니다.

## 제작 스킬

`skills/`의 스킬은 전역으로 설치해 어느 프로젝트에서든 사용할 수 있습니다. 이 저장소를 작업 폴더로 열 필요가 없습니다.

| 스킬 | 용도 |
| --- | --- |
| [instagram-content](skills/instagram-content/SKILL.md) | 인스타 브랜드 설정, 사진을 곁들인 캐러셀, 참고 사진을 활용한 프로필·캐릭터를 제작합니다. 계정·주제·언어·색상·사진은 작업별로 지정하며, 반복 출력용 도구도 포함합니다. |
| [design-punctuation](skills/design-punctuation/SKILL.md) | 콘텐츠와 웹디자인의 제목·짧은 캡션·큰 글씨에서 불필요한 끝마침표를 생략합니다. 의미와 데이터에 필요한 문장부호는 유지합니다. |

처음 설치할 때는 이 저장소에서 다음과 같이 실행합니다.

```sh
mkdir -p "$HOME/.agents/skills"
cp -R skills/instagram-content "$HOME/.agents/skills/"
cp -R skills/design-punctuation "$HOME/.agents/skills/"
```

필요한 파일을 Codex의 사용자 전역 스킬 폴더에 복사하므로 다른 프로젝트에서도 사용할 수 있고, 원래 저장소를 옮겨도 작동합니다. 업데이트할 때는 설치본에 별도 수정한 내용이 있는지 확인하고 보관한 뒤 교체합니다. Codex는 변경된 스킬을 자동으로 감지하며, 목록에 보이지 않을 때만 재시작합니다. 설치 위치는 [OpenAI 공식 문서](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills)를 따릅니다.

호출 예시: `$instagram-content로 독립서점의 기존 브랜드 설정에 맞춰 사진이 들어간 인스타 캐러셀을 만들어줘.`

색상·캐릭터·언어·Acknowledgement는 작업별 입력값입니다. 기존 [치와와 AI 예시](examples/instagram/chihuahua-ai/README.md)는 별도로 보관하며, 선택했을 때만 사용하고 전역 설치에는 포함하지 않습니다. 각 계정의 설정과 제작한 파일은 해당 작업 폴더에 저장합니다. 입력 형식과 검증 방법은 [렌더러 안내](skills/instagram-content/references/renderer.md)에 있습니다. 파일 제작만으로 인스타에 자동 게시되지는 않습니다.

반복 제작에는 [로컬 실행 하네스](skills/instagram-content/references/harness.md)를 사용합니다. 선택한 계정 설정으로 완성 캡션과 장수를 검사하고, 장별 PNG·미리보기·업로드 ZIP을 만든 뒤 파일 구성을 검증합니다. 다음 작업에 쓸 설정과 제작 보고서도 저장합니다. 렌더링 없이 입력값만 검사하려면 `--validate-only`를 사용합니다.

```sh
python -m pip install -r "$HOME/.agents/skills/instagram-content/scripts/requirements.txt"
python -B "$HOME/.agents/skills/instagram-content/scripts/run_carousel.py" /path/to/post.json \
  --brief /path/to/brand-brief.json --out /path/to/output/carousel \
  --font-regular /path/to/Regular.ttf --font-bold /path/to/Bold.ttf
```

캡션 길이·해시태그 수·장수·문장부호 선호는 계정별로 지정합니다. 출처 확인과 실제 이미지 검토는 스킬의 제작 과정에 포함됩니다. [동작 테스트](skills/instagram-content/tests/)는 Python 3.10·3.12 CI에서 실행하며, 복사한 스킬을 다른 폴더에서 실행하는 경우도 검사합니다. [재현 예시](examples/instagram/layout-demo/README.md)에서 실행 방법을 확인할 수 있습니다.

## 참여 조건

1. **12주 동안 성실하게 참여할 수 있는 사람** (최우선)
2. Codex·Claude 등 프로젝트에 필요한 AI 도구를 갖춘 사람
3. 이 속도감에 공감되는 사람
4. 실패해도 계속 변화를 시도하는 사람
5. 스스로 동기부여하고 움직이는 사람

## 참여 혜택

- **실전 자동화 경험:** 아이디어를 실제 결과물로 만드는 자동화 시스템에 기여하는 경험을 얻게 됩니다.
- **개인 포트폴리오:** 프로젝트 기간 중 제작한 논문·서비스·콘텐츠를 소유합니다.
- **동료 피드백:** 서로의 결과물을 검토하며 개선점을 찾고 제작 노하우를 나눕니다.

## 소유권과 Acknowledgement

결과물은 본인의 성과로 보유·활용할 수 있습니다. 논문의 저자, 앱·서비스의 소유주, 포스팅 계정의 소유주가 될 수 있습니다.

단, 개인 명의로 공개·운영하더라도 다음과 같은 **Acknowledgement를 표시**합니다. 감사의 글, 소개·크레딧, 포스팅 본문 등에 넣으면 됩니다.

> 이 결과물은 가짜연구소(Pseudo Lab) No-More-Slops 그룹 활동의 일환으로 제작되었습니다.

제작 시스템을 기여하는 **GitHub 저장소는 가짜연구소 소속**입니다. 기여한 코드·skill·프롬프트·문서는 [MIT License](LICENSE)로 공개되며, 개인 명의로 결과물을 활용해도 이 라이선스는 유지됩니다.
