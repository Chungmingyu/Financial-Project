<template>
  <div class="main-page" @wheel="onWheel">
    <!-- 네비게이션 메뉴 -->
    <nav class="nav-bar">
      <ul>
        <li @click="scrollToSection(0)">소개</li>
        <li @click="scrollToSection(1)">서비스</li>
        <li @click="scrollToSection(2)">추천 플랜</li>
        <li @click="scrollToSection(3)">문의</li>
      </ul>
    </nav>

    <!-- 섹션들 -->
    <section v-for="(section, index) in sections" :key="index" :ref="(el) => (sectionRefs[index] = el)" class="section" :class="section.class">
      {{ section.text }}
    </section>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";

export default {
  name: "MainPage",
  setup() {
    const sectionRefs = ref([]);
    const sections = [
      { text: "소개 섹션", class: "intro" },
      { text: "서비스 섹션", class: "service" },
      { text: "추천 플랜 섹션", class: "plan" },
      { text: "문의 섹션", class: "contact" },
    ];
    let currentIndex = ref(0);
    let isScrolling = false;

    // 특정 섹션으로 부드럽게 스크롤
    const scrollToSection = (index) => {
      if (sectionRefs.value[index]) {
        sectionRefs.value[index].scrollIntoView({ behavior: "smooth" });
        currentIndex.value = index;
      }
    };

    // 마우스 휠 이벤트 핸들러
    const onWheel = (event) => {
      if (isScrolling) return;
      isScrolling = true;

      if (event.deltaY > 0 && currentIndex.value < sections.length - 1) {
        // 아래로 스크롤 -> 다음 섹션으로 이동
        currentIndex.value += 1;
      } else if (event.deltaY < 0 && currentIndex.value > 0) {
        // 위로 스크롤 -> 이전 섹션으로 이동
        currentIndex.value -= 1;
      }

      scrollToSection(currentIndex.value);

      // 연속 스크롤 방지를 위해 딜레이 추가
      setTimeout(() => {
        isScrolling = false;
      }, 700);
    };

    return {
      sections,
      sectionRefs,
      scrollToSection,
      onWheel,
    };
  },
};
</script>

<style scoped>
/* 네비게이션 스타일 */
.nav-bar {
  position: fixed;
  top: 0;
  width: 100%;
  background-color: #333;
  color: #fff;
  text-align: center;
  padding: 10px;
  z-index: 100;
}
.nav-bar ul {
  list-style: none;
  display: flex;
  justify-content: space-around;
}
.nav-bar li {
  cursor: pointer;
  padding: 10px;
  transition: color 0.3s;
}
.nav-bar li:hover {
  color: #ffd700;
}

/* 섹션 스타일 */
.section {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 2rem;
}
.intro {
  background-color: #f5a623;
}
.service {
  background-color: #f8e71c;
}
.plan {
  background-color: #7ed321;
}
.contact {
  background-color: #4a90e2;
}
</style>
