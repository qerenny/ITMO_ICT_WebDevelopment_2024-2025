<template>
    <v-container class="mt-4">
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
        <v-btn color="primary" type="submit">Войти</v-btn>
        <v-btn text @click="$router.push('/start')">Назад</v-btn>
      </v-form>
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
          // Djoser вернёт { auth_token: "..." }
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