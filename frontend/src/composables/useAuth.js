import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

export function useAuth() {
  const authStore = useAuthStore()

  const user = computed(() => authStore.user)
  const isAuthenticated = computed(() => authStore.isAuthenticated)
  const token = computed(() => authStore.token)

  const login = async (credentials) => {
    return await authStore.login(credentials)
  }

  const logout = async () => {
    return await authStore.logout()
  }

  const register = async (userData) => {
    return await authStore.register(userData)
  }

  return {
    user,
    isAuthenticated,
    token,
    login,
    logout,
    register
  }
}