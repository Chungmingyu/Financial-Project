<template>
  <div>
    <h1>회원가입</h1>
    <form @submit.prevent="handleRegister">
      <input v-model="formData.username" placeholder="이름" required />
      <input v-model="formData.password1" type="password" placeholder="비밀번호" required />
      <input v-model="formData.password2" type="password" placeholder="비밀번호 확인" required />
      <input v-model="formData.email" type="email" placeholder="이메일" required />
      <input v-model="formData.nickname" placeholder="닉네임" required />
      <select v-model="formData.gender" required>
        <option value="M">남성</option>
        <option value="W">여성</option>
      </select>
      <input v-model="formData.age" type="number" placeholder="나이" required />
      <button type="submit">회원가입</button>
    </form>
  </div>
</template>

<script>
import { reactive } from "vue"; // reactive 함수 가져오기
import { useUserStore } from "../stores/user"; // Pinia Store import
import { useRouter } from "vue-router"; // vue-router에서 useRouter 임포트

export default {
  setup() {
    const userStore = useUserStore();
    const router = useRouter(); // useRouter 호출하여 router 객체 받기

    // formData를 reactive로 관리
    const formData = reactive({
      username: "",
      password1: "",
      password2: "",
      email: "",
      nickname: "",
      gender: "",
      age: null,
    });

    // 회원가입 처리 메서드
    const handleRegister = async () => {
      try {
        // formData를 사용해 회원가입 처리
        console.log(formData);
        await userStore.registerUser(formData,router);
        console.log("회원가입 완료");
      } catch (error) {
        console.error("회원가입 중 오류 발생", error);
      }
    };

    // return을 통해 formData와 handleRegister 메서드를 반환하여 템플릿에서 사용
    return {
      formData,
      handleRegister,
      userStore,
    };
  },
};
</script>
