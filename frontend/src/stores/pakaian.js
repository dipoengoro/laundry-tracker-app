import { defineStore } from "pinia";
import apiClient from "../api";
import { API_BASE_URL } from "../utils/constants";

export const usePakaianStore = defineStore('pakaian', {
  state: () => ({
    items: [],
    isLoading: false,
    error: null,
    totalItems: 0,
    currentPage: 1,
    itemsPerPage: 12,
    searchQuery: '',
    selectedCategory: '',
    logs: []
  }),

  getters: {
    filteredItems: (state) => {
      let filtered = state.items;
      
      if (state.searchQuery) {
        filtered = filtered.filter(item => 
          item.nama_pakaian.toLowerCase().includes(state.searchQuery.toLowerCase()) ||
          (item.kategori && item.kategori.toLowerCase().includes(state.searchQuery.toLowerCase())) ||
          (item.jenis_pakaian && item.jenis_pakaian.toLowerCase().includes(state.searchQuery.toLowerCase()))
        );
      }
      
      if (state.selectedCategory) {
        filtered = filtered.filter(item => item.kategori === state.selectedCategory);
      }
      
      return filtered;
    },
    
    paginatedItems: (state) => {
      const filtered = state.filteredItems;
      const start = (state.currentPage - 1) * state.itemsPerPage;
      const end = start + state.itemsPerPage;
      return filtered.slice(start, end);
    },
    
    totalPages: (state) => {
      return Math.ceil(state.filteredItems.length / state.itemsPerPage);
    },

    categoryStats: (state) => {
      const stats = {};
      state.items.forEach(item => {
        const category = item.kategori || 'Tidak Berkategori';
        stats[category] = (stats[category] || 0) + 1;
      });
      return stats;
    }
  },

  actions: {
    normalizeFotoUrl(item) {
      if (!item) return item;
      const foto = item.foto_url ?? item.foto ?? null;
      if (!foto) return { ...item, foto_url: foto };

      const isAbsolute = /^https?:\/\//i.test(foto) || /^\/\//.test(foto);
      if (isAbsolute) {
        return { ...item, foto_url: foto };
      }

      const path = foto.startsWith('/') ? foto.slice(1) : foto;
      return { ...item, foto_url: `${API_BASE_URL}/${path}` };
    },

    normalizeItemsArray(items) {
      return items.map(i => this.normalizeFotoUrl(i));
    },

    async fetchPakaian() {
      console.log("[PakaianStore] 👕 Fetching pakaian...");
      this.isLoading = true;
      this.error = null;
      
      try {
        const response = await apiClient.get('/pakaian/');
        this.items = this.normalizeItemsArray(response.data);
        this.totalItems = response.data.length;
        console.log("[PakaianStore] ✅ Pakaian fetched:", this.items.length, "items");
        
        this.addLog({
          action: 'FETCH',
          details: `Loaded ${this.items.length} clothing items`,
          status: 'SUCCESS'
        });

        this.addLog({
          action: 'FETCH',
          details: `${this.items}`,
          status: 'SUCCESS'
        })
        
      } catch (error) {
        console.error('[PakaianStore] ❌ Failed to fetch pakaian:', error);
        this.error = 'Gagal mengambil data pakaian';
        
        this.addLog({
          action: 'FETCH',
          details: 'Failed to load clothing items',
          status: 'ERROR'
        });
        
        throw error;
      } finally {
        this.isLoading = false;
      }
    },

    async addPakaian(pakaianData) {
      this.isLoading = true;
      this.error = null;
      
      try {
        console.log("[PakaianStore] ➕ Adding pakaian:", pakaianData);
        const response = await apiClient.post('/pakaian/', pakaianData);
        
        // Add to local state
        const normalized = this.normalizeFotoUrl(response.data);
        this.items.push(normalized);
        this.totalItems++;
        
        console.log("[PakaianStore] ✅ Pakaian added successfully:", response.data);
        
        this.addLog({
          action: 'CREATE',
          item_name: pakaianData.nama_pakaian,
          details: `Added new clothing item: ${pakaianData.nama_pakaian}`,
          status: 'SUCCESS'
        });
        
        return normalized;
      } catch (error) {
        console.error('[PakaianStore] ❌ Failed to add pakaian:', error);
        this.error = 'Gagal menambah data pakaian';
        
        this.addLog({
          action: 'CREATE',
          item_name: pakaianData.nama_pakaian,
          details: 'Failed to add clothing item',
          status: 'ERROR'
        });
        
        throw error;
      } finally {
        this.isLoading = false;
      }
    },

    async updatePakaian(id, pakaianData) {
      this.isLoading = true;
      this.error = null;
      
      try {
        console.log("[PakaianStore] 📝 Updating pakaian:", id, pakaianData);
        const response = await apiClient.put(`/pakaian/${id}`, pakaianData);
        
        // Update local state
        const normalized = this.normalizeFotoUrl(response.data);
        const index = this.items.findIndex(item => item.id === id);
        if (index !== -1) {
          this.items[index] = normalized;
        }
        
        console.log("[PakaianStore] ✅ Pakaian updated successfully:", response.data);
        
        this.addLog({
          action: 'UPDATE',
          item_name: pakaianData.nama_pakaian,
          details: `Updated clothing item: ${pakaianData.nama_pakaian}`,
          status: 'SUCCESS'
        });
        
        return normalized;
      } catch (error) {
        console.error('[PakaianStore] ❌ Failed to update pakaian:', error);
        this.error = 'Gagal memperbarui data pakaian';
        
        this.addLog({
          action: 'UPDATE',
          item_name: pakaianData.nama_pakaian,
          details: 'Failed to update clothing item',
          status: 'ERROR'
        });
        
        throw error;
      } finally {
        this.isLoading = false;
      }
    },

    async deletePakaian(id) {
      this.isLoading = true;
      this.error = null;
      
      try {
        const item = this.items.find(p => p.id === id);
        console.log("[PakaianStore] 🗑️ Deleting pakaian:", id);
        
        await apiClient.delete(`/pakaian/${id}`);
        
        // Remove from local state
        this.items = this.items.filter(item => item.id !== id);
        this.totalItems--;
        
        console.log("[PakaianStore] ✅ Pakaian deleted successfully");
        
        this.addLog({
          action: 'DELETE',
          item_name: item?.nama_pakaian || `ID: ${id}`,
          details: `Deleted clothing item: ${item?.nama_pakaian || id}`,
          status: 'SUCCESS'
        });
        
      } catch (error) {
        console.error('[PakaianStore] ❌ Failed to delete pakaian:', error);
        this.error = 'Gagal menghapus data pakaian';
        
        this.addLog({
          action: 'DELETE',
          item_name: `ID: ${id}`,
          details: 'Failed to delete clothing item',
          status: 'ERROR'
        });
        
        throw error;
      } finally {
        this.isLoading = false;
      }
    },

    async uploadImage(id, file) {
      try {
        console.log("[PakaianStore] 📷 Uploading image for pakaian:", id);
        
        const formData = new FormData();
        formData.append('file', file);
        
        const response = await apiClient.post(`/pakaian/${id}/image`, formData, {
          headers: {}
        });
        
        // Update local state
        const normalized = this.normalizeFotoUrl(response.data);
        const index = this.items.findIndex(item => item.id === id);
        if (index !== -1) {
          this.items[index] = normalized;
        }
        
        console.log("[PakaianStore] ✅ Image uploaded successfully");
        
        this.addLog({
          action: 'UPLOAD_IMAGE',
          item_name: response.data.nama_pakaian,
          details: `Uploaded image for ${response.data.nama_pakaian}`,
          status: 'SUCCESS'
        });
        
        return normalized;
      } catch (error) {
        console.error('[PakaianStore] ❌ Failed to upload image:', error);
        
        this.addLog({
          action: 'UPLOAD_IMAGE',
          item_name: `ID: ${id}`,
          details: 'Failed to upload image',
          status: 'ERROR'
        });
        
        throw error;
      }
    },

    // Bulk operations
    async bulkDelete(ids) {
      this.isLoading = true;
      const results = [];
      
      for (const id of ids) {
        try {
          await this.deletePakaian(id);
          results.push({ id, success: true });
        } catch (error) {
          results.push({ id, success: false, error: error.message });
        }
      }
      
      this.isLoading = false;
      return results;
    },

    // Search and filter
    setSearchQuery(query) {
      this.searchQuery = query;
      this.currentPage = 1;
    },

    setSelectedCategory(category) {
      this.selectedCategory = category;
      this.currentPage = 1;
    },

    setCurrentPage(page) {
      this.currentPage = page;
    },

    // Logging
    addLog(logData) {
      const log = {
        id: Date.now(),
        timestamp: new Date().toISOString(),
        user: 'Current User', // This should come from auth store
        ...logData
      };
      
      this.logs.unshift(log);
      
      // Keep only last 100 logs
      if (this.logs.length > 100) {
        this.logs = this.logs.slice(0, 100);
      }
    },

    exportData() {
      const dataToExport = {
        items: this.items,
        exported_at: new Date().toISOString(),
        total_items: this.items.length,
        categories: this.categoryStats
      };
      
      const blob = new Blob([JSON.stringify(dataToExport, null, 2)], {
        type: 'application/json'
      });
      
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `pakaian-data-${new Date().toISOString().split('T')}.json`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      
      this.addLog({
        action: 'EXPORT',
        details: `Exported ${this.items.length} clothing items`,
        status: 'SUCCESS'
      });
    }
  }
});
