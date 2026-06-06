﻿import axios from "axios";
import { message } from "ant-design-vue";

const request = axios.create({
  baseURL: "/api",
  timeout: 30000,
});

request.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = "Bearer " + token;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  },
);

request.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response) {
      const status = error.response.status;
      const data = error.response.data;

      if (status === 401) {
        localStorage.removeItem("token");
        localStorage.removeItem("user");
        window.location.href = "/login";
        message.error("登录已过期，请重新登录");
      } else if (data && data.detail) {
        message.error(data.detail);
      } else {
        message.error(error.message);
      }
    } else {
      message.error("网络错误，请稍后重试");
    }
    return Promise.reject(error);
  },
);

export default request;
