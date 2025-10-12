<template>
    <div v-if="show" class="fixed inset-0 bg-black bg-opacity-50 z-40 flex items-center justify-center" @click.self="$emit('close')">
        <div class="bg-white rounded-lg shadow-xl max-w-lg w-full p-6 m-4">
            <div class="flex justify-between items-center mb-4">
                <h3 class="text-xl font-semibold">{{ title }}</h3>
                <button @click="$emit('close')" class="text-gray-400 hover:text-gray-600">&times;</button>
            </div>
        </div>
        <div>
            <slot></slot>
        </div>
    </div>
</template>

<script setup>
defineProps({
    show: Boolean,
    title: String,
});
defineEmits(['close']);
</script>