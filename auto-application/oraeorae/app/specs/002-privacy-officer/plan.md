# Implementation Plan: 개인정보 보호책임자 표기

**Branch**: `002-privacy-officer` | **Date**: 2026-10-10 | **Spec**: [spec.md](./spec.md)

## Summary

`SERVICE.officer` 값을 담당 이름으로 바꾸고, 처리방침의 "성명"·하단의 "보호책임자" 라벨을 담당 이름에 맞게 고친다.

## Technical Context

**Language/Version**: TypeScript, Next.js 16.4 | **Storage**: N/A | **Testing**: lint + build, 배포 주소 확인

## Constitution Check

| 원칙 | 확인 |
|---|---|
| I–IV | 해당 없음 (문구 변경) |
| V. 최소 변경 | 상수 1개와 라벨 2곳 |

## Project Structure

```text
src/lib/service.ts        # officer 값과 이유 주석
src/app/site-footer.tsx   # 라벨
src/app/privacy/page.tsx  # 라벨
```

## Complexity Tracking

없음.
