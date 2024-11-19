<template>
    <div>
        <form @submit.prevent="handleSearch">
            <p>예시 : OO시 OO구 OO은행</p>
            <input type="text" v-model="searchPlace" placeholder="검색어를 입력하세요">
            <button>찾기</button>
        </form>
        <div id="map"></div>
    </div>
    <div>
        <div>
      <!-- 검색 결과 목록 -->
      <ul v-if="searchResults.length > 0" class="results-list">
          <p>"{{ searchPlaceSave }}" 검색 결과 입니다.</p>
        <li v-for="(place, index) in searchResults" :key="index">
          <strong>{{ place.place_name }}</strong><br />
          {{ place.address_name }}
        </li>
      </ul>
      <p v-else>검색 결과가 없습니다.</p>
    </div>
    </div>
    <!-- <RouterView/> -->
</template>

<script>
import { ref, onMounted, computed } from 'vue';
import { useNaverMapStore } from '@/stores/naverMap';
// import { RouterLink,RouterView } from 'vue-router';

export default {
  name: 'BankMapView',
  
  setup() {
    const mapStore = useNaverMapStore();
    const searchPlace = ref(mapStore.searchPlace);
    const searchResults = computed(() => mapStore.searchResults); // 검색 결과 가져오기
    const searchPlaceSave = ref('')
    console.log(searchResults)
    
    onMounted(() => {
      const API_KEY = '81ad137000a5ac27ad17632931b78e28'; // 카카오 API 키
      const script = document.createElement('script');
      script.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=${API_KEY}&autoload=false`;
  
      script.onload = () => {
        kakao.maps.load(mapStore.initMap);
      };
  
      document.body.appendChild(script);
    });

    const handleSearch = () => {
      mapStore.setSearchPlace(searchPlace.value); // 검색어 업데이트
      mapStore.keywordSearch(); // 검색 실행
      searchPlaceSave.value = searchPlace.value
      searchPlace.value = ''; // 검색 후 검색어 초기화
      console.log(searchPlaceSave)
    };

    return {
      searchResults,
      searchPlace,
      handleSearch,
      searchPlaceSave
    };
  }
};
</script>

<style scoped>
#map {
  width: 80%;
  height: 60vh;
}

.results-list {
  margin-top: 20px;
  padding: 0;
  list-style: none;
}

.results-list li {
  margin-bottom: 10px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: #f9f9f9;
}

.results-list li strong {
  color: #333;
}
</style>