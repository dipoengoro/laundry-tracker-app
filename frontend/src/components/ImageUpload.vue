<template>
  <div class="space-y-4">
    <!-- Preview -->
    <div v-if="previewUrl || currentImage" class="relative">
      <img
        :src="urlClothing(previewUrl) || currentImage"
        alt="Preview"
        class="w-32 h-32 object-cover rounded-lg border"
      >
      <button
        v-if="previewUrl"
        @click="clearImage"
        class="absolute -top-2 -right-2 w-6 h-6 bg-red-500 text-white rounded-full flex items-center justify-center hover:bg-red-600 transition-colors"
      >
        ×
      </button>
    </div>
    
    <!-- Upload Area -->
    <div
      @drop="handleDrop"
      @dragover="handleDragOver"
      @dragleave="handleDragLeave"
      :class="[
        'border-2 border-dashed rounded-lg p-6 text-center cursor-pointer transition-colors',
        isDragging ? 'border-primary-500 bg-primary-50' : 'border-gray-300 hover:border-gray-400'
      ]"
      @click="triggerFileInput"
    >
      <input
        ref="fileInput"
        type="file"
        accept="image/*"
        class="hidden"
        @change="handleFileSelect"
      >
      
      <div class="space-y-2">
        <svg class="w-8 h-8 text-gray-400 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
        </svg>
        <p class="text-sm text-gray-600">
          Drag & drop gambar atau <span class="text-primary-500 font-medium">klik untuk pilih</span>
        </p>
        <p class="text-xs text-gray-500">PNG, JPG, GIF hingga 5MB</p>
      </div>
    </div>
    
    <!-- Upload Button -->
    <div v-if="selectedFile && !uploading" class="flex justify-center">
      <button
        @click="handleUpload"
        class="btn-primary"
      >
        Upload Gambar
      </button>
    </div>
    
    <!-- Loading -->
    <div v-if="uploading" class="flex justify-center">
      <LoadingSpinner />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useToast } from '@/composables/useToast'
import LoadingSpinner from './LoadingSpinner.vue'

const props = defineProps({
  currentImage: {
    type: String,
    default: null
  }
})

const emit = defineEmits(['uploaded', 'error'])

const { showToast } = useToast()

const fileInput = ref(null)
const selectedFile = ref(null)
const previewUrl = ref(null)
const isDragging = ref(false)
const uploading = ref(false)

const triggerFileInput = () => {
  fileInput.value.click()
}

const handleFileSelect = (event) => {
  const file = event.target.files[0]
  if (file) {
    validateAndSetFile(file)
  }
}

const handleDrop = (event) => {
  event.preventDefault()
  isDragging.value = false
  
  const file = event.dataTransfer.files[0]
  if (file) {
    validateAndSetFile(file)
  }
}

const urlClothing = (url) => {
        if (!url) return null
      return `http://localhost:8000${url}`
    }

const handleDragOver = (event) => {
  event.preventDefault()
  isDragging.value = true
}

const handleDragLeave = () => {
  isDragging.value = false
}

const validateAndSetFile = (file) => {
  // Validate file type
  if (!file.type.startsWith('image/')) {
    showToast('error', 'Hanya file gambar yang diperbolehkan')
    return
  }
  
  // Validate file size (5MB)
  if (file.size > 5 * 1024 * 1024) {
    showToast('error', 'Ukuran file maksimal 5MB')
    return
  }
  
  selectedFile.value = file
  
  // Create preview
  const reader = new FileReader()
  reader.onload = (e) => {
    previewUrl.value = e.target.result
  }
  reader.readAsDataURL(file)
}

const clearImage = () => {
  selectedFile.value = null
  previewUrl.value = null
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

const handleUpload = () => {
  if (!selectedFile.value) return
  
  emit('uploaded', selectedFile.value)
  clearImage()
}
</script>