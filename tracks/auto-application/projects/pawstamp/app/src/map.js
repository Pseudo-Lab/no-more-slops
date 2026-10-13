// 카카오맵 래퍼. main.js 는 이 파일의 함수만 쓰고 카카오 API 를 직접 만지지 않는다.
// 카카오 줌 "레벨"은 숫자가 작을수록 가깝다 (1 = 가장 가까움, 14 = 가장 멂).

const KEY = import.meta.env.VITE_KAKAO_MAP_KEY;

export function loadKakao() {
  return new Promise((resolve, reject) => {
    if (!KEY) return reject(new Error('카카오맵 키가 없어요. .env 에 VITE_KAKAO_MAP_KEY 를 넣어주세요.'));
    const s = document.createElement('script');
    s.src = `https://dapi.kakao.com/v2/maps/sdk.js?appkey=${KEY}&autoload=false&libraries=services`;
    s.onload = () => window.kakao.maps.load(() => resolve(window.kakao));
    s.onerror = () => reject(new Error('카카오맵을 불러오지 못했어요. 카카오 개발자 설정에 이 사이트 주소가 등록돼 있는지 확인해 주세요.'));
    document.head.appendChild(s);
  });
}

export class KakaoMap {
  constructor(kakao, el, { lat, lng, level }) {
    this.k = kakao.maps;
    this.map = new this.k.Map(el, { center: new this.k.LatLng(lat, lng), level });
    this.map.addControl(new this.k.ZoomControl(), this.k.ControlPosition.BOTTOMLEFT);
    this.overlays = [];
    this.draft = null;
    this.places = new this.k.services.Places();
  }

  get level() { return this.map.getLevel(); }

  onZoom(cb) { this.k.event.addListener(this.map, 'zoom_changed', cb); }
  onClick(cb) {
    this.k.event.addListener(this.map, 'click', (e) => cb({ lat: e.latLng.getLat(), lng: e.latLng.getLng() }));
  }

  // 화면 위 픽셀 좌표 (묶음 계산용)
  point({ lat, lng }) {
    return this.map.getProjection().containerPointFromCoords(new this.k.LatLng(lat, lng));
  }

  setView({ lat, lng }, level = this.level) {
    this.map.setLevel(level);
    this.map.setCenter(new this.k.LatLng(lat, lng));
  }
  panBy(dx, dy) { this.map.panBy(dx, dy); }

  fitBounds(points, maxLevel = 1) {
    if (!points.length) return;
    const b = new this.k.LatLngBounds();
    for (const p of points) b.extend(new this.k.LatLng(p.lat, p.lng));
    this.map.setBounds(b, 80, 60, 120, 60);
    if (this.level < maxLevel) this.map.setLevel(maxLevel);
  }

  // HTML 마커들을 한 번에 갈아끼운다. items: [{ lat, lng, el }]
  setMarkers(items) {
    for (const o of this.overlays) o.setMap(null);
    this.overlays = items.map(({ lat, lng, el }) => new this.k.CustomOverlay({
      map: this.map, position: new this.k.LatLng(lat, lng), content: el, xAnchor: 0.5, yAnchor: 1, clickable: true,
    }));
  }

  showDraft({ lat, lng }) {
    this.clearDraft();
    const el = document.createElement('div');
    el.className = 'draft-dot';
    this.draft = new this.k.CustomOverlay({ map: this.map, position: new this.k.LatLng(lat, lng), content: el, xAnchor: 0.5, yAnchor: 0.5 });
  }
  clearDraft() {
    this.draft?.setMap(null);
    this.draft = null;
  }

  // 장소 검색: 지도 중심 근처 우선
  search(query) {
    return new Promise((resolve) => {
      this.places.keywordSearch(query, (data, status) => {
        if (status !== this.k.services.Status.OK) return resolve([]);
        resolve(data.slice(0, 6).map((d) => ({
          name: d.place_name, address: d.road_address_name || d.address_name, lat: Number(d.y), lng: Number(d.x),
        })));
      }, { location: this.map.getCenter() });
    });
  }
}
