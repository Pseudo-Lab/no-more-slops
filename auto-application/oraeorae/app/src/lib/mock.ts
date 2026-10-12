import type { Item } from "./health";

// Future: stands in for AI extraction until OPENAI_API_KEY is configured; the user edits these before saving.
export const SAMPLE_EXTRACTED: Item[] = [
  { key: "sbp", label: "수축기 혈압", unit: "mmHg", section: null, value: 128, textValue: null, reference: null, flag: null, judgement: "정상" },
  { key: "dbp", label: "이완기 혈압", unit: "mmHg", section: null, value: 82, textValue: null, reference: null, flag: null, judgement: "경계" },
  { key: "glucose", label: "공복혈당", unit: "mg/dL", section: null, value: 104, textValue: null, reference: null, flag: null, judgement: "경계" },
  { key: "ldl", label: "LDL 콜레스테롤", unit: "mg/dL", section: null, value: 152, textValue: null, reference: null, flag: null, judgement: "경계" },
  { key: "alt", label: "ALT(간)", unit: "U/L", section: null, value: 24, textValue: null, reference: null, flag: null, judgement: "정상" },
];
