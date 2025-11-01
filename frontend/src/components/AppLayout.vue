<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Sidebar -->
    <div class="fixed inset-y-0 left-0 z-50 w-64 bg-white shadow-lg transform transition-transform duration-300 ease-in-out" :class="sidebarOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'">
      <div class="flex flex-col h-full">
        <!-- Logo -->
        <div class="flex items-center justify-center h-16 px-4 border-b border-gray-200">
          <h1 class="text-xl font-bold text-primary-600">🧺 Laundry Tracker</h1>
        </div>
        
        <!-- Navigation -->
        <nav class="flex-1 px-4 py-6 space-y-2">
          <router-link
            v-for="item in navigationItems"
            :key="item.name"
            :to="item.path"
            class="flex items-center px-4 py-3 text-sm font-medium text-gray-600 rounded-lg hover:bg-gray-100 hover:text-gray-900 transition-colors"
            :class="{ 'bg-primary-50 text-primary-700 border-r-2 border-primary-500': $route.path === item.path }"
            @click="logAction('NAVIGATION', `Navigate to ${item.name}`)"
          >
            <span class="mr-3 text-lg">{{ item.icon }}</span>
            {{ item.name }}
          </router-link>
        </nav>
        
        <!-- User Info -->
        <div class="p-4 border-t border-gray-200">
          <div class="flex items-center space-x-3">
            <img
              :src="user?.foto_profil_url  || '/default-avatar.png'"
              :alt="user?.username"
              class="w-10 h-10 rounded-full object-cover"
            >
            <div class="flex-1 min-w-0">
              <p class="text-sm font-medium text-gray-900 truncate">
                {{ user?.username }}
              </p>
              <p class="text-xs text-gray-500 truncate">
                {{ user?.email }}
              </p>
            </div>
          </div>
          <button
            @click="handleLogout"
            class="w-full mt-3 px-3 py-2 text-sm text-red-600 hover:text-red-800 hover:bg-red-50 rounded-lg transition-colors"
          >
            Logout
          </button>
        </div>
      </div>
    </div>
    
    <!-- Main Content -->
    <div class="md:ml-64">
      <!-- Top Bar -->
      <div class="bg-white shadow-sm border-b border-gray-200 px-4 py-3 md:px-6">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-3">
            <button
              @click="toggleSidebar"
              class="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg md:hidden"
            >
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
              </svg>
            </button>
            <h2 class="text-lg font-semibold text-gray-900">{{ pageTitle }}</h2>
          </div>
          
          <div class="flex items-center space-x-3">
            <!-- Notifications or other actions can go here -->
          </div>
        </div>
      </div>
      
      <!-- Page Content -->
      <main class="p-4 md:p-6">
        <slot></slot>
      </main>
    </div>
    
    <!-- Mobile Backdrop -->
    <div
      v-if="sidebarOpen"
      class="fixed inset-0 bg-black bg-opacity-50 z-40 md:hidden"
      @click="closeSidebar"
    ></div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useLogging } from '@/composables/useLogging'
import { NAVIGATION_ITEMS } from '@/utils/constants'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const { logAction } = useLogging()

const sidebarOpen = ref(false)
const user = computed(() => authStore.user)
const navigationItems = NAVIGATION_ITEMS

const pageTitle = computed(() => {
  const currentRoute = navigationItems.find(item => item.path === route.path)
  return currentRoute?.name || 'Dashboard'
})

const toggleSidebar = () => {
  sidebarOpen.value = !sidebarOpen.value
}

const closeSidebar = () => {
  sidebarOpen.value = false
}

const handleLogout = async () => {
  try {
    await authStore.logout()
    logAction('AUTH', 'User logged out')
    router.push('/login')
  } catch (error) {
    console.error('Logout error:', error)
  }
}
</script>