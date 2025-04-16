import axios from 'axios';

const API_URL = `${import.meta.env.VITE_API_URL}/medical_card/`;

export const api = axios.create({
  baseURL: API_URL,
  validateStatus: (status) => {
    return status >= 200 && status < 300; // Считаем успешными статусы 200-299, включая 201
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

export const createMedicalCard = async (data) => {
  return await api.post('medical-cards/', data);
};

export const getMedicalCardById = async (id, params = {}) => {
  return await api.get(`medical-cards/${id}/`, { params });
};

export const updateMedicalCard = async (id, data) => {
  return await api.patch(`medical-cards/${id}/`, data);
};

export const getMedicalCardEntryById = async (medicalCardId, entryId) => {
  return await api.get(`medical-cards/${medicalCardId}/entries/${entryId}/`);
};

export const createMedicalCardEntry = async (medicalCardId, data) => {
  return await api.post(`medical-cards/${medicalCardId}/entries/`, data);
};

export const updateMedicalCardEntry = async (medicalCardId, entryId, data) => {
  return await api.patch(`medical-cards/${medicalCardId}/entries/${entryId}/`, data);
};

export const getMedicalCardEntryFiles = async (entryId) => {
  return await api.get(`medical-card-entries/${entryId}/files/`);
};

export const uploadMedicalCardEntryFile = async (entryId, file) => {
  const formData = new FormData();
  formData.append('file', file);
  return await api.post(`medical-card-entries/${entryId}/files/`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};

export const getPrescriptions = async (entryId) => {
  return await api.get(`medical-card-entries/${entryId}/prescriptions/`);
};

export const createPrescription = async (entryId, data) => {
  return await api.post(`medical-card-entries/${entryId}/prescriptions/`, data);
};

export const getPrescriptionMedications = async (prescriptionId) => {
  return await api.get(`prescriptions/${prescriptionId}/medications/`);
};

export const createPrescriptionMedication = async (prescriptionId, data) => {
  return await api.post(`prescriptions/${prescriptionId}/medications/`, data);
};

export const updatePrescriptionMedication = async (prescriptionId, data) => {
  return await api.patch(`prescriptions/${prescriptionId}/medications/`, data);
};

export const deletePrescriptionMedication = async (prescriptionId, data) => {
  return await api.delete(`prescriptions/${prescriptionId}/medications/`, data);
};