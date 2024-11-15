import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import LogInView from "@/views/LogInView.vue";
import SignUpView from "@/views/SignUpView.vue";
import HomeView2 from "@/views/HomeView2.vue";
import HomeView3 from "@/views/HomeView3.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/login",
      name: "LogInView",
      component: LogInView,
    },
    {
      path: "/signup",
      name: "SignUpView",
      component: SignUpView,
    },
    {
      path: "/test",
      name: "home2",
      component: HomeView2,
    },
    {
      path: "/test/test",
      name: "home3",
      component: HomeView3,
    },
  ],
});

export default router;
