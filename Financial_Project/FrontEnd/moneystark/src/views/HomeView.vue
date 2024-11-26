<template>
  <div data-scroll-container>
    <!-- 히어로 섹션 -->
    <div class="section hero-section" data-scroll-section>
      <div class="overlay"></div>
      <div class="content">
        <img class="fade-in" width="1500" src="@/assets/navbar/home6.png" alt="Money Industry Logo" />
      </div>
    </div>

    <!-- 스크롤로 보여줄 다양한 정보 섹션 -->
    <div class="section scroll-section" :style="{ backgroundImage: `url(${test2})` }" data-scroll-section>
      <div class="content">
        <h2 data-scroll data-scroll-speed="3">최고의 예금 상품</h2>
        <p data-scroll data-scroll-speed="2">당신의 자산을 불려줄 예금 상품을 추천드립니다.</p>
      </div>

      <!-- 동그란 버튼들 -->
      <div class="circle-container" data-scroll data-scroll-speed="1">
        <div class="circle-item" @click="navigateTo('traditional-asset')">
          <p>
            신뢰와 투명성
            <br />
            고객의 신뢰를 최우선으로 하며, 모든 금융 정보와 서비스는 투명하고 정직하게 제공한다.
          </p>
        </div>
        <div class="circle-item" @click="navigateTo('corporate-finance')">
          <p>
            고객 중심의 혁신
            <br />
            고객의 니즈를 중심으로 끊임없는 혁신을 통해 최적의 재테크 솔루션을 제안한다.
          </p>
        </div>
        <div class="circle-item" @click="navigateTo('private-equity')">
          <p>
            전문성 강화와 책임감
            <br />
            금융 및 투자 분야의 전문성을 기반으로 책임감 있는 서비스를 제공하고, 고객의 자산을 안전하게 관리한다.
          </p>
        </div>
        <div class="circle-item" @click="navigateTo('alternative-investment')">
          <p>
            지속 가능한 성장
            <br />
            재무적 이익뿐 아니라 사회적, 환경적 가치를 고려한 지속 가능한 성장을 추구한다.
          </p>
        </div>
        <!-- <div class="circle-item" @click="navigateTo('new-business')">
          <p>
            지식 공유와 교육
            <br />
            Business
          </p>
        </div> -->
      </div>
    </div>

    <div
      class="section scroll-section"
      :style="{
        backgroundImage: `url(${home5})`,
        backgroundColor: 'rgba(0, 0, 0, 0.45)', // 어두운 색 추가
        backgroundBlendMode: 'multiply', // 배경 이미지와 색상 혼합
      }"
      data-scroll-section
    >
      <div class="content">
        <h2>여러 이미지를 한 번에 확인하세요</h2>
        <p>한 화면에 여러 이미지를 스와이프하며 확인할 수 있습니다.</p>
      </div>
      <Swiper :modules="swiperModules" :slides-per-view="3" space-between="30" loop class="custom-swiper">
        <!-- 슬라이드 1 -->
        <SwiperSlide>
          <a href="https://example.com/link1" target="_blank" class="slide-link">
            <img src="@/assets/home/home1.jpg" alt="Image 1" />
          </a>
        </SwiperSlide>
        <!-- 슬라이드 2 -->
        <SwiperSlide>
          <a href="https://example.com/link2" target="_blank" class="slide-link">
            <img src="@/assets/home/home2.jpg" alt="Image 2" />
          </a>
        </SwiperSlide>
        <!-- 슬라이드 3 -->
        <SwiperSlide>
          <a href="https://example.com/link3" target="_blank" class="slide-link">
            <img src="@/assets/home/home3.jpg" alt="Image 3" />
          </a>
        </SwiperSlide>
        <!-- 슬라이드 4 -->
        <SwiperSlide>
          <a href="https://example.com/link4" target="_blank" class="slide-link">
            <img src="@/assets/home/home4.jpg" alt="Image 4" />
          </a>
        </SwiperSlide>
      </Swiper>
    </div>

    <div class="section scroll-section" :style="{ backgroundImage: `url(${home4})` }" data-scroll-section>
      <div class="content">
        <h2>재테크 뉴스</h2>
        <p>실시간으로 제공되는 최신 금융 뉴스로 앞서가세요.</p>
      </div>
    </div>
  </div>
</template>

<script>
import LocomotiveScroll from "locomotive-scroll";
import "locomotive-scroll/dist/locomotive-scroll.css";
import { Swiper, SwiperSlide } from "swiper/vue"; // Vue용 Swiper 컴포넌트
import { Navigation } from "swiper/modules"; // Swiper 10.x 이상에서는 modules에서 가져옴
import "swiper/swiper-bundle.css"; // Swiper 스타일

import home1 from "@/assets/home/home1.jpg";
import home2 from "@/assets/home/home2.jpg";
import home3 from "@/assets/home/home3.jpg";
import home4 from "@/assets/home/home4.jpg";
import home5 from "@/assets/home/home5.jpg";
import test2 from "@/assets/home/test2.jpg";

export default {
  name: "HomeView",
  components: {
    Swiper,
    SwiperSlide,
  },
  data() {
    return {
      test2,
      home1,
      home2,
      home3,
      home4,
      home5,
      sections: [], // Section positions
      currentSectionIndex: 0, // Current section index
      isScrolling: false, // Check if scrolling
      sectionActive: [], // Track active sections
      swiperModules: [Navigation], // Swiper Navigation 모듈 추가
    };
  },
  mounted() {
    // Locomotive Scroll 초기화
    this.scroll = new LocomotiveScroll({
      el: document.querySelector("[data-scroll-container]"),
      smooth: true,
    });

    // 섹션 위치 초기화
    this.initializeSections();

    // 스크롤 이벤트 추가
    window.addEventListener("wheel", this.handleScroll);
  },
  beforeUnmount() {
    // Locomotive Scroll 정리
    if (this.scroll) this.scroll.destroy();

    // 스크롤 이벤트 제거
    window.removeEventListener("wheel", this.handleScroll);
  },
  methods: {
    initializeSections() {
      const sectionElements = document.querySelectorAll(".section");
      this.sections = Array.from(sectionElements).map((section) => section.offsetTop);
      this.sectionActive = Array(this.sections.length).fill(false);
      this.sectionActive[0] = true;
    },
    handleScroll(event) {
      if (this.isScrolling) return;
      this.isScrolling = true;

      if (event.deltaY > 0) {
        this.moveToNextSection();
      } else if (event.deltaY < 0) {
        this.moveToPreviousSection();
      }

      setTimeout(() => {
        this.isScrolling = false;
      }, 1000);
    },
    moveToNextSection() {
      if (this.currentSectionIndex < this.sections.length - 1) {
        this.currentSectionIndex++;
        this.scrollToSection();
      }
    },
    moveToPreviousSection() {
      if (this.currentSectionIndex > 0) {
        this.currentSectionIndex--;
        this.scrollToSection();
      }
    },
    scrollToSection() {
      const targetOffset = this.sections[this.currentSectionIndex];
      this.scroll.scrollTo(targetOffset, {
        duration: 1000,
        easing: [0.25, 0.1, 0.25, 1],
      });
      setTimeout(() => {
        this.sectionActive = this.sectionActive.map(() => false);
        this.sectionActive[this.currentSectionIndex] = true;
      }, 1000);
    },
    navigateTo(route) {
      this.$router.push(route);
    },
  },
};
</script>

<style scoped>
/* 섹션 스타일 */
.section {
  height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  background-size: cover;
  background-position: center;
  position: relative;
}

/* 히어로 섹션 스타일 업데이트 */
.hero-section {
  position: relative;
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center; /* 가운데 정렬 추가 */
  background: url("@/assets/home/home1.jpg") no-repeat center center/cover;
}

.overlay {
  background: linear-gradient(to right, rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.3));
}

.hero-section .content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  color: white;
}

.hero-section h1 {
  font-size: 4rem;
  font-weight: 700;
  margin-bottom: 1rem;
  opacity: 0;
  animation: fadeInUp 1s ease-out forwards;
}

.hero-section h2 {
  font-size: 2.5rem;
  margin-bottom: 1.5rem;
  opacity: 0;
  animation: fadeInUp 1s ease-out 0.3s forwards;
}

.hero-section p {
  font-size: 1.2rem;
  margin-bottom: 2rem;
  opacity: 0;
  animation: fadeInUp 1s ease-out 0.6s forwards;
}

.cta-buttons {
  display: flex;
  gap: 1rem;
  opacity: 0;
  animation: fadeInUp 1s ease-out 0.9s forwards;
}

.primary-btn,
.secondary-btn {
  padding: 1rem 2rem;
  border-radius: 30px;
  font-size: 1.1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.primary-btn {
  background: #007bff;
  color: white;
  border: none;
}

.secondary-btn {
  background: transparent;
  color: white;
  border: 2px solid white;
}

.primary-btn:hover {
  background: #0056b3;
  transform: translateY(-2px);
}

.secondary-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateY(-2px);
}

.hero-section {
  color: white;
  background: url("@/assets/home/home1.jpg") no-repeat center center/cover;
  position: relative;
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(to bottom, rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5));
  z-index: 1;
}

.content {
  position: relative;
  z-index: 2;
  display: flex;
  /* flex-direction: column; */
  align-items: center;
  justify-content: center;
  padding: 20px;
  max-width: 1500px;
  margin: 0 auto;
  top: auto;
  left: auto;
  transform: none;
  padding: 20px;
  width: 100%;
}

.content img {
  margin: 0 auto; /* 상하 마진 제거, 좌우 auto */
  width: 130%;
  max-width: 1500px;
  height: auto;
}

.hero-content {
  opacity: 0;
  transform: translateY(20px);
  transition: all 1s ease;
}

.hero-content[data-scroll] {
  opacity: 1;
  transform: translateY(0);
}

.hero-content p {
  font-size: 160px;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}

.hero-content h4 {
  font-size: 20px;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}

.scroll-section {
  color: white;
  background-color: rgba(0, 0, 0, 0.5);
}

/* 반응형 스타일 */
/* 태블릿 크기 */
@media (max-width: 920px) {
  .content {
    top: 30%;
    left: 20%;
    padding: 10px;
    transform: none;
  }
  .content p,
  .content h2 {
    font-size: 14px;
    visibility: visible;
  }
}

@media (max-width: 480px) {
  .content {
    top: 50%;
    left: 20%;
    padding: 10px;
    transform: translate(-10%, -200%);
  }
  .content p,
  .content h2 {
    visibility: hidden;
    height: 0;
  }
}

@media (max-width: 850px) {
  .hero-content p,
  .hero-content h4 {
    font-size: 20px;
  }
}

@media (max-width: 480px) {
  .hero-content p,
  .hero-content h4 {
    font-size: 10px;
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.content .fade-in {
  opacity: 0;
  animation: fadeInUp 1s ease-in-out forwards;
  animation-delay: 0s;
}

.content h2 {
  animation: fadeInUp 3s ease-in-out 0.9s forwards;
}

.content p {
  animation: fadeInUp 3s ease-in-out 1.8s forwards;
}

.content h4 {
  animation: fadeInUp 3s ease-in-out 2.7s forwards;
}

/* Circle Buttons */
.circle-container {
  display: flex;
  justify-content: center;
  gap: 20px;
}

.circle-item {
  width: 400px;
  height: 300px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  text-align: center;
}
.circle-item:hover {
  transform: scale(1.1);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
}

.circle-item p {
  margin: 0;
  font-size: 16px;
  color: #333;
  font-weight: bold;
}

/* Swiper 스타일 */
.custom-swiper {
  width: 80%;
  margin: 0 auto;
  padding: 40px 0;
  margin-top: 100px;
}

.custom-swiper .swiper-slide {
  display: flex;
  justify-content: center;
  align-items: center;
}

.custom-swiper .slide-link {
  display: block;
  width: 60%;
  height: 60%;
  overflow: hidden;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.custom-swiper .slide-link img {
  width: 100%;
  height: 100%;
  display: block;
  transition: transform 0.3s ease;
}

.custom-swiper .slide-link:hover img {
  transform: scale(1.1);
}

.custom-swiper .slide-link:hover {
  transform: scale(1.05);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
}

/* 반응형 스타일 */
@media (max-width: 768px) {
  .circle-container {
    flex-direction: column;
    gap: 10px;
  }

  .circle-item {
    width: 100px;
    height: 100px;
  }

  .custom-swiper {
    width: 100%;
  }

  .custom-swiper .swiper-slide {
    width: 80%;
  }
}

@media (max-width: 480px) {
  .circle-item {
    width: 80px;
    height: 80px;
  }

  .circle-item p {
    font-size: 14px;
  }
}
</style>
