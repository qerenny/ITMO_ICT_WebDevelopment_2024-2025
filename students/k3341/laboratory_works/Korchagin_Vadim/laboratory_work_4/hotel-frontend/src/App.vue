<template>
  <v-app>
    <!-- Показываем панель, только если пользователь авторизован -->
    <NavigationBar v-if="userLoggedIn" />
    <v-main>
      <!-- <v-container fluid class="pa-4"> -->
        <router-view />
      <!-- </v-container> -->
    </v-main>
  </v-app>
</template>

<script>
import NavigationBar from './components/NavigationBar.vue'

export default {
  name: 'App',
  components: { NavigationBar },
  data() {
    return {
      userLoggedIn: false
    }
  },
  created() {
    this.checkAuth()
  },
  watch: {
    // Будем следить за сменой маршрута
    $route() {
      this.checkAuth()
    }
  },
  methods: {
    checkAuth() {
      // Если токен в localStorage есть — пользователь авторизован
      const token = localStorage.getItem('token')
      this.userLoggedIn = !!token
    }
  }
}
</script>