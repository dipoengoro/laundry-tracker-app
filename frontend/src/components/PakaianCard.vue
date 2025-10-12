<script setup>
defineProps({
    pakaian: {
        type: Object,
        required:true
    },
});
</script>

<template>
    <div class="bg-white rounded-lg shadow-md overflow-hidden transform hover:-translate-y-1 transition-transform duration-300">
        <div class="h-48 bg-gray-200 flex items-center justify-center">
            <img v-if="pakaian.foto_url" :src="`http://localhost:8000${pakaian.foto_url}`" :alt="pakaian.nama_pakaian" class="w-full h-full object-cover">
            <span v-else class="text-gray-400">Tidak Ada Gambar</span>
        </div>
        <div class="p-4">
            <h3 class="font-bold text-lg truncate" :title="pakaian.nama_pakaian">{{ pakaian.nama_pakaian }}</h3>
            <p class="text-sm text-gray-600">{{ pakaian.kategori || 'Tanpa Kategori' }}</p>
        </div>
    </div>
</template>