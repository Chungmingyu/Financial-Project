<template>
  <div class="calculator-container">
    <div class="glass-card">
      <h1 class="title">환율 계산기</h1>
      <form id="exchange-form">
        <div class="form-group">
          <label for="currency">통화 선택</label>
          <div class="input-wrapper">
            <select id="currency" v-model="selectedCurrency" @change="convertToForeign" class="currency-select">
              <option v-for="rate in rates" :key="rate.cur_unit" :value="rate.cur_unit">
                {{ rate.cur_nm }}
              </option>
            </select>
          </div>
        </div>

        <div class="form-group">
          <label>외화 금액</label>
          <div class="input-wrapper">
            <input type="number" v-model="foreignAmount" @input="convertToKrw" class="amount-input" />
            <span class="currency-symbol">{{ selectedCurrencySymbol }}</span>
          </div>
        </div>

        <div class="form-group">
          <label>원화 금액</label>
          <div class="input-wrapper">
            <input type="number" v-model="krwAmount" @input="convertToForeign" class="amount-input" />
            <span class="currency-symbol">₩</span>
          </div>
        </div>

        <div class="info-text">* 엔화, 인도네시아 루피아는 100단위, 나머지는 모두 1 단위</div>
      </form>
      <p v-if="error" class="error-message">{{ error }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import axios from "axios";

const krwAmount = ref(0);
const foreignAmount = ref(0);
const selectedCurrency = ref("");
const rates = ref([]);
const error = ref("");

const fetchRates = async () => {
  try {
    const response = await axios.get("http://127.0.0.1:8000/exchanges/");
    rates.value = response.data.rates;
    if (rates.value.length > 0) {
      selectedCurrency.value = rates.value[0].cur_unit;
    }
  } catch (err) {
    console.error("Error fetching exchange rates:", err);
    error.value = "환율 정보를 가져오는 중 오류가 발생했습니다.";
  }
};

const convertToForeign = () => {
  const rate = rates.value.find((rate) => rate.cur_unit === selectedCurrency.value).deal_bas_r;
  foreignAmount.value = (krwAmount.value / parseFloat(rate.replace(",", ""))).toFixed(2);
};

const convertToKrw = () => {
  const rate = rates.value.find((rate) => rate.cur_unit === selectedCurrency.value).deal_bas_r;
  krwAmount.value = (foreignAmount.value * parseFloat(rate.replace(",", ""))).toFixed(2);
};

const selectedCurrencySymbol = computed(() => {
  const rate = rates.value.find((rate) => rate.cur_unit === selectedCurrency.value);
  return rate ? rate.cur_unit : "";
});

onMounted(fetchRates);
</script>
<style scoped>
.calculator-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 20px;
}

.glass-card {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 40px;
  box-shadow: 0 8px 32px rgba(31, 38, 135, 0.15);
  width: 100%;
  max-width: 500px;
  border: 1px solid rgba(255, 255, 255, 0.18);
}

.title {
  color: #2c3e50;
  font-size: 2rem;
  font-weight: 700;
  text-align: center;
  margin-bottom: 2rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  color: #34495e;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.currency-select,
.amount-input {
  width: 100%;
  padding: 12px;
  border: 2px solid #e0e0e0;
  border-radius: 10px;
  font-size: 1rem;
  transition: all 0.3s ease;
  background: white;
}

.currency-select:focus,
.amount-input:focus {
  border-color: #FFBF00;
  outline: none;
  box-shadow: 0 0 0 3px rgba(119, 0, 255, 0.1);
}

.currency-symbol {
  position: absolute;
  right: 12px;
  color: #FFBF00;
  font-weight: 600;
}

.info-text {
  font-size: 0.8rem;
  color: #666;
  margin-top: 1rem;
  text-align: center;
}

.error-message {
  color: #e74c3c;
  text-align: center;
  margin-top: 1rem;
  padding: 10px;
  background: rgba(231, 76, 60, 0.1);
  border-radius: 8px;
}

/* 반응형 디자인 */
@media (max-width: 600px) {
  .glass-card {
    padding: 20px;
  }

  .title {
    font-size: 1.5rem;
  }
}

/* 호버 효과 */
.currency-select:hover,
.amount-input:hover {
  border-color: #FFBF00;
}

/* 애니메이션 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.glass-card {
  animation: fadeIn 0.6s ease-out;
}
</style>
