<template>
  <div class="map-container">
    <div class="search-section">
      <form @submit.prevent="handleSearch" class="search-form">
        <div class="search-box">
          <input type="text" v-model="searchPlace" placeholder="은행명 또는 지역을 검색하세요" class="search-input" />
          <button class="search-button">
            <i class="fas fa-search"></i>
          </button>
        </div>
        <p class="search-example">예시: 서울시 강남구 국민은행</p>
      </form>
    </div>

    <div class="content-wrapper">
      <div id="map" class="map-view"></div>

      <div class="results-section">
        <div v-if="searchResults.length > 0">
          <h3 class="results-title">
            "
            <span class="highlight">{{ searchPlaceSave }}</span>
            " 검색 결과
          </h3>
          <ul class="results-list">
            <li v-for="(place, index) in searchResults" :key="index" class="result-item">
              <h4>{{ place.place_name }}</h4>
              <p>{{ place.address_name }}</p>
            </li>
          </ul>
        </div>
        <div v-else class="no-results">
          <p>검색 결과가 없습니다</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from "vue";
import { useNaverMapStore } from "@/stores/naverMap";
// import { RouterLink,RouterView } from 'vue-router';

export default {
  name: "BankMapView",

  setup() {
    const mapStore = useNaverMapStore();
    const searchPlace = ref(mapStore.searchPlace);
    const searchResults = computed(() => mapStore.searchResults); // 검색 결과 가져오기
    const searchPlaceSave = ref("");
    console.log(searchResults);

    onMounted(() => {
      const API_KEY = "81ad137000a5ac27ad17632931b78e28"; // 카카오 API 키
      const script = document.createElement("script");
      script.src = `//dapi.kakao.com/v2/maps/sdk.js?appkey=${API_KEY}&autoload=false`;

      script.onload = () => {
        kakao.maps.load(mapStore.initMap);
      };

      document.body.appendChild(script);
    });

    const handleSearch = () => {
      mapStore.setSearchPlace(searchPlace.value); // 검색어 업데이트
      mapStore.keywordSearch(); // 검색 실행
      searchPlaceSave.value = searchPlace.value;
      searchPlace.value = ""; // 검색 후 검색어 초기화
      console.log(searchPlaceSave);
    };

    return {
      searchResults,
      searchPlace,
      handleSearch,
      searchPlaceSave,
    };
  },
};
</script>

<style scoped>
.map-container {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 0 1rem;
}

.search-section {
  margin-bottom: 2rem;
}

.search-form {
  max-width: 600px;
  margin: 0 auto;
}

.search-box {
  display: flex;
  gap: 0.5rem;
  background: white;
  border-radius: 50px;
  padding: 0.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.search-input {
  flex: 1;
  border: none;
  padding: 0.8rem 1.5rem;
  font-size: 1rem;
  border-radius: 25px;
  outline: none;
}

.search-button {
  background: #7700ff;
  color: white;
  border: none;
  padding: 0.8rem 1.5rem;
  border-radius: 25px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.search-button:hover {
  background: #6600cc;
}

.search-example {
  text-align: center;
  color: #666;
  font-size: 0.9rem;
  margin-top: 0.5rem;
}

.content-wrapper {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 2rem;
  margin-top: 2rem;
}

.map-view {
  width: 100%;
  height: 70vh;
  border-radius: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.results-section {
  background: white;
  border-radius: 20px;
  padding: 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  height: 70vh;
  overflow-y: auto;
}

.results-title {
  color: #333;
  margin-bottom: 1rem;
  font-size: 1.2rem;
}

.highlight {
  color: #7700ff;
  font-weight: bold;
}

.results-list {
  list-style: none;
  padding: 0;
}

.result-item {
  padding: 1rem;
  border-radius: 10px;
  background: #f8f9fa;
  margin-bottom: 1rem;
  transition: transform 0.2s ease;
}

.result-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.result-item h4 {
  color: #333;
  margin: 0 0 0.5rem 0;
}

.result-item p {
  color: #666;
  margin: 0;
  font-size: 0.9rem;
}

.no-results {
  text-align: center;
  color: #666;
  padding: 2rem;
}

@media (max-width: 768px) {
  .content-wrapper {
    grid-template-columns: 1fr;
  }

  .map-view {
    height: 50vh;
  }

  .results-section {
    height: auto;
    max-height: 50vh;
  }
}
</style>
