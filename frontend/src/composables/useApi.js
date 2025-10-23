import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

export function useApi() {
  const api = axios.create({
    baseURL: '/api',
    timeout: 10000,
  })

  // Request interceptor
  api.interceptors.request.use(
    (config) => {
      const authStore = useAuthStore()
      const token = authStore.token
      
      if (token) {
        config.headers.Authorization = `Bearer ${token}`
      }
      
      return config
    },
    (error) => {
      return Promise.reject(error)
    }
  )

  // Response interceptor
  api.interceptors.response.use(
    (response) => {
      return response
    },
    (error) => {
      if (error.response?.status === 401) {
        const authStore = useAuthStore()
        authStore.logout()
      }
      
      return Promise.reject(error)
    }
  )

  return { api }
}