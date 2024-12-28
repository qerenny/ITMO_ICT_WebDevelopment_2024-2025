<template>
  <v-container class="mt-4" max-width="400">
    <v-card class="pa-4 elevated-card">
      <h2>Авторизация</h2>
      <v-form @submit.prevent="handleLogin">
        <v-text-field
          v-model="form.username"
          label="Логин"
          required
        ></v-text-field>
        <v-text-field
          v-model="form.password"
          label="Пароль"
          type="password"
          required
        ></v-text-field>
        <v-btn variant="outlined" color="primary" type="submit">
          Войти
        </v-btn>
        <v-btn variant="outlined" color="error" @click="$router.push('/start')">
          Назад
        </v-btn>
      </v-form>
    </v-card>
  </v-container>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Login',
  data() {
    return {
      form: {
        username: '',
        password: ''
      }
    }
  },
  methods: {
    async handleLogin() {
      try {
        const response = await axios.post('http://127.0.0.1:8000/auth/token/login/', {
          username: this.form.username,
          password: this.form.password
        })
        const token = response.data.auth_token
        localStorage.setItem('token', token)
        this.$router.push({ name: 'home' })
      } catch (error) {
        console.error(error)
      }
    }
  }
}
</script>