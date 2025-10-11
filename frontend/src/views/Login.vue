<template>
    <AuthLayout title="Selamat Datang Kembali">
        <form class="mt-8 space-y-6" @submit.prevent="login">
            <div class="rounded-md shadow-sm -space-y-px">
                <div>
                    <label for="email-address" class="sr-only">Email Address</label>
                    <input id="email-address" name="email" type="email" v-model="user.email" required class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm" placeholder="Alamat email">
                </div>
                <div>
                    <label for="password" class="sr-only">Password</label>
                    <input type="password" id="password" name="password" v-model="user.password" required class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm" placeholder="Password">
                </div>
            </div>

            <div>
                <button type="submit" class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                    Login
                </button>
            </div>
        </form>
        <p class="mt-2 text-center text-sm text-gray-600">
            Belum punya akun?
            {{ ' ' }}
            <router-link to="/register" class="font-medium text-blue-600 hover:text-blue-500">
                Daftar di sini
            </router-link>
        </p>
    </AuthLayout>
</template>

<script setup>
import { ref } from "vue";
import AuthLayout from "../components/AuthLayout.vue";
import { useAuthStore } from "../stores/auth";
import { useRouter } from "vue-router";

const user = ref({
    email: '',
    password: '',
});

const authStore = useAuthStore();
const router = useRouter();

async function login() {
    try {
        await authStore.login(user.value);
        router.push({ name: 'Dashboard' });
    } catch (error) {
        alert("Login gagal, periksa kembali email dan password Anda.")
    }
}
</script>