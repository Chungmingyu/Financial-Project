<template>
  <nav :class="['navbar', { 'navbar-main': isHomePage }]">
    <div class="container-fluid">
      <a class="navbar-brand" @click.prevent="$router.push({ name: 'home' })">
        <img :src="isHomePage ? homeLogo : otherLogo" :class="isHomePage ? 'logo-home' : 'logo-other'" alt="Logo" class="logo" />
      </a>

      <div class="menu-group">
        <button
          v-for="(item, index) in menuItems"
          :key="index"
          :class="['menu-item', { 'menu-item-dark': !isHomePage }, { 'menu-item-active': currentRoute === item.route }]"
          @click.prevent="$router.push({ name: item.route })"
        >
          {{ item.text }}
        </button>
        <div class="menu-switch">
          <button :class="['switch-btn', { 'switch-btn-active': !isStableMenu }]" @click="toggleMenu">투자 스타일 변경</button>
        </div>
      </div>

      <div class="right-menu-group">
        <div class="hamburger">
          <button class="hamburger-btn" @click="toggleSidebar">
            <span :class="['hamburger-line', { active: isSidebarOpen }]"></span>
            <span :class="['hamburger-line', { active: isSidebarOpen }]"></span>
            <span :class="['hamburger-line', { active: isSidebarOpen }]"></span>
          </button>
        </div>
      </div>
    </div>

    <!-- Sidebar Overlay -->
    <div v-if="isSidebarOpen" class="sidebar-overlay" @click="closeSidebar"></div>

    <!-- Sidebar -->
    <div :class="['sidebar', { open: isSidebarOpen }]">
      <div class="sidebar-header">
        <button class="close-btn" @click="closeSidebar">×</button>
      </div>

      <div class="sidebar-content">
        <div v-if="isLoggedIn" class="user-section">
          <div class="user-greeting">환영합니다!</div>
          <div class="profile-card">
            <div class="profile-image">
              <svg viewBox="0 0 36 36" fill="none" role="img" xmlns="http://www.w3.org/2000/svg" width="80" height="80">
                <mask id=":r1k:" maskUnits="userSpaceOnUse" x="0" y="0" width="36" height="36"><rect width="36" height="36" rx="72" fill="#FFFFFF"></rect></mask>
                <g mask="url(#:r1k:)">
                  <rect width="36" height="36" fill="#eb0a44"></rect>
                  <rect x="0" y="0" width="36" height="36" transform="translate(1 7) rotate(63 18 18) scale(1)" fill="#f2a73d" rx="36"></rect>
                  <g transform="translate(-7 3.5) rotate(3 18 18)">
                    <path d="M13,19 a1,0.75 0 0,0 10,0" fill="#000000"></path>
                    <rect x="11" y="14" width="1.5" height="2" rx="1" stroke="none" fill="#000000"></rect>
                    <rect x="23" y="14" width="1.5" height="2" rx="1" stroke="none" fill="#000000"></rect>
                  </g>
                </g>
              </svg>
            </div>
            <div class="profile-info">
              <div class="profile-name">{{ userName }}</div>
              <div class="profile-details">{{ userDetails }}</div>
            </div>
          </div>
          <div class="sidebar-menu">
            <button class="sidebar-item" @click="navigateToExchangeCalculator">
              <span class="item-icon">💱</span>
              환율 계산기
            </button>
            <button class="sidebar-item" @click="navigateToUserInfo">
              <span class="item-icon">👤</span>
              회원정보
            </button>
            <button class="sidebar-item" @click="handleLogout">
              <span class="item-icon">🚪</span>
              로그아웃
            </button>
          </div>
        </div>
        <div v-else class="auth-section">
          <div class="sidebar-menu">
            <button class="sidebar-item" @click="navigateToExchangeCalculator">
              <span class="item-icon">💱</span>
              환율 계산기
            </button>
            <button class="sidebar-item" @click="navigateToLogin">
              <span class="item-icon">🔑</span>
              로그인
            </button>
            <button class="sidebar-item" @click="navigateToSignup">
              <span class="item-icon">✏️</span>
              회원가입
            </button>
          </div>
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
    const isSidebarOpen = ref(false);

    const isHomePage = computed(() => route.name === "home");
    const currentRoute = computed(() => route.name);
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

    const menuItems = ref([...stableMenuItems]);
    const isStableMenu = ref(true);

    const toggleMenu = () => {
      isStableMenu.value = !isStableMenu.value;
      menuItems.value = isStableMenu.value ? stableMenuItems : aggressiveMenuItems;
    };

    const toggleSidebar = () => {
      isSidebarOpen.value = !isSidebarOpen.value;
      if (isSidebarOpen.value) {
        document.body.style.overflow = "hidden";
      } else {
        document.body.style.overflow = "";
      }
    };

    const closeSidebar = () => {
      isSidebarOpen.value = false;
      document.body.style.overflow = "";
    };

    const isMobile = ref(false);
    const isLoggedIn = computed(() => store.isLoggedIn);

    const updateDeviceStatus = () => {
      isMobile.value = window.innerWidth <= 768;
    };

    const navigateToLogin = () => {
      router.push({ name: "LogInView" });
      closeSidebar();
    };

    const navigateToSignup = () => {
      router.push({ name: "SignUpView" });
      closeSidebar();
    };

    const navigateToUserInfo = () => {
      router.push({ name: "UserDetailView" });
      closeSidebar();
    };

    const navigateToExchangeCalculator = () => {
      router.push({ name: "CurrencyCalculatorView" });
      closeSidebar();
    };

    const handleLogout = () => {
      store.logout();
      alert("로그아웃 되었습니다.");
      router.push({ name: "home" });
      closeSidebar();
    };

    onMounted(() => {
      window.addEventListener("resize", updateDeviceStatus);
      updateDeviceStatus();
    });

    onUnmounted(() => {
      window.removeEventListener("resize", updateDeviceStatus);
      document.body.style.overflow = "";
    });

    return {
      currentRoute, 
      isHomePage,
      homeLogo,
      otherLogo,
      menuItems,
      isStableMenu,
      toggleMenu,
      isMobile,
      isLoggedIn,
      isSidebarOpen,
      toggleSidebar,
      closeSidebar,
      navigateToLogin,
      navigateToSignup,
      navigateToUserInfo,
      navigateToExchangeCalculator,
      handleLogout,
      userProfileImage: store.userProfileImage,
      userName: store.userName,
      userDetails: store.userDetails,
    };
  },
};
</script>

<style scoped>

.switch-btn {
  background: none;
  border: 2px solid #ffffff;
  border-radius: 20px;
  color: #000000;
  font-weight: 600;
  padding: 8px 16px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.switch-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: #ffffff;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  z-index: -1;
}

.switch-btn:hover::before {
  left: 0;
}

.switch-btn:hover {
  color: rgb(0, 0, 0);
  transform: scale(1.05);
}

.switch-btn-active {
  background: #000000;
  color: rgb(0, 0, 0);
}

.switch-btn:active {
  transform: scale(0.95);
}

.menu-item {
  position: relative;
  overflow: hidden;
}

.menu-item::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  width: 0;
  height: 2px;
  background: currentColor;
  transition: all 0.3s ease;
  transform: translateX(-50%);
}

.menu-item:hover::after {
  width: 100%;
}

.menu-item-active::after {
  width: 100%;
  background: #000000;
}

.menu-item-active {
  color: #000000 !important;
}

.navbar-main .menu-item-active {
  color: #000000 !important;
}

.navbar-main .menu-item-active::after {
  background: #000000;
}

.menu-item:active {
  transform: scale(0.95);
  
}
.navbar {
  position: relative;
  top: 0;
  width: 100%;
  z-index: 1000;
  background-color: #fff;
  transition: all 0.5s ease;
  height: 100px;
}

.navbar.navbar-main {
  position: fixed;
  background-color: transparent;
  height: 120px;
}

.container-fluid {
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
}

.navbar-brand {
  display: flex;
  align-items: center;
}

.logo {
  height: 80px;
  transition: all 0.5s ease;
}

.navbar.navbar-main .logo {
  height: 100px;
}

.menu-group {
  display: flex;
  gap: 3rem;
  margin: 0 2rem;
  padding-bottom: 10px;
}

.menu-item {
  position: relative;
  font-size: 1.2rem;
  font-weight: 600;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem 0;
  transition: all 0.3s ease;
}

.menu-item-dark {
  color: #333;
}

.navbar-main .menu-item {
  color: white;
}

.right-menu-group {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.switch-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem 1rem;
  transition: all 0.3s ease;
}

.hamburger-btn {
  display: flex;
  flex-direction: column;
  gap: 6px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
  padding-right: 30px;
  z-index: 1100;
  padding-bottom: 20px;
}

.hamburger-line {
  width: 24px;
  height: 2px;
  background-color: currentColor;
  transition: all 0.3s ease;
}

.hamburger-line.active:nth-child(1) {
  transform: rotate(45deg) translate(5px, 5px);
}

.hamburger-line.active:nth-child(2) {
  opacity: 0;
}

.hamburger-line.active:nth-child(3) {
  transform: rotate(-45deg) translate(7px, -7px);
}

.sidebar-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 1000;
  transition: opacity 0.3s ease;
}

.sidebar {
  position: fixed;
  top: 0;
  right: -400px;
  width: 400px;
  height: 100vh;
  background-color: white;
  z-index: 1100;
  transition: right 0.3s ease;
  box-shadow: -2px 0 5px rgba(0, 0, 0, 0.1);
}

.sidebar.open {
  right: 0;
}

.sidebar-header {
  display: flex;
  justify-content: flex-end;
  padding: 1rem;
}

.close-btn {
  background: none;
  border: none;
  font-size: 2rem;
  cursor: pointer;
  padding: 0.5rem;
  padding-right: 30px;
}

.sidebar-content {
  padding: 1rem;
}

.user-greeting {
  font-size: 1.2rem;
  font-weight: 500;
  margin-bottom: 2rem;
  text-align: center;
}

.profile-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
  justify-content: center;
  padding-bottom: 30px;
}

.profile-image {
  width: 50px;
  height: 50px;
  border-radius: 50%;
}

.profile-info {
  display: flex;
  flex-direction: column;
}

.profile-name {
  font-size: 1.2rem;
  font-weight: 600;
}

.profile-details {
  font-size: 0.9rem;
  color: #666;
}

.sidebar-menu {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.sidebar-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  width: 100%;
  padding: 1rem;
  background: none;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  font-size: 1rem;
}

.sidebar-item:hover {
  background-color: #f5f5f5;
}

.item-icon {
  font-size: 1.2rem;
}

@media (max-width: 962px) {
  .menu-group {
    display: none;
  }

  .right-menu-group {
    gap: 1rem;
  }

  .navbar {
    padding: 0.5rem 1rem;
  }
}
</style>
