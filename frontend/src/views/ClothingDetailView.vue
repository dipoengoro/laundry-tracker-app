<template>
  <AppLayout>
    <div v-if="loading" class="flex justify-center py-12">
      <LoadingSpinner size="large" />
    </div>
    
    <div v-else-if="clothing" class="max-w-4xl mx-auto space-y-6">
      <!-- Back Button -->
      <button
        @click="$router.go(-1)"
        class="flex items-center text-gray-600 hover:text-gray-900"
      >
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
        </svg>
        Kembali
      </button>
      
      <!-- Clothing Detail Card -->
      <div class="bg-white rounded-lg shadow-lg overflow-hidden">
        <div class="md:flex">
          <!-- Image -->
          <div class="md:w-1/2">
            <div class="aspect-square bg-gray-100">
              <img
                v-if="clothing.foto_url"
                :src="clothing.foto_url"
                :alt="clothing.nama_pakaian"
                class="w-full h-full object-cover"
              >
              <div v-else class="w-full h-full flex items-center justify-center text-gray-400">
                <svg class="w-24 h-24" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                </svg>
              </div>
            </div>
          </div>
          
          <!-- Details -->
          <div class="md:w-1/2 p-6">
            <div class="space-y-4">
              <div>
                <h1 class="text-2xl font-bold text-gray-900 mb-2">{{ clothing.nama_pakaian }}</h1>
                <div v-if="clothing.mudah_luntur" class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-yellow-100 text-yellow-800">
                  ⚠️ Mudah Luntur
                </div>
              </div>
              
              <div class="space-y-3">
                <div v-if="clothing.kategori" class="flex">
                  <span class="w-24 text-sm font-medium text-gray-600">Kategori:</span>
                  <span class="text-sm text-gray-900">{{ clothing.kategori }}</span>
                </div>
                
                <div v-if="clothing.jenis_pakaian" class="flex">
                  <span class="w-24 text-sm font-medium text-gray-600">Jenis:</span>
                  <span class="text-sm text-gray-900">{{ clothing.jenis_pakaian }}</span>
                </div>
                
                <div v-if="clothing.warna" class="flex">
                  <span class="w-24 text-sm font-medium text-gray-600">Warna:</span>
                  <span class="text-sm text-gray-900">{{ clothing.warna }}</span>
                </div>
                
                <div v-if="clothing.bahan" class="flex">
                  <span class="w-24 text-sm font-medium text-gray-600">Bahan:</span>
                  <span class="text-sm text-gray-900">{{ clothing.bahan }}</span>
                </div>
              </div>
              
              <div v-if="clothing.petunjuk_pencucian" class="bg-blue-50 p-4 rounded-lg">
                <h3 class="text-sm font-medium text-blue-900 mb-2">Petunjuk Pencucian:</h3>
                <p class="text-sm text-blue-800">{{ clothing.petunjuk_pencucian }}</p>
              </div>
              
              <!-- Actions -->
              <div class="flex space-x-3 pt-4">
                <button
                  @click="editClothing"
                  class="btn-primary"
                >
                  Edit Pakaian
                </button>
                <button
                  @click="deleteClothing"
                  class="px-4 py-2 text-sm font-medium text-red-600 bg-red-50 rounded-lg hover:bg-red-100 transition-colors"
                >
                  Hapus
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div v-else class="text-center py-12">
      <p class="text-gray-500">Pakaian tidak ditemukan</p>
    </div>
    
    <ConfirmDialog
      ref="confirmDialog"
      title="Hapus Pakaian"
      message="Apakah Anda yakin ingin menghapus pakaian ini?"
    />
  </AppLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useClothingStore } from '@/stores/clothing'
import { useToast } from '@/composables/useToast'
import { useLogging } from '@/composables/useLogging'
import AppLayout from '@/components/AppLayout.vue'
import LoadingSpinner from '@/components/LoadingSpinner.vue'
import ConfirmDialog from '@/components/ConfirmDialog.vue'

const route = useRoute()
const router = useRouter()
const clothingStore = useClothingStore()
const { showToast } = useToast()
const { logAction } = useLogging()

const loading = ref(true)
const clothing = ref(null)
const confirmDialog = ref(null)

const editClothing = () => {
  router.push('/clothing')
}

const deleteClothing = async () => {
  const confirmed = await confirmDialog.value.show()
  if (confirmed) {
    try {
      await clothingStore.deleteClothing(clothing.value.id)
      logAction('CLOTHING', 'Clothing deleted from detail view', { clothingId: clothing.value.id })
      showToast('success', 'Pakaian berhasil dihapus')
      router.push('/clothing')
    } catch (error) {
      showToast('error', 'Gagal menghapus pakaian')
    }
  }
}

onMounted(async () => {
  const clothingId = parseInt(route.params.id)
  logAction('NAVIGATION', 'Clothing detail view loaded', { clothingId })
  
  try {
    clothing.value = await clothingStore.getClothingById(clothingId)
    if (!clothing.value) {
      showToast('error', 'Pakaian tidak ditemukan')
      router.push('/clothing')
    }
    console.log(clothing.value)
  } catch (error) {
    showToast('error', 'Gagal memuat detail pakaian')
    router.push('/clothing')
  } finally {
    loading.value = false
  }
})
</script>