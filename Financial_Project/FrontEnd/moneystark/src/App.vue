<template>
  <div>
    <RouterLink :to="{name:'home'}"/>
  </div>
  <RouterView/>
</template>

<script setup>
import { RouterLink, RouterView } from 'vue-router';
</script>

<style scoped>

</style>