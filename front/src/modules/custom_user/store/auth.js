// @/modules/custom_user/store/auth.js
import { defineStore } from 'pinia';
import { login, logout } from '../api/auth';
import axios from 'axios';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null, // Данные пользователя (например, { id, username, role, ... })
    token: null, // Токен авторизации
  }),
  actions: {
    async login(credentials) {
      try {
        const response = await login(credentials);
        this.user = response.data; // Сохраняем данные пользователя
        this.token = response.data.auth_token; // Сохраняем токен
        localStorage.setItem('token', this.token); // Сохраняем токен в localStorage
        // Устанавливаем токен в заголовки axios
        axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`;
        return response;
      } catch (error) {
        throw error;
      }
    },
    async logout() {
      try {
        await logout();
        this.user = null;
        this.token = null;
        localStorage.removeItem('token');
        // Удаляем заголовок Authorization
        delete axios.defaults.headers.common['Authorization'];
      } catch (error) {
        throw error;
      }
    },
    async initializeAuth() {
      const token = localStorage.getItem('token');
      if (token) {
        this.token = token;
        // Устанавливаем токен в заголовки axios
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        // Опционально: загружаем данные пользователя
        try {
          const response = await axios.get('/api/users/me/'); // Предполагаемый эндпоинт для получения данных пользователя
          this.user = response.data;
        } catch (error) {
          console.error('Ошибка при загрузке данных пользователя:', error);
          // Если токен недействителен, выполняем logout
          if (error.response?.status === 401) {
            this.logout();
          }
        }
      }
    },
  },
  getters: {
    isAuthenticated: (state) => !!state.token,
    userRole: (state) => state.user?.role || null,
  },
});