import axios from "axios";

const MEDICAL_HUB_API_URL = `${import.meta.env.VITE_API_URL}/medical_hub/`;

const medical_hub_Api = axios.create({
  baseURL: MEDICAL_HUB_API_URL,
})

medical_hub_Api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

export const getHospitals = async (params = {}) => {
  return await medical_hub_Api.get('hospitals/', {params})
}