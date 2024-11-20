<template>
  <div>
    <div v-if="showLoader" class="loading-container">
      <div class="loading-content">
        <div class="logo-container">
          <img src="@/assets/logo_black.png" alt="Logo" class="logo" />
        </div>
        <div class="loading-bar-container">
          <div class="loading-bar"></div>
        </div>
        <div class="loading-text geist-mono">Loading...</div>
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
  }, 3000);
});
</script>

<style scoped>
.loading-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100vh;
  background: white;
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.loading-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2rem;
}

.logo-container {
  animation: pulse 2s infinite;
}

.logo {
  width: 200px;
  height: auto;
}

.loading-bar-container {
  width: 200px;
  height: 3px;
  background: #f0f0f0;
  border-radius: 10px;
  overflow: hidden;
}

.loading-bar {
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, #7700ff, #4e90ff);
  animation: loading 2s infinite;
}

.loading-text {
  font-size: 1.2rem;
  color: #333;
  letter-spacing: 3px;
  animation: fadeInOut 2s infinite;
}

@keyframes loading {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}

@keyframes pulse {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
  100% {
    transform: scale(1);
  }
}

@keyframes fadeInOut {
  0%, 100% {
    opacity: 0.3;
  }
  50% {
    opacity: 1;
  }
}
</style>