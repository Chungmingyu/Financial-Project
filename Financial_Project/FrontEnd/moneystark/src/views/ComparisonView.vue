<template>
  <div>
    <h1>금리비교</h1>
    <div class="nav-links">
      <span @click="selectItem('deposit')" :class="{ active: selectedItem === 'deposit' }">정기예금</span>
      <span @click="selectItem('saving')" :class="{ active: selectedItem === 'saving' }">정기적금</span>
    </div>
    <div>
      <component :is="selectedComponent" v-if="productStore.isComponentVisible" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useProductStore } from "@/stores/product";
import DepositList from "@/components/Compare/DepositList.vue";
import SavingList from "@/components/Compare/SavingList.vue";

const productStore = useProductStore();
const selectedItem = ref("deposit"); // 초기값을 'deposit'으로 설정

const selectedComponent = computed(() => {
  if (selectedItem.value === "deposit") {
    return DepositList;
  } else if (selectedItem.value === "saving") {
    return SavingList;
  } else {
    return null;
  }
});

const selectItem = (item) => {
  selectedItem.value = item;
};

onMounted(() => {
  if (!productStore.isDataSaved) {
    setTimeout(() => {
      productStore.savedata();
      productStore.isDataSaved = true;
    }, 5000); // 3초 지연
    productStore.isComponentVisible = true;
  }
});
</script>

<style scoped>
h1 {
  text-align: center;
  margin-bottom: 20px;
}

.nav-links {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.nav-links span {
  margin: 0 15px;
  cursor: pointer;
  font-size: 18px;
  color: #007bff;
}

.nav-links span.active {
  font-weight: bold;
  text-decoration: underline;
}
</style>
