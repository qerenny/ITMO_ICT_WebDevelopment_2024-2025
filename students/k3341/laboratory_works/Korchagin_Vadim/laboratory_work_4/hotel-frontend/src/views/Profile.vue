<template>
  <v-container>
    <h2 class="mb-4">Профиль пользователя</h2>
    <v-card class="elevated-card pa-4 mb-4">
      <v-card-title class="text-h5">
        Информация о текущем пользователе
      </v-card-title>
      <v-card-text>
        <div><strong>Имя пользователя:</strong> {{ userData.username }}</div>
        <div><strong>Email:</strong> {{ userData.email }}</div>
        <div><strong>Роль:</strong> {{ userData.is_staff ? 'Администратор' : 'Пользователь' }}</div>
      </v-card-text>
      <v-card-actions class="d-flex justify-center">
        <v-btn
          variant="outlined"
          color="primary"
          @click="editProfile"
        >
          Редактировать профиль
        </v-btn>
        <v-btn
          variant="outlined"
          color="error"
          @click="logout"
        >
          Выйти
        </v-btn>
      </v-card-actions>
    </v-card>

    <v-dialog
      v-model="dialog"
      max-width="500px"
      persistent
    >
      <v-card class="dialog-card pa-6">
        <v-card-title class="dialog-title text-h5">
          Редактирование профиля
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text>
          <v-text-field
            v-model="userForm.username"
            label="Имя пользователя"
          ></v-text-field>
          <v-text-field
            v-model="userForm.email"
            label="Email"
          ></v-text-field>
          <v-text-field
            v-model="userForm.password"
            label="Пароль"
            type="password"
          ></v-text-field>
          <v-text-field
            v-model="userForm.password2"
            label="Повторите пароль"
            type="password"
          ></v-text-field>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions class="d-flex justify-end">
          <v-btn
            variant="outlined"
            color="primary"
            class="mr-2"
            @click="saveProfile"
          >
            Сохранить
          </v-btn>
          <v-btn
            variant="outlined"
            color="error"
            @click="dialog = false"
          >
            Отмена
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Profile',
  data() {
    return {
      userData: {},
      dialog: false,
      userForm: {
        username: '',
        email: '',
        password: '',
        password2: ''
      }
    }
  },
  async created() {
    this.fetchUserData()
  },
  methods: {
    async fetchUserData() {
      const token = localStorage.getItem('token')
      try {
        const response = await axios.get('http://127.0.0.1:8000/auth/users/me/', {
          headers: { Authorization: `Token ${token}` }
        })
        this.userData = response.data
      } catch (error) {
        console.error('Ошибка при загрузке данных пользователя', error)
      }
    },
    editProfile() {
      this.userForm = {
        username: this.userData.username,
        email: this.userData.email,
        password: '',
        password2: ''
      }
      this.dialog = true
    },
    async saveProfile() {
      const token = localStorage.getItem('token')
      if (this.userForm.password !== this.userForm.password2) {
        console.error('Пароли не совпадают')
        return
      }
      try {
        await axios.put('http://127.0.0.1:8000/auth/users/me/', this.userForm, {
          headers: { Authorization: `Token ${token}` }
        })
        this.dialog = false
        this.fetchUserData()
      } catch (error) {
        console.error('Ошибка при обновлении профиля', error)
      }
    },
    logout() {
      localStorage.removeItem('token')
      this.$router.push('/start')
    }
  }
}
</script>