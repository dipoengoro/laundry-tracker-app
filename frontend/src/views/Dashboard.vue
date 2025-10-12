<template>
  <div class="p-4 sm:p-6 md:p-8">
    <header class="flex items-center justify-between pb-4 border-b border-gray-200">
      <div>
        <h1 class="text-2xl font-bold text-gray-800">
          Welcome, {{ authStore.user?.username || 'User' }}!
        </h1>
        <p class="text-gray-500">
          Yuk, atur koleksi pakaianmu di Laundry Tracker.
        </p>
      </div>
      <button 
        @click="handleLogout" 
        class="px-4 py-2 text-sm font-medium text-red-600 bg-red-100 rounded-lg hover:bg-red-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
      >
        Logout
      </button>
    </header>

    <main class="mt-6">
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-xl font-semibold text-gray-700">Katalog Pakaian Saya</h2>
        
        <button 
          @click="openModal"
          class="px-5 py-2.5 font-medium text-white bg-blue-700 rounded-lg hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300"
        >
          + Tambah Pakaian
        </button>
      </div>

      <div v-if="pakaianList.length > 0" class="grid grid-cols-2 gap-4 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5">
        <PakaianCard  v-for="item in pakaianList" :key="item.id" :pakaian="item" />
      </div>
      <div v-else class="py-10 text-center text-gray-500 bg-gray-50 rounded-lg">
        <p>Kamu belum punya pakaian nih. Yuk, tambahkan sekarang!</p>
      </div>
    </main>

    <Modal
      v-if="isModalVisible"
      @close="closeModal"
      @submit="handleSavePakaian"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import { usePakaianStore } from '../stores/pakaian';
import api from '../api';

// Import komponen Modal
import Modal from '../components/Modal.vue';
import PakaianCard from '../components/PakaianCard.vue';

// Inisialisasi store dan router
const authStore = useAuthStore();
const pakaianStore = usePakaianStore()
const router = useRouter();

// === STATE MANAGEMENT UNTUK DASHBOARD ===

// 1. State untuk menyimpan daftar pakaian
const pakaianList = computed(() => pakaianStore.items)

// 2. State baru untuk mengontrol visibilitas modal
const isModalVisible = ref(false);


// === FUNGSI-FUNGSI ===

// Fungsi untuk mengambil data pakaian dari API
const fetchPakaian = async () => {
  try {
    if (authStore.isAuthenticated) {
      pakaianStore.fetchPakaian();
    }
  } catch (error) {
    console.error('Gagal fetch data pakaian:', error);
    // Mungkin bisa ditambahkan notifikasi error untuk user di sini
  }
};

// Fungsi untuk logout
const handleLogout = () => {
  authStore.logout();
  router.push('/login');
};

// 3. Fungsi baru untuk membuka modal
const openModal = () => {
  isModalVisible.value = true;
};

// 4. Fungsi baru untuk menutup modal
const closeModal = () => {
  isModalVisible.value = false;
};

// 5. Fungsi baru untuk menangani penyimpanan data dari modal
const handleSavePakaian = async (formData) => {
  try {
    // Kirim data baru ke backend
    await api.post('/pakaian', {
      nama: formData.nama,
      kategori: formData.kategori,
      // gambar_url bisa ditambahkan di sini jika ada
    });

    // Jika berhasil, panggil ulang fetchPakaian untuk refresh data
    await fetchPakaian();

    // Terakhir, tutup modalnya
    closeModal();
    
  } catch (error) {
    console.error('Gagal menyimpan pakaian baru:', error);
    // Di sini kamu bisa mengirim pesan error kembali ke modal jika mau
    // atau menampilkan notifikasi error global.
  }
};


// === LIFECYCLE HOOK ===

// Panggil fetchPakaian saat komponen pertama kali di-mount
onMounted(fetchPakaian);
</script>