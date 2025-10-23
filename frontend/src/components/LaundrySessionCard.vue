<template>
  <div class="bg-white rounded-lg shadow-md p-6">
    <!-- Header -->
    <div class="flex justify-between items-start mb-4">
      <div>
        <h3 class="text-lg font-semibold text-gray-900">
          Sesi #{{ session.id }}
        </h3>
        <p class="text-sm text-gray-500">
          {{ formatDate(session.tanggal_masuk) }}
        </p>
      </div>
      
      <!-- Status Badge -->
      <span
        :class="[
          'inline-flex items-center px-3 py-1 rounded-full text-xs font-medium',
          getStatusColor(session.status)
        ]"
      >
        {{ session.status }}
      </span>
    </div>
    
    <!-- Items Count -->
    <div class="mb-4">
      <p class="text-sm text-gray-600">
        <span class="font-medium">{{ session.item_pakaian.length }}</span> item pakaian
      </p>
    </div>
    
    <!-- Items Preview -->
    <div class="mb-4">
      <div class="flex flex-wrap gap-2">
        <div
          v-for="(item, index) in session.item_pakaian.slice(0, 3)"
          :key="item.id"
          class="flex items-center space-x-1 bg-gray-100 px-2 py-1 rounded text-xs"
        >
          <span>{{ item.nama_pakaian }}</span>
        </div>
        <div
          v-if="session.item_pakaian.length > 3"
          class="flex items-center px-2 py-1 bg-gray-200 rounded text-xs text-gray-600"
        >
          +{{ session.item_pakaian.length - 3 }} lainnya
        </div>
      </div>
    </div>
    
    <!-- Progress Bar -->
    <div class="mb-4">
      <div class="flex justify-between text-xs text-gray-500 mb-1">
        <span>Progress</span>
        <span>{{ getProgressPercentage(session.status) }}%</span>
      </div>
      <div class="w-full bg-gray-200 rounded-full h-2">
        <div
          class="bg-primary-500 h-2 rounded-full transition-all duration-300"
          :style="{ width: `${getProgressPercentage(session.status)}%` }"
        ></div>
      </div>
    </div>
    
    <!-- Estimated Completion -->
    <div v-if="session.estimasi_selesai" class="mb-4 text-sm text-gray-600">
      <span class="font-medium">Estimasi selesai:</span>
      {{ formatDate(session.estimasi_selesai) }}
    </div>
    
    <!-- Actions -->
    <div class="flex justify-between items-center">
      <button
        @click="$emit('view-details', session)"
        class="text-primary-600 hover:text-primary-700 text-sm font-medium"
      >
        Lihat Detail
      </button>
      
      <div class="space-x-2" v-if="canUpdateStatus(session.status)">
        <select
          :value="session.status"
          @change="$emit('update-status', session.id, $event.target.value)"
          class="text-xs border border-gray-300 rounded px-2 py-1 focus:outline-none focus:ring-1 focus:ring-primary-500"
        >
          <option v-for="status in availableStatuses" :key="status.value" :value="status.value">
            {{ status.label }}
          </option>
        </select>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { LAUNDRY_STATUSES } from '@/utils/constants'
import { formatDateTime } from '@/utils/helpers'

const props = defineProps({
  session: {
    type: Object,
    required: true
  }
})

defineEmits(['view-details', 'update-status'])

const availableStatuses = LAUNDRY_STATUSES

const formatDate = (dateString) => {
  return formatDateTime(dateString)
}

const getStatusColor = (status) => {
  const statusObj = LAUNDRY_STATUSES.find(s => s.value === status)
  if (!statusObj) return 'bg-gray-100 text-gray-800'
  
  const colorMap = {
    blue: 'bg-blue-100 text-blue-800',
    indigo: 'bg-indigo-100 text-indigo-800',
    purple: 'bg-purple-100 text-purple-800',
    pink: 'bg-pink-100 text-pink-800',
    green: 'bg-green-100 text-green-800',
    gray: 'bg-gray-100 text-gray-800'
  }
  
  return colorMap[statusObj.color] || 'bg-gray-100 text-gray-800'
}

const getProgressPercentage = (status) => {
  const statusIndex = LAUNDRY_STATUSES.findIndex(s => s.value === status)
  return Math.round(((statusIndex + 1) / LAUNDRY_STATUSES.length) * 100)
}

const canUpdateStatus = (currentStatus) => {
  return !['Selesai', 'Diambil'].includes(currentStatus)
}
</script>