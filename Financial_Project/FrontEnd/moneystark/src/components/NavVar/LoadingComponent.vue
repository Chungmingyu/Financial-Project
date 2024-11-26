<template>
  <div>
    <div v-if="showLoader" class="loading-container">
      <div class="overlay"></div>
      <div class="loading-content">
        <div class="logo-container">
          <img src="@/assets/logo_black.png" alt="Logo" class="logo" />
        </div>
        <div class="loading-bar-container">
          <div class="loading-bar"></div>
        </div>
        <div class="loading-text">서비스를 준비 중입니다...</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

const showLoader = ref(true);

onMounted(() => {
  setTimeout(() => {
    showLoader.value = false;
  }, 4000); // 로딩 지속 시간 (ms)
});
</script>

<style scoped>
/* 배경 이미지 및 전체 화면 설정 */
.loading-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  /* background: url("@/assets/home/home3.jpg") no-repeat center center/cover; */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

/* 어두운 오버레이 */
.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5); /* 반투명 검정색 */
  z-index: 1;
}

/* 로딩 콘텐츠 */
.loading-content {
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
  color: white;
}

/* 로고 */
.logo-container {
  animation: pulse 2s infinite ease-in-out;
}

.logo {
  width: 300px;
  height: auto;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.7));
  opacity: 0.9;
}

/* 로딩 바 */
.loading-bar-container {
  width: 300px;
  height: 4px;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 10px;
  overflow: hidden;
  position: relative;
}

.loading-bar {
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, #ff7f50, #ff6347, #ffc400);
  animation: loading 1.5s infinite linear;
}

/* 로딩 텍스트 */
.loading-text {
  font-size: 1.1rem;
  font-family: "Spoqa Han Sans Neo", sans-serif;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.7);
  animation: fadeInOut 2s infinite;
}

/* 애니메이션 */
@keyframes loading {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}

@keyframes pulse {
  0%,
  100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
}

@keyframes fadeInOut {
  0%,
  100% {
    opacity: 0.5;
  }
  50% {
    opacity: 1;
  }
}
</style>
