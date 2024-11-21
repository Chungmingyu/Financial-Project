<template>
  <div>
    <h1>주식 정보</h1>

    <input type="text" id="" v-model="stockInput" />
    <button v-if="stockInput" @click.prevent="fetchStockData(stockInput)"></button>
    <div v-for="(stock, index) in store.stockData">
      <p>날짜 : {{ index }}</p>
      <p>고가 : {{ stock["2. high"] }}</p>
      <p>저가 : {{ stock["3. low"] }}</p>
      <p>물량 : {{ stock["5. volume"] }}</p>
      <hr />
      <!-- {{ stock }} -->
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useStockStore } from "../../stores/stock";

const stockInput = ref("");
const store = useStockStore();
const stockDataArray = store.stockDataArray;
const fetchStockData = function (stockInput) {
  store.fetchStockData(stockInput);
};
</script>

<style scoped></style>
