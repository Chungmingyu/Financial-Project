<template>
  <div class="image-container">
    <div class="image-overlay">
      <h2>
        <i class="mdi mdi-chart-line"></i>
        주식 트렌드와 실시간 차트
      </h2>
      <p>종목별 데이터와 시장 흐름을 시각화된 차트로 확인하고, 관련 뉴스를 통해 더 깊은 통찰을 얻으세요.</p>
    </div>
  </div>
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

.image-container {
  position: relative;
  width: 70%;
  height: 400px; /* 이미지 높이 설정 */
  margin: 0 auto; /* 가로 중앙 정렬 */
  margin-top: 40px;
  background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), /* 어두운 레이어 추가 */ url("@/assets/stock/stock.jpg") no-repeat center center/cover; /* 배경 이미지 설정 */
}

/* 이미지 위 텍스트 스타일 */
.image-overlay {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  text-align: center;
  /* background: rgba(0, 0, 0, 0.5); 반투명 배경 */
  padding: 20px;
  border-radius: 10px;
  /* box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3); */
}

.image-overlay h2 {
  font-size: 36px;
  margin-bottom: 10px;
  color: white;
}

.image-overlay p {
  font-size: 22px;
  margin: 0;
}
</style>
