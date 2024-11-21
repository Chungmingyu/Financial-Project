// src/stores/stockStore.js
import { defineStore } from "pinia";
import axios from "axios";

export const useStockStore = defineStore("stock", {
  state: () => ({
    stockData: null,
    loading: false,
    error: null,
  }),
  getters: {
    stockDataArray() {
      if (!this.stockData) {
        return [];
      }

      return Object.entries(this.stockData).map(([date, data]) => ({
        date,
        ...data,
      }));
    },
  },
  actions: {
    async fetchStockData(symbol) {
      this.loading = true;
      this.error = null;
      console.log(symbol);
      try {
        const MY_API = import.meta.env.VITE_STOCK_API_1;
        const response = await axios.get("https://www.alphavantage.co/query", {
          params: {
            function: "TIME_SERIES_INTRADAY",
            symbol: symbol,
            interval: "5min", // 5분 간격으로 데이터 요청
            apikey: `${MY_API}`,
            datatype: "json",
          },
        });

        this.stockData = response.data["Time Series (5min)"];
        console.log(this.stockData);
        console.log(response);
      } catch (err) {
        this.error = "Failed to fetch stock data";
        console.error(err);
      } finally {
        this.loading = false;
      }
    },
  },
});
