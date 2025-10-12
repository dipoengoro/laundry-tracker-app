// stores/auth.js
import { defineStore } from "pinia";
import apiClient from "../api";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    token: localStorage.getItem("token") || null,
    user: null,
    isLoading: false,
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    getUser: (state) => state.user,
  },

  actions: {
    async login(credentials) {
      this.isLoading = true;
      try {
        console.log("[Auth] 🔐 Attempting login...");

        const formData = new URLSearchParams();
        formData.append("username", credentials.email);
        formData.append("password", credentials.password);

        const response = await apiClient.post("/auth/login", formData, {
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
        });

        console.log("[Auth] ✅ Login success:", response.data);

        this.token = response.data.access_token;
        localStorage.setItem("token", this.token);
        apiClient.defaults.headers.common["Authorization"] = `Bearer ${this.token}`;

        await this.fetchUser();
      } catch (error) {
        console.error("[Auth] ❌ Login failed:", error);
        this.logout();
        throw error;
      } finally {
        this.isLoading = false;
      }
    },

    async logout() {
      console.log("[Auth] 🚪 Logging out...");
      this.token = null;
      this.user = null;
      localStorage.removeItem("token");
      delete apiClient.defaults.headers.common["Authorization"];
      console.log("[Auth] ✅ Logged out successfully.");
    },

    async fetchUser() {
      if (!this.token) {
        console.warn("[Auth] ⚠️ No token found, cannot fetch user.");
        return;
      }

      try {
        console.log("[Auth] 👤 Fetching user data...");
        const response = await apiClient.get("/auth/users/me");
        this.user = response.data;
        console.log("[Auth] ✅ User fetched:", this.user);
        return response.data;
      } catch (error) {
        console.error("[Auth] ❌ Failed to fetch user:", error);
        if (error.response?.status === 401) this.logout();
        throw error;
      }
    },

    initializeAuth() {
      const token = localStorage.getItem("token");
      if (token) {
        console.log("[Auth] ♻️ Initializing auth with saved token.");
        this.token = token;
        apiClient.defaults.headers.common["Authorization"] = `Bearer ${token}`;
        this.fetchUser().catch(() => {
          console.warn("[Auth] Token invalid, performing logout.");
          this.logout();
        });
      } else {
        console.log("[Auth] 🔄 No token found on startup.");
      }
    },
  },
});
