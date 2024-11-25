<template>
  <div data-scroll-container>
    <!-- 상단 이미지 섹션 -->
    <div class="section hero-section" data-scroll-section>
      <div class="content">
        <h2 class="fade-in">Make your money work for you.</h2>
        <p class="fade-in" style="animation-delay: 0.5s">다양한 금융 서비스를 통해 최적의 재테크와 투자 솔루션을 제공합니다.</p>
        <h4 class="fade-in" style="animation-delay: 1s">추가 설명 텍스트입니다.</h4>
      </div>
    </div>

    <!-- 스크롤로 보여줄 다양한 정보 섹션 -->
    <div class="section scroll-section" :style="{ backgroundImage: `url(${home2})` }" data-scroll-section>
      <div class="content">
        <h2 data-scroll data-scroll-speed="3">최고의 예금 상품</h2>
        <p data-scroll data-scroll-speed="2">당신의 자산을 불려줄 예금 상품을 추천드립니다.</p>
      </div>

      <!-- 동그란 버튼들 -->
      <div class="circle-container" data-scroll data-scroll-speed="1">
        <div class="circle-item" @click="navigateTo('traditional-asset')">
          <p>
            전통자산
            <br />
            운용
          </p>
        </div>
        <div class="circle-item" @click="navigateTo('corporate-finance')">
          <p>
            기업금융
            <br />
            (IB)
          </p>
        </div>
        <div class="circle-item" @click="navigateTo('private-equity')">
          <p>
            경영참여
            <br />
            (PE)
          </p>
        </div>
        <div class="circle-item" @click="navigateTo('alternative-investment')">
          <p>
            대체투자
            <br />
            운용
          </p>
        </div>
        <div class="circle-item" @click="navigateTo('new-business')">
          <p>
            New
            <br />
            Business
          </p>
        </div>
      </div>
    </div>

    <div class="section scroll-section" :style="{ backgroundImage: `url(${home3})` }" data-scroll-section>
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

export default {
  name: "HomeView",
  components: {
    Swiper,
    SwiperSlide,
  },
  data() {
    return {
      home1,
      home2,
      home3,
      home4,
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

.hero-section {
  color: white;
  background: url("@/assets/home/home1.jpg") no-repeat center center/cover;
}

.hero-content {
  opacity: 0;
  transform: translateY(20px);
  transition: all 1s ease;
  /* width: 100vh; */
}

.hero-content[data-scroll] {
  opacity: 1;
  transform: translateY(0);
}
.hero-content p {
  font-size: 160px;
}
.hero-content h4 {
  font-size: 20px;
}

.scroll-section {
  color: white;
  background-color: rgba(0, 0, 0, 0.5);
}

/* content p, h4 */
.content {
  position: absolute; /* 절대 위치로 설정 */
  top: 25%; /* 기본값: 섹션 상단에서 30% 아래 */
  left: 10%; /* 기본값: 섹션 왼쪽에서 10% 오른쪽으로 */
  transform: translate(-10%, -50%); /* 위치 정렬 */
  display: flex; /* Flexbox 활성화 */
  flex-direction: column; /* 세로 방향 정렬 */
  justify-content: flex-start; /* 세로 방향: 위쪽 정렬 */
  align-items: flex-start; /* 가로 방향: 왼쪽 정렬 */
  text-align: left; /* 텍스트 정렬을 왼쪽으로 */
  height: auto; /* 높이를 콘텐츠 크기에 맞춤 */
  padding: 20px; /* 콘텐츠와 섹션 가장자리 간의 여백 추가 */
}

/* 반응형 스타일 */
/* 태블릿 크기 */
@media (max-width: 920px) {
  .content {
    top: 30%;
    left: 20%;
    padding: 10px; /* 패딩 축소 */
    transform: none; /* 위치 조정 제거 */
  }
  .content p,
  .content h2 {
    font-size: 14px; /* 폰트 크기 축소 */
    visibility: visible; /* 글자 보이기 */
  }
}

@media (max-width: 480px) {
  .content {
    top: 50%; /* 모바일에서 중앙으로 이동 */
    left: 20%; /* 여백 증가 */
    padding: 10px; /* 패딩 축소 */
    transform: translate(-10%, -200%); /* 유지 */
  }
  .content p,
  .content h2 {
    visibility: hidden; /* 글자 숨기기 */
    height: 0; /* 높이를 0으로 설정 */
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
    opacity: 0; /* 투명도 0으로 시작 */
    transform: translateY(20px); /* 아래에서 위로 이동 */
  }
  to {
    opacity: 1; /* 투명도 1로 종료 */
    transform: translateY(0); /* 원래 위치로 이동 */
  }
}
.content .fade-in {
  opacity: 0; /* 초기 상태를 투명하게 설정 */
  animation: fadeInUp 1s ease-in-out forwards; /* 애니메이션 적용 */
  animation-delay: 0s; /* 기본 딜레이 없음 */
}
/* 애니메이션 적용 */
.content h2 {
  animation: fadeInUp 3s ease-in-out 0.9s forwards; /* 0.3초 딜레이 후 실행 */
}

.content p {
  animation: fadeInUp 3s ease-in-out 1.8s forwards; /* 0.6초 딜레이 후 실행 */
}

.content h4 {
  animation: fadeInUp 3s ease-in-out 2.7s forwards; /* 0.9초 딜레이 후 실행 */
}

/* Circle Buttons */
.circle-container {
  display: flex;
  justify-content: center;
  gap: 20px;
}

.circle-item {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  cursor: pointer;
  transition: transform 0.3s ease;
  text-align: center;
}

.circle-item:hover {
  transform: scale(1.1);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
}

.circle-item p {
  margin: 0;
  font-size: 14px;
  font-weight: bold;
  text-align: center;
}
/* swiper  */
/* Swiper 컨테이너 */
.custom-swiper {
  width: 80%;
  max-width: 1500px; /* 컨테이너 최대 너비 */
  height: auto; /* 높이는 내용에 맞게 자동 설정 */
  margin: 0 auto;
  margin-top: 500px;
  padding: 20px 0; /* 상하 여백 추가 */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* 그림자 효과 */
  border-radius: 10px;
  background: none; /* 배경 없음 */
}

/* 이미지 스타일 */
.custom-swiper img {
  width: 100%; /* 슬라이드의 너비에 맞춤 */
  height: 100%; /* 이미지 높이를 키움 */
  object-fit: cover; /* 이미지 비율 유지하며 채우기 */
  border-radius: 10px; /* 모서리를 둥글게 */
}

/* 네비게이션 버튼 스타일 */
.swiper-button-prev,
.swiper-button-next {
  color: #fff;
  background-color: rgba(0, 0, 0, 0.5);
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.swiper-button-prev:hover,
.swiper-button-next:hover {
  background-color: #000;
}

/* 네비게이션 버튼 위치 조정 */
.swiper-button-prev {
  left: -20px;
}
.swiper-button-next {
  right: -20px;
}

/* 페이지네이션 스타일 */
.swiper-pagination-bullet {
  background-color: #000;
  opacity: 0.6;
}

.swiper-pagination-bullet-active {
  background-color: #ff5733;
  opacity: 1;
}
</style>
