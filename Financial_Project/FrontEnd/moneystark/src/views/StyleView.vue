<template>
  <div class="titles-page">
    <button style="display: flex" @click.prevent="$router.push({ name: 'UserDetailView' })">뒤로가기</button>
    <!-- 제목 및 설명 -->
    <header class="header">
      <div class="header-content">
        <h1>투자 칭호와 레벨</h1>
        <p>투자 경험과 능력을 반영한 특별한 칭호입니다. 당신의 칭호를 확인하고 투자 여정을 이어가세요!</p>
      </div>
    </header>

    <!-- 레벨별 섹션 -->
    <div class="level-section" v-for="(titles, level) in levelTitles" :key="level">
      <div class="level-header">
        <h2 class="level-title">{{ level }}</h2>
        <p class="level-description">이 레벨에 해당하는 투자자 칭호입니다.</p>
      </div>
      <div class="title-grid">
        <div v-for="title in titles" :key="title" class="title-card" :class="{ 'highlight-card': title === store.user }">
          <!-- {{ store.user }} -->
          <div class="icon-wrapper">
            <i :class="titleIcons[title]" class="title-icon"></i>
          </div>
          <h3 class="title-name">{{ title }}</h3>
          <p class="title-description">{{ getDescription(title) }}</p>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { useUserStore } from "../stores/user";
export default {
  setup() {
    // 칭호와 아이콘
    const store = useUserStore();
    console.log(store.user);
    const titleIcons = {
      "투자 초보": "fas fa-seedling",
      "무지의 용사": "fas fa-user-shield",
      "금융 신입": "fas fa-baby",
      "중급 투자자": "fas fa-user-tie",
      "투자 도전자": "fas fa-fist-raised",
      "금융 중수": "fas fa-graduation-cap",
      "고급 투자자": "fas fa-chess-knight",
      "숙련된 전략가": "fas fa-brain",
      "금융 마에스트로": "fas fa-magic",
      "전설의 투자자": "fas fa-crown",
      "투자의 마스터": "fas fa-user-secret",
      "엘리트 금융 전문가": "fas fa-gem",
    };

    // 레벨별 칭호
    const levelTitles = {
      "레벨 0-10": ["투자 초보", "무지의 용사", "금융 신입"],
      "레벨 11-20": ["중급 투자자", "투자 도전자", "금융 중수"],
      "레벨 21-30": ["고급 투자자", "숙련된 전략가", "금융 마에스트로"],
      "레벨 31-40": ["전설의 투자자", "투자의 마스터", "엘리트 금융 전문가"],
    };

    // 사용자 칭호 (예: 동적으로 설정 가능)
    const userTitle = "금융 마에스트로";

    // 칭호 설명
    const getDescription = (title) => {
      const descriptions = {
        "투자 초보": "투자의 세계에 막 발을 들인 초보자.",
        "무지의 용사": "금융을 배우는 용감한 시작자.",
        "금융 신입": "금융 세계에서 첫발을 내딛은 사람.",
        "중급 투자자": "투자 경험을 쌓으며 성장 중인 투자자.",
        "투자 도전자": "끊임없이 도전하는 열정적인 투자자.",
        "금융 중수": "금융에 대한 깊이 있는 이해를 가진 사람.",
        "고급 투자자": "투자에서 통찰력을 발휘하는 전문가.",
        "숙련된 전략가": "정교한 전략으로 투자를 이끄는 리더.",
        "금융 마에스트로": "금융의 진정한 대가, 마에스트로.",
        "전설의 투자자": "투자계의 전설로 불리는 상징적 존재.",
        "투자의 마스터": "투자의 마스터로 불리는 고수.",
        "엘리트 금융 전문가": "금융 분야의 엘리트, 최고의 전문가.",
      };
      return descriptions[title] || "설명이 없는 칭호입니다.";
    };

    return {
      titleIcons,
      levelTitles,
      userTitle,
      getDescription,
      store,
    };
  },
};
</script>

<style scoped>
.titles-page {
  background: linear-gradient(120deg, #f0f4ff, #e8f5e9);
  padding: 50px 20px;
  font-family: "Roboto", sans-serif;
  color: #333;
  text-align: center;
  min-height: 100vh;
}

.header h1 {
  font-size: 3rem;
  color: #007bff;
  margin-bottom: 10px;
}

.header p {
  font-size: 1.2rem;
  color: #555;
}

.level-section {
  margin-bottom: 50px;
}

.level-title {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 20px;
  color: #007bff;
}

.title-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.title-card {
  background: #ffffff;
  border-radius: 15px;
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
  padding: 20px;
  text-align: center;
  transition: transform 0.3s, box-shadow 0.3s;
}

.title-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 25px rgba(0, 0, 0, 0.2);
}

.icon-wrapper {
  background: #f0f4ff;
  width: 80px;
  height: 80px;
  margin: 0 auto 15px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.title-icon {
  font-size: 2.5rem;
  color: #007bff;
}

.title-name {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 10px;
}

.title-description {
  font-size: 1rem;
  color: #555;
  margin: 0;
}

/* 강조된 칭호 카드 스타일 */
.highlight-card {
  border: 3px solid #ff9800;
  box-shadow: 0 10px 20px rgba(255, 152, 0, 0.5);
  transform: scale(1.1);
  background: linear-gradient(120deg, #fff3e0, #ffe0b2);
}
</style>
