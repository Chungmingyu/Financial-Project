<template>
  <div class="page-container">
    <div class="content-container">
      <!-- 검색 섹션 -->
      <div class="search-section">
        <form @submit.prevent="handleSearch" class="search-box">
          <i class="mdi mdi-magnify search-icon"></i>
          <input type="text" v-model="searchInput" placeholder="코인명을 검색하세요 (예: 비트코인)" class="search-input" />
          <button type="submit" class="search-button">
            <i class="mdi mdi-magnify"></i>
            검색
          </button>
        </form>
      </div>

      <!-- 검색 결과 섹션 -->
      <div v-if="isSearching" class="search-results">
        <div class="search-header">
          <div class="search-result-summary">"{{ searchInput }}" 검색 결과: {{ filteredCoins.length }}건</div>
          <button @click="clearSearch" class="back-button">
            <i class="mdi mdi-keyboard-return"></i>
            기본 목록으로
          </button>
        </div>

        <div v-if="filteredCoins.length === 0" class="no-results">검색 결과가 없습니다.</div>

        <div v-else class="coins-grid">
          <div v-for="coin in filteredCoins" :key="coin.market" :class="['coin-card', { up: coin.change_rate > 0, down: coin.change_rate < 0 }]">
            <div class="card-header">
              <h3>{{ coin.korean_name }}</h3>
              <span class="market-code">{{ coin.market }}</span>
            </div>
            <div class="coin-info">
              <div class="price-info">
                <p class="current-price">{{ formatPrice(coin.current_price) }}원</p>
                <p class="change-rate" :class="{ up: coin.change_rate > 0, down: coin.change_rate < 0 }">
                  {{ coin.change_rate > 0 ? "▲" : "▼" }}
                  {{ Math.abs(coin.change_rate).toFixed(2) }}%
                </p>
                <p class="change-price" :class="{ up: coin.change_rate > 0, down: coin.change_rate < 0 }">{{ formatPrice(Math.abs(coin.change_price)) }}원</p>
              </div>
              <div class="chart-container">
                <CoinChart :market="coin.market" :current-price="coin.current_price" :is-up="coin.change_rate > 0" />
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 기본 코인 목록 섹션 -->
      <div v-else class="default-coins">
        <div class="intro-section">
          <h2>
            <i class="mdi mdi-bitcoin"></i>
            실시간 가상화폐 시세
          </h2>
          <p>국내 거래소의 실시간 가상화폐 가격 정보를 확인하세요.</p>
        </div>

        <div class="coins-grid">
          <div v-for="coin in coins" :key="coin.market" :class="['coin-card', { up: coin.change_rate > 0, down: coin.change_rate < 0 }]">
            <div class="card-header">
              <h3>{{ coin.korean_name }}</h3>
              <span class="market-code">{{ coin.market }}</span>
            </div>
            <div class="coin-info">
              <div class="price-info">
                <p class="current-price">{{ formatPrice(coin.current_price) }}원</p>
                <p class="change-rate" :class="{ up: coin.change_rate > 0, down: coin.change_rate < 0 }">
                  {{ coin.change_rate > 0 ? "▲" : "▼" }}
                  {{ Math.abs(coin.change_rate).toFixed(2) }}%
                </p>
                <p class="change-price" :class="{ up: coin.change_rate > 0, down: coin.change_rate < 0 }">{{ formatPrice(Math.abs(coin.change_price)) }}원</p>
              </div>
              <div class="chart-container">
                <CoinChart :market="coin.market" :current-price="coin.current_price" :is-up="coin.change_rate > 0" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import CoinChart from "./CoinChart.vue";

export default {
  name: "CoinData",
  components: {
    CoinChart,
  },
  data() {
    return {
      coins: [], // 기본 표시용 (10개)
      allCoins: [], // 전체 코인 데이터
      intervalId: null,
      isActive: true,
      searchInput: "", // 검색 입력값
      searchTerm: "", // 실제 검색에 사용될 값
    };
  },
  computed: {
    filteredCoins() {
      if (!this.searchInput) return [];

      const searchLower = this.searchInput.toLowerCase();
      return this.allCoins.filter((coin) => coin.korean_name.toLowerCase().includes(searchLower) || coin.market.toLowerCase().includes(searchLower));
    },
  },
  methods: {
    async fetchCoinData() {
      if (!this.isActive) return;

      try {
        const response = await fetch("http://127.0.0.1:8000/moneys/coin_data/");
        const data = await response.json();

        // 전체 데이터 저장
        this.allCoins = data.data;
        // 기본 표시용 10개
        this.coins = data.data.slice(0, 10);
      } catch (error) {
        console.error("코인 데이터 조회 실패:", error);
      }
    },
    formatPrice(price) {
      return price.toLocaleString();
    },
    startPolling() {
      this.isActive = true;
      this.fetchCoinData();
      this.intervalId = setInterval(this.fetchCoinData, 5000);
    },
    stopPolling() {
      this.isActive = false;
      if (this.intervalId) {
        clearInterval(this.intervalId);
        this.intervalId = null;
      }
    },
    handleSearch(e) {
      e.preventDefault();
      if (!this.searchInput.trim()) {
        this.isSearching = false;
        return;
      }
      this.isSearching = true;
    },
    clearSearch() {
      this.searchInput = "";
      this.isSearching = false;
    },
  },
  mounted() {
    this.startPolling();
  },
  beforeUnmount() {
    this.stopPolling();
  },
};
</script>

<style scoped>
.page-container {
  min-height: 100vh;
  background-color: #f5f7fa;
  padding: 40px 20px;
}

.content-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.search-section {
  margin-bottom: 40px;
}

.search-box {
  max-width: 800px;
  margin: 0 auto;
}
.search-icon {
  position: absolute;
  left: 15px;
  top: 50%;
  transform: translateY(-50%);
  color: #999;
  font-size: 20px;
}

.search-input {
  width: 100%;
  padding: 15px 20px 15px 45px;
  font-size: 1rem;
  border: 1px solid #e8e8e8;
  border-radius: 10px;
  background-color: #fff;
  transition: all 0.3s ease;
  color: #333;
}

.search-input:focus {
  outline: none;
  border-color: #1890ff;
  box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.2);
}

.search-input::placeholder {
  color: #999;
}
.search-button {
  padding: 0 35px;
  height: 50px;
  background-color: #1890ff;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  /* display: flex; */
  width: 25%;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
}
@media (max-width: 768px) {
  .search-section {
    padding: 0 15px;
  }

  .search-input {
    padding: 12px 15px 12px 40px;
    font-size: 0.9rem;
  }

  .search-icon {
    font-size: 18px;
  }
}

.search-box {
  position: relative;
  max-width: 600px;
  margin: 0 auto;
  display: flex;
  gap: 10px;
}
.intro-section {
  background: #ffffff;
  border-radius: 12px;
  padding: 30px;
  margin-bottom: 40px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.coins-grid,
.results-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
  gap: 24px;
  padding: 0;
}

.coin-card {
  background: #ffffff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.coin-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.price-info {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chart-container {
  height: 250px;
  border-radius: 8px;
  overflow: hidden;
}

@media (max-width: 1024px) {
  .content-container {
    padding: 0 16px;
  }

  .coins-grid,
  .results-grid {
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
  }
}

@media (max-width: 768px) {
  .page-container {
    padding: 20px 16px;
  }

  .content-container {
    padding: 0;
  }

  .coin-card {
    padding: 20px;
  }

  .price-info {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .chart-container {
    height: 200px;
  }
}

.up {
  color: #ff4d4f;
}

.down {
  color: #1890ff;
}

.current-price {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0;
}

.change-rate,
.change-price {
  font-size: 1rem;
  margin: 0;
}

.market-code {
  color: #666;
  font-size: 0.9rem;
}
.search-results {
  margin-top: 20px;
  padding: 20px;
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.search-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 8px;
}

.search-result-summary {
  color: #666;
  font-size: 1rem;
}

.back-button {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background-color: #fff;
  color: #1890ff;
  border: 1px solid #1890ff;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

.back-button:hover {
  background-color: #1890ff;
  color: #fff;
}

.results-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 20px;
}

.coin-card {
  max-width: 800px;
  margin: 0 auto;
}

.chart-container {
  width: 100%;
  height: 300px;
  margin-top: 20px;
}

.no-results {
  text-align: center;
  padding: 40px;
  color: #666;
  font-size: 1.1rem;
  background: #f9f9f9;
  border-radius: 8px;
  margin: 20px 0;
}

@media (max-width: 768px) {
  .search-header {
    flex-direction: column;
    gap: 10px;
  }

  .back-button {
    width: 100%;
    justify-content: center;
  }
}
</style>
