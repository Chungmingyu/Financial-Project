<template>
  <div>
    <!-- 사용자 입력 -->
    <input type="text" v-model="store.coinSymbol" placeholder="코인 심볼 (예: BTC)" />
    <input type="text" v-model="store.coinMarket" placeholder="시장 (예: USD)" />
    <button @click="fetchCryptoData">코인 정보 가져오기</button>

    <!-- 로딩 상태 -->
    <div v-if="store.loading">로딩 중...</div>

    <!-- 에러 메시지 -->
    <div v-if="store.error" class="error">{{ store.error }}</div>

    <!-- 데이터 출력 -->
    <div v-if="store.cryptoDataArray.length > 0">
      <h3>코인 데이터:</h3>
      <ul>
        <li v-for="data in store.cryptoDataArray" :key="data.time">시간: {{ data.time }}, 가격: {{ data["1a. price (USD)"] }}</li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { useCryptoStore } from "../../stores/coin";

// Pinia 스토어 연결
const store = useCryptoStore();

// 데이터 가져오는 함수
const fetchCryptoData = () => {
  store.fetchCryptoData(); // store의 상태를 사용
};
</script>

<style scoped>
.error {
  color: red;
}
</style>
