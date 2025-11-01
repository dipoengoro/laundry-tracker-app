<template>
  <AppLayout>
    <div class="space-y-6">
      <!-- Header -->
      <div class="flex justify-between items-center">
        <h1 class="text-2xl font-bold text-gray-900">Kelola Pakaian</h1>
        <button
          @click="showAddModal = true"
          class="btn-primary"
        >
          <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
          </svg>
          Tambah Pakaian
        </button>
      </div>
      
      <!-- Search and Filter -->
      <div class="bg-white rounded-lg shadow-md p-4">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div class="md:col-span-2">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Cari pakaian..."
              class="form-input w-full"
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
              <option value="">Semua Warna</option>
              <option v-for="color in CLOTHING_COLORS" :key="color" :value="color">
                {{ color }}
              </option>
            </select>
          </div>
        </div>
      </div>
      
      <!-- Clothes Grid -->
      <div v-if="loading" class="flex justify-center py-12">
        <LoadingSpinner size="large" />
      </div>
      
      <div v-else-if="filteredClothes.length" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        <ClothingCard
          v-for="clothing in filteredClothes"
          :key="clothing.id"
          :clothing="clothing"
          @view="viewClothing"
          @edit="editClothing"
          @delete="deleteClothing"
        />
      </div>
      
      <div v-else class="text-center py-12">
        <div class="text-gray-400 mb-4">
          <svg class="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"></path>
          </svg>
        </div>
        <h3 class="text-lg font-medium text-gray-900 mb-2">Belum ada pakaian</h3>
        <p class="text-gray-600 mb-4">Mulai dengan menambahkan pakaian pertama Anda</p>
        <button @click="showAddModal = true" class="btn-primary">
          Tambah Pakaian Pertama
        </button>
      </div>
    </div>
    
    <!-- Add/Edit Modal -->
    <div v-if="showAddModal || showEditModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div class="p-6 border-b border-gray-200">
          <div class="flex justify-between items-center">
            <h3 class="text-lg font-semibold text-gray-900">
              {{ showAddModal ? 'Tambah Pakaian Baru' : 'Edit Pakaian' }}
            </h3>
            <button @click="closeModal" class="text-gray-400 hover:text-gray-600">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
              </svg>
            </button>
          </div>
        </div>
        
        <div class="p-6">
          <form @submit.prevent="submitForm" class="space-y-4">
            <div>
              <label class="form-label">Nama Pakaian *</label>
              <input
                v-model="form.nama_pakaian"
                type="text"
                class="form-input w-full"
                placeholder="Contoh: Kemeja Putih Kantor"
                required
              >
            </div>
            
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="form-label">Kategori</label>
                <select v-model="form.kategori" class="form-input w-full">
                  <option value="">Pilih Kategori</option>
                  <option v-for="category in CLOTHING_CATEGORIES" :key="category" :value="category">
                    {{ category }}
                  </option>
                </select>
              </div>
              
              <div>
                <label class="form-label">Jenis Pakaian</label>
                <select v-model="form.jenis_pakaian" class="form-input w-full">
                  <option value="">Pilih Jenis</option>
                  <option v-for="type in CLOTHING_TYPES" :key="type" :value="type">
                    {{ type }}
                  </option>
                </select>
              </div>
            </div>
            
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label class="form-label">Warna</label>
                <select v-model="form.warna" class="form-input w-full">
                  <option value="">Pilih Warna</option>
                  <option v-for="color in CLOTHING_COLORS" :key="color" :value="color">
                    {{ color }}
                  </option>
                </select>
              </div>
              
              <div>
                <label class="form-label">Bahan</label>
                <select v-model="form.bahan" class="form-input w-full">
                  <option value="">Pilih Bahan</option>
                  <option v-for="material in CLOTHING_MATERIALS" :key="material" :value="material">
                    {{ material }}
                  </option>
                </select>
              </div>
            </div>
            
            <div>
              <label class="form-label">Petunjuk Pencucian</label>
              <textarea
                v-model="form.petunjuk_pencucian"
                class="form-input w-full h-20"
                placeholder="Contoh: Cuci dengan air dingin, jangan gunakan pemutih"
              ></textarea>
            </div>
            
            <div class="flex items-center">
              <input
                v-model="form.mudah_luntur"
                type="checkbox"
                class="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
              >
              <label class="ml-2 text-sm text-gray-700">
                Mudah luntur (perlu perhatian khusus)
              </label>
            </div>
            
            <!-- Image Upload -->
            <div>
              <label class="form-label">Foto Pakaian</label>
              <ImageUpload
               :pakaianId="editingClothing?.id" :current-image="form.foto_url"
               @uploaded="onImageUploaded" @file-selected="onFileSelected"
              />
            </div>
            
            <div class="flex justify-end space-x-3 pt-4">
              <button
                type="button"
                @click="closeModal"
                class="btn-secondary"
              >
                Batal
              </button>
              <button
                type="submit"
                :disabled="submitting"
                class="btn-primary disabled:opacity-50"
              >
                <LoadingSpinner v-if="submitting" size="small" />
                <span v-else>{{ showAddModal ? 'Tambah' : 'Simpan' }}</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
    
    <!-- Confirm Delete -->
    <ConfirmDialog
      ref="confirmDialog"
      title="Hapus Pakaian"
      message="Apakah Anda yakin ingin menghapus pakaian ini? Tindakan ini tidak dapat dibatalkan."
      confirm-text="Ya, Hapus"
      cancel-text="Batal"
    />
  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useClothingStore } from '@/stores/clothing'
import { useToast } from '@/composables/useToast'
import { useLogging } from '@/composables/useLogging'
import { 
  CLOTHING_CATEGORIES, 
  CLOTHING_TYPES, 
  CLOTHING_COLORS, 
  CLOTHING_MATERIALS 
} from '@/utils/constants'
import AppLayout from '@/components/AppLayout.vue'
import ClothingCard from '@/components/ClothingCard.vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import ConfirmDialog from '@/components/ConfirmDialog.vue'
import ImageUpload from '@/components/ImageUpload.vue'
import { usePresignedUrl } from "@/composables/usePresignedUrl";

const router = useRouter()
const clothingStore = useClothingStore()
const { showToast } = useToast()
const { logAction } = useLogging()

const loading = ref(true)
const submitting = ref(false)
const showAddModal = ref(false)
const showEditModal = ref(false)
const confirmDialog = ref(null)

const searchQuery = ref('')
const filterCategory = ref('')
const filterColor = ref('')
const { getPresignedUrl, uploadFile } = usePresignedUrl()
const fileToUpload = ref(null)

const form = ref({
  nama_pakaian: '',
  kategori: '',
  jenis_pakaian: '',
  warna: '',
  bahan: '',
  petunjuk_pencucian: '',
  mudah_luntur: false,
  foto_url: null
})

const editingClothing = ref(null)

const filteredClothes = computed(() => {
  let clothes = clothingStore.clothes
  
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    clothes = clothes.filter(c => 
      c.nama_pakaian.toLowerCase().includes(query) ||
      c.kategori?.toLowerCase().includes(query) ||
      c.jenis_pakaian?.toLowerCase().includes(query) ||
      c.warna?.toLowerCase().includes(query) ||
      c.bahan?.toLowerCase().includes(query)
    )
  }
  
  if (filterCategory.value) {
    clothes = clothes.filter(c => c.kategori === filterCategory.value)
  }
  
  if (filterColor.value) {
    clothes = clothes.filter(c => c.warna === filterColor.value)
  }
  
  return clothes
})

const onFileSelected = (file) => {
  logAction('CLOTHING_FORM', 'File selected for upload', { name: file?.name })
  fileToUpload.value = file
}

const viewClothing = (clothing) => {
  logAction('CLOTHING', 'View clothing detail', { clothingId: clothing.id })
  router.push(`/clothing/${clothing.id}`)
}

const editClothing = (clothing) => {
  logAction('CLOTHING', 'Edit clothing started', { clothingId: clothing.id })
  editingClothing.value = clothing
  form.value = { ...clothing }
  showEditModal.value = true
}

const deleteClothing = async (clothing) => {
  const confirmed = await confirmDialog.value.show()
  if (confirmed) {
    try {
      await clothingStore.deleteClothing(clothing.id)
      logAction('CLOTHING', 'Clothing deleted', { clothingId: clothing.id })
      showToast('success', 'Pakaian berhasil dihapus')
    } catch (error) {
      logAction('CLOTHING', 'Delete clothing failed', { error: error.message })
      showToast('error', 'Gagal menghapus pakaian')
    }
  }
}

const onImageUploaded = async () => {
  try {
    const updatedClothing = await clothingStore.getClothingById(editingClothing.value.id)
    form.value.foto_url = updatedClothing.foto_url
    await clothingStore.fetchClothes()
    showToast('success', 'Gambar berhasil di-refresh')
  } catch (error) {
    showToast('error', 'Gagal nge-refresh data gambar')
  }
}

const submitForm = async () => {
  submitting.value = true;
  const textData = {
    nama_pakaian: form.value.nama_pakaian,
    kategori: form.value.kategori,
    jenis_pakaian: form.value.jenis_pakaian,
    warna: form.value.warna,
    bahan: form.value.bahan,
    petunjuk_pencucian: form.value.petunjuk_pencucian,
    mudah_luntur: form.value.mudah_luntur,
  }
  if (showAddModal.value) {
    let newClothing = null
    try {
      newClothing = await clothingStore.createClothing(textData)
      logAction('CLOTHING', 'New clothing created', { id: newClothing.id, name: newClothing.nama_pakaian })

      if (fileToUpload.value) {
        logAction('CLOTHING', 'Starting image upload waterfall...', { id: newClothing.id })
        const urlData = await getPresignedUrl(newClothing.id, fileToUpload.value)
        await uploadFile(urlData, fileToUpload.value)
        logAction('CLOTHING', 'Image upload complete', { id: newClothing.id })
      }
      showToast('success', 'Pakaian berhasil ditambahkan!')
      closeModal()
      await clothingStore.fetchClothes()
    } catch (error) {
      logAction('CLOTHING', 'Create/Upload failed', { error: error.message })
      if (newClothing) {
        showToast('warning', 'Data teks sukses, tapi upload foto gagal.')
        closeModal()
        await clothingStore.fetchClothes();
      } else {
        showToast('error', 'Gagal membuat pakaian')
      }
    } finally {
      submitting.value = false
    }
  } else  {
    try {
      await clothingStore.updateClothing(editingClothing.value.id, textData)
      logAction('CLOTHING', 'Clothing updated', { clothingId: editingClothing.value.id })
      showToast('success', 'Pakaian berhasil diperbarui')
      closeModal()
      await clothingStore.fetchClothes()
    } catch (error) {
      logAction('CLOTHING', 'Update clothing failed', { error: error.message })
      showToast('error', 'Gagal memperbarui pakaian')
    } finally {
      submitting.valu = false
    }
  }
}

const closeModal = () => {
  showAddModal.value = false
  showEditModal.value = false
  editingClothing.value = null
  fileToUpload.value = null
  form.value = {
    nama_pakaian: '',
    kategori: '',
    jenis_pakaian: '',
    warna: '',
    bahan: '',
    petunjuk_pencucian: '',
    mudah_luntur: false,
    foto_url: null
  }
}

onMounted(async () => {
  logAction('NAVIGATION', 'Clothing view loaded')
  try {
    await clothingStore.fetchClothes()
  } catch (error) {
    showToast('error', 'Gagal memuat data pakaian')
  } finally {
    loading.value = false
  }
})
</script>