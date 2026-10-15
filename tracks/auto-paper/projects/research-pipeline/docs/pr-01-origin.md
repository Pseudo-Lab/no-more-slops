# PR #1 기여 기록

- 작성자: [chewonc](https://github.com/chewonc)
- 원 제출: [Auto-Paper 연구 기획 스킬 #1](https://github.com/Pseudo-Lab/no-more-slops/pull/1)
- 정리 전 스킬 원본: [c3ed0c0 커밋](https://github.com/chewonc/no-more-slops/tree/c3ed0c0b26f6e4d496974afec0ca09e73b9eeb0e/auto-paper/claude-skills/.claude/skills)
- 기획 개선 출처: [#12](https://github.com/Pseudo-Lab/no-more-slops/pull/12)

## 현재 공유 구현

#1에서 시작한 기초 연구 기획 스킬 7개는 `tracks/auto-paper/skills/`에서 관리합니다. #12가 개선한 최신 본문과 참조 자료를 #1에도 반영하여 #16 이후 두 PR의 병합 순서가 결과를 바꾸지 않도록 했습니다. 연구 질문 파싱, 벤치마크 조사, 선행연구 확인, 계산 계획, 연구 계획과 준비도 판단이라는 원 기여 범위는 유지합니다.

이 문서는 #1의 출처와 원 기여 내용을 남기는 독립적인 기록입니다. 스킬 구현을 복사해 보관하지 않습니다. #12가 먼저 반영되어도 #1의 이 기록을 추가할 수 있습니다. 기존 커밋 이력은 보존했습니다.

## 원 제출 설명

## Summary

Adds a set of Claude skills for the Auto-Paper research workflow.

The pipeline helps convert initial research questions into feasible, benchmark-grounded research projects by supporting:

- Parsing research questions from documents
- Benchmark discovery and validation
- Prior-work and overlap checking
- Compute and duration feasibility planning
- Research plan review
- End-to-end research planning

## Added skills

- `research-pipeline`
- `research-question-parser`
- `research-planner`
- `benchmark-finder`
- `prior-work-checker`
- `compute-planner`
- `research-readiness-advisor`

Supporting reference files for benchmark selection, compute planning, and research guidance are also included.

## Goal

The goal is to make the Auto-Paper workflow more systematic and reproducible while keeping research projects feasible within the user's specified time and compute constraints.
