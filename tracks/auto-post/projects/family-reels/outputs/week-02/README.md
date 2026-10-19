# 2주차 · MiniMax 장면 분석과 Seedance 생성·편집 실험

- 작성자: [임경태 · darkwingduck-code](https://github.com/darkwingduck-code)
- 트랙·프로젝트: Auto-Post · `tracks/auto-post/projects/family-reels/`
- 제출 PR: [#9](https://github.com/Pseudo-Lab/no-more-slops/pull/9), 대상 `main`
- 상태: **실행 결과 공유와 실패 분석**. 영상 품질 최종 승인·Instagram 게시·성과 측정은 미완료.

이번에는 화면 시연 이후 실제 API 호출과 로컬 렌더까지 실행했다. MiniMax는 **장면 분석·자막 초안**, Seedance는 **텍스트 기반 사물·풍경 생성**에 사용했다. 같은 원본을 바탕으로 한 제작 실험이며 두 모델의 영상 생성 성능을 공정 비교한 벤치마크는 아니다.

## 결과물

| 결과·Drive 영상 | 길이 | 제출 당시 상태 |
| --- | ---: | --- |
| [MiniMax 장면 분석 후 편집본](https://drive.google.com/file/d/1zI2Bmg0al0wERv_bOimK8eSytVMIH1v-/view?usp=drivesdk) | 45.5초 | M3 초안 13개를 시각 근거로 모두 보정. 기술 QA 통과, 전체 시청·청취와 사용자 채택 대기. Hailuo 영상 생성물이 아님. |
| [Seedance 첫 연결 시험](https://drive.google.com/file/d/1zpzHN1dGVIT06X3C4sn0by8j7j1Ttcxh/view?usp=drivesdk) | 5초 계획 / 5.041667초 실측 | 연결 성공. 원본과 관련성·길이·영상 품질이 부족하다는 사용자 피드백으로 미채택. |
| [Seedance 추가 생성 후보](https://drive.google.com/file/d/1KUmgf-EBYZa-Ij6SygNpu2GpPDspvbtm/view?usp=drivesdk) | 15초 계획 / 15.041667초 실측 | 길이를 늘린 사물·풍경 후보. 금속 구조물이 원본 난간과 달라 정밀 재현 실패. 채택 대기. |
| [실사+AI 교차 편집 검토본](https://drive.google.com/file/d/19VkMOEv05N4UGnxgRqIX_Ov0YLTeKswE/view?usp=drivesdk) | 32.4초 | 실사 17.4초 + AI 15초. AI 구간 표시, 자체 BGM·효과음, 기술 QA 통과. 사용자 품질 승인 대기. |

네 파일을 [Drive 결과 폴더](https://drive.google.com/drive/folders/1GUxj50qibVNpL4_bwhduNEr98OePMsw9)에 새로 업로드했다. **현재 공유 상태는 소유자 전용이다.** 업로드는 확인했으나 동료의 열람 권한은 아직 부여하지 못했다. 다른 계정은 접근 요청이 필요하며, 이를 공개 영상으로 표시하지 않는다. 원본·아기 프리뷰·얼굴 포함 영상·ZIP은 Git에 넣지 않았다.

- [실험 과정·실패·다음 개선 기준](experiment-report.md)
- [파일별 SHA-256·실측 길이·기술 QA 요약](results.json)
- [트렌드 조사와 선정 보류 근거](trend-brief.md)
- [이번 제출에서 수행한 검사](submission-verification.md)

## 함께 제출하는 제작 스킬

- [instagram-reel / SKILL.md](../../../../skills/instagram-reel/SKILL.md): 원본 확인, 자막·음악·렌더·기술 및 편집 검수.
- [family-reel-meme-preflight / SKILL.md](../../../../skills/family-reel-meme-preflight/SKILL.md): 편집 전 시장별 최신 근거와 아기 안전 검토.
- [MiniMax·Seedance 사용 절차와 실패 방지 참고 문서](../../../../skills/instagram-reel/references/minimax-seedance-workflow.md): 로컬·외부 호출, 입력 범위, 길이·비용 승인, 수락 불명 재시도, 후보와 완성본 검수의 구분.

기존 두 `SKILL.md`는 이 PR의 변경 목록에 포함되어 있다. #15와 공유하는 파일의 내용은 유지하고 새 참고 문서와 2주차 기록만 추가했다. 별도 스킬이나 프로젝트 내부의 스킬 사본은 만들지 않는다. #18의 일반 릴스 검수·뉴스 카피와 #23의 사람 없는 제품 CGI 광고는 관련 분야지만, 이번 기여는 가족 촬영 영상의 장면 분석·안전 선별과 생성 컷 연결 실험이다.

## 비용과 재현 범위

기본 컷·자막·자체 BGM·렌더는 로컬 경로이며 MiniMax 결제가 필수는 아니다. 이번에는 선택형 M3 클라우드 분석을 사용했다. 로컬 작업실에서 실행해도 외부 API 호출까지 무료가 되는 것은 아니다. Seedance 생성도 별도 유료 요청이다. 기존 응답·후보를 이용한 재편집과 새 생성 호출은 분리했다. 이번 Git 문서 작업에서는 공급자 호출·재생성·재렌더를 하지 않았다.

개인 원본과 API 키를 공개하지 않으므로 이 제출만으로 같은 생성물을 다시 만드는 완전 재현은 제공하지 않는다. 제작 당시의 파일 해시·타임라인·검사 수치와 실패 경계를 공유한다. 영상 접근 권한을 가진 검토자는 내려받은 파일 이름을 `results.json`의 `filename`에 맞춘 뒤 해시와 길이를 확인할 수 있다.

```sh
python -c "import hashlib,pathlib; p=pathlib.Path('minimax-result.mp4'); print(hashlib.file_digest(p.open('rb'),'sha256').hexdigest())"
ffprobe -v error -show_entries format=duration:stream=codec_name,width,height,r_frame_rate -of json minimax-result.mp4
```

저장소 루트에서 제출 구조만 검사하려면 다음을 실행한다. Python 3.11 이상과 Git이 필요하며, 영상 확인에는 별도로 FFmpeg의 `ffprobe`가 필요하다.

```sh
python scripts/check_repository.py
python -m unittest discover -s scripts -p test_check_repository.py
git diff --check
```

## 지표·레슨런·리뷰 요청

한국 Instagram 최근 72시간 기준의 적격 트렌드 표본은 **0건**이다. 최신 밈 선정·조회수 순위·좋아요 개선은 검증하지 못했다. 이번 영상은 장면 중심 창작 실험으로 제출한다. API 성공과 기술 QA만으로 결과 품질을 보장할 수 없었고, 특히 생성 컷이 원본 사물·행동에 연결되는지 별도 판단이 필요했다.

동료에게는 다음 세 가지를 검토 부탁드린다.

1. MiniMax 자막이 실제 보이는 행동을 설명하는지, 보정 후에도 과한 해석이 남았는지.
2. Seedance 컷이 원본의 숟가락·난간과 자연스럽게 연결되는지, 빼는 편이 나은 컷은 무엇인지.
3. 기술 검사·편집 승인·트렌드 입증·실제 게시의 상태가 자료에서 명확히 구분되는지.

---

## 초기 제출 기록 · 밈 사전 기획과 파이프라인 화면

아래는 초기 시연 제출의 범위와 당시 검증 기록이다. 후속 실제 API 실행과 혼동하지 않도록 보존한다.

- 작성자: [임경태 · darkwingduck-code](https://github.com/darkwingduck-code)
- 원본 PR: [#9](https://github.com/Pseudo-Lab/no-more-slops/pull/9)
- 관련 제작 이력: [1주차 #15](https://github.com/Pseudo-Lab/no-more-slops/pull/15). 공통 규칙 PR #16을 반영한 뒤 두 PR의 병합 순서는 자유입니다.
- 결과물: [instagram-automation-pipeline.html](instagram-automation-pipeline.html)
- 제작 절차: [family-reel-meme-preflight](../../../../skills/family-reel-meme-preflight/SKILL.md), [instagram-reel](../../../../skills/instagram-reel/SKILL.md)

저장소 루트에서 `python -m http.server 8000`을 실행하고 다음 주소를 엽니다.

```text
http://localhost:8000/tracks/auto-post/projects/family-reels/outputs/week-02/instagram-automation-pipeline.html
```

화면은 1·2주차 흐름, Three.js 보물상자와 단계별 진행 시연, Instagram·YouTube·TikTok·X × 한국·일본·미국의 12개 조합 상태판, 로컬 `trend-plan.json` 읽기를 제공합니다. 진행 체험은 화면 시연이며 플랫폼 API·Python·FFmpeg를 직접 실행하지 않습니다. JSON은 브라우저 안에서 읽고 서버에 업로드하지 않습니다. 버전을 고정한 Three.js CDN 모듈이 로드되지 않으면 2D 대체 화면이 남습니다.

원본 PR에는 스킬 형식 검사, 별도 선별기 테스트 4개, 브라우저 렌더 및 스크립트 구문 검사를 수행했다고 기록되어 있습니다. 해당 선별기·영상 렌더 스크립트, 5분 발표 PPTX, 대본·예상 Q&A는 별도 제작 저장소에 있으며 이 저장소에 포함되지 않습니다.

현재 12개 조합은 확인된 원본 조회수·안전 검토 근거가 부족해 후보 선정을 보류한 상태입니다. 공개 지표 자동 수집은 연결되지 않았으며 조회수 증가를 보장하지 않습니다. 1주차 영상 링크는 [1주차 결과물](../week-01/README.md)에 보관합니다.

이 결과물은 가짜연구소(Pseudo Lab) No-More-Slops 그룹 활동의 일환으로 제작되었습니다.
