<template>
    <v-container>
      <h2>Уборки (CleaningExecution)</h2>
      <v-data-table :headers="headers" :items="cleanings">
        <template #item.actions="{ item }">
          <v-btn small @click="editCleaning(item)">Ред.</v-btn>
          <v-btn small color="error" @click="deleteCleaning(item.cleaning_execution_id)">Удалить</v-btn>
        </template>
      </v-data-table>
      <v-btn color="primary" class="mt-4" @click="openDialog">Добавить запись</v-btn>
  
      <v-dialog v-model="dialog" max-width="600px">
        <v-card>
          <v-card-title>{{ cleaningForm.cleaning_execution_id ? 'Редактирование' : 'Новая' }} уборка</v-card-title>
          <v-card-text>
            <v-select
              v-model="cleaningForm.staff_id"
              :items="staffList"
              label="Сотрудник"
              :item-text="(s) => s.last_name + ' ' + s.first_name"
              :item-value="(s) => s.staff_id"
            />
            <v-select
              v-model="cleaningForm.room_id"
              :items="roomsList"
              label="Номер"
              :item-text="(r) => 'Room ' + r.room_id"
              :item-value="(r) => r.room_id"
              :return-object="false"
              :allow-empty="true"
            />
            <v-text-field
              v-model="cleaningForm.floor"
              label="Этаж"
              type="number"
            />
            <v-text-field
              v-model="cleaningForm.time_and_day_of_week"
              label="Время и день (например: 'Понедельник 10:00')"
            />
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" @click="createOrUpdateCleaning">Сохранить</v-btn>
            <v-btn text @click="dialog = false">Отмена</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-container>
  </template>
  
  <script>
  import axios from 'axios'
  
  export default {
    name: 'Cleanings',
    data() {
      return {
        cleanings: [],
        dialog: false,
        cleaningForm: {
          cleaning_execution_id: null,
          staff_id: null,
          room_id: null,
          floor: 1,
          time_and_day_of_week: ''
        },
        staffList: [],
        roomsList: [],
        headers: [
          { text: 'ID', value: 'cleaning_execution_id' },
          { text: 'Сотрудник', value: 'staff.last_name' },
          { text: 'Номер', value: 'room.room_id' },
          { text: 'Этаж', value: 'floor' },
          { text: 'День/Время', value: 'time_and_day_of_week' },
          { text: 'Действия', value: 'actions', sortable: false }
        ]
      }
    },
    async created() {
      this.fetchCleanings()
      this.fetchStaff()
      this.fetchRooms()
    },
    methods: {
      async fetchCleanings() {
        const token = localStorage.getItem('token')
        try {
          const res = await axios.get('http://127.0.0.1:8000/api/cleaning-executions/', {
            headers: { Authorization: `Token ${token}` }
          })
          this.cleanings = res.data
        } catch (error) {
          console.error(error)
        }
      },
      async fetchStaff() {
        const token = localStorage.getItem('token')
        try {
          const res = await axios.get('http://127.0.0.1:8000/api/staff/', {
            headers: { Authorization: `Token ${token}` }
          })
          this.staffList = res.data
        } catch (error) {
          console.error(error)
        }
      },
      async fetchRooms() {
        const token = localStorage.getItem('token')
        try {
          const res = await axios.get('http://127.0.0.1:8000/api/rooms/', {
            headers: { Authorization: `Token ${token}` }
          })
          this.roomsList = res.data
        } catch (error) {
          console.error(error)
        }
      },
      openDialog() {
        this.cleaningForm = {
          cleaning_execution_id: null,
          staff_id: null,
          room_id: null,
          floor: 1,
          time_and_day_of_week: ''
        }
        this.dialog = true
      },
      editCleaning(item) {
        this.cleaningForm = {
          cleaning_execution_id: item.cleaning_execution_id,
          staff_id: item.staff.staff_id,
          room_id: item.room ? item.room.room_id : null,
          floor: item.floor,
          time_and_day_of_week: item.time_and_day_of_week
        }
        this.dialog = true
      },
      async createOrUpdateCleaning() {
        const token = localStorage.getItem('token')
        try {
          if (this.cleaningForm.cleaning_execution_id) {
            await axios.put(
              `http://127.0.0.1:8000/api/cleaning-executions/${this.cleaningForm.cleaning_execution_id}/`,
              this.cleaningForm,
              { headers: { Authorization: `Token ${token}` } }
            )
          } else {
            await axios.post(
              `http://127.0.0.1:8000/api/cleaning-executions/`,
              this.cleaningForm,
              { headers: { Authorization: `Token ${token}` } }
            )
          }
          this.dialog = false
          this.fetchCleanings()
        } catch (error) {
          console.error(error)
        }
      },
      async deleteCleaning(id) {
        const token = localStorage.getItem('token')
        try {
          await axios.delete(`http://127.0.0.1:8000/api/cleaning-executions/${id}/`, {
            headers: { Authorization: `Token ${token}` }
          })
          this.fetchCleanings()
        } catch (error) {
          console.error(error)
        }
      }
    }
  }
  </script>