<template>
  <div>
    <!-- 상단 이미지 섹션 -->
    <section id="hero-section">
      <div class="hero-content">
        <p>Make your money work for you.</p>
        <h1>전환점</h1>
      </div>
    </section>

    <!-- 스크롤로 보여줄 다양한 정보 섹션 -->
    <section id="section1" class="scroll-section">
      <div class="content">
        <h2>최고의 예금 상품</h2>
        <p>당신의 자산을 불려줄 다양한 예금 상품을 추천드립니다.</p>
      </div>
    </section>

    <section id="section2" class="scroll-section">
      <div class="content">
        <h2>투자 트렌드</h2>
        <p>현재 시장에서 가장 인기 있는 투자 트렌드를 확인하세요.</p>
      </div>
    </section>

    <section id="section3" class="scroll-section">
      <div class="content">
        <h2>재테크 뉴스</h2>
        <p>실시간으로 제공되는 최신 금융 뉴스로 앞서가세요.</p>
      </div>
    </section>

    <footer id="footer">
      <p>&copy; 2024 전환점. 모든 권리 보유.</p>
    </footer>
  </div>
</template>

<script>
import { onMounted } from "vue";
import ScrollMagic from "scrollmagic";
import { gsap } from "gsap";
import { ScrollMagicPluginGsap } from "scrollmagic-plugin-gsap";

// ScrollMagic과 GSAP 플러그인을 연결
ScrollMagicPluginGsap(ScrollMagic, gsap);

export default {
  name: "HomeView",
  setup() {
    onMounted(() => {
      const controller = new ScrollMagic.Controller();

      // 각 섹션 애니메이션 추가
      document.querySelectorAll(".scroll-section").forEach((section) => {
        const tween = gsap.fromTo(section.querySelector(".content"), { opacity: 0, y: 50 }, { opacity: 1, y: 0, duration: 1 });

        new ScrollMagic.Scene({
          triggerElement: section,
          triggerHook: 0.8,
          reverse: false,
        })
          .setTween(tween)
          .addTo(controller);
      });
    });
  },
};
</script>

<style scoped>
/* 전체 페이지 스타일 */
body {
  margin: 0;
  font-family: "Arial", sans-serif;
  scroll-behavior: smooth;
}
section {
  height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 20px;
}
#hero-section {
  display: flex;
  flex-direction: column; /* 수직 정렬 */
  align-items: center; /* 수평 가운데 정렬 */
  justify-content: flex-start; /* 위로 정렬 */
  height: 100vh;
  background: url("@/assets/home/home1.jpg") no-repeat center center/cover;
  color: white;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.8);
}

.hero-content {
  margin-top: 500px; /* 위쪽 여백 조정 */
  text-align: center;
  font-size: 100px;
  font-family: "Noto Sans", sans-serif;
  font-optical-sizing: auto;
  font-weight: 700;
  font-style: normal;
  font-variation-settings: "wdth" 100;
  font-size: 100px;
}

.scroll-section {
  background-color: #f8f9fa;
  border-bottom: 1px solid #ddd;
}
.scroll-section:nth-child(even) {
  background-color: #e9ecef;
}
.content h2 {
  font-size: 2rem;
  margin-bottom: 1rem;
}
.content p {
  font-size: 1.2rem;
  line-height: 1.6;
}
#footer {
  background-color: #333;
  color: white;
  text-align: center;
  padding: 20px;
}
</style>
