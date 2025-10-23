<template>
  <div class="flex justify-center items-center">
    <div
      :class="[
        'animate-spin rounded-full border-t-2 border-b-2 border-primary-500',
        size === 'small' ? 'w-4 h-4' :
        size === 'medium' ? 'w-8 h-8' :
        'w-12 h-12'
      ]"
    ></div>
  </div>
</template>

<script setup>
defineProps({
  size: {
    type: String,
    default: 'medium',
    validator: (value) => ['small', 'medium', 'large'].includes(value)
  }
})
</script>