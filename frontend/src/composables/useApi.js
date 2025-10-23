import axios from 'axios'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export function useApi() {
  const api = axios.create({
    baseURL: API_BASE_URL,
    timeout: 10000,
    headers: {
      'Content-Type': 'application/json'
    }
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
      const authStore = useAuthStore()
      const router = useRouter()
      
      if (error.response?.status === 401) {
        authStore.logout()
        router.push('/login')
      }
      
      return Promise.reject(error)
    }
  )

  return { api }
}