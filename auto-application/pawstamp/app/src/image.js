import exifr from 'exifr';

// 사진의 위치(GPS)와 찍은 날짜를 읽는다. 없으면 null.
export async function readPhotoMeta(file) {
  try {
    const data = await exifr.parse(file, { gps: true, pick: ['DateTimeOriginal', 'latitude', 'longitude'] });
    return {
      lat: data?.latitude ?? null,
      lng: data?.longitude ?? null,
      takenAt: data?.DateTimeOriginal instanceof Date ? data.DateTimeOriginal : null,
    };
  } catch {
    return { lat: null, lng: null, takenAt: null };
  }
}

// 업로드 전에 사진을 줄여서 JPEG Blob 으로 만든다. (위치 정보는 여기서 떨어져 나간다)
export async function shrinkImage(file, maxSize = 1280, quality = 0.82) {
  const url = URL.createObjectURL(file);
  try {
    const img = await new Promise((res, rej) => {
      const i = new Image();
      i.onload = () => res(i);
      i.onerror = () => rej(new Error('이 사진 형식은 열 수 없어요. JPG나 PNG로 올려주세요.'));
      i.src = url;
    });
    const scale = Math.min(1, maxSize / Math.max(img.naturalWidth, img.naturalHeight));
    const canvas = document.createElement('canvas');
    canvas.width = Math.round(img.naturalWidth * scale);
    canvas.height = Math.round(img.naturalHeight * scale);
    canvas.getContext('2d').drawImage(img, 0, 0, canvas.width, canvas.height);
    return await new Promise((res) => canvas.toBlob(res, 'image/jpeg', quality));
  } finally {
    URL.revokeObjectURL(url);
  }
}

// 두 좌표 사이 거리(m)
export function distance(a, b) {
  const R = 6371000, toRad = (d) => (d * Math.PI) / 180;
  const dLat = toRad(b.lat - a.lat), dLng = toRad(b.lng - a.lng);
  const h = Math.sin(dLat / 2) ** 2 + Math.cos(toRad(a.lat)) * Math.cos(toRad(b.lat)) * Math.sin(dLng / 2) ** 2;
  return 2 * R * Math.asin(Math.sqrt(h));
}
