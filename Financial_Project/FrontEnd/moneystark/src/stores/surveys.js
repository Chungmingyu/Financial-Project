import axiosInstance from "./api/userStore";
import { defineStore } from "pinia";
import { ref, computed } from "vue";

export const useSurveysStore = defineStore("surveys", () => {
  const answers = ref([]); // 설문 응답

  // 답변을 스토어에 설정하는 함수
  const setAnswers = (newAnswers) => {
    answers.value = newAnswers;
    console.log(answers.value);
  };

  // 서버에 점수만 저장하는 함수
  const saveAnswers = async () => {
    const totalScore = answers.value.reduce((acc, curr) => acc + curr, 0); // 점수 총합 계산

    try {
      const response = await axiosInstance.post("/surveys/submit/", {
        tendency: totalScore, // 점수 총합만 전송
      });
      console.log("Response:", response.data);
    } catch (error) {
      console.error("Error saving answers:", error.response?.data || error);
    }
  };

  // 총합 계산하기 (computed 속성)
  const totalScore = computed(() => {
    return answers.value.reduce((acc, curr) => acc + curr, 0);
  });

  return { answers, setAnswers, saveAnswers, totalScore };
});
