<template>
    <v-app-bar app color="primary" dark>
      <v-toolbar-title>Hotel System</v-toolbar-title>
      <v-spacer></v-spacer>
  
      <!-- Общие вкладки для всех авторизованных -->
      <v-btn text to="/">Главная</v-btn>
      <v-btn text to="/profile">Профиль</v-btn>
  
      <!-- Кнопки только для админа -->
      <template v-if="userData.is_staff">
        <v-btn text to="/clients">Клиенты</v-btn>
        <v-btn text to="/staff">Сотрудники</v-btn>
        <v-btn text to="/rooms">Номера</v-btn>
        <v-btn text to="/stays">Проживания</v-btn>
        <v-btn text to="/cleanings">Уборки</v-btn>
        <v-btn text to="/schedules">Расписания</v-btn>
        <v-btn text to="/report">Отчёт</v-btn>
      </template>
  
      <v-btn text @click="logout">Выйти</v-btn>
    </v-app-bar>
  </template>
  
  <script>
  import axios from 'axios'
  
  export default {
    name: 'NavigationBar',
    data() {
      return {
        token: null,
        userData: {}
      }
    },
    created() {
      // проверяем, есть ли токен
      this.token = localStorage.getItem('token')
      if (this.token) {
        this.fetchUser()
      }
    },
    methods: {
      async fetchUser() {
        try {
          let response = await axios.get('http://127.0.0.1:8000/auth/users/me/', {
            headers: { Authorization: `Token ${this.token}` }
          })
          this.userData = response.data
        } catch (error) {
          console.error(error)
        }
      },
      logout() {
        localStorage.removeItem('token')
        this.token = null
        this.userData = {}
        // Отправляем пользователя на /start (или /login)
        this.$router.push('/start')
      }
    }
  }
  </script>