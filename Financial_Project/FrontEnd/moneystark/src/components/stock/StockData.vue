<template>
  <div class="container">
    <input v-model="symbol" @keyup.enter="fetchStockData" placeholder="주식 티커를 입력하세요 (예: AAPL)" class="input" />
    <button @click="fetchStockData" class="search-button">검색</button>

    <div>
      <h3>인기 있는 주식 심볼</h3>
      <div v-for="item in popularSymbols" :key="item.symbol" class="symbol-container">
        <button @click="fetchStockData(item.symbol)" class="symbol-button">{{ item.symbol }} - {{ item.name }} ({{ item.sector }})</button>
        <div v-if="symbolData[item.symbol]" class="stock-data">
          <p>현재 가격: {{ symbolData[item.symbol].quote.c }}</p>
          <p>고가: {{ symbolData[item.symbol].quote.h }}</p>
          <p>저가: {{ symbolData[item.symbol].quote.l }}</p>
          <p>시가: {{ symbolData[item.symbol].quote.o }}</p>
          <p>이전 종가: {{ symbolData[item.symbol].quote.pc }}</p>
        </div>
      </div>
    </div>

    <div v-if="loading" class="loading">로딩 중...</div>

    <div v-if="stockData" class="stock-data">
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
      popularSymbols: [
        { symbol: "AAPL", name: "Apple Inc.", sector: "기술" },
        { symbol: "AMZN", name: "Amazon.com, Inc.", sector: "소매/기술" },
        { symbol: "GOOGL", name: "Alphabet Inc. (Google)", sector: "기술" },
        { symbol: "MSFT", name: "Microsoft Corporation", sector: "기술" },
        { symbol: "TSLA", name: "Tesla, Inc.", sector: "자동차/기술" },
        { symbol: "FB", name: "Meta Platforms, Inc. (구 Facebook)", sector: "기술" },
        { symbol: "NFLX", name: "Netflix, Inc.", sector: "미디어/기술" },
        { symbol: "NVDA", name: "NVIDIA Corporation", sector: "반도체/기술" },
        { symbol: "INTC", name: "Intel Corporation", sector: "반도체/기술" },
        { symbol: "DIS", name: "The Walt Disney Company", sector: "엔터테인먼트" },
        { symbol: "V", name: "Visa Inc.", sector: "금융" },
        { symbol: "MA", name: "Mastercard Incorporated", sector: "금융" },
        { symbol: "BA", name: "Boeing Company", sector: "항공/방위산업" },
        { symbol: "GS", name: "Goldman Sachs Group, Inc.", sector: "금융" },
        { symbol: "PYPL", name: "PayPal Holdings, Inc.", sector: "금융" },
        { symbol: "IBM", name: "International Business Machines Corporation", sector: "기술" },
        { symbol: "KO", name: "The Coca-Cola Company", sector: "음료" },
        { symbol: "PEP", name: "PepsiCo, Inc.", sector: "음료" },
        { symbol: "WMT", name: "Walmart Inc.", sector: "소매" },
        { symbol: "T", name: "AT&T Inc.", sector: "통신" },
        { symbol: "CVX", name: "Chevron Corporation", sector: "에너지" },
        { symbol: "XOM", name: "ExxonMobil Corporation", sector: "에너지" },
        { symbol: "JPM", name: "JPMorgan Chase & Co.", sector: "금융" },
        { symbol: "MCD", name: "McDonald's Corporation", sector: "패스트푸드" },
        { symbol: "AMD", name: "Advanced Micro Devices, Inc.", sector: "반도체/기술" },
        { symbol: "SPY", name: "SPDR S&P 500 ETF Trust", sector: "ETF" },
        { symbol: "QQQ", name: "Invesco QQQ Trust", sector: "ETF, NASDAQ" },
        { symbol: "VZ", name: "Verizon Communications Inc.", sector: "통신" },
        { symbol: "LMT", name: "Lockheed Martin Corporation", sector: "방위산업" },
        { symbol: "NKE", name: "NIKE, Inc.", sector: "소매/운동" },
      ],
      symbolData: {}, // 각 심볼의 데이터를 저장할 객체
    };
  },
  methods: {
    async fetchStockData(symbol = this.symbol) {
      if (symbol.trim() === "") return;

      this.loading = true;
      try {
        const response = await axios.get(`http://127.0.0.1:8000/moneys/stock_data/${symbol}/`);
        console.log(response.data); // 응답 데이터 구조 확인
        this.symbolData = { ...this.symbolData, [symbol]: response.data };
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
.container {
  background-color: #1e1e1e;
  color: #ffffff;
  padding: 20px;
  border-radius: 10px;
  max-width: 800px;
  margin: 0 auto;
}

.input {
  width: calc(100% - 22px);
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ffbf00;
  border-radius: 5px;
  background-color: #333333;
  color: #ffffff;
}

.search-button {
  background-color: #ffbf00;
  color: #1e1e1e;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
}

.search-button:hover {
  background-color: #e6ac00;
}

.symbol-container {
  margin-bottom: 20px;
}

.symbol-button {
  background-color: #333333;
  color: #ffbf00;
  border: 1px solid #ffbf00;
  padding: 10px;
  border-radius: 5px;
  cursor: pointer;
  width: 100%;
  text-align: left;
}

.symbol-button:hover {
  background-color: #444444;
}

.stock-data {
  background-color: #2e2e2e;
  padding: 10px;
  border-radius: 5px;
  margin-top: 10px;
}

.loading {
  color: #ffbf00;
  font-weight: bold;
}
</style>
