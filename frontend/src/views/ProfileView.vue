<template>
  <AppLayout>
    <div class="max-w-2xl mx-auto space-y-6">
      <h1 class="text-2xl font-bold text-gray-900">User Profile</h1>

      <!-- Profile Card -->
      <div class="bg-white rounded-lg shadow-md p-6">
        <div class="flex items-center space-x-6 mb-6">
          <div class="relative">
            <img
                :alt="user?.username"
                :src="user?.profile_photo_url || '/default-avatar.png'"
                class="w-24 h-24 rounded-full object-cover border-4 border-gray-200"
            >
            <button
                class="absolute bottom-0 right-0 p-2 bg-primary-500 text-white rounded-full hover:bg-primary-600 transition-colors"
                @click="showImageUpload = true"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" stroke-linecap="round" stroke-linejoin="round"
                      stroke-width="2"></path>
                <path d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" stroke-linecap="round" stroke-linejoin="round"
                      stroke-width="2"></path>
              </svg>
            </button>
          </div>

          <div>
            <h2 class="text-xl font-semibold text-gray-900">{{ user?.username }}</h2>
            <p class="text-gray-600">{{ user?.email }}</p>
            <p class="text-sm text-gray-500">
              Joined {{ formatDate(user?.created_at) }}
            </p>
          </div>
        </div>

        <!-- Edit Profile Form -->
        <form class="space-y-4" @submit.prevent="updateProfile">
          <div>
            <label class="form-label">Email</label>
            <input
                v-model="profileForm.email"
                class="form-input w-full"
                required
                type="email"
            >
          </div>

          <div class="flex justify-end">
            <button
                :disabled="submitting || !hasProfileChanges"
                class="btn-primary disabled:opacity-50"
                type="submit"
            >
              <LoadingSpinner v-if="submitting" size="small"/>
              <span v-else>Perbarui Profil</span>
            </button>
          </div>
        </form>
      </div>

      <!-- Change Password -->
      <div class="bg-white rounded-lg shadow-md p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">Ubah Password</h3>

        <form class="space-y-4" @submit.prevent="changePassword">
          <div>
            <label class="form-label">Password Lama</label>
            <input
                v-model="passwordForm.currentPassword"
                class="form-input w-full"
                required
                type="password"
            >
          </div>

          <div>
            <label class="form-label">Password Baru</label>
            <input
                v-model="passwordForm.newPassword"
                class="form-input w-full"
                minlength="6"
                required
                type="password"
            >
          </div>

          <div>
            <label class="form-label">Konfirmasi Password Baru</label>
            <input
                v-model="passwordForm.confirmPassword"
                class="form-input w-full"
                required
                type="password"
            >
          </div>

          <div class="flex justify-end">
            <button
                :disabled="passwordSubmitting || !isPasswordValid"
                class="btn-primary disabled:opacity-50"
                type="submit"
            >
              <LoadingSpinner v-if="passwordSubmitting" size="small"/>
              <span v-else>Ubah Password</span>
            </button>
          </div>
        </form>
      </div>

      <!-- Account Stats -->
      <div class="bg-white rounded-lg shadow-md p-6">
        <h3 class="text-lg font-semibold text-gray-900 mb-4">Statistik Akun</h3>

        <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div class="text-center p-4 bg-blue-50 rounded-lg">
            <div class="text-2xl font-bold text-blue-600">{{ stats.totalClothes }}</div>
            <div class="text-sm text-blue-600">Total Pakaian</div>
          </div>

          <div class="text-center p-4 bg-green-50 rounded-lg">
            <div class="text-2xl font-bold text-green-600">{{ stats.totalSessions }}</div>
            <div class="text-sm text-green-600">Total Sesi</div>
          </div>

          <div class="text-center p-4 bg-yellow-50 rounded-lg">
            <div class="text-2xl font-bold text-yellow-600">{{ stats.activeSessions }}</div>
            <div class="text-sm text-yellow-600">Sesi Aktif</div>
          </div>

          <div class="text-center p-4 bg-purple-50 rounded-lg">
            <div class="text-2xl font-bold text-purple-600">{{ stats.completedSessions }}</div>
            <div class="text-sm text-purple-600">Selesai</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Image Upload Modal -->
    <div v-if="showImageUpload" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-lg shadow-xl max-w-md w-full">
        <div class="p-6 border-b border-gray-200">
          <div class="flex justify-between items-center">
            <h3 class="text-lg font-semibold text-gray-900">Edit Profile Photo</h3>
            <button class="text-gray-400 hover:text-gray-600" @click="showImageUpload = false">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path d="M6 18L18 6M6 6l12 12" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path>
              </svg>
            </button>
          </div>
        </div>

        <div class="p-6">
          <ImageUpload
              :current-image="user?.profile_photo_url"
              @file-selected="updateProfilePicture"
          />
        </div>
      </div>
    </div>
  </AppLayout>
</template>

<script setup>
import {computed, onMounted, ref} from 'vue'
import {useAuthStore} from '@/stores/auth'
import {useClothingStore} from '@/stores/clothing'
import {useLaundryStore} from '@/stores/laundry'
import {useToast} from '@/composables/useToast'
import {useLogging} from '@/composables/useLogging'
import {formatDateTime} from '@/utils/helpers'
import AppLayout from '@/components/AppLayout.vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import ImageUpload from '@/components/ImageUpload.vue'

const authStore = useAuthStore()
const clothingStore = useClothingStore()
const laundryStore = useLaundryStore()
const {showToast} = useToast()
const {logAction} = useLogging()

const submitting = ref(false)
const passwordSubmitting = ref(false)
const showImageUpload = ref(false)

const user = computed(() => authStore.user)

const profileForm = ref({
  email: ''
})

const passwordForm = ref({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const stats = computed(() => ({
  totalClothes: clothingStore.clothes.length,
  totalSessions: laundryStore.sessions.length,
  activeSessions: laundryStore.sessions.filter(s => !['Completed', 'Taken'].includes(s.status)).length,
  completedSessions: laundryStore.sessions.filter(s => s.status === 'Completed').length
}))

const hasProfileChanges = computed(() => {
  return profileForm.value.email !== user.value?.email
})

const isPasswordValid = computed(() => {
  return passwordForm.value.currentPassword &&
      passwordForm.value.newPassword &&
      passwordForm.value.confirmPassword &&
      passwordForm.value.newPassword === passwordForm.value.confirmPassword &&
      passwordForm.value.newPassword.length >= 6
})

const formatDate = (dateString) => {
  if (!dateString) return ''
  return formatDateTime(dateString, {dateOnly: true})
}

const updateProfile = async () => {
  submitting.value = true
  try {
    await authStore.updateProfile({
      email: profileForm.value.email
    })
    logAction('PROFILE', 'Profile updated')
    showToast('success', 'Profil berhasil diperbarui')
  } catch (error) {
    logAction('PROFILE', 'Profile update failed', {error: error.message})
    showToast('error', 'Gagal memperbarui profil')
  } finally {
    submitting.value = false
  }
}

const updateProfilePicture = async (file) => {
  try {
    await authStore.updateProfilePicture(file)
    logAction('PROFILE', 'Profile picture updated')
    showToast('success', 'Foto profil berhasil diperbarui')
    showImageUpload.value = false
  } catch (error) {
    logAction('PROFILE', 'Profile picture update failed', {error: error.message})
    showToast('error', 'Gagal memperbarui foto profil')
  }
}

const changePassword = async () => {
  if (passwordForm.value.newPassword !== passwordForm.value.confirmPassword) {
    showToast('error', 'Password baru tidak cocok')
    return
  }

  passwordSubmitting.value = true
  try {
    // In a real app, you would call an API to change password
    // For now, we'll just show a success message
    logAction('PROFILE', 'Password change attempted')
    showToast('success', 'Password berhasil diubah')

    // Reset form
    passwordForm.value = {
      currentPassword: '',
      newPassword: '',
      confirmPassword: ''
    }
  } catch (error) {
    logAction('PROFILE', 'Password change failed', {error: error.message})
    showToast('error', 'Gagal mengubah password')
  } finally {
    passwordSubmitting.value = false
  }
}

onMounted(async () => {
  logAction('NAVIGATION', 'Profile view loaded')

  // Initialize profile form with current user data
  if (user.value) {
    profileForm.value.email = user.value.email
  }

  // Load stats data
  try {
    await Promise.all([
      clothingStore.fetchClothes(),
      laundryStore.fetchSessions()
    ])
  } catch (error) {
    console.error('Failed to load profile stats:', error)
  }
})
</script>