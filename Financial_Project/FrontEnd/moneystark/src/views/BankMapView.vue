<template>
  <div class="map-container">
    <div class="search-section">
      <h4 class="do-hyeon-regular">은행을 검색해 보세요!</h4>
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
          <!-- 은행 선택 -->
          <select v-model="selectedBank" id="bank" class="form-control select-input">
            <option value="">은행을 선택하세요</option>
            <option v-for="bank in banks" :key="bank" :value="bank.name">{{ bank.name }}</option>
          </select>

          <!-- 추가 검색어 입력 -->
          <!-- <input type="text" v-model="searchPlaceInput" placeholder="은행명을 입력하세요" class="search-input" /> -->

          <button class="search-button">
            <i class="fas fa-search"></i>
          </button>
        </div>
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
import { useProductStore} from "@/stores/product"
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
    const banks = ref([
  { name: "우리은행", url: "https://www.wooribank.com", logo: "https://simg.wooribank.com/img/intro/header/h1_01.png" },
  { name: "한국스탠다드차타드은행", url: "https://www.standardchartered.co.kr", logo: "https://www.standardchartered.co.kr/np/assets/images/kr/base/chb_log_reb.png" },
  { name: "아이엠뱅크", url: "https://www.imbank.co.kr/dgb_ebz_main.jsp", logo: "https://www.imbank.co.kr/img/common/main/ebz_top_dgb_logo_up.png?v=20240607" },
  { name: "부산은행", url: "https://www.busanbank.co.kr", logo: "https://blog.kakaocdn.net/dn/18TFu/btqyWKDIInm/GfE8079nzAF9txBlV71XS0/img.jpg" },
  { name: "광주은행", url: "https://www.kjbank.com", logo: "https://imgs.kjbank.com/resource/img/common/logo.png" },
  { name: "제주은행", url: "https://www.jejubank.co.kr", logo: "https://i.namu.wiki/i/DLhrLR38bUexuN_K8jiwwCqAo5gi2nEc7NmDI_MabOpop-ZWaI0G3KYRmjqyf8-7Crc0rv047buDbEChYyFqcQ.svg" },
  { name: "전북은행", url: "https://www.jbbank.co.kr/", logo: "https://www.jbbank.co.kr/img/common/renew-logo.png" },
  { name: "경남은행", url: "https://www.knbank.com", logo: "https://i.namu.wiki/i/dw9S4Oh4zaH3jLwxF8JixDMrQ36XQAJOTBMu0C4sLZ6f6NERx8dnsb5_sCY0DOHF4SuuNOJ7lLe4H1DfNyZjsQ.svg" },
  { name: "중소기업은행", url: "https://www.ibk.co.kr", logo: "https://www.ibk.co.kr/img/navigation/h1_logo_sub.gif" },
  { name: "한국산업은행", url: "https://www.kdb.co.kr", logo: "https://blog.kakaocdn.net/dn/SMJ1N/btqDjHIMQ0r/jAKsKJ2lT2XhGiEIsvZGN0/img.jpg" },
  { name: "국민은행", url: "https://www.kbstar.com", logo: "https://blog.kakaocdn.net/dn/bYyqeR/btqwFAWAKWf/wXPLrundPBKPrhtXgr0Iv1/img.jpg" },
  { name: "신한은행", url: "https://www.shinhan.com", logo: "https://i.namu.wiki/i/Etmt-wojOBWr5gVcPR0qrTxuej558yfzzyYr0xXYSxljpLuEdPWGSPi-aPdJHQrpZY2o7zvuUMb4PE6PvFjQ3Q.svg" },
  { name: "농협은행주식회사", url: "https://www.nonghyup.com", logo: "https://blog.kakaocdn.net/dn/bDOvRh/btqyXx4zjvs/gb3v21tHkeCYrozbCH0AYk/img.jpg" },
  { name: "하나은행", url: "https://www.kebhana.com", logo: "https://image.kebhana.com/cont/common/img/newmain2021/logo.png" },
  { name: "주식회사 케이뱅크", url: "https://www.kbanknow.com", logo: "https://www.kbanknow.com/resource/img/reform/layout/logo_kbank.png" },
  { name: "수협은행", url: "https://suhyup-bank.com", logo: "https://suhyup-bank.com/images/sub_new_main/img_logo.png" },
  { name: "한국씨티은행", url: "https://www.citibank.co.kr", logo: "https://i.namu.wiki/i/MejG2B28te9lfxBlpdWqCguVOnCa6zvyxJrf2u4KamJ7l8lXOG3rCMUyURui3PZhNbcH4aA6CKQK0JMbRjb8kQ.svg" },
  { name: "주식회사 카카오뱅크", url: "https://www.kakaobank.com", logo: "https://i.namu.wiki/i/tcO6LsmBe-rB-laaABweXNy9TaTU1fruiJaYVH39cCCZzg054tDwfbSmzsOvDU_zVZCJZzPS_YRe7vdgED3xQA.svg" },
  { name: "토스뱅크 주식회사", url: "https://www.tossbank.com", logo: "https://static.toss.im/icons/png/4x/logo-bank-blue.png" },
]);
    const mapStore = useNaverMapStore();
    const searchPlace = ref(mapStore.searchPlace);
    const searchResults = computed(() => mapStore.searchResults); // 검색 결과 가져오기
    const searchPlaceSave = ref("");
    const selectedBank = ref("");
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
      searchPlace.value = selectedCity.value + selectedDistrict.value + selectedBank.value;
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
      // searchPlaceInput,
      banks,
      // bankSet,
      selectedBank
    };
  },
};
</script>

<style scoped>
.select-input {
  margin-left: 20px; /* 왼쪽 여백 */
  padding: 12px 16px; /* 내부 여백 */
  font-size: 16px; /* 글자 크기 */
  color: #17bebb; /* 텍스트 색상 */
  border: 2px solid #17bebb; /* 테두리 색상 */
  border-radius: 10px; /* 둥근 모서리 */
  background-color: white; /* 배경색 흰색 */
  outline: none; /* 포커스 시 기본 외곽선 제거 */
  transition: all 0.3s ease; /* 부드러운 애니메이션 */
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* 살짝 그림자 */
  appearance: none; /* 기본 드롭다운 화살표 제거 */
  -webkit-appearance: none;
  -moz-appearance: none;
}

/* 포커스 시 스타일 */
.select-input:focus {
  border-color: #17bebb; /* 포커스 시 테두리 색상 유지 */
  box-shadow: 0 0 10px rgba(23, 190, 187, 0.5); /* 포커스 시 그림자 강조 */
}

/* 비활성화 상태 */
.select-input:disabled {
  background-color: #f2f2f2; /* 비활성화 시 배경색 */
  color: #999; /* 비활성화 시 텍스트 색상 */
  cursor: not-allowed; /* 비활성화 시 커서 */
  border-color: #ccc; /* 비활성화 시 테두리 색상 */
}

/* 드롭다운 화살표 커스터마이즈 */
.select-input {
  background-image: url("data:image/svg+xml;charset=UTF-8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 4 5'%3E%3Cpath fill='%2317bebb' d='M2 0L0 2h4z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 10px center; /* 드롭다운 화살표 위치 */
  background-size: 10px;
}

/* 호버 효과 */
.select-input:hover {
  border-color: #15a8a3; /* 테두리 색상 조금 어둡게 */
  box-shadow: 0 0 8px rgba(23, 190, 187, 0.5); /* 호버 시 그림자 */
  cursor: pointer; /* 포인터 커서 */
}

.map-container {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 0 1rem;
}

.search-section {
  margin-bottom: 2rem;
}

.search-form {
  max-width: 800px;
  margin: 0 auto;
}

.search-box {
  display: flex;
  gap: 0.5rem;
  background: white;
  border-radius: 50px;
  padding: 0.5rem;
  width: 100%;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.search-input {
  flex: 1;
  border: none;
  margin-left: 20px;
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
.do-hyeon-regular {
  text-align: center;
  font-family: 'Do Hyeon', sans-serif; /* 구글 폰트 'Do Hyeon' 적용 */
  font-weight: 400; /* 기본 굵기 */
  font-style: normal; /* 기본 스타일 */
}

</style>
