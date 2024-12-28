<template>
    <v-container class="mt-4" max-width="400">
      <h2>Регистрация</h2>
      <v-form @submit.prevent="handleRegister">
        <v-text-field v-model="form.username" label="Логин" required></v-text-field>
        <v-text-field v-model="form.email" label="Email" required></v-text-field>
        <v-text-field
          v-model="form.password"
          label="Пароль"
          type="password"
          required
        ></v-text-field>
        <v-text-field
          v-model="form.password2"
          label="Повтор пароля"
          type="password"
          required
        ></v-text-field>
        <v-btn color="primary" type="submit">Зарегистрироваться</v-btn>
        <v-btn text @click="$router.push('/start')">Назад</v-btn>
      </v-form>
    </v-container>
  </template>
  
  <script>
  import axios from 'axios'
  
  export default {
    name: 'Register',
    data() {
      return {
        form: {
          username: '',
          email: '',
          password: '',
          password2: ''
        }
      }
    },
    methods: {
      async handleRegister() {
        try {
          await axios.post('http://127.0.0.1:8000/auth/users/', {
            username: this.form.username,
            email: this.form.email,
            password: this.form.password,
            re_password: this.form.password2
          })
          // регистрация прошла успешно -> перенаправляем на /login
          this.$router.push('/login')
        } catch (error) {
          console.error(error)
        }
      }
    }
  }
  </script>