<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center bg-gray-900/60 backdrop-blur-sm" @click="closeModal">
    <div class="relative w-full max-w-md transform rounded-lg bg-white text-left shadow-xl transition-all" @click.stop>
      <div class="flex items-start justify-between rounded-t border-b border-gray-200 p-4">
        <h2 class="text-xl font-semibold text-gray-900">Tambah Pakaian Baru</h2>
        <button type="button" class="ml-auto inline-flex items-center rounded-lg bg-transparent p-1.5 text-sm text-gray-400 hover:bg-gray-200 hover:text-gray-900" @click="closeModal">
          <svg class="h-5 w-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>
        </button>
      </div>
      <form @submit.prevent="handleSubmit">
        <div class="space-y-4 p-6">
          <p v-if="errorMessage" class="rounded-lg bg-red-100 p-3 text-center text-sm text-red-700">{{ errorMessage }}</p>
          <div>
            <label for="namaPakaian" class="mb-2 block text-sm font-medium text-gray-900">Nama Pakaian</label>
            <input type="text" name="namaPakaian" id="namaPakaian" v-model="namaPakaian" class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-blue-500 focus:ring-blue-500" placeholder="Contoh: Kemeja Flanel">
          </div>
          <div>
            <label for="kategori" class="mb-2 block text-sm font-medium text-gray-900">Kategori</label>
            <select id="kategori" v-model="kategori" class="block w-full rounded-lg border border-gray-300 bg-gray-50 p-2.5 text-sm text-gray-900 focus:border-blue-500 focus:ring-blue-500">
              <option value="" disabled>-- Pilih Kategori --</option>
              <option v-for="cat in categories" :key="cat" :value="cat">
                {{ cat.charAt(0).toUpperCase() + cat.slice(1).toLowerCase() }}
              </option>
            </select>
          </div>
        </div>
        <div class="flex items-center space-x-2 rounded-b border-t border-gray-200 bg-gray-50 p-6">
          <button type="submit" :disabled="isLoading" class="rounded-lg bg-blue-700 px-5 py-2.5 text-center text-sm font-medium text-white hover:bg-blue-800 focus:outline-none focus:ring-4 focus:ring-blue-300 disabled:cursor-not-allowed disabled:bg-blue-400">
            {{ isLoading ? 'Menyimpan...' : 'Simpan' }}
          </button>
          <button type="button" @click="closeModal" class="rounded-lg border border-gray-200 bg-white px-5 py-2.5 text-sm font-medium text-gray-500 hover:bg-gray-100 hover:text-gray-900 focus:z-10 focus:outline-none focus:ring-4 focus:ring-gray-200">
            Batal
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const emit = defineEmits(['close', 'submit']);

// --- PERUBAHAN UTAMA ADA DI SINI ---
// 1. Definisikan kategori sesuai enum di backend
const categories = ['ATASAN', 'BAWAHAN', 'DALAMAN', 'AKSESORIS', 'LAINNYA'];

// 2. State untuk form
const namaPakaian = ref('');
const kategori = ref(''); // Default value sekarang string kosong
const isLoading = ref(false);
const errorMessage = ref('');

// --- Sisanya sama persis seperti sebelumnya ---
const logger = {
  info: (message, context) => console.log(`[MODAL_INFO] ${message}`, context || ''),
  error: (message, context) => console.error(`[MODAL_ERROR] ${message}`, context || ''),
};

const closeModal = () => {
  emit('close'); // Ini akan memicu @close di parent
};

const handleSubmit = async () => {
  logger.info('Submit initiated.', { nama: namaPakaian.value, kategori: kategori.value });
  if (!namaPakaian.value.trim() || !kategori.value) {
    const errorMsg = 'Ups, nama pakaian dan kategori wajib diisi ya!';
    logger.error('Validation failed.', { error: errorMsg });
    errorMessage.value = errorMsg;
    return;
  }
  isLoading.value = true;
  errorMessage.value = '';
  try {
    emit('submit', { nama: namaPakaian.value, kategori: kategori.value });
  } catch (err) {
    const errorMsg = 'Yah, gagal menyimpan. Coba lagi nanti ya.';
    logger.error('Submission failed.', { error: err });
    errorMessage.value = errorMsg;
  } finally {
    isLoading.value = false;
  }
};
</script>