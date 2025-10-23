<template>
  <div class="min-h-screen bg-gradient-to-br from-primary-50 to-blue-100 flex items-center justify-center px-4">
    <div class="max-w-md w-full">
      <!-- Logo -->
      <div class="text-center mb-8">
        <h1 class="text-3xl font-bold text-primary-600 mb-2">🧺 Laundry Tracker</h1>
        <p class="text-gray-600">Kelola laundry Anda dengan mudah</p>
      </div>
      
      <!-- Form Container -->
      <div class="bg-white rounded-lg shadow-xl p-8">
        <!-- Toggle Buttons -->
        <div class="flex rounded-lg bg-gray-100 p-1 mb-6">
          <button
            @click="isLogin = true"
            :class="[
              'flex-1 py-2 px-4 rounded-md text-sm font-medium transition-colors',
              isLogin ? 'bg-white text-gray-900 shadow-sm' : 'text-gray-500 hover:text-gray-700'
            ]"
          >
            Masuk
          </button>
          <button
            @click="isLogin = false"
            :class="[
              'flex-1 py-2 px-4 rounded-md text-sm font-medium transition-colors',
              !isLogin ? 'bg-white text-gray-900 shadow-sm' : 'text-gray-500 hover:text-gray-700'
            ]"
          >
            Daftar
          </button>
        </div>
        
        <!-- Login Form -->
        <form v-if="isLogin" @submit.prevent="handleLogin" class="space-y-4">
          <div>
            <label class="form-label">Email</label>
            <input
              v-model="loginForm.email"
              type="email"
              class="form-input w-full"
              placeholder="Masukkan email Anda"
              required
            >
          </div>
          
          <div>
            <label class="form-label">Password</label>
            <div class="relative">
              <input
                v-model="loginForm.password"
                :type="showPassword ? 'text' : 'password'"
                class="form-input w-full pr-10"
                placeholder="Masukkan password Anda"
                required
              >
              <button
                type="button"
                @click="showPassword = !showPassword"
                class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
              >
                <svg v-if="!showPassword" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
                </svg>
                <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L8.464 8.464m1.414 1.414l-1.414 1.414M14.12 14.12l1.414 1.414m-1.414-1.414l1.414-1.414m-1.414 1.414l-1.414 1.414"></path>
                </svg>
              </button>
            </div>
          </div>
          
          <button
            type="submit"
            :disabled="loading"
            class="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <LoadingSpinner v-if="loading" size="small" />
            <span v-else>Masuk</span>
          </button>
          
          <div class="text-center">
            <button
              type="button"
              @click="showForgotPassword = true"
              class="text-sm text-primary-600 hover:text-primary-700"
            >
              Lupa password?
            </button>
          </div>
        </form>
        
        <!-- Register Form -->
        <form v-else @submit.prevent="handleRegister" class="space-y-4">
          <div>
            <label class="form-label">Username</label>
            <input
              v-model="registerForm.username"
              type="text"
              class="form-input w-full"
              placeholder="Masukkan username Anda"
              required
            >
          </div>
          
          <div>
            <label class="form-label">Email</label>
            <input
              v-model="registerForm.email"
              type="email"
              class="form-input w-full"
              placeholder="Masukkan email Anda"
              required
            >
          </div>
          
          <div>
            <label class="form-label">Password</label>
            <input
              v-model="registerForm.password"
              type="password"
              class="form-input w-full"
              placeholder="Masukkan password Anda"
              required
              minlength="6"
            >
          </div>
          
          <div>
            <label class="form-label">Konfirmasi Password</label>
            <input
              v-model="registerForm.confirmPassword"
              type="password"
              class="form-input w-full"
              placeholder="Konfirmasi password Anda"
              required
            >
          </div>
          
          <button
            type="submit"
            :disabled="loading || registerForm.password !== registerForm.confirmPassword"
            class="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <LoadingSpinner v-if="loading" size="small" />
            <span v-else>Daftar</span>
          </button>
          
          <p v-if="registerForm.password && registerForm.confirmPassword && registerForm.password !== registerForm.confirmPassword" 
             class="text-red-500 text-sm">
            Password tidak cocok
          </p>
        </form>
      </div>
      
      <!-- Forgot Password Modal -->
      <div v-if="showForgotPassword" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div class="bg-white rounded-lg shadow-xl max-w-md w-full mx-4 p-6">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-lg font-semibold">Reset Password</h3>
            <button
              @click="showForgotPassword = false"
              class="text-gray-400 hover:text-gray-600"
            >
              ×
            </button>
          </div>
          
          <form @submit.prevent="handleForgotPassword" class="space-y-4">
            <div>
              <label class="form-label">Email</label>
              <input
                v-model="forgotPasswordEmail"
                type="email"
                class="form-input w-full"
                placeholder="Masukkan email Anda"
                required
              >
            </div>
            
            <button
              type="submit"
              :disabled="loading"
              class="w-full btn-primary disabled:opacity-50"
            >
              <LoadingSpinner v-if="loading" size="small" />
              <span v-else>Kirim Link Reset</span>
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useToast } from '@/composables/useToast'
import { useLogging } from '@/composables/useLogging'
import LoadingSpinner from '@/components/LoadingSpinner.vue'

const router = useRouter()
const authStore = useAuthStore()
const { showToast } = useToast()
const { logAction } = useLogging()

const isLogin = ref(true)
const loading = ref(false)
const showPassword = ref(false)
const showForgotPassword = ref(false)

const loginForm = ref({
  email: '',
  password: ''
})

const registerForm = ref({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const forgotPasswordEmail = ref('')

const handleLogin = async () => {
  loading.value = true
  try {
    await authStore.login(loginForm.value)
    logAction('AUTH', 'User logged in successfully')
    showToast('success', 'Login berhasil!')
    router.push('/dashboard')
  } catch (error) {
    logAction('AUTH', 'Login failed', { error: error.message })
    showToast('error', error.response?.data?.detail || 'Login gagal')
  } finally {
    loading.value = false
  }
}

const handleRegister = async () => {
  if (registerForm.value.password !== registerForm.value.confirmPassword) {
    showToast('error', 'Password tidak cocok')
    return
  }
  
  loading.value = true
  try {
    await authStore.register({
      username: registerForm.value.username,
      email: registerForm.value.email,
      password: registerForm.value.password
    })
    logAction('AUTH', 'User registered successfully')
    showToast('success', 'Registrasi berhasil! Silakan login.')
    isLogin.value = true
    
    // Reset form
    registerForm.value = {
      username: '',
      email: '',
      password: '',
      confirmPassword: ''
    }
  } catch (error) {
    logAction('AUTH', 'Registration failed', { error: error.message })
    showToast('error', error.response?.data?.detail || 'Registrasi gagal')
  } finally {
    loading.value = false
  }
}

const handleForgotPassword = async () => {
  loading.value = true
  try {
    await authStore.forgotPassword(forgotPasswordEmail.value)
    logAction('AUTH', 'Password reset requested')
    showToast('success', 'Link reset password telah dikirim ke email Anda')
    showForgotPassword.value = false
    forgotPasswordEmail.value = ''
  } catch (error) {
    logAction('AUTH', 'Password reset failed', { error: error.message })
    showToast('error', 'Gagal mengirim link reset password')
  } finally {
    loading.value = false
  }
}
</script>