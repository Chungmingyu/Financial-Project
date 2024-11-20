<template>
  <div id="app" class="relative">
    <div v-if="loading">
      <LoadingComponent />
    </div>
    <div v-else class="app-container">
      <NavVarComponent />
      <main class="main-content">
        <RouterView />
      </main>
      <div v-if="!showChatbot" class="chatbot-button" @click="toggleChatbot">
        <span>💬</span>
      </div>
      <div :class="['chatbot-popup', { active: showChatbot }]">
        <ChatBotView @close="toggleChatbot" />
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import NavVarComponent from "./components/NavVar/NavVarComponent.vue";
import LoadingComponent from "./components/NavVar/LoadingComponent.vue";
import ChatBotView from "./views/ChatBotView.vue";

const loading = ref(true);
const showChatbot = ref(false);
const router = useRouter();

const toggleChatbot = () => {
  showChatbot.value = !showChatbot.value;
};

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
});
import { useProductStore } from "@/stores/product";

const productStore = useProductStore();
onMounted(() => {
  if (!productStore.isDataSaved) {
    productStore.savedata();
    productStore.isDataSaved = true;
    productStore.isComponentVisible = true;
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
  margin-top: 100px;
  flex: 1;
  width: 100%;
  position: relative;
}

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

.chatbot-button:active {
  transform: scale(1.1);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.4);
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
.app-container {
  position: relative;
  z-index: 1;
}

.chatbot-popup {
  z-index: 1000;
}

.main-content {
  position: relative;
  z-index: 1;
}
</style>
