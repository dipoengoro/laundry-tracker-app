<!-- App.vue -->
<script setup>
import { onMounted } from "vue";
import { useAuthStore } from "./stores/auth";

const auth = useAuthStore();

onMounted(() => {
  console.log("[App] 🚀 Initializing app...");
  auth.initializeAuth();
});
</script>

<template>
  <router-view />
</template>
