<template>
  <div class="search-container">
    <!-- Блок формы (слева) -->
    <div class="search-box">
      <h2>Поиск пациента</h2>

      <!-- Вкладки для выбора метода поиска -->
      <div class="tabs">
        <button
          :class="{ active: activeTab === 'snilsOrFio' }"
          @click="activeTab = 'snilsOrFio'; stopCamera()"
        >
          По ФИО или СНИЛС
        </button>
        <button
          :class="{ active: activeTab === 'face' }"
          @click="activeTab = 'face'; startCamera()"
        >
          По лицу
        </button>
      </div>

      <!-- Форма поиска по ФИО/СНИЛС -->
      <div v-if="activeTab === 'snilsOrFio'" class="search-form">
        <form @submit.prevent="searchBySnilsOrFio">
          <div class="form-group">
            <label for="query">ФИО или СНИЛС</label>
            <input
              type="text"
              id="query"
              v-model="searchQuery"
              placeholder="Введите ФИО или СНИЛС"
              required
            />
          </div>
          <!-- Контейнер для кнопок -->
          <div class="button-group">
            <button type="submit" class="search-button" :disabled="loading">
              {{ loading ? 'Поиск...' : 'Найти' }}
            </button>
            <button type="button" class="create-button" @click="goToCreatePatient">
              Создать
            </button>
          </div>
        </form>
      </div>

      <!-- Поиск по лицу через веб-камеру -->
      <div v-if="activeTab === 'face'" class="search-form">
        <div class="camera-container">
          <video
            v-show="!capturedImage"
            ref="video"
            autoplay
            playsinline
            class="camera-video"
          ></video>
          <canvas ref="canvas" style="display: none;"></canvas>
          <div v-if="capturedImage" class="captured-image">
            <img :src="capturedImage" alt="Captured Photo" />
          </div>
          <div class="camera-controls">
            <button type="button" @click="capturePhoto" :disabled="loading">
              Сфотографировать
            </button>
            <button
              type="button"
              @click="searchByFace"
              :disabled="!capturedImage || loading"
            >
              {{ loading ? 'Поиск...' : 'Найти' }}
            </button>
          </div>
        </div>
        <!-- Кнопка "Создать" отдельно -->
        <button type="button" class="create-button standalone" @click="goToCreatePatient">
          Создать
        </button>
      </div>

      <!-- Сообщение об ошибке -->
      <p v-if="error" class="error">{{ error }}</p>
    </div>

    <!-- Блок результатов (справа) -->
    <div v-if="patients.length" class="results-box">
      <h3>Результаты поиска</h3>
      <div class="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>ФИО</th>
              <th>СНИЛС</th>
              <th>Группа крови</th>
              <th>Медицинская карта</th>
              <th>Информация о пациенте</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="patient in patients" :key="patient.short_info_patient.id">
              <td>{{ patient.short_info_patient.full_name }}</td>
              <td>{{ patient.short_info_patient.snils }}</td>
              <td>{{ patient.blood_type || 'Не указана' }}</td>
              <td>
                <router-link :to="`/medical-cards/${patient.id}`">
                  Открыть медкарту
                </router-link>
              </td>
              <td>
                <router-link :to="`/patients/${patient.short_info_patient.id}`">
                  Подробнее
                </router-link>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onUnmounted } from 'vue';
import { useRouter } from 'vue-router'; // Импортируем useRouter
import { searchPatientsBySnilsOrFio, searchPatientsByFace } from '../api/patient';

export default {
  name: 'PatientSearch',
  setup() {
    const router = useRouter(); // Инициализируем роутер
    const activeTab = ref('snilsOrFio');
    const searchQuery = ref('');
    const patients = ref([]);
    const loading = ref(false);
    const error = ref('');

    // Переменные для работы с веб-камерой
    const video = ref(null);
    const canvas = ref(null);
    const capturedImage = ref(null);
    let stream = null;

    // Поиск по ФИО или СНИЛС
    const searchBySnilsOrFio = async () => {
      if (!searchQuery.value) {
        error.value = 'Введите ФИО или СНИЛС';
        return;
      }

      loading.value = true;
      error.value = '';
      patients.value = [];

      try {
        const isSnils = searchQuery.value.match(/^\d{3}-\d{3}-\d{3}\s\d{2}$/);
        const params = isSnils
          ? { snils: searchQuery.value }
          : { full_name: searchQuery.value };

        const response = await searchPatientsBySnilsOrFio(params);
        patients.value = response.data;
        if (!patients.value.length) {
          error.value = 'Пациенты не найдены';
        }
      } catch (err) {
        error.value = err.response?.data?.detail || 'Ошибка при поиске';
      } finally {
        loading.value = false;
      }
    };

    // Запуск веб-камеры
    const startCamera = async () => {
      try {
        if (stream) {
          video.value.srcObject = stream;
          return;
        }

        stream = await navigator.mediaDevices.getUserMedia({
          video: { facingMode: 'user' },
        });
        video.value.srcObject = stream;
      } catch (err) {
        error.value = 'Не удалось получить доступ к камере: ' + err.message;
      }
    };

    // Остановка веб-камеры
    const stopCamera = () => {
      if (stream) {
        stream.getTracks().forEach((track) => track.stop());
        stream = null;
        if (video.value) {
          video.value.srcObject = null;
        }
      }
    };

    // Захват фото с веб-камеры
    const capturePhoto = () => {
      if (!video.value || !video.value.srcObject) {
        error.value = 'Камера не активна. Попробуйте перезапустить.';
        startCamera();
        return;
      }

      const context = canvas.value.getContext('2d');
      canvas.value.width = video.value.videoWidth;
      canvas.value.height = video.value.videoHeight;

      if (canvas.value.width === 0 || canvas.value.height === 0) {
        error.value = 'Не удалось определить размеры видео. Попробуйте снова.';
        return;
      }

      context.drawImage(video.value, 0, 0, canvas.value.width, canvas.value.height);
      capturedImage.value = canvas.value.toDataURL('image/jpeg');
    };

    // Поиск по лицу
    const searchByFace = async () => {
      if (!capturedImage.value) {
        error.value = 'Сначала сделайте фото';
        return;
      }

      loading.value = true;
      error.value = '';
      patients.value = [];

      try {
        const response = await fetch(capturedImage.value);
        const blob = await response.blob();
        const file = new File([blob], 'photo.jpg', { type: 'image/jpeg' });

        const searchResponse = await searchPatientsByFace(file);
        patients.value = searchResponse.data;
        if (!patients.value.length) {
          error.value = 'Пациенты не найдены';
        }
      } catch (err) {
        error.value = err.response?.data?.detail || 'Ошибка при поиске';
      } finally {
        loading.value = false;
      }

      capturedImage.value = null;
      startCamera();
    };

    // Переход на страницу создания пациента
    const goToCreatePatient = () => {
      router.push('/create-patient');
    };

    // Очистка при выходе из компонента
    onUnmounted(() => {
      stopCamera();
    });

    return {
      activeTab,
      searchQuery,
      patients,
      loading,
      error,
      video,
      canvas,
      capturedImage,
      searchBySnilsOrFio,
      startCamera,
      stopCamera,
      capturePhoto,
      searchByFace,
      goToCreatePatient,
    };
  },
};
</script>

<style scoped>
/* Существующие стили */
.search-container {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 20vh;
  background-color: #fff;
}

.search-box {
  width: 650px;
  padding: 30px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.results-box {
  width: 650px;
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

h3 {
  margin-bottom: 10px;
  font-size: 18px;
  font-weight: bold;
  color: #333;
}

.tabs {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.tabs button {
  padding: 12px 30px;
  border: none;
  background-color: #e0e0e0;
  cursor: pointer;
  font-size: 16px;
  color: #333;
  transition: background 0.3s;
}

.tabs button.active {
  background-color: #000;
  color: white;
}

.search-form {
  display: flex;
  flex-direction: column;
  width: 100%;
}

.search-form form {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.search-form button {
  margin-top: 30px;
}

.form-group {
  display: flex;
  flex-direction: column;
  text-align: left;
  width: 100%;
}

label {
  margin-bottom: 5px;
  font-weight: 600;
  color: #333;
  font-size: 14px;
}

input {
  padding: 12px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 16px;
  width: 100%;
  box-sizing: border-box;
}

.button-group {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  margin-top: 20px;
  width: 100%; /* Убедимся, что контейнер занимает всю ширину */
}

/* Общие стили для кнопок */
.search-button,
.create-button {
  flex: 1; /* Кнопки равномерно делят пространство */
  padding: 12px;
  background-color: #000;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.3s;
  text-align: center;
}

.search-button:hover,
.create-button:hover {
  background-color: #333;
}

.search-button:disabled,
.create-button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}


.create-button.standalone {
  width: 100%;
  margin-top: 20px;
  padding: 12px;
  background-color: #000;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.3s;
  text-align: center;
}

.create-button.standalone:hover {
  background-color: #333;
}

.create-button.standalone:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}


button {
  padding: 12px;
  background-color: #000;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.3s;
}

button:hover {
  background-color: #333;
}

button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.error {
  color: red;
  margin-top: 10px;
  font-size: 14px;
}

.table-wrapper {
  max-height: 400px;
  overflow-y: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  padding: 12px;
  border: 1px solid #ccc;
  text-align: left;
  font-size: 14px;
}

th {
  background-color: #e0e0e0;
  font-weight: bold;
  position: sticky;
  top: 0;
  z-index: 1;
}

a {
  color: #007bff;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}

.camera-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 30px;
}

.camera-video,
.captured-image img {
  width: 500px;
  height: 300px;
  border: 1px solid #ccc;
  border-radius: 6px;
  object-fit: cover;
}

.camera-controls {
  display: flex;
  gap: 10px;
  width: 100%;
  max-width: 500px;
}

.camera-controls button {
  flex: 1;
}

/* Стили для кнопки "Создать пациента" */
.create-button {
  margin-top: 20px;
  padding: 12px;
  background-color: #000;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.3s;
}

.create-button:hover {
  background-color: #000000;
}
</style>