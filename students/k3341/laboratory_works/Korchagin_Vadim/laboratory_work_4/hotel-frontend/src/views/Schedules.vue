<template>
    <v-container>
      <h2>Расписания уборок (CleaningSchedule)</h2>
      <v-data-table :headers="headers" :items="schedules">
        <template #item.actions="{ item }">
          <v-btn small @click="editSchedule(item)">Ред.</v-btn>
          <v-btn small color="error" @click="deleteSchedule(item.cleaning_schedule_id)">Удалить</v-btn>
        </template>
      </v-data-table>
  
      <v-btn color="primary" class="mt-4" @click="openDialog">Добавить запись</v-btn>
  
      <v-dialog v-model="dialog" max-width="600px">
        <v-card>
          <v-card-title>
            {{ scheduleForm.cleaning_schedule_id ? 'Редактирование' : 'Новое' }} расписание
          </v-card-title>
          <v-card-text>
            <v-select
              v-model="scheduleForm.staff_id"
              :items="staffList"
              label="Сотрудник"
              :item-text="(s) => s.last_name + ' ' + s.first_name"
              :item-value="(s) => s.staff_id"
            />
            <v-select
              v-model="scheduleForm.room_id"
              :items="roomsList"
              label="Номер (необязательно)"
              :item-text="(r) => 'Room ' + r.room_id"
              :item-value="(r) => r.room_id"
              :allow-empty="true"
            />
            <v-text-field
              v-model="scheduleForm.floor"
              label="Этаж"
              type="number"
            />
            <v-text-field
              v-model="scheduleForm.time_and_day_of_week"
              label="День/время"
            />
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" @click="createOrUpdateSchedule">Сохранить</v-btn>
            <v-btn text @click="dialog = false">Отмена</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-container>
  </template>
  
  <script>
  import axios from 'axios'
  
  export default {
    name: 'Schedules',
    data() {
      return {
        schedules: [],
        dialog: false,
        scheduleForm: {
          cleaning_schedule_id: null,
          staff_id: null,
          room_id: null,
          floor: 1,
          time_and_day_of_week: ''
        },
        staffList: [],
        roomsList: [],
        headers: [
          { text: 'ID', value: 'cleaning_schedule_id' },
          { text: 'Сотрудник', value: 'staff.last_name' },
          { text: 'Номер', value: 'room.room_id' },
          { text: 'Этаж', value: 'floor' },
          { text: 'День/Время', value: 'time_and_day_of_week' },
          { text: 'Действия', value: 'actions', sortable: false }
        ]
      }
    },
    async created() {
      await this.fetchSchedules()
      await this.fetchStaff()
      await this.fetchRooms()
    },
    methods: {
      async fetchSchedules() {
        const token = localStorage.getItem('token')
        try {
          const res = await axios.get('http://127.0.0.1:8000/api/cleaning-schedules/', {
            headers: { Authorization: `Token ${token}` }
          })
          this.schedules = res.data
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
        this.scheduleForm = {
          cleaning_schedule_id: null,
          staff_id: null,
          room_id: null,
          floor: 1,
          time_and_day_of_week: ''
        }
        this.dialog = true
      },
      editSchedule(item) {
        this.scheduleForm = {
          cleaning_schedule_id: item.cleaning_schedule_id,
          staff_id: item.staff.staff_id,
          room_id: item.room ? item.room.room_id : null,
          floor: item.floor,
          time_and_day_of_week: item.time_and_day_of_week
        }
        this.dialog = true
      },
      async createOrUpdateSchedule() {
        const token = localStorage.getItem('token')
        try {
          if (this.scheduleForm.cleaning_schedule_id) {
            await axios.put(
              `http://127.0.0.1:8000/api/cleaning-schedules/${this.scheduleForm.cleaning_schedule_id}/`,
              this.scheduleForm,
              { headers: { Authorization: `Token ${token}` } }
            )
          } else {
            await axios.post(
              `http://127.0.0.1:8000/api/cleaning-schedules/`,
              this.scheduleForm,
              { headers: { Authorization: `Token ${token}` } }
            )
          }
          this.dialog = false
          this.fetchSchedules()
        } catch (error) {
          console.error(error)
        }
      },
      async deleteSchedule(id) {
        const token = localStorage.getItem('token')
        try {
          await axios.delete(`http://127.0.0.1:8000/api/cleaning-schedules/${id}/`, {
            headers: { Authorization: `Token ${token}` }
          })
          this.fetchSchedules()
        } catch (error) {
          console.error(error)
        }
      }
    }
  }
  </script>