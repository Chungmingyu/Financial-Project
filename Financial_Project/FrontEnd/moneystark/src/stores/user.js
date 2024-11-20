import { defineStore } from 'pinia';
import axiosInstance from './api/userStore'; // axiosInstance를 import
import { useRouter } from 'vue-router';
export const useUserStore = defineStore('user', {
  state: () => ({
    user: null,
    token: localStorage.getItem('authToken') || null,
  }),
  getters: {
    isLoggedIn: (state) => !!state.token
  },
  actions: {
    async registerUser(formData) {
      console.log('폼 데이터:', formData)
      try {
        const response = await axiosInstance.post('accounts/signup/', formData);
        console.log('회원가입 성공:', response.data);
      } catch (error) {
        if (error.response && error.response.data) {
          console.error('회원가입 실패:', error.response.data);  // 구체적인 오류 메시지 출력
        } else {
          console.error('회원가입 실패:', error);
        }
        throw error;
      }
    },
    
    async loginUser(credentials) {
      try {
        const response = await axiosInstance.post('accounts/login/', credentials);
        if (response && response.data) {
          this.user = response.data.user;
          this.token = response.data.key;
          localStorage.setItem('authToken', this.token);
          console.log('로그인 성공:', response.data);
        } else {
          throw new Error('Unexpected response format');
        }
      } catch (error) {
        console.error(
          '로그인 실패:',
          error.response?.data || error.message || 'Unknown error'
        );
        throw error;
      }
    },
    
    async fetchUser() {
      try {
        const response = await axiosInstance.get('accounts/user/');
        this.user = response.data;
        console.log('사용자 정보 가져오기 성공:', response.data);
      } catch (error) {
        console.error('사용자 정보 가져오기 실패:', error.response.data);
        throw error;
      }
    },
    logout() {
      this.token = null;
      this.user = null;
      localStorage.removeItem('authToken'); // 로컬 스토리지에서 토큰 삭제
      console.log('로그아웃 성공');
    },
    async updateUser(updatedData) {
      try {
        // PATCH 요청을 사용하여 필요한 정보만 수정하도록 수정
        const response = await axiosInstance.patch('accounts/user/', updatedData, {
          headers: {
            Authorization: `Bearer ${this.token}`,
          },
        });
        
        // 서버에서 수정된 사용자 정보를 받아와서 상태를 갱신
        this.user = response.data;  
        console.log('사용자 정보 업데이트 성공:', response.data);
      } catch (error) {
        // 오류 처리: 응답 데이터가 있을 경우와 없을 경우를 구분하여 출력
        console.error('사용자 정보 수정 실패:', error.response ? error.response.data : error);
        throw error; // 에러를 다시 던져서 호출하는 컴포넌트에서 처리할 수 있도록 함
      }
    },
    async containProduct(productData) {
      try {
        // 제품 정보 업데이트를 위한 PATCH 요청을 보냅니다.
        const response = await axiosInstance.patch('accounts/user/update/', {
          deposit_fin_prdt_cd: productData.deposit_fin_prdt_cd || null,  // DepositProduct ID
          saving_fin_prdt_cd: productData.saving_fin_prdt_cd || null,    // SavingProduct ID
        }, {
          headers: {
            Authorization: `Bearer ${this.token}`, // 토큰 인증 헤더 추가
          }
        });
    
        // 서버에서 응답한 데이터로 사용자 정보를 갱신
        this.user = response.data;
        console.log('사용자 제품 정보 업데이트 성공:', response.data);
    
      } catch (error) {
        // 오류 처리
        console.error('제품 정보 추가 실패:', error.response ? error.response.data : error);
        throw error; // 호출하는 컴포넌트에서 에러를 처리할 수 있도록 에러를 다시 던짐
      }
    }
    
    
  },
});