import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import LogInView from "@/views/LogInView.vue";
import SignUpView from "@/views/SignUpView.vue";
import ChartView from "@/views/ChartView.vue";
import ComparisonView from "@/views/ComparisonView.vue";
import ProductSuggestionView from "@/views/ProductSuggestionView.vue";
import CurrencyCalculatorView from "@/views/CurrencyCalculatorView.vue";
import BankView from "@/views/BankView.vue";
import BankMapView from "@/views/BankMapView.vue";
import UserDetailView from "@/views/UserDetailView.vue";
import UserChangeView from "@/views/UserChangeView.vue";
import NewsView from "@/views/NewsView.vue";
import StockComponent from "../components/stock/stockComponent.vue";
import CoinComponent from "../components/stock/coinComponent.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/home",
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
      path: "/user",
      name: "UserDetailView",
      component: UserDetailView,
    },
    {
      path: "/userchange",
      name: "UserChangeView",
      component: UserChangeView,
    },
    {
      path: "/news",
      name: "news",
      component: NewsView,
    },
    {
      path: "/stock",
      name: "StockComponent",
      component: StockComponent,
    },
    {
      path: "/coin",
      name: "CoinComponent",
      component: CoinComponent,
    },
  ],
});

export default router;
