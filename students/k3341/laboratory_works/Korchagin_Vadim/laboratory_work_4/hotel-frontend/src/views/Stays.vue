<template>
  <v-container>
    <h2 class="mb-4">Проживания</h2>
    <v-btn
      variant="outlined"
      color="primary"
      class="mb-4"
      @click="openCreateDialog"
    >
      Добавить проживание
    </v-btn>

    <v-row>
      <v-col
        v-for="stay in stays"
        :key="stay.stay_id"
        cols="12"
        md="6"
        lg="4"
      >
        <v-card class="mb-4 elevated-card pa-2">
          <v-card-item>
            <div>
              <div class="text-h6">ID: {{ stay.stay_id }}</div>
              <div class="text-subtitle-2 mb-2">
                Клиент: {{ stay.client?.last_name }} {{ stay.client?.first_name }}
                (<strong>ID {{ stay.client?.client_id }}</strong>)
              </div>
              <div class="text-caption">
                Номер: {{ stay.room?.room_id }}  
              </div>
              <div class="mt-2">
                Дата заезда: {{ stay.check_in_date }} <br>
                Дата выезда: {{ stay.check_out_date }}
              </div>
            </div>
          </v-card-item>
          <v-card-actions>
            <v-btn
              variant="outlined"
              color="primary"
              @click="editStay(stay)"
            >
              Редактировать
            </v-btn>
            <v-btn
              variant="outlined"
              color="error"
              @click="deleteStay(stay.stay_id)"
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
        <v-card-title class="my-dialog-title dialog-title">
          {{ stayForm.stay_id ? 'Редактирование проживания' : 'Новое проживание' }}
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
            :item-text="(r) => 'Room ' + r.room_id"
            :item-value="(r) => r.room_id"
          />
          <v-text-field
            v-model="stayForm.check_in_date"
            label="Дата заезда (YYYY-MM-DD)"
          />
          <v-text-field
            v-model="stayForm.check_out_date"
            label="Дата выезда (YYYY-MM-DD)"
          />
        </v-card-text>
        <v-card-actions>
          <v-btn variant="outlined" color="primary" @click="createOrUpdateStay">
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
  name: 'Stays',
  data() {
    return {
      stays: [],
      availableClients: [],
      availableRooms: [],
      dialog: false,
      stayForm: {
        stay_id: null,
        client_id: null,
        room_id: null,
        check_in_date: '',
        check_out_date: ''
      }
    }
  },
  async created() {
    this.fetchStays()
    this.fetchClients()
    this.fetchRooms()
  },
  methods: {
    async fetchStays() {
      const token = localStorage.getItem('token')
      try {
        const res = await axios.get('http://127.0.0.1:8000/api/stays/', {
          headers: { Authorization: `Token ${token}` }
        })
        this.stays = res.data
      } catch (error) {
        console.error(error)
      }
    },
    async fetchClients() {
  const token = localStorage.getItem('token')
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/clients/', {
      headers: { Authorization: `Token ${token}` }
    })
    this.availableClients = res.data.map((client) => ({
      client_id: client.client_id,
      last_name: client.last_name,
      first_name: client.first_name
    }))
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
    this.availableRooms = res.data.map((room) => ({
      room_id: room.room_id,
      phone_number: room.phone_number,
    }))
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
          await axios.put(
            `http://127.0.0.1:8000/api/stays/${this.stayForm.stay_id}/`,
            this.stayForm,
            { headers: { Authorization: `Token ${token}` } }
          )
        } else {
          await axios.post(
            'http://127.0.0.1:8000/api/stays/',
            this.stayForm,
            { headers: { Authorization: `Token ${token}` } }
          )
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