<template>
  <div id="app" class="relative">
    <!-- 로딩 컴포넌트 -->
    <div v-if="loading">
      <LoadingComponent />
    </div>
    <!-- 애플리케이션 컨텐츠 -->
    <div v-else class="app-container">
      <!-- Navbar -->
      <NavVarComponent />
      <!-- 메인 컨텐츠 -->
      <main class="main-content">
        <RouterView />
      </main>
      <!-- 챗봇 버튼 -->
      <div v-if="!showChatbot" class="chatbot-button" @click="toggleChatbot">
        <span>💬</span>
      </div>
      <!-- 챗봇 팝업 -->
      <div :class="['chatbot-popup', { active: showChatbot }]">
        <ChatBotView @close="toggleChatbot" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter, RouterView } from "vue-router";
import NavVarComponent from "./components/NavVar/NavVarComponent.vue";
import LoadingComponent from "./components/NavVar/LoadingComponent.vue";
import ChatBotView from "./views/ChatBotView.vue";
import { useProductStore } from "@/stores/product";

const loading = ref(true);
const showChatbot = ref(false);
const router = useRouter();

const toggleChatbot = () => {
  showChatbot.value = !showChatbot.value;
};

const productStore = useProductStore();
onMounted(() => {
  const hasLoaded = localStorage.getItem("hasLoaded");

  if (!hasLoaded) {
    setTimeout(() => {
      loading.value = false;
      router.push({ name: "home" });
      localStorage.setItem("hasLoaded", "true");
    }, 3000);
  } else {
    loading.value = false;
  }

  if (!productStore.isDataSaved) {
    productStore.savedata();
    productStore.isDataSaved = true;
    productStore.isComponentVisible = true;
  }
});
</script>

<style scoped>
/* App 기본 스타일 */
#app {
  min-height: 100vh; /* 화면 전체를 채움 */
}

/* 메인 컨텐츠 */
.main-content {
  flex: 1;
  width: 100%;
  position: relative;
  /* Navbar 높이에 의한 마진 제거 */
  margin-top: 0;
  z-index: 1;
}

/* 챗봇 버튼 스타일 */
.chatbot-button {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background-color: #ffbf00;
  color: white;
  border-radius: 50%;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  font-size: 24px;
  z-index: 1000;
  transition: all 0.3s ease;
}

.chatbot-button:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
}

.chatbot-popup {
  position: fixed;
  bottom: 80px;
  right: 20px;
  width: 450px;
  height: 650px;
  background-color: white;
  border: 1px solid #ccc;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  z-index: 1000;
  transition: all 0.3s ease;
  transform: scale(0);
  opacity: 0;
}

.chatbot-popup.active {
  transform: scale(1);
  opacity: 1;
}

/* Navbar 높이에 따른 간격 제거 */
.app-container {
  position: relative;
  z-index: 1;
  padding-top: 0; /* Navbar 높이에 의한 패딩 제거 */
}
</style>
