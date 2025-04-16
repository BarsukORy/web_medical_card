<template>
  <div class="patient-detail-container">
    <div class="patient-detail-box">
      <h2>Информация о пациенте</h2>

      <!-- Сообщение об ошибке -->
      <p v-if="error" class="error">{{ error }}</p>

      <!-- Кнопки управления -->
      <div class="controls">
        <button v-if="!isEditing" @click="startEditing">Редактировать</button>
        <button v-if="isEditing" @click="saveChanges">Сохранить</button>
        <button v-if="isEditing" @click="cancelEditing">Отмена</button>
      </div>

      <!-- Информация о пациенте -->
      <div v-if="patient" class="patient-info">
        <!-- Фото пациента -->
        <div class="patient-photo">
          <img v-if="patient.photo && !newPhoto" :src="patient.photo" alt="Фото пациента" />
          <img v-if="newPhoto" :src="newPhoto" alt="Новое фото" />
          <div v-if="isEditing" class="camera-container">
            <video
              v-show="!newPhoto"
              ref="video"
              autoplay
              playsinline
              class="camera-video"
            ></video>
            <canvas ref="canvas" style="display: none;"></canvas>
            <div class="camera-controls">
              <button type="button" @click="capturePhoto" :disabled="loading">
                Сфотографировать
              </button>
              <button type="button" @click="clearPhoto" v-if="newPhoto" :disabled="loading">
                Очистить фото
              </button>
            </div>
          </div>
        </div>

        <!-- Текстовая информация или форма редактирования -->
        <div class="patient-details">
          <div v-if="!isEditing">
            <div class="info-row">
              <span class="label">ФИО:</span>
              <span class="value">{{ patient.last_name }} {{ patient.first_name }} {{ patient.middle_name }}</span>
            </div>
            <div class="info-row">
              <span class="label">СНИЛС:</span>
              <span class="value">{{ patient.snils }}</span>
            </div>
            <div class="info-row">
              <span class="label">Дата рождения:</span>
              <span class="value">{{ patient.birth_date }}</span>
            </div>
            <div class="info-row">
              <span class="label">Пол:</span>
              <span class="value">{{ patient.gender === 'M' ? 'Мужской' : patient.gender === 'F' ? 'Женский' : 'Не указан' }}</span>
            </div>
            <div class="info-row">
              <span class="label">Адрес регистрации:</span>
              <span class="value">{{ patient.registration_address || 'Не указан' }}</span>
            </div>
            <div class="info-row">
              <span class="label">Фактический адрес:</span>
              <span class="value">{{ patient.actual_address || 'Не указан' }}</span>
            </div>
            <div class="info-row" v-if="patient.medical_card">
              <span class="label">Медицинская карта:</span>
              <span class="value">
                <router-link
                  :to="`/medical-cards/${patient.medical_card.id}`"
                  custom
                  v-slot="{ href, navigate }"
                >
                  <a :href="href" @click="navigate" target="_blank">
                    Открыть медкарту
                  </a>
                </router-link>
              </span>
            </div>
          </div>

          <!-- Форма редактирования -->
          <div v-else class="edit-form">
            <div class="info-row">
              <span class="label">Фамилия:</span>
              <input v-model="editedPatient.last_name" placeholder="Фамилия" />
            </div>
            <div class="info-row">
              <span class="label">Имя:</span>
              <input v-model="editedPatient.first_name" placeholder="Имя" />
            </div>
            <div class="info-row">
              <span class="label">Отчество:</span>
              <input v-model="editedPatient.middle_name" placeholder="Отчество" />
            </div>
            <div class="info-row">
              <span class="label">СНИЛС:</span>
              <input v-model="editedPatient.snils" placeholder="СНИЛС" />
            </div>
            <div class="info-row">
              <span class="label">Дата рождения:</span>
              <input type="date" v-model="editedPatient.birth_date" />
            </div>
            <div class="info-row">
              <span class="label">Пол:</span>
              <select v-model="editedPatient.gender">
                <option value="M">Мужской</option>
                <option value="F">Женский</option>
                <option value="">Не указан</option>
              </select>
            </div>
            <div class="info-row">
              <span class="label">Адрес регистрации:</span>
              <input v-model="editedPatient.registration_address" placeholder="Адрес регистрации" />
            </div>
            <div class="info-row">
              <span class="label">Фактический адрес:</span>
              <input v-model="editedPatient.actual_address" placeholder="Фактический адрес" />
            </div>
          </div>
        </div>
      </div>

      <!-- Загрузка -->
      <p v-if="loading">Загрузка...</p>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue';
import { useRoute } from 'vue-router';
import { getPatientById, updatePatient } from '../api/patient';

export default {
  name: 'PatientDetail',
  setup() {
    const route = useRoute();
    const patient = ref(null);
    const editedPatient = ref(null);
    const loading = ref(false);
    const error = ref('');
    const isEditing = ref(false);
    const newPhoto = ref(null);
    const video = ref(null);
    const canvas = ref(null);
    let stream = null;

    // Загрузка данных пациента
    const fetchPatient = async () => {
      loading.value = true;
      error.value = '';
      try {
        console.log('Fetching patient with ID:', route.params.id);
        console.log('Token in localStorage:', localStorage.getItem('token'));
        const response = await getPatientById(route.params.id);
        console.log('Patient data:', response.data);
        patient.value = response.data;
        // Инициализируем editedPatient только с редактируемыми полями
        editedPatient.value = {
          first_name: response.data.first_name,
          last_name: response.data.last_name,
          middle_name: response.data.middle_name,
          snils: response.data.snils,
          birth_date: response.data.birth_date,
          gender: response.data.gender,
          registration_address: response.data.registration_address,
          actual_address: response.data.actual_address,
        };
      } catch (err) {
        console.error('Ошибка при загрузке данных пациента:', err);
        if (err.response) {
          console.error('Статус ошибки:', err.response.status);
          console.error('Данные ошибки:', err.response.data);
          error.value = err.response.data?.detail || `Ошибка ${err.response.status}: Не удалось загрузить данные пациента`;
        } else {
          error.value = 'Ошибка сети или сервера недоступен';
        }
      } finally {
        loading.value = false;
      }
    };

    // Начало редактирования
    const startEditing = () => {
      isEditing.value = true;
      startCamera();
    };

    // Отмена редактирования
    const cancelEditing = () => {
      isEditing.value = false;
      editedPatient.value = {
        first_name: patient.value.first_name,
        last_name: patient.value.last_name,
        middle_name: patient.value.middle_name,
        snils: patient.value.snils,
        birth_date: patient.value.birth_date,
        gender: patient.value.gender,
        registration_address: patient.value.registration_address,
        actual_address: patient.value.actual_address,
      };
      newPhoto.value = null;
      stopCamera();
    };

    // Сохранение изменений
    const saveChanges = async () => {
      loading.value = true;
      error.value = '';
      try {
        let photoFile = null;
        if (newPhoto.value) {
          const blob = await fetch(newPhoto.value).then((res) => res.blob());
          photoFile = new File([blob], 'photo.jpg', { type: 'image/jpeg' });
        }

        const response = await updatePatient(route.params.id, editedPatient.value, photoFile);
        console.log('Update response:', response.data);
        patient.value = response.data;

        isEditing.value = false;
        newPhoto.value = null;
        stopCamera();
      } catch (err) {
        console.error('Ошибка при сохранении данных:', err);
        if (err.response) {
          console.error('Статус ошибки:', err.response.status);
          console.error('Данные ошибки:', err.response.data);
          error.value = err.response.data?.detail || `Ошибка ${err.response.status}: Не удалось сохранить данные`;
        } else {
          error.value = 'Ошибка сети или сервера недоступен';
        }
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
      newPhoto.value = canvas.value.toDataURL('image/jpeg');
    };

    // Очистка нового фото
    const clearPhoto = () => {
      newPhoto.value = null;
      startCamera();
    };

    // Загрузка данных при монтировании
    onMounted(() => {
      fetchPatient();
    });

    // Очистка при выходе из компонента
    onUnmounted(() => {
      stopCamera();
    });

    return {
      patient,
      editedPatient,
      loading,
      error,
      isEditing,
      newPhoto,
      video,
      canvas,
      startEditing,
      cancelEditing,
      saveChanges,
      startCamera,
      stopCamera,
      capturePhoto,
      clearPhoto,
    };
  },
};
</script>

<style scoped>
/* Контейнер для страницы */
.patient-detail-container {
  display: flex;
  justify-content: center;
  margin-top: 20vh;
  background-color: #fff;
}

/* Блок с информацией о пациенте */
.patient-detail-box {
  width: 800px;
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

/* Кнопки управления */
.controls {
  margin-bottom: 20px;
}

.controls button {
  padding: 10px 20px;
  margin-right: 10px;
  background-color: #000;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.3s;
}

.controls button:hover {
  background-color: #333;
}

.controls button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

/* Контейнер для информации о пациенте */
.patient-info {
  display: flex;
  gap: 30px;
  text-align: left;
}

/* Фото пациента */
.patient-photo img {
  width: 200px;
  height: 200px;
  object-fit: cover;
  border-radius: 8px;
  border: 1px solid #ccc;
}

/* Текстовая информация */
.patient-details {
  flex: 1;
}

.info-row {
  display: flex;
  margin-bottom: 15px;
  align-items: center;
}

.label {
  font-weight: 600;
  color: #333;
  width: 150px;
  font-size: 16px;
}

.value {
  font-size: 16px;
  color: #555;
}

/* Форма редактирования */
.edit-form input,
.edit-form select {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 16px;
  width: 100%;
  max-width: 300px;
  box-sizing: border-box;
}

a {
  color: #007bff;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}

/* Стили для камеры */
.camera-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  margin-top: 10px;
}

.camera-video {
  width: 200px;
  height: 200px;
  border: 1px solid #ccc;
  border-radius: 6px;
  object-fit: cover;
}

.camera-controls {
  display: flex;
  gap: 10px;
}

.camera-controls button {
  padding: 8px 16px;
  background-color: #000;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.3s;
}

.camera-controls button:hover {
  background-color: #333;
}

.camera-controls button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}
</style>