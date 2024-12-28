<template>
    <v-container class="mt-4">
      <h2>Сотрудники</h2>
      <v-data-table :headers="headers" :items="staff" class="elevation-1">
        <template #item.actions="{ item }">
          <v-btn small @click="editStaff(item)">Ред.</v-btn>
          <v-btn small color="error" @click="deleteStaff(item.staff_id)">Удалить</v-btn>
        </template>
      </v-data-table>
  
      <v-btn color="primary" class="mt-4" @click="openCreateDialog">Нанять сотрудника</v-btn>
  
      <v-dialog v-model="dialog" max-width="600px">
        <v-card>
          <v-card-title>{{ staffForm.staff_id ? 'Редактирование' : 'Новый' }} сотрудник</v-card-title>
          <v-card-text>
            <v-text-field v-model="staffForm.last_name" label="Фамилия"></v-text-field>
            <v-text-field v-model="staffForm.first_name" label="Имя"></v-text-field>
            <v-text-field v-model="staffForm.middle_name" label="Отчество"></v-text-field>
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" @click="createOrUpdateStaff">Сохранить</v-btn>
            <v-btn text @click="dialog = false">Отмена</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-container>
  </template>
  
  <script>
  import axios from 'axios'
  export default {
    name: 'Staff',
    data() {
      return {
        staff: [],
        dialog: false,
        staffForm: {
          staff_id: null,
          last_name: '',
          first_name: '',
          middle_name: ''
        },
        headers: [
          { text: 'ID', value: 'staff_id' },
          { text: 'Фамилия', value: 'last_name' },
          { text: 'Имя', value: 'first_name' },
          { text: 'Отчество', value: 'middle_name' },
          { text: 'Действия', value: 'actions', sortable: false }
        ]
      }
    },
    async created() {
      await this.fetchStaff()
    },
    methods: {
      async fetchStaff() {
        const token = localStorage.getItem('token')
        try {
          const response = await axios.get('http://127.0.0.1:8000/api/staff/', {
            headers: { Authorization: `Token ${token}` }
          })
          this.staff = response.data
        } catch (error) {
          console.error(error)
        }
      },
      openCreateDialog() {
        this.clearForm()
        this.dialog = true
      },
      clearForm() {
        this.staffForm = {
          staff_id: null,
          last_name: '',
          first_name: '',
          middle_name: ''
        }
      },
      editStaff(item) {
        this.staffForm = { ...item }
        this.dialog = true
      },
      async createOrUpdateStaff() {
        const token = localStorage.getItem('token')
        try {
          if (this.staffForm.staff_id) {
            await axios.put(`http://127.0.0.1:8000/api/staff/${this.staffForm.staff_id}/`, this.staffForm, {
              headers: { Authorization: `Token ${token}` }
            })
          } else {
            await axios.post('http://127.0.0.1:8000/api/staff/', this.staffForm, {
              headers: { Authorization: `Token ${token}` }
            })
          }
          this.dialog = false
          this.fetchStaff()
        } catch (error) {
          console.error(error)
        }
      },
      async deleteStaff(id) {
        const token = localStorage.getItem('token')
        try {
          await axios.delete(`http://127.0.0.1:8000/api/staff/${id}/`, {
            headers: { Authorization: `Token ${token}` }
          })
          this.fetchStaff()
        } catch (error) {
          console.error(error)
        }
      }
    }
  }
  </script>