<template>
  <div class="container">
    <!-- 상단 섹션 -->
    <div class="top-section">
      <div class="header">
        <button @click="$emit('back')" class="back-button">뒤로가기</button>
        <!-- 은행 로고를 조건에 맞게 표시 -->
        <img v-if="currentBank" :src="currentBank.logo" class="bank-icon" />
      </div>
      <h2>{{ saving.kor_co_nm }} - {{ saving.fin_prdt_nm }}</h2>
      <div class="highest-rate">
        <span>최고 금리: {{ highestRate }}% ({{ highestRateTerm }}개월)</span>
      </div>
      <div class="button-group">
        <button v-if="isLoggedIn" @click="joinProduct(saving.id, savingAmount)" class="join-button">가입하기</button>
        <button @click="goToOfficialSite" class="official-site-button">공식 홈에서 알아보기</button>
        <button @click="showNewsPopup" class="news-button">관련 뉴스 보기</button>
      </div>
    </div>

    <!-- 하단 섹션 -->
    <div class="bottom-section">
      <div class="saving-info">
        <h3>상품 안내</h3>
        <hr />
        <div class="info-item">
          <span class="label">가입 방법</span>
          <span class="value">{{ saving.join_way }}</span>
        </div>
        <div class="info-item">
          <span class="label">우대조건</span>
          <span class="value">{{ saving.spcl_cnd }}</span>
        </div>
        <div class="info-item">
          <span class="label">가입제한</span>
          <span class="value">{{ saving.join_deny }}</span>
        </div>
        <div class="info-item">
          <span class="label">가입대상</span>
          <span class="value">{{ saving.join_member }}</span>
        </div>
        <div class="info-item">
          <span class="label">기타 유의사항</span>
          <span class="value">{{ saving.etc_note }}</span>
        </div>
        <div class="info-item">
          <span class="label">최고한도</span>
          <span class="value">{{ saving.max_limit }}</span>
        </div>
        <div v-if="isNewsPopupVisible" class="news-popup">
          <NewsView :query="newsQuery" @update:query="updateNewsQuery" />
          <button @click="closeNewsPopup" class="close-popup-button">닫기</button>
        </div>
      </div>

      <!-- 금리 안내 섹션 -->
      <div class="rate-info">
        <h3>금리 안내</h3>
        <p>12개월 만기 시 받을 이자</p>
        <label for="savingAmount">월 예치금액 (원):</label>
        <input type="number" id="savingAmount" v-model.number="savingAmount" @input="calculateInterest" />
        <p>월 예치금액: {{ (savingAmount / 10000).toLocaleString() }}만원</p>
        <div class="rate-buttons">
          <button :class="{ selected: selectedRate === highestRate }" @click="selectRate(highestRate)">최고 금리: {{ highestRate }}%</button>
          <button :class="{ selected: selectedRate === basicRate }" @click="selectRate(basicRate)">기본 금리: {{ basicRate }}%</button>
        </div>
        <div v-if="selectedRate !== null">
          <p>원금: {{ (savingAmount * 12).toLocaleString() }}원</p>
          <p>이자: {{ calculatedInterest.toLocaleString() }}원</p>
          <p>총 합: {{ (savingAmount * 12 + calculatedInterest).toLocaleString() }}원</p>
          <small>유의 사항: 세전</small>
        </div>
      </div>

      <!-- 금리 정보 테이블 -->
      <table class="table table-striped">
        <thead>
          <tr>
            <th scope="col">개월 수</th>
            <th scope="col">금리 유형</th>
            <th scope="col">금리 유형명</th>
            <th scope="col">적립 유형</th>
            <th scope="col">적립 유형명</th>
            <th scope="col">금리</th>
            <th scope="col">최고 우대금리</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="option in saving.options" :key="option.save_trm">
            <td>{{ option.save_trm }}개월</td>
            <td>{{ option.intr_rate_type }}</td>
            <td>{{ option.intr_rate_type_nm }}</td>
            <td>{{ option.rsrv_type }}</td>
            <td>{{ option.rsrv_type_nm }}</td>
            <td>{{ option.intr_rate }}%</td>
            <td>{{ option.intr_rate2 }}%</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useDepositStore } from "@/stores/deposit";
import NewsView from "@/views/NewsView.vue"; // NewsView 컴포넌트 import

const store = useDepositStore();
const props = defineProps({
  saving: Object,
});

const isLoggedIn = ref(true); // 로그인 상태를 나타내는 변수 (예시로 true로 설정)
const savingAmount = ref(props.saving.max_limit && props.saving.max_limit !== "없음" ? parseInt(props.saving.max_limit.replace(/[^0-9]/g, "")) : 100000); // 최고한도 또는 기본값 10만원
const calculatedInterest = ref(null);
const selectedRate = ref(null);
const isNewsPopupVisible = ref(false); // 뉴스 팝업 상태 변수
const newsQuery = ref(""); // 뉴스 검색어

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

const highestRate = Math.max(...props.saving.options.map((option) => option.intr_rate2));
const highestRateTerm = props.saving.options.find((option) => option.intr_rate2 === highestRate).save_trm;
const basicRate = props.saving.options.find((option) => option.save_trm === 12).intr_rate;

const currentBank = computed(() => {
  return banks.value.find((bank) => bank.name === props.saving.kor_co_nm);
});

const goToOfficialSite = () => {
  if (currentBank.value) {
    window.open(currentBank.value.url, "_blank");
  }
};

const joinProduct = async (productData, savingAmount) => {
  // 가입한 상품 목록에 상품 ID 추가 로직
  await store.addSaving(productData, savingAmount);

  if (store.error) {
    alert(store.error);
  } else {
    console.log(`상품 ID ${props.saving.id}가 가입한 상품 목록에 추가되었습니다.`);
  }
};

const calculateInterest = () => {
  let totalInterest = 0;
  for (let month = 1; month <= 12; month++) {
    const remainingMonths = 12 - (month - 1);
    const interest = (savingAmount.value * selectedRate.value * remainingMonths) / 1200;
    totalInterest += interest;
  }
  calculatedInterest.value = totalInterest;
};

const selectRate = (rate) => {
  selectedRate.value = rate;
  calculateInterest();
};

const showNewsPopup = () => {
  newsQuery.value = `${props.saving.kor_co_nm} - ${props.saving.fin_prdt_nm} 뉴스`;
  isNewsPopupVisible.value = true;
};

const closeNewsPopup = () => {
  isNewsPopupVisible.value = false;
};

const updateNewsQuery = (newQuery) => {
  newsQuery.value = newQuery;
};

onMounted(() => {
  selectedRate.value = highestRate;
  calculateInterest();
});
</script>

<style scoped>
.news-popup {
  position: fixed;
  top: 60%; /* 팝업을 살짝 아래로 내림 */
  left: 50%;
  transform: translate(-50%, -50%);
  width: 80%;
  max-width: 900px;
  background-color: white;
  border: 1px solid #ddd;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 20px;
  z-index: 1000;
}

.close-popup-button {
  display: block;
  margin: 20px auto 0;
  padding: 10px 20px;
  background-color: #000;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
}

.close-popup-button:hover {
  background-color: #333;
}

/* 전체 컨테이너 */
.container {
  width: 90%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 30px;
  border: 1px solid #ddd;
  border-radius: 12px;
  background-color: #fff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column; /* 수직 방향 정렬 */
  gap: 40px; /* 섹션 간 간격 */
  min-height: 1800px; /* 최소 높이 설정 */
}

/* 상단 섹션 */
.top-section {
  text-align: center; /* 중앙 정렬 */
  padding: 20px;
  border-bottom: 2px solid #ddd; /* 하단에 경계선 추가 */
}

.header {
  margin-bottom: 20px;
  display: flex; /* flex 레이아웃 사용 */
  justify-content: space-between; /* 양쪽 끝으로 정렬 */
  align-items: center; /* 수직 중앙 정렬 */
}

.back-button {
  background-color: #000; /* 검은색 배경 */
  color: white;
  border: none;
  border-radius: 8px;
  padding: 10px 20px;
  cursor: pointer;
  font-size: 16px;
}

.back-button:hover {
  background-color: #333;
}
.bank-icon {
  width: 100px;
  height: auto;
  margin-left: 20px;
}

h2 {
  font-size: 24px;
  color: #333;
  margin-bottom: 20px;
  font-weight: bolder;
}

.highest-rate {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 20px;
}

.button-group {
  display: flex;
  justify-content: center;
  gap: 10px;
}

.join-button {
  width: 220px;
  display: inline-block;
  margin: 20px;
  padding: 12px 24px;
  background-color: #000; /* 파란색 배경 */
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s;
}

.join-button:hover {
  background-color: #333;
}

.official-site-button {
  width: 220px;
  display: inline-block;
  margin: 20px;
  padding: 12px 24px;
  background-color: #000; /* 검은색 배경 */
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s;
}

.official-site-button:hover {
  background-color: #333;
}

.news-button {
  width: 220px;
  display: inline-block;
  margin: 20px;
  padding: 12px 24px;
  background-color: #ffbf00; /* 파란색 배경 */
  color: black;
  font-weight: bolder;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s;
}

/* 하단 섹션 */
.bottom-section {
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 12px;
}

.saving-info {
  margin-bottom: 40px;
}

.info-item {
  display: flex;
  justify-content: space-between;
  padding: 12px 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #fff;
  margin-bottom: 10px;
}

.label {
  font-weight: bold;
  color: #333;
  margin-right: 20px; /* label과 value 사이에 여백 추가 */
}

.value {
  color: #555;
  flex: 1; /* value가 남은 공간을 차지하도록 설정 */
  text-align: right; /* value를 오른쪽 정렬 */
}

/* 금리 안내 섹션 */
.rate-info {
  padding: 20px;
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.rate-info h3 {
  font-size: 24px;
  color: #333;
  margin-bottom: 20px;
  font-weight: bolder;
}

.rate-info p {
  font-size: 16px;
  color: #666;
  margin-bottom: 10px;
}

.rate-info label {
  font-size: 16px;
  color: #333;
  margin-right: 10px;
}

.rate-info input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
  margin-bottom: 20px;
}

.rate-buttons {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.rate-buttons button {
  flex: 1;
  padding: 12px 24px;
  background-color: #000;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s;
  margin-right: 10px;
}

.rate-buttons button.selected {
  background-color: #ffbf00;
  color: black;
}

.rate-buttons button:hover {
  background-color: #333;
}

.rate-buttons button:last-child {
  margin-right: 0;
}

/* 금리 정보 테이블 */
.table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  background-color: #fff;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  border-radius: 12px;
  overflow: hidden;
  margin-top: 40px; /* 테이블과 위 요소 사이에 여백 추가 */
}

.table th,
.table td {
  text-align: center;
  padding: 15px;
  border: 1px solid #ddd;
  font-size: 14px;
}

.table th {
  background-color: #ffbf00; /* 노란색 배경 */
  color: white;
}

.table td {
  background-color: #fffbe6; /* 연한 노란색 배경 */
}

.table tr:first-child th:first-child {
  border-top-left-radius: 12px;
}

.table tr:first-child th:last-child {
  border-top-right-radius: 12px;
}

.table tr:last-child td:first-child {
  border-bottom-left-radius: 12px;
}

.table tr:last-child td:last-child {
  border-bottom-right-radius: 12px;
}
</style>
