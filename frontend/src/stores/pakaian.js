import { defineStore } from "pinia";
import apiClient from "../api";

export const usePakaianStore = defineStore('pakaian', {
    state: () => ({
        items: [],
        isLoading: false,
    }),
    actions: {
        async fetchPakaian() {
            console.log("[PakaianStore] 👕 Fetching pakaian...");
            this.isLoading = true;

            try {
                const response = await apiClient.get('/pakaian/');
                this.items = response.data;
                console.log("[PakaianStore] ✅ Pakaian fetched:", this.items);
            } catch (error) {
                console.error('[PakaianStore] ❌ Failed to fetch pakaian:', error);
                alert('Gagal mengambil data pakaian.');
            } finally {
                this.isLoading = false;
            }
        },
        async addPakaian(pakaianData) {
            this.isLoading = true;
            try {
                await apiClient.post('/pakaian/', pakaianData);
                console.log("[PakaianStore] ✅ Pakaian added successfully.");

                await this.fetchPakaian();
            } catch (error) {
                console.error('[PakaianStore] ❌ Failed to add pakaian:', error);
                alert('Gagal menambah data pakaian.');
            } finally {
                this.isLoading = false;
            }
        },
    },
});