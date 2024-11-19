<template>
  <div>
    <div class="home-container">
      <!-- 히어로 섹션 -->
      <section class="hero-section">
        <div class="image-container" id="imageSection" ref="imageSection">
          <div class="gradient-overlay" :style="{ opacity: gradientOpacity }"></div>
          <img src="@/assets/berelin.jpg" alt="Background Image" />
          <div class="hero-content">
            <p class="texts animate__animated animate__fadeIn">
              <span class="main-title">MONEY INDUSTRY</span>
              <span class="sub-title">Your Financial Future Starts Here</span>
            </p>
            <div class="cta-buttons">
              <button class="primary-btn">시작하기</button>
              <button class="secondary-btn">더 알아보기</button>
            </div>
          </div>
        </div>
      </section>

      <!-- 특징 섹션 -->
      <section class="features-section">
        <div class="feature-grid">
          <div class="feature-card" v-for="(feature, index) in features" :key="index" :class="{ visible: isReveal1Visible }">
            <i :class="feature.icon"></i>
            <h3>{{ feature.title }}</h3>
            <p>{{ feature.description }}</p>
          </div>
        </div>
      </section>

      <!-- 통계 섹션 -->
      <section class="stats-section">
        <div class="stats-container">
          <div class="stat-item" v-for="(stat, index) in stats" :key="index">
            <h2>{{ stat.value }}</h2>
            <p>{{ stat.label }}</p>
          </div>
        </div>
      </section>
    </div>
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
import NavVarComponent from "@/components/NavVar/NavVarComponent.vue";

export default {
  name: "App",
  components: {
    NavVarComponent,
  },
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
    const features = [
      {
        icon: "fas fa-chart-line",
        title: "실시간 차트",
        description: "최신 금융 데이터를 실시간으로 분석하세요",
      },
      {
        icon: "fas fa-exchange-alt",
        title: "환율 계산",
        description: "정확한 환율 정보와 계산 도구를 제공합니다",
      },
      {
        icon: "fas fa-percentage",
        title: "금리 비교",
        description: "다양한 금융 상품의 금리를 한눈에 비교해보세요",
      },
    ];

    const stats = [
      { value: "100K+", label: "사용자" },
      { value: "50+", label: "은행 제휴" },
      { value: "24/7", label: "고객 지원" },
    ];
    return {
      features,
      stats,
      isNavbarHidden,
      gradientOpacity,
      isReveal1Visible,
      isReveal2Visible,
    };
  },
};
</script>
<style scoped>
.home-container {
  width: 100%;
  overflow-x: hidden;
}

.hero-section {
  height: 100vh;
  position: relative;
}

.hero-content {
  position: relative;
  z-index: 3;
  text-align: center;
  color: white;
}

.main-title {
  font-size: 4rem;
  font-weight: 700;
  margin-bottom: 1rem;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}

.sub-title {
  font-size: 1.5rem;
  margin-bottom: 2rem;
}

.cta-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 2rem;
}

.primary-btn,
.secondary-btn {
  padding: 1rem 2rem;
  border-radius: 50px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.primary-btn {
  background: #2c3e50;
  color: white;
  border: none;
}

.secondary-btn {
  background: transparent;
  color: white;
  border: 2px solid white;
}

.features-section {
  padding: 5rem 0;
  background: #f8f9fa;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  padding: 0 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.feature-card {
  background: white;
  padding: 2rem;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.stats-section {
  background: #2c3e50;
  color: white;
  padding: 4rem 0;
}

.stats-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  text-align: center;
}

.stat-item h2 {
  font-size: 3rem;
  margin-bottom: 0.5rem;
}

@media (max-width: 768px) {
  .main-title {
    font-size: 2.5rem;
  }

  .sub-title {
    font-size: 1.2rem;
  }
}
</style>
