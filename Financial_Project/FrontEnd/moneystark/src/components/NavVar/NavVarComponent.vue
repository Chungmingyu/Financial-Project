<template>
  <header>
    <nav class="navbar bg-body-tertiary fixed-top" style="padding: 0" :class="{ hidden: isNavbarHidden }">
      <div class="container-fluid" style="padding: 0">
        <a class="navbar-brand" style="padding: 0" @click.prevent="$router.push({ name: 'home' })"><img src="@/assets/logo_black.png" style="padding: 0; height: 100px" /></a>
        <div style="display: flex; width: 600px; justify-content: space-between">
          <button class="btn geist-mono" :class="{ 'active-menu': $route.name === 'ChartView' }" @click.prevent="$router.push({ name: 'ChartView' })">차트</button>
          <button class="btn geist-mono" :class="{ 'active-menu': $route.name === 'CurrencyCalculatorView' }" @click.prevent="$router.push({ name: 'CurrencyCalculatorView' })">환율 계산기</button>
          <button class="btn geist-mono" :class="{ 'active-menu': $route.name === 'ComparisonView' }" @click.prevent="$router.push({ name: 'ComparisonView' })">금리 비교</button>
          <button class="btn geist-mono" :class="{ 'active-menu': $route.name === 'BankView' }" @click.prevent="$router.push({ name: 'BankView' })">근처 은행</button>
          <button class="btn geist-mono" :class="{ 'active-menu': $route.name === 'ProductSuggestionView' }" @click.prevent="$router.push({ name: 'ProductSuggestionView' })">상품 추천</button>
          <button class="btn geist-mono" :class="{ 'active-menu': $route.name === 'BankMapView' }" @click.prevent="$router.push({ name: 'BankMapView' })">지도</button>
          <button class="btn geist-mono" :class="{ 'active-menu': $route.name === 'StockComponent' }" @click.prevent="$router.push({ name: 'StockComponent' })">주식 정보</button>
          <button class="btn geist-mono" :class="{ 'active-menu': $route.name === 'CoinComponent' }" @click.prevent="$router.push({ name: 'CoinComponent' })">코인 정보</button>
        </div>
        <button class="navbar-toggler" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasNavbar" aria-controls="offcanvasNavbar" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon white"></span>
        </button>

        <div class="offcanvas offcanvas-end" tabindex="-1" id="offcanvasNavbar" aria-labelledby="offcanvasNavbarLabel">
          <div class="offcanvas-header">
            <h5 class="offcanvas-title" id="offcanvasNavbarLabel">Offcanvas</h5>
            <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
          </div>
          <div class="offcanvas-body">
            <ul class="navbar-nav justify-content-end flex-grow-1 pe-3">
              <li class="nav-item">
                <!-- 로그인 상태에 따라 버튼 토글 -->
                <button v-if="!isLoggedIn" class="nav-link active" aria-current="page" @click.prevent="navigateToLogin">로그인</button>
                <div v-else>
                  <button class="nav-link active" @click.prevent="handlerLogout">로그아웃</button>
                  <br />
                  <button class="nav-link active" @click.prevent="handlerUser">회원정보</button>
                </div>
              </li>
              <li class="nav-item">
                <a class="nav-link" href="#"></a>
              </li>
              <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">Dropdown</a>
                <ul class="dropdown-menu">
                  <li><a class="dropdown-item" href="#">Action</a></li>
                  <li><a class="dropdown-item" href="#">Another action</a></li>
                  <li><hr class="dropdown-divider" /></li>
                  <li><a class="dropdown-item" href="#">Something else here</a></li>
                </ul>
              </li>
            </ul>
            <form class="d-flex mt-3" role="search">
              <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search" />
              <button class="btn btn-outline-success" type="submit">Search</button>
            </form>
          </div>
        </div>
      </div>
    </nav>
  </header>
</template>

<script>
import { ref, onMounted, onUnmounted } from "vue";
import ScrollMagic from "scrollmagic";
import { gsap } from "gsap";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap";
import { useUserStore } from "@/stores/user";
import { useRouter } from "vue-router";

export default {
  name: "NavVarComponent",
  props: {
    isNavbarHidden: {
      type: Boolean,
      required: true,
    },
  },
  setup() {
    const isNavbarHidden = ref(false);
    const gradientOpacity = ref(0);
    const isReveal1Visible = ref(false);
    const isReveal2Visible = ref(false);
    const store = useUserStore();
    const router = useRouter();

    const navigateToLogin = () => {
      router.push({ name: "LogInView" });
    };

    const handlerLogout = () => {
      store.logout();
      window.location.href = "/home";
      console.log("홈으로 이동");
    };

    const handlerUser = () => {
      window.location.href = "/user";
    };
    // ScrollMagic 설정
    const initScrollMagic = () => {
      const controller = new ScrollMagic.Controller();

      // Scene 1: #trigger1을 트리거로 설정하여 스크롤 시 첫 번째 요소 보이게
      new ScrollMagic.Scene({
        triggerElement: "#trigger1",
        triggerHook: 0.9,
        duration: "80%",
        offset: 50,
      })
        .on("enter", () => {
          isReveal1Visible.value = true;
        })
        .on("leave", () => {
          isReveal1Visible.value = false;
        })
        .addTo(controller);

      // Scene 2: #trigger2를 트리거로 설정하여 두 번째 요소 보이게
      new ScrollMagic.Scene({
        triggerElement: "#trigger2",
        triggerHook: 0.9,
        offset: 50,
        reverse: false,
      })
        .on("enter", () => {
          isReveal2Visible.value = true;
        })
        .addTo(controller);
    };

    // 스크롤 이벤트 핸들러
    const handleScroll = () => {
      const imageSection = document.querySelector(".image-container");
      if (!imageSection) return;

      const imageSectionBottom = imageSection.offsetTop + imageSection.offsetHeight;
      const scrollPosition = window.scrollY;
      const windowHeight = window.innerHeight;

      // Navbar 숨김/표시 처리
      isNavbarHidden.value = scrollPosition > imageSectionBottom;

      // 그라데이션 opacity 계산
      gradientOpacity.value = Math.min(scrollPosition / windowHeight, 1);
    };

    onMounted(() => {
      initScrollMagic();
      window.addEventListener("scroll", handleScroll);
    });

    onUnmounted(() => {
      window.removeEventListener("scroll", handleScroll);
    });

    // text효과
    onMounted(() => {
      // 페이지가 로드되면 active 클래스 추가
      document.querySelectorAll(".texts").forEach((item) => {
        item.classList.add("active");
      });
    });
    return {
      isNavbarHidden,
      gradientOpacity,
      isReveal1Visible,
      isReveal2Visible,
      isLoggedIn: store.isLoggedIn,
      logout: store.logout,
      navigateToLogin,
      handlerLogout,
      handlerUser,
    };
  },
};
</script>

<style>
.navbar-toggler-icon {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 30 30'%3E%3Cpath stroke='white' stroke-width='2' d='M4 7h22M4 15h22M4 23h22'/%3E%3C/svg%3E");
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: Arial, sans-serif;
}

.scrollContent {
  margin: 0 auto;
  width: 100%;
}

#titlechart2 {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100vw;
  min-height: 100vh; /* 화면 크기만큼 영역을 채우도록 설정 */
  background: linear-gradient(black, rgb(0, 0, 49));
}

.image-container {
  position: relative;
  width: 100%;
  height: 100vh; /* 배경 이미지 영역을 화면 전체 크기만큼 설정 */
  display: flex;
  align-items: center;
  justify-content: center;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  color: white;
}

.image-container img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  position: absolute;
  top: 0;
  left: 0;
}

.gradient-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(to bottom, rgba(0, 0, 0, 0) 0%, rgba(0, 0, 0, 1) 100%);
  pointer-events: none;
  z-index: 2;
  transition: opacity 0.8s ease-in-out;
}

.box2 {
  width: 100%;
  height: 200px;
  margin: 20px auto;
  background-color: #ccc;
  text-align: center;
  line-height: 200px;
  font-size: 24px;
  opacity: 0;
  transition: all 1s ease-in-out;
}

.box2.visible {
  opacity: 1;
}

.blue {
  background-color: #4e90ff;
}

.green {
  background-color: #00d084;
}

.spacer {
  height: 150px;
}

.navbar {
  position: fixed;
  width: 100%;
  top: 0;
  transition: transform 0.5s ease-in-out, opacity 0.5s ease-in-out;
}

.navbar.hidden {
  transform: translateY(-100%);
  opacity: 0;
}

/* text 효과 */
.texts {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  color: black;
  font-size: 50px;
}

.texts span {
  opacity: 0;
  transform: translateY(20px); /* 화면 아래에서 시작 */
  animation: fadeUp 3s forwards;
  animation-delay: 0s; /* 처음부터 시작 */
}

.texts.active span {
  animation-play-state: running;
}

@keyframes fadeUp {
  0% {
    opacity: 0;
    transform: translateY(20px); /* 처음에 아래에 위치 */
  }
  100% {
    opacity: 1;
    transform: translateY(0); /* 끝날 때는 원래 위치로 */
  }
}

.texts:nth-child(1) span {
  animation-delay: 0s;
}

.texts:nth-child(2) span {
  animation-delay: 0s;
}

.texts:nth-child(3) span {
  animation-delay: 0s;
}

.geist-mono {
  font-family: "Oswald", sans-serif;
  font-optical-sizing: auto;
  font-weight: 1000;
  font-style: normal;
}
.btn {
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
}

.btn:focus {
  box-shadow: none !important;
}

.active-menu {
  color: #ffbf00; /* 선택된 메뉴 색상 */
  font-weight: bold;
}

/* bootstrap의 기본 버튼 스타일 override */
.btn:active,
.btn:focus-visible {
  outline: none !important;
  box-shadow: none !important;
}
/*------------------------------------------------------------- */
.navbar {
  position: fixed;
  width: 100%;
  top: 0;
  transition: transform 0.5s ease-in-out, opacity 0.5s ease-in-out, background-color 0.3s ease;
  backdrop-filter: blur(10px);
  background-color: rgb(0, 0, 0) !important;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.navbar.hidden {
  transform: translateY(-100%);
  opacity: 0;
}

/* 네비게이션 버튼 스타일 */
.geist-mono {
  font-family: "Oswald", sans-serif;
  font-weight: 500;
  font-size: 1rem;
  padding: 8px 16px;
  transition: all 0.3s ease;
  position: relative;
  color: #ffffff;
}

.geist-mono::after {
  content: "";
  position: absolute;
  width: 0;
  height: 2px;
  bottom: 0;
  left: 50%;
  background-color: #ffbf00;
  transition: all 0.3s ease;
  transform: translateX(-50%);
}

.geist-mono:hover {
  color: #ffbf00;
}

.geist-mono:hover::after {
  width: 80%;
}

.active-menu {
  color: #ffbf00;
}

.active-menu::after {
  width: 80%;
}

/* 로고 컨테이너 */
.navbar-brand {
  position: relative; /* 필요 시 사용 */
  display: inline-block;
  transition: all 0.3s ease; /* 부드러운 애니메이션 효과 */
  font-weight: bold; /* 글자 두께 추가 */
  font-size: 1.5em; /* 글자 크기 조정 */
}

.navbar-brand:hover {
  transform: scale(1.05);
  color: #ffbf00; /* 기존 호버 색상 유지 */
  text-shadow: 0 0 10px #ffbf00, 0 0 20px #ffbf00, 0 0 30px #ffbf00; /* 글자 빛 효과 */
}

.navbar-brand:hover::after {
  content: "";
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255, 191, 0, 0.5), rgba(255, 191, 0, 0));
  border-radius: 50%;
  z-index: -1; /* 로고 뒤에 배치 */
  filter: blur(20px); /* 부드러운 빛 퍼짐 효과 */
  animation: glow 6s infinite ease-in-out; /* 빛나는 애니메이션 추가 */
}

@keyframes glow {
  0%,
  100% {
    opacity: 0.4;
  }
  50% {
    opacity: 1;
  }
}

/* 스크롤바 스타일 */
::-webkit-scrollbar {
  height: 0; /* 아래쪽 스크롤바 숨기기 */
  width: 12px;
}

::-webkit-scrollbar-track {
  background: #1f1f1f; /* 검은색 배경 */
}

::-webkit-scrollbar-thumb {
  background: linear-gradient(145deg, #ffbf00, #ffd700); /* 노란색 그라데이션 */
  border-radius: 6px;
  border: 3px solid #1f1f1f; /* 검은색 테두리 */
}

::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(145deg, #ffd700, #ffbf00); /* 호버 시 색상 반전 */
}

/* 마우스 커서 스타일 */
body,
button,
input,
select,
textarea {
  cursor: url("https://example.com/custom-cursor.png"), auto; /* 커스텀 커서 이미지 URL */
}
/* 햄버거 메뉴 스타일링 */
.navbar-toggler {
  border: none;
  padding: 0.5rem;
  color: white;
}

.navbar-toggler:focus {
  box-shadow: none;
}
/* 
오프캔버스 스타일링 */
.offcanvas {
  width: 300px !important; /* 너비 고정 */
  height: 100vh !important; /* 높이 고정 */
  z-index: 1045 !important; /* 최상위로 보이도록 */
  position: fixed !important;
  visibility: visible;
  background-color: rgba(255, 255, 255, 0.98);
  transform: none;
}

.offcanvas.offcanvas-end {
  top: 0;
  right: 0;
  transform: translateX(100%);
  transition: transform 0.3s ease-in-out;
}

.offcanvas.show {
  transform: translateX(0) !important;
}

.offcanvas-header {
  padding: 1rem;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
}

.offcanvas-body {
  padding: 1rem;
  overflow-y: auto;
}
.navbar-brand {
  width: 160px; /* 로고의 고정 너비 */
  display: flex;
  justify-content: flex-start;
  transition: transform 0.3s ease;
}

/* 햄버거 버튼 컨테이너 스타일 추가 */
.navbar-toggler {
  width: 160px; /* 로고와 동일한 너비 */
  display: flex;
  justify-content: center;
  border: none;
  padding: 0.5rem;
}

/* 기존 스타일 유지 */
.navbar-toggler:focus {
  box-shadow: none;
}
</style>
