import axios from "axios";

const CATALOG_API_URL = `${import.meta.env.VITE_API_URL}/catalog/`;

const catalogApi = axios.create({
  baseURL: CATALOG_API_URL,
});

catalogApi.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

export const getDiseases = async (params = {}) => {
  return await catalogApi.get('diseases/', { params });
};

export const getMedications = async (params = {}) => {
  return await catalogApi.get('medications/', { params });
};