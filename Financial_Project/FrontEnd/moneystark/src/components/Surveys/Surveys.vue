<template>
  <div class="survey">
    <h2>금융 투자 성향 설문지</h2>
    <form @submit.prevent="submitSurvey">
      <!-- 반복적으로 질문 렌더링 -->
      <div v-for="(question, index) in questions" :key="index" class="question">
        <p>{{ index + 1 }}. {{ question.text }}</p>
        <div v-for="(option, optIndex) in question.options" :key="optIndex" class="option">
          <label class="radio-label">
            <input type="radio" :name="'question' + index" :value="optIndex" v-model="answers[index]" />
            <span>{{ option }}</span>
          </label>
        </div>
      </div>
      <button type="submit">제출</button>
    </form>
  </div>
</template>

<script>
import { ref } from "vue";
import axios from "axios"; // Axios import
import { useSurveysStore } from "../../stores/surveys"; // Pinia store import
import { useRoute, useRouter } from "vue-router";

export default {
  name: "Survey",
  setup() {
    const surveysStore = useSurveysStore(); // Pinia store 사용
    const questions = ref([
      {
        text: "지금까지 투자 경험이 얼마나 있습니까?",
        options: [
          "전혀 없음", // 0점 (소극적)
          "조금 있음",
          "보통",
          "많음",
          "전문가 수준", // 4점 (적극적)
        ],
      },
      {
        text: "귀하의 주요 투자 목적은 무엇입니까?",
        options: [
          "자산 보호", // 0점 (소극적)
          "자산 증가",
          "단기 수익",
          "장기 은퇴 준비",
          "기타", // 4점 (적극적)
        ],
      },
      {
        text: "귀하가 투자금을 인출하지 않고 유지할 수 있는 기간은 어느 정도입니까?",
        options: [
          "1년 미만", // 0점 (소극적)
          "1~3년",
          "3~5년",
          "5년 이상", // 4점 (적극적)
        ],
      },
      {
        text: "귀하가 기대하는 투자 수익률은 어느 정도입니까?",
        options: [
          "5% 이하", // 0점 (소극적)
          "5~10%",
          "10~15%",
          "15% 이상", // 4점 (적극적)
        ],
      },
      {
        text: "손실 가능성을 고려했을 때, 귀하는 어떤 투자를 선호하십니까?",
        options: [
          "손실은 싫지만 수익도 적은 투자", // 0점 (소극적)
          "약간의 손실 가능성을 감수하는 투자",
          "높은 수익과 손실 가능성이 있는 투자", // 4점 (적극적)
        ],
      },
      {
        text: "귀하의 투자 원금이 20% 손실을 본다면 어떻게 반응하시겠습니까?",
        options: [
          "즉시 투자 중단", // 0점 (소극적)
          "일부 회수 고려",
          "그대로 유지",
          "추가 매수", // 4점 (적극적)
        ],
      },
      {
        text: "금융 상품(주식, 채권, 펀드 등)에 대한 귀하의 이해 수준은 어떻습니까?",
        options: [
          "전혀 없음", // 0점 (소극적)
          "기본 지식 있음",
          "상당히 잘 알고 있음",
          "전문가 수준", // 4점 (적극적)
        ],
      },
      {
        text: "귀하의 자산 중 투자에 할당 가능한 비율은 어느 정도입니까?",
        options: [
          "10% 이하", // 0점 (소극적)
          "10~30%",
          "30~50%",
          "50% 이상", // 4점 (적극적)
        ],
      },
      {
        text: "투자한 자산의 가격 변동이 심할 때 귀하의 행동은 무엇입니까?",
        options: [
          "즉시 자산을 매도", // 0점 (소극적)
          "가격 회복까지 기다림",
          "추가 투자 고려", // 4점 (적극적)
        ],
      },
      {
        text: "귀하의 현재 재정 상태는 어떻습니까?",
        options: [
          "저축 중", // 0점 (소극적)
          "대출 상환 중",
          "여유 자금 있음",
          "기타", // 4점 (적극적)
        ],
      },
    ]);

    const answers = ref(Array(questions.value.length).fill(null)); // 사용자의 답변 상태
    const router = useRouter();
    const submitSurvey = () => {
      if (answers.value.includes(null)) {
        alert("모든 질문에 답변해 주세요.");
        return;
      }

      // 답변을 스토어에 설정
      surveysStore.setAnswers(answers.value);

      // 서버에 점수만 저장
      surveysStore
        .saveAnswers()
        .then(() => {
          alert("설문이 제출되었습니다!");
          router.push({ name: "home" });
        })
        .catch((error) => {
          alert("설문 제출에 실패했습니다. 다시 시도해주세요.");
        });
    };

    return {
      questions,
      answers,
      submitSurvey,
    };
  },
};
</script>

<style scoped>
.survey {
  font-family: Arial, sans-serif;
  margin: 20px;
}

.question {
  margin-bottom: 20px;
}

.option {
  margin-bottom: 10px;
}

.radio-label {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
  cursor: pointer;
}

input[type="radio"] {
  margin-right: 10px;
}

button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  font-size: 16px;
}

button:hover {
  background-color: #0056b3;
}
</style>
