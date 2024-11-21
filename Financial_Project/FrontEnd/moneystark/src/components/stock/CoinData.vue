<template>
  <div class="container">
    <div v-for="coin in coins" :key="coin.market" :class="['coin-card', { up: coin.change_rate > 0, down: coin.change_rate < 0 }]">
      <div class="card-header">
        <h3>{{ coin.korean_name }}</h3>
        <span class="market-code">{{ coin.market }}</span>
      </div>
      <div class="coin-info">
        <div class="price-info">
          <p class="current-price">{{ formatPrice(coin.current_price) }}원</p>
          <p class="change-rate" :class="{ up: coin.change_rate > 0, down: coin.change_rate < 0 }">{{ coin.change_rate > 0 ? "▲" : "▼" }} {{ Math.abs(coin.change_rate).toFixed(2) }}%</p>
          <p class="change-price" :class="{ up: coin.change_rate > 0, down: coin.change_rate < 0 }">{{ formatPrice(Math.abs(coin.change_price)) }}원</p>
        </div>
        <div class="chart-container">
          <CoinChart :market="coin.market" :current-price="coin.current_price" :is-up="coin.change_rate > 0" />
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
      coins: [],
      intervalId: null,
      isActive: true,
    };
  },
  methods: {
    async fetchCoinData() {
      if (!this.isActive) return;

      try {
        const response = await fetch("http://127.0.0.1:8000/moneys/coin_data/");
        const data = await response.json();

        // 처음 10개만 선택
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
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  background: #1a1a1a;
  min-height: 100vh;
}

.coin-card {
  border: 1px solid #333;
  border-radius: 12px;
  padding: 25px;
  margin-bottom: 25px;
  background: #242424;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
}

.coin-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.3);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #333;
}

.card-header h3 {
  font-size: 1.5rem;
  font-weight: 600;
  margin: 0;
  color: #fff;
}

.market-code {
  color: #999;
  font-size: 0.9rem;
}

.coin-info {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 40px;
  min-height: 300px;
}

.price-info {
  flex: 1;
  padding-top: 20px;
}

.current-price {
  font-size: 2rem;
  font-weight: 700;
  margin: 0 0 15px 0;
  color: #fff;
}

.change-rate,
.change-price {
  font-size: 1.2rem;
  margin: 8px 0;
  font-weight: 500;
}

.up {
  color: #ff5252;
}

.down {
  color: #2962ff;
}

.chart-container {
  width: 600px;
  height: 300px;
  flex-shrink: 0;
  background: #242424;
  border-radius: 12px;
  padding: 15px;
  border: 1px solid #333;
}

@media (max-width: 768px) {
  .coin-info {
    flex-direction: column;
    min-height: auto;
  }

  .chart-container {
    width: 100%;
    height: 250px;
    margin-top: 20px;
  }
}
</style>
