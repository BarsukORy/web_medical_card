<template>
  <div class="create-patient-container">
    <div class="create-patient-box">
      <h2>Создать пациента</h2>

      <!-- Сообщение об ошибке -->
      <p v-if="error" class="error">{{ error }}</p>

      <!-- Форма создания пациента -->
      <div class="patient-info">
        <!-- Камера для фото -->
        <div class="patient-photo">
          <img v-if="newPhoto" :src="newPhoto" alt="Новое фото" />
          <div class="camera-container">
            <video
              v-show="!newPhoto"
              ref="video"
              autoplay
              playsinline
              class="camera-video"
            ></video>
            <canvas ref="canvas" style="display: none;"></canvas>
            <div class="camera-controls">
              <button type="button" @click="capturePhoto" :disabled="loading || cameraError">
                Сфотографировать
              </button>
              <button type="button" @click="clearPhoto" v-if="newPhoto" :disabled="loading">
                Очистить фото
              </button>
            </div>
          </div>
        </div>

        <!-- Поля для ввода -->
        <div class="patient-details">
          <!-- Блок информации о пациенте -->
          <div class="section">
            <h3>Информация о пациенте</h3>
            <div class="edit-form">
              <div class="info-row">
                <span class="label">Фамилия:</span>
                <input v-model="patient.last_name" placeholder="Фамилия" required />
              </div>
              <div class="info-row">
                <span class="label">Имя:</span>
                <input v-model="patient.first_name" placeholder="Имя" required />
              </div>
              <div class="info-row">
                <span class="label">Отчество:</span>
                <input v-model="patient.middle_name" placeholder="Отчество" />
              </div>
              <div class="info-row">
                <span class="label">СНИЛС:</span>
                <input v-model="patient.snils" placeholder="СНИЛС" required />
              </div>
              <div class="info-row">
                <span class="label">Дата рождения:</span>
                <input type="date" v-model="patient.birth_date" required />
              </div>
              <div class="info-row">
                <span class="label">Пол:</span>
                <select v-model="patient.gender">
                  <option value="M">Мужской</option>
                  <option value="F">Женский</option>
                  <option value="">Не указан</option>
                </select>
              </div>
              <div class="info-row">
                <span class="label">Адрес регистрации:</span>
                <input v-model="patient.registration_address" placeholder="Адрес регистрации" />
              </div>
              <div class="info-row">
                <span class="label">Фактический адрес:</span>
                <input v-model="patient.actual_address" placeholder="Фактический адрес" />
              </div>
            </div>
          </div>

          <!-- Блок медицинской карты -->
          <div class="section">
            <h3>Медицинская карта</h3>
            <div class="edit-form">
              <div class="info-row">
                <span class="label">Группа крови:</span>
                <select v-model="medicalCard.blood_type">
                  <option value="">Не указана</option>
                  <option value="O+">O+</option>
                  <option value="O-">O-</option>
                  <option value="A+">A+</option>
                  <option value="A-">A-</option>
                  <option value="B+">B+</option>
                  <option value="B-">B-</option>
                  <option value="AB+">AB+</option>
                  <option value="AB-">AB-</option>
                </select>
              </div>
              <div class="info-row">
                <span class="label">Аллергии:</span>
                <input v-model="medicalCard.allergies" placeholder="Аллергии (если есть)" />
              </div>
              <div class="info-row">
                <span class="label">Хронические заболевания:</span>
                <input v-model="medicalCard.chronic_diseases" placeholder="Хронические заболевания (если есть)" />
              </div>
              <div class="info-row">
                <span class="label">Больница:</span>
                <select v-model="medicalCard.attachment_hospital_id">
                  <option value="">Не выбрана</option>
                  <option v-for="hospital in hospitals" :key="hospital.id" :value="hospital.id">
                    {{ hospital.name }}
                  </option>
                </select>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Кнопки управления -->
      <div class="controls">
        <button @click="createPatient" :disabled="loading || isSubmitting">
          {{ loading ? 'Создание...' : 'Создать' }}
        </button>
        <button @click="goBack" :disabled="loading">Назад</button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import { createPatient_Api } from '../api/patient';
import { createMedicalCard } from 'src/modules/medical_card/api/medical_card';
import { getHospitals} from "@/modules/medical_hub/api/medical_hub.js";

export default {
  name: 'CreatePatient',
  setup() {
    const router = useRouter();
    const patient = ref({
      first_name: '',
      last_name: '',
      middle_name: '',
      snils: '',
      birth_date: '',
      gender: '',
      registration_address: '',
      actual_address: '',
    });
    const medicalCard = ref({
      blood_type: '',
      allergies: '',
      chronic_diseases: '',
      attachment_hospital_id: '',
    });
    const hospitals = ref([]);
    const newPhoto = ref(null);
    const video = ref(null);
    const canvas = ref(null);
    const loading = ref(false);
    const error = ref('');
    const cameraError = ref(false);
    const isSubmitting = ref(false);
    let stream = null;
    let isStartingCamera = false;

    const fetchHospitals = async () => {
      try {
        const response = await getHospitals();
        hospitals.value = response.data.results || response.data;
        console.log('Список больниц загружен:', hospitals.value);
      } catch (err) {
        error.value = 'Не удалось загрузить список больниц: ' + (err.response?.data?.detail || err.message);
        console.error('Ошибка при загрузке больниц:', err);
      }
    };

    const startCamera = async () => {
      if (isStartingCamera) {
        console.log('Камера уже запускается, пропускаем вызов');
        return;
      }

      isStartingCamera = true;
      try {
        if (stream) {
          video.value.srcObject = stream;
          isStartingCamera = false;
          return;
        }

        stream = await navigator.mediaDevices.getUserMedia({
          video: {facingMode: 'user'},
        });
        video.value.srcObject = stream;
        cameraError.value = false;
        console.log('Камера успешно запущена');
      } catch (err) {
        error.value = 'Не удалось получить доступ к камере: ' + err.message;
        cameraError.value = true;
        console.error('Ошибка запуска камеры:', err);
      } finally {
        isStartingCamera = false;
      }
    };

    const stopCamera = () => {
      if (stream) {
        stream.getTracks().forEach((track) => track.stop());
        stream = null;
        if (video.value) {
          video.value.srcObject = null;
        }
        console.log('Камера остановлена');
      }
    };

    const capturePhoto = () => {
      if (cameraError.value) {
        error.value = 'Камера недоступна. Проверьте доступ и попробуйте снова.';
        return;
      }

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
      console.log('Фото захвачено:', newPhoto.value);
    };

    const clearPhoto = () => {
      newPhoto.value = null;
      startCamera();
      console.log('Фото очищено');
    };

    const createPatient = async () => {
      if (isSubmitting.value) {
        console.log('Создание уже выполняется, пропускаем вызов');
        return;
      }

      if (!patient.value.first_name || !patient.value.last_name || !patient.value.snils || !patient.value.birth_date) {
        error.value = 'Пожалуйста, заполните все обязательные поля (Фамилия, Имя, СНИЛС, Дата рождения)';
        return;
      }

      isSubmitting.value = true;
      loading.value = true;
      error.value = '';

      try {
        console.log('Создание пациента с данными:', patient.value);

        let photoFile = null;
        if (newPhoto.value) {
          console.log('Обработка фото...');
          const blob = await fetch(newPhoto.value).then((res) => res.blob());
          photoFile = new File([blob], 'photo.jpg', {type: 'image/jpeg'});
          console.log('Фото успешно преобразовано в File:', photoFile);
        }

        console.log('Отправка запроса на создание пациента...');
        const patientResponse = await createPatient_Api(patient.value, photoFile);
        console.log('Пациент успешно создан:', patientResponse.data);
        const patientId = patientResponse.data.id;

        const hasMedicalCardData = medicalCard.value.blood_type || medicalCard.value.allergies || medicalCard.value.chronic_diseases || medicalCard.value.attachment_hospital_id;
        if (hasMedicalCardData) {
          console.log('Создание медицинской карты...');
          const medicalCardData = {
            patient_id: patientId,
            blood_type: medicalCard.value.blood_type || '',
            allergies: medicalCard.value.allergies || '',
            chronic_diseases: medicalCard.value.chronic_diseases || '',
            attachment_hospital_id: medicalCard.value.attachment_hospital_id || null,
          };
          console.log('Данные медицинской карты:', medicalCardData);
          const medicalCardResponse = await createMedicalCard(medicalCardData);
          console.log('Медицинская карта успешно создана:', medicalCardResponse.data);
        } else {
          console.log('Медицинская карта не создаётся, так как поля не заполнены');
        }

        console.log('Перенаправление на страницу пациента:', `/patients/${patientId}`);
        await router.push(`/patients/${patientId}`);
        console.log('Роутинг завершён');
      } catch (err) {
        error.value = err.response?.data?.detail || 'Ошибка при создании пациента или медицинской карты';
        console.error('Ошибка:', err);
      } finally {
        loading.value = false;
        isSubmitting.value = false;
      }
    };

    const goBack = () => {
      router.push('/patients/search');
    };

    onMounted(() => {
      error.value = '';
      startCamera();
      fetchHospitals();
    });

    onUnmounted(() => {
      stopCamera();
    });

    return {
      patient,
      medicalCard,
      hospitals,
      newPhoto,
      video,
      canvas,
      loading,
      error,
      cameraError,
      isSubmitting,
      capturePhoto,
      clearPhoto,
      createPatient,
      goBack,
    };
  },
};
</script>

<style scoped>
/* Контейнер для страницы */
.create-patient-container {
  display: flex;
  justify-content: center;
  margin-top: 5vh;
  background-color: #f5f5f5;
  min-height: 100vh;
}

/* Блок с информацией о пациенте */
.create-patient-box {
  width: 900px;
  padding: 30px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
}

h2 {
  margin-bottom: 20px;
  font-size: 24px;
  font-weight: bold;
  color: #333;
}

h3 {
  margin-bottom: 15px;
  font-size: 18px;
  font-weight: 600;
  color: #444;
  text-align: left;
  border-bottom: 2px solid #e0e0e0;
  padding-bottom: 5px;
}

.error {
  color: red;
  margin-top: 10px;
  font-size: 16px;
}

/* Контейнер для информации о пациенте */
.patient-info {
  display: flex;
  gap: 30px;
  text-align: left;
  margin-bottom: 20px;
}

/* Фото пациента */
.patient-photo {
  flex: 0 0 auto;
}

.patient-photo img {
  width: 300px;
  height: 200px;
  object-fit: cover;
  border-radius: 8px;
  border: 1px solid #ccc;
}

/* Текстовая информация */
.patient-details {
  flex: 1;
}

/* Секции */
.section {
  background: #fafafa;
  padding: 20px;
  border-radius: 6px;
  margin-bottom: 20px;
  border: 1px solid #e0e0e0;
}

.info-row {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

.label {
  font-weight: 600;
  color: #333;
  width: 180px;
  font-size: 16px;
}

.edit-form input,
.edit-form select {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 16px;
  width: 100%;
  max-width: 300px;
  box-sizing: border-box;
  transition: border-color 0.3s;
}

.edit-form input:focus,
.edit-form select:focus {
  border-color: #007bff;
  outline: none;
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
  width: 300px;
  height: 200px;
  border: 1px solid #ccc;
  border-radius: 6px;
  object-fit: cover;
}

.camera-controls {
  display: flex;
  gap: 10px;
  width: 100%;
  max-width: 300px;
}

.camera-controls button {
  flex: 1;
  padding: 10px;
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

/* Кнопки управления */
.controls {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-top: 20px;
}

.controls button {
  padding: 12px 30px;
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

.controls button:nth-child(2) {
  background-color: #e0e0e0;
  color: #333;
}

.controls button:nth-child(2):hover {
  background-color: #cccccc;
}
</style>