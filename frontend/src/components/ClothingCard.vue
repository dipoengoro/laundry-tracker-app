<template>
  <div class="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow p-4">
    <!-- Image -->
    <div class="aspect-square bg-gray-100 rounded-lg mb-4 overflow-hidden">
      <img
        v-if="clothing.foto_url"
        :src="clothing.foto_url"
        :alt="clothing.nama_pakaian"
        class="w-full h-full object-cover"
      >
      <div v-else class="w-full h-full flex items-center justify-center text-gray-400">
        <svg class="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
        </svg>
      </div>
    </div>
    
    <!-- Content -->
    <div class="space-y-2">
      <h3 class="font-semibold text-gray-900 truncate">{{ clothing.nama_pakaian }}</h3>
      
      <div class="space-y-1 text-sm text-gray-600">
        <p v-if="clothing.kategori">
          <span class="font-medium">Kategori:</span> {{ clothing.kategori }}
        </p>
        <p v-if="clothing.jenis_pakaian">
          <span class="font-medium">Jenis:</span> {{ clothing.jenis_pakaian }}
        </p>
        <p v-if="clothing.warna">
          <span class="font-medium">Warna:</span> {{ clothing.warna }}
        </p>
        <p v-if="clothing.bahan">
          <span class="font-medium">Bahan:</span> {{ clothing.bahan }}
        </p>
      </div>
      
      <!-- Care Instructions -->
      <div v-if="clothing.petunjuk_pencucian" class="text-xs text-gray-500 bg-gray-50 p-2 rounded">
        <span class="font-medium">Petunjuk:</span> {{ clothing.petunjuk_pencucian }}
      </div>
      
      <!-- Mudah Luntur Badge -->
      <div v-if="clothing.mudah_luntur" class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
        ⚠️ Mudah Luntur
      </div>
    </div>
    
    <!-- Actions -->
    <div class="mt-4 flex justify-between">
      <button
        @click="$emit('view', clothing)"
        class="text-primary-600 hover:text-primary-700 text-sm font-medium"
      >
        Lihat Detail
      </button>
      
      <div class="space-x-2">
        <button
          @click="$emit('edit', clothing)"
          class="text-blue-600 hover:text-blue-700 text-sm"
        >
          Edit
        </button>
        <button
          @click="$emit('delete', clothing)"
          class="text-red-600 hover:text-red-700 text-sm"
        >
          Hapus
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  clothing: {
    type: Object,
    required: true
  }
})

defineEmits(['view', 'edit', 'delete'])
</script>