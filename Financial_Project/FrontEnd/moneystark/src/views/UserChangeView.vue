<template>
  <div>
    <h1>회원정보 수정</h1>
    <form @submit.prevent="updateUserInfo">
      <label for="nickname">닉네임</label>
      <input v-model="nickname" id="nickname" type="text" />

      <label for="gender">성별</label>
      <select v-model="gender" id="gender">
        <option value="M">남성</option>
        <option value="W">여성</option>
      </select>

      <label for="age">나이</label>
      <input v-model="age" id="age" type="number" />

      <button type="submit">회원정보 수정</button>
    </form>
  </div>
</template>

<script>
import { useUserStore } from "../stores/user";
import { useRouter } from "vue-router";

export default {
  data() {
    const router = useRouter();
    return {
      nickname: "", // 사용자 닉네임
      gender: "", // 사용자 성별
      age: 0, // 사용자 나이
      router,
    };
  },
  computed: {
    // Pinia store의 user 상태를 가져옵니다.
    user() {
      return useUserStore().user;
    },
  },
  methods: {
    async updateUserInfo() {
      // this로 접근하여 data 값들을 제대로 사용해야 합니다
      const updatedData = {
        nickname: this.nickname,
        gender: this.gender,
        age: this.age,
      };

      try {
        // Pinia store에서 제공하는 updateUser 액션 호출
        await useUserStore().updateUser(updatedData, this.router);
        alert("회원정보가 성공적으로 수정되었습니다!");
      } catch (error) {
        alert("회원정보 수정에 실패했습니다.");
        console.error("Error:", error);
      }
    },
  },
  mounted() {
    // 컴포넌트가 마운트되었을 때 사용자 정보를 불러옵니다.
    if (this.user) {
      this.nickname = this.user.nickname;
      this.gender = this.user.gender;
      this.age = this.user.age;
    }
  },
};
</script>
