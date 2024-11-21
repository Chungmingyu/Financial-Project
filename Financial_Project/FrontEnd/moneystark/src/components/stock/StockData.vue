<template>
  <div>
    <input v-model="symbol" @keyup.enter="fetchStockData" placeholder="주식 티커를 입력하세요 (예: AAPL)" />
    <button @click="fetchStockData">검색</button>

    <div v-if="loading">로딩 중...</div>

    <div v-if="stockData">
      <h2>{{ stockData.symbol }}의 주식 데이터</h2>
      <p>현재 가격: {{ stockData.quote.c }}</p>
      <p>고가: {{ stockData.quote.h }}</p>
      <p>저가: {{ stockData.quote.l }}</p>
      <p>시가: {{ stockData.quote.o }}</p>
      <p>이전 종가: {{ stockData.quote.pc }}</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      symbol: "",
      stockData: null,
      loading: false,
    };
  },
  methods: {
    async fetchStockData() {
      if (this.symbol.trim() === "") return;

      this.loading = true;
      try {
        const response = await axios.get(`http://127.0.0.1:8000/moneys/stock_data/${this.symbol}/`);
        this.stockData = response.data;
      } catch (error) {
        console.error("Error fetching stock data:", error);
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
input {
  margin: 10px 0;
}
</style>
