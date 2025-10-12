<template>
    <form @submit.prevent="handleSubmit" class="space-y-4">
        <div>
            <label for="nama_pakaian" class="block text-sm font-medium text-gray-700">Nama Pakaian</label>
            <input type="text" v-model="formData.nama_pakaian" id="nama_pakaian" required class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500">
        </div>
        <div>
            <label for="kategori" class="block text-sm font-medium text-gray-700">Kategori</label>
            <input type="text" v-model="formData.kategori" id="kategori" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-blue-500 focus:border-blue-500">
        </div>
        <div class="flex justify-end pt-4">
            <button type="button" @click="$emit('cancel')" class="bg-gray-200 text-gray-700 px-4 py-2 rounded-md mr-2 hover:bg-gray-300">Batal</button>
            <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700">Simpan</button>
        </div>
    </form>
</template>

<script setup>
import { ref } from 'vue';

const emit = defineEmits(['submit', 'cancel']);

const formData = ref({
    nama_pakaian: '',
    kategori: '',
});

function handleSubmit() {
    emit('submit', formData.value)
}
</script>