<template>
  <div>
    <div v-if="showLoader" class="loading-container">
      <div class="spinner"></div>
    </div>
    <video v-else class="video-container" src="@/assets/나의 비디오-2.mp4" autoplay muted controls></video>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

const showLoader = ref(true);

onMounted(() => {
  setTimeout(() => {
    showLoader.value = false;
  }, 3000); // 3초 후 로더 숨기기
});
</script>

<style scoped>
/* 로더 스타일 */
.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #000;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 5px solid rgba(255, 255, 255, 0.3);
  border-top: 5px solid #fff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

/* 비디오 스타일 */
.video-container {
  width: 100%;
  height: auto;
  background-color: #000;
}

/* 애니메이션 */
@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
