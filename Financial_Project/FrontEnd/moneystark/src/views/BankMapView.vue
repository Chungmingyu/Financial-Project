<template>
  <div class="map-container">
    <div class="search-section">
      <form @submit.prevent="handleSearch" class="search-form">
        <div class="search-box">
          <!-- 시/도 선택 -->
          <select v-model="selectedCity" class="select-input">
            <option value="" disabled>시/도를 선택하세요</option>
            <option v-for="city in cities" :key="city" :value="city">{{ city }}</option>
          </select>
          <!-- <input type="text" v-model="searchPlace" placeholder="은행명 또는 지역을 검색하세요" class="search-input" /> -->
          <!-- 구/동 선택 -->
          <select v-model="selectedDistrict" class="select-input" :disabled="!selectedCity">
            <option value="" disabled>구/동을 선택하세요</option>
            <option v-for="district in districts[selectedCity] || []" :key="district" :value="district">
              {{ district }}
            </option>
          </select>

          <!-- 추가 검색어 입력 -->
          <input type="text" v-model="searchPlaceInput" placeholder="은행명을 입력하세요" class="search-input" />

          <button class="search-button">
            <i class="fas fa-search"></i>
          </button>
        </div>
        <p class="search-example">예시: 서울특별시 강남구 국민은행</p>
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
    const cities = ref([
      "서울특별시",
      "부산광역시",
      "대구광역시",
      "인천광역시",
      "광주광역시",
      "대전광역시",
      "울산광역시",
      "세종특별자치시",
      "경기도",
      "강원도",
      "충청북도",
      "충청남도",
      "전라북도",
      "전라남도",
      "경상북도",
      "경상남도",
      "제주특별자치도",
    ]);

    const districts = ref({
      서울특별시: [
        "강남구",
        "강동구",
        "강북구",
        "강서구",
        "관악구",
        "광진구",
        "구로구",
        "금천구",
        "노원구",
        "도봉구",
        "동대문구",
        "동작구",
        "마포구",
        "서대문구",
        "서초구",
        "성동구",
        "성북구",
        "송파구",
        "양천구",
        "영등포구",
        "용산구",
        "은평구",
        "종로구",
        "중구",
        "중랑구",
      ],
      부산광역시: ["강서구", "금정구", "기장군", "남구", "동구", "동래구", "부산진구", "북구", "사상구", "사하구", "서구", "수영구", "연제구", "영도구", "중구", "해운대구"],
      대구광역시: ["남구", "달서구", "달성군", "동구", "북구", "서구", "수성구", "중구"],
      인천광역시: ["강화군", "계양구", "미추홀구", "남동구", "동구", "부평구", "서구", "연수구", "옹진군", "중구"],
      광주광역시: ["광산구", "남구", "동구", "북구", "서구"],
      대전광역시: ["대덕구", "동구", "서구", "유성구", "중구"],
      울산광역시: ["남구", "동구", "북구", "울주군", "중구"],
      세종특별자치시: ["전체"],
      경기도: [
        "가평군",
        "고양시",
        "과천시",
        "광명시",
        "광주시",
        "구리시",
        "군포시",
        "김포시",
        "남양주시",
        "동두천시",
        "부천시",
        "성남시",
        "수원시",
        "시흥시",
        "안산시",
        "안성시",
        "안양시",
        "양주시",
        "양평군",
        "여주시",
        "연천군",
        "오산시",
        "용인시",
        "의왕시",
        "의정부시",
        "이천시",
        "파주시",
        "평택시",
        "포천시",
        "하남시",
        "화성시",
      ],
      강원도: ["강릉시", "고성군", "동해시", "삼척시", "속초시", "양구군", "양양군", "영월군", "원주시", "인제군", "정선군", "철원군", "춘천시", "태백시", "평창군", "홍천군", "화천군", "횡성군"],
      충청북도: ["괴산군", "단양군", "보은군", "영동군", "옥천군", "음성군", "제천시", "진천군", "청주시", "충주시"],
      충청남도: ["계룡시", "공주시", "금산군", "논산시", "당진시", "보령시", "부여군", "서산시", "서천군", "아산시", "연기군", "예산군", "천안시", "청양군", "태안군", "홍성군"],
      전라북도: ["고창군", "군산시", "김제시", "남원시", "무주군", "부안군", "순창군", "완주군", "익산시", "임실군", "장수군", "전주시", "정읍시", "진안군"],
      전라남도: [
        "강진군",
        "고흥군",
        "곡성군",
        "광양시",
        "구례군",
        "나주시",
        "담양군",
        "목포시",
        "무안군",
        "보성군",
        "순천시",
        "신안군",
        "여수시",
        "영광군",
        "영암군",
        "완도군",
        "장성군",
        "장흥군",
        "진도군",
        "함평군",
        "해남군",
        "화순군",
      ],
      경상북도: [
        "경산시",
        "경주시",
        "고령군",
        "구미시",
        "군위군",
        "김천시",
        "문경시",
        "봉화군",
        "상주시",
        "성주군",
        "안동시",
        "영덕군",
        "영양군",
        "영주시",
        "영천시",
        "예천군",
        "울릉군",
        "울진군",
        "의성군",
        "청도군",
        "청송군",
        "칠곡군",
        "포항시",
      ],
      경상남도: ["거제시", "거창군", "고성군", "김해시", "남해군", "밀양시", "사천시", "산청군", "양산시", "의령군", "진주시", "창녕군", "창원시", "통영시", "하동군", "함안군", "함양군", "합천군"],
      제주특별자치도: ["서귀포시", "제주시"],
    });

    const mapStore = useNaverMapStore();
    const searchPlace = ref(mapStore.searchPlace);
    const searchResults = computed(() => mapStore.searchResults); // 검색 결과 가져오기
    const searchPlaceSave = ref("");
    const searchPlaceInput = ref("");
    const selectedCity = ref("");
    const selectedDistrict = ref("");
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
      searchPlace.value = selectedCity.value + selectedDistrict.value + searchPlaceInput.value;
      console.log(searchPlace.value);
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
      cities,
      districts,
      selectedCity,
      selectedDistrict,
      searchPlaceInput,
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
  background: #ffbf00;
  color: white;
  border: none;
  padding: 0.8rem 1.5rem;
  border-radius: 25px;
  cursor: pointer;
  transition: background 0.3s ease;
}

.search-button:hover {
  background: #e6ac00;
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
  color: #ffbf00;
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
