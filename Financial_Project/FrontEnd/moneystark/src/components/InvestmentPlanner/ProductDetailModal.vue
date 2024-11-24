<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg w-full max-w-2xl">
      <!-- 모달 헤더 -->
      <div class="border-b px-6 py-4 flex justify-between items-center">
        <h2 class="text-xl font-bold">상품 상세 정보</h2>
        <button @click="$emit('close')" class="text-gray-500 hover:text-gray-700">
          <span class="text-2xl">&times;</span>
        </button>
      </div>

      <!-- 모달 본문 -->
      <div class="px-6 py-4 overflow-y-auto max-h-[70vh]">
        <div v-if="product">
          <div class="mb-4">
            <p class="text-gray-600">{{ product.kor_co_nm }}</p>
            <h3 class="text-lg font-bold">{{ product.fin_prdt_nm }}</h3>
          </div>

          <!-- 기본 정보 -->
          <div class="grid grid-cols-2 gap-4 mb-4">
            <div>
              <span class="text-sm text-gray-500">가입 기간</span>
              <p>{{ product.save_trm }}개월</p>
            </div>
            <div>
              <span class="text-sm text-gray-500">금리 유형</span>
              <p>{{ product.intr_rate_type_nm }}</p>
            </div>
          </div>

          <!-- 상세 정보 섹션 -->
          <div class="border-t mt-4 pt-4">
            <h4 class="font-semibold mb-3">금리 정보</h4>
            <div class="bg-gray-50 p-4 rounded-lg mb-4">
              <table class="w-full">
                <thead>
                  <tr class="text-sm text-gray-600">
                    <th class="text-left pb-2">가입기간</th>
                    <th class="text-left pb-2">기본금리</th>
                    <th class="text-left pb-2">최대우대금리</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="option in product.options" :key="option.save_trm">
                    <td class="py-1">{{ option.save_trm }}개월</td>
                    <td class="py-1">{{ option.intr_rate }}%</td>
                    <td class="py-1">{{ option.intr_rate2 }}%</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- 가입 조건 -->
            <div class="space-y-3">
              <h4 class="font-semibold">가입 조건</h4>
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <span class="text-sm text-gray-500">가입 방법</span>
                  <p>{{ product.join_way }}</p>
                </div>
                <div>
                  <span class="text-sm text-gray-500">가입 대상</span>
                  <p>{{ product.join_member }}</p>
                </div>
              </div>

              <!-- 기타 유의사항 -->
              <div class="mt-4">
                <h4 class="font-semibold mb-2">유의사항</h4>
                <p class="text-sm text-gray-600 whitespace-pre-line">{{ product.etc_note }}</p>
              </div>
            </div>
          </div>

          <!-- 예상 수익 계산기 추가 -->
          <div class="border-t mt-4 pt-4">
            <h4 class="font-semibold mb-3">예상 수익 계산기</h4>
            <div class="bg-gray-50 p-4 rounded-lg">
              <div class="space-y-4">
                <div>
                  <label class="block text-sm text-gray-600 mb-1">투자 금액</label>
                  <input type="number" v-model="calculatorAmount" class="w-full p-2 border rounded" min="0" step="10000" />
                </div>
                <div>
                  <label class="block text-sm text-gray-600 mb-1">투자 기간</label>
                  <select v-model="calculatorPeriod" class="w-full p-2 border rounded">
                    <option v-for="option in product.options" :key="option.save_trm" :value="option.save_trm">{{ option.save_trm }}개월</option>
                  </select>
                </div>
                <div class="bg-white p-3 rounded border">
                  <div class="grid grid-cols-2 gap-4">
                    <div>
                      <span class="text-sm text-gray-500">만기 예상 금액</span>
                      <p class="font-semibold">{{ calculateExpectedAmount }}원</p>
                    </div>
                    <div>
                      <span class="text-sm text-gray-500">총 이자 수익</span>
                      <p class="font-semibold text-blue-600">{{ calculateInterestAmount }}원</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 가입 채널 정보 추가 -->
          <div class="border-t mt-4 pt-4">
            <h4 class="font-semibold mb-3">가입 채널</h4>
            <div class="space-y-2">
              <div v-for="(available, channel) in availableJoinWays" :key="channel" class="flex items-center p-2 rounded" :class="available ? 'bg-green-50' : 'bg-gray-50'">
                <span class="material-icons mr-2" :class="available ? 'text-green-600' : 'text-gray-400'">
                  {{ available ? "check_circle" : "cancel" }}
                </span>
                <span :class="available ? 'text-green-800' : 'text-gray-500'">
                  {{ getChannelName(channel) }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 모달 푸터 -->
      <div class="border-t px-6 py-4 bg-gray-50">
        <button class="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition-colors" @click="$emit('select', product)">상품 선택하기</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ProductDetailModal",

  props: {
    product: {
      type: Object,
      required: true,
    },
  },

  data() {
    return {
      calculatorAmount: 1000000,
      calculatorPeriod: null,
      availableJoinWays: {
        internet: false,
        mobile: false,
        branch: false,
        phone: false,
      },
    };
  },

  computed: {
    calculateExpectedAmount() {
      if (!this.calculatorAmount || !this.calculatorPeriod) return "0";
      const option = this.product.options.find((opt) => opt.save_trm === this.calculatorPeriod);
      if (!option) return "0";

      const rate = option.intr_rate2 || option.intr_rate;
      const interest = (this.calculatorAmount * (rate / 100) * this.calculatorPeriod) / 12;
      return this.formatAmount(Math.round(this.calculatorAmount + interest));
    },

    calculateInterestAmount() {
      if (!this.calculatorAmount || !this.calculatorPeriod) return "0";
      const total = parseInt(this.calculateExpectedAmount.replace(/,/g, ""));
      return this.formatAmount(total - this.calculatorAmount);
    },
  },

  methods: {
    formatAmount(amount) {
      return new Intl.NumberFormat("ko-KR").format(amount);
    },

    getChannelName(channel) {
      const names = {
        internet: "인터넷뱅킹",
        mobile: "모바일뱅킹",
        branch: "영업점",
        phone: "전화뱅킹",
      };
      return names[channel];
    },

    parseJoinWays() {
      const joinWay = this.product.join_way || "";
      this.availableJoinWays = {
        internet: joinWay.includes("인터넷"),
        mobile: joinWay.includes("모바일"),
        branch: joinWay.includes("영업점"),
        phone: joinWay.includes("전화"),
      };
    },
  },

  created() {
    this.calculatorPeriod = this.product.options[0]?.save_trm;
    this.parseJoinWays();
  },
};
</script>

<style scoped>
.modal-container {
  animation: fadeIn 0.3s ease-out;
}

.modal-header {
  background-color: #f8f9fa;
  border-bottom: 1px solid #e9ecef;
}

.modal-title {
  color: #1890ff;
  font-weight: bold;
}

.section-title {
  color: #1890ff;
  font-size: 1.1rem;
  margin-bottom: 1rem;
}

.info-table {
  width: 100%;
  border-collapse: collapse;
  margin: 1rem 0;
}

.info-table th,
.info-table td {
  padding: 12px;
  border-bottom: 1px solid #eee;
}

.info-table th {
  background-color: #fafafa;
  font-weight: normal;
  color: #666;
}

.calculator-section {
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 1.5rem;
  margin: 1rem 0;
}

.result-box {
  background-color: white;
  border-radius: 6px;
  padding: 1rem;
  margin-top: 1rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.join-channel {
  display: flex;
  align-items: center;
  padding: 0.5rem;
  border-radius: 4px;
  margin: 0.5rem 0;
  transition: background-color 0.2s;
}

.join-channel:hover {
  background-color: #e6f7ff;
}

.channel-icon {
  color: #1890ff;
  margin-right: 0.5rem;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

@media (max-width: 768px) {
  .modal-container {
    margin: 1rem;
  }
}
</style>
