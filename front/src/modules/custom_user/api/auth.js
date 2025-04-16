import axios from 'axios';

const API_URL = `${import.meta.env.VITE_API_URL}/auth/auth/`;

// Создаём экземпляр Axios с базовыми настройками
const api = axios.create({
  baseURL: API_URL,
});

// Функция для авторизации
export const login = async (credentials) => {
  return await api.post('login/', credentials);
};

// Функция для выхода
export const logout = async () => {
  const token = localStorage.getItem('token');
  return await api.post('logout/', {}, {
    headers: {
      Authorization: `Token ${token}`,
    },
  });
};

// Настройка перехватчика для добавления токена ко всем запросам
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});