<template>
  <header class="header">
    <nav class="nav">
      <div class="nav-links">
        <router-link to="/patients" class="nav-link">Главная</router-link>
        <router-link to="/medications" class="nav-link">Медикаменты</router-link>
        <router-link to="/diseases" class="nav-link">Болезни</router-link>
      </div>
      <button class="logout-btn" @click="handleLogout" :disabled="isLoggingOut">
        {{ isLoggingOut ? 'Выход...' : 'Выход' }}
      </button>
    </nav>
  </header>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores';
import { logout } from 'src/modules/custom_user/api/auth'; // Укажи правильный путь

const router = useRouter();
const authStore = useAuthStore();
const isLoggingOut = ref(false);

const handleLogout = async () => {
  isLoggingOut.value = true;
  try {
    await logout();
    authStore.$reset();
    localStorage.removeItem('token');
    router.push('/login');
  } catch (error) {
    console.error('Ошибка при выходе:', error);
  } finally {
    isLoggingOut.value = false;
  }
};
</script>

<style scoped>
.header {
  background-color: #000;
  position: fixed; /* Фиксируем шапку вверху */
  top: 0; /* Прижимаем к верхнему краю */
  left: 0; /* Прижимаем к левому краю */
  width: 100%; /* Растягиваем на всю ширину */
  margin: 0; /* Убираем все внешние отступы */
  padding: 0; /* Убираем все внутренние отступы */
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  z-index: 1000;
}

.nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px 30px; /* Отступы только внутри nav */
}

.nav-links {
  display: flex;
  gap: 20px;
}

.nav-link {
  text-decoration: none;
  color: #fff;
  font-size: 16px;
  font-weight: 600;
  transition: color 0.3s ease;
}

.nav-link:hover {
  color: #ccc;
}

.logout-btn {
  padding: 10px 20px;
  background-color: #fff;
  color: #000;
  border: none;
  border-radius: 20px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.logout-btn:hover:not(:disabled) {
  background-color: #e0e0e0;
  color: #000;
}

.logout-btn:disabled {
  background-color: #cccccc;
  color: #666;
  cursor: not-allowed;
}
</style>