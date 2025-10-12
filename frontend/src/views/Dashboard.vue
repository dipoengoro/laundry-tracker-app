<template>
  <div class="min-h-screen bg-gray-100">
    <nav class="bg-white shadow-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center">
            <h1 class="text-xl font-semibold text-gray-900">🧺 Laundry Tracker</h1>
          </div>
          <div class="flex items-center space-x-4">
            <span v-if="user" class="text-sm text-gray-700">Welcome, <span class="font-medium">{{ user.username || user.email }}</span></span>
            <button @click="handleLogout" :disabled="authStore.isLoading" class="bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700 disabled:opacity-50">
              {{ authStore.isLoading ? 'Logging out...' : 'Logout' }}
            </button>
          </div>
        </div>
      </div>
    </nav>

    <main class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div class="px-4 py-6 sm:px-0">
        <div class="flex justify-between items-center mb-6">
          <h2 class="text-2xl font-bold text-gray-800">Katalog Pakaian Saya</h2>
          <button @click="isModalOpen = true" class="bg-blue-600 text-white px-4 py-2 rounded-md shadow-sm hover:bg-blue-700">
            + Tambah Pakaian
          </button>
        </div>

        <div v-if="pakaianStore.isLoading" class="text-center py-10">
          <p class="text-gray-500">Memuat data pakaian...</p>
        </div>

        <div v-else-if="pakaianItems.length === 0" class="text-center bg-white p-12 rounded-lg shadow">
          <h3 class="text-xl font-medium text-gray-900">Katalog Kosong</h3>
          <p class="mt-2 text-gray-500">Kamu belum punya pakaian di katalogmu. Tambahkan sekarang!</p>
        </div>

        <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
          <PakaianCard v-for="item in pakaianItems" :key="item.id" :pakaian="item" />
        </div>
      </div>
    </main>

    <Modal :show="isModalOpen" title="Tambah Pakaian Baru" @close="isModalOpen = false">
      <PakaianForm @cancel="isModalOpen = false" @submit="handlePakaianSubmit" />
    </Modal>
  </div>

</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from "vue-router";
import { useAuthStore } from "../stores/auth";
import { usePakaianStore } from '../stores/pakaian';
import PakaianCard from '../components/PakaianCard.vue';
import PakaianForm from '../components/PakaianForm.vue';
import Modal from '../components/Modal.vue';

const router = useRouter();
const authStore = useAuthStore();
const pakaianStore = usePakaianStore();

const isModalOpen = ref(false);

const user = computed(() => authStore.user);
const pakaianItems = computed(() => pakaianStore.items);

const handlePakaianSubmit = async (formData) => {
  await pakaianStore.addPakaian(formData);
  isModalOpen.value = false;
}

onMounted(() => {
  if (authStore.isAuthenticated) {
    pakaianStore.fetchPakaian();
  }
});

const handleLogout = async () => {
  await authStore.logout();
  console.log("[Dashboard] 🚪 Logged out, redirecting...");
  router.push("/login");
};
</script>