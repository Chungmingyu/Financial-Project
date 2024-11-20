<template>
    <div v-if="user">
      <h1>회원 정보</h1>
      <p>이름: {{ user.first_name }} {{ user.last_name }}</p>
      <p>닉네임: {{ user.nickname }}</p>
      <p>성별: {{ user.gender }}</p>
      <p>나이: {{ user.age }}</p>
      <p>이메일: {{ user.email }}</p>
      <button @click="goToEditProfile">회원 정보 수정</button>
    </div>
    <div v-else>
      <p>사용자 정보를 불러오는 중...</p>
    </div>
  </template>
  
  <script>
  import { useUserStore } from '../stores/user';
  import { ref, onMounted } from 'vue';
  import { useRouter } from 'vue-router'
  
  export default {
    setup() {
      const userStore = useUserStore();  // Pinia store 인스턴스 가져오기
      const user = ref(null);  // 반응형으로 사용자 정보 관리
      const error = ref(null);  // 에러 상태 관리
      const router = useRouter()
  
      // 사용자 정보를 가져오는 함수
      const fetchUserData = async () => {
        try {
          await userStore.fetchUser();  // 사용자 정보 가져오기
          user.value = userStore.user;  // 가져온 사용자 정보 저장
          console.log('Fetched User:', user.value);  // 데이터 확인
        } catch (err) {
          error.value = '사용자 정보를 불러오는 데 실패했습니다.';  // 에러 처리
          console.error(err);  // 에러 로그 출력
        }
      };
  
      // 수정 페이지로 이동하는 함수
      const goToEditProfile = () => {
        router.push({ name: 'UserChangeView' });  // 수정 페이지로 이동
      };
  
      // 컴포넌트가 마운트되었을 때 사용자 정보 가져오기
      onMounted(fetchUserData);
  
      // 템플릿에서 사용할 데이터 반환
      return {
        user,
        error,
        goToEditProfile
      };
    }
  };
  </script>
  