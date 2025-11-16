<template>
  <AppLayout>
    <div class="space-y-6">
      <!-- Header -->
      <div class="flex justify-between items-center">
        <h1 class="text-2xl font-bold text-gray-900">Laundry Sessions</h1>
        <button
            class="btn-primary"
            @click="showCreateModal = true"
        >
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path d="M12 4v16m8-8H4" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path>
          </svg>
          New Session
        </button>
      </div>

      <!-- Filter Tabs -->
      <div class="bg-white rounded-lg shadow-md p-1">
        <nav class="flex space-x-1">
          <button
              v-for="filter in statusFilters"
              :key="filter.key"
              :class="[
              'flex-1 py-2 px-4 rounded-md text-sm font-medium transition-colors',
              activeFilter === filter.key
                ? 'bg-primary-500 text-white'
                : 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'
            ]"
              @click="activeFilter = filter.key"
          >
            {{ filter.label }}
            <span v-if="filter.count !== undefined" class="ml-2 px-2 py-1 bg-white bg-opacity-20 rounded-full text-xs">
              {{ filter.count }}
            </span>
          </button>
        </nav>
      </div>

      <!-- Sessions Grid -->
      <div v-if="loading" class="flex justify-center py-12">
        <LoadingSpinner size="large"/>
      </div>

      <div v-else-if="filteredSessions.length" class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <LaundrySessionCard
            v-for="session in filteredSessions"
            :key="session.id"
            :session="session"
            @view-details="viewSessionDetails"
            @update-status="updateSessionStatus"
        />
      </div>

      <div v-else class="text-center py-12">
        <div class="text-gray-400 mb-4">
          <svg class="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" stroke-linecap="round" stroke-linejoin="round"
                  stroke-width="2"></path>
          </svg>
        </div>
        <h3 class="text-lg font-medium text-gray-900 mb-2">
          {{
            activeFilter === 'all' ? 'There is no session laundry yet' :
                'There is no session laundry with this status'
          }}
        </h3>
        <p class="text-gray-600 mb-4">
          {{ activeFilter === 'all' ? 'Create your first laundry session' : 'Try other filter' }}
        </p>
        <button v-if="activeFilter === 'all'" class="btn-primary" @click="showCreateModal = true">
          Create your first laundry session
        </button>
      </div>
    </div>

    <!-- Create Session Modal -->
    <div v-if="showCreateModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div class="p-6 border-b border-gray-200">
          <div class="flex justify-between items-center">
            <h3 class="text-lg font-semibold text-gray-900">Create New Laundry Session</h3>
            <button class="text-gray-400 hover:text-gray-600" @click="closeCreateModal">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path d="M6 18L18 6M6 6l12 12" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path>
              </svg>
            </button>
          </div>
        </div>

        <div class="p-6">
          <div v-if="!availableClothes.length" class="text-center py-8">
            <div class="text-gray-400 mb-4">
              <svg class="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" stroke-linecap="round" stroke-linejoin="round"
                      stroke-width="2"></path>
              </svg>
            </div>
            <h3 class="text-lg font-medium text-gray-900 mb-2">There is no clothing</h3>
            <p class="text-gray-600 mb-4">Please add clothing first before create laundry session</p>
            <router-link class="btn-primary" to="/clothing">
              Add Clothing
            </router-link>
          </div>

          <div v-else>
            <div class="mb-4">
              <label class="form-label">Select clothing for laundry session</label>
              <div class="text-sm text-gray-600 mb-3">
                Select clothing for this laundry session
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 max-h-96 overflow-y-auto">
              <div
                  v-for="clothing in availableClothes"
                  :key="clothing.id"
                  :class="[
                  'border-2 rounded-lg p-4 cursor-pointer transition-colors',
                  selectedClothingIds.includes(clothing.id)
                    ? 'border-primary-500 bg-primary-50'
                    : 'border-gray-200 hover:border-gray-300'
                ]"
                  @click="toggleClothing(clothing.id)"
              >
                <div class="flex items-center space-x-3">
                  <div class="w-12 h-12 bg-gray-200 rounded-lg flex-shrink-0 overflow-hidden">
                    <img
                        v-if="clothing.photo_url"
                        :alt="clothing.name"
                        :src="clothing.photo_url"
                        class="w-full h-full object-cover"
                    >
                    <div v-else class="w-full h-full flex items-center justify-center text-gray-400">
                      <span class="text-xs">👕</span>
                    </div>
                  </div>

                  <div class="flex-1 min-w-0">
                    <p class="font-medium text-gray-900 truncate">{{ clothing.name }}</p>
                    <p class="text-sm text-gray-600 truncate">{{ clothing.category }}</p>
                    <div v-if="clothing.fades_easily" class="text-xs text-yellow-600 font-medium">
                      ⚠️ Fades Easily
                    </div>
                  </div>

                  <div class="flex-shrink-0">
                    <div
                        :class="[
                        'w-5 h-5 rounded border-2 flex items-center justify-center',
                        selectedClothingIds.includes(clothing.id)
                          ? 'bg-primary-500 border-primary-500 text-white'
                          : 'border-gray-300'
                      ]"
                    >
                      <svg v-if="selectedClothingIds.includes(clothing.id)" class="w-3 h-3" fill="currentColor"
                           viewBox="0 0 20 20">
                        <path clip-rule="evenodd"
                              d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                              fill-rule="evenodd"></path>
                      </svg>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div class="mt-6 flex justify-between items-center">
              <p class="text-sm text-gray-600">
                {{ selectedClothingIds.length }} selected clothing
              </p>

              <div class="space-x-3">
                <button
                    class="btn-secondary"
                    @click="closeCreateModal"
                >
                  Cancel
                </button>
                <button
                    :disabled="!selectedClothingIds.length || submitting"
                    class="btn-primary disabled:opacity-50"
                    @click="createSession"
                >
                  <LoadingSpinner v-if="submitting" size="small"/>
                  <span v-else>Create session ({{ selectedClothingIds.length }} item)</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import {computed, onMounted, ref} from 'vue'
import {useLaundryStore} from '@/stores/laundry'
import {useClothingStore} from '@/stores/clothing'
import {useToast} from '@/composables/useToast'
import {useLogging} from '@/composables/useLogging'
import AppLayout from '@/components/AppLayout.vue'
import LaundrySessionCard from '@/components/LaundrySessionCard.vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import {LAUNDRY_STATUSES} from "../utils/constants.js";

const laundryStore = useLaundryStore()
const clothingStore = useClothingStore()
const {showToast} = useToast()
const {logAction} = useLogging()

const loading = ref(true)
const submitting = ref(false)
const showCreateModal = ref(false)
const activeFilter = ref('all')
const selectedClothingIds = ref([])

const statusFilters = computed(() => [
  { key: 'all', label: 'All', count: laundryStore.sessions.length },
  { key: 'active', label: 'Active', count: laundryStore.sessions.filter(s => !['Completed', 'Taken'].includes(s.status)).length },
  { key: 'completed', label: 'Completed', count: laundryStore.sessions.filter(s => s.status === 'Completed').length },
  { key: 'taken', label: 'Taken', count: laundryStore.sessions.filter(s => s.status === 'Taken').length }
])

const filteredSessions = computed(() => {
  let sessions = laundryStore.sessions

  switch (activeFilter.value) {
    case 'active':
      return sessions.filter(s => !['Completed', 'Taken'].includes(s.status))
    case 'completed':
      return sessions.filter(s => s.status === 'Completed')
    case 'taken':
      return sessions.filter(s => s.status === 'Taken')
    default:
      return sessions
  }
})

const availableClothes = computed(() => {
  // Filter out clothes that are already in active sessions
  const activeSessions = laundryStore.sessions.filter(s => !['Completed', 'Taken'].includes(s.status))
  // 'item_pakaian' -> 'clothing_items'
  const usedClothingIds = activeSessions.flatMap(s => s.clothing_items.map(item => item.id))

  return clothingStore.clothes.filter(clothing => !usedClothingIds.includes(clothing.id))
})

const toggleClothing = (clothingId) => {
  const index = selectedClothingIds.value.indexOf(clothingId)
  if (index > -1) {
    selectedClothingIds.value.splice(index, 1)
  } else {
    selectedClothingIds.value.push(clothingId)
  }
}

const viewSessionDetails = (session) => {
  logAction('LAUNDRY', 'View session details', {sessionId: session.id})
  // In a real app, you might navigate to a detail page
  showToast('info', `Detail sesi #${session.id}`)
}

const updateSessionStatus = async (sessionId, newStatus) => {
  try {
    await laundryStore.updateSessionStatus(sessionId, newStatus)
    logAction('LAUNDRY', 'Session status updated', {sessionId, newStatus})
    showToast('success', 'Session status updated successfully')
  } catch (error) {
    logAction('LAUNDRY', 'Update session status failed', {error: error.message})
    showToast('error', 'Failed to update session status')
  }
}

const createSession = async () => {
  if (!selectedClothingIds.value.length) return

  submitting.value = true
  try {
    const sessionData = {
      clothing_item_ids: selectedClothingIds.value
    }

    await laundryStore.createSession(sessionData)
    logAction('LAUNDRY', 'New session created', {itemCount: selectedClothingIds.value.length})
    showToast('success', `New Session created with ${selectedClothingIds.value.length} item`)
    closeCreateModal()
  } catch (error) {
    logAction('LAUNDRY', 'Create session failed', {error: error.message})
    showToast('error', 'Failed to created new session')
  } finally {
    submitting.value = false
  }
}

const closeCreateModal = () => {
  showCreateModal.value = false
  selectedClothingIds.value = []
}

onMounted(async () => {
  logAction('NAVIGATION', 'Laundry view loaded')
  try {
    await Promise.all([
      laundryStore.fetchSessions(),
      clothingStore.fetchClothes()
    ])
  } catch (error) {
    showToast('error', 'Failed to load laundry session data')
  } finally {
    loading.value = false
  }
})
</script>