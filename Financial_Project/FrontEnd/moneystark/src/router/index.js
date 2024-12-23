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
// import StockComponent from "../components/stock/stockComponent.vue";
// import CoinComponent from "../components/stock/coinComponent.vue";
import BoardView from "../views/BoardView.vue";
import BoardsCreate from "../components/boards/BoardsCreate.vue";
import StockView from "../views/StockView.vue";
import CoinData from "../components/stock/CoinData.vue";
import Surveys from "../components/Surveys/Surveys.vue";
import BoardsListItem from "../components/boards/BoardsListItem.vue";
import HomeData from "../components/stock/HomeData.vue";
import UserDetailByNickname from "@/views/UserDetailByNickname.vue";
import StyleView from "../views/StyleView.vue";

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
      name: "StockView",
      component: StockView,
    },
    {
      path: "/homedata",
      name: "HomeData",
      component: HomeData,
    },
    {
      path: "/coin",
      name: "CoinData",
      component: CoinData,
      meta: { keepAlive: true },
    },
    {
      path: "/boards",
      name: "BoardView",
      component: BoardView,
    },
    {
      path: "/boards/create",
      name: "BoardsCreate",
      component: BoardsCreate,
    },
    {
      path: "/surveys",
      name: "Surveys",
      component: Surveys,
    },
    {
      path: "/boards/:id",
      name: "BoardsListItem",
      component: BoardsListItem,
    },
    {
      path: "/user/:nickname",
      name: "UserDetailByNickname",
      component: UserDetailByNickname,
      props: true, // 닉네임을 props로 전달
    },
    {
      path: "/style",
      name: "StyleView",
      component: StyleView,
    },
  ],
});

export default router;
