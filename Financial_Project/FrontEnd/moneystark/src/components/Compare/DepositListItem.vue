<template>
  <div class="deposit-detail-container">
    <!-- 헤더 섹션 -->
    <header class="header">
      <button @click="$emit('back')" class="back-button">
        <i class="mdi mdi-arrow-left"></i>
        뒤로가기
      </button>
      <!-- 은행 로고 -->
      <img v-if="currentBank" :src="currentBank.logo" class="bank-logo" alt="은행 로고" />
    </header>

    <!-- 상품 정보 섹션 -->
    <section class="product-info">
      <h1>{{ deposit.fin_prdt_nm }}</h1>
      <h2>{{ deposit.kor_co_nm }}</h2>
      <div class="highest-rate">
        <span>
          최고 금리:
          <strong>{{ highestRate.toFixed(2) }}%</strong>
          <template v-if="highestRateTerm > 0"> ({{ highestRateTerm }}개월)</template>
        </span>
      </div>
      <div class="button-group">
        <button v-if="isLoggedIn" @click="joinProduct(deposit.id, depositAmount)" class="join-button">
          <i class="mdi mdi-account-check"></i>
          가입하기
        </button>
        <button @click="goToOfficialSite" class="official-site-button">
          <i class="mdi mdi-bank"></i>
          공식 홈페이지
        </button>
        <button @click="showNewsPopup" class="news-button">
          <i class="mdi mdi-newspaper"></i>
          관련 뉴스
        </button>
      </div>
    </section>

    <!-- 상품 안내 섹션 -->
    <section class="deposit-info">
      <h3>
        <i class="mdi mdi-information-outline"></i>
        상품 안내
      </h3>
      <div class="info-list">
        <div class="info-item">
          <span class="label">
            <i class="mdi mdi-login"></i>
            가입 방법
          </span>
          <span class="value">{{ deposit.join_way || "정보 없음" }}</span>
        </div>
        <div class="info-item">
          <span class="label">
            <i class="mdi mdi-star"></i>
            우대 조건
          </span>
          <span class="value">{{ deposit.spcl_cnd || "정보 없음" }}</span>
        </div>
        <div class="info-item">
          <span class="label">
            <i class="mdi mdi-alert-circle"></i>
            가입 제한
          </span>
          <span class="value">{{ deposit.join_deny || "정보 없음" }}</span>
        </div>
        <div class="info-item">
          <span class="label">
            <i class="mdi mdi-account-group"></i>
            가입 대상
          </span>
          <span class="value">{{ deposit.join_member || "정보 없음" }}</span>
        </div>
        <div class="info-item">
          <span class="label">
            <i class="mdi mdi-cash"></i>
            최고 한도
          </span>
          <span class="value">{{ deposit.max_limit || "제한 없음" }}</span>
        </div>
        <div class="info-item">
          <span class="label">
            <i class="mdi mdi-note-text"></i>
            기타 유의사항
          </span>
          <span class="value">{{ deposit.etc_note || "정보 없음" }}</span>
        </div>
      </div>
    </section>

    <!-- 금리 계산기 섹션 -->
    <section class="rate-calculator">
      <h3>
        <i class="mdi mdi-calculator"></i>
        이자 계산기
      </h3>
      <div class="calculator-form">
        <label for="depositAmount">
          <i class="mdi mdi-currency-krw"></i>
          예치 금액 (원)
        </label>
        <input type="number" id="depositAmount" v-model.number="depositAmount" @input="calculateInterest" placeholder="예: 10,000,000" />
        <div class="rate-buttons">
          <button :class="{ selected: selectedRateType === 'highest' }" @click="selectRate(highestRate, 'highest')">최고 우대금리 {{ highestRate.toFixed(2) }}% ({{ selectedTerm }}개월)</button>
          <button :class="{ selected: selectedRateType === 'basic' }" @click="selectRate(basicRate, 'basic')">기본금리 {{ basicRate.toFixed(2) }}% ({{ selectedTerm }}개월)</button>
        </div>
        <div v-if="selectedRate !== null" class="calculation-result">
          <p>
            예상 이자:
            <strong>{{ calculatedInterest.toLocaleString() }}원</strong>
          </p>
          <p>
            세전 총액:
            <strong>{{ (depositAmount + calculatedInterest).toLocaleString() }}원</strong>
          </p>
        </div>
      </div>
    </section>

    <!-- 금리 정보 테이블 -->
    <section class="rate-info">
      <h3>
        <i class="mdi mdi-chart-line"></i>
        금리 정보
      </h3>
      <table class="rate-table">
        <thead>
          <tr>
            <th>예치 기간 (개월)</th>
            <th>금리 유형</th>
            <th>기본 금리</th>
            <th>최고 우대 금리</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="option in deposit.options" :key="option.save_trm">
            <td>{{ option.save_trm }}</td>
            <td>{{ option.intr_rate_type_nm }}</td>
            <td>{{ option.intr_rate }}%</td>
            <td>{{ option.intr_rate2 || option.intr_rate }}%</td>
          </tr>
        </tbody>
      </table>
    </section>

    <!-- 뉴스 팝업 -->
    <div v-if="isNewsPopupVisible" class="news-popup-overlay">
      <div class="news-popup">
        <header class="news-popup-header">
          <h3>
            <i class="mdi mdi-newspaper"></i>
            관련 뉴스
          </h3>
          <button @click="closeNewsPopup" class="close-button">
            <i class="mdi mdi-close"></i>
          </button>
        </header>
        <div class="news-popup-body">
          <NewsView :query="newsQuery" @update:query="updateNewsQuery" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useDepositStore } from "@/stores/deposit";
import NewsView from "@/views/NewsView.vue";

const store = useDepositStore();
const props = defineProps({
  deposit: Object,
});

const isLoggedIn = ref(true); // 실제 로그인 상태에 따라 변경 필요
const depositAmount = ref(10000000); // 기본값: 1,000만원
const calculatedInterest = ref(0);
const selectedRate = ref(null);
const isNewsPopupVisible = ref(false);
const newsQuery = ref("");
const selectedRateType = ref("highest");

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
// highestRateData computed 속성 수정
const highestRateData = computed(() => {
  if (!props.deposit?.options?.length)
    return {
      rate: 0,
      term: 0,
      option: null,
    };

  const maxOption = [...props.deposit.options].reduce((max, curr) => {
    const maxRate = parseFloat(max.intr_rate2 || max.intr_rate);
    const currRate = parseFloat(curr.intr_rate2 || curr.intr_rate);

    if (maxRate === currRate) {
      return parseInt(curr.save_trm) < parseInt(max.save_trm) ? curr : max;
    }
    return currRate > maxRate ? curr : max;
  });

  return {
    rate: parseFloat(maxOption.intr_rate2 || maxOption.intr_rate),
    term: parseInt(maxOption.save_trm),
    option: maxOption,
  };
});

// 특정 기간의 기본금리 옵션 찾기
const findBasicRateForTerm = (term) => {
  return props.deposit.options.find((opt) => parseInt(opt.save_trm) === term);
};
const highestRate = computed(() => {
  if (!highestRateData.value) return 0;
  return parseFloat(highestRateData.value.rate);
});

// highestRateTerm computed 속성 수정
const highestRateTerm = computed(() => {
  if (!highestRateData.value || !highestRateData.value.term) return 0;
  return parseInt(highestRateData.value.term);
});

const basicOption = computed(() => {
  if (!selectedTerm.value || !props.deposit?.options) return null;

  // 최고금리 기간에 해당하는 기본금리 찾기
  return props.deposit.options.find((opt) => parseInt(opt.save_trm) === selectedTerm.value);
});

const basicRate = computed(() => {
  if (!basicOption.value) return 0;
  return parseFloat(basicOption.value.intr_rate);
});

const basicRateTerm = basicOption ? parseInt(basicOption.save_trm, 10) : highestRateTerm;

// 현재 은행 정보
const currentBank = computed(() => {
  return banks.value.find((bank) => bank.name === props.deposit.kor_co_nm);
});

const selectedTerm = computed(() => {
  if (!highestRateData.value) return null;
  return highestRateData.value.term;
});

const goToOfficialSite = () => {
  if (currentBank.value) {
    window.open(currentBank.value.url, "_blank");
  } else {
    alert("은행 공식 홈페이지 정보를 찾을 수 없습니다.");
  }
};

const joinProduct = async (productId, amount) => {
  await store.addDeposit(productId, amount);

  if (store.error) {
    alert(store.error);
  } else {
    alert("상품에 가입되었습니다.");
  }
};
// 이자 계산 함수 수정
const calculateInterest = () => {
  if (!selectedRate.value || !depositAmount.value || !selectedTerm.value) return;

  const rate = selectedRate.value;
  const term = selectedTerm.value;

  const annualRate = rate / 100;
  const years = term / 12;
  const interest = depositAmount.value * annualRate * years;

  calculatedInterest.value = Math.floor(interest);
};
// 금리 선택 함수 수정
// 금리 선택 함수 수정
const selectRate = (rate, type) => {
  selectedRate.value = rate;
  selectedRateType.value = type;
  calculateInterest();
};

const showNewsPopup = () => {
  newsQuery.value = `${props.deposit.kor_co_nm} ${props.deposit.fin_prdt_nm} 뉴스`;
  isNewsPopupVisible.value = true;
};

const closeNewsPopup = () => {
  isNewsPopupVisible.value = false;
};

const updateNewsQuery = (newQuery) => {
  newsQuery.value = newQuery;
};

// onMounted 함수도 수정
onMounted(() => {
  selectedRate.value = highestRate.value;
  selectedRateType.value = "highest";
  calculateInterest();
});
</script>

<style scoped>
/* 전체 컨테이너 스타일 */
.deposit-detail-container {
  max-width: 1200px;
  margin: 40px auto;
  padding: 20px;
  font-family: "Noto Sans KR", sans-serif;
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
}

/* 헤더 스타일 */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.back-button {
  background: none;
  border: none;
  color: #1890ff;
  font-size: 1.2rem;
  cursor: pointer;
}

.back-button:hover {
  text-decoration: underline;
}

.bank-logo {
  width: 120px;
  height: auto;
}

/* 상품 정보 섹션 스타일 */
.product-info {
  text-align: center;
  margin-bottom: 40px;
}

.product-info h1 {
  font-size: 2rem;
  color: #333;
  margin-bottom: 10px;
}

.product-info h2 {
  font-size: 1.5rem;
  color: #555;
  margin-bottom: 20px;
}

.highest-rate {
  font-size: 1.2rem;
  color: #ff4d4f;
  margin-bottom: 20px;
}

.button-group {
  display: flex;
  justify-content: center;
  gap: 15px;
}

.button-group button {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

.join-button {
  background-color: #1890ff;
  color: #fff;
}

.join-button:hover {
  background-color: #40a9ff;
}

.official-site-button {
  background-color: #52c41a;
  color: #fff;
}

.official-site-button:hover {
  background-color: #73d13d;
}

.news-button {
  background-color: #faad14;
  color: #fff;
}

.news-button:hover {
  background-color: #ffc53d;
}

/* 상품 안내 섹션 스타일 */
.deposit-info {
  margin-bottom: 40px;
}

.deposit-info h3 {
  font-size: 1.8rem;
  color: #333;
  margin-bottom: 20px;
}

.info-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.info-item {
  display: flex;
  padding: 15px;
  background-color: #fafafa;
  border-radius: 8px;
}

.info-item .label {
  flex: 1;
  font-weight: bold;
  color: #555;
}

.info-item .value {
  flex: 2;
  color: #777;
}

/* 금리 계산기 섹션 스타일 */
.rate-calculator {
  margin-bottom: 40px;
}

.rate-calculator h3 {
  font-size: 1.8rem;
  color: #333;
  margin-bottom: 20px;
}

.calculator-form {
  max-width: 500px;
  margin: 0 auto;
}

.calculator-form label {
  display: block;
  font-size: 1rem;
  color: #555;
  margin-bottom: 8px;
}

.calculator-form input {
  width: 100%;
  padding: 10px;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 5px;
  margin-bottom: 20px;
}

.rate-buttons {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.rate-buttons button {
  flex: 1;
  padding: 12px;
  background-color: #f0f0f0;
  color: #555;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.rate-buttons button.selected {
  background-color: #1890ff;
  color: #fff;
}

.rate-buttons button:hover {
  background-color: #e6f7ff;
}

.calculation-result {
  text-align: center;
  font-size: 1.2rem;
  color: #333;
}

/* 금리 정보 테이블 스타일 */
.rate-info h3 {
  font-size: 1.8rem;
  color: #333;
  margin-bottom: 20px;
}

.rate-table {
  width: 100%;
  border-collapse: collapse;
}

.rate-table th,
.rate-table td {
  padding: 12px;
  text-align: center;
  border: 1px solid #eee;
}

.rate-table th {
  background-color: #fafafa;
  font-weight: bold;
  color: #555;
}

.rate-table tr:hover {
  background-color: #f9f9f9;
}
.news-popup-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.news-popup {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 90%;
  max-width: 800px;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
  animation: popup-fade 0.3s ease-out;
}

.news-popup-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid #eee;
}

.news-popup-header h3 {
  margin: 0;
  font-size: 1.25rem;
  color: #333;
}

.close-button {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #666;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.close-button:hover {
  background-color: #f5f5f5;
}

.news-popup-body {
  padding: 20px;
  overflow-y: auto;
  flex: 1;
}

@keyframes popup-fade {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .button-group {
    flex-direction: column;
    gap: 10px;
  }

  .rate-buttons {
    flex-direction: column;
  }

  .calculator-form {
    width: 100%;
  }
}

.header .back-button i,
.button-group button i,
section h3 i {
  margin-right: 8px;
}

.button-group button i {
  font-size: 1.2rem;
}

section h3 i {
  color: #1890ff;
}

.close-button i {
  font-size: 24px;
}

.info-item .label i {
  margin-right: 5px;
  color: #1890ff;
}

/* 아이콘 스타일 추가 */
.info-item .label i {
  width: 24px;
  font-size: 1.2rem;
  margin-right: 8px;
  color: #1890ff;
  vertical-align: middle;
}

.info-item {
  transition: all 0.3s ease;
  border-left: 4px solid transparent;
}

.info-item:hover {
  border-left-color: #1890ff;
  background-color: #f0f7ff;
  transform: translateX(5px);
}

section h3 i {
  font-size: 1.5rem;
  margin-right: 10px;
  color: #1890ff;
  vertical-align: middle;
}

.calculator-form label i {
  color: #1890ff;
  margin-right: 5px;
}

/* 애니메이션 효과 */
.info-item {
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}
</style>
