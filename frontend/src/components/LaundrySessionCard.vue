<template>
  <div class="bg-white rounded-lg shadow-md p-6">
    <!-- Header -->
    <div class="flex justify-between items-start mb-4">
      <div>
        <h3 class="text-lg font-semibold text-gray-900">
          Sesi #{{ session.id }}
        </h3>
        <p class="text-sm text-gray-500">
          {{ formatDate(session.date_received) }}
        </p>
      </div>

      <!-- Status Badge -->
      <span
          :class="[
          'inline-flex items-center px-3 py-1 rounded-full text-xs font-medium',
          getStatusBadgeClass(session.status)
        ]"
      >
        {{ session.status }}
      </span>
    </div>

    <!-- Items Count -->
    <div class="mb-4">
      <p class="text-sm text-gray-600">
        <span class="font-medium">{{ session.clothing_items.length }}</span> clothing item
      </p>
    </div>

    <!-- Items Preview -->
    <div class="mb-4">
      <div class="flex flex-wrap gap-2">
        <div
            v-for="(item, _) in session.clothing_items.slice(0, 3)"
            :key="item.id"
            class="flex items-center space-x-1 bg-gray-100 px-2 py-1 rounded text-xs"
        >
          <span>{{ item.name }}</span>
        </div>
        <div
            v-if="session.clothing_items.length > 3"
            class="flex items-center px-2 py-1 bg-gray-200 rounded text-xs text-gray-600"
        >
          +{{ session.clothing_items.length - 3 }} others
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
            :style="{ width: `${getProgressPercentage(session.status)}%` }"
            class="bg-primary-500 h-2 rounded-full transition-all duration-300"
        ></div>
      </div>
    </div>

    <!-- Estimated Completion -->
    <div v-if="session.estimated_completion" class="mb-4 text-sm text-gray-600">
      <span class="font-medium">Estimated completion:</span>
      {{ formatDate(session.estimated_completion) }}
    </div>

    <!-- Actions -->
    <div class="flex justify-between items-center">
      <button
          class="text-primary-600 hover:text-primary-700 text-sm font-medium"
          @click="$emit('view-details', session)"
      >
        View Details
      </button>

      <div v-if="canUpdateStatus(session.status)" class="space-x-2">
        <select
            :value="session.status"
            class="text-xs border border-gray-300 rounded px-2 py-1 focus:outline-none focus:ring-1 focus:ring-primary-500"
            @change="$emit('update-status', session.id, $event.target.value)"
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
import {LAUNDRY_STATUSES} from '@/utils/constants'
import {formatDateTime, getStatusBadgeClass} from '@/utils/helpers'

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

const getProgressPercentage = (status) => {
  const statusIndex = LAUNDRY_STATUSES.findIndex(s => s.value === status)
  if (statusIndex === -1) return 0
  return Math.round(((statusIndex + 1) / LAUNDRY_STATUSES.length) * 100)
}

const canUpdateStatus = (currentStatus) => {
  return !['Completed', 'Taken'].includes(currentStatus)
}
</script>