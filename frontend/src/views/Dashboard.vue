<script setup>
import { useAuthStore } from '../stores/auth';
const authStore = useAuthStore();
</script>

<template>
    <div class="p-8">
        <h1 class="text-3xl font-bold">Selamat Datang di Dashboard!</h1>
        <button @click="authStore.logout()" class="mt-4 bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded">
            Logout
        </button>
    </div>
</template>