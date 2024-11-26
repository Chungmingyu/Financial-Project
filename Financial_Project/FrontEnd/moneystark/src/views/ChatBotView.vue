<template>
  <div class="chatbot">
    <div class="chatbot-header">
      <span>재비스</span>
      <button @click="$emit('close')">X</button>
    </div>
    <div class="messages">
      <div v-for="(message, index) in messages" :key="index" :class="['message', message.type]">
        <div class="message-content" v-html="renderMarkdown(message.text)"></div>
      </div>
    </div>
    <div class="input-container">
      <input v-model="userInput" @keyup.enter="sendMessage" placeholder="무엇이든 물어보세요!" />
      <button @click="sendMessage">물어보기</button>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import OpenAI from "openai";
import { marked } from "marked";

const API_KEY = import.meta.env.VITE_CHATGPT_API;
const openai = new OpenAI({
  apiKey: API_KEY,
  dangerouslyAllowBrowser: true,
});

export default {
  setup() {
    const messages = ref([{ text: "안녕하세요 MONEY INDUSTRY입니다! 무엇을 도와드릴까요?", type: "bot" }]);
    const userInput = ref("");

    const sendMessage = async () => {
      if (userInput.value.trim() === "") return;

      messages.value.push({ text: userInput.value, type: "user" });

      const stream = await openai.chat.completions.create({
        model: "gpt-4o-mini",
        messages: [
          { role: "system", content: "MONEY INDUSTRY는 재테크를 확인하고 추천할 수 있는 사이트입니다." },
          { role: "user", content: userInput.value },
        ],
        stream: true,
      });

      let botMessage = "";
      for await (const chunk of stream) {
        botMessage += chunk.choices[0]?.delta?.content || "";
      }

      messages.value.push({ text: botMessage, type: "bot" });

      userInput.value = "";
    };

    const renderMarkdown = (text) => {
      return marked(text);
    };

    return {
      messages,
      userInput,
      sendMessage,
      renderMarkdown,
    };
  },
};
</script>

<style scoped>
.chatbot {
  display: flex;
  flex-direction: column;
  height: 100%;
  background-color: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  font-family: "Arial", sans-serif;
}

.chatbot-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  background-color: #f08d0dc9;
  color: rgb(0, 0, 0);
  font-weight: bold;
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
}

.messages {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
  background-color: #fff;
}

.input-container {
  display: flex;
  padding: 10px;
  background-color: #fff;
  border-top: 1px solid #ccc;
}

input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  margin-right: 10px;
}

button {
  padding: 10px 20px;
  background-color: #f08d0dc9;
  color: black;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.message {
  display: flex;
  margin-bottom: 10px;
  position: relative;
  padding: 10px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.message.user {
  justify-content: flex-end;
}

.message.bot {
  justify-content: flex-start;
}

.message-content {
  max-width: 70%;
  padding: 10px;
  border-radius: 10px;
  background-color: #e0e0e0;
  position: relative;
}

.message.user .message-content {
  background-color: #f08d0dc9;
  color: white;
}

.message.bot .message-content {
  background-color: #f1f1f1;
  color: black;
}

.message.user .message-content::after {
  content: "";
  position: absolute;
  top: 50%;
  right: -10px;
  transform: translateY(-50%);
  border-width: 10px;
  border-style: solid;
  border-color: transparent transparent transparent #f08e0d00;
}

.message.bot .message-content::after {
  content: "";
  position: absolute;
  top: 50%;
  left: -10px;
  transform: translateY(-50%);
  border-width: 10px;
  border-style: solid;
  border-color: transparent #f1f1f1 transparent transparent;
}
</style>
