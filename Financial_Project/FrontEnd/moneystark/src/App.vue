<template>
  <div v-if="loading">
    <LoadingComponent />
  </div>
  <div v-else>
    <NavVarComponent />
    <RouterView />
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import NavVarComponent from "./components/NavVar/NavVarComponent.vue";
import LoadingComponent from "./components/NavVar/LoadingComponent.vue";

const loading = ref(true);
const router = useRouter();

onMounted(() => {
  setTimeout(() => {
    loading.value = false;
    router.push({ name: "home" });
  }, 11000);
});
</script>

<style scoped></style>
