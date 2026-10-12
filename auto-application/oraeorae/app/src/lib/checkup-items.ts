// Business: numeric items of the Korean national health checkup (1차). Keys must never change —
// trends match exams across years by key. Qualitative items (urine protein, chest X-ray) are left out.
// `find` is how the national checkup form prints the item; it locates the result page inside long PDFs.
export const CHECKUP_ITEMS = [
  { key: "height", label: "키", unit: "cm", find: "키(cm)" },
  { key: "weight", label: "몸무게", unit: "kg", find: "몸무게" },
  { key: "waist", label: "허리둘레", unit: "cm", find: "허리둘레" },
  { key: "bmi", label: "체질량지수", unit: "kg/m²", find: "체질량지수" },
  { key: "sbp", label: "수축기 혈압", unit: "mmHg", find: "수축기" },
  { key: "dbp", label: "이완기 혈압", unit: "mmHg", find: "이완기" },
  { key: "glucose", label: "공복혈당", unit: "mg/dL", find: "공복혈당" },
  { key: "total_chol", label: "총콜레스테롤", unit: "mg/dL", find: "총콜레스테롤" },
  { key: "hdl", label: "HDL 콜레스테롤", unit: "mg/dL", find: "고밀도" },
  { key: "ldl", label: "LDL 콜레스테롤", unit: "mg/dL", find: "저밀도" },
  { key: "tg", label: "중성지방", unit: "mg/dL", find: "중성지방" },
  { key: "hemoglobin", label: "혈색소", unit: "g/dL", find: "혈색소" },
  { key: "creatinine", label: "혈청 크레아티닌", unit: "mg/dL", find: "크레아티닌" },
  { key: "egfr", label: "신사구체여과율(eGFR)", unit: "mL/min/1.73m²", find: "신사구체여과율" },
  { key: "ast", label: "AST(간)", unit: "U/L", find: "AST" },
  { key: "alt", label: "ALT(간)", unit: "U/L", find: "ALT" },
  { key: "ggt", label: "감마지티피(간)", unit: "U/L", find: "감마" },
] as const;
