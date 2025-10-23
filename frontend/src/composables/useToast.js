import { ref } from 'vue'

const toasts = ref([])

export function useToast() {
  const showToast = (type, message, duration = 5000) => {
    const id = Date.now() + Math.random()
    const toast = {
      id,
      type, // 'success', 'error', 'warning', 'info'
      message,
      duration
    }
    
    toasts.value.push(toast)
    
    // Auto remove after duration
    setTimeout(() => {
      removeToast(id)
    }, duration)
    
    return id
  }
  
  const removeToast = (id) => {
    const index = toasts.value.findIndex(toast => toast.id === id)
    if (index > -1) {
      toasts.value.splice(index, 1)
    }
  }
  
  const clearAllToasts = () => {
    toasts.value = []
  }
  
  return {
    toasts,
    showToast,
    removeToast,
    clearAllToasts
  }
}