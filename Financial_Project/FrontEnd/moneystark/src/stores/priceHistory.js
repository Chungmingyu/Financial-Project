// stores/priceHistory.js
import { defineStore } from "pinia";

export const usePriceHistoryStore = defineStore("priceHistory", {
  state: () => ({
    priceData: {},
  }),
  actions: {
    updatePrice(market, price) {
      if (!this.priceData[market]) {
        this.priceData[market] = {
          prices: [],
          times: [],
        };
      }

      const data = this.priceData[market];
      const now = new Date().toLocaleTimeString();

      // 새 배열 생성하여 할당
      const newPrices = [...data.prices, price];
      const newTimes = [...data.times, now];

      // 최대 10개 데이터만 유지
      if (newPrices.length > 10) {
        newPrices.shift();
        newTimes.shift();
      }

      // 새로운 객체로 할당
      this.priceData[market] = {
        prices: newPrices,
        times: newTimes,
      };
    },
  },
});
