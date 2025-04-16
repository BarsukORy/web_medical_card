<template>
  <div class="diseases-container">
    <div class="diseases-box">
      <h2>Болезни</h2>

      <div v-if="error" class="error">{{ error }}</div>
      <p v-if="loading">Загрузка...</p>

      <div v-if="diseases.length" class="table-wrapper">
        <table class="diseases-table">
          <thead>
            <tr>
              <th>Название</th>
              <th>Описание</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="disease in diseases" :key="disease.id">
              <td>{{ disease.name }}</td>
              <td>{{ disease.description || 'Нет описания' }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <p v-else-if="!loading">Болезни не найдены.</p>

      <div class="pagination-controls" v-if="nextUrl">
        <button @click="fetchDiseases(nextUrl)" :disabled="loading">
          {{ loading ? 'Загрузка...' : 'Загрузить ещё' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { getDiseases } from 'src/modules/catalog_medical_data/api/catalog_medical_data';
import axios from 'axios';

const diseases = ref([]);
const loading = ref(false);
const error = ref('');
const nextUrl = ref(null);

const fetchDiseases = async (url = null) => {
  loading.value = true;
  error.value = '';
  try {
    const response = url ? await axios.get(url) : await getDiseases();
    const newDiseases = response.data.results || response.data;
    diseases.value = [...diseases.value, ...newDiseases];
    nextUrl.value = response.data.next;
  } catch (err) {
    error.value = err.response?.data?.detail || 'Ошибка загрузки болезней';
  } finally {
    loading.value = false;
  }
};

// Загружаем первую страницу при монтировании
fetchDiseases();
</script>

<style scoped>
.diseases-container {
  display: flex;
  justify-content: center;
  margin-top: 20vh;
  background-color: #fff;
}

.diseases-box {
  width: 90%;
  max-width: 1200px;
  padding: 30px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
}

h2 {
  margin-bottom: 20px;
  font-size: 22px;
  font-weight: bold;
  color: #333;
}

.error {
  color: red;
  margin-top: 10px;
  font-size: 16px;
}

.table-wrapper {
  max-height: 500px;
  overflow-y: auto;
}

.diseases-table {
  width: 100%;
  border-collapse: collapse;
  table-layout: fixed;
}

.diseases-table th,
.diseases-table td {
  padding: 12px;
  border: 1px solid #ccc;
  text-align: left;
  font-size: 14px;
  word-break: break-word;
}

.diseases-table th {
  background-color: #e0e0e0;
  font-weight: bold;
  position: sticky;
  top: 0;
  z-index: 1;
}

.pagination-controls {
  margin-top: 20px;
  text-align: center;
}

.pagination-controls button {
  padding: 10px 20px;
  background-color: #000;
  color: white;
  border: none;
  border-radius: 20px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.pagination-controls button:hover:not(:disabled) {
  background-color: #333;
}

.pagination-controls button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}
</style>