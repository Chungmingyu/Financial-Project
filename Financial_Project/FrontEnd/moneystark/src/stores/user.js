import { defineStore } from "pinia";
import axiosInstance from "./api/userStore"; // axiosInstance를 import
export const useUserStore = defineStore("user", {
  state: () => ({
    user: null,
    token: localStorage.getItem("authToken") || null,
  }),
  getters: {
    isLoggedIn: (state) => !!state.token,
  },
  actions: {
    // 회원탈퇴
    // 회원조회
    async registerUser(formData, router) {
      console.log("폼 데이터:", formData);
      try {
        const response = await axiosInstance.post("accounts/signup/", formData);
        console.log("회원가입 성공:", response.data);
        router.push({ name: "LogInView" });
      } catch (error) {
        if (error.response && error.response.data) {
          console.error("회원가입 실패:", error.response.data); // 구체적인 오류 메시지 출력
        } else {
          console.error("회원가입 실패:", error);
        }
        throw error;
      }
    },

    async loginUser(credentials) {
      try {
        const response = await axiosInstance.post("accounts/login/", credentials);
        if (response && response.data) {
          this.user = response.data.user;
          this.token = response.data.key;
          localStorage.setItem("authToken", this.token);
          console.log("로그인 성공:", response.data);
        } else {
          throw new Error("Unexpected response format");
        }
      } catch (error) {
        console.error("로그인 실패:", error.response?.data || error.message || "Unknown error");
        throw error;
      }
    },

    async fetchUser() {
      try {
        const response = await axiosInstance.get("accounts/user/");
        this.user = response.data;
        console.log(this.user);
        // console.log("사용자 정보 가져오기 성공:", response.data);
      } catch (error) {
        console.error("사용자 정보 가져오기 실패:", error.response.data);
        throw error;
      }
    },
    logout() {
      this.token = null;
      this.user = null;
      localStorage.removeItem("authToken"); // 로컬 스토리지에서 토큰 삭제
      console.log("로그아웃 성공");
    },

    async deleteUser() {
      try {
        const response = await axiosInstance.delete('accounts/delete/');
        alert(response.data.message);
        console.log(response.data.message)
        useUserStore.logout
        this.user = null; // 회원 탈퇴 후 유저 정보를 초기화
        this.token = null
        localStorage.removeItem("authToken");
        // router.push({name: 'home'})
      } catch (error) {
        console.error('회원탈퇴 중 오류 발생:', error);
        alert('회원탈퇴에 실패했습니다.');
      }
    },
    async updateUser(updatedData, router) {
      try {
        // PATCH 요청을 사용하여 필요한 정보만 수정하도록 수정
        const response = await axiosInstance.patch("accounts/user/", updatedData, {
          headers: {
            Authorization: `Bearer ${this.token}`,
          },
        });

        // 서버에서 수정된 사용자 정보를 받아와서 상태를 갱신
        this.user = response.data;
        console.log("사용자 정보 업데이트 성공:", response.data);
        router.push({ name: "UserDetailView" });
      } catch (error) {
        // 오류 처리: 응답 데이터가 있을 경우와 없을 경우를 구분하여 출력
        console.error("사용자 정보 수정 실패:", error.response ? error.response.data : error);
        throw error; // 에러를 다시 던져서 호출하는 컴포넌트에서 처리할 수 있도록 함
      }
    },
  },
});
