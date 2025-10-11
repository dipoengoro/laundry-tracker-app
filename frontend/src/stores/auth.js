import { defineStore } from "pinia";
import apiClient from "../api";

export const useAuthStore = defineStore('auth', {
    state: () => ({
        token: localStorage.getItem('token') || null,
        user: null,
    }),
    actions: {
        async login(credentials) {
            try {
                const formData = new URLSearchParams();
                formData.append('username', credentials.email);
                formData.append('password', credentials.password);

                const response = await apiClient.post('/auth/login', formData, {
                    headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
                });

                this.token = response.data.access_token;
                localStorage.setItem('token', this.token);
            } catch (error) {
                this.token = null;
                localStorage.removeItem('token');
                console.error("Login Gagal: ", error);
                throw error;
            }
        },
        logout() {
            this.token = null;
            localStorage.removeItem('token');
            console.error("Login Gagal: ", error);

            throw error;
        }
    },
});