<template>
  <div class="survey-container">
    <h2>금융 투자 성향 설문지</h2>
    <div v-if="currentQuestionIndex < questions.length">
      <!-- 현재 질문 표시 -->
      <div class="question">
        <p class="question-text">
          {{ currentQuestionIndex + 1 }}. {{ currentQuestion.text }}
        </p>
        <div class="options">
          <button
            v-for="(option, optIndex) in currentQuestion.options"
            :key="optIndex"
            class="option-button"
            @click="selectAnswer(optIndex)"
          >
            {{ optIndex + 1 }}
          </button>
        </div>
        <!-- 선택지 설명 추가 -->
        <div class="option-descriptions">
          <div
            v-for="(option, optIndex) in currentQuestion.options"
            :key="'desc' + optIndex"
            class="option-description"
          >
            <strong>{{ optIndex + 1 }}.</strong> {{ option }}
          </div>
        </div>
      </div>
    </div>
    <div v-else>
      <!-- 설문 완료 메시지 -->
      <p class="completion-message">설문이 완료되었습니다. 제출 중...</p>
    </div>
  </div>
</template>

<script>
import { ref, computed } from "vue";
import { useSurveysStore } from "../../stores/surveys";
import { useRouter } from "vue-router";

export default {
  name: "Survey",
  setup() {
    const surveysStore = useSurveysStore();
    const router = useRouter();

    // 질문 데이터
    const questions = ref([
      {
        text: "지금까지 투자 경험이 얼마나 있습니까?",
        options: ["전혀 없음", "조금 있음", "보통", "많음", "전문가 수준"],
      },
      {
        text: "귀하의 주요 투자 목적은 무엇입니까?",
        options: ["자산 보호", "자산 증가", "단기 수익", "장기 은퇴 준비", "인생을 걸었음"],
      },
      {
        text: "귀하가 투자금을 인출하지 않고 유지할 수 있는 기간은 어느 정도입니까?",
        options: ["1년 미만", "1~3년", "3~5년", "5년 이상"],
      },
      {
        text: "귀하가 기대하는 투자 수익률은 어느 정도입니까?",
        options: ["5% 이하", "5~10%", "10~15%", "15% 이상"],
      },
      {
        text: "손실 가능성을 고려했을 때, 귀하는 어떤 투자를 선호하십니까?",
        options: [
          "손실은 싫지만 수익도 적은 투자",
          "약간의 손실 가능성을 감수하는 투자",
          "높은 수익과 손실 가능성이 있는 투자",
        ],
      },
      {
        text: "귀하의 투자 원금이 20% 손실을 본다면 어떻게 반응하시겠습니까?",
        options: ["즉시 투자 중단", "일부 회수 고려", "그대로 유지", "추가 매수"],
      },
      {
        text: "금융 상품(주식, 채권, 펀드 등)에 대한 귀하의 이해 수준은 어떻습니까?",
        options: ["전혀 없음", "기본 지식 있음", "상당히 잘 알고 있음", "전문가 수준"],
      },
      {
        text: "귀하의 자산 중 투자에 할당 가능한 비율은 어느 정도입니까?",
        options: ["10% 이하", "10~30%", "30~50%", "50% 이상"],
      },
      {
        text: "투자한 자산의 가격 변동이 심할 때 귀하의 행동은 무엇입니까?",
        options: ["즉시 자산을 매도", "가격 회복까지 기다림", "추가 투자 고려"],
      },
      {
        text: "귀하의 현재 재정 상태는 어떻습니까?",
        options: ["저축 중", "대출 상환 중", "여유 자금 있음", "기타"],
      },
    ]);

    const currentQuestionIndex = ref(0); // 현재 질문 인덱스
    const answers = ref([]); // 사용자의 답변 저장

    // 현재 질문 계산
    const currentQuestion = computed(() => {
      return questions.value[currentQuestionIndex.value];
    });

    // 답변 선택 함수
    const selectAnswer = (optIndex) => {
      answers.value.push(optIndex);

      if (currentQuestionIndex.value < questions.value.length - 1) {
        // 다음 질문으로 이동
        currentQuestionIndex.value++;
      } else {
        // 설문 완료 시
        submitSurvey();
      }
    };

    // 설문 제출 함수
    const submitSurvey = () => {
      // 답변을 스토어에 설정
      surveysStore.setAnswers(answers.value);

      // 서버에 점수 저장
      surveysStore
        .saveAnswers()
        .then(() => {
          alert("설문이 제출되었습니다! 부여받은 칭호는 회원정보에서 확인해보세요!");
          router.push({ name: "home" });
        })
        .catch((error) => {
          alert("설문 제출에 실패했습니다. 다시 시도해주세요.");
          console.error(error);
        });
    };

    return {
      questions,
      currentQuestionIndex,
      currentQuestion,
      selectAnswer,
    };
  },
};
</script>

<style scoped>
/* 전체 컨테이너 스타일 */
.survey-container {
  max-width: 600px;
  margin: 60px auto;
  padding: 40px;
  background-color: #ffffff;
  border-radius: 12px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
  font-family: 'Noto Sans KR', sans-serif;
}

/* 제목 스타일 */
.survey-container h2 {
  text-align: center;
  font-size: 2.2rem;
  color: #333;
  margin-bottom: 40px;
}

/* 질문 스타일 */
.question-text {
  font-size: 1.4rem;
  color: #555;
  margin-bottom: 30px;
}

/* 옵션 버튼 스타일 */
.options {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-bottom: 30px;
}

.option-button {
  width: 60px;
  height: 60px;
  background-color: #1890ff;
  color: #fff;
  border: none;
  border-radius: 50%;
  font-size: 1.5rem;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.option-button:hover {
  background-color: #40a9ff;
  transform: translateY(-5px);
}

/* 선택지 설명 스타일 */
.option-descriptions {
  margin-top: 20px;
}

.option-description {
  font-size: 1rem;
  color: #444;
  margin-bottom: 8px;
}

.option-description strong {
  color: #1890ff;
}

/* 설문 완료 메시지 */
.completion-message {
  text-align: center;
  font-size: 1.5rem;
  color: #333;
}

/* 반응형 디자인 */
@media (max-width: 768px) {
  .survey-container {
    padding: 30px;
  }

  .survey-container h2 {
    font-size: 1.8rem;
  }

  .question-text {
    font-size: 1.2rem;
  }

  .option-button {
    width: 50px;
    height: 50px;
    font-size: 1.2rem;
  }

  .option-description {
    font-size: 0.95rem;
  }
}
</style>
