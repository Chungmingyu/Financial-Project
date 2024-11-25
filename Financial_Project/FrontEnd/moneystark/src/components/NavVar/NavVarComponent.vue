<template>
  <nav :class="['navbar', { 'navbar-main': isHomePage }]">
    <div class="container-fluid">
      <!-- 로고 -->
      <a class="navbar-brand" @click.prevent="$router.push({ name: 'home' })">
        <img :src="isHomePage ? homeLogo : otherLogo" :class="isHomePage ? 'logo-home' : 'logo-other'" alt="Logo" class="logo" />
      </a>

      <!-- 메뉴 -->
      <div class="menu-group">
        <button v-for="(item, index) in menuItems" :key="index" :class="['menu-item', { 'menu-item-dark': !isHomePage }]" @click.prevent="$router.push({ name: item.route })">
          {{ item.text }}
        </button>
      </div>

      <!-- 투자 스타일 변경 버튼 -->
      <div class="menu-switch">
        <button class="switch-btn" @click="toggleMenu">투자 스타일 변경</button>
      </div>

      <!-- 햄버거 버튼 -->
      <div class="hamburger">
        <button class="hamburger-btn" @click="toggleDropdown">☰</button>
        <div v-if="dropdownVisible" class="dropdown-menu">
          <button v-if="isLoggedIn" class="menu-item" @click="navigateToUserInfo">회원정보</button>
          <button v-if="isLoggedIn" class="menu-item" @click="handleLogout">로그아웃</button>
          <button v-if="!isLoggedIn" class="menu-item" @click="navigateToLogin">로그인</button>
          <button v-if="!isLoggedIn" class="menu-item" @click="navigateToSignup">회원가입</button>
        </div>
      </div>
    </div>
  </nav>
</template>
<script>
import { computed, ref, onMounted, onUnmounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import homeLogo from "@/assets/navbar/logo2.png";
import otherLogo from "@/assets/navbar/logo_white.png";
import { useUserStore } from "../../stores/user";

export default {
  name: "NavBarComponent",
  setup() {
    const route = useRoute();
    const router = useRouter();
    const store = useUserStore();

    // 현재 페이지가 메인 화면인지 확인
    const isHomePage = computed(() => route.name === "home");

    // 메뉴 데이터
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

    // 초기 메뉴 상태
    const menuItems = ref([...stableMenuItems]); // 기본값: stableMenuItems
    const isStableMenu = ref(true);

    // 투자 스타일 변경
    const toggleMenu = () => {
      isStableMenu.value = !isStableMenu.value;
      menuItems.value = isStableMenu.value ? stableMenuItems : aggressiveMenuItems;
    };

    // 반응형 상태
    const isMobile = ref(false);
    const updateDeviceStatus = () => {
      isMobile.value = window.innerWidth <= 768;
    };

    // 햄버거 메뉴 상태
    const dropdownVisible = ref(false);
    const toggleDropdown = () => {
      dropdownVisible.value = !dropdownVisible.value;
    };

    // 로그인 상태
    const isLoggedIn = computed(() => store.isLoggedIn);

    // 로그인/회원 관련 동작
    const navigateToLogin = () => router.push({ name: "LogInView" });
    const navigateToSignup = () => router.push({ name: "SignUpView" });
    const navigateToUserInfo = () => router.push({ name: "UserDetailView" });
    const handleLogout = () => {
      store.logout();
      alert("로그아웃 되었습니다.");
      router.push({ name: "home" });
    };

    // 이벤트 등록 및 해제
    onMounted(() => {
      window.addEventListener("resize", updateDeviceStatus);
      updateDeviceStatus(); // 초기화
    });

    onUnmounted(() => {
      window.removeEventListener("resize", updateDeviceStatus);
    });

    return {
      isHomePage,
      homeLogo,
      otherLogo,
      menuItems,
      isStableMenu,
      toggleMenu,
      isMobile,
      dropdownVisible,
      toggleDropdown,
      isLoggedIn,
      navigateToLogin,
      navigateToSignup,
      navigateToUserInfo,
      handleLogout,
    };
  },
};
</script>

<style scoped>
.navbar {
  position: relative; /* 기본적으로 문서 흐름에 포함 */
  top: 0;
  width: 100%;
  z-index: 1; /* 일반 화면에서는 낮은 z-index */
  background-color: rgba(255, 255, 255, 0.9); /* 기본 배경색 */
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); /* 그림자 추가 */
  border-bottom: 1px solid #727272; /* 회색 줄 추가 */
  transition: all 0.3s ease;
  color: black; /* 기본 텍스트 색상 */
}

.navbar.navbar-main {
  position: fixed; /* 메인 화면에서는 고정 */
  z-index: 5; /* 메인 화면에서 다른 요소 위에 표시 */
  background-color: transparent; /* 투명 배경 */
  box-shadow: none; /* 그림자 제거 */
  color: white; /* 메인 화면에서는 흰색 텍스트 */
}

.navbar-brand img {
  height: 130px;
}

.menu-group {
  display: flex;
  gap: 20px;
}

.menu-item {
  font-size: 16px;
  color: inherit; /* 부모의 색상 상속 */
  background: none;
  border: none;
  cursor: pointer;
  transition: color 0.3s ease;
}

.menu-item-dark {
  color: black; /* 다른 화면에서 검은색 텍스트 */
}

.menu-item:hover {
  color: #17bebb; /* Hover 시 색상 */
}
.logo {
  height: 100px; /* 로고 크기 조정 */
  transition: all 0.3s ease; /* 부드러운 전환 효과 */
  padding: 0;
}

.navbar.navbar-main .logo {
  height: 100px; /* 메인 화면에서 로고 크기 조정 */
}
.hamburger {
  position: relative;
}

.hamburger-btn {
  font-size: 24px;
  background: none;
  border: none;
  cursor: pointer;
  color: inherit;
}

/* 드롭다운 메뉴 */
.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  background: white;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  z-index: 1000;
}

.dropdown-menu .menu-item {
  padding: 10px 20px;
  color: #333;
}

.dropdown-menu .menu-item:hover {
  background: #f1f1f1;
}

.menu-divider {
  height: 1px;
  background: #ddd;
  margin: 5px 0;
}

/* 반응형 설정 */
@media (max-width: 962px) {
  .menu-group {
    display: none; /* 작은 화면에서는 메뉴 숨김 */
  }

  .hamburger {
    display: block; /* 작은 화면에서 햄버거 메뉴 표시 */
  }
}
</style>
