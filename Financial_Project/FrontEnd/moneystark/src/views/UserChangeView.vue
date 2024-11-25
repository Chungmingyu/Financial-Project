<template>
  <div class="user-change-container">
    <!-- 뒤로가기 버튼 -->
    <button class="back-button" @click.prevent="$router.push({ name: 'UserDetailView' })">
      <i class="mdi mdi-arrow-left"></i>
      뒤로가기
    </button>

    <h1>
      <i class="mdi mdi-account-edit-outline"></i>
      회원정보 수정
    </h1>
    <p class="description">회원님의 정보를 수정할 수 있습니다. 변경할 내용을 입력하고 저장 버튼을 눌러주세요.</p>
    <form @submit.prevent="updateUserInfo" class="user-form">
      <div class="form-group">
        <label for="nickname">닉네임</label>
        <input v-model="nickname" id="nickname" type="text" />
      </div>

      <div class="form-group">
        <label for="gender">성별</label>
        <select v-model="gender" id="gender">
          <option value="M">남성</option>
          <option value="W">여성</option>
        </select>
      </div>

      <div class="form-group">
        <label for="age">나이</label>
        <input v-model="age" id="age" type="number" />
      </div>

      <button type="submit" class="submit-button">
        <i class="mdi mdi-content-save-outline"></i>
        회원정보 수정
      </button>
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

<style scoped>
/* 컨테이너 스타일 */
.user-change-container {
  max-width: 600px;
  margin: 20px auto;
  padding: 20px;
  background: #ffffff;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

/* 뒤로가기 버튼 스타일 */
.back-button {
  background: #007bff;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-weight: bold;
  transition: background 0.3s;
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.back-button i {
  margin-right: 5px;
}

.back-button:hover {
  background: #0056b3;
}

/* 설명 스타일 */
.description {
  font-size: 16px;
  color: #555;
  margin-bottom: 20px;
}

/* 헤더 스타일 */
h1 {
  display: flex;
  align-items: center;
  font-size: 24px;
  color: #333;
  margin-bottom: 10px;
}

h1 i {
  margin-right: 10px;
}

/* 폼 스타일 */
.user-form {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  font-size: 14px;
  color: #333;
  margin-bottom: 5px;
}

input[type="text"],
input[type="number"],
select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.3s, box-shadow 0.3s;
}

input[type="text"]:focus,
input[type="number"]:focus,
select:focus {
  border-color: #007bff;
  box-shadow: 0 0 8px rgba(0, 123, 255, 0.2);
}

/* 제출 버튼 스타일 */
.submit-button {
  background: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  transition: background 0.3s, box-shadow 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.submit-button i {
  margin-right: 5px;
}

.submit-button:hover {
  background: #0056b3;
  box-shadow: 0 4px 8px rgba(0, 86, 179, 0.4);
}

/* 반응형 스타일 */
@media (max-width: 768px) {
  .user-change-container {
    padding: 15px;
  }

  h1 {
    font-size: 20px;
  }

  .submit-button {
    padding: 8px 15px;
    font-size: 14px;
  }
}
</style>
