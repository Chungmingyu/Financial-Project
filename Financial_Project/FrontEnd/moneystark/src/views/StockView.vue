<template>
  <div class="stock-page">
    <h2>
      <i class="mdi mdi-chart-line"></i>
      해외 주식 정보 조회
    </h2>
    <p class="subtitle">실시간 해외 주식 시세를 확인하세요</p>
    <StockData />
  </div>
</template>

<script setup>
import StockData from "../components/stock/StockData.vue";
</script>

<style scoped>
.stock-page {
  max-width: 1200px;
  margin: 40px auto;
  padding: 20px;
  font-family: "Noto Sans KR", sans-serif;
  animation: fadeInUp 0.5s ease-out;
}

h2 {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  color: #1890ff;
  margin-bottom: 10px;
  font-size: 2rem;
}

h2 i {
  font-size: 2rem;
}

.subtitle {
  text-align: center;
  color: #666;
  margin-bottom: 30px;
  font-size: 1.1rem;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .stock-page {
    margin: 20px auto;
    padding: 15px;
  }

  h2 {
    font-size: 1.5rem;
  }

  h2 i {
    font-size: 1.5rem;
  }

  .subtitle {
    font-size: 1rem;
  }
}
</style>