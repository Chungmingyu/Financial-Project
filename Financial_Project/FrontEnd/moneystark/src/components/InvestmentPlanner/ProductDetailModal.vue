<template>
  <div class="deposit-detail-container">
    <!-- 헤더 섹션 (흰색 배경) -->
    <header class="white-header">
      <div class="header-content">
        <button @click="$emit('close')" class="back-button">
          <i class="mdi mdi-arrow-left"></i>
          뒤로가기
        </button>
        <img v-if="currentBank" :src="currentBank.logo" class="bank-logo" alt="은행 로고" />
      </div>
    </header>

    <!-- 상품 정보 섹션 (파란색 그라데이션 배경) -->
    <section class="product-info-section">
      <div class="product-title">
        <h1>{{ product.fin_prdt_nm }}</h1>
        <h2>{{ product.kor_co_nm }}</h2>
      </div>
      
      <div class="interest-rate">
        <span class="rate-label">최고 금리</span>
        <strong class="rate-value">{{ getMaxRate }}%</strong>
        <span v-if="selectedTerm" class="rate-term">({{ selectedTerm }}개월)</span>
      </div>

      <div class="action-buttons">
        <button class="primary-button">
          <i class="mdi mdi-check-circle"></i>
          선택하기
        </button>
        <button class="secondary-button" @click="goToOfficialSite">
          <i class="mdi mdi-bank"></i>
          공식 홈페이지
        </button>
        <button class="accent-button" @click="showNewsPopup">
          <i class="mdi mdi-newspaper"></i>
          관련 뉴스
        </button>
      </div>
    </section>

    <div class="modal-body custom-scrollbar">
      <!-- 상품 정보 카드 -->
      <section class="info-section">
        <h4>
          <i class="mdi mdi-information"></i>
          상품 정보
        </h4>
        <div class="info-grid">
          <div class="info-item">
            <i class="mdi mdi-calendar-range"></i>
            <div>
              <span class="label">가입기간</span>
              <p class="value">{{ product.save_trm || "기본 12"  }}개월</p>
            </div>
          </div>
          <div class="info-item">
            <i class="mdi mdi-account-group"></i>
            <div>
              <span class="label">가입대상</span>
              <p class="value">{{ product.join_member || "제한없음" }}</p>
            </div>
          </div>
          <div class="info-item">
            <i class="mdi mdi-currency-krw"></i>
            <div>
              <span class="label">최소 가입금액</span>
              <p class="value">{{ formatAmount(product.min_limit) || "제한없음" }}</p>
            </div>
          </div>
          <div class="info-item">
            <i class="mdi mdi-bank"></i>
            <div>
              <span class="label">가입방법</span>
              <p class="value">{{ product.join_way || "제한없음" }}</p>
            </div>
          </div>
        </div>
      </section>

      <!-- 금리 정보 테이블 -->
      <section class="rates-section">
        <h4>
          <i class="mdi mdi-percent"></i>
          금리 정보
        </h4>
        <div class="rates-table">
          <table>
            <thead>
              <tr>
                <th>가입기간</th>
                <th>기본금리</th>
                <th>우대금리</th>
                <th>최고금리</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="option in product.options" :key="option.save_trm">
                <td>{{ option.save_trm }}개월</td>
                <td>{{ option.intr_rate }}%</td>
                <td>{{ getPreferentialRate(option) }}%</td>
                <td class="highlight">{{ option.intr_rate2 || option.intr_rate }}%</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- 수익 계산기 -->
      <section class="calculator-section">
        <h4>
          <i class="mdi mdi-calculator"></i>
          수익 계산기
        </h4>
        <div class="calculator-content">
          <div class="input-group">
            <label>
              <i class="mdi mdi-currency-krw"></i>
              투자 금액
            </label>
            
          </div>
            <input type="number" v-model="calculatorAmount" min="0" step="10000" class="calculator-input" />
          <div class="input-group">
            <label>
              <i class="mdi mdi-calendar"></i>
              투자 기간
            </label>
            <select v-model="calculatorPeriod" class="calculator-select">
              <option v-for="option in product.options" :key="option.save_trm" :value="option.save_trm">{{ option.save_trm }}개월</option>
            </select>
          </div>
          <div class="calculation-results">
            <div class="result-item">
              <span class="label">만기 예상 금액</span>
              <strong class="value">{{ calculateExpectedAmount }}원</strong>
            </div>
            <div class="result-item highlight">
              <span class="label">예상 이자 수익</span>
              <strong class="value">{{ calculateInterestAmount }}원</strong>
            </div>
          </div>
        </div>
      </section>

      <!-- 가입 채널
      <section class="channels-section">
        <h4><i class="mdi mdi-bank-network"></i> 가입 채널</h4>
        <div class="channels-grid">
          <div v-for="(available, channel) in availableJoinWays" 
               :key="channel"
               :class="['channel-item', { available }]">
            <i :class="getChannelIcon(channel)"></i>
            <span>{{ getChannelName(channel) }}</span>
            <i class="status-icon" :class="available ? 'mdi mdi-check-circle' : 'mdi mdi-close-circle'"></i>
          </div>
        </div>
      </section> -->
    </div>

    <!-- 뉴스 팝업 개선 -->
    <Transition name="fade">
      <div v-if="isNewsPopupVisible" class="news-modal">
        <div class="news-container">
          <header class="news-header">
            <h3>
              <i class="mdi mdi-newspaper"></i>
              {{ product.fin_prdt_nm }} 관련 뉴스
            </h3>
            <button @click="closeNewsPopup" class="close-news">
              <i class="mdi mdi-close"></i>
            </button>
          </header>
          <div class="news-content">
            <NewsView :query="newsQuery" @update:query="updateNewsQuery" />
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script>
import { ref, computed, watch } from "vue";
import { BANK_INFO } from "@/constants/bankInfo";
import NewsView from "@/views/NewsView.vue";

export default {
  name: "ProductDetailModal",
  components: { NewsView },

  props: {
    product: {
      type: Object,
      required: true,
    },
  },

  setup(props, { emit }) {
    const calculatorAmount = ref(10000000);
    const calculatorPeriod = ref(props.product.options[0]?.save_trm || null);
    const isNewsPopupVisible = ref(false);
    const newsQuery = ref("");

    const currentBank = computed(() => {
      return BANK_INFO.find((bank) => bank.name === props.product.kor_co_nm);
    });

    const selectedTerm = computed(() => {
      const maxOption = props.product.options.reduce((max, curr) => {
        const maxRate = parseFloat(max.intr_rate2 || max.intr_rate);
        const currRate = parseFloat(curr.intr_rate2 || curr.intr_rate);
        return currRate > maxRate ? curr : max;
      });
      return maxOption.save_trm;
    });

    const getMaxRate = computed(() => {
      return props.product.options
        .reduce((max, opt) => {
          const rate = parseFloat(opt.intr_rate2 || opt.intr_rate);
          return Math.max(max, rate);
        }, 0)
        .toFixed(2);
    });

    // 메소드 정의
    const formatAmount = (amount) => {
      if (!amount) return "0";
      return new Intl.NumberFormat("ko-KR").format(amount);
    };

    const getChannelName = (channel) => {
      const names = {
        internet: "인터넷뱅킹",
        mobile: "모바일뱅킹",
        branch: "영업점",
        phone: "전화뱅킹",
      };
      return names[channel];
    };

    const getChannelIcon = (channel) => {
      const icons = {
        internet: "mdi mdi-web",
        mobile: "mdi mdi-cellphone",
        branch: "mdi mdi-store",
        phone: "mdi mdi-phone",
      };
      return icons[channel];
    };

    const getPreferentialRate = (option) => {
      if (!option.intr_rate2) return "-";
      return (option.intr_rate2 - option.intr_rate).toFixed(2);
    };

    const goToOfficialSite = () => {
      if (currentBank.value) {
        window.open(currentBank.value.url, "_blank");
      }
    };

    const showNewsPopup = () => {
      newsQuery.value = `${props.product.kor_co_nm} ${props.product.fin_prdt_nm} 뉴스`;
      isNewsPopupVisible.value = true;
    };

    const closeNewsPopup = () => {
      isNewsPopupVisible.value = false;
    };

    const updateNewsQuery = (newQuery) => {
      newsQuery.value = newQuery;
    };

    const calculateInterest = () => {
      if (!calculatorAmount.value || !calculatorPeriod.value) return 0;
      const option = props.product.options.find((opt) => opt.save_trm === calculatorPeriod.value);
      if (!option) return 0;

      const rate = option.intr_rate2 || option.intr_rate;
      const years = calculatorPeriod.value / 12;
      const interest = calculatorAmount.value * (rate / 100) * years;
      return Math.floor(interest);
    };

    watch([calculatorAmount, calculatorPeriod], () => {
      calculateInterest();
    });

    return {
      calculatorAmount,
      calculatorPeriod,
      currentBank,
      selectedTerm,
      getMaxRate,
      isNewsPopupVisible,
      newsQuery,
      formatAmount,
      getChannelName,
      getChannelIcon,
      getPreferentialRate,
      goToOfficialSite,
      showNewsPopup,
      closeNewsPopup,
      updateNewsQuery,
      calculateInterest,
    };
  },

  computed: {
    calculateExpectedAmount() {
      const interest = this.calculateInterest();
      return this.formatAmount(Math.round(this.calculatorAmount + interest));
    },

    calculateInterestAmount() {
      const interest = this.calculateInterest();
      return this.formatAmount(Math.round(interest));
    },
  },
};
</script>

<style scoped>
/* 기본 컨테이너 스타일 */
.deposit-detail-container {
  width: 100%;
  max-width: 900px;
  max-height: 90vh;
  background: white;
  border-radius: 1.25rem;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

/* 흰색 헤더 스타일 */
.white-header {
  background: white;
  padding: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.bank-logo {
  height: 40px;
  object-fit: contain;
}

.back-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #2563eb;
  font-weight: 500;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  border: none;
  background: transparent;
  transition: all 0.2s;
}

.back-button:hover {
  background: #e0f2fe;
}

/* 상품 정보 섹션 스타일 */
.product-info-section {
  background: linear-gradient(135deg, #2563eb, #3b82f6);
  padding: 2.5rem 2rem;
  color: white;
  text-align: center;
}

.product-title {
  margin-bottom: 1.5rem;
}

.product-title h1 {
  font-size: 1.75rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.product-title h2 {
  font-size: 1.25rem;
  opacity: 0.9;
}

.interest-rate {
  margin: 2rem 0;
  display: flex;
  align-items: baseline;
  justify-content: center;
  gap: 0.5rem;
}

.rate-label {
  font-size: 1.25rem;
}

.rate-value {
  font-size: 3rem;
  font-weight: 700;
  color: #fbbf24;
  text-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.rate-term {
  font-size: 1.25rem;
  opacity: 0.9;
}

/* 액션 버튼 스타일 */
.action-buttons {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-top: 2rem;
}

.action-buttons button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border-radius: 0.75rem;
  font-weight: 500;
  transition: all 0.2s;
  border: none;
}

.primary-button {
  background: #fbbf24;
  color: #1a202c;
}

.secondary-button {
  background: #10b981;
  color: white;
}

.accent-button {
  background: #8b5cf6;
  color: white;
}

.action-buttons button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* 뉴스 모달 스타일 */
.news-modal {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  z-index: 100;
  backdrop-filter: blur(4px);
}

.news-container {
  width: 100%;
  max-width: 800px;
  max-height: 80vh;
  background: white;
  border-radius: 1rem;
  overflow: hidden;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
}

.news-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  background: linear-gradient(135deg, #2563eb, #3b82f6);
  color: white;
}

.news-header h3 {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.25rem;
  font-weight: 600;
}

.close-news {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  padding: 0.5rem;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.2s;
}

.close-news:hover {
  background: rgba(255, 255, 255, 0.3);
}

.news-content {
  padding: 1.5rem;
  overflow-y: auto;
  max-height: calc(80vh - 4rem);
}

/* 커스텀 스크롤바 */
.custom-scrollbar {
  scrollbar-width: thin;
  scrollbar-color: #cbd5e0 #f1f5f9;
}

.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: #f1f5f9;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: #cbd5e0;
  border-radius: 3px;
}

/* DepositListItem의 스타일을 그대로 가져와서 사용 */
.deposit-detail-container {
  max-width: 900px;
  width: 100%;
  margin: 0;
  padding: 0;
  background-color: #ffffff;
  border-radius: 1rem;
  overflow: hidden;
}

.modal-body {
  padding: 2rem;
  overflow-y: auto;
}

.info-section {
  background: #f8fafc;
  border-radius: 1rem;
  padding: 1.5rem;
  margin-bottom: 2rem;
}

.info-section h4 {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.25rem;
  color: #1f2937;
  margin-bottom: 1.5rem;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: white;
  border-radius: 0.75rem;
  border: 1px solid #e5e7eb;
  transition: all 0.2s;
}

.info-item:hover {
  border-color: #2563eb;
  transform: translateY(-2px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.info-item i {
  font-size: 1.5rem;
  color: #2563eb;
}

.info-item .label {
  font-size: 0.875rem;
  color: #6b7280;
}

.info-item .value {
  font-weight: 500;
  color: #1f2937;
}

/* 금리 테이블 스타일링 */
.rates-section {
  margin-bottom: 2rem;
}

.rates-table {
  overflow-x: auto;
}

.rates-table table {
  width: 100%;
  border-collapse: collapse;
}

.rates-table th,
.rates-table td {
  padding: 1rem;
  text-align: center;
  border-bottom: 1px solid #e5e7eb;
}

.rates-table th {
  background: #f8fafc;
  font-weight: 500;
  color: #4b5563;
}

.rates-table td.highlight {
  color: #2563eb;
  font-weight: 600;
}

/* 계산기 섹션 스타일링 */
.calculator-section {
  background: #f8fafc;
  border-radius: 1rem;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.calculator-input,
.calculator-select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  font-size: 1rem;
  transition: all 0.2s;
}

.calculator-input:focus,
.calculator-select:focus {
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
  outline: none;
}

.calculation-results {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-top: 1.5rem;
  padding: 1rem;
  background: white;
  border-radius: 0.75rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.result-item {
  text-align: center;
}

.result-item .label {
  font-size: 0.875rem;
  color: #6b7280;
  margin-bottom: 0.5rem;
}

.result-item .value {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
}

.result-item.highlight .value {
  color: #2563eb;
  font-size: 1.5rem;
}

/* 채널 섹션 스타일링 */
.channels-section {
  margin-bottom: 2rem;
}

.channels-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
}

.channel-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  background: #f8fafc;
  border-radius: 0.75rem;
  border: 1px solid #e5e7eb;
  transition: all 0.2s;
}

.channel-item.available {
  background: #ecfdf5;
  border-color: #10b981;
}

.channel-item i {
  font-size: 1.25rem;
  color: #6b7280;
}

.channel-item.available i {
  color: #10b981;
}

.modal-wrapper {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1.5rem;
  z-index: 50;
  backdrop-filter: blur(4px);
}

.modal-content {
  width: 100%;
  max-width: 900px;
  max-height: 90vh;
  background: white;
  border-radius: 1rem;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.modal-body {
  flex: 1;
  overflow-y: auto;
  padding: 2rem;
  scrollbar-width: thin;
  scrollbar-color: #cbd5e0 #f1f5f9;
}

/* 스크롤��� 스타일링 */
.modal-body::-webkit-scrollbar {
  width: 8px;
}

.modal-body::-webkit-scrollbar-track {
  background: #f1f5f9;
  border-radius: 4px;
}

.modal-body::-webkit-scrollbar-thumb {
  background-color: #cbd5e0;
  border-radius: 4px;
}

/* 은행 로고 스타일링 */
.bank-logo {
  width: 120px;
  height: 40px;
  object-fit: contain;
  background: white;
  padding: 0.5rem;
  border-radius: 0.5rem;
}

.header {
  background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%);
  padding: 1.5rem;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.bank-logo {
  height: 40px;
  width: auto;
  max-width: 150px;
  object-fit: contain;
  background: white;
  padding: 0.5rem;
  border-radius: 0.5rem;
}

/* 버튼 스타일 재정의 */
.join-button {
  background-color: #2563eb !important;
}

.official-site-button {
  background-color: #059669 !important;
}

.news-button {
  background-color: #7c3aed !important;
}

.button-group button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* 계산기 섹션 스타일 개선 */
.calculator-section {
  background: #f8fafc;
  border-radius: 1rem;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.calculator-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.calculation-results {
  background: white;
  padding: 1.5rem;
  border-radius: 0.75rem;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

@media (max-width: 768px) {
  .action-buttons {
    flex-direction: column;
    padding: 0 1rem;
  }

  .product-name {
    font-size: 1.5rem;
  }

  .bank-name {
    font-size: 1.125rem;
  }

  .rate-value {
    font-size: 1.75rem;
  }
}
</style>
