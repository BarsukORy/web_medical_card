<template>
  <div class="login-container">
    <div class="login-box">
      <h2>Добрый день</h2>
      <p>Пожалуйста, авторизуйтесь</p>
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="username">Логин</label>
          <input
            type="text"
            id="username"
            v-model="credentials.username"
            required
            placeholder="Введите логин"
          />
        </div>
        <div class="form-group">
          <label for="password">Пароль</label>
          <input
            type="password"
            id="password"
            v-model="credentials.password"
            required
            placeholder="Введите пароль"
          />
        </div>
        <button type="submit" :disabled="loading">
          {{ loading ? "Вход..." : "Войти" }}
        </button>
        <p v-if="error" class="error">{{ error }}</p>
      </form>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores";

export default {
  setup() {
    const authStore = useAuthStore();
    const router = useRouter();
    const credentials = ref({ username: "", password: "" });
    const loading = ref(false);
    const error = ref("");

    const handleLogin = async () => {
      loading.value = true;
      error.value = "";
      try {
        await authStore.login(credentials.value);
        router.push("/patients");
      } catch (err) {
        error.value = "Ошибка авторизации";
      } finally {
        loading.value = false;
      }
    };

    return { credentials, loading, error, handleLogin };
  },
};
</script>

<style scoped>
/* Контейнер с отступом сверху */
.login-container {
  display: flex;
  justify-content: center;
  margin-top: 20vh; /* Опускаем форму вниз */
  background-color: #fff;
}

/* Блок формы */
.login-box {
  width: 400px;
  padding: 30px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
}

h2 {
  margin-bottom: 10px;
  font-size: 22px;
  font-weight: bold;
  color: #333;
}

p {
  margin-bottom: 20px;
  color: #666;
  font-size: 14px;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.login-form button {
  margin-top: 30px;
}

.form-group {
  display: flex;
  flex-direction: column;
  text-align: left;
}

label {
  margin-bottom: 5px;
  font-weight: 600;
  color: #333;
  font-size: 14px;
}

input {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 16px;
}

button {
  padding: 12px;
  background-color: #000; /* Черная кнопка */
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
</style>
