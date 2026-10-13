// 올리기 전 걸러내기: 욕설 텍스트, 사람 얼굴이 보이는 사진.
// 브라우저에서 먼저 막고(빠른 안내), 욕설은 Supabase 쪽에서도 한 번 더 막는다(schema.sql 의 has_bad_words).

// 띄어쓰기·숫자·기호를 끼워 넣어 피하는 경우("시 1 발", "ㅅ.ㅂ")까지 잡으려고 한글·영문만 남겨서 검사한다.
// "새끼"(강아지 새끼), "시바"(시바견)는 일상 표현이라 단독으로는 막지 않는다.
const BAD = [
  '시발', '씨발', '씨바', '씨빨', '시빨', '쓰발', 'ㅅㅂ', 'ㅆㅂ', 'ㅄ', 'ㅂㅅ',
  '병신', '븅신', '빙신', '병쉰', '개새끼', '개색기', '개색끼', '개세끼', '개쌔끼', '개새기',
  '좆', '존나', '졸라', 'ㅈㄴ', '지랄', 'ㅈㄹ', '미친놈', '미친년', '미친새끼', '또라이',
  '엠창', '느금', '니애미', '니어미', '니미', '썅', '쌍년', '쌍놈', '걸레년', '창녀', '꺼져', '닥쳐',
  'fuck', 'shit', 'bitch', 'asshole',
];

const normalize = (text) => String(text ?? '').toLowerCase().replace(/[^가-힣ㄱ-ㅎa-z]/g, '');

export function hasBadWords(...texts) {
  return texts.some((t) => {
    const n = normalize(t);
    return n && BAD.some((w) => n.includes(w));
  });
}

// ---------- 사람 얼굴 감지 ----------
// 사진을 고를 때 한 번만 모델을 내려받는다(약 1MB).
// 폰 브라우저(아이폰 사파리, 카톡·인스타 인앱)에서 모델이 안 뜨거나 멈출 수 있어서,
// 실패하거나 6초 안에 준비가 안 되면 검사 없이 사진을 통과시킨다. 사진 올리기가 막히면 안 되니까.
const within = (promise, ms) => Promise.race([promise, new Promise((res) => setTimeout(() => res(null), ms))]);
let detectorPromise = null;
function getDetector() {
  return within(loadDetector(), 6000);
}
function loadDetector() {
  detectorPromise ??= (async () => {
    const { FilesetResolver, FaceDetector } = await import('@mediapipe/tasks-vision');
    const vision = await FilesetResolver.forVisionTasks('https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@1.0.1/wasm');
    return FaceDetector.createFromOptions(vision, {
      baseOptions: {
        modelAssetPath: 'https://storage.googleapis.com/mediapipe-models/face_detector/blaze_face_short_range/float16/1/blaze_face_short_range.tflite',
        delegate: 'CPU', // GPU(WebGL) 대신 CPU: 폰 인앱 브라우저에서 더 잘 돈다
      },
      runningMode: 'IMAGE',
      minDetectionConfidence: 0.7,
    });
  })().catch((err) => {
    console.warn('[Pawstamp] 얼굴 감지 모델을 불러오지 못했어요', err);
    detectorPromise = null;
    return null;
  });
  return detectorPromise;
}

// 사람 얼굴을 찾아서 그 부분만 모자이크한 사진을 돌려준다. { blob, faces: 가린 얼굴 수 }
// 강아지와 찍은 셀카는 이 서비스의 핵심 사진이라 막지 않고 얼굴만 가린다.
export async function blurFaces(blob) {
  try {
    return await blurFacesUnsafe(blob);
  } catch (err) {
    console.warn('[Pawstamp] 얼굴 가림을 건너뛰어요', err);
    return { blob, faces: 0 };
  }
}
async function blurFacesUnsafe(blob) {
  const detector = await getDetector();
  if (!detector) return { blob, faces: 0 };
  const bitmap = await createImageBitmap(blob);
  try {
    const found = detector.detect(bitmap).detections;
    if (!found.length) return { blob, faces: 0 };
    const canvas = document.createElement('canvas');
    canvas.width = bitmap.width;
    canvas.height = bitmap.height;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(bitmap, 0, 0);
    for (const { boundingBox: b } of found) {
      // 머리카락·턱까지 덮도록 상자를 넉넉히 키운다
      const pad = 0.45;
      const x = Math.max(0, b.originX - b.width * pad);
      const y = Math.max(0, b.originY - b.height * pad * 1.3);
      const w = Math.min(canvas.width - x, b.width * (1 + pad * 2));
      const h = Math.min(canvas.height - y, b.height * (1 + pad * 2.3));
      // 작게 줄였다가 다시 키워서 모자이크
      const cells = 8;
      const tmp = document.createElement('canvas');
      tmp.width = cells;
      tmp.height = Math.max(1, Math.round((cells * h) / w));
      tmp.getContext('2d').drawImage(canvas, x, y, w, h, 0, 0, tmp.width, tmp.height);
      ctx.imageSmoothingEnabled = false;
      ctx.drawImage(tmp, 0, 0, tmp.width, tmp.height, x, y, w, h);
      ctx.imageSmoothingEnabled = true;
    }
    const out = await new Promise((res) => canvas.toBlob(res, 'image/jpeg', 0.85));
    return { blob: out, faces: found.length };
  } finally {
    bitmap.close();
  }
}

export async function hasHumanFace(blob) {
  try {
    return await hasHumanFaceUnsafe(blob);
  } catch (err) {
    console.warn('[Pawstamp] 얼굴 검사를 건너뛰어요', err);
    return false;
  }
}
async function hasHumanFaceUnsafe(blob) {
  const detector = await getDetector();
  if (!detector) return false;
  const bitmap = await createImageBitmap(blob);
  try {
    return detector.detect(bitmap).detections.length > 0;
  } finally {
    bitmap.close();
  }
}

// 페이지가 열리면 미리 준비해 둔다 (사진 고를 때 기다림 줄이기)
export const warmUpFaceDetector = () => loadDetector();
