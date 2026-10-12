# issues

레포가 연결되기 전에 쌓아 두는 GitHub 이슈 초안. 파일 하나가 이슈 하나다.

## 형식
```markdown
---
title: "이슈 제목"
labels: bug, auth
---

본문 (GitHub 이슈 본문 그대로)
```

게시되면 frontmatter에 `issue: <URL>` 줄이 추가된다. 이 줄이 있는 파일은 다시 게시하지 않는다.

## 게시
레포를 만들고 `origin`을 연결한 뒤:

```bash
gh auth status          # 로그인 확인
scripts/publish-issues.sh
```

없는 라벨은 자동으로 만든다.
