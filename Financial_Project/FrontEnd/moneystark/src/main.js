import piniaPluginPersistedstate from "pinia-plugin-persistedstate";
import { createApp } from "vue";
import { createPinia } from "pinia";
import App from "./App.vue";
import router from "./router";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap";
import "@fortawesome/fontawesome-free/css/all.css";
import { createNaverMap } from "vue3-naver-maps";
import VueApexCharts from "vue3-apexcharts";
import '@mdi/font/css/materialdesignicons.css'
const app = createApp(App).use(createNaverMap, {
  clientId: "your clientId", // Required
  category: "ncp", // Optional
  subModules: [], // Optional
});
const pinia = createPinia();

pinia.use(piniaPluginPersistedstate);
// app.use(createPinia())
app.use(pinia);
app.use(router);
app.use(VueApexCharts);

app.mount("#app");
