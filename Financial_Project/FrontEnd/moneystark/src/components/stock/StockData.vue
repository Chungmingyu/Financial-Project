<template>
  <div class="container">
    <input v-model="symbol" @keyup.enter="fetchStockData" placeholder="주식 티커를 입력하세요 (예: AAPL)" class="input" />
    <button @click="fetchStockData" class="search-button">검색</button>

    <div v-if="loading" class="loading">로딩 중...</div>

    <div v-if="stockData" class="stock-data">
      <h2>
        <i class="mdi mdi-chart-line"></i>
        {{ stockData.symbol }}의 실시간 시세
      </h2>
      <div class="price-grid">
        <div class="price-card">
          <div class="price-label">
            <i class="mdi mdi-currency-usd"></i>
            현재 가격
          </div>
          <div class="price-value highlight">${{ stockData.quote.c.toFixed(2) }}</div>
          <div class="price-change" :class="priceChangeClass">
            {{ getPriceChange() }}
          </div>
        </div>
        <div class="price-card">
          <div class="price-label">
            <i class="mdi mdi-arrow-up-bold"></i>
            고가
          </div>
          <div class="price-value">${{ stockData.quote.h.toFixed(2) }}</div>
        </div>
        <div class="price-card">
          <div class="price-label">
            <i class="mdi mdi-arrow-down-bold"></i>
            저가
          </div>
          <div class="price-value">${{ stockData.quote.l.toFixed(2) }}</div>
        </div>
        <div class="price-card">
          <div class="price-label">
            <i class="mdi mdi-clock-start"></i>
            시가
          </div>
          <div class="price-value">${{ stockData.quote.o.toFixed(2) }}</div>
        </div>
        <div class="price-card">
          <div class="price-label">
            <i class="mdi mdi-clock-end"></i>
            이전 종가
          </div>
          <div class="price-value">${{ stockData.quote.pc.toFixed(2) }}</div>
        </div>
      </div>
    </div>
    <div>
      <h3>인기 있는 주식 심볼</h3>
      <div v-for="item in popularSymbols" :key="item.symbol" class="symbol-container">
        <button @click="fetchStockData(item.symbol)" class="symbol-button">{{ item.symbol }} - {{ item.name }} ({{ item.sector }})</button>
        <!-- <div v-if="symbolData[item.symbol]" class="stock-data">
          <p>현재 가격: {{ symbolData[item.symbol].quote.c }}</p>
          <p>고가: {{ symbolData[item.symbol].quote.h }}</p>
          <p>저가: {{ symbolData[item.symbol].quote.l }}</p>
          <p>시가: {{ symbolData[item.symbol].quote.o }}</p>
          <p>이전 종가: {{ symbolData[item.symbol].quote.pc }}</p>
        </div> -->
      </div>
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
      // symbol이 문자열이 아닌 경우를 처리
      const symbolStr = typeof symbol === "string" ? symbol : this.symbol;

      if (!symbolStr || symbolStr.trim() === "") return;

      this.loading = true;
      try {
        const response = await axios.get(`http://127.0.0.1:8000/moneys/stock_data/${symbolStr}/`);
        console.log(response.data);
        this.symbolData = { ...this.symbolData, [symbolStr]: response.data };
        this.stockData = response.data; // 검색 결과도 표시
      } catch (error) {
        console.error("Error fetching stock data:", error);
      } finally {
        this.loading = false;
      }
    },
    getPriceChange() {
      if (!this.stockData) return "";
      const change = this.stockData.quote.c - this.stockData.quote.pc;
      const changePercent = (change / this.stockData.quote.pc) * 100;
      const sign = change >= 0 ? "+" : "";
      return `${sign}${change.toFixed(2)} (${sign}${changePercent.toFixed(2)}%)`;
    },
  },
  computed: {
    priceChangeClass() {
      if (!this.stockData) return "";
      const change = this.stockData.quote.c - this.stockData.quote.pc;
      return change >= 0 ? "price-up" : "price-down";
    },
  },
};
</script>

<style scoped>
.container {
  max-width: 1200px;
  margin: 40px auto;
  padding: 20px;
  font-family: "Noto Sans KR", sans-serif;
  background-color: #ffffff;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.input {
  width: calc(100% - 22px);
  padding: 12px 20px;
  margin-bottom: 20px;
  border: 1px solid #d9d9d9;
  border-radius: 6px;
  font-size: 1rem;
  color: #555;
  transition: all 0.3s ease;
}

.input:focus {
  border-color: #1890ff;
  box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.2);
  outline: none;
}

.search-button {
  background-color: #1890ff;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.search-button:hover {
  background-color: #40a9ff;
}

.symbol-container {
  margin-bottom: 15px;
}

.symbol-button {
  background-color: #f9f9f9;
  color: #555;
  border: 1px solid #d9d9d9;
  padding: 15px;
  border-radius: 6px;
  cursor: pointer;
  width: 100%;
  text-align: left;
  transition: all 0.3s ease;
  font-size: 1rem;
}

.symbol-button:hover {
  border-color: #1890ff;
  background-color: #f0f7ff;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.stock-data {
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  margin-top: 15px;
  border: 1px solid #eee;
}

.stock-data h2 {
  color: #1890ff;
  margin-bottom: 15px;
}

.stock-data p {
  color: #555;
  margin: 8px 0;
  font-size: 1rem;
  line-height: 1.5;
}

.loading {
  color: #1890ff;
  font-weight: bold;
  text-align: center;
  padding: 20px;
}

h3 {
  color: #1890ff;
  margin: 30px 0 20px;
  font-size: 1.5rem;
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .container {
    padding: 15px;
    margin: 20px;
  }

  .symbol-button {
    padding: 12px;
    font-size: 0.9rem;
  }

  .stock-data {
    padding: 15px;
  }
}
.price-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.price-card {
  background: white;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.price-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.price-label {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 10px;
}

.price-label i {
  color: #1890ff;
  font-size: 1.2rem;
}

.price-value {
  font-size: 1.5rem;
  font-weight: bold;
  color: #333;
  margin-bottom: 5px;
}

.price-value.highlight {
  font-size: 1.8rem;
  color: #1890ff;
}

.price-change {
  font-size: 1rem;
  font-weight: 500;
}

.price-up {
  color: #52c41a;
}

.price-down {
  color: #f5222d;
}

.stock-data h2 {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #1890ff;
  margin-bottom: 20px;
}

.stock-data h2 i {
  font-size: 1.8rem;
}

.price-grid {
  display: grid;
  /* 5개의 카드를 균등하게 배치 */
  grid-template-columns: repeat(5, 1fr);
  gap: 20px;
  margin-top: 20px;
}

/* 1400px 이하일 때 */
@media (max-width: 1400px) {
  .price-grid {
    grid-template-columns: repeat(3, 1fr); /* 3열로 변경 */
  }
}

/* 1024px 이하일 때 */
@media (max-width: 1024px) {
  .price-grid {
    grid-template-columns: repeat(2, 1fr); /* 2열로 변경 */
  }
}

/* 768px 이하일 때 */
@media (max-width: 768px) {
  .price-grid {
    grid-template-columns: 1fr; /* 1열로 변경 */
    gap: 15px;
  }

  .price-card {
    padding: 15px;
  }

  .price-value {
    font-size: 1.3rem;
  }

  .price-value.highlight {
    font-size: 1.5rem;
  }
}

.container {
  max-width: 1400px; /* 컨테이너 최대 너비 증가 */
  margin: 40px auto;
  padding: 20px;
}

.price-card {
  min-width: 200px; /* 최소 너비 설정 */
  background: white;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}
</style>
