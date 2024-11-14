<template>
  <div>
    <h1>회원가입</h1>
    <form @submit.prevent="signUp">
      <div>
        <label for="username">ID :</label>
        <input type="text" id="username" v-model.trim="username" />
      </div>
      <div>
        <label for="password1">Password :</label>
        <input type="password" id="password1" v-model.trim="password1" />
      </div>
      <div>
        <label for="password2">Password Confirm :</label>
        <input type="password" id="password2" v-model.trim="password2" />
      </div>
      <button type="submit">회원가입</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useUserStore } from "@/stores/userStore.js";

const username = ref("");
const password1 = ref("");
const password2 = ref("");
const userStore = useUserStore();

const signUp = () => {
  const payload = {
    username: username.value,
    password1: password1.value,
    password2: password2.value,
  };
  userStore.signUp(payload);
};
</script>

<style scoped></style>
