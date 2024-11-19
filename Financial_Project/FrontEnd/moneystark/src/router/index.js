import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import LogInView from "@/views/LogInView.vue";
import SignUpView from "@/views/SignUpView.vue";
import ChartView from "@/components/ChartView.vue";
import ComparisonView from "@/components/ComparisonView.vue";
import ProductSuggestionView from "@/components/ProductSuggestionView.vue";
import CurrencyCalculatorView from "@/components/CurrencyCalculatorView.vue";
import BankView from "@/components/BankView.vue";
import BankMapView from "@/views/BankMapView.vue";
import NavbarView from "@/views/NavbarView.vue";

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
      path: "/chart",
      name: "ChartView",
      component: ChartView,
    },
    {
      path: "/comparison",
      name: "ComparisonView",
      component: ComparisonView,
    },
    {
      path: "/suggestion",
      name: "ProductSuggestionView",
      component: ProductSuggestionView,
    },
    {
      path: "/currency",
      name: "CurrencyCalculatorView",
      component: CurrencyCalculatorView,
    },
    {
      path: "/bank",
      name: "BankView",
      component: BankView,
    },
    {
      path: "/bankmap",
      name: "BankMapView",
      component: BankMapView,
    },
    {
      path: "/navbar",
      name: "NavbarView",
      component: NavbarView,
    },
  ],
});

export default router;
