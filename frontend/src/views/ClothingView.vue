<template>
  <AppLayout>
    <div class="space-y-6">
      <!-- Header -->
      <div class="flex justify-between items-center">
        <h1 class="text-2xl font-bold text-gray-900">Manage Clothing</h1>
        <button
            class="btn-primary"
            @click="showAddModal = true"
        >
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path d="M12 4v16m8-8H4" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path>
          </svg>
          Add Clothing
        </button>
      </div>

      <!-- Search and Filter -->
      <div class="bg-white rounded-lg shadow-md p-4">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div class="md:col-span-2">
            <input
                v-model="searchQuery"
                class="form-input w-full"
                placeholder="Search clothing..."
                type="text"
            >
          </div>

          <div>
            <select v-model="filterCategory" class="form-input w-full">
              <option value="">Semua Kategori</option>
              <option v-for="category in CLOTHING_CATEGORIES" :key="category" :value="category">
                {{ category }}
              </option>
            </select>
          </div>

          <div>
            <select v-model="filterColor" class="form-input w-full">
              <option value="">All Colors</option>
              <option v-for="color in CLOTHING_COLORS" :key="color" :value="color">
                {{ color }}
              </option>
            </select>
          </div>
        </div>
      </div>

      <!-- Clothes Grid -->
      <div v-if="loading" class="flex justify-center py-12">
        <LoadingSpinner size="large"/>
      </div>

      <div v-else-if="filteredClothes.length"
           class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        <ClothingCard
            v-for="clothing in filteredClothes"
            :key="clothing.id"
            :clothing="clothing"
            @delete="deleteClothing"
            @edit="editClothing"
            @view="viewClothing"
        />
      </div>

      <div v-else class="text-center py-12">
        <div class="text-gray-400 mb-4">
          <svg class="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" stroke-linecap="round" stroke-linejoin="round"
                  stroke-width="2"></path>
          </svg>
        </div>
        <h3 class="text-lg font-medium text-gray-900 mb-2">There is no clothing yet</h3>
        <p class="text-gray-600 mb-4">Start to add your first clothing</p>
        <button class="btn-primary" @click="showAddModal = true">
          Add First Clothing
        </button>
      </div>
    </div>

    <!-- Add/Edit Modal -->
    <div v-if="showAddModal || showEditModal"
         class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div class="p-6 border-b border-gray-200">
          <div class="flex justify-between items-center">
            <h3 class="text-lg font-semibold text-gray-900">
              {{ showAddModal ? 'Add First Clothing' : 'Edit Clothing' }}
            </h3>
            <button class="text-gray-400 hover:text-gray-600" @click="closeModal">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path d="M6 18L18 6M6 6l12 12" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"></path>
              </svg>
            </button>
          </div>
        </div>

        <div class="p-6">
          <form class="space-y-4" @submit.prevent="submitForm">
            <div>
              <label class="form-label">Name *</label>
              <input
                  v-model="form.name"
                  class="form-input w-full"
                  placeholder="Example: Office White Shirt"
                  required
                  type="text"
              >
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="form-label">Category</label>
                <select v-model="form.category" class="form-input w-full">
                  <option value="">Select Category</option>
                  <option v-for="category in CLOTHING_CATEGORIES" :key="category" :value="category">
                    {{ category }}
                  </option>
                </select>
              </div>

              <div>
                <label class="form-label">Type</label>
                <select v-model="form.type" class="form-input w-full">
                  <option value="">Select Type</option>
                  <option v-for="type in CLOTHING_TYPES" :key="type" :value="type">
                    {{ type }}
                  </option>
                </select>
              </div>
            </div>

            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="form-label">Color</label>
                <select v-model="form.color" class="form-input w-full">
                  <option value="">Select Color</option>
                  <option v-for="color in CLOTHING_COLORS" :key="color" :value="color">
                    {{ color }}
                  </option>
                </select>
              </div>

              <div>
                <label class="form-label">Material</label>
                <select v-model="form.material" class="form-input w-full">
                  <option value="">Select Material</option>
                  <option v-for="material in CLOTHING_MATERIALS" :key="material" :value="material">
                    {{ material }}
                  </option>
                </select>
              </div>
            </div>

            <div>
              <label class="form-label">Washing Instructions</label>
              <textarea
                  v-model="form.washing_instructions"
                  class="form-input w-full h-20"
                  placeholder="Example: Wash with cold water, don't use bleach"
              ></textarea>
            </div>

            <div class="flex items-center">
              <input
                  v-model="form.fades_easily"
                  class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                  type="checkbox"
              >
              <label class="ml-2 text-sm text-gray-700">
                Fades easily (need special attention)
              </label>
            </div>

            <!-- Image Upload -->
            <div>
              <label class="form-label">Clothing Photo</label>
              <ImageUpload
                  :current-image="form.photo_url" :pakaianId="editingClothing?.id"
                  @uploaded="onImageUploaded" @file-selected="onFileSelected"
              />
            </div>

            <div class="flex justify-end space-x-3 pt-4">
              <button
                  class="btn-secondary"
                  type="button"
                  @click="closeModal"
              >
                Cancel
              </button>
              <button
                  :disabled="submitting"
                  class="btn-primary disabled:opacity-50"
                  type="submit"
              >
                <LoadingSpinner v-if="submitting" size="small"/>
                <span v-else>{{ showAddModal ? 'Add' : 'Save' }}</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Confirm Delete -->
    <ConfirmDialog
        ref="confirmDialog"
        cancel-text="Cancel"
        confirm-text="Yes, Confirm"
        message="Are you sure you want to delete this item? This action cannot be undone."
        title="Delete Clothing"
    />
  </AppLayout>
</template>

<script setup>
import {computed, onMounted, ref} from 'vue'
import {useRouter} from 'vue-router'
import {useClothingStore} from '@/stores/clothing'
import {useToast} from '@/composables/useToast'
import {useLogging} from '@/composables/useLogging'
import {CLOTHING_CATEGORIES, CLOTHING_COLORS, CLOTHING_MATERIALS, CLOTHING_TYPES} from '@/utils/constants'
import AppLayout from '@/components/AppLayout.vue'
import ClothingCard from '@/components/ClothingCard.vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import ConfirmDialog from '@/components/ConfirmDialog.vue'
import ImageUpload from '@/components/ImageUpload.vue'
import {usePresignedUrl} from "@/composables/usePresignedUrl";

const router = useRouter()
const clothingStore = useClothingStore()
const {showToast} = useToast()
const {logAction} = useLogging()

const loading = ref(true)
const submitting = ref(false)
const showAddModal = ref(false)
const showEditModal = ref(false)
const confirmDialog = ref(null)

const searchQuery = ref('')
const filterCategory = ref('')
const filterColor = ref('')
const {getPresignedUrl, uploadFile} = usePresignedUrl()
const fileToUpload = ref(null)

const form = ref({
  name: '',
  category: '',
  type: '',
  color: '',
  material: '',
  washing_instructions: '',
  fades_easily: false,
  photo_url: null
})

const editingClothing = ref(null)

const filteredClothes = computed(() => {
  let clothes = clothingStore.clothes

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    clothes = clothes.filter(c =>
        c.name.toLowerCase().includes(query) ||
        c.category?.toLowerCase().includes(query) ||
        c.type?.toLowerCase().includes(query) ||
        c.color?.toLowerCase().includes(query) ||
        c.material?.toLowerCase().includes(query)
    )
  }

  if (filterCategory.value) {
    clothes = clothes.filter(c => c.category === filterCategory.value)
  }

  if (filterColor.value) {
    clothes = clothes.filter(c => c.color === filterColor.value)
  }

  return clothes
})

const onFileSelected = (file) => {
  logAction('CLOTHING_FORM', 'File selected for upload', {name: file?.name})
  fileToUpload.value = file
}

const viewClothing = (clothing) => {
  logAction('CLOTHING', 'View clothing detail', {clothingId: clothing.id})
  router.push(`/clothing/${clothing.id}`)
}

const editClothing = (clothing) => {
  logAction('CLOTHING', 'Edit clothing started', {clothingId: clothing.id})
  editingClothing.value = clothing
  form.value = {...clothing}
  showEditModal.value = true
}

const deleteClothing = async (clothing) => {
  const confirmed = await confirmDialog.value.show()
  if (confirmed) {
    try {
      await clothingStore.deleteClothing(clothing.id)
      logAction('CLOTHING', 'Clothing deleted', {clothingId: clothing.id})
      showToast('success', 'Clothes successfully removed')
    } catch (error) {
      logAction('CLOTHING', 'Delete clothing failed', {error: error.message})
      showToast('error', 'Failed to remove clothes')
    }
  }
}

const onImageUploaded = async () => {
  try {
    const updatedClothing = await clothingStore.fetchClothingById(editingClothing.value.id)
    form.value.photo_url = updatedClothing.photo_url
    await clothingStore.fetchClothes()
    showToast('success', 'The clothing image has been refreshed')
  } catch (error) {
    showToast('error', 'Failed to refresh the clothes image')
  }
}

const submitForm = async () => {
  submitting.value = true;

  // === GANTI SEMUA KEY DI 'textData' ===
  const textData = {
    name: form.value.name,
    category: form.value.category,
    type: form.value.type,
    color: form.value.color,
    material: form.value.material,
    washing_instructions: form.value.washing_instructions,
    fades_easily: form.value.fades_easily,
  }
  // === SELESAI ===

  if (showAddModal.value) {
    let newClothing = null
    try {
      newClothing = await clothingStore.createClothing(textData) // Store udah bener
      logAction('CLOTHING', 'New clothing created', { id: newClothing.id, name: newClothing.name })

      if (fileToUpload.value) {
        logAction('CLOTHING', 'Starting image upload waterfall...', { id: newClothing.id })
        // usePresignedUrl (getPresignedUrl, uploadFile) udah kita benerin endpoint-nya
        const urlData = await getPresignedUrl(newClothing.id, fileToUpload.value)
        await uploadFile(urlData, fileToUpload.value)
        logAction('CLOTHING', 'Image upload complete', { id: newClothing.id })
      }
      showToast('success', 'Clothes added successfully!')
      closeModal()
      await clothingStore.fetchClothes()
    } catch (error) {
      logAction('CLOTHING', 'Create/Upload failed', { error: error.message })
      if (newClothing) {
        showToast('warning', 'Text data successful, but photo upload failed.')
        closeModal()
        await clothingStore.fetchClothes();
      } else {
        showToast('error', 'Failed to make clothes')
      }
    } finally {
      submitting.value = false
    }
  } else  {
    try {
      await clothingStore.updateClothing(editingClothing.value.id, textData) // Store udah bener
      logAction('CLOTHING', 'Clothing updated', { clothingId: editingClothing.value.id })
      showToast('success', 'Clothes successfully updated')
      closeModal()
      await clothingStore.fetchClothes()
    } catch (error) {
      logAction('CLOTHING', 'Update clothing failed', { error: error.message })
      showToast('error', 'Failed to update clothes')
    } finally {
      submitting.value = false
    }
  }
}

const closeModal = () => {
  showAddModal.value = false
  showEditModal.value = false
  editingClothing.value = null
  fileToUpload.value = null
  form.value = {
    name: '',
    category: '',
    type: '',
    color: '',
    material: '',
    washing_instructions: '',
    fades_easily: false,
    photo_url: null
  }
}

onMounted(async () => {
  logAction('NAVIGATION', 'Clothing view loaded')
  try {
    await clothingStore.fetchClothes()
  } catch (error) {
    showToast('error', 'Failed to load clothing data')
  } finally {
    loading.value = false
  }
})
</script>