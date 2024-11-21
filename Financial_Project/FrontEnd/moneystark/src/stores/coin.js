// src/stores/cryptoStore.js
import { defineStore } from "pinia";
import axios from "axios";

export const useCryptoStore = defineStore("crypto", {
  state: () => ({
    cryptoData: null, // 코인 데이터 저장
    coinSymbol: "BTC", // 기본 심볼
    coinMarket: "USD", // 기본 시장
    loading: false, // 로딩 상태
    error: null, // 에러 상태
  }),
  getters: {
    cryptoDataArray: (state) => {
      if (!state.cryptoData) return [];
      return Object.entries(state.cryptoData).map(([time, data]) => ({
        time,
        ...data,
      }));
    },
    latestCryptoData: (state) => {
      if (!state.cryptoData) return null;
      const keys = Object.keys(state.cryptoData);
      return keys.length > 0 ? { time: keys[0], ...state.cryptoData[keys[0]] } : null;
    },
  },
  actions: {
    async fetchCryptoData() {
      this.loading = true;
      this.error = null;

      try {
        const MY_API = import.meta.env.VITE_STOCK_API; // 환경 변수에서 API 키 가져오기

        // DIGITAL_CURRENCY 엔드포인트를 사용하여 암호화폐 데이터 요청
        const response = await axios.get("https://www.alphavantage.co/query", {
          params: {
            function: "DIGITAL_CURRENCY", // 무료 계정에서 사용할 수 있는 엔드포인트
            symbol: this.coinSymbol, // 상태에서 가져오기
            market: this.coinMarket, // 상태에서 가져오기
            apikey: MY_API, // API 키
          },
        });

        // 응답 데이터 처리
        if (response.data["Time Series (Digital Currency)"]) {
          this.cryptoData = response.data["Time Series (Digital Currency)"];
          console.log("Crypto Data Loaded:", this.cryptoData);
        } else {
          this.error = response.data["Note"] || "No data available";
          console.error("API Error:", response.data);
        }
      } catch (err) {
        this.error = "Failed to fetch cryptocurrency data";
        console.error("Fetch Error:", err);
      } finally {
        this.loading = false;
      }
    },
  },
});
