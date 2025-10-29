<template>
  <div class="dashboard">
    <!-- Header with Statistics -->
    <div class="dashboard-header">
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-icon">👕</div>
          <div class="stat-content">
            <div class="stat-number">{{ pakaianStore.totalItems }}</div>
            <div class="stat-label">Total Pakaian</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">📂</div>
          <div class="stat-content">
            <div class="stat-number">{{ Object.keys(pakaianStore.categoryStats).length }}</div>
            <div class="stat-label">Kategori</div>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">🔍</div>
          <div class="stat-content">
            <div class="stat-number">{{ pakaianStore.filteredItems.length }}</div>
            <div class="stat-label">Hasil Filter</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Search and Filters -->
    <div class="controls-section">
      <div class="search-section">
        <div class="search-box">
          <input
            type="text"
            v-model="searchQuery"
            @input="handleSearch"
            placeholder="Cari nama pakaian, kategori, atau jenis..."
            class="search-input"
          >
          <button class="search-btn">
            <svg width="20" height="20" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd" />
            </svg>
          </button>
        </div>
        
        <div class="filter-section">
          <select
            v-model="selectedCategory"
            @change="handleCategoryFilter"
            class="category-filter"
          >
            <option value="">Semua Kategori</option>
            <option v-for="category in categories" :key="category" :value="category">
              {{ category }}
            </option>
          </select>
        </div>
      </div>

      <div class="action-section">
        <button @click="openAddModal" class="btn btn-primary">
          <svg width="20" height="20" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" />
          </svg>
          Tambah Pakaian
        </button>
        
        <button 
          @click="toggleBulkMode" 
          class="btn btn-secondary"
          :class="{ active: bulkMode }"
        >
          <svg width="20" height="20" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clip-rule="evenodd" />
          </svg>
          {{ bulkMode ? 'Batal Pilih' : 'Pilih Multiple' }}
        </button>
        
        <div class="view-toggle">
          <button 
            @click="viewMode = 'grid'"
            class="view-btn"
            :class="{ active: viewMode === 'grid' }"
          >
            <svg width="20" height="20" fill="currentColor" viewBox="0 0 20 20">
              <path d="M5 3a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2V5a2 2 0 00-2-2H5zM5 11a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2v-2a2 2 0 00-2-2H5zM11 5a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V5zM11 13a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
            </svg>
          </button>
          <button 
            @click="viewMode = 'list'"
            class="view-btn"
            :class="{ active: viewMode === 'list' }"
          >
            <svg width="20" height="20" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clip-rule="evenodd" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Bulk Actions Bar -->
    <div v-if="bulkMode && selectedItems.size > 0" class="bulk-actions">
      <div class="bulk-info">
        {{ selectedItems.size }} item(s) dipilih
      </div>
      <div class="bulk-buttons">
        <button @click="bulkDelete" class="btn btn-danger">
          <svg width="20" height="20" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9zM4 5a2 2 0 012-2h8a2 2 0 012 2v6a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 102 0v3a1 1 0 11-2 0V9zm4 0a1 1 0 10-2 0v3a1 1 0 002 0V9z" clip-rule="evenodd" />
          </svg>
          Hapus Terpilih
        </button>
        <button @click="selectedItems.clear()" class="btn btn-secondary">
          Batal Pilih
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="pakaianStore.isLoading" class="loading-state">
      <div class="spinner"></div>
      <p>Memuat data pakaian...</p>
    </div>

    <!-- Empty State -->
    <div v-else-if="pakaianStore.filteredItems.length === 0 && !pakaianStore.isLoading" class="empty-state">
      <div class="empty-icon">👕</div>
      <h3>{{ searchQuery || selectedCategory ? 'Tidak ada hasil' : 'Belum ada pakaian' }}</h3>
      <p>
        {{ searchQuery || selectedCategory 
          ? 'Coba ubah kata kunci pencarian atau filter kategori' 
          : 'Kamu belum punya pakaian nih. Yuk, tambahkan sekarang!' 
        }}
      </p>
      <button v-if="!searchQuery && !selectedCategory" @click="openAddModal" class="btn btn-primary">
        Tambah Pakaian Pertama
      </button>
    </div>

    <!-- Content Grid/List -->
    <div v-else class="content-area">
      <!-- Grid View -->
      <div v-if="viewMode === 'grid'" class="pakaian-grid">
        <div 
          v-for="pakaian in pakaianStore.paginatedItems" 
          :key="pakaian.id" 
          class="pakaian-card"
          :class="{ 
            selected: selectedItems.has(pakaian.id),
            'bulk-mode': bulkMode 
          }"
          @click="handleCardClick(pakaian)"
        >
          <!-- Bulk Selection Checkbox -->
          <div v-if="bulkMode" class="bulk-checkbox">
            <input 
              type="checkbox" 
              :checked="selectedItems.has(pakaian.id)"
              @change="toggleItemSelection(pakaian.id)"
              @click.stop
            >
          </div>

          <!-- Clothing Image -->
          <div class="card-image">
            <img 
              v-if="pakaian.foto_url" 
              :src="pakaian.foto_url" 
              :alt="pakaian.nama_pakaian"
              class="clothing-img"
            >
            <div v-else class="no-image">
              <svg width="48" height="48" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M4 3a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V5a2 2 0 00-2-2H4zm12 12H4l4-8 3 6 2-4 3 6z" clip-rule="evenodd" />
              </svg>
              <span>Tidak Ada Gambar</span>
            </div>
          </div>

          <!-- Card Content -->
          <div class="card-content">
            <div class="card-header">
              <h3 class="card-title">{{ pakaian.nama_pakaian }}</h3>
              <div class="card-category">{{ pakaian.kategori || 'Tanpa Kategori' }}</div>
            </div>
            
            <div class="card-details">
              <div v-if="pakaian.jenis_pakaian" class="detail-item">
                <span class="detail-label">Jenis:</span>
                <span class="detail-value">{{ pakaian.jenis_pakaian }}</span>
              </div>
              <div v-if="pakaian.warna" class="detail-item">
                <span class="detail-label">Warna:</span>
                <span class="detail-value">{{ pakaian.warna }}</span>
              </div>
              <div v-if="pakaian.bahan" class="detail-item">
                <span class="detail-label">Bahan:</span>
                <span class="detail-value">{{ pakaian.bahan }}</span>
              </div>
              <div v-if="pakaian.mudah_luntur" class="warning-badge">
                ⚠️ Mudah Luntur
              </div>
            </div>

            <!-- Card Actions -->
            <div v-if="!bulkMode" class="card-actions">
              <button @click.stop="openEditModal(pakaian)" class="action-btn edit-btn">
                <svg width="16" height="16" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                </svg>
              </button>
              <button @click.stop="confirmDelete(pakaian)" class="action-btn delete-btn">
                <svg width="16" height="16" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9zM4 5a2 2 0 012-2h8a2 2 0 012 2v6a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 102 0v3a1 1 0 11-2 0V9zm4 0a1 1 0 10-2 0v3a1 1 0 002 0V9z" clip-rule="evenodd" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- List View -->
      <div v-else class="pakaian-list">
        <div class="list-header">
          <div class="list-col">
            <input 
              v-if="bulkMode" 
              type="checkbox" 
              @change="toggleSelectAll"
              :checked="selectedItems.size === pakaianStore.paginatedItems.length"
            >
            Nama
          </div>
          <div class="list-col">Kategori</div>
          <div class="list-col">Jenis</div>
          <div class="list-col">Warna</div>
          <div class="list-col">Bahan</div>
          <div class="list-col">Status</div>
          <div class="list-col">Aksi</div>
        </div>

        <div 
          v-for="pakaian in pakaianStore.paginatedItems" 
          :key="pakaian.id" 
          class="list-row"
          :class="{ selected: selectedItems.has(pakaian.id) }"
        >
          <div class="list-col">
            <input 
              v-if="bulkMode" 
              type="checkbox" 
              :checked="selectedItems.has(pakaian.id)"
              @change="toggleItemSelection(pakaian.id)"
            >
            <div class="item-info">
              <img 
                v-if="pakaian.foto_url" 
                :src="urlClothing(pakaian.foto_url)" 
                :alt="pakaian.nama_pakaian"
                class="list-img"
              >
              <div v-else class="list-no-img">📷</div>
              <span class="item-name">{{ pakaian.nama_pakaian }}</span>
            </div>
          </div>
          <div class="list-col">
            <span class="category-badge">{{ pakaian.kategori || '-' }}</span>
          </div>
          <div class="list-col">{{ pakaian.jenis_pakaian || '-' }}</div>
          <div class="list-col">{{ pakaian.warna || '-' }}</div>
          <div class="list-col">{{ pakaian.bahan || '-' }}</div>
          <div class="list-col">
            <span v-if="pakaian.mudah_luntur" class="warning-badge">⚠️ Mudah Luntur</span>
            <span v-else class="ok-badge">✅ Normal</span>
          </div>
          <div class="list-col">
            <div class="list-actions">
              <button @click="openEditModal(pakaian)" class="action-btn edit-btn">
                ✏️
              </button>
              <button @click="confirmDelete(pakaian)" class="action-btn delete-btn">
                🗑️
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Pagination -->
      <div v-if="pakaianStore.totalPages > 1" class="pagination">
        <button 
          @click="goToPage(pakaianStore.currentPage - 1)"
          :disabled="pakaianStore.currentPage === 1"
          class="page-btn"
        >
          ← Sebelumnya
        </button>
        
        <div class="page-numbers">
          <button
            v-for="page in visiblePages"
            :key="page"
            @click="goToPage(page)"
            :class="{ active: page === pakaianStore.currentPage }"
            class="page-number"
          >
            {{ page }}
          </button>
        </div>
        
        <button 
          @click="goToPage(pakaianStore.currentPage + 1)"
          :disabled="pakaianStore.currentPage === pakaianStore.totalPages"
          class="page-btn"
        >
          Selanjutnya →
        </button>
      </div>
    </div>

    <!-- Modals -->
    <PakaianModal 
      :visible="isModalVisible"
      :editData="editingItem"
      @close="closeModal"
      @save="handleSavePakaian"
    />

    <ConfirmDialog
      :visible="showDeleteConfirm"
      :title="deleteTarget ? `Hapus ${deleteTarget.nama_pakaian}?` : 'Hapus Item?'"
      :message="deleteTarget ? `Apakah Anda yakin ingin menghapus pakaian '${deleteTarget.nama_pakaian}'? Tindakan ini tidak dapat dibatalkan.` : 'Apakah Anda yakin?'"
      @confirm="handleDelete"
      @cancel="cancelDelete"
    />

    <!-- Toast Notifications -->
    <Toast
      :visible="toast.visible"
      :message="toast.message"
      :type="toast.type"
      @close="hideToast"
    />
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { usePakaianStore } from '../stores/pakaian'
import PakaianModal from '../components/Modal.vue'
import ConfirmDialog from '../components/ConfirmDialog.vue'
import Toast from '../components/Toast.vue'

export default {
  name: 'Dashboard',
  components: {
    PakaianModal,
    ConfirmDialog,
    Toast
  },
  setup() {
    const pakaianStore = usePakaianStore()
    
    // State
    const isModalVisible = ref(false)
    const editingItem = ref(null)
    const searchQuery = ref('')
    const selectedCategory = ref('')
    const viewMode = ref('grid') // 'grid' or 'list'
    const bulkMode = ref(false)
    const selectedItems = ref(new Set())
    const showDeleteConfirm = ref(false)
    const deleteTarget = ref(null)
    
    // Toast notification
    const toast = reactive({
      visible: false,
      message: '',
      type: 'success' // 'success', 'error', 'warning', 'info'
    })
    
    // Categories for filter
    const categories = ref([
      'Atasan', 'Bawahan', 'Dalam', 'Formal', 'Olahraga', 'Lainnya'
    ])
    
    // Computed
    const visiblePages = computed(() => {
      const total = pakaianStore.totalPages
      const current = pakaianStore.currentPage
      const pages = []
      
      // Always show first page
      if (total > 0) pages.push(1)
      
      // Calculate range around current page
      let start = Math.max(2, current - 2)
      let end = Math.min(total - 1, current + 2)
      
      // Add ellipsis if needed
      if (start > 2) pages.push('...')
      
      // Add pages around current
      for (let i = start; i <= end; i++) {
        if (i !== 1 && i !== total) pages.push(i)
      }
      
      // Add ellipsis if needed
      if (end < total - 1) pages.push('...')
      
      // Always show last page if more than 1 page
      if (total > 1) pages.push(total)
      
      return pages
    })
    
    // Methods
    const showToast = (message, type = 'success') => {
      toast.message = message
      toast.type = type
      toast.visible = true
      
      setTimeout(() => {
        toast.visible = false
      }, 3000)
    }
    
    const hideToast = () => {
      toast.visible = false
    }
    
    const openAddModal = () => {
      editingItem.value = null
      isModalVisible.value = true
    }
    
    const openEditModal = (pakaian) => {
      editingItem.value = pakaian
      isModalVisible.value = true
    }
    
    const closeModal = () => {
      isModalVisible.value = false
      editingItem.value = null
    }
    
    const handleSavePakaian = async () => {
      await pakaianStore.fetchPakaian()
      showToast(editingItem.value ? 'Pakaian berhasil diupdate!' : 'Pakaian berhasil ditambahkan!')
    }
    
    const handleSearch = () => {
      pakaianStore.setSearchQuery(searchQuery.value)
    }
    
    const handleCategoryFilter = () => {
      pakaianStore.setSelectedCategory(selectedCategory.value)
    }
    
    const goToPage = (page) => {
      if (page >= 1 && page <= pakaianStore.totalPages) {
        pakaianStore.setCurrentPage(page)
      }
    }
    
    const toggleBulkMode = () => {
      bulkMode.value = !bulkMode.value
      selectedItems.value.clear()
    }
    
    const toggleItemSelection = (id) => {
      if (selectedItems.value.has(id)) {
        selectedItems.value.delete(id)
      } else {
        selectedItems.value.add(id)
      }
    }
    
    const toggleSelectAll = () => {
      if (selectedItems.value.size === pakaianStore.paginatedItems.length) {
        selectedItems.value.clear()
      } else {
        selectedItems.value.clear()
        pakaianStore.paginatedItems.forEach(item => {
          selectedItems.value.add(item.id)
        })
      }
    }
    
    const handleCardClick = (pakaian) => {
      if (bulkMode.value) {
        toggleItemSelection(pakaian.id)
      } else {
        openEditModal(pakaian)
      }
    }
    
    const confirmDelete = (pakaian) => {
      deleteTarget.value = pakaian
      showDeleteConfirm.value = true
    }
    
    const cancelDelete = () => {
      showDeleteConfirm.value = false
      deleteTarget.value = null
    }
    
    const handleDelete = async () => {
      if (deleteTarget.value) {
        try {
          await pakaianStore.deletePakaian(deleteTarget.value.id)
          showToast(`Pakaian '${deleteTarget.value.nama_pakaian}' berhasil dihapus!`)
        } catch (error) {
          showToast('Gagal menghapus pakaian!', 'error')
        }
      }
      showDeleteConfirm.value = false
      deleteTarget.value = null
    }
    
    const bulkDelete = async () => {
      if (selectedItems.value.size === 0) return
      
      try {
        const results = await pakaianStore.bulkDelete([...selectedItems.value])
        const successful = results.filter(r => r.success).length
        const failed = results.filter(r => !r.success).length
        
        if (failed === 0) {
          showToast(`${successful} pakaian berhasil dihapus!`)
        } else {
          showToast(`${successful} pakaian berhasil dihapus, ${failed} gagal!`, 'warning')
        }
        
        selectedItems.value.clear()
        bulkMode.value = false
      } catch (error) {
        showToast('Gagal menghapus pakaian!', 'error')
      }
    }
    
    // Lifecycle
    onMounted(async () => {
      await pakaianStore.fetchPakaian()
    })
    
    // Watch for store changes
    watch(() => pakaianStore.searchQuery, (newQuery) => {
      searchQuery.value = newQuery
    })
    
    watch(() => pakaianStore.selectedCategory, (newCategory) => {
      selectedCategory.value = newCategory
    })
    
    return {
      // Store
      pakaianStore,
      
      // State
      isModalVisible,
      editingItem,
      searchQuery,
      selectedCategory,
      viewMode,
      bulkMode,
      selectedItems,
      showDeleteConfirm,
      deleteTarget,
      toast,
      categories,
      
      // Computed
      visiblePages,
      
      // Methods
      showToast,
      hideToast,
      openAddModal,
      openEditModal,
      closeModal,
      handleSavePakaian,
      handleSearch,
      handleCategoryFilter,
      goToPage,
      toggleBulkMode,
      toggleItemSelection,
      toggleSelectAll,
      handleCardClick,
      confirmDelete,
      cancelDelete,
      handleDelete,
      bulkDelete,
      getImageUrl
    }
  }
}
</script>

<style scoped>
.dashboard {
  padding: 1.5rem;
  max-width: 1400px;
  margin: 0 auto;
}

.dashboard-header {
  margin-bottom: 2rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.stat-card {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  display: flex;
  align-items: center;
  gap: 1rem;
}

.stat-icon {
  font-size: 2rem;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f3f4f6;
  border-radius: 12px;
}

.stat-number {
  font-size: 1.875rem;
  font-weight: 700;
  color: #111827;
}

.stat-label {
  color: #6b7280;
  font-size: 0.875rem;
}

.controls-section {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  margin-bottom: 2rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.search-section {
  display: flex;
  gap: 1rem;
  align-items: center;
  flex-wrap: wrap;
}

.search-box {
  display: flex;
  flex: 1;
  min-width: 300px;
  position: relative;
}

.search-input {
  flex: 1;
  padding: 0.75rem 1rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 0.875rem;
}

.search-btn {
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #6b7280;
  cursor: pointer;
  padding: 4px;
}

.category-filter {
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 0.875rem;
  min-width: 150px;
}

.action-section {
  display: flex;
  gap: 1rem;
  align-items: center;
  flex-wrap: wrap;
}

.btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  border: none;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary {
  background: #3b82f6;
  color: white;
}

.btn-primary:hover {
  background: #2563eb;
}

.btn-secondary {
  background: #f3f4f6;
  color: #374151;
}

.btn-secondary:hover {
  background: #e5e7eb;
}

.btn-secondary.active {
  background: #dbeafe;
  color: #2563eb;
}

.btn-danger {
  background: #dc2626;
  color: white;
}

.btn-danger:hover {
  background: #b91c1c;
}

.view-toggle {
  display: flex;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  overflow: hidden;
}

.view-btn {
  padding: 0.5rem;
  background: white;
  border: none;
  cursor: pointer;
  color: #6b7280;
  transition: all 0.2s;
}

.view-btn.active {
  background: #3b82f6;
  color: white;
}

.bulk-actions {
  background: #fef3c7;
  border: 1px solid #f59e0b;
  padding: 1rem 1.5rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.bulk-info {
  font-weight: 500;
  color: #92400e;
}

.bulk-buttons {
  display: flex;
  gap: 0.5rem;
}

.loading-state {
  text-align: center;
  padding: 4rem 2rem;
  color: #6b7280;
}

.spinner {
  width: 2rem;
  height: 2rem;
  border: 3px solid #f3f4f6;
  border-top: 3px solid #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 1rem;
}

.empty-state {
  text-align: center;
  padding: 4rem 2rem;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.empty-state h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #111827;
  margin-bottom: 0.5rem;
}

.empty-state p {
  color: #6b7280;
  margin-bottom: 2rem;
}

.content-area {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  overflow: hidden;
}

.pakaian-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  padding: 1.5rem;
}

.pakaian-card {
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.2s;
  cursor: pointer;
  position: relative;
}

.pakaian-card:hover {
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.pakaian-card.selected {
  border-color: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
}

.bulk-checkbox {
  position: absolute;
  top: 0.75rem;
  left: 0.75rem;
  z-index: 2;
}

.card-image {
  height: 200px;
  overflow: hidden;
  background: #f9fafb;
  display: flex;
  align-items: center;
  justify-content: center;
}

.clothing-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.no-image {
  text-align: center;
  color: #9ca3af;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.card-content {
  padding: 1rem;
}

.card-header {
  margin-bottom: 1rem;
}

.card-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #111827;
  margin-bottom: 0.25rem;
}

.card-category {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  background: #dbeafe;
  color: #1e40af;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
}

.card-details {
  margin-bottom: 1rem;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.25rem;
  font-size: 0.875rem;
}

.detail-label {
  color: #6b7280;
}

.detail-value {
  color: #111827;
  font-weight: 500;
}

.warning-badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  background: #fef3c7;
  color: #92400e;
  border-radius: 4px;
  font-size: 0.75rem;
  margin-top: 0.5rem;
}

.card-actions {
  display: flex;
  gap: 0.5rem;
  justify-content: flex-end;
}

.action-btn {
  padding: 0.5rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
}

.edit-btn {
  background: #dbeafe;
  color: #1e40af;
}

.edit-btn:hover {
  background: #bfdbfe;
}

.delete-btn {
  background: #fecaca;
  color: #dc2626;
}

.delete-btn:hover {
  background: #fca5a5;
}

/* List View Styles */
.pakaian-list {
  width: 100%;
}

.list-header,
.list-row {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr 1fr 1fr 120px;
  gap: 1rem;
  align-items: center;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #e5e7eb;
}

.list-header {
  background: #f9fafb;
  font-weight: 600;
  color: #374151;
  font-size: 0.875rem;
}

.list-row:hover {
  background: #f9fafb;
}

.list-row.selected {
  background: #eff6ff;
}

.item-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.list-img {
  width: 40px;
  height: 40px;
  border-radius: 6px;
  object-fit: cover;
}

.list-no-img {
  width: 40px;
  height: 40px;
  background: #f3f4f6;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
}

.item-name {
  font-weight: 500;
}

.category-badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  background: #e5e7eb;
  color: #374151;
  border-radius: 4px;
  font-size: 0.75rem;
}

.ok-badge {
  color: #059669;
  font-size: 0.75rem;
}

.list-actions {
  display: flex;
  gap: 0.5rem;
}

/* Pagination */
.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 1.5rem;
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

.page-numbers {
  display: flex;
  gap: 0.25rem;
}

.page-number {
  width: 40px;
  height: 40px;
  border: 1px solid #d1d5db;
  background: white;
  color: #374151;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.875rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.page-number:hover {
  background: #f3f4f6;
}

.page-number.active {
  background: #3b82f6;
  color: white;
  border-color: #3b82f6;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .dashboard {
    padding: 1rem;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .controls-section {
    padding: 1rem;
  }
  
  .search-section {
    flex-direction: column;
    align-items: stretch;
  }
  
  .search-box {
    min-width: auto;
  }
  
  .action-section {
    justify-content: center;
  }
  
  .pakaian-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
    padding: 1rem;
  }
  
  .list-header,
  .list-row {
    grid-template-columns: 1fr;
    gap: 0.5rem;
  }
  
  .list-col {
    padding: 0.25rem 0;
  }
  
  .bulk-actions {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
}
</style>
