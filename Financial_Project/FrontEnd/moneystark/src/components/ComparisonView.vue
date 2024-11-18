<template>
    <div>
      <h1>금리비교</h1>
      <div>
        <button @click="selectItem('deposit')">정기예금</button>
        <button @click="selectItem('saving')">정기적금</button>
      </div>
      <div>
        <DepositItem v-if="selectedItem === 'deposit'" />
        <SavingItem v-if="selectedItem === 'saving'" />
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from "vue";
  import { useProductStore } from "@/stores/product";
  import DepositItem from "./Compare/DepositItem.vue";
  import SavingItem from "./Compare/SavingItem.vue";
  
  const productStore = useProductStore();
  const selectedItem = ref(null);
  
  onMounted(() => {
    productStore.savedata();
  });
  
  const selectItem = (item) => {
    selectedItem.value = item;
  };
  </script>
  
  <style scoped></style>