import { ref, computed } from "vue";
import { defineStore } from "pinia";
import axios from "axios";

export const useProductStore = defineStore(
  "product",
  () => {
    const depositProduct = ref([]);
    const savingProduct = ref([]);
    const BASE_URL = "http://127.0.0.1:8000/moneys";
    const savedata = () => {
      axios({
        url: `${BASE_URL}/save-products/`,
        method: "GET",
      })
        .then((response) => {
          console.log(response);
        })
        .catch((error) => {
          console.log(error);
        });
    };

    const getDepositProduct = () => {
      axios({
        url: `${BASE_URL}/deposit-products/`,
        method: "GET",
      })
        .then((response) => {
          console.log(response.data);
          depositProduct.value = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    };

    const getSavingProduct = () => {
      axios({
        url: `${BASE_URL}/saving-products/`,
        method: "GET",
      })
        .then((response) => {
          console.log(response);
          savingProduct.value = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    };

    return { depositProduct, savingProduct, savedata, getDepositProduct, getSavingProduct };
  },
  { persist: true }
);
