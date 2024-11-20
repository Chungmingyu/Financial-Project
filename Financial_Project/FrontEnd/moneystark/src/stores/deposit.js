import { defineStore } from "pinia";
// import axios from "axios";
import axiosInstance from "./api/userStore"; // axiosInstance를 import
export const useDepositStore = defineStore("deposit", {
  state: () => ({
    deposits: [], // 장바구니에 담긴 예금 목록
    loading: false,
    error: null,
  }),
  getters: {
    // 예금 가입 여부 확인 (이미 가입한 예금이 있는지 확인)
    isProductJoined: (state) => {
      return (depositId) => {
        return state.deposits.some((deposit) => deposit.id === depositId);
      };
    },
  },
  actions: {
    async fetchDeposits() {
      this.loading = true;
      this.error = null;
      try {
        const response = await axiosInstance.get("/moneys/deposits/");
        this.deposits = response.data;
      } catch (error) {
        this.error = error.response?.data || "Failed to fetch deposits";
      } finally {
        this.loading = false;
      }
    },
    async addDeposit(depositProductId, depositAmount) {
      this.error = null;

      try {
        // 서버로 전송할 데이터 확인
        console.log(depositProductId);
        console.log(depositAmount);

        // 예금 추가 요청
        const response = await axiosInstance.post("/moneys/deposits/", {
          deposit_product: depositProductId, // 'deposit_product_id'가 아님
          amount: depositAmount,
        });

        // 성공적으로 예금을 추가했다면 deposits에 응답 데이터 추가
        this.deposits.push(response.data);

        // 예금 목록을 다시 가져옴
        await this.fetchDeposits();
      } catch (error) {
        // 오류 메시지를 받아서 처리
        if (error.response && error.response.status === 400) {
          // 400 에러 (이미 존재하는 예금 상품)
          this.error = error.response.data.error || "Failed to add deposit"; // 서버에서 전달된 오류 메시지를 사용
        } else {
          // 그 외의 에러 처리
          this.error = "Failed to add deposit";
        }
      }
    },

    async removeDeposit(depositId) {
      this.error = null;
      try {
        await axiosInstance.delete(`/moneys/deposits/${depositId}/`);
        this.deposits = this.deposits.filter((deposit) => deposit.id !== depositId);
      } catch (error) {
        this.error = error.response?.data || "Failed to remove deposit";
      }
    },
  },
});
