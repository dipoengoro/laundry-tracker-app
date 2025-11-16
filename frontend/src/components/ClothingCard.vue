<template>
  <div class="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow p-4">
    <!-- Image -->
    <div class="aspect-square bg-gray-100 rounded-lg mb-4 overflow-hidden">
      <img
          v-if="clothing.photo_url"
          :src="clothing.photo_url"
          :alt="clothing.name"
          class="w-full h-full object-cover"
      >
      <div v-else class="w-full h-full flex items-center justify-center text-gray-400">
        <svg class="w-12 h-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
        </svg>
      </div>
    </div>

    <!-- Content -->
    <div class="space-y-2">
      <h3 class="font-semibold text-gray-900 truncate">{{ clothing.name }}</h3>

      <div class="space-y-1 text-sm text-gray-600">
        <p v-if="clothing.category">
          <span class="font-medium">Category:</span> {{ clothing.category }}
        </p>
        <p v-if="clothing.type">
          <span class="font-medium">Type:</span> {{ clothing.type }}
        </p>
        <p v-if="clothing.color">
          <span class="font-medium">Color:</span> {{ clothing.color }}
        </p>
        <p v-if="clothing.material">
          <span class="font-medium">Material:</span> {{ clothing.material }}
        </p>
      </div>

      <!-- Care Instructions -->
      <div v-if="clothing.washing_instructions" class="text-xs text-gray-500 bg-gray-50 p-2 rounded">
        <span class="font-medium">Washing Instruction:</span> {{ clothing.washing_instructions }}
      </div>

      <!-- Mudah Luntur Badge -->
      <div v-if="clothing.fades_easily"
           class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
        ⚠️ Fades easily
      </div>
    </div>

    <!-- Actions -->
    <div class="mt-4 flex justify-between">
      <button
          @click="$emit('view', clothing)"
          class="text-primary-600 hover:text-primary-700 text-sm font-medium"
      >
        See Details
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
          Delete
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