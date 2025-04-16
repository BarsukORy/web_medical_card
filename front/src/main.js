import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router';
import axios from 'axios';
import { useAuthStore } from '@/stores';

const app = createApp(App);
const pinia = createPinia();

axios.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('token'); // Удаляем token
      router.push('/login');
    }
    return Promise.reject(error);
  }
);

app.use(pinia);
app.use(router);

const authStore = useAuthStore();
authStore.initializeAuth();

app.mount('#app');