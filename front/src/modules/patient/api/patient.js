import axios from 'axios';

const API_URL = `${import.meta.env.VITE_API_URL}/patient/`; // Базовый URL для API пациентов

const api = axios.create({
  baseURL: API_URL,
});

// Перехватчик для добавления токена (уже настроен в auth.js, но на всякий случай)
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

// Поиск пациентов по ФИО или СНИЛС
export const searchPatientsBySnilsOrFio = async (params) => {
  return await api.get('patients/search-by-snils-or-fio/', { params });
};

// Поиск пациентов по лицу
export const searchPatientsByFace = async (photo) => {
  const formData = new FormData();
  formData.append('photo', photo);
  return await api.post('patients/search-by-face/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};

// Получение данных пациента по ID
export const getPatientById = async (id) => {
  return await api.get(`/patients/${id}/`); // Используем api, чтобы перехватчик добавлял токен
};

export const updatePatient = async (id, data, photo = null) => {
  const formData = new FormData();

  // Фильтруем данные, отправляем только редактируемые поля
  const editableFields = [
    'first_name',
    'last_name',
    'middle_name',
    'snils',
    'birth_date',
    'gender',
    'registration_address',
    'actual_address',
  ];

  for (const key of editableFields) {
    if (data[key] !== undefined && data[key] !== null) {
      formData.append(key, data[key]);
    }
  }

  // Добавляем фото, если оно есть
  if (photo) {
    formData.append('photo', photo);
  }

  return await api.patch(`/patients/${id}/`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};

export const createPatient_Api = async (data, photo = null) => {
  const formData = new FormData();

  const fields = [
    'first_name',
    'last_name',
    'middle_name',
    'snils',
    'birth_date',
    'gender',
    'registration_address',
    'actual_address',
  ];

  for (const key of fields) {
    if (data[key] !== undefined && data[key] !== null) {
      formData.append(key, data[key]);
    }
  }

  if (photo) {
    formData.append('photo', photo);
  }

  return await api.post('patients/', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};