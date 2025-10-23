import { defineStore } from 'pinia'
import { useApi } from '@/composables/useApi'

export const useLaundryStore = defineStore('laundry', {
  state: () => ({
    sessions: [],
    loading: false
  }),

  actions: {
    async fetchSessions() {
      const { api } = useApi()
      this.loading = true
      
      try {
        const response = await api.get('/laundry/')
        this.sessions = response.data
        return response.data
      } catch (error) {
        console.error('Failed to fetch laundry sessions:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    async createSession(sessionData) {
      const { api } = useApi()
      
      try {
        const response = await api.post('/laundry/', sessionData)
        this.sessions.unshift(response.data)
        return response.data
      } catch (error) {
        console.error('Failed to create laundry session:', error)
        throw error
      }
    },

    async updateSessionStatus(sessionId, status) {
      const { api } = useApi()
      
      try {
        const response = await api.put(`/laundry/${sessionId}/status`, { status })
        const index = this.sessions.findIndex(s => s.id === sessionId)
        if (index !== -1) {
          this.sessions[index] = response.data
        }
        return response.data
      } catch (error) {
        console.error('Failed to update session status:', error)
        throw error
      }
    },

    getSessionById(id) {
      return this.sessions.find(s => s.id === id)
    }
  }
})