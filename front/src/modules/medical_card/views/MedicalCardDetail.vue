<template>
  <div class="medical-card-detail-container">
    <div class="medical-card-detail-box">
      <h2>Медицинская карта</h2>

      <div v-if="globalError" class="global-error">
        {{ globalError }}
      </div>

      <div class="main-content">
        <div class="top-section">
          <div class="left-top">
            <h3>Данные карты</h3>
            <div v-if="medicalCard" class="medical-card-info">
              <div class="medical-card-details">
                <div v-if="!isEditingCard">
                  <div class="info-row">
                    <span class="label">Пациент:</span>
                    <span class="value">{{ medicalCard.short_info_patient.full_name }}</span>
                  </div>
                  <div class="info-row">
                    <span class="label">Группа крови:</span>
                    <span class="value">{{ medicalCard.blood_type || 'Не указана' }}</span>
                  </div>
                  <div class="info-row">
                    <span class="label">Аллергены:</span>
                    <span class="value">{{ medicalCard.allergies || 'Не указаны' }}</span>
                  </div>
                  <div class="info-row">
                    <span class="label">Хронические заболевания:</span>
                    <span class="value">{{ medicalCard.chronic_diseases || 'Не указаны' }}</span>
                  </div>
                  <div class="info-row">
                    <span class="label">Больница:</span>
                    <span class="value">{{ medicalCard.attachment_hospital_info?.name || 'Не указана' }}</span>
                  </div>
                </div>

                <div v-else class="edit-form">
                  <div class="info-row">
                    <span class="label">Группа крови:</span>
                    <input v-model="editedMedicalCard.blood_type" placeholder="Группа крови" />
                  </div>
                  <div class="info-row">
                    <span class="label">Аллергены:</span>
                    <textarea v-model="editedMedicalCard.allergies" placeholder="Аллергены" rows="3"></textarea>
                  </div>
                  <div class="info-row">
                    <span class="label">Хронические заболевания:</span>
                    <textarea v-model="editedMedicalCard.chronic_diseases" placeholder="Хронические заболевания" rows="3"></textarea>
                  </div>
                  <div class="info-row">
                    <span class="label">Больница:</span>
                    <div class="hospital-select-wrapper">
                      <select v-model="editedMedicalCard.attachment_hospital_id" :disabled="loadingHospitals">
                        <option :value="null">Выберите больницу</option>
                        <option v-for="hospital in hospitals" :key="hospital.id" :value="hospital.id">{{ hospital.name }}</option>
                      </select>
                      <p v-if="loadingHospitals" class="loading-message">Загрузка больниц...</p>
                      <p v-if="hospitalError" class="error">{{ hospitalError }}</p>
                      <p v-if="!loadingHospitals && !hospitalError && hospitals.length === 0" class="no-data-message">Больницы не найдены</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="controls" v-if="medicalCard">
              <button v-if="!isEditingCard" @click="startEditingCard">Редактировать карту</button>
              <button v-if="isEditingCard" @click="saveCardChanges">Сохранить</button>
              <button v-if="isEditingCard" @click="cancelEditingCard">Отмена</button>
              <router-link v-if="medicalCard?.short_info_patient?.id" :to="`/patients/${medicalCard.short_info_patient.id}`" custom v-slot="{ href, navigate }">
                <button @click="navigate">Информация о пациенте</button>
              </router-link>
            </div>
          </div>

          <div class="right-top">
            <div class="entries-section">
              <h3>Записи</h3>
              <button @click="showNewEntryForm = true" v-if="!showNewEntryForm">Добавить запись</button>

              <div v-if="showNewEntryForm" class="new-entry-form">
                <h4>Новая запись</h4>
                <div v-if="localErrors.newEntry" class="error">{{ localErrors.newEntry }}</div>
                <div class="info-row">
                  <span class="label">Дата визита:</span>
                  <input type="date" v-model="newEntry.visit_date" />
                </div>
                <div class="info-row">
                  <span class="label">Диагноз:</span>
                  <select v-model="newEntry.diagnosis" @change="newEntry.custom_diagnosis = ''">
                    <option :value="null">Выберите диагноз</option>
                    <option v-for="disease in diseases" :key="disease.id" :value="disease.id">{{ disease.name }}</option>
                  </select>
                </div>
                <div class="info-row">
                  <span class="label">Или кастомный диагноз:</span>
                  <input v-model="newEntry.custom_diagnosis" placeholder="Пользовательский диагноз" :disabled="newEntry.diagnosis !== null" @input="clearDiagnosis" />
                </div>
                <div class="info-row">
                  <span class="label">Лечение:</span>
                  <textarea v-model="newEntry.custom_treatment" placeholder="Пользовательское лечение" rows="3"></textarea>
                </div>
                <div class="info-row">
                  <span class="label">Заметки:</span>
                  <textarea v-model="newEntry.notes" placeholder="Заметки" rows="3"></textarea>
                </div>
                <div class="info-row">
                  <span class="label">Больница:</span>
                  <div class="hospital-select-wrapper">
                    <select v-model="newEntry.hospital_id" :disabled="loadingHospitals">
                      <option :value="null">Выберите больницу</option>
                      <option v-for="hospital in hospitals" :key="hospital.id" :value="hospital.id">{{ hospital.name }}</option>
                    </select>
                    <p v-if="loadingHospitals" class="loading-message">Загрузка больниц...</p>
                    <p v-if="hospitalError" class="error">{{ hospitalError }}</p>
                    <p v-if="!loadingHospitals && !hospitalError && hospitals.length === 0" class="no-data-message">Больницы не найдены</p>
                  </div>
                </div>
                <div class="controls">
                  <button @click="createEntry">Создать</button>
                  <button @click="showNewEntryForm = false">Отмена</button>
                </div>
              </div>

              <div class="entries-list">
                <table class="entries-table">
                  <thead>
                  <tr>
                    <th>Дата визита</th>
                    <th>Диагноз</th>
                    <th>Врач</th>
                    <th>Действия</th>
                  </tr>
                  </thead>
                  <tbody>
                  <tr v-for="entry in medicalCard?.entries?.results" :key="entry.id">
                    <td>{{ entry.visit_date }}</td>
                    <td>{{ entry.get_diagnosis }}</td>
                    <td>{{ entry.doctor_full_name }}</td>
                    <td>
                      <button @click="fetchEntryDetails(entry.id)">Подробнее</button>
                    </td>
                  </tr>
                  </tbody>
                </table>
                <p v-if="!medicalCard?.entries?.results?.length">Записей нет.</p>
                <div class="pagination" v-if="medicalCard?.entries?.count > 0">
                  <button
                      :disabled="!medicalCard?.entries?.previous"
                      @click="fetchEntries(medicalCard.entries.previous)"
                  >
                    Предыдущая
                  </button>
                  <span>Страница {{ currentPage }} из {{ totalPages }}</span>
                  <button
                      :disabled="!medicalCard?.entries?.next"
                      @click="fetchEntries(medicalCard.entries.next)"
                  >
                    Следующая
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <hr class="section-divider" />

        <div class="bottom-section">
          <div class="left-bottom">
            <div v-if="selectedEntry" class="entry-details">
              <h3>Детали записи</h3>
              <div class="info-row">
                <span class="label">Дата визита:</span>
                <span class="value">{{ selectedEntry.visit_date }}</span>
              </div>
              <div class="info-row">
                <span class="label">Диагноз:</span>
                <span class="value">{{ displayDiagnosis }}</span>
              </div>
              <div class="info-row">
                <span class="label">Лечение:</span>
                <span class="value">{{ selectedEntry.custom_treatment || selectedEntry.treatment || 'Не указано' }}</span>
              </div>
              <div class="info-row">
                <span class="label">Заметки:</span>
                <span class="value">{{ selectedEntry.notes || 'Нет заметок' }}</span>
              </div>
              <div class="info-row">
                <span class="label">Больница:</span>
                <span class="value">{{ selectedEntry.hospital_info?.name || 'Не указана' }}</span>
              </div>
              <div class="info-row">
                <span class="label">Врач:</span>
                <span class="value">{{ selectedEntry.doctor?.full_name || 'Не указан' }}</span>
              </div>
              <div class="info-row">
                <span class="label">Специальность врача:</span>
                <span class="value">{{ selectedEntry.doctor?.specialties || 'Не указана' }}</span>
              </div>
              <div class="controls">
                <button @click="startEditingEntry">Редактировать</button>
              </div>

              <div v-if="isEditingEntry" class="edit-entry-form">
                <h4>Редактировать запись</h4>
                <div v-if="localErrors.editEntry" class="error">{{ localErrors.editEntry }}</div>
                <div class="info-row">
                  <span class="label">Дата визита:</span>
                  <input type="date" v-model="editedEntry.visit_date" />
                </div>
                <div class="info-row">
                  <span class="label">Диагноз:</span>
                  <select v-model="editedEntry.diagnosis" @change="editedEntry.custom_diagnosis = ''">
                    <option :value="null">Выберите диагноз</option>
                    <option v-for="disease in diseases" :key="disease.id" :value="disease.id">{{ disease.name }}</option>
                  </select>
                </div>
                <div class="info-row">
                  <span class="label">Или кастомный диагноз:</span>
                  <input v-model="editedEntry.custom_diagnosis" placeholder="Пользовательский диагноз" :disabled="editedEntry.diagnosis !== null" @input="clearDiagnosisForEdit" />
                </div>
                <div class="info-row">
                  <span class="label">Лечение:</span>
                  <textarea v-model="editedEntry.custom_treatment" placeholder="Пользовательское лечение" rows="3"></textarea>
                </div>
                <div class="info-row">
                  <span class="label">Заметки:</span>
                  <textarea v-model="editedEntry.notes" placeholder="Заметки" rows="3"></textarea>
                </div>
                <div class="info-row">
                  <span class="label">Больница:</span>
                  <div class="hospital-select-wrapper">
                    <select v-model="editedEntry.hospital_id" :disabled="loadingHospitals">
                      <option :value="null">Выберите больницу</option>
                      <option v-for="hospital in hospitals" :key="hospital.id" :value="hospital.id">{{ hospital.name }}</option>
                    </select>
                    <p v-if="loadingHospitals" class="loading-message">Загрузка больниц...</p>
                    <p v-if="hospitalError" class="error">{{ hospitalError }}</p>
                    <p v-if="!loadingHospitals && !hospitalError && hospitals.length === 0" class="no-data-message">Больницы не найдены</p>
                  </div>
                </div>
                <div class="controls">
                  <button @click="saveEditedEntry">Сохранить</button>
                  <button @click="cancelEditingEntry">Отмена</button>
                </div>
              </div>
            </div>
          </div>

          <div class="right-bottom">
            <div v-if="selectedEntry">
              <div class="files-section">
                <h4>Файлы</h4>
<!--                <div v-if="localErrors.uploadFile" class="error">{{ localErrors.uploadFile }}</div>-->
                <div v-if="selectedEntry.files?.length">
                  <div v-for="file in selectedEntry.files" :key="file.id" class="file-item">
                    <a :href="file.file" target="_blank">{{ file.file_name }}</a>
                  </div>
                </div>
                <p v-else>Файлов нет.</p>
                <div class="file-upload">
                  <input type="file" @change="onFileChange" ref="fileInput" />
                  <button @click="uploadFile">Загрузить файл</button>
                </div>
              </div>

              <hr class="section-divider" />

              <div class="prescriptions-section">
                <h4>Назначения</h4>
                <button @click="showNewPrescriptionForm = true" v-if="!showNewPrescriptionForm">Добавить назначение</button>

                <div v-if="showNewPrescriptionForm" class="new-prescription-form">
                  <h5>Новое назначение</h5>
                  <div v-if="localErrors.newPrescription" class="error">{{ localErrors.newPrescription }}</div>
                  <div class="info-row">
                    <span class="label">Инструкции:</span>
                    <textarea v-model="newPrescription.administration_notes" placeholder="Инструкции по применению" rows="3"></textarea>
                  </div>
                  <div class="controls">
                    <button @click="createNewPrescription">Создать</button>
                    <button @click="showNewPrescriptionForm = false">Отмена</button>
                  </div>
                </div>

                <div v-if="prescriptions.length" class="prescriptions-list">
                  <div v-for="prescription in prescriptions" :key="prescription.id" class="prescription-item">
                    <div class="info-row">
                      <span class="label">Инструкции:</span>
                      <span class="value">{{ prescription.administration_notes || 'Не указаны' }}</span>
                    </div>
                    <button @click="toggleMedications(prescription.id)">
                      {{ prescription.showMedications ? 'Скрыть медикаменты' : 'Показать медикаменты' }}
                    </button>
                    <div v-if="prescription.showMedications && prescription.medications?.length" class="medications-list">
                      <h5>Медикаменты</h5>
                      <div v-for="med in prescription.medications" :key="med.id" class="medication-item">
                        <div class="info-row">
                          <span class="label">Препарат:</span>
                          <span class="value">{{ med.medication_info?.name || med.medication }}</span>
                        </div>
                        <div class="info-row">
                          <span class="label">Дозировка:</span>
                          <span class="value">{{ med.dosage }}</span>
                        </div>
                        <div class="info-row">
                          <span class="label">Частота:</span>
                          <span class="value">{{ med.frequency }}</span>
                        </div>
                        <div class="info-row">
                          <span class="label">Длительность:</span>
                          <span class="value">{{ med.duration }}</span>
                        </div>
                        <div class="info-row">
                          <span class="label">Заметки:</span>
                          <span class="value">{{ med.individual_notes || 'Нет заметок' }}</span>
                        </div>
                        <div class="medication-actions">
                          <button @click="startEditingMedication(prescription.id, med)">Редактировать</button>
                          <button @click="deleteMedication(prescription.id, med.id)">Удалить</button>
                        </div>
                      </div>
                    </div>
                    <button @click="showNewMedicationForm[prescription.id] = true" v-if="!showNewMedicationForm[prescription.id]">Добавить медикамент</button>
                    <div v-if="showNewMedicationForm[prescription.id]" class="new-medication-form">
                      <h5>Новый медикамент</h5>
                      <div v-if="localErrors.newMedication" class="error">{{ localErrors.newMedication }}</div>
                      <div class="info-row">
                        <span class="label">Препарат:</span>
                        <select v-model="newMedication.medication">
                          <option :value="null">Выберите препарат</option>
                          <option v-for="med in medications" :key="med.id" :value="med.id">{{ med.name }} ({{ med.form }})</option>
                        </select>
                      </div>
                      <div class="info-row">
                        <span class="label">Дозировка:</span>
                        <input v-model="newMedication.dosage" placeholder="Дозировка" />
                      </div>
                      <div class="info-row">
                        <span class="label">Частота:</span>
                        <input v-model="newMedication.frequency" placeholder="Частота" />
                      </div>
                      <div class="info-row">
                        <span class="label">Длительность:</span>
                        <input v-model="newMedication.duration" placeholder="Длительность" />
                      </div>
                      <div class="info-row">
                        <span class="label">Заметки:</span>
                        <textarea v-model="newMedication.individual_notes" placeholder="Индивидуальные заметки" rows="3"></textarea>
                      </div>
                      <div class="controls">
                        <button @click="createMedication(prescription.id)">Добавить</button>
                        <button @click="showNewMedicationForm[prescription.id] = false">Отмена</button>
                      </div>
                    </div>
                    <div v-if="editingMedication[prescription.id]" class="edit-medication-form">
                      <h5>Редактировать медикамент</h5>
                      <div v-if="localErrors.editMedication" class="error">{{ localErrors.editMedication }}</div>
                      <div class="info-row">
                        <span class="label">Препарат:</span>
                        <select v-model="editingMedication[prescription.id].medication">
                          <option :value="null">Выберите препарат</option>
                          <option v-for="med in medications" :key="med.id" :value="med.id">{{ med.name }} ({{ med.form }})</option>
                        </select>
                      </div>
                      <div class="info-row">
                        <span class="label">Дозировка:</span>
                        <input v-model="editingMedication[prescription.id].dosage" placeholder="Дозировка" />
                      </div>
                      <div class="info-row">
                        <span class="label">Частота:</span>
                        <input v-model="editingMedication[prescription.id].frequency" placeholder="Частота" />
                      </div>
                      <div class="info-row">
                        <span class="label">Длительность:</span>
                        <input v-model="editingMedication[prescription.id].duration" placeholder="Длительность" />
                      </div>
                      <div class="info-row">
                        <span class="label">Заметки:</span>
                        <textarea v-model="editingMedication[prescription.id].individual_notes" placeholder="Индивидуальные заметки" rows="3"></textarea>
                      </div>
                      <div class="controls">
                        <button @click="saveMedication(prescription.id)">Сохранить</button>
                        <button @click="cancelEditingMedication(prescription.id)">Отмена</button>
                      </div>
                    </div>
                  </div>
                </div>
                <p v-else>Назначений нет.</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <p v-if="loading">Загрузка...</p>
    </div>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAuthStore } from '@/stores';
import { api } from '../api/medical_card'; // Импортируем настроенный api
const API_URL = 'http://127.0.0.1:8000/medical_card/'; // Добавляем API_URL
import {
  getMedicalCardById,
  updateMedicalCard,
  createMedicalCardEntry,
  getMedicalCardEntryById,
  updateMedicalCardEntry,
  getMedicalCardEntryFiles,
  uploadMedicalCardEntryFile,
  getPrescriptions,
  createPrescription,
  getPrescriptionMedications,
  createPrescriptionMedication,
  updatePrescriptionMedication,
  deletePrescriptionMedication,
} from '../api/medical_card';
import {
  getDiseases,
  getMedications,
} from 'src/modules/catalog_medical_data/api/catalog_medical_data';
import {
  getHospitals,
} from 'src/modules/medical_hub/api/medical_hub';

export default {
  name: 'MedicalCardDetail',
  setup() {
    const route = useRoute();
    const router = useRouter();
    const authStore = useAuthStore();

    const MedicalCardEntryPagination = {
      pageSize: 10,
    };

    const medicalCard = ref(null);
    const editedMedicalCard = ref({
      blood_type: '',
      allergies: '',
      chronic_diseases: '',
      attachment_hospital_id: null,
    });
    const loading = ref(false);
    const globalError = ref('');
    const localErrors = reactive({
      newEntry: '',
      editEntry: '',
      uploadFile: '',
      newPrescription: '',
      newMedication: '',
      editMedication: '',
    });
    const isEditingCard = ref(false);

    const hospitals = ref([]);
    const loadingHospitals = ref(false);
    const hospitalError = ref('');

    const newEntry = reactive({
      visit_date: '',
      diagnosis: null,
      custom_diagnosis: '',
      custom_treatment: '',
      notes: '',
      hospital_id: null,
    });
    const showNewEntryForm = ref(false);
    const diseases = ref([]);
    const medications = ref([]);
    const selectedEntry = ref(null);
    const editedEntry = reactive({});
    const isEditingEntry = ref(false);
    const prescriptions = ref([]);
    const showNewPrescriptionForm = ref(false);
    const newPrescription = reactive({ administration_notes: '' });
    const showNewMedicationForm = ref({});
    const newMedication = reactive({
      medication: null,
      dosage: '',
      frequency: '',
      duration: '',
      individual_notes: '',
    });
    const editingMedication = ref({});
    const selectedFile = ref(null);
    const fileInput = ref(null);

    const currentPage = ref(1);
    const totalPages = computed(() => {
      if (!medicalCard.value?.entries?.count) return 1;
      return Math.ceil(medicalCard.value.entries.count / MedicalCardEntryPagination.pageSize);
    });

    const displayDiagnosis = computed(() => {
      if (!selectedEntry.value) return 'Не указано';
      if (selectedEntry.value.diagnosis && diseases.value.length) {
        return diseases.value.find(d => d.id === selectedEntry.value.diagnosis)?.name || 'Не указано';
      }
      return selectedEntry.value.custom_diagnosis || 'Не указано';
    });

    const checkAuth = () => {
      if (!authStore.isAuthenticated) {
        globalError.value = 'Вы не авторизованы. Перенаправляем на страницу входа...';
        setTimeout(() => router.push('/login'), 2000);
        return false;
      }
      return true;
    };

    const handleAuthError = async (err) => {
      if (err.response?.status === 401 || err.response?.status === 403) {
        globalError.value = 'Ошибка авторизации. Выполняется выход...';
        await authStore.logout();
        setTimeout(() => router.push('/login'), 2000);
        return true;
      }
      return false;
    };

    const fetchMedicalCard = async (url = null) => {
      if (!checkAuth()) return;
      loading.value = true;
      globalError.value = '';
      try {
        let response;
        if (url) {
          const relativeUrl = url.replace(API_URL, '');
          response = await api.get(relativeUrl);
        } else {
          response = await getMedicalCardById(route.params.id);
        }
        medicalCard.value = response.data;
        editedMedicalCard.value = {
          blood_type: response.data.blood_type || '',
          allergies: response.data.allergies || '',
          chronic_diseases: response.data.chronic_diseases || '',
          attachment_hospital_id: response.data.attachment_hospital_info?.id || null,
        };
      } catch (err) {
        if (await handleAuthError(err)) return;
        globalError.value = err.response?.data?.detail || 'Ошибка загрузки карты';
      } finally {
        loading.value = false;
      }
    };

    const startEditingCard = () => (isEditingCard.value = true);

    const cancelEditingCard = () => {
      isEditingCard.value = false;
      editedMedicalCard.value = {
        blood_type: medicalCard.value.blood_type || '',
        allergies: medicalCard.value.allergies || '',
        chronic_diseases: medicalCard.value.chronic_diseases || '',
        attachment_hospital_id: medicalCard.value.attachment_hospital_info?.id || null,
      };
    };

    const saveCardChanges = async () => {
      if (!checkAuth()) return;
      loading.value = true;
      try {
        const response = await updateMedicalCard(route.params.id, {
          blood_type: editedMedicalCard.value.blood_type,
          allergies: editedMedicalCard.value.allergies,
          chronic_diseases: editedMedicalCard.value.chronic_diseases,
          attachment_hospital_id: editedMedicalCard.value.attachment_hospital_id,
        });
        medicalCard.value = response.data;
        isEditingCard.value = false;
      } catch (err) {
        if (await handleAuthError(err)) return;
        globalError.value = err.response?.data?.detail || 'Ошибка сохранения карты';
      } finally {
        loading.value = false;
      }
    };

    const fetchDiseases = async () => {
      if (!checkAuth()) return;
      try {
        const response = await getDiseases();
        diseases.value = response.data.results || response.data;
      } catch (err) {
        if (await handleAuthError(err)) return;
        globalError.value = 'Ошибка загрузки заболеваний';
      }
    };

    const fetchHospitals = async () => {
      if (!checkAuth()) return;
      loadingHospitals.value = true;
      hospitalError.value = '';
      try {
        let url = null;
        do {
          const response = await getHospitals(url ? url : undefined);
          const data = response.data;
          const newHospitals = data.results || data;
          hospitals.value = hospitals.value.concat(newHospitals);
          url = data.next;
        } while (url);
      } catch (err) {
        if (await handleAuthError(err)) return;
        hospitalError.value = err.response?.data?.detail || 'Ошибка загрузки списка больниц';
        console.error('Ошибка при загрузке больниц:', err);
      } finally {
        loadingHospitals.value = false;
      }
    };

    const fetchMedications = async () => {
      if (!checkAuth()) return;
      try {
        const response = await getMedications();
        medications.value = response.data.results || response.data;
      } catch (err) {
        if (await handleAuthError(err)) return;
        globalError.value = 'Ошибка загрузки медикаментов';
      }
    };

    const clearDiagnosis = () => {
      if (newEntry.custom_diagnosis) newEntry.diagnosis = null;
    };

    const clearDiagnosisForEdit = () => {
      if (editedEntry.custom_diagnosis) editedEntry.diagnosis = null;
    };

    const resetNewEntry = () => {
      Object.assign(newEntry, {
        visit_date: '',
        diagnosis: null,
        custom_diagnosis: '',
        custom_treatment: '',
        notes: '',
        hospital_id: null,
      });
    };

    const fetchEntries = async (url = null) => {
      if (!checkAuth()) return;
      loading.value = true;
      globalError.value = '';
      try {
        let response;
        if (url) {
          const relativeUrl = url.replace(API_URL, '');
          response = await api.get(relativeUrl);
        } else {
          response = await getMedicalCardById(route.params.id);
        }
        medicalCard.value.entries = response.data.entries;
        if (url) {
          const urlParams = new URLSearchParams(url.split('?')[1]);
          currentPage.value = parseInt(urlParams.get('page')) || 1;
        } else {
          currentPage.value = 1;
        }
      } catch (err) {
        if (await handleAuthError(err)) return;
        globalError.value = err.response?.data?.detail;
      } finally {
        loading.value = false;
      }
    };

    const createEntry = async () => {
      if (!checkAuth()) return;
      if (!newEntry.visit_date) {
        localErrors.newEntry = 'Дата визита обязательна';
        return;
      }
      if (!newEntry.diagnosis && !newEntry.custom_diagnosis) {
        localErrors.newEntry = 'Укажите диагноз';
        return;
      }
      loading.value = true;
      localErrors.newEntry = '';
      try {
        const response = await createMedicalCardEntry(route.params.id, { ...newEntry });
        await fetchEntries();
        showNewEntryForm.value = false;
        resetNewEntry();
      } catch (err) {
        if (await handleAuthError(err)) return;
        localErrors.newEntry = err.response?.data?.detail || 'Ошибка создания записи';
      } finally {
        loading.value = false;
      }
    };

    const fetchEntryDetails = async (entryId) => {
      if (!checkAuth()) return;
      try {
        const response = await getMedicalCardEntryById(route.params.id, entryId);
        selectedEntry.value = response.data;
        if (selectedEntry.value.diagnosis && selectedEntry.value.disease_url) {
          const diseaseRelativeUrl = selectedEntry.value.disease_url.replace('http://127.0.0.1:8000/', '');
          const diseaseResponse = await api.get(diseaseRelativeUrl);
          selectedEntry.value.get_diagnosis = diseaseResponse.data.name;
        }
        await fetchEntryFiles(entryId);
        await fetchEntryPrescriptions(entryId);
      } catch (err) {
        if (await handleAuthError(err)) return;
        globalError.value = err.response?.data?.detail || 'Ошибка загрузки записи';
      }
    };

    const startEditingEntry = () => {
      isEditingEntry.value = true;
      Object.assign(editedEntry, selectedEntry.value);
    };

    const cancelEditingEntry = () => {
      isEditingEntry.value = false;
      Object.assign(editedEntry, {});
    };

    const saveEditedEntry = async () => {
      if (!checkAuth()) return;
      if (!editedEntry.visit_date) {
        localErrors.editEntry = 'Дата визита обязательна';
        return;
      }
      loading.value = true;
      localErrors.editEntry = '';
      try {
        const response = await updateMedicalCardEntry(route.params.id, selectedEntry.value.id, { ...editedEntry });
        Object.assign(selectedEntry.value, response.data);
        medicalCard.value.entries.results = medicalCard.value.entries.results.map(entry =>
          entry.id === selectedEntry.value.id ? response.data : entry
        );
        isEditingEntry.value = false;
      } catch (err) {
        if (await handleAuthError(err)) return;
        localErrors.editEntry = err.response?.data?.detail || 'Ошибка сохранения записи';
      } finally {
        loading.value = false;
      }
    };

    const fetchEntryFiles = async (entryId) => {
      if (!checkAuth()) return;
      try {
        const response = await getMedicalCardEntryFiles(entryId);
        selectedEntry.value.files = response.data.results || response.data;
      } catch (err) {
        if (await handleAuthError(err)) return;
        if (!localErrors.uploadFile) {
          localErrors.uploadFile = err.response?.data?.detail || 'Ошибка загрузки файлов';
        }
      }
    };

    const onFileChange = (event) => {
      selectedFile.value = event.target.files[0];
    };

    const uploadFile = async () => {
      if (!checkAuth()) return;
      if (!selectedFile.value || !selectedEntry.value) {
        localErrors.uploadFile = 'Файл или запись не выбраны';
        return;
      }
      loading.value = true;
      localErrors.uploadFile = '';
      try {
        const response = await uploadMedicalCardEntryFile(selectedEntry.value.id, selectedFile.value);
        if (response.status === 201 || response.status === 200) {
          selectedEntry.value.files.push(response.data);
          selectedFile.value = null;
          if (fileInput.value) fileInput.value.value = '';
          await fetchEntryFiles(selectedEntry.value.id);
        } else {
          throw new Error(`Неожиданный статус ответа: ${response.status}`);
        }
      } catch (err) {
        console.error('Ошибка при загрузке файла:', err);
        if (await handleAuthError(err)) return;
        localErrors.uploadFile = err.response?.data?.detail;
      } finally {
        loading.value = false;
      }
    };

    const fetchEntryPrescriptions = async (entryId) => {
      if (!checkAuth()) return;
      try {
        const response = await getPrescriptions(entryId);
        prescriptions.value = (response.data.results || response.data).map(p => ({
          ...p,
          showMedications: false,
          medications: p.medications || [],
        }));
      } catch (err) {
        if (await handleAuthError(err)) return;
        globalError.value = 'Ошибка загрузки назначений';
      }
    };

    const createNewPrescription = async () => {
      if (!checkAuth()) return;
      if (!selectedEntry.value) return;
      loading.value = true;
      localErrors.newPrescription = '';
      try {
        const response = await createPrescription(selectedEntry.value.id, { ...newPrescription });
        prescriptions.value.unshift({ ...response.data, showMedications: false, medications: [] });
        showNewPrescriptionForm.value = false;
        newPrescription.administration_notes = '';
      } catch (err) {
        if (await handleAuthError(err)) return;
        localErrors.newPrescription = err.response?.data?.detail || 'Ошибка создания назначения';
      } finally {
        loading.value = false;
      }
    };

    const toggleMedications = async (prescriptionId) => {
      const prescription = prescriptions.value.find(p => p.id === prescriptionId);
      if (!prescription) return;
      if (!prescription.showMedications && !prescription.medications.length) {
        await fetchPrescriptionMedications(prescriptionId);
      }
      prescription.showMedications = !prescription.showMedications;
    };

    const fetchPrescriptionMedications = async (prescriptionId) => {
      if (!checkAuth()) return;
      try {
        const response = await getPrescriptionMedications(prescriptionId);
        const prescription = prescriptions.value.find(p => p.id === prescriptionId);
        if (prescription) prescription.medications = response.data.results || response.data;
      } catch (err) {
        if (await handleAuthError(err)) return;
        localErrors.newMedication = 'Ошибка загрузки медикаментов';
      }
    };

    const createMedication = async (prescriptionId) => {
      if (!checkAuth()) return;
      if (!newMedication.medication) {
        localErrors.newMedication = 'Препарат обязателен';
        return;
      }
      loading.value = true;
      localErrors.newMedication = '';
      try {
        const response = await createPrescriptionMedication(prescriptionId, { ...newMedication });
        const prescription = prescriptions.value.find(p => p.id === prescriptionId);
        prescription.medications.push(response.data);
        showNewMedicationForm.value[prescriptionId] = false;
        Object.assign(newMedication, { medication: null, dosage: '', frequency: '', duration: '', individual_notes: '' });
      } catch (err) {
        if (await handleAuthError(err)) return;
        localErrors.newMedication = err.response?.data?.detail || 'Ошибка добавления медикамента';
      } finally {
        loading.value = false;
      }
    };

    const startEditingMedication = (prescriptionId, med) => {
      editingMedication.value[prescriptionId] = { ...med };
    };

    const saveMedication = async (prescriptionId) => {
      if (!checkAuth()) return;
      loading.value = true;
      localErrors.editMedication = '';
      try {
        const response = await updatePrescriptionMedication(prescriptionId, editingMedication.value[prescriptionId].id, {
          ...editingMedication.value[prescriptionId],
        });
        const prescription = prescriptions.value.find(p => p.id === prescriptionId);
        prescription.medications = prescription.medications.map(m =>
          m.id === response.data.id ? response.data : m
        );
        editingMedication.value[prescriptionId] = null;
      } catch (err) {
        if (await handleAuthError(err)) return;
        localErrors.editMedication = err.response?.data?.detail || 'Ошибка сохранения медикамента';
      } finally {
        loading.value = false;
      }
    };

    const cancelEditingMedication = (prescriptionId) => {
      editingMedication.value[prescriptionId] = null;
    };

    const deleteMedication = async (prescriptionId, medicationId) => {
      if (!checkAuth()) return;
      if (!confirm('Вы уверены?')) return;
      loading.value = true;
      try {
        await deletePrescriptionMedication(prescriptionId, medicationId);
        const prescription = prescriptions.value.find(p => p.id === prescriptionId);
        prescription.medications = prescription.medications.filter(m => m.id !== medicationId);
      } catch (err) {
        if (await handleAuthError(err)) return;
        localErrors.editMedication = err.response?.data?.detail || 'Ошибка удаления медикамента';
      } finally {
        loading.value = false;
      }
    };

    onMounted(async () => {
      await authStore.initializeAuth();
      if (!checkAuth()) return;
      fetchMedicalCard();
      fetchDiseases();
      fetchHospitals();
      fetchMedications();
      fetchEntries();
    });

    return {
      medicalCard,
      editedMedicalCard,
      loading,
      globalError,
      localErrors,
      isEditingCard,
      startEditingCard,
      cancelEditingCard,
      saveCardChanges,
      newEntry,
      showNewEntryForm,
      diseases,
      hospitals,
      loadingHospitals,
      hospitalError,
      medications,
      selectedEntry,
      editedEntry,
      isEditingEntry,
      prescriptions,
      showNewPrescriptionForm,
      newPrescription,
      showNewMedicationForm,
      newMedication,
      editingMedication,
      selectedFile,
      displayDiagnosis,
      createEntry,
      fetchEntryDetails,
      startEditingEntry,
      cancelEditingEntry,
      saveEditedEntry,
      onFileChange,
      uploadFile,
      createNewPrescription,
      toggleMedications,
      createMedication,
      clearDiagnosis,
      clearDiagnosisForEdit,
      startEditingMedication,
      saveMedication,
      cancelEditingMedication,
      deleteMedication,
      currentPage,
      totalPages,
      fetchEntries,
      MedicalCardEntryPagination,
      fileInput,
    };
  },
};
</script>

<style scoped>
:root {
  --primary-color: #000;
  --hover-color: #333;
  --font-size-base: 16px;
}

.medical-card-detail-container {
  display: flex;
  justify-content: center;
  margin-top: 20vh;
  background-color: #fff;
  min-height: 100vh;
}

.medical-card-detail-box {
  width: 90%;
  max-width: 1200px;
  padding: 30px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
}

h2, h3, h4, h5 {
  margin-bottom: 20px;
  font-size: 22px;
  font-weight: bold;
  color: #333;
}

h3 {
  font-size: 20px;
}

h4 {
  font-size: 18px;
}

h5 {
  font-size: 16px;
}

.global-error {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 1000;
  background: #ffebee;
  padding: 10px;
  border-radius: 4px;
  color: red;
  font-size: 16px;
  max-width: 300px;
}

.error {
  color: red;
  margin-top: 10px;
  font-size: 16px;
}

.loading-message {
  color: #555;
  font-size: 14px;
  margin-top: 5px;
}

.no-data-message {
  color: #888;
  font-size: 14px;
  margin-top: 5px;
}

.hospital-select-wrapper {
  flex: 1;
}

.main-content {
  display: flex;
  flex-direction: column;
  gap: 30px;
  width: 100%;
}

.top-section {
  display: flex;
  gap: 30px;
  width: 100%;
}

.left-top,
.right-top {
  flex: 1;
  min-width: 0;
  text-align: left;
}

.bottom-section {
  display: flex;
  gap: 30px;
  width: 100%;
}

.left-bottom,
.right-bottom {
  flex: 1;
  min-width: 0;
  text-align: left;
}

.section-divider {
  border: 0;
  border-top: 1px solid #ccc;
  margin: 20px 10px;
  width: calc(100% - 20px);
}

.controls {
  margin-top: 20px;
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
}

.medical-card-detail-container .controls button {
  padding: 10px 20px;
  background-color: var(--primary-color, #000);
  color: white;
  border: none;
  border-radius: 20px;
  font-size: var(--font-size-base, 16px);
  font-weight: bold;
  cursor: pointer;
  transition: background 0.3s ease;
  white-space: nowrap;
}

.medical-card-detail-container .controls button:hover {
  background-color: var(--hover-color, #333);
}

.medical-card-detail-container .controls button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.medical-card-info {
  text-align: left;
}

.medical-card-details {
  flex: 1;
}

.info-row {
  display: flex;
  margin-bottom: 15px;
  align-items: flex-start;
  width: 100%;
}

.label {
  font-weight: 600;
  color: #333;
  width: 150px;
  min-width: 150px;
  font-size: 16px;
  word-break: break-word;
}

.value {
  font-size: 16px;
  color: #555;
  white-space: pre-wrap;
  word-break: break-word;
}

.edit-form input,
.edit-form textarea,
.edit-form select,
.new-entry-form input,
.new-entry-form textarea,
.new-entry-form select,
.new-prescription-form textarea,
.new-medication-form input,
.new-medication-form textarea,
.new-medication-form select,
.edit-medication-form input,
.edit-medication-form textarea,
.edit-medication-form select,
.edit-entry-form input,
.edit-entry-form textarea,
.edit-entry-form select {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 16px;
  width: 100%;
  max-width: 300px;
  box-sizing: border-box;
  resize: vertical;
}

.entries-section {
  margin-top: 0;
}

.medical-card-detail-container .entries-section button,
.medical-card-detail-container .prescriptions-section button {
  padding: 10px 20px;
  background-color: var(--primary-color, #000);
  color: white;
  border: none;
  border-radius: 20px;
  font-size: var(--font-size-base, 16px);
  font-weight: bold;
  cursor: pointer;
  transition: background 0.3s ease;
}

.medical-card-detail-container .entries-section button:hover,
.medical-card-detail-container .prescriptions-section button:hover {
  background-color: var(--hover-color, #333);
}

.new-entry-form,
.new-prescription-form,
.new-medication-form,
.edit-medication-form,
.edit-entry-form {
  border: 1px solid #ccc;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
  background-color: #f9f9f9;
  width: 100%;
  box-sizing: border-box;
}

.entries-list {
  margin-top: 20px;
}

.entries-table {
  width: 100%;
  border-collapse: collapse;
  table-layout: fixed;
}

.entries-table th,
.entries-table td {
  padding: 10px;
  border: 1px solid #ccc;
  text-align: left;
  font-size: 14px;
  word-break: break-word;
}

.entries-table th {
  background-color: #e0e0e0;
  font-weight: bold;
}

.medical-card-detail-container .entries-table td button {
  padding: 8px 16px;
  background-color: var(--primary-color, #000);
  color: white;
  border: none;
  border-radius: 20px;
  font-size: 14px;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.3s ease;
}

.medical-card-detail-container .entries-table td button:hover {
  background-color: var(--hover-color, #333);
}

.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
  margin-top: 20px;
}

.pagination button {
  padding: 8px 16px;
  background-color: var(--primary-color, #000);
  color: white;
  border: none;
  border-radius: 20px;
  font-size: 14px;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.3s ease;
}

.pagination button:hover {
  background-color: var(--hover-color, #333);
}

.pagination button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.pagination span {
  font-size: 14px;
  color: #333;
}

.entry-details {
  margin-top: 0;
  width: 100%;
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.files-section,
.prescriptions-section {
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
  margin: 0 auto;
}

.files-section {
  margin-top: 0;
}

.file-item {
  margin-bottom: 10px;
}

.file-item a {
  color: #007bff;
  text-decoration: none;
}

.file-item a:hover {
  text-decoration: underline;
}

.file-upload {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
  flex-wrap: wrap;
}

.file-upload input[type="file"] {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 14px;
  flex: 1;
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.medical-card-detail-container .file-upload button {
  padding: 8px 16px;
  background-color: var(--primary-color, #000);
  color: white;
  border: none;
  border-radius: 20px;
  font-size: 14px;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.3s ease;
  flex-shrink: 0;
}

.medical-card-detail-container .file-upload button:hover {
  background-color: var(--hover-color, #333);
}

.prescriptions-section {
  margin-top: 0;
}

.prescriptions-list {
  margin-top: 20px;
}

.prescription-item {
  border-bottom: 1px solid #ccc;
  padding: 10px 0;
}

.prescription-item button {
  padding: 8px 16px;
  background-color: var(--primary-color, #000);
  color: white;
  border: none;
  border-radius: 20px;
  font-size: 14px;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.3s ease;
  width: 180px;
  margin-right: 10px;
  margin-bottom: 10px;
}

.prescription-item button:hover {
  background-color: var(--hover-color, #333);
}

.medications-list {
  margin-top: 10px;
  padding-left: 20px;
}

.medication-item {
  margin-bottom: 10px;
  padding: 10px;
  background-color: #fff;
  border: 1px solid #e0e0e0;
  border-radius: 6px;
}

.medical-card-detail-container .medication-actions button {
  padding: 8px 16px;
  background-color: var(--primary-color, #000);
  color: white;
  border: none;
  border-radius: 20px;
  font-size: 14px;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.3s ease;
}

.medical-card-detail-container .medication-actions button:hover {
  background-color: var(--hover-color, #333);
}
</style>