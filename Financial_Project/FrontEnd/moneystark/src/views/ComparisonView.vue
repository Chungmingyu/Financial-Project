<template>
  <div class="image-container">
    <div class="image-overlay">
      <h2>
        <i class="mdi mdi-chart-line"></i>
        금리 비교
      </h2>
      <p>다양한 금융사의 최신 금리 데이터를 바탕으로 최적의 예적금 상품을 추천드립니다.</p>
    </div>
  </div>
  <div class="comparison-container">
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

.image-container {
  position: relative;
  width: 70%;
  height: 400px; /* 이미지 높이 설정 */
  margin: 0 auto; /* 가로 중앙 정렬 */
  margin-top: 40px;
  background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), /* 어두운 레이어 추가 */ url("@/assets/compare/deposit.jpg") no-repeat center center/cover; /* 배경 이미지 설정 */
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
}

.image-overlay p {
  font-size: 22px;
  margin: 0;
}
</style>
