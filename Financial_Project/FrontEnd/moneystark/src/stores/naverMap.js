import { defineStore } from 'pinia';

export const useNaverMapStore = defineStore('naverMap', {
  state: () => ({
    searchPlace: '', // 검색어
    map: null, // 지도 객체
    infowindow: null, // 인포윈도우
    placesService: null, // 장소 검색 서비스
    markers: [], // 지도에 표시된 마커들을 배열로 관리
    searchResults: []
  }),

  actions: {

    // 지도 초기화
    initMap() {
      const infowindow = new kakao.maps.InfoWindow({ zIndex: 1 });
      var ps = new kakao.maps.services.Places()
      const mapContainer = document.getElementById('map');
      const mapOption = {
        center: new kakao.maps.LatLng(37.566826, 126.9786567), // 기본 중심 좌표
        level: 3 // 확대 레벨
      };

      this.map = new kakao.maps.Map(mapContainer, mapOption);
      this.infowindow = infowindow;
      this.placesService = new kakao.maps.services.Places();
    },
    // 키워드로 장소 검색하고 목록으로 표출하기

    // 키워드로 장소 검색
    keywordSearch() {
        console.log('키워드서치')
      if (this.searchPlace.trim() === '') {
        alert('검색어를 입력해주세요.');
        return;
      }

      // 이전에 생성된 마커들을 모두 제거
      this.clearMarkers();

      this.placesService.keywordSearch(this.searchPlace, (data, status) => {
        console.log(data)
        if (status === kakao.maps.services.Status.OK) {
          const bounds = new kakao.maps.LatLngBounds();
          this.searchResults = data; // 검색 결과 저장
          for (let i = 0; i < data.length; i++) {
            this.displayMarker(data[i], bounds);
          }
          this.map.setBounds(bounds);
        } else {
          alert('검색 결과가 없습니다.');
        }
      });
    },

    // 마커 표시
    displayMarker(place, bounds) {
      const marker = new kakao.maps.Marker({
        map: this.map,
        position: new kakao.maps.LatLng(place.y, place.x)
      });

      // 마커 클릭 시 인포윈도우 표시
      kakao.maps.event.addListener(marker, 'click', () => {
        this.infowindow.setContent(`<div style="padding:5px;font-size:12px;">${place.place_name}</div>`);
        this.infowindow.open(this.map, marker);
      });

      // 마커를 배열에 추가
      this.markers.push(marker);

      // bounds 객체에 좌표 추가
      bounds.extend(new kakao.maps.LatLng(place.y, place.x));
    },

    // 마커 초기화
    clearMarkers() {
      // 현재 지도에 표시된 마커들을 모두 제거
      for (let i = 0; i < this.markers.length; i++) {
        this.markers[i].setMap(null);
      }
      // 마커 배열 초기화
      this.markers = [];
    },

    // 검색어 업데이트
    setSearchPlace(place) {
      this.searchPlace = place;
    },

    // 검색어 초기화
    clearSearchPlace() {
      this.searchPlace = ''; // 검색어 초기화
    }
  }
});