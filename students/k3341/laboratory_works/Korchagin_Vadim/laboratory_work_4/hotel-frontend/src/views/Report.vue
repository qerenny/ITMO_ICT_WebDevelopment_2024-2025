<template>
    <v-container>
      <h2>Отчёт по гостинице</h2>
      <v-select
        :items="[1,2,3,4]"
        v-model="selectedQuarter"
        label="Выберите квартал"
        dense
      ></v-select>
      <v-btn color="primary" class="mt-4" @click="fetchReport">Сформировать отчёт</v-btn>
  
      <div v-if="reportData" class="mt-4">
        <h3>Число клиентов по номерам</h3>
        <ul>
          <li
            v-for="item in reportData.stays_per_room"
            :key="item.room__room_id"
          >
            Номер {{ item.room__room_id }} — Клиентов: {{ item.client_count }}
          </li>
        </ul>
  
        <h3>Количество номеров на этажах</h3>
        <ul>
          <li
            v-for="floorInfo in reportData.rooms_per_floor"
            :key="floorInfo.floor"
          >
            Этаж {{ floorInfo.floor }} — Номеров: {{ floorInfo.room_count }}
          </li>
        </ul>
  
        <h3>Доход по каждому номеру</h3>
        <ul>
          <li
            v-for="roomIncome in reportData.income_per_room"
            :key="roomIncome.room_id"
          >
            Номер {{ roomIncome.room_id }} — Доход: {{ roomIncome.total_income }}
          </li>
        </ul>
  
        <h3>Суммарный доход: {{ reportData.total_income }}</h3>
      </div>
    </v-container>
  </template>
  
  <script>
  import axios from 'axios'
  
  export default {
    name: 'Report',
    data() {
      return {
        selectedQuarter: null,
        reportData: null
      }
    },
    methods: {
      async fetchReport() {
        if (!this.selectedQuarter) return
        const token = localStorage.getItem('token')
        try {
          const response = await axios.get(`http://127.0.0.1:8000/report/?quarter=${this.selectedQuarter}`, {
            headers: { Authorization: `Token ${token}` }
          })
          this.reportData = response.data
        } catch (error) {
          console.error(error)
        }
      }
    }
  }
  </script>