# Instagram 제작 도구

[English](README.md)

작성자: [유민형 · gogoymh](https://github.com/gogoymh). 원본 기여: [PR #5](https://github.com/Pseudo-Lab/no-more-slops/pull/5).

아래 저장소 명령은 저장소 루트에서 실행합니다. 공통 스킬은 `tracks/auto-post/skills/`에 한 번만 보관합니다. 계정 입력은 `examples/`, 공유 결과물은 [outputs/week-01/](outputs/week-01/README.md)에 둡니다.

## 제작 스킬

`tracks/auto-post/skills/`의 스킬은 전역으로 설치해 어느 프로젝트에서든 사용할 수 있습니다. 이 저장소를 작업 폴더로 열 필요가 없습니다.

| 스킬 | 용도 |
| --- | --- |
| [instagram-content](../../skills/instagram-content/SKILL.md) | 인스타 브랜드 설정, 사진을 곁들인 캐러셀, 참고 사진을 활용한 프로필·캐릭터를 제작합니다. 계정·주제·언어·색상·사진은 작업별로 지정하며, 반복 출력용 도구도 포함합니다. |
| [design-punctuation](../../skills/design-punctuation/SKILL.md) | 콘텐츠와 웹디자인의 제목·짧은 캡션·큰 글씨에서 불필요한 끝마침표를 생략합니다. 의미와 데이터에 필요한 문장부호는 유지합니다. |

처음 설치할 때는 이 저장소에서 다음과 같이 실행합니다.

```sh
mkdir -p "$HOME/.agents/skills"
cp -R tracks/auto-post/skills/instagram-content "$HOME/.agents/skills/"
cp -R tracks/auto-post/skills/design-punctuation "$HOME/.agents/skills/"
```

필요한 파일을 Codex의 사용자 전역 스킬 폴더에 복사하므로 다른 프로젝트에서도 사용할 수 있고, 원래 저장소를 옮겨도 작동합니다. 업데이트할 때는 설치본에 별도 수정한 내용이 있는지 확인하고 보관한 뒤 교체합니다. Codex는 변경된 스킬을 자동으로 감지하며, 목록에 보이지 않을 때만 재시작합니다. 설치 위치는 [OpenAI 공식 문서](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills)를 따릅니다.

호출 예시: `$instagram-content로 독립서점의 기존 브랜드 설정에 맞춰 사진이 들어간 인스타 캐러셀을 만들어줘.`

색상·캐릭터·언어·Acknowledgement는 작업별 입력값입니다. 기존 [치와와 AI 예시](examples/chihuahua-ai/README.md)는 별도로 보관하며, 선택했을 때만 사용하고 전역 설치에는 포함하지 않습니다. 각 계정의 설정과 제작한 파일은 해당 작업 폴더에 저장합니다. 입력 형식과 검증 방법은 [렌더러 안내](../../skills/instagram-content/references/renderer.md)에 있습니다. 파일 제작만으로 인스타에 자동 게시되지는 않습니다.

반복 제작에는 [로컬 실행 하네스](../../skills/instagram-content/references/harness.md)를 사용합니다. 선택한 계정 설정으로 완성 캡션과 장수를 검사하고, 장별 PNG·미리보기·업로드 ZIP을 만든 뒤 파일 구성을 검증합니다. 다음 작업에 쓸 설정과 제작 보고서도 저장합니다. 렌더링 없이 입력값만 검사하려면 `--validate-only`를 사용합니다.

```sh
python -m pip install -r "$HOME/.agents/skills/instagram-content/scripts/requirements.txt"
python -B "$HOME/.agents/skills/instagram-content/scripts/run_carousel.py" /path/to/post.json \
  --brief /path/to/brand-brief.json --out /path/to/output/carousel \
  --font-regular /path/to/Regular.ttf --font-bold /path/to/Bold.ttf
```

캡션 길이·해시태그 수·장수·문장부호 선호는 계정별로 지정합니다. 출처 확인과 실제 이미지 검토는 스킬의 제작 과정에 포함됩니다. [동작 테스트](../../skills/instagram-content/tests)는 Python 3.10·3.12 CI에서 실행하며, 복사한 스킬을 다른 폴더에서 실행하는 경우도 검사합니다. [재현 예시](examples/layout-demo/README.md)에서 실행 방법을 확인할 수 있습니다.
