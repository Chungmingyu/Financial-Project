<template>
  <div>
    <header>
      <nav class="navbar bg-body-tertiary fixed-top" style="padding: 0" :class="{ hidden: isNavbarHidden }">
        <div class="container-fluid" style="padding: 0">
          <a class="navbar-brand" style="padding: 0"><img src="@/assets/Logo.jpg" style="padding: 0; height: 100px" /></a>
          <div style="display: flex; width: 600px; justify-content: space-between">
            <button class="btn geist-mono" role="button" data-bs-toggle="button" @click.prevent="$router.push({ name: 'ChartView' })">차트</button>
            <button class="btn geist-mono" role="button" data-bs-toggle="button" @click.prevent="$router.push({ name: 'CurrencyCalculatorView' })">환율 계산기</button>
            <button class="btn geist-mono" role="button" data-bs-toggle="button" @click.prevent="$router.push({ name: 'ComparisonView' })">금리 비교</button>
            <button class="btn geist-mono" role="button" data-bs-toggle="button" @click.prevent="$router.push({ name: 'BankView' })">근처 은행</button>
            <button class="btn geist-mono" role="button" data-bs-toggle="button" @click.prevent="$router.push({ name: 'ProductSuggestionView' })">상품 추천</button>
            <button class="btn geist-mono" role="button" data-bs-toggle="button" @click.prevent="$router.push({ name: 'BankMapView' })">지도</button>
          </div>
          <button class="navbar-toggler" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasNavbar" aria-controls="offcanvasNavbar" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="offcanvas offcanvas-end" tabindex="-1" id="offcanvasNavbar" aria-labelledby="offcanvasNavbarLabel">
            <div class="offcanvas-header">
              <h5 class="offcanvas-title" id="offcanvasNavbarLabel">Offcanvas</h5>
              <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
            </div>
            <div class="offcanvas-body">
              <ul class="navbar-nav justify-content-end flex-grow-1 pe-3">
                <li class="nav-item">
                  <a class="nav-link active" aria-current="page" href="#">메인페이지</a>
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
    <!-- 제이쿼리 -->
    <!-- 배경 이미지와 그라디언트 오버레이 포함 -->
    <div class="image-container" id="imageSection" ref="imageSection">
      <div class="gradient-overlay" :style="{ opacity: gradientOpacity }"></div>
      <img src="@/assets/berelin.jpg" alt="Background Image" />
      <p class="texts">
        <span>MONEY</span>
        <span>INDUSTRY</span>
      </p>
    </div>

    <!-- 타이틀과 애니메이션 적용 -->
    <div id="titlechart2">
      <div class="scrollContent">
        <h1>ScrollMagic Animations</h1>
        <h2>Scroll to reveal animations as you pass through different sections!</h2>
        <p>
          This demo uses
          <strong>ScrollMagic</strong>
          to reveal and animate elements as they enter and leave the viewport.
        </p>

        <div id="trigger1" class="spacer"></div>
        <div id="reveal1" class="box2 blue" :class="{ visible: isReveal1Visible }">
          <p>I will be revealed when scrolled into view and hidden when scrolled past.</p>
        </div>

        <div id="trigger2" class="spacer"></div>
        <div id="reveal2" class="box2 green" :class="{ visible: isReveal2Visible }">
          <p>I will stay visible once revealed.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from "vue";
import ScrollMagic from "scrollmagic";
import { gsap } from "gsap";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap";

export default {
  name: "App",
  setup() {
    const isNavbarHidden = ref(false);
    const gradientOpacity = ref(0);
    const isReveal1Visible = ref(false);
    const isReveal2Visible = ref(false);

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
    };
  },
};
</script>

<style>
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
</style>
