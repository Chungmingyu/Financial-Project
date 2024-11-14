<template>
  <div>
    <h1>로그인</h1>
    <form @submit.prevent="logIn">
      <div>
        <label for="id">ID : </label>
        <input type="text" id="id" v-model.trim="username" />
      </div>
      <div>
        <label for="password">Password : </label>
        <input type="password" id="password" v-model.trim="password" />
      </div>
      <button type="submit">로그인</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useUserStore } from "@/stores/userStore.js";
const username = ref("");
const password = ref("");
const userStore = useUserStore();
const logIn = function () {
  const payload = {
    username: username.value,
    password: password.value,
  };
  userStore.logIn(payload);
};
</script>

<style scoped></style>
