<template>
  <div
    class="modal-overlay"
    v-if="visible"
    @click="handleOverlayClick"
  >
    <div class="modal-container" @click.stop>
      <div class="modal-header">
        <h2 class="modal-title">{{ isEdit ? 'Edit Pakaian' : 'Tambah Pakaian Baru' }}</h2>
        <button class="modal-close" @click="$emit('close')">&times;</button>
      </div>

      <div class="modal-body">
        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>

        <div v-if="successMessage" class="success-message">
          {{ successMessage }}
        </div>

        <form @submit.prevent="handleSubmit" class="pakaian-form">
          <div class="form-group">
            <label for="nama_pakaian" class="form-label">
              Nama Pakaian <span class="required">*</span>
            </label>
            <input
              type="text"
              id="nama_pakaian"
              v-model="formData.nama_pakaian"
              class="form-input"
              :class="{ 'error': errors.nama_pakaian }"
              placeholder="Contoh: Kemeja Flanel"
              required
            >
            <span v-if="errors.nama_pakaian" class="error-text">{{ errors.nama_pakaian }}</span>
          </div>

          <div class="form-group">
            <label for="kategori" class="form-label">
              Kategori <span class="required">*</span>
            </label>
            <select
              id="kategori"
              v-model="formData.kategori"
              class="form-select"
              :class="{ 'error': errors.kategori }"
              @change="updateJenisPakaian"
              required
            >
              <option value="">-- Pilih Kategori --</option>
              <option v-for="cat in categories" :key="cat" :value="cat">
                {{ cat }}
              </option>
            </select>
            <span v-if="errors.kategori" class="error-text">{{ errors.kategori }}</span>
          </div>

          <div class="form-group">
            <label for="jenis_pakaian" class="form-label">Jenis Pakaian</label>
            <select
              id="jenis_pakaian"
              v-model="formData.jenis_pakaian"
              class="form-select"
              :disabled="!formData.kategori"
            >
              <option value="">-- Pilih Jenis --</option>
              <option
                v-for="jenis in availableJenisPakaian"
                :key="jenis"
                :value="jenis"
              >
                {{ jenis }}
              </option>
            </select>
          </div>

          <div class="form-group">
            <label for="warna" class="form-label">Warna</label>
            <select id="warna" v-model="formData.warna" class="form-select">
              <option value="">-- Pilih Warna --</option>
              <option v-for="color in colors" :key="color" :value="color">
                {{ color }}
              </option>
            </select>
          </div>

          <div class="form-group">
            <label for="bahan" class="form-label">Bahan</label>
            <select id="bahan" v-model="formData.bahan" class="form-select">
              <option value="">-- Pilih Bahan --</option>
              <option v-for="material in materials" :key="material" :value="material">
                {{ material }}
              </option>
            </select>
          </div>

          <div class="form-group">
            <label for="petunjuk_pencucian" class="form-label">Petunjuk Pencucian</label>
            <textarea
              id="petunjuk_pencucian"
              v-model="formData.petunjuk_pencucian"
              class="form-textarea"
              placeholder="Contoh: Cuci dengan air dingin, jangan diperas, hindari pemutih"
              rows="3"
            ></textarea>
          </div>

          <div class="form-group checkbox-group">
            <label class="checkbox-label">
              <input
                type="checkbox"
                v-model="formData.mudah_luntur"
                class="form-checkbox"
              >
              <span class="checkbox-text">Pakaian mudah luntur</span>
            </label>
          </div>

          <div class="form-group">
            <label for="foto" class="form-label">Foto Pakaian</label>
            <input
              type="file"
              id="foto"
              @change="handleImageUpload"
              accept="image/*"
              class="form-file"
              ref="fileInputRef" >
            <div v-if="imagePreview" class="image-preview">
              <img :src="imagePreview" alt="Preview" class="preview-img">
            </div>
          </div>

          <div class="form-actions">
            <button type="button" @click="$emit('close')" class="btn btn-secondary">
              Batal
            </button>
            <button
              type="submit"
              class="btn btn-primary"
              :disabled="isSubmitting"
            >
              <span v-if="isSubmitting" class="spinner"></span>
              {{ isSubmitting ? 'Menyimpan...' : (isEdit ? 'Update' : 'Simpan') }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, computed, watch } from 'vue'
import { usePakaianStore } from '../stores/pakaian'

export default {
  name: 'PakaianModal',
  emits: ['close', 'save'],
  props: {
    visible: {
      type: Boolean,
      default: false
    },
    editData: {
      type: Object,
      default: null
    }
  },
  setup(props, { emit }) {
    const pakaianStore = usePakaianStore()

    // State
    const isSubmitting = ref(false)
    const errorMessage = ref('')
    const successMessage = ref('')
    const imageFile = ref(null)      // Untuk menyimpan File object
    const imagePreview = ref('')    // Untuk menyimpan URL preview (bisa path asli atau blob)
    const fileInputRef = ref(null) // Ref untuk input file

    // Form data
    const formData = reactive({
      nama_pakaian: '',
      kategori: '',
      jenis_pakaian: '',
      warna: '',
      bahan: '',
      petunjuk_pencucian: '',
      mudah_luntur: false,
      foto_url: '' // Ini akan tetap berisi path asli jika mode edit
    })

    // Validation errors
    const errors = reactive({
      nama_pakaian: '',
      kategori: ''
    })

    // Options
    const categories = ref([
      'Atasan', 'Bawahan', 'Dalam', 'Formal', 'Olahraga', 'Lainnya'
    ])

    const clothingTypes = ref({
      'Atasan': ['Kemeja', 'T-Shirt', 'Blouse', 'Jacket', 'Sweater', 'Hoodie', 'Tank Top'],
      'Bawahan': ['Celana', 'Rok', 'Jeans', 'Celana Pendek', 'Legging', 'Chino'],
      'Dalam': ['Bra', 'Celana Dalam', 'Kaos Dalam', 'Singlet'],
      'Formal': ['Jas', 'Dress', 'Kemeja Formal', 'Celana Formal', 'Blazer'],
      'Olahraga': ['Jersey', 'Celana Olahraga', 'Sepatu Olahraga', 'Jaket Olahraga'],
      'Lainnya': ['Handuk', 'Sprei', 'Sarung Bantal', 'Selimut', 'Karpet']
    })

    const materials = ref([
      'Katun', 'Polyester', 'Sutra', 'Wol', 'Linen', 'Denim',
      'Spandex', 'Rayon', 'Nylon', 'Campuran'
    ])

    const colors = ref([
      'Putih', 'Hitam', 'Abu-abu', 'Merah', 'Biru', 'Hijau',
      'Kuning', 'Orange', 'Ungu', 'Pink', 'Coklat', 'Cream', 'Navy'
    ])

    // Computed
    const isEdit = computed(() => !!props.editData)

    const availableJenisPakaian = computed(() => {
      return formData.kategori ? clothingTypes.value[formData.kategori] || [] : []
    })

    // Methods
    // Fungsi untuk cleanup Object URL
    const revokePreviewUrl = () => {
      if (imagePreview.value && imagePreview.value.startsWith('blob:')) {
        URL.revokeObjectURL(imagePreview.value);
      }
    }

    const resetForm = () => {
      Object.keys(formData).forEach(key => {
        if (key === 'mudah_luntur') formData[key] = false;
        else if (key !== 'foto_url') formData[key] = ''; // Jangan reset foto_url di sini
        else formData[key] = ''; // Reset foto_url hanya jika bukan edit
      })
      Object.keys(errors).forEach(key => { errors[key] = '' })
      errorMessage.value = ''
      successMessage.value = ''

      revokePreviewUrl(); // Hapus URL blob lama
      imageFile.value = null; // Reset file yg dipilih
      imagePreview.value = ''; // Reset tampilan preview
      if (fileInputRef.value) {
          fileInputRef.value.value = null; // Reset input file HTML
      }
    }

    const populateForm = () => {
      resetForm(); // Mulai dengan reset
      if (props.editData) {
        Object.keys(formData).forEach(key => {
          if (props.editData[key] !== undefined) {
            formData[key] = props.editData[key]
          }
        })
        // Set preview ke URL asli jika ada
        if (props.editData.foto_url) {
          // Asumsi foto_url dari editData sudah dinormalisasi (full URL) oleh komponen parent
          imagePreview.value = props.editData.foto_url
        } else {
          imagePreview.value = '' // Pastikan kosong jika tidak ada URL asli
        }
        imageFile.value = null // Belum ada file BARU yg dipilih saat populate
      }
    }

    const validateForm = () => {
      let isValid = true

      // Reset errors
      Object.keys(errors).forEach(key => {
        errors[key] = ''
      })

      // Validate nama_pakaian
      if (!formData.nama_pakaian.trim()) {
        errors.nama_pakaian = 'Nama pakaian wajib diisi'
        isValid = false
      } else if (formData.nama_pakaian.length < 2) {
        errors.nama_pakaian = 'Nama pakaian minimal 2 karakter'
        isValid = false
      }

      // Validate kategori
      if (!formData.kategori) {
        errors.kategori = 'Kategori wajib dipilih'
        isValid = false
      }

      return isValid
    }

    const handleImageUpload = (event) => {
      errorMessage.value = '';
      const file = event.target.files[0]; // Ambil file pertama
      const MAX_SIZE_MB = 5;
      const MAX_SIZE_BYTES = MAX_SIZE_MB * 1024 * 1024;

      // 1. Bersihkan preview lama & file lama jika ada file baru atau user batal
      revokePreviewUrl();
      imageFile.value = null; // Anggap batal dulu

      // Jika user klik cancel (tidak pilih file)
      if (!file) {
        // Jika mode edit, kembalikan preview ke gambar asli
        if (isEdit.value && props.editData?.foto_url) {
          imagePreview.value = props.editData.foto_url;
        } else {
          imagePreview.value = ''; // Kosongkan preview jika mode tambah
        }
        // Jangan reset file input value di sini, biarkan user bisa klik lagi
        return; // Selesai
      }

      // --- Ada file dipilih ---

      // 2. Validasi Tipe
      const allowedTypes = ['image/jpeg', 'image/png', 'image/gif'];
      if (!allowedTypes.includes(file.type)) {
        errorMessage.value = 'Format file tidak valid. Gunakan JPEG, PNG, atau GIF';
        imagePreview.value = ''; // Kosongkan preview jika error
        if (fileInputRef.value) fileInputRef.value.value = null; // Reset input agar bisa pilih file yg sama
        return;
      }

      // 3. Validasi Ukuran
      if (file.size > MAX_SIZE_BYTES) {
        errorMessage.value = `Ukuran file terlalu besar. Maksimal ${MAX_SIZE_MB}MB`;
        imagePreview.value = ''; // Kosongkan preview jika error
        if (fileInputRef.value) fileInputRef.value.value = null; // Reset input agar bisa pilih file yg sama
        return;
      }

      // --- File Valid ---

      // 4. Simpan File Object untuk di-upload nanti
      imageFile.value = file;

      // 5. Buat dan tampilkan URL preview (Blob URL)
      imagePreview.value = URL.createObjectURL(file);

      // 6. Hapus pesan error jika lolos semua
      errorMessage.value = '';
    }

    const updateJenisPakaian = () => {
      formData.jenis_pakaian = ''
    }

    const handleSubmit = async () => {
      if (!validateForm()) return

      isSubmitting.value = true
      errorMessage.value = ''
      successMessage.value = ''

      try {
        // Salin formData. JANGAN kirim foto_url jika isinya blob
        // Biarkan backend yg urus jika tidak ada file baru di mode edit
        const submitData = { ...formData };
        if (imagePreview.value && imagePreview.value.startsWith('blob:')) {
           // Hapus blob URL dari data yg dikirim untuk update info,
           // karena backend butuh path asli atau tidak sama sekali
           // Jika imageFile ada isinya, backend akan tahu ada upload baru.
          delete submitData.foto_url;
        }


        if (isEdit.value) {
          // Update data teks dulu
          await pakaianStore.updatePakaian(props.editData.id, submitData)

          // Upload gambar HANYA jika ada file BARU yg dipilih
          if (imageFile.value) { // imageFile hanya berisi file jika user memilih yg baru
            console.log("Mengupload gambar baru untuk edit...");
            await pakaianStore.uploadImage(props.editData.id, imageFile.value) // Kirim File object
          } else {
            console.log("Tidak ada gambar baru untuk diupload.");
          }

          successMessage.value = 'Pakaian berhasil diupdate!'
        } else {
          // Tambah data teks dulu
          const newPakaian = await pakaianStore.addPakaian(submitData)

          // Upload gambar jika ada file yg dipilih dan ID Pakaian baru ada
          if (imageFile.value && newPakaian?.id) {
             console.log("Mengupload gambar untuk pakaian baru...");
            await pakaianStore.uploadImage(newPakaian.id, imageFile.value) // Kirim File object
          }

          successMessage.value = 'Pakaian berhasil ditambahkan!'
          resetForm() // Reset setelah berhasil tambah
        }

        emit('save') // Beritahu parent bahwa ada perubahan

        setTimeout(() => {
          emit('close')
        }, 1500)

      } catch (error) {
        console.error('Error saving pakaian:', error)
        // Coba ambil detail error dari response, jika tidak ada pakai pesan default
        let detailError = 'Terjadi kesalahan saat menyimpan data';
        if (error.response && error.response.data && error.response.data.detail) {
          // Jika detail berupa array (umumnya dari Pydantic validation error)
          if (Array.isArray(error.response.data.detail)) {
            detailError = error.response.data.detail.map(err => `${err.loc.join('.')}: ${err.msg}`).join('; ');
          }
          // Jika detail berupa string
          else if (typeof error.response.data.detail === 'string') {
            detailError = error.response.data.detail;
          }
        } else if (error.message) {
          detailError = error.message;
        }
        errorMessage.value = detailError;
      } finally {
        isSubmitting.value = false
      }
    }

    const handleOverlayClick = () => {
      emit('close')
    }

    // Watchers
    watch(() => props.visible, (newVal) => {
      errorMessage.value = '' // Selalu reset error message saat modal muncul/hilang
      successMessage.value = '' // Selalu reset success message
      if (newVal) {
        if (props.editData) {
          populateForm()
        } else {
          resetForm()
        }
      } else {
        // Cleanup saat modal ditutup (terutama jika ditutup paksa tanpa save/cancel button)
        revokePreviewUrl();
        imageFile.value = null; // Pastikan file direset
        // Reset input file value saat modal ditutup,
        // agar jika dibuka lagi dan pilih file yg sama, event change tetap ter-trigger
        if (fileInputRef.value) {
            fileInputRef.value.value = null;
        }
      }
    })

    return {
      // State
      isSubmitting,
      errorMessage,
      successMessage,
      imagePreview,
      formData,
      errors,
      fileInputRef, // Expose ref

      // Options
      categories,
      materials,
      colors,

      // Computed
      isEdit,
      availableJenisPakaian,

      // Methods
      handleSubmit,
      handleImageUpload,
      updateJenisPakaian,
      handleOverlayClick,
    }
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
  max-width: 600px;
  width: 100%;
  max-height: 90vh;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.modal-header {
  padding: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #f9fafb;
}

.modal-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #111827;
  margin: 0;
}

.modal-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #6b7280;
  padding: 0.25rem;
  line-height: 1;
  border-radius: 4px;
}

.modal-close:hover {
  background-color: #f3f4f6;
  color: #374151;
}

.modal-body {
  padding: 1.5rem;
  overflow-y: auto;
  flex: 1;
}

.error-message {
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #dc2626;
  padding: 0.75rem;
  border-radius: 6px;
  margin-bottom: 1rem;
  font-size: 0.875rem;
}

.success-message {
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
  color: #16a34a;
  padding: 0.75rem;
  border-radius: 6px;
  margin-bottom: 1rem;
  font-size: 0.875rem;
}

.pakaian-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-label {
  font-weight: 500;
  margin-bottom: 0.5rem;
  color: #374151;
  font-size: 0.875rem;
}

.required {
  color: #dc2626;
}

.form-input,
.form-select,
.form-textarea {
  border: 1px solid #d1d5db;
  border-radius: 6px;
  padding: 0.75rem;
  font-size: 0.875rem;
  transition: border-color 0.15s ease;
}

.form-input:focus,
.form-select:focus,
.form-textarea:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.form-input.error,
.form-select.error {
  border-color: #dc2626;
}

.form-textarea {
  resize: vertical;
  min-height: 80px;
}

.error-text {
  color: #dc2626;
  font-size: 0.75rem;
  margin-top: 0.25rem;
}

.checkbox-group {
  flex-direction: row;
  align-items: center;
}

.checkbox-label {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.form-checkbox {
  margin-right: 0.5rem;
}

.form-file {
  border: 1px solid #d1d5db;
  border-radius: 6px;
  padding: 0.5rem;
  font-size: 0.875rem;
}

/* Style for native file input */
input[type="file"]::file-selector-button {
  margin-right: 0.5rem;
  border: none;
  background: #e5e7eb;
  padding: 0.5rem 0.75rem;
  border-radius: 4px;
  color: #374151;
  cursor: pointer;
  transition: background-color 0.15s ease;
}

input[type="file"]::file-selector-button:hover {
  background: #d1d5db;
}

.image-preview {
  margin-top: 1rem; /* Beri jarak lebih */
}

.preview-img {
  max-width: 150px;
  max-height: 150px;
  border-radius: 6px;
  object-fit: cover;
  border: 1px solid #e5e7eb; /* Tambah border tipis */
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 1.5rem;
}

.btn {
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  border: none;
  font-size: 0.875rem;
  display: flex;
  align-items: center;
  justify-content: center; /* Pusatkan konten tombol */
  gap: 0.5rem;
  transition: all 0.15s ease;
}

.btn-secondary {
  background: #f3f4f6;
  color: #374151;
}

.btn-secondary:hover {
  background: #e5e7eb;
}

.btn-primary {
  background: #3b82f6;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #2563eb;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.spinner {
  width: 1rem;
  height: 1rem;
  border: 2px solid transparent;
  border-top: 2px solid currentColor;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@media (max-width: 640px) {
  .modal-container {
    max-width: calc(100vw - 2rem);
    margin: 1rem;
  }

  .modal-header,
  .modal-body {
    padding: 1rem;
  }

  .form-actions {
    flex-direction: column;
  }

  .btn {
    width: 100%; /* Buat tombol full width di mobile */
  }
}
</style>