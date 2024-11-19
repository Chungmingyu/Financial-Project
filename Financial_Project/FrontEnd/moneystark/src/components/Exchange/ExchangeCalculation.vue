<template>
  <div class="container mt-5">
    <h1 class="text-center mb-4">환율 계산기</h1>
    <form id="exchange-form">
      <div class="form-group row mb-3 align-items-center">
        <label for="currency" class="col-sm-2 col-form-label">통화:</label>
        <div class="col-sm-3">
          <select id="currency" v-model="selectedCurrency" @change="convertToForeign" class="form-control">
            <option v-for="rate in rates" :key="rate.cur_unit" :value="rate.cur_unit">
              {{ rate.cur_nm }}
            </option>
          </select>
        </div>
        <div class="col-sm-5">
          <input type="number" id="foreign-amount" v-model="foreignAmount" @input="convertToKrw" class="form-control" />
        </div>
        <div class="col-sm-2">
          <span class="input-group-text">{{ selectedCurrencySymbol }}</span>
        </div>
      </div>
      <div class="form-group row mb-3 align-items-center">
        <label for="krw-amount" class="col-sm-2 col-form-label">원화 금액:</label>
        <div class="col-sm-8">
          <input type="number" id="krw-amount" v-model="krwAmount" @input="convertToForeign" class="form-control" />
        </div>
        <div class="col-sm-2">
          <span class="input-group-text">₩</span>
        </div>
      </div>
      <div class="form-group row">
        <div class="col-sm-12">
          <small class="form-text text-muted">* 엔화, 인도네시아 루피아는 100단위, 나머지는 모두 1 단위</small>
        </div>
      </div>
    </form>
    <p id="result" class="mt-4"></p>
    <p v-if="error" class="text-danger mt-4">{{ error }}</p>
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
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

h1 {
  color: #333;
}

.input-group-text {
  background-color: #e9ecef;
  border: 1px solid #ced4da;
  border-radius: 0.25rem;
  padding: 0.375rem 0.75rem;
}

.text-danger {
  color: red;
}
</style>
