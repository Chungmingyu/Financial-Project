<template>
  <div class="deposit-detail-container">
    <!-- 헤더 섹션 -->
    <header class="header">
      <button @click="$emit('back')" class="back-button">← 뒤로가기</button>
      <!-- 은행 로고 -->
      <img v-if="currentBank" :src="currentBank.logo" class="bank-logo" alt="은행 로고" />
    </header>

    <!-- 상품 정보 섹션 -->
    <section class="product-info">
      <h1>{{ deposit.fin_prdt_nm }}</h1>
      <h2>{{ deposit.kor_co_nm }}</h2>
      <div class="highest-rate">
        <span>최고 금리: <strong>{{ highestRate.toFixed(2) }}%</strong> ({{ highestRateTerm }}개월)</span>
      </div>
      <div class="button-group">
        <button v-if="isLoggedIn" @click="joinProduct(deposit.id, depositAmount)" class="join-button">
          가입하기
        </button>
        <button @click="goToOfficialSite" class="official-site-button">공식 홈페이지</button>
        <button @click="showNewsPopup" class="news-button">관련 뉴스</button>
      </div>
    </section>

    <!-- 상품 안내 섹션 -->
    <section class="deposit-info">
      <h3>상품 안내</h3>
      <div class="info-list">
        <div class="info-item">
          <span class="label">가입 방법</span>
          <span class="value">{{ deposit.join_way || '정보 없음' }}</span>
        </div>
        <div class="info-item">
          <span class="label">우대 조건</span>
          <span class="value">{{ deposit.spcl_cnd || '정보 없음' }}</span>
        </div>
        <div class="info-item">
          <span class="label">가입 제한</span>
          <span class="value">{{ deposit.join_deny || '정보 없음' }}</span>
        </div>
        <div class="info-item">
          <span class="label">가입 대상</span>
          <span class="value">{{ deposit.join_member || '정보 없음' }}</span>
        </div>
        <div class="info-item">
          <span class="label">최고 한도</span>
          <span class="value">{{ deposit.max_limit || '제한 없음' }}</span>
        </div>
        <div class="info-item">
          <span class="label">기타 유의사항</span>
          <span class="value">{{ deposit.etc_note || '정보 없음' }}</span>
        </div>
      </div>
    </section>

    <!-- 금리 계산기 섹션 -->
    <section class="rate-calculator">
      <h3>이자 계산기</h3>
      <div class="calculator-form">
        <label for="depositAmount">예치 금액 (원)</label>
        <input
          type="number"
          id="depositAmount"
          v-model.number="depositAmount"
          @input="calculateInterest"
          placeholder="예: 10,000,000"
        />
        <div class="rate-buttons">
          <button
            :class="{ selected: selectedRate === highestRate }"
            @click="selectRate(highestRate)"
          >
            최고 금리 적용
          </button>
          <button
            :class="{ selected: selectedRate === basicRate }"
            @click="selectRate(basicRate)"
          >
            기본 금리 적용
          </button>
        </div>
        <div v-if="selectedRate !== null" class="calculation-result">
          <p>예상 이자: <strong>{{ calculatedInterest.toLocaleString() }}원</strong></p>
          <p>세전 총액: <strong>{{ (depositAmount + calculatedInterest).toLocaleString() }}원</strong></p>
        </div>
      </div>
    </section>

    <!-- 금리 정보 테이블 -->
    <section class="rate-info">
      <h3>금리 정보</h3>
      <table class="rate-table">
        <thead>
          <tr>
            <th>예치 기간 (개월)</th>
            <th>금리 유형</th>
            <th>금리</th>
            <th>최고 우대 금리</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="option in deposit.options" :key="option.save_trm">
            <td>{{ option.save_trm }}</td>
            <td>{{ option.intr_rate_type_nm }}</td>
            <td>{{ option.intr_rate }}%</td>
            <td>{{ option.intr_rate2 }}%</td>
          </tr>
        </tbody>
      </table>
    </section>

    <!-- 뉴스 팝업 -->
    <div v-if="isNewsPopupVisible" class="news-popup">
      <div class="news-popup-content">
        <NewsView :query="newsQuery" @update:query="updateNewsQuery" />
        <button @click="closeNewsPopup" class="close-popup-button">닫기</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useDepositStore } from '@/stores/deposit';
import NewsView from '@/views/NewsView.vue';

const store = useDepositStore();
const props = defineProps({
  deposit: Object,
});

const isLoggedIn = ref(true); // 실제 로그인 상태에 따라 변경 필요
const depositAmount = ref(10000000); // 기본값: 1,000만원
const calculatedInterest = ref(0);
const selectedRate = ref(null);
const isNewsPopupVisible = ref(false);
const newsQuery = ref('');

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

])
// 최고 금리 및 기간 계산
const highestRateData = computed(() => {
  const maxOption = props.deposit.options.reduce((prev, current) =>
    parseFloat(current.intr_rate2) > parseFloat(prev.intr_rate2) ? current : prev
  );
  return {
    rate: parseFloat(maxOption.intr_rate2),
    term: parseInt(maxOption.save_trm, 10),
  };
});

const highestRate = highestRateData.value.rate;
const highestRateTerm = highestRateData.value.term;

// 기본 금리 (예: 12개월 기준)
const basicOption = props.deposit.options.find(
  (option) => parseInt(option.save_trm, 10) === 12
);
const basicRate = basicOption ? parseFloat(basicOption.intr_rate) : highestRate;
const basicRateTerm = basicOption ? parseInt(basicOption.save_trm, 10) : highestRateTerm;

// 현재 은행 정보
const currentBank = computed(() => {
  return banks.value.find((bank) => bank.name === props.deposit.kor_co_nm);
});

const goToOfficialSite = () => {
  if (currentBank.value) {
    window.open(currentBank.value.url, '_blank');
  } else {
    alert('은행 공식 홈페이지 정보를 찾을 수 없습니다.');
  }
};

const joinProduct = async (productId, amount) => {
  await store.addDeposit(productId, amount);

  if (store.error) {
    alert(store.error);
  } else {
    alert('상품에 가입되었습니다.');
  }
};

const calculateInterest = () => {
  if (selectedRate.value !== null && depositAmount.value) {
    let term;
    if (selectedRate.value === highestRate) {
      term = highestRateTerm;
    } else if (selectedRate.value === basicRate) {
      term = basicRateTerm;
    } else {
      term = 12; // 기본값으로 12개월 사용
    }

    const interest = (depositAmount.value * selectedRate.value * term) / 1200;
    calculatedInterest.value = Math.floor(interest);
  }
};

const selectRate = (rate) => {
  selectedRate.value = rate;
  calculateInterest();
};

const showNewsPopup = () => {
  newsQuery.value = `${props.deposit.kor_co_nm} ${props.deposit.fin_prdt_nm}`;
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
/* 전체 컨테이너 스타일 */
.deposit-detail-container {
  max-width: 1200px;
  margin: 40px auto;
  padding: 20px;
  font-family: 'Noto Sans KR', sans-serif;
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

/* 뉴스 팝업 스타일 */
.news-popup {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.news-popup-content {
  background-color: #fff;
  width: 90%;
  max-width: 800px;
  padding: 20px;
  border-radius: 12px;
  position: relative;
}

.close-popup-button {
  position: absolute;
  top: 20px;
  right: 20px;
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
}

.close-popup-button:hover {
  color: #ff4d4f;
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
</style>
