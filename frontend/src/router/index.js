// router/index.js
import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "../stores/auth";
import Login from "../views/Login.vue";
import Dashboard from "../views/Dashboard.vue";

const routes = [
  { path: "/", redirect: "/dashboard" },
  { path: "/login", name: "Login", component: Login },
  {
    path: "/dashboard",
    name: "Dashboard",
    component: Dashboard,
    meta: { requiresAuth: true },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// ✅ Global navigation guard
router.beforeEach((to, from, next) => {
  const auth = useAuthStore();

  console.log(`[Router] 🧭 Navigating to: ${to.fullPath}`);

  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    console.warn("[Router] ❌ Not authenticated, redirecting to /login");
    return next("/login");
  }

  if (to.path === "/login" && auth.isAuthenticated) {
    console.log("[Router] ✅ Already logged in, redirecting to dashboard");
    return next("/dashboard");
  }

  next();
});

export default router;
