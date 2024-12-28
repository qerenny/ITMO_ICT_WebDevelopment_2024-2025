<template>
  <v-container class="d-flex justify-center">
    <v-card
      class="pa-5 elevated-card"
      width="400"
      height="200"
    >
      <h2>Добро пожаловать в гостиницу!</h2>
      <p>Здесь можно управлять клиентами, сотрудниками, номерами и т. д.</p>
      <v-btn variant="outlined" color="primary" to="/profile" >
        Перейти к профилю
      </v-btn>
    </v-card>
  </v-container>
</template>

<script>
export default {
  name: 'Home'
}
</script>
