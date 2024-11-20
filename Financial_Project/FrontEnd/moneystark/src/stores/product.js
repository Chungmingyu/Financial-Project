import { ref, computed } from "vue";
import { defineStore } from "pinia";
import axios from "axios";

export const useProductStore = defineStore(
  "product",
  () => {
    const isComponentVisible = ref(false);
    const isDataSaved = ref(false);
    const depositProduct = ref([]);
    const savingProduct = ref([]);
    const BASE_URL = "http://127.0.0.1:8000/moneys";
    const savedata = () => {
      axios({
        url: `${BASE_URL}/save-products/`,
        method: "GET",
      })
        .then((response) => {})
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
          savingProduct.value = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    };

    return { isComponentVisible, isDataSaved, depositProduct, savingProduct, savedata, getDepositProduct, getSavingProduct };
  },
  { persist: true }
);
