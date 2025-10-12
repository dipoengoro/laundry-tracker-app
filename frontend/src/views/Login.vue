<template>
  <AuthLayout title="Selamat Datang Kembali">
    <div v-if="errorMessage" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded-lg relative mb-4" role="alert">
      <span class="block sm:inline">{{ errorMessage }}</span>
    </div>

    <form class="space-y-6" @submit.prevent="handleLogin">
      <div>
        <label for="email" class="block text-sm font-medium text-gray-700">Alamat Email</label>
        <div class="mt-1">
          <input id="email" v-model="email" name="email" type="email" autocomplete="email" required
                 :disabled="isLoading"
                 class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-50"
                 placeholder="anda@email.com">
        </div>
      </div>

      <div>
        <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
        <div class="mt-1">
          <input id="password" v-model="password" name="password" type="password" autocomplete="current-password" required
                 :disabled="isLoading"
                 class="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-50"
                 placeholder="Password">
        </div>
      </div>

      <div>
        <button type="submit"
                :disabled="isLoading || !email || !password"
                class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:bg-blue-300 disabled:cursor-not-allowed">
          <span v-if="isLoading" class="flex items-center">
            <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Memproses...
          </span>
          <span v-else>Login</span>
        </button>
      </div>
    </form>
    
    <p class="mt-6 text-center text-sm text-gray-600">
      Belum punya akun?
      {{ ' ' }}
      <router-link to="/register" class="font-medium text-blue-600 hover:text-blue-500">
        Daftar di sini
      </router-link>
    </p>
  </AuthLayout>
</template>

<script setup>
import { ref } from "vue";
import { useAuthStore } from "../stores/auth";
import { useRouter } from "vue-router";
import AuthLayout from '../components/AuthLayout.vue'; // Pastikan komponen ini ada

const email = ref("");
const password = ref("");
const errorMessage = ref("");
const isLoading = ref(false);

const auth = useAuthStore();
const router = useRouter();

const handleLogin = async () => {
  isLoading.value = true;
  errorMessage.value = '';
  try {
    await auth.login({ email: email.value, password: password.value });
    console.log("[Login] ✅ Login successful, redirecting to dashboard...");
    router.push("/dashboard"); 
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || "Email atau password salah.";
    console.error("[Login] ❌ Login failed:", error);
  } finally {
    isLoading.value = false;
  }
};
</script>