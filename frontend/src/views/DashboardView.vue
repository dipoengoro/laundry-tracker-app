<template>
  <AppLayout>
    <div class="space-y-6">
      <!-- Welcome Section -->
      <div class="bg-gradient-to-r from-primary-500 to-blue-600 rounded-lg p-6 text-white">
        <h1 class="text-2xl font-bold mb-2">
          Selamat datang, {{ user?.username }}! 👋
        </h1>
        <p class="text-primary-100">
          Kelola pakaian dan sesi laundry Anda dengan mudah
        </p>
      </div>
      
      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div class="bg-white rounded-lg shadow-md p-6">
          <div class="flex items-center">
            <div class="p-3 rounded-full bg-blue-100 text-blue-600">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"></path>
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">Total Pakaian</p>
              <p class="text-2xl font-semibold text-gray-900">{{ stats.totalClothes }}</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white rounded-lg shadow-md p-6">
          <div class="flex items-center">
            <div class="p-3 rounded-full bg-green-100 text-green-600">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">Sesi Aktif</p>
              <p class="text-2xl font-semibold text-gray-900">{{ stats.activeSessions }}</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white rounded-lg shadow-md p-6">
          <div class="flex items-center">
            <div class="p-3 rounded-full bg-yellow-100 text-yellow-600">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">Sedang Proses</p>
              <p class="text-2xl font-semibold text-gray-900">{{ stats.inProgress }}</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white rounded-lg shadow-md p-6">
          <div class="flex items-center">
            <div class="p-3 rounded-full bg-purple-100 text-purple-600">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">Selesai</p>
              <p class="text-2xl font-semibold text-gray-900">{{ stats.completed }}</p>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Quick Actions -->
      <div class="bg-white rounded-lg shadow-md p-6">
        <h2 class="text-lg font-semibold text-gray-900 mb-4">Aksi Cepat</h2>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <router-link
            to="/clothing"
            class="flex flex-col items-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
            @click="logAction('NAVIGATION', 'Quick action: Add clothing')"
          >
            <div class="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center mb-2">
              <span class="text-2xl">👕</span>
            </div>
            <span class="text-sm font-medium text-gray-700">Tambah Pakaian</span>
          </router-link>
          
          <router-link
            to="/laundry"
            class="flex flex-col items-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
            @click="logAction('NAVIGATION', 'Quick action: New laundry session')"
          >
            <div class="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mb-2">
              <span class="text-2xl">🧺</span>
            </div>
            <span class="text-sm font-medium text-gray-700">Sesi Laundry</span>
          </router-link>
          
          <router-link
            to="/profile"
            class="flex flex-col items-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
            @click="logAction('NAVIGATION', 'Quick action: Profile')"
          >
            <div class="w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center mb-2">
              <span class="text-2xl">👤</span>
            </div>
            <span class="text-sm font-medium text-gray-700">Profil</span>
          </router-link>
          
          <button
            @click="refreshData"
            class="flex flex-col items-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors"
          >
            <div class="w-12 h-12 bg-orange-100 rounded-full flex items-center justify-center mb-2">
              <span class="text-2xl">🔄</span>
            </div>
            <span class="text-sm font-medium text-gray-700">Refresh Data</span>
          </button>
        </div>
      </div>
      
      <!-- Recent Activity -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Recent Laundry Sessions -->
        <div class="bg-white rounded-lg shadow-md p-6">
          <div class="flex justify-between items-center mb-4">
            <h2 class="text-lg font-semibold text-gray-900">Sesi Terbaru</h2>
            <router-link to="/laundry" class="text-primary-600 hover:text-primary-700 text-sm font-medium">
              Lihat Semua
            </router-link>
          </div>
          
          <div class="space-y-3">
            <div
              v-for="session in recentSessions"
              :key="session.id"
              class="flex justify-between items-center p-3 bg-gray-50 rounded-lg"
            >
              <div>
                <p class="font-medium text-gray-900">Sesi #{{ session.id }}</p>
                <p class="text-sm text-gray-600">{{ session.item_pakaian.length }} item</p>
              </div>
              <span
                :class="[
                  'px-2 py-1 rounded-full text-xs font-medium',
                  getStatusBadgeClass(session.status)
                ]"
              >
                {{ session.status }}
              </span>
            </div>
            
            <div v-if="!recentSessions.length" class="text-center py-8 text-gray-500">
              <p>Belum ada sesi laundry</p>
              <router-link to="/laundry" class="text-primary-600 hover:text-primary-700 text-sm">
                Buat sesi baru
              </router-link>
            </div>
          </div>
        </div>
        
        <!-- Recent Clothes -->
        <div class="bg-white rounded-lg shadow-md p-6">
          <div class="flex justify-between items-center mb-4">
            <h2 class="text-lg font-semibold text-gray-900">Pakaian Terbaru</h2>
            <router-link to="/clothing" class="text-primary-600 hover:text-primary-700 text-sm font-medium">
              Lihat Semua
            </router-link>
          </div>
          
          <div class="space-y-3">
            <div
              v-for="clothing in recentClothes"
              :key="clothing.id"
              class="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg"
            >
              <div class="w-12 h-12 bg-gray-200 rounded-lg flex-shrink-0 overflow-hidden">
                <img
                  v-if="clothing.foto_url"
                  :src="clothing.foto_url"
                  :alt="clothing.nama_pakaian"
                  class="w-full h-full object-cover"
                >
                <div v-else class="w-full h-full flex items-center justify-center text-gray-400">
                  <span class="text-xs">👕</span>
                </div>
              </div>
              <div class="flex-1 min-w-0">
                <p class="font-medium text-gray-900 truncate">{{ clothing.nama_pakaian }}</p>
                <p class="text-sm text-gray-600 truncate">{{ clothing.kategori }}</p>
              </div>
            </div>
            
            <div v-if="!recentClothes.length" class="text-center py-8 text-gray-500">
              <p>Belum ada pakaian</p>
              <router-link to="/clothing" class="text-primary-600 hover:text-primary-700 text-sm">
                Tambah pakaian
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useClothingStore } from '@/stores/clothing'
import { useLaundryStore } from '@/stores/laundry'
import { useLogging } from '@/composables/useLogging'
import { getStatusBadgeClass } from '@/utils/helpers'
import AppLayout from '@/components/AppLayout.vue'

const authStore = useAuthStore()
const clothingStore = useClothingStore()
const laundryStore = useLaundryStore()
const { logAction } = useLogging()

const user = computed(() => authStore.user)

const stats = computed(() => ({
  totalClothes: clothingStore.clothes.length,
  activeSessions: laundryStore.sessions.filter(s => !['Selesai', 'Diambil'].includes(s.status)).length,
  inProgress: laundryStore.sessions.filter(s => ['Dicuci', 'Dikeringkan', 'Disetrika'].includes(s.status)).length,
  completed: laundryStore.sessions.filter(s => s.status === 'Selesai').length
}))

const recentSessions = computed(() => 
  laundryStore.sessions
    .slice()
    .sort((a, b) => new Date(b.tanggal_masuk) - new Date(a.tanggal_masuk))
    .slice(0, 5)
)

const recentClothes = computed(() => 
  clothingStore.clothes
    .slice(0, 5)
)

const refreshData = async () => {
  try {
    logAction('DASHBOARD', 'Refreshing dashboard data')
    await Promise.all([
      clothingStore.fetchClothes(),
      laundryStore.fetchSessions()
    ])
  } catch (error) {
    console.error('Failed to refresh data:', error)
  }
}

onMounted(async () => {
  logAction('NAVIGATION', 'Dashboard loaded')
  await refreshData()
})
</script>