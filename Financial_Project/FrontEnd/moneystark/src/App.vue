<template>
  <div v-if="loading">
    <LoadingComponent />
  </div>
  <div v-else class="app-container">
    <NavVarComponent />
    <main class="main-content">
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import NavVarComponent from "./components/NavVar/NavVarComponent.vue";
import LoadingComponent from "./components/NavVar/LoadingComponent.vue";

const loading = ref(true);
const router = useRouter();

onMounted(() => {
  // 로컬 스토리지에서 로딩 여부 확인
  const hasLoaded = localStorage.getItem("hasLoaded");

  if (!hasLoaded) {
    // 처음 로딩일 경우
    setTimeout(() => {
      loading.value = false;
      router.push({ name: "home" });
      localStorage.setItem("hasLoaded", "true"); // 로딩 완료 상태 저장
    }, 3000);
  } else {
    // 이미 로딩이 완료된 경우
    loading.value = false;
  }
});
</script>

<style scoped>
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  margin-top: 100px; /* NavVarComponent의 높이만큼 여백 설정 */
  flex: 1;
  width: 100%;
  position: relative;
}
</style>
