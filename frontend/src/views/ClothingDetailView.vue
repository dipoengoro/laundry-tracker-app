<template>
  <AppLayout>
    <div v-if="loading" class="flex justify-center py-12">
      <LoadingSpinner size="large"/>
    </div>

    <div v-else-if="clothing" class="max-w-4xl mx-auto space-y-6">
      <!-- Back Button -->
      <button
          class="flex items-center text-gray-600 hover:text-gray-900"
          @click="$router.go(-1)"
      >
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path d="M15 19l-7-7 7-7" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path>
        </svg>
        Back
      </button>

      <!-- Clothing Detail Card -->
      <div class="bg-white rounded-lg shadow-lg overflow-hidden">
        <div class="md:flex">
          <!-- Image -->
          <div class="md:w-1/2">
            <ImageUpload
                :clothingId="clothing.id"
                :currentImage="clothing.photo_url"
                @uploaded="handleImageUploaded"
            />
          </div>

          <!-- Details -->
          <div class="md:w-1/2 p-6">
            <div class="space-y-4">
              <div>
                <h1 class="text-2xl font-bold text-gray-900 mb-2">{{ clothing.name }}</h1>
                <div v-if="clothing.fades_easily"
                     class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-yellow-100 text-yellow-800">
                  ⚠️ Fades Easily
                </div>
              </div>

              <div class="space-y-3">
                <div v-if="clothing.category" class="flex">
                  <span class="w-24 text-sm font-medium text-gray-600">Category:</span>
                  <span class="text-sm text-gray-900">{{ clothing.category }}</span>
                </div>

                <div v-if="clothing.type" class="flex">
                  <span class="w-24 text-sm font-medium text-gray-600">Type:</span>
                  <span class="text-sm text-gray-900">{{ clothing.type }}</span>
                </div>

                <div v-if="clothing.color" class="flex">
                  <span class="w-24 text-sm font-medium text-gray-600">Color:</span>
                  <span class="text-sm text-gray-900">{{ clothing.color }}</span>
                </div>

                <div v-if="clothing.material" class="flex">
                  <span class="w-24 text-sm font-medium text-gray-600">Material:</span>
                  <span class="text-sm text-gray-900">{{ clothing.material }}</span>
                </div>
              </div>

              <div v-if="clothing.washing_instructions" class="bg-blue-50 p-4 rounded-lg">
                <h3 class="text-sm font-medium text-blue-900 mb-2">Washing Instructions:</h3>
                <p class="text-sm text-blue-800">{{ clothing.washing_instructions }}</p>
              </div>

              <!-- Actions -->
              <div class="flex space-x-3 pt-4">
                <button
                    class="btn-primary"
                    @click="editClothing"
                >
                  Edit Clothing
                </button>
                <button
                    class="px-4 py-2 text-sm font-medium text-red-600 bg-red-50 rounded-lg hover:bg-red-100 transition-colors"
                    @click="deleteClothing"
                >
                  Delete
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="text-center py-12">
      <p class="text-gray-500">No clothing found</p>
    </div>

    <ConfirmDialog
        ref="confirmDialog"
        message="Are you sure you want to delete this item?"
        title="Delete Clothing"
    />
  </AppLayout>
</template>

<script setup>
import {onMounted, ref} from 'vue'
import {useRoute, useRouter} from 'vue-router'
import {useClothingStore} from '@/stores/clothing'
import {useToast} from '@/composables/useToast'
import {useLogging} from '@/composables/useLogging'
import AppLayout from '@/components/AppLayout.vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import ConfirmDialog from '@/components/ConfirmDialog.vue'
import ImageUpload from '@/components/ImageUpload.vue'

const route = useRoute()
const router = useRouter()
const clothingStore = useClothingStore()
const {showToast} = useToast()
const {logAction} = useLogging()

const loading = ref(true)
const clothing = ref(null)
const confirmDialog = ref(null)

const fetchClothing = async () => {
  const clothingId = parseInt(route.params.id)
  try {
    clothing.value = await clothingStore.fetchClothingById(clothingId)
    if (!clothing.value) {
      showToast('error', 'No clothing found')
      router.push('/clothing')
    }
  } catch (error) {
    showToast('error', 'Failed to load clothing details')
    router.push('/clothing')
  }
}

const handleImageUploaded = async () => {
  await fetchClothing()
}

const editClothing = () => {
  router.push('/clothing')
}

const deleteClothing = async () => {
  const confirmed = await confirmDialog.value.show()
  if (confirmed) {
    try {
      await clothingStore.deleteClothing(clothing.value.id)
      logAction('CLOTHING', 'Clothing deleted from detail view', {clothingId: clothing.value.id})
      showToast('success', 'Clothes successfully removed')
      router.push('/clothing')
    } catch (error) {
      showToast('error', 'Failed to remove clothes')
    }
  }
}

onMounted(async () => {
  const clothingId = parseInt(route.params.id)
  logAction('NAVIGATION', 'Clothing detail view loaded', {clothingId})

  loading.value = true
  await fetchClothing()
  loading.value = false
})
</script>