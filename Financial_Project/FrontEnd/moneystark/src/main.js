import piniaPluginPersistedstate from "pinia-plugin-persistedstate";
import { createApp } from "vue";
import { createPinia } from "pinia";
import App from "./App.vue";
import router from "./router";
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap'
import { createNaverMap } from "vue3-naver-maps";
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

app.mount("#app");
