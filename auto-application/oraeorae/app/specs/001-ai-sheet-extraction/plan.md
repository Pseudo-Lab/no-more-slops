# Implementation Plan: 결과지 AI 판독

**Branch**: `001-ai-sheet-extraction` | **Date**: 2026-10-10 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-ai-sheet-extraction/spec.md`

## Summary

업로드 화면에서 결과지를 서버 액션으로 보내 OpenAI Responses API(구조화 출력)로 표준 항목의 수치·판정을
뽑고, 같은 화면에서 바로 확인 단계로 넘어간다. 원본과 추출값은 저장 전까지 서버·URL·브라우저 저장소
어디에도 남기지 않는다.

## Technical Context

**Language/Version**: TypeScript, Next.js 16.4 (App Router, Cache Components), React 19.3
**Primary Dependencies**: 기존 의존성만 사용. OpenAI는 SDK 없이 `fetch`로 호출 (의존성 추가 없음)
**Storage**: 변경 없음 (`exams`, `exam_items`). 판정은 기존 check 제약을 그대로 따른다
**Testing**: lint + build, 로컬에서 키 없이 예시 값 경로 확인, 배포 주소에서 실제 결과지로 확인
**Target Platform**: 모바일 웹(Safari/Chrome), Vercel icn1
**Project Type**: web-service (단일 Next.js 앱)
**Performance Goals**: 사진 선택→확인 화면 20초 이내
**Constraints**: Vercel 함수 요청 본문 4.5MB 한도 → 서버 액션 한도 4MB, 사진은 기기에서 긴 변 2048px로 축소
**Scale/Scope**: 가족 단위 소수 사용자, 결과지 1장/요청

## Constitution Check

| 원칙 | 확인 |
|---|---|
| I. 최소 수집 | 원본은 요청 메모리에서만 사용, `store: false`, 로그에는 상태 코드만 |
| II. 동의 | 서버 액션에서 `transfer` 동의를 확인한 뒤에만 호출. 수탁자는 기존 고지(OpenAI) 그대로 |
| III. 진단 금지 | 결과지에 적힌 판정만 추출, 없으면 `null` → 사용자가 직접 고름 |
| IV. 경계 보안 | `OPENAI_API_KEY`는 서버 전용, 로그인·가족 구성원 확인 후 호출, 실패는 `{ error }` 반환 |
| V. 최소 변경 | SDK·새 라우트 없음. `/upload/review` 라우트는 삭제하고 업로드 화면에서 단계 전환 |

## Project Structure

### Documentation (this feature)

```text
specs/001-ai-sheet-extraction/
├── spec.md
├── plan.md
├── tasks.md
└── checklists/requirements.md
```

### Source Code (repository root)

```text
next.config.ts                          # serverActions.bodySizeLimit
src/lib/checkup-items.ts                # 표준 항목 목록 (키·이름·단위)
src/lib/analytics.ts                    # extract_error 이벤트
src/app/(family)/upload/extract.ts      # 서버 액션: 동의 확인 → OpenAI 호출 → 항목 반환
src/app/(family)/upload/page.tsx        # 헤더를 단계별로 바꾸도록 폼으로 이동
src/app/(family)/upload/upload-form.tsx # 축소·전송·오류 안내, 성공 시 ReviewForm 표시
src/app/(family)/upload/review-form.tsx # (review/에서 이동) 판정 null 허용
src/app/(family)/upload/review/         # 삭제
src/lib/mock.ts                         # 키 없는 환경용 예시 값으로 유지
```

**Structure Decision**: 추출값을 페이지 사이로 넘기려면 URL·저장소에 건강 정보를 남겨야 하므로,
업로드와 확인을 한 클라이언트 컴포넌트의 두 단계로 합친다.

## Complexity Tracking

없음.

## Cost & Accuracy (2026-10-11)

| 조치 | 효과 | 근거 |
|---|---|---|
| 사진을 2,500 패치(32px)·긴 변 2048px 안으로 기기에서 축소 | 업로드 감소, OpenAI 쪽 재축소로 인한 흐림 방지. 토큰은 장당 약 3,000으로 상한 | OpenAI vision 문서 (gpt-5.4-mini, detail high) |
| `reasoning.effort: "none"` 명시 | 추론 토큰 0 — 옮겨 적기에는 추론이 필요 없음 | 모델 기본값과 무관하게 고정 |
| 고정 `instructions` (사용자별 내용 없음) | 접두어 캐시 대상, 지시문이 커져도 비용 증가 억제 | Prompt caching |
| 항목 목록에 key·결과지 표기·단위를 함께 제공 | `tg`·`ggt` 같은 키만으로 추측하던 매칭 오류 감소 | — |
| 이전 연도 값·참고치 옮기지 않기 규칙 | 결과지 표의 다른 열을 잘못 읽는 오류 감소 | — |
| `uncertain` 필드 → 확인 화면 "확인 필요" 표시 | 흐린 글자·단위 불일치를 사용자가 먼저 확인 | 헌법 III (사용자 확인) |
| 날짜 고정 모델 스냅샷 | 별칭 갱신으로 정확도가 조용히 바뀌는 것 방지 | — |
| 429·5xx 1회 재시도, 미완료·파싱 실패 처리 | 일시 오류로 인한 실패 감소, 서버 예외 대신 안내 문구 | — |

예상 비용: 사진 1장 ≈ 입력 3,300 토큰 + 출력 약 300 토큰 ≈ $0.004 (입력 $0.75 / 출력 $4.5 per 1M).
PDF는 페이지마다 텍스트와 이미지가 함께 들어가 여러 장이면 몇 배가 될 수 있다 — 사진 업로드를 기본 안내로 둔다.

## Multi-page PDF (2026-10-11)

A 36-page, 7.6MB clinic report exceeded the 4MB limit and would cost roughly 20x a photo if sent whole.

- **On-device parsing (pdfjs-dist):** the PDF is read in the browser, so there is no size limit and no original upload.
- **Text:** every page's text goes up with page numbers. This is about 19k characters, 32KB. Resident registration numbers are masked on the device first.
- **Image:** one image of the page that names the most catalog items (`find` hints) is rendered at the 2,500-patch budget. The ■/□ judgement boxes are read from it.
- **Rules:**
  - Values come from the text; judgements come from the image's checkmarks.
  - Split slash values such as 117/70.
  - Skip `***` (not applicable) items.
  - Map 전단계/장애 의심 to 경계.
- **Scanned PDF with no text layer:** the user is asked to take a photo instead.
- **Verified on a real report:** page 26 was picked with 17/17 items. The output was a 1331×1883 JPEG of 398KB plus 18.8k characters, and no RRN remained.
