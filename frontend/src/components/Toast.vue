<template>
  <Transition name="toast">
    <div 
      v-if="visible" 
      class="toast"
      :class="`toast-${type}`"
    >
      <div class="toast-content">
        <div class="toast-icon">
          {{ getIcon(type) }}
        </div>
        <div class="toast-message">{{ message }}</div>
        <button @click="$emit('close')" class="toast-close">
          ×
        </button>
      </div>
    </div>
  </Transition>
</template>

<script>
export default {
  name: 'Toast',
  emits: ['close'],
  props: {
    visible: Boolean,
    message: String,
    type: {
      type: String,
      default: 'success'
    }
  },
  methods: {
    getIcon(type) {
      const icons = {
        success: '✅',
        error: '❌',
        warning: '⚠️',
        info: 'ℹ️'
      }
      return icons[type] || icons.info
    }
  }
}
</script>

<style scoped>
.toast {
  position: fixed;
  top: 2rem;
  right: 2rem;
  z-index: 1002;
  min-width: 300px;
  max-width: 500px;
}

.toast-content {
  background: white;
  border-radius: 8px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
  padding: 1rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  border-left: 4px solid;
}

.toast-success .toast-content {
  border-color: #10b981;
}

.toast-error .toast-content {
  border-color: #ef4444;
}

.toast-warning .toast-content {
  border-color: #f59e0b;
}

.toast-info .toast-content {
  border-color: #3b82f6;
}

.toast-message {
  flex: 1;
  font-size: 0.875rem;
  font-weight: 500;
  color: #111827;
}

.toast-close {
  background: none;
  border: none;
  font-size: 1.25rem;
  cursor: pointer;
  color: #6b7280;
  padding: 0;
  line-height: 1;
}

.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from {
  transform: translateX(100%);
  opacity: 0;
}

.toast-leave-to {
  transform: translateX(100%);
  opacity: 0;
}
</style>
