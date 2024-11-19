<template>
  <div>
    <h1>환율 계산기</h1>
    <ExchangeCalculator />
  </div>
</template>

<script setup>
import ExchangeCalculator from "@/components/Exchange/ExchangeCalculation.vue";
</script>

<style scoped>
h1 {
  text-align: center;
  margin-bottom: 20px;
}
</style>
