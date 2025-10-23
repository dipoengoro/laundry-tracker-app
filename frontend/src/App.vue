<template>
  <div id="app">
    <router-view />
    
    <!-- Toast Notifications -->
    <div class="fixed bottom-4 right-4 z-50">
      <div
        v-for="toast in toasts"
        :key="toast.id"
        :class="[
          'mb-2 p-4 rounded-lg shadow-lg max-w-sm transform transition-all duration-300',
          toast.type === 'success' ? 'bg-green-500 text-white' :
          toast.type === 'error' ? 'bg-red-500 text-white' :
          toast.type === 'warning' ? 'bg-yellow-500 text-white' :
          'bg-blue-500 text-white'
        ]"
      >
        <div class="flex justify-between items-center">
          <span>{{ toast.message }}</span>
          <button @click="removeToast(toast.id)" class="ml-2 text-white hover:text-gray-200">
            ×
          </button>
        </div>
      </div>
    </div>
    
    <!-- Loading Overlay -->
    <div v-if="loading" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <LoadingSpinner size="large" />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useUIStore } from '@/stores/ui'
import { useToast } from '@/composables/useToast'
import LoadingSpinner from '@/components/LoadingSpinner.vue'

const uiStore = useUIStore()
const { toasts, removeToast } = useToast()

const loading = computed(() => uiStore.isLoading)
</script>