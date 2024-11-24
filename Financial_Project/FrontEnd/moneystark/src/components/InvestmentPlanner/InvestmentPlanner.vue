<template>
  <div class="investment-planner">
    <div class="planner-container">
      <div class="page-title">
        <h1>
          <i class="mdi mdi-robot-excited"></i>
          AI 맞춤형 투자 플래너
          <span class="subtitle">똑똑한 AI가 추천하는 최적의 금융 포트폴리오</span>
        </h1>
      </div>

      <!-- 입력 폼과 포트폴리오 차트 섹션 -->
      <section class="form-chart-section">
        <div class="form-wrapper">
          <form @submit.prevent="generatePlan" class="investment-form">
            <!-- 투자 금액 입력 -->
            <div class="input-group">
              <label>
                <i class="mdi mdi-currency-krw"></i>
                투자 금액
              </label>
              <div class="input-with-icon">
                <input type="number" v-model="formData.total_amount" min="1000000" step="1000000" placeholder="최소 100만원" />
                <span class="input-suffix">원</span>
              </div>
            </div>

            <!-- 투자 기간 입력 -->
            <div class="input-group">
              <label>
                <i class="mdi mdi-calendar-range"></i>
                투자 기간
              </label>
              <div class="input-with-icon">
                <input type="number" v-model="formData.period_months" min="6" max="120" placeholder="6-120개월" />
                <span class="input-suffix">개월</span>
              </div>
            </div>

            <!-- 선호 은행 선택 -->
            <div class="input-group">
              <label>
                <i class="mdi mdi-bank"></i>
                선호 은행
              </label>
              <div class="bank-selection">
                <div class="selected-banks">
                  <span v-for="bank in selectedBanks" :key="bank.code" class="bank-tag">
                    {{ bank.name }}
                    <button @click="removeBank(bank.code)" type="button" class="remove-bank">
                      <i class="mdi mdi-close"></i>
                    </button>
                  </span>
                </div>
                <select v-model="formData.preferred_banks" multiple class="bank-select">
                  <option v-for="bank in availableBanks" :key="bank.code" :value="bank.code">
                    {{ bank.name }}
                  </option>
                </select>
              </div>
            </div>

            <!-- 제출 버튼 -->
            <button type="submit" class="submit-button" :disabled="loading">
              <i class="mdi mdi-calculator"></i>
              {{ loading ? "계획 생성 중..." : "투자 계획 생성" }}
            </button>
          </form>

          <!-- 차트 토글 버튼 -->
          <button v-if="plan" @click="toggleCharts" class="toggle-charts-button">
            <i class="mdi" :class="showCharts ? 'mdi-chevron-up' : 'mdi-chevron-down'"></i>
            차트 {{ showCharts ? "숨기기" : "보기" }}
          </button>
        </div>

        <!-- 포트폴리오 차트 -->
        <Transition name="fade">
          <div v-if="showCharts && plan" class="chart-container">
            <h2>
              <i class="mdi mdi-chart-pie"></i>
              포트폴리오 분포
            </h2>
            <PortfolioChart :items="plan.items" />
          </div>
        </Transition>
      </section>

      <!-- 타임라인 차트 -->
      <Transition name="fade">
        <section v-if="showCharts && plan" class="timeline-section">
          <h2>
            <i class="mdi mdi-chart-timeline"></i>
            투자 타임라인
          </h2>
          <TimelineChart :items="plan.items" :products="products" />
        </section>
      </Transition>

      <!-- 추천 상품 리스트 -->
      <section v-if="plan" class="products-section">
        <h2>
          <i class="mdi mdi-format-list-bulleted"></i>
          추천 투자 상품 상세
        </h2>
        <div class="products-grid">
          <div v-for="item in plan.items" :key="item.product_id" class="product-card">
            <!-- 상품 헤더 -->
            <div class="product-header">
              <div>
                <span class="bank-name">{{ getBankName(item.product_id) }}</span>
                <h3 class="product-name">{{ getProductName(item.product_id) }}</h3>
              </div>
              <span :class="['product-type', item.product_type]">
                {{ getProductType(item.product_type) }}
              </span>
            </div>

            <!-- 상품 상세 정보 -->
            <div class="product-details">
              <div class="detail-item">
                <i class="mdi mdi-cash"></i>
                <span class="label">투자금액</span>
                <strong>{{ formatAmount(item.amount) }}원</strong>
              </div>
              <div class="detail-item">
                <i class="mdi mdi-cash-multiple"></i>
                <span class="label">예상 만기금액</span>
                <strong class="amount">{{ calculateMaturityAmount(item) }}원</strong>
              </div>
              <div class="detail-item">
                <i class="mdi mdi-calendar-start"></i>
                <span class="label">투자 시작</span>
                <strong>{{ item.start_month }}개월 후</strong>
              </div>
              <div class="detail-item">
                <i class="mdi mdi-calendar-clock"></i>
                <span class="label">투자 기간</span>
                <strong>{{ item.period }}개월</strong>
              </div>
            </div>

            <!-- 상세 정보 버튼 -->
            <button @click="showProductDetails(item)" class="details-button">
              <i class="mdi mdi-information"></i>
              상세 정보 보기
            </button>
          </div>
        </div>
      </section>
    </div>

    <!-- 상품 상세 모달 -->
    <Teleport to="body">
      <Transition name="modal">
        <div v-if="selectedProduct" class="modal-overlay" @click="selectedProduct = null">
          <div class="modal-container" @click.stop>
            <ProductDetailModal :product="selectedProduct" @close="selectedProduct = null" @select="handleProductSelect" />
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script>
import { ref, reactive, computed } from "vue";
import axios from "axios";
import TimelineChart from "./TimelineChart.vue";
import PortfolioChart from "./PortfolioChart.vue";
import ProductDetailModal from "./ProductDetailModal.vue";

export default {
  name: "InvestmentPlanner",
  components: {
    TimelineChart,
    PortfolioChart,
    ProductDetailModal,
  },

  setup() {
    const formData = reactive({
      total_amount: 10000000,
      period_months: 120,
      preferred_banks: [],
      risk_preference: 3,
    });

    const loading = ref(false);
    const plan = ref(null);
    const banks = ref([]);
    const products = reactive({
      deposit: {},
      saving: {},
    });
    const selectedStrategy = ref("balanced");
    const selectedProduct = ref(null);

    const showCharts = ref(false);
    const toggleCharts = () => {
      showCharts.value = !showCharts.value;
    };

    const generatePlan = async () => {
      loading.value = true;
      try {
        const response = await axios.post("http://127.0.0.1:8000/recommendations/investment-plans/", {
          total_amount: formData.total_amount,
          period_months: formData.period_months,
          preferred_banks: formData.preferred_banks.join(","),
          risk_preference: formData.risk_preference,
        });
        plan.value = response.data;
        await fetchProductDetails();
        showCharts.value = false; // 초기에는 숨김 상태로 설정
      } catch (error) {
        console.error("Error generating plan:", error);
      } finally {
        loading.value = false;
      }
    };

    const fetchProductDetails = async () => {
      const productIds = plan.value.items.map((item) => item.product_id);
      try {
        const response = await axios.get("http://127.0.0.1:8000/recommendations/products/", {
          params: { product_ids: productIds.join(",") },
        });
        response.data.forEach((product) => {
          if (product.type === "deposit") {
            products.deposit[product.fin_prdt_cd] = product;
          } else {
            products.saving[product.fin_prdt_cd] = product;
          }
        });
      } catch (error) {
        console.error("Error fetching product details:", error);
      }
    };

    const getProductType = (type) => (type === "deposit" ? "예금" : "적금");

    const formatAmount = (amount) => new Intl.NumberFormat("ko-KR").format(amount);

    const getProductName = (productId) => {
      const depositProduct = products.deposit[productId];
      const savingProduct = products.saving[productId];
      return (depositProduct || savingProduct)?.fin_prdt_nm || "상품명 로딩 중...";
    };

    const getExpectedReturn = (item) => {
      const product = products[item.product_type]?.[item.product_id];
      if (!product) return "계산 중...";
      const option = product.options.find((opt) => opt.save_trm === item.period);
      if (!option) return "계산 중...";
      return option.intr_rate2 ? ((option.intr_rate + option.intr_rate2) / 2).toFixed(2) : option.intr_rate.toFixed(2);
    };

    const calculateMaturityAmount = (item) => {
      const amount = item.amount;
      const rate = getExpectedReturn(item);
      const period = item.period;
      return formatAmount(Math.round(amount * (1 + (rate / 100) * (period / 12))));
    };

    const getBankName = (productId) => {
      const product = products.deposit[productId] || products.saving[productId];
      return product?.kor_co_nm || "은행명 로딩 중...";
    };

    const showProductDetails = (item) => {
      selectedProduct.value = products[item.product_type][item.product_id];
    };

    // 초기 은행 목록 조회
    const fetchBanks = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:8000/recommendations/banks/");
        banks.value = response.data;
      } catch (error) {
        console.error("Error fetching banks:", error);
      }
    };

    // 컴포넌트 생성 시 은행 목록 조회
    fetchBanks();

    const selectedBanks = computed(() => {
      return banks.value.filter((bank) => formData.preferred_banks.includes(bank.code));
    });

    const availableBanks = computed(() => {
      return banks.value.filter((bank) => !formData.preferred_banks.includes(bank.code));
    });

    // methods
    const removeBank = (code) => {
      formData.preferred_banks = formData.preferred_banks.filter((b) => b !== code);
    };

    return {
      toggleCharts,
      showCharts,
      formData,
      loading,
      plan,
      banks,
      products,
      selectedStrategy,
      selectedProduct,
      generatePlan,
      getProductType,
      getProductName,
      formatAmount,
      calculateMaturityAmount,
      getBankName,
      showProductDetails,
      getExpectedReturn,
      selectedBanks,
      availableBanks,
      removeBank,
    };
  },
};
</script>
<style scoped>
.investment-planner {
  min-height: 100vh;
  background-color: #f5f7fa;
}

.planner-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

/* 헤더 스타일 */
.page-title {
  text-align: center;
  padding: 2.5rem 0;
  margin-bottom: 3rem;
  background: linear-gradient(135deg, rgba(24, 144, 255, 0.1), rgba(82, 196, 26, 0.1));
  border-radius: 1rem;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.page-title h1 {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  color: #1890ff;
  font-size: 2.5rem;
  font-weight: 700;
  margin: 0;
}

.page-title h1 i {
  font-size: 3.5rem;
  background: linear-gradient(45deg, #1890ff, #52c41a);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 0.5rem;
}

.subtitle {
  font-size: 1.2rem;
  color: #666;
  font-weight: normal;
  margin-top: 0.5rem;
}

@media (max-width: 768px) {
  .page-title h1 {
    font-size: 2rem;
  }
  
  .page-title h1 i {
    font-size: 2.8rem;
  }
  
  .subtitle {
    font-size: 1rem;
  }
}

/* 입력 폼 섹션 */
.form-chart-section {
  display: grid;
  grid-template-columns: minmax(300px, 400px) 1fr; /* 폼 영역 크기 고정 */
  gap: 2rem;
  background: white;
  padding: 2rem;
  border-radius: 1rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  overflow: hidden; /* 넘치는 부분 숨김 */
}

.chart-container {
  min-width: 0; /* 차트 영역이 넘치지 않도록 설정 */
  width: 100%;
}

.form-wrapper {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.investment-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* 입력 그룹 스타일 */
.input-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.input-group label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  color: #4b5563;
}

.input-group label i {
  color: #2563eb;
}

.input-with-icon {
  position: relative;
}

.input-with-icon input {
  width: 100%;
  padding: 0.75rem 3rem 0.75rem 1rem;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  font-size: 1rem;
  transition: all 0.2s;
}

.input-with-icon input:focus {
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
  outline: none;
}

.input-suffix {
  position: absolute;
  right: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #6b7280;
}

/* 은행 선택 스타일 */
.bank-selection {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.selected-banks {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  min-height: 2rem;
}

.bank-tag {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.25rem 0.75rem;
  background: #e0e7ff;
  color: #4f46e5;
  border-radius: 1rem;
  font-size: 0.875rem;
}

.remove-bank {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.125rem;
  color: #4f46e5;
  border-radius: 50%;
  transition: all 0.2s;
}

.remove-bank:hover {
  background-color: #4f46e5;
  color: white;
}

.bank-select {
  padding: 0.75rem;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  height: 8rem;
}

/* 버튼 스타일 */
.submit-button,
.details-button,
.join-button,
.select-button {
  background-color: #2563eb !important;
  color: white !important;
}

.submit-button:hover:not(:disabled),
.details-button:hover,
.join-button:hover,
.select-button:hover {
  background-color: #1d4ed8 !important;
}

.submit-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem;
  background-color: #2563eb;
  color: white;
  border-radius: 0.5rem;
  font-weight: 500;
  transition: all 0.2s;
}

.submit-button:hover:not(:disabled) {
  background-color: #1d4ed8;
}

.submit-button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.toggle-charts-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem;
  background-color: white;
  border: 1px solid #2563eb;
  color: #2563eb;
  border-radius: 0.5rem;
  font-weight: 500;
  transition: all 0.2s;
}

.toggle-charts-button:hover {
  background-color: #e0e7ff;
}

/* 차트 컨테이너 스타일 */
.chart-container {
  padding: 1.5rem;
  background: white;
  border-radius: 1rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

/* 상품 리스트 스타일 */
.products-section {
  margin-top: 2rem;
  padding: 2rem;
  background: white;
  border-radius: 1rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.products-section h2 {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.75rem;
  color: #1e40af;
  margin-bottom: 2rem;
  padding-bottom: 0.5rem;
  border-bottom: 3px solid #3b82f6;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.product-card {
  padding: 1.5rem;
  border: 1px solid #e5e7eb;
  border-radius: 0.75rem;
  transition: all 0.2s;
}

.product-card:hover {
  border-color: #2563eb;
  transform: translateY(-2px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

/* 모달 스타일 */
.modal-overlay {
  position: fixed;
  inset: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
  backdrop-filter: blur(4px);
}

.modal-container {
  width: 100%;
  max-width: 900px;
  max-height: 90vh;
  background: transparent;
  border-radius: 1rem;
  display: flex;
  flex-direction: column;
}

/* 버튼 스타일 통일 */
.details-button {
  background-color: #2563eb !important;
  color: white !important;
  border: none !important;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  transition: all 0.2s ease;
}

.details-button:hover {
  background-color: #1d4ed8 !important;
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* 버튼 스타일 통일 */
.submit-button,
.details-button,
.join-button,
.select-button,
.official-site-button,
.news-button {
  background-color: #2563eb !important;
  color: white !important;
  border: none !important;
  transition: all 0.2s ease !important;
}

.submit-button:hover:not(:disabled),
.details-button:hover,
.join-button:hover,
.select-button:hover,
.official-site-button:hover,
.news-button:hover {
  background-color: #1d4ed8 !important;
  transform: translateY(-1px);
}

/* 애니메이션 */
.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-1rem);
}

/* 반응형 디자인 */
@media (max-width: 1024px) {
  .form-chart-section {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .planner-container {
    padding: 1rem;
  }

  .products-grid {
    grid-template-columns: 1fr;
  }
}
</style>
