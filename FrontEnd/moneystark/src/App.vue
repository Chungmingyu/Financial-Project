<script setup>
import { RouterLink, RouterView } from "vue-router";
</script>

<template>
  <header>
    <h1>MoneyStark</h1>

    <nav>
      <RouterLink to="/">Home</RouterLink>
      |
      <RouterLink to="/signup">회원가입</RouterLink>
      |
      <RouterLink to="/login">로그인</RouterLink>
    </nav>
  </header>

  <RouterView />
</template>

<style scoped></style>
