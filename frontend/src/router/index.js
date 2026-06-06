﻿import { createRouter, createWebHistory } from "vue-router";
import { useUserStore } from "../stores/user";

const routes = [
  {
    path: "/login",
    name: "Login",
    component: () => import("../views/Login.vue"),
    meta: { requiresAuth: false },
  },
  {
    path: "/register",
    name: "Register",
    component: () => import("../views/Register.vue"),
    meta: { requiresAuth: false },
  },
  {
    path: "/",
    component: () => import("../layouts/MainLayout.vue"),
    meta: { requiresAuth: true, role: "member" },
    children: [
      {
        path: "",
        redirect: "/recommend",
      },
      {
        path: "recommend",
        name: "Recommend",
        component: () => import("../views/Recommend.vue"),
      },
      {
        path: "matches",
        name: "Matches",
        component: () => import("../views/Matches.vue"),
      },
      {
        path: "activities",
        name: "Activities",
        component: () => import("../views/Activities.vue"),
      },
      {
        path: "profile",
        name: "Profile",
        component: () => import("../views/Profile.vue"),
      },
      {
        path: "preference",
        name: "Preference",
        component: () => import("../views/Preference.vue"),
      },
    ],
  },
  {
    path: "/matchmaker",
    component: () => import("../layouts/MatchmakerLayout.vue"),
    meta: { requiresAuth: true, role: "matchmaker" },
    children: [
      {
        path: "",
        redirect: "/matchmaker/dashboard",
      },
      {
        path: "dashboard",
        name: "Dashboard",
        component: () => import("../views/matchmaker/Dashboard.vue"),
      },
      {
        path: "profile-review",
        name: "ProfileReview",
        component: () => import("../views/matchmaker/ProfileReview.vue"),
      },
      {
        path: "activities",
        name: "MatchmakerActivities",
        component: () => import("../views/matchmaker/Activities.vue"),
      },
      {
        path: "manual-match",
        name: "ManualMatch",
        component: () => import("../views/matchmaker/ManualMatch.vue"),
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const userStore = useUserStore();
  const token = userStore.token;

  if (to.meta.requiresAuth && !token) {
    next("/login");
  } else if (to.meta.role && userStore.user?.role !== to.meta.role) {
    if (userStore.user?.role === "matchmaker") {
      next("/matchmaker/dashboard");
    } else {
      next("/");
    }
  } else if ((to.path === "/login" || to.path === "/register") && token) {
    if (userStore.user?.role === "matchmaker") {
      next("/matchmaker/dashboard");
    } else {
      next("/");
    }
  } else {
    next();
  }
});

export default router;
