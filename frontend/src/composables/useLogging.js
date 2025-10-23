import { ref } from 'vue'

const logs = ref([])

export function useLogging() {
  const logAction = (category, action, details = null) => {
    const timestamp = new Date().toISOString()
    const logEntry = {
      id: Date.now() + Math.random(),
      timestamp,
      category,
      action,
      details,
      userAgent: navigator.userAgent
    }
    
    // Add to local logs array
    logs.value.unshift(logEntry)
    
    // Limit logs to last 1000 entries
    if (logs.value.length > 1000) {
      logs.value = logs.value.slice(0, 1000)
    }
    
    // Console logging with formatting
    const logMessage = `[${category}] ${action}`
    const logDetails = details ? ` | Details: ${JSON.stringify(details)}` : ''
    
    console.log(`🔄 ${timestamp} ${logMessage}${logDetails}`)
    
    // Store in localStorage for persistence
    try {
      const storedLogs = JSON.parse(localStorage.getItem('appLogs') || '[]')
      storedLogs.unshift(logEntry)
      localStorage.setItem('appLogs', JSON.stringify(storedLogs.slice(0, 100))) // Keep only last 100
    } catch (error) {
      console.warn('Failed to store logs in localStorage:', error)
    }
  }
  
  const getLogs = () => {
    return logs.value
  }
  
  const clearLogs = () => {
    logs.value = []
    localStorage.removeItem('appLogs')
  }
  
  const exportLogs = () => {
    const logsData = JSON.stringify(logs.value, null, 2)
    const blob = new Blob([logsData], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    
    const a = document.createElement('a')
    a.href = url
    a.download = `laundry-tracker-logs-${new Date().toISOString().split('T')[0]}.json`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    
    URL.revokeObjectURL(url)
  }
  
  return {
    logAction,
    getLogs,
    clearLogs,
    exportLogs,
    logs
  }
}