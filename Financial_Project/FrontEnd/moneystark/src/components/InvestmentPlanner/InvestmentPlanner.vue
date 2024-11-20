<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- 입력 폼과 포트폴리오 차트 섹션 -->
      <div class="bg-white shadow-lg rounded-xl p-8 mb-8">
        <h1 class="text-3xl font-bold mb-8 text-gray-800">맞춤형 투자 플래너</h1>

        <div class="flex flex-col lg:flex-row gap-8">
          <!-- 입력 폼 -->
          <div class="lg:w-1/2">
            <!-- col-span-1 추가 -->
            <form @submit.prevent="generatePlan" class="space-y-6">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">투자 금액</label>
                <div class="relative">
                  <input type="number" v-model="formData.total_amount" class="w-full p-3 border rounded-lg pr-12" min="1000000" step="1000000" />
                  <span class="absolute right-3 top-3 text-gray-500">원</span>
                </div>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">투자 기간</label>
                <div class="relative">
                  <input type="number" v-model="formData.period_months" class="w-full p-3 border rounded-lg pr-16" min="6" max="120" />
                  <span class="absolute right-3 top-3 text-gray-500">개월</span>
                </div>
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">선호 은행</label>
                <div class="relative">
                  <div class="flex flex-wrap gap-2 mb-2">
                    <span v-for="bank in selectedBanks" :key="bank.code" class="inline-flex items-center px-3 py-1 rounded-full text-sm bg-blue-100 text-blue-700">
                      {{ bank.name }}
                      <button @click="removeBank(bank.code)" class="ml-2 text-blue-500 hover:text-blue-700">×</button>
                    </span>
                  </div>
                  <select v-model="formData.preferred_banks" multiple class="w-full p-3 border rounded-lg">
                    <option v-for="bank in availableBanks" :key="bank.code" :value="bank.code">
                      {{ bank.name }}
                    </option>
                  </select>
                </div>
              </div>

              <button type="submit" class="w-full bg-blue-600 text-white py-3 px-6 rounded-lg hover:bg-blue-700 transition-colors" :disabled="loading">
                {{ loading ? "계획 생성 중..." : "투자 계획 생성" }}
              </button>
            </form>
            <button
              v-if="plan"
              @click="toggleCharts"
              class="w-full mt-4 px-4 py-2 border border-blue-600 text-blue-600 rounded-lg hover:bg-blue-50 transition-colors flex items-center justify-center gap-2"
            >
              <span>차트 {{ showCharts ? "숨기기" : "보기" }}</span>
              <span class="transform transition-transform" :class="{ 'rotate-180': showCharts }">▼</span>
            </button>
          </div>

          <!-- 포트폴리오 차트 -->
          <Transition name="fade">
            <div v-if="showCharts && plan" class="lg:w-1/2">
              <div class="w-full">
                <h2 class="text-xl font-semibold mb-4">포트폴리오 분포</h2>
                <PortfolioChart :items="plan.items" />
              </div>
            </div>
          </Transition>
        </div>
      </div>

      <!-- 타임라인 차트 -->
      <div v-if="showCharts && plan" class="bg-white shadow-lg rounded-xl p-8 mb-8">
        <h2 class="text-xl font-semibold mb-6">투자 타임라인</h2>
        <TimelineChart :items="plan.items" :products="products" />
      </div>

      <!-- 투�� 상품 상세 리스트 -->
      <div v-if="plan" class="bg-white shadow-lg rounded-xl p-8">
        <h2 class="text-xl font-semibold mb-6">추천 투자 상품 상세</h2>
        <div class="space-y-4">
          <div v-for="item in plan.items" :key="item.product_id" class="bg-white rounded-lg border hover:border-blue-500 transition-colors duration-200 p-6">
            <div class="flex items-center justify-between mb-4">
              <div>
                <span class="text-sm text-gray-500">{{ getBankName(item.product_id) }}</span>
                <h3 class="text-lg font-semibold">{{ getProductName(item.product_id) }}</h3>
              </div>
              <span class="px-4 py-2 rounded-full text-sm font-medium" :class="item.product_type === 'deposit' ? 'bg-blue-100 text-blue-800' : 'bg-green-100 text-green-800'">
                {{ getProductType(item.product_type) }}
              </span>
            </div>

            <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div>
                <span class="text-sm text-gray-500">투자금액</span>
                <p class="text-lg font-semibold">{{ formatAmount(item.amount) }}원</p>
              </div>
              <div>
                <span class="text-sm text-gray-500">예상 만기금액</span>
                <p class="text-lg font-semibold text-blue-600">{{ calculateMaturityAmount(item) }}원</p>
              </div>
              <div>
                <span class="text-sm text-gray-500">투자 시작</span>
                <p>{{ item.start_month }}개월 후</p>
              </div>
              <div>
                <span class="text-sm text-gray-500">투자 기간</span>
                <p>{{ item.period }}개월</p>
              </div>
            </div>

            <button @click="showProductDetails(item)" class="mt-4 px-4 py-2 border border-blue-600 text-blue-600 rounded hover:bg-blue-50 transition-colors">상세 정보 보기</button>
          </div>
        </div>
      </div>
    </div>

    <!-- 모달 -->
    <Teleport to="#app">
      <transition name="fade">
        <div v-if="selectedProduct" class="fixed inset-0 z-[1100]" style="background: rgba(0, 0, 0, 0.5)">
          <div class="fixed inset-0 flex items-center justify-center p-4">
            <div class="relative bg-white rounded-xl shadow-2xl w-full max-w-2xl" @click.stop>
              <ProductDetailModal :product="selectedProduct" @close="selectedProduct = null" />
            </div>
          </div>
        </div>
      </transition>
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
select[multiple] {
  height: 120px;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
/* 기존 스타일 유지하고 추가 */
.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

select[multiple] {
  height: 120px;
}

/* 가로 스크롤바 스타일링 */
.overflow-x-auto {
  scrollbar-width: thin;
  scrollbar-color: #cbd5e0 #edf2f7;
}

.overflow-x-auto::-webkit-scrollbar {
  height: 6px;
}

.overflow-x-auto::-webkit-scrollbar-track {
  background: #edf2f7;
  border-radius: 3px;
}

.overflow-x-auto::-webkit-scrollbar-thumb {
  background-color: #cbd5e0;
  border-radius: 3px;
}
.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}
.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

/* 화살표 회전 애니메이션 */
.rotate-180 {
  transform: rotate(180deg);
}

.transform {
  transition: transform 0.3s ease;
}
</style>
