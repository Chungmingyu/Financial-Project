import { ref, computed } from "vue";
import { defineStore } from "pinia";
import axios from "axios";

export const useUserStore = defineStore(
  "user",
  () => {
    const token = ref(null);
    const BASE_URL = "http://127.0.0.1:8000/accounts";
    const logIn = (payload) => {
      axios({
        url: `${BASE_URL}/login/`,
        method: "POST",
        data: {
          username: payload.username,
          password: payload.password,
        },
      })
        .then((response) => {
          console.log(response);
          token.value = response.data.key;
        })
        .catch((error) => {
          console.log(error);
        });
    };

    const signUp = (payload) => {
      axios({
        url: `${BASE_URL}/signup/`,
        method: "POST",
        data: {
          username: payload.username,
          password1: payload.password1,
          password2: payload.password2,
        },
      })
        .then((response) => {
          console.log(response);
        })
        .catch((error) => {
          console.log(error);
        });
    };

    return { token, signUp, logIn };
  },
  { persist: true }
);
