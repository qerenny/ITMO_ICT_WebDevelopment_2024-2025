<template>
    <v-container>
      <h2>Проживания (Stays)</h2>
      <v-data-table :headers="headers" :items="stays">
        <template #item.actions="{ item }">
          <v-btn small @click="editStay(item)">Ред.</v-btn>
          <v-btn small color="error" @click="deleteStay(item.stay_id)">Удалить</v-btn>
        </template>
      </v-data-table>
  
      <v-btn color="primary" class="mt-4" @click="openCreateDialog">Добавить проживание</v-btn>
  
      <v-dialog v-model="dialog" max-width="600px">
        <v-card>
          <v-card-title>
            {{ stayForm.stay_id ? 'Редактирование' : 'Новое' }} проживание
          </v-card-title>
          <v-card-text>
            <v-select
              label="Клиент"
              v-model="stayForm.client_id"
              :items="availableClients"
              :item-text="(c) => c.last_name + ' ' + c.first_name"
              :item-value="(c) => c.client_id"
            />
            <v-select
              label="Номер"
              v-model="stayForm.room_id"
              :items="availableRooms"
              :item-text="(r) => 'Номер ' + r.room_id"
              :item-value="(r) => r.room_id"
            />
            <v-text-field
              v-model="stayForm.check_in_date"
              label="Дата заезда (YYYY-MM-DD)"
            ></v-text-field>
            <v-text-field
              v-model="stayForm.check_out_date"
              label="Дата выезда (YYYY-MM-DD)"
            ></v-text-field>
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" @click="createOrUpdateStay">Сохранить</v-btn>
            <v-btn text @click="dialog = false">Отмена</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-container>
  </template>
  
  <script>
  import axios from 'axios'
  
  export default {
    name: 'Stays',
    data() {
      return {
        stays: [],
        dialog: false,
        stayForm: {
          stay_id: null,
          client_id: null,
          room_id: null,
          check_in_date: '',
          check_out_date: ''
        },
        availableClients: [],
        availableRooms: [],
        headers: [
          { text: 'ID', value: 'stay_id' },
          { text: 'Клиент', value: 'client.last_name' },
          { text: 'Номер', value: 'room.room_id' },
          { text: 'Заезд', value: 'check_in_date' },
          { text: 'Выезд', value: 'check_out_date' },
          { text: 'Действия', value: 'actions', sortable: false }
        ]
      }
    },
    async created() {
      await this.fetchStays()
      await this.fetchClients()
      await this.fetchRooms()
    },
    methods: {
      async fetchStays() {
        const token = localStorage.getItem('token')
        try {
          const response = await axios.get('http://127.0.0.1:8000/api/stays/', {
            headers: { Authorization: `Token ${token}` }
          })
          this.stays = response.data
        } catch (error) {
          console.error(error)
        }
      },
      async fetchClients() {
        const token = localStorage.getItem('token')
        try {
          const response = await axios.get('http://127.0.0.1:8000/api/clients/', {
            headers: { Authorization: `Token ${token}` }
          })
          this.availableClients = response.data
        } catch (error) {
          console.error(error)
        }
      },
      async fetchRooms() {
        const token = localStorage.getItem('token')
        try {
          const response = await axios.get('http://127.0.0.1:8000/api/rooms/', {
            headers: { Authorization: `Token ${token}` }
          })
          this.availableRooms = response.data
        } catch (error) {
          console.error(error)
        }
      },
      openCreateDialog() {
        this.clearForm()
        this.dialog = true
      },
      clearForm() {
        this.stayForm = {
          stay_id: null,
          client_id: null,
          room_id: null,
          check_in_date: '',
          check_out_date: ''
        }
      },
      editStay(stay) {
        // нужно аккуратно извлечь client_id и room_id
        this.stayForm = {
          stay_id: stay.stay_id,
          client_id: stay.client.client_id,
          room_id: stay.room.room_id,
          check_in_date: stay.check_in_date,
          check_out_date: stay.check_out_date
        }
        this.dialog = true
      },
      async createOrUpdateStay() {
        const token = localStorage.getItem('token')
        try {
          if (this.stayForm.stay_id) {
            await axios.put(`http://127.0.0.1:8000/api/stays/${this.stayForm.stay_id}/`, this.stayForm, {
              headers: { Authorization: `Token ${token}` }
            })
          } else {
            await axios.post('http://127.0.0.1:8000/api/stays/', this.stayForm, {
              headers: { Authorization: `Token ${token}` }
            })
          }
          this.dialog = false
          this.fetchStays()
        } catch (error) {
          console.error(error)
        }
      },
      async deleteStay(id) {
        const token = localStorage.getItem('token')
        try {
          await axios.delete(`http://127.0.0.1:8000/api/stays/${id}/`, {
            headers: { Authorization: `Token ${token}` }
          })
          this.fetchStays()
        } catch (error) {
          console.error(error)
        }
      }
    }
  }
  </script>