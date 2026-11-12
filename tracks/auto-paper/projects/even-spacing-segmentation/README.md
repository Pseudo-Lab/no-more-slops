# even-spacing-segmentation

Auto-Paper 트랙의 [YOOHYOJEONG](https://github.com/YOOHYOJEONG) 기여입니다. 원 PR: #번호

전사(transcript) 기반 분할·챕터링 평가에서, 경계를 맞았다고 인정하는 허용 오차(tolerance)가 평균 구간 길이에 비해 얼마나 넓은지에 따라 모델 순위가 뒤집히는 현상을 다룹니다. 허용 오차가 넓으면 정답 경계 수만 알고 경계를 균등하게 배치하는 기준선(even spacing)이 학습된 분할 모델을 이길 수 있습니다.

Week 04 프로젝트 [sparse-recomputation-segmentation](https://github.com/Pseudo-Lab/no-more-slops/pull/37)의 VT-SSum 결과(균등 배치 대비 이점이 결론 불가로 나오고, 더 넓은 허용 오차에서 역전됨)에서 출발한 후속 연구입니다. 이 PR은 그 PR과 독립적이며 먼저 병합될 필요가 없습니다.

## 주차별 결과물

- [Week 05](outputs/week-05/README.md): 영문 논문 PDF

## 폴더 구성

| 경로 | 내용 |
| --- | --- |
| [outputs/week-05/](outputs/week-05/) | 논문 PDF와 주차 기록 |

## 사용한 스킬

이 저장소의 스킬은 추가하거나 변경하지 않았습니다.

---

This work was created as part of the No-More-Slops group activities at Pseudo Lab.

이 결과물은 가짜연구소(Pseudo Lab) No-More-Slops 그룹 활동의 일환으로 제작되었습니다.
