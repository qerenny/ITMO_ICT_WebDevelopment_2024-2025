<template>
  <v-container>
    <h2 class="mb-4">Уборки (CleaningExecution)</h2>

    <!-- staff_cleaned_client_room -->
    <v-card class="mb-4 pa-2 elevated-card">
      <v-card-title class="text-h6">Кто убирал номер клиента в день недели</v-card-title>
      <v-card-text>
        <v-text-field
          v-model="cleaningParams.client_id"
          label="client_id"
          type="number"
          class="mb-2"
        ></v-text-field>
        <v-text-field
          v-model="cleaningParams.day_of_week"
          label="День недели (например, 'понедельник')"
        ></v-text-field>
        <v-btn variant="outlined" color="primary" @click="staffCleanedClientRoom">
          Посмотреть
        </v-btn>
      </v-card-text>
      <v-card-subtitle v-if="cleaningResult.length > 0">
        <div class="mt-2">
          <div
            v-for="st in cleaningResult"
            :key="st.staff_id"
          >
            {{ st.last_name }} {{ st.first_name }} (ID={{ st.staff_id }})
          </div>
        </div>
      </v-card-subtitle>
    </v-card>

    <v-btn
      variant="outlined"
      color="primary"
      class="mb-4"
      @click="openDialog"
    >
      Добавить запись об уборке
    </v-btn>

    <v-row>
      <v-col
        v-for="cleaning in cleanings"
        :key="cleaning.cleaning_execution_id"
        cols="12"
        md="6"
        lg="4"
      >
        <v-card class="elevated-card mb-4 pa-2">
          <v-card-item>
            <div>
              <div class="text-h6">ID: {{ cleaning.cleaning_execution_id }}</div>
              <div class="text-subtitle-2 mb-2">
                Schedule ID: {{ cleaning.cleaning_schedule?.cleaning_schedule_id }}
              </div>
              <div class="text-caption">
                Сотрудник: {{ cleaning.staff?.last_name }} {{ cleaning.staff?.first_name }} <br>
                Комната: {{ cleaning.room?.room_id }} <br>
                Этаж: {{ cleaning.floor }} <br>
                День недели: {{ cleaning.time_and_day_of_week }}
              </div>
            </div>
          </v-card-item>
          <v-card-actions>
            <v-btn
              variant="outlined"
              color="primary"
              @click="editCleaning(cleaning)"
            >
              Редактировать
            </v-btn>
            <v-btn
              variant="outlined"
              color="error"
              @click="deleteCleaning(cleaning.cleaning_execution_id)"
            >
              Удалить
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>


    <!-- Диалог -->
    <v-dialog
      v-model="dialog"
      max-width="600px"
      persistent
    >
      <v-card class="dialog-card pa-6">
        <v-card-title class="text-h5" style="color: #1867C0;">
          {{ cleaningForm.cleaning_execution_id ? 'Редактирование' : 'Новая' }} уборка
        </v-card-title>
        <v-card-text>
          <!-- Обязательное поле cleaning_schedule_id -->
          <v-select
            v-model="cleaningForm.cleaning_schedule_id"
            :items="scheduleList"
            :item-text="(cs) => 'ID ' + cs.cleaning_schedule_id"
            :item-value="(cs) => cs.cleaning_schedule_id"
            label="Cleaning Schedule ID"
          />
          <!-- staff -->
          <v-select
            v-model="cleaningForm.staff_id"
            :items="staffList"
            :item-text="(s) => s.last_name + ' ' + s.first_name"
            :item-value="(s) => s.staff_id"
            label="Сотрудник"
          />
          <!-- room -->
          <v-select
            v-model="cleaningForm.room_id"
            :items="roomsList"
            :item-text="(r) => 'Room ' + r.room_id"
            :item-value="(r) => r.room_id"
            label="Комната"
            :allow-empty="true"
          />
          <v-text-field
            v-model="cleaningForm.floor"
            label="Этаж"
            type="number"
          />
          <v-text-field
            v-model="cleaningForm.time_and_day_of_week"
            label="День/время"
          />
        </v-card-text>
        <v-card-actions>
          <v-btn variant="outlined" color="primary" @click="createOrUpdateCleaning">
            Сохранить
          </v-btn>
          <v-btn variant="outlined" color="error" @click="dialog = false">
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
  name: 'Cleanings',
  data() {
    return {
      cleanings: [],
      dialog: false,
      cleaningForm: {
        cleaning_execution_id: null,
        cleaning_schedule_id: null, // обязательный
        staff_id: null,
        room_id: null,
        floor: 1,
        time_and_day_of_week: ''
      },
      scheduleList: [], // для cleaning_schedule
      staffList: [],
      roomsList: [],


      // для staff_cleaned_client_room
      cleaningParams: {
        client_id: '',
        day_of_week: ''
      },
      cleaningResult: []
    }
  },
  async created() {
    this.fetchCleanings()
    this.fetchStaff()
    this.fetchRooms()
    this.fetchSchedules()
  },
  methods: {
    async fetchCleanings() {
      const token = localStorage.getItem('token')
      try {
        const res = await axios.get(`http://127.0.0.1:8000/api/cleaning-executions/`, {
          headers: { Authorization: `Token ${token}` }
        })
        this.cleanings = res.data.results ? res.data.results : res.data
      } catch (error) {
        console.error(error)
      }
    },
    async fetchSchedules() {
      const token = localStorage.getItem('token')
      try {
        const resp = await axios.get('http://127.0.0.1:8000/api/cleaning-schedules/', {
          headers: { Authorization: `Token ${token}` }        })
        this.scheduleList = resp.data.results ? resp.data.results : resp.data
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
        this.staffList = res.data.results ? res.data.results : res.data
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
        this.roomsList = res.data.results ? res.data.results : res.data
      } catch (error) {
        console.error(error)
      }
    },
    openDialog() {
      this.cleaningForm = {
        cleaning_execution_id: null,
        cleaning_schedule_id: null,
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
        cleaning_schedule_id: item.cleaning_schedule?.cleaning_schedule_id || null,
        staff_id: item.staff?.staff_id || null,
        room_id: item.room?.room_id || null,
        floor: item.floor,
        time_and_day_of_week: item.time_and_day_of_week
      }
      this.dialog = true
    },
    async createOrUpdateCleaning() {
      const token = localStorage.getItem('token')
      try {
        if (this.cleaningForm.cleaning_execution_id) {
          // update
          await axios.put(
            `http://127.0.0.1:8000/api/cleaning-executions/${this.cleaningForm.cleaning_execution_id}/`,
            this.cleaningForm,
            { headers: { Authorization: `Token ${token}` } }
          )
        } else {
          // create
          await axios.post(
            'http://127.0.0.1:8000/api/cleaning-executions/',
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
    },

    // staff_cleaned_client_room
    async staffCleanedClientRoom() {
      const token = localStorage.getItem('token')
      const { client_id, day_of_week } = this.cleaningParams
      if (!client_id || !day_of_week) return
      try {
        const resp = await axios.get(
          `http://127.0.0.1:8000/api/cleaning-executions/staff_cleaned_client_room/?client_id=${client_id}&day_of_week=${day_of_week}`,
          { headers: { Authorization: `Token ${token}` } }
        )
        this.cleaningResult = resp.data
      } catch (error) {
        console.error(error)
      }
    }
  }
}
</script>