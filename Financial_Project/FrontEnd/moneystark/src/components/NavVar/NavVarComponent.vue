<template>
  <header>
    <nav class="navbar bg-body-tertiary fixed-top" style="padding: 0" :class="{ hidden: isNavbarHidden }">
      <div class="container-fluid" style="padding: 0">
        <a class="navbar-brand" style="padding: 0" @click.prevent="$router.push({ name: 'home' })">
          <img src="@/assets/logo_white.png" style="padding: 0; height: 100px" />
        </a>

        <!-- 메뉴 컨테이너 -->
        <div class="menu-container">
          <div class="menu-wrapper" :class="{ 'slide-left': !isStableMenu, 'slide-right': isStableMenu }">
            <!-- 안정적 성향 메뉴 -->
            <div class="menu-group">
              <button
                v-for="(item, index) in stableMenuItems"
                :key="index"
                class="btn geist-mono"
                :class="{ 'active-menu': $route.name === item.route }"
                @click.prevent="$router.push({ name: item.route })"
              >
                {{ item.text }}
              </button>
            </div>
            <!-- 공격적 성향 메뉴 -->
            <div class="menu-group">
              <button
                v-for="(item, index) in aggressiveMenuItems"
                :key="index"
                class="btn geist-mono"
                :class="{ 'active-menu': $route.name === item.route }"
                @click.prevent="$router.push({ name: item.route })"
              >
                {{ item.text }}
              </button>
            </div>
          </div>
        </div>

        <!-- 토글 버튼을 오른쪽으로 이동 -->
        <button class="btn toggle-btn geist-mono" @click="toggleMenuType">
          {{ isStableMenu ? "공격적 투자 메뉴" : "안정적 투자 메뉴" }}
          <span class="toggle-icon" :class="{ rotate: !isStableMenu }">↔</span>
        </button>
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
    const isStableMenu = ref(true); // 기본값은 안정적 메뉴
    const stableMenuItems = [
      { text: "금리 비교", route: "ComparisonView" },
      { text: "상품 추천", route: "ProductSuggestionView" },
      { text: "지도", route: "BankMapView" },
      { text: "자유 게시판", route: "BoardView" },
    ];

    const aggressiveMenuItems = [
      { text: "주식 정보", route: "StockView" },
      { text: "코인 정보", route: "CoinData" },
      { text: "아파트 정보", route: "HomeData" },
      { text: "자유 게시판", route: "BoardView" },
    ];

    const toggleMenuType = () => {
      isStableMenu.value = !isStableMenu.value;
    };

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
      stableMenuItems,
      aggressiveMenuItems,
      isStableMenu,
      toggleMenuType,
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
/* 색상 변수 정의 */
:root {
  --primary-color: #17BEBB;
  --primary-dark: #139795;
  --white: #ffffff;
  --black: #333333;
  --gray-light: #f5f5f5;
}

/* 기본 리셋 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

/* Navbar 기본 스타일 */
.navbar {
  position: fixed;
  width: 100%;
  top: 0;
  background-color: var(--white) !important;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  transition: transform 0.5s ease-in-out, opacity 0.5s ease-in-out;
}

.navbar.hidden {
  transform: translateY(-100%);
  opacity: 0;
}

/* 로고 스타일 */
.navbar-brand {
  padding: 0;
  transition: transform 0.3s ease;
}

.navbar-brand:hover {
  transform: scale(1.05);
}

/* 메뉴 버튼 스타일 */
.geist-mono {
  font-family: "Oswald", sans-serif;
  font-weight: 500;
  color: var(--black);
  padding: 8px 16px;
  position: relative;
  transition: color 0.3s ease;
}

.geist-mono::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 50%;
  width: 0;
  height: 2px;
  background-color: var(--primary-color);
  transition: all 0.3s ease;
  transform: translateX(-50%);
}

.geist-mono:hover {
  color: var(--primary-color);
}

.geist-mono:hover::after {
  width: 80%;
}

/* 활성 메뉴 스타일 */
.active-menu {
  color: var(--primary-color);
}

.active-menu::after {
  width: 80%;
}

/* 토글 버튼 스타일 */
.toggle-btn {
  background: var(--white);
  color: var(--primary-color);
  border: 1px solid var(--primary-color);
  padding: 8px 16px;
  border-radius: 20px;
  transition: all 0.3s ease;
}

.toggle-btn:hover {
  background: var(--primary-color);
  color: var(--white);
}

/* 메뉴 컨테이너 스타일 */
.menu-container {
  flex: 1;
  overflow: hidden;
  margin: 0 20px;
}

.menu-wrapper {
  display: flex;
  width: 200%;
  transition: transform 0.5s ease;
}

.menu-wrapper.slide-left {
  transform: translateX(-50%);
}

.menu-wrapper.slide-right {
  transform: translateX(0);
}

.menu-group {
  display: flex;
  width: 50%;
  justify-content: space-around;
  align-items: center;
}

/* 오프캔버스 메뉴 스타일 */
.offcanvas {
  background-color: var(--white);
  width: 300px !important;
}

.offcanvas-header {
  border-bottom: 1px solid var(--gray-light);
}

/* 스크롤바 스타일 */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: var(--gray-light);
}

::-webkit-scrollbar-thumb {
  background: var(--primary-color);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: var(--primary-dark);
}
</style>
