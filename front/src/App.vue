<template>
  <div id="app">
    <Header v-if="authStore.isAuthenticated" />
    <router-view />
  </div>
</template>

<script setup>
import Header from '@/components/Header.vue';
import { useAuthStore } from '@/stores';
const authStore = useAuthStore();
</script>

<style>
#app {
  font-family: Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

:deep(.app-container > *:not(header)) {
  margin-top: 60px; /* Примерная высота шапки (20px padding сверху + 20px снизу + высота текста) */
}
</style>