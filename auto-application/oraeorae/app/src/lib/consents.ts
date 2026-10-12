// Constraint: PIPA arts. 15, 17, 23 and 28-8 require each consent to state purpose, items, retention and the right to refuse.
// The consent form, privacy policy and settings all read this list so the wording can't drift apart.
export const CONSENTS = [
  {
    id: "sensitive",
    title: "건강정보(민감정보) 수집·이용",
    summary: "검진 수치와 판정을 가족 기록을 위해 저장해요.",
    rows: [
      ["목적", "건강검진 결과 기록, 해마다 변화 확인"],
      ["항목", "검진일, 검사 항목별 수치와 결과지에 적힌 판정, 가족에게 보일 이름·관계·출생연도"],
      ["보유 기간", "회원 탈퇴 또는 기록 삭제 시 즉시 파기"],
      ["거부할 권리", "동의하지 않을 수 있어요. 다만 건강 기록 서비스를 이용할 수 없어요."],
    ],
  },
  {
    id: "share",
    title: "가족 그룹 내 제공",
    summary: "같은 가족 그룹의 구성원만 내 기록을 볼 수 있어요.",
    rows: [
      ["제공받는 자", "내가 만들거나 참여한 가족 그룹의 구성원"],
      ["목적", "가족이 서로의 건강검진 결과를 함께 확인"],
      ["항목", "위 건강정보 전체"],
      ["보유 기간", "가족 그룹에 참여하는 동안 (탈퇴 시 즉시 중단)"],
      ["거부할 권리", "동의하지 않을 수 있어요. 다만 가족과 기록을 함께 볼 수 없어요."],
    ],
  },
  {
    id: "transfer",
    title: "AI 판독을 위한 국외 이전",
    summary: "결과지를 읽기 위해 해외 AI 서비스로 보내고, 원본은 저장하지 않아요.",
    rows: [
      ["이전받는 자", "OpenAI, L.L.C. (미국) · privacy@openai.com"],
      ["이전 항목", "업로드한 결과지 이미지에 담긴 정보"],
      ["시기·방법", "결과지를 올릴 때 암호화된 네트워크로 전송"],
      ["목적", "결과지의 검사 수치와 판정 읽기"],
      ["보유 기간", "판독 후 서비스에는 원본을 저장하지 않아요. OpenAI는 정책에 따라 최대 30일 보관 후 삭제하고 학습에 쓰지 않아요."],
      ["거부할 권리", "동의하지 않을 수 있어요. 다만 결과지 자동 판독을 이용할 수 없어요."],
    ],
  },
] as const;

export type ConsentId = (typeof CONSENTS)[number]["id"];
