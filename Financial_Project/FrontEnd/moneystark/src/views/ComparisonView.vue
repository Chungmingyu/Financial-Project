<template>
  <div class="comparison-container">
    <h1>
      <i class="mdi mdi-chart-line"></i>
      금리비교
    </h1>
    <div class="nav-links">
      <button @click="selectItem('deposit')" :class="{ active: selectedItem === 'deposit' }" class="nav-button">
        <i class="mdi mdi-bank"></i>
        정기예금
      </button>
      <button @click="selectItem('saving')" :class="{ active: selectedItem === 'saving' }" class="nav-button">
        <i class="mdi mdi-piggy-bank"></i>
        정기적금
      </button>
    </div>
    <div class="component-container">
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
    productStore.savedata();
    productStore.isDataSaved = true;
    productStore.isComponentVisible = true;
  }
});
</script>

<style scoped>
.comparison-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
  animation: fadeIn 0.5s ease-out;
}

h1 {
  text-align: center;
  font-size: 2.5rem;
  color: #1890ff;
  margin: 40px 0;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
}

h1 i {
  font-size: 2.5rem;
}

.nav-links {
  display: flex;
  justify-content: center;
  margin: 40px 0;
  gap: 20px;
  padding: 0 20px;
}

.nav-button {
  padding: 15px 30px;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  font-size: 1.1rem;
  color: #555;
  background-color: #f0f0f0;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 160px;
  justify-content: center;
}

.nav-button i {
  font-size: 1.3rem;
}

.nav-button:hover {
  background-color: #e6f7ff;
  color: #1890ff;
  transform: translateY(-2px);
}

.nav-button.active {
  background-color: #1890ff;
  color: white;
  box-shadow: 0 4px 12px rgba(24, 144, 255, 0.3);
}

.component-container {
  animation: slideUp 0.5s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideUp {
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
  .nav-links {
    flex-direction: column;
    gap: 15px;
  }

  .nav-button {
    width: 100%;
  }

  h1 {
    font-size: 2rem;
  }

  h1 i {
    font-size: 2rem;
  }
}
</style>
