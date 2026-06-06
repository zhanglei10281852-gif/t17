﻿import { defineStore } from "pinia";
import request from "../utils/request";
import { ref, computed } from "vue";

export const useUserStore = defineStore("user", () => {
  const token = ref(localStorage.getItem("token") || "");
  const user = ref(JSON.parse(localStorage.getItem("user") || "null"));

  const isLoggedIn = computed(() => !!token.value);

  function setToken(newToken) {
    token.value = newToken;
    localStorage.setItem("token", newToken);
  }

  function setUser(newUser) {
    user.value = newUser;
    localStorage.setItem("user", JSON.stringify(newUser));
  }

  async function login(phone, password) {
    const res = await request.post("/auth/login", {
      phone,
      password,
    });
    setToken(res.data.access_token);
    const userRes = await request.get("/auth/me");
    setUser(userRes.data);
    return userRes.data;
  }

  async function register(data) {
    const res = await request.post("/auth/register", data);
    return res.data;
  }

  function logout() {
    token.value = "";
    user.value = null;
    localStorage.removeItem("token");
    localStorage.removeItem("user");
  }

  async function fetchUser() {
    const res = await request.get("/auth/me");
    setUser(res.data);
    return res.data;
  }

  return {
    token,
    user,
    isLoggedIn,
    login,
    register,
    logout,
    fetchUser,
  };
});
