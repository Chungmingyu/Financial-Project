<template>
  <div class="login-container">
    <h2>
      <i class="mdi mdi-login"></i>
      로그인
    </h2>
    <!-- 에러 메시지 표시 영역 -->
    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </div>
    <form @submit.prevent="handlerLogin" class="login-form">
      <div class="form-group">
        <input v-model="formData.email" type="email" placeholder="Email" />
      </div>
      <div class="form-group">
        <input v-model="formData.password" type="password" placeholder="Password" />
      </div>
      <div class="form-group checkbox-group">
        <input type="checkbox" id="rememberMe" style="width: 30px" />
        <label for="rememberMe">로그인 정보 저장</label>
      </div>
      <div class="form-group">
        <button type="submit" class="btn primary">Log in</button>
      </div>
      <div class="form-group">
        <button 
          type="button" 
          class="btn secondary" 
          @click.prevent="$router.push({ name: 'SignUpView' })"
        >
          회원가입
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import { useUserStore } from "../stores/user";
import { useRouter } from "vue-router";

export default {
  data() {
    return {
      formData: {
        email: "",
        password: "",
      },
      errorMessage: "", // 에러 메시지를 저장할 상태 추가
    };
  },
  setup() {
    const userStore = useUserStore();
    const router = useRouter();

    if (userStore.isLoggedIn) {
      router.push({ name: "home" });
    }

    return {
      userStore,
      router,
    };
  },
  methods: {
    async handlerLogin() {
      try {
        // 에러 메시지 초기화
        this.errorMessage = "";
        
        // 입력 값 검증
        if (!this.formData.email || !this.formData.password) {
          this.errorMessage = "이메일과 비밀번호를 모두 입력해주세요.";
          return;
        }

        const credentials = {
          username: this.formData.email,
          password: this.formData.password,
        };

        await this.userStore.loginUser(credentials);
        console.log("로그인 성공");
        
        window.history.back();
        window.location.reload();
      } catch (error) {
        // 에러 메시지 설정
        if (error.response) {
          // 서버에서 받은 에러 메시지가 있는 경우
          this.errorMessage = error.response.data.message || "로그인에 실패했습니다.";
        } else if (error.request) {
          // 서버에 요청이 도달하지 못한 경우
          this.errorMessage = "서버와의 연결에 실패했습니다. 잠시 후 다시 시도해주세요.";
        } else {
          // 기타 에러
          this.errorMessage = "로그인 중 오류가 발생했습니다. 다시 시도해주세요.";
        }
        console.error("로그인 실패:", error.response ? error.response.data : error);
      }
    },
  },
};
</script>

<style scoped>
/* 기존 스타일은 유지하고 에러 메시지 스타일 추가 */
.error-message {
  background-color: #fee2e2; /* 연한 빨간색 배경 */
  color: #dc2626; /* 빨간색 텍스트 */
  padding: 10px;
  margin-bottom: 15px;
  border-radius: 5px;
  font-size: 14px;
  width: 100%;
  text-align: center;
  border: 1px solid #fecaca;
}

/* 기존 스타일들... */
.login-container {
  max-width: 400px;
  margin: 50px auto;
  padding: 20px;
  background: #ffffff;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
  align-content: center;
  position: relative;
  transform: translateY(70%);
}
/* 컨테이너 스타일 */
.login-container {
  max-width: 400px;
  margin: 50px auto;
  padding: 20px;
  background: #ffffff;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
  align-content: center;
  position: relative;
  transform: translateY(70%);
}

/* 헤더 스타일 */
h2 {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: #333;
  margin-bottom: 20px;
}

h2 i {
  margin-right: 10px;
}

/* 폼 스타일 */
.login-form {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.form-group {
  margin-bottom: 15px;
  width: 100%;
}

input[type="email"],
input[type="password"] {
  width: 100%;
  padding: 10px;
  font-size: 15px;
  border: 1px solid #ccc;
  border-radius: 5px;
  outline: none;
  transition: border-color 0.3s, box-shadow 0.3s;
}

input[type="email"]:focus,
input[type="password"]:focus {
  border-color: #007bff;
  box-shadow: 0 0 8px rgba(0, 123, 255, 0.2);
}

/* 체크박스 스타일 */
.checkbox-group {
  display: flex;
  align-items: center;
  justify-content: flex-start;
  width: 100%;
}

.checkbox-group input[type="checkbox"] {
  margin-right: 5px;
}

.checkbox-group label {
  font-size: 14px;
  color: #555;
  margin: 0;
}

/* 버튼 스타일 */
.btn {
  width: 100%;
  padding: 10px;
  font-size: 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.3s, box-shadow 0.2s;
}

.btn.primary {
  background-color: #007bff;
  color: white;
}

.btn.primary:hover {
  background-color: #0056b3;
  box-shadow: 0 4px 8px rgba(0, 86, 179, 0.4);
}

.btn.secondary {
  background-color: #6c757d;
  color: white;
}

.btn.secondary:hover {
  background-color: #5a6268;
  box-shadow: 0 4px 8px rgba(90, 98, 104, 0.4);
}

/* 반응형 스타일 */
@media (max-width: 768px) {
  .login-container {
    padding: 15px;
  }

  h2 {
    font-size: 20px;
  }

  .btn {
    padding: 8px 15px;
    font-size: 14px;
  }
}
</style>
