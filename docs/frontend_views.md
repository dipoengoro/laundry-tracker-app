# Dokumentasi Kode Frontend (Vue)

Berbeda dengan backend, kode frontend (Vue) perlu dimasukkan secara manual
ke dalam dokumentasi.

## Tampilan Profil (`ProfileView.vue`)

**Path:** `frontend/src/views/ProfileView.vue`

Tampilan ini digunakan user untuk mengelola data profil mereka,
mengganti foto, dan mengubah password.

```vue
<template>
  <AppLayout>
    <div class="max-w-2xl mx-auto space-y-6">
      <h1 class="text-2xl font-bold text-gray-900">Profil Pengguna</h1>

      <div class="bg-white rounded-lg shadow-md p-6">
        </div>
    </div>

    </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
// ... (Sisa isi <script> kamu) ...
</script>
