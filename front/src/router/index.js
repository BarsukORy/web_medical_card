import { useAuthStore } from '@/stores';
import { createRouter, createWebHistory } from 'vue-router';
import Login from '@/modules/custom_user/views/Login.vue';
import PatientSearch from '@/modules/patient/views/PatientSearch.vue';
import PatientDetail from '@/modules/patient/views/PatientDetail.vue';
import CreatePatient from "@/modules/patient/views/CreatePatient.vue";
import MedicalCardDetail from '@/modules/medical_card/views/MedicalCardDetail.vue';
import Medications from "@/modules/catalog_medical_data/views/Medications.vue";
import Diseases from "@/modules/catalog_medical_data/views/Diseases.vue";


const routes = [
    {
    path: '/login',
    name: 'Login',
    component: Login,
  },
    {
    path: '/patients',
    name: 'PatientSearch',
    component: PatientSearch,
    meta: { requiresAuth: true }, // Требуется авторизация
  },
    {
    path: '/patients/:id',
    name: 'PatientDetail',
    component: PatientDetail,
    meta: { requiresAuth: true },
  },
    {
    path: '/create-patient',
    name: 'CreatePatient',
    component: CreatePatient,
      meta: { requiresAuth: true },
  },
    {
     path: '/medical-cards/:id',
     name: 'MedicalCardDetail',
     component: MedicalCardDetail,
     meta: { requiresAuth: true }, // Требуется авторизация
  },
    {
  path: '/medications',
  name: 'Medications',
  component: Medications,
  meta: { requiresAuth: true },
  },
    {
  path: '/diseases',
  name: 'Diseases',
  component: Diseases,
  meta: { requiresAuth: true },
  },
    {
    path: '/',
    redirect: '/login', // По умолчанию перенаправляем на страницу логина
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login'); // Если не авторизован, перенаправляем на логин
  } else {
    next();
  }
});

export default router;