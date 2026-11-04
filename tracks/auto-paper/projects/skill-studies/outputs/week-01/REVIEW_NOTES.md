# 원고·해설서 통합 검토 v5

작성일: 2026-10-12. 검토는 연구 설계를 개선하기 위한 작업이며 학술 심사·신규성·사실성·인과 효과 인증으로 쓰지 않는다.

## 작성과 검토의 분리

- skills_papers가 SkillMerge의 paper/해설/방법/source 파일을 작성했고, purpleforge_papers가 수식·개별 개선 자격·θ 모집단·cohort 분리·비용·가설 경계를 읽기 전용으로 검토했다.
- purpleforge_papers가 Second-Chance 파일을 작성했고, probeflow_compact가 점수 항등식·경로 감사·선택/교훈 fork·endpoint·분모를 읽기 전용으로 검토했다.
- probeflow_compact가 ProbeFlow 파일을 작성했고, purpleforge_papers가 cache 조건부 반례·XOR/proxy·제한 Bellman·free information·calibration·실제 데이터 준비를 읽기 전용으로 검토했다.
- root는 세 원고와 계약을 읽고 작은 계산을 독립 구현했다. 조판·본문 보존·원본 연결·PDF 구조·폰트·페이지 경계를 검증하고 배포를 담당한다.

## 문헌 대조가 바꾼 기여 범위

SkillSmith의 typed signature·atomic migration·interaction, SkillCommit의 directed replay, SkillOpt/SkillOpt-Sleep의 rejected buffer·replay·memory update, L2M/NM-PPG/BRiG-AFA의 acquisition·non-myopic 계획을 공식 원문에서 확인했다. 그 아이디어의 첫 제안이라는 주장은 제거했다. 각 연구는 개별 자격 후 조합 효과의 측정, 평가기 교정의 downstream 선택·교훈 복구, 공유 자원과 실제 공개 상태의 acquisition 효과를 구체적 비교로 설계한다.

선행논문의 모든 코드를 재현하거나 우선권을 판정하지 않았다. SkillMerge/ProbeFlow의 설명용 정리와 반례는 가정이 있는 저자 모형이며 신규 이론 또는 실제 모델 성능으로 제시하지 않는다.

## 정량·형식 검토

SkillMerge의 3입력 상태별 성공 행렬(1,2,2,0,3)은 원고의 typed functions를 별도로 구현해 확인했다. 마지막3은 adapter 상태다. mathematical mean gain은 empirical Q-qualified event와 다르다. Negative τ를 strict1110와 구분하고 θ는 scoring에서 사후 선택한 최고 단일군을 baseline으로 쓰지 않는다. 남은 핵심 설계 결정은 θ의 source family/history 가중치와 effective cluster다. S 이전에 고정해야 한다.

Second-Chance의 frozen output score identity와 inclusive version DAG 경로 범위는 명시한 가정 안에서 확인했다. Desc(D)∩Anc(T)는 recorded affected live path를 덮는 집합이며 최소 행동 수정 집합이 아니다. RAUC는 left-step 계산이고 missing positive-width interval은 NA다. nonmonotonic first observed hit를 first-ever recovery의 인증 시간으로 쓰지 않는다.

Second-Chance 교차 검토는 조건부 재발과 전체 이력의 later-panel failure를 원고에서도 명시적으로 구분하도록 요구했다. 또한 같은 stochastic selector를 쓰는 것으로 같은 selected repair가 보장되지 않으므로 lesson-only paired contrast는 실제 selection/integration artifact와 state hash를 먼저 고정한 뒤 lesson만 fork하도록 요구했다. Full factorial의 procedure effect와 이 paired memory contrast를 분리한다.

ProbeFlow의 원시 source cache와 실제 공개 mask는 다른 객체지만 언제나 별도 state가 필요하다는 주장은 하지 않는다. 성공한 결정론적 DAG와 완전한 provenance에서는 cache를 재구성할 수 있다. 값과 독립인 실패가 source만 유지하는 반례에서 동일 empty mask/remaining budget에도 다음 비용1과5가 다름을 확인했다. XOR risk, noisy proxy, exact-identity 공유 비용도 계산했다. 온전한 finite outcome model과 비음수 비용/α가 없는 산업 설정에 stopping certificate를 옮기지 않는다. Learned all-input teacher는 Bayes relaxation이 아니다.

## 검증 범위

root의 15개 formal example 검사와 7개 source/math/guide-footer 조판 검사가 통과했다. 원고는 각4페이지이며 authored prose가 잘리지 않았는지, reference URL·내부 인용·수학 및 outline font·source/PDF hash·페이지별 절 위치를 검사한다. 해설서는 수학 fence 외 모든 문단·표 셀·목록의 prose 보존을 비교하고 embedded fonts·본문 경계·source/PDF hash를 검사한다.

해설서 페이지를 가로지르는 문단을 대조할 때 PDF footer 숫자가 본문에 끼는 문제가 있어, 식별한 마지막 footer 줄만 제거하도록 검증기를 수정했다. 본문에 있는 숫자를 함께 제거하지 않는 회귀 검사도 넣었다. 이는 텍스트 검증의 수정이며 원고 문장을 삭제한 것이 아니다.

기존 v3/v4 기록은 새 성능 실험으로 표시하지 않았다. 실제 모델 생성·자연 통합 이력·현재 복구·산업 학습·calibration·정책 실측·사전등록은 미완료다. 데이터와 이전 실행·활성 skill·기존 Git PR은 보존했다.
