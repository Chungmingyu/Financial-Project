<template>
  <div>
    <input v-model="symbol" @keyup.enter="fetchStockData" placeholder="주식 티커를 입력하세요 (예: AAPL)" />
    <button @click="fetchStockData">검색</button>
    <!-- 인기 있는 미국 주식 심볼 (Ticker Symbols)
AAPL - Apple Inc. (기술)
AMZN - Amazon.com, Inc. (소매/기술)
GOOGL - Alphabet Inc. (Google) (기술)
MSFT - Microsoft Corporation (기술)
TSLA - Tesla, Inc. (자동차/기술)
FB - Meta Platforms, Inc. (구 Facebook) (기술)
NFLX - Netflix, Inc. (미디어/기술)
NVDA - NVIDIA Corporation (반도체/기술)
INTC - Intel Corporation (반도체/기술)
DIS - The Walt Disney Company (엔터테인먼트)
V - Visa Inc. (금융)
MA - Mastercard Incorporated (금융)
BA - Boeing Company (항공/방위산업)
GS - Goldman Sachs Group, Inc. (금융)
PYPL - PayPal Holdings, Inc. (금융)
IBM - International Business Machines Corporation (기술)
KO - The Coca-Cola Company (음료)
PEP - PepsiCo, Inc. (음료)
WMT - Walmart Inc. (소매)
T - AT&T Inc. (통신)
CVX - Chevron Corporation (에너지)
XOM - ExxonMobil Corporation (에너지)
JPM - JPMorgan Chase & Co. (금융)
MCD - McDonald's Corporation (패스트푸드)
AMD - Advanced Micro Devices, Inc. (반도체/기술)
SPY - SPDR S&P 500 ETF Trust (ETF)
QQQ - Invesco QQQ Trust (ETF, NASDAQ)
VZ - Verizon Communications Inc. (통신)
LMT - Lockheed Martin Corporation (방위산업)
NKE - NIKE, Inc. (소매/운동) -->

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
