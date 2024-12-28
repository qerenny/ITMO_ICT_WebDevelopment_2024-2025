<template>
    <v-container class="mt-4">
      <h2>Мои данные</h2>
      <v-form @submit.prevent="updateProfile">
        <v-text-field
          v-model="profileForm.username"
          label="Логин"
        ></v-text-field>
        <v-text-field
          v-model="profileForm.email"
          label="Email"
        ></v-text-field>
        <v-btn color="primary" type="submit">Сохранить</v-btn>
      </v-form>
  
      <v-divider class="my-5"></v-divider>
  
      <h2>Смена пароля</h2>
      <v-form @submit.prevent="updatePassword">
        <v-text-field
          v-model="passwordForm.current_password"
          type="password"
          label="Текущий пароль"
        ></v-text-field>
        <v-text-field
          v-model="passwordForm.new_password"
          type="password"
          label="Новый пароль"
        ></v-text-field>
        <v-text-field
          v-model="passwordForm.re_new_password"
          type="password"
          label="Повтор пароля"
        ></v-text-field>
        <v-btn color="primary" type="submit">Изменить</v-btn>
      </v-form>
    </v-container>
  </template>
  
  <script>
  import axios from 'axios'
  
  export default {
    name: 'Profile',
    data() {
      return {
        profileForm: {
          username: '',
          email: ''
        },
        passwordForm: {
          current_password: '',
          new_password: '',
          re_new_password: ''
        }
      }
    },
    async created() {
      await this.fetchProfile()
    },
    methods: {
      async fetchProfile() {
        try {
          const token = localStorage.getItem('token')
          const response = await axios.get('http://127.0.0.1:8000/auth/users/me/', {
            headers: { Authorization: `Token ${token}` }
          })
          this.profileForm.username = response.data.username
          this.profileForm.email = response.data.email
        } catch (error) {
          console.error(error)
        }
      },
      async updateProfile() {
        try {
          const token = localStorage.getItem('token')
          await axios.patch(
            'http://127.0.0.1:8000/auth/users/me/',
            {
              username: this.profileForm.username,
              email: this.profileForm.email
            },
            { headers: { Authorization: `Token ${token}` } }
          )
        } catch (error) {
          console.error(error)
        }
      },
      async updatePassword() {
        try {
          const token = localStorage.getItem('token')
          await axios.post(
            'http://127.0.0.1:8000/auth/users/set_password/',
            {
              current_password: this.passwordForm.current_password,
              new_password: this.passwordForm.new_password,
              re_new_password: this.passwordForm.re_new_password
            },
            { headers: { Authorization: `Token ${token}` } }
          )
          // Можно сделать разлогин или оставить всё как есть
        } catch (error) {
          console.error(error)
        }
      }
    }
  }
  </script>