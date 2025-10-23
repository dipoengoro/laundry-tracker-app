import { defineStore } from 'pinia'

export const useUIStore = defineStore('ui', {
  state: () => ({
    isLoading: false,
    sidebarOpen: false,
    toasts: []
  }),

  actions: {
    setLoading(loading) {
      this.isLoading = loading
    },

    toggleSidebar() {
      this.sidebarOpen = !this.sidebarOpen
    },

    closeSidebar() {
      this.sidebarOpen = false
    },

    addToast(toast) {
      this.toasts.push(toast)
    },

    removeToast(id) {
      this.toasts = this.toasts.filter(toast => toast.id !== id)
    }
  }
})