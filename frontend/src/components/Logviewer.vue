<template>
  <div class="log-viewer">
    <div class="log-header">
      <h2>Activity Logs</h2>
      <div class="log-actions">
        <button @click="exportLogs" class="btn btn-secondary">
          📊 Export Logs
        </button>
        <button @click="clearLogs" class="btn btn-danger">
          🗑️ Clear Logs
        </button>
      </div>
    </div>

    <!-- Filters -->
    <div class="log-filters">
      <select v-model="filterAction" @change="applyFilters" class="filter-select">
        <option value="">All Actions</option>
        <option value="CREATE">Create</option>
        <option value="UPDATE">Update</option>
        <option value="DELETE">Delete</option>
        <option value="FETCH">Fetch</option>
        <option value="UPLOAD_IMAGE">Upload Image</option>
      </select>
      
      <select v-model="filterStatus" @change="applyFilters" class="filter-select">
        <option value="">All Status</option>
        <option value="SUCCESS">Success</option>
        <option value="ERROR">Error</option>
      </select>
      
      <input 
        type="date" 
        v-model="filterDate" 
        @change="applyFilters"
        class="filter-date"
      >
    </div>

    <!-- Log Entries -->
    <div class="log-entries">
      <div 
        v-for="log in filteredLogs" 
        :key="log.id"
        class="log-entry"
        :class="`log-${log.status.toLowerCase()}`"
      >
        <div class="log-meta">
          <div class="log-timestamp">
            {{ formatTimestamp(log.timestamp) }}
          </div>
          <div class="log-user">{{ log.user }}</div>
        </div>
        
        <div class="log-content">
          <div class="log-action">
            <span class="action-badge" :class="`action-${log.action.toLowerCase()}`">
              {{ log.action }}
            </span>
            <span v-if="log.item_name" class="item-name">{{ log.item_name }}</span>
          </div>
          <div class="log-details">{{ log.details }}</div>
        </div>
        
        <div class="log-status">
          <span 
            class="status-badge"
            :class="`status-${log.status.toLowerCase()}`"
          >
            {{ log.status === 'SUCCESS' ? '✅' : '❌' }} {{ log.status }}
          </span>
        </div>
      </div>

      <div v-if="filteredLogs.length === 0" class="no-logs">
        <div class="no-logs-icon">📝</div>
        <p>No activity logs found</p>
      </div>
    </div>

    <!-- Pagination -->
    <div v-if="totalPages > 1" class="log-pagination">
      <button 
        @click="currentPage--"
        :disabled="currentPage === 1"
        class="page-btn"
      >
        Previous
      </button>
      
      <span class="page-info">
        Page {{ currentPage }} of {{ totalPages }}
      </span>
      
      <button 
        @click="currentPage++"
        :disabled="currentPage === totalPages"
        class="page-btn"
      >
        Next
      </button>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { usePakaianStore } from '../stores/pakaian'

export default {
  name: 'LogViewer',
  setup() {
    const pakaianStore = usePakaianStore()
    
    // Filters
    const filterAction = ref('')
    const filterStatus = ref('')
    const filterDate = ref('')
    const currentPage = ref(1)
    const itemsPerPage = 10
    
    // Computed
    const filteredLogs = computed(() => {
      let logs = [...pakaianStore.logs]
      
      // Apply filters
      if (filterAction.value) {
        logs = logs.filter(log => log.action === filterAction.value)
      }
      
      if (filterStatus.value) {
        logs = logs.filter(log => log.status === filterStatus.value)
      }
      
      if (filterDate.value) {
        const filterDateStr = filterDate.value
        logs = logs.filter(log => {
          const logDate = new Date(log.timestamp).toISOString().split('T')
          return logDate === filterDateStr
        })
      }
      
      // Apply pagination
      const start = (currentPage.value - 1) * itemsPerPage
      const end = start + itemsPerPage
      
      return logs.slice(start, end)
    })
    
    const totalPages = computed(() => {
      let logs = [...pakaianStore.logs]
      
      // Apply filters for count
      if (filterAction.value) {
        logs = logs.filter(log => log.action === filterAction.value)
      }
      
      if (filterStatus.value) {
        logs = logs.filter(log => log.status === filterStatus.value)
      }
      
      if (filterDate.value) {
        const filterDateStr = filterDate.value
        logs = logs.filter(log => {
          const logDate = new Date(log.timestamp).toISOString().split('T')
          return logDate === filterDateStr
        })
      }
      
      return Math.ceil(logs.length / itemsPerPage)
    })
    
    // Methods
    const formatTimestamp = (timestamp) => {
      const date = new Date(timestamp)
      return date.toLocaleString('id-ID', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
      })
    }
    
    const applyFilters = () => {
      currentPage.value = 1
    }
    
    const exportLogs = () => {
      const logsToExport = pakaianStore.logs.map(log => ({
        timestamp: formatTimestamp(log.timestamp),
        user: log.user,
        action: log.action,
        item_name: log.item_name || '',
        details: log.details,
        status: log.status
      }))
      
      // Convert to CSV
      const headers = ['Timestamp', 'User', 'Action', 'Item Name', 'Details', 'Status']
      const csvContent = [
        headers.join(','),
        ...logsToExport.map(log => 
          [log.timestamp, log.user, log.action, log.item_name, log.details, log.status]
            .map(field => `"${field}"`)
            .join(',')
        )
      ].join('\n')
      
      // Download
      const blob = new Blob([csvContent], { type: 'text/csv' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `activity-logs-${new Date().toISOString().split('T')}.csv`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      URL.revokeObjectURL(url)
    }
    
    const clearLogs = () => {
      if (confirm('Are you sure you want to clear all logs? This action cannot be undone.')) {
        pakaianStore.logs.splice(0)
      }
    }
    
    return {
      pakaianStore,
      filterAction,
      filterStatus,
      filterDate,
      currentPage,
      filteredLogs,
      totalPages,
      formatTimestamp,
      applyFilters,
      exportLogs,
      clearLogs
    }
  }
}
</script>

<style scoped>
.log-viewer {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

.log-header {
  padding: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #f9fafb;
}

.log-header h2 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: #111827;
}

.log-actions {
  display: flex;
  gap: 0.5rem;
}

.log-filters {
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.filter-select,
.filter-date {
  padding: 0.5rem 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 0.875rem;
}

.log-entries {
  max-height: 600px;
  overflow-y: auto;
}

.log-entry {
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #f3f4f6;
  display: grid;
  grid-template-columns: 200px 1fr 120px;
  gap: 1rem;
  align-items: start;
}

.log-entry.log-error {
  background: #fef2f2;
}

.log-meta {
  font-size: 0.75rem;
  color: #6b7280;
}

.log-timestamp {
  font-weight: 500;
  margin-bottom: 0.25rem;
}

.log-user {
  color: #9ca3af;
}

.log-content {
  min-width: 0;
}

.log-action {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.action-badge {
  padding: 0.125rem 0.5rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
}

.action-create { background: #dcfce7; color: #166534; }
.action-update { background: #dbeafe; color: #1e40af; }
.action-delete { background: #fee2e2; color: #dc2626; }
.action-fetch { background: #f3f4f6; color: #374151; }
.action-upload_image { background: #fef3c7; color: #92400e; }

.item-name {
  font-weight: 500;
  color: #111827;
  truncate: true;
}

.log-details {
  font-size: 0.875rem;
  color: #6b7280;
  line-height: 1.4;
}

.log-status {
  text-align: right;
}

.status-badge {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 500;
}

.status-success {
  background: #dcfce7;
  color: #166534;
}

.status-error {
  background: #fee2e2;
  color: #dc2626;
}

.no-logs {
  text-align: center;
  padding: 4rem 2rem;
  color: #6b7280;
}

.no-logs-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.log-pagination {
  padding: 1rem 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1px solid #e5e7eb;
}

.page-btn {
  padding: 0.5rem 1rem;
  border: 1px solid #d1d5db;
  background: white;
  color: #374151;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.875rem;
}

.page-btn:hover:not(:disabled) {
  background: #f3f4f6;
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-info {
  font-size: 0.875rem;
  color: #6b7280;
}

.btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-secondary {
  background: #f3f4f6;
  color: #374151;
}

.btn-secondary:hover {
  background: #e5e7eb;
}

.btn-danger {
  background: #dc2626;
  color: white;
}

.btn-danger:hover {
  background: #b91c1c;
}

@media (max-width: 768px) {
  .log-entry {
    grid-template-columns: 1fr;
    gap: 0.5rem;
  }
  
  .log-filters {
    flex-direction: column;
  }
  
  .log-header {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
}
</style>
