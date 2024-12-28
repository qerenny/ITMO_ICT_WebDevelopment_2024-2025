<template>
    <v-container>
      <h2>Номера</h2>
      <v-data-table :headers="headers" :items="rooms" class="elevation-1 mt-4">
        <template #item.actions="{ item }">
          <v-btn small @click="editRoom(item)">Ред.</v-btn>
          <v-btn small color="error" @click="deleteRoom(item.room_id)">Удалить</v-btn>
        </template>
      </v-data-table>
      <v-btn color="primary" class="mt-4" @click="openCreateDialog">Добавить номер</v-btn>
  
      <v-dialog v-model="dialog" max-width="600px">
        <v-card>
          <v-card-title>{{ roomForm.room_id ? 'Редактирование номера' : 'Новый номер' }}</v-card-title>
          <v-card-text>
            <v-select
              v-model="roomForm.room_type"
              :items="roomTypes"
              label="Тип номера"
            ></v-select>
            <v-text-field
              v-model="roomForm.cost_per_day"
              label="Стоимость в сутки"
              type="number"
            ></v-text-field>
            <v-text-field
              v-model="roomForm.floor"
              label="Этаж"
              type="number"
            ></v-text-field>
            <v-switch
              v-model="roomForm.is_available"
              label="Свободен?"
            ></v-switch>
            <v-text-field
              v-model="roomForm.phone_number"
              label="Телефон"
            ></v-text-field>
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" @click="createOrUpdateRoom">Сохранить</v-btn>
            <v-btn text @click="dialog = false">Отмена</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-container>
  </template>
  
  <script>
  import axios from 'axios'
  export default {
    name: 'Rooms',
    data() {
      return {
        rooms: [],
        dialog: false,
        roomForm: {
          room_id: null,
          room_type: 'SINGLE',
          cost_per_day: 0,
          floor: 1,
          is_available: true,
          phone_number: ''
        },
        roomTypes: ['SINGLE', 'DOUBLE', 'TRIPLE'],
        headers: [
          { text: 'ID', value: 'room_id' },
          { text: 'Тип', value: 'room_type' },
          { text: 'Стоимость', value: 'cost_per_day' },
          { text: 'Этаж', value: 'floor' },
          { text: 'Свободен?', value: 'is_available' },
          { text: 'Телефон', value: 'phone_number' },
          { text: 'Действия', value: 'actions', sortable: false }
        ]
      }
    },
    async created() {
      this.fetchRooms()
    },
    methods: {
      async fetchRooms() {
        const token = localStorage.getItem('token')
        try {
          const response = await axios.get('http://127.0.0.1:8000/api/rooms/', {
            headers: { Authorization: `Token ${token}` }
          })
          this.rooms = response.data
        } catch (error) {
          console.error(error)
        }
      },
      openCreateDialog() {
        this.clearForm()
        this.dialog = true
      },
      clearForm() {
        this.roomForm = {
          room_id: null,
          room_type: 'SINGLE',
          cost_per_day: 0,
          floor: 1,
          is_available: true,
          phone_number: ''
        }
      },
      editRoom(room) {
        this.roomForm = { ...room }
        this.dialog = true
      },
      async createOrUpdateRoom() {
        const token = localStorage.getItem('token')
        try {
          if (this.roomForm.room_id) {
            await axios.put(`http://127.0.0.1:8000/api/rooms/${this.roomForm.room_id}/`, this.roomForm, {
              headers: { Authorization: `Token ${token}` }
            })
          } else {
            await axios.post('http://127.0.0.1:8000/api/rooms/', this.roomForm, {
              headers: { Authorization: `Token ${token}` }
            })
          }
          this.dialog = false
          this.fetchRooms()
        } catch (error) {
          console.error(error)
        }
      },
      async deleteRoom(id) {
        const token = localStorage.getItem('token')
        try {
          await axios.delete(`http://127.0.0.1:8000/api/rooms/${id}/`, {
            headers: { Authorization: `Token ${token}` }
          })
          this.fetchRooms()
        } catch (error) {
          console.error(error)
        }
      }
    }
  }
  </script>