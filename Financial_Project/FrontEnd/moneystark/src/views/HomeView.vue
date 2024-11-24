<template>
  <div id="fullpage">
    <!-- 상단 이미지 섹션 -->
    <div class="section hero-section">
      <div class="hero-content" :class="{ active: activeSection === 1 }">
        <p class="fade-in fade-in-first">Make your money work for you.</p>
        <h4 class="fade-in fade-in-second">다양한 금융 서비스를 통해 최적의 재테크와 투자 솔루션을 제공합니다.</h4>
      </div>
    </div>

    <!-- 스크롤로 보여줄 다양한 정보 섹션 -->
    <div class="section scroll-section" :style="{ backgroundImage: `url(${home2})` }">
      <div class="content" :class="{ active: activeSection === 2 }">
        <h2 class="fade-in fade-in-first">최고의 예금 상품</h2>
        <br />
        <p class="fade-in fade-in-second">당신의 자산을 불려줄 다양한 예금 상품을 추천드립니다.</p>
      </div>
      <div class="content" :class="{ active: activeSection === 2 }">
        <p>ㅇㄹㅇ</p>
      </div>

      <!-- 동그란 버튼들 -->
      <div class="circle-container">
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

    <div class="section scroll-section" :style="{ backgroundImage: `url(${home3})` }">
      <div class="content" :class="{ active: activeSection === 3 }">
        <h2>투자 트렌드</h2>
        <p>현재 시장에서 가장 인기 있는 투자 트렌드를 확인하세요.</p>
      </div>
    </div>

    <div class="section scroll-section" :style="{ backgroundImage: `url(${home4})` }">
      <div class="content" :class="{ active: activeSection === 4 }">
        <h2>재테크 뉴스</h2>
        <p>실시간으로 제공되는 최신 금융 뉴스로 앞서가세요.</p>
      </div>
    </div>
  </div>
  <footer class="section footer">
    <div class="footer-content" :class="{ active: activeSection === 5 }">
      <p>&copy; 2024 전환점. 모든 권리 보유.</p>
    </div>
  </footer>
</template>
<script>
import "fullpage.js/dist/fullpage.css";
import fullpage from "fullpage.js";
import home1 from "@/assets/home/home1.jpg";
import home2 from "@/assets/home/home2.jpg";
import home3 from "@/assets/home/home3.jpg";
import home4 from "@/assets/home/home4.jpg";

export default {
  name: "HomeView",
  data() {
    return {
      activeSection: 1,
      home1,
      home2,
      home3,
      home4,
    };
  },
  mounted() {
    this.initializeFullPage(); // FullPage.js 초기화
  },
  beforeUnmount() {
    this.destroyFullPage(); // 페이지를 떠날 때 FullPage.js 정리
  },
  methods: {
    initializeFullPage() {
      if (document.querySelector("#fullpage").fp_initialized) return;

      // FullPage.js 초기화
      new fullpage("#fullpage", {
        licenseKey: "YOUR_LICENSE_KEY",
        autoScrolling: true,
        navigation: true,
        navigationPosition: "right",
        scrollHorizontally: true,
        easingcss3: "cubic-bezier(0.25, 0.1, 0.25, 1)",
        scrollingSpeed: 1500,
        responsiveWidth: 768,
        afterLoad: (origin, destination) => {
          this.activeSection = destination.index + 1;
        },
      });
    },
    destroyFullPage() {
      // FullPage.js 정리
      if (document.querySelector("#fullpage").fp_initialized) {
        fullpage_api.destroy("all");
      }

      // FullPage.js가 추가한 전역 스타일 제거
      document.documentElement.style.overflow = "";
      document.body.style.overflow = "";
    },
  },
};
</script>

<style scoped>
/* 전체 페이지 스타일 */
body {
  margin: 0;
  font-family: "Arial", sans-serif;
  overflow: hidden; /* 스크롤 제거 */
}

/* 각 섹션 기본 스타일 */
.section {
  height: 100vh;
  display: flex;
  align-items: flex-start; /* 세로 방향: 위쪽 정렬 */
  justify-content: flex-start; /* 가로 방향: 왼쪽 정렬 */
  text-align: left; /* 텍스트 정렬: 왼쪽 */
  padding: 190px 50px 50px; /* 글자 위치 조정: Y축 40px 내려감 */
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  position: relative;
  overflow: hidden;
}

.section::before {
  content: ""; /* 가상 요소 생성 */
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.4); /* 검은색 반투명 레이어 */
  z-index: 1; /* 콘텐츠보다 뒤에 배치 */
}

.section .content,
.hero-content,
.footer-content {
  position: relative; /* 가상 요소 위에 나타나도록 설정 */
  z-index: 2; /* 가상 요소보다 위에 표시 */
  max-width: 800px; /* 콘텐츠 가로 폭 제한 */
  width: 100%;
}

.hero-section {
  display: flex;
  flex-direction: column;
  align-items: center; /* 가로 중앙 정렬 */
  justify-content: flex-start; /* 세로 방향: 약간 위로 */
  text-align: center;
  padding-top: 16%; /* 상단 여백 추가 */
  height: 100vh; /* 섹션 높이를 화면 전체로 설정 */
  background: url("@/assets/home/home1.jpg") no-repeat center center/cover; /* 배경 이미지 설정 */
  color: white; /* 텍스트 색상 */
  /* text-shadow: 0 2px 4px rgba(0, 0, 0, 0.8); 텍스트 그림자 */
  font-size: 88px;
  font-weight: bold;
}

.hero-content {
  opacity: 0; /* 초기 상태 숨김 */
  transform: translateY(40px); /* 초기 위치 */
  transition: all 0.8s ease-in-out; /* 부드러운 전환 효과 */
  width: 100%;
}
.content h2 {
  opacity: 0; /* 처음에는 숨김 */
  transform: translateY(40px); /* 초기 위치를 아래로 이동 */
  transition: all 0.8s ease-in-out; /* 부드러운 전환 효과 */
  color: white;
  font-size: 50px;
  width: 100%;
}
.content p {
  opacity: 0; /* 처음에는 숨김 */
  transform: translateY(40px); /* 초기 위치를 아래로 이동 */
  transition: all 0.8s ease-in-out; /* 부드러운 전환 효과 */
  color: white;
}

.hero-content.active {
  opacity: 1; /* 활성화 시 보이도록 설정 */
  transform: translateY(0); /* 제자리로 이동 */
}
.content.active h2,
.content.active p {
  opacity: 1; /* 활성화 시 보임 */
  transform: translateY(0); /* 제자리로 이동 */
  width: 100%;
}

.scroll-section {
  color: white;
  background-color: rgba(0, 0, 0, 0.5); /* 투명한 배경 위에 이미지 */
}

.scroll-section:nth-child(even) {
  background-color: rgba(255, 255, 255, 0.5);
  color: black;
}

.footer {
  background-color: #333;
  color: white;
  text-align: left;
  padding: 50px;
}

.footer-content {
  opacity: 0;
  transform: translateY(40px);
  transition: all 0.8s ease-in-out;
}

.footer-content.active {
  opacity: 1;
  transform: translateY(0);
}

/* 반응형 디자인 */
@media screen and (max-width: 768px) {
  .section {
    padding: 30px;
  }

  .hero-content {
    font-size: 36px;
  }

  .content {
    font-size: 18px;
  }
}
.fade-in {
  opacity: 0; /* 초기 상태 숨김 */
  transform: translateY(30px); /* 초기 위치 설정 */
  transition: opacity 1s ease, transform 1s ease; /* 부드러운 전환 효과 */
}

/* p 태그에 대한 애니메이션 */
.fade-in-first {
  transition-delay: 0.2s; /* 0.2초 딜레이 */
}

/* h4 태그에 대한 애니메이션 */
.fade-in-second {
  transition-delay: 0.6s; /* 0.6초 딜레이 */
}

/* 활성화 상태에서 애니메이션 */
.hero-content.active .fade-in {
  opacity: 1; /* 보이게 설정 */
  transform: translateY(0); /* 원래 위치로 이동 */
}
/* Circle Links 스타일 */
.circle-container {
  position: absolute;
  bottom: 10%; /* 화면 아래에 배치 */
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 20px;
  z-index: 10;
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
  transition: all 0.3s ease-in-out;
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
</style>
