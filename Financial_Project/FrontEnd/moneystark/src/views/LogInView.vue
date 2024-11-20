<template>
  <table>
    <tr>
      <td><h2>로그인</h2></td>
    </tr>
    <tr>
      <td><input v-model="formData.email" type="email" placeholder="Email" /></td>
    </tr>
    <tr>
      <td><input v-model="formData.password" type="password" placeholder="Password" /></td>
    </tr>
    <tr>
      <td><input type="checkbox" /> 로그인 정보 저장</td>
    </tr>
    <tr>
      <td><input type="submit" value="Log in" class="btn" @click.prevent="handlerLogin" /></td>
    </tr>
    <tr>
      <td><button @click.prevent="$router.push({ name: 'SignUpView' })">회원가입</button></td>
    </tr>
  </table>
</template>

<script>
import { useUserStore } from '../stores/user';
import { useRouter } from 'vue-router';

export default {
  data() {
    return {
      formData: {
        email: '', // 이메일 필드로 변경
        password: '', // 비밀번호 필드
      },
    };
  },
  setup() {
    const userStore = useUserStore();
    const router = useRouter();

    // 로그인되어 있으면 홈 화면으로 리다이렉트
    if (userStore.isLoggedIn) {
      router.push({ name: 'home' });
    }

    return {
      userStore,
      router,
    };
  },
  methods: {
    // 로그인 처리 함수
    async handlerLogin() {
      try {
        // 로그인 시도
        const credentials = {
          username: this.formData.email,  // 'email'을 'username' 필드에 담아서 로그인 요청
          password: this.formData.password  // 비밀번호
        };

        await this.userStore.loginUser(credentials);
        console.log('로그인 성공');

        // 로그인 후 페이지 새로고침 및 이전 페이지로 돌아가기
        window.history.back();  // 이전 페이지로 돌아가기
        window.location.reload(); // 페이지 새로고침
      } catch (error) {
        console.error('로그인 실패:', error.response ? error.response.data : error);
      }
    }
  },
};
</script>

<style scoped>
table {
  width: 280px;
  height: 250px;
  margin: auto;
  font-size: 15px;
}

input[type='email'],
input[type='password'] {
  width: 250px;
  height: 32px;
  font-size: 15px;
  border: 0;
  border-radius: 15px;
  outline: none;
  padding-left: 10px;
  background-color: rgb(233, 233, 233);
}

.btn {
  width: 263px;
  height: 32px;
  font-size: 15px;
  border: 0;
  border-radius: 15px;
  outline: none;
  padding-left: 10px;
  background-color: rgb(164, 199, 255);
}

.btn:active {
  background-color: rgb(61, 135, 255);
}
</style>
