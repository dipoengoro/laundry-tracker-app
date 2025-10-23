export function formatDateTime(dateString, options = {}) {
  if (!dateString) return ''
  
  const date = new Date(dateString)
  const now = new Date()
  
  if (options.dateOnly) {
    return date.toLocaleDateString('id-ID', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    })
  }
  
  // Check if it's today
  const isToday = date.toDateString() === now.toDateString()
  
  if (isToday) {
    return date.toLocaleTimeString('id-ID', {
      hour: '2-digit',
      minute: '2-digit'
    })
  }
  
  // Check if it's this week
  const diffTime = Math.abs(now - date)
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  
  if (diffDays <= 7) {
    return date.toLocaleDateString('id-ID', {
      weekday: 'long',
      hour: '2-digit',
      minute: '2-digit'
    })
  }
  
  return date.toLocaleDateString('id-ID', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

export function truncateText(text, maxLength = 100) {
  if (!text) return ''
  if (text.length <= maxLength) return text
  return text.substring(0, maxLength) + '...'
}

export function capitalizeFirst(str) {
  if (!str) return ''
  return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase()
}

export function generateId() {
  return Math.random().toString(36).substring(2) + Date.now().toString(36)
}

export function downloadFile(data, filename, type = 'application/json') {
  const blob = new Blob([data], { type })
  const url = URL.createObjectURL(blob)
  
  const link = document.createElement('a')
  link.href = url
  link.download = filename
  
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  
  URL.revokeObjectURL(url)
}

export function debounce(func, delay) {
  let timeoutId
  return (...args) => {
    clearTimeout(timeoutId)
    timeoutId = setTimeout(() => func.apply(null, args), delay)
  }
}

export function throttle(func, delay) {
  let inThrottle
  return (...args) => {
    if (!inThrottle) {
      func.apply(null, args)
      inThrottle = true
      setTimeout(() => (inThrottle = false), delay)
    }
  }
}

export function validateEmail(email) {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return re.test(email)
}

export function validatePassword(password) {
  // At least 6 characters
  return password && password.length >= 6
}

export function formatFileSize(bytes) {
  if (bytes === 0) return '0 Bytes'
  
  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

export function getStatusBadgeClass(status) {
  const statusClasses = {
    'Diterima': 'bg-blue-100 text-blue-800',
    'Dicuci': 'bg-indigo-100 text-indigo-800',
    'Dikeringkan': 'bg-purple-100 text-purple-800',
    'Disetrika': 'bg-pink-100 text-pink-800',
    'Selesai': 'bg-green-100 text-green-800',
    'Diambil': 'bg-gray-100 text-gray-800'
  }
  
  return statusClasses[status] || 'bg-gray-100 text-gray-800'
}



export function normalizedUrl(path) {
  if (!path) return null
  if (path.startsWith('http')) return path
  return `/api${path.startsWith('/') ? path : '/' + path}`
}

export function normalizedDataClothing(clothing) {
  return {
    ...clothing,
    foto_url: normalizedUrl(clothing.foto_url)
  }
}