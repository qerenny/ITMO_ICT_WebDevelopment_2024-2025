<template>
    <v-container class="mt-4">
      <h2>Клиенты</h2>
      <v-text-field
        v-model="searchCity"
        label="Фильтр по городу (city_of_origin)"
        @input="fetchClients"
      ></v-text-field>
  
      <v-data-table
        :headers="headers"
        :items="clients"
        class="elevation-1 mt-4"
      >
        <template #item.actions="{ item }">
          <v-btn small @click="editClient(item)">Ред.</v-btn>
          <v-btn small color="error" @click="deleteClient(item.client_id)">Удалить</v-btn>
        </template>
      </v-data-table>
  
      <v-btn color="primary" class="mt-4" @click="openCreateDialog">Добавить клиента</v-btn>
  
      <!-- Диалог создания/редактирования -->
      <v-dialog v-model="dialog" max-width="600px">
        <v-card>
          <v-card-title>
            {{ clientForm.client_id ? 'Редактирование клиента' : 'Новый клиент' }}
          </v-card-title>
          <v-card-text>
            <v-text-field
              label="Паспорт"
              v-model="clientForm.passport_number"
            ></v-text-field>
            <v-text-field
              label="Фамилия"
              v-model="clientForm.last_name"
            ></v-text-field>
            <v-text-field
              label="Имя"
              v-model="clientForm.first_name"
            ></v-text-field>
            <v-text-field
              label="Отчество"
              v-model="clientForm.middle_name"
            ></v-text-field>
            <v-text-field
              label="Город"
              v-model="clientForm.city_of_origin"
            ></v-text-field>
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" @click="createOrUpdateClient">Сохранить</v-btn>
            <v-btn text @click="dialog = false">Отмена</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-container>
  </template>
  
  <script>
  import axios from 'axios'
  
  export default {
    name: 'Clients',
    data() {
      return {
        clients: [],
        searchCity: '',
        dialog: false,
        clientForm: {
          client_id: null,
          passport_number: '',
          last_name: '',
          first_name: '',
          middle_name: '',
          city_of_origin: ''
        },
        headers: [
          { text: 'ID', value: 'client_id' },
          { text: 'Фамилия', value: 'last_name' },
          { text: 'Имя', value: 'first_name' },
          { text: 'Паспорт', value: 'passport_number' },
          { text: 'Город', value: 'city_of_origin' },
          { text: 'Действия', value: 'actions', sortable: false }
        ]
      }
    },
    async created() {
      await this.fetchClients()
    },
    methods: {
      async fetchClients() {
        try {
          const token = localStorage.getItem('token')
          let url = 'http://127.0.0.1:8000/api/clients/'
          if (this.searchCity) {
            // вариант 1: filterset_fields = ['city_of_origin']
            url += `?city_of_origin=${this.searchCity}`
          }
          // вариант 2: ?search=... (если включён SearchFilter для city_of_origin)
          const response = await axios.get(url, {
            headers: { Authorization: `Token ${token}` }
          })
          this.clients = response.data
        } catch (error) {
          console.error(error)
        }
      },
      openCreateDialog() {
        this.clearForm()
        this.dialog = true
      },
      clearForm() {
        this.clientForm = {
          client_id: null,
          passport_number: '',
          last_name: '',
          first_name: '',
          middle_name: '',
          city_of_origin: ''
        }
      },
      editClient(client) {
        this.clientForm = { ...client }
        this.dialog = true
      },
      async createOrUpdateClient() {
        const token = localStorage.getItem('token')
        try {
          if (this.clientForm.client_id) {
            // update
            await axios.put(`http://127.0.0.1:8000/api/clients/${this.clientForm.client_id}/`, this.clientForm, {
              headers: { Authorization: `Token ${token}` }
            })
          } else {
            // create
            await axios.post('http://127.0.0.1:8000/api/clients/', this.clientForm, {
              headers: { Authorization: `Token ${token}` }
            })
          }
          this.dialog = false
          this.fetchClients()
        } catch (error) {
          console.error(error)
        }
      },
      async deleteClient(clientId) {
        const token = localStorage.getItem('token')
        try {
          await axios.delete(`http://127.0.0.1:8000/api/clients/${clientId}/`, {
            headers: { Authorization: `Token ${token}` }
          })
          this.fetchClients()
        } catch (error) {
          console.error(error)
        }
      }
    }
  }
  </script>