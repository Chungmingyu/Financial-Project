<template>
  <div class="signup-container">
    <h2>
      <i class="mdi mdi-account-plus"></i>
      회원가입
    </h2>
    <!-- 에러 메시지 표시 영역 -->
    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </div>
    <form @submit.prevent="handleRegister" class="signup-form">
      <div class="form-group">
        <input 
          v-model="formData.username" 
          placeholder="이름" 
          required 
          @blur="validateField('username')"
        />
        <span v-if="fieldErrors.username" class="field-error">{{ fieldErrors.username }}</span>
      </div>
      <div class="form-group">
        <input 
          v-model="formData.email" 
          type="email" 
          placeholder="이메일" 
          required
          @blur="validateField('email')"
        />
        <span v-if="fieldErrors.email" class="field-error">{{ fieldErrors.email }}</span>
      </div>
      <div class="form-group">
        <input 
          v-model="formData.password1" 
          type="password" 
          placeholder="비밀번호" 
          required
          @blur="validateField('password1')"
        />
        <span v-if="fieldErrors.password1" class="field-error">{{ fieldErrors.password1 }}</span>
      </div>
      <div class="form-group">
        <input 
          v-model="formData.password2" 
          type="password" 
          placeholder="비밀번호 확인" 
          required
          @blur="validateField('password2')"
        />
        <span v-if="fieldErrors.password2" class="field-error">{{ fieldErrors.password2 }}</span>
      </div>
      <div class="form-group">
        <input 
          v-model="formData.nickname" 
          placeholder="닉네임" 
          required
          @blur="validateField('nickname')"
        />
        <span v-if="fieldErrors.nickname" class="field-error">{{ fieldErrors.nickname }}</span>
      </div>
      <div class="form-group select-group">
        <select 
          v-model="formData.gender" 
          required
          @blur="validateField('gender')"
        >
          <option value="" disabled selected>성별을 선택하세요</option>
          <option value="M">남성</option>
          <option value="W">여성</option>
        </select>
        <span v-if="fieldErrors.gender" class="field-error">{{ fieldErrors.gender }}</span>
      </div>
      <div class="form-group">
        <input 
          v-model="formData.age" 
          type="number" 
          placeholder="나이" 
          required
          @blur="validateField('age')"
        />
        <span v-if="fieldErrors.age" class="field-error">{{ fieldErrors.age }}</span>
      </div>
      <div class="form-group">
        <button type="submit" class="btn primary">회원가입</button>
      </div>
      <div class="form-group">
        <button type="button" class="btn secondary" @click="$router.push({ name: 'LogInView' })">
          로그인 페이지로 이동
        </button>
      </div>
    </form>
  </div>
</template>

<script>
import { reactive, ref } from "vue";
import { useUserStore } from "../stores/user";
import { useRouter } from "vue-router";

export default {
  setup() {
    const userStore = useUserStore();
    const router = useRouter();
    const errorMessage = ref("");
    const fieldErrors = reactive({
      username: "",
      email: "",
      password1: "",
      password2: "",
      nickname: "",
      gender: "",
      age: "",
    });

    if (userStore.isLoggedIn) {
      router.push({ name: "home" });
    }

    const formData = reactive({
      username: "",
      password1: "",
      password2: "",
      email: "",
      nickname: "",
      gender: "",
      age: null,
    });

    const validateField = (field) => {
      fieldErrors[field] = ""; // 초기화

      switch (field) {
        case 'username':
          if (formData.username.length < 2) {
            fieldErrors.username = "이름은 2자 이상이어야 합니다.";
          }
          break;
        case 'email':
          const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
          if (!emailRegex.test(formData.email)) {
            fieldErrors.email = "올바른 이메일 형식이 아닙니다.";
          }
          break;
        case 'password1':
          if (formData.password1.length < 8) {
            fieldErrors.password1 = "비밀번호는 8자 이상이어야 합니다.";
          }
          break;
        case 'password2':
          if (formData.password1 !== formData.password2) {
            fieldErrors.password2 = "비밀번호가 일치하지 않습니다.";
          }
          break;
        case 'nickname':
          if (formData.nickname.length < 2) {
            fieldErrors.nickname = "닉네임은 2자 이상이어야 합니다.";
          }
          break;
        case 'gender':
          if (!formData.gender) {
            fieldErrors.gender = "성별을 선택해주세요.";
          }
          break;
        case 'age':
          if (!formData.age || formData.age < 1) {
            fieldErrors.age = "올바른 나이를 입력해주세요.";
          }
          break;
      }
    };

    const validateForm = () => {
      // 모든 필드 검증
      Object.keys(formData).forEach(field => validateField(field));
      
      // 에러가 있는지 확인
      return !Object.values(fieldErrors).some(error => error !== "");
    };

    const handleRegister = async () => {
      try {
        errorMessage.value = ""; // 에러 메시지 초기화
        
        // 폼 전체 검증
        if (!validateForm()) {
          errorMessage.value = "입력 정보를 다시 확인해주세요.";
          return;
        }

        await userStore.registerUser(formData, router);
        console.log("회원가입 완료");
      } catch (error) {
        if (error.response) {
          // 서버에서 받은 에러 메시지 처리
          errorMessage.value = error.response.data.message || "회원가입에 실패했습니다.";
        } else if (error.request) {
          errorMessage.value = "서버와의 연결에 실패했습니다. 잠시 후 다시 시도해주세요.";
        } else {
          errorMessage.value = "회원가입 중 오류가 발생했습니다. 다시 시도해주세요.";
        }
        console.error("회원가입 중 오류 발생:", error.response ? error.response.data : error);
      }
    };

    return {
      formData,
      handleRegister,
      userStore,
      errorMessage,
      fieldErrors,
      validateField,
    };
  },
};
</script>

<style scoped>
/* 기존 스타일 유지하고 에러 메시지 관련 스타일 추가 */
.error-message {
  background-color: #fee2e2;
  color: #dc2626;
  padding: 10px;
  margin-bottom: 15px;
  border-radius: 5px;
  font-size: 14px;
  width: 100%;
  text-align: center;
  border: 1px solid #fecaca;
}

.field-error {
  color: #dc2626;
  font-size: 12px;
  display: block;
  margin-top: 4px;
  text-align: left;
}

/* 에러가 있는 입력 필드 스타일 */
input:invalid,
select:invalid {
  border-color: #dc2626;
}
.signup-container {
  max-width: 400px;
  margin: 50px auto;
  padding: 20px;
  background: #ffffff;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
  position: relative;
  transform: translateY(20%);
}

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

.signup-form {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.form-group {
  margin-bottom: 15px;
  width: 100%;
}

input,
select {
  width: 100%;
  padding: 10px;
  font-size: 15px;
  border: 1px solid #ccc;
  border-radius: 5px;
  outline: none;
  transition: border-color 0.3s, box-shadow 0.3s;
}

input:focus,
select:focus {
  border-color: #007bff;
  box-shadow: 0 0 8px rgba(0, 123, 255, 0.2);
}

select {
  background-color: white;
  cursor: pointer;
}

.select-group select {
  width: 100%;
}

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

@media (max-width: 768px) {
  .signup-container {
    margin: 20px;
    padding: 15px;
    transform: translateY(10%);
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
