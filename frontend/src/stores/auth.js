import { defineStore } from 'pinia'
import { useApi } from '@/composables/useApi'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token'),
    isAuthenticated: false
  }),

  actions: {
    async login(credentials) {
      const { api } = useApi()
      
      try {
        // const formData = new FormData()
        // formData.append('username', credentials.email)
        // formData.append('password', credentials.password)

        const params = new URLSearchParams()
        params.append('username', credentials.email)
        params.append('password', credentials.password)

        const response = await api.post('/auth/login', params)
        
        const { access_token, token_type } = response.data
        
        this.token = access_token
        this.isAuthenticated = true
        
        localStorage.setItem('token', access_token)
        
        // Fetch user data
        await this.fetchUser()
        
        return response.data
      } catch (error) {
        this.token = null
        this.user = null
        this.isAuthenticated = false
        localStorage.removeItem('token')
        throw error
      }
    },

    async register(userData) {
      const { api } = useApi()
      
      const response = await api.post('/auth/register', userData)
      return response.data
    },

    async fetchUser() {
      const { api } = useApi()
      
      try {
        const response = await api.get('/auth/users/me')
        this.user = response.data
        this.isAuthenticated = true
        return response.data
      } catch (error) {
        this.logout()
        throw error
      }
    },

    async updateProfile(data) {
      const { api } = useApi()
      
      const response = await api.put('/auth/me', data)
      this.user = response.data
      return response.data
    },

    async updateProfilePicture(file) {
      const { api } = useApi()
      
      const formData = new FormData()
      formData.append('file', file)
      
      const response = await api.put('/auth/me/picture', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      
      this.user = response.data
      return response.data
    },

    async forgotPassword(email) {
      const { api } = useApi()
      
      const response = await api.post('/auth/forgot-password', { email })
      return response.data
    },

    async resetPassword(token, newPassword) {
      const { api } = useApi()
      
      const response = await api.post('/auth/reset-password', {
        token,
        new_password: newPassword
      })
      return response.data
    },

    async logout() {
      const { api } = useApi()
      
      try {
        await api.post('/auth/logout')
      } catch (error) {
        console.error('Logout API call failed:', error)
      } finally {
        this.user = null
        this.token = null
        this.isAuthenticated = false
        localStorage.removeItem('token')
      }
    },

    async initializeAuth() {
      if (this.token) {
        try {
          await this.fetchUser()
        } catch (error) {
          this.logout()
        }
      }
    }
  }
})